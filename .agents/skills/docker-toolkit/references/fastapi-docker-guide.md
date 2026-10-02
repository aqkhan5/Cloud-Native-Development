# Official FastAPI Docker Containerization Guide

This reference documents official patterns and best practices for containerizing FastAPI applications, based on official FastAPI documentation (`fastapi.tiangolo.com/deployment/docker`).

---

## 1. Core Principles of FastAPI in Docker

### Host Binding: `0.0.0.0` vs `127.0.0.1`
When running an ASGI server inside a Docker container:
- **Never bind to `127.0.0.1` or `localhost`** inside the container. Doing so makes the server only accessible from within the container's isolated network namespace, causing connection refused errors from the host.
- **Always bind to `0.0.0.0`** (`--host 0.0.0.0`), which tells Uvicorn / FastAPI to listen on all network interfaces inside the container.

### Docker Layer Caching Strategy
Docker builds images sequentially using cached layers:
1. Docker checks if the files in a `COPY` command have changed.
2. If unchanged, Docker reuses the cached layer and all subsequent layers until a changed instruction is encountered.
3. **Best Practice**: Always copy dependency definitions (`requirements.txt`, `pyproject.toml`, `uv.lock`) and run package installation *before* copying the application source code.
4. Because application source code changes frequently while dependencies change rarely, this keeps rebuild times to seconds rather than minutes.

---

## 2. Choosing Server Runners

FastAPI applications can be served using several command runners:

### Option A: `fastapi run` (FastAPI CLI)
- **Use for**: Simplicity, modern FastAPI projects (FastAPI >= 0.111.0).
- Automatically configures production settings (e.g. workers based on available CPUs if enabled).
```dockerfile
CMD ["fastapi", "run", "main.py", "--port", "8000"]
```

### Option B: `uvicorn` Directly
- **Use for**: Explicit control over workers, proxy headers, log levels.
```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--proxy-headers"]
```

### Option C: Gunicorn with Uvicorn Workers
- **Use for**: High-concurrency enterprise deployments requiring process management and zero-downtime restarts.
```dockerfile
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
```

---

## 3. Proxy Headers & Reverse Proxies (Nginx, Traefik, Caddy)

When running behind an ingress controller, load balancer, or reverse proxy:
- Client IP addresses and SSL certificates terminate at the proxy.
- Ensure Uvicorn recognizes `X-Forwarded-For` and `X-Forwarded-Proto` headers:
  ```bash
  uvicorn main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips="*"
  ```
- Or set in code:
  ```python
  from fastapi.middleware.trustedhost import TrustedHostMiddleware
  # add middleware as needed
  ```

---

## 4. Container Healthchecks

FastAPI applications should provide a lightweight status endpoint for Docker and orchestrators:

```python
@app.get("/health", tags=["Monitoring"])
def health_check():
    return {"status": "ok"}
```

In the `Dockerfile`:
```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

If `curl` is omitted to minimize image size, use Python's standard library:
```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
```
