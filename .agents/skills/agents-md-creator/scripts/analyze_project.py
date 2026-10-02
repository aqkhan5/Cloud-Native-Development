#!/usr/bin/env python3
"""
Inspects the current repository to extract high-signal configuration,
framework versions, test runners, and package managers for AGENTS.md generation.
"""

import json
import os
import sys
from pathlib import Path


def analyze_repo(root: Path) -> dict:
    info = {
        "project_name": root.name,
        "languages": [],
        "package_manager": None,
        "frameworks": [],
        "test_runner": None,
        "test_command": None,
        "lint_command": None,
        "dev_command": None,
        "directories": [],
    }

    # 1. Python ecosystem
    if (root / "pyproject.toml").exists() or (root / "requirements.txt").exists():
        info["languages"].append("Python")
        if (root / "uv.lock").exists():
            info["package_manager"] = "uv"
            info["test_command"] = "uv run pytest -v"
            info["dev_command"] = "uv run uvicorn main:app --reload"
            info["lint_command"] = "uv run ruff check ."
        elif (root / "poetry.lock").exists():
            info["package_manager"] = "poetry"
            info["test_command"] = "poetry run pytest -v"
            info["dev_command"] = "poetry run uvicorn main:app --reload"
        else:
            info["package_manager"] = "pip"
            info["test_command"] = "pytest -v"
            info["dev_command"] = "uvicorn main:app --reload"

        # Check pyproject or requirements for frameworks
        pyproject_path = root / "pyproject.toml"
        if pyproject_path.exists():
            txt = pyproject_path.read_text().lower()
            if "fastapi" in txt:
                info["frameworks"].append("FastAPI")
            if "django" in txt:
                info["frameworks"].append("Django")
            if "flask" in txt:
                info["frameworks"].append("Flask")

    # 2. Node/TypeScript ecosystem
    if (root / "package.json").exists():
        info["languages"].append("JavaScript/TypeScript")
        try:
            pkg = json.loads((root / "package.json").read_text())
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "next" in deps:
                info["frameworks"].append(f"Next.js ({deps['next']})")
            if "react" in deps:
                info["frameworks"].append("React")
            if "express" in deps:
                info["frameworks"].append("Express")

            if (root / "pnpm-lock.yaml").exists():
                info["package_manager"] = "pnpm"
            elif (root / "yarn.lock").exists():
                info["package_manager"] = "yarn"
            else:
                info["package_manager"] = "npm"

            pm = info["package_manager"]
            if "vitest" in deps:
                info["test_command"] = f"{pm} vitest run"
            elif "jest" in deps:
                info["test_command"] = f"{pm} test"

            scripts = pkg.get("scripts", {})
            if "dev" in scripts:
                info["dev_command"] = f"{pm} run dev"
            if "lint" in scripts:
                info["lint_command"] = f"{pm} run lint"
        except Exception:
            pass

    # 3. Top-level directories (excluding hidden, venv, caches)
    excluded = {".git", ".venv", "venv", "__pycache__", "node_modules", ".pytest_cache", ".agents"}
    dirs = [
        d.name
        for d in root.iterdir()
        if d.is_dir() and d.name not in excluded and not d.name.startswith(".")
    ]
    info["directories"] = sorted(dirs)

    return info


def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    result = analyze_repo(target)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
