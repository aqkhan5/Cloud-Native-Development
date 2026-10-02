# Docker CLI Common Commands Reference

A comprehensive quick-reference guide for essential Docker commands used in containerizing and managing FastAPI applications.

---

## 1. Container Lifecycle Commands

| Command | Description |
|---------|-------------|
| `docker run -d -p 8000:8000 --name app <image>` | Run container in background (detached), map host port 8000 to container port 8000 |
| `docker run --rm -it <image> /bin/sh` | Run container interactively with a terminal and auto-remove when stopped |
| `docker run --env-file .env <image>` | Run container injecting environment variables from file |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers (including stopped) |
| `docker stop <container>` | Gracefully stop running container (SIGTERM followed by SIGKILL) |
| `docker start <container>` | Start stopped container |
| `docker restart <container>` | Restart container |
| `docker rm <container>` | Remove stopped container |
| `docker rm -f <container>` | Force-remove running container |

---

## 2. Image Management Commands

| Command | Description |
|---------|-------------|
| `docker build -t <tag> .` | Build Docker image from Dockerfile in current directory |
| `docker build -t <tag> -f <dockerfile> .` | Build specifying a custom Dockerfile path |
| `docker build --no-cache -t <tag> .` | Rebuild image from scratch without reusing cached layers |
| `docker images` | List all local Docker images |
| `docker rmi <image>` | Remove local image |
| `docker tag <source-image> <target-tag>` | Tag an existing image with a new name or version |
| `docker history <image>` | Show build history and layer breakdown for an image |

---

## 3. Inspection & Debugging Commands

| Command | Description |
|---------|-------------|
| `docker logs -f <container>` | Stream container logs in real time |
| `docker logs --tail 100 <container>` | View last 100 log lines |
| `docker exec -it <container> /bin/sh` | Open interactive shell inside running container |
| `docker exec -it <container> python -m pytest` | Run commands (e.g. tests) inside active container |
| `docker inspect <container_or_image>` | Display detailed JSON metadata and runtime settings |
| `docker stats` | Live stream resource usage (CPU, memory, network I/O) |
| `docker top <container>` | Display running processes of a container |
| `docker port <container>` | List port mappings for a container |

---

## 4. Volume & Network Management

| Command | Description |
|---------|-------------|
| `docker volume ls` | List Docker persistent volumes |
| `docker volume create <name>` | Create named volume |
| `docker volume rm <name>` | Delete named volume |
| `docker network ls` | List Docker networks |
| `docker network create <name>` | Create user-defined bridge network |
| `docker network inspect <name>` | Inspect network configuration and connected containers |

---

## 5. System Cleanup Commands

| Command | Description |
|---------|-------------|
| `docker system df` | Display disk usage of containers, images, and volumes |
| `docker container prune -f` | Remove all stopped containers |
| `docker image prune -a -f` | Remove all unused images (not referenced by any container) |
| `docker system prune -a --volumes -f` | **Deep clean**: removes all stopped containers, unused networks, images, and volumes |

---

## 6. Docker Compose Commands

| Command | Description |
|---------|-------------|
| `docker compose up -d` | Start all services in background |
| `docker compose up --build` | Rebuild images before starting services |
| `docker compose -f compose.dev.yaml up` | Start using specific compose configuration |
| `docker compose ps` | Check status of composed services |
| `docker compose logs -f <service>` | Follow logs for a specific service |
| `docker compose exec <service> sh` | Execute command in a service container |
| `docker compose down` | Stop and remove containers and networks |
| `docker compose down -v` | Stop containers, remove networks, and destroy volumes |
| `docker compose watch` | Run Compose Watch for hot-reloading code changes |
