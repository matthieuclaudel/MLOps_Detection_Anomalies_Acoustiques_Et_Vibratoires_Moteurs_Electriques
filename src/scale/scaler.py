import argparse
import pandas as pd
import dagshub
import mlflow
import os
import pickle


DAGSHUB_USER_TOKEN = os.getenv('DAGSHUB_USER_TOKEN', 'Token par défaut')

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

def transform_data(input_path, output_path):
    # Charger les données depuis le fichier CSV
    df = pd.read_csv(input_path, sep=';', decimal=',').drop(['moyenne', 'ecartype', 'mediane', 'min', 'max', 'target'], axis=1)

    # Assurez-vous que seules les colonnes numériques sont normalisées
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    scaler = load_scaler()
    scaled_data = scaler.transform(df[numeric_columns])

    # Remplacez les données dans le DataFrame
    df[numeric_columns] = scaled_data

    # Sauvegarder les données transformées dans un nouveau fichier CSV
    df.to_csv(output_path, index=False)
    print(f"Les données transformées ont été enregistrées dans {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform CSV data using StandardScaler")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--output", required=True, help="Path to output CSV file")
    args = parser.parse_args()

    transform_data(args.input, args.output)