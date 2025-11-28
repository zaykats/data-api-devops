# API de Données DevOps - Démonstration GCP

API REST simple pour démontrer un pipeline CI/CD complet sur Google Cloud Platform.

## 🏗️ Architecture
```
GitHub → Cloud Build → Artifact Registry → Cloud Run
```

## 🚀 Technologies

- **Backend**: Python 3.11 + Flask
- **Conteneurisation**: Docker
- **CI/CD**: Cloud Build
- **Registry**: Artifact Registry
- **Déploiement**: Cloud Run
- **Monitoring**: Cloud Logging + Cloud Monitoring

## 📋 Prérequis

- Compte Google Cloud Platform
- Projet GCP créé
- `gcloud` CLI installé
- Git et GitHub configurés

## 🛠️ Installation Locale

1. Cloner le repository:
```bash
git clone https://github.com/votre-username/data-api-devops.git
cd data-api-devops
```

2. Créer un environnement virtuel:
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installer les dépendances:
```bash
pip install -r requirements.txt
```

4. Lancer l'application:
```bash
python app.py
```

5. Tester l'API:
```bash
curl http://localhost:8080/
curl http://localhost:8080/data
curl http://localhost:8080/health
```

## ☁️ Déploiement sur GCP

### Étape 1: Configuration du Projet
```bash
# Définir le projet
export PROJECT_ID="devops-demo-api"
gcloud config set project $PROJECT_ID

# Activer les APIs nécessaires
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
```

### Étape 2: Créer Artifact Registry
```bash
gcloud artifacts repositories create data-api-repo \
    --repository-format=docker \
    --location=europe-west1 \
    --description="Demo API repository"
```

### Étape 3: Configurer les Permissions
```bash
# Récupérer le numéro du projet
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
    --role=roles/run.admin

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
    --role=roles/iam.serviceAccountUser

gcloud iam service-accounts add-iam-policy-binding \
    $PROJECT_NUMBER-compute@developer.gserviceaccount.com \
    --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
    --role=roles/iam.serviceAccountUser
```

### Étape 4: Connecter GitHub à Cloud Build

1. Aller dans Cloud Console → Cloud Build → Triggers
2. Cliquer sur "Connect Repository"
3. Sélectionner GitHub et suivre les instructions
4. Créer un trigger:
   - Nom: `deploy-data-api-production`
   - Événement: Push to branch
   - Branche: `^main$`
   - Configuration: `cloudbuild.yaml`

### Étape 5: Déployer
```bash
# Commit et push
git add .
git commit -m "Initial deployment"
git push origin main
```

Le déploiement se lance automatiquement!

## 🧪 Tests de l'API Déployée
```bash
# Remplacer URL par votre URL Cloud Run
export API_URL="https://data-api-xxxxx-ew.a.run.app"

# Test de base
curl $API_URL/

# Récupérer les données
curl $API_URL/data

# Vérifier la santé
curl $API_URL/health

# Recherche
curl "$API_URL/api/v1/search?q=Produit"

# Données par ID
curl $API_URL/data/1
```

## 📊 Endpoints Disponibles

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Page d'accueil |
| `/health` | GET | Vérification de santé |
| `/data` | GET | Liste tous les produits |
| `/data/:id` | GET | Produit spécifique |
| `/stats` | GET | Statistiques |
| `/api/v1/search?q=` | GET | Recherche |

## 📈 Monitoring

### Logs
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=data-api" --limit 50
```

### Métriques
Aller dans Cloud Console → Cloud Run → data-api → Metrics

## 🔄 Workflow de Développement

1. Créer une branche:
```bash
git checkout -b feature/nouvelle-fonctionnalite
```

2. Faire vos modifications

3. Tester localement:
```bash
python app.py
```

4. Commit et push:
```bash
git add .
git commit -m "Ajout de nouvelle fonctionnalité"
git push origin feature/nouvelle-fonctionnalite
```

5. Créer une Pull Request sur GitHub

6. Après merge dans `main`, le déploiement est automatique

## 🎯 Démonstration

Pour la démo, modifier `API_VERSION` dans `app.py`:
```python
API_VERSION = "1.1.0"  # Changer cette ligne
```

Puis:
```bash
git add app.py
git commit -m "Update: Version 1.1.0"
git push origin main
```

Suivre le build dans Cloud Console!

## 🛡️ Sécurité

- ✅ Application tourne avec utilisateur non-root
- ✅ HTTPS automatique sur Cloud Run
- ✅ Scanning de vulnérabilités dans Artifact Registry
- ✅ Pas de secrets dans le code
- ✅ IAM pour contrôle d'accès

## 💰 Coûts Estimés

- Cloud Build: 120 min/jour gratuit
- Cloud Run: Gratuit jusqu'à 2M requêtes/mois
- Artifact Registry: 0.5 GB gratuit

**Coût mensuel estimé: < 5€ pour usage de démo**

## 📚 Ressources

- [Documentation Cloud Build](https://cloud.google.com/build/docs)
- [Documentation Cloud Run](https://cloud.google.com/run/docs)
- [Artifact Registry Guide](https://cloud.google.com/artifact-registry/docs)

## 👤 Auteur

[Votre Nom] - Présentation DevOps GCP

## 📝 Licence

Ce projet est à usage éducatif.