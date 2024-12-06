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
from sklearn.metrics import classification_report, confusion_matrix

from src.models.utils import (
    import_dataset,
    normalize_prediction,
    fX_test,
    fy_test,
    default_model_filename
)

def load_model(model_filename):
    with open(model_filename, 'rb') as file:
        loaded_model = pickle.load(file)
    return loaded_model

def save_prediction(target, prediction, results_filename):

    df = pd.DataFrame(
        data=np.c_[target, prediction],
        columns=['target', 'prediction']
    )
    
    df.to_csv(results_filename, index=False)
    print(f"Prédictions sauvegardées dans {results_filename}")

def predict_model(model_filename, X, y=None):
    model = load_model(model_filename)
    y_pred = model.predict(X)
    y_pred = normalize_prediction(y_pred)
    if y is not None:
        print("Rapport de classification sur le jeu données : \n", classification_report(y, y_pred), "\n")
        save_prediction(y.values.squeeze(), y_pred.squeeze(), 'data/predictions.csv')
        print(confusion_matrix(y, y_pred=y_pred))
    
    return

def eval_model(model_filename):
    X_test = import_dataset(fX_test)
    y_test = import_dataset(fy_test)
    
    predict_model(model_filename, X_test.values, y_test)


def main(model_filename=default_model_filename):
    eval_model(model_filename)

if __name__ == "__main__":
    main()
