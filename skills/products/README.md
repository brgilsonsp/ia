# Skills de Produto e Negócio

Skills para IA com perfil de **PM (Product Manager)**, **AN (Arquiteto de Negócio)** e **AR (Analista de Requisitos de Negócio)**. Projetadas para uso como Skills no Claude Code — invocadas manualmente com `/nome-da-skill`.

---

## Skills disponíveis

> Este diretório ainda não contém skills. As skills serão adicionadas conforme criadas.

Quando populado, cada skill seguirá a estrutura abaixo.

---

## Papéis cobertos

| Sigla | Papel | Foco principal |
|-------|-------|----------------|
| **PM** | Product Manager | Visão de produto, priorização, roadmap, métricas e alinhamento estratégico |
| **AN** | Arquiteto de Negócio | Modelagem de domínio, processos, capacidades e estrutura organizacional |
| **AR** | Analista de Requisitos de Negócio | Levantamento, documentação e refinamento de requisitos funcionais e não funcionais |

---

## Como instalar

Skills podem ser instaladas em nível de **perfil do usuário** (disponível em todos os projetos) ou em nível de **projeto** (escopo restrito ao repositório atual).

### Perfil do usuário — disponível em todos os projetos

```bash
cp <nome_da_skill>.md ~/.claude/skills/
```

### Nível de projeto — restrito ao projeto atual

```bash
mkdir -p .claude/skills
cp <nome_da_skill>.md .claude/skills/
```

---

## Como usar

### Opção 1 — Invocação explícita via `/`

```
/pm_roadmap_planner Preciso priorizar o roadmap do Q2 com base nos seguintes temas...
/ar_requirements_elicitation Módulo de autenticação — precisamos levantar os requisitos
/an_domain_modeler Domínio: gestão de contratos para uma fintech B2B
```

### Opção 2 — Sem argumentos (fluxo de contexto insuficiente)

Se invocada sem argumentos, a skill solicita o contexto necessário antes de prosseguir:

```
/pm_roadmap_planner
```

> A skill listará o que precisa saber (produto, objetivos, restrições, stakeholders) antes de qualquer análise.

---

## Nomenclatura de arquivos

| Prefixo | Papel | Exemplo |
|---------|-------|---------|
| `pm_` | Product Manager | `pm_roadmap_planner.md` |
| `an_` | Arquiteto de Negócio | `an_domain_modeler.md` |
| `ar_` | Analista de Requisitos | `ar_requirements_elicitation.md` |

---

## Guardrails aplicados

Todas as skills deste diretório seguem os 10 guardrails de precisão, escopo e anti-alucinação definidos em `guardrails/scope_precision_anti-hallucination.md`:

- Proibição de fabricação de dados — incertezas são rotuladas com classificadores padronizados
- Separação obrigatória entre fato, análise e recomendação
- Perguntas de clarificação quando o contexto for insuficiente (máximo 3 por turno)
- Controle de escopo — desvios são sinalizados antes de qualquer engajamento
- Proibição de autoridade implícita e linguagem vaga sem classificação

Para o detalhamento completo, ver [`CLAUDE.md`](./CLAUDE.md).

---

## Veja também

- `guardrails/scope_precision_anti-hallucination.md` — fonte canônica dos guardrails
- `docs/skill_agent_doc.md` — quando usar skills vs agents
- `skills/consult/` — skills com perfil de consultor (referência de estrutura e padrão)
