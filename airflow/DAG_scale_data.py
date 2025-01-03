from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pymongo
import pickle
import pandas as pd
import dagshub
import mlflow
from influxdb_client import InfluxDBClient, Point, WritePrecision

# DAGSUB
DAGSHUB_USER_TOKEN = os.getenv('DAGSHUB_USER_TOKEN', 'Token par défaut')

# MongoDB Configuration
MONGO_URI = "mongodb://mongodb:27017"
MONGO_DB = "db_raw"
MONGO_COLLECTION = "measurements"

# InfluxDB Configuration
INFLUXDB_URL = "http://influxdb:8086"
INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN', 'Token par defaut')
INFLUXDB_ORG = ""
INFLUXDB_BUCKET = "preprocessed"

# Load StandardScaler
def load_scaler(name="StandardScaler"):
    # Connexion au dépôt DagsHub et récupération du modèle
    dagshub.auth.add_app_token(token=DAGSHUB_USER_TOKEN )
    dagshub.init(repo_owner='crotelius77', repo_name='MLOps_Detection_Anomalies_Acoustiques_Et_Vibratoires_Moteurs_Electriques', mlflow=True)
    # create a client to access the MLflow tracking server
    client = mlflow.MlflowClient()
    for model in client.search_registered_models(filter_string="name LIKE '%'"):
        for model_version in model.latest_versions:
            print(f"name={model_version.name}; run_id={model_version.run_id}; version={model_version.version}, stage={model_version.current_stage}")   
    # Get the latest version for the model
    version = client.get_latest_versions(name=name)[0].version

    # Construct the model URI
    model_uri = f'models:/{name}/{version}'
    # Charge le modèle depuis le fichier Pickle ou le télécharge depuis MLflow si nécessaire.
    if not os.path.exists(f"models/{name}/{version}.pkl"):
        print(f"Modèle non trouvé à {model_uri}. Téléchargement depuis DagsHubs-MLflow...")
        # Load the model
        model = mlflow.sklearn.load_model(model_uri)
        os.makedirs(os.path.dirname(f"models/{name}/{version}.pkl)"))
        with open(f"models/{name}/{version}.pkl", "wb") as f:
            pickle.dump(model, f)
        print("Modèle téléchargé et sauvegardé en Pickle.")
    else:
        print(f"Chargement du modèle depuis {model_uri}...")
        with open(f"models/{name}/{version}.pkl", "rb") as f:
            model = pickle.load(f)
    return model

# Step 1: Extract Data from MongoDB
def extract_data(**context):
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    data = list(collection.find())
    df = pd.DataFrame(data)
    context['ti'].xcom_push(key='raw_data', value=df.to_dict())
    client.close()

# Step 2: Transform Data using StandardScaler
def transform_data(**context):
    raw_data = context['ti'].xcom_pull(key='raw_data', task_ids='extract_data')
    df = pd.DataFrame(raw_data)
    df = df.drop(['_id', 'target', 'index'], axis=1)
    scaler = load_scaler()
    scaled_data = scaler.transform(df.select_dtypes(include='number'))
    df[df.select_dtypes(include='number').columns] = scaled_data
    context['ti'].xcom_push(key='transformed_data', value=df.to_dict())

# Step 3: Load Data into InfluxDB
def load_data(**context):
    transformed_data = context['ti'].xcom_pull(key='transformed_data', task_ids='transform_data')
    df = pd.DataFrame(transformed_data)

    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=WritePrecision.NS)
        for _, row in df.iterrows():
            point = Point("measurement_name").field("value", row['value_column'])
            write_api.write(INFLUXDB_BUCKET, INFLUXDB_ORG, point)

# Define the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

with DAG(
    'mongo_to_influx',
    default_args=default_args,
    description='ETL DAG for MongoDB to InfluxDB',
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    extract_data_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    transform_data_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
    )

    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )

    extract_data_task >> transform_data_task >> load_data_task
