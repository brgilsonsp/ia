# Agile Project Management Agents — Scrum Master

## Overview

This directory contains prompt files for AI agents designed to support agile product planning. The current focus is on **PRD analysis and sprint planning pipelines** — structured, multi-agent workflows that transform a Product Requirements Document into a fully estimated backlog with epics, tasks, story points, and hours.

All agents follow strict anti-hallucination and scope control rules embedded directly in their prompt files.

---

## Pipeline: PRD → Estimated Backlog

The main agent (`prd_pipeline_orchestrator.md`) orchestrates a 4-stage sequential pipeline:

| Stage | Agent(s) | Output |
|-------|----------|--------|
| 1 — PRD Quality Analysis | Product Manager | `resultado_analise_prd-PM_v[N].md` |
| 2 — Technical Feasibility | Arquiteto de Soluções | `resultado_analise_prd_AS_v[N].md` |
| 3 — Refinement | Tech Lead + Product Manager | `refinamento_prd_v[N].md` (status: `em andamento`) |
| 4 — Estimation | Specialists (BE, FE_WEB, FE_MOB, DBA, OPS, SEC) | `refinamento_prd_v[N].md` (status: `finalizado`) |

Automated validation gates (VALID agent) run between every stage — max 3 retries per gate. The pipeline pauses for human review when blockers are found and resumes after the human marks the file as `revisado`.

---

## Team

| Code | Role |
|------|------|
| `PM` | Product Manager |
| `ARCH` | Arquiteto de Soluções Digital |
| `TL` | Tech Lead Engenheiro de Software |
| `BE` | Engenheiro Backend Java/Spring |
| `FE_WEB` | Engenheiro Frontend Web React/TypeScript |
| `FE_MOB` | Engenheiro Frontend Mobile React Native |
| `DBA` | Database Administrator |
| `OPS` | Engenheiro DevOps/SRE Azure |
| `SEC` | Engenheiro de Segurança OWASP/LGPD |
| `VALID` | Validation Agent (internal) |

---

## Technology Stack (fixed)

Azure · Java 21 · Spring · React + TypeScript · React Native · Docker · OWASP · LGPD

No agent may recommend or assume technologies outside this stack.

---

## Agents

| Agent | Role | Status |
|-------|------|--------|
| [`prd_pipeline_orchestrator.md`](./prd_pipeline_orchestrator.md) | Scrum Master — Orchestrates the full PRD → Estimated Backlog pipeline (4 stages, validation gates, human-in-the-loop) | Ready |
| *(coming soon)* | Sprint Planner | Planned |
| *(coming soon)* | Daily Standup Facilitator | Planned |
| *(coming soon)* | Backlog Manager | Planned |
| *(coming soon)* | Retrospective Facilitator | Planned |
| *(coming soon)* | Sprint Review Assistant | Planned |

---

## How to Use

1. Open Claude Code in the directory where the PRD file is located.
2. Invoke the agent: `/prd_pipeline_orchestrator`
3. Provide the PRD — either as a file path or pasted content.
4. The pipeline runs automatically. When a blocker is found, it pauses and asks for human review.
5. To resume after review: open the flagged file, resolve the issue, set `status: revisado`, and reinvoke the agent.

The final output is `refinamento_prd_v[N].md` with all epics, tasks, story point estimates, and hours — ready for sprint planning.

---

## File Conventions

All generated files follow these rules:

- **Directory**: saved in the directory where the agent was invoked
- **Versioning**: `_v[N]` suffix — e.g., `resultado_analise_prd-PM_v1.md`
- **Status field** (mandatory in every generated file):

| Value | Set by | Meaning |
|-------|--------|---------|
| `em andamento` | Agent | Started, not complete |
| `aguardando revisão` | Agent | Blocked — awaiting human review |
| `revisado` | Human | Human reviewed and approved continuation |
| `finalizado` | Agent | Completed without blockers |

- **The original PRD is never modified** — under any circumstance, by any agent.

---

## Guardrails

All guardrails are embedded directly in each agent prompt. Key rules:

- No fabricated data, metrics, or requirements
- All inferences and estimates explicitly labeled (`[Inferência]`, `[Estimativa]`, `[Não Confirmado]`, etc.)
- Mandatory stop-and-ask when information is insufficient
- Strict scope control — no unsolicited recommendations
- No implicit authority ("best practices suggest", "the market adopts") without `[Conhecimento Geral Não Quantificado]`

---

## Conventions

- Output language: **Brazilian Portuguese**
- Agile and technical terms remain in English (Sprint, Backlog, Story Points, DoR, etc.)
- Each agent prompt is self-contained with all guardrails, input/output formats, and error recovery instructions

---

## Contributing

To add a new agent:

1. Create a `.md` file in this directory following the naming convention `[role]_[function].md`.
2. Include: role definition, context, task, instructions, guardrails, tool use policy, error recovery, and output format.
3. Add a row to the Agents table in this README.
