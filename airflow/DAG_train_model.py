from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from influxdb import InfluxDBClient
import mlflow
import mlflow.sklearn
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import f1_score
import numpy as np
import os
import dagshub
import mlflow
from mlflow import MlflowClient

# Configuration du DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'train_model_dag',
    default_args=default_args,
    description='DAG pour entraîner un modèle et le pousser dans MLFlow',
    schedule_interval=timedelta(days=1),
)

# Fonction pour récupérer les données depuis InfluxDB
#def fetch_data_from_influxdb():
#    client = InfluxDBClient(host='localhost', port=8086, database='mydb')
#    query = 'SELECT * FROM my_measurement'
#    result = client.query(query)
#    points = list(result.get_points())
#    data = np.array([[point['field1'], point['field2']] for point in points])
#    return data

# Fonction pour se connecter à MLFlox et DagsHub
def connect_to_mlflow_and_dagshub():
    #mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])
    #mlflow.set_experiment(os.environ['MLFLOW_EXPERIMENT_NAME'])
    #mlflow.start_run(run_name='train_model')
    dagshub.init(repo_owner='crotelius77', repo_name='MLOps_Detection_Anomalies_Acoustiques_Et_Vibratoires_Moteurs_Electriques', mlflow=True)
    client = MlflowClient(tracking_uri='https://dagshub.com/crotelius77/MLOps_Detection_Anomalies_Acoustiques_Et_Vibratoires_Moteurs_Electriques.mlflow')
    matt_experiment = mlflow.set_experiment("models")
    mlflow.autolog(disable=True)
    return client, matt_experiment
    #os.system(f"dvc pull {os.environ['DAGSHUB_REPO']}")
    #os.system(f"dvc repro {os.environ['DAGSHUB_DVC_FILE']}")

# Fonction pour charger les données train depuis le github local
def load_data_train_from_github():
    data_train = pd.read_csv('https://raw.githubusercontent.com/crotelius77/MLOps_Detection_Anomalies_Acoustiques_Et_Vibratoires_Moteurs_Electriques/main/raw/DATASET_SCALED.zip', sep=';', decimal=',')
    return data_train

# Fonction pour charger les données test depuis le github local
def load_data_test_from_github():
    data_test = pd.read_csv('https://raw.githubusercontent.com/crotelius77/MLOps_Detection_Anomalies_Acoustiques_Et_Vibratoires_Moteurs_Electriques/main/raw/DATASET_VALIDATION_SCALED.csv', sep=';', decimal=',')
    return data_test

# Fonction pour entraîner et évaluer les modèles
def train_and_evaluate_model():
    #data = fetch_data_from_influxdb()
    X_train = load_data_train_from_github()
    data_test = load_data_test_from_github()
    X_test = data_test.drop(columns=['target'])
    y_test = data_test['target']
    #client, matt_experiment = connect_to_mlflow_and_dagshub()
    
    # Entraînement du modèle
    best_model = None
    best_score = -np.inf
    
    cont = ['auto',0.01,0.05,0.1,0.25,0.5]
    neig = [2,5,10,20,30]
    met = ["cityblock","minkowski"]

    for m in met:
        for n in neig:
            for c in cont:
                model = LocalOutlierFactor(novelty=True,n_neighbors=n,contamination=c,metric=m,n_jobs=-1)
                model.fit(X_train)
                y_pred = model.predict(X_test)
                y_pred[y_pred == 1] = 0
                y_pred[y_pred == -1] = 1
                
                score = f1_score(y_test, y_pred)
                if score > best_score:
                    best_score = score
                    best_model = model
    
    mlflow.sklearn.log_model(best_model, "best_model")
    mlflow.log_metric("best_score", best_score)

#Tâches Airflow
connect_task = PythonOperator(
    task_id='connect_MLFlow_and_DagsHub',
    python_callable=connect_to_mlflow_and_dagshub,
    dag=dag,
)

load_task_1 = PythonOperator(
    task_id='load_data_train_from_github',
    python_callable=load_data_train_from_github,
    dag=dag,
)

load_task_2 = PythonOperator(
    task_id='load_data_test_from_github',
    python_callable=load_data_test_from_github,
    dag=dag,
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_and_evaluate_model,
    dag=dag,
)

# Dépendances des tâches
connect_task >> [load_task_1,load_task_2] >> train_model_task