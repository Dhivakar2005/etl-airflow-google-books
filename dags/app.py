from datetime import datetime, timedelta
from airflow import DAG
import requests
import logging

from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Constants
POSTGRES_CONN_ID = "book_connection"
GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes"

# Extract task
def fetch_book_data(num_books: int):
    params = {
        "q": "data engineering",
        "maxResults": min(num_books, 40),  # API limit is 40
    }

    response = requests.get(GOOGLE_BOOKS_API, params=params, timeout=30)

    if response.status_code != 200:
        raise ValueError("Failed to fetch data from Google Books API")

    data = response.json()
    items = data.get("items", [])

    if not items:
        raise ValueError("No books returned from Google Books API")

    books = []

    for item in items:
        volume = item.get("volumeInfo", {})

        books.append(
            {
                "title": volume.get("title"),
                "authors": ", ".join(volume.get("authors", [])),
                "price": None,  # Google Books may not provide price
                "rating": volume.get("averageRating"),
            }
        )

    logging.info(f"Fetched {len(books)} books from Google Books API")
    return books[:num_books]

# Load task
def insert_book_data_into_postgres(ti):
    book_data = ti.xcom_pull(task_ids="fetch_book_data")

    if not book_data:
        raise ValueError("No book data found in XCom")

    postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

    rows = [
        (
            book["title"],
            book["authors"],
            book["price"],
            book["rating"],
        )
        for book in book_data
    ]

    postgres_hook.insert_rows(
        table="books",
        rows=rows,
        target_fields=["title", "authors", "price", "rating"],
        commit_every=100,
    )

# DAG definition
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 6, 20),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="fetch_and_store_books_google_api",
    default_args=default_args,
    description="Fetch book data from Google Books API and store it in Postgres",
    schedule=timedelta(days=1),
    catchup=False,
    tags=["etl", "books", "google-api"],
) as dag:

    fetch_book_data = PythonOperator(
        task_id="fetch_book_data",
        python_callable=fetch_book_data,
        op_kwargs={"num_books": 50},
    )

    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id=POSTGRES_CONN_ID,
        sql="""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                authors TEXT,
                price TEXT,
                rating TEXT
            );
        """,
    )

    insert_book_data = PythonOperator(
        task_id="insert_book_data",
        python_callable=insert_book_data_into_postgres,
    )

    fetch_book_data >> create_table >> insert_book_data
