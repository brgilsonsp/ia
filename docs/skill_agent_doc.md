# Claude Code — Agents vs Skills

A practical guide on when to use each, how to create them, and where to save them.

---

## What Are They?

Claude Code has two main extension mechanisms for customizing and automating behavior:

| | **Subagent** | **Skill** |
|---|---|---|
| **Purpose** | Specialized AI assistant for isolated tasks | Reusable workflow or knowledge template |
| **Context** | Isolated (own context window) | Inline (main conversation) |
| **Trigger** | Auto-delegated by Claude or explicit request | Manual `/skill-name` or auto-match |
| **Returns** | One final message to the orchestrator | Continues inline in conversation |
| **File location** | `agents/` folder | `skills/` folder |

---

## Subagents

### What is a subagent?

A subagent is a specialized AI with its own system prompt, tool restrictions, and optionally its own model. When Claude receives a task that matches a subagent's description, it can **automatically delegate** the task to that subagent — or you can request it explicitly.

The subagent runs in an **isolated context window**: it does not see your full conversation history, and when it finishes, it returns a single final message back to the main conversation.

### Why use a subagent?

- **Isolation**: The subagent's work (file reads, analysis, long reasoning) does not bloat your main context
- **Specialization**: It has a focused system prompt with deep expertise for one type of task
- **Tool control**: You can restrict exactly which tools it can use
- **Autonomy**: Claude decides when to delegate — you don't need to trigger it manually
- **Parallelization**: Multiple subagents can run in background simultaneously

### When to use a subagent

Use a subagent when:

- The task **produces a standalone artifact** (a prompt, a report, a plan, an analysis)
- The task is **self-contained** — give it input, get back output
- You want the work done **without cluttering your main conversation**
- The task requires **deep specialization** (e.g., prompt engineering, security review, architecture design)
- You want Claude to **automatically recognize and delegate** the task type

Do NOT use a subagent when:
- You need to see and interact with intermediate steps
- The task is a multi-step workflow where you want control at each stage
- The task is a simple shortcut or command

### Real scenarios

| Scenario | Why subagent? |
|---|---|
| "Create an agent prompt for a git monitor" | Isolated, produces one artifact, benefits from specialization |
| "Analyze this PRD for quality and completeness" | Self-contained analysis, returns a structured report |
| "Review this code for security vulnerabilities" | Specialized expertise, isolated context, returns findings |
| "Research how Redis handles TTL expiration" | Deep research stays isolated, returns a clean summary |

### How to create a subagent

Create a Markdown file with YAML frontmatter:

```markdown
---
description: Short description — this is what Claude reads to decide when to delegate
tools: Read, Grep, Glob, Bash, WebSearch
model: claude-sonnet-4-6
---

# IDENTITY AND ROLE
You are a [specialist type]...

# TASK
What you must accomplish...

# INSTRUCTIONS
Step-by-step execution logic...

# OUTPUT FORMAT
How to structure your final response...

# GUARDRAILS
What you must never do...

# TOOL USE POLICY
When and how to use each tool...

# ERROR RECOVERY
What to do when something goes wrong...
```

**Mandatory frontmatter fields:**
- `description` — critical: Claude uses this to decide when to delegate

**Optional frontmatter fields:**
- `tools` — restrict which tools the agent can use (if omitted, inherits all)
- `model` — override the model for this agent
- `permissionMode` — `default`, `acceptEdits`, `bypassPermissions`
- `maxTurns` — limit the number of turns the agent can take

### Where to save a subagent

| Scope | Path | When to use |
|---|---|---|
| **User profile** (all projects) | `~/.claude/agents/name.md` | Specialists you want everywhere (prompt engineer, security reviewer) |
| **Project only** | `.claude/agents/name.md` | Agents specific to one codebase or domain |

### How subagents are invoked

```
# Automatically — Claude decides based on description match
"Create an agent prompt for a git monitor"
→ Claude invokes prompt_engineering_agent automatically

# Explicitly by name
"Use the prompt-engineering-agent to improve this prompt: ./my_agent.md"

# Programmatically via Agent tool
subagent_type: "prompt_engineering_agent"
prompt: "Analyze and rewrite: ./agents/my_agent.md"
```

---

## Skills

### What is a skill?

A skill is a reusable prompt template or workflow that runs **inline in your main conversation**. You trigger it manually with `/skill-name`, optionally passing arguments. Skills can include supporting files (templates, scripts, examples) and can inject dynamic content via shell commands.

### Why use a skill?

- **Manual control**: You decide exactly when to trigger it
- **Inline visibility**: Every step happens in your main conversation — you see progress and can intervene
- **Parameterization**: Accepts arguments via `$ARGUMENTS`, `$1`, `$2`
- **Reusability**: Define once, use in any project (if saved to profile)
- **Dynamic context**: Can run shell commands at invocation time and inject their output

### When to use a skill

Use a skill when:

- The task is a **multi-step workflow** where you want visibility at each step
- You want to **trigger it manually** at a specific moment
- The task involves **user interaction** during execution (decisions, confirmations)
- It is a **recurring workflow** you run frequently (implement feature, commit, deploy)
- You want to pass **specific arguments** at call time

Do NOT use a skill when:
- The task is fully autonomous and self-contained (use a subagent instead)
- You want Claude to decide when to trigger it without input (use a subagent)
- The task produces a large isolated artifact that would clutter the conversation

### Real scenarios

| Scenario | Why skill? |
|---|---|
| `implement-feature TICKET-42` | Multi-step workflow, user wants to see plan → code → test → commit |
| `create-pr "add CSV export"` | Sequential steps, needs confirmation before pushing |
| `daily-review` | Routine you trigger every morning — check PRs, issues, metrics |
| `scaffold-module payments` | Template-based generation, parameterized, runs inline |

### How to create a skill

Create a directory with a `SKILL.md` file inside:

```
~/.claude/skills/
└── implement-feature/
    ├── SKILL.md          ← required
    ├── template.md       ← optional supporting file
    └── checklist.md      ← optional supporting file
```

**`SKILL.md` structure:**

```markdown
---
description: Implement a feature end-to-end from ticket to pull request
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Implement the feature described in: $ARGUMENTS

Follow these steps:
1. Read the ticket or description provided
2. Explore the codebase to understand the impact area
3. Write an implementation plan and confirm with the user
4. Implement the changes
5. Write or update tests
6. Create a commit following the project's convention
7. Open a pull request
```

**Useful frontmatter fields:**

| Field | Description |
|---|---|
| `description` | What the skill does — used for auto-invocation matching |
| `user-invocable` | `true` to allow `/skill-name` invocation |
| `allowed-tools` | Restrict which tools the skill can use |
| `model` | Override the model for this skill |
| `disable-model-invocation` | `true` to prevent Claude from auto-triggering the skill |
| `context` | `fork` to run in an isolated subagent instead of inline |

**Argument substitution:**

```markdown
# In SKILL.md body:
Implement the feature: $ARGUMENTS     ← full argument string
Ticket: $1                            ← first argument
Branch: $2                            ← second argument
```

**Shell command injection (dynamic context):**

```markdown
---
description: Review open PRs
---

Current open PRs:
`!gh pr list --json number,title,author`

Review each one and summarize what needs attention.
```

### Where to save a skill

| Scope | Path | When to use |
|---|---|---|
| **User profile** (all projects) | `~/.claude/skills/name/SKILL.md` | Workflows you use everywhere (implement-feature, commit, daily-review) |
| **Project only** | `.claude/skills/name/SKILL.md` | Workflows specific to one project's conventions or tools |

### How skills are invoked

```
# Manual invocation
/implement-feature TICKET-42

# With multiple arguments
/scaffold-module payments service

# Auto-invocation (if disable-model-invocation is false)
"implement the export CSV feature from ticket 87"
→ Claude matches description and invokes automatically
```

---

## Decision Guide

```
Is the task self-contained and does it produce a standalone artifact?
  └── YES → Subagent

Is it a multi-step workflow where you want visibility and control?
  └── YES → Skill

Does Claude need to decide when to trigger it (no manual step)?
  └── YES → Subagent  (description-based auto-delegation)

Do you want to trigger it yourself at a specific moment?
  └── YES → Skill  (/skill-name)

Should intermediate steps stay out of the main conversation?
  └── YES → Subagent  (isolated context)

Do you need to pass arguments at call time?
  └── YES → Skill  ($ARGUMENTS)
```

---

## Folder Structure Reference

```
~/.claude/                          ← user profile (global, all projects)
├── agents/
│   ├── prompt_engineering_agent.md
│   └── security_reviewer.md
└── skills/
    ├── implement-feature/
    │   └── SKILL.md
    └── daily-review/
        └── SKILL.md

<project-root>/.claude/             ← project level (scoped to one repo)
├── agents/
│   └── domain_specialist.md
└── skills/
    └── scaffold-module/
        └── SKILL.md
```

**Priority order** (when names conflict): CLI flag > project `.claude/` > user `~/.claude/` > plugins

---

## This Project's Agents

| File | Type | Description |
|---|---|---|
| `agents/roles/prompt_engineering_agent.md` | Subagent | Designs and optimizes prompts for agentic contexts |
| `agents/roles/prompt_engineering_llm.md` | Subagent | Designs and optimizes prompts for general LLM use cases |

**Install to your profile:**

```bash
cp agents/roles/prompt_engineering_agent.md ~/.claude/agents/
cp agents/roles/prompt_engineering_llm.md   ~/.claude/agents/
```
