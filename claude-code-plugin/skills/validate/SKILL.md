---
description: Validate a conversus.yml config file and show the estimated LLM launch count before committing to a real run.
---

# Conversus Validate

Check a conversus.yml config for syntax errors and estimate the cost (total LLM launches) before running.

## Step 0: Check installation

```bash
command -v conversus >/dev/null 2>&1 || echo "NOT_INSTALLED"
```

If `NOT_INSTALLED`, stop and tell the user:
```
pip install git+https://github.com/Build-Fractal/conversus-oss.git
```

## Step 1: Parse arguments

Expected: `/conversus:validate <config.yml>`

If no config path given, ask:
> Which config should I validate?

## Step 2: Run validation

```bash
conversus validate <config_path>
```

## Step 3: Interpret the output

The command prints:
- **Mode** (cooperative, red-blue, mechanism-design, etc.)
- **Agent count**
- **Iterations**
- **Arbiter** (yes/no)
- **Per-phase launch breakdown** (review, cross-review, revision, disputes, synthesis, arbitration)
- **Total LLM launches**

Show the output verbatim to the user. Then interpret:
- **Under 15 launches**: cheap, safe to run
- **15-30 launches**: moderate cost, worth a mock dry-run first
- **30+ launches**: expensive, confirm with user before a real run
- **50+ launches**: very expensive, suggest reducing iterations or agent count unless the user is confident

## Step 4: Suggest next steps

If validation passes, tell the user:
> Config is valid. Next steps:
> - Dry-run with mock provider (free): `conversus run <config> --provider mock`
> - Real run: `conversus run <config> --provider claude-code`

Note on provider selection for the real run: if the user is on Anthropic OAuth (Claude Max / subscription) without `ANTHROPIC_API_KEY` set, the default `anthropic` provider 429s on a server-side concurrency policy gate. Use `--provider claude-code` to route through the OAuth-friendly subprocess path. The `/conversus:run` skill applies this preflight automatically; mirror that behavior if you launch the run directly here.

If validation fails, show the specific error and suggest the fix. Common errors:
- **"mode: required"** — add a `mode:` field at the top level
- **"agents: required"** — add an `agents:` list
- **"target: file not found"** — check the path is relative to the config file's location
- **"unknown mode: X"** — list the 8 valid modes
