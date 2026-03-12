# Prompt Engineering Specialists

This directory contains two complementary prompt engineering specialists — one for **agentic** contexts and one for **general LLM** contexts. Both are designed to run inside Claude Code.

---

## Prompts

### 1. `prompt_engineering_agent.md` — Agent Prompt Engineer

Specialist for designing and optimizing prompts that run as **AI agents** — systems that use tools, maintain session state, handle multi-turn interactions, and operate within agentic pipelines.

**Use when you need to:**
- Build a prompt for a Claude Code subagent
- Diagnose and fix an existing agent prompt (missing guardrails, broken tool policy, no error recovery)
- Design prompts for orchestrator/worker patterns
- Add session state, destructive action gates, or fallback behavior to an agent

**Do NOT use for:** simple one-shot tasks, chatbots, or content generation without tool use.

---

### 2. `prompt_engineering_llm.md` — LLM Prompt Engineer

Specialist for designing and optimizing prompts for **general LLM use cases** — one-shot tasks, structured queries, content generation, text analysis, classification, and simple chatbots.

**Use when you need to:**
- Write a prompt for a single API call or direct LLM interaction
- Improve a chatbot or content generation prompt
- Optimize prompts for classification, summarization, or structured output
- Tune prompts for a specific model (GPT, Gemini, Claude, Llama)

**Do NOT use for:** agents with tools, autonomous pipelines, or multi-turn session management.

---

## Installation

Both prompts can be installed at **user profile level** (available in all projects) or **project level** (scoped to one repo).

### User profile — available everywhere

```bash
# Agent specialist
cp prompt_engineering_agent.md ~/.claude/agents/prompt_engineering_agent.md

# LLM specialist
cp prompt_engineering_llm.md ~/.claude/agents/prompt_engineering_llm.md
```

### Project level — scoped to one project

```bash
# Run from inside the project root
mkdir -p .claude/agents

cp /path/to/prompt_engineering_agent.md .claude/agents/prompt_engineering_agent.md
cp /path/to/prompt_engineering_llm.md   .claude/agents/prompt_engineering_llm.md
```

---

## How to Use

### Option 1 — Ask Claude Code directly

Just describe your task and Claude Code will invoke the right specialist automatically:

```
Analyze this agent prompt and fix the gaps: ./my_agent.md
```

```
Build a prompt for an agent that reviews PRDs and writes a quality report
```

```
I need a prompt to classify customer support tickets — no tools, just a single API call
```

### Option 2 — Invoke explicitly via the Agent tool (in code or orchestrators)

```python
# Example using the Anthropic SDK with Claude Code agent tool
{
  "type": "tool_use",
  "name": "Agent",
  "input": {
    "subagent_type": "prompt_engineering_agent",
    "prompt": "Analyze and rewrite this prompt: ./agents/my_agent.md"
  }
}
```

### Option 3 — Reference in another agent prompt

```markdown
# SUBAGENT DELEGATION

When the user requests prompt creation or diagnosis, delegate to:
- subagent_type: `prompt_engineering_agent` — for agentic prompts
- subagent_type: `prompt_engineering_llm` — for general LLM prompts
```

---

## Decision Guide

```
Does the prompt involve tools, autonomous execution, or multi-turn state?
  ├── YES → prompt_engineering_agent.md
  └── NO  → prompt_engineering_llm.md
```

---

## File Reference

| File | Type | Folder for global install |
|---|---|---|
| `prompt_engineering_agent.md` | Claude Code subagent | `~/.claude/agents/` |
| `prompt_engineering_llm.md` | Claude Code subagent | `~/.claude/agents/` |
