# skills/

Prompts ready to install as Claude Code skills. Copy files to `.claude/skills/` in a project or profile.

Skills run **inline in the main conversation** and are triggered manually with `/skill-name $ARGUMENTS`. Unlike agents, they don't use an isolated context window — every step is visible and interactive.

---

## Structure

```
skills/
├── roles/          # Prompt engineering specialists
├── consult/        # Business consulting personas
├── guardrails/     # Guardrail audit tool (AgentSentinel)
└── pipelines/
    └── sdd/        # SDD pipeline entry point
```

---

## How to install

```bash
# User profile — available in all projects
cp skills/roles/prompt_engineering_agent.md ~/.claude/skills/

# Project level — scoped to one repo
cp skills/roles/prompt_engineering_agent.md .claude/skills/
```

Invoke with `/filename` (without `.md` extension):

```
/prompt_engineering_agent Analyze and fix: ./agents/my_agent.md
/agent_sentinel ./agents/my_new_agent.md
/ceo_especialista_mvp_agent Tenho 15 features no meu MVP, o que cortar?
```

---

## Available skills

| File | Invocation | Description |
|------|------------|-------------|
| `roles/prompt_engineering_agent.md` | `/prompt_engineering_agent` | Design/optimize prompts for agentic contexts |
| `roles/prompt_engineering_llm.md` | `/prompt_engineering_llm` | Design/optimize prompts for general LLM use |
| `consult/ceo_especialista_mvp_agent.md` | `/ceo_especialista_mvp_agent` | MVP advisor for B2B SaaS founders (pt-BR) |
| `consult/consult_fundador_b2b_saas_brasil_agent.md` | `/consult_fundador_b2b_saas_brasil_agent` | B2B SaaS strategy consulting (pt-BR) |
| `guardrails/agent_sentinel.md` | `/agent_sentinel` | Audit agent prompts against 10 guardrails |
| `pipelines/sdd/prd-analysis-refinement-orchestrator.md` | `/prd-analysis-refinement-orchestrator` | PRD analysis and refinement pipeline (SDD) |

---

## See also

- `agents/` — subagent prompts (isolated context, auto-delegated by Claude)
- `guardrails/scope_precision_anti-hallucination.md` — 10 canonical rules applied across all skills
- `docs/skill_agent_doc.md` — when to use skills vs agents
