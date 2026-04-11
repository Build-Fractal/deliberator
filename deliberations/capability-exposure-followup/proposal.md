# Capability Exposure: Binding Decision on Q6

## What this deliberation is

The previous deliberation at `deliberations/capability-exposure/` produced a synthesis that converged on principles ("CLI is canonical", "eliminate duplication via shared metadata", "capacity limits") but **failed to commit to a specific architectural pattern**. The synthesis acknowledged "irreducible tensions" around registry vs. CLI-first vs. discovery and recommended "balanced trade-offs" — which is a non-answer.

The architecture-purist's final revision shifted from "pure build-time generation" to "Hybrid runtime/build-time" with bounded surface-specificity — close to the adapter pattern but never named explicitly.

**This follow-up deliberation does ONE thing**: pick a binding answer to Q6 from the previous proposal — should conversus adopt the **registry + per-surface adapters** pattern, or keep one of the alternatives?

## Inputs (read these)

- The original proposal: `../capability-exposure/proposal.md`
- Each agent's final revision: `../capability-exposure/output/{architecture-purist,non-tech-user-advocate,developer-power-user,pragmatist-maintainer}/revision.md`
- The synthesis: `../capability-exposure/output/summary/final.md`

## The question

**Q**: Adopt the registry + per-surface adapters pattern (define each capability once in a Python registry; provide optional per-surface adapter classes that override the projection only when surface-specific UX matters; build script generates the 4 surface files), OR keep an alternative (hand-written surfaces with discipline, or status quo with no shared metadata)?

## What "registry + adapters" means concretely

```python
# capabilities.py
@capability(
    name="decide",
    summary="Run an ad-hoc deliberation",
    surfaces=[Surface.CLI, Surface.MCP, Surface.PLUGIN, Surface.MCPB],
    params=[Param("question", str, required=True), ...],
    handler=lambda question, provider, mode: engine.run_decide(...),
)
class DecideCapability:
    """Default adapters cover all 4 surfaces. Override only when needed."""

@DecideCapability.mcp_adapter
class DecideMCPAdapter(MCPAdapter):
    description = "Verbose disambiguation hint for Claude's tool selection..."

@DecideCapability.cli_adapter
class DecideCLIAdapter(CLIAdapter):
    def render_result(self, result):
        return rich_table_from(result)
```

A `make build-surfaces` step reads the registry, applies adapters (default or custom), and generates `engine/cli/__init__.py`, `mcp_server.py`, `claude-code-plugin/skills/`, and `desktop-extension/manifest.json`. Hand-editing those generated files is forbidden — they're build artifacts.

## The three positions

### Option A: Registry + adapters (Q6 from previous proposal)

- **Cost**: 3-4 days to build the framework, default adapters, projector, and migrate the existing 12 capabilities
- **Payoff**: every new capability is one registry entry. Drift between surfaces becomes architecturally impossible.
- **Risk**: framework code becomes a maintenance burden of its own. If the surface formats change (new MCPB version, new plugin schema), the projector has to be updated alongside.

### Option B: Hand-written surfaces with discipline

- **Cost**: 0 days framework, but ongoing cost per capability = ~30 minutes of edit-4-files-carefully
- **Payoff**: maximum flexibility per surface, no framework abstractions to learn
- **Risk**: drift is inevitable as the project grows. By 25 capabilities × 4 surfaces = 100 maintained projections, drift becomes a real bug source.

### Option C: Status quo

- **Cost**: 0 days
- **Payoff**: nothing changes
- **Risk**: same as Option B but without even the discipline. Current state.

## Decision criteria

The deliberation must answer:

1. **Which option** at conversus's CURRENT scale (12 capabilities, 4 surfaces, ~5 active developers, 0 paid users)?
2. **The trigger** to revisit: under what condition would a chosen "no" become "yes" in the future? (e.g., "if we hit N capabilities", "if drift causes X bug reports", "if someone donates Y days of refactor time")
3. **A first-week implementation plan** for whichever option wins — what to build first, what to test, what to commit
4. **A NO list** — under the chosen option, what should we explicitly NOT do? (e.g., if Option A, don't try to auto-generate skill bodies; if Option B, don't try to share metadata via imports)

## Constraints

- Small team — 1-2 active maintainers
- Pre-1.0, pre-public, zero paid users
- 4 distribution surfaces already exist (CLI, MCP, plugin, .mcpb)
- 12 capabilities already exist across them with some duplication
- The team's bandwidth for "infrastructure work that doesn't ship features" is limited
- Whatever the answer is, we live with it for at least the next 6 months
