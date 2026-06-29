---
description: Run an ad-hoc deliberator deliberation on a natural-language question. Uses the built-in pragmatist + devil's advocate agents, no config file needed.
---

# Deliberator Decide

Run a quick ad-hoc deliberation. No config file, just a question.

## Step 0: Check installation

```bash
command -v deliberator >/dev/null 2>&1 || echo "NOT_INSTALLED"
```

If `NOT_INSTALLED`, stop and tell the user to install:
```
pip install git+https://github.com/Build-Fractal/deliberator.git
```

## Step 1: Parse arguments

Expected invocation: `/deliberator:decide "<question>" [--provider <provider>] [--mode <mode>]`

If the user didn't provide a question, ask:
> What decision do you want me to deliberate on? Be specific.

Providers available: `mock` (default, no API key), `anthropic`, `openai`, `claude-code`, `ollama`, `gemini`, `codex`, `copilot`, `aider`, `opencode`.

Modes available to `decide`: `cooperative` (default), `winner-take-all`, `prisoners-dilemma`, `red-blue`.

## Step 2: Preflight — OAuth provider auto-selection

The default `anthropic` provider hits Anthropic's API directly and requires `ANTHROPIC_API_KEY`. On Anthropic OAuth (Claude Max / subscription), that path 429s instantly on a server-side concurrency policy gate — retrying won't help. The fix is to route through `claude-code` instead, which spawns `claude -p` subprocesses (designed for OAuth).

Before the run, auto-set `DELIBERATOR_PROVIDER=claude-code` when ALL of:
- The user did NOT pass `--provider` explicitly (let the operator's choice always win, even an empty string).
- `DELIBERATOR_PROVIDER` is unset in the environment.
- `ANTHROPIC_API_KEY` is unset.
- `~/.deliberator/auth.json` exists and shows an OAuth marker.

```bash
if [ -z "${DELIBERATOR_PROVIDER+set}" ] && [ -z "${ANTHROPIC_API_KEY:-}" ] && [ -f "$HOME/.deliberator/auth.json" ]; then
  if grep -qE '"(access_token|oauth)"' "$HOME/.deliberator/auth.json" 2>/dev/null; then
    export DELIBERATOR_PROVIDER=claude-code
    echo "note: detected Anthropic OAuth auth with no ANTHROPIC_API_KEY; auto-set DELIBERATOR_PROVIDER=claude-code" >&2
  fi
fi
```

Skip this preflight when the user passed `--provider <X>` — their explicit value (including empty) wins.

## Step 3: Run

```bash
deliberator decide "<question>" --provider <provider> --mode <mode>
```

Examples:
```bash
# Quick mock run (free, synthetic responses)
deliberator decide "Should we use Redis or Postgres for session storage?" --provider mock

# Real run with Claude Code
deliberator decide "Build vs buy for our auth system?" --provider claude-code --mode cooperative

# Red-team mode for adversarial review
deliberator decide "What could go wrong with this migration plan?" --provider anthropic --mode red-blue
```

## Step 4: Display results

Show the CLI output verbatim. Preserve any Rich-formatted tables or progress output. The final synthesis is what the user cares about most.

If the command exits non-zero, diagnose:
- **"Question too vague" classifier error**: suggest rephrasing to be more specific (e.g., "Should we do X or Y?" rather than "What should we do?")
- **Provider auth error**: run `deliberator status` to check, then `deliberator login <provider>` if needed
- **MCP extras missing**: `pip install "deliberator[mcp] @ git+https://github.com/Build-Fractal/deliberator.git"`

## Tip for first-time users

If this is the user's first deliberation, suggest they try the mock provider first to see the pipeline shape without spending credits:

> Want to see what the pipeline looks like before spending credits? Run with `--provider mock` — it uses synthetic responses but shows you all 5 phases (review → cross-review → revision → disputes → synthesis).
