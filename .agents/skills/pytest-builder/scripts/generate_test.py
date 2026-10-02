#!/usr/bin/env python3
import sys
import shutil
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: generate_test.py <name_of_test_file>")
        sys.exit(1)
        
    test_name = sys.argv[1]
    if not test_name.startswith("test_"):
        test_name = f"test_{test_name}"
    if not test_name.endswith(".py"):
        test_name = f"{test_name}.py"
        
    tests_dir = Path.cwd() / "tests"
    tests_dir.mkdir(exist_ok=True)
    
    dest = tests_dir / test_name
    if dest.exists():
        print(f"{test_name} already exists!")
        sys.exit(0)
        
    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    src = assets_dir / "test_template.py"
    
    if src.exists():
        shutil.copy(src, dest)
        print(f"Generated test file: {dest}")
    else:
        dest.write_text("""def test_example():
    assert True
""")
        print(f"Generated default test file: {dest}")

if __name__ == "__main__":
    main()
