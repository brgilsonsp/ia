# SDD Agent Pipeline — Spec-Driven Development with Claude Code

A complete multi-agent pipeline for building web applications (Frontend + Backend) using **Spec-Driven Development (SDD)** in Claude Code. The pipeline coordinates 10 specialized agents across 3 phases, combining sequential specification gates with parallel implementation to deliver quality at speed.

---

## Table of Contents

1. [What is Spec-Driven Development?](#what-is-spec-driven-development)
2. [Pipeline Architecture](#pipeline-architecture)
3. [Directory Structure](#directory-structure)
4. [The 10 Agents](#the-10-agents)
5. [Phase 1 — Sequential Specification](#phase-1--sequential-specification)
6. [Phase 2 — Parallel Implementation](#phase-2--parallel-implementation)
7. [Phase 3 — Review and Integration](#phase-3--review-and-integration)
8. [Human Approval Gates](#human-approval-gates)
9. [Guardrails — Anti-Hallucination and Scope Control](#guardrails--anti-hallucination-and-scope-control)
10. [How to Use This in a New Project](#how-to-use-this-in-a-new-project)
11. [Prompt Files Reference](#prompt-files-reference)
12. [Design Decisions](#design-decisions)

---

## What is Spec-Driven Development?

**Spec-Driven Development (SDD)** is a methodology in which no code is written until a complete, human-approved specification exists. Every implementation decision is traceable to a requirement. Every agent reads the spec before acting.

The core rule: **specs first, code second, always.**

This approach eliminates the most common failure modes of AI-assisted development:

| Problem | SDD Solution |
|---------|-------------|
| AI invents features not asked for | No code without an approved spec |
| AI makes silent assumptions | Every ambiguity is surfaced and escalated |
| Output diverges from intent | Human approval gates between every phase |
| Agents contradict each other | Shared read-only spec files as single source of truth |
| Hard to review AI output | Structured review agent compares code against spec line by line |

---

## Pipeline Architecture

```
PRD (you provide)
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 1 — SEQUENTIAL SPECIFICATION                      │
│                                                          │
│  Agent 1: Requirements Analyst                           │
│    reads: docs/prd.md                                    │
│    writes: docs/specs/requirements.md                    │
│    ⏸ GATE 1: human reviews and approves                  │
│                                                          │
│  Agent 2: System Architect                               │
│    reads: docs/specs/requirements.md                     │
│    writes: docs/specs/design.md                          │
│    ⏸ GATE 2: human reviews and approves                  │
│                                                          │
│  Agent 3: Task Planner                                   │
│    reads: requirements.md + design.md                    │
│    writes: docs/specs/tasks.md                           │
│    ⏸ GATE 3: human reviews and approves                  │
└─────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 2 — PARALLEL IMPLEMENTATION                       │
│                                                          │
│  Agent 4: Orchestrator                                   │
│    reads: docs/specs/tasks.md                            │
│    dispatches subagents in parallel batches              │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │  BATCH N (all run simultaneously)                  │  │
│  │  ├─ Subagent: Backend Developer  → src/backend/   │  │
│  │  ├─ Subagent: Frontend Developer → src/frontend/  │  │
│  │  ├─ Subagent: DB Specialist      → src/db/        │  │
│  │  └─ Subagent: Test Engineer      → tests/         │  │
│  └────────────────────────────────────────────────────┘  │
│    writes: docs/progress.md (execution log)              │
└─────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 3 — SEQUENTIAL REVIEW AND INTEGRATION            │
│                                                          │
│  Agent 9: Code Reviewer                                  │
│    reads: src/ + tests/ vs. requirements.md + design.md  │
│    writes: docs/review.md                                │
│    ⏸ GATE 4: human reviews and approves                  │
│                                                          │
│  Agent 10: Integration Agent                             │
│    validates: frontend↔backend↔db alignment              │
│    runs: full test suite and build                       │
│    writes: docs/integration-report.md                    │
└─────────────────────────────────────────────────────────┘
```

### Why Hybrid Sequential + Parallel?

**Specification phases are sequential** because each phase validates and feeds the next, and human approval is required before advancing. You cannot design the system before knowing the requirements. You cannot plan tasks before the design exists.

**Implementation phases are parallel** because once the specs are locked, tasks that touch different files and have no logical dependencies can run simultaneously. The Orchestrator dispatches independent tasks to isolated subagents, each with its own context window.

This combines two advantages: **quality through structured approval**, and **speed through real parallelism**.

---

## Directory Structure

This repository (`pipeline-sdd/`) is a **reference and template library**. The files here are copied into your target project, not used directly.

```
pipeline-sdd/
├── README.md                                   ← This file
├── CLAUDE.md                                   ← Project instructions for Claude (embeds guardrails)
├── pipeline-agentes-sdd-claude-code.md        ← Original pipeline guide and architecture
├── prd-analysis-refinement-orchestrator.md    ← Agent: Scrum Master orquestrador de análise de PRD
└── prompts/                                    ← Production-ready agent prompt files
    ├── 01-requirements-analyst.md
    ├── 02-system-architect.md
    ├── 03-task-planner.md
    ├── 04-orchestrator.md
    ├── 05-backend-developer.md
    ├── 06-frontend-developer.md
    ├── 07-db-specialist.md
    ├── 08-test-engineer.md
    ├── 09-code-reviewer.md
    └── 10-integration-agent.md
```

When you start a new project, your target project structure will look like this:

```
my-project/
├── CLAUDE.md                    ← Project constitution (all agents read this)
├── docs/
│   ├── prd.md                   ← Your PRD (you create this)
│   ├── progress.md              ← Orchestrator execution log (auto-generated)
│   ├── review.md                ← Code Reviewer output (auto-generated)
│   ├── integration-report.md   ← Integration Agent output (auto-generated)
│   └── specs/
│       ├── requirements.md      ← Requirements Analyst output
│       ├── design.md            ← System Architect output
│       └── tasks.md             ← Task Planner output
├── .claude/
│   └── agents/                  ← Agent definitions (copied from prompts/)
│       ├── requirements-analyst.md
│       ├── system-architect.md
│       ├── task-planner.md
│       ├── orchestrator.md
│       ├── backend-developer.md
│       ├── frontend-developer.md
│       ├── db-specialist.md
│       ├── test-engineer.md
│       ├── code-reviewer.md
│       └── integration-agent.md
├── src/
│   ├── backend/
│   ├── frontend/
│   └── db/
└── tests/
```

---

## The 10 Agents

| # | File | Agent | Phase | Input | Output |
|---|------|-------|-------|-------|--------|
| 1 | `01-requirements-analyst.md` | Requirements Analyst | Phase 1 | `docs/prd.md` | `docs/specs/requirements.md` |
| 2 | `02-system-architect.md` | System Architect | Phase 1 | `requirements.md` | `docs/specs/design.md` |
| 3 | `03-task-planner.md` | Task Planner | Phase 1 | `requirements.md` + `design.md` | `docs/specs/tasks.md` |
| 4 | `04-orchestrator.md` | Orchestrator | Phase 2 | `tasks.md` | `docs/progress.md` |
| 5 | `05-backend-developer.md` | Backend Developer (subagent) | Phase 2 | task activation message | `src/backend/` |
| 6 | `06-frontend-developer.md` | Frontend Developer (subagent) | Phase 2 | task activation message | `src/frontend/` |
| 7 | `07-db-specialist.md` | DB Specialist (subagent) | Phase 2 | task activation message | `src/db/` |
| 8 | `08-test-engineer.md` | Test Engineer (subagent) | Phase 2 | task activation message | `tests/` |
| 9 | `09-code-reviewer.md` | Code Reviewer | Phase 3 | `src/` + `tests/` + specs | `docs/review.md` |
| 10 | `10-integration-agent.md` | Integration Agent | Phase 3 | all code + specs | `docs/integration-report.md` |

---

## Phase 1 — Sequential Specification

Phase 1 transforms your PRD into three structured specification documents. Each document is reviewed and approved by a human before the next agent begins.

### Agent 1: Requirements Analyst

**Purpose**: Transform a raw PRD into a formal, exhaustive Requirements Specification.

**What it does**:
- Reads `docs/prd.md` and `CLAUDE.md`
- Identifies every feature, capability, and constraint in the PRD
- Assigns a unique ID to each functional requirement (`RF-001`, `RF-002`, ...)
- Defines at least one testable acceptance criterion per requirement
- Assigns priority levels: `P0` (critical), `P1` (high), `P2` (medium)
- Identifies ambiguities and either resolves them with `[Logical Inference]` or escalates via `AskUserQuestion`
- Defines non-functional requirements (performance, security, scalability, accessibility, observability)
- Lists what is explicitly OUT of scope

**Output format** (`docs/specs/requirements.md`):
```
# Requirements Specification
## 1. Product Scope
## 2. Functional Requirements (RF-001, RF-002, ...)
## 3. Non-Functional Requirements (RNF-001, RNF-002, ...)
## 4. Ambiguities Identified and Resolutions
## 5. Out of Scope
## 6. Open Questions
```

**Gate 1**: Review `requirements.md`. Verify all PRD features are captured, ambiguities are resolved, and acceptance criteria are testable.

---

### Agent 2: System Architect

**Purpose**: Translate the approved requirements into a complete system design.

**What it does**:
- Reads `docs/specs/requirements.md` and `CLAUDE.md`
- Maps every RF-XXX to a design decision, component, endpoint, or schema element
- Produces architecture decisions with justifications, traceable to requirements
- Creates a component diagram showing frontend, backend, database, and external services
- Defines the complete database schema (all tables, columns, types, constraints, indexes, relationships)
- Defines all API contracts (method, path, request body, response shapes for all status codes)
- Documents the main user flows (step-by-step)
- Defines the security strategy (authentication method, authorization rules, data protection)

**Output format** (`docs/specs/design.md`):
```
# System Design
## 1. Architecture Decisions (table: decision, choice, justification, requirement)
## 2. Component Diagram (ASCII)
## 3. Database Schema (table per entity: columns, types, constraints)
## 4. API Contracts (per endpoint: request, response 200/4XX/5XX)
## 5. Main User Flows (step-by-step)
## 6. Security Strategy (authentication, authorization, data protection)
```

**Gate 2**: Review `design.md`. Verify the architecture satisfies all requirements, APIs are well-defined, the schema is complete, and the security strategy is sound.

---

### Agent 3: Task Planner

**Purpose**: Decompose the system design into atomic, parallelizable implementation tasks.

**What it does**:
- Reads `requirements.md`, `design.md`, and `CLAUDE.md`
- Decomposes every design element into an atomic task (1–2 hours of work each)
- Tags each task with the responsible agent: `[backend]`, `[frontend]`, `[db]`, or `[test]`
- Maps dependencies between tasks and groups them into parallel batches
- Applies conflict analysis: no two tasks in the same batch may modify the same file
- Produces a File Ownership Map showing which files each task modifies
- Produces a Coverage Verification table mapping every RF-XXX to its implementing task(s)

**Batch structure** (`docs/specs/tasks.md`):
```
# Implementation Tasks
## Batch 1 — Parallel (no dependencies)
  - TASK-001 [db] Create migration for users table
  - TASK-002 [backend] Scaffold Express project
  - TASK-003 [frontend] Scaffold React project
## Batch 2 — Parallel (depends on Batch 1)
  - TASK-004 [backend] Implement POST /api/auth/register (depends: TASK-001, TASK-002)
  - TASK-005 [frontend] Implement registration screen (depends: TASK-003)
## File Ownership Map
## Coverage Verification
```

**Gate 3**: Review `tasks.md`. Verify tasks are atomic, dependencies are correct, no parallel conflicts exist, and all requirements are covered.

---

## Phase 2 — Parallel Implementation

Phase 2 begins after Gate 3 approval. The Orchestrator reads `tasks.md` and dispatches subagents in parallel batches.

### Agent 4: Orchestrator

**Purpose**: Coordinate all implementation by dispatching tasks to subagents in safe parallel batches.

**What it does**:
- Reads `docs/specs/tasks.md` completely
- Initializes `docs/progress.md` with all tasks in "Pending" status
- For each batch: dispatches ALL tasks simultaneously using the `Task` tool with `run_in_background: true`
- Waits for the entire batch to complete before starting the next batch
- Verifies each subagent's output after the batch (commits, errors, conflicts)
- Updates `docs/progress.md` after each batch with actual status
- Resolves minor failures autonomously; escalates blockers via `AskUserQuestion`

**Subagent routing**:

| Task tag | Subagent |
|----------|----------|
| `[backend]` | `backend-developer` |
| `[frontend]` | `frontend-developer` |
| `[db]` | `db-specialist` |
| `[test]` | `test-engineer` |

**Dispatch message template** sent to each subagent:
```
Task ID: TASK-XXX
Task description: [from tasks.md]
Agent role: [agent name]
Files to create/modify: [from tasks.md File Ownership Map]
Requirement: RF-XXX
Design reference: [design.md section]

Before starting:
1. Read CLAUDE.md
2. Read docs/specs/design.md — focus on your relevant section
3. Read docs/specs/requirements.md — focus on the requirement above

Implement the task according to the specs. Commit when done:
"feat([scope]): [description] — TASK-XXX"
```

---

### Subagents (Agents 5–8)

All four subagents share the same behavioral contract:

**Common rules for all subagents**:
- Read `CLAUDE.md`, `design.md`, and `requirements.md` before writing any code
- Implement ONLY what is in the task activation message
- Do not modify any file outside the task's File Ownership Map entry
- Make one atomic commit per task using the Conventional Commits format
- **NEVER use the `Task` tool** — subagents execute, they do not orchestrate

**Agent 5: Backend Developer**
- Implements API endpoints following the exact contracts in `design.md`
- Validates all inputs with schema validation (Zod, Joi, or equivalent)
- Separates route handlers from business logic (service layer pattern)
- Enforces authentication middleware on all protected endpoints
- Writes JSDoc for all exported functions

**Agent 6: Frontend Developer**
- Implements React/TypeScript components and pages
- Uses strict TypeScript — no implicit `any`
- Calls only the API endpoints defined in `design.md`
- Handles all response cases (200, 4XX, 5XX) with user-readable messages
- Implements accessibility: `aria-label` on interactive elements, semantic HTML, keyboard navigation
- Mobile-first responsive design

**Agent 7: DB Specialist**
- Creates reversible SQL migrations with UP and DOWN blocks
- Uses the exact table names, column names, types, and constraints from `design.md`
- Adds indexes on all foreign key columns and query-pattern columns
- Follows naming conventions: tables plural snake_case, indexes named `idx_table_column`
- Seeds are idempotent: `INSERT ... ON CONFLICT DO NOTHING`

**Agent 8: Test Engineer**
- Derives every test case from an acceptance criterion in `requirements.md`
- Names tests in Portuguese: `"deve [behavior] quando [condition]"`
- Uses Arrange-Act-Assert structure
- Covers happy path + at least one edge case per criterion
- Writes unit tests (services/validators), integration tests (API endpoints), E2E tests (user flows)
- Minimum 80% line coverage per module
- Never modifies the test to make it pass if the implementation is the bug

---

## Phase 3 — Review and Integration

Phase 3 runs sequentially after all Phase 2 batches are complete.

### Agent 9: Code Reviewer

**Purpose**: Perform a structured, spec-driven code review of all Phase 2 output.

**What it does**:
- Reads all spec files and all code in `src/` and `tests/`
- Performs four review passes:
  1. **Acceptance Criteria Coverage**: every RF-XXX criterion has code and a test
  2. **API Contract Compliance**: every endpoint matches method, path, request, response, status codes
  3. **Database Schema Compliance**: every migration matches the schema in `design.md`
  4. **Security and Convention Compliance**: auth, input validation, naming, TypeScript strictness
- Classifies each issue by severity:
  - `P0 — Blocker`: acceptance criterion unmet, wrong status code, missing auth, data loss risk
  - `P1 — Major`: wrong response shape, missing error handling, test coverage below 80%
  - `P2 — Minor`: naming convention, missing JSDoc, style inconsistency

**Gate 4**: Review `docs/review.md`. All P0 issues must be resolved. Decide which P1 issues to fix before integration.

---

### Agent 10: Integration Agent

**Purpose**: Validate that all components work together as an integrated system, then produce the final delivery verdict.

**What it does**:
- **Frontend↔Backend**: verifies every API call in `src/frontend/` matches the endpoint, method, path, and request shape in `design.md`
- **Backend↔Database**: verifies every column reference in `src/backend/` matches the migration schema
- **Runs the full test suite**: analyzes failures and classifies them as implementation bugs or test bugs
- **Runs the build**: reports any build errors as P0 blockers
- Fixes integration-level issues autonomously (wrong URL strings, wrong field name strings, missing imports)
- Escalates anything requiring a design decision
- Produces `docs/integration-report.md` with verdict: **READY FOR DELIVERY** or **BLOCKED**

**Fix scope — what the Integration Agent can fix autonomously**:
- Wrong URL path strings
- Wrong field name strings
- Missing imports for existing modules
- Obvious typos in variable/field names

**Fix scope — what requires human escalation**:
- Business logic changes
- Auth/authorization strategy changes
- Database schema changes
- API contract changes
- Test assertion logic

---

## Human Approval Gates

| Gate | Artifact | When it runs | What to check |
|------|----------|--------------|---------------|
| **Gate 1** | `docs/specs/requirements.md` | After Requirements Analyst | All PRD features captured? Ambiguities resolved? Acceptance criteria testable? Out of scope defined? |
| **Gate 2** | `docs/specs/design.md` | After System Architect | Architecture satisfies requirements? APIs well-defined (all status codes)? Schema complete? Security strategy sound? |
| **Gate 3** | `docs/specs/tasks.md` | After Task Planner | Tasks are atomic? Dependencies correct? No file conflicts in same batch? All RF-XXX covered? |
| **Gate 4** | `docs/review.md` | After Code Reviewer | P0 issues resolved? P1 issues addressed or accepted? Ready for integration? |

Gates are intentional interruptions. The pipeline does not advance without your explicit approval. This is what makes SDD reliable — every phase's output is reviewed by a human before it becomes another phase's input.

---

## Guardrails — Anti-Hallucination and Scope Control

All 10 agents embed the same guardrail system, defined in `CLAUDE.md`. These rules govern agent behavior at every step.

### Information Classification

Every piece of information an agent outputs must be classified:

| Label | Meaning |
|-------|---------|
| `[User-Provided Fact]` | Directly stated in the PRD, requirements, or design |
| `[Logical Inference]` | Derived from context — not explicitly stated |
| `[Hypothesis]` | Plausible interpretation, not confirmed |
| `[Estimate]` | Approximation in absence of specification |
| `[Unconfirmed]` | Requires human validation before proceeding |

An agent must never present a `[Hypothesis]` or `[Logical Inference]` as a confirmed fact.

### The 10 Guardrail Rules

1. **No data fabrication**: Never invent facts, metrics, requirements, or references. Use `[Unconfirmed]` when uncertain.
2. **Mandatory uncertainty handling**: Every uncertain statement must be classified. Never present a hypothesis as fact.
3. **Obligation to ask**: If there is ambiguity or missing information, stop and use `AskUserQuestion` before continuing.
4. **Scope control**: Respond only to what was assigned. Do not expand into unsolicited areas or future phases.
5. **No implicit assumptions**: Do not assume undeclared technical, regulatory, or operational context.
6. **Fact vs. analysis separation**: Clearly separate what was provided, what is being analyzed, what is a recommendation, and what requires validation.
7. **Coherence**: Check for internal inconsistencies before finalizing. Flag conflicts — do not silently resolve them.
8. **No implicit authority**: Never use "studies show" or "experts say" without a source or `[Unconfirmed]` label.
9. **Precision language**: Avoid vague terms ("generally", "typically") unless labeled `[Unquantified General Knowledge]`.
10. **Insufficient information protocol**: Stop → list gaps → request data → wait. Do not proceed with assumptions.

### What happens when an agent detects ambiguity

```
Agent behavior when information is insufficient:

1. Stop the current elaboration
2. List the gaps: what is missing, why it matters, what impact it has
3. Use AskUserQuestion to request clarification
4. Wait for the human response
5. Resume only after receiving the answer
```

---

## How to Use This in a New Project

### Step 1 — Set up the project structure

```bash
mkdir -p my-project/.claude/agents
mkdir -p my-project/docs/specs
mkdir -p my-project/src/{backend,frontend,db}
mkdir -p my-project/tests
cd my-project
git init
```

### Step 2 — Copy the agent prompt files

```bash
# Copy all prompts from this repository to your project's agents directory
cp /path/to/pipeline-sdd/prompts/*.md my-project/.claude/agents/

# Rename files to remove the numeric prefix (Claude Code uses the filename's `name` frontmatter)
# The files are already named correctly in .claude/agents/ after renaming:
# 01-requirements-analyst.md → requirements-analyst.md
# etc.
```

### Step 3 — Create your CLAUDE.md

Create `my-project/CLAUDE.md` with your project's tech stack:

```markdown
# Project: [Your Product Name]

## Tech Stack
- Backend: [e.g., Node.js + Express + TypeScript / Python + FastAPI]
- Frontend: [e.g., React + TypeScript + Vite / Next.js]
- Database: [e.g., PostgreSQL]
- ORM / Query builder: [e.g., Prisma / Drizzle / raw SQL]
- Tests: [e.g., Vitest + Playwright / Jest + Cypress]
- Auth: [e.g., JWT / NextAuth / Supabase Auth]

## Methodology: Spec-Driven Development (SDD)
1. No code is written without an approved spec
2. Every agent reads specs before acting
3. Atomic commits after each task
4. Subagents NEVER spawn other subagents

## Code Conventions
- Comment language: Portuguese
- Variables: camelCase
- Classes/Components: PascalCase
- Commits: Conventional Commits (feat:, fix:, docs:, test:)

## Important Paths
- PRD: docs/prd.md
- Requirements: docs/specs/requirements.md
- Design: docs/specs/design.md
- Tasks: docs/specs/tasks.md
```

### Step 4 — Write your PRD

Create `my-project/docs/prd.md` with your Product Requirements Document. It can be as rough as a few paragraphs describing what you want to build — the Requirements Analyst will structure it.

### Step 5 — Invoke Phase 1 agents in sequence

Open Claude Code in your project directory (`claude` in the terminal), then:

**Invoke Agent 1:**
```
Você é o Requirements Analyst. Leia docs/prd.md e gere docs/specs/requirements.md.
```
Review `docs/specs/requirements.md`, then approve (Gate 1).

**Invoke Agent 2:**
```
Você é o System Architect. Leia docs/specs/requirements.md e gere docs/specs/design.md.
```
Review `docs/specs/design.md`, then approve (Gate 2).

**Invoke Agent 3:**
```
Você é o Task Planner. Leia docs/specs/requirements.md e docs/specs/design.md e gere docs/specs/tasks.md.
```
Review `docs/specs/tasks.md`, then approve (Gate 3).

### Step 6 — Invoke the Orchestrator (Phase 2)

```
Você é o Orchestrator. Leia docs/specs/tasks.md e implemente todas as tarefas
usando o Task tool para delegar a subagentes especializados em paralelo.
```

The Orchestrator will dispatch all subagents automatically. Monitor `docs/progress.md`.

### Step 7 — Invoke Phase 3 agents in sequence

**Invoke Agent 9:**
```
Você é o Code Reviewer. Analise todo o código em src/ e tests/ contra as specs aprovadas.
Gere docs/review.md.
```
Review `docs/review.md`, resolve P0 issues, approve (Gate 4).

**Invoke Agent 10:**
```
Você é o Integration Agent. Valide a integração completa do sistema e gere
docs/integration-report.md.
```

Review `docs/integration-report.md`. If the verdict is **READY FOR DELIVERY**, the pipeline is complete.

---

## Prompt Files Reference

Each file in `prompts/` is a self-contained, production-ready agent prompt with:

- **YAML frontmatter** (`name`, `description`) — required by Claude Code for `.claude/agents/` autodiscovery
- **Identity and Role** — who the agent is and the boundaries of its behavior
- **Context** — pipeline position, inputs, outputs, and dependencies
- **Task** — what the agent must accomplish, scoped and specific
- **Instructions** — step-by-step execution logic with decision points
- **Output Format** — exact template the agent must follow for its output file
- **Guardrails** — behavioral constraints, scope limits, anti-hallucination rules
- **Tool Use Policy** — which tools to use, when, and how to report results
- **Error Recovery** — defined behavior for every critical failure mode

### Prompt file sizes

| File | Size | Key feature |
|------|------|-------------|
| `01-requirements-analyst.md` | ~10 KB | Embedded `requirements.md` output template |
| `02-system-architect.md` | ~10 KB | Embedded `design.md` output template |
| `03-task-planner.md` | ~11 KB | Parallelism safety rules, file conflict detection |
| `04-orchestrator.md` | ~9 KB | Parallel dispatch protocol, progress logging |
| `05-backend-developer.md` | ~8 KB | Service layer pattern, input validation, security |
| `06-frontend-developer.md` | ~9 KB | TypeScript strictness, accessibility, API alignment |
| `07-db-specialist.md` | ~9 KB | Reversible migrations, index strategy, naming |
| `08-test-engineer.md` | ~9 KB | Criterion-to-test mapping, Portuguese test names |
| `09-code-reviewer.md` | ~10 KB | 4-pass review, P0/P1/P2 severity classification |
| `10-integration-agent.md` | ~11 KB | Frontend↔backend↔db validation, build/test runner |

---

## Design Decisions

### Why sequential for specs, parallel for implementation?

Spec phases have hard sequential dependencies: you cannot design what you have not specified, and you cannot plan tasks for a design that does not exist. Human approval gates enforce this.

Implementation tasks, once specs are locked, can be parallelized safely because the Task Planner explicitly maps file ownership and removes all within-batch conflicts. Tasks that touch `src/backend/` never share files with tasks in `src/frontend/` or `src/db/`.

### Why are subagents prohibited from using the Task tool?

The Task tool is how the Orchestrator spawns subagents. If a subagent could also spawn subagents, the pipeline could create unbounded agent trees with no way to track progress, detect failures, or maintain the batch-sequential execution order. The prohibition is absolute: subagents execute, they do not orchestrate.

### Why embed guardrails in every agent?

Each agent operates in an isolated context window — it has no memory of what other agents said or did. If guardrails were only in a shared system prompt, an agent that does not read that prompt would be unguarded. Embedding the same guardrail system in every prompt ensures that every agent, regardless of context, follows the same behavioral contract.

### Why use information classification labels?

`[Logical Inference]`, `[Unconfirmed]`, `[Estimate]` and the other labels make agent uncertainty explicit and visible in the output. When you review a spec document and see `[Logical Inference]`, you know exactly which statements were derived by the AI and which came directly from your PRD. This makes the review process faster and reduces the risk of silent assumptions becoming design decisions.

### Why Portuguese test names?

The SDD convention (`"deve [behavior] quando [condition]"`) produces test names that read as requirements in natural language. When a test fails, the error message tells you exactly which behavior is broken and under what condition — without needing to read the test code. This is especially valuable during Phase 3 integration review.
