# Utiliser une image Python de base
FROM python:3.12-bullseye

# Installer les dépendances nécessaires
RUN pip install --no-cache-dir pymongo pandas

# Définir le répertoire de travail
WORKDIR /app

# Copier le script Python dans le conteneur
COPY raw_data.py /app/raw_data.py

# Définir la commande d'exécution par défaut
ENTRYPOINT ["python", "/app/raw_data.py"]