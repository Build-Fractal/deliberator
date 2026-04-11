---
description: Run an ad-hoc conversus deliberation on a natural-language question. Uses the built-in pragmatist + devil's advocate agents, no config file needed.
---

# Conversus Decide

Run a quick ad-hoc deliberation. No config file, just a question.

## Step 0: Check installation

```bash
conversus --version 2>/dev/null || echo "NOT_INSTALLED"
```

If `NOT_INSTALLED`, stop and tell the user to install:
```
pip install git+https://github.com/Build-Fractal/conversus-oss.git
```

## Step 1: Parse arguments

Expected invocation: `/conversus:decide "<question>" [--provider <provider>] [--mode <mode>]`

If the user didn't provide a question, ask:
> What decision do you want me to deliberate on? Be specific.

Providers available: `mock` (default, no API key), `anthropic`, `openai`, `claude-code`, `ollama`, `gemini`, `codex`, `copilot`, `aider`, `opencode`.

Modes available to `decide`: `cooperative` (default), `winner-take-all`, `prisoners-dilemma`, `red-blue`.

## Step 2: Run

```bash
conversus decide "<question>" --provider <provider> --mode <mode>
```

Examples:
```bash
# Quick mock run (free, synthetic responses)
conversus decide "Should we use Redis or Postgres for session storage?" --provider mock

# Real run with Claude Code
conversus decide "Build vs buy for our auth system?" --provider claude-code --mode cooperative

# Red-team mode for adversarial review
conversus decide "What could go wrong with this migration plan?" --provider anthropic --mode red-blue
```

## Step 3: Display results

Show the CLI output verbatim. Preserve any Rich-formatted tables or progress output. The final synthesis is what the user cares about most.

If the command exits non-zero, diagnose:
- **"Question too vague" classifier error**: suggest rephrasing to be more specific (e.g., "Should we do X or Y?" rather than "What should we do?")
- **Provider auth error**: run `conversus status` to check, then `conversus login <provider>` if needed
- **MCP extras missing**: `pip install "conversus[mcp] @ git+https://github.com/Build-Fractal/conversus-oss.git"`

## Tip for first-time users

If this is the user's first deliberation, suggest they try the mock provider first to see the pipeline shape without spending credits:

> Want to see what the pipeline looks like before spending credits? Run with `--provider mock` — it uses synthetic responses but shows you all 5 phases (review → cross-review → revision → disputes → synthesis).
