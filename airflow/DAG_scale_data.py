from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime
import os
import pandas as pd
import pymongo
from influxdb_client import InfluxDBClient, Point, WritePrecision

# Configuration MongoDB
MONGO_URI = "mongodb://mongodb:27017"
MONGO_DB = "production"
MONGO_COLLECTION = "api_mesures"

# Configuration InfluxDB
INFLUXDB_URL = "http://influxdb:8086"
INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN', 'Token par defaut')
INFLUXDB_ORG = "my-org"
INFLUXDB_BUCKET = "preprocessed"

# Chemins pour les fichiers CSV
DATA_DIR = "/shared_data"  # Répertoire partagé via volume
INPUT_FILE = os.path.join(DATA_DIR, "input.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "output.csv")

# Step 1: Récupération des données brutes de MongoDB et écriture dans input.csv
def extract_data_to_csv(**context):
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]

    # Récupérer les données non encore transformées
    # Assumant qu'il y a un champ `timestamp` dans MongoDB pour filtrer les nouvelles données
    latest_transformed_time = context['ti'].xcom_pull(key='latest_time', task_ids='get_latest_time')
    query = {"timestamp": {"$gt": latest_transformed_time}} if latest_transformed_time else {}
    raw_data = list(collection.find(query))

    # Écriture dans un fichier CSV
    if raw_data:
        df = pd.DataFrame(raw_data)
        df.to_csv(INPUT_FILE, index=False)
        print(f"Les données brutes ont été écrites dans {INPUT_FILE}")
    else:
        print("Aucune nouvelle donnée à transformer.")
    
    client.close()

# Step 0: Récupérer le dernier timestamp des données dans InfluxDB
def get_latest_time_from_influx(**context):
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        query_api = client.query_api()
        query = f'from(bucket: "{INFLUXDB_BUCKET}") |> range(start: 0) |> last()'
        result = query_api.query(query=query)
        if result and len(result) > 0:
            latest_time = result[0].records[0].get_time()
            context['ti'].xcom_push(key='latest_time', value=latest_time)
        else:
            context['ti'].xcom_push(key='latest_time', value=None)

# Step 3: Lecture de output.csv et écriture dans InfluxDB
def load_data_to_influx(**context):
    # Lecture du fichier CSV
    df = pd.read_csv(OUTPUT_FILE)

    # Écriture dans InfluxDB
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=WritePrecision.NS)
        for _, row in df.iterrows():
            point = (
                Point("measurement_name")
                .field("value", row["value_column"])  # Remplacez par le nom de votre colonne
                .time(row["timestamp"])  # Assurez-vous que le champ timestamp existe
            )
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

# Définition du DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
}

with DAG(
    "mongo_to_influx_with_scaler",
    default_args=default_args,
    description="ETL DAG: MongoDB to InfluxDB with data transformation using a Docker container",
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # Tâche 1 : Récupérer le dernier timestamp des données dans InfluxDB
    get_latest_time_task = PythonOperator(
        task_id="get_latest_time",
        python_callable=get_latest_time_from_influx,
    )

    # Tâche 2 : Extraire les données brutes de MongoDB et écrire dans input.csv
    extract_data_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data_to_csv,
        provide_context=True,
    )

    # Tâche 3 : Exécuter le conteneur Docker pour transformer les données
    transform_data_task = DockerOperator(
        task_id="transform_data",
        image="ludodo/mlops-dst-project-scaler:latest",
        container_name="scaler_container",
        auto_remove=True,
        volumes=["/shared_data:/shared_data"],
        command=f"--input {INPUT_FILE} --output {OUTPUT_FILE}",
        network_mode="bridge",
    )

    # Tâche 4 : Charger les données transformées dans InfluxDB
    load_data_task = PythonOperator(
        task_id="load_data",
        python_callable=load_data_to_influx,
    )

    # Dépendances
    get_latest_time_task >> extract_data_task >> transform_data_task >> load_data_task
