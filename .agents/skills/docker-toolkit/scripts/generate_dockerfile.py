#!/usr/bin/env python3
"""
Scaffold an optimized Dockerfile and .dockerignore for FastAPI / Python applications.
Auto-detects packaging tools (uv, poetry, pip) or accepts explicit --type.
"""

import argparse
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"


def detect_project_type(cwd: Path) -> str:
    """Auto-detect package manager in current directory."""
    if (cwd / "uv.lock").exists() or (cwd / "pyproject.toml").exists() and "uv" in (cwd / "pyproject.toml").read_text():
        return "uv"
    if (cwd / "requirements.txt").exists():
        return "production"
    return "simple"


def main():
    parser = argparse.ArgumentParser(description="Generate Dockerfile and .dockerignore for FastAPI")
    parser.add_argument(
        "--type",
        choices=["simple", "production", "uv"],
        help="Type of Dockerfile to generate (defaults to auto-detection)",
    )
    parser.add_argument(
        "--target-dir",
        default=".",
        help="Directory to write Dockerfile and .dockerignore (default: current dir)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing Dockerfile / .dockerignore if present",
    )

    args = parser.parse_args()
    target_dir = Path(args.target_dir).resolve()

    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)

    choice = args.type or detect_project_type(target_dir)
    print(f"📦 Selected configuration: {choice}")

    template_name = f"Dockerfile.{choice}"
    src_dockerfile = ASSETS_DIR / template_name
    src_dockerignore = ASSETS_DIR / ".dockerignore"

    dest_dockerfile = target_dir / "Dockerfile"
    dest_dockerignore = target_dir / ".dockerignore"

    # Write Dockerfile
    if dest_dockerfile.exists() and not args.force:
        print(f"⚠️  {dest_dockerfile} already exists. Use --force to overwrite.")
    else:
        dest_dockerfile.write_text(src_dockerfile.read_text())
        print(f"✅ Generated: {dest_dockerfile} (from {template_name})")

    # Write .dockerignore
    if dest_dockerignore.exists() and not args.force:
        print(f"⚠️  {dest_dockerignore} already exists. Use --force to overwrite.")
    else:
        dest_dockerignore.write_text(src_dockerignore.read_text())
        print(f"✅ Generated: {dest_dockerignore}")


if __name__ == "__main__":
    main()
