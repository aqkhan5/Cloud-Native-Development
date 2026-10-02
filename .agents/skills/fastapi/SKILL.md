---
name: fastapi
description: Use when the user wants to create, structure, implement, test, or deploy projects using FastAPI (from Hello World to professional production-grade APIs). This skill guides you through bootstrapping projects, implementing SQLAlchemy DB dependencies, configuring settings via Pydantic, adding OAuth2/JWT security, and writing pytest test suites.
---

# FastAPI Development Skill

This skill provides step-by-step guidance, project scaffolding tools, and coding patterns to develop high-performance, robust FastAPI web applications.

---

## Workflow Decision Tree

Before writing any code, determine the project scope:

1. **Hello World / Prototyping** (Single file, minor tools, testing simple endpoints):
   - File: Create a single `main.py`
   - Execution: Run dev server with `fastapi dev main.py`
2. **Professional Production APIs** (Complex database schemas, user auth, config files, testing environments):
   - Action: Scaffold the project structure using `scripts/scaffold_project.py`
   - Routing: Group logic into separate routers using `APIRouter`
   - Auth: Configure OAuth2 password flow with JWT tokens
   - DB: Manage SQLAlchemy sessions with dependency injection

---

## 1. Setup & Installation

FastAPI projects require python 3.10+ and package management (recommended: `uv` or `pip`).

```bash
# Add core dependencies
pip install fastapi "uvicorn[standard]" pydantic pydantic-settings

# Add security and DB dependencies
pip install pyjwt "pwdlib[argon2]" sqlalchemy

# Add development tools
pip install pytest httpx
```

---

## 2. Bootstrapping a Production Project

To build a professional structured API, run the bundled scaffolding utility to create the recommended repository layout:

```bash
# Run from your project directory (runs scripts/scaffold_project.py)
python3 path/to/fastapi/scripts/scaffold_project.py [target_directory]
```

This will create a clean layout with:
- Config: Environment variables parsed via `pydantic-settings`
- Database: Connection setups and db session injections (`get_db`)
- User Security: Password hashes (argon2) and token generators (JWT)
- Organization: Routers grouped in `app/routers/` and CRUD logic in `app/crud/`
- Testing: Conftest setup with in-memory DB override and test client

---

## 3. Running & Testing the App

### Running the App
```bash
# Start development server with hot reload
fastapi dev app/main.py

# Start production server
fastapi run app/main.py
```

### Running Tests
```bash
# Execute pytest suite
pytest
```

---

## 4. Production Coding Patterns

For detailed code blocks and production best practices, refer to the following reference documentation:

- **Settings & CORS**: Configuration management using Pydantic Settings.
- **Database Dependency Injection**: Session lifetime handling via generators.
- **OAuth2 & JWT Flow**: Password validation, JWT creation, route protection.
- **Pytest Database Overrides**: Mocking database configurations for testing.

See: [production_patterns.md](references/production_patterns.md)
