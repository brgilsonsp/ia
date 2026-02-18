# AI Prompts & Guardrails

A collection of reusable prompts and guardrails for LLM-based workflows, focused on quality, precision, and anti-hallucination.

---

## Structure

```
ia/
├── prompts/
│   ├── roles/
│   │   └── prompt_engineering.md          # Prompt Engineer specialist role
│   ├── product/
│   │   └── product_manager_digital_service.md  # Product Manager (PRD co-creation)
│   ├── translator/
│   │   └── translator_br_to_en.md         # Brazilian Portuguese → American English translator
│   └── validate_text/
│       ├── validate_pt_br_general_text.md     # General pt-BR text reviewer (any domain)
│       └── validate_pt_br_technical_text.md   # Technical pt-BR text reviewer (Software Architecture)
└── guardrails/
    ├── scope_precision_anti-hallucination.md  # Reusable guardrail block
    └── validate_english_prompt/
        ├── validate_english.py            # Claude Code hook — grammar check on user prompts
        ├── CLAUDE.md                      # Hook configuration for Claude Code CLI
        ├── settings.json                  # Hook settings
        └── LEIA-ME.md                     # Setup instructions (pt-BR)
```

---

## Prompts

### `roles/prompt_engineering.md`
A **Prompt Engineer** specialist that helps design, analyze, and optimize prompts for any LLM. Works in consultative mode: diagnoses existing prompts, proposes improvements with justification, and follows a structured workflow (Discovery → Analysis → Construction → Validation).

### `product/product_manager_digital_service.md`
A **Product Manager** that co-creates PRDs (Product Requirements Documents) using Socratic questioning. Focuses strictly on *what* the product does and *why* it exists — no technology decisions. Outputs PRD content in Brazilian Portuguese; all conversation in English.

### `translator/translator_br_to_en.md`
A **professional translator** for Brazilian Portuguese → American English. Handles idiomatic expressions, cultural adaptations, false cognates, and registers (formal, informal, technical). Strictly one-directional; will not accept reverse translation requests.

### `validate_text/validate_pt_br_general_text.md`
A **multidisciplinary review panel** for pt-BR texts across any domain. Reviews through six specialist lenses: linguistic quality, structure, factual accuracy, UX writing, purpose alignment, and QA. Outputs a severity-classified report and a revised version.

### `validate_text/validate_pt_br_technical_text.md`
Same review panel, specialized for **Software Architecture and technical digital products** (ADRs, RFCs, READMEs, runbooks, API docs, PRDs). Includes a dedicated Software Architect Reviewer and Product Manager Reviewer role.

---

## Guardrails

### `scope_precision_anti-hallucination.md`
A standalone guardrail block covering:
- Prohibition of data fabrication
- Mandatory uncertainty handling with classification labels
- Permission and obligation to ask clarifying questions
- Scope control (no unsolicited expansion)
- Prohibition of implicit assumptions and authority claims
- Coherence and consistency checks

This block can be embedded into any custom prompt.

### `validate_english_prompt/`
A **Claude Code hook** that intercepts user prompts before they reach Claude, validates the English grammar, and blocks the prompt with feedback if errors are found. Designed for A2/B1 level English learners.

- Requires `ANTHROPIC_API_KEY` in environment
- Uses `claude-haiku-4-5-20251001` for fast, low-cost validation
- See `LEIA-ME.md` for setup instructions

---

## Design Principles

All prompts in this repository follow these conventions:

- **Explicit guardrails** — every prompt defines what the model must *never* do
- **Certainty labeling** — outputs classify information as `[User-Provided Fact]`, `[Hypothesis]`, `[Estimate]`, etc.
- **Ask before assume** — models stop and ask when context is ambiguous or insufficient
- **Scope discipline** — models do not expand into unsolicited areas
- **Iterative workflow** — prompts define a step-by-step process with validation checkpoints
