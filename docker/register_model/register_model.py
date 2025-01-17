import os
import pickle
import mlflow
from mlflow.tracking import MlflowClient
import dagshub

# Connecter MLflow et Dagshub
def connect_to_mlflow_and_dagshub():
    dagshub.auth.add_app_token(token=os.environ['DAGSHUB_TOKEN'])
    dagshub.init(repo_owner=os.environ['DAGSHUB_USER'], repo_name='MLOps_Detection_Anomalies_Acoustiques_Et_Vibratoires_Moteurs_Electriques', mlflow=True)
    mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])
    mlflow.set_experiment(os.environ['MLFLOW_EXPERIMENT_NAME'])
    mlflow.start_run(run_name='register_model')
    mlflow.autolog(disable=True)
    print('connected to Dagshub')
    client = MlflowClient(tracking_uri=os.environ['MLFLOW_TRACKING_URI'])
    return client

# Enregistrer le modèle dans MLflow
def register_model():
    connect_to_mlflow_and_dagshub()
    with open('/app/test/best_model.pkl', 'rb') as f:
        best_model = pickle.load(f)
    with open('/app/test/best_score.pkl', 'rb') as f:
        metrics = pickle.load(f)
    with open('/app/test/model_params.pkl', 'rb') as f:
        params = pickle.load(f)  
    
    mlflow.sklearn.log_model(best_model, "model")
    
    for metric_name, metric_value in metrics.items():
        mlflow.log_metric(metric_name, metric_value)
        
    for param_name, param_value in params.items():
        mlflow.log_param(param_name, param_value) 
        
    mlflow.end_run()
    print('model registered')

if __name__ == "__main__":
    register_model()