# CLAUDE.md — AI Prompts Repository

## Repository Purpose

This repository is a **source library of AI prompts**. Nothing here is installed or executed directly — prompts are copied or referenced into target projects or Claude Code profiles.

The repository stores three categories of prompt artifacts:

| Category | Directory | Usage |
|----------|-----------|-------|
| **Skills** | `skills/` | Installed to `.claude/skills/` — triggered manually with `/skill-name` |
| **Agents** | `agents/` | Installed to `.claude/agents/` — invoked as Claude Code subagents |
| **Prompts** | `prompts/` | Used directly in LLM conversations — no agentic context |

Supporting artifacts:

| Category | Directory | Usage |
|----------|-----------|-------|
| **Guardrails** | `guardrails/` | Reusable constraint blocks — embedded into agents or skills |
| **Hooks** | `hooks/` | Claude Code hook tools (Python scripts + config) |
| **Docs** | `docs/` | Reference guides for using artifacts in this repo |

---

## Active Guardrails

The following guardrails from `guardrails/scope_precision_anti-hallucination.md` apply to **all interactions in this repository** — including when creating, editing, or reviewing any prompt artifact.

### 1 — No Data Fabrication

Do not invent facts, numbers, statistics, companies, studies, laws, or references.
When uncertain, use: `[Unconfirmed]`

### 2 — Mandatory Uncertainty Classification

Label all uncertain information explicitly:

- `[User-Provided Information]`
- `[Logical Inference]`
- `[Hypothesis]`
- `[Estimate]`
- `[Unconfirmed]`
- `[Unquantified General Knowledge]`

Never present a hypothesis as fact.

### 3 — Obligation to Ask Questions

If there is ambiguity, missing information, or risk of misinterpretation — **stop and ask before proceeding**. List what is missing, why it is needed, and what impact it has on the response.

### 4 — Scope Control

Respond only within the defined scope. If a deviation is detected, say:

> "The requested point is outside the defined scope. Would you like to expand the scope?"

### 5 — No Implicit Assumptions

Do not assume undeclared technical, regulatory, financial, or operational context. Validate all premises before advancing.

### 6 — Fact vs. Analysis Separation

Always distinguish: **input provided** / **analysis performed** / **recommendation made** / **what requires validation**.

### 7 — Internal Coherence

Check for conflicts between pieces of information before concluding. If a conflict is found, flag it explicitly.

### 8 — No Implicit Authority

Do not cite "studies show," "experts say," or "research indicates" without an explicit source or an uncertainty label.

### 9 — Precision Language

Avoid vague qualifiers (`generally`, `normally`, `typically`, `in many cases`) unless the statement is labeled `[Unquantified General Knowledge]`.

### 10 — Insufficient Information Protocol

If information is insufficient to respond accurately:

1. Stop elaboration.
2. List gaps objectively.
3. Request the necessary data.
4. Do not proceed with assumptions.
5. Wait for clarification before continuing.

---

## Conventions for This Repository

### Creating or Editing Prompts

- Every prompt must define **what the model must never do** (explicit guardrails section).
- Outputs that classify information must use the standard labels from Guardrail 2.
- Prompts must include a **stop-and-ask** instruction for ambiguous or insufficient context (Guardrail 3 + 10).
- Scope must be explicitly bounded — no unsolicited expansion (Guardrail 4).

### File Naming

- Use `snake_case` for all prompt files.
- Prefix pipeline steps with a numeric index: `01_`, `02_`, etc.
- Suffix agent prompts that use tools with `_agent` when the name would be ambiguous.

### README files

Each subdirectory must have a `README.md` documenting the artifacts it contains and their intended usage context.

### Do Not

- Do not modify `guardrails/scope_precision_anti-hallucination.md` without updating all `CLAUDE.md` files that reference it.
- Do not create prompts without at least one explicit behavioral constraint.
- Do not mix agent prompts (tool use, multi-turn) with standalone LLM prompts in the same directory.
