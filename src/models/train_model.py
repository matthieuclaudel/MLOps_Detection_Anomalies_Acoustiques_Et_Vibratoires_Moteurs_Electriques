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
from sklearn.metrics import classification_report

from utils import (
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
    print(f"import data encours ...")
    X_train = import_dataset(fX_train)
    y_train = import_dataset(fy_train)
    print(f"Modèle entraînement encours ...")
    model.fit(X_train.values)

    return model

def main(model_class=LocalOutlierFactor,
        params={
            "novelty": True,
            "n_neighbors": 240,
            "contamination": 0.06,
            "metric": "cosine",
            "n_jobs": -1,
        },
        model_filename=default_model_filename
):
    model = fit_model(model_class, params)
    save_model(model_filename, model)

if __name__ == "__main__":
    main()
