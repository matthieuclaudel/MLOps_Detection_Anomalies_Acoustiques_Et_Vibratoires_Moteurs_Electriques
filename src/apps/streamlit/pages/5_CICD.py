import streamlit as st
import requests
import json

# Set the page configuration
st.set_page_config(page_title="CI-CD", layout="wide", page_icon="📊", initial_sidebar_state='expanded')

# Title and Introduction
st.title("CI-CD")
st.markdown("""
This app is to CI/CD process.
""")

# Input for Airflow API details
st.subheader("Trigger Airflow DAG")
airflow_url = st.text_input("Airflow URL", "http://82.67.110.221:30003")
dag_id = st.text_input("train_model_dag", "train_model_dag")
username = st.text_input("Username", "admin")
password = st.text_input("Password", type="password")

if st.button("Lancer un réentrainement du modèle"):
    # Trigger the DAG
    auth = (username, password)
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{airflow_url}/api/v1/dags/{dag_id}/dagRuns", auth=auth, headers=headers, data=json.dumps({}))

    if response.status_code == 200:
        st.success(f"DAG {dag_id} triggered successfully!")
    else:
        st.error(f"Failed to trigger DAG {dag_id}. Response: {response.text}")