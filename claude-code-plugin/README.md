# Conversus — Claude Code / Cowork Plugin

A plugin for **Claude Code** and **Cowork** that adds a `/conversus` command for running competitive multi-agent deliberation directly from your editor or desktop agent.

## Install

The `conversus-oss` repo IS its own plugin marketplace. Two steps:

```shell
/plugin marketplace add Build-Fractal/conversus-oss
/plugin install conversus@conversus
```

After install, try:

```shell
/conversus:design                         # guided config wizard
/conversus:decide "Postgres or MongoDB?"  # ad-hoc deliberation
```

## Prerequisites

The plugin wraps the conversus CLI, so you need the Python package installed too:

```bash
pip install git+https://github.com/Build-Fractal/conversus-oss.git
```

The plugin will prompt you with the install command if it can't find `conversus` on your PATH.

## What you get

Eight slash commands, each namespaced with `conversus:` to avoid conflicts with other plugins:

### Core deliberation

| Command | What it does |
|---|---|
| `/conversus:design` | **Guided config builder** — walks you through creating a `conversus.yml` interactively. No YAML knowledge needed. |
| `/conversus:decide` | Ad-hoc deliberation on a natural-language question (no config file needed) |
| `/conversus:run` | Run a full deliberation from a config file |
| `/conversus:validate` | Validate a config and show cost estimate before running |

### Setup and auth

| Command | What it does |
|---|---|
| `/conversus:init` | **Run this once per project** — sets up runtime permissions so deliberations can dispatch sub-agents without interactive approval prompts |
| `/conversus:status` | Show authentication status for all model providers |
| `/conversus:login` | Authenticate with a provider via OAuth (anthropic, openai, …) |
| `/conversus:logout` | Remove stored credentials for a provider |

The `conversus mcp` subcommand (MCP server) is not exposed as a slash command because it's a stdio server invoked by editors, not by users.

## Providers

`anthropic`, `openai`, `claude-code`, `ollama`, `gemini`, `codex`, `copilot`, `aider`, `opencode`, and `mock` (no API key, for testing).

## Example — first-time user flow

```shell
# 1. One-time project setup (grants runtime permissions)
/conversus:init

# 2. Check which providers you're logged into
/conversus:status

# 3. Log in if needed
/conversus:login anthropic

# 4. Start with the guided flow — no YAML needed
/conversus:design

# Or ask a question directly
/conversus:decide "Should we split the auth service out of the monolith?" --provider claude-code

# Or run a prebuilt config (after validating cost)
/conversus:validate deliberations/my-review/conversus.yml
/conversus:run deliberations/my-review/conversus.yml --provider claude-code
```

## Links

- [Full documentation](https://github.com/Build-Fractal/conversus-oss)
- [Building a config guide](https://github.com/Build-Fractal/conversus-oss/blob/main/docs/user-guide/building-a-config.md)
- [Example configs](https://github.com/Build-Fractal/conversus-oss/tree/main/deliberations)
