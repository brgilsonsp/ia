# Spec Kit + Claude Code — Guia com PRD como entrada

> Greenfield · Claude Code (terminal) · PRD como documento de entrada

---

## Pré-requisitos

- Node.js 20.19.0 ou superior
- Python 3.11+ com `uv` instalado
- Git
- Claude Code instalado (`npm install -g @anthropic-ai/claude-code`)

Instalar o Spec Kit globalmente:

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

---

## Passo 1 — Bootstrap do projeto

**Objetivo:** criar a estrutura de pastas e configurar o Spec Kit para Claude Code.

```powershell
specify init meu-projeto --ai claude
cd meu-projeto
claude
```

Após rodar `claude`, os comandos `/speckit.*` ficam disponíveis no agente. Isso confirma que está pronto.

**Artefatos gerados:**
- `.specify/`
- `scripts/`
- `templates/`
- `CLAUDE.md`

---

## Passo 2 — Definir a constituição do projeto

**Comando:** `/speckit.constitution`  
**Objetivo:** estabelecer os princípios que o agente vai seguir em todas as sessões — padrões de código, arquitetura, testes. Feito **uma vez por projeto**.

**Prompt para colar no Claude Code:**

```
/speckit.constitution Crie os princípios do projeto com foco em:
- Qualidade de código: TypeScript strict, sem any implícito
- Testes: cobertura mínima de 80%, testes unitários e de integração
- Arquitetura: separação clara entre domínio, aplicação e infraestrutura
- UX: acessibilidade WCAG 2.1 AA como requisito mínimo
- Performance: tempo de resposta abaixo de 200ms para operações críticas
```

> Adapte os critérios ao seu contexto. Quanto mais específico, melhor o agente vai tomar decisões técnicas ao longo do projeto.

**Artefatos gerados:**
- `.specify/memory/constitution.md`

---

## Passo 3 — Passar o PRD para gerar a spec

**Comando:** `/speckit.specify`  
**Objetivo:** transformar o conteúdo do PRD em user stories estruturadas e requisitos funcionais. Você referencia o arquivo — não copia o conteúdo no chat.

**Prompt para colar no Claude Code:**

```
/speckit.specify Leia o arquivo PRD em @docs/prd.md e gere a especificação
funcional completa. Extraia todas as histórias de usuário, requisitos funcionais
e regras de negócio descritas no documento. Não infira stack técnica — foque
apenas no comportamento esperado do produto.
```

> O `@docs/prd.md` usa a sintaxe de referência de arquivo do Claude Code. Substitua pelo caminho real do seu PRD dentro do projeto.

> Se o PRD cobre múltiplas features grandes, rode o fluxo inteiro **uma vez por feature**. Cada feature vira uma pasta `001-nome`, `002-nome`, etc., com sua própria branch no Git.

**Artefatos gerados:**
- `.specify/specs/001-nome-feature/spec.md`

---

## Passo 4 — Clarificar ambiguidades do PRD *(recomendado)*

**Comando:** `/speckit.clarify`  
**Objetivo:** PRDs frequentemente têm lacunas — casos de borda não cobertos, comportamentos implícitos, regras conflitantes. O clarify força o agente a explicitar essas dúvidas antes de qualquer decisão técnica.

**Prompt para colar no Claude Code:**

```
/speckit.clarify Revise a spec gerada e identifique pontos ambíguos ou não
cobertos pelo PRD. Para cada ponto, faça uma pergunta objetiva. Após minhas
respostas, atualize o spec.md com as clarificações.
```

> Responda cada pergunta do agente diretamente no chat. Ele vai incorporar as respostas na spec automaticamente.

> Com PRD como entrada, esse passo é especialmente valioso porque PRDs tendem a descrever o "happy path" bem, mas deixam casos de erro e fluxos alternativos vagos.

**Artefatos atualizados:**
- `spec.md` (seção Clarifications adicionada)

---

## Passo 5 — Gerar o plano técnico

**Comando:** `/speckit.plan`  
**Objetivo:** definir a stack, arquitetura e contratos técnicos. É aqui — e **só aqui** — que você fala em tecnologia.

**Prompt para colar no Claude Code:**

```
/speckit.plan A stack escolhida é:
- Frontend: Next.js 14 com App Router, TypeScript, Tailwind CSS
- Backend: Node.js com Fastify, TypeScript
- Banco de dados: PostgreSQL com Prisma ORM
- Autenticação: NextAuth.js
- Infraestrutura: Vercel (frontend) + Railway (backend + banco)

Gere o plano de implementação, modelo de dados e contratos de API
seguindo a spec aprovada.
```

> Se a sua stack usa algo que muda rápido (ex: um framework recente), peça ao agente para pesquisar a versão atual antes de planejar: _"pesquise a documentação do Fastify v5 antes de definir os contratos"_.

**Artefatos gerados:**
- `plan.md`
- `data-model.md`
- `research.md`
- `contracts/api-spec.json`

---

## Passo 6 — Auditar consistência spec × plan *(opcional)*

**Comando:** `/speckit.analyze`  
**Objetivo:** detectar requisitos da spec que não foram cobertos no plano, ou decisões técnicas do plano que contradizem a spec. Vale especialmente quando o PRD é extenso.

**Prompt para colar no Claude Code:**

```
/speckit.analyze Faça uma análise de consistência cruzando spec.md com plan.md.
Liste: (1) requisitos da spec sem cobertura no plano, (2) decisões técnicas que
contradizem regras de negócio, (3) gaps no modelo de dados.
```

**Saída:** relatório inline no chat.

---

## Passo 7 — Quebrar em tasks atômicas

**Comando:** `/speckit.tasks`  
**Objetivo:** transformar o plano em uma lista de tasks ordenadas, com dependências e marcação de paralelismo. É o input direto para a implementação.

**Prompt para colar no Claude Code:**

```
/speckit.tasks Gere o breakdown de tasks a partir do plan.md. Para cada task:
especifique o arquivo exato a criar/modificar, marque com [P] as que podem
rodar em paralelo, e inclua tasks de teste logo após a implementação de
cada componente.
```

**Artefatos gerados:**
- `.specify/specs/001-nome-feature/tasks.md`

---

## Passo 8 — Implementar

**Comando:** `/speckit.implement`  
**Objetivo:** executar todas as tasks do `tasks.md` em ordem, respeitando dependências. O agente valida pré-requisitos antes de começar.

**Prompt para colar no Claude Code:**

```
/speckit.implement
```

**Se precisar retomar após limpar o contexto (`/clear`):**

```
Retome a implementação do projeto. A spec está em
@.specify/specs/001-nome-feature/spec.md, o plano em
@.specify/specs/001-nome-feature/plan.md e as tasks em
@.specify/specs/001-nome-feature/tasks.md.
Já concluí até a task 3.2. Continue a partir da task 3.3.
```

> Este é o **único momento** onde limpar o contexto entre sessões faz sentido. Use o prompt de retomada acima sempre que reiniciar.

**Artefatos gerados:**
- código-fonte
- testes

---

## Referência rápida

| Passo | Comando | Tipo | Artefato principal |
|-------|---------|------|--------------------|
| 1 | `specify init` | Terminal | estrutura do projeto |
| 2 | `/speckit.constitution` | Obrigatório | `constitution.md` |
| 3 | `/speckit.specify` | Obrigatório | `spec.md` |
| 4 | `/speckit.clarify` | Recomendado | `spec.md` atualizado |
| 5 | `/speckit.plan` | Obrigatório | `plan.md`, `data-model.md` |
| 6 | `/speckit.analyze` | Opcional | relatório inline |
| 7 | `/speckit.tasks` | Obrigatório | `tasks.md` |
| 8 | `/speckit.implement` | Obrigatório | código + testes |

---

## Quando limpar — e quando não limpar — o contexto (`/clear`)

A regra geral é simples: **nunca limpe dentro de uma feature, sempre limpe entre features.**

| Transição | Limpar? | Por quê |
|-----------|---------|---------|
| Passo 2 → 3 (constitution → specify) | ❌ Não | O agente precisa dos princípios que acabou de estabelecer para gerar a spec corretamente |
| Passo 3 → 4 (specify → clarify) | ❌ Não | O clarify analisa a spec recém-gerada; sem contexto, ele perde as decisões tomadas |
| Passo 4 → 5 (clarify → plan) | ❌ Não | As clarificações respondidas precisam estar no contexto para informar as decisões técnicas do plano |
| Passo 5 → 6 (plan → analyze) | ❌ Não | O analyze cruza spec e plan — ambos precisam estar no contexto ativo |
| Passo 6 → 7 (analyze → tasks) | ❌ Não | Os gaps identificados no analyze devem refletir nas tasks geradas |
| Passo 7 → 8 (tasks → implement) | ❌ Não | O agente precisa do contexto completo para começar a implementação com todos os artefatos em mente |
| Durante o passo 8, entre sessões longas | ✅ Sim | O contexto fica pesado com histórico de código; limpe e use o prompt de retomada |
| Ao iniciar uma nova feature (feature 001 → 002) | ✅ Sim | Cada feature é um ciclo independente; o contexto da feature anterior pode confundir o agente |

### Prompt de retomada após `/clear` no passo 8

Sempre que limpar o contexto durante a implementação, use este prompt para reorientar o agente:

```
Retome a implementação do projeto. A spec está em
@.specify/specs/001-nome-feature/spec.md, o plano em
@.specify/specs/001-nome-feature/plan.md e as tasks em
@.specify/specs/001-nome-feature/tasks.md.
Já concluí até a task 3.2. Continue a partir da task 3.3.
```

---

## Regras importantes

- **Não limpe o contexto entre os passos 2 e 7.** O agente precisa do histórico da conversa para manter coerência entre as fases. Os artefatos em disco guardam os resultados, mas não guardam o raciocínio e as decisões tomadas no chat.
- **Limpe o contexto apenas durante sessões longas de implementação** (passo 8) ou ao iniciar uma nova feature, usando sempre o prompt de retomada com referências `@` aos arquivos.
- **Um PRD grande = múltiplas features separadas.** Não tente processar tudo em uma única rodada do fluxo.
- **A constituição é global.** Ela vale para todas as features do projeto — não precisa ser refeita a cada feature nova.

---

## Referências

- [Spec Kit — GitHub](https://github.com/github/spec-kit)
- [Spec Kit — documentação completa](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- [Claude Code — documentação](https://docs.claude.com)