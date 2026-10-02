# Concrete AGENTS.md Section Examples

Real-world, high-signal examples for each section of `AGENTS.md` across common ecosystems.

---

## Example 1: FastAPI + uv + SQLAlchemy (Python)

```markdown
## Project Overview
- Python 3.12, FastAPI 0.115, SQLAlchemy 2.0 (asyncio + asyncpg), Pydantic v2.
- Package manager: uv (enforce uv.lock).

## Build & Test Commands
- Dev Server: `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Full Test Suite: `uv run pytest -v`
- Single Test: `uv run pytest tests/api/test_items.py::test_create_item -v`
- Migrations: `uv run alembic upgrade head`
- Lint & Format: `uv run ruff check --fix . && uv run ruff format .`

## Code Style & Non-Standard Rules
- All database queries must use SQLAlchemy 2.0 `select()` syntax; no legacy `session.query()`.
- Endpoints must return explicit Pydantic response models using `response_model=...`.
- Never catch generic `Exception` without re-raising or logging via `structlog`.

## Project Structure & Boundaries
- `/app/api/`: Thin controllers; input validation only.
- `/app/services/`: Business transactions; all DB commits happen here.
- `/app/models/`: SQLAlchemy declarative tables.
- **Boundaries**: Never modify files under `/app/generated/`. Never commit `.env` or secret keys.

## Testing & Mocking
- Test Runner: pytest with `pytest-asyncio`.
- DB Isolation: Tests run against an isolated SQLite test database with transaction rollback after every test. Do NOT mock database calls.
- External APIs: Mock Stripe/Twilio calls using `respx`.
```

---

## Example 2: Next.js + TypeScript + Prisma (Node.js)

```markdown
## Project Overview
- Next.js 15 (App Router), TypeScript 5.5, Prisma ORM, Tailwind CSS.
- Package manager: pnpm.

## Build & Test Commands
- Dev Server: `pnpm dev`
- Build: `pnpm build`
- Unit Tests: `pnpm vitest run`
- Single Test: `pnpm vitest run src/components/button.test.tsx`
- E2E Tests: `pnpm playwright test`
- Typecheck: `pnpm tsc --noEmit`

## Code Style & Non-Standard Rules
- Server Components by default; add `'use client'` only when hook or DOM events are needed.
- Named exports only; no default exports except for Next.js page/route conventions.
- Data fetching must occur in Server Components or Server Actions; avoid `useEffect` for data loading.

## Project Structure & Boundaries
- `/src/app/`: Route segments, layouts, and page entrypoints.
- `/src/components/ui/`: Atomic presentation components (shadcn).
- `/src/lib/`: Database clients, utility functions, auth helpers.
- **Boundaries**: Do NOT edit `/prisma/migrations/` manually. Run `pnpm prisma migrate dev`.
```
