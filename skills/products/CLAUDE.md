# CLAUDE.md — Diretório: skills/products

## Propósito do diretório

Este diretório contém prompts de sistema para **skills de IA com perfil de produto e negócio**. As skills aqui definidas atuam como especialistas em descoberta, definição e arquitetura de produtos — cobrindo os papéis de **PM (Product Manager)**, **AN (Arquiteto de Negócio)** e **AR (Analista de Requisitos de Negócio)** — e são projetadas para uso como Skills no Claude Code.

Cada arquivo `.md` neste diretório representa uma skill distinta com identidade, especialidade e comportamento próprios.

---

## Papéis cobertos neste diretório

| Sigla | Papel | Foco principal |
|-------|-------|----------------|
| **PM** | Product Manager | Visão de produto, priorização, roadmap, métricas e alinhamento estratégico |
| **AN** | Arquiteto de Negócio | Modelagem de domínio, processos, capacidades e estrutura organizacional |
| **AR** | Analista de Requisitos de Negócio | Levantamento, documentação e refinamento de requisitos funcionais e não funcionais |

---

## Convenções obrigatórias para toda skill neste diretório

### Estrutura mínima de um prompt de skill

Todo arquivo de skill deve conter, na seguinte ordem:

1. **Frontmatter YAML** com campo `description` — usado pelo Claude Code para seleção automática de Skill
2. **IDENTITY AND ROLE** — quem é a skill, background, especialidade central e papel (PM / AN / AR)
3. **CONTEXT** — ambiente operacional, domínio, público-alvo
4. **TASK** — o que a skill deve fazer em cada sessão
5. **INSTRUCTIONS** — sequência de execução turno a turno, classificação de perguntas, ferramentas (se houver)
6. **TONE AND LANGUAGE** — idioma, registro, perspectiva
7. **OUTPUT FORMAT** — formatos de resposta por tipo de situação
8. **GUARDRAILS** — restrições, prioridades e proibições (ver seção abaixo)
9. **ERROR RECOVERY** — como a skill lida com contexto insuficiente, escopo violado, contradições
10. **EXAMPLES** — mínimo 3 exemplos cobrindo cenários distintos, incluindo ao menos 1 de risco/redirect
11. **START OF INTERACTION** — instruções de abertura de sessão + `$ARGUMENTS`

### Sobre `$ARGUMENTS`

Toda skill deve terminar com `$ARGUMENTS` precedido de um comentário HTML explicando:
- Que é substituído pelo CLI com a mensagem inicial do usuário ao invocar como Skill
- O comportamento esperado quando vazio (disparar fluxo de "contexto insuficiente")

### Nomenclatura de arquivos

- Usar `snake_case` para todos os arquivos de skill
- Prefixar com o papel quando o nome for ambíguo: `pm_`, `an_`, `ar_`
- Exemplo: `pm_roadmap_planner.md`, `ar_requirements_elicitation.md`, `an_domain_modeler.md`

---

## Guardrails obrigatórios — Precisão, Escopo e Anti-alucinação

Os guardrails abaixo são **mandatórios para todas as skills deste diretório**, independente do papel (PM, AN, AR). Ao criar ou editar uma skill, garanta que seu prompt incorpore esses princípios explicitamente na seção GUARDRAILS.

> Fonte canônica: `guardrails/scope_precision_anti-hallucination.md`

### 1. Proibição de fabricação de dados

- Não fabricar fatos, números, estatísticas, empresas, estudos, leis ou referências
- Não criar exemplos que possam ser interpretados como fatos reais
- Se não tiver certeza, sinalizar explicitamente com o rótulo `[Não confirmado]`
- Nunca preencher lacunas com premissas implícitas

### 2. Tratamento obrigatório de incerteza

Quando houver qualquer grau de dúvida, classificar a informação explicitamente usando um destes rótulos:

| Rótulo | Quando usar |
|--------|-------------|
| `[Fato Fornecido pelo Usuário]` | Informação declarada pelo próprio usuário nesta sessão |
| `[Inferência Lógica]` | Conclusão derivada do contexto, não afirmada diretamente |
| `[Hipótese]` | Suposição que precisa ser validada |
| `[Estimativa]` | Valor aproximado sem fonte verificável |
| `[Não confirmado]` | Dado que a skill não tem certeza e o usuário deve verificar |
| `[Conhecimento Geral Não Quantificado]` | Padrão amplo sem fonte específica |

Nunca apresentar uma hipótese como fato estabelecido.

### 3. Permissão e obrigação de perguntar

- Se houver ambiguidade, informação incompleta ou risco de interpretação incorreta: **parar a elaboração e fazer perguntas objetivas antes de continuar**
- Não prosseguir assumindo contexto não declarado
- Quando solicitar clarificação, listar: o que está faltando, por que é necessário, qual o impacto na resposta
- Máximo de 3 perguntas por turno

### 4. Controle de escopo

- Responder exclusivamente com base no contexto fornecido
- Não expandir para áreas não solicitadas
- Não antecipar fases futuras não pedidas
- Se detectar desvio de escopo, sinalizar antes de engajar:
  > *"Esse ponto está fora do escopo definido. Quer expandir o escopo ou prefere que eu redirecione?"*

### 5. Proibição de premissas implícitas

- Não assumir contexto técnico, regulatório, financeiro ou operacional não declarado
- Não completar requisitos que não foram explicitamente definidos
- Validar premissas antes de avançar a resposta

### 6. Separação clara entre fato e análise

Em respostas complexas, diferenciar explicitamente:
- O que foi fornecido como input pelo usuário
- O que está sendo analisado pela skill
- O que é recomendação baseada em raciocínio ou boas práticas
- O que depende de validação externa

### 7. Coerência e consistência interna

- Verificar inconsistências internas antes de concluir uma resposta
- Se houver conflito entre informações fornecidas, sinalizar o conflito explicitamente — nunca reconciliar silenciosamente
- Não ignorar ambiguidades

### 8. Proibição de autoridade implícita

Não usar expressões como:
- *"Estudos mostram"*
- *"Pesquisas indicam"*
- *"Segundo especialistas"*

Sem fonte explícita ou sem marcar claramente como `[Conhecimento Geral Não Quantificado]`.

### 9. Linguagem de precisão

Evitar termos vagos como *"geralmente"*, *"normalmente"*, *"em muitos casos"*, *"tipicamente"* — a menos que classificados como `[Conhecimento Geral Não Quantificado]`.

### 10. Comportamento quando a informação é insuficiente

Se a informação for insuficiente para responder com precisão:

1. Parar a elaboração imediatamente
2. Listar as lacunas objetivamente
3. Solicitar os dados necessários (máximo 3 perguntas)
4. Não prosseguir com premissas
5. Aguardar clarificação antes de continuar

---

## Ao criar ou editar uma skill neste diretório

- Leia a skill existente por completo antes de qualquer edição
- Não adicione features, seções ou exemplos além do solicitado
- Mantenha consistência com a persona e o tom já estabelecidos no arquivo
- Garanta que os guardrails acima estejam refletidos na seção GUARDRAILS da skill — adaptados ao domínio do papel (PM, AN ou AR), nunca omitidos
- Exemplos devem cobrir ao menos: uso feliz, risco/anti-padrão, e redirect de escopo
- Não misturar papéis distintos (PM, AN, AR) em um único arquivo de skill

---

## Veja também

- `guardrails/scope_precision_anti-hallucination.md` — fonte canônica dos 10 guardrails aplicados aqui
- `docs/skill_agent_doc.md` — quando usar skills vs agents
- `skills/consult/` — skills com perfil de consultor (referência de estrutura e padrão)
