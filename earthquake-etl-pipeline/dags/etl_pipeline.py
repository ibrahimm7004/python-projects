from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
}

with DAG(
    dag_id='earthquake_etl_pipeline',
    default_args=default_args,
    schedule_interval=None,  # Manual trigger
    catchup=False,
    description='ETL pipeline for Earthquake data using PySpark',
) as dag:

    download_data = BashOperator(
        task_id='download_data',
        bash_command='''bash /opt/airflow/scripts/download_data.sh''',
        dag=dag,
    )

    transform_data = BashOperator(
        task_id='transform_data',
        bash_command='''python /opt/airflow/scripts/transform_data.py''',
        dag=dag,
    )

    store_data = BashOperator(
        task_id='store_data',
        bash_command='''python /opt/airflow/scripts/store_data.py''',
        dag=dag,
    )

    download_data >> transform_data >> store_data
