import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle

def load_data():
    # chargement du jeu de données raw.csv généré par le script de prétraitement via le DAG_raw_data.py
    data_train = pd.read_csv('/app/test/raw.csv', sep=',')
    # suppression de la colonne date_de_creation
    data_train = data_train.drop(columns=['date_de_creation'], axis=1)

    # Normalisation des données avec un standard scaler
    scaler_model = StandardScaler()
    raw_values_scaled = scaler_model.fit_transform(data_train)
    data_train_scaled = pd.DataFrame(raw_values_scaled,)
    data_train_scaled.columns = data_train.columns

    # Chargement du jeu de données de validation et normalisation avec le modèle de normalisation
    data_validation = pd.read_csv('/app/test/DATASET_VALIDATION.csv', sep=',') 
    target = data_validation['target']
    index = data_validation['index']
    data_validation = data_validation.drop(columns=['index','target'], axis=1)
    # Normalisation des données de validation
    validation_values_scaled = scaler_model.transform(data_validation)
    data_validation_scaled = pd.DataFrame(validation_values_scaled,)
    data_validation_scaled.columns = data_validation.columns
    data_validation_scaled['target'] = target.values
    data_validation_scaled['index'] = index.values

    data_train_scaled.to_csv('/app/test/data_train.csv', index=False)
    data_validation_scaled.to_csv('/app/test/data_test.csv', index=False)
    
    print('Data loaded successfully')
    return scaler_model

def saved_scaler_model(x):   
    # Sauvegarde du modèle de normalisation dans le répertoire /app/test
    with open('/app/test/scaler_model.pkl', 'wb') as f:
        pickle.dump(x, f)


if __name__ == "__main__":
    load_data()
    saved_scaler_model(scaler_model)