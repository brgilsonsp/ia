# AI Prompts Repository

A collection of prompts for use in other repositories or Claude Code profiles.
Nothing here is installed — this is a source library.

---

## Structure

```
ia/
├── prompts/          # standalone prompts for direct LLM use (no agentic context)
├── agents/           # prompts to install as .claude/agents/ (subagents)
├── skills/           # prompts to install as .claude/skills/ (manual triggers)
├── guardrails/       # reusable guardrail blocks (embed into agents or skills)
├── hooks/            # Claude Code hook tools (Python scripts + config)
└── docs/             # reference guides
```

---

## `prompts/`

Standalone prompts for direct conversation use. Not agents, not skills.

| Path | Description |
|------|-------------|
| `roles/prompt_engineering.md` | Prompt Engineer specialist |
| `product/product_manager_digital_service.md` | Product Manager — PRD co-creation via Socratic method |
| `translator/translator_br_to_en.md` | Brazilian Portuguese → American English translator |
| `consult/consult_fundador_b2b_saas_brasil.md` | Strategy consulting for Brazilian B2B SaaS founders |
| `validate_text/validate_pt_br_general_text.md` | Multi-lens reviewer for general pt-BR text |
| `validate_text/validate_pt_br_technical_text.md` | Multi-lens reviewer for technical pt-BR text |
| `build_mvp/step_01…06` | 6-step pipeline for MVP specification (sequential prompts) |

---

## `agents/`

Prompts formatted for Claude Code subagents. Install to `.claude/agents/` in a project.

```
agents/
└── pipelines/
    ├── sdd/                        # Spec-Driven Development pipeline
    │   ├── 01-requirements-analyst.md
    │   ├── 02-system-architect.md
    │   ├── 03-task-planner.md
    │   ├── 04-orchestrator.md
    │   ├── 05-backend-developer.md
    │   ├── 06-frontend-developer.md
    │   ├── 07-db-specialist.md
    │   ├── 08-test-engineer.md
    │   ├── 09-code-reviewer.md
    │   └── 10-integration-agent.md
    └── build-product/              # PRD creation pipeline
        ├── prd_template.md
        └── pipeline_prd_from_scratch/
            └── prd-creation-orchestrator.md
```

---

## `skills/`

Prompts formatted for Claude Code skills. Install to `.claude/skills/` in a project or profile.
Triggered manually with `/skill-name`.

```
skills/
├── roles/
│   ├── prompt_engineering_agent.md   # Prompt engineering for agentic contexts
│   └── prompt_engineering_llm.md     # Prompt engineering for general LLM use
├── consult/
│   ├── ceo_especialista_mvp_agent.md               # CEO advisor — MVP scope & prioritization
│   └── consult_fundador_b2b_saas_brasil_agent.md   # B2B SaaS strategy — Brazilian market
├── guardrails/
│   └── agent_sentinel.md             # Audits agent prompts against 10 guardrails
└── pipelines/
    └── sdd/
        └── prd-analysis-refinement-orchestrator.md  # Entry point for SDD pipeline
```

---

## `guardrails/`

Reusable guardrail content. Copy or reference from any agent or skill prompt.

| File | Description |
|------|-------------|
| `scope_precision_anti-hallucination.md` | 10 canonical rules: no fabrication, uncertainty labels, scope control, etc. |
| `CLAUDE.md` | Mandatory behavioral conventions for agents using these guardrails |

---

## `hooks/`

Claude Code hook tools — not prompts. Install to `.claude/` settings.

| Path | Description |
|------|-------------|
| `validate_english_prompt/` | Pre-prompt hook that validates English grammar (A2/B1 learner support) |

See `hooks/validate_english_prompt/LEIA-ME.md` for setup instructions.

---

## `docs/`

Reference guides.

| File | Description |
|------|-------------|
| `skill_agent_doc.md` | When to use agents vs skills, how to create and configure each |
| `pipeline-agentes-sdd-claude-code.md` | SDD pipeline architecture and methodology |

---

## Design Principles

All prompts follow these conventions:

- **Explicit guardrails** — every prompt defines what the model must never do
- **Certainty labeling** — outputs classify information as `[User-Provided Fact]`, `[Hypothesis]`, `[Estimate]`, etc.
- **Ask before assume** — models stop and ask when context is ambiguous or insufficient
- **Scope discipline** — models do not expand into unsolicited areas
