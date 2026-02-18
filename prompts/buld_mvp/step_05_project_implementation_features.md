# Agent Prompt — Step 5: Project Scaffold & Development Environment

## Your Role

You are a senior software engineer. Your job is to create the project scaffold and local development environment for the IntegrOn MVP. You are not designing — all structural and technology decisions have already been made in the SDD provided below. Your job is to implement exactly what is specified.

---

## Input

### MVP Architecture Design (Step 3 output)
<mvp_architecture>
{{PASTE MVP ARCHITECTURE CONTENT HERE}}
</mvp_architecture>

### Technical Stack Selection (Step 4 output)
<stack_selection>
{{PASTE STACK SELECTION CONTENT HERE}}
</stack_selection>

---

## Task

Produce all files necessary to set up the project from zero. A developer must be able to clone the repository, run a single command, and have a working local development environment with no additional setup.

### 1. Repository Structure
Create the full directory and file tree for the project, following the module structure defined in the MVP Architecture. Include every directory and file that needs to exist at scaffold time — even if the file is empty or contains only a placeholder.

For each file, provide its full content.

### 2. Dependency Management
Create the dependency manifest file(s) for the chosen language/runtime (e.g., `go.mod`, `package.json`, `pom.xml`, `pyproject.toml`). Include only the libraries chosen in Step 4. Pin versions.

### 3. Linter and Formatter Configuration
Create configuration files for the linter and formatter chosen in Step 4. The configuration must:
- Enforce the code style conventions appropriate for the chosen language
- Be runnable via a single command (e.g., `make lint`, `make fmt`)

### 4. Makefile (or equivalent task runner)
Create a `Makefile` (or the task runner appropriate for the chosen stack) with the following targets:

| Target | Action |
|--------|--------|
| `build` | Compile/build the application |
| `run` | Run the application locally |
| `test` | Run all tests |
| `lint` | Run the linter |
| `fmt` | Run the formatter |
| `dev-up` | Start the local development environment (Docker Compose) |
| `dev-down` | Stop the local development environment |

### 5. Docker Compose — Local Development Environment
Create a `docker-compose.yml` that provides all external dependencies needed for local development and testing:
- A relational database (matching the decision in Step 4)
- A local blob storage service (e.g., MinIO or Azurite, matching the decision in Step 4)
- Any other external service required by the MVP

The Compose file must:
- Use named volumes for persistence between restarts
- Expose all necessary ports
- Include a health check for each service
- Be ready to use with `make dev-up` without any manual configuration

### 6. Database Initialization Script
Create the SQL script that sets up the database schema required for the NFe/SEFAZ MVP use case:
- Table with columns for CNPJ, NSU, and quantity of NFe to retrieve
- Seed data with one example row so the pipeline can run immediately

### 7. Environment Variables
Create a `.env.example` file listing all environment variables the application requires, with placeholder values and a comment explaining each one. Create a `.env` file with values pre-filled for the local Docker Compose environment.

### 8. Example JSON Configuration File
Create a complete, ready-to-use `pipeline.example.json` configuration file for the NFe/SEFAZ use case, following exactly the JSON Schema defined in the MVP Architecture (Step 3). Use the local Docker Compose services as the target endpoints.

### 9. .gitignore
Create a `.gitignore` appropriate for the chosen language and tooling. Ensure it includes:
- The `.env` file (never committed)
- Build artifacts
- IDE files
- Any file that may contain secrets

### 10. CI Skeleton
Create a CI pipeline configuration file (GitHub Actions, GitLab CI, or the equivalent appropriate for the project) with the following jobs:
- `lint`: runs the linter
- `build`: compiles/builds the application
- `test`: runs all tests

The CI must run on every push to any branch.

---

## Output Format

For each file, use this format:

~~~
### `<relative/path/to/file>`
```<language>
<full file content>
```
~~~

After all files, produce a **Setup Instructions** section with the exact commands a developer must run to go from zero to a running local environment:

```
## Setup Instructions

1. <step>
2. <step>
...
```

---

## Constraints

- Implement **exactly** what is specified in the SDD — do not introduce new structure, patterns, or libraries not defined in Steps 3 and 4
- Every file must be **complete and ready to use** — no TODOs, no placeholders in functional code
- The local development environment must work **without internet access** after the initial image pull
- Secrets must never be hardcoded — use environment variables or the secrets mechanism defined in Step 4
- The scaffold must compile and pass linting with zero errors before any feature code is written
