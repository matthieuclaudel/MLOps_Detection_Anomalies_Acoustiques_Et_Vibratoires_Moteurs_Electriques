from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks,Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel,Field
from typing import Optional
from bson import ObjectId
from hashlib import sha256
import numpy as np
import json
import os
import time
from datetime import datetime, timedelta
import jwt
from cryptography.fernet import Fernet
from fastapi.responses import HTMLResponse
import dagshub
import mlflow
import pickle
from prometheus_fastapi_instrumentator import Instrumentator
from motor.motor_asyncio import AsyncIOMotorClient
from app_model_models import DataModel,Mesure,Token,UserInDB,UserOut,User,DataCollection,PyObjectId
# Variable d'env
from dotenv import load_dotenv
load_dotenv()
app = FastAPI(
    title="Acoustic API",
    summary="Application predict and to add collection to a MongoDB collection.",
)
# Constants
JSON_FILE_PATH = os.path.expanduser("./data/users.json")
SECRET_KEY = Fernet.generate_key()
ALGORITHM = "HS256"
MONGO_DETAILS = os.getenv('MONGODB_URI', "mongodb://localhost:27017")  # Remplacez par votre URI MongoDB si nécessaire
DAGSHUB_USER_TOKEN = os.getenv('DAGSHUB_USER_TOKEN', 'Token par défaut')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
version_sc = 0
version_model = 0
# Configurer la connexion à MongoDB
client = AsyncIOMotorClient(MONGO_DETAILS)
print(client,MONGO_DETAILS)
database = client.production  # Accéder à la base de données "production"

# Exemple d'une collection spécifique
collection_name = database["api_mesures"]  # Remplacez par le nom de votre collection
instrumentator = Instrumentator().instrument(app).expose(app)

# Functions for initialization and configuration
def load_models(name = 'model_docker'): 
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
    """Charge le modèle depuis le fichier Pickle ou le télécharge depuis MLflow si nécessaire."""
    if not os.path.exists(f"models/{name}/{version}.pkl"):
        print(f"Modèle non trouvé à {model_uri}. Téléchargement depuis DagsHubs-MLflow...")
        # Load the model
        model = mlflow.sklearn.load_model(model_uri)
        os.makedirs(os.path.dirname(f"models/{name}/{version}.pkl)"),exist_ok=True)
        with open(f"models/{name}/{version}.pkl", "wb") as f:
            pickle.dump(model, f)
        print("Modèle téléchargé et sauvegardé en Pickle.")
    else:
        print(f"Chargement du modèle depuis {model_uri}...")
        with open(f"models/{name}/{version}.pkl", "rb") as f:
            model = pickle.load(f)
    return model,version

# Initialization   
model,version_model = load_models(name = 'model_docker')
sc,version_sc = load_models(name = 'StandardScaler')
# Helper Functions
def verify_password(plain_password, hashed_password):
    return sha256(plain_password.encode()).hexdigest() == hashed_password

def load_users():
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, "r") as file:
            users_data = json.load(file)
        return [UserInDB(**user) for user in users_data]
    return []

def save_user(user: UserInDB):
    users = load_users()
    users.append(user)
    with open(JSON_FILE_PATH, "w") as file:
        json.dump([user.dict() for user in users], file)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=1440)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload["sub"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

def prediction(Mesures_CNI: Mesure):
    # Conversion en tableau numpy et reshape pour le modèle
    features_array=[]
    features_array=list(Mesures_CNI.dict().values())
    array_float = np.array(features_array)
    reshaped_values = array_float.reshape(1, -1)
    X_test=sc.transform(reshaped_values)
    predictions = model.predict(X_test)
    print(f"longeur X_test = {len(X_test[0])},prediction = {predictions[0]}")
    return predictions
async def insert_database(data:DataModel):
    data.versionmodel=int(version_model)
    data.versionsc=int(version_sc)
    try:
        # Insérer dans MongoDB
        result = await collection_name.insert_one(data.model_dump(by_alias=True, exclude=["id"]))
        # Retourner une réponse avec l'ID de l'objet inséré
        print({"id": str(result.inserted_id)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Endpoints
@app.post("/register", response_model=UserOut,tags=["User Management"],
            summary="Create a new user",
            description="This endpoint creates a new user in the system.",)
async def register(user: User, current_user: UserOut = Depends(get_current_user)):
    hashed_password = sha256(user.password.encode()).hexdigest()
    user_data = user.dict(exclude={"password"})
    user_in_db = UserInDB(**user_data, password=hashed_password)
    save_user(user_in_db)
    return UserOut(**user_data)

@app.post("/token", response_model=Token,tags=["User Management"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    users = load_users()
    for user in users:
        if user.username == username and verify_password(password, user.password): 
            token_data = {"sub": username}
            access_token = create_access_token(token_data, expires_delta=timedelta(minutes=30))
            return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@app.post("/predict-test/",tags=["Model"],
            summary="Prédictions manuelle.",
            description="Réalise la prédiction avec le modèle chargé manuellement sans archivage dans mongodb.",)
async def predict_sign(Mesures_CNI: Mesure, current_user: UserOut = Depends(get_current_user)):
    pred=prediction(Mesures_CNI)
    return {"Prediction":int(pred)}

@app.post("/predict/",tags=["Model"],
            summary="Prédictions automatiques.",
            description="Prédictions avec le modèle Present sous dagshubs. Puis archivage des datas dans mongoDB.",)
async def add_data(Mesures: DataModel, background_tasks: BackgroundTasks, current_user: UserOut = Depends(get_current_user)):
    start_time = time.perf_counter()
    # Effectuer la prédiction
    pred=prediction(Mesures.Mesure_CNI)
    end_time = time.perf_counter()
    Mesures.client=current_user["username"]
    Mesures.prediction=int(pred)
    Mesures.temp_rep=end_time - start_time
    Mesures.date_de_creation=datetime.utcnow()
    # Démarrer la sauvegarde en arrière-plan (cela ne bloquera pas la réponse)
    background_tasks.add_task(insert_database, Mesures)
    return {"prediction": int(pred)}

@app.post("/Archivage/",tags=["Model"],
            summary="Test pour insertion d'une ligne dans mongoDB",
            description="Essentiellement utile pour le développeur.",)
async def test(cni: DataModel = Body(...), current_user: UserOut = Depends(get_current_user)):
    result = await collection_name.insert_one(cni.model_dump(by_alias=True, exclude=["id"]))
    return {"Prediction":0}

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Endpoint Docs</title>
    </head>
    <body>
        <h1>Bienvenue sur mon application FastAPI Mesure acoustic</h1>
        <h2>by Datascientest!</h2>
        <p>Pour accéder à la documentation de l'API, cliquez sur le lien ci-dessous :</p>
        <a href="/api/docs" target="_blank">Accéder à la documentation de l'API</a>
    </body>
    </html>
    """
    return html_content

# Endpoint pour vérifier la version
@app.get("/version",tags=["Model"],
            summary="Renvoie le numéro de version.",
            description="Renvoie le dernier Numéro de version du modèle Et du standard scalaire présent dans dagshubs cloud.",)
async def get_version():
    return {"version standard scaler" : version_sc , "version model" : version_model }

# Endpoint pour Mettre à jour les versions du modèle à partir dagshub.
@app.put("/reload",tags=["Model"],
            summary="Recharge le dernier modèle validé dans le cloud",
            description="Viens chercher le dernier modèle et le dernier standard scalaire de mise à jour dans le cloud",)
async def put_relaod():
    global model,version_model,sc,version_sc
    model,version_model = load_models(name = 'model_docker')
    sc,version_sc = load_models(name = 'StandardScaler')
    return {"version standard scaler" : version_sc , "version model" : version_model }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_model:app", host="0.0.0.0", port=8000, root_path="/api")
