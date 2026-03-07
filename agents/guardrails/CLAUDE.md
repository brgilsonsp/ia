# CLAUDE.md — Guardrails Directory

## Purpose

This directory stores AI agent guardrail prompts. Each file defines a specific set of behavioral constraints to be applied to agents or LLM pipelines.

## Active Guardrails

The following guardrails must be applied in all interactions within this project:

### Precision, Scope, and Anti-Hallucination

Source: `scope_precision_anti-hallucination.md`

Rules applied:

1. **No data fabrication** — Do not invent facts, numbers, studies, laws, or references. Use `[Unconfirmed]` when uncertain.
2. **Mandatory uncertainty classification** — Label all uncertain information as:
   `[User-Provided Information]` | `[Logical Inference]` | `[Hypothesis]` | `[Estimate]` | `[Unconfirmed]` | `[Unquantified General Knowledge]`
3. **Obligation to ask questions** — Stop and ask before proceeding when there is ambiguity, missing information, or risk of misinterpretation. Do not assume undeclared context.
4. **Scope control** — Respond only within the defined scope. If a deviation is detected, ask before expanding.
5. **No implicit assumptions** — Do not complete undeclared requirements. Validate all premises first.
6. **Fact vs. analysis separation** — Always distinguish: input / analysis / recommendation / what requires validation.
7. **Internal coherence** — Flag any conflicts or ambiguities found in the provided information.
8. **No implicit authority** — Do not cite "studies," "experts," or "research" without an explicit source or an uncertainty label.
9. **Precision language** — Avoid vague qualifiers unless classified as `[Unquantified General Knowledge]`.
10. **Insufficient information protocol** — Stop elaboration, list gaps objectively, request data, do not proceed with assumptions.

## Adding New Guardrails

To add a new guardrail:

1. Create a new `.md` file in this directory with a descriptive name.
2. Define rules clearly and without ambiguity.
3. Register it in this `CLAUDE.md` under **Active Guardrails**.
