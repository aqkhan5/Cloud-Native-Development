---
name: plan-mode-first
description: Guide for conducting rigorous architectural planning before implementing non-trivial tasks. Use when starting a new project, adding complex features, designing architecture, refactoring across multiple files, or when planning mode is explicitly requested.
---

# Plan Mode First (Always)

A procedural skill enforcing Boris Cherny's **"Plan Mode First"** workflow: separate architectural planning and user alignment from code execution.

---

## When to Invoke This Skill

**Invoke AUTOMATICALLY when:**
- Starting a brand-new project, service, or repository.
- Implementing non-trivial features (multi-file edits, schema changes, auth).
- Undertaking major refactoring across modules.
- The user uses `/plan` or requests architectural planning.

**Do NOT invoke when:**
- Making one-line typo fixes or single-line docstring edits.
- Running quick diagnostic commands (`git status`, test runs under 30s).

---

## The 5-Step Execution Workflow

```
1. Start with a Goal
   └── Define target outcome & scope boundaries
        │
2. Enter Plan Mode
   └── Restrict tools to read-only exploration & design drafting
        │
3. Discuss and Refine
   └── Present PLAN.md, iterate with user, verify edge cases
        │
4. Switch to Execution Mode
   └── Obtain explicit user agreement on the architecture
        │
5. One-Shot Execution
   └── Implement cleanly in a single pass & verify with tests
```

---

## Core Planning Checklist

Before modifying any source files, confirm that your proposed plan addresses:

1. **Impacted Files**: Explicit list of files created, modified, or deleted.
2. **Design Rationale**: Why this approach was selected over alternatives.
3. **Dependencies**: Whether new packages are required (with version rationale).
4. **Edge Cases**: Network timeouts, null states, error status codes, concurrency.
5. **Verification Steps**: Exact command lines with flags to verify the work.

---

## Bundled Utilities

### Automation Scripts (`scripts/`)
- `scripts/init_plan.py`: Scaffolds a pre-structured `PLAN.md` in the current directory.
  ```bash
  python3 path/to/plan-mode-first/scripts/init_plan.py "Feature Title"
  ```

### Assets (`assets/`)
- `assets/PLAN.template.md`: Full architectural plan template covering goals, tradeoffs, file mapping, and verification criteria.

### References (`references/`)
- [boris-cherny-workflow.md](references/boris-cherny-workflow.md): Deep background on Boris Cherny's philosophy, the economics of planning, and avoiding context thrashing.
