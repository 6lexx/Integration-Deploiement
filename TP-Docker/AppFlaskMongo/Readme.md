# TP Docker – Exercice 6 : Docker Compose avec Flask et MongoDB

Application web **Flask** connectée à une base de données **MongoDB**, les deux services étant orchestrés avec **Docker Compose**.

## Structure du projet

```
AppFlaskMongo/
├── .gitignore            # Fichiers exclus du dépôt Git
├── .dockerignore         # Fichiers exclus de l'image Docker
├── requirements.txt      # Dépendances Python
├── app.py                # Application Flask + connexion MongoDB
├── Dockerfile            # Construction de l'image de l'application
├── docker-compose.yml    # Orchestration des services web et mongo
└── README.md
```

## Architecture

Docker Compose crée un réseau commun dans lequel chaque service est joignable par son nom. L'application Flask se connecte donc à la base via l'adresse `mongo:27017`, et non `localhost`.

---

## Étapes de réalisation


### 0. Création de la branche de travail

```powershell
git checkout main
git pull
git checkout -b features-docker-compose
```

### 1. Initialisation du dossier

```powershell
cd TP-Docker
mkdir AppFlaskMongo
cd AppFlaskMongo
```

**`.gitignore`**

```
venv/
__pycache__/
*.pyc
```

**`.dockerignore`**

```
venv/
__pycache__/
.git/
```

```powershell
git add .gitignore .dockerignore
git commit -m "Init du dossier AppFlaskMongo"
```

### 2. Dépendances – `requirements.txt`

```
flask
pymongo
```

`pymongo` est le driver Python officiel pour se connecter à MongoDB.

```powershell
git add requirements.txt
git commit -m "ajout des dépendences avec requirements.txt"
```

### 3. Application Flask de base – `app.py`

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5174)
```

```powershell
git add app.py
git commit -m "ajout de l'application Flask de base"
```

### 4. Connexion à MongoDB et route de test

`app.py` est complété avec la connexion à la base et une route `/db` qui vérifie la connexion :

```python
import os
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
db = client["tpdb"]


@app.route("/")
def hello():
    return "Hello World"


@app.route("/db")
def test_db():
    try:
        client.admin.command("ping")
        db.visites.insert_one({"message": "visite"})
        nb = db.visites.count_documents({})
        return f"Connexion MongoDB OK - {nb} visite(s) enregistrée(s)"
    except Exception as e:
        return f"Erreur de connexion MongoDB : {e}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5174)
```

```powershell
git add app.py
git commit -m "ajout de la connexion MongoDB et de la route /db"
```

### 5. Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5174

CMD ["python", "app.py"]
```

Test de construction de l'image :

```powershell
docker build -t app-flask-mongo .
```

```text
[+] Building 10.6s (11/11) FINISHED
 => [3/5] COPY requirements.txt .
 => [4/5] RUN pip install --no-cache-dir -r requirements.txt
 => [5/5] COPY app.py .
 => => naming to docker.io/library/app-flask-mongo
```

```powershell
git add Dockerfile
git commit -m "ajout du Dockerfile"
```

### 6. Docker Compose – `docker-compose.yml`

```yaml
services:
  web:
    build: .
    ports:
      - "5174:5174"
    environment:
      - MONGO_URI=mongodb://mongo:27017/
    depends_on:
      - mongo

  mongo:
    image: mongo:7
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

#### Lancement

```powershell
docker compose up -d --build
```

```text
[+] Running 4/4
 ✔ Network appflaskmongo_default      Created
 ✔ Volume "appflaskmongo_mongo_data"  Created
 ✔ Container appflaskmongo-mongo-1    Started
 ✔ Container appflaskmongo-web-1      Started
```

Docker Compose a créé :

- un **réseau** commun aux deux services ;
- un **volume** pour les données MongoDB ;
- les **deux conteneurs** `web` et `mongo`.

#### Vérification des conteneurs

```powershell
docker compose ps
```

```text
NAME                    IMAGE               COMMAND                  SERVICE   STATUS          PORTS
appflaskmongo-mongo-1   mongo:7             "docker-entrypoint.s…"   mongo     Up 33 seconds   27017/tcp
appflaskmongo-web-1     appflaskmongo-web   "python app.py"          web       Up 33 seconds   0.0.0.0:5174->5174/tcp
```

Les deux conteneurs sont à l'état `Up`. Seul le service `web` expose un port vers la machine. MongoDB n'est accessible que depuis le réseau interne.

#### Vérification de la connexion à la base

1. Ouvrir <http://localhost:5174> : la page affiche **Hello World**.
2. Ouvrir <http://localhost:5174/db> : la page affiche **Connexion MongoDB OK - 1 visite(s) enregistrée(s)**.
3. Vérifier directement dans MongoDB que le document a bien été écrit :

```powershell
docker compose exec mongo mongosh --eval "db.getSiblingDB('tpdb').visites.find()"
```

```text
[ { _id: ObjectId('<ID>'), message: 'visite' } ]
```

Le document inséré par l'application Flask est bien présent dans la base `tpdb` : **la connexion entre les deux conteneurs fonctionne.**

```powershell
git add docker-compose.yml
git commit -m "ajout du docker-compose avec les services web"
```

### 7. Push de la branche

```powershell
git push -u origin features-docker-compose
```

### 8. Arrêt de l'environnement

```powershell
docker compose down
```

### 9. Fusion dans `main`

```powershell
git checkout main
git pull
git merge features-docker-compose
git push
```

---

## Historique des commits

```
ajout du docker-compose avec les services web
ajout du Dockerfile
ajout de la connexion MongoDB et de la route /db
ajout de l'application Flask de base
ajout des dépendences avec requirements.txt
Init du dossier AppFlaskMongo
+ ajoute du Readme.md
```