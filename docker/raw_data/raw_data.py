import os
import pandas as pd
from pymongo import MongoClient

def process_mongo_data(data):
    """
    Transforme les données MongoDB pour créer un DataFrame où chaque clé de `Mesure_CNI`
    devient une colonne distincte.
    """
    processed_rows = []

    for record in data:
        # Extraire la date de création
        row = {"date_de_creation": record.get("date_de_creation")}

        # Extraire les mesures et les ajouter comme colonnes
        mesure_cni = record.get("Mesure_CNI", {})
        row.update(mesure_cni)

        # Ajouter la ligne transformée
        processed_rows.append(row)

    # Créer un DataFrame pandas à partir des lignes transformées
    return pd.DataFrame(processed_rows)

def fetch_data_from_mongo(mongo_uri, database_name, collection_name, output_file):
    # Connexion à MongoDB
    client = MongoClient(mongo_uri)
    db = client[database_name]
    collection = db[collection_name]

    # Récupération des données
    print(f"Fetching data from MongoDB collection: {collection_name}...")
    data = list(collection.find())

    # Vérification si des données ont été trouvées
    if not data:
        print("No data found in the collection.")
        return

    # Transformation des données
    print("Processing data...")
    df = process_mongo_data(data)

    # Écriture des données dans un fichier CSV
    print(f"Writing data to {output_file}...")
    df.to_csv(output_file, index=False)
    print(f"Data successfully written to {output_file}.")

if __name__ == "__main__":
    
    # Configurations
    MONGO_URI = os.getenv('MONGO_URI', 'ERROR')
    MONGO_DB = os.getenv('MONGO_DB', 'production')
    MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'api_mesures')
    output_file = os.getenv("OUTPUT_FILE", "/shared_data/raw/raw.csv")

    print(f"MONGO_URI {MONGO_URI}")

    # Exécution de la tâche
    fetch_data_from_mongo(MONGO_URI, MONGO_DB, MONGO_COLLECTION, output_file)
