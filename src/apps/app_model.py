from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from hashlib import sha256
import numpy as np
import json
import os
from datetime import datetime, timedelta
import jwt
from cryptography.fernet import Fernet
from fastapi.responses import HTMLResponse
import dagshub
import mlflow
import pickle
from prometheus_fastapi_instrumentator import Instrumentator
# Variable d'env
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()
instrumentator = Instrumentator().instrument(app).expose(app)
# Constants
JSON_FILE_PATH = os.path.expanduser("./data/users.json")
SECRET_KEY = Fernet.generate_key()
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
DAGSHUB_USER_TOKEN = os.getenv('DAGSHUB_USER_TOKEN', 'Token par défaut')
version_sc = 0
version_model = 0
# User Models
class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str

class UserOut(BaseModel):
    username: str
    first_name: str
    last_name: str

class UserInDB(User):
    password: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Define the mesure input model
class Mesure(BaseModel):
    V1_AC_down: float = 27.516
    V1_vib_down: float = 1.0375
    V2_AC_down: float = 27.032
    V2_vib_down: float = 0.054563
    V3_AC_down: float = 24.072
    V3_vib_down: float = 0.16013
    V4_AC_down: float = 23.279
    V4_vib_down: float = 0.097066
    V5_AC_down: float = 28.821
    V5_vib_down: float = 0.58251
    V6_AC_down: float = 23.2
    V6_vib_down: float = 0.19269
    V7_AC_down: float = 23.601
    V7_vib_down: float = 0.13146
    V8_AC_down: float = 37.332
    V8_vib_down: float = 0.31652
    V9_AC_down: float = 19.943
    V9_vib_down: float = 0.016273
    V10_AC_down: float = 22.327
    V10_vib_down: float = 0.026746
    V11_AC_down: float = 25.424
    V11_vib_down: float = 0.013227
    V12_AC_down: float = 26.854
    V12_vib_down: float = 0.013001
    V13_AC_down: float = 28.43
    V13_vib_down: float = 0.0095903
    V14_AC_down: float = 23.168
    V14_vib_down: float = 0.010181
    V15_AC_down: float = 24.831
    V15_vib_down: float = 0.075872
    V16_AC_down: float = 21.607
    V16_vib_down: float = 0.10122
    V17_AC_down: float = 20.208
    V17_vib_down: float = 0.019105
    V18_AC_down: float = 19.808
    V18_vib_down: float = 0.018459
    V19_AC_down: float = 21.65
    V19_vib_down: float = 0.010824
    V20_AC_down: float = 24.124
    V20_vib_down: float = 0.011493
    V21_AC_down: float = 19.979
    V21_vib_down: float = 0.015512
    V22_AC_down: float = 18.155
    V22_vib_down: float = 0.029608
    V23_AC_down: float = 22.999
    V23_vib_down: float = 0.05716
    V24_AC_down: float = 27.8
    V24_vib_down: float = 0.13207
    V25_AC_down: float = 30.245
    V25_vib_down: float = 0.034133
    V26_AC_down: float = 30.853
    V26_vib_down: float = 0.01591
    V27_AC_down: float = 29.161
    V27_vib_down: float = 0.020644
    V28_AC_down: float = 31.175
    V28_vib_down: float = 0.016985
    V29_AC_down: float = 32.12
    V29_vib_down: float = 0.024358
    V30_AC_down: float = 27.942
    V30_vib_down: float = 0.083462
    V31_AC_down: float = 27.601
    V31_vib_down: float = 0.054542
    V32_AC_down: float = 24.803
    V32_vib_down: float = 0.10694
    V33_AC_down: float = 20.835
    V33_vib_down: float = 0.021737
    V34_AC_down: float = 27.367
    V34_vib_down: float = 0.020813
    V35_AC_down: float = 22.767
    V35_vib_down: float = 0.032191
    V36_AC_down: float = 23.014
    V36_vib_down: float = 0.017922
    V37_AC_down: float = 24.351
    V37_vib_down: float = 0.03089
    V38_AC_down: float = 31.673
    V38_vib_down: float = 0.1196
    V39_AC_down: float = 27.85
    V39_vib_down: float = 0.074197
    V40_AC_down: float = 24.571
    V40_vib_down: float = 0.16688
    V41_AC_down: float = 19.109
    V41_vib_down: float = 0.029364
    V42_AC_down: float = 19.101
    V42_vib_down: float = 0.02291
    V43_AC_down: float = 19.825
    V43_vib_down: float = 0.024917
    V44_AC_down: float = 15.488
    V44_vib_down: float = 0.024305
    V45_AC_down: float = 23.453
    V45_vib_down: float = 0.16486
    V46_AC_down: float = 26.943
    V46_vib_down: float = 0.057635
    V47_AC_down: float = 25.809
    V47_vib_down: float = 0.061154
    V48_AC_down: float = 24.96
    V48_vib_down: float = 0.22945
    V49_AC_down: float = 21.595
    V49_vib_down: float = 0.092725
    V50_AC_down: float = 18.723
    V50_vib_down: float = 0.040875
    V51_AC_down: float = 21.542
    V51_vib_down: float = 0.023956
    V52_AC_down: float = 24.862
    V52_vib_down: float = 0.054276
    V53_AC_down: float = 25.466
    V53_vib_down: float = 0.18848
    V54_AC_down: float = 27.247
    V54_vib_down: float = 0.10681
    V55_AC_down: float = 29.729
    V55_vib_down: float = 0.072246
    V56_AC_down: float = 29.185
    V56_vib_down: float = 0.218
    V57_AC_down: float = 16.451
    V57_vib_down: float = 0.10698
    V58_AC_down: float = 12.733
    V58_vib_down: float = 0.046233
    V59_AC_down: float = 24.6
    V59_vib_down: float = 0.052155
    V60_AC_down: float = 21.245
    V60_vib_down: float = 0.18039
    V61_AC_down: float = 26.442
    V61_vib_down: float = 0.070065
    V62_AC_down: float = 31.383
    V62_vib_down: float = 0.13211
    V63_AC_down: float = 30.663
    V63_vib_down: float = 0.080012
    V64_AC_down: float = 32.33
    V64_vib_down: float = 0.27912
    V65_AC_down: float = 24.875
    V65_vib_down: float = 0.13927
    V66_AC_down: float = 24.108
    V66_vib_down: float = 0.072203
    V67_AC_down: float = 25.236
    V67_vib_down: float = 0.090114
    V68_AC_down: float = 29.533
    V68_vib_down: float = 0.24807
    V69_AC_down: float = 27.225
    V69_vib_down: float = 0.095514
    V70_AC_down: float = 24.424
    V70_vib_down: float = 0.14341
    V71_AC_down: float = 26.618
    V71_vib_down: float = 0.11593
    V72_AC_down: float = 28.046
    V72_vib_down: float = 0.27711
    V73_AC_down: float = 26.088
    V73_vib_down: float = 0.15312
    V74_AC_down: float = 23.665
    V74_vib_down: float = 0.083412
    V75_AC_down: float = 28.791
    V75_vib_down: float = 0.11726
    G1_AC_down: float = 41.004
    G1_vib_down: float = 1.38
    G2_AC_down: float = 44.174
    G2_vib_down: float = 1.1419
    G3_AC_down: float = 38.932
    G3_vib_down: float = 0.069734
    G4_AC_down: float = 37.2
    G4_vib_down: float = 0.23839
    G5_AC_down: float = 39.903
    G5_vib_down: float = 0.30421
    G6_AC_down: float = 45.049
    G6_vib_down: float = 0.10896
    G7_AC_down: float = 39.949
    G7_vib_down: float = 0.27819
    G8_AC_down: float = 39.968
    G8_vib_down: float = 0.37541
    G9_AC_down: float = 34.714
    G9_vib_down: float = 0.32634
    G10_AC_down: float = 38.801
    G10_vib_down: float = 0.6095
    G11_AC_down: float = 39.709
    G11_vib_down: float = 0.4823
    G12_AC_down: float = 38.568
    G12_vib_down: float = 0.54575
    G13_AC_down: float = 43.49
    G13_vib_down: float = 0.78234
    G14_AC_down: float = 39.874
    G14_vib_down: float = 0.67117
    G15_AC_down: float = 40.848
    G15_vib_down: float = 0.87189
    G16_AC_down: float = 44.901
    G16_vib_down: float = 0.94675
    G17_AC_down: float = 46.415
    G17_vib_down: float = 1.3566
    G18_AC_down: float = 47.117
    G18_vib_down: float = 2.4552
    G19_AC_down: float = 46.713
    G19_vib_down: float = 2.1732
    G20_AC_down: float = 46.082
    G20_vib_down: float = 2.2956
    G21_AC_down: float = 34.595
    G21_vib_down: float = 0.49028
    G22_AC_down: float = 40.308
    G22_vib_down: float = 0.55665
    G23_AC_down: float = 34.41
    G23_vib_down: float = 0.79437
    G24_AC_down: float = 34.116
    G24_vib_down: float = 0.98987
    G25_AC_down: float = 31.375
    G25_vib_down: float = 1.5449
    G26_AC_down: float = 31.973
    G26_vib_down: float = 2.1337
    G27_AC_down: float = 35.239
    G27_vib_down: float = 3.7475
    G28_AC_down: float = 34.327
    G28_vib_down: float = 3.5612
    G29_AC_down: float = 29.597
    G29vib_down: float = 1.5189
    G30_AC_down: float = 25.879
    G30_vib_down: float = 1.0476
    G31_AC_down: float = 29.022
    G31_vib_down: float = 1.1055
    G32_AC_down: float = 26.571
    G32_vib_down: float = 0.75217
    G33_AC_down: float = 24.422
    G33_vib_down: float = 0.68547
    V1_AC_up: float = 25.375
    V1_vib_up: float = 0.67244
    V2_AC_up: float = 22.658
    V2_vib_up: float = 0.06666
    V3_AC_up: float = 25.15
    V3_vib_up: float = 0.36003
    V4_AC_up: float = 24.478
    V4_vib_up: float = 0.09714
    V5_AC_up: float = 28.774
    V5_vib_up: float = 0.14745
    V6_AC_up: float = 26.248
    V6_vib_up: float = 0.24403
    V7_AC_up: float = 21.555
    V7_vib_up: float = 0.23143
    V8_AC_up: float = 39.813
    V8_vib_up: float = 0.28303
    V9_AC_up: float = 28.995
    V9_vib_up: float = 0.022949
    V10_AC_up: float = 22.766
    V10_vib_up: float = 0.018225
    V11_AC_up: float = 32.783
    V11_vib_up: float = 0.056749
    V12_AC_up: float = 42.319
    V12_vib_up: float = 0.036571
    V13_AC_up: float = 28.977
    V13_vib_up: float = 0.035213
    V14_AC_up: float = 32.489
    V14_vib_up: float = 0.022277
    V15_AC_up: float = 28.239
    V15_vib_up: float = 0.020807
    V16_AC_up: float = 29.466
    V16_vib_up: float = 0.047595
    V17_AC_up: float = 25.807
    V17_vib_up: float = 0.027949
    V18_AC_up: float = 26.221
    V18_vib_up: float = 0.04707
    V19_AC_up: float = 20.359
    V19_vib_up: float = 0.024741
    V20_AC_up: float = 30.48
    V20_vib_up: float = 0.021321
    V21_AC_up: float = 22.543
    V21_vib_up: float = 0.024154
    V22_AC_up: float = 25.762
    V22_vib_up: float = 0.029678
    V23_AC_up: float = 29.036
    V23_vib_up: float = 0.036128
    V24_AC_up: float = 32.541
    V24_vib_up: float = 0.06797
    V25_AC_up: float = 27.224
    V25_vib_up: float = 0.061699
    V26_AC_up: float = 20.992
    V26_vib_up: float = 0.034838
    V27_AC_up: float = 29.672
    V27_vib_up: float = 0.030865
    V28_AC_up: float = 35.567
    V28_vib_up: float = 0.035529
    V29_AC_up: float = 38.374
    V29_vib_up: float = 0.020647
    V30_AC_up: float = 41.568
    V30_vib_up: float = 0.0277
    V31_AC_up: float = 36.358
    V31_vib_up: float = 0.032939
    V32_AC_up: float = 37.809
    V32_vib_up: float = 0.046575
    V33_AC_up: float = 37.52
    V33_vib_up: float = 0.038298
    V34_AC_up: float = 38.41
    V34_vib_up: float = 0.021978
    V35_AC_up: float = 30.376
    V35_vib_up: float = 0.019035
    V36_AC_up: float = 25.852
    V36_vib_up: float = 0.022767
    V37_AC_up: float = 28.693
    V37_vib_up: float = 0.024962
    V38_AC_up: float = 24.803
    V38_vib_up: float = 0.024894
    V39_AC_up: float = 25.858
    V39_vib_up: float = 0.087563
    V40_AC_up: float = 22.581
    V40_vib_up: float = 0.097954
    V41_AC_up: float = 24.127
    V41_vib_up: float = 0.10523
    V42_AC_up: float = 21.56
    V42_vib_up: float = 0.02988
    V43_AC_up: float = 22.134
    V43_vib_up: float = 0.027358
    V44_AC_up: float = 23.361
    V44_vib_up: float = 0.024201
    V45_AC_up: float = 19.893
    V45_vib_up: float = 0.027952
    V46_AC_up: float = 17.961
    V46_vib_up: float = 0.025843
    V47_AC_up: float = 22.974
    V47_vib_up: float = 0.08481
    V48_AC_up: float = 24.778
    V48_vib_up: float = 0.075039
    V49_AC_up: float = 24.762
    V49_vib_up: float = 0.061422
    V50_AC_up: float = 20.024
    V50_vib_up: float = 0.066467
    V51_AC_up: float = 20.214
    V51_vib_up: float = 0.035296
    V52_AC_up: float = 18.802
    V52_vib_up: float = 0.033435
    V53_AC_up: float = 24.658
    V53_vib_up: float = 0.027953
    V54_AC_up: float = 26.471
    V54_vib_up: float = 0.031418
    V55_AC_up: float = 28.922
    V55_vib_up: float = 0.062949
    V56_AC_up: float = 29.887
    V56_vib_up: float = 0.068101
    V57_AC_up: float = 26.516
    V57_vib_up: float = 0.069572
    V58_AC_up: float = 20.349
    V58_vib_up: float = 0.044181
    V59_AC_up: float = 21.538
    V59_vib_up: float = 0.030939
    V60_AC_up: float = 22.04
    V60_vib_up: float = 0.027365
    V61_AC_up: float = 23.796
    V61_vib_up: float = 0.035521
    V62_AC_up: float = 29.714
    V62_vib_up: float = 0.049347
    V63_AC_up: float = 35.307
    V63_vib_up: float = 0.11306
    V64_AC_up: float = 34.998
    V64_vib_up: float = 0.13307
    V65_AC_up: float = 28.571
    V65_vib_up: float = 0.09306
    V66_AC_up: float = 20.882
    V66_vib_up: float = 0.066939
    V67_AC_up: float = 19.629
    V67_vib_up: float = 0.035928
    V68_AC_up: float = 19.7
    V68_vib_up: float = 0.0308
    V69_AC_up: float = 25.098
    V69_vib_up: float = 0.040055
    V70_AC_up: float = 23.74
    V70_vib_up: float = 0.056014
    V71_AC_up: float = 32.334
    V71_vib_up: float = 0.11118
    V72_AC_up: float = 35.22
    V72_vib_up: float = 0.15794
    V73_AC_up: float = 35.561
    V73_vib_up: float = 0.12893
    V74_AC_up: float = 31.752
    V74_vib_up: float = 0.089805
    V75_AC_up: float = 26.567
    V75_vib_up: float = 0.049949
    G1_AC_up: float = 43.817
    G1_vib_up: float = 0.88193
    G2_AC_up: float = 47.811
    G2_vib_up: float = 0.74298
    G3_AC_up: float = 44.676
    G3_vib_up: float = 0.18236
    G4_AC_up: float = 41.91
    G4_vib_up: float = 0.17445
    G5_AC_up: float = 47.689
    G5_vib_up: float = 0.27424
    G6_AC_up: float = 54.021
    G6_vib_up: float = 0.1942
    G7_AC_up: float = 40.744
    G7_vib_up: float = 0.36034
    G8_AC_up: float = 36.644
    G8_vib_up: float = 0.22032
    G9_AC_up: float = 36.456
    G9_vib_up: float = 0.30828
    G10_AC_up: float = 42.286
    G10_vib_up: float = 0.28954
    G11_AC_up: float = 45.525
    G11_vib_up: float = 0.40513
    G12_AC_up: float = 39.472
    G12_vib_up: float = 0.33044
    G13_AC_up: float = 47.583
    G13_vib_up: float = 0.57522
    G14_AC_up: float = 46.07
    G14_vib_up: float = 0.50018
    G15_AC_up: float = 42.238
    G15_vib_up: float = 0.59023
    G16_AC_up: float = 42.74
    G16_vib_up: float = 0.77256
    G17_AC_up: float = 47.601
    G17_vib_up: float = 1.2176
    G18_AC_up: float = 47.984
    G18_vib_up: float = 2.1397
    G19_AC_up: float = 43.746
    G19_vib_up: float = 1.5615
    G20_AC_up: float = 41.303
    G20_vib_up: float = 1.1253
    G21_AC_up: float = 31.972
    G21_vib_up: float = 0.39171
    G22_AC_up: float = 33.211
    G22_vib_up: float = 0.44509
    G23_AC_up: float = 35.089
    G23_vib_up: float = 0.62889
    G24_AC_up: float = 32.537
    G24_vib_up: float = 0.52202
    G25_AC_up: float = 27.174
    G25_vib_up: float = 0.88852
    G26_AC_up: float = 28.881
    G26_vib_up: float = 1.804
    G27_AC_up: float = 34.6
    G27_vib_up: float = 2.4826
    G28_AC_up: float = 32.72
    G28_vib_up: float = 1.8244
    G29_AC_up: float = 28.69
    G29vib_up: float = 1.0759
    G30_AC_up: float = 25.342
    G30_vib_up: float = 0.73923
    G31_AC_up: float = 23.137
    G31_vib_up: float = 0.57734
    G32_AC_up: float = 21.211
    G32_vib_up: float = 0.51112
    G33_AC_up: float = 21.966
    G33_vib_up: float = 0.39971


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
        os.makedirs(os.path.dirname(f"models/{name}/{version}.pkl)"))
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
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload["sub"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

# Endpoints
@app.post("/register", response_model=UserOut)
async def register(user: User):
    hashed_password = sha256(user.password.encode()).hexdigest()
    user_data = user.dict(exclude={"password"})
    user_in_db = UserInDB(**user_data, password=hashed_password)
    save_user(user_in_db)
    return UserOut(**user_data)

@app.post("/token", response_model=Token)
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

@app.post("/predict/")
async def predict_sign(Mesures_CNI: Mesure):#, current_user: UserOut = Depends(get_current_user)):
    # Conversion en tableau numpy et reshape pour le modèle
    features_array=[]
    features_array=list(Mesures_CNI.dict().values())
    array_float = np.array(features_array)
    reshaped_values = array_float.reshape(1, -1)
    X_test=sc.transform(reshaped_values)
    prediction = model.predict(X_test)
    print(f"longeur X_test = {len(X_test[0])},prediction = {prediction[0]}")
    return {"Prediction":int(prediction)}

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <html>
    <body>
        <h1>Welcome to the Mesure acoustic Prediction API!</h1>
    </body>
    </html>
    """
    return html_content

# Endpoint pour vérifier la version
@app.get("/version")
async def get_version():
    return {"version standard scaler" : version_sc , "version model" : version_model }

# Endpoint pour Mettre à jour les versions du modèle à partir dagshub.
@app.put("/relaod")
async def put_relaod():
    global model,version_model,sc,version_sc
    model,version_model = load_models(name = 'model_docker')
    sc,version_sc = load_models(name = 'StandardScaler')
    return {"version standard scaler" : version_sc , "version model" : version_model }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_model:app", host="0.0.0.0", port=8000, reload=True)
