from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime
import os


# Définition du DAG

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'train_model_dag',
    default_args=default_args,
    description='DAG pour entraîner un modèle et le pousser dans MLFlow',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:
    
    # Tâche : Exécuter le conteneur pour récupérer les données influxDB, entrainer un modèle et le pousser dans MLFlow
    train_model_from_influxdB = DockerOperator(
        task_id="model_training",
        image="",  # Remplacez par le nom de l'image Docker
        auto_remove=True,
        volumes=["/shared_data:/shared_data"],
        environment={
            "INFLUXDB_URL": "http://influxdb:8086",
            "INFLUXDB_TOKEN": os.getenv('INFLUXDB_TOKEN', '1Yrce-Jd5WhAMpQOxL7njYGXw6dYHlPmYGuj0Wq8PwApzXmuagtd-MxVfD5p3jxzLUHzCCWFLxxeCIIogq7G0A=='),
            "INFLUXDB_ORG": "my-org",
            "INFLUXDB_BUCKET": "preprocessed",
            "MLFLOW_URI": "https://dagshub.com/crotelius77/MLOps_Detection_Anomalies_Acoustiques_Et_Vibratoires_Moteurs_Electriques.mlflow",
        },
        network_mode="bridge",
    )

    # Dépendances
    train_model_from_influxdB
