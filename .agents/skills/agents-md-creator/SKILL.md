---
name: agents-md-creator
description: Scaffolds, audits, and generates high-signal AGENTS.md and CLAUDE.md repository guides for AI coding agents. This skill should be used when the user wants to initialize or optimize an AGENTS.md or CLAUDE.md file for a repository, establish agent coding guidelines, configure explicit project boundaries and exact test commands, avoid token redundancy, or set up the Hybrid Subagent Delegation Model for complex architectures.
---

# AGENTS.md Creator

Generates dense, high-signal, non-redundant `AGENTS.md` (and `CLAUDE.md`) instructions for AI coding agents.

---

## Core Philosophy: Redundancy is the Enemy

Research shows that auto-generated agent instructions duplicating `README.md` content **reduce task success rates** and cause a **23% increase in token costs**. Every line must provide information the agent cannot infer from reading package manifests, standard language conventions, or existing code.

### Hard Constraints
- **Strict Ceiling**: Never exceed **32 KiB** (Codex silently truncates content beyond 32 KiB).
- **Target Size**: 1 KiB to 4 KiB (~200 to 800 tokens).

---

## Workflow Decision Tree

```
Generate AGENTS.md
  │
  ├── 1. Analyze Project Environment
  │      └── Run: python3 path/to/scripts/analyze_project.py [target_dir]
  │          • Detects language versions, package manager, frameworks, test runners
  │
  ├── 2. Select Architecture Pattern
  │      ├── Standard Project (Monolith, single API, linear tests)
  │      │     └── Use: assets/AGENTS.template.md
  │      │
  │      └── Complex Project (Multi-service, complex test suite, or requested delegation)
  │            └── Use: assets/AGENTS.hybrid-delegation.template.md
  │                • Embeds Subagent Task Routing Matrix & Hybrid Model
  │
  ├── 3. Populate 6 Core High-Signal Sections
  │      1. Project Overview (Versions & runtime stack)
  │      2. Build & Test Commands (Exact commands with flags)
  │      3. Code Style Rules (ONLY deviations from language defaults)
  │      4. Project Structure (Directory responsibility map)
  │      5. Testing & Mocking (Single-test runner, database isolation)
  │      6. Boundaries & Gotchas (Forbidden files, secrets, legacy code)
  │
  └── 4. Validate & Audit
         └── Run: python3 path/to/scripts/validate_agents_md.py [path/to/AGENTS.md]
             • Verifies size <= 32 KiB, checks for vague platitudes, audits sections
```

---

## Include vs. Exclude Rules

| INCLUDE in AGENTS.md | EXCLUDE from AGENTS.md | Reason |
|---|---|---|
| Exact commands with explicit flags (`uv run pytest tests/unit/ -v`) | Commands in package.json or pyproject scripts | Agents already read package manifests. |
| Rules differing from defaults (`Named exports only`) | Standard conventions (PEP 8, Prettier) | Agents already know standard styles. |
| Directory responsibility mapping | Full API documentation & tutorials | Link to external docs; do not embed. |
| Explicit boundaries (e.g. `Never edit /generated/`) | Generic advice (e.g. "write clean code") | Wastes context; agents already try to write clean code. |
| Project-specific gotchas & tricky workarounds | Verbatim copies of README.md | Redundancy confuses agent attention and raises costs. |

---

## Subagent Delegation: The Hybrid Model

When a repository contains complex architectures or test suites, or when the user requests it, include the **Hybrid Subagent Model** in `AGENTS.md`:

### The Case Against Maximum Delegation
1. **Coordination Overhead**: Detailed prompting, async waiting, and parsing summaries loses technical detail.
2. **Context Continuity Loss**: The main session maintains implicit conversation understanding; subagents start fresh.
3. **Decision-Making Quality**: Complex decisions require holistic context; subagents only optimize locally.
4. **Interactive Refinement**: The main session enables real-time course correction based on immediate user reactions.

### Optimal Task Routing

| Task Type | Best Approach | Rationale |
|---|---|---|
| **Codebase Exploration** | Subagents (Explore) | Isolated ephemeral file scanning |
| **Multi-File Search / Grep** | Subagents | Large search results do not bloat main context |
| **Independent Parallel Tasks** | Background Subagents | Concurrent execution of decoupled units |
| **Complex Planning** | Plan Subagents | Draft and stress-test execution plans |
| **Iterative Refinement** | Main Session | Tight feedback loops with user |
| **Tasks Needing Feedback Loops** | Main Session | Real-time alignment on design decisions |
| **Quick Operations (<30s)** | Main Session | Direct execution avoids delegation serialization |

### Hybrid Model Principles
1. **Use Subagents for Research**: Exploration, searching, and understanding patterns.
2. **Keep Decisions in Main Session**: Primary agent synthesizes findings and discusses with user.
3. **Use Memory for Continuity**: Persist key decisions and patterns so context compaction does not erase them.
4. **Delegate Implementation of Well-Defined Tasks**: Once agreed upon, subagents execute bounded slices.
- *Key Insight*: Subagents are tools for gathering information and executing work; the main session is the "brain".

---

## Bundled Utilities

### Automation Scripts (`scripts/`)
- `scripts/analyze_project.py`: Detects project stack, package managers, and directories to scaffold drafting inputs.
- `scripts/validate_agents_md.py`: Audits `AGENTS.md` / `CLAUDE.md` against size limits, required sections, and anti-patterns.

### Assets (`assets/`)
- `assets/AGENTS.template.md`: Standard baseline template with all 6 required sections.
- `assets/AGENTS.hybrid-delegation.template.md`: Extended template with the Hybrid Subagent Strategy for complex repos.

### References (`references/`)
- [agents-md-spec.md](references/agents-md-spec.md): Sizing constraints, attention budgeting, and include/exclude matrix.
- [subagent-delegation-guide.md](references/subagent-delegation-guide.md): Complete rationale and strategy for the Hybrid Subagent Model.
- [section-examples.md](references/section-examples.md): Real-world examples for Python, TypeScript/Next.js, and more.
