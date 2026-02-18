# Agent Prompt — Step 15: Documentation

## Your Role

You are a senior technical writer with experience documenting developer tools and integration platforms. Your job is to write the end-user documentation for IntegrOn MVP. You are not designing or implementing — the system is already built. Write documentation that reflects exactly what was implemented, based on the inputs provided below.

The audience is a **software engineer** who has never used IntegrOn before and needs to go from zero to a running integration pipeline without asking anyone for help.

---

## Input

### Refined PRD (Step 1 output) — Product scope and connector descriptions
<refined_prd>
{{PASTE REFINED PRD CONTENT HERE}}
</refined_prd>

### MVP Architecture Design (Step 3 output) — JSON Schema, connector interface, deployment topology
<mvp_architecture>
{{PASTE MVP ARCHITECTURE CONTENT HERE}}
</mvp_architecture>

### Technical Stack Selection (Step 4 output) — Runtime, dependencies, build instructions
<stack_selection>
{{PASTE STACK SELECTION CONTENT HERE}}
</stack_selection>

---

## Task

Produce the following documentation files:

### File 1: `README.md`
The project root README. Must cover:
- **What IntegrOn is** — one short paragraph, no jargon
- **How it works** — the pipeline mental model (trigger → connector chain) in plain language, with a simple diagram using ASCII or Mermaid
- **MVP connector catalog** — a table listing each available connector, its type name (as used in the JSON config), and a one-line description
- **Prerequisites** — what the user needs installed before running IntegrOn
- **Quick start** — 3–5 steps to get the application running for the first time, linking to the full quickstart guide
- **Project structure** — the directory layout with a one-line description of each top-level directory
- **Configuration** — how the JSON configuration file works, with a link to the connector reference
- **Logs and alerts** — where logs go and how email alerts are configured
- **License**

### File 2: `docs/quickstart.md`
A step-by-step guide for the NFe/SEFAZ use case from the PRD. Must cover:
1. Prerequisites (runtime, Docker, credentials, digital certificate)
2. Clone and build the project
3. Start the local development environment (`make dev-up`)
4. Set up environment variables (reference `.env.example`)
5. Write the pipeline configuration file for the NFe use case (include the complete example from Step 3)
6. Run the application
7. Verify the pipeline executed successfully (where to look in the logs, what to check in the database and blob storage)
8. Stop the application

Every step must include the exact command(s) to run. Do not assume the reader knows anything beyond basic terminal usage.

### File 3: `docs/connectors/cron-trigger.md`
Reference documentation for the CRON Trigger connector. Must cover:
- Description: what this connector does
- When to use it
- Configuration fields table: field name, type, required/optional, description, example value
- Constraints and behavior: overlap prevention, missed tick behavior
- Complete configuration example (JSON snippet)
- Common errors and how to resolve them

### File 4: `docs/connectors/database-read.md`
Reference documentation for the Database Read connector. Must cover:
- Description: what this connector does
- Supported databases
- Configuration fields table: field name, type, required/optional, description, example value
- How query results are passed to the next connector (output envelope)
- Complete configuration example (JSON snippet)
- Common errors and how to resolve them

### File 5: `docs/connectors/http.md`
Reference documentation for the HTTP connector. Must cover:
- Description: what this connector does
- Supported authentication methods (focus on mTLS/digital certificate)
- How secrets are referenced (not stored inline)
- Configuration fields table: field name, type, required/optional, description, example value
- How the previous connector's output is used in the request
- How the response is passed to the next connector
- Complete configuration example for the SEFAZ use case (JSON snippet)
- Common errors and how to resolve them

### File 6: `docs/connectors/blob-storage-write.md`
Reference documentation for the Blob Storage Write connector. Must cover:
- Description: what this connector does
- Supported providers
- Configuration fields table: field name, type, required/optional, description, example value
- File naming conventions and path configuration
- Complete configuration example (JSON snippet)
- Common errors and how to resolve them

### File 7: `docs/connectors/database-write.md`
Reference documentation for the Database Write connector. Must cover:
- Description: what this connector does
- Supported operations (INSERT, UPDATE)
- How the previous connector's output is used as query parameters
- Configuration fields table: field name, type, required/optional, description, example value
- Complete configuration example for NSU update (JSON snippet)
- Common errors and how to resolve them

### File 8: `docs/troubleshooting.md`
A troubleshooting guide covering the most common failure scenarios. For each scenario, provide:
- **Symptom**: what the user observes (error message, behavior)
- **Cause**: what is likely wrong
- **Resolution**: exact steps to fix it

Cover at minimum:
- Application fails to start: invalid JSON configuration
- Application fails to start: unknown connector type
- Application fails to start: cannot reach secrets vault
- Pipeline fails: database connection error
- Pipeline fails: SEFAZ returns unexpected response
- Pipeline fails: blob storage write fails
- Pipeline fails: NSU not updated after successful blob write
- Email alert not received after pipeline failure
- CRON fires but pipeline does not start (overlap prevention active)

---

## Output Format

For each file, use this format:

~~~
### `<relative/path/to/file>`
```markdown
<full file content>
```
~~~

---

## Constraints

- Write **only what is true** about the implemented system — do not document features that are out of scope for the MVP (no UI, no multi-tenancy, no async mode, no data transformation)
- Every configuration field in the connector reference must match **exactly** the JSON Schema defined in Step 3
- Every command in the quickstart guide must match the Makefile targets defined in Step 5
- Use **plain, direct language** — avoid marketing language, avoid overexplaining, avoid filler phrases like "it is important to note that"
- All configuration examples must be **complete and valid** — a user must be able to copy them directly and run them with only credential substitution
