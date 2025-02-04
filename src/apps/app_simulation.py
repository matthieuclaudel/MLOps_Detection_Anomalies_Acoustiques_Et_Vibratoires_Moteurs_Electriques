#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nom du fichier : app_simulation.py
Description : Ce script Récupère les datas du fichier CSV présents dans le sous dossier data Row Ensuite envoie des commandes de type Curl à l'aPI model.
Auteur : Pinel.A
Date : 2024-12-02
"""
import sys
import os
import logging
import pandas as pd
import time
import requests
import json
from dotenv import load_dotenv
print(f"Version de Python : {sys.version}")
# Fonctions
def import_dataset(file_path, **kwargs): 
    df = pd.read_csv(file_path+'/DATASIMU750.csv', **kwargs)
    logger.info(f"df nbre de lignes :{len(df)}")
    return df
   
# Function to get data API at a specific page
def fetch_job(API_URL, datas,headers,API_USER, API_PWD): 
    ENDPOINT = "/predict"
    val=datas["Mesure_CNI"].get("G14_vib_up")
    logger.info(f"URL d'appel = {API_URL+ENDPOINT}/ data G14_vib_up = {val}")
    response = requests.post(f"{API_URL+ENDPOINT}/", json=datas, headers=headers)
    logger.info(f"response.status_code : {response.status_code} reason : {response.reason[:100]} URL : {response.url[:70]} content : {response.content[:70]}")
    if response.status_code == 200: 
        return response.status_code
    else:
        logger.warning("Failed to fetch data:", response.status_code)
        time.sleep(1)
        response = requests.post(f"{API_URL+ENDPOINT}/", json=datas, headers=headers)
        if response.status_code == 200: 
            data = response.json()
            logger.info(f"response.json : {data}")
            return response.status_code
        else:
            logger.error("Failed again to fetch data:", response.status_code)
            return response.status_code
def credentials(user, pwd,url,): 
     # Send login request to get an access token
    auth_response = requests.post(url + "/token", data={"username": user, "password": pwd})
    # Extract the access token from the response
    if auth_response.status_code == 200: 
        access_token = json.loads(auth_response.text)["access_token"]
        # Set headers for authenticated request
        headers = {"Authorization": f"Bearer {access_token}"}
        logger.info(f"Authorization: Bearer {access_token}")
    else:
        print(auth_response.url+auth_response.text)
        logger.error("Failed to authenticate with API : "+auth_response.text+user)
        exit(402)
    return headers
# Fonction principale
def main(input_filepath='./data/raw'): 
    """
    Point d'entrée principal du programme.
    Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in../preprocessed).
    """
    load_dotenv(verbose=True, override=True)
    logger.info('making data set from raw data')
    # Récupérer les arguments
    if len(os.getenv('API_URL')) > 1: 
        API_URL = os.getenv('API_URL', 'App par défaut')  # Convertir le 1er argument
        API_USER = os.getenv('API_USER', 'App par défaut')
        API_PWD = os.getenv('API_PWD', 'App par défaut')
    else:
        logger.error("Veuillez fournir un paramètre str en argument.")
        sys.exit(1)
    
    df = import_dataset(input_filepath, sep=';', decimal=',', index_col="index")
    headers=credentials(API_USER, API_PWD,API_URL)
    try:
        while True:
            # Code à exécuter à chaque itération
            # Pause d'une seconde entre chaque itération
            time.sleep(1)
            # Extraire une ligne aléatoire
            ligne_aleatoire = df.sample(n=1)
            # Convertir la ligne en dictionnaire
            ligne_dict={}
            ligne_dict["Mesure_CNI"] = ligne_aleatoire.to_dict(orient='records')[0]
            error=fetch_job(API_URL,ligne_dict,headers,API_USER, API_PWD)
            if error == 401: 
                headers=credentials(API_USER, API_PWD,API_URL)


    except KeyboardInterrupt:
        # Capture l'interruption manuelle (Ctrl+C)
        logger.warning("Boucle interrompue par l'utilisateur.")

    except Exception as e:
        # Capture d'autres exceptions imprévues
        logger.error(f"Erreur inattendue : {e}")

    finally:
        # Code à exécuter après la sortie de la boucle (nettoyage)
        logger.info("Fin de la boucle.") 



# Bloc pour lancer le script en tant que programme principal
logger = logging.getLogger("App_Simu")
load_dotenv()
if __name__ == "__main__": 
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
