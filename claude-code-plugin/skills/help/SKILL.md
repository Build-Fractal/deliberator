---
description: List all available `/deliberator:*` slash commands with one-line descriptions. Use this when you want to see what deliberator capabilities are available without searching.
---

# Deliberator Help

Discover what `/deliberator:*` slash commands are available in this Claude Code session.

## What this skill does

Lists the available deliberator slash commands with one-line descriptions, so users can pick the right command for their decision-making need without having to remember each command's exact syntax.

## Available commands

```
/deliberator:decide   — Quick ad-hoc deliberation. Just give it a natural-language
                       question; deliberator runs a built-in pragmatist + devil's
                       advocate against it.

/deliberator:run      — Run a full deliberation from a config file. Use this for
                       reproducible deliberations with custom agents, modes, and
                       target documents.

/deliberator:validate — Validate a deliberator.yml config and estimate the LLM
                       launch cost before running. Useful before kicking off
                       a real (expensive) deliberation.

/deliberator:design   — Guided config builder. Walks you through writing a
                       deliberator.yml interactively — picks mode, agents,
                       targets, and writes the file.

/deliberator:init     — Initialize a `.deliberator/` directory in the current
                       project with runtime permissions and default settings.

/deliberator:login    — Log in to a model provider via OAuth (Anthropic, OpenAI,
                       Google).

/deliberator:logout   — Log out of a model provider.

/deliberator:status   — Show authentication status for all configured providers
                       and the effective settings cascade.
```

## Picking the right command

| Situation | Command |
|---|---|
| You have a question and want a quick answer | `/deliberator:decide` |
| You have a config file you want to run | `/deliberator:run` |
| You want to know how much a config will cost | `/deliberator:validate` |
| You want to build a config interactively | `/deliberator:design` |
| First time using deliberator in a project | `/deliberator:init` |
| Auth issue or want to check setup | `/deliberator:status` |

## Equivalent CLI commands

The same capabilities are available from the terminal — the `/deliberator:*` slash commands wrap the CLI:

| Slash command | CLI equivalent |
|---|---|
| `/deliberator:decide "..."` | `deliberator decide "..."` |
| `/deliberator:run config.yml` | `deliberator run config.yml` |
| `/deliberator:validate config.yml` | `deliberator validate config.yml` |
| `/deliberator:status` | `deliberator status` |
| `/deliberator:init` | `deliberator init` |

The CLI also has `deliberator skills` (lists all available skills) and `deliberator skill <name>` (prints the guided workflow for a specific skill) — useful when you want to see the same guided content from the terminal that the slash commands provide in Claude Code.

## Cross-refs

- Spec 059 §2.3 — skill discovery for Claude Code / Cowork (Phase 3 meta-skill)
- `/deliberator:design` — the next-most-discoverable command for new users
- `claude-code-plugin/skills/` — the source of truth for all skill content
