---
description: Set up deliberator runtime permissions for the current project. Run this ONCE per project so deliberations can dispatch parallel sub-agents without interactive approval prompts.
---

# Deliberator Init

Configure the current project so deliberator deliberations can run **unattended** — without stopping at every sub-agent dispatch to ask for permission. This is the one command every new project needs to run first.

## Why you need this

A `decide` run dispatches 5-10 sub-agents. A full 4-agent mechanism-design run dispatches 29. Without `init`, every single dispatch stops and waits for you to click Approve. `init` writes a runtime-specific settings file that pre-grants the permissions deliberator needs so the pipeline runs end-to-end.

## Step 0: Check installation

```bash
command -v deliberator >/dev/null 2>&1 || echo "NOT_INSTALLED"
```

If `NOT_INSTALLED`, stop and tell the user:
```
pip install git+https://github.com/Build-Fractal/deliberator.git
```

## Step 1: Parse arguments

Expected: `/deliberator:init [--runtime <runtime>] [--provider <provider>] [--model <model>] [--force]`

If no arguments given, assume defaults: `claude-code` runtime, no pre-set provider or model.

Runtimes available:
- `claude-code` (default) — writes `.claude/settings.json`
- `opencode` — writes `.opencode/config.toml`
- `copilot` — writes `.github/copilot-settings.json`
- `gemini` — writes `.gemini/settings.json`
- `codex` — writes `.codex/settings.json`
- `aider` — writes `.aider.conf.yml`

## Step 2: Check for existing settings

Before writing, check if the target file already exists:

```bash
ls -la .claude/settings.json 2>/dev/null
```

If it does and the user didn't pass `--force`, ask:
> A `.claude/settings.json` already exists. Overwrite it? (Pass `--force` to overwrite without asking.)

## Step 3: Run init

```bash
deliberator init [--runtime <runtime>] [--provider <provider>] [--model <model>] [--force]
```

Examples:
```bash
# Default — Claude Code, no provider preset
deliberator init

# Multiple runtimes at once
deliberator init --runtime claude-code --runtime opencode

# Pre-configure a default provider and model
deliberator init --provider anthropic --model claude-opus-4-20250514

# Overwrite existing settings
deliberator init --force
```

## Step 4: Confirm and show next steps

After success, tell the user:
> Done. `.claude/settings.json` (or the relevant runtime file) now has the permissions deliberator needs.
>
> Next steps:
> - Try a quick deliberation: `/deliberator:decide "your question here"`
> - Build a config: `/deliberator:design`
> - Or run an existing config: `/deliberator:run path/to/deliberator.yml`

If the user also needs provider auth, suggest:
> Run `/deliberator:status` to check which providers you're logged into, or `/deliberator:login anthropic` to authenticate.
