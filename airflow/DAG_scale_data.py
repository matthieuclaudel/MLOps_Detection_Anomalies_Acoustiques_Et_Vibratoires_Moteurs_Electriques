from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime
import os

# Configuration des volumes partagés et des chemins
DATA_DIR = "/shared_data"
INPUT_FILE = os.path.join(DATA_DIR, "input.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "output.csv")

# Définir le DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
}

with DAG(
    "docker_based_etl",
    default_args=default_args,
    description="ETL DAG: MongoDB and InfluxDB to InfluxDB with Docker-based processing",
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # Tâche 1 : Exécuter le conteneur pour extraire les données depuis MongoDB et InfluxDB
    mongo_to_csv_task = DockerOperator(
        task_id="mongo_to_csv",
        image="ludodo/mlops-dst-project-get-from-mongo:latest",
        auto_remove=True,
        volumes=["/shared_data:/shared_data"],
        environment={
            "MONGO_URI": "mongodb://mongodb:27017",
            "MONGO_DB": "production",
            "MONGO_COLLECTION": "api_mesures",
            "INFLUXDB_URL": "http://influxdb:8086",
            "INFLUXDB_TOKEN": os.getenv('INFLUXDB_TOKEN', '1Yrce-Jd5WhAMpQOxL7njYGXw6dYHlPmYGuj0Wq8PwApzXmuagtd-MxVfD5p3jxzLUHzCCWFLxxeCIIogq7G0A=='),
            "INFLUXDB_ORG": "my-org",
            "INFLUXDB_BUCKET": "preprocessed",
            "INPUT_FILE": INPUT_FILE,
        },
        network_mode="bridge",
    )

    # Tâche 2 : Exécuter le conteneur pour transformer les données
    transform_data_task = DockerOperator(
        task_id="transform_data",
        image="ludodo/mlops-dst-project-scaler:latest",
        auto_remove=True,
        volumes=["/shared_data:/shared_data"],
        command=f"--input {INPUT_FILE} --output {OUTPUT_FILE}",
        network_mode="bridge",
    )

    # Tâche 3 : Exécuter le conteneur pour charger les données transformées dans InfluxDB
    load_to_influx_task = DockerOperator(
        task_id="load_to_influx",
        image="ludodo/mlops-dst-project-load-to-influx:latest",  # Remplacez par le nom de l'image Docker
        auto_remove=True,
        volumes=["/shared_data:/shared_data"],
        environment={
            "INFLUXDB_URL": "http://influxdb:8086",
            "INFLUXDB_TOKEN": os.getenv('INFLUXDB_TOKEN', '1Yrce-Jd5WhAMpQOxL7njYGXw6dYHlPmYGuj0Wq8PwApzXmuagtd-MxVfD5p3jxzLUHzCCWFLxxeCIIogq7G0A=='),
            "INFLUXDB_ORG": "my-org",
            "INFLUXDB_BUCKET": "preprocessed",
            "OUTPUT_FILE": OUTPUT_FILE,
        },
        network_mode="bridge",
    )

    # Dépendances
    mongo_to_csv_task >> transform_data_task >> load_to_influx_task
