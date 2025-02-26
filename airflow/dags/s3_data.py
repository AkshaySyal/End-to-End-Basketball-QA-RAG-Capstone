from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import boto3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
KAGGLE_DATASET = "wyattowalsh/basketball"
FILE_NAME = "nba.sqlite"
LOCAL_DIR = "/opt/airflow/data"  # Shared directory inside Docker
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_KEY = f"nba_data/{FILE_NAME}"

# Ensure the directory exists
os.makedirs(LOCAL_DIR, exist_ok=True)

def download_kaggle_dataset():
    """Download the dataset and overwrite if it exists."""
    file_path = os.path.join(LOCAL_DIR, FILE_NAME)
    
    # Remove existing file to ensure overwriting
    if os.path.exists(file_path):
        logger.info(f"Removing existing file: {file_path}")
        os.remove(file_path)

    logger.info(f"Downloading dataset {KAGGLE_DATASET} to {LOCAL_DIR}")
    try:
        os.system(f"kaggle datasets download -d {KAGGLE_DATASET} -p {LOCAL_DIR} --unzip")
        
        # Verify file download
        if os.path.exists(file_path):
            logger.info(f"Dataset downloaded successfully at {file_path}")
        else:
            logger.error(f"Download failed! {file_path} not found.")
    except Exception as e:
        logger.error(f"Error downloading dataset: {e}")


def upload_to_s3():
    """Upload all CSV files from the 'csv' directory to S3."""
    csv_dir = os.path.join(LOCAL_DIR, "csv")  # Path to the CSV folder

    if not os.path.exists(csv_dir):
        raise FileNotFoundError(f"{csv_dir} does not exist. Ensure the Kaggle download step succeeded.")

    logger.info(f"Uploading CSV files from {csv_dir} to S3 bucket {S3_BUCKET_NAME}")

    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

        # Loop through all CSV files and upload them
        for file in os.listdir(csv_dir):
            if file.endswith(".csv"):
                file_path = os.path.join(csv_dir, file)
                s3_key = f"nba_data/csv/{file}"  # S3 folder structure

                logger.info(f"Uploading {file} to {S3_BUCKET_NAME} at {s3_key}")
                s3_client.upload_file(file_path, S3_BUCKET_NAME, s3_key)
        
        logger.info("All CSV files uploaded successfully.")
    except Exception as e:
        logger.error(f"Error uploading CSV files to S3: {e}")


# Default arguments for Airflow
default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 2, 10),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define DAG
dag = DAG(
    "kaggle_to_s3_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
)

# Define tasks
download_task = PythonOperator(
    task_id="download_kaggle_data",
    python_callable=download_kaggle_dataset,
    dag=dag,
)

upload_task = PythonOperator(
    task_id="upload_to_s3",
    python_callable=upload_to_s3,
    dag=dag,
)

# Set task dependencies
download_task >> upload_task
