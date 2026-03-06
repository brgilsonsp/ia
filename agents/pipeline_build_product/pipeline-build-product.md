PIPELINE DE CONSTRUÇÃO DE PRODUTO DIGITAL

O objetivo é criar uma pipeline de construção de produto digital, onde cada agente tem um papel específico e contribui para o desenvolvimento do produto de software.

A pipeline é orquestrada por um humano, que interage com cada agente seguindo a sequência lógica definida neste documento. A cada etapa, o humano fornece os artefatos necessários ao agente, lê o que foi produzido e decide o próximo passo: avançar com o artefato ou retornar ao agente responsável com base no feedback recebido.

Regra de outputs:
- Todo artefato produzido por qualquer agente deve ser salvo em arquivo.
- Todo feedback produzido pelos Agentes 02, 03, 04, 06 e 07 deve ser salvo em arquivo. O Agente 05 não produz feedback separado — seu artefato 05-gate-report.md cobre tanto aprovação quanto bloqueio.
- O Agente 01 pode fornecer feedback diretamente no prompt, sem necessidade de arquivo; porém seu artefato deve ser salvo em arquivo.

Sequência lógica da pipeline:

   01 → 02 → 03 → 04 → 05 → 06 (paralelo, por especialidade definida pelo Agente 04) → 07

---

AGENTES

01 - Discovery/Briefing

Responsabilidade: receber a entrada bruta do usuário (ideias, problemas, oportunidades) e transformá-la em um brief estruturado que sirva de input consistente para o Product Manager.

Entrada: descrição inicial fornecida pelo humano sobre o produto que deseja construir.

Artefato de saída (arquivo): brief estruturado contendo:
- Problema a ser resolvido
- Segmento-alvo
- Restrições técnicas conhecidas
- Critérios de sucesso esperados

Feedback (prompt): caso a entrada do humano seja insuficiente ou ambígua, o agente deve solicitar esclarecimentos diretamente no prompt antes de produzir o artefato, indicando exatamente quais informações estão faltando.

---

02 - Product Manager

Responsabilidade: definir os requisitos do produto e criar o PRD com base no brief estruturado.

Entrada: artefato do Agente 01 (brief estruturado).

Artefato de saída (arquivo): PRD (Product Requirements Document) detalhando os requisitos funcionais e não funcionais do produto.

Feedback de saída (arquivo): caso o brief recebido seja ambíguo, incompleto ou contraditório ao ponto de impedir a criação de um PRD coerente, o agente deve produzir um arquivo de feedback indicando: o problema identificado e as informações necessárias para retomar. O humano deverá retornar ao Agente 01 com esse feedback.

---

03 - Tech Lead Arquiteto de Soluções Digitais

Responsabilidade: projetar a arquitetura técnica do produto garantindo aderência aos requisitos do PRD.

Entrada: artefato do Agente 02 (PRD).

Artefato de saída (arquivo): arquitetura técnica do produto, incluindo estrutura e componentes do sistema, stack tecnológica e diretrizes para implementação.

Feedback de saída (arquivo): caso os requisitos do PRD sejam tecnicamente inviáveis, contraditórios ou insuficientes para definir uma arquitetura, o agente deve produzir um arquivo de feedback indicando: o problema identificado e os esclarecimentos necessários. O humano deverá retornar ao Agente 02 com esse feedback.

---

04 - Engenheiro de Software Sênior

Responsabilidade: refinar as tarefas de desenvolvimento com base no PRD e na arquitetura técnica, classificando-as por domínio, sequenciando-as por dependência e definindo critérios de aceite para cada uma. Como parte desse processo, o agente deve identificar e propor as especialidades técnicas necessárias para implementar cada tarefa, e interagir com o humano para validar ou ajustar essas especialidades antes de produzir o artefato final.

Entrada: artefatos dos Agentes 02 (PRD) e 03 (arquitetura técnica).

Interação com o humano: antes de produzir o artefato, o agente deve apresentar ao humano a lista de especialidades técnicas identificadas para o conjunto de tarefas, por exemplo:
- Engenheiro Sênior Backend Java com Spring Boot
- Engenheiro Sênior Frontend Web React
- Engenheiro Pleno Frontend Mobile React Native
- DBA Sênior PostgreSQL
O humano pode confirmar, ajustar, adicionar ou remover especialidades. O artefato final só deve ser produzido após essa validação.

Artefato de saída (arquivo): lista de tarefas de desenvolvimento contendo, para cada tarefa:
- Domínio: backend, frontend, banco de dados ou outro domínio identificado
- Especialidade técnica necessária para implementar a tarefa (conforme validado com o humano)
- Descrição objetiva da tarefa
- Dependências em relação a outras tarefas
- Critérios de aceite testáveis

Feedback de saída (arquivo): caso a arquitetura contenha lacunas que impeçam a decomposição em tarefas, ou caso o PRD apresente requisitos funcionais ausentes, o agente deve produzir um arquivo de feedback indicando: o problema identificado e o agente de destino do retorno (Agente 02 ou 03). O humano deverá encaminhar o feedback ao agente correspondente.

---

05 - Gate de Consistência

Responsabilidade: verificar a coerência entre os três artefatos principais da pipeline (PRD, arquitetura técnica e tarefas de desenvolvimento) antes de liberar o avanço para a implementação.

Entrada: artefatos dos Agentes 02 (PRD), 03 (arquitetura técnica) e 04 (tarefas de desenvolvimento).

Verificações obrigatórias:
- GC-01 Cobertura de requisitos: todos os requisitos do PRD estão cobertos por ao menos uma tarefa de desenvolvimento.
- GC-02 Aderência arquitetural: nenhuma tarefa propõe abordagem técnica que contradiga ou ignore a arquitetura definida.
- GC-03 Completude dos critérios de aceite: todas as tarefas possuem critérios de aceite definidos, objetivos e testáveis.
- GC-04 Sequenciamento e dependências: a ordem de execução das tarefas respeita as dependências técnicas entre especialidades, conforme definido pelo Agente 04. Especialidades cujos artefatos são pré-requisito de outras devem ser executadas primeiro.
- GC-05 Ausência de conflitos entre domínios: não há sobreposição ou conflito entre tarefas de domínios diferentes que possa gerar inconsistências na integração.

Artefato de saída (arquivo): 05-gate-report.md, sempre produzido ao final da verificação. O campo Resultado indica APROVADO ou BLOQUEADO. Quando APROVADO, o arquivo lista as especialidades a acionar e a ordem de execução. Quando BLOQUEADO, o arquivo detalha as verificações que falharam, o problema identificado em cada uma e o agente de destino do retorno (Agente 02, 03 ou 04). O humano deverá encaminhar as falhas ao agente correspondente antes de retornar ao Gate.

---

06 - Engenheiro de Software

Este agente é instanciado uma vez para cada especialidade técnica listada na seção "Especialidades Técnicas Validadas" do artefato do Agente 04. Ao ser acionado, o humano informa apenas o identificador de especialidade — exatamente como está registrado em 04-tasks.md. O agente lê esse artefato, assume o perfil, nível de senioridade, stack e boas práticas da especialidade informada, e filtra automaticamente as tarefas atribuídas a ela. Nenhuma outra configuração é necessária por parte do humano.

A ordem de execução entre instâncias segue o sequenciamento de dependências definido pelo Agente 04: instâncias cujos artefatos são pré-requisito de outras devem ser executadas antes, ou em paralelo quando não houver dependência entre elas.

Responsabilidade: assumir a especialidade definida pelo Agente 04 e implementar as tarefas atribuídas a ela, garantindo qualidade e aderência aos critérios de aceite definidos.

Entrada: identificador de especialidade informado pelo humano (deve corresponder exatamente a um valor listado em 04-tasks.md), artefatos dos Agentes 02 (PRD), 03 (arquitetura técnica) e 04 (tarefas de desenvolvimento). Quando houver dependência do artefato de outro Agente 06, esse artefato também deve ser fornecido como entrada antes do início da implementação.

Artefato de saída (arquivo): código-fonte referente às tarefas da especialidade assumida, implementado e pronto para implantação.

Feedback de saída (arquivo): caso as tarefas sejam ambíguas, incompletas ou impossíveis de implementar como descritas, ou caso um artefato de dependência de outro Agente 06 esteja incompleto ou inconsistente, o agente deve produzir um arquivo de feedback indicando: o problema identificado e o agente de destino do retorno (Agente 04 ou o Agente 06 responsável pelo artefato de dependência). O humano deverá encaminhar o feedback ao agente correspondente.

---

07 - QA Engineer Sênior

Responsabilidade: implementar os testes automatizados para os artefatos produzidos pelas instâncias do Agente 06, validando que o código produzido atende aos critérios de aceite definidos nas tarefas.

Entrada: artefatos dos Agentes 02 (PRD), 03 (arquitetura técnica), 04 (tarefas com critérios de aceite) e os artefatos de código-fonte de todas as instâncias do Agente 06.

Artefato de saída (arquivo): código-fonte dos testes automatizados implementados e prontos para execução.

Feedback de saída (arquivo): caso algum código-fonte não atenda aos critérios de aceite, ou os critérios de aceite sejam insuficientes para definir os cenários de teste, o agente deve produzir um arquivo de feedback indicando: o problema identificado e o agente de destino do retorno (Agente 04 ou a instância 06 responsável pelo código problemático). O humano deverá encaminhar o feedback ao agente correspondente.

---

FEEDBACK LOOPS

Quando um agente não consegue produzir seu artefato, ele produz um arquivo de feedback em vez do artefato. O arquivo de feedback deve conter:
- Agente que identificou o problema
- Agente de destino do retorno
- Descrição objetiva do problema
- Informações ou esclarecimentos necessários para retomar

O humano lê o arquivo de feedback, retorna ao agente indicado com as informações necessárias e, após a correção, reinicia a pipeline a partir do ponto de falha.

Mapeamento dos feedback loops:

   FB-01: Agente 02 → Agente 01
   Condição: brief ambíguo, incompleto ou contraditório.

   FB-02: Agente 03 → Agente 02
   Condição: PRD com requisitos tecnicamente inviáveis, contraditórios ou insuficientes.

   FB-03: Agente 04 → Agente 03
   Condição: arquitetura com lacunas que impedem a decomposição em tarefas.

   FB-04: Agente 04 → Agente 02
   Condição: requisitos funcionais ausentes no PRD identificados durante o refinamento.

   FB-05: Agente 05 → Agente 02, 03 ou 04
   Condição: falha em qualquer uma das verificações GC-01 a GC-05.

   FB-06: Agente 06 → Agente 03 ou 04
   Condição: tarefas atribuídas à especialidade são ambíguas, incompletas, impossíveis de implementar como descritas, ou inconsistentes com o PRD ou a arquitetura técnica. O agente de destino do retorno é o 04 quando o problema está na definição da tarefa, ou o 03 quando o problema está na arquitetura.

   FB-07: Agente 06 → Outro Agente 06
   Condição: artefato de dependência de outro Agente 06 está incompleto ou inconsistente com as tarefas a implementar.

   FB-08: Agente 07 → Agente 06 responsável
   Condição: código-fonte de um Agente 06 não atende aos critérios de aceite das tarefas.

   FB-09: Agente 07 → Agente 04
   Condição: critérios de aceite insuficientes ou contraditórios para definir os cenários de teste.

---

CONTRATOS DE I/O

Define o esquema obrigatório de cada arquivo produzido na pipeline. Todo campo listado é obrigatório. O formato de todos os arquivos é Markdown.

Esquema comum — Arquivo de Feedback (Agentes 02, 03, 04, 06 e 07)
Nome do arquivo: [número-agente]-feedback.md
Exemplo: 04-feedback.md
Observação: o Agente 05 não utiliza este esquema. Seu único artefato de saída é o 05-gate-report.md, que cobre tanto aprovação quanto bloqueio.

   # Feedback

   **Agente de Origem:** [número e nome do agente]
   **Agente de Destino:** [número e nome do agente]

   ## Problema Identificado
   [descrição objetiva do problema que impediu a produção do artefato]

   ## Informações Necessárias para Retomar
   [o que precisa ser fornecido ou corrigido para que a execução seja retomada]

---

Agente 01 — Artefato
Nome do arquivo: 01-brief.md

   # Brief do Produto

   ## Problema a Resolver
   [descrição clara e objetiva do problema que o produto se propõe a resolver]

   ## Segmento-alvo
   [descrição do perfil do usuário ou cliente que o produto atende]

   ## Restrições Técnicas Conhecidas
   [limitações técnicas já conhecidas: stack obrigatória, integrações existentes, infraestrutura, etc.]

   ## Critérios de Sucesso
   [indicadores ou condições que definem que o produto foi bem-sucedido]

---

Agente 02 — Artefato
Nome do arquivo: 02-prd.md

   # Product Requirements Document

   ## Visão Geral do Produto
   [descrição do produto, seu propósito e o problema que resolve]

   ## Objetivos
   [lista dos objetivos de negócio e de produto]

   ## Requisitos Funcionais
   [lista numerada de funcionalidades que o produto deve ter]

   ## Requisitos Não Funcionais
   [lista de requisitos de qualidade: performance, segurança, disponibilidade, etc.]

   ## Restrições
   [limitações que o produto deve respeitar: técnicas, regulatórias, de prazo, etc.]

   ## Fora de Escopo
   [lista do que explicitamente não será coberto por este produto]

---

Agente 03 — Artefato
Nome do arquivo: 03-architecture.md

   # Arquitetura Técnica

   ## Visão Geral
   [descrição resumida da arquitetura e das principais decisões técnicas]

   ## Componentes do Sistema
   [lista e descrição de cada componente, serviço ou módulo do sistema]

   ## Stack Tecnológica
   [lista das tecnologias, frameworks e ferramentas adotadas por camada]

   ## Interfaces e Integrações
   [descrição das APIs, contratos de comunicação e integrações externas]

   ## Diretrizes de Implementação
   [regras e padrões que os agentes de implementação devem seguir]

---

Agente 04 — Artefato
Nome do arquivo: 04-tasks.md

   # Tarefas de Desenvolvimento

   ## Especialidades Técnicas Validadas
   [lista das especialidades confirmadas com o humano. Cada valor desta lista é o identificador
   que o humano deve fornecer ao Agente 06 para acionar a instância correspondente.
   O valor deve ser idêntico ao usado no campo Especialidade de cada tarefa abaixo.]
   - [Especialidade 1]
   - [Especialidade 2]

   ## Tarefas

   ### TASK-001: [título da tarefa]
   **Especialidade:** [deve corresponder exatamente a um valor listado em Especialidades Técnicas Validadas]
   **Domínio:** [backend | frontend | banco de dados | outro]
   **Descrição:** [descrição objetiva do que deve ser implementado]
   **Dependências:** [lista de IDs de tarefas que devem ser concluídas antes desta, ou "nenhuma"]
   **Critérios de Aceite:**
   - [ ] [critério testável 1]
   - [ ] [critério testável 2]

   [repetir bloco ### TASK-XXX para cada tarefa]

---

Agente 05 — Artefato
Nome do arquivo: 05-gate-report.md
O arquivo deve registrar APROVADO ou BLOQUEADO, nunca os dois.

   # Relatório do Gate de Consistência

   **Resultado:** APROVADO | BLOQUEADO

   ## Verificações
   - GC-01 Cobertura de requisitos: PASSOU | FALHOU
   - GC-02 Aderência arquitetural: PASSOU | FALHOU
   - GC-03 Completude dos critérios de aceite: PASSOU | FALHOU
   - GC-04 Sequenciamento e dependências: PASSOU | FALHOU
   - GC-05 Ausência de conflitos entre domínios: PASSOU | FALHOU

   ## Próximos Passos
   [presente apenas se Resultado = APROVADO]
   [lista das instâncias 06 a acionar, na ordem de execução definida pelo Agente 04]

   ## Falhas Identificadas
   [presente apenas se Resultado = BLOQUEADO]
   [para cada verificação que falhou:]
   - Verificação: [GC-XX]
   - Problema: [descrição]
   - Agente de destino do retorno: [número e nome]
   - Ação necessária: [o que deve ser corrigido]

---

Agente 06 — Artefato
Nome do arquivo: 06-[slug-da-especialidade].md
Exemplo: 06-backend-java.md, 06-frontend-react.md, 06-dba-postgresql.md
O slug deve ser derivado do identificador de especialidade registrado em 04-tasks.md.
Para acionar este agente, o humano fornece o identificador de especialidade exatamente como
registrado na seção "Especialidades Técnicas Validadas" de 04-tasks.md. O agente lê o arquivo,
assume o perfil da especialidade e filtra as tarefas correspondentes.

   # Implementação — [valor exato do identificador de especialidade lido de 04-tasks.md]

   ## Tarefas Implementadas

   ### TASK-001: [título da tarefa]
   **Status:** Concluída | Bloqueada
   **Arquivos criados/modificados:**
   - [caminho/do/arquivo.ext]
   **Observações:** [considerações técnicas relevantes, ou "nenhuma"]

   [repetir bloco ### TASK-XXX para cada tarefa atribuída a esta especialidade]

---

Agente 07 — Artefato
Nome do arquivo: 07-tests.md

   # Testes Automatizados

   ## Tarefas Cobertas

   ### TASK-001: [título da tarefa]
   **Tipo de Teste:** unitário | integração | e2e
   **Cenários Cobertos:**
   - [ ] [cenário 1]
   - [ ] [cenário 2]
   **Arquivos de Teste:**
   - [caminho/do/arquivo-de-teste.ext]

   [repetir bloco ### TASK-XXX para cada tarefa coberta pelos testes]
