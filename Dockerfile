# Utiliser l'image Python officielle légère
FROM python:3.11-slim

# Définir le mainteneur
LABEL maintainer="zaynaberreghay@gmail.com"

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements en premier (pour le cache Docker)
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY app.py .

# Créer un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Exposer le port 8080 (standard pour Cloud Run)
EXPOSE 8080

# Variables d'environnement par défaut
ENV PORT=8080
ENV ENV=production

# Commande de démarrage avec Gunicorn
# 4 workers, timeout de 120 secondes
CMD exec gunicorn --bind :$PORT --workers 4 --threads 2 --timeout 120 --access-logfile - --error-logfile - app:app
