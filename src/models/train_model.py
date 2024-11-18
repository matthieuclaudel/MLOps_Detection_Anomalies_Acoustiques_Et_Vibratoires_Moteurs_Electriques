import pickle
import pandas as pd
from sklearn.neighbors import NearestNeighbors,LocalOutlierFactor
from sklearn.metrics import classification_report,confusion_matrix
def import_dataset(file_path, **kwargs):
    return pd.read_csv(file_path, **kwargs)

input_filepath='./data/processed'
fX_train = f"{input_filepath}/X_train_scaled.csv"
f_ytrain = f"{input_filepath}/y_train.csv"
fX_test = f"{input_filepath}/X_test_scaled.csv"
f_ytest = f"{input_filepath}/y_test.csv"
    # Import datasets
X_train = import_dataset(fX_train,header=None)
y_train = import_dataset(f_ytrain)

# Instanciation de l'algo LOF de base
params = {
    "novelty":True,
    "n_neighbors":2,
    "contamination":0.25,
    "metric":"cosine",
    "n_jobs":-1,
}
model = LocalOutlierFactor(**params)
    # Training sans réduction de dimension
y_pred=model.fit(X_train)
y_pred=model.predict(X_train)
y_pred[y_pred == 1] = 0
print("Rapport de classification : \n",classification_report(y_train,y_pred),"\n")
print(confusion_matrix(y_train.values, y_pred=y_pred))
# Sauvegarder le modèle entraîné dans un fichier .pkl
model_filename = 'models/trained_LOF_model.pkl'
with open(model_filename, 'wb') as file:
    pickle.dump(model, file)
print(f"Modèle entraîné sauvegardé sous {model_filename}")