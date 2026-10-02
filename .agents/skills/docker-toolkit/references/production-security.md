# Container Security Best Practices for Python & FastAPI

This reference outlines security hardening practices for production container deployments.

---

## 1. Never Run as Root

By default, Docker containers run processes as `root` (UID 0). If an application vulnerability allows Remote Code Execution (RCE), an attacker gains root privileges inside the container and can potentially escape to the host.

### Creating an Unprivileged User

```dockerfile
# Create system group and user with explicit UID/GID
RUN groupadd --gid 10001 appgroup && \
    useradd --uid 10001 --gid appgroup --shell /bin/false --no-create-home appuser

# Set proper file permissions
WORKDIR /app
COPY --chown=appuser:appgroup . .

# Switch user before entrypoint/cmd
USER appuser
```

---

## 2. Pin Base Images & Avoid `latest`

Using `python:latest` introduces non-deterministic builds and security risks:
- New Python minor versions might contain breaking changes or deprecated syntax.
- **Rule**: Pin specific patch or minor versions (e.g. `python:3.12.9-slim` or `python:3.12-slim`).
- Prefer Debian `slim` over `alpine` for Python to avoid Musl libc compatibility and performance issues with pre-compiled C-extensions (wheels).

---

## 3. Minimize Image Size & Attack Surface

- Use multi-stage builds so compiler toolchains (such as `gcc`, `make`, `build-essential`) are present only in the builder stage and completely absent in the runtime image.
- Clean package manager caches:
  ```dockerfile
  RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      && rm -rf /var/lib/apt/lists/*
  ```
- Use a comprehensive `.dockerignore` to prevent leaking secrets (`.env`), git history (`.git`), or temporary test artifacts into the build context.

---

## 4. Environment Variables & Secrets Management

- **Never hardcode secrets** into `Dockerfile` instructions (`ENV SECRET=xxx` remains visible in image history).
- Use runtime environment variables provided by Docker Compose, Kubernetes secrets, or cloud secrets managers.
- In Docker Compose:
  ```yaml
  services:
    web:
      environment:
        - DATABASE_URL=${DATABASE_URL}
      # Or via env_file:
      env_file:
        - .env.production
  ```

---

## 5. Read-Only Root Filesystem

Prevent attackers or malicious scripts from writing executables to `/` or `/usr/`:
- Run container with `--read-only`:
  ```bash
  docker run --read-only --tmpfs /tmp --tmpfs /app/tmp -p 8000:8000 myapp
  ```
- If the application writes logs or uploads, mount a dedicated volume or tmpfs partition.
