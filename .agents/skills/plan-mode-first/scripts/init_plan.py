#!/usr/bin/env python3
"""
Scaffolds an implementation PLAN.md in the current working directory from the template.
"""

import argparse
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = SKILL_DIR / "assets" / "PLAN.template.md"


def init_plan(title: str, output_path: Path, force: bool = False):
    if output_path.exists() and not force:
        print(f"⚠️  {output_path} already exists. Use --force to overwrite.")
        sys.exit(1)

    template_content = TEMPLATE_PATH.read_text(encoding="utf-8")
    customized_content = template_content.replace("<Feature / Task Title>", title)
    output_path.write_text(customized_content, encoding="utf-8")
    print(f"✅ Generated implementation plan: {output_path}")
    print("📝 Fill out the sections with the user before switching to execution mode.")


def main():
    parser = argparse.ArgumentParser(description="Initialize a structured implementation PLAN.md")
    parser.add_argument("title", nargs="?", default="New Feature / Task", help="Title of the task or feature")
    parser.add_argument("--output", "-o", default="PLAN.md", help="Destination file path (default: PLAN.md)")
    parser.add_argument("--force", "-f", action="store_true", help="Overwrite if file already exists")

    args = parser.parse_args()
    init_plan(title=args.title, output_path=Path(args.output).resolve(), force=args.force)


if __name__ == "__main__":
    main()
