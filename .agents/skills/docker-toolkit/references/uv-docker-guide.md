# High-Performance Python Containerization with uv

This reference documents the modern pattern for building Python and FastAPI container images using Astral's `uv`, based on official Docker documentation.

---

## 1. Why Use `uv` in Docker?

- **Speed**: Resolves and installs Python packages 10x-100x faster than traditional `pip`.
- **Reproducibility**: Enforces locked dependency trees via `uv.lock`.
- **Ephemeral Build Efficiency**: Uses BuildKit cache and bind mounts without bloating Docker images.

---

## 2. Recommended Multi-Stage uv Pattern

```dockerfile
# syntax=docker/dockerfile:1
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

# 1. Bind mount manifests so lockfiles don't need to be copied into image layers
# 2. Cache mount uv's download cache to reuse packages across rebuilds
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Final minimal runtime
FROM python:3.12-slim AS runtime

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only the compiled virtual environment
COPY --from=builder /app/.venv /app/.venv

# Copy source code
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 3. Key uv Flags Explained

| Flag | Purpose |
|------|---------|
| `UV_LINK_MODE=copy` | Forces `uv` to copy files instead of creating hardlinks across distinct Docker volume mounts. |
| `UV_COMPILE_BYTECODE=1` | Compiles Python files to bytecode (`.pyc`) ahead of time to reduce container cold-start latency. |
| `--frozen` | Fails immediately if `uv.lock` is out of sync with `pyproject.toml`, preventing unintended version drift. |
| `--no-install-project` | Installs dependencies into `.venv` without copying application code yet, enabling maximum layer caching. |
| `--no-dev` | Omits development dependencies (e.g. pytest, mypy, black) to minimize image footprint. |

---

## 4. Bind Mounts vs. Traditional COPY

In traditional Docker builds:
```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
```
This adds `requirements.txt` to the image layer history.

With BuildKit bind mounts:
```dockerfile
RUN --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project
```
The files are temporarily mounted into the container during the build step only. They never become permanent image layers, reducing layer count and image size.
