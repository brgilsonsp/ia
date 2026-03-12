# Agentes de Consultoria

Prompts de agente para consultores de IA de qualquer especialidade. Cada agente atua como um especialista consultivo com identidade, domínio e comportamento próprios. Projetados para uso como Skills no Claude Code ou como system prompts em interfaces de chat multi-turn.

---

## Agentes disponíveis

### `ceo_especialista_mvp_agent.md`

**Persona:** CEO Startup MVP — fundadora experiente, especialista em MVP de produtos B2B SaaS no Brasil.

**Foco principal:** Definição, escopo, priorização e validação de MVPs.

**Quando usar:**
- Fundador precisa definir ou reduzir o escopo do MVP
- Lista de features cresceu além do necessário
- Fundador quer saber se o MVP está pronto para construção ou lançamento
- Orientação estratégica sobre validação de mercado, go-to-market, pricing, dinâmicas de co-fundador, AI tooling ou fundraising no Brasil

**Ferramentas estruturadas incluídas:**
- MVP Canvas — define o MVP completo de forma colaborativa
- Matriz de Priorização (Valor vs. Esforço) — corta features com critério objetivo
- MVP Scorecard — verifica se o escopo está pronto para construção
- Métricas de Sucesso do MVP — define critérios de pivot/persevere

**Idioma de resposta:** Português Brasileiro (independente do idioma da pergunta)

---

### `consult_fundador_b2b_saas_brasil_agent.md`

**Persona:** CEO experiente, consultor de fundadores early-stage de B2B SaaS no Brasil.

**Foco principal:** Consultoria estratégica ampla — ideação, validação, go-to-market, pricing, fundraising.

**Quando usar:**
- Fundador precisa de orientação estratégica geral, não necessariamente focada em MVP
- Questões de mercado, ecossistema, ICP, willingness-to-pay
- Primeiros passos de uma startup, ainda na fase de ideação ou validação

**Idioma de resposta:** Inglês (prompt original em inglês)

---

## Como usar em outros projetos

Os agentes deste diretório podem ser disponibilizados globalmente (em qualquer projeto) ou localmente (apenas no projeto atual). Existem duas formas de uso no Claude Code: como **Skill** ou como **Custom Agent**.

---

### Opção 1 — Como Skill (invocação manual via `/`)

Skills são invocados explicitamente pelo usuário com `/nome-do-arquivo`.

**Global (disponível em todos os projetos):**
Copie o arquivo `.md` do agente para `~/.claude/skills/`:
```bash
cp ceo_especialista_mvp_agent.md ~/.claude/skills/
```
Invoque em qualquer projeto com:
```
/ceo_especialista_mvp_agent Tenho uma lista de 15 features para o meu MVP de SaaS para clínicas. Quero saber o que cortar.
```

**Local (apenas no projeto atual):**
Copie o arquivo para `.claude/skills/` na raiz do projeto:
```bash
mkdir -p .claude/skills
cp ceo_especialista_mvp_agent.md .claude/skills/
```

Se invocado sem argumentos, o agente solicita contexto inicial antes de aconselhar.

---

### Opção 2 — Como Custom Agent (seleção automática pelo Claude)

Custom Agents são selecionados automaticamente pelo Claude com base na `description` do frontmatter YAML — sem necessidade de invocação manual.

**Global (disponível em todos os projetos):**
Copie o arquivo `.md` do agente para `~/.claude/agents/`:
```bash
cp ceo_especialista_mvp_agent.md ~/.claude/agents/
```

**Local (apenas no projeto atual):**
Copie o arquivo para `.claude/agents/` na raiz do projeto:
```bash
mkdir -p .claude/agents
cp ceo_especialista_mvp_agent.md .claude/agents/
```

O Claude selecionará o agente automaticamente quando a conversa corresponder à descrição definida no campo `description` do arquivo.

---

### Qual usar?

| | Skill | Custom Agent |
|---|---|---|
| Ativação | Manual — você digita `/nome` | Automática — Claude seleciona pelo contexto |
| Controle | Total — você decide quando usar | Delegado ao Claude |
| Ideal para | Consultas pontuais e intencionais | Workflows onde o Claude roteia para o especialista certo |

---

## Diferenças entre os dois agentes

| Dimensão | CEO Startup MVP (MVP specialist) | Consult (estratégico geral) |
|---|---|---|
| Especialidade | MVP — escopo, priorização, validação | Consultoria early-stage ampla |
| Ferramentas estruturadas | Canvas, Scorecard, Matriz, Métricas | Não tem ferramentas estruturadas |
| Idioma | Português Brasileiro | Inglês |
| Perfil do fundador rastreado | Sim, com campos específicos de MVP | Sim, mais genérico |
| Exemplos incluídos | 6 (cobre MVP, risco, co-fundador, escopo) | Não tem exemplos |

**Recomendação:** use **CEO Startup MVP** quando o foco da sessão for MVP. Use o agente **consult** para sessões de estratégia mais ampla ou quando o idioma inglês for preferível.

---

## Convenções e guardrails do diretório

As convenções de estrutura e os guardrails obrigatórios para todos os agentes aqui definidos estão documentados em [`CLAUDE.md`](./CLAUDE.md). Esse arquivo é lido automaticamente pelo Claude Code ao trabalhar neste diretório.

Resumo dos guardrails aplicados a todos os agentes:
- Proibição de fabricação de dados — incertezas são rotuladas explicitamente com classificadores padronizados
- Separação obrigatória entre fato, análise e recomendação
- Perguntas de clarificação antes de aconselhar quando o contexto é insuficiente
- Controle de escopo — desvios são sinalizados antes de qualquer engajamento
- Proibição de autoridade implícita e linguagem vaga sem classificação

Para o detalhamento completo, ver `CLAUDE.md`.
