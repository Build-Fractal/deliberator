# CLI Reference

The `deliberator` CLI has 12 commands. Entry point: `pyproject.toml` wires `deliberator = "engine.cli:cli"`.

| Command | One-line purpose |
|---|---|
| `run` | Run a full deliberation from a YAML config |
| `decide` | Ad-hoc deliberation on a natural-language question (no config needed) |
| `validate` | Dry-run a config: parse, validate, print cost estimate |
| `init` | Initialize `.deliberator/` settings + runtime permissions in the current project |
| `mcp` | Start the deliberator MCP server (stdio transport) |
| `login` | OAuth login to a model provider (`anthropic` / `openai`) |
| `logout` | Remove stored credentials for a provider |
| `status` | Show auth status for all providers + effective settings cascade |
| `context` | Print detected invocation context (runtime / provider / model) |
| `skills` | List all deliberator skills with summaries |
| `skill` | Print the SKILL.md guided workflow for a named capability |
| `snap` | Snap-verdict deliberation for Claude Code PreToolUse hooks |

!!! note "Running commands"
    If you installed via `uv sync` (recommended), prefix commands with `uv run`: e.g., `uv run deliberator run config.yml`. If you installed via `pip install -e .`, use `deliberator` directly.

!!! warning "Provider defaults differ by surface"
    The provider default depends on how you run deliberator:

    - **Config file** (`provider:` field): defaults to `anthropic`
    - **CLI** (`--provider` flag): defaults to `mock`
    - **SDK** (`provider=` parameter): defaults to `mock`

    The CLI `--provider` flag does **not** read the config file's `provider` field -- it always applies its own default. Set `--provider` explicitly when your config specifies a different provider.

### Default models per provider

| Provider | Default model |
|----------|---------------|
| `mock` | `mock-default` (synthetic responses, no API key) |
| `anthropic` | `claude-sonnet-4-20250514` |
| `openai` | `gpt-4o` |

Pass `--model <id>` to override.

## `deliberator run <config.yml>`

Run a full deliberation from a YAML config file.

```bash
# Default mock provider (no API key)
deliberator run path/to/deliberator.yml

# With Anthropic
deliberator run path/to/deliberator.yml --provider anthropic

# Override model
deliberator run path/to/deliberator.yml --provider anthropic --model claude-opus-4-20250514

# Override round count
deliberator run path/to/deliberator.yml --provider anthropic --rounds 3
```

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--provider` | `mock` | One of: `mock` (alias `demo`), `anthropic`, `claude-code`, `claude-desktop`, `aider`, `opencode`, `codex`, `gemini`, `copilot`, `pi`, `ollama`, `llama-cpp`, `vllm`. See the [Providers](https://github.com/Build-Fractal/deliberator#providers) table for install + auth per provider. |
| `--model` | provider default | Override LLM model identifier |
| `--rounds` | config value | Override deliberation rounds |
| `--phase` | `all` | Phase to run (`all` or `review`) |

**Output:** Prints paths to all written files. Files go to the `output` directory specified in the config.

**`--phase review`:** Runs only Phase 1 (initial reviews) and stops. This produces `review.md` files for each agent but skips cross-reviews, revisions, disputes, and synthesis. Useful for quick spot-checks when you want to see agent perspectives without running the full pipeline.

## `deliberator decide <question>`

Run an ad-hoc deliberation on a natural-language question. Generates a temp config with pragmatist + devil's advocate presets, runs the full pipeline, and prints structured results.

```bash
# Quick deliberation
deliberator decide "Should we use Postgres or MongoDB?" --provider anthropic

# Different mode
deliberator decide "Build vs buy?" --provider openai --mode red-blue

# JSON output (for piping)
deliberator decide "Monorepo or polyrepo?" --provider anthropic --format json

# Save output to a directory
deliberator decide "Redis vs Memcached?" --provider anthropic --output ./cache-decision/
```

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--provider` | `mock` | One of: `mock` (alias `demo`), `anthropic`, `claude-code`, `claude-desktop`, `aider`, `opencode`, `codex`, `gemini`, `copilot`, `pi`, `ollama`, `llama-cpp`, `vllm`. See the [Providers](https://github.com/Build-Fractal/deliberator#providers) table for install + auth per provider. |
| `--mode` | `cooperative` | `cooperative`, `winner-take-all`, `prisoners-dilemma`, `red-blue` |
| `--output` | temp dir | Output directory (cleaned up if not specified) |
| `--format` | `rich` | `rich` (terminal) or `json` |

**Question gate:** The CLI runs a question classifier before execution. Insufficient questions get a warning but are not blocked.

**Note:** The `decide` command supports 4 modes (`cooperative`, `winner-take-all`, `prisoners-dilemma`, `red-blue`) for quick ad-hoc deliberation. The full set of 8 deliberation modes (including `negotiation`, `resource-allocation`, `fair-division`, and `mechanism-design`) is available when using a config file with `deliberator run`. See [Deliberation Modes](modes.md) for details on all 8 modes.

## `deliberator validate <config.yml>`

Dry-run a config: parse, validate, and print a cost estimate without running any LLM calls.

```bash
deliberator validate path/to/deliberator.yml

# Also classify a question
deliberator validate path/to/deliberator.yml --question "Is this clear enough?"
```

**Output:**

```
Config valid: path/to/deliberator.yml
Mode: cooperative

Cost estimate: 9 total LLM launches
  Agents: 2
  Iterations: 1
  Arbiter: no

  Per-phase breakdown:
    review: 2
    cross_review: 2
    revision: 2
    disputes: 2
    synthesis: 1
```

## `deliberator login <provider>`

Authenticate with a model provider via OAuth PKCE.

```bash
deliberator login anthropic    # Opens browser, paste code#state
deliberator login openai       # Opens browser, localhost callback
```

Credentials are stored in `~/.deliberator/auth.json` with `chmod 600` permissions.

**Anthropic flow:** Opens `claude.ai/oauth/authorize`, shows a code on `platform.claude.com`, you paste `code#state` into the terminal.

**OpenAI flow:** Opens `auth.openai.com/authorize`, redirects to a localhost callback server.

## `deliberator logout <provider>`

Remove stored credentials for a provider.

```bash
deliberator logout anthropic
deliberator logout openai
```

## `deliberator status`

Show authentication status for all providers.

```bash
deliberator status
```

**Output:** Rich table showing each provider's login state, credential type (OAuth token, env var, or not configured), and token expiry.

## `deliberator mcp`

Start the Deliberator MCP server using stdio transport. This exposes deliberator deliberation tools to MCP-compatible editors such as Claude Code, Cursor, and Windsurf.

```bash
deliberator mcp
```

**Tools exposed:**

| Tool | Description |
|------|-------------|
| `deliberator_validate` | Validate a YAML config and estimate cost |
| `deliberator_run` | Validate config and run a deliberation |
| `deliberator_decide` | Run an ad-hoc deliberation on a question |

**Registration with Claude Code:**

```bash
claude mcp add deliberator -- deliberator mcp
```

Requires the MCP extras: `pip install "deliberator[mcp] @ git+https://github.com/Build-Fractal/deliberator.git"`

## `deliberator init`

Configure the current project so deliberator agents can run **without permission prompts**. Deliberator dispatches parallel sub-agents through your chosen runtime — `init` writes the settings file each runtime needs to auto-approve those dispatches so deliberations run end-to-end unattended.

```bash
deliberator init                                           # Default: claude-code
deliberator init --runtime opencode                        # Configure opencode
deliberator init --runtime claude-code --runtime gemini    # Multiple runtimes
deliberator init --provider anthropic --model opus         # Pre-set defaults
deliberator init --force                                   # Overwrite existing
```

### What it creates

Each runtime gets its own settings file with auto-approval granted for the tools deliberator needs (Agent dispatch, file I/O, Bash for sub-process invocation):

| Runtime | File written | Purpose |
|---------|-------------|---------|
| `claude-code` | `.claude/settings.json` | Permission grants for Agent, Read, Write, Bash |
| `opencode` | `.opencode/config.toml` | `auto_approve` for tool use |
| `copilot` | `.github/copilot-settings.json` | Copilot agent permissions |
| `gemini` | `.gemini/settings.json` | Gemini CLI tool permissions |
| `codex` | `.codex/settings.json` | Codex tool grants |
| `aider` | `.aider.conf.yml` | `yes-always`, `no-auto-commits` |

### Why you need it

Without `init`, deliberator deliberations stop at every agent dispatch waiting for interactive approval. In a 29-launch pipeline (review → cross-review → revision → disputes → synthesis), that's 29 interruptions. `init` grants the tool permissions once so the pipeline runs unattended.

**Run it once per project.** You can re-run with `--force` to update settings later.

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--runtime` | `claude-code` | Runtimes to configure (repeatable) |
| `--provider` | none | Pre-configure a default execution provider |
| `--model` | none | Pre-configure a default model identifier |
| `--force` | `false` | Overwrite existing settings files |

## `deliberator context`

Print the detected invocation context and exit. Useful for debugging which runtime, provider, and model deliberator is detecting from your environment.

```bash
deliberator context
```

## Auth resolution order

When you specify `--provider anthropic`, the engine resolves credentials in this order:

1. `ANTHROPIC_API_KEY` environment variable
2. Stored OAuth token from `~/.deliberator/auth.json`
3. Error with instructions to set env var or run `deliberator login`

The `mock` provider always works without credentials.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Config error, provider error, or pipeline failure |
