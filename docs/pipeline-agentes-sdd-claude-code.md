# Pipeline de Agentes com Spec-Driven Development no Claude Code
> Web App (Frontend + Backend) · Orquestração: Híbrido Sequencial + Paralelo via Subagents

---

## Por que Híbrido Sequencial + Paralelo?

As fases de **especificação são sequenciais** — cada fase valida e alimenta a próxima, e você (o humano) aprova os artefatos antes de avançar. As fases de **implementação são paralelas** — o Orquestrador distribui tarefas independentes para subagentes especializados rodando em contextos isolados simultaneamente.

Isso combina o melhor dos dois mundos: qualidade através de aprovações estruturadas, e velocidade através de paralelismo real.

---

## Visão Geral da Pipeline

```
PRD (você fornece)
     │
     ▼
[FASE 1 - SEQUENCIAL] ──────────────────────────────────
     │
     ├─→ Agente 1: Requirements Analyst
     │        Lê o PRD → gera docs/specs/requirements.md
     │        ⏸ GATE: você revisa e aprova
     │
     ├─→ Agente 2: System Architect
     │        Lê requirements.md → gera docs/specs/design.md
     │        ⏸ GATE: você revisa e aprova
     │
     └─→ Agente 3: Task Planner
              Lê design.md → gera docs/specs/tasks.md
              ⏸ GATE: você revisa e aprova

[FASE 2 - PARALELA] ────────────────────────────────────
     │
     └─→ Orquestrador lê tasks.md e dispara subagentes:
              │
              ├─→ [Subagente] Backend Developer    → src/backend/
              ├─→ [Subagente] Frontend Developer   → src/frontend/
              ├─→ [Subagente] DB Schema Specialist → src/db/
              └─→ [Subagente] Test Engineer        → tests/

[FASE 3 - SEQUENCIAL] ──────────────────────────────────
     │
     ├─→ Agente 4: Code Reviewer
     │        Revisa todos os outputs → docs/review.md
     │        ⏸ GATE: você aprova ou solicita ajustes
     │
     └─→ Agente 5: Integration Agent
              Integra, resolve conflitos, valida build final
```

---

## Estrutura de Diretórios do Projeto

```
meu-projeto/
├── CLAUDE.md                    ← Constituição do projeto (lido por todos os agentes)
├── docs/
│   ├── prd.md                   ← Seu PRD (cole ou faça upload aqui)
│   └── specs/
│       ├── requirements.md      ← Output do Agente 1
│       ├── design.md            ← Output do Agente 2
│       └── tasks.md             ← Output do Agente 3
├── .claude/
│   └── agents/                  ← Definições dos subagentes
│       ├── backend-developer.md
│       ├── frontend-developer.md
│       ├── db-specialist.md
│       └── test-engineer.md
├── src/
│   ├── backend/
│   ├── frontend/
│   └── db/
└── tests/
```

---

## CLAUDE.md — A Constituição do Projeto

Crie este arquivo na raiz. Todos os agentes o leem automaticamente.

```markdown
# Projeto: [Nome do Produto]

## Stack Tecnológica
- Backend: [ex: Node.js + Express / Python + FastAPI]
- Frontend: [ex: React + TypeScript / Next.js]
- Banco de dados: [ex: PostgreSQL]
- Testes: [ex: Jest + Playwright]

## Metodologia: Spec-Driven Development (SDD)
Este projeto segue SDD rigorosamente:
1. Nenhum código é escrito sem spec aprovada
2. Cada agente deve ler os specs relevantes antes de agir
3. Commits atômicos após cada tarefa concluída
4. Subagentes NUNCA spawnam outros subagentes

## Convenções de Código
- Idioma dos comentários: Português
- Nomenclatura: camelCase para variáveis, PascalCase para classes
- Commits: Conventional Commits (feat:, fix:, docs:, test:)

## Caminhos Importantes
- PRD: docs/prd.md
- Requirements: docs/specs/requirements.md
- Design: docs/specs/design.md
- Tasks: docs/specs/tasks.md

## Regras para Todos os Agentes
- Sempre leia o CLAUDE.md e o spec relevante antes de começar
- Nunca assuma — pergunte se algo está ambíguo
- Faça commit ao finalizar cada tarefa
- Documente decisões técnicas no próprio código
```

---

## Fase 1 — Agentes Sequenciais de Especificação

### Como invocar cada agente

Na sessão principal do Claude Code, use os comandos abaixo em sequência,
aguardando sua aprovação entre cada um.

---

### Agente 1: Requirements Analyst

**Comando para invocar:**
```
Você é o Requirements Analyst. Leia o PRD em docs/prd.md e gere o arquivo 
docs/specs/requirements.md seguindo o template abaixo. 

Seja exaustivo: liste todos os requisitos funcionais e não-funcionais, 
identifique ambiguidades e proponha resoluções, defina critérios de aceitação 
claros para cada funcionalidade. 

Use AskUserQuestion se precisar de esclarecimentos sobre o PRD antes de prosseguir.
```

**Formato de saída esperado (docs/specs/requirements.md):**
```markdown
# Requirements Specification

## 1. Escopo do Produto
[resumo executivo do que será construído]

## 2. Requisitos Funcionais
### RF-001: [Nome da Feature]
- Descrição: ...
- Critérios de Aceitação:
  - [ ] ...
  - [ ] ...
- Prioridade: P0 / P1 / P2

## 3. Requisitos Não-Funcionais
- Performance: [ex: p95 < 200ms]
- Segurança: [ex: autenticação JWT, OWASP Top 10]
- Escalabilidade: [ex: suportar 1000 usuários simultâneos]

## 4. Ambiguidades Identificadas e Resoluções
| Ambiguidade | Resolução Proposta |
|-------------|-------------------|
| ...         | ...               |

## 5. Fora do Escopo
[o que explicitamente NÃO será construído]
```

⏸ **GATE 1:** Revise `docs/specs/requirements.md` e aprove antes de continuar.

---

### Agente 2: System Architect

**Comando para invocar:**
```
Você é o System Architect. Leia docs/specs/requirements.md e gere o arquivo 
docs/specs/design.md com a arquitetura completa do sistema.

Inclua: decisões de arquitetura com justificativas, diagrama de componentes 
(em texto/ASCII), schema do banco de dados, contratos de API (endpoints), 
e estratégia de autenticação/autorização.
```

**Formato de saída esperado (docs/specs/design.md):**
```markdown
# System Design

## 1. Decisões de Arquitetura
| Decisão | Escolha | Justificativa |
|---------|---------|---------------|
| ...     | ...     | ...           |

## 2. Diagrama de Componentes
[diagrama ASCII ou descrição estruturada]

## 3. Schema do Banco de Dados
### Tabela: users
| Campo | Tipo | Constraints |
|-------|------|-------------|
| id    | UUID | PK, NOT NULL |
| ...   | ...  | ...         |

## 4. Contratos de API
### POST /api/auth/login
- Request: { email: string, password: string }
- Response 200: { token: string, user: UserDTO }
- Response 401: { error: string }

## 5. Fluxos Principais
[diagrama ou descrição dos fluxos críticos]

## 6. Estratégia de Segurança
[autenticação, autorização, proteção de dados]
```

⏸ **GATE 2:** Revise `docs/specs/design.md` e aprove antes de continuar.

---

### Agente 3: Task Planner

**Comando para invocar:**
```
Você é o Task Planner. Leia docs/specs/requirements.md e docs/specs/design.md.

Gere docs/specs/tasks.md com todas as tarefas de implementação decompostas.
Cada tarefa deve ser atômica (1-2h de trabalho), ter dependências mapeadas,
e estar claramente atribuída a: backend, frontend, db, ou test.

Organize as tarefas para máximo paralelismo: identifique quais podem rodar
simultaneamente sem conflitos de arquivo.
```

**Formato de saída esperado (docs/specs/tasks.md):**
```markdown
# Implementation Tasks

## Batch 1 — Pode rodar em PARALELO
- [ ] TASK-001 [db] Criar migrations do schema de users e sessions
- [ ] TASK-002 [backend] Scaffold do projeto Express com estrutura de pastas
- [ ] TASK-003 [frontend] Scaffold do projeto React com roteamento base

## Batch 2 — Depende do Batch 1
- [ ] TASK-004 [backend] Implementar endpoint POST /api/auth/register
  - Depende de: TASK-001, TASK-002
- [ ] TASK-005 [frontend] Implementar tela de cadastro com formulário validado
  - Depende de: TASK-003

## Batch 3 — Depende do Batch 2
- [ ] TASK-006 [test] Testes E2E do fluxo de cadastro e login
  - Depende de: TASK-004, TASK-005
...

## Mapeamento de Arquivos por Tarefa
| Task | Arquivos que modifica |
|------|----------------------|
| TASK-001 | src/db/migrations/001_users.sql |
| TASK-002 | src/backend/app.ts, src/backend/routes/ |
```

⏸ **GATE 3:** Revise `docs/specs/tasks.md` e aprove antes de continuar.

---

## Definição dos Subagentes (.claude/agents/)

Crie os arquivos abaixo. O Claude Code os carrega automaticamente.

### .claude/agents/backend-developer.md
```markdown
---
name: backend-developer
description: Implementa endpoints de API, lógica de negócio e integrações de backend. Ativado para tarefas marcadas com [backend] em tasks.md.
---

Você é um Backend Developer sênior especializado em [Node.js/Python — conforme CLAUDE.md].

Antes de qualquer implementação:
1. Leia CLAUDE.md
2. Leia docs/specs/design.md (seção de API Contracts)
3. Leia a task específica que foi atribuída a você

Padrões obrigatórios:
- Valide todos os inputs com schema validation
- Trate todos os erros com mensagens descritivas
- Escreva JSDoc/docstrings em todas as funções públicas
- Faça commit ao finalizar cada endpoint: "feat(api): implementa POST /recurso"

NUNCA use o Task tool — você é um subagente, não o orquestrador.
```

### .claude/agents/frontend-developer.md
```markdown
---
name: frontend-developer
description: Implementa componentes React, páginas, e integração com a API. Ativado para tarefas marcadas com [frontend] em tasks.md.
---

Você é um Frontend Developer sênior especializado em React + TypeScript.

Antes de qualquer implementação:
1. Leia CLAUDE.md
2. Leia docs/specs/design.md (fluxos de usuário)
3. Leia a task específica atribuída a você

Padrões obrigatórios:
- Componentes funcionais com TypeScript tipado
- Sem any implícito
- Acessibilidade: aria-labels em elementos interativos
- Responsividade: mobile-first
- Faça commit ao finalizar cada componente: "feat(ui): implementa ComponenteName"

NUNCA use o Task tool — você é um subagente, não o orquestrador.
```

### .claude/agents/db-specialist.md
```markdown
---
name: db-specialist
description: Cria migrations, seeds e queries otimizadas de banco de dados. Ativado para tarefas marcadas com [db] em tasks.md.
---

Você é um Database Specialist com foco em PostgreSQL.

Antes de qualquer implementação:
1. Leia CLAUDE.md
2. Leia docs/specs/design.md (seção Database Schema)
3. Leia a task específica atribuída

Padrões obrigatórios:
- Migrations reversíveis (UP e DOWN)
- Índices em todas as foreign keys e colunas de busca frequente
- Nomenclatura: snake_case, tabelas no plural
- Faça commit ao finalizar: "feat(db): migration TASK-XXX nome_da_tabela"

NUNCA use o Task tool.
```

### .claude/agents/test-engineer.md
```markdown
---
name: test-engineer
description: Escreve testes unitários, de integração e E2E. Ativado para tarefas marcadas com [test] em tasks.md.
---

Você é um Test Engineer especializado em garantia de qualidade.

Antes de qualquer implementação:
1. Leia CLAUDE.md
2. Leia docs/specs/requirements.md (critérios de aceitação)
3. Leia a task específica atribuída

Padrões obrigatórios:
- Cubra os happy paths E os edge cases
- Nomeie testes em PT-BR: "deve [comportamento] quando [condição]"
- Cobertura mínima: 80% por módulo
- Faça commit ao finalizar: "test: cobertura de TASK-XXX"

NUNCA use o Task tool.
```

---

## Fase 2 — Orquestrador de Implementação

Quando as specs estiverem aprovadas, use este comando no Claude Code:

```
Você é o Orchestrator. Leia docs/specs/tasks.md e implemente todas as tarefas
usando o Task tool para delegar a subagentes especializados.

Regras de orquestração:
1. Para cada Batch em tasks.md, dispare os subagentes em PARALELO (run_in_background: true)
2. Aguarde a conclusão do Batch antes de iniciar o próximo
3. Atribua cada task ao subagente correto pelo seu prefixo: [backend], [frontend], [db], [test]
4. Após cada Batch, verifique se houve erros e resolva conflitos antes de avançar
5. Mantenha um log de progresso em docs/progress.md

Exemplo de como delegar (faça isso para cada tarefa do Batch 1):
- TASK-001 [db] → subagente: db-specialist
- TASK-002 [backend] → subagente: backend-developer  
- TASK-003 [frontend] → subagente: frontend-developer
```

---

## Fase 3 — Revisão e Integração

### Agente 4: Code Reviewer

```
Você é o Code Reviewer. Analise todo o código produzido em src/ e tests/.

Compare cada implementação contra:
- docs/specs/requirements.md (critérios de aceitação foram atendidos?)
- docs/specs/design.md (arquitetura foi respeitada?)

Gere docs/review.md com:
1. Issues por severidade (P0=blocker, P1=major, P2=minor)
2. Itens aprovados
3. Lista de ajustes necessários antes do merge
```

⏸ **GATE 4:** Revise `docs/review.md` e decida o que precisa ser corrigido.

---

### Agente 5: Integration Agent

```
Você é o Integration Agent. Sua missão é garantir que o sistema funcione
como um todo integrado.

1. Verifique se o frontend está chamando os endpoints corretos definidos em design.md
2. Valide que as migrations do banco estão alinhadas com os models do backend
3. Execute os testes: rode `npm test` (ou equivalente) e corrija falhas
4. Gere um relatório final em docs/integration-report.md
```

---

## Comandos de Setup Rápido

```bash
# 1. Criar a estrutura de diretórios
mkdir -p docs/specs .claude/agents src/{backend,frontend,db} tests

# 2. Instalar cc-sdd (toolkit SDD para Claude Code)
npx cc-sdd@latest --claude-agent

# 3. Iniciar o Claude Code no projeto
claude

# 4. Dentro do Claude Code, iniciar o fluxo SDD
/kiro:spec-init     # se usar cc-sdd
# ou manualmente invocar o Agente 1 com o comando desta documentação
```

---

## Checklist Antes de Começar

- [ ] PRD salvo em `docs/prd.md`
- [ ] `CLAUDE.md` criado e stack tecnológica preenchida
- [ ] Estrutura de diretórios criada
- [ ] Subagentes definidos em `.claude/agents/`
- [ ] Claude Code instalado (`npm install -g @anthropic-ai/claude-code`)

---

## Fluxo de Aprovação Resumido

| Gate | Artefato | O que verificar |
|------|----------|-----------------|
| Gate 1 | requirements.md | Todos os requisitos do PRD cobertos? Ambiguidades resolvidas? |
| Gate 2 | design.md | Arquitetura faz sentido? APIs bem definidas? Schema correto? |
| Gate 3 | tasks.md | Tarefas são atômicas? Dependências mapeadas? Paralelos identificados? |
| Gate 4 | review.md | Critérios de aceitação atendidos? Sem bugs críticos? |

---

## Próximo Passo

**Faça upload do seu PRD** e salve-o como `docs/prd.md` no projeto.
Em seguida, invoque o **Agente 1 (Requirements Analyst)** com o comando desta documentação
para iniciar o fluxo.
