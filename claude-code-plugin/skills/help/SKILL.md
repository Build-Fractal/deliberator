---
description: List all available `/conversus:*` slash commands with one-line descriptions. Use this when you want to see what conversus capabilities are available without searching.
---

# Conversus Help

Discover what `/conversus:*` slash commands are available in this Claude Code session.

## What this skill does

Lists the available conversus slash commands with one-line descriptions, so users can pick the right command for their decision-making need without having to remember each command's exact syntax.

## Available commands

```
/conversus:decide   — Quick ad-hoc deliberation. Just give it a natural-language
                       question; conversus runs a built-in pragmatist + devil's
                       advocate against it.

/conversus:run      — Run a full deliberation from a config file. Use this for
                       reproducible deliberations with custom agents, modes, and
                       target documents.

/conversus:validate — Validate a conversus.yml config and estimate the LLM
                       launch cost before running. Useful before kicking off
                       a real (expensive) deliberation.

/conversus:design   — Guided config builder. Walks you through writing a
                       conversus.yml interactively — picks mode, agents,
                       targets, and writes the file.

/conversus:init     — Initialize a `.conversus/` directory in the current
                       project with runtime permissions and default settings.

/conversus:login    — Log in to a model provider via OAuth (Anthropic, OpenAI,
                       Google).

/conversus:logout   — Log out of a model provider.

/conversus:status   — Show authentication status for all configured providers
                       and the effective settings cascade.
```

## Picking the right command

| Situation | Command |
|---|---|
| You have a question and want a quick answer | `/conversus:decide` |
| You have a config file you want to run | `/conversus:run` |
| You want to know how much a config will cost | `/conversus:validate` |
| You want to build a config interactively | `/conversus:design` |
| First time using conversus in a project | `/conversus:init` |
| Auth issue or want to check setup | `/conversus:status` |

## Equivalent CLI commands

The same capabilities are available from the terminal — the `/conversus:*` slash commands wrap the CLI:

| Slash command | CLI equivalent |
|---|---|
| `/conversus:decide "..."` | `conversus decide "..."` |
| `/conversus:run config.yml` | `conversus run config.yml` |
| `/conversus:validate config.yml` | `conversus validate config.yml` |
| `/conversus:status` | `conversus status` |
| `/conversus:init` | `conversus init` |

The CLI also has `conversus skills` (lists all available skills) and `conversus skill <name>` (prints the guided workflow for a specific skill) — useful when you want to see the same guided content from the terminal that the slash commands provide in Claude Code.

## Cross-refs

- Spec 059 §2.3 — skill discovery for Claude Code / Cowork (Phase 3 meta-skill)
- `/conversus:design` — the next-most-discoverable command for new users
- `claude-code-plugin/skills/` — the source of truth for all skill content
