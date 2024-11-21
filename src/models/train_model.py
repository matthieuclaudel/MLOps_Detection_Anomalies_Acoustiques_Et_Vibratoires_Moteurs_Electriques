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


input_filepath = './data/processed'
fX_train = f"{input_filepath}/X_train_scaled.csv"
fy_train = f"{input_filepath}/y_train.csv"


def normalize_prediction(y: 'numpy.ndarray') -> 'numpy.ndarray':
    y[y == 1] = 0
    # y[y == -1] = 1
    return y


def import_dataset(file_path, **kwargs):
    if os.path.exists(file_path):
        return pd.read_csv(file_path, **kwargs)
    else:
        raise FileNotFoundError(f'{file_path} does not exist !')


def save_model(model_filename, model):
    with open(model_filename, 'wb') as file:
        pickle.dump(model, file)
        print(f"Modèle entraîné sauvegardé sous {model_filename}")


def fit_model(model_class, params):
    model = model_class(**params)

    X_train = import_dataset(fX_train, header=None)
    y_train = import_dataset(fy_train)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_train)
    y_pred = normalize_prediction(y_pred)

    print("Rapport de classification sur le jeu d'entrainement : \n", classification_report(y_train, y_pred), "\n")

    return model


def main(
        model_class=LocalOutlierFactor,
        params={
            "novelty": True,
            "n_neighbors": 2,
            "contamination": 0.25,
            "metric": "cosine",
            "n_jobs": -1,
        },
        model_filename='models/trained_LOF_model.pkl'
):
    model = fit_model(model_class, params)
    save_model(model_filename, model)

if __name__ == "__main__":
    main()