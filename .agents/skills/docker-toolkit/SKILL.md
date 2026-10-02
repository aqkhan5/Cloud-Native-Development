---
name: docker-toolkit
description: Comprehensive Docker toolkit for containerizing and deploying Python and FastAPI applications. Use when containerizing FastAPI services, generating or optimizing Dockerfiles, configuring multi-container Docker Compose architectures, implementing multi-stage builds with uv or pip, hardening container security with non-root users, or executing Docker CLI workflows.
license: Complete terms in LICENSE.txt
---

# Docker Toolkit for Python & FastAPI Applications

A comprehensive toolkit to containerize FastAPI applications from single-file prototypes to hardened, production-grade deployments based on official Docker and FastAPI standards.

---

## Workflow Decision Tree

Before creating container assets, determine the project scope and package manager:

```
FastAPI Project Scope
  ├── 1. Prototyping / Single File (main.py, learning, hello world)
  │      └── Action: Use assets/Dockerfile.simple or assets/Dockerfile.fastapi.template
  │          • Single-stage python:3.12-slim
  │          • fastapi run or uvicorn main:app
  │
  ├── 2. Modern uv-based Project (pyproject.toml, uv.lock)
  │      └── Action: Use assets/Dockerfile.uv
  │          • Multi-stage build with ghcr.io/astral-sh/uv
  │          • Bind & cache mounts (uv sync --frozen --no-install-project)
  │          • Non-root runtime user (UID 10001)
  │
  ├── 3. Production pip-based Project (requirements.txt)
  │      └── Action: Use assets/Dockerfile.production
  │          • Multi-stage build with build-essential separation
  │          • Pre-built virtual environment (/opt/venv)
  │          • Non-root execution & curl healthcheck
  │
  └── 4. Multi-Service Infrastructure (API + Postgres + Redis)
         ├── Development: Use assets/compose.dev.yaml (with Compose Watch)
         ├── Production: Use assets/compose.prod.yaml (healthchecks & resource limits)
         └── Template: Use assets/docker-compose.template.yml
```

---

## Executable Utilities

This skill provides automated Python scripts in `scripts/`:

### 1. Scaffold Dockerfile & .dockerignore
Auto-detects whether the project uses `uv`, `requirements.txt`, or standard Python and writes the optimized files:
```bash
python3 path/to/docker-toolkit/scripts/generate_dockerfile.py [--type simple|uv|production] [--force]
```

### 2. Build Helper
Validates Docker availability, builds image, and displays image inspection stats:
```bash
python3 path/to/docker-toolkit/scripts/build_image.py --tag <tag-name> [--file <dockerfile>] [--no-cache]
```

### 3. Audit & Lint Dockerfile
Checks a Dockerfile against security and production guidelines:
```bash
python3 path/to/docker-toolkit/scripts/lint_dockerfile.py [path/to/Dockerfile]
```

---

## Quick Reference Commands

### Building & Running Single Containers

```bash
# Build image with current directory context
docker build -t my-fastapi-app .

# Run container on port 8000 (detached, auto-remove on stop)
docker run -d --rm -p 8000:8000 --name fastapi-app my-fastapi-app

# Inspect running logs
docker logs -f fastapi-app

# Execute interactive shell inside running container
docker exec -it fastapi-app /bin/sh
```

### Multi-Service Management (Docker Compose)

```bash
# Start local development with Compose Watch
docker compose -f compose.dev.yaml up --build

# Run in background with production configuration
docker compose -f compose.prod.yaml up -d

# Check health and status of all services
docker compose ps

# Stop and tear down containers
docker compose down -v
```

---

## Core Containerization Rules

1. **Always Bind to `0.0.0.0`**: Inside containers, bind ASGI servers to `--host 0.0.0.0`. Binding to `127.0.0.1` makes the service unreachable from the host.
2. **Order Layers for Caching**: Copy package manifests (`requirements.txt`, `uv.lock`) and install dependencies *before* copying application code (`COPY . .`).
3. **Never Run as Root in Production**: Use `useradd` with an explicit UID (e.g. 10001) and declare `USER appuser`.
4. **Always Include a `.dockerignore`**: Exclude `.venv`, `__pycache__`, `.git`, `.pytest_cache`, and sensitive environment files (`.env`).
5. **Pin Base Image Versions**: Use explicit version tags (e.g. `python:3.12-slim`). Avoid `python:latest`.

---

## Bundled Assets & References

### Templates (`assets/`)
- `assets/Dockerfile.fastapi.template`: Configurable FastAPI Dockerfile template with healthcheck.
- `assets/docker-compose.template.yml`: Multi-service template with FastAPI, PostgreSQL, Redis, and volumes.
- `assets/Dockerfile.simple`: Quick single-stage Dockerfile for prototypes.
- `assets/Dockerfile.production`: Hardened multi-stage Dockerfile with non-root security.
- `assets/Dockerfile.uv`: High-speed multi-stage Dockerfile using `uv`.
- `assets/compose.dev.yaml`: Compose configuration with hot reload and Compose Watch.
- `assets/compose.prod.yaml`: Multi-service compose with resource limits and health checks.
- `assets/.dockerignore`: Comprehensive ignore file for Python projects.

### Detailed References (`references/`)
- [common-commands.md](references/common-commands.md): Quick reference cheat sheet for Docker and Compose CLI commands.
- [dockerfile-patterns.md](references/dockerfile-patterns.md): Multi-stage, caching, non-root, and healthcheck architectural patterns.
- [fastapi-docker-guide.md](references/fastapi-docker-guide.md): Official FastAPI recommendations, server runners, and reverse proxy headers.
- [uv-docker-guide.md](references/uv-docker-guide.md): BuildKit cache mounts and `uv` container workflows.
- [production-security.md](references/production-security.md): User permission hardening, secret safety, and read-only filesystems.
- [compose-spec.md](references/compose-spec.md): Docker Compose v2 patterns and service health dependencies.
