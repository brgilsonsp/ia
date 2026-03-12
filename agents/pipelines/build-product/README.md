# Pipeline Build Product — README

## What This Repository Is

This repository stores **agent-creation prompts** for building digital product specifications using Claude Code.

Each `.md` file in a pipeline directory is a **prompt** — meant to be pasted into Claude Code to create or configure a Claude Code agent. The agents themselves are not stored here; only the prompts used to instantiate them.

---

## Goal of All Pipelines

Every pipeline in this repository has the same ultimate goal:

> **Produce a complete, structured product specification** following the format defined in `prd_template.md`.

All pipelines must reference and comply with:
- `prd_template.md` — the mandatory output structure for PRDs
- `guardrails/scope_precision_anti-hallucination.md` (repo root) — mandatory guardrails applied to every agent

---

## Repository Structure

```
guardrails/                                            # repo root
└── scope_precision_anti-hallucination.md              # Mandatory guardrails for all agents

agents/pipelines/build-product/
├── README.md                                          # This file
├── CLAUDE.md                                          # Project conventions (agents must follow these)
├── prd_template.md                                    # Mandatory PRD output template
│
└── <pipeline-name>/                                   # One directory per pipeline
    ├── README.md                                      # Pipeline description: purpose, inputs, outputs, execution order
    └── <step-N>_<agent-role>.md                      # One prompt file per agent step
```

---

## Pipeline Naming Convention

| Element | Convention | Example |
|---|---|---|
| Pipeline directory | `pipeline_<name>/` | `pipeline_prd_from_scratch/` |
| Agent step file | `<NN>_<role>.md` | `01_product_strategist.md` |
| Step numbering | Two digits, sequential | `01`, `02`, `03`... |
| Role name | Lowercase, underscored, descriptive | `tech_lead`, `ux_researcher` |

---

## How Agents Interact Within a Pipeline

Agents in a pipeline may run **sequentially** or **in parallel**, depending on the pipeline design:

- **Sequential**: The output of step N is the input of step N+1. Use when each step depends on the result of the previous one.
- **Parallel**: Multiple agents run independently and their outputs are later consolidated. Use when steps are independent and can save time by running concurrently.

Each pipeline's `README.md` must explicitly define the execution order and data flow between steps.

---

## How to Use a Prompt

1. Open Claude Code.
2. Open the `.md` file for the agent step you want to run.
3. Copy the full content of the file.
4. Paste it into Claude Code as the agent's system prompt or initial instruction.
5. Provide the required inputs defined in that prompt.
6. Collect the output and pass it to the next step, if applicable.

---

## How to Create a New Pipeline

1. Create a new directory: `pipeline_<name>/`
2. Add a `README.md` with:
   - **Purpose**: What problem this pipeline solves
   - **Inputs**: What the user must provide to start the pipeline
   - **Outputs**: What artifacts the pipeline produces
   - **Steps**: Ordered list of agents, with execution mode (sequential/parallel) and data flow
3. Create one `.md` prompt file per agent step: `01_<role>.md`, `02_<role>.md`, etc.
4. Each prompt must include:
   - Agent **role and identity**
   - **Inputs** the agent expects
   - **Output** the agent must produce (format and structure)
   - Reference to `../guardrails/scope_precision_anti-hallucination.md` guardrails
   - Reference to `prd_template.md` if the agent produces PRD content

---

## Agent Prompt Structure (Template)

Each agent prompt file should follow this structure:

```
# ROLE
[Who this agent is and what it specializes in]

# GUARDRAILS
[Reference to scope_precision_anti-hallucination.md rules — copy or link]

# INPUT
[What this agent receives. List each input with name, type, and description]

# TASK
[What this agent must do — specific, verifiable, unambiguous]

# OUTPUT
[Exact format and structure of the output. Use the prd_template.md when applicable]

# CONSTRAINTS
[What this agent must NOT do — scope boundaries, forbidden assumptions, etc.]
```

---

## Existing Pipelines

| Pipeline | Description | Status |
|---|---|---|
| `pipeline_prd_from_scratch/` | Co-create a full PRD from a raw product idea (5 stages, 3 human gates) | Active |

---

## References

- Guardrails: `guardrails/scope_precision_anti-hallucination.md` (repo root)
- PRD Template: `prd_template.md`
- Project conventions: `CLAUDE.md`
