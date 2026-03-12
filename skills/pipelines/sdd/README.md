# skills/pipelines/sdd/

SDD pipeline entry point — invoked manually by the user to trigger PRD analysis and refinement.

---

## Skill

### `prd-analysis-refinement-orchestrator.md`

**Invocation:** `/prd-analysis-refinement-orchestrator <path/to/prd.md>`

**What it does:** Orchestrates a 4-stage pipeline with a multidisciplinary team:

| Stage | Agents | Output |
|-------|--------|--------|
| 1 — PRD Quality Analysis | Product Manager | Quality report |
| 2 — Technical Feasibility | Solution Architect + Tech Lead | Feasibility report |
| 3 — Refinement | Full team | Refined PRD |
| 4 — Estimation | Backend, Frontend, Mobile, DBA, DevOps, Security | Effort estimates |

**Key behaviors:**
- Automatic validation between stages (max 3 retries)
- Human review gates with pipeline resume support
- Original PRD is never modified — outputs are versioned files

---

## Installation

```bash
# User profile
cp prd-analysis-refinement-orchestrator.md ~/.claude/skills/

# Project level
cp prd-analysis-refinement-orchestrator.md .claude/skills/
```

---

## Usage

```
/prd-analysis-refinement-orchestrator ./docs/prd.md
```

Provide the path to the PRD file. The orchestrator reads it and starts Stage 1 automatically.

---

## Subagents

The implementation subagents for this pipeline live in `agents/pipelines/sdd/`.
