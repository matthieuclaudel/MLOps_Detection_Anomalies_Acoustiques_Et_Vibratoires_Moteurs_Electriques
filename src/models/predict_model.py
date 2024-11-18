#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nom du fichier : predict_model.py
Description : Ce script Teste les données. À partir du modèle pré-entraîné.
Auteur : Pinel.A
Date : 2024-11-18
"""

import pickle
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
def import_dataset(file_path, **kwargs):
    return pd.read_csv(file_path, **kwargs)

# Chargement des données pour évaluation (Remplacer par votre méthode de chargement)
input_filepath='./data/processed'
fX_test = f"{input_filepath}/X_test_scaled.csv"
f_ytest = f"{input_filepath}/y_test.csv"
fX_train = f"{input_filepath}/X_train_scaled.csv"
    # Import datasets
X_test = import_dataset(fX_test,header=None)
y_test = import_dataset(f_ytest)
X_train = import_dataset(fX_train,header=None)
# Chemin vers le modèle sauvegardé
model_filename = 'models/trained_LOF_model.pkl'

# Charger les modèles entraînés
with open(model_filename, 'rb') as file:
    loaded_model = pickle.load(file)

print("Modèle chargé avec succès !")
# Faire des prédictions avec le modèle chargé
y_pred = loaded_model.predict(X_test)
y_pred[y_pred == 1] = 0

print("somme ypred", np.abs(y_pred.sum()), ", somme y_test",np.abs(y_test.sum()))
print("moy acc", (np.abs(y_pred.sum())/np.abs(y_test.sum()))*100,"%")
print("Rapport de classification : \n", classification_report(y_test,y_pred), "\n")
# Sauvegarder les prédictions et les vraies valeurs dans un nouveau fichier CSV
predictions_df =y_test
predictions_df["y_pred"]=y_pred
data_filename = 'data/predictions.csv'
predictions_df.to_csv(data_filename, index=False)

print(f"Prédictions sauvegardées dans {data_filename}")