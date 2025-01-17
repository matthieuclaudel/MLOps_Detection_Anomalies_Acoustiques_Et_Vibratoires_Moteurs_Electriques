import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from kubernetes.client import models as k8s

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    #'retries': 1,
    #'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'train_model_dag',
    default_args=default_args,
    description='DAG pour entraîner un modèle et le pousser dans MLFlow',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

# Définir le volume et le montage de volume
volume = k8s.V1Volume(
    name='data-folder',
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name='data-folder')
)

volume_mount = k8s.V1VolumeMount(
    name='data-folder',
    mount_path='/app/test'
)

# Tâche pour charger les données dans un pod Kubernetes
load_data_task = KubernetesPodOperator(
    task_id='load_data',
    name='load-data',
    namespace='default',
    image='matthieu247/load_data',  # Remplacez par le nom de votre image Docker
    cmds=["python", "app/load_data.py"],
    volume_mounts=[volume_mount],
    volumes=[volume],
    get_logs=True,
    dag=dag,
)    


# Tâche pour entraîner le modèle dans un pod Kubernetes
train_model_task = KubernetesPodOperator(
    task_id='train_model',
    name='train-model',
    namespace='default',
    image='matthieu247/train_accoustic_model',  # Remplacez par le nom de votre image Docker
    cmds=["python", "app/train_model.py"],
    volume_mounts=[volume_mount],
    volumes=[volume],
    get_logs=True,
    dag=dag,
)

# Tâche pour enregistrer le meilleur modèle dans un pod Kubernetes
register_model_task = KubernetesPodOperator(
    task_id='register_model',
    name='register-model',
    namespace='default',
    image='matthieu247/register',  # Remplacez par le nom de votre image Docker
    cmds=["python", "app/register_model.py"],
    env_vars={
        'MLFLOW_TRACKING_URI': os.environ['MLFLOW_TRACKING_URI'],
        'MLFLOW_EXPERIMENT_NAME': os.environ['MLFLOW_EXPERIMENT_NAME'],
        'DAGSHUB_USER': os.environ['DAGSHUB_USER'],
        'DAGSHUB_TOKEN': os.environ['DAGSHUB_TOKEN']
    },
    volume_mounts=[volume_mount],
    volumes=[volume],
    get_logs=True,
    dag=dag,
)

load_data_task >> train_model_task >> register_model_task
