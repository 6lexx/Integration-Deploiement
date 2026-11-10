# Integration-Deploiement

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