# agents/pipelines/

Multi-agent pipelines. Each subdirectory is a self-contained pipeline with its own agents, documentation, and conventions.

---

## Pipelines

| Pipeline | Entry point | Agents | Purpose |
|----------|------------|--------|---------|
| [`sdd/`](sdd/README.md) | Invoke agents sequentially (see README) | 10 subagents | Spec-Driven Development for web apps |
| [`build-product/`](build-product/README.md) | `prd-creation-orchestrator` (via skills/) | 1 orchestrator | Co-create a PRD from a raw product idea |

---

## How pipelines relate to skills/

Pipeline orchestrators that are triggered manually live in `skills/pipelines/`, not here.

- `skills/pipelines/sdd/prd-analysis-refinement-orchestrator.md` — analysis and refinement of an existing PRD
- The SDD agents (01–10) are invoked directly from `.claude/agents/` — no skill entry point needed

Implementation subagents always live here in `agents/pipelines/`.
