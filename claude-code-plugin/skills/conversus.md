---
name: conversus
description: >-
  Run competitive multi-agent deliberation using the conversus CLI.
  Supports: run (full deliberation from config), decide (ad-hoc question),
  validate (check config + cost estimate), init (project setup),
  status (provider auth), login/logout (provider credentials).
allowed-tools: Bash
---

## Usage

`/conversus <subcommand> [args]`

| Invocation | Action |
|---|---|
| `/conversus run config.yml` | Run full deliberation from a config file |
| `/conversus run config.yml --provider anthropic` | Run with a specific provider |
| `/conversus decide "Should we use Postgres or MongoDB?"` | Ad-hoc deliberation on a question |
| `/conversus decide "question" --mode red-blue --provider openai` | Ad-hoc with mode + provider |
| `/conversus validate config.yml` | Validate config and show cost estimate |
| `/conversus init` | Initialize project with runtime permissions |
| `/conversus status` | Show provider authentication status |
| `/conversus login anthropic` | Log in to a provider |
| `/conversus logout anthropic` | Log out of a provider |
| `/conversus` (no args) | Show help |

## Step 1: Check installation

Run this first:

```bash
conversus --version 2>/dev/null || echo "NOT_INSTALLED"
```

If the output is `NOT_INSTALLED`, tell the user:

> conversus is not installed. Install it with:
> ```
> pip install conversus
> ```
> Then re-run your command.

Stop here if not installed.

## Step 2: Dispatch

Parse the user's arguments after `/conversus`. The first word is the subcommand.

If no arguments were given, run:
```bash
conversus --help
```
and display the output.

### run

```bash
conversus run <config_path> [--provider <provider>] [--model <model>] [--rounds <n>] [--phase <phase>]
```

Providers: `mock` (default), `anthropic`, `openai`, `claude-code`, `ollama`, `gemini`, and others.

Example:
```bash
conversus run conversus.yml --provider anthropic
```

After running, display the output paths written and any synthesis summary if present.

### decide

```bash
conversus decide "<question>" [--provider <provider>] [--mode <mode>] [--format <rich|json>]
```

Modes: `cooperative` (default), `winner-take-all`, `prisoners-dilemma`, `red-blue`.

Example:
```bash
conversus decide "Build vs buy for our auth system?" --provider anthropic --mode cooperative
```

Display the structured result output from the CLI.

### validate

```bash
conversus validate <config_path> [--question "<question>"]
```

Example:
```bash
conversus validate conversus.yml
```

Display the validation result and cost estimate.

### init

```bash
conversus init [--runtime <runtime>] [--provider <provider>] [--model <model>] [--force]
```

Runtimes: `claude-code` (default), `opencode`, `copilot`, `gemini`, `codex`, `aider`.

Example:
```bash
conversus init --runtime claude-code
```

### status / login / logout

```bash
conversus status
conversus login <provider>
conversus logout <provider>
```

## Step 3: Display results

- Show CLI output verbatim, preserving any Rich-formatted tables or progress output.
- If the command exits non-zero, display the error message and suggest fixes:
  - Config errors: check YAML syntax, required fields (`mode`, `agents`, `target`).
  - Provider errors: run `conversus status` to check auth, or `conversus login <provider>`.
  - File not found: confirm the config path is correct relative to the current directory.

## Unknown subcommand

If the first argument doesn't match a known subcommand (`run`, `decide`, `validate`, `init`, `status`, `login`, `logout`, `context`), say:

> Unknown subcommand: '<arg>'. Available: run, decide, validate, init, status, login, logout, context.
