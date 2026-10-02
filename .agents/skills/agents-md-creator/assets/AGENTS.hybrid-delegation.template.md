# AGENTS.md

> Guidance for AI agents working in this repository. Follow the core repository rules and the Hybrid Subagent Delegation Strategy.

## Project Overview
- **Project**: <Project Name>
- **Primary Stack**: <Language> <Version>, <Framework> <Version>
- **Runtime / Package Manager**: <uv / pnpm / poetry / cargo> <Version>
- **Architecture**: <Monolith / Microservice / Clean Architecture / Modular Monolith>

## Build & Test Commands
> Include exact commands with all required flags.

- **Dev Server**: `<exact command, e.g. uv run uvicorn main:app --reload --port 8000>`
- **Run Full Test Suite**: `<exact command, e.g. uv run pytest -v>`
- **Run Single Test**: `<exact command, e.g. uv run pytest tests/unit/test_service.py::test_case -v>`
- **Database Migrations**: `<exact command, e.g. uv run alembic upgrade head>`
- **Type Check / Linter**: `<exact command, e.g. uv run ruff check . && uv run mypy .>`

## Code Style & Non-Standard Rules
> ONLY list rules that differ from language defaults. Do NOT repeat standard PEP 8 or Prettier rules.

- **Exports / Handlers**: <e.g. Named exports only, no default exports. All route handlers must be async.>
- **Error Handling**: <e.g. Raise domain exceptions inheriting from `AppException`; never return raw dicts for errors.>
- **Data Validation**: <e.g. Use Pydantic v2 `BaseModel` with strict type annotations; never use untyped payloads.>
- **State & Scope**: <e.g. No global state. Inject database sessions and clients via framework dependencies.>

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

## Subagent Delegation Strategy (Hybrid Model)
> Apply this strategy when handling complex tasks, extensive refactors, large test suites, or when explicitly requested.

### The Case Against Maximum Delegation
Avoid blindly delegating every task to subagents because:
1. **Coordination Overhead**: Each subagent call requires prompt crafting, execution waiting, and result synthesis where returned summaries lose granular detail.
2. **Context Continuity Loss**: The main session accumulates implicit understanding (user preferences, edge cases tested, subtle project constraints). Subagents start fresh and only know what is explicitly passed.
3. **Decision-Making Quality**: Complex architectural choices require weighing multiple conversation factors. Subagents optimize locally for their slice but miss the system-wide picture.
4. **Interactive Refinement**: The main session allows immediate course correction; subagents execute blindly to completion before returning.

### Task Routing Matrix

| Task Type | Best Approach | Rationale |
|---|---|---|
| **Codebase Exploration** | Subagents (Explore) | Read-only scanning isolates token consumption from main context |
| **Multi-File Search / Grep** | Subagents | Deep searching without polluting conversation history |
| **Independent Parallel Tasks** | Background Subagents | Concurrent execution of decoupled units |
| **Complex Planning** | Plan Subagents | Draft and stress-test multi-phase execution plans |
| **Iterative Refinement** | Main Session | Tight feedback loops and incremental code edits |
| **Tasks Needing Feedback Loops**| Main Session | Fast user alignment and immediate verification |
| **Quick Operations (<30s)** | Main Session | Direct execution avoids delegation coordination overhead |

### Operational Workflow (Hybrid Model)
1. **Use Subagents for Research**: Offload codebase scanning, file searching, and pattern investigation.
2. **Keep Decisions in Main Session**: The main agent synthesizes subagent findings, aligns on design with the user, and maintains the overarching architecture.
3. **Use Memory for Continuity**: Persist key decisions, architectural patterns, and verified test results so context compaction does not lose them.
4. **Delegate Implementation of Well-Defined Tasks**: Once the approach is agreed upon in the main session, dispatch bounded, unambiguous tasks to subagents.

> **Key Rule**: Subagents are tools for gathering information and executing bounded work; the main session remains the "brain" that maintains coherent understanding of project goals.

## Git & PR Guidelines
- **Branch Naming**: `<type>/<issue-id>-<short-description>` (e.g. `feat/AUTH-102-jwt-refresh`)
- **Commit Format**: Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`)
- **Merge Strategy**: Squash and merge only.
