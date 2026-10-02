# AGENTS.md Specification & Content Guidelines

This reference defines the structural, sizing, and content rules for high-performance `AGENTS.md` (and `CLAUDE.md`) files.

---

## 1. Core Principles: Redundancy is the Enemy

Follow-up research on agent behavior revealed that auto-generated `AGENTS.md` files duplicating existing `README.md` content **actually reduced task success rates** and caused a **23% increase in token costs**.

Every line in `AGENTS.md` must contain high-signal information the agent **cannot** get by reading code, package manifests, or existing documentation.

---

## 2. Include vs. Exclude Matrix

| Include | Exclude | Why |
|---|---|---|
| **Non-obvious commands with flags** | Standard scripts already declared in `package.json` or `pyproject.toml` | Agents can already read manifests directly. |
| **Rules that differ from defaults** | Standard language conventions (e.g. PEP 8, Prettier formatting) | Agents already know standard language styles. |
| **Architecture constraints & directory mapping** | Full API documentation & tutorials | Link to docs; do not embed heavy prose in context. |
| **Explicit boundaries (files never to touch)** | Obvious platitudes (e.g. "write clean, maintainable code") | Wastes context budget. The agent already aims for clean code. |
| **Project-specific gotchas & tricky edge cases** | Information verbatim duplicated from `README.md` | Redundancy competes for attention budget and degrades performance. |

---

## 3. Strict Size Limits & Budgeting

- **Hard Ceiling**: Tools and models (such as OpenAI Codex) enforce a **32 KiB** default limit on `AGENTS.md`. Content beyond that limit is **silently truncated**.
- **Optimal Target**: **1 KiB - 4 KiB** (~200 to 800 tokens).
- **Rule of Thumb**: Keep it dense and brief. Every unnecessary token degrades retrieval precision across long multi-turn sessions.

---

## 4. Standard 6-Section Blueprint

1. **Project Overview**: Primary language, framework with exact versions, architectural paradigm.
2. **Build & Test Commands**: Exact commands with explicit flags (`uv run pytest tests/unit/ -v`, not "run tests").
3. **Code Style Guidelines**: Non-standard rules (e.g., "Named exports only", "All endpoints must be async").
4. **Project Structure & Boundaries**: Directory-to-responsibility map, plus explicit forbidden files/zones.
5. **Testing & Mocking**: Single test runner syntax, what to mock vs. real database usage.
6. **Git Workflow & Security**: Commit conventions, branch format, merge strategy, secrets handling.
