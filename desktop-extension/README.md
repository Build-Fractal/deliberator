# Conversus Claude Desktop Extension (.mcpb)

One-click install for Claude Desktop. Wraps the `conversus mcp` stdio server.

## Prerequisites

Install conversus with MCP extras:

```bash
pip install "conversus[mcp] @ git+https://github.com/Build-Fractal/conversus-oss.git"
```

Verify the CLI is on your PATH:

```bash
conversus --version
```

## Build the .mcpb bundle

```bash
cd desktop-extension
./build.sh
```

This produces `conversus.mcpb` in the repo root.

## Install

Double-click `conversus.mcpb` — Claude Desktop opens an install dialog.

Or: Claude Desktop → Settings → Extensions → Install from file.

## Manual MCP registration (Claude Code / Cursor / Windsurf)

If you prefer raw MCP config instead of the .mcpb bundle:

```bash
claude mcp add conversus -- conversus mcp
```

Or add to your MCP client config JSON:

```json
{
  "mcpServers": {
    "conversus": {
      "command": "conversus",
      "args": ["mcp"]
    }
  }
}
```
