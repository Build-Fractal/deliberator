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

| Command | What it does |
|---|---|
| `/conversus:design` | **Guided config builder** — walks you through creating a `conversus.yml` interactively. No YAML knowledge needed. |
| `/conversus:run <config>` | Run a full deliberation from a config file |
| `/conversus:decide "<question>"` | Ad-hoc deliberation on a natural-language question |
| `/conversus:validate <config>` | Validate a config and show cost estimate |
| `/conversus:init` | Set up runtime permissions for this project |
| `/conversus:status` | Show provider authentication status |
| `/conversus:login <provider>` | Authenticate with a model provider |

All commands are namespaced with `conversus:` to avoid conflicts with other plugins.

## Providers

`anthropic`, `openai`, `claude-code`, `ollama`, `gemini`, `codex`, `copilot`, `aider`, `opencode`, and `mock` (no API key, for testing).

## Example

```shell
# Start with the guided flow
/conversus:design

# Or ask a question directly
/conversus:decide "Should we split the auth service out of the monolith?" --provider claude-code

# Or run a prebuilt config
/conversus:run deliberations/my-review/conversus.yml --provider claude-code
```

## Links

- [Full documentation](https://github.com/Build-Fractal/conversus-oss)
- [Building a config guide](https://github.com/Build-Fractal/conversus-oss/blob/main/docs/user-guide/building-a-config.md)
- [Example configs](https://github.com/Build-Fractal/conversus-oss/tree/main/deliberations)
