---
name: pytest-builder
description: Scaffolds and sets up pytest configuration, test clients, database test suites, and fixtures. Use this skill when configuring a Python/FastAPI project for testing, initializing pytest.ini, conftest.py, generating mock files, or scaffolding sync/async tests.
---

# Pytest Builder

Scaffold testing environments for FastAPI and general Python applications.

## Overview

This skill offers a structured collection of templates, references, and executable scripts to configure, run, and scale tests with pytest.

## Executable Utilities

Use these scripts from the skill's root to set up your project structure automatically:

- **Initialize Pytest Configuration**: Creates a standard `pytest.ini` in the current working directory.
  ```bash
  python3 scripts/setup_pytest_config.py
  ```
- **Generate Fixtures (`conftest.py`)**: Generates a standard setup for testing (defaults to `basic`, use `fastapi` as an argument to scaffold FastAPI clients).
  ```bash
  python3 scripts/generate_fixtures.py [basic|fastapi]
  ```
- **Generate Test File**: Creates a new boilerplate test file in the `tests/` directory.
  ```bash
  python3 scripts/generate_test.py <test_name>
  ```

---

## Skill Directory Structure

```
pytest-builder/
├── SKILL.md                  # Main skill documentation
├── scripts/                  # Automating setup steps
│   ├── setup_pytest_config.py
│   ├── generate_fixtures.py
│   └── generate_test.py
├── references/               # Best practice guides
│   ├── fastapi-testing.md
│   ├── fixtures-library.md
│   ├── async-testing.md
│   └── database-testing.md
└── assets/                   # Configuration & template files
    ├── pytest.ini
    ├── conftest_basic.py
    ├── conftest_fastapi.py
    └── test_template.py
```

---

## Detailed References

For production-ready code samples and specific test cases:
*   **FastAPI Specific Testing Patterns**: See [references/fastapi-testing.md](references/fastapi-testing.md) for endpoint checks.
*   **Pytest Fixture Library**: See [references/fixtures-library.md](references/fixtures-library.md) for sharing state and parametrization.
*   **Asynchronous Testing**: See [references/async-testing.md](references/async-testing.md) for running `async/await` tests.
*   **Database Isolation & Cleanups**: See [references/database-testing.md](references/database-testing.md) for setting up transaction rollbacks.
