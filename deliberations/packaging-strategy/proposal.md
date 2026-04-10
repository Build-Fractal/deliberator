# Conversus Distribution Strategy — Proposal for Deliberation

## Context

Conversus is an open-source competitive multi-agent deliberation engine. It needs a distribution strategy that meets developers where they work. The engine is written in Python with a CLI entry point, and supports multiple LLM providers.

## The Question

How should conversus be packaged and distributed to maximize adoption across different developer workflows?

## Distribution Channels Under Consideration

### 1. PyPI Package (`pip install conversus`)
- Traditional Python package distribution
- CLI tool + importable library
- Handles the engine, providers, game theory modes
- Well-understood, broad reach in Python ecosystem

### 2. Claude Code Plugin (Official Marketplace)
- Bundles skills + hooks + MCP servers into a distributable package
- 101 plugins in official Anthropic marketplace as of March 2026
- Community marketplaces are GitHub repos (`/plugin marketplace add owner/repo`)
- Plugin = skill (slash command) + supporting files (templates, configs, assets)
- Direct integration with Claude Code's agent orchestration

### 3. Claude Code Skill (Single `.claude/skills/` file)
- Lightest-weight option — just a SKILL.md with frontmatter
- Slash command invocation (`/conversus`)
- Can spawn subagents, accept arguments, use tools
- No marketplace needed — git clone or copy the file

### 4. MCP Server (`conversus --mcp`)
- Model Context Protocol server exposing conversus as tools
- Works with Claude Code, Cursor, Claude Desktop, Windsurf, any MCP client
- Universal protocol — the "USB-C" of AI tool integration
- Cursor has 40-tool limit; Claude Code unlimited

### 5. APM Package (`apm install conversus`)
- Agent Package Manager — distributes agent artifacts (skills, prompts, presets)
- Can target multiple output formats from single source
- Manages dependencies, versioning, compilation
- Less established ecosystem than PyPI or Claude Code marketplace

### 6. Cursor Extension
- Via MCP server (shared with #4) or VS Code extension format
- Cursor-specific marketplace
- Growing but separate ecosystem from Claude Code

### 7. VS Code Extension
- Largest IDE marketplace
- Can wrap MCP server or direct integration
- Reaches non-Claude, non-Cursor developers

## Key Facts

- MCP servers work identically across Claude Code, Cursor, Claude Desktop
- Claude Code plugins bundle skills + hooks + MCP servers
- Cursor has a 40-tool hard limit vs Claude Code's unlimited
- APM can compile packages targeting multiple formats
- The Claude Code official marketplace is curated by Anthropic (33 Anthropic-built plugins)
- Community marketplaces are just GitHub repos — no verification required
- PyPI has the broadest reach but no AI-native integration
- Most developers discovering conversus will be AI-tool users (Claude Code, Cursor, etc.)

## Constraints

- Small team — can't maintain 7 separate distribution targets
- Must work for non-technical users (one-command install)
- Must work for power users (composable, configurable)
- Should leverage existing tooling where possible
- Open source — community should be able to contribute distribution targets

## What We Need to Decide

1. **Primary distribution**: What's the default `install conversus` experience?
2. **Secondary channels**: Which 1-2 additional channels maximize incremental reach?
3. **Build system**: Should APM be the meta-packager that targets all formats?
4. **Plugin vs Skill vs MCP**: For the Claude Code ecosystem, which granularity?
5. **Cross-IDE strategy**: MCP as universal layer, or per-IDE packages?
