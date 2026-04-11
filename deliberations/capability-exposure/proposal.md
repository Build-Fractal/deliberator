# Capability Exposure Boundaries

## Context

Over the last two days conversus-oss has grown four distinct distribution surfaces, each with its own installation path and UX:

1. **Python CLI** (`conversus` binary) — installed via `pip install git+...`
2. **MCP server** exposed via `conversus mcp` (stdio transport) — used by MCP clients (Claude Desktop, Cursor, Windsurf, Zed)
3. **Claude Code / Cowork plugin** — installed via `/plugin marketplace add Build-Fractal/conversus-oss`
4. **Claude Desktop Extension** (`.mcpb` bundle) — double-click install, self-contained

Each surface currently exposes a **different subset** of conversus's capabilities, and the boundaries grew organically — we made ad-hoc decisions along the way about what to put where. This deliberation is a step back: **what's the right separation?**

## Current state

### Surface 1: Python CLI (9 commands)

| Command | Purpose |
|---|---|
| `conversus run <config>` | Run deliberation from YAML |
| `conversus decide "<question>"` | Ad-hoc deliberation |
| `conversus validate <config>` | Validate + cost estimate |
| `conversus init` | Write runtime settings files |
| `conversus mcp` | Launch MCP stdio server |
| `conversus status` | Show provider auth state |
| `conversus login <provider>` | OAuth login |
| `conversus logout <provider>` | Remove credentials |
| `conversus context` | Debug: print detected runtime |

**Who uses it**: developers scripting CI/CD, power users, terminal natives.

### Surface 2: MCP tools (3 tools)

Exposed via `mcp_server.py` in the conversus Python package:

| Tool | Purpose |
|---|---|
| `conversus_decide` | Ad-hoc deliberation from a question |
| `conversus_run` | Run or parse a full deliberation |
| `conversus_validate` | Validate YAML + estimate cost |

**Who uses it**: users of MCP-compatible editors (Cursor, Windsurf, Claude Desktop via `.mcpb`, Claude Code via `claude mcp add`).

### Surface 3: Claude Code / Cowork plugin (8 slash commands)

Each is a SKILL.md in `claude-code-plugin/skills/<name>/SKILL.md`:

| Command | Purpose |
|---|---|
| `/conversus:design` | **Guided conversational config wizard** (not in CLI or MCP) |
| `/conversus:decide` | Wraps CLI `decide` |
| `/conversus:run` | Wraps CLI `run` |
| `/conversus:validate` | Wraps CLI `validate` |
| `/conversus:init` | Wraps CLI `init` |
| `/conversus:status` | Wraps CLI `status` |
| `/conversus:login` | Wraps CLI `login` |
| `/conversus:logout` | Wraps CLI `logout` |

**Who uses it**: Claude Code users, Cowork knowledge workers. The slash command layer is the "discoverable menu" — users type `/` and see all 8 options.

### Surface 4: Claude Desktop Extension (`.mcpb`, 3 tools)

The `.mcpb` wraps the MCP server — its `tools[]` list in `manifest.json` matches whatever `mcp_server.py` registers. Currently 3 tools (same as Surface 2).

**Who uses it**: non-technical users, knowledge workers who installed conversus by double-clicking the bundle. The Claude Desktop install dialog shows the `tools[]` list as the primary **discovery surface** — users browsing extensions see only these 3 tools and infer from them what conversus does.

## The fragmentation problem

### Observation 1: Capability fragmentation

Some capabilities exist only on one surface:

- **`design` (guided wizard)** — ONLY in plugin. No CLI equivalent, no MCP tool. If you're in Claude Desktop (not Claude Code), you can't use it at all.
- **`init`, `status`, `login`, `logout`** — in CLI and plugin, but NOT as MCP tools. Users of Claude Desktop can't set up permissions or check auth without leaving the app and opening a terminal.
- **Discovery/listing** (modes, providers, presets, example configs) — NOT available anywhere. Users have no way to ask conversus "what modes do you have?" from any surface.

### Observation 2: Implementation duplication

The same logic exists in up to 3 places:

- `decide` appears as CLI command, MCP tool, AND plugin slash command — three implementations with three slightly different docstrings/descriptions
- `run` and `validate` are the same — three surfaces each
- Plugin slash commands are thin bash wrappers around the CLI, which is fine — but the CLI is itself a thin wrapper around engine functions, and MCP tools duplicate the same logic with slightly different signatures

### Observation 3: Discovery asymmetry

The Claude Desktop install dialog shows `tools[]` from the manifest. Right now that's **3 tools** — so users browsing extensions see a minimal capability set and may dismiss conversus as "just a decide tool". Meanwhile the plugin surface shows **8 slash commands** and the CLI shows **9 subcommands**. The Desktop Extension users — the people who most need clear discovery — see the smallest menu.

## Open questions

The deliberation should resolve each of these:

### Q1: Should MCP tools expand to match CLI coverage?

Option A: Keep MCP tools minimal (3: decide, run, validate). MCP tools are for "things Claude invokes autonomously" — setup commands don't fit.

Option B: Add MCP tools for init, status, login, logout, design. Full parity with CLI. Downside: tool list bloats, Claude's selection accuracy drops.

Option C: Add discovery-only tools (list_modes, list_providers, list_presets, list_examples) — 3 action tools + 4 listing tools = 7 total. The listing tools expand the discovery surface without bloating action space.

### Q2: Should the guided `design` flow exist on non-plugin surfaces?

The plugin's `/conversus:design` is a conversational wizard that walks a user through building a conversus.yml. It lives only in the plugin because it needs conversational interaction.

Option A: Keep it plugin-only. Claude Desktop users should use `/conversus:decide` for quick questions and write YAML by hand for custom configs.

Option B: Add `conversus_design_config` as an MCP tool that returns a draft config from structured parameters (question, mode, agents, target). Less conversational but usable from Claude Desktop.

Option C: Add `conversus design` as a CLI subcommand with interactive Rich prompts. Works in terminal without needing the plugin.

### Q3: Should discovery be a first-class capability?

Right now there's no way to ask "what modes does conversus support?" from any surface. You have to read the docs.

Option A: Leave discovery in docs. Docs are the source of truth for "what is conversus", tools are the source of truth for "do things".

Option B: Add listing tools (`list_modes`, `list_providers`, `list_presets`, `list_examples`) on all surfaces. Claude can introspect capabilities and tell users what's available.

Option C: Only add listing on the install dialog surface — hardcode the capability list in `manifest.json`'s `long_description` field (users see it once at install time, no runtime tool calls needed).

### Q4: What's the rule for where new functionality lives?

When we add a new capability in the future (e.g., `conversus export-html` to generate a static HTML deliberation report), where does it go?

Option A: **CLI first, plugin wraps, MCP mirrors.** New capability = new CLI subcommand. Plugin and MCP automatically get it as a wrapper. Highest implementation consistency but requires triple-documentation.

Option B: **Core engine function, each surface chooses.** Functionality lives in `conversus/` Python modules. CLI, MCP, and plugin each decide independently whether to expose it. Highest flexibility but risks divergence.

Option C: **Surface-appropriate placement.** Conversational features → plugin only. Action features → CLI + MCP. Discovery → hardcoded in manifest + optional list tools.

### Q5: Should we use a single-source-of-truth registry generated at build time?

**This is the key architectural question.** Right now we hand-write every surface separately — CLI commands in Python, MCP tools in Python (different file), plugin slash commands as markdown SKILL.md files, manifest tools[] as JSON. Adding a new capability means editing 4 files in 4 different formats.

The alternative: **define each capability ONCE in a single source of truth** (e.g., a Python registry, a YAML file, or decorator metadata), then **generate the surfaces at build time**:

- A `tools.yml` (or `capabilities.py`) declares each capability with metadata: name, description, parameters, surfaces it should appear on, handler function
- Build script reads this registry and emits:
  - CLI commands (Click subcommands)
  - MCP tool registrations (`@mcp.tool()` decorators)
  - Plugin SKILL.md files (with frontmatter and bash dispatch)
  - Manifest `tools[]` JSON for the .mcpb
- Single source = single edit point. No drift between surfaces is possible because they all derive from the same definition.

Sub-questions for the deliberation:

**Q5a — Is one artifact that does it all the right end state?** A monorepo where capabilities are defined once and projected to N surfaces, vs. the current "N surfaces with parallel implementations".

**Q5b — Or are purpose-built surfaces actually better?** A skill / slash command / MCP tool tailored to a specific environment (Cowork form UI, Claude Desktop install dialog) might lose fidelity if auto-generated from a generic registry. Hand-tuned UX per surface beats generic UX everywhere.

**Q5c — If we go single-source, what's the registry format?** Python file with decorators? YAML manifest? JSON schema? Generated from `engine/cli/__init__.py` directly via Click introspection?

**Q5d — Build-time vs. runtime?** Generate the surfaces during a build step (one artifact, committed to repo) or have each surface introspect a runtime registry (more dynamic but requires importing the registry into 4 different runtimes)?

Options:

**Option A: Single-source registry, build-time projection.** Define everything once (e.g., `capabilities.yml`). A `make build-surfaces` step regenerates CLI, MCP, plugin, and manifest. Maximum consistency, requires upfront tooling investment.

**Option B: Hand-written surfaces, but with shared metadata.** Each surface stays hand-written, but pulls description strings, parameter schemas, and tool lists from a shared module. Less generation magic, but still drift-prone.

**Option C: Status quo.** Each surface is independently maintained. Drift is accepted as a maintenance cost. Simplest, but the cost compounds with every new capability.

**Option D: Purpose-built per surface.** Explicitly reject the "one source" goal. Each surface is hand-tuned for its environment. Cowork forms get a different UX from Claude Desktop tools from CLI subcommands. Highest UX quality, highest maintenance cost.

### Q6: Could a registry + per-surface adapters give us BOTH consistency AND tuned UX?

The dichotomy in Q5 (single source vs. purpose-built) may be false. There's a third option that combines them:

**Pattern**: define each capability ONCE in a registry, but allow OPTIONAL per-surface adapter classes that override how that capability gets projected to a specific surface. Surfaces that don't need tuning use the default adapter and get consistency for free; surfaces that need surface-specific UX (Cowork forms, Claude Desktop install dialog tool descriptions, Rich CLI tables) provide an adapter that overrides only the parts that matter.

**Example sketch**:

```python
# capabilities.py — single source of truth
@capability(
    name="decide",
    summary="Run an ad-hoc deliberation on a question",
    surfaces=[Surface.CLI, Surface.MCP, Surface.PLUGIN, Surface.MCPB],
    params=[
        Param("question", str, required=True),
        Param("provider", str, default="mock"),
        Param("mode", str, default="cooperative"),
    ],
    handler=lambda question, provider, mode: engine.run_decide(question, provider, mode),
)
class DecideCapability:
    """Most surfaces use the default adapter — only override when needed."""


# Optional override: richer MCP tool description for Claude's tool selection
@DecideCapability.mcp_adapter
class DecideMCPAdapter(MCPAdapter):
    description = """Run an ad-hoc deliberation. Use this when the user describes
    a decision (e.g. "Postgres or MongoDB?"). Don't use for vague questions —
    the sufficiency classifier will reject them."""


# Optional override: Rich table output in CLI
@DecideCapability.cli_adapter
class DecideCLIAdapter(CLIAdapter):
    def render_result(self, result):
        return rich_table_from(result)
```

**What this gives us**:

- **Single source of truth** for the canonical capability: name, parameters, handler, intent. Drift between surfaces is impossible.
- **Surface-specific UX tuning** for the cases where it matters — install dialog text, Rich tables, conversational dispatch, form fields — through opt-in adapter classes.
- **Default adapters** cover 80%+ of capabilities with no extra code. The 20% that need tuning get explicit adapter overrides.
- **Skip-a-surface support**: a capability can declare `surfaces=[Surface.CLI, Surface.PLUGIN]` to opt out of MCP/.mcpb entirely (e.g., `login` is terminal-only because OAuth needs a browser).

**The build flow stays the same as Option A**: a single `make build-surfaces` reads the registry, applies the adapter (default or override) for each surface, and emits the projected files (`engine/cli/__init__.py`, `mcp_server.py`, `claude-code-plugin/skills/`, `desktop-extension/manifest.json`).

**Implementation cost**: ~3-4 days of focused work for the registry framework + default adapters + projector + migration of existing 12 capabilities. Each new capability after that is one registry entry plus optional adapter overrides only when surface-specific UX is needed.

**This is the option to take seriously** if the answers to Q1-Q5 keep colliding between "consistency" and "per-surface UX" — it dissolves the false dichotomy. It's strictly more flexible than Option A (pure registry) and strictly less work than Option D (full purpose-built).

**Sub-question**: is the upfront framework cost (3-4 days) worth it for a project at conversus's current scale (~12 capabilities across 4 surfaces)? Or is it premature engineering until the project grows past some threshold (say, 25+ capabilities)?

## Constraints

- Small team — we can't maintain 3 copies of every command indefinitely
- Users of Claude Desktop Extension are the LEAST technical audience — they can't easily "drop to the terminal" to run setup commands
- The `.mcpb` install dialog is the primary discovery surface for non-technical users
- The MCP tool list (shown in manifest.json tools[]) is what users see in the install dialog
- Slash commands are discovered via the `/` menu in Claude Code / Cowork
- CLI commands are discovered via `conversus --help` in a terminal
- Every exposed capability is a maintenance cost (docs, tests, surface area)

## What we need

A concrete set of rules with:

1. **A surface-to-capability matrix** — for each capability class (actions, setup, auth, discovery, conversational UX), which surfaces should expose it?
2. **A decision framework for new features** — given a proposed feature, where should it live?
3. **A cleanup list** — what should we REMOVE or consolidate from the current state?
4. **A "discoverability floor"** — what minimum set of capabilities must be visible on EVERY surface?
5. **Specific resolution** of Q1-Q4 above
