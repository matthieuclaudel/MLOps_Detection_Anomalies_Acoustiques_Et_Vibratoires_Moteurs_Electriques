Détection des anomalies acoustiques et vibratoires des moteurs électriques
==============================

L'objectif de ce projet est d'automatiser la détection d'anomalies sur des moteurs électriques à la sortie d'une chaîne de production.

## Equipe projet

- Ludovic ANDRIEUX [GitHub](https://github.com/ludodo23)
- Matthieu CLAUDEL ([GitHub](https://github.com/matthieuclaudel) / [LinkedIn](http://www.linkedin.com/in/matthieu-claudel-8a927857))
- Adrien PINEL [GitHub](https://github.com/Adriencalvados) / [LinkedIn](www.linkedin.com/in/adrien-pinel-machine-learning-ingenieur)
- Harold MOUKALA MITATI [GitHub](https://github.com/Ngulumanua)

## Architecture de l'application

![Architecture](./data/Archi.png)

## Repository Tree

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── logs               <- Logs from training and predicting
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   ├── visualization  <- Scripts to create exploratory and results oriented visualizations
    │   │   └── visualize.py
    │   └── config         <- Describe the parameters used in train_model.py and predict_model.py

--------

## Installation
## 🎬 Getting Started for Developers

```shell
git clone https://github.com/matthieuclaudel/MLOps_Detection_Anomalies_Acoustiques_Et_Vibratoires_Moteurs_Electriques
```


---

## Table des Matières

1. [Installation](#installation)
2. [Utilisation](#utilisation)
3. [Conteneurs Docker](#conteneurs-docker)
4. [Prérequis](#prérequis)
5. [Installation Kubernetes](#installation-kubernetes)
6. [Orchestration et Charts Helm](#orchestration-et-charts-helm)
7. [Configuration des Redirections avec Traefik](#configuration-des-redirections-avec-traefik)
8. [Évaluation et Surveillance](#évaluation-et-surveillance)
9. [Pods Créés](#pods-créés)
10. [Architecture Globale](#architecture-globale)
11. [Contributions](#contributions)
12. [Licence](#licence)
13. [Remerciements](#remerciements)

---

## Installation

### Étapes d'installation

🔧 **Cloner le dépôt GitHub :**

```bash
git clone https://github.com/matthieuclaudel/MLOps_Detection_Anomalies_Acoustiques_Et_Vibratoires_Moteurs_Electriques.git
```

💻 **Naviguer dans le répertoire du projet :**

```bash
cd MLOps_Detection_Anomalies_Acoustiques_Et_Vibratoires_Moteurs_Electriques
```

🛠️ **Créer et activer un environnement virtuel Python :**

```bash
python3 -m venv venv
source venv/bin/activate
```

📦 **Installer les dépendances :**

```bash
pip install -r requirements.txt
```

---

## Utilisation

1. **Activer l'environnement virtuel :**

```bash
source venv/bin/activate
```

2. **Lancer l'application :**

```bash
python main.py
```

⚙️ **Fonction principale :** Lors de son exécution, le script `main.py` récupère les données depuis DVC, crée les ensembles X\_test, X\_train, Y\_test, et Y\_train dans les dossiers `data`, applique une transformation avec un standard scaler, entraîne un modèle, et le stocke dans Dagshub (MLflow Cloud). 🚀

3. **Accéder à l'application via votre navigateur :**

Par exemple : `http://localhost:3000`. 🌐

---

## Conteneurs Docker

### Conteneurs disponibles

🚢 **Créer un réseau de bridge :**

```bash
docker network create bridge_test_container
```

🛠️ **API FastAPI (root URL : /api) :**

```bash
docker build -t adrien157/api -f docker/dockerfile.app_model .
docker push adrien157/api:latest
docker run --rm --name api --env-file .env -p 30001:30001 --network bridge_test_container adrien157/api:latest
```
![Architecture fastapi](./images/Diagramme-2025-01-06-2022.png)
🌐 **Simulation de requêtes :**

```bash
docker build -t adrien157/simulation_request_model -f docker/dockerfile.app_simu .
docker push adrien157/simulation_request_model:latest
docker run --rm --name simu_request --env-file .env --network bridge_test_container adrien157/simulation_request_model:latest
```

📊 **Application Streamlit :**

```bash
docker build -t adrien157/app_streamlit -f docker/dockerfile.app_streamlit .
docker push adrien157/app_streamlit:latest
docker run --rm --name app_streamlit --env-file .env -p 8501:8501 --network bridge_test_container adrien157/app_streamlit:latest
```

---

## Prérequis

Pour utiliser ce projet, vous aurez besoin de :

- Un compte [DagsHub](https://dagshub.com/) 🖥️
- Un compte [Docker](https://www.docker.com/) 🐳
- Une machine avec Debian installé 🖧
- Kubernetes K3S installé ☸️

---

## Installation Kubernetes

### Étapes d'installation avec Helm

🔨 **Installer Helm :**

```bash
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```

📋 **Configurer Kubernetes avec K3S :**

```bash
curl -sfL https://get.k3s.io | sh -
```

🚀 **Déployer des applications avec Helm :**

```bash
helm repo add stable https://charts.helm.sh/stable
helm repo update
helm install my-app stable/chart-name
```

---

## Orchestration et Charts Helm

### Exemple de déploiement avec Minikube

🌐 **Activer les ports nécessaires :**

```bash
minikube service multi-port-service-public --url
```

Ou démarrer Minikube avec des ports spécifiques :

```bash
minikube start --driver=docker --ports 30000:30000 --ports 30001:30001 \
--ports 30002:30002 --ports 30003:30003 --ports 30004:30004 \
--ports 8081:8081 --ports 30005:30005 --ports 27017:27017
```

📈 **Prometheus Stack :**

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install my-kube-prometheus-stack prometheus-community/kube-prometheus-stack --version 66.3.1
```

✈️ **Apache Airflow :**

```bash
helm repo add apache-airflow https://airflow.apache.org/
helm repo update
helm install my-airflow apache-airflow/airflow --version 1.15.0
```

---

## Configuration des Redirections avec Traefik

### Routes Configurées

| Service       | URL de Redirection                   | Port  |
| ------------- | ------------------------------------ | ----- |
| **FastAPI**   | `https://inteva.hopto.org/api`       | 30001 |
| **Streamlit** | `https://inteva.hopto.org/streamlit` | 30002 |
| **Airflow**   | `https://inteva.hopto.org/airflow`   | 30003 |
| **Grafana**   | `https://inteva.hopto.org/grafana`   | 30004 |

---

## Évaluation et Surveillance

### Évaluation en Production

📝 Le modèle est évalué à l'aide de fichiers test.csv étiquetés manuellement. Ces fichiers servent à mesurer la précision et la robustesse des prédictions dans un environnement simulé proche de la production. 📊

### Réentraînement

🔄 Les données collectées par FastAPI sont intégrées dans MongoDB avec des métadonnées comme l'heure, le résultat des prédictions et les mesures associées.

- Airflow se charge de récupérer ces données pour effectuer des étapes de transformation comme la standardisation via un scaler.
- Une fois prêtes, les données sont stockées dans InfluxDB pour un usage ultérieur dans les phases de réentraînement.
- Un nouveau modèle validé est automatiquement rechargé dans les pods concernés après chaque itération de réentraînement. ⚡

### Collecte et CI/CD

1. Airflow applique des pipelines CI/CD pour intégrer des processus automatisés d'entraînement et de déploiement.
2. Une surveillance continue permet de détecter les anomalies dans les données et d'améliorer les performances des modèles au fil du temps. 🛠️

### Surveillance des Performances

📉 Le stack Prometheus et Grafana permet de suivre :

- Les métriques issues de FastAPI, MongoDB et InfluxDB.
- Les performances des ressources matérielles comme le CPU, la RAM et les disques.
- Les volumes de requêtes et les latences pour chaque service.
- Des alertes configurées pour détecter les anomalies ou les baisses de performance. 🚨

---

## Pods Créés

🚀 Voici les pods actifs et leurs fonctions principales :

- **alertmanager-my-kube-prometheus-stack-alertmanager-0** : Supervision des alertes Prometheus.
- **app-streamlit-deployment-599d5b7b5f-xcckj** : Interface utilisateur pour la visualisation des prédictions.
![-](./images/Capture_streamlit.jpg)

- **curl-pod** : Outil de diagnostic pour tester les communications entre services.
- **model-deployment-674988f5c7-q8pw7** : Déploiement du modèle ML pour les prédictions.
![-](./images/Capture_fastapi_root.jpg)
![-](./images/Capture_fastapi_docs.jpg)

- **my-airflow-postgresql-0** : Base de données pour Apache Airflow.
- **my-airflow-redis-0** : Cache Redis utilisé par Airflow.
- **my-airflow-scheduler-579d984dd7-9xh99** : Gestion des tâches planifiées.
- **my-airflow-statsd-66699fb8b9-rxlg6** : Collecte des statistiques d'Airflow.
![-](./images/Capture_airflow_dags.jpg)
- **grafana**
![-](./images/Capture_grafana.jpg)
---

## Architecture Globale

🎨 **Schéma de l'architecture technique** :

1. API FastAPI pour la gestion des prédictions et des utilisateurs.
2. Pipeline CI/CD pour l'entraînement et le déploiement automatisé.
3. Monitoring centralisé avec Grafana et Prometheus.
4. Orchestration des services avec Kubernetes et Helm.
5. Stockage des données avec MongoDB et InfluxDB.

---

## Contributions

🤝 Les contributions sont les bienvenues ! Veuillez soumettre vos propositions via des pull requests sur le dépôt GitHub.

---