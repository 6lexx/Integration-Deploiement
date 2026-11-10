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