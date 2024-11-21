from fastapi import FastAPI, UploadFile, File, header
import pandas as pd 
from sklearn.cluster import DBSCAN
import json
import datetime
from sklearn.externals import joblib

app = FastAPI

@app.get('/train',mac = header())
async def train(dataset: UploadFile = File(...)):
    #preprocessing
    #entrainement du modele (à remplacer)
    dataset = pd.read_csv(file.file) 
    model = DBSCAN(eps=0.5, min_samples=5) 
    model.fit(dataset) 
    
    # Stockage des métriques et des logs 
    metrics = {'n_clusters': len(set(model.labels_)) - (1 if -1 in model.labels_ else 0)} 
    with open('metrics.txt', 'w') as f: 
        f.write(json.dumps(metrics)) 
    with open('test_logs.txt', 'w') as f: 
        f.write(f"{datetime.now()};'Training completed successfully\n'") 
        #Stockage du modèle dans un fichier

    joblib.dump(model, 'trained_model')

@app.post('/predict')
async def predict():
    mp = joblib.load('trained_model')
    mp.predict()