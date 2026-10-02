#!/usr/bin/env python3
"""
Validates an AGENTS.md (or CLAUDE.md) file against size limits, required sections,
and anti-patterns (such as vague platitudes or duplicated standard language rules).
"""

import argparse
import os
import re
import sys
from pathlib import Path

MAX_ALLOWED_SIZE_BYTES = 32 * 1024  # 32 KiB Codex hard limit
RECOMMENDED_SIZE_BYTES = 8 * 1024   # 8 KiB optimal budget

REQUIRED_SECTIONS = [
    ("Overview", [r"project overview", r"overview"]),
    ("Commands", [r"build.*test", r"commands", r"development commands"]),
    ("Code Style", [r"code style", r"style rules", r"coding standards"]),
    ("Structure & Boundaries", [r"structure", r"boundaries", r"architecture"]),
    ("Testing", [r"testing", r"test instructions", r"mocking"]),
]

VAGUE_PATTERNS = [
    r"\bwrite clean code\b",
    r"\bfollow best practices\b",
    r"\bwrite readable code\b",
    r"\bwrite maintainable code\b",
    r"\bwrite modular code\b",
]

DEFAULT_LANGUAGE_RULES = [
    r"\bindent with 4 spaces\b",
    r"\buse 2 spaces for indentation\b",
    r"\bpep 8 compliant\b",
    r"\bstandard prettier formatting\b",
]


def validate_file(path: Path):
    if not path.exists():
        print(f"❌ Error: File {path} not found.")
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    size_bytes = len(content.encode("utf-8"))

    errors = []
    warnings = []
    passes = []

    # 1. Size checks
    if size_bytes > MAX_ALLOWED_SIZE_BYTES:
        errors.append(
            f"File size ({size_bytes / 1024:.1f} KiB) exceeds the 32 KiB hard limit. "
            "Codex will silently truncate content beyond 32 KiB."
        )
    elif size_bytes > RECOMMENDED_SIZE_BYTES:
        warnings.append(
            f"File size ({size_bytes / 1024:.1f} KiB) exceeds recommended 8 KiB budget. "
            "Excessive documentation increases token costs (up to 23%) and competes for attention."
        )
    else:
        passes.append(f"Size is optimal: {size_bytes} bytes ({size_bytes / 1024:.2f} KiB <= 8 KiB).")

    # 2. Required section checks
    for section_name, patterns in REQUIRED_SECTIONS:
        found = any(re.search(pat, content, re.IGNORECASE) for pat in patterns)
        if found:
            passes.append(f"Section '{section_name}' is covered.")
        else:
            warnings.append(f"Missing recommended section: '{section_name}'.")

    # 3. Anti-pattern checks (Vague filler words)
    for pat in VAGUE_PATTERNS:
        match = re.search(pat, content, re.IGNORECASE)
        if match:
            warnings.append(
                f"Contains generic platitude '{match.group(0)}'. "
                "Agents already attempt clean code; replace with explicit architectural constraints."
            )

    # 4. Anti-pattern checks (Default language rules)
    for pat in DEFAULT_LANGUAGE_RULES:
        match = re.search(pat, content, re.IGNORECASE)
        if match:
            warnings.append(
                f"Contains standard default '{match.group(0)}'. "
                "Agents already know language defaults; only document rules that deviate."
            )

    # 5. Check if Subagent / Hybrid strategy is present
    has_subagents = bool(re.search(r"subagent", content, re.IGNORECASE))
    if has_subagents:
        passes.append("Subagent delegation / Hybrid model instructions detected.")

    # Summary Output
    print("=" * 60)
    print(f"Validation Report for: {path.name}")
    print("=" * 60)

    for p in passes:
        print(f"  ✅ [PASS] {p}")

    for w in warnings:
        print(f"  ⚠️  [WARN] {w}")

    for e in errors:
        print(f"  ❌ [FAIL] {e}")

    print("=" * 60)
    if errors:
        print(f"Result: FAILED with {len(errors)} critical error(s).")
        sys.exit(1)
    elif warnings:
        print(f"Result: PASSED with {len(warnings)} recommendation(s).")
    else:
        print("Result: PERFECT SCORE (No errors or warnings). 🎉")


def main():
    parser = argparse.ArgumentParser(description="Validate AGENTS.md or CLAUDE.md file")
    parser.add_argument("file", nargs="?", default="AGENTS.md", help="Path to AGENTS.md / CLAUDE.md")
    args = parser.parse_args()
    validate_file(Path(args.file).resolve())


if __name__ == "__main__":
    main()
