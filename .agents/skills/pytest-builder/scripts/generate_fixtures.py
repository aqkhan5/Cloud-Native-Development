#!/usr/bin/env python3
import sys
import shutil
from pathlib import Path

def main():
    tests_dir = Path.cwd() / "tests"
    tests_dir.mkdir(exist_ok=True)
    
    dest = tests_dir / "conftest.py"
    if dest.exists():
        print("conftest.py already exists!")
        sys.exit(0)
        
    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    
    test_type = "basic"
    if len(sys.argv) > 1 and sys.argv[1] == "fastapi":
        test_type = "fastapi"
        
    src = assets_dir / f"conftest_{test_type}.py"
    if src.exists():
        shutil.copy(src, dest)
        print(f"Generated {test_type} conftest.py in tests/")
    else:
        print("Error: Template not found!")

if __name__ == "__main__":
    main()
