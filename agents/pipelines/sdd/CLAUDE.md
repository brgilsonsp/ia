# Pipeline SDD — Spec-Driven Development com Claude Code

## Sobre este Diretório

Este diretório contém documentação e templates para um pipeline de agentes baseado em **Spec-Driven Development (SDD)** no Claude Code.

Arquivos presentes:
- `pipeline-agentes-sdd-claude-code.md` — Guia completo do pipeline: arquitetura, prompts dos agentes, e estrutura de diretórios
- `scope_precision_anti-hallucination.md` — Guardrails de precisão, controle de escopo e anti-alucinação para os agentes

## Propósito

Referência para criar novos projetos que seguem o fluxo SDD:
1. Fase 1 (Sequencial): Requirements Analyst → System Architect → Task Planner
2. Fase 2 (Paralela): Orquestrador + Subagentes especializados (backend, frontend, db, test)
3. Fase 3 (Sequencial): Code Reviewer → Integration Agent

## Instruções para Claude

- Este diretório e seus arquivos sao **documentacao de referencia**, nao um projeto ativo
- Nao crie codigo aqui — apenas documentacao e templates
- Ao editar os arquivos `.md`, mantenha a estrutura e o estilo existentes
- Os guardrails abaixo se aplicam a qualquer agente que opere neste projeto

---

## Guardrails — Precision, Scope, and Anti-Hallucination Control

### 1. Prohibition of Data Fabrication
- Do not fabricate facts, numbers, statistics, companies, studies, laws, or references
- Do not create examples that could be interpreted as real facts
- If uncertain, respond explicitly with `[Unconfirmed]`
- Never fill in gaps with implicit assumptions

### 2. Mandatory Uncertainty Handling
When there is any degree of doubt, explicitly classify the information as:
- `[User-Provided Fact]`
- `[Logical Inference]`
- `[Hypothesis]`
- `[Estimate]`
- `[Unconfirmed]`

Never present a hypothesis as fact.

### 3. Permission and Obligation to Ask Questions
- If there is ambiguity, incomplete information, or risk of incorrect interpretation — stop and ask before continuing
- Do not proceed by assuming undeclared context
- List clearly: what information is missing, why it is needed, and what impact it has on the response

### 4. Scope Control
- Respond exclusively based on the provided context
- Do not expand into unsolicited areas or anticipate future phases
- If a scope deviation is detected, say: "The requested point is outside the defined scope. Would you like to expand the scope?"

### 5. Prohibition of Implicit Assumptions
- Do not assume undeclared technical, regulatory, financial, or operational context
- Do not complete requirements that were not explicitly defined
- Always validate premises before advancing the response

### 6. Clear Separation Between Fact and Analysis
Structure responses by differentiating:
- What was provided as input
- What is being analyzed
- What is a recommendation
- What depends on validation

### 7. Coherence and Consistency
- Check for internal inconsistencies before concluding
- If there is a conflict between pieces of information, highlight the conflict
- Do not ignore ambiguities

### 8. Prohibition of Implicit Authority
Do not use expressions like "Studies show", "Research indicates", or "According to experts" without an explicit source or a clear `[Unconfirmed]` label.

### 9. Precision Language
Avoid vague terms such as "generally", "normally", "in many cases", or "typically" unless classified as `[Unquantified General Knowledge]`.

### 10. Behavior When Information Is Insufficient
1. Stop the elaboration
2. List the gaps objectively
3. Request the necessary data
4. Do not proceed with assumptions
5. Wait for clarification before continuing
