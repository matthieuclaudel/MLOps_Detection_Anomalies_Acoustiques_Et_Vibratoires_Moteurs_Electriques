import os
import pandas as pd
from pymongo import MongoClient
from influxdb_client import InfluxDBClient

# Configurations
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb:27017')
MONGO_DB = os.getenv('MONGO_DB', 'production')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'api_mesures')

INFLUXDB_URL = os.getenv('INFLUXDB_URL', 'http://influxdb:8086')
INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN', '1Yrce-Jd5WhAMpQOxL7njYGXw6dYHlPmYGuj0Wq8PwApzXmuagtd-MxVfD5p3jxzLUHzCCWFLx
xeCIIogq7G0A==')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG', 'my-org')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET', 'preprocessed')

INPUT_FILE = os.getenv('INPUT_FILE', '/shared_data/input.csv')

# Étape 1 : Récupérer le dernier timestamp depuis InfluxDB
def get_latest_time_from_influx():
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        query_api = client.query_api()
        query = f'from(bucket: "{INFLUXDB_BUCKET}") |> range(start: 0) |> last()'
        result = query_api.query(query=query)

        if result and len(result) > 0:
            latest_time = result[0].records[0].get_time()
            print(f"Dernier timestamp récupéré depuis InfluxDB : {latest_time}")
            return latest_time
        else:
            print("Aucun timestamp trouvé dans InfluxDB.")
            return None

# Étape 2 : Extraire les données brutes de MongoDB
def extract_data_to_csv(latest_time):
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]

    # Préparer la requête pour MongoDB
    query = {"timestamp": {"$gt": latest_time}} if latest_time else {}
    raw_data = list(collection.find(query))

    # Écrire les données dans un fichier CSV
    if raw_data:
        df = pd.DataFrame(raw_data)
        df.to_csv(INPUT_FILE, index=False)
        print(f"Les données brutes ont été écrites dans {INPUT_FILE}")
    else:
        print("Aucune nouvelle donnée à transformer.")
    client.close()

# Main : Appeler les deux étapes
if __name__ == "__main__":
    latest_time = get_latest_time_from_influx()
    extract_data_to_csv(latest_time)