# Schema Engineer Disputes — 016 Plugin System Infrastructure

**Role**: schema-engineer
**Phase**: 4 — Disputes
**Date**: 2026-03-24

---

## Remaining Disputes

- **Dispute: PluginFacingConfig model — typed config vs. dict passthrough**
  - **My claim**: Replace `DeliberationState.config: dict[str, Any]` with a typed `PluginFacingConfig` model that has `mode: str`, `rounds: int`, `iterations: int`, `agent_names: list[str]`, and `extra="allow"`. Cite: schema-engineer revision R-1.
  - **Opposing position(s)**: Spec-compliance T-1 argues the typed model creates a maintenance coupling. Plugin-architect does not directly oppose but proposes complementary changes.
  - **Why I will not concede**: The `dict[str, Any]` config is the most common source of plugin author errors: accessing `config["mode"]` with a typo key (`config["moed"]`) fails silently (returns None or KeyError at runtime). A typed model catches this at construction time. The `extra="allow"` flag preserves backward compatibility -- unknown fields pass through. The maintenance cost is minimal: the fields (mode, rounds, iterations) are stable deliberation parameters that have not changed across 16 specs.
  - **Counter-argument to their position**: Spec-compliance argues about coupling, but the PluginFacingConfig is defined in the plugins package, not the engine. It is a plugin-facing view of the config, not a mirror of EngineConfig. If the engine adds a field, the PluginFacingConfig does not need to be updated -- the field passes through via `extra="allow"`.
  - **Proposed resolution path**: Add PluginFacingConfig to the plugins package. The orchestrator constructs it from the raw config dict when building DeliberationState. The synthesizer should decide.

- **Dispute: load_plugins() typed signature timing**
  - **My claim**: Change `load_plugins(list[dict])` to `load_plugins(list[PluginConfigEntry])` now. Cite: schema-engineer R-3.
  - **Opposing position(s)**: No reviewer opposes this directly, but the change requires updating all test code that calls `load_plugins()` with raw dicts.
  - **Why I will not concede**: The test migration is mechanical (10 minutes of work for the existing test suite). The type safety benefit is immediate: callers cannot pass unvalidated config to the loader.
  - **Counter-argument to their position**: N/A -- no active opposition.
  - **Proposed resolution path**: Adopt the typed signature. Update tests. The synthesizer should include this in actionable changes.

---

## Convergence

- **Converged: Engine integration is the critical deliverable**
  - **Shared position**: Wire execute_hooks() into the engine pipeline.
  - **Agreeing agents**: All three reviewers.
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1.

- **Converged: Amend FR-012 to conversus.plugins**
  - **Shared position**: Spec references actual namespace.
  - **Agreeing agents**: All three reviewers.
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1.

- **Converged: Remove config param from execute()**
  - **Shared position**: Simplified signature: `execute(self, state) -> PluginResult`.
  - **Agreeing agents**: All three reviewers.
  - **Strength**: Unanimous
  - **Path to convergence**: Emerged through cross-review. All three independently endorsed in Phase 3.

- **Converged: Remove AgentState.positions**
  - **Shared position**: Dead field. Remove it.
  - **Agreeing agents**: All three reviewers.
  - **Strength**: Unanimous
  - **Path to convergence**: Schema-engineer identified in Phase 1; all agreed by Phase 3.

- **Converged: Validate Plugin.name/hooks in __init__**
  - **Shared position**: Early validation catches missing class attributes.
  - **Agreeing agents**: schema-engineer (R-2), plugin-architect (T-1)
  - **Strength**: Bilateral
  - **Path to convergence**: Proposed Phase 1, agreed Phase 2.

---

## Final Position Statement

**Non-Negotiables**:
- Remove config parameter from Plugin.execute(). The triple-config pattern is universally agreed to be wrong. This must be part of the spec 016 deliverables.
- Remove dead AgentState.positions field. False API surfaces are worse than missing fields.

**Flexibility**:
- PluginFacingConfig vs. dict config. I strongly prefer typing, but will accept `dict[str, Any]` with documented field names if the synthesizer determines the typing is premature.
- Version field on Plugin (R-5). Useful but not blocking. Can be added later.
