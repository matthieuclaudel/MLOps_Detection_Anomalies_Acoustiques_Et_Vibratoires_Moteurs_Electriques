import os
import pandas as pd
from pymongo import MongoClient

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

    # Conversion des données en DataFrame pandas
    print("Converting data to pandas DataFrame...")
    df = pd.DataFrame(data)

    # Suppression de l'_id car il n'est pas directement sérialisable en CSV
    if "_id" in df.columns:
        df.drop(columns=["_id"], inplace=True)

    # Écriture des données dans un fichier CSV
    print(f"Writing data to {output_file}...")
    df.to_csv(output_file, index=False)
    print(f"Data successfully written to {output_file}.")

if __name__ == "__main__":
    
    # Configurations
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb:27017')
    MONGO_DB = os.getenv('MONGO_DB', 'production')
    MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'api_mesures')
    output_file = os.getenv("OUTPUT_FILE", "/shared_data/output.csv")

    # Exécution de la tâche
    fetch_data_from_mongo(MONGO_URI, MONGO_DB, MONGO_COLLECTION, output_file)
