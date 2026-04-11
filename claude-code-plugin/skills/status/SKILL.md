---
description: Show authentication status for all conversus model providers — which ones are logged in, which use env vars, which are not configured.
---

# Conversus Status

Check which model providers conversus can use right now. Run this when you're not sure if you're authenticated, or to diagnose "provider auth error" messages.

## Step 0: Check installation

```bash
conversus --version 2>/dev/null || echo "NOT_INSTALLED"
```

If `NOT_INSTALLED`, stop and tell the user to install:
```
pip install git+https://github.com/Build-Fractal/conversus-oss.git
```

## Step 1: Run status

```bash
conversus status
```

## Step 2: Display the output

Show the Rich-formatted table verbatim. It shows each provider with columns:
- **Provider name** — `anthropic`, `openai`, `claude-code`, `ollama`, `gemini`, etc.
- **Login state** — logged in / not configured
- **Credential type** — OAuth token / env var / not set
- **Token expiry** — for OAuth tokens

## Step 3: Help interpret the output

After showing the table, help the user understand it:

- **`mock`** always shows as ready — it needs no credentials
- **Providers with env vars** (e.g., `ANTHROPIC_API_KEY`) — ready to use, credentials loaded from environment
- **Providers with stored OAuth** — ready, credentials in `~/.conversus/auth.json`
- **"Not configured"** providers — need `/conversus:login <provider>` before use

If the user is running a command that needs a specific provider, remind them:
> You're about to run with `--provider anthropic`. Make sure it shows as logged in above, or run `/conversus:login anthropic` first.

## Auth resolution order

When conversus needs credentials for a provider, it checks:
1. Environment variable (e.g., `ANTHROPIC_API_KEY`)
2. Stored OAuth token in `~/.conversus/auth.json`
3. Error if neither is set

`mock` always works without credentials and is the safest choice for first-time testing.
