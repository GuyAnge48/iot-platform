# Dockerfile — IoT Platform
# Utilise Python 3.12 slim (image légère, stable, compatible avec toutes nos dépendances)
# Python 3.14 n'a pas encore d'image Docker officielle stable — 3.12 est identique pour notre projet

FROM python:3.12-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie d'abord requirements.txt seul pour profiter du cache Docker
# Si les dépendances ne changent pas, Docker réutilise cette couche sans réinstaller
COPY requirements.txt .

# Installe les dépendances Python
# --no-cache-dir réduit la taille de l'image
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le reste du projet dans le conteneur
# (app/, templates/, static/)
COPY . .

# Expose le port utilisé par Uvicorn
EXPOSE 8000

# Commande de démarrage
# --host 0.0.0.0 obligatoire pour que le conteneur soit accessible depuis l'extérieur
# --port 8000 correspond à l'EXPOSE ci-dessus
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
