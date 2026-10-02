# AGENTS.md

> Guidance for AI agents working in this repository. Keep instructions dense, factual, and non-redundant.

## Project Overview
- **Project**: <Project Name>
- **Primary Stack**: <Language> <Version>, <Framework> <Version> (e.g. Python 3.12, FastAPI 0.115)
- **Runtime / Package Manager**: <uv / pnpm / poetry / cargo> <Version>
- **Architecture**: <Monolith / Microservice / Clean Architecture / Modular Monolith>

## Build & Test Commands
> Include exact commands with all required flags.

- **Dev Server**: `<exact command, e.g. uv run uvicorn main:app --reload --port 8000>`
- **Run Full Test Suite**: `<exact command, e.g. uv run pytest -v>`
- **Run Single Test**: `<exact command, e.g. uv run pytest tests/test_auth.py::test_login_success -v>`
- **Database Migrations**: `<exact command, e.g. uv run alembic upgrade head>`
- **Type Check / Linter**: `<exact command, e.g. uv run ruff check . && uv run mypy .>`

## Code Style & Non-Standard Rules
> ONLY list rules that differ from language defaults. Do NOT repeat standard PEP 8 or Prettier rules.

- **Exports / Handlers**: <e.g. Named exports only, no default exports. All route handlers must be async.>
- **Error Handling**: <e.g. Raise domain exceptions inheriting from `AppException`; never return raw dicts for errors.>
- **Data Validation**: <e.g. Use Pydantic v2 `BaseModel` with strict type annotations; never use untyped `dict` payloads.>
- **State & Scope**: <e.g. No global state. Inject database sessions and clients via FastAPI dependencies.>

## Project Structure & Responsibilities
- `<dir1>/`: <Responsibility, e.g. `/src/api/`: Thin route controllers (validate input, delegate to services)>
- `<dir2>/`: <Responsibility, e.g. `/src/services/`: Core business logic, transaction handling>
- `<dir3>/`: <Responsibility, e.g. `/src/models/`: Database schemas and ORM entities>
- `<dir4>/`: <Responsibility, e.g. `/src/core/`: Settings, telemetry, and base security configs>

## Testing Instructions & Mocking Strategy
- **Runner**: <pytest / vitest / jest / cargo test>
- **Database in Tests**: <e.g. Do NOT mock the database. Use the transactional SQLite in-memory test database with automatic rollback.>
- **Third-Party APIs**: <e.g. Mock all external HTTP requests using `respx` or `httpx-mock`. Never hit live external services in unit tests.>
- **Test Data**: <e.g. Use Factory Boy fixtures for test fixtures; avoid hardcoded static IDs.>

## Explicit Boundaries & Gotchas
> What the agent should NEVER touch or change.

- **Forbidden Files**: Never modify files in `/generated/` or `/dist/`.
- **Environment & Secrets**: Never read, commit, or log `.env` files or API secrets.
- **Legacy Modules**: <e.g. The `/legacy/` module uses synchronous database drivers; do not convert them to async.>
- **Dependencies**: Do not add new third-party dependencies without explicit approval.

## Git & PR Guidelines
- **Branch Naming**: `<type>/<issue-id>-<short-description>` (e.g. `feat/AUTH-102-jwt-refresh`)
- **Commit Format**: Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`)
- **Merge Strategy**: Squash and merge only.
