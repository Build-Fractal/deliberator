# Deliberator Claude Desktop Extension (.mcpb)

One-click install for Claude Desktop. Wraps the `deliberator mcp` stdio server.

## Prerequisites

Install deliberator with MCP extras:

```bash
pip install "deliberator[mcp] @ git+https://github.com/Build-Fractal/deliberator.git"
```

Verify the CLI is on your PATH:

```bash
deliberator --version
```

## Build the .mcpb bundle

```bash
cd desktop-extension
./build.sh
```

This produces `deliberator.mcpb` in the repo root.

## Install

Double-click `deliberator.mcpb` — Claude Desktop opens an install dialog.

Or: Claude Desktop → Settings → Extensions → Install from file.

## Manual MCP registration (Claude Code / Cursor / Windsurf)

If you prefer raw MCP config instead of the .mcpb bundle:

```bash
claude mcp add deliberator -- deliberator mcp
```

Or add to your MCP client config JSON:

```json
{
  "mcpServers": {
    "deliberator": {
      "command": "deliberator",
      "args": ["mcp"]
    }
  }
}
```
