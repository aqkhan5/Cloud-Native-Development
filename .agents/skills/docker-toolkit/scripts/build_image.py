#!/usr/bin/env python3
"""
Build helper script for Docker images.
Validates Docker availability, builds image, and displays image inspection stats.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def check_docker_installed() -> bool:
    """Check if docker CLI is available and daemon is reachable."""
    try:
        res = subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res.returncode == 0
    except FileNotFoundError:
        return False


def build_image(tag: str, dockerfile: str = "Dockerfile", path: str = ".", no_cache: bool = False):
    if not check_docker_installed():
        print("❌ Error: Docker is either not installed or the Docker daemon is not running.")
        sys.exit(1)

    df_path = Path(path) / dockerfile
    if not df_path.exists():
        print(f"❌ Error: Dockerfile not found at {df_path}")
        sys.exit(1)

    cmd = ["docker", "build", "-t", tag, "-f", str(df_path)]
    if no_cache:
        cmd.append("--no-cache")
    cmd.append(path)

    print(f"🚀 Running command: {' '.join(cmd)}")
    print("-" * 60)

    try:
        proc = subprocess.run(cmd, check=True)
        print("-" * 60)
        print(f"✅ Successfully built Docker image: {tag}")

        # Display image size
        inspect_res = subprocess.run(
            ["docker", "images", tag, "--format", "table {{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"],
            capture_output=True,
            text=True,
        )
        if inspect_res.returncode == 0 and inspect_res.stdout:
            print("\n📊 Image Details:")
            print(inspect_res.stdout.strip())

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with exit code: {e.returncode}")
        sys.exit(e.returncode)


def main():
    parser = argparse.ArgumentParser(description="Docker build helper script for Python/FastAPI applications")
    parser.add_argument("--tag", "-t", required=True, help="Image tag (e.g., my-fastapi-app:latest)")
    parser.add_argument("--file", "-f", default="Dockerfile", help="Path to Dockerfile (default: Dockerfile)")
    parser.add_argument("--path", "-p", default=".", help="Build context directory (default: .)")
    parser.add_argument("--no-cache", action="store_true", help="Do not use cache when building the image")

    args = parser.parse_args()
    build_image(tag=args.tag, dockerfile=args.file, path=args.path, no_cache=args.no_cache)


if __name__ == "__main__":
    main()
