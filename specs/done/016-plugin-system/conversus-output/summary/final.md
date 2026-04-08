# Synthesis: 016 Plugin System Infrastructure

**Synthesizer**: neutral
**Spec**: 016-plugin-system
**Date**: 2026-03-24

---

## Process Summary

- **Agents**: 3 -- plugin-architect, schema-engineer, spec-compliance
- **Total artifacts**: 16
- **Phase 1 reviews**: 3
- **Phase 2 cross-reviews**: 6
- **Phase 3 revisions**: 3
- **Phase 4 disputes**: 3
- **Recommendations proposed** (Phase 1 total): 21
- **Recommendations withdrawn** (Phase 3): 3
- **Recommendations modified** (Phase 3): 6
- **Recommendations surviving** (Phase 3): 12
- **New recommendations added** (Phase 3): 3
- **Disputes remaining** (Phase 4): 4
- **Convergence points** (Phase 4): 4

---

## Recommendation Scorecard

| # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Challenged By | Convergence | Final Status |
|---|-------|---------------|-------------------|---------------------|---------------|-------------|--------------|
| 1 | plugin-architect | Add features to DeliberationState | P1 | Modified (untyped dict) | spec-compliance DC-1 | None | Disputed |
| 2 | plugin-architect | Remove config param from execute() | P2 | Modified (simplified) | None | Unanimous | Accepted |
| 3 | plugin-architect | Add hook param to execute() | P2 | Withdrawn | schema-engineer NR-1 | None | Rejected |
| 4 | plugin-architect | Named plugin class resolution | P2 | Surviving | schema-engineer T-3 | None | Disputed |
| 5 | plugin-architect | Define engine integration points | P1 | Surviving | None | Unanimous | Accepted |
| 6 | plugin-architect | Add POST_ITERATION hook | P3 | Withdrawn | spec-compliance T-1, schema-engineer T-2 | None | Rejected |
| 7 | plugin-architect | Plugin-to-plugin data passing | P3 | Withdrawn | schema-engineer DC-2, spec-compliance T-2 | None | Rejected |
| 8 | plugin-architect | Align AgentState with AgentFeatures | P2 | Modified (remove positions) | schema-engineer O-1 | Unanimous | Accepted-Modified |
| 9 | schema-engineer | PluginFacingConfig model | P2 | Modified (extra=allow) | spec-compliance T-1 | None | Disputed |
| 10 | schema-engineer | Validate Plugin.name/hooks in __init__ | P1 | Surviving | None | Bilateral | Accepted |
| 11 | schema-engineer | Typed load_plugins() signature | P2 | Surviving | None | None | Accepted |
| 12 | schema-engineer | Minimal Position model or remove | P3 | Modified (remove) | plugin-architect R-8 | Unanimous | Accepted-Modified |
| 13 | schema-engineer | Plugin version field | P3 | Surviving | None | None | Accepted |
| 14 | schema-engineer | Only create plugins/ dir on success | P3 | Surviving | None | None | Accepted |
| 15 | schema-engineer | Add __all__ to base.py | P3 | Surviving | None | None | Accepted |
| 16 | spec-compliance | Wire plugins into engine pipeline | P1 | Surviving | None | Unanimous | Accepted |
| 17 | spec-compliance | Amend FR-012 package naming | P1 | Surviving | None | Unanimous | Accepted |
| 18 | spec-compliance | Integration test (as part of R-16) | P1 | Modified (folded into R-16) | schema-engineer T-2 | None | Accepted-Modified |
| 19 | spec-compliance | Only create plugins/ dir on output | P3 | Surviving | None | None | Accepted |
| 20 | spec-compliance | Document engine integration contract | P2 | Surviving | None | None | Accepted |
| NR-1 | schema-engineer | Remove config param from execute() | P1 | New | None | Unanimous | Accepted |
| NR-2 | spec-compliance | Remove config param from execute() | P1 | New | None | Unanimous | Accepted (duplicate of NR-1) |
| NR-3 | spec-compliance | Add plugins field to EngineConfig | P1 | New | None | None | Accepted |

---

## Dangerous Contradictions Found

**Resolved Contradictions**:

1. **execute() config parameter** -- Plugin-architect proposed removing or renaming. Schema-engineer proposed removing. Spec-compliance endorsed removal. Resolution: unanimous agreement to simplify signature to `execute(self, state: DeliberationState) -> PluginResult`.

2. **AgentState.positions field** -- Schema-engineer flagged as dead. Plugin-architect proposed alignment with AgentFeatures, then agreed removal is cleaner. Spec-compliance acknowledged. Resolution: remove the field.

3. **POST_ITERATION and PluginContext** -- Plugin-architect proposed both. Schema-engineer and spec-compliance identified as scope creep. Resolution: withdrawn by plugin-architect. Defer to specs that need them.

4. **FR-012 package naming** -- Same pattern as spec 015's FR-014. Resolution: amend to `conversus.plugins`.

**Unresolved Contradictions**:

1. **FeatureSet on DeliberationState** -- Plugin-architect wants `features: dict[str, Any] | None` added now. Spec-compliance wants deferral to spec 017. Assessment below.

2. **PluginFacingConfig** -- Schema-engineer wants typed config. Spec-compliance prefers dict. Assessment below.

---

## Systemic Contradictions

- **Framework scope boundary**
  - **Manifests in**: Features field dispute, PluginFacingConfig dispute, POST_ITERATION withdrawal.
  - **Root cause**: Spec 016 is simultaneously "the framework foundation" (no dependencies, minimal) and "the infrastructure plugins need" (must provide useful state). These goals conflict when plugin needs (features, typed config) require framework additions.
  - **Implication for spec**: Define an explicit scope boundary in the spec: "Spec 016 provides hook mechanism, state interface, and output namespace. Data enrichment of the state (features, typed config) is the responsibility of consuming specs or bridge specs." This prevents scope creep while documenting where enrichment belongs.

- **Engine integration ownership ambiguity**
  - **Manifests in**: FR-001/FR-003/FR-006 partial compliance, plugin-architect's "missing wiring" observation, spec-compliance's "must be spec 016 deliverable" position.
  - **Root cause**: The spec defines what the orchestrator must do but the orchestrator code is in a different module (`engine/phases.py`). The plugin package is framework; the engine is the caller. The spec does not clearly assign ownership of the glue code.
  - **Implication for spec**: Add a "Engine Integration" section to the spec that provides the exact code changes needed in `engine/phases.py`. This makes the deliverable unambiguous and testable.

- **Model duplication between plugins and schemas packages**
  - **Manifests in**: AgentState vs. AgentFeatures overlap, DeliberationState.config vs. EngineConfig, positions field death.
  - **Root cause**: The plugins package and schemas package were designed independently. AgentState was created for plugins before AgentFeatures was created for extraction. The packages do not share types because they do not import from each other.
  - **Implication for spec**: When specs 017-019 bridge features and plugins, they should establish the canonical type direction (schemas types are canonical; plugins types are views). This prevents further duplication.

---

## Convergence Achieved

- **Engine integration is the critical deliverable** -- Strength: Unanimous
  - **Agreed recommendation**: Add `plugins` field to EngineConfig. Call `load_plugins()` at startup. Call `execute_hooks()` at PRE_EXECUTION (after config), POST_PHASE_5 (after synthesis), POST_DELIBERATION (after all rounds), POST_ARBITRATION (after arbitration).
  - **Supporting agents**: plugin-architect (R-5), schema-engineer (SA-5), spec-compliance (R-1)
  - **Evidence basis**: FR-006 says "MUST call execute()." The orchestrator does not call it.
  - **Pre-existing or earned**: Pre-existing -- all three reviews identified it in Phase 1.

- **Amend FR-012 to conversus.plugins** -- Strength: Unanimous
  - **Agreed recommendation**: Change FR-012 to reference `conversus.plugins` namespace.
  - **Supporting agents**: All three reviewers.
  - **Evidence basis**: The package ships as `conversus.plugins`, not `conversus-plugins`.
  - **Pre-existing or earned**: Pre-existing -- identified in Phase 1.

- **Remove config parameter from execute()** -- Strength: Unanimous
  - **Agreed recommendation**: Simplify to `execute(self, state: DeliberationState) -> PluginResult`. Plugins use `self.plugin_config` for plugin-specific config and `state.config` for deliberation config.
  - **Supporting agents**: plugin-architect (R-2), schema-engineer (NR-1), spec-compliance (NR-1/NR-2)
  - **Evidence basis**: The current triple-config pattern (state.config, config param, self.plugin_config) is unanimously agreed to be confusing.
  - **Pre-existing or earned**: Earned -- emerged through cross-review when all three independently endorsed.

- **Remove dead AgentState.positions** -- Strength: Unanimous
  - **Agreed recommendation**: Remove `positions: list[dict[str, Any]]` from AgentState. No code populates it.
  - **Supporting agents**: All three reviewers.
  - **Evidence basis**: Schema-engineer O-1 identified the field as dead.
  - **Pre-existing or earned**: Earned -- schema-engineer identified in Phase 1, all agreed by Phase 3.

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
## Remaining Disputes

- **Dispute: FeatureSet field on DeliberationState**
  - **Positions**: Plugin-architect wants `features: dict[str, Any] | None = None` added to DeliberationState in spec 016. Spec-compliance wants deferral to spec 017, arguing spec 016 should remain dependency-free. Cite: plugin-architect disputes R-1, spec-compliance disputes R-1.
  - **Arguments**: Plugin-architect argues every numerical plugin will need features, and the framework should provide the data pathway. Spec-compliance argues spec 016 declares "Depends On: None" and the features field is a data concern, not a framework concern. Plugins can read features from `output_dir / "features.json"`.
  - **Synthesizer assessment**: Spec-compliance's position is stronger. Spec 016 is the framework foundation, and its "Depends On: None" is a deliberate design choice that should be preserved. The features field is a data enrichment that belongs in the consuming spec, not the framework. Plugin-architect's concern about "filesystem scavenging" is mitigated by `output_dir` being on the state -- reading `output_dir / "features.json"` is not scavenging, it is reading a known artifact from a known location. When spec 017 is implemented, it can add `features` to the state if needed.
  - **Recommended resolution**: Defer the features field to spec 017. Document in spec 016 that `output_dir` on DeliberationState is the canonical mechanism for plugins to access deliberation artifacts. If spec 017 finds this insufficient, it can propose adding features to the state.

- **Dispute: PluginFacingConfig typed model**
  - **Positions**: Schema-engineer wants `PluginFacingConfig` model with typed fields and `extra="allow"`. Spec-compliance prefers `dict[str, Any]` for simplicity. Plugin-architect does not directly oppose either. Cite: schema-engineer disputes R-1, spec-compliance disputes flexibility statement.
  - **Arguments**: Schema-engineer argues typed access prevents runtime KeyError bugs. Spec-compliance argues the typed model creates a maintenance obligation.
  - **Synthesizer assessment**: Schema-engineer's position is marginally stronger. The `PluginFacingConfig` with `extra="allow"` provides typed access to stable fields (mode, rounds, iterations) without blocking unknown fields. The maintenance cost is real but minimal: these fields have been stable across all conversus specs. The risk of `config["moed"]` typo bugs in plugin code is concrete and immediate. However, this is a P2 improvement, not a P1 blocker.
  - **Recommended resolution**: Adopt `PluginFacingConfig` with `extra="allow"`. Define it in the plugins package, not the engine. Include `mode: str`, `rounds: int = 1`, `iterations: int = 1`, `agent_names: list[str] = []`. Replace `DeliberationState.config: dict[str, Any]` with `DeliberationState.config: PluginFacingConfig`.

- **Dispute: Named plugin class resolution**
  - **Positions**: Plugin-architect wants `class_name: str | None` on PluginConfigEntry. Schema-engineer suggests deferral. Cite: plugin-architect disputes R-2, schema-engineer T-3.
  - **Arguments**: Plugin-architect argues the first-found behavior is nondeterministic for multi-class modules. Schema-engineer argues no multi-class module exists yet.
  - **Synthesizer assessment**: Plugin-architect's correctness argument is sound: `dir()` ordering is alphabetical, making the behavior nondeterministic by naming rather than by intent. However, the one-plugin-per-package convention makes this a theoretical issue with no current impact. The fix is low-cost (one config field, one getattr call) and prevents a class of bugs.
  - **Recommended resolution**: Add `class_name: str | None = None` to PluginConfigEntry. When present, `_find_plugin_class()` resolves the named class directly. This is a defensive improvement with no downside.

- **Dispute: FR-001 compliance level**
  - **Positions**: Spec-compliance marks FR-001 as PARTIALLY MET (config not consumed by engine). Schema-engineer argues FR-001 is MET at the parsing layer. Cite: spec-compliance disputes R-2, schema-engineer DC-1.
  - **Arguments**: Spec-compliance argues "allow declaring plugins" implies the declaration is actionable. Schema-engineer separates parsing from consumption.
  - **Synthesizer assessment**: Spec-compliance's reading is more faithful to the spec's intent. FR-001 says "MUST allow declaring plugins" -- this implies the declaration has an effect. A field that is parsed but silently ignored does not "allow" anything meaningful. PARTIALLY MET is the correct assessment until engine integration is complete.
  - **Recommended resolution**: Record FR-001 as PARTIALLY MET. Engine integration (convergence C-1) is the deliverable that completes it.
<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

**P1 -- Must implement** (blocking issues or unanimous convergence):

1. **Wire plugin system into engine pipeline**: Add `plugins: list[PluginConfigEntry] = []` to EngineConfig. Call `load_plugins()` at startup. Call `execute_hooks()` at PRE_EXECUTION, POST_PHASE_5, POST_DELIBERATION, POST_ARBITRATION in `_run_single_round()` and `run_pipeline()`. Include integration test as acceptance criterion. Source: all three reviewers, unanimous convergence.

2. **Remove `config` parameter from Plugin.execute()**: Change ABC signature to `execute(self, state: DeliberationState) -> PluginResult`. Update `execute_hooks()` to call `plugin.execute(state)`. Update all test plugins. Source: all three reviewers, unanimous convergence.

3. **Remove `positions` from AgentState**: Remove `positions: list[dict[str, Any]]` from AgentState. Update spec Section 2 DeliberationState definition. Source: all three reviewers, unanimous convergence.

4. **Amend FR-012**: Change to "The plugin base class, hook points, state objects, and result type MUST ship in the `conversus.plugins` package." Update import path examples. Source: all three reviewers, unanimous convergence.

5. **Add Plugin.name/hooks validation in __init__**: Raise TypeError if class attributes are missing or empty. Source: schema-engineer R-2, plugin-architect agreement.

**P2 -- Should implement** (majority convergence or strong single-agent case):

1. **Adopt PluginFacingConfig with extra="allow"**: Define `PluginFacingConfig` model in plugins package with `mode`, `rounds`, `iterations`, `agent_names`. Replace `DeliberationState.config: dict[str, Any]`. Source: schema-engineer R-1, synthesizer assessment.

2. **Type load_plugins() to accept list[PluginConfigEntry]**: Change signature and update all callers/tests. Source: schema-engineer R-3.

3. **Add `class_name: str | None = None` to PluginConfigEntry**: Enable named class resolution for multi-class modules. Source: plugin-architect R-4, synthesizer assessment.

4. **Document engine integration contract**: Provide exact hook insertion points in engine/phases.py, with code examples. Source: spec-compliance R-5.

5. **Add `plugins` field to EngineConfig**: Part of the engine integration (P1-1), but documented separately as a config schema change. Source: spec-compliance NR-3.

**P3 -- Consider implementing** (bilateral agreement or strong but disputed):

1. **Add `version: str = "0.1.0"` to Plugin class**: Include version in output JSON. Source: schema-engineer R-5.

2. **Only create plugins/ dir when plugins produce output**: Move mkdir inside success path. Source: schema-engineer R-7.

3. **Add `__all__` to base.py**: Declare public API. Source: schema-engineer R-8.

4. **Add AgentState.positions removal to spec Section 2**: Documentation update. Source: convergence C-4.

---

## Key Concessions

**plugin-architect**:
- Withdrew R-3 (hook parameter on execute), R-6 (POST_ITERATION hook), and R-7 (PluginContext). All three were correctly identified as scope creep by cross-reviewers. Significant intellectual honesty in withdrawing three recommendations that went beyond the spec's framework scope.
- Modified R-1 (FeatureSet field) from typed FeatureSet to untyped dict based on schema-engineer's cross-package dependency concern.
- Modified R-8 (AgentState alignment) from alignment-with-AgentFeatures to removal-of-positions based on schema-engineer's dead-field analysis.

**schema-engineer**:
- Modified R-1 (PluginFacingConfig) to include `extra="allow"` based on spec-compliance's forward-compatibility concern.
- Modified R-4 (Position model) to simple removal based on plugin-architect's revised position.

**spec-compliance**:
- Modified R-3 (integration test) from standalone recommendation to acceptance criterion for engine integration, based on schema-engineer's feedback that the test depends on integration being done first.
- Made no significant concessions on FR compliance assessments, maintaining PARTIALLY MET for FR-001 throughout the process.
