# Compte rendu – TP Docker

> Les identifiants (ID d'images, ID de conteneurs, digests et hashs `sha256`) ont été masqués.

---

## 1. Vérifier la version de Docker

```powershell
PS C:\Users\matth> docker --version
```

```text
Docker version 27.4.0, build <BUILD_ID>
```

---

## 2. Lister les images présentes en local

```powershell
PS C:\Users\matth> docker images
```

```text
REPOSITORY      TAG          IMAGE ID       CREATED         SIZE
tp2-frontend    latest       <IMAGE_ID>     20 months ago   48.2MB
tp2-frontend2   latest       <IMAGE_ID>     20 months ago   522MB
sonarqube       community    <IMAGE_ID>     20 months ago   1.17GB
tp2-backend     latest       <IMAGE_ID>     21 months ago   136MB
postgres        12           <IMAGE_ID>     23 months ago   419MB
mariadb         10.6-focal   <IMAGE_ID>     2 years ago     396MB
```

---

## 3. Télécharger l'image `hello-world`

```powershell
PS C:\Users\matth> docker pull hello-world
```

```text
Using default tag: latest
latest: Pulling from library/hello-world
<LAYER_ID>: Pull complete
Digest: sha256:<DIGEST>
Status: Downloaded newer image for hello-world:latest
docker.io/library/hello-world:latest

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview hello-world
```

---

## 4. Lancer un conteneur à partir de `hello-world`

```powershell
PS C:\Users\matth> docker run hello-world
```

```text
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

---

## 5. Lister les conteneurs en cours d'exécution

```powershell
PS C:\Users\matth> docker ps
```

```text
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

---

## 6. Lister tous les conteneurs (y compris arrêtés)

```powershell
PS C:\Users\matth> docker ps -a
```

```text
CONTAINER ID     IMAGE                 COMMAND                  CREATED          STATUS                       PORTS                    NAMES
<CONTAINER_ID>   hello-world           "/hello"                 48 seconds ago   Exited (0) 47 seconds ago                             cranky_fermat
<CONTAINER_ID>   sonarqube:community   "/opt/sonarqube/dock…"   20 months ago    Exited (255) 5 minutes ago   0.0.0.0:9000->9000/tcp   sonar-sonarqube-1
<CONTAINER_ID>   postgres:12           "docker-entrypoint.s…"   20 months ago    Exited (255) 5 minutes ago   5432/tcp                 sonar-db-1
<CONTAINER_ID>   mariadb:10.6-focal    "docker-entrypoint.s…"   20 months ago    Exited (255) 5 minutes ago   3306/tcp                 tp2-bdd-1
<CONTAINER_ID>   tp2-frontend          "/docker-entrypoint.…"   20 months ago    Exited (255) 5 minutes ago   0.0.0.0:8081->80/tcp     tp2-frontend-1
<CONTAINER_ID>   tp2-frontend2         "docker-entrypoint.s…"   20 months ago    Exited (255) 5 minutes ago   0.0.0.0:8082->8081/tcp   tp2-frontend2-1
<CONTAINER_ID>   tp2-backend           "docker-entrypoint.s…"   20 months ago    Exited (255) 5 minutes ago   0.0.0.0:8080->8080/tcp   tp2-backend-1
```

---

## 7. Supprimer le conteneur `hello-world`

```powershell
PS C:\Users\matth> docker rm <CONTAINER_ID>
```

```text
<CONTAINER_ID>
```

---

## 8. Supprimer l'image `hello-world`

```powershell
PS C:\Users\matth> docker rmi <IMAGE_ID>
```

```text
Untagged: hello-world:latest
Untagged: hello-world@sha256:<DIGEST>
Deleted: sha256:<IMAGE_HASH>
Deleted: sha256:<LAYER_HASH>
```

---

## Récapitulatif des commandes

| Commande | Rôle |
|---|---|
| `docker --version` | Affiche la version de Docker installée |
| `docker images` | Liste les images présentes en local |
| `docker pull <image>` | Télécharge une image depuis Docker Hub |
| `docker run <image>` | Crée et lance un conteneur à partir d'une image |
| `docker ps` | Liste les conteneurs en cours d'exécution |
| `docker ps -a` | Liste tous les conteneurs, y compris arrêtés |
| `docker rm <id>` | Supprime un conteneur |
| `docker rmi <id>` | Supprime une image |
