# CLAUDE.md — Pipeline Build Product

## Project Purpose

This directory stores **agent pipeline prompts** for building digital product specifications.

Each pipeline is a structured sequence of AI agent steps that produces a specific output — such as a PRD, MVP scope, technical roadmap, or architecture definition.

---

## Project Structure

```
pipeline_build_product/
├── CLAUDE.md                              # This file
├── prd_template.md                        # Mandatory PRD output template
../guardrails/
└── scope_precision_anti-hallucination.md  # Mandatory guardrails (applied to all pipelines)
├── <pipeline-name>/                       # One directory per pipeline
│   ├── README.md                          # Pipeline description and usage
│   └── <step-N>_<agent-role>.md          # Agent prompt per step
```

---

## Pipelines in This Project

| Pipeline | Description |
|---|---|
| `pipeline_prd_from_scratch` | Create a full PRD starting from a raw product idea |
| `pipeline_mvp_from_prd` | Extract an MVP scope from an existing PRD |
| *(others to be added)* | — |

---

## Mandatory Rules for All Pipelines

### 1. Guardrails

All pipelines **must** apply the rules defined in `../guardrails/scope_precision_anti-hallucination.md`:

- No fabrication of facts, numbers, companies, studies, or references.
- Explicit uncertainty labeling: `[User-Provided Fact]`, `[Logical Inference]`, `[Hypothesis]`, `[Estimate]`, `[Unconfirmed]`.
- Stop and ask before proceeding when context is ambiguous or incomplete.
- Never fill gaps with implicit assumptions.
- Scope must be respected — do not expand into unsolicited areas.

### 2. PRD Template

When a pipeline produces a PRD, it **must** follow the structure and conventions of `prd_template.md` as the reference template.

### 3. Prompt Design Standards

- Each agent step must have a clearly defined **role**, **input**, and **output**.
- Prompts must be self-contained — no step should assume context from outside its defined inputs.
- Use structured output formats (tables, lists, labeled sections) for machine-readability.
- Avoid vague language. Prefer specific, verifiable statements.

### 4. Language

- Pipeline prompts are written in **English**.
- Product content (PRDs, specs) may be written in **Brazilian Portuguese** when targeting Brazilian products.

---

## How to Add a New Pipeline

1. Create a new directory: `pipeline_<name>/`
2. Add a `README.md` describing: purpose, inputs, outputs, and step sequence.
3. Create one `.md` file per agent step: `01_<role>.md`, `02_<role>.md`, etc.
4. Include the guardrails reference at the top of each agent prompt.

---

## References

- Guardrails: `../guardrails/scope_precision_anti-hallucination.md`
- PRD Template: `prd_template.md`
- PRD Example: `prd_example.md`
