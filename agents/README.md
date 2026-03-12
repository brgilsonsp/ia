# agents/

Prompts ready to install as Claude Code subagents. Copy files to `.claude/agents/` in a project.

Agents run autonomously in isolated context windows. They are invoked by Claude or by an orchestrator via the `Task` tool — not triggered manually by the user.

---

## Structure

```
agents/
└── pipelines/
    ├── sdd/             # Spec-Driven Development — 10 agents for building web apps
    └── build-product/   # PRD creation pipeline — co-creates a full PRD from a raw idea
```

---

## How to install

Copy the agent `.md` files into your project's `.claude/agents/` directory:

```bash
# SDD pipeline
cp /path/to/agents/pipelines/sdd/*.md my-project/.claude/agents/

# PRD creation pipeline
cp /path/to/agents/pipelines/build-product/pipeline_prd_from_scratch/prd-creation-orchestrator.md my-project/.claude/agents/
```

Claude Code automatically reads all files in `.claude/agents/` and makes them available as subagents, identified by their `name` frontmatter field.

---

## Available pipelines

| Pipeline | Agents | Description |
|----------|--------|-------------|
| [`pipelines/sdd/`](pipelines/sdd/README.md) | 10 | Spec-Driven Development — requirements → design → tasks → parallel implementation → review |
| [`pipelines/build-product/`](pipelines/build-product/README.md) | 1 orchestrator + sub-agents | Co-create a complete PRD from a free-form product idea |

---

## See also

- `skills/` — prompts for manual triggers (skills), including pipeline entry points
- `guardrails/scope_precision_anti-hallucination.md` — 10 canonical rules embedded in all agents
- `docs/skill_agent_doc.md` — when to use agents vs. skills
