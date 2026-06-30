---
description: Authenticate with a deliberator model provider via OAuth. Walks through browser-based login for Anthropic, OpenAI, or other OAuth-capable providers.
---

# Deliberator Login

Authenticate with a model provider so deliberator can use it. Supports OAuth PKCE for providers that offer it (Anthropic, OpenAI, others).

## Step 0: Check installation

```bash
command -v deliberator >/dev/null 2>&1 || echo "NOT_INSTALLED"
```

If `NOT_INSTALLED`, stop and tell the user to install:
```
pip install git+https://github.com/Build-Fractal/deliberator.git
```

## Step 1: Parse arguments

Expected: `/deliberator:login <provider>`

Providers that support OAuth login:
- `anthropic` — opens `claude.ai/oauth/authorize`, paste `code#state` back into terminal
- `openai` — opens `auth.openai.com/authorize`, uses localhost callback

If no provider given, ask:
> Which provider do you want to log in to? Options: `anthropic`, `openai`.

If the provider uses API keys instead of OAuth (e.g., `gemini`, `ollama`), tell the user:
> `<provider>` uses an environment variable, not OAuth. Set `<PROVIDER_API_KEY>` in your environment instead, then run `/deliberator:status` to verify.

## Step 2: Warn about the interactive flow

**Important**: `deliberator login` requires interactive input. The browser-based OAuth flow opens a URL, the user authenticates in the browser, and the CLI prompts for an authorization code to paste back.

This means:
- The plugin CANNOT complete the login on the user's behalf — they must be at the terminal to paste the code
- If running from inside Claude Code, the user needs a real terminal session

Tell the user:
> The login command needs to run in your terminal — I can't paste the OAuth code for you. Open a terminal in this project directory and run:
> ```
> deliberator login <provider>
> ```
> Then come back here when you're done.

## Step 3: Alternative — environment variable

Mention the faster path for API-key providers:

> If you already have an `ANTHROPIC_API_KEY` (or equivalent) as an environment variable, you don't need to log in at all — deliberator picks it up automatically. Run `/deliberator:status` to confirm.

## After login

Once the user completes login in their terminal, have them run `/deliberator:status` to verify the credentials are stored, then `/deliberator:decide` or `/deliberator:run` to use the provider.
