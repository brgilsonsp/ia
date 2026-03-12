# [Nome do Produto] — Product Requirements Document (PRD)

**Versão**: 1.0
**Data**: [AAAA-MM-DD]
**Status**: [Rascunho | Em revisão | Aprovado]

---

## 1. VISÃO DO PRODUTO

### Proposta de Valor

<!-- O que o produto é e qual entrega de valor ele oferece ao usuário. Descreva de forma direta: o que é o produto, para quem é e qual problema resolve de forma diferenciada. Evite jargão de marketing. -->

[Descreva em 2–4 frases o que é o produto, quem é o usuário-alvo e qual valor entrega.]

### Problema a Resolver

<!-- Descreva o problema real que o usuário enfrenta hoje. Contextualize o cenário atual antes de falar da solução. Seja específico: qual é a dor, em qual situação ela ocorre, qual o impacto. -->

[Descreva o cenário atual e por que ele é problemático para o usuário. Inclua o impacto concreto do problema — tempo, custo, risco, dependência.]

### Solução Proposta

<!-- Descreva como o produto resolve o problema. Seja objetivo: o que o produto faz, não como ele funciona internamente. -->

[Descreva a abordagem da solução. Se houver múltiplas formas de uso ou modos de operação, liste-os com marcadores.]

---

## 2. USUÁRIOS E CASOS DE USO

### Personas

#### Persona 1: [Nome/Papel]

- **Perfil**: [Quem é essa pessoa — papel, senioridade, área]
- **Contexto**: [Em que situação usa o produto]
- **Objetivo**: [O que quer alcançar com o produto]
- **Dor principal**: [O maior obstáculo ou frustração hoje]
- **Nível técnico**: [Alto | Médio | Baixo — e o que isso significa para o uso do produto]

#### Persona 2: [Nome/Papel]

- **Perfil**: [...]
- **Contexto**: [...]
- **Objetivo**: [...]
- **Dor principal**: [...]
- **Nível técnico**: [...]

<!-- Adicione mais personas se necessário. Evite criar personas sem impacto direto no design do produto. -->

### Principais Casos de Uso

#### Caso de Uso 1: [Nome descritivo do caso de uso]

**Ator**: [Persona que executa este caso de uso]

**Objetivo**: [O que o ator quer alcançar ao final deste fluxo]

**Pré-condição**: [O que precisa estar verdadeiro para o fluxo começar — opcional se não houver]

**Fluxo principal**:

1. [Primeiro passo do usuário ou do sistema]
2. [Próximo passo]
3. [...]

**Resultado esperado**: [O que acontece ao final do fluxo bem-sucedido]

#### Caso de Uso 2: [Nome descritivo]

**Ator**: [...]

**Objetivo**: [...]

**Fluxo principal**:

1. [...]

**Resultado esperado**: [...]

<!-- Adicione casos de uso adicionais conforme necessário. -->

### Jornada do Usuário

#### Jornada 1: [Nome da jornada]

1. [Passo 1 da jornada — perspectiva do usuário]
2. [Passo 2]
3. [...]

#### Jornada 2: [Nome da jornada]

1. [...]

---

## 3. CONCEITOS FUNDAMENTAIS

### Definições

<!-- Liste os termos específicos do domínio do produto que precisam de definição precisa. Evite termos genéricos que não precisam de esclarecimento. -->

| Termo | Definição |
|---|---|
| **[Termo 1]** | [Definição precisa do termo no contexto deste produto] |
| **[Termo 2]** | [Definição] |
| **[Termo 3]** | [Definição] |

### Modelo Mental

<!-- Explique como o usuário deve pensar no produto — a metáfora ou analogia que melhor representa o funcionamento. Isso orienta o design e a comunicação do produto. -->

[Descreva a analogia ou modelo mental que ajuda o usuário a entender como o produto funciona. Use uma frase de ancoragem seguida de uma explicação do fluxo principal.]

### Regras de Negócio

<!-- Liste as regras que governam o comportamento do produto. Cada regra deve ser verificável e não ambígua. Numere para facilitar referência. -->

1. **[Nome da Regra]**: [Descrição precisa da regra]
2. **[Nome da Regra]**: [Descrição]
3. **[Nome da Regra]**: [Descrição]

<!-- Continue numerando conforme necessário. -->

---

## 4. FUNCIONALIDADES

<!-- Para cada funcionalidade, siga o padrão abaixo. Não inclua funcionalidades que não estejam claras o suficiente para ter critérios de aceitação. -->

### Funcionalidade 1: [Nome da Funcionalidade]

**Descrição**: [O que esta funcionalidade faz — em 1 a 3 frases.]

**Motivação**: [Por que esta funcionalidade existe. Qual problema do usuário ela resolve e por que é necessária agora.]

**Comportamento esperado**:
- [O que o usuário faz]
- [O que o sistema faz em resposta]
- [Variações de comportamento relevantes]

**Critérios de aceitação**:
- [ ] [Critério verificável e objetivo]
- [ ] [Critério]
- [ ] [Critério — inclua casos de erro relevantes]

---

### Funcionalidade 2: [Nome da Funcionalidade]

**Descrição**: [...]

**Motivação**: [...]

**Comportamento esperado**:
- [...]

**Critérios de aceitação**:
- [ ] [...]

---

<!-- Adicione funcionalidades seguindo o mesmo padrão. Numere sequencialmente. -->

> **Ponto de atenção para refinamento**: [Se houver decisões de design em aberto que afetam diretamente o comportamento de uma funcionalidade, registre aqui com clareza. Indique qual decisão precisa ser tomada e qual o impacto no produto.]

---

## 5. REQUISITOS NÃO FUNCIONAIS

### Usabilidade
- [Requisito de usabilidade — ex.: tempo para completar uma tarefa, clareza de mensagens de erro, formatos suportados]
- [...]

### Acessibilidade
- [Padrão ou diretriz de acessibilidade a seguir — ex.: WCAG 2.1 nível AA]

### Performance
- [Requisito de performance mensurável — ex.: tempo de resposta, throughput, latência máxima aceitável]

### Segurança
- [Requisito de segurança — ex.: armazenamento de credenciais, criptografia, controle de acesso]

### Conformidade
- [Requisito regulatório ou de compliance aplicável — ex.: LGPD, SOC 2, ISO 27001]

### Integrações
- [Sistemas externos com os quais o produto deve se integrar e a natureza da integração]

---

## 6. LIMITAÇÕES E RESTRIÇÕES

### Premissas

<!-- Liste o que o produto assume como verdade no ambiente do usuário. Premissas não verificadas tornam-se riscos. -->

- [Premissa sobre o ambiente do usuário — ex.: o cliente gerencia suas próprias credenciais]
- [Premissa sobre o modelo de entrega — ex.: o produto é oferecido como SaaS]

### Dependências Externas

<!-- Liste sistemas, serviços ou condições externas das quais o produto depende para funcionar. Para cada um, descreva o impacto caso esteja indisponível. -->

| Dependência | Descrição | Impacto se indisponível |
|---|---|---|
| [Nome da dependência] | [O que é e por que o produto depende dela] | [O que deixa de funcionar] |
| [Nome da dependência] | [...] | [...] |

### Fora de Escopo

<!-- Liste explicitamente o que NÃO faz parte deste produto ou desta versão. Reduz ambiguidade e alinha expectativas. -->

- [O que o produto não faz intencionalmente]
- [Funcionalidade excluída desta versão]

---

## 7. GLOSSÁRIO

<!-- Glossário consolidado de todos os termos do produto. Inclua aqui os mesmos termos da seção 3 mais quaisquer outros relevantes para leitores externos. -->

| Termo | Definição |
|---|---|
| **[Termo]** | [Definição completa] |
| **[Termo]** | [Definição] |
