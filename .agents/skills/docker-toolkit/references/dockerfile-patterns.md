# Essential Dockerfile Design Patterns for Python & FastAPI

This reference documents the industry-standard Dockerfile architectural patterns for building production-grade container images.

---

## Pattern 1: Optimized Layer Caching with uv

Docker caches layers by evaluating the files in each `COPY` or `RUN --mount` instruction. If dependencies and configurations are unchanged, subsequent layers reuse the cache.

```dockerfile
# 1. Base setup: infrequent changes
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
WORKDIR /app

# 2. Dependency resolution: Mount lockfiles and install into venv before copying app code
#    Cached across rebuilds via BuildKit cache mount
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# 3. Application code: Copied after dependencies are installed
COPY . .
```

**Rule**: Always mount/copy and install dependencies *before* copying the application source code.

---

## Pattern 2: Multi-Stage Build with uv

Compilers and SDK tools (like `gcc`, `build-essential`, `cargo`) and build utilities are isolated to the builder stage, keeping the production runtime minimal and secure.

```dockerfile
# Stage 1: Build stage using uv for ultra-fast dependency synchronization
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Stage 2: Clean runtime stage using minimal Python slim
FROM python:3.12-slim AS runtime
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

# Copy pre-compiled virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code with non-root ownership
COPY --chown=appuser:appgroup . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Pattern 3: Unprivileged Non-Root User

Running containers as `root` (UID 0) poses severe privilege escalation risks.

```dockerfile
# Create system group and user
RUN groupadd --gid 10001 appgroup && \
    useradd --uid 10001 --gid appgroup --shell /bin/false --no-create-home appuser

# Set working directory and copy files with ownership
WORKDIR /app
COPY --chown=appuser:appgroup . .

# Drop root privileges
USER appuser
```

---

## Pattern 4: BuildKit Cache & Bind Mounts

BuildKit enables ephemeral mounts that speed up builds without persisting temporary files to image layers:

```dockerfile
# Bind mount: uses local uv.lock without creating an image layer
# Cache mount: preserves package download cache across rebuilds
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project
```

---

## Pattern 5: Dual Target (Dev vs. Production)

Maintain a single Dockerfile that serves both local development with reload and hardened production:

```dockerfile
FROM python:3.12-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Development target: runs with reload enabled
FROM base AS development
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production target: non-root, multiple workers, healthchecks
FROM python:3.12-slim AS production
RUN groupadd -g 10001 appgroup && useradd -u 10001 -g appgroup appuser
WORKDIR /app
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=base /usr/local/bin /usr/local/bin
COPY --chown=appuser:appgroup . .
USER appuser
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8000/ || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

---

## Pattern 6: Container Healthcheck

Ensure container orchestrators (Docker Swarm, Kubernetes, Docker Compose) know when the service is ready:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1
```
