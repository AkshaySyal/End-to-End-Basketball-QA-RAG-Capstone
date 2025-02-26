from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime
import sqlite3
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SQLITE_DB_PATH = "/opt/airflow/data/nba.sqlite"  # Ensure consistent path

def query_sqlite():
    """Query the SQLite database and log table names."""
    logger.info(f"Connecting to SQLite database at {SQLITE_DB_PATH}")
    if not os.path.exists(SQLITE_DB_PATH):
        raise FileNotFoundError(f"{SQLITE_DB_PATH} does not exist. Ensure the Kaggle download step succeeded.")

    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        logger.info(f"Tables found in SQLite database: {tables}")
        conn.close()
    except Exception as e:
        logger.error(f"Error querying SQLite: {e}")

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 2, 10),
}

dag = DAG(
    "read_sqlite",
    default_args=default_args,
    schedule_interval=None,  # Do not run automatically
    catchup=False,
)

read_task = PythonOperator(
    task_id="read_sqlite_data",
    python_callable=query_sqlite,
    dag=dag,
)
