# The Boris Cherny "Plan Mode First" Workflow

This reference explains the **"Plan Mode First (Always)"** pattern created and championed by Boris Cherny (creator of Claude Code at Anthropic).

---

## 1. Core Philosophy

> *"A good plan is really important!"* — **Boris Cherny**

When working with autonomous coding agents, rushing to write code for non-trivial tasks introduces severe compounding failures:
- Incorrect assumptions about requirements or existing architecture.
- Wasted context tokens from failed attempts, rolled-back patches, and syntax errors.
- Unwanted side effects in dependent modules.

Separating **plan alignment** from **code execution** ensures that implementation is deterministic, swift, and accurate.

---

## 2. The 5-Step Pattern

| Step | Action | Description |
|:---:|:---|:---|
| **1** | **Start with a Goal** | State the target outcome clearly (e.g. *"Implement Stripe checkout webhook with signature verification"*). |
| **2** | **Enter Plan Mode** | Activate Plan Mode (`Shift + Tab` twice or type `/plan`). The agent is constrained to read-only exploration and plan drafting. |
| **3** | **Discuss and Refine** | Iterate collaboratively on the proposal, verify impacted files, and challenge edge cases until both user and agent agree. |
| **4** | **Switch to Execution** | Toggle out of Plan Mode into execution (auto-accept) mode. |
| **5** | **One-Shot Execution** | The agent implements the agreed-upon design in a clean, decisive pass and verifies it against the test suite. |

---

## 3. The Economics of Planning

- **Context Preservation**: Failed code iterations bloat the context window with irrecoverable token noise. A structured 500-token plan prevents 10,000 tokens of churn.
- **Fast Execution**: When the blueprint is exact, execution is rapid and typically succeeds on the very first try.
- **Interactive Course-Correction**: Clarifying an ambiguity during planning takes seconds; fixing a misunderstood architecture after writing 500 lines takes hours.
