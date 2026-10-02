# Implementation Plan: <Feature / Task Title>

> Proposed plan drafted during Plan Mode. Do NOT edit code until this plan is agreed upon.

## 1. Goal & Objectives
- **Objective**: <Clear 1-2 sentence description of what will be achieved>
- **Scope Boundary**: <What is explicitly in scope vs. out of scope>

## 2. Architecture & Design Decisions
- **Chosen Approach**: <Summary of the design approach>
- **Trade-offs Evaluated**: <Alternatives considered and why this approach was selected>
- **New Dependencies**: <None / specific package with version rationale>

## 3. Impacted Files & New Components
| File Path | Action | Description |
|---|---|---|
| `<path/to/existing_file.py>` | Modify | <Brief summary of changes> |
| `<path/to/new_file.py>` | Create | <Purpose of new module> |
| `<path/to/tests/test_feature.py>` | Create / Modify | <Unit/integration tests covering new behavior> |

## 4. Step-by-Step Implementation Sequence
1. **Preparation**: <e.g. Add dependency or create migrations>
2. **Core Logic**: <e.g. Implement model/service layer>
3. **Endpoint / Interface**: <e.g. Wire up route handler or API controller>
4. **Validation & Tests**: <e.g. Add test fixtures and run test suite>

## 5. Edge Cases & Risk Mitigation
- **Failure Mode 1**: <Scenario & how the implementation handles it>
- **Failure Mode 2**: <Scenario & how the implementation handles it>
- **Rollback Strategy**: <How to revert if an unexpected error occurs>

## 6. Verification Criteria
- [ ] Run test suite: `<exact command, e.g. uv run pytest tests/test_feature.py -v>`
- [ ] Run linter & typecheck: `<exact command, e.g. uv run ruff check .>`
- [ ] Manual check / API response: `<exact curl or smoke test check>`
