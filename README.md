# ETL Airflow Google Books

A data pipeline project that extracts book information from the **Google Books API**, transforms it, and loads it into a structured format using **Apache Airflow**.

## ETL Pipeline Overview

This project demonstrates an automated ETL workflow using Airflow to streamline the process of extracting, transforming, and loading book data from the Google Books API. The pipeline performs the following steps:

1. **Extract** book data from the Google Books API.
2. **Transform** the data into a clean, consistent, and structured format.
3. **Load** the processed data into a database or storage system for further analysis.
The workflow is designed to be modular, efficient, and maintainable, ensuring:
  - Reliable extraction from external sources.
  - Robust transformation with validation and data cleansing.
  - Seamless loading into target systems for analytics or reporting.

***The ETL pipeline workflow is illustrated below:***
![ETL_Pipeline_Workflow.png](output/ETL_Pipeline_Workflow.png)

## Installation

1. **Clone the repository**  
    ```bash
    git clone https://github.com/Dhivakar2005/etl-airflow-google-books.git
    cd etl-airflow-google-books

2. Create a virtual environment
    ```bash
    python -m venv venv
    venv\Scripts\activate
    
3. Running with Docker Compose

    You can run this Airflow ETL project using Docker Compose for an isolated and reproducible environment.  
    For detailed instructions on setting up Airflow with Docker Compose, refer to the official guide: [Apache Airflow Docker Compose](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)

4. To install PostgreSQL(pgadmin):
   Code to add in `docker-compose.yaml` file
   ```bash
    # PostgreSQL service
    postgres:
      image: postgres:16
      environment:
        POSTGRES_USER: airflow
        POSTGRES_PASSWORD: airflow
        POSTGRES_DB: airflow
      volumes:
        - postgres-db-volume:/var/lib/postgresql/data
      healthcheck:
        test: ["CMD", "pg_isready", "-U", "airflow"]
        interval: 10s
        retries: 5
        start_period: 5s
      restart: always
      ports:
        - "5432:5432"

    # pgAdmin service
    pgadmin:
      container_name: pgadmin4_container2
      image: dpage/pgadmin4
      restart: always
      environment:
        PGADMIN_DEFAULT_EMAIL: admin@admin.com
        PGADMIN_DEFAULT_PASSWORD: root
      ports:
        - "5050:80"

      
5. Access PostgreSQL and PostgreSQL 

After starting the Docker containers or running Airflow locally, open your browser and go to:  
    - Airflow: http://localhost:8080
    - PostgreSQL: http://localhost:5050
  

## Features

- Automated ETL workflow using **Apache Airflow DAGs**  
- Fetches book data from the **Google Books API**  
- Data cleaning and transformation  
- Configurable storage options (database, CSV, or cloud)  
- Easy to extend for additional APIs or datasets  

## Tech Stack

- **Python 3.x**  
- **Apache Airflow**  
- **Google Books API**

## Output

**Airflow:**  
![Airflow](/output/airflow.png)

**PostgreSQL (pgAdmin):**  
![PG Admin](/output/pg.png)

**Extracted Data:**  
You can view the extracted data in [`output/data-1765824853797.csv`](output/data-1765824853797.csv).

## Future Work

- **Load data into a cloud database** (e.g., PostgreSQL, BigQuery) for easier access and analytics  
- **Add more APIs** to enrich the dataset, like Goodreads or Open Library  
- **Automate incremental updates** so the pipeline only fetches new or updated books  
- **Add data validation and monitoring** using Airflow sensors or external tools  
- **Create dashboards** for visualizing book trends using tools like Tableau, Power BI, or Apache Superset  
- **Dockerize the entire project** with Airflow, database, and storage for production-ready deployment  

## Contributing

Contributions are welcome! Feel free to fork the repo and suggest improvements.


## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
