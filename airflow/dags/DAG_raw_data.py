from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as k8s
from datetime import datetime
import os

# Configuration des volumes partagés et des chemins
SHARED_DATA_PATH = "/shared_data"
OUTPUT_FILE = f"{SHARED_DATA_PATH}/output.csv"

# Volume partagé entre les pods
shared_volume = k8s.V1Volume(
    name='data-folder',
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name='data-folder')
)

shared_volume_mount = k8s.V1VolumeMount(
    name='data-folder',
    mount_path=SHARED_DATA_PATH,
)

# Définir le DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
}

with DAG(
    "mongo_to_csv",
    default_args=default_args,
    description="Read from MongoDB and write to CSV in a shared volume",
    schedule_interval="0 8,14,22 * * *",  # tous les jours à 8h, 14, 22h
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # Tâche : Lire les données depuis MongoDB et écrire dans un fichier CSV
    mongo_to_csv_task = KubernetesPodOperator(
        task_id="mongo_to_csv",
        name="mongo-to-csv",
        namespace="default",
        image="ludodo/mlops-dst-project-get-from-mongo:latest",
        env_vars={
            "OUTPUT_FILE": OUTPUT_FILE,
        },
        secrets=[
            k8s.V1EnvVar(
                name="MONGO_URI",
                value_from=k8s.V1EnvVarSource(
                    secret_key_ref=k8s.V1SecretKeySelector(
                        name="mongodbconnect-secret",
                        key="mongodburi",
                    )
                )
            )
        ],
        volumes=[shared_volume],
        volume_mounts=[shared_volume_mount],
        get_logs=True,
    )
