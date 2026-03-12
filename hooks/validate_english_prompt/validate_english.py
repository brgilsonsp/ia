#!/usr/bin/env python3
"""
English Grammar Validator Hook for Claude Code CLI
Intercepts every prompt, checks grammar/clarity, and teaches the user.
Level: A2/B1 - Explains errors and lets the user correct them.
"""

import json
import sys
import os
import urllib.request
import urllib.error

def call_claude_api(prompt_text: str) -> dict:
    """Call Claude API to validate English grammar."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return {"valid": True, "reason": "No API key found, skipping validation."}

    system_prompt = """You are an English grammar tutor for a Brazilian Portuguese speaker at A2/B1 level.

Your job is to analyze the user's English prompt and check:
1. Grammar correctness (tense, subject-verb agreement, articles, word order)
2. Spelling errors
3. Whether the meaning/intent is clear

Rules:
- Be encouraging and kind, never harsh
- Explain errors in simple terms, using Portuguese when necessary to explain grammar concepts
- Do NOT correct the text for the user — explain what is wrong and let them fix it
- If the text is perfectly correct, say so with enthusiasm
- Keep explanations short and focused

Respond ONLY in this exact JSON format (no markdown, no extra text):
{
  "is_correct": true or false,
  "errors": [
    {
      "original": "the wrong part",
      "explanation": "Why it is wrong (in PT-BR if needed)",
      "hint": "A tip to help fix it, without giving the full answer"
    }
  ],
  "encouragement": "A short motivational message in Portuguese"
}

If there are no errors, return:
{
  "is_correct": true,
  "errors": [],
  "encouragement": "Mensagem motivacional curta em português"
}"""

    payload = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 1024,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": f"Please check this English text:\n\n{prompt_text}"}
        ]
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=data,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode("utf-8"))
            text = result["content"][0]["text"]
            return json.loads(text)
    except Exception as e:
        return {"valid": True, "error": str(e)}


def format_feedback(analysis: dict) -> str:
    """Format the grammar feedback for display in terminal."""
    lines = []
    lines.append("\n" + "="*60)
    lines.append("📚 ENGLISH TUTOR — Grammar Check")
    lines.append("="*60)

    if analysis.get("is_correct"):
        lines.append("✅ Perfect English! No errors found.")
        if analysis.get("encouragement"):
            lines.append(f"💬 {analysis['encouragement']}")
    else:
        errors = analysis.get("errors", [])
        if errors:
            lines.append(f"⚠️  Found {len(errors)} issue(s) in your prompt:\n")
            for i, error in enumerate(errors, 1):
                lines.append(f"  [{i}] Original: \"{error.get('original', '')}\"")
                lines.append(f"      ❌ Problem: {error.get('explanation', '')}")
                lines.append(f"      💡 Hint: {error.get('hint', '')}")
                lines.append("")
        if analysis.get("encouragement"):
            lines.append(f"💬 {analysis['encouragement']}")

    lines.append("="*60)
    return "\n".join(lines)


def main():
    """Main hook entry point — reads JSON from stdin (Claude Code format)."""
    try:
        raw = sys.stdin.read()
        hook_input = json.loads(raw)
    except Exception:
        # If we can't parse input, let Claude proceed normally
        sys.exit(0)

    # Extract the prompt text from Claude Code's hook payload
    prompt = hook_input.get("prompt", "").strip()

    # Skip very short prompts (commands, single words)
    if len(prompt) < 8:
        sys.exit(0)

    # Skip prompts that look like slash commands
    if prompt.startswith("/"):
        sys.exit(0)

    # Validate the English
    analysis = call_claude_api(prompt)

    # If there's an error or text is correct, proceed normally
    if analysis.get("is_correct", True) or "error" in analysis:
        if analysis.get("is_correct"):
            feedback = format_feedback(analysis)
            print(feedback, file=sys.stderr)
        sys.exit(0)

    # Show errors and block the prompt
    feedback = format_feedback(analysis)
    print(feedback, file=sys.stderr)

    # Return JSON to Claude Code to block and show message
    output = {
        "decision": "block",
        "reason": "Your prompt has grammar issues. Please correct them and try again! 📝"
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
