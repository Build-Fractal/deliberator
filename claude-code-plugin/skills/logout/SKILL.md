---
description: Remove stored OAuth credentials for a deliberator model provider. Use this when rotating credentials or switching accounts.
---

# Deliberator Logout

Remove stored OAuth credentials for a provider. Use this when:
- You want to switch to a different account for the same provider
- You're rotating credentials
- You're on a shared machine and want to clear your session

## Step 0: Check installation

```bash
command -v deliberator >/dev/null 2>&1 || echo "NOT_INSTALLED"
```

If `NOT_INSTALLED`, stop and tell the user to install:
```
pip install git+https://github.com/Build-Fractal/deliberator.git
```

## Step 1: Parse arguments

Expected: `/deliberator:logout <provider>`

If no provider given, first run `deliberator status` to show which providers are logged in, then ask:
> Which provider do you want to log out of? You're currently logged into: <list from status>

## Step 2: Confirm

Before logging out, confirm:
> This will remove the stored OAuth token for `<provider>` from `~/.deliberator/auth.json`. You'll need to run `/deliberator:login <provider>` again (or set the env var) to use this provider after logging out.
>
> Continue? (yes/no)

Wait for explicit confirmation before running the command.

## Step 3: Run logout

```bash
deliberator logout <provider>
```

## Step 4: Verify

After logout, run status to confirm:

```bash
deliberator status
```

Show the table to the user and confirm the provider now shows as "not configured" (unless they also have an environment variable for it, in which case that takes over).

## Note on environment variables

If the user has `ANTHROPIC_API_KEY` (or equivalent) set in their environment, `deliberator logout anthropic` only removes the OAuth token — the env var is still active and deliberator will use it. To fully disconnect, tell them to also `unset` the env var in their shell.
