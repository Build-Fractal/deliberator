# Feature Specification: Capability Registry with Per-Surface Adapters

**Feature ID**: `055-capability-registry`
**Created**: 2026-04-11
**Status**: Approved (binding deliberation outcome) — Day 1-4 complete, constitution-aligned
**Depends On**: `distribution-strategy.md`, existing CLI/MCP/plugin/`.mcpb` implementations
**Decided by**: `deliberations/capability-exposure-followup/output/arbiter/resolution.md`
**Governed by**: `CONSTITUTION.md` (principles IX, XI, XII, XIV)

> **Amendment 2026-04-11** — After Day 1-4 implementation and before Day 5,
> `CONSTITUTION.md` was copied over from the conversus repo and adopted as
> governing for conversus-oss. Day 1-4 was reworked in place to satisfy
> principle IX (no module-level mutable state; Pydantic models for data
> structures; StrEnum for closed behavioral choices; no `Any` on public
> signatures). Section 3 code examples and the Day 5 bullets below
> reflect the post-rework implementation, per principle XIV
> (Spec-Implementation Parity). The binding decision (Option A: registry
> + per-surface adapters) is unchanged — only the implementation shape
> was adjusted to fit the constitution.

---

## 1. Summary

Conversus exposes capabilities (`decide`, `run`, `validate`, `init`, `login`, etc.) across **four distribution surfaces**:

| Surface | Format | Audience |
|---|---|---|
| CLI (`engine/cli/__init__.py`) | Click commands | Developers, scripts, CI/CD |
| MCP server (`mcp_server.py`) | `@mcp.tool()` functions | MCP-compatible editors (Cursor, Windsurf, etc.) |
| Claude Code / Cowork plugin (`claude-code-plugin/skills/*/SKILL.md`) | Markdown skills | Claude Code and Cowork users |
| Claude Desktop Extension (`desktop-extension/manifest.json`) | JSON tools array | Claude Desktop users via `.mcpb` install |

Currently each capability is **hand-written 4 times in 4 different formats**, causing drift, capability fragmentation (Desktop Extension users can't authenticate, discover modes, or use the design wizard), and a maintenance cost that grows as O(capabilities × surfaces).

This spec defines a **capability registry** as the single source of truth for all conversus capabilities, with optional **per-surface adapter classes** that override the projection only when surface-specific UX matters. A `make build-surfaces` script reads the registry, applies the adapters (default or override), and emits the four surface files. Generated files become build artifacts — never hand-edited.

---

## 2. Decision basis

Two deliberations resolved the architecture:

| Deliberation | Mode | Launches | Outcome |
|---|---|---|---|
| `deliberations/capability-exposure/` | mechanism-design | 26 | Converged on principles ("CLI canonical", "eliminate duplication via shared metadata") but failed to commit to a specific pattern. Synthesis recommended "balanced trade-offs" — a non-answer. |
| `deliberations/capability-exposure-followup/` | winner-take-all | 10 | Focused on the binding question. Phase 5 synthesizer picked anti-framework-skeptic on resource economics; **Phase 6 arbiter overrode it** and picked Option A (registry + adapters) citing user-equity as a foundational principle. |

Verbatim from the binding ruling:

> Desktop Extension users cannot authenticate with providers. They cannot discover available modes or providers. They're missing the design wizard entirely. This isn't "tomorrow's scale problem" — it's a current user equity failure that contradicts my foundational accessibility principles.

The arbiter's framing is critical: this is not infrastructure optimization for future scale — it is **fixing a current user-equity gap** where one of the four surfaces (the most user-friendly one) is missing capabilities that exist on the other three.

---

## 3. Architecture

### 3.1 The registry

A single source of truth — `capabilities.py` at the repo root — declares each capability as a `Capability` Pydantic model and exports an explicit `CAPABILITIES` list that the projector walks:

```python
# capabilities.py
from conversus.registry import Capability, Param, Surface

decide = Capability(
    name="decide",
    summary="Run an ad-hoc deliberation on a natural-language question",
    long_description=(
        "Quick deliberation without needing a config file. Uses the "
        "built-in pragmatist + devils-advocate agents and runs the full "
        "5-phase pipeline."
    ),
    surfaces=[Surface.CLI, Surface.MCP, Surface.PLUGIN, Surface.MCPB],
    params=[
        Param(name="question", type=str, required=True,
              help="The decision to deliberate. Be specific."),
        Param(name="provider", type=str, default="mock",
              choices=["mock", "anthropic", "openai", "claude-code", "ollama"],
              help="LLM provider to use."),
        Param(name="mode", type=str, default="cooperative",
              choices=["cooperative", "winner-take-all", "prisoners-dilemma", "red-blue"],
              help="Deliberation mode."),
        Param(name="max_launches", type=int, default=20,
              help="Safety cap on LLM launches.",
              surfaces=[Surface.MCP]),  # MCP-only; CLI uses its own flow
    ],
    handler="engine.handlers:run_decide_cli",
    handlers={Surface.MCP: "engine.handlers:run_decide_mcp"},
)

CAPABILITIES: list[Capability] = [decide]
```

**Why direct construction, not a decorator**: `CONSTITUTION.md` principle IX forbids mutable module-level state. A `@capability(...)` decorator that appends to a module-level `REGISTRY` list is exactly the pattern the principle prohibits. The explicit `CAPABILITIES = [...]` export is the constitution-compliant replacement — the projector reads it directly, and there is no hidden registration via import-time side effects.

**Why two handlers**: `decide` has intrinsic surface-specific behavior (CLI prints + exits; MCP returns structured data). The `handlers` dict is an optional per-surface override; most capabilities use a single `handler` across all surfaces and leave `handlers` unset. See principle XIV (spec-implementation parity) for why this was added during Day 5 migration rather than scaffolded speculatively on Day 1-2.

The `handler` field is a Python import string (`module.path:func_name`) that points to the canonical implementation. The registry never duplicates logic — it points to it.

### 3.2 Default adapters

Each surface has a `Default*Adapter` class that derives the surface-specific projection from the canonical metadata. Most capabilities use only the defaults.

```python
# conversus/registry/adapters/cli.py
class DefaultCLIAdapter(CLIAdapter):
    def render(self, capability):
        # Generate a Click command function from the capability metadata.
        # Maps params to @click.option / @click.argument decorators.
        # Wires the handler import to the command body.
        return click_command_source(capability)


# conversus/registry/adapters/mcp.py
class DefaultMCPAdapter(MCPAdapter):
    def render(self, capability):
        # Generate a @mcp.tool() function with type-annotated parameters
        # derived from the capability's Param list.
        return mcp_tool_source(capability)


# conversus/registry/adapters/plugin.py
class DefaultPluginAdapter(PluginAdapter):
    def render(self, capability):
        # Generate a skills/<name>/SKILL.md file with frontmatter and a
        # body that dispatches to the CLI via Bash.
        return skill_md_source(capability)


# conversus/registry/adapters/mcpb.py
class DefaultMCPBAdapter(MCPBAdapter):
    def render(self, capability):
        # Generate a tools[] entry for the manifest.json.
        return mcpb_tool_entry(capability)
```

### 3.3 Per-surface override adapters

Capabilities that need surface-specific UX instantiate adapter subclasses and pass them to the `Capability(...)` constructor via the `cli_adapter` / `mcp_adapter` / `plugin_adapter` / `mcpb_adapter` kwargs:

```python
# Example: decide needs a richer MCP description for Claude's tool selection
from conversus.registry import DefaultMCPAdapter

class DecideMCPAdapter(DefaultMCPAdapter):
    description = """
    Run an ad-hoc deliberation. Use this when the user describes a
    decision they're facing (e.g. "Postgres or MongoDB?"). Don't use
    for vague questions — the sufficiency classifier rejects them.
    """

decide = Capability(
    name="decide",
    # ... other fields ...
    mcp_adapter=DecideMCPAdapter(),
)
```

**Why constructor kwargs, not class decorators**: the `@DecideCapability.mcp_adapter` syntax required a module-level mutable Capability instance that the decorator could attach to — another violation of principle IX. The constructor-kwarg pattern is a pure function call with no side effects.

Post-construction assignment also works (`decide.mcp_adapter = DecideMCPAdapter()`) because `Capability` has `model_config = ConfigDict(validate_assignment=True)` — this gives capability authors flexibility when an adapter depends on state computed after the initial `Capability(...)` call.

**Subclass `Default<Surface>Adapter`, not the bare ABC**: override adapters should extend the default implementation so they inherit rendering and only need to change the attribute that differs (usually `description`). Subclass the bare ABC only when you want to replace the full `render()` method.

Resolution order at projection time:

1. If `cap.<surface>_adapter` is set, use it
2. Otherwise, use `Default<Surface>Adapter(cap)`

### 3.4 The projector / build script

`scripts/build-surfaces.py` iterates the registry and emits the four surface files:

```python
from capabilities import REGISTRY
from conversus.registry.adapters import (
    DefaultCLIAdapter, DefaultMCPAdapter,
    DefaultPluginAdapter, DefaultMCPBAdapter,
)

def project_to_cli(registry):
    parts = [_cli_preamble()]
    for cap in registry:
        if Surface.CLI not in cap.surfaces:
            continue
        adapter = cap.cli_adapter or DefaultCLIAdapter()
        parts.append(adapter.render(cap))
    return "\n\n".join(parts)


def project_to_mcp(registry):
    # Same pattern for MCP server
    ...


def project_to_plugin_skills(registry, output_dir):
    # Writes one SKILL.md per capability
    ...


def project_to_mcpb_manifest(registry, manifest_path):
    # Updates only the tools[] array in manifest.json
    # leaves other fields (display_name, long_description, etc) untouched
    ...


if __name__ == "__main__":
    write("engine/cli/__init__.py", project_to_cli(REGISTRY))
    write("mcp_server.py", project_to_mcp(REGISTRY))
    project_to_plugin_skills(REGISTRY, "claude-code-plugin/skills/")
    project_to_mcpb_manifest(REGISTRY, "desktop-extension/manifest.json")
```

A `Makefile` target wraps this:

```makefile
build-surfaces:
	python scripts/build-surfaces.py
	@echo "Surfaces regenerated. Verify with: pytest && conversus --help"
```

### 3.5 Skip-a-surface support

Capabilities can opt out of surfaces where they don't make sense:

```python
@capability(
    name="login",
    summary="OAuth login for a model provider",
    surfaces=[Surface.CLI, Surface.PLUGIN],   # NOT MCP, NOT MCPB
    params=[Param("provider", str, required=True)],
    handler="conversus.engine.auth:oauth_login",
)
class LoginCapability:
    """OAuth flows need a browser — terminal-only by design."""
```

The projector skips this capability when generating `mcp_server.py` and the `.mcpb` manifest. No empty stubs, no broken tools.

---

## 4. Implementation plan (1 week)

The arbiter's binding day-by-day plan:

### Day 1-2: Registry framework

**Goal**: the `@capability` decorator and base classes exist and can be unit-tested.

- Create `conversus/registry/__init__.py` with public exports
- Create `conversus/registry/capability.py` with the `@capability` decorator + `Capability` class
- Create `conversus/registry/params.py` with `Param` dataclass + `Surface` enum
- Create `conversus/registry/adapters/base.py` with abstract base classes:
  - `CLIAdapter`, `MCPAdapter`, `PluginAdapter`, `MCPBAdapter`
- Create `conversus/registry/registry.py` with `REGISTRY` global + iteration helpers

**Validation**: a unit test that defines a sample `@capability(...)` and asserts:
1. It's registered in `REGISTRY`
2. Its `params`, `surfaces`, and `handler` are accessible
3. Surface-specific adapter overrides can be attached via `@CapName.cli_adapter` decorator

### Day 3-4: Default adapters and projector

**Goal**: a one-capability registry can be projected to all 4 surface files.

- Implement `DefaultCLIAdapter` that emits Click command source code (string-template based, no AST manipulation)
- Implement `DefaultMCPAdapter` that emits `@mcp.tool()` function source
- Implement `DefaultPluginAdapter` that emits a `skills/<name>/SKILL.md` file with YAML frontmatter and a body that dispatches via Bash to the CLI
- Implement `DefaultMCPBAdapter` that emits a `tools[]` entry as JSON
- Write `scripts/build-surfaces.py` that calls the projectors and writes the output files
- Add `make build-surfaces` target

**Validation**: a registry with a single sample capability (e.g., `hello`) is projected to all 4 surfaces. The CLI command runs, the MCP tool registers, the plugin skill loads, the manifest tools[] entry is valid JSON.

### Day 5: Migrate `decide` (proof migration #1)

**Goal**: `decide` works end-to-end via the registry, byte-identical (or functionally equivalent) to the hand-written version.

**Pre-work — extract shared result types** (principle XI, single source of truth):

- Move `CostEstimate`, `DecideResult`, and `_estimate_cost` out of `mcp_server.py` into a neutral module (`engine/results.py`). Do NOT duplicate them into `engine/handlers.py` — the first draft of Day 5 planned "temporary duplication to unblock migration", but principle XI forbids writing the same fact in two places even temporarily.
- Re-export the moved names from `mcp_server.py` for backward compatibility with existing test imports (`linter/test_mcp_server.py`, `engine/tests/test_integration.py`).

**Handler extraction**:

- Create `engine/handlers.py` with `run_decide_cli(question, provider, mode, output_dir, output_format) -> None` and `run_decide_mcp(question, provider, mode, max_launches) -> DecideResult`. Both functions import the result types from `engine.results`, not from `mcp_server`.
- `run_decide_cli` body mirrors the existing `decide` Click callback in `engine/cli/__init__.py` (validation + classification + config + pipeline + parse + render + exit).
- `run_decide_mcp` body mirrors the existing `mcp_server._decide` function.

**Capability declaration**:

- Create `capabilities.py` at the repo root.
- Define `decide = Capability(...)` directly — no decorator. Use `handler="engine.handlers:run_decide_cli"` as the default, with `handlers={Surface.MCP: "engine.handlers:run_decide_mcp"}` for the per-surface override.
- Attach a `DecideMCPAdapter(DefaultMCPAdapter)` subclass with a richer `description` via the `mcp_adapter=` constructor kwarg.
- Use `Param.surfaces=[Surface.MCP]` to scope `max_launches` to MCP only, and `Param.surfaces=[Surface.CLI]` to scope `output_dir` / `output_format` to CLI only.
- Export `CAPABILITIES: list[Capability] = [decide]` at the bottom of the file — the projector reads this explicit list, not a module-level registry.

**Projection and diff**:

- Run `make build-surfaces-dry-run` to preview changes without writing files.
- Run `python scripts/build-surfaces.py --output-dir /tmp/surfaces-day5` to write to a sandbox.
- Diff the generated `engine/cli/__init__.py decide` block against the existing hand-written version.
- Diff the generated `mcp_server.py conversus_decide` function against the existing.
- Adjust the adapter or default until functionally equivalent.

**Validation**:
- `conversus decide "test question" --provider mock` produces identical output via generated vs hand-written
- The generated MCP tool has the same signature as the hand-written one
- All existing tests for `decide` still pass against the generated code
- The constitution's principle XII check: no "dead infrastructure" — every field on the new `Capability` must be consumed by at least one adapter, every adapter class added must be consumed by at least one capability.

### Day 6: Migrate `run` and `validate` (proof migrations #2 and #3)

**Goal**: three capabilities migrated, framework validated.

Per the arbiter's NO list rule #4: **don't build the framework before migrating at least 3 existing capabilities as proof**. These three migrations are non-optional.

- Repeat the migration process for `run` and `validate`
- These are the data-transformation capabilities — they should be the easiest to migrate because they have minimal surface-specific UX
- Both should work with the default adapters (no overrides needed)

**Validation**:
- All existing engine + linter tests pass (1104 total at Day 7 end; 4 pre-existing fixture-missing failures unchanged from baseline)
- `mcp_server.py` regenerated from the registry produces the same 3 tools with the same JSON schemas (Claude Desktop's existing `.mcpb` install continues to work without re-registration)
- Principle XI: ``mcp_server._run_config is engine.handlers.run_mcp``, ``mcp_server._validate_config is engine.handlers.validate_mcp``, ``mcp_server._run_in_process is engine.handlers._run_in_process`` — all verified by identity tests in ``test_day6_run_validate_migration.py``

### Day 7: Migrate remaining capabilities + full validation

**Goal**: all existing capabilities migrated; registry is the single source of truth.

> **Amendment 2026-04-11**: The original spec planned 12+ capabilities
> including discovery tools (`list_modes`, `list_providers`,
> `list_presets`, `list_examples`, `show_docs`). Day 7 migrated the 9
> hand-written CLI commands + the `design` plugin wizard = **10
> capabilities total**. Discovery tools are deferred to a follow-up
> spec — they don't exist yet and adding them is a new feature, not a
> migration. The `init` command has a known divergence: the hand-written
> CLI accepts repeatable ``--runtime a --runtime b`` flags via Click's
> ``multiple=True``; the generated version accepts a comma-separated
> string ``--runtimes "a,b"`` because the registry ``Param`` model does
> not yet support ``multiple=True``. This is tracked as a framework
> polish item (``Param.multiple`` support).

**Completed**:

- Migrated `login`, `logout`, `status` (auth/setup — CLI + Plugin surfaces)
- Migrated `init` (project initialization — CLI + Plugin, comma-separated runtimes divergence noted above)
- Migrated `context` (debug context detection — CLI-only)
- Migrated `mcp` (stdio server launcher — CLI-only meta-command)
- Defined `design` capability with `surfaces=[Surface.PLUGIN]` only. Uses a `DesignPluginAdapter` override that reads the existing 153-line hand-written SKILL.md verbatim from `claude-code-plugin/skills/design/SKILL.md`. The projector writes it back unchanged — NO list rule #1 satisfied.
- Patched `desktop-extension/manifest.json` tools[] from the registry (still 3 tools: decide/run/validate — the other capabilities don't opt into MCPB)

**Handler extraction**: all 6 new CLI handlers (`login_cli`, `logout_cli`, `status_cli`, `context_cli`, `mcp_cli`, `init_cli`) added to `engine/handlers.py`. These are CLI-only — no MCP variants because the capabilities don't project to MCP.

**Validation**:
- 1104 engine + linter tests pass (4 pre-existing fixture-missing failures unchanged from baseline)
- Generated CLI has 9 commands matching the hand-written set exactly: `context`, `decide`, `init`, `login`, `logout`, `mcp`, `run`, `status`, `validate`
- Generated MCP server has 3 tools matching the hand-written set: `conversus_decide`, `conversus_run`, `conversus_validate`
- Plugin projection produces 9 SKILL.md files (8 generated + 1 hand-written `design` via override adapter)
- MCPB manifest tools[] array has 3 entries (only the MCP-opted capabilities)
- All principle XI single-source-of-truth proofs remain green

**Not completed (deferred)**:
- Discovery capabilities (`list_modes`, `list_providers`, `list_presets`, `list_examples`, `show_docs`) — new features, not migrations. Belong in a follow-up spec.
- `Param.multiple` support for repeatable Click options — framework polish item.
- `Param.flag` override for custom flag names (`--format` instead of `--output-format`).
- `Capability.epilog` for Click command usage examples.
- MCP adapter return type (`-> str` instead of `-> DecideResult`) — cosmetic.

---

## 5. NO list

From the arbiter's binding ruling — five things to explicitly NOT do under this architecture:

1. **Don't auto-generate conversational skill bodies.** The `design` wizard SKILL.md body stays hand-written even after migration. The registry projects metadata; humans write the conversational logic.

2. **Don't try to make all surfaces identical.** Adapters exist precisely so surfaces can have different UX. CLI gets Rich tables; MCP gets verbose tool descriptions for Claude's selection accuracy; plugin gets conversational dispatch hints; manifest gets short tagline-style descriptions for the install dialog. Use the adapter system as designed.

3. **Don't abandon CLI canonical authority.** The registry derives from CLI patterns. CLI is the foundation; other surfaces are projections. If you find yourself adding capabilities to MCP or plugin without a corresponding CLI command, stop and add the CLI command first.

4. **Don't build the framework before migrating at least 3 existing capabilities as proof.** Days 5-6 are non-optional. Without successful migrations of `decide`, `run`, and `validate`, the framework is theoretical and may have hidden assumptions that don't survive contact with real capabilities.

5. **Don't skip capability budgets per surface.** Even with the framework, complexity must remain bounded. Add a `MAX_CAPABILITIES_PER_SURFACE` constant (initial value: 15) so the registry can't accidentally grow to 50 MCP tools and overwhelm Claude's tool selection accuracy.

---

## 6. Trigger to revisit

From the binding ruling, the decision should be revisited if EITHER:

- **Framework maintenance consumes >20% of development time over 3 months**
  - Measured by: time spent updating the projector, fixing adapter bugs, debugging generated code
  - Rolling 3-month window
- **Surface format changes break the projector more than twice per quarter**
  - Triggered by: MCPB schema bumps, Claude Code plugin format changes, Click API changes, etc.
  - Each break = projector rewrite for that surface

If either condition fires, run a new deliberation that re-evaluates registry vs hand-written.

---

## 7. Success criteria

| ID | Criterion | How to verify |
|---|---|---|
| **SC-001** | All 12 existing CLI capabilities are defined in the registry by end of Day 7 | `grep -c "^@capability" capabilities.py` returns 12+ |
| **SC-002** | `make build-surfaces` regenerates all 4 surface files from the registry without errors | Exit code 0; generated files present |
| **SC-003** | All 977 existing tests pass against the regenerated surface code | `pytest engine/tests/` exit code 0 |
| **SC-004** | At least 3 capabilities (`decide`, `run`, `validate`) work end-to-end on all 4 surfaces via the regenerated code | Manual smoke tests + existing test suite |
| **SC-005** | Adding a new capability requires editing only `capabilities.py` (and optionally one adapter file) — never the 4 generated surface files | Follow the workflow for a sample new capability and confirm it lights up on all targeted surfaces |
| **SC-006** | Desktop Extension users can access the discovery, auth, and design capabilities they previously could not | Reinstall the regenerated `.mcpb` in Claude Desktop and verify tools list includes the new capabilities |
| **SC-007** | The `.mcpb` bundle's existing 3 tools (`conversus_decide`, `conversus_run`, `conversus_validate`) keep their exact signatures so Claude Desktop's cached MCP schemas don't break | Diff generated MCP tool signatures against hand-written ones; require zero schema changes for the 3 originals |
| **SC-008** | Generated files have a header comment marking them as build artifacts and pointing to `capabilities.py` | All 4 generated files start with `# AUTO-GENERATED BY scripts/build-surfaces.py — DO NOT EDIT` |
| **SC-009** | A pre-commit hook fails the commit if a generated file is edited without re-running `make build-surfaces` | Hook installed and tested |

---

## 8. Files affected

### New files

| Path | Purpose |
|---|---|
| `conversus/registry/__init__.py` | Public exports |
| `conversus/registry/capability.py` | `@capability` decorator + `Capability` class |
| `conversus/registry/params.py` | `Param` dataclass + `Surface` enum |
| `conversus/registry/registry.py` | `REGISTRY` global + iteration helpers |
| `conversus/registry/adapters/__init__.py` | Adapter exports |
| `conversus/registry/adapters/base.py` | Abstract adapter base classes |
| `conversus/registry/adapters/cli.py` | `DefaultCLIAdapter` |
| `conversus/registry/adapters/mcp.py` | `DefaultMCPAdapter` |
| `conversus/registry/adapters/plugin.py` | `DefaultPluginAdapter` |
| `conversus/registry/adapters/mcpb.py` | `DefaultMCPBAdapter` |
| `capabilities.py` | The registry — every capability declared here |
| `scripts/build-surfaces.py` | The projector |
| `Makefile` | `make build-surfaces` target |
| `.git/hooks/pre-commit` (or `.pre-commit-config.yaml`) | Hook that detects manual edits to generated files |

### Files that become generated artifacts (after Day 7)

These are still committed to git, but no longer hand-edited. Each gets a header comment marking it as auto-generated.

| Path | What's generated |
|---|---|
| `engine/cli/__init__.py` | All Click commands derived from the registry |
| `mcp_server.py` | All `@mcp.tool()` functions derived from the registry |
| `claude-code-plugin/skills/*/SKILL.md` | All skill files except `design/SKILL.md` (hand-written body) |
| `desktop-extension/manifest.json` (`tools[]` only) | The tools array; other fields stay hand-written |

### Files NOT touched

- `engine/` (everything except `cli/`) — the deliberation engine internals
- `conversus/schemas/`, `conversus/plugins/`, `conversus/domains/`
- `deliberations/` (all deliberation outputs)
- `docs/` (all documentation)
- `tests/` (all existing tests)
- `desktop-extension/server/main.py` (bootstrap)
- `desktop-extension/build.sh` (bundle build)
- `.github/workflows/` (CI)

---

## 9. Open questions

These need resolution during implementation but don't block the spec being approved:

1. **Plugin skill body generation**: defaults will produce a minimal SKILL.md that wraps the CLI command via Bash. Is this enough for non-trivial slash commands like `init` (which has runtime detection logic) and `decide` (which benefits from sufficiency classifier hints)? Or do most need explicit plugin adapters? **Resolve during Day 4-7.**

2. **Backward compatibility for MCP schemas**: should the generated `mcp_server.py` preserve the existing 3 tools' EXACT JSON schemas so existing `.mcpb` installations don't need re-registration? Likely yes — backward-compat is important for MCP clients that have cached schemas. **Track via SC-007.**

3. **Versioning of generated files**: should generated files have a header comment with the registry hash, or just a timestamp, or just "auto-generated"? Hash gives perfect change detection but adds noise to diffs. **Default: no hash, just a static comment. Revisit if drift occurs.**

4. ~~**Adapter discovery mechanism**: should adapters be attached via decorator (`@CapName.mcp_adapter`) or via a separate adapter module that imports the capability and registers?~~ **Resolved 2026-04-11 by constitutional adoption.** Adapters are attached via constructor kwargs (`Capability(..., mcp_adapter=DecideMCPAdapter())`) or post-construction assignment (`decide.mcp_adapter = DecideMCPAdapter()`). The class-decorator form was dropped because it required the mutable module-level Capability instance that principle IX forbids.

5. **What happens to existing `claude-code-plugin/skills/conversus/SKILL.md`?** That's the old monolithic skill we already deleted. Confirm it stays deleted and the registry is the source for all 8 plugin slash commands.

---

## 10. Sources

| Source | Use |
|---|---|
| `CONSTITUTION.md` | **Governing document** — principles IX (no mutable global state, Pydantic, StrEnum, no Any), XI (single source of truth), XII (no dead infrastructure), XIV (spec-implementation parity) bound the Day 1-4 rework and the Day 5 result-type extraction |
| `deliberations/capability-exposure/proposal.md` | Original 5-question proposal that surfaced the duplication problem |
| `deliberations/capability-exposure/output/architecture-purist/revision.md` | Architecture-purist's final position — close to the adapter pattern but never named it |
| `deliberations/capability-exposure/output/summary/final.md` | First synthesis — converged on principles but failed to commit to a pattern |
| `deliberations/capability-exposure-followup/proposal.md` | Focused Q6 follow-up that named the adapter pattern explicitly |
| `deliberations/capability-exposure-followup/output/summary/final.md` | Second synthesis — picked anti-framework on resource economics |
| `deliberations/capability-exposure-followup/output/arbiter/resolution.md` | **Binding decision** — overrode the synthesis and chose Option A on user-equity grounds |
| `specs/distribution-strategy.md` | Established the 4 distribution surfaces this spec consolidates |
| `docs/developer-guide/gotchas.md` | Agent hand-off memo — subtle bugs and Pydantic behaviors discovered during Day 1-4. Read before touching the registry, the projector, or generated surface files. |

---

## 11. Out of scope

These are intentionally NOT addressed by this spec:

- **New capabilities themselves**. This spec defines HOW capabilities are exposed, not which capabilities should exist. New capabilities (e.g., `export-html`, `compare-deliberations`) are separate features that will use this framework when added.
- **The deliberation engine internals**. Phases, providers, agent dispatch, synthesis logic — none of that changes. The registry is a packaging/projection layer above the engine.
- **Documentation generation**. This spec doesn't auto-generate the docs site from the registry. Docs stay hand-written. (Could be a future spec — `056-docs-from-registry`.)
- **Schema versioning**. If a capability's parameter signature changes, downstream consumers (existing `.mcpb` installations, scripts depending on CLI flags) need to handle the migration manually. This spec doesn't define a schema-evolution policy.
- **Telemetry / analytics**. The registry could be used to instrument capability invocations, but that's out of scope here.

---

## 12. Acceptance

This spec is approved when:

1. The implementation plan has been completed (Day 1-7 above)
2. All success criteria SC-001 through SC-009 pass
3. The trigger conditions in §6 are documented in the project's `MAINTENANCE.md` or equivalent
4. A demo PR shows adding a brand-new capability via the registry that lights up on all 4 surfaces with no hand-edits to generated files
