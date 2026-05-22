# Quickstart

## Prerequisites

- **Python 3.12+** -- check with `python --version`

## Install

```bash
pip install git+https://github.com/Build-Fractal/conversus-oss.git
```

This installs the engine with all 8 deliberation modes, templates, presets, CLI, and MCP server.

For local development:

```bash
git clone https://github.com/Build-Fractal/conversus-oss.git && cd conversus
pip install -e .          # editable install
# or: uv sync            # if using uv
```

!!! note "Running commands"
    Examples below use the bare `conversus` command (matches the `pip install` path). If you installed via `uv sync`, prefix every command with `uv run`: e.g., `uv run conversus decide ...`.

## First deliberation

```bash
conversus decide "Should we use Redis or Postgres for caching?" --provider mock
```

The `--provider mock` flag uses a built-in mock provider that returns synthetic responses -- no API key needed. This lets you explore the full pipeline without spending anything.

## What just happened

Conversus ran a 5-phase deliberation:

1. **Review** -- Two agents (pragmatist + devil's advocate) each reviewed your question from their perspective.
2. **Cross-review** -- Each agent critiqued the other's position, looking for weak arguments and missed angles.
3. **Revision** -- Each agent revised their position based on the cross-review feedback.
4. **Disputes** -- Each agent stated their final position on remaining disagreements.
5. **Synthesis** -- A synthesizer agent merged all positions into a verdict with convergence points and surviving disputes.

You will see five phase headers -- Review, Cross-review, Revision, Disputes, Synthesis -- followed by a headline verdict and a summary. The output includes:

- **Headline** -- One-sentence verdict.
- **Summary** -- Agent count, phases completed, convergence/dispute counts.
- **Full analysis** -- The complete synthesis markdown.
- **Quality indicators** -- Structured metrics from the deliberation.

Run with `--format json` to verify the phase structure programmatically:

```bash
conversus decide "Should we use Redis or Postgres for caching?" --provider mock --format json
```

## Try with a real provider

```bash
# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Or log in via OAuth
conversus login anthropic

# Run with real LLM agents
conversus decide "Should we use Redis or Postgres for caching?" --provider anthropic
```

Verify your provider credentials at any time:

```bash
conversus status
```

## Try the Guided Workflow (in Your AI Editor)

The `/conversus` commands below are **slash commands typed inside an AI assistant** (such as Claude Code, Cursor, or another MCP-compatible editor). They are not terminal commands -- do not run them in your shell.

The guided workflow walks you through problem definition, interest discovery, mode selection, and execution:

```
/conversus define "We need to decide between Redis and Postgres for our metadata cache"
/conversus interests
/conversus mode
/conversus converge
```

See [Guided Workflow](guided-workflow.md) for the full walkthrough.

## Try a config file

For repeatable deliberations, write a `conversus.yml`:

```yaml
mode: cooperative
target: docs/architecture.md
output: docs/architecture-review/

agents:
  - name: pragmatist
    preset: pragmatist
  - name: devils-advocate
    preset: devils-advocate
```

```bash
conversus run conversus.yml --provider anthropic
```

See [Config Reference](config-reference.md) for the full schema.

## Next steps

- **Explore:** Read [Deliberation Modes](modes.md) to understand the 8 competition modes and when to use each one.
- **Build:** Read the [Developer Guide](../developer-guide/architecture.md) to create your own plugins and domains.
