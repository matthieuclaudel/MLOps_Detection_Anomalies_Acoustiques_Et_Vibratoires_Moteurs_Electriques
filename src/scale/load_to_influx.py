import os
import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision

# Configurations
INFLUXDB_URL = os.getenv('INFLUXDB_URL', 'http://my-influxdb2.default.svc.cluster.local:80')
INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN', '1Yrce-Jd5WhAMpQOxL7njYGXw6dYHlPmYGuj0Wq8PwApzXmuagtd-MxVfD5p3jxzLUHzCCWFLxxeCIIogq7G0A==')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG', 'my-org')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET', 'preprocessed')
OUTPUT_FILE = os.getenv('OUTPUT_FILE', '/shared_data/output.csv')

# Lecture et chargement des données
def load_to_influx():
    df = pd.read_csv(OUTPUT_FILE)
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=WritePrecision.NS)
        for _, row in df.iterrows():
            point = Point("measurement_name").field("value", row["value_column"]).time(row["timestamp"])
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        print(f"Les données de {OUTPUT_FILE} ont été chargées dans InfluxDB.")

if __name__ == "__main__":
    load_to_influx()