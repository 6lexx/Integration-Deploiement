# Mesures – step-0 (baseline)

| Mesure | step-0 |
|---|---|
| Taille image | 1.32 Go |
| Couches | 13 |
| Build à froid | 61.8 s |
| Rebuild après modif de server.js | 27.6 s |
| RAM au repos | 20,1 Mo |
| Temps de docker stop | 10,3 s |
| Utilisateur | root |
| GET /big (fichier absent) | 200 au lieu de 404 |
| Build sans `npm install` préalable | échec (COPY node_modules) |