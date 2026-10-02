# Docker Compose Specification for FastAPI Services

This reference provides architectural patterns for multi-service local development and production deployments using Docker Compose Specification.

---

## 1. File Naming Standard

The Compose Specification standardizes on:
- `compose.yaml` (default preferred) or `compose.yml`
- Environment-specific files: `compose.dev.yaml` and `compose.prod.yaml`

Commands:
```bash
# Development
docker compose -f compose.dev.yaml up --build

# Production
docker compose -f compose.prod.yaml up -d
```

---

## 2. Fast Local Development with Compose Watch

Docker Compose Watch replaces heavy file volume polling with native file sync and automated rebuilds:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    develop:
      watch:
        # Sync source files directly into container without restarting
        - action: sync
          path: ./app
          target: /app/app
        # Automatically rebuild image when dependencies change
        - action: rebuild
          path: pyproject.toml
```

To run with watch mode enabled:
```bash
docker compose watch
```

---

## 3. Service Health Dependencies

Never start your API before dependent services (such as PostgreSQL or Redis) are fully ready to accept connections. Use `condition: service_healthy`:

```yaml
services:
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secretpassword
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
```

---

## 4. Production Resource Constraints

Prevent any container from exhausting host resources:

```yaml
deploy:
  resources:
    limits:
      cpus: "2.0"
      memory: 2048M
    reservations:
      cpus: "0.5"
      memory: 512M
```
