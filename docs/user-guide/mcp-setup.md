# MCP Setup

Deliberator exposes three tools via the Model Context Protocol (MCP) for use in AI coding assistants.

## Available MCP tools

| Tool | Purpose |
|------|---------|
| `deliberator_validate` | Validate a YAML config, classify questions, estimate cost |
| `deliberator_run` | Validate + run or parse existing output |
| `deliberator_decide` | Ad-hoc deliberation with question quality gate |

## Claude Code

The project includes `.mcp.json` at the root -- Claude Code picks it up automatically when you open the project directory.

If auto-detection doesn't work, register manually:

```bash
claude mcp add deliberator -- deliberator mcp
```

Requires MCP extras:

```bash
pip install "deliberator[mcp] @ git+https://github.com/Build-Fractal/deliberator.git"
```

**Verify:** Open Claude Code in the deliberator directory and ask it to validate a config. The `deliberator_validate` tool should appear in the tool list.

## Cursor

Add to `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "deliberator": {
      "command": "uv",
      "args": ["run", "python3", "mcp_server.py"],
      "cwd": "/path/to/deliberator"
    }
  }
}
```

Restart Cursor after adding the config.

## VS Code (with MCP extension)

If using an MCP-compatible VS Code extension, add the same server config to the extension's settings. The exact location varies by extension.

## Tool reference

### deliberator_validate

Validate a config without executing.

**Parameters:**
- `config_yaml` (string, required): Full YAML config content.
- `question` (string, optional): Question to classify for sufficiency.

**Returns:** `ValidateResult` with:
- `valid`: boolean
- `errors`: list of error strings
- `cost_estimate`: `{ total_launches, launches_per_phase, agent_count, iteration_count }`
- `classification`: question sufficiency result (if question provided)
- `preset_info`: mode, agent names, iteration count

### deliberator_run

Validate and optionally run a deliberation.

**Three modes:**

1. **Validate-only** (no `output_path`, no `provider`): validates config, returns cost estimate and execution instructions.
2. **Parse-results** (`output_path` set): validates config, reads and parses the synthesis file at that path into structured JSON.
3. **In-process** (`provider` set, no `output_path`): validates config, runs the full pipeline in-process, returns structured output.

**Parameters:**
- `config_yaml` (string, required): Full YAML config content.
- `output_path` (string, optional): Path to existing `summary/final.md`.
- `provider` (string, optional): `'mock'`, `'anthropic'`, or `'openai'`.

**Returns:** `RunResult` with structured `DeliberatorOutput` when output is available.

### deliberator_decide

Ad-hoc deliberation with quality gate.

**Parameters:**
- `question` (string, required): Natural-language question.
- `provider` (string, default `'mock'`): Provider name.
- `mode` (string, default `'cooperative'`): Deliberation mode.
- `max_launches` (int, default `20`): Cost safeguard.

**Returns:** `DecideResult` with:
- `sufficient`: whether the question passed the quality gate
- `output`: structured deliberation output (when successful)
- `cost_estimate`: estimated launches before execution
- `errors`: any error messages

The tool rejects insufficient questions before spending any API calls. For 2 agents / 1 iteration, the default config needs 9 launches.

## Troubleshooting

**Tool not appearing:** Make sure `uv` is on your PATH and you're in the deliberator project directory. Run `uv run python3 mcp_server.py` manually to check for import errors.

**Provider auth errors:** The MCP server resolves credentials the same way as the CLI -- env var first, then `~/.deliberator/auth.json`. Run `deliberator login anthropic` in a terminal before using the MCP tools.

**Timeout on large deliberations:** The MCP server runs synchronously. For large configs (many agents, multiple rounds), use `deliberator run` from the CLI instead.
