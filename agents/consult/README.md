# Agentes de Consultoria

Prompts de agente para consultores de IA de qualquer especialidade. Cada agente atua como um especialista consultivo com identidade, domínio e comportamento próprios. Projetados para uso como Skills no Claude Code ou como system prompts em interfaces de chat multi-turn.

---

## Agentes disponíveis

### `sheila_ceo_especialista_mvp_agent.md`

**Persona:** CEO Sheila — fundadora experiente, especialista em MVP de produtos B2B SaaS no Brasil.

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

## Como usar como Skill no Claude Code

Adicione os agentes ao arquivo `~/.claude/skills.md` ou à pasta de skills do seu projeto. Ao invocar via `/skill`, o conteúdo de `$ARGUMENTS` é substituído pela mensagem inicial do fundador.

Exemplo de invocação:
```
/sheila_ceo_especialista_mvp_agent Tenho uma lista de 15 features para o meu MVP de SaaS para clínicas. Quero saber o que cortar.
```

Se invocado sem argumentos, o agente solicita contexto inicial antes de aconselhar.

---

## Diferenças entre os dois agentes

| Dimensão | Sheila (MVP specialist) | Consult (estratégico geral) |
|---|---|---|
| Especialidade | MVP — escopo, priorização, validação | Consultoria early-stage ampla |
| Ferramentas estruturadas | Canvas, Scorecard, Matriz, Métricas | Não tem ferramentas estruturadas |
| Idioma | Português Brasileiro | Inglês |
| Perfil do fundador rastreado | Sim, com campos específicos de MVP | Sim, mais genérico |
| Exemplos incluídos | 6 (cobre MVP, risco, co-fundador, escopo) | Não tem exemplos |

**Recomendação:** use **Sheila** quando o foco da sessão for MVP. Use o agente **consult** para sessões de estratégia mais ampla ou quando o idioma inglês for preferível.

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
