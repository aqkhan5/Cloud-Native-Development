#!/usr/bin/env python3
"""
Scaffold an optimized, uv-powered Dockerfile and .dockerignore for FastAPI / Python applications.
Enforces:
1. Instruction ordering for optimal Docker layer caching
2. High-performance package installation via Astral's uv (instead of pip)
3. Intelligent .dockerignore management (creates if missing, or updates if already present)
4. Comprehensive inline documentation for every Dockerfile instruction
"""

import argparse
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"


def detect_project_type(cwd: Path) -> str:
    """Auto-detect package manager in current directory."""
    if (cwd / "uv.lock").exists() or (cwd / "pyproject.toml").exists():
        return "uv"
    if (cwd / "requirements.txt").exists():
        return "production"
    return "uv"


def sync_dockerignore(target_dir: Path, src_dockerignore: Path) -> str:
    """
    Generate .dockerignore if absent, or merge missing rules if already present.
    Preserves existing user rules and comments.
    """
    dest_dockerignore = target_dir / ".dockerignore"

    if not src_dockerignore.exists():
        return "skipped (source template missing)"

    if not dest_dockerignore.exists():
        dest_dockerignore.write_text(src_dockerignore.read_text())
        return "created"

    existing_content = dest_dockerignore.read_text()
    # Normalize existing lines into a set for membership checking
    existing_rules = {
        line.strip()
        for line in existing_content.splitlines()
        if line.strip() and not line.strip().startswith("#")
    }

    # Find rules from source template not currently present
    src_lines = src_dockerignore.read_text().splitlines()
    missing_rules = []
    for line in src_lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            # Check direct match or trailing-slash variants
            norm_rule = stripped.rstrip("/")
            if stripped not in existing_rules and norm_rule not in existing_rules and f"{norm_rule}/" not in existing_rules:
                missing_rules.append(stripped)

    if not missing_rules:
        return "already up-to-date"

    # Append missing rules non-destructively
    append_block = "\n# --- Added by docker-toolkit (missing essential patterns) ---\n" + "\n".join(missing_rules) + "\n"
    with open(dest_dockerignore, "a") as f:
        f.write(append_block)

    return f"updated (added {len(missing_rules)} missing rules)"


def main():
    parser = argparse.ArgumentParser(
        description="Generate uv-optimized Dockerfile and managed .dockerignore for FastAPI"
    )
    parser.add_argument(
        "--type",
        choices=["uv", "production", "simple", "template"],
        help="Type of Dockerfile to generate (defaults to auto-detection: uv)",
    )
    parser.add_argument(
        "--target-dir",
        default=".",
        help="Directory to write Dockerfile and .dockerignore (default: current dir)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing Dockerfile if present",
    )

    args = parser.parse_args()
    target_dir = Path(args.target_dir).resolve()

    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)

    choice = args.type or detect_project_type(target_dir)
    print(f"⚡ Selected configuration: {choice} (uv-accelerated)")

    if choice == "template":
        template_name = "Dockerfile.fastapi.template"
    else:
        template_name = f"Dockerfile.{choice}"

    src_dockerfile = ASSETS_DIR / template_name
    src_dockerignore = ASSETS_DIR / ".dockerignore"

    dest_dockerfile = target_dir / "Dockerfile"

    # Write Dockerfile
    if dest_dockerfile.exists() and not args.force:
        print(f"⚠️  {dest_dockerfile} already exists. Use --force to overwrite.")
    else:
        if not src_dockerfile.exists():
            print(f"❌ Error: Source template {src_dockerfile} not found.")
            sys.exit(1)
        dest_dockerfile.write_text(src_dockerfile.read_text())
        print(f"✅ Generated Dockerfile: {dest_dockerfile} (using Astral uv & layer caching)")

    # Manage .dockerignore (generate or update)
    ignore_status = sync_dockerignore(target_dir, src_dockerignore)
    print(f"📄 .dockerignore status: {ignore_status} at {target_dir / '.dockerignore'}")


if __name__ == "__main__":
    main()
