import streamlit as st
import time
import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype
import requests
import json

# Définition des groupes de colonnes
col_t0_vib=['target','index','V1_vib_down',		'V2_vib_down',		'V3_vib_down',		'V4_vib_down',		'V5_vib_down',		'V6_vib_down',		'V7_vib_down',		'V8_vib_down',		'V9_vib_down',		'V10_vib_down',		'V11_vib_down',		'V12_vib_down',		'V13_vib_down',		'V14_vib_down',		'V15_vib_down',		'V16_vib_down',		'V17_vib_down',		'V18_vib_down',		'V19_vib_down',		'V20_vib_down',		'V21_vib_down',		'V22_vib_down',		'V23_vib_down',		'V24_vib_down',		'V25_vib_down',		'V26_vib_down',		'V27_vib_down',		'V28_vib_down',		'V29_vib_down',		'V30_vib_down',		'V31_vib_down',		'V32_vib_down',		'V33_vib_down',		'V34_vib_down',		'V35_vib_down',		'V36_vib_down',		'V37_vib_down',		'V38_vib_down',		'V39_vib_down',		'V40_vib_down',		'V41_vib_down',		'V42_vib_down',		'V43_vib_down',		'V44_vib_down',		'V45_vib_down',		'V46_vib_down',		'V47_vib_down',		'V48_vib_down',		'V49_vib_down',		'V50_vib_down',		'V51_vib_down',		'V52_vib_down',		'V53_vib_down',		'V54_vib_down',		'V55_vib_down',		'V56_vib_down',		'V57_vib_down',		'V58_vib_down',		'V59_vib_down',		'V60_vib_down',		'V61_vib_down',		'V62_vib_down',		'V63_vib_down',		'V64_vib_down',		'V65_vib_down',		'V66_vib_down',		'V67_vib_down',		'V68_vib_down',		'V69_vib_down',		'V70_vib_down',		'V71_vib_down',		'V72_vib_down',		'V73_vib_down',		'V74_vib_down',		'V75_vib_down',		'G1_vib_down',		'G2_vib_down',		'G3_vib_down',		'G4_vib_down',		'G5_vib_down',		'G6_vib_down',		'G7_vib_down',		'G8_vib_down',		'G9_vib_down',		'G10_vib_down',		'G11_vib_down',		'G12_vib_down',		'G13_vib_down',		'G14_vib_down',		'G15_vib_down',		'G16_vib_down',		'G17_vib_down',		'G18_vib_down',		'G19_vib_down',		'G20_vib_down',		'G21_vib_down',		'G22_vib_down',		'G23_vib_down',		'G24_vib_down',		'G25_vib_down',		'G26_vib_down',		'G27_vib_down','G28_vib_down','G29_vib_down','G30_vib_down','G31_vib_down','G32_vib_down','G33_vib_down']
col_t0_ac=['target','index','V1_vib_up',		'V2_vib_up',		'V3_vib_up',		'V4_vib_up',		'V5_vib_up',		'V6_vib_up',		'V7_vib_up',		'V8_vib_up',		'V9_vib_up',		'V10_vib_up',		'V11_vib_up',		'V12_vib_up',		'V13_vib_up',		'V14_vib_up',		'V15_vib_up',		'V16_vib_up',		'V17_vib_up',		'V18_vib_up',		'V19_vib_up',		'V20_vib_up',		'V21_vib_up',		'V22_vib_up',		'V23_vib_up',		'V24_vib_up',		'V25_vib_up',		'V26_vib_up',		'V27_vib_up',		'V28_vib_up',		'V29_vib_up',		'V30_vib_up',		'V31_vib_up',		'V32_vib_up',		'V33_vib_up',		'V34_vib_up',		'V35_vib_up',		'V36_vib_up',		'V37_vib_up',		'V38_vib_up',		'V39_vib_up',		'V40_vib_up',		'V41_vib_up',		'V42_vib_up',		'V43_vib_up',		'V44_vib_up',		'V45_vib_up',		'V46_vib_up',		'V47_vib_up',		'V48_vib_up',		'V49_vib_up',		'V50_vib_up',		'V51_vib_up',		'V52_vib_up',		'V53_vib_up',		'V54_vib_up',		'V55_vib_up',		'V56_vib_up',		'V57_vib_up',		'V58_vib_up',		'V59_vib_up',		'V60_vib_up',		'V61_vib_up',		'V62_vib_up',		'V63_vib_up',		'V64_vib_up',		'V65_vib_up',		'V66_vib_up',		'V67_vib_up',		'V68_vib_up',		'V69_vib_up',		'V70_vib_up',		'V71_vib_up',		'V72_vib_up',		'V73_vib_up',		'V74_vib_up',		'V75_vib_up',		'G1_vib_up',		'G2_vib_up',		'G3_vib_up',		'G4_vib_up',		'G5_vib_up',		'G6_vib_up',		'G7_vib_up',		'G8_vib_up',		'G9_vib_up',		'G10_vib_up',		'G11_vib_up',		'G12_vib_up',		'G13_vib_up',		'G14_vib_up',		'G15_vib_up',		'G16_vib_up',		'G17_vib_up',		'G18_vib_up',		'G19_vib_up',		'G20_vib_up',		'G21_vib_up',		'G22_vib_up',		'G23_vib_up',		'G24_vib_up',		'G25_vib_up',		'G26_vib_up',		'G27_vib_up','G28_vib_up','G29_vib_up','G30_vib_up','G31_vib_up','G32_vib_up','G33_vib_up']
col_t1_vib=['target','index','V1_AC_up',		'V2_AC_up',		'V3_AC_up',		'V4_AC_up',		'V5_AC_up',		'V6_AC_up',		'V7_AC_up',		'V8_AC_up',		'V9_AC_up',		'V10_AC_up',		'V11_AC_up',		'V12_AC_up',		'V13_AC_up',		'V14_AC_up',		'V15_AC_up',		'V16_AC_up',		'V17_AC_up',		'V18_AC_up',		'V19_AC_up',		'V20_AC_up',		'V21_AC_up',		'V22_AC_up',		'V23_AC_up',		'V24_AC_up',		'V25_AC_up',		'V26_AC_up',		'V27_AC_up',		'V28_AC_up',		'V29_AC_up',		'V30_AC_up',		'V31_AC_up',		'V32_AC_up',		'V33_AC_up',		'V34_AC_up',		'V35_AC_up',		'V36_AC_up',		'V37_AC_up',		'V38_AC_up',		'V39_AC_up',		'V40_AC_up',		'V41_AC_up',		'V42_AC_up',		'V43_AC_up',		'V44_AC_up',		'V45_AC_up',		'V46_AC_up',		'V47_AC_up',		'V48_AC_up',		'V49_AC_up',		'V50_AC_up',		'V51_AC_up',		'V52_AC_up',		'V53_AC_up',		'V54_AC_up',		'V55_AC_up',		'V56_AC_up',		'V57_AC_up',		'V58_AC_up',		'V59_AC_up',		'V60_AC_up',		'V61_AC_up',		'V62_AC_up',		'V63_AC_up',		'V64_AC_up',		'V65_AC_up',		'V66_AC_up',		'V67_AC_up',		'V68_AC_up',		'V69_AC_up',		'V70_AC_up',		'V71_AC_up',		'V72_AC_up',		'V73_AC_up',		'V74_AC_up',		'V75_AC_up',		'G1_AC_up',		'G2_AC_up',		'G3_AC_up',		'G4_AC_up',		'G5_AC_up',		'G6_AC_up',		'G7_AC_up',		'G8_AC_up',		'G9_AC_up',		'G10_AC_up',		'G11_AC_up',		'G12_AC_up',		'G13_AC_up',		'G14_AC_up',		'G15_AC_up',		'G16_AC_up',		'G17_AC_up',		'G18_AC_up',		'G19_AC_up',		'G20_AC_up',		'G21_AC_up',		'G22_AC_up',		'G23_AC_up',		'G24_AC_up',		'G25_AC_up',		'G26_AC_up',		'G27_AC_up','G28_AC_up','G29_AC_up','G30_AC_up','G31_AC_up','G32_AC_up','G33_AC_up']
col_t1_ac=['target','index','V1_AC_down',		'V2_AC_down',		'V3_AC_down',		'V4_AC_down',		'V5_AC_down',		'V6_AC_down',		'V7_AC_down',		'V8_AC_down',		'V9_AC_down',		'V10_AC_down',		'V11_AC_down',		'V12_AC_down',		'V13_AC_down',		'V14_AC_down',		'V15_AC_down',		'V16_AC_down',		'V17_AC_down',		'V18_AC_down',		'V19_AC_down',		'V20_AC_down',		'V21_AC_down',		'V22_AC_down',		'V23_AC_down',		'V24_AC_down',		'V25_AC_down',		'V26_AC_down',		'V27_AC_down',		'V28_AC_down',		'V29_AC_down',		'V30_AC_down',		'V31_AC_down',		'V32_AC_down',		'V33_AC_down',		'V34_AC_down',		'V35_AC_down',		'V36_AC_down',		'V37_AC_down',		'V38_AC_down',		'V39_AC_down',		'V40_AC_down',		'V41_AC_down',		'V42_AC_down',		'V43_AC_down',		'V44_AC_down',		'V45_AC_down',		'V46_AC_down',		'V47_AC_down',		'V48_AC_down',		'V49_AC_down',		'V50_AC_down',		'V51_AC_down',		'V52_AC_down',		'V53_AC_down',		'V54_AC_down',		'V55_AC_down',		'V56_AC_down',		'V57_AC_down',		'V58_AC_down',		'V59_AC_down',		'V60_AC_down',		'V61_AC_down',		'V62_AC_down',		'V63_AC_down',		'V64_AC_down',		'V65_AC_down',		'V66_AC_down',		'V67_AC_down',		'V68_AC_down',		'V69_AC_down',		'V70_AC_down',		'V71_AC_down',		'V72_AC_down',		'V73_AC_down',		'V74_AC_down',		'V75_AC_down',		'G1_AC_down',		'G2_AC_down',		'G3_AC_down',		'G4_AC_down',		'G5_AC_down',		'G6_AC_down',		'G7_AC_down',		'G8_AC_down',		'G9_AC_down',		'G10_AC_down',		'G11_AC_down',		'G12_AC_down',		'G13_AC_down',		'G14_AC_down',		'G15_AC_down',		'G16_AC_down',		'G17_AC_down',		'G18_AC_down',		'G19_AC_down',		'G20_AC_down',		'G21_AC_down',		'G22_AC_down',		'G23_AC_down',		'G24_AC_down',		'G25_AC_down',		'G26_AC_down',		'G27_AC_down','G28_AC_down','G29_AC_down','G30_AC_down','G31_AC_down','G32_AC_down','G33_AC_down']

# Dictionnaire regroupant les groupes de colonnes
group_columns = {
    "T0 - Vibration (Down)": col_t0_vib,
    "T0 - Acoutic (Up)": col_t0_ac,
    "T1 - Vibration (Up)": col_t1_vib,
    "T1 - Acoutic (Down)": col_t1_ac,
}
# Set the page configuration
st.set_page_config(page_title="Testeur d'API", layout="wide", page_icon="📊", initial_sidebar_state='expanded')

# Title and Introduction
st.title("✨ Model - Web App")
st.markdown("""
This app allows you to upload your data, test model production.
""")
# Gestion du fichier CSV via session_state
if "data" not in st.session_state:
    st.session_state.data = None
    
with st.sidebar:
    if st.session_state.data is not None:
        st.success("File uploaded!")
        df = st.session_state.data
        # 2. Suppression des colonnes (via la barre latérale)
        st.sidebar.header("Sélectionnez les colonnes à supprimer")
        columns_to_drop = st.sidebar.multiselect("Colonnes disponibles :", options=df.columns.tolist())

        if columns_to_drop:
            df = df.drop(columns=columns_to_drop)
            st.success("Données supprimée")
        st.sidebar.subheader("Filtrer les colonnes à afficher")
        selected_groups = st.sidebar.multiselect(
            "Choisissez les groupes de colonnes à afficher :", 
            group_columns.keys()
        )

        if selected_groups:
            # Liste combinée des colonnes sélectionnées
            selected_columns = [col for group in selected_groups for col in group_columns[group] if col in df.columns]
            df = df[selected_columns]
            st.success("Données filtrées")
if st.session_state.data is not None:
    
    options = ["VisuData", "MODEL"]
    selection = st.segmented_control(
        "Directions", options, selection_mode="single"
    )
    # Preprocess the dataset: Convert dates to numerical features and encode categorical variables
    for col in df.columns:
        if col=="index":
            df.index=df[col]
            df.drop(columns=col,inplace=True)
            continue
        if is_string_dtype(df[col]):
            try:
                df = pd.get_dummies(df, columns=[col], drop_first=True)
            except Exception:
                df = pd.get_dummies(df, columns=[col], drop_first=True)
    # This scales each column to have mean=0 and standard deviation=1
    if selection == "VisuData":
        # Data Preview Section
        st.subheader("Data Preview")
        preview_rows = st.slider("How many rows to display?", 1, 50, 1)
        st.dataframe(df.head(preview_rows))
    if selection == "MODEL":
        # 2. Saisie de l'adresse IP de l'API
        st.subheader("Entrez l'Utilisateur de l'API")
        API_USER = st.text_input("Utilisateur", placeholder="user")
        if API_USER:
            API_PWD = st.text_input("Mot de passe", placeholder="mdp")
            if API_USER != "" and API_PWD != "":
                st.subheader("Entrez l'adresse IP ou l'URL de l'API")
                API_URL = st.text_input("Adresse IP ou URL de l'API", placeholder="http://127.0.0.1:5000")
                ENDPOINT = "/predict"
                if API_URL != '' and API_USER != '' and API_PWD!='':
                    # 3. Bouton pour tester l'API
                    if st.button("Connect to API"):
                        # Send login request to get an access token
                        auth_response = requests.post(API_URL + "/token", data={"username": API_USER, "password": API_PWD})
                        if auth_response.ok:
                            # Extract the access token from the response
                            access_token = json.loads(auth_response.text)["access_token"]
                            # Set headers for authenticated request
                            headers = {"Authorization": f"Bearer {access_token}"}
                            st.write(headers)
                    st.header("Envoyer les données à l'API")
                    preview_rows = st.slider("How many rows to PREDICTS?", 1, 50, 1)
                    if st.button("Tester l'API"):
                        responses = []
                        with st.spinner("Envoi des requêtes..."):
                            for i, row in df[:preview_rows].iterrows():
                                try:
                                    # Conversion des lignes de DataFrame en JSON
                                    json_data = row.to_dict()

                                    # Envoi de la requête POST
                                    response = requests.post(API_URL, json=json_data, headers=headers)
                                    time.sleep(1)
                                    # Ajout de la réponse à la liste des réponses
                                    responses.append({
                                        "Données envoyées": json_data,
                                        "Code de réponse": response.status_code,
                                        "Réponse": response.json() if response.status_code == 200 else response.text
                                    })
                                except Exception as e:
                                    responses.append({
                                        "Données envoyées": json_data,
                                        "Code de réponse": "Erreur",
                                        "Réponse": str(e)
                                    })

                        # 4. Affichage des résultats
                        st.success("Toutes les requêtes ont été envoyées.")
                        st.write("Résultats des requêtes:")
                        st.json(responses)