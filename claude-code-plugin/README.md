# Deliberator — Claude Code / Cowork Plugin

A plugin for **Claude Code** and **Cowork** that adds a `/deliberator` command for running competitive multi-agent deliberation directly from your editor or desktop agent.

## Install

The `deliberator` repo IS its own plugin marketplace. Two steps:

```shell
/plugin marketplace add Build-Fractal/deliberator
/plugin install deliberator@deliberator
```

After install, try:

```shell
/deliberator:design                         # guided config wizard
/deliberator:decide "Postgres or MongoDB?"  # ad-hoc deliberation
```

## Prerequisites

The plugin wraps the deliberator CLI, so you need the Python package installed too:

```bash
pip install git+https://github.com/Build-Fractal/deliberator.git
```

The plugin will prompt you with the install command if it can't find `deliberator` on your PATH.

## What you get

Eight slash commands, each namespaced with `deliberator:` to avoid conflicts with other plugins:

### Core deliberation

| Command | What it does |
|---|---|
| `/deliberator:design` | **Guided config builder** — walks you through creating a `deliberator.yml` interactively. No YAML knowledge needed. |
| `/deliberator:decide` | Ad-hoc deliberation on a natural-language question (no config file needed) |
| `/deliberator:run` | Run a full deliberation from a config file |
| `/deliberator:validate` | Validate a config and show cost estimate before running |

### Setup and auth

| Command | What it does |
|---|---|
| `/deliberator:init` | **Run this once per project** — sets up runtime permissions so deliberations can dispatch sub-agents without interactive approval prompts |
| `/deliberator:status` | Show authentication status for all model providers |
| `/deliberator:login` | Authenticate with a provider via OAuth (anthropic, openai, …) |
| `/deliberator:logout` | Remove stored credentials for a provider |

The `deliberator mcp` subcommand (MCP server) is not exposed as a slash command because it's a stdio server invoked by editors, not by users.

## Providers

`anthropic`, `openai`, `claude-code`, `ollama`, `gemini`, `codex`, `copilot`, `aider`, `opencode`, and `mock` (no API key, for testing).

## Example — first-time user flow

```shell
# 1. One-time project setup (grants runtime permissions)
/deliberator:init

# 2. Check which providers you're logged into
/deliberator:status

# 3. Log in if needed
/deliberator:login anthropic

# 4. Start with the guided flow — no YAML needed
/deliberator:design

# Or ask a question directly
/deliberator:decide "Should we split the auth service out of the monolith?" --provider claude-code

# Or run a prebuilt config (after validating cost)
/deliberator:validate deliberations/my-review/deliberator.yml
/deliberator:run deliberations/my-review/deliberator.yml --provider claude-code
```

## Links

- [Full documentation](https://github.com/Build-Fractal/deliberator)
- [Building a config guide](https://github.com/Build-Fractal/deliberator/blob/main/docs/user-guide/building-a-config.md)
- [Example configs](https://github.com/Build-Fractal/deliberator/tree/main/deliberations)
