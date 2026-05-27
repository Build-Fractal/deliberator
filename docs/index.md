---
hide:
  - navigation
---

# Conversus

Competitive multi-agent deliberation framework. Multiple AI agents with different perspectives compete under game-theory-informed rules to surface the strongest arguments, expose hidden contradictions, and produce battle-tested decisions.

[![Tests](https://img.shields.io/badge/tests-1%2C302%20passed-brightgreen)](https://github.com/Build-Fractal/conversus-oss)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](https://github.com/Build-Fractal/conversus-oss/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org)

---

## What's Included

| Component | Description |
|-----------|-------------|
| **CLI** | 12 commands: `run`, `decide`, `validate`, `mcp`, `init`, `login`, `logout`, `status`, `context`, `skills`, `skill`, `snap` |
| **8 Modes** | cooperative, winner-take-all, prisoner's dilemma, red-blue, negotiation, resource-allocation, fair-division, mechanism-design |
| **25 Presets** | Ready-to-use agent configurations for common review patterns |
| **MCP Server** | Connect to Claude Code, Cursor, Windsurf, and other MCP-compatible editors |
| **Plugin System** | Extensible plugin framework for custom scoring and analysis |
| **Template System** | Mode-specific templates for dispute headings, objective functions, and synthesis |

---

## Quick Install

```bash
# Install directly from GitHub (Python 3.12+)
pip install git+https://github.com/Build-Fractal/conversus-oss.git
```

Or for local development:

```bash
git clone https://github.com/Build-Fractal/conversus-oss.git && cd conversus
pip install -e .          # editable install
# or: uv sync            # if using uv
```

!!! tip "MCP extras"
    To use conversus as an MCP server with Claude Code, Cursor, etc.:
    ```bash
    pip install "conversus[mcp] @ git+https://github.com/Build-Fractal/conversus-oss.git"
    ```

!!! tip "Claude Code plugin"
    Install the conversus plugin to get the `/conversus:design` guided config wizard and the full CLI as slash commands:
    ```
    /plugin marketplace add Build-Fractal/conversus-oss
    /plugin install conversus@conversus
    ```

See the [Quickstart](user-guide/quickstart.md) for prerequisites and first-run instructions.

!!! tip "Reading these docs"
    MkDocs is the primary reading surface. For the best experience, build and view locally: `uv run mkdocs serve`. API reference pages require the built site.

---

## Quick Links

<div class="grid cards" markdown>

-   :material-rocket-launch: **[Quickstart](user-guide/quickstart.md)**

    Get a deliberation running in under 2 minutes.

-   :material-console: **[CLI Reference](user-guide/cli.md)**

    All 12 commands, config files, presets, auth, JSON output.

-   :material-language-python: **[Python SDK](user-guide/sdk.md)**

    Programmatic API for scripts, CI/CD, and custom tooling.

-   :material-code-braces: **[API Reference](api/index.md)**

    Schemas, plugins, and domain module documentation.

-   :material-sword-cross: **[Deliberation Modes](user-guide/modes.md)**

    8 modes: cooperative, winner-take-all, prisoner's dilemma, red-blue, negotiation, resource-allocation, fair-division, mechanism-design. The CLI `decide` command supports 4 modes for quick ad-hoc use; all 8 are available via config files.

-   :material-connection: **[MCP Setup](user-guide/mcp-setup.md)**

    Connect conversus to Claude Code, Cursor, and other MCP-compatible editors.

</div>
