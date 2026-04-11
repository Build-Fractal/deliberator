---
description: Run a full conversus deliberation from a conversus.yml config file. Use this for reproducible deliberations with custom agents, modes, and target documents.
---

# Conversus Run

Run a full deliberation from a config file. Use `/conversus:decide` for ad-hoc questions; use this for reproducible, custom-agent deliberations.

## Step 0: Check installation

```bash
conversus --version 2>/dev/null || echo "NOT_INSTALLED"
```

If `NOT_INSTALLED`, stop and tell the user:
```
pip install git+https://github.com/Build-Fractal/conversus-oss.git
```

## Step 1: Parse arguments

Expected: `/conversus:run <config.yml> [--provider <provider>] [--model <model>] [--rounds <n>] [--phase <phase>]`

If no config path given, ask:
> Which config file? (e.g., `deliberations/my-review/conversus.yml`)

If the path doesn't exist, verify with `ls -la <path>` and ask for the correct one.

## Step 2: Validate first (recommended)

Before running, check the config is valid and estimate cost:

```bash
conversus validate <config_path>
```

This prints the mode, agent count, iterations, and total LLM launches. Show the output to the user. If the launch count looks surprisingly high (>30), ask:
> This run will use N LLM launches. Is that expected, or want to reduce iterations/agents?

## Step 3: Run

```bash
conversus run <config_path> --provider <provider> [--model <model>] [--rounds <n>] [--phase <phase>]
```

Providers: `mock` (default), `anthropic`, `openai`, `claude-code`, `ollama`, `gemini`, `codex`, `copilot`, `aider`, `opencode`.

Phases: `all` (default) runs the full pipeline, `review` runs only the first phase for spot-checking.

Examples:
```bash
# Full run with Claude Code
conversus run deliberations/auth-review/conversus.yml --provider claude-code

# Mock dry-run to see pipeline shape
conversus run deliberations/auth-review/conversus.yml --provider mock

# Just the review phase (fast spot-check)
conversus run deliberations/auth-review/conversus.yml --provider anthropic --phase review
```

## Step 4: Display results

Show the CLI's progress output (phase checkmarks, agent dispatches, timings). After completion:

1. Show the paths to output files that were written
2. If `summary/final.md` exists, read it and summarize the verdict for the user
3. If any phase failed, show the error and suggest fixes

## Common errors

- **Config validation error**: `conversus validate` will give a specific message. Typically missing `mode`, `agents`, or `target` fields.
- **Provider auth error**: run `conversus status`, then `conversus login <provider>`.
- **File not found**: confirm the target path(s) in the config exist relative to the current directory.
- **MCP extras missing**: `pip install "conversus[mcp] @ git+https://github.com/Build-Fractal/conversus-oss.git"`
