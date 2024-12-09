import streamlit as st
import pandas as pd
import csv

def read_csv_file(file,separator):
    """
    Lecture robuste d'un fichier CSV avec détection automatique des séparateurs.
    :param file: fichier téléchargé
    :return: DataFrame pandas
    """
    try:
        # Utilise le module csv pour détecter le délimiteur
        sample = file.read(1024).decode('utf-8')
        file.seek(0)  # Remet le curseur au début
        dialect = csv.Sniffer().sniff(sample, delimiters=",;|")
        
        # Lit le CSV avec le délimiteur détecté
        df = pd.read_csv(file, delimiter=dialect.delimiter,decimal=separator)
        return df
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
        return None
    
st.set_page_config(
    page_title="Évaluation Acoustique",
    page_icon="👋",
)

# Titre principal
st.title("Projet MLOps : Système d'Évaluation Acoustique Basé sur l'IA")

# Sous-titre ou slogan
st.subheader("Révolutionner le contrôle de la qualité acoustique grâce à l'intelligence artificielle")

# Description du contexte
st.markdown("""
**Contexte :**  
L'entreprise vise à moderniser son système d'évaluation acoustique actuel, devenu obsolète et difficile à maintenir.  
L'objectif est de **réduire les faux négatifs** lors des contrôles qualité tout en optimisant les performances des lignes de production.
""")

# Objectifs principaux
st.markdown("""
**Objectifs du projet :**
- Déployer un modèle d'IA avancé pour améliorer la précision des diagnostics acoustiques.
- Assurer une **mise à jour adaptative** des modèles en fonction des variations des conditions de production.
- Fournir une **interface de contrôle** avec un retour en temps réel via une API.
- Intégrer le nouveau système à l'infrastructure actuelle (Kubernetes, Grafana).
""")

# Synthèse des bénéfices
st.markdown("""
**Bénéfices attendus :**
- Réduction des erreurs de détection (faux négatifs).
- Meilleure fiabilité des diagnostics.
- Optimisation des processus de production et de contrôle.
""")

# Footer ou mention importante
st.info("Ce projet est réalisé en collaboration avec les équipes Méthodes Industrielles et les experts en acoustique.")
# Gestion du fichier CSV via session_state
if "data" not in st.session_state:
    st.session_state.data = None
with st.sidebar:
    st.header("Upload and Select Data")
    separator = st.selectbox("Sélectionnez un séparateur décimal", [",", "."])
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    if uploaded_file is not None:
        df = read_csv_file(uploaded_file,separator)
        if df is not None:
            # Vérifier si la colonne "Target" existe
            if "target" not in df.columns:
                # Ajouter la colonne avec une valeur par défaut de 0
                df["target"] = 0
                st.info("La colonne 'target' a été ajoutée avec des valeurs par défaut à 0.")

            st.session_state.data = df
            st.success("File successfully uploaded!")