# Subagent Delegation Guide: The Hybrid Model

This guide explains when and how to direct agents to delegate work to subagents versus retaining execution in the primary session.

---

## 1. The Case AGAINST Maximum Delegation

Blindly spinning up subagents for every subtask leads to severe operational inefficiencies:

### 1. Coordination Overhead
Each subagent invocation requires:
- Crafting a comprehensive prompt with all necessary background context.
- Waiting asynchronously for completion.
- Parsing, filtering, and integrating returned summaries (which frequently lose critical technical nuance).

### 2. Context Continuity Loss
The primary session continuously builds implicit understanding through conversation history:
- User style preferences and design philosophies.
- Approaches already tried and abandoned.
- Subtle domain constraints and edge cases.
Subagents start with a clean slate and only know what was explicitly forwarded in the delegation prompt.

### 3. Degradation in Decision-Making Quality
Complex technical decisions require weighing multiple interdependent factors that emerged throughout the conversation. A subagent given an isolated slice of the problem tends to optimize locally while compromising system-wide coherence.

### 4. Loss of Interactive Refinement
In the main session, an agent can course-correct immediately based on real-time user reactions and tool outputs. Subagents execute entirely to completion before returning, making course corrections expensive.

---

## 2. The Optimal Task Routing Matrix

| Task Type | Best Approach | Why |
|---|---|---|
| **Codebase Exploration** | Subagents (Explore) | Reading numerous files consumes context; subagents keep exploration ephemeral. |
| **Multi-File Search / Grep** | Subagents | Deep pattern searching is isolated from primary conversation tokens. |
| **Independent Parallel Tasks** | Background Subagents | Completely decoupled tasks run concurrently without blocking. |
| **Complex Planning** | Plan Subagents | Draft and stress-test architectural plans before committing. |
| **Iterative Refinement** | Main Session | Tight feedback loops and continuous dialogue with the user. |
| **Tasks Needing Feedback Loops** | Main Session | User input is required at each decision fork. |
| **Quick Operations (<30s)** | Main Session | Faster to run directly than paying delegation serialization overhead. |

---

## 3. The Recommended Hybrid Model

1. **Use Subagents for Research**: Offload reading, exploring, and multi-file search to subagents.
2. **Keep Decisions in Main Session**: The primary agent synthesizes findings and discusses tradeoffs with the user.
3. **Use Memory for Continuity**: Record key architectural decisions, test fixtures, and learnings so context compaction does not lose them.
4. **Delegate Implementation of Well-Defined Tasks**: Once the approach is agreed upon and unambiguous, dispatch execution to subagents.

> **Key Rule**: Subagents are tools for gathering information and executing defined tasks; the main session must remain the "brain" maintaining a coherent view of project goals.

---

## 4. When to Include in AGENTS.md

Embed the Subagent Delegation Strategy section into `AGENTS.md` when:
- The project is large or complex (monorepo, microservices, multiple frameworks).
- The test suite is complex (integration tests, mock servers, distributed fixtures).
- The user explicitly requests subagent delegation guidelines.
