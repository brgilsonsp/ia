# Pipeline: PRD From Scratch

## Purpose

Co-create a complete, high-quality PRD starting from a free-form product idea, through a structured pipeline of executor + validator agents.

The final output is a `.md` file following `prd_template.md`, written in Brazilian Portuguese, created in the directory where the orchestrator was invoked.

---

## Inputs

| Input | Format | Description |
|---|---|---|
| Product idea | Free-form text | Raw description of the product — can be 1 sentence or several paragraphs |

---

## Output

| Artifact | Format | Location |
|---|---|---|
| Final PRD | `prd_[product-slug]_v1.md` | Directory where the orchestrator was invoked |

---

## Execution Model

Single orchestrator agent that spawns sub-agents sequentially.

The orchestrator maintains state. Each sub-agent receives only the minimal input it needs — not the full conversation history.

---

## Pipeline Stages

```
[USER] Free-form product idea
       │
       ▼
┌─────────────────────────────────────┐
│ STAGE 1 — DISCOVERY                 │
│  Executor:  discovery_analyst        │
│  Validator: discovery_checker        │
│  ► HUMAN GATE 1: validate brief      │
└──────────────┬──────────────────────┘
               │ Structured Discovery Brief
               ▼
┌─────────────────────────────────────┐
│ STAGE 2 — PRODUCT STRATEGY          │
│  Executor:  product_strategist       │
│  Validator: strategy_checker         │
│  (runs autonomously)                 │
└──────────────┬──────────────────────┘
               │ PRD Sections 1 + 2
               ▼
┌─────────────────────────────────────┐
│ STAGE 3 — FEATURE DEFINITION        │
│  Executor:  feature_definer          │
│  Validator: feature_checker          │
│  ► HUMAN GATE 2: validate features   │
└──────────────┬──────────────────────┘
               │ PRD Section 4
               ▼
┌─────────────────────────────────────┐
│ STAGE 4 — REQUIREMENTS              │
│  Executor:  requirements_analyst     │
│  Validator: requirements_checker     │
│  (runs autonomously)                 │
└──────────────┬──────────────────────┘
               │ PRD Sections 3 + 5 + 6
               ▼
┌─────────────────────────────────────┐
│ STAGE 5 — PRD ASSEMBLY              │
│  Executor:  prd_assembler            │
│  Validator: prd_quality_gate         │
│  ► HUMAN GATE 3: final approval      │
└──────────────┬──────────────────────┘
               │
               ▼
     prd_[product-slug]_v1.md
```

---

## Human Gates

| Gate | Trigger | User Action |
|---|---|---|
| Gate 1 | After Discovery | Validate understanding of the product. Correct or approve. |
| Gate 2 | After Feature Definition | Add, remove, or adjust features. Approve scope. |
| Gate 3 | After PRD Assembly | Approve the final PRD or request targeted revisions. |

---

## Retry Policy

- Each stage: max **2 automatic retries** when validator returns FAIL.
- After 2 retries: orchestrator pauses, presents the issue to the user, and asks how to proceed.
- The orchestrator never proceeds past a failed validation without explicit user approval.

---

## Guardrails

All agents in this pipeline apply the rules defined in `../../guardrails/scope_precision_anti-hallucination.md`:

- No fabrication of facts, numbers, companies, references, or technical details.
- All uncertainty must be labeled: `[Inferência Lógica]`, `[Hipótese]`, `[Estimativa]`, `[Não Confirmado]`.
- Orchestrator stops and asks the user before proceeding when context is ambiguous.
- Scope is respected — agents do not expand into unsolicited areas.
- PRD original (if any) is never modified.

---

## How to Use

1. Open Claude Code in any directory where you want the PRD file to be created.
2. Invoke the agent defined in `orchestrator.md`.
3. Provide your free-form product idea when prompted.
4. Respond at each of the 3 human gates.
5. The final PRD file will be created in your current directory.

---

## References

- Orchestrator prompt: `prd-creation-orchestrator.md`
- PRD template: `../prd_template.md`
- Guardrails: `../../guardrails/scope_precision_anti-hallucination.md`
