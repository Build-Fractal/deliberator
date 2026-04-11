---
description: Set up conversus runtime permissions for the current project. Run this ONCE per project so deliberations can dispatch parallel sub-agents without interactive approval prompts.
---

# Conversus Init

Configure the current project so conversus deliberations can run **unattended** — without stopping at every sub-agent dispatch to ask for permission. This is the one command every new project needs to run first.

## Why you need this

A `decide` run dispatches 5-10 sub-agents. A full 4-agent mechanism-design run dispatches 29. Without `init`, every single dispatch stops and waits for you to click Approve. `init` writes a runtime-specific settings file that pre-grants the permissions conversus needs so the pipeline runs end-to-end.

## Step 0: Check installation

```bash
conversus --version 2>/dev/null || echo "NOT_INSTALLED"
```

If `NOT_INSTALLED`, stop and tell the user:
```
pip install git+https://github.com/Build-Fractal/conversus-oss.git
```

## Step 1: Parse arguments

Expected: `/conversus:init [--runtime <runtime>] [--provider <provider>] [--model <model>] [--force]`

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
conversus init [--runtime <runtime>] [--provider <provider>] [--model <model>] [--force]
```

Examples:
```bash
# Default — Claude Code, no provider preset
conversus init

# Multiple runtimes at once
conversus init --runtime claude-code --runtime opencode

# Pre-configure a default provider and model
conversus init --provider anthropic --model claude-opus-4-20250514

# Overwrite existing settings
conversus init --force
```

## Step 4: Confirm and show next steps

After success, tell the user:
> Done. `.claude/settings.json` (or the relevant runtime file) now has the permissions conversus needs.
>
> Next steps:
> - Try a quick deliberation: `/conversus:decide "your question here"`
> - Build a config: `/conversus:design`
> - Or run an existing config: `/conversus:run path/to/conversus.yml`

If the user also needs provider auth, suggest:
> Run `/conversus:status` to check which providers you're logged into, or `/conversus:login anthropic` to authenticate.
