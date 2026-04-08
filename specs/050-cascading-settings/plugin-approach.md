# Spec 050 Addendum: Claude Code Plugin Pattern for Settings

**Date**: 2026-04-07
**Context**: `conversus init` overwrites `.claude/settings.json`, shadowing parent monorepo permissions. Plugin pattern solves this.

## Problem

`conversus init --runtime claude-code` creates `.claude/settings.json` with 21 agent permissions. If the project (or its parent monorepo) already has a `.claude/settings.json` with 52 permissions + hooks, the new file **shadows** it — Claude Code reads the nearest one, ignoring the parent.

Merge logic helps but is fragile. The real fix: don't write `.claude/settings.json` at all.

## Solution: Conversus as a Claude Code Plugin

Claude Code plugins declare permissions in their manifest. Plugin permissions are **additive** — they merge with project permissions automatically. No file shadowing.

### Plugin Structure

```
~/.claude/plugins/conversus/
├── manifest.json
├── settings.json        # conversus-specific defaults
└── mcp-server.json      # optional: MCP server config for spec 049
```

### manifest.json

```json
{
  "name": "conversus",
  "version": "0.1.0",
  "description": "Multi-agent deliberation engine",
  "permissions": {
    "allow": [
      "Read", "Write", "Edit", "Glob", "Grep", "Agent",
      "Bash(cat:*)", "Bash(head:*)", "Bash(tail:*)",
      "Bash(wc:*)", "Bash(find:*)", "Bash(ls:*)",
      "Bash(diff:*)", "Bash(sort:*)", "Bash(echo:*)",
      "Bash(mkdir:*)", "Bash(pwd)", "Bash(which:*)",
      "Bash(git:*)", "Bash(python:*)", "Bash(python3:*)"
    ]
  },
  "skills": [
    "conversus",
    "conversus-ask"
  ],
  "mcp_servers": {
    "conversus": {
      "command": "conversus",
      "args": ["mcp-server"],
      "description": "Conversus deliberation engine MCP tools"
    }
  }
}
```

### How It Works

1. User installs conversus: `pip install conversus` or `curl | bash`
2. Plugin auto-registers: `conversus plugin install` copies manifest to `~/.claude/plugins/conversus/`
3. User enables in project: add `"conversus": true` to `.claude/settings.json` `enabledPlugins`
4. Claude Code merges plugin permissions with project permissions — **never overwrites**
5. `conversus init` now only creates `.conversus/settings.json` (project config) — no `.claude/` touchpoint

### Migration

- `conversus init` stops writing `.claude/settings.json`
- `conversus init` still creates `.conversus/settings.json` (project defaults)
- `conversus plugin install` replaces the `.claude/` permission management
- Backward compat: if no plugin installed, conversus agents use `--dangerously-skip-permissions` (existing behavior)

### Impact on Spec 050 Cascade

The 4-level cascade becomes:

```
~/.claude/plugins/conversus/settings.json   # Plugin defaults
~/.conversus/settings.json                   # Global user overrides
<project>/.conversus/settings.json           # Project overrides
conversus.yml agent-level                    # Per-agent
CLI flags                                    # Per-invocation
```

Plugin defaults are the base layer. User/project settings override them. The plugin manifest handles permissions separately (merged by Claude Code, not by conversus).

## Open Source Implications

The plugin pattern is ideal for open source because:
1. No monorepo-specific `.claude/settings.json` in the repo
2. Plugin manifest is self-contained and portable
3. Users `pip install conversus && conversus plugin install` — done
4. Works across any Claude Code project without init ceremony
