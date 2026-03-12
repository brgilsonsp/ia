# skills/pipelines/

Pipeline entry points — skills that trigger or orchestrate multi-agent pipelines.

These are the **user-facing entry points** for pipelines whose subagents live in `agents/pipelines/`. The user invokes the skill manually; the skill's orchestrator then dispatches subagents as needed.

---

## Available pipelines

| Subdirectory | Skill | Pipeline it triggers |
|---|---|---|
| `sdd/` | `/prd-analysis-refinement-orchestrator` | PRD quality analysis, technical feasibility, refinement, and estimation |

---

## Relationship with `agents/pipelines/`

```
User
 │
 │  /prd-analysis-refinement-orchestrator   ← skill (this directory)
 ▼
skills/pipelines/sdd/prd-analysis-refinement-orchestrator.md
 │
 │  dispatches via Task tool
 ▼
agents/pipelines/sdd/01-requirements-analyst.md
agents/pipelines/sdd/02-system-architect.md
... (subagents)
```

Skills in this directory are **orchestrators** — they coordinate, they don't implement.
