# SDD Agent Pipeline — Spec-Driven Development with Claude Code

A complete multi-agent pipeline for building full-stack products (Backend + Frontend Web + Mobile) using **Spec-Driven Development (SDD)** in Claude Code. The pipeline coordinates 17 specialized agents across 3 phases, combining sequential specification gates with parallel implementation to deliver quality at speed.

---

## Table of Contents

1. [What is Spec-Driven Development?](#what-is-spec-driven-development)
2. [Pipeline Architecture](#pipeline-architecture)
3. [Directory Structure](#directory-structure)
4. [The 17 Agents](#the-17-agents)
5. [Phase 1 — Sequential Specification](#phase-1--sequential-specification)
6. [Phase 2 — Parallel Implementation](#phase-2--parallel-implementation)
7. [Phase 3 — Review and Integration](#phase-3--review-and-integration)
8. [Human Approval Gates](#human-approval-gates)
9. [BDD and TDD Strategy](#bdd-and-tdd-strategy)
10. [Guardrails — Anti-Hallucination and Scope Control](#guardrails--anti-hallucination-and-scope-control)
11. [How to Use This in a New Project](#how-to-use-this-in-a-new-project)
12. [Prompt Files Reference](#prompt-files-reference)
13. [Design Decisions](#design-decisions)

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
| Tests written after implementation | TDD-first: failing unit tests committed before business logic |
| No behavior contract before coding | BDD: Gherkin feature files generated from acceptance criteria |
| Hard to review AI output | Structured review agents compare artifacts against specs |

---

## Pipeline Architecture

```
PRD (you provide)
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1 — SEQUENTIAL SPECIFICATION                          │
│                                                              │
│  Agent 01: Requirements Analyst                              │
│    reads: docs/prd.md + CLAUDE.md                            │
│    writes: docs/specs/requirements.md                        │
│                                                              │
│  Agent 01b: Requirements Reviewer  ◄─ automated gate        │
│    reads: docs/specs/requirements.md + docs/prd.md          │
│    writes: docs/reviews/requirements-review.md               │
│    ⏸ GATE 1: human reviews and approves                      │
│                                                              │
│  Agent 02: System Architect                                  │
│    reads: docs/specs/requirements.md + CLAUDE.md             │
│    writes: docs/specs/design.md                              │
│                                                              │
│  Agent 02b: Design Reviewer  ◄─ automated gate               │
│    reads: docs/specs/design.md + requirements.md             │
│    writes: docs/reviews/design-review.md                     │
│    ⏸ GATE 2: human reviews and approves                      │
│                                                              │
│  Agent 02c: BDD Spec Writer  ◄─ runs after Gate 2            │
│    reads: requirements.md + design.md                        │
│    writes: src/test/resources/features/*.feature             │
│                                                              │
│  Agent 03: Task Planner                                      │
│    reads: requirements.md + design.md + *.feature            │
│    writes: docs/specs/tasks.md                               │
│    ⏸ GATE 3: human reviews and approves                      │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2 — PARALLEL IMPLEMENTATION (TDD order)               │
│                                                              │
│  Agent 04: Orchestrator                                      │
│    reads: docs/specs/tasks.md                                │
│    dispatches subagents in parallel batches                  │
│                                                              │
│  BATCH 1 — Foundation (no dependencies)                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  DB Specialist · Backend Scaffold · Frontend Scaffold │   │
│  │  Mobile Scaffold · DevOps Engineer · Docs (ADRs)      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  BATCH 2 — TDD Pre-Implementation (depends on Batch 1)       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Test Engineer [test-unit] — failing tests only       │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  BATCH 3 — Business Logic (depends on Batch 2)               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Backend Developer · Security Engineer                │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  BATCH 4 — Integration + UI (depends on Batch 3)             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Test Engineer [test-integration] · Frontend Dev      │   │
│  │  Mobile Developer · Technical Writer (OpenAPI)        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  BATCH 5 — Full System Tests + Docs (depends on Batch 4)     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Test Engineer [test-e2e] [test-load] [test-contract] │   │
│  │  [test-mobile] · Technical Writer (guides, runbooks)  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│    writes: docs/progress.md (execution log)                  │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 3 — SEQUENTIAL REVIEW AND INTEGRATION                  │
│                                                              │
│  Agent 09: Code Reviewer                                     │
│    reads: src/ + tests/ + infra/ + docs/ vs. all specs       │
│    writes: docs/review.md                                    │
│    ⏸ GATE 4: human reviews and approves                      │
│                                                              │
│  Agent 10: Integration Agent                                 │
│    validates: frontend↔backend↔db alignment                  │
│    runs: full test suite and build                           │
│    writes: docs/integration-report.md                        │
└─────────────────────────────────────────────────────────────┘
```

### Why Hybrid Sequential + Parallel?

**Specification phases are sequential** because each phase validates and feeds the next, and human approval is required before advancing. You cannot design the system before knowing the requirements. You cannot plan tasks before the design exists.

**Review agents run automatically** before each human gate, pre-validating specs so humans can focus on judgment rather than checking completeness.

**Implementation phases are parallel** because once the specs are locked, tasks that touch different files and have no logical dependencies can run simultaneously. The Orchestrator dispatches independent tasks to isolated subagents, each with its own context window.

This combines three advantages: **quality through structured approval**, **speed through real parallelism**, and **reliability through automated pre-validation**.

---

## Directory Structure

This directory (`agents/pipelines/sdd-pipeline-build_product/`) is a **reference and template library**. The files here are copied into your target project, not used directly.

```
agents/pipelines/sdd-pipeline-build_product/
├── README.md                      ← This file
├── 01-requirements-analyst.md
├── 01b-requirements-reviewer.md
├── 02-system-architect.md
├── 02b-design-reviewer.md
├── 02c-bdd-spec-writer.md
├── 03-task-planner.md
├── 04-orchestrator.md
├── 05-backend-developer.md
├── 06-frontend-developer.md
├── 07-db-specialist.md
├── 08-test-engineer.md
├── 09-code-reviewer.md
├── 10-integration-agent.md
├── 11-mobile-developer.md
├── 12-devops-engineer.md
├── 13-security-engineer.md
└── 14-technical-writer.md
```

When you start a new project, your target project structure will look like this:

```
my-project/
├── CLAUDE.md                          ← Project constitution (all agents read this)
├── .github/
│   └── workflows/
│       ├── ci.yml                     ← CI: test + build (DevOps Engineer output)
│       └── cd.yml                     ← CD: push to GHCR + deploy to Azure
├── docs/
│   ├── prd.md                         ← Your PRD (you create this)
│   ├── progress.md                    ← Orchestrator execution log (auto-generated)
│   ├── review.md                      ← Code Reviewer output (auto-generated)
│   ├── integration-report.md          ← Integration Agent output (auto-generated)
│   ├── reviews/
│   │   ├── requirements-review.md     ← Requirements Reviewer output
│   │   └── design-review.md           ← Design Reviewer output
│   ├── specs/
│   │   ├── requirements.md            ← Requirements Analyst output
│   │   ├── design.md                  ← System Architect output
│   │   └── tasks.md                   ← Task Planner output
│   ├── security/
│   │   └── permission-matrix.md       ← Security Engineer output
│   ├── adr/
│   │   └── ADR-001-*.md               ← Architecture Decision Records
│   ├── guides/
│   │   └── integration-guide.md       ← Technical Writer output
│   ├── runbooks/
│   │   └── operations.md              ← Technical Writer output
│   └── infra/
│       └── github-secrets.md          ← DevOps Engineer secrets documentation
├── src/
│   ├── main/java/[package]/
│   │   ├── controller/
│   │   ├── service/
│   │   ├── repository/
│   │   ├── domain/
│   │   ├── dto/
│   │   ├── config/
│   │   └── exception/
│   ├── test/
│   │   ├── java/[package]/
│   │   └── resources/
│   │       └── features/              ← BDD Gherkin feature files
│   │           ├── auth.feature
│   │           └── [domain].feature
│   └── frontend/
│       └── src/
├── mobile/                            ← React Native app
│   └── src/
│       ├── screens/
│       ├── components/
│       └── navigation/
└── infra/
    ├── Dockerfile.backend
    ├── Dockerfile.frontend
    └── docker-compose.yml
```

---

## The 17 Agents

### Phase 1 — Specification

| # | File | Agent | Role | Input | Output |
|---|------|-------|------|-------|--------|
| 01 | `01-requirements-analyst.md` | Requirements Analyst | Generates requirements | `docs/prd.md` | `docs/specs/requirements.md` |
| 01b | `01b-requirements-reviewer.md` | Requirements Reviewer | Validates requirements | `requirements.md` + `prd.md` | `docs/reviews/requirements-review.md` |
| 02 | `02-system-architect.md` | System Architect | Generates design | `requirements.md` | `docs/specs/design.md` |
| 02b | `02b-design-reviewer.md` | Design Reviewer | Validates design | `design.md` + `requirements.md` | `docs/reviews/design-review.md` |
| 02c | `02c-bdd-spec-writer.md` | BDD Spec Writer | Generates Gherkin feature files | `requirements.md` + `design.md` | `src/test/resources/features/*.feature` |
| 03 | `03-task-planner.md` | Task Planner | Decomposes tasks | `requirements.md` + `design.md` + `*.feature` | `docs/specs/tasks.md` |

### Phase 2 — Implementation (subagents dispatched by Orchestrator)

| # | File | Agent | Task tags | Output |
|---|------|-------|-----------|--------|
| 04 | `04-orchestrator.md` | Orchestrator | — | `docs/progress.md` |
| 05 | `05-backend-developer.md` | Backend Developer | `[backend]` | Java 21 + Spring code in `src/main/java/` |
| 06 | `06-frontend-developer.md` | Frontend Developer | `[frontend]` | React + TypeScript in `src/frontend/` |
| 07 | `07-db-specialist.md` | DB Specialist | `[db]` | SQL migrations in `src/db/migrations/` |
| 08 | `08-test-engineer.md` | Test Engineer | `[test-unit]` `[test-integration]` `[test-e2e]` `[test-load]` `[test-contract]` `[test-mobile]` | Test code in `src/test/java/` and `e2e/` |
| 11 | `11-mobile-developer.md` | Mobile Developer | `[mobile]` | React Native + TypeScript in `mobile/` |
| 12 | `12-devops-engineer.md` | DevOps Engineer | `[devops]` | Dockerfiles, docker-compose, GitHub Actions workflows |
| 13 | `13-security-engineer.md` | Security Engineer | `[security]` | JWT filter, RBAC/ABAC, rate limiting, LGPD controls |
| 14 | `14-technical-writer.md` | Technical Writer | `[docs]` | OpenAPI annotations, ADRs, guides, runbooks |

### Phase 3 — Review and Integration

| # | File | Agent | Input | Output |
|---|------|-------|-------|--------|
| 09 | `09-code-reviewer.md` | Code Reviewer | All code + specs + infra + docs | `docs/review.md` |
| 10 | `10-integration-agent.md` | Integration Agent | All code + specs | `docs/integration-report.md` |

---

## Phase 1 — Sequential Specification

### Agent 01: Requirements Analyst

**Purpose**: Transform a raw PRD into a formal, exhaustive Requirements Specification.

**What it does**:
- Reads `docs/prd.md` and `CLAUDE.md`
- Assigns a unique ID to each functional requirement (`RF-001`, `RF-002`, ...)
- Defines at least one testable acceptance criterion per requirement
- Assigns priority levels: `P0` (critical), `P1` (high), `P2` (medium)
- Identifies ambiguities and either resolves them with `[Logical Inference]` or escalates via `AskUserQuestion`
- Defines non-functional requirements (RNF-XXX): performance, security, scalability, accessibility, observability
- Lists explicitly what is OUT of scope

**Output** (`docs/specs/requirements.md`)

---

### Agent 01b: Requirements Reviewer

**Purpose**: Automated pre-validation of `requirements.md` before human Gate 1.

**What it does** (6 review passes):
1. **PRD Coverage** — every PRD feature maps to at least one RF-XXX
2. **Invention Check** — no RF-XXX invented without a PRD source
3. **Acceptance Criteria Quality** — each criterion is testable and measurable
4. **NFR Completeness** — at least one RNF per PRD constraint
5. **Classification Labels** — all inferences labeled correctly
6. **Format & Consistency** — IDs unique, priorities present, out-of-scope defined

**Gate recommendation**: `APPROVED`, `CONDITIONAL`, or `BLOCKED`

**Output** (`docs/reviews/requirements-review.md`)

**Gate 1**: Review both `requirements.md` and `requirements-review.md`. Approve when all blockers resolved.

---

### Agent 02: System Architect

**Purpose**: Translate the approved requirements into a complete system design.

**What it does**:
- Maps every RF-XXX to a component, endpoint, or schema element
- Produces architecture decisions with justifications traceable to requirements
- Creates a component diagram (ASCII) showing all layers and external services
- Defines the complete database schema (tables, columns, types, constraints, indexes, relationships)
- Defines all API contracts (method, path, request, response 200/4XX/5XX, status codes)
- Documents main user flows
- Defines the security strategy (JWT, RBAC/ABAC, LGPD, OWASP coverage)

**Output** (`docs/specs/design.md`)

---

### Agent 02b: Design Reviewer

**Purpose**: Automated pre-validation of `design.md` before human Gate 2.

**What it does** (7 review passes):
1. **Requirements Coverage** — every RF-XXX has a design element
2. **Invention Check** — no endpoint or table invented without a requirement
3. **API Contract Completeness** — all endpoints have full request/response/error contracts
4. **DB Schema Completeness** — all tables have columns, types, constraints
5. **Security Strategy Completeness** — auth, authorization, OWASP, LGPD addressed
6. **Internal Consistency** — no endpoint references a non-existent table
7. **Format & Labels** — all inferences labeled, no vague language

**Gate recommendation**: `APPROVED`, `CONDITIONAL`, or `BLOCKED`

**Output** (`docs/reviews/design-review.md`)

**Gate 2**: Review `design.md` and `design-review.md`. Approve when all blockers resolved.

---

### Agent 02c: BDD Spec Writer

**Purpose**: Convert acceptance criteria into executable Gherkin feature files, establishing the behavioral contract before implementation.

**What it does**:
- Runs after Gate 2, before the Task Planner
- Reads `requirements.md` and `design.md` API contracts
- Produces one `.feature` file per feature domain in `src/test/resources/features/`
- Each scenario is tagged `@RF-XXX` linking it to its requirement
- Gherkin values (URLs, field names, status codes) come exactly from `design.md` — never invented
- Does NOT write step definitions (that is the Test Engineer's job in Batch 4)

**Output** (`src/test/resources/features/*.feature`)

---

### Agent 03: Task Planner

**Purpose**: Decompose the system design into atomic, parallelizable implementation tasks organized for TDD-first execution.

**What it does**:
- Reads `requirements.md`, `design.md`, `CLAUDE.md`, and all `.feature` files
- Decomposes every design element into an atomic task (1–2 hours of work each)
- Tags each task with the responsible agent (see tag table below)
- Maps dependencies and groups tasks into parallel batches following the TDD batch structure
- Applies conflict analysis: no two tasks in the same batch modify the same file
- Produces a File Ownership Map and a Coverage Verification table

**Task tags**:

| Tag | Agent | When |
|-----|-------|------|
| `[db]` | DB Specialist | Batch 1 — schema migrations |
| `[backend]` | Backend Developer | Batch 1 (scaffold) or Batch 3 (business logic) |
| `[frontend]` | Frontend Developer | Batch 1 (scaffold) or Batch 4 (UI implementation) |
| `[mobile]` | Mobile Developer | Batch 1 (scaffold) or Batch 4 (screens) |
| `[devops]` | DevOps Engineer | Batch 1 — Dockerfiles, docker-compose, CI/CD |
| `[security]` | Security Engineer | Batch 3 — JWT, RBAC/ABAC, rate limiting, LGPD |
| `[docs]` | Technical Writer | Batch 1 (ADRs) or Batch 4 (OpenAPI) or Batch 5 (guides, runbooks) |
| `[test-unit]` | Test Engineer | **Batch 2** — failing unit tests BEFORE Batch 3 backend |
| `[test-integration]` | Test Engineer | Batch 4 — Cucumber step definitions after backend is done |
| `[test-e2e]` | Test Engineer | Batch 5 — Cypress/Playwright after all frontend done |
| `[test-load]` | Test Engineer | Batch 5 — k6 when RNF defines a concrete threshold |
| `[test-contract]` | Test Engineer | Batch 5 — Pact consumer/provider |
| `[test-mobile]` | Test Engineer | Batch 5 — Detox after all mobile done |

**Gate 3**: Review `tasks.md`. Verify tasks are atomic, TDD order is correct, dependencies are correct, and all RF-XXX are covered.

---

## Phase 2 — Parallel Implementation

### Agent 04: Orchestrator

**Purpose**: Coordinate all implementation by dispatching tasks to subagents in safe parallel batches following TDD order.

**Key rules**:
- Dispatches ALL tasks in a batch simultaneously using `Task` with `run_in_background: true`
- Waits for the entire batch to complete before starting the next batch
- **TDD enforcement**: `[test-unit]` tasks in Batch 2 must fully complete and commit before any `[backend]` business-logic tasks in Batch 3 are dispatched
- Verifies each subagent's output and updates `docs/progress.md` after each batch
- Resolves minor failures autonomously; escalates blockers via `AskUserQuestion`

**Subagent routing**:

| Task tag | Subagent dispatched |
|----------|---------------------|
| `[backend]` | `backend-developer` |
| `[frontend]` | `frontend-developer` |
| `[db]` | `db-specialist` |
| `[mobile]` | `mobile-developer` |
| `[devops]` | `devops-engineer` |
| `[security]` | `security-engineer` |
| `[docs]` | `technical-writer` |
| `[test-unit]` `[test-integration]` `[test-e2e]` `[test-load]` `[test-contract]` `[test-mobile]` | `test-engineer` |

---

### Agent 05: Backend Developer

**Language/Framework**: Java 21 + Spring Boot, Spring Web, Spring Data JPA, Spring Security, Spring Validation, Spring Actuator

**Architecture**: Clean/Hexagonal — `controller/` `service/` `repository/` `domain/` `dto/` `config/` `exception/`

**Key behaviors**:
- Reads failing `[test-unit]` files before writing any code — blocked if they do not exist (TDD enforcement)
- Returns exact response shapes and status codes from `design.md` API contracts
- Applies `@Valid` on all `@RequestBody` parameters — never skips validation
- JWT authentication via `OncePerRequestFilter`; authorization via `@PreAuthorize`
- `@Transactional` on all service write methods
- Runs `./mvnw test` after implementation to confirm unit tests pass
- Never uses Node.js, TypeScript, or non-Java libraries

---

### Agent 06: Frontend Developer

**Language/Framework**: React + TypeScript + Vite (or as defined in `CLAUDE.md`)

**Key behaviors**:
- Strict TypeScript — no implicit `any`
- Calls only API endpoints defined in `design.md`
- Handles all response cases (200, 4XX, 5XX) with user-readable messages
- Accessibility: `aria-label`, semantic HTML, keyboard navigation
- Mobile-first responsive design

---

### Agent 07: DB Specialist

**Key behaviors**:
- Reversible SQL migrations with UP and DOWN blocks
- Exact column names, types, and constraints from `design.md` schema
- Named indexes: `idx_table_column`
- Idempotent seeds: `INSERT ... ON CONFLICT DO NOTHING`

---

### Agent 08: Test Engineer

**Categories and execution order**:

| Category | Tag | When | Framework | Blocker if missing |
|----------|-----|------|-----------|-------------------|
| Unit (TDD pre-impl) | `[test-unit]` | **Batch 2 — before backend** | JUnit 5 + Mockito | Yes — blocks Backend Developer |
| Integration (BDD step defs) | `[test-integration]` | Batch 4 — after backend | Testcontainers + Cucumber | No |
| E2E | `[test-e2e]` | Batch 5 | Cypress / Playwright | No |
| Load | `[test-load]` | Batch 5 | k6 | No — only when RNF defines a threshold |
| Contract | `[test-contract]` | Batch 5 | Pact | No |
| Mobile E2E | `[test-mobile]` | Batch 5 | Detox | No |

**TDD rule**: `[test-unit]` tasks must produce **failing** tests and **commit** a `BUILD FAILURE` log. The backend-developer verifies tests pass after implementation.

---

### Agent 11: Mobile Developer

**Language/Framework**: React Native + TypeScript

**Key behaviors**:
- Never stores tokens in AsyncStorage — uses `react-native-keychain` (Keychain/Keystore)
- Checks `package.json` before using any native module
- Uses `by.id()` test selectors for Detox compatibility
- Handles network errors gracefully; never crashes on native module unavailability
- Push notifications only when granted explicitly in `design.md`

---

### Agent 12: DevOps Engineer

**Key behaviors**:
- Docker multi-stage builds with non-root users and pinned base image tags
- `docker-compose.yml` with healthchecks, named volumes, and resource limits
- **GitHub Actions CI** (`.github/workflows/ci.yml`): 3 parallel jobs — test-backend (`./mvnw verify` + Testcontainers), test-frontend (`npm test`), build-images (Docker build only, no push)
- **GitHub Actions CD** (`.github/workflows/cd.yml`): build + push to GHCR, deploy to Azure VM via SSH — requires GitHub Environment approval gate
- Secrets safety: `grep -r "password\|secret\|token"` before every commit
- Documents required GitHub Secrets in `docs/infra/github-secrets.md`

---

### Agent 13: Security Engineer

**Key behaviors**:
- JWT: `JwtAuthenticationFilter extends OncePerRequestFilter`, validated via `SecurityFilterChain`
- RBAC: `@PreAuthorize` with role checks; ABAC: `PermissionEvaluator` for ownership checks
- Rate limiting: Redis token bucket → 429 + `Retry-After` header
- Security headers: HSTS, X-Frame-Options, CSP, X-Content-Type-Options
- CORS: no `allowedOrigins("*")` on authenticated endpoints
- Azure Key Vault: Spring Cloud Azure config for all secrets
- OWASP Top 10: A01–A09 addressed (as applicable to the project)
- LGPD: personal data map, granular consent per purpose, data subject rights (export + anonymization), audit trail

---

### Agent 14: Technical Writer

**Artifact types**:

| Tag | Artifact | Batch |
|-----|----------|-------|
| `[docs]` ADRs | Architecture Decision Records (MADR format) in `docs/adr/` | Batch 1 |
| `[docs]` OpenAPI | SpringDoc annotations on controllers and DTOs | Batch 4 |
| `[docs]` Integration Guide | `docs/guides/integration-guide.md` | Batch 5 |
| `[docs]` Onboarding | `docs/guides/technical-onboarding.md` | Batch 5 |
| `[docs]` Runbooks | `docs/runbooks/operations.md` | Batch 5 |

**Rules**: Never uses Bash tool. Uses only information from spec files. Example data is clearly fictional (no real CPFs, real emails).

---

## Phase 3 — Review and Integration

### Agent 09: Code Reviewer

**Purpose**: Structured, spec-driven code review of all Phase 2 output.

**7 review passes**:
1. **Test Coverage** — RF-XXX criteria have unit tests, integration tests, and load/contract/mobile tests where applicable
2. **API Contract Compliance** — endpoint method, path, request, response, status codes match `design.md` exactly
3. **DB Schema Compliance** — migrations match the schema; entity `@Column` annotations match migration column names
4. **Code Quality** — architecture layers, naming conventions, no business logic in controllers
5. **Security & LGPD** — JWT filter present, `@PreAuthorize` on protected endpoints, consent and audit controls present
6. **Documentation Compliance** — OpenAPI annotations on all controllers, ADRs present, runbooks present
7. **Infrastructure** — Dockerfiles have multi-stage builds and non-root users; CI/CD secrets not hardcoded

**Severity**:
- `P0 — Blocker`: unmet acceptance criterion, missing auth, wrong status code, data loss risk
- `P1 — Major`: wrong response shape, missing error handling, missing load test for a RNF threshold
- `P2 — Minor`: naming, missing Javadoc, style inconsistency

**Gate 4**: Resolve all P0 issues. Review P1 issues. Approve before integration.

---

### Agent 10: Integration Agent

**Purpose**: Validate that all components work together, then produce the final delivery verdict.

**What it does**:
- **Frontend↔Backend**: every API call in `src/frontend/` matches `design.md` endpoint, method, path, request shape
- **Backend↔Database**: every column reference in service/repository code matches the migration schema
- **Runs full test suite**: classifies failures as implementation bugs or test bugs
- **Runs build**: any build error is a P0 blocker
- Fixes integration-level issues autonomously (wrong URL strings, wrong field names, missing imports)
- Escalates anything requiring a design decision

**Verdict**: `READY FOR DELIVERY` or `BLOCKED`

---

## Human Approval Gates

| Gate | Artifact(s) to review | When | Key questions |
|------|----------------------|------|---------------|
| **Gate 1** | `requirements.md` + `requirements-review.md` | After Requirements Reviewer | All PRD features captured? No invented requirements? Acceptance criteria testable? Reviewer verdict APPROVED? |
| **Gate 2** | `design.md` + `design-review.md` | After Design Reviewer | Architecture satisfies all requirements? All APIs complete (request/response/errors)? Schema complete? Security strategy covers OWASP + LGPD? Reviewer verdict APPROVED? |
| **Gate 3** | `tasks.md` | After Task Planner | Tasks atomic? TDD order correct ([test-unit] before [backend])? No same-batch file conflicts? All RF-XXX covered? |
| **Gate 4** | `docs/review.md` | After Code Reviewer | All P0 issues resolved? P1 issues addressed or accepted? CI pipeline passes? |

Gates are intentional interruptions. The pipeline does not advance without your explicit approval. This is what makes SDD reliable.

---

## BDD and TDD Strategy

### Why BDD + TDD?

| Without BDD/TDD | With BDD/TDD |
|----------------|-------------|
| Tests written after code — test the implementation, not the behavior | Tests define the expected behavior before the implementation exists |
| AI may silently skip edge cases | Gherkin scenarios cover every acceptance criterion before a line of code is written |
| Hard to trace test failures to requirements | Every test is tagged `@RF-XXX` — a failure immediately names the broken requirement |
| No living documentation | Feature files are executable documentation readable by non-technical stakeholders |

### Execution Order (enforced by Orchestrator)

```
Gate 2 approved
     │
     ▼
BDD Spec Writer → writes Gherkin .feature files (behavioral contract)
     │
     ▼
Task Planner → reads .feature files, generates tasks.md with correct TDD batch order
     │
Gate 3 approved
     │
     ▼
Batch 1: DB + Scaffolding + DevOps + ADRs
     │
     ▼
Batch 2: Test Engineer writes FAILING unit tests → commits BUILD FAILURE log
     │  (Orchestrator verifies tests fail before dispatching Batch 3)
     ▼
Batch 3: Backend Developer + Security Engineer
     │  (Backend reads failing tests → implements until tests pass)
     ▼
Batch 4: Test Engineer writes Cucumber step defs + Frontend + Mobile + OpenAPI docs
     │
     ▼
Batch 5: E2E + Load + Contract + Mobile tests + Remaining docs
```

### TDD Enforcement

The Orchestrator enforces TDD by design:
- Before dispatching Batch 3, it verifies that every `[test-unit]` task committed a `BUILD FAILURE` log
- The Backend Developer is blocked from starting if no failing unit tests exist for the task
- If a `[backend]` task has no corresponding `[test-unit]` task in `tasks.md`, the Task Planner must flag it as a planning gap

---

## Guardrails — Anti-Hallucination and Scope Control

All 17 agents embed the same guardrail system. These rules govern agent behavior at every step.

### Information Classification

Every piece of information an agent outputs must be classified:

| Label | Meaning |
|-------|---------|
| `[User-Provided Fact]` | Directly stated in the PRD, requirements, or design |
| `[Logical Inference]` | Derived from context — not explicitly stated |
| `[Logical Inference from Tech Stack]` | Standard pattern for the chosen technology |
| `[Hypothesis]` | Plausible interpretation, not confirmed |
| `[Estimate]` | Approximation in absence of specification |
| `[Unconfirmed]` | Requires human validation before proceeding |

An agent must never present a `[Hypothesis]` or `[Logical Inference]` as a confirmed fact.

### The 10 Guardrail Rules

1. **No data fabrication**: Never invent facts, metrics, requirements, or references. Use `[Unconfirmed]` when uncertain.
2. **Mandatory uncertainty classification**: Every uncertain statement must be classified. Never present a hypothesis as fact.
3. **Obligation to ask**: If there is ambiguity or missing information, stop and use `AskUserQuestion` before continuing.
4. **Scope control**: Respond only to what was assigned. Do not expand into unsolicited areas.
5. **No implicit assumptions**: Do not assume undeclared technical, regulatory, or operational context.
6. **Fact vs. analysis separation**: Clearly separate what was provided, what is being analyzed, what is a recommendation, and what requires validation.
7. **Coherence**: Check for internal inconsistencies before finalizing. Flag conflicts — do not silently resolve them.
8. **No implicit authority**: Never use "studies show" or "experts say" without a source or `[Unconfirmed]` label.
9. **Precision language**: Avoid vague terms ("generally", "typically") unless labeled `[Unquantified General Knowledge]`.
10. **Insufficient information protocol**: Stop → list gaps → request data → wait. Do not proceed with assumptions.

---

## How to Use This in a New Project

### Step 1 — Set up the project structure

```bash
mkdir -p my-project/.claude/agents
mkdir -p my-project/docs/{specs,reviews,adr,security,guides,runbooks,infra}
mkdir -p my-project/src/{main,test}/java
mkdir -p my-project/src/test/resources/features
mkdir -p my-project/src/frontend/src
mkdir -p my-project/mobile/src
mkdir -p my-project/infra
mkdir -p my-project/.github/workflows
cd my-project
git init
```

### Step 2 — Copy the agent prompt files

```bash
# Copy all agent prompts to your project's agents directory
cp /path/to/agents/pipelines/sdd-pipeline-build_product/*.md my-project/.claude/agents/

# Claude Code identifies agents by the `name` field in each file's YAML frontmatter.
# The numeric prefix is for ordering in this repo only.
```

### Step 3 — Create your CLAUDE.md

Create `my-project/CLAUDE.md` with your project's tech stack and conventions:

```markdown
# Project: [Your Product Name]

## Tech Stack
- Backend: Java 21 + Spring Boot 3.x
- Frontend Web: React + TypeScript + Vite
- Mobile: React Native + TypeScript
- Database: PostgreSQL
- ORM: Spring Data JPA + Hibernate + Flyway
- Auth: JWT (HS256) — access token 1h, refresh 7d
- Cache/Sessions: Redis
- Container: Docker + docker-compose
- Cloud: Azure (VM, API Management, Key Vault, PostgreSQL Flexible Server, Monitor)
- CI/CD: GitHub Actions + GHCR

## Methodology: Spec-Driven Development (SDD)
1. No code is written without an approved spec
2. BDD: feature files define behavior before implementation
3. TDD: failing unit tests committed before business logic
4. Atomic commits after each task
5. Subagents NEVER spawn other subagents

## Code Conventions
- Comment language: Portuguese
- Variables/methods: camelCase
- Classes/Components: PascalCase
- Constants: SCREAMING_SNAKE_CASE
- Commits: Conventional Commits (feat:, fix:, docs:, test:)

## Important Paths
- PRD: docs/prd.md
- Requirements: docs/specs/requirements.md
- Design: docs/specs/design.md
- Tasks: docs/specs/tasks.md
- Feature files: src/test/resources/features/
```

### Step 4 — Write your PRD

Create `my-project/docs/prd.md` with your Product Requirements Document. It can be as rough as a few paragraphs. The Requirements Analyst will structure it.

### Step 5 — Invoke Phase 1 agents in sequence

Open Claude Code in your project directory (`claude` in the terminal), then:

**Invoke Agent 01 (Requirements Analyst):**
```
You are the requirements-analyst. Read docs/prd.md and generate docs/specs/requirements.md.
```

**Invoke Agent 01b (Requirements Reviewer):**
```
You are the requirements-reviewer. Read docs/specs/requirements.md and docs/prd.md.
Generate docs/reviews/requirements-review.md.
```
Review both files. Resolve any `BLOCKED` items, then approve (Gate 1).

**Invoke Agent 02 (System Architect):**
```
You are the system-architect. Read docs/specs/requirements.md and generate docs/specs/design.md.
```

**Invoke Agent 02b (Design Reviewer):**
```
You are the design-reviewer. Read docs/specs/design.md and docs/specs/requirements.md.
Generate docs/reviews/design-review.md.
```
Review both files. Resolve any `BLOCKED` items, then approve (Gate 2).

**Invoke Agent 02c (BDD Spec Writer):**
```
You are the bdd-spec-writer. Read docs/specs/requirements.md and docs/specs/design.md.
Generate Gherkin feature files in src/test/resources/features/.
```

**Invoke Agent 03 (Task Planner):**
```
You are the task-planner. Read docs/specs/requirements.md, docs/specs/design.md,
and all feature files in src/test/resources/features/. Generate docs/specs/tasks.md.
```
Review `tasks.md`. Confirm TDD order, no file conflicts, and all RF-XXX covered. Approve (Gate 3).

### Step 6 — Invoke the Orchestrator (Phase 2)

```
You are the orchestrator. Read docs/specs/tasks.md and implement all tasks
using the Task tool to dispatch specialized subagents in parallel batches.
Follow the TDD batch order: test-unit tasks must complete before backend business logic tasks.
```

The Orchestrator dispatches all subagents automatically. Monitor `docs/progress.md`.

### Step 7 — Invoke Phase 3 agents in sequence

**Invoke Agent 09 (Code Reviewer):**
```
You are the code-reviewer. Analyze all code in src/, mobile/, infra/, and .github/
against the approved specs in docs/specs/ and docs/reviews/.
Generate docs/review.md.
```
Review `docs/review.md`. Resolve all P0 issues, then approve (Gate 4).

**Invoke Agent 10 (Integration Agent):**
```
You are the integration-agent. Validate the complete system integration and
generate docs/integration-report.md.
```

Review `docs/integration-report.md`. If the verdict is **READY FOR DELIVERY**, the pipeline is complete.

---

## Prompt Files Reference

Each file is a self-contained, production-ready agent prompt with:

- **YAML frontmatter** (`name`, `description`, `tools`) — required by Claude Code for `.claude/agents/` autodiscovery
- **Identity and Role** — who the agent is and the boundaries of its behavior
- **Context** — pipeline position, inputs, outputs, and dependencies
- **Task** — what the agent must accomplish, scoped and specific
- **Instructions** — step-by-step execution logic with decision points
- **Output Format** — exact template the agent must follow for its output file
- **Guardrails** — behavioral constraints, scope limits, anti-hallucination rules
- **Tool Use Policy** — which tools to use, when, and how to report results
- **Error Recovery** — defined behavior for every critical failure mode
- **Final Checklist** — self-validation before writing output

### Agent files

| File | Agent | Key feature |
|------|-------|-------------|
| `01-requirements-analyst.md` | Requirements Analyst | Embedded `requirements.md` output template, PRD traceability |
| `01b-requirements-reviewer.md` | Requirements Reviewer | 6-pass review, BLOCKED/CONDITIONAL/APPROVED verdict |
| `02-system-architect.md` | System Architect | Full API contracts, DB schema, security strategy |
| `02b-design-reviewer.md` | Design Reviewer | 7-pass review, internal consistency validation |
| `02c-bdd-spec-writer.md` | BDD Spec Writer | Gherkin from acceptance criteria, @RF-XXX tags, no step definitions |
| `03-task-planner.md` | Task Planner | TDD batch structure, file conflict detection, 13 task tags |
| `04-orchestrator.md` | Orchestrator | TDD enforcement, parallel batch dispatch, progress logging |
| `05-backend-developer.md` | Backend Developer | Java 21 + Spring, Clean Architecture, TDD-first, `./mvnw test` |
| `06-frontend-developer.md` | Frontend Developer | React + TypeScript, strict types, accessibility |
| `07-db-specialist.md` | DB Specialist | Reversible migrations, UP/DOWN, index strategy |
| `08-test-engineer.md` | Test Engineer | 6 test categories, TDD BUILD FAILURE enforcement, Pact + Detox + k6 |
| `09-code-reviewer.md` | Code Reviewer | 7-pass review, P0/P1/P2 severity, security + LGPD pass |
| `10-integration-agent.md` | Integration Agent | Frontend↔Backend↔DB validation, build/test runner, READY/BLOCKED verdict |
| `11-mobile-developer.md` | Mobile Developer | React Native, Keychain storage, Detox selectors |
| `12-devops-engineer.md` | DevOps Engineer | Docker multi-stage, GitHub Actions CI + CD, GHCR, Azure VM deploy |
| `13-security-engineer.md` | Security Engineer | JWT filter, RBAC/ABAC, rate limiting, OWASP Top 10, LGPD |
| `14-technical-writer.md` | Technical Writer | OpenAPI (SpringDoc), ADRs (MADR), guides, runbooks |

---

## Design Decisions

### Why sequential for specs, parallel for implementation?

Spec phases have hard sequential dependencies: you cannot design what you have not specified, and you cannot plan tasks for a design that does not exist. Human approval gates enforce this. Implementation tasks, once specs are locked, can be parallelized safely because the Task Planner explicitly maps file ownership and removes all within-batch conflicts.

### Why review agents before each human gate?

Review agents (01b, 02b) perform mechanical completeness checks that humans would otherwise have to do manually. They catch missing IDs, untraced requirements, incomplete API contracts, and label violations before the human sees the artifact. This means Gate reviews focus on judgment (is this the right design?) rather than checking (did it forget an endpoint?).

### Why BDD before task planning?

Feature files establish the behavioral contract before any code or test task is planned. This means the Task Planner can reference concrete Gherkin scenarios when defining `[test-integration]` tasks, and the Test Engineer knows exactly which step definitions to implement. It also creates living documentation that non-technical stakeholders can validate before implementation begins.

### Why [test-unit] in Batch 2 before [backend] in Batch 3?

This enforces TDD at the pipeline level, not just at the developer level. The Orchestrator verifies that unit tests were committed and failed before dispatching the backend implementation tasks. The Backend Developer reads the failing tests before writing a single line of code. This eliminates the common pattern where AI writes code first and then writes tests that are trivially easy to pass.

### Why are subagents prohibited from using the Task tool?

The Task tool is how the Orchestrator spawns subagents. If a subagent could also spawn subagents, the pipeline could create unbounded agent trees with no way to track progress, detect failures, or maintain the batch-sequential execution order. The prohibition is absolute: subagents execute, they do not orchestrate.

### Why embed guardrails in every agent?

Each agent operates in an isolated context window — it has no memory of what other agents said or did. Embedding the same guardrail system in every prompt ensures that every agent, regardless of context, follows the same behavioral contract.

### Why use information classification labels?

`[Logical Inference]`, `[Unconfirmed]`, `[Estimate]` and the other labels make agent uncertainty explicit and visible in the output. When you review a spec document and see `[Logical Inference]`, you know exactly which statements were derived by the AI and which came directly from your PRD. This makes the review process faster and reduces the risk of silent assumptions becoming design decisions.
