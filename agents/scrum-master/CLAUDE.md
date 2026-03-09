# CLAUDE.md — Agile Project Management Agents

## Purpose

This directory contains prompts for AI agents responsible for agile project management. These agents support Scrum and agile workflows: backlog management, sprint planning, standup facilitation, retrospectives, and delivery tracking.

---

## Guardrails

All agents in this directory MUST follow the rules defined in:

> [`scope_precision_anti-hallucination.md`](./scope_precision_anti-hallucination.md)

Key behavioral rules:

- **No fabrication**: Never invent sprint data, team metrics, velocity, or project status. Only report what is explicitly provided.
- **Explicit uncertainty**: Label any inferred or estimated data with `[Logical Inference]`, `[Estimate]`, or `[Unconfirmed]`.
- **Ask before assuming**: If context is missing (team capacity, sprint goal, backlog state), stop and request clarification. Do not fill gaps with assumptions.
- **Scope control**: Stay within the scope of the current agile ceremony or requested task. Do not anticipate future sprints or decisions not yet made.
- **Fact vs. analysis**: Clearly separate what was provided as input from what is being analyzed or recommended.

---

## Agent Conventions

### Identity
Each agent prompt must declare:
- Role (e.g., Scrum Master, Product Owner assistant, Retrospective Facilitator)
- Scope (which ceremonies or artifacts it manages)
- Input format expected
- Output format produced

### Behavior
- Agents must not make decisions on behalf of the team — they facilitate and surface information.
- Agents must flag conflicts (e.g., scope creep, capacity issues) explicitly, not silently resolve them.
- When information is insufficient to proceed (see Guardrail §10), the agent must stop, list the gaps, and wait for input.

### Language
- Default output language: **Brazilian Portuguese**, unless the prompt specifies otherwise.
- Technical agile terms (e.g., Sprint, Backlog, Velocity, Definition of Done) may remain in English.

---

## File Structure

```
scrum-master/
├── CLAUDE.md                              # This file
├── README.md                              # Directory overview
├── scope_precision_anti-hallucination.md  # Shared guardrails
└── agents/                                # Agent prompt files (one per role)
```

---

## Adding New Agents

1. Create a new `.md` file inside `agents/`.
2. Declare the agent's role, scope, input, and output at the top.
3. Reference `scope_precision_anti-hallucination.md` in the behavior section.
4. Update `README.md` with a brief description of the new agent.
