# 🇧🇷 Guia de Instalação — English Tutor para Claude Code CLI
## Windows — Passo a Passo Completo

---

## O que essa configuração faz?

Toda vez que você digitar um prompt no Claude CLI:

1. **Intercepta seu texto** antes de enviar para o Claude
2. **Verifica a gramática** em inglês automaticamente
3. Se encontrar erros:
   - Mostra **o que está errado** e **por quê**
   - Dá uma **dica** para você corrigir (sem dar a resposta pronta)
   - **Bloqueia o envio** até você corrigir
4. Se estiver correto: mostra uma mensagem de parabéns e envia normalmente
5. O Claude também vai reforçar o aprendizado nas respostas dele

---

## Pré-requisitos

- [ ] Claude Code CLI instalado (`npm install -g @anthropic-ai/claude-code`)
- [ ] Python 3.8+ instalado ([python.org](https://python.org))
- [ ] Variável de ambiente `ANTHROPIC_API_KEY` configurada

---

## Instalação (5 minutos)

### Passo 1 — Criar a pasta do Claude (se não existir)

Abra o **PowerShell** ou **Prompt de Comando** e execute:

```powershell
mkdir "$env:USERPROFILE\.claude\hooks" -Force
```

### Passo 2 — Copiar os arquivos

Copie os arquivos desta pasta para os destinos abaixo:

| Arquivo deste pacote | Destino no seu computador |
|---|---|
| `hooks\validate_english.py` | `C:\Users\SEU_USUARIO\.claude\hooks\validate_english.py` |
| `CLAUDE.md` | `C:\Users\SEU_USUARIO\.claude\CLAUDE.md` |
| `settings.json` | `C:\Users\SEU_USUARIO\.claude\settings.json` |

**Substituindo SEU_USUARIO pelo seu nome de usuário do Windows.**

Ou via PowerShell (execute na pasta deste pacote):

```powershell
# Substitua o caminho abaixo pelo local onde você salvou os arquivos
$source = ".\english-tutor-setup"

Copy-Item "$source\hooks\validate_english.py" "$env:USERPROFILE\.claude\hooks\validate_english.py"
Copy-Item "$source\CLAUDE.md"               "$env:USERPROFILE\.claude\CLAUDE.md"
Copy-Item "$source\settings.json"           "$env:USERPROFILE\.claude\settings.json"

Write-Host "✅ Arquivos copiados com sucesso!" -ForegroundColor Green
```

### Passo 3 — Verificar sua ANTHROPIC_API_KEY

O hook usa a API do Claude para validar a gramática. Certifique-se de que a variável está configurada:

```powershell
echo $env:ANTHROPIC_API_KEY
```

Se estiver vazia, configure assim (permanente):

```powershell
[System.Environment]::SetEnvironmentVariable(
  "ANTHROPIC_API_KEY",
  "sk-ant-SUA_CHAVE_AQUI",
  "User"
)
```

> 💡 Você encontra sua chave em: https://console.anthropic.com/settings/keys

### Passo 4 — Testar a instalação

Abra um novo terminal e execute:

```powershell
claude
```

Digite um prompt em inglês com erro proposital, por exemplo:
```
I has go to the market yesterday
```

Você deve ver algo assim:
```
============================================================
📚 ENGLISH TUTOR — Grammar Check
============================================================
⚠️  Found 2 issue(s) in your prompt:

  [1] Original: "has go"
      ❌ Problem: "Has" não é o auxiliar correto aqui. Para passado, use "went" (go é irregular)
      💡 Hint: Pense em qual tempo verbal você quer usar. "Yesterday" indica passado...

  [2] Original: "has"
      ❌ Problem: Para o sujeito "I", o verbo "have" no passado é "had", não "has"
      💡 Hint: "I has" nunca está correto. "I have" (presente) ou "I had" (passado)

💬 Boa tentativa! Você está praticando e isso é o mais importante! 🌟
============================================================
```

---

## Como funciona para o Claude.ai (chat web)?

O hook só funciona no CLI. Para o **claude.ai no navegador**, o `CLAUDE.md` global não é carregado automaticamente.

**Solução para o chat web:** Crie um **Projeto** no claude.ai e cole o conteúdo do arquivo `CLAUDE.md` nas instruções do projeto. Assim o Claude vai corrigir sua gramática nas respostas de todas as conversas dentro daquele projeto.

Passos:
1. Acesse claude.ai → clique em **"Projects"** → **"New Project"**
2. Dê um nome: "English Practice"
3. Em **"Project instructions"**, cole o conteúdo do arquivo `CLAUDE.md`
4. Use esse projeto para todas as suas conversas de prática

---

## Estrutura de arquivos criada

```
C:\Users\SEU_USUARIO\.claude\
├── CLAUDE.md              ← Instruções globais para o Claude
├── settings.json          ← Configura o hook de validação
└── hooks\
    └── validate_english.py ← Script que valida sua gramática
```

---

## Solução de problemas

| Problema | Solução |
|---|---|
| Hook não executa | Verifique se Python está no PATH: `python --version` |
| Erro de API key | Verifique `echo $env:ANTHROPIC_API_KEY` |
| Hook valida mas não bloqueia | Verifique se o `settings.json` está no lugar certo |
| Quer desativar temporariamente | Renomeie `settings.json` para `settings.json.bak` |

---

## Custos

O hook usa o modelo **Claude Haiku** (o mais barato) para validar gramática.
Custo estimado: menos de **$0.01 por 100 prompts**. Praticamente zero!

---

*Bons estudos! Every mistake is a step forward. 🚀*
