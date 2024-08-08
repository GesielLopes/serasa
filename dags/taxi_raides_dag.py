import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from src.producer import produce_events
from src.consumer import consume_events
from src.consolidate import consolidate_data

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 12, 25),
    'retries': 1,
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('taxi_fare_pipeline', default_args=default_args, schedule_interval='@daily') as dag:

    start_producer = PythonOperator(
        task_id='start_producer',
        python_callable=produce_events,
    )

    start_consumer = PythonOperator(
        task_id='start_consumer',
        python_callable=consume_events,
    )

    start_consolidate = PythonOperator(
        task_id='start_consolidate',
        python_callable=consolidate_data,
    )

    start_producer >> start_consumer >> start_consolidate