#!/usr/bin/env python3
"""
Lint and audit a Dockerfile against FastAPI & Docker security/production best practices.
"""

import argparse
import re
import sys
from pathlib import Path


def audit_dockerfile(dockerfile_path: Path):
    if not dockerfile_path.exists():
        print(f"❌ Error: {dockerfile_path} not found.")
        sys.exit(1)

    content = dockerfile_path.read_text()
    lines = content.splitlines()

    issues = []
    passes = []

    # 1. Base Image check
    from_matches = re.findall(r"^\s*FROM\s+([^\s]+)", content, re.MULTILINE | re.IGNORECASE)
    has_latest = any(":latest" in img or (":" not in img and "@" not in img) for img in from_matches)
    if has_latest:
        issues.append("CRITICAL: Base image uses 'latest' or unpinned tag. Pin specific versions (e.g. python:3.12-slim).")
    else:
        passes.append("Base image is pinned to specific version.")

    # 2. Non-root user check
    user_match = re.search(r"^\s*USER\s+([^\s]+)", content, re.MULTILINE | re.IGNORECASE)
    if not user_match or user_match.group(1).lower() in ("root", "0"):
        issues.append("WARNING: No non-root USER instruction found. Container may execute as root (UID 0).")
    else:
        passes.append(f"Non-root user configured: {user_match.group(1)}.")

    # 3. Layer caching order check
    has_bind_mount = any("type=bind" in l and any(m in l for m in ("uv.lock", "requirements.txt", "pyproject.toml")) for l in lines)
    copy_lines = [idx for idx, l in enumerate(lines) if re.match(r"^\s*COPY\b", l, re.IGNORECASE)]
    has_manifest_first = has_bind_mount
    if not has_manifest_first:
        for idx in copy_lines:
            line = lines[idx]
            if any(manifest in line for manifest in ("requirements.txt", "pyproject.toml", "uv.lock", "Pipfile", ".venv")):
                has_manifest_first = True
                break
            if "." in line or "app" in line:
                break
    if has_manifest_first:
        passes.append("Dependency manifest/cache mounted or copied before application code for optimal layer caching.")
    else:
        issues.append("RECOMMENDATION: Copy dependency manifests (requirements.txt / uv.lock) before application source code to maximize Docker cache reuse.")

    # 4. Host binding check (exclude HEALTHCHECK CMD)
    startup_cmds = [
        l for l in lines 
        if re.match(r"^\s*(CMD|ENTRYPOINT)\b", l, re.IGNORECASE) 
        and not any("HEALTHCHECK" in prev for prev in lines[max(0, lines.index(l)-2):lines.index(l)+1])
    ]
    cmd_or_entrypoint = "\n".join(startup_cmds)
    if "127.0.0.1" in cmd_or_entrypoint or ("localhost" in cmd_or_entrypoint and "curl" not in cmd_or_entrypoint):
        issues.append("CRITICAL: Server bound to localhost/127.0.0.1 inside container. Bind to 0.0.0.0 instead.")
    elif "0.0.0.0" in cmd_or_entrypoint or "--port" in cmd_or_entrypoint or "fastapi run" in cmd_or_entrypoint:
        passes.append("Server command binds properly to container network interfaces.")

    # 5. Healthcheck check
    if re.search(r"^\s*HEALTHCHECK\b", content, re.MULTILINE | re.IGNORECASE):
        passes.append("HEALTHCHECK instruction defined.")
    else:
        issues.append("RECOMMENDATION: Add HEALTHCHECK instruction for container orchestrators.")

    # 6. .dockerignore check
    dockerignore_path = dockerfile_path.parent / ".dockerignore"
    if dockerignore_path.exists():
        passes.append(".dockerignore file is present in project root.")
    else:
        issues.append("WARNING: No .dockerignore found. Potential risk of leaking .venv, .git, or secrets.")

    # Print Report
    print("=" * 60)
    print(f"Docker Audit Report: {dockerfile_path}")
    print("=" * 60)

    for p in passes:
        print(f"  ✅ [PASS] {p}")

    for i in issues:
        print(f"  ⚠️  [ISSUE] {i}")

    print("=" * 60)
    if issues:
        print(f"Found {len(issues)} issue(s) / recommendation(s).")
    else:
        print("All audit checks passed successfully! 🎉")


def main():
    parser = argparse.ArgumentParser(description="Lint and audit Dockerfile for FastAPI")
    parser.add_argument("dockerfile", nargs="?", default="Dockerfile", help="Path to Dockerfile (default: ./Dockerfile)")
    args = parser.parse_args()
    audit_dockerfile(Path(args.dockerfile))


if __name__ == "__main__":
    main()
