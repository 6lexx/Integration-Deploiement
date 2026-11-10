# TP Docker – Exercice 5 : application Python Flask

Application web minimale développée avec **Flask** et conteneurisée avec **Docker**.
---

## Étapes de réalisation

### 1. Création de la branche de travail

```powershell
git checkout -b appPythonFlask
```

### 2. Environnement virtuel Python (test en local)

Le développement est réalisé dans un environnement virtuel, afin d'isoler les dépendances du projet du reste de la machine.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install flask
```

### 3. Écriture de l'application – `app.py`

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World"

if __name__ == "__main__":
    app.run(app.run(host="0.0.0.0", port=5173)
```


```powershell
python app.py
```

L'application est accessible sur <http://127.0.0.1:5173>.

### 4. Dépendances – `requirements.txt`

```
flask
```

### 5. Fichiers d'exclusion

**`.gitignore`** – fichiers à ne pas versionner :

```
venv/
__pycache__/
*.pyc
```

**`.dockerignore`** – fichiers à ne pas copier dans l'image :

```
venv/
__pycache__/
.git/
```

### 6. Écriture du `Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

### 7. Construction de l'image

```powershell
docker build -t mon-app-flask .
```

- `-t mon-app-flask` : nom donné à l'image
- `.` : le `Dockerfile` se trouve dans le dossier courant

Vérification :

```powershell
docker images
```

### 8. Lancement du conteneur

```powershell
docker run -d -p 5173:5173 --name mon_flask mon-app-flask
```

Vérification :

```powershell
docker ps
```

### 9. Test dans le navigateur

Ouvrir <http://localhost:5173> : la page affiche **Hello World**.

En cas de problème :

```powershell
docker logs mon_flask
```

### 10. Arrêt et suppression du conteneur

```powershell
docker stop mon_flask
docker rm mon_flask
```

### 11. Versionnement

```powershell
git add app.py requirements.txt Dockerfile .dockerignore .gitignore README.md
git commit -m "Application Flask conteneurisée avec Docker"
git push -u origin appPythonFlask
```


### 12. Fusion dans la branche `main`

Une fois validé, la branche `appPythonFlask` est fusionnée dans `main`.

**Mettre la branche de travail à jour et la pousser :**

```powershell
git pull --rebase
git push
```

**Se placer sur `main` et la mettre à jour :**

```powershell
git checkout main
git pull
```

**Fusionner la branche de travail :**

```powershell
git merge appPythonFlask
```

**Pousser `main` :**

```powershell
git push
```