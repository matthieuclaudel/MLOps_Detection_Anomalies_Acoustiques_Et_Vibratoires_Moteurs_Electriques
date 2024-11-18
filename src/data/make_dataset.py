#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nom du fichier : make_dataset.py
Description : Ce script crée le fichier Config . local à partir du secret inclus dans git Récupère les datas..
Auteur : Pinel.A
Date : 2024-11-04
"""
import sys, subprocess, os, logging, inspect
import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
# Fonctions
def pull_data_with_dvc(logger):
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    cmd = [sys.executable, "-m", "dvc", "pull"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        logger.info("extract OK")
        logger.info(result.stdout)
    else:
        logger.info("extract NOK")
        logger.info(result.stderr)
    return result.returncode

def modifconfigsecret(file_path, secret, logger):
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    chemin_fichier = file_path+"config.local"

    if os.path.exists(chemin_fichier):
        logger.info("Le fichier existe.")
    else:
        logger.info("Le fichier n'existe pas.")
        # Contenu du fichier
        contenu = f"['remote \"origin\"']\n    access_key_id = {secret}\n    secret_access_key = {secret}"
        # Création du fichier et écriture du contenu
        with open(chemin_fichier, "w") as fichier:
            result=fichier.write(contenu)
            logger.info("credentials pass")
        return result

def import_dataset(logger, file_path, **kwargs):
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    df_go = pd.read_csv(file_path+'/DATASET_GO_NG.csv', **kwargs)
    logger.info(f"df all nbre de lignes :{len(df_go)}")
    df_ng = pd.read_csv(file_path+'/DATASET_NG.csv', **kwargs)
    logger.info(f"df test nbre de lignes :{len(df_ng)}")
    return df_go, df_ng
    
def split_data(df, df_ng):
    # Split data into training and testing sets
    df_all = pd.concat([df, df_ng])
    X = shuffle(df_all)

    # Séparer les données sans NaN (clean) et celles avec NaN
    X_clean = X.dropna()
    X_with_nan = X[X.isna().any(axis=1)]
    Y_clean = X_clean["target"].astype(float).astype(int)
    # Split uniquement sur les données sans NaN avec stratification
    X_train_clean, X_test, y_train_clean, y_test = train_test_split(
        X_clean.drop(["target"], axis=1), Y_clean, test_size=0.1, stratify=Y_clean, random_state=42
    )
    # Ajouter les données contenant des NaN uniquement à X_train et y_train
    X_train = pd.concat([X_train_clean, X_with_nan.drop(["target"],axis=1)])
    y_train = pd.concat([y_train_clean, X_with_nan["target"]])
    # Réinitialiser les index pour éviter les conflits
    X_train.reset_index(drop=True, inplace=True)
    X_test.reset_index(drop=True, inplace=True)
    y_train.reset_index(drop=True, inplace=True)
    y_test.reset_index(drop=True, inplace=True)   
 
    return X_train, X_test, y_train, y_test
    
def create_folder_if_necessary(output_folderpath):
    # Create folder if necessary
    if os.path.exists(output_folderpath) == False:
        os.makedirs(output_folderpath)

def save_dataframes(X_train, X_test, y_train, y_test, output_folderpath) :
    # Save dataframes to their respective output file paths
    for file, filename in zip([X_train, X_test, y_train, y_test], ['X_train', 'X_test', 'y_train', 'y_test']):
        output_filepath = os.path.join(output_folderpath, f'{filename}.csv')
        file.to_csv(output_filepath, index=False)
        
# Fonction principale
def main(input_filepath='./data/raw', output_filepath='./data/interim') :
    """
    Point d'entrée principal du programme.
    Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in../preprocessed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making data set from raw data')
    # Récupérer les arguments de la ligne de commande
    if len(sys.argv) > 1:
        secret = str(sys.argv[1])  # Convertir le 1er argument
    else:
        logger.info("Veuillez fournir un paramètre str en argument.")
        sys.exit(1)

    # Appel de fonction avec le paramètre d'entrée
    resultat = modifconfigsecret(".dvc/", secret,logger)
    logger.info(f"Le résultat est : {resultat}")
    # Appel de fonction pull dvc
    resultat = pull_data_with_dvc(logger)
    logger.info(f"Le résultat est : {resultat}")

    df,df_ng = import_dataset(logger, input_filepath, sep=';', decimal=',', index_col="index")
    # Split data into training and testing sets    
    X_train, X_test, y_train, y_test = split_data(df, df_ng)

    # Create folder if necessary
    create_folder_if_necessary(output_filepath)

    # Save dataframes to their respective output file paths
    logger.info('save_dataframes progress ...')
    save_dataframes(X_train, X_test, y_train, y_test, output_filepath)
    
    logger.info('make interim data set')

# Bloc pour lancer le script en tant que programme principal
if __name__ == "__main__" :
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
