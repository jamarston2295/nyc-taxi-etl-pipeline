import sys
sys.path.append('/opt/airflow')
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from datetime import timedelta
from scripts.extract import extract
from scripts.transform import transform
from scripts.load import load

with DAG(
    "etl_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    extract_task = PythonOperator(
    task_id="extract",
    python_callable=extract,
    retries=2,
    retry_delay=timedelta(minutes=1)
    )

    transform_task = PythonOperator(
    task_id="transform",
    python_callable=transform,
    retries=2,
    retry_delay=timedelta(minutes=1)
    )

    load_task = PythonOperator(
    task_id="load",
    python_callable=load,
    retries=2,
    retry_delay=timedelta(minutes=1)
    )

    extract_task >> transform_task >> load_task