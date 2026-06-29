---
description: Run a full deliberator deliberation from a deliberator.yml config file. Use this for reproducible deliberations with custom agents, modes, and target documents.
---

# Deliberator Run

Run a full deliberation from a config file. Use `/deliberator:decide` for ad-hoc questions; use this for reproducible, custom-agent deliberations.

## Step 0: Check installation

```bash
command -v deliberator >/dev/null 2>&1 || echo "NOT_INSTALLED"
```

If `NOT_INSTALLED`, stop and tell the user:
```
pip install git+https://github.com/Build-Fractal/deliberator.git
```

## Step 1: Parse arguments

Expected: `/deliberator:run <config.yml> [--provider <provider>] [--model <model>] [--rounds <n>] [--phase <phase>]`

If no config path given, ask:
> Which config file? (e.g., `deliberations/my-review/deliberator.yml`)

If the path doesn't exist, verify with `ls -la <path>` and ask for the correct one.

## Step 2: Validate first (recommended)

Before running, check the config is valid and estimate cost:

```bash
deliberator validate <config_path>
```

This prints the mode, agent count, iterations, and total LLM launches. Show the output to the user. If the launch count looks surprisingly high (>30), ask:
> This run will use N LLM launches. Is that expected, or want to reduce iterations/agents?

## Step 3: Preflight — OAuth provider auto-selection

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

## Step 4: Run

```bash
deliberator run <config_path> --provider <provider> [--model <model>] [--rounds <n>] [--phase <phase>]
```

Providers: `mock` (default), `anthropic`, `openai`, `claude-code`, `ollama`, `gemini`, `codex`, `copilot`, `aider`, `opencode`.

Phases: `all` (default) runs the full pipeline, `review` runs only the first phase for spot-checking.

Examples:
```bash
# Full run with Claude Code
deliberator run deliberations/auth-review/deliberator.yml --provider claude-code

# Mock dry-run to see pipeline shape
deliberator run deliberations/auth-review/deliberator.yml --provider mock

# Just the review phase (fast spot-check)
deliberator run deliberations/auth-review/deliberator.yml --provider anthropic --phase review
```

## Step 5: Display results

Show the CLI's progress output (phase checkmarks, agent dispatches, timings). After completion:

1. Show the paths to output files that were written
2. If `summary/final.md` exists, read it and summarize the verdict for the user
3. If any phase failed, show the error and suggest fixes

## Common errors

- **Config validation error**: `deliberator validate` will give a specific message. Typically missing `mode`, `agents`, or `target` fields.
- **Provider auth error**: run `deliberator status`, then `deliberator login <provider>`.
- **File not found**: confirm the target path(s) in the config exist relative to the current directory.
- **MCP extras missing**: `pip install "deliberator[mcp] @ git+https://github.com/Build-Fractal/deliberator.git"`
