# Feature Specification: MCP Prompts + CLI Skill Interface

**Feature ID**: `059-prompt-and-skill-interface`
**Created**: 2026-04-13
**Status**: Draft
**Depends On**: `055-capability-registry`, existing plugin SKILL.md files, MCP server
**Motivated by**: Desktop Extension users can't reliably trigger conversus — Claude gives its own answer instead of invoking the deliberation tools

---

## 1. Problem

Three related UX failures across different surfaces:

### Desktop Extension users: Claude doesn't use conversus

A non-technical user installs the `.mcpb` bundle, opens Claude Desktop, and asks: "Should I use Postgres or MongoDB for my user profiles?"

Claude gives its own opinion. It does NOT invoke `conversus_decide`. The user has no idea conversus is available, no way to explicitly trigger it, and no reason to believe a multi-agent deliberation would produce a better answer than Claude's confident one-shot response.

**Root cause**: MCP tools are passive — Claude decides when to use them based on tool descriptions. There's no explicit invocation mechanism for Desktop users. Claude Code has `/conversus:decide` slash commands; Desktop has nothing equivalent.

**MCP protocol solution**: The MCP spec defines `prompts` alongside `tools`. Prompts appear in the Claude Desktop UI as clickable actions — the equivalent of slash commands for Desktop. When a user clicks a prompt, Claude pre-fills the tool invocation. No ambiguity, no hoping the tool description matches.

### CLI users: no guided workflow

A developer installs conversus via pip and runs `conversus --help`. They see 11 commands. They try `conversus decide "my question" --provider mock` and it works. But they don't know:

- When to use `decide` vs `run` vs `validate`
- What the `--mode red-blue` flag actually means for their question
- That they should run `validate` before `run` to check cost
- That `--provider mock` exists for free testing before spending credits

The Claude Code plugin solves this with SKILL.md files — guided step-by-step workflows that ask the user one question at a time and build the command incrementally. But CLI-only users don't have access to the plugin's guidance.

### Cowork/Claude Code users: skills exist but aren't discoverable

The plugin has 8 skills (`decide`, `run`, `validate`, `init`, `login`, `logout`, `status`, `design`). But users only find them if they already know to type `/conversus:decide`. There's no `conversus skills` command that lists what's available.

---

## 2. Proposed solution

### 2.1 MCP Prompts for Desktop (P1)

Add `@mcp.prompt()` functions to the MCP server. These register with Claude Desktop as clickable prompt templates in the UI.

**Prompts to add:**

| Prompt name | User sees | What it does |
|---|---|---|
| `deliberate` | "Run a conversus deliberation" | Asks for the question, invokes `conversus_decide` with the configured default provider |
| `deliberate_red_blue` | "Red-team a decision" | Same but sets `--mode red-blue` — adversarial attack/defend |
| `deliberate_winner` | "Force a decision" | Same but sets `--mode winner-take-all` — no compromise, pick one |
| `review_config` | "Review a conversus config" | Asks for the config YAML, invokes `conversus_run` |
| `check_cost` | "Check deliberation cost" | Asks for the config YAML, invokes `conversus_validate` |

**Why these 5**: They map to the three core decision patterns a non-technical user has:

1. "I need help deciding" → `deliberate` (cooperative mode)
2. "I need someone to challenge my thinking" → `deliberate_red_blue`
3. "I need a definitive answer, not a balanced trade-off" → `deliberate_winner`
4. "I have a config, run it" → `review_config`
5. "How much will this cost?" → `check_cost`

**Implementation**: Each prompt is a function decorated with `@mcp.prompt()` that returns a list of MCP `PromptMessage` objects. The message content instructs Claude to call the appropriate tool with the user's input.

### 2.2 CLI skill viewer (P2)

New command: `conversus skill <name>`

```bash
# List all available skills
$ conversus skills
Available skills:
  decide      Run an ad-hoc deliberation
  run         Run from a config file
  validate    Check config and estimate cost
  design      Guided config builder (interactive)
  init        Set up project permissions
  ...

# View a specific skill's guided workflow
$ conversus skill decide
# Conversus Decide

Run a quick ad-hoc deliberation. No config file, just a question.

## Step 0: Check installation
...
```

**What `conversus skill <name>` does**: reads and prints the SKILL.md for that capability. The SKILL.md files already exist in `claude-code-plugin/skills/<name>/SKILL.md` — this command just makes them accessible from the terminal.

**Why this matters**: a developer who installed via pip and is using the CLI gets the same guided workflow that a Claude Code user gets via `/conversus:decide`. The skill content is the same — just the delivery surface differs. This is the registry pattern applied to documentation: one source (SKILL.md), multiple surfaces (plugin slash command, CLI print, Desktop prompt).

### 2.3 Skill discovery for Claude Code / Cowork (P3)

The plugin's SKILL.md files are discoverable via `/conversus:` tab-completion in Claude Code. But there's no `conversus skills` equivalent that works inside Claude Code. Adding a skill that lists other skills:

```
User: /conversus:help
Claude: Here are the available conversus commands:
  /conversus:decide   — quick ad-hoc deliberation
  /conversus:run      — full config-based deliberation
  /conversus:validate — check config and estimate cost
  /conversus:design   — guided config builder
  ...
```

This is a meta-skill — a SKILL.md that lists the other skills. Simple but high-impact for discoverability.

---

## 3. Surface projection

| Capability | CLI | MCP | Plugin | MCPB | Notes |
|---|---|---|---|---|---|
| MCP prompts | n/a | ✅ (prompts) | n/a | ✅ (via MCP) | Desktop-only concept |
| `skill <name>` | ✅ | ✅ (tool) | ✅ | ✅ | Read-only — returns SKILL.md text |
| `skills` (list) | ✅ | ✅ (tool) | ✅ | ✅ | Returns capability names + summaries |
| `help` meta-skill | n/a | n/a | ✅ | n/a | Plugin-only slash command |

---

## 4. Implementation plan

### Phase 1: MCP Prompts (Desktop UX fix)

1. Add 5 `@mcp.prompt()` functions to `mcp_server.py`
2. Each returns a `PromptMessage` with role="user" and content that instructs Claude to call the relevant tool
3. No registry changes needed — MCP prompts are registered directly with FastMCP, not through the capability registry
4. Test: install the `.mcpb` in Claude Desktop, verify prompts appear in the UI, verify clicking one triggers the correct tool

**Why not through the registry**: MCP prompts are a protocol-level feature (`prompts/list`, `prompts/get`) that sit alongside tools. They're not capabilities in the conversus sense — they're invocation shortcuts for existing capabilities. Routing them through the registry would add complexity without benefit.

### Phase 2: CLI skill viewer

1. Add `skill_cli(name: str)` and `skills_cli()` handlers to `engine/handlers.py`
2. `skill_cli` reads `claude-code-plugin/skills/<name>/SKILL.md` and prints it
3. `skills_cli` lists all capabilities with their summaries from `CAPABILITIES`
4. Register `skill` and `skills` as capabilities in `capabilities.py`
5. Project via `make build-surfaces`

### Phase 3: Help meta-skill

1. Create `claude-code-plugin/skills/help/SKILL.md` that lists all available `/conversus:*` commands with one-line descriptions
2. Register in `capabilities.py` with `surfaces=[Surface.PLUGIN]`
3. Hand-written SKILL.md (like `design`) — the help text IS the skill body

---

## 5. How prompts solve the Desktop problem

**Before (current)**:
```
User: "Should I use Postgres or MongoDB?"
Claude: "Great question! Here are the key differences..." [gives its own opinion]
[conversus_decide is never called]
```

**After (with prompts)**:
```
User: [clicks "Run a conversus deliberation" prompt]
Claude: "What decision are you facing?"
User: "Should I use Postgres or MongoDB for user profiles?"
Claude: [calls conversus_decide with the question]
→ Full 5-phase deliberation runs
→ Adversarial review, not a one-shot answer
```

The prompt is the explicit invocation mechanism that Desktop users need. It's the equivalent of typing `/conversus:decide` in Claude Code — but accessible via a clickable UI element rather than slash-command syntax.

---

## 6. Success criteria

- SC-001: Claude Desktop shows "Run a conversus deliberation" as a clickable prompt after installing the extension
- SC-002: Clicking the prompt triggers `conversus_decide` with the user's question
- SC-003: `conversus skills` lists all available skills with summaries
- SC-004: `conversus skill decide` prints the full SKILL.md for the decide capability
- SC-005: `/conversus:help` in Claude Code lists all available `/conversus:*` commands
- SC-006: MCP prompts use the settings cascade — a user with `default_provider: anthropic` in their settings gets a real deliberation, not mock

---

## 7. Out of scope

- **Prompt customization** — users can't create their own prompts. Future spec.
- **Prompt chaining** — running multiple prompts in sequence (e.g. validate → run). Future spec.
- **Inline skill editing** — editing SKILL.md from the CLI. Skills are authored by developers, not end users.

---

## 8. Sources

| Source | Use |
|---|---|
| MCP protocol spec (`prompts/list`, `prompts/get`) | The protocol feature that enables Desktop prompts |
| `claude-code-plugin/skills/*/SKILL.md` | The skill content that the CLI viewer exposes |
| `specs/055-capability-registry.md` | Registry framework for the `skill` and `skills` capabilities |
| `specs/057-settings-architecture.md` | Settings cascade that prompts should respect |
| MCPB MANIFEST.md | Manifest format for the `.mcpb` bundle |
