# REPERTOIRE DATA

Ce répertoire contient les jeux de données constitués dans le cadre de l'ETL à savoir :

- raw.csv : dataset brut permettant le ré-entrainement d'un modèle Local Outlier Factor
- DATASET_VALIDATION.csv : dataset ETALON pour mesurer les performances des nouveaux modèles
- data_train.csv : dataset raw.csv pré-processé et normalisé
- data_test.csv : dataset DATASET_VALIDATION pré-processé et normalisé à partir du modèle StandardScaler utilisé pour data_train.csv
- best_model.pkl : sauvegarde du modèle avec le meilleur FN rate 
- best_score.pkl : sauvegarde des métriques de best_model.pkl 
- model_params.pkl : sauvegarde des hyper-paramètres du modèle
- scaler_model.pkl : sauvegarde du modèle de normalisations

Toutes les sauvegardes .pkl sont utilisées dans le DAG **train_model_dag** pour assurer le suivi des expériences dans DagsHub/MLFlow

## Structure

    ├── data
    │   └── raw            <- Original, immutable, temporarily generated data dump.



