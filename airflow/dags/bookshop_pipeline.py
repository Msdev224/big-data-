from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook


PROJECT_ROOT = Path("/opt/airflow/project")
DBT_PROJECT_DIR = PROJECT_ROOT / "app" / "dbt_bookshop"
SNOWFLAKE_SQL_DIR = PROJECT_ROOT / "sql" / "snowflake"
DBT_PROFILES_FILE = DBT_PROJECT_DIR / "profiles.yml"
DBT_PROFILES_EXAMPLE_FILE = DBT_PROJECT_DIR / "profiles.yml.example"


RAW_TABLES = {
    "CATEGORY": ["ID", "CODE", "INTITULE"],
    "BOOKS": ["ID", "CATEGORY_ID", "CODE", "INTITULE", "ISBN_10", "ISBN_13", "PRIX_CATALOGUE"],
    "CUSTOMERS": ["ID", "CODE", "FIRST_NAME", "LAST_NAME", "EMAIL", "CITY", "COUNTRY"],
    "FACTURES": ["ID", "CUSTOMER_ID", "CODE", "QTE_TOTALE", "TOTAL_AMOUNT", "TOTAL_PAID", "DATE_EDIT"],
    "VENTES": ["ID", "FACTURE_ID", "BOOK_ID", "PU", "QTE", "DATE_EDIT"],
}


def _run_snowflake_sql_file(file_name: str) -> None:
    sql_path = SNOWFLAKE_SQL_DIR / file_name
    logger.info("Executing Snowflake SQL file: %s", sql_path)
    sql = sql_path.read_text(encoding="utf-8")
    hook = SnowflakeHook(snowflake_conn_id="snowflake_bookshop")
    hook.run(sql)
    logger.info("Completed Snowflake SQL file: %s", file_name)


def create_bookshop_structures() -> None:
    """Create the BOOKSHOP database, schemas and RAW tables in Snowflake."""
    _run_snowflake_sql_file("01_setup_bookshop.sql")
    _run_snowflake_sql_file("02_raw_tables.sql")


def _truncate_raw_tables(hook: SnowflakeHook) -> None:
    statements = [f"truncate table if exists BOOKSHOP.RAW.{table};" for table in RAW_TABLES]
    hook.run("\n".join(statements))


def ingest_postgres_to_snowflake() -> None:
    """Copy all RAW tables from PostgreSQL source into Snowflake BOOKSHOP.RAW."""
    postgres = PostgresHook(postgres_conn_id="postgres_bookshop")
    snowflake = SnowflakeHook(snowflake_conn_id="snowflake_bookshop")

    _truncate_raw_tables(snowflake)

    pg_conn = postgres.get_conn()
    sf_conn = snowflake.get_conn()

    try:
        for table_name, columns in RAW_TABLES.items():
            query = f"select {', '.join(column.lower() for column in columns)} from {table_name.lower()};"
            with pg_conn.cursor() as pg_cursor:
                pg_cursor.execute(query)
                rows = pg_cursor.fetchall()

            logger.info("Fetched %s rows from Postgres table %s", len(rows), table_name)

            if not rows:
                logger.warning("Skipping empty table %s", table_name)
                continue

            placeholders = ", ".join(["%s"] * len(columns))
            insert_sql = (
                f"insert into BOOKSHOP.RAW.{table_name} ({', '.join(columns)}) "
                f"values ({placeholders})"
            )
            with sf_conn.cursor() as sf_cursor:
                sf_cursor.executemany(insert_sql, rows)
            logger.info("Inserted %s rows into Snowflake BOOKSHOP.RAW.%s", len(rows), table_name)

        sf_conn.commit()
        logger.info("Snowflake ingestion committed successfully")
    finally:
        pg_conn.close()
        sf_conn.close()


def ensure_dbt_profile() -> None:
    # Airflow mounts the repo at runtime, so create the working dbt profile if needed.
    if DBT_PROFILES_FILE.exists():
        logger.info("dbt profile already present at %s", DBT_PROFILES_FILE)
        return
    logger.info("Creating dbt profile from example at %s", DBT_PROFILES_EXAMPLE_FILE)
    DBT_PROFILES_FILE.write_text(DBT_PROFILES_EXAMPLE_FILE.read_text(encoding="utf-8"), encoding="utf-8")


default_args = {
    "owner": "codex",
    "depends_on_past": False,
}


with DAG(
    dag_id="bookshop_pipeline",
    description="Pipeline Big Data Bookshop: ingestion PostgreSQL -> Snowflake -> dbt",
    start_date=datetime(2025, 3, 11),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["bookshop", "bigdata", "snowflake", "dbt"],
) as dag:
    create_structures = PythonOperator(
        task_id="create_bookshop_structures",
        python_callable=create_bookshop_structures,
    )

    load_raw = PythonOperator(
        task_id="ingest_postgres_to_snowflake",
        python_callable=ingest_postgres_to_snowflake,
    )

    prepare_dbt_profile = PythonOperator(
        task_id="ensure_dbt_profile",
        python_callable=ensure_dbt_profile,
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            f"cd {DBT_PROJECT_DIR} && dbt build --profiles-dir ."
        ),
        env={
            **os.environ,
            "SNOWFLAKE_ACCOUNT": os.environ.get("SNOWFLAKE_ACCOUNT", ""),
            "SNOWFLAKE_USER": os.environ.get("SNOWFLAKE_USER", ""),
            "SNOWFLAKE_PASSWORD": os.environ.get("SNOWFLAKE_PASSWORD", ""),
            "SNOWFLAKE_ROLE": os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
            "SNOWFLAKE_WAREHOUSE": os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
            "SNOWFLAKE_DATABASE": os.environ.get("SNOWFLAKE_DATABASE", "BOOKSHOP"),
            "SNOWFLAKE_SCHEMA": os.environ.get("SNOWFLAKE_SCHEMA", "RAW"),
        },
    )

    create_structures >> load_raw >> prepare_dbt_profile >> dbt_build
