# Integration-Deploiement - TP Optimisation Docker

## Analyse du Dockerfile

Nom du fichier
- Le fichier ne suit pas la convention de base "Dockerfile" avec une majuscule

FROM node:latest
- la version d'import de node n'est pas figée. Cela rend le projet vulnérable en cas de mise à jour de version.

COPY node_modules ./node_modules
- le docker file copie les modules de Node installé sur le poste Windows dans une image Linux. Cette action est inutile, car npm install suit

COPY . /app sans .dockerignore
- effectue une copie des nodes_modules une deuxième fois, action pas utile

COPY . avant npm install
- Une modification du code invalide le cache, toutes les dépendances sont réinstallées à chaque build

apt-get install build-essential locales...
- Les paquets sont inutiles, aucun module natif n'est compilé.

EXPOSE 3000 4000 5000
- Seul le port 3000 est utilisé, 4000 et 5000 inutiles

ENV NODE_ENV=development
- Express est plus lent et plus bavard en mode développement

RUN npm run build
- Le script ne fait qu’un echo : c’est une couche inutile

USER root
- le conteneur tourne en root, cela pose un problème de sécurité

## Analyse du code

"mongodb" dans package.json
- la dépendance n'est jamais utilisée dans server.js : elle ajoute environ 9 Mo et 11 paquets à l'image pour rien

"nodemon" dans devDependencies
- il n'est utilisé dans aucun script, et npm install l'installe quand même dans l'image alors que le conteneur démarre avec node

"build" dans package.json
- le script ne fait qu'un echo, il ne compile et ne génère rien

app.use(console.log...)
- il y a un log sur chaque requête, même en production. console.log est synchrone et ralentit le serveur sous charge

fs.existsSync + fs.readFileSync sur /big
- les deux appels sont synchrones et bloquent tout le serveur pendant la lecture. Le fichier entier est chargé en mémoire, puis copié une deuxième fois par le replace

res.send('Fichier introuvable')
- le fichier maybe-big-file.txt n'existe pas dans le projet, la route répond toujours "Fichier introuvable" mais avec un code 200 au lieu d'un 404

app.listen sans gestion du SIGTERM
- dans le conteneur, node tourne en PID 1 et ignore le SIGTERM : docker stop attend 10 secondes avant de tuer le processus, et les requêtes en cours sont coupées

En-tête X-Powered-By
- Express envoie "X-Powered-By: Express" par défaut, ce qui indique la technologie utilisée à un éventuel attaquant
