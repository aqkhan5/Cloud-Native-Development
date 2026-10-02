#!/usr/bin/env python3
import shutil
import sys
from pathlib import Path

def main():
    dest = Path.cwd() / "pytest.ini"
    if dest.exists():
        print("pytest.ini already exists!")
        sys.exit(0)
    
    # Locate assets
    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    src = assets_dir / "pytest.ini"
    
    if src.exists():
        shutil.copy(src, dest)
        print("Successfully created pytest.ini from template!")
    else:
        print("Template not found, writing default pytest.ini...")
        dest.write_text("""[pytest]
minversion = 6.0
addopts = -ra -q --tb=short
testpaths = tests
""")
        print("Done.")

if __name__ == "__main__":
    main()
