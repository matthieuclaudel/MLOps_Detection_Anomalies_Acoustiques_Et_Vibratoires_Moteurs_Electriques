#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nom du fichier : train_model.py
Description : 
Auteur : Pinel.A
Date : 2024-11-04
"""
import pickle
import os
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import classification_report, confusion_matrix

from . import (
    normalize_prediction,
    import_dataset,
    fX_train,
    fy_train,
    default_model_filename
)

def save_model(model_filename, model):
    with open(model_filename, 'wb') as file:
        pickle.dump(model, file)
        print(f"Modèle entraîné sauvegardé sous {model_filename}")

def fit_model(model_class, params):
    model = model_class(**params)
    X_train = import_dataset(fX_train)
    y_train = import_dataset(fy_train)

    model.fit(X_train.values)

    y_pred = model.predict(X_train.values)
    y_pred = normalize_prediction(y_pred)

    print("Rapport de classification sur le jeu d'entrainement : \n", classification_report(y_train, y_pred), "\n")
    print(confusion_matrix(y_train.values, y_pred=y_pred))
    return model

def main(
        model_class=LocalOutlierFactor
        params={
            "novelty": True,
            "n_neighbors": 2,
            "contamination": 0.25,
            "metric": "cosine",
            "n_jobs": -1,
        },
        model_filename=default_model_filename
):
    model = fit_model(model_class, params)
    save_model(model_filename, model)

if __name__ == "__main__":
    main()
