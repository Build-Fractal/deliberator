# Distribution Strategy Specification

**Feature ID**: distribution-strategy
**Created**: 2026-04-08
**Status**: Active
**Depends On**: PyPI packaging, MCP server, Claude Code plugin

## 1. Summary

Conversus uses a three-layer distribution architecture that covers 7+ platforms from a single codebase. This spec documents the strategy, the deliberation that produced it, and the packaging artifacts.

## 2. Deliberation Methodology

A conversus mechanism-design deliberation evaluated 7 distribution options with 4 agents:
- **APM Maximizer**: maximize ecosystem reach via meta-packaging
- **Non-Technical User Advocate**: healthcare analyst / PM who uses AI tools but doesn't code
- **Technical Power User**: senior engineer, OSS contributor, CI/CD integration
- **Fact-Based Arbiter**: brings verifiable facts, resolves disputes with evidence

5 phases (review → cross-review → revision → disputes → synthesis), 29 LLM launches, 2 iterations.

**Unanimous consensus** on: MCP as universal foundation, Claude Code Plugin as primary marketplace channel, staged evidence-based expansion, security validation framework.

## 3. Three-Layer Architecture

### Layer 1: PyPI Package (P1 — Done)
- `pip install conversus`
- Canonical package — all other layers wrap this
- Powers: CLI, Python SDK, CI/CD pipelines
- Optional extras: `[mcp]`, `[docs]`, `[test]`, `[nashopt]`, `[kalman]`, `[ampl]`, `[solvers]`

### Layer 2: MCP Server (P1 — Done)  
- `conversus mcp` — stdio transport
- Works with: Claude Code, Cursor, Claude Desktop, Windsurf, Zed, Continue, VS Code+Copilot
- Tools exposed: conversus_validate, conversus_run, conversus_decide
- Registration: `claude mcp add conversus -- conversus mcp`
- Key constraint: Cursor has 40-tool limit, Claude Code unlimited

### Layer 3: Claude Code Plugin (P1 — Done)
- `claude-code-plugin/` directory with plugin.json + skills/conversus.md
- Thin CLI wrapper — checks install, dispatches to `conversus` CLI via Bash
- `/conversus` slash command
- Marketplace install for non-technical users

## 4. Extended Platform Coverage

Research (April 2026) confirmed the plugin format is shared across multiple Anthropic surfaces:

### 4a. Cowork (P1 — Packaging needed)
- Anthropic's desktop agent for knowledge workers ("Claude Code for everyone else")
- **Same plugin format** as Claude Code (`.claude-plugin/` with SKILL.md)
- Shared marketplace at claude.com/plugins covers both Claude Code and Cowork
- GUI install: Customize sidebar → Browse plugins → Install (under 30 seconds)
- Non-technical users see form-based slash commands, not raw prompts
- **Action**: Submit existing Claude Code plugin to shared marketplace

### 4b. Claude Desktop Extension (P1 — Packaging needed)
- `.mcpb` format (MCP Bundle) — ZIP archive with manifest.json + server reference
- One-click install: double-click .mcpb file or Settings → Extensions → Browse
- No JSON editing, no Node.js, no terminal required
- Replaced older `.dxt` format (still backwards compatible)
- **Action**: Create .mcpb bundle wrapping `conversus mcp` stdio server

### 4c. claude.ai Web Skills (P2 — Future)
- Skills tab in claude.ai web interface
- Same SKILL.md format as Claude Code/Cowork plugins
- Available to Free/Pro/Max/Team/Enterprise users
- No app install required — works entirely in browser
- **Action**: Submit SKILL.md as claude.ai Skill (requires Anthropic review)

## 5. Compatibility Matrix

| Platform | MCP Native | Plugin Format | Min Skill Level | Zero-Setup | Status |
|---|---|---|---|---|---|
| Claude Code (CLI/VS Code) | Yes (stdio) | .claude-plugin/ | Developer | No | Done |
| Cowork | Yes (HTTP+OAuth) | Same as Claude Code | Non-technical | Yes (marketplace) | Needs submission |
| Claude Desktop | Yes (.mcpb) | .mcpb bundle | Non-technical | Yes (double-click) | Needs .mcpb |
| claude.ai web | Yes (remote MCP) | SKILL.md | Non-technical | Near-zero | Future (P2) |
| Cursor / Windsurf / Zed | Yes (stdio) | MCP config JSON | Developer | No | Done (via MCP) |
| VS Code + Copilot | Yes | MCP config | Developer | No | Done (via MCP) |
| PyPI / CLI | N/A | pip package | Developer | No | Done |

## 6. Paid/OSS Boundary

Strict separation — paid features excluded from OSS distribution:
- **Excluded**: nashopt scorer, web interface (BYOK), code-review domain, blog, REST API docs
- **Enforcement**: Separate packages, not conditional imports
- **Docs**: MkDocs Material, same framework as paid docs for mergeability

## 7. Deferred Items

| Item | Priority | Reason |
|---|---|---|
| APM meta-packaging | P2 | Experimental — validate compilation targets first |
| VS Code native extension | P3 | MCP covers this; dedicated extension adds maintenance |
| Cursor native extension | P3 | Same as VS Code — MCP sufficient |
| Blog | P2 | Defer to v0.2+ |

## 8. Unresolved Tensions

1. **APM compilation vs native packaging** — APM as experimental secondary until proven
2. **Security validation vs zero-friction install** — marketplace review provides some validation
3. **Resource constraints** — even 3+2 channels may stretch a small team; Cowork shares the Claude Code plugin so minimal incremental cost

## 9. Sources

- Cowork launch: claude.com/blog/cowork-research-preview (Jan 2026)
- Cowork plugins: claude.com/blog/cowork-plugins (Feb 2026)
- Shared marketplace: claude.com/plugins
- Desktop Extensions (.mcpb): anthropic.com/engineering/desktop-extensions
- MCP donated to Linux Foundation Agentic AI Foundation: Dec 2025
- Claude Code plugin marketplace: 101 plugins, 33 Anthropic-built (March 2026)
