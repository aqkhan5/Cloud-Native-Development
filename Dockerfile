# syntax=docker/dockerfile:1
# ==============================================================================
# Dockerfile.uv: Blazing-Fast Multi-Stage Build Using Astral's uv
# Designed for production FastAPI applications with pyproject.toml / uv.lock
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build & Dependency Synchronization (Builder Stage)
# ------------------------------------------------------------------------------
# 1. Base image: Use official uv image with Debian slim for speed and glibc support
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# 2. Environment flags:
#    - PYTHONDONTWRITEBYTECODE=1: Prevents creation of temporary .pyc files during build
#    - PYTHONUNBUFFERED=1: Ensures instant stdout/stderr log emission
#    - UV_LINK_MODE=copy: Forces uv to copy dependencies instead of hardlinks across volumes
#    - UV_COMPILE_BYTECODE=1: Ahead-of-time bytecode compilation reduces container startup time
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

# 3. Workdir: Establish isolated build directory before copying files
WORKDIR /app

# 4. Layer caching: Install dependencies using BuildKit bind mounts and cache mounts
#    - --mount=type=cache: Persists package cache across builds without saving in image layers
#    - --mount=type=bind: Mounts lockfile/manifest into builder without adding image layer overhead
#    - --frozen: Guarantees deterministic builds by requiring uv.lock to match pyproject.toml
#    - --no-install-project: Builds dependencies into .venv before copying source code for cache reuse
#    - --no-dev: Excludes development dependencies (pytest, linters) from production build
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# ------------------------------------------------------------------------------
# Stage 2: Clean, Hardened Runtime Image (Runtime Stage)
# ------------------------------------------------------------------------------
# 5. Base runtime image: Minimal Debian slim runtime without build compilers or uv binary
FROM python:3.12-slim AS runtime

# 6. Runtime environment: Prepend isolated virtual environment to PATH
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# 7. Workdir: Establish container application directory
WORKDIR /app

# 8. System dependencies: Install curl for container health check probes, clean apt caches immediately
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 9. Security: Create an unprivileged system group and user with explicit UID 10001
RUN groupadd --gid 10001 appgroup && \
    useradd --uid 10001 --gid appgroup --shell /bin/false --no-create-home appuser

# 10. Layer caching: Copy pre-built virtual environment from builder stage before source code
COPY --from=builder /app/.venv /app/.venv

# 11. Application code: Copy source code with unprivileged user ownership; cached when dependencies don't change
COPY --chown=appuser:appgroup . .

# 12. Security: Drop root privileges to prevent container breakout exploits
USER appuser

# 13. Metadata: Expose standard FastAPI port for documentation and container discovery
EXPOSE 8000

# 14. Healthcheck: Enable container engine / orchestrator to probe application responsiveness
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# 15. Runtime execution: Bind Uvicorn ASGI server to 0.0.0.0 to listen on all container interfaces
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]