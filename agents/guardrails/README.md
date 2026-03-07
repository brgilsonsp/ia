# Guardrails — AI Agent Behavioral Constraints

This directory stores guardrail definitions and guardrail-enforcing agents for AI pipelines built with Claude Code.

Guardrails are non-negotiable behavioral constraints applied to AI agents to prevent hallucination, scope drift, implicit authority, and fabrication. Every production-grade agent prompt in this project is expected to comply with the canonical guardrail set defined here.

---

## Directory Structure

```
guardrails/
├── README.md                              # This file
├── CLAUDE.md                              # Claude Code instructions for this directory
├── scope_precision_anti-hallucination.md  # The 10 canonical guardrails (source of truth)
└── agent_sentinel.md                      # AgentSentinel — guardrail audit agent
```

---

## Canonical Guardrails

Source: [`scope_precision_anti-hallucination.md`](./scope_precision_anti-hallucination.md)

| # | Guardrail | Summary |
|---|---|---|
| G1 | Prohibition of Data Fabrication | No invented facts, numbers, studies, or references. Use `[Unconfirmed]` when uncertain. |
| G2 | Mandatory Uncertainty Handling | Classify all uncertain information with standard tags. Never present a hypothesis as fact. |
| G3 | Obligation to Ask Questions | Stop and ask before proceeding when there is ambiguity or missing information. |
| G4 | Scope Control | Respond only within the defined context. Signal scope deviations explicitly. |
| G5 | Prohibition of Implicit Assumptions | Do not assume undeclared context. Validate all premises first. |
| G6 | Clear Separation Between Fact and Analysis | Distinguish input, analysis, recommendation, and what requires validation. |
| G7 | Coherence and Consistency | Check for internal inconsistencies. Flag conflicts. Never ignore ambiguities. |
| G8 | Prohibition of Implicit Authority | Do not cite authority ("studies show", "experts say") without a verifiable source. |
| G9 | Precision Language | Avoid vague qualifiers unless tagged as `[Unquantified General Knowledge]`. |
| G10 | Behavior When Information Is Insufficient | Stop, list gaps, request data, do not proceed with assumptions. |

### Uncertainty Classification Tags

| Tag | Meaning |
|---|---|
| `[User-Provided Information]` | Came directly from user input — not independently verified |
| `[Logical Inference]` | Derived from the inputs through reasoning |
| `[Hypothesis]` | A possible interpretation, not confirmed |
| `[Estimate]` | A quantitative approximation, not declared in the input |
| `[Unconfirmed]` | Could not be verified from available information |
| `[Unquantified General Knowledge]` | General knowledge used when precision is not possible |

---

## Agents

### AgentSentinel

**File:** [`agent_sentinel.md`](./agent_sentinel.md)

An audit agent that receives any AI agent prompt and:

1. Audits it against the 10 canonical guardrails
2. Reports which guardrails are `[PRESENT]`, `[PARTIAL]`, `[ABSENT]`, or `[CONFLICT]`
3. Detects structural conflicts between the prompt's existing instructions and guardrail requirements
4. Delivers an improved version of the prompt with all missing guardrails integrated
5. Saves the improved prompt to a new file — never overwriting the original

**Use when:** you have a new or existing agent prompt and want to validate and harden it before production use.

---

## Adding a New Guardrail

1. Add the rule to `scope_precision_anti-hallucination.md` following the existing format
2. Register it in `CLAUDE.md` under **Active Guardrails**
3. Update the table in this README
4. Update `agent_sentinel.md` — add it to the 10 canonical guardrails list in Phase 2 and to the OUTPUT FORMAT audit table

## Adding a New Agent

1. Create a new `.md` file in this directory
2. Name it descriptively (e.g., `agent_scope_enforcer.md`)
3. Add an entry for it in this README under **Agents**
