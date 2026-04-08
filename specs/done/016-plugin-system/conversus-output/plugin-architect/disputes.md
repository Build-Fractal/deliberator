# Plugin Architect Disputes — 016 Plugin System Infrastructure

**Role**: plugin-architect
**Phase**: 4 — Disputes
**Date**: 2026-03-24

---

## Remaining Disputes

- **Dispute: FeatureSet field typing on DeliberationState — untyped dict vs. typed import**
  - **My claim**: Adding `features: dict[str, Any] | None = None` (my revision R-1) is the right approach: it provides the data pathway without creating a cross-package import dependency. Cite: plugin-architect revision R-1.
  - **Opposing position(s)**: Schema-engineer's R-1 (PluginFacingConfig) does not directly address features, but their DC-1 raises the question of whether the plugins package may import from schemas. Spec-compliance DC-1 argues the field should not be added at all in spec 016 because it introduces a spec 015 dependency.
  - **Why I will not concede**: Without a features pathway on DeliberationState, every numerical plugin (specs 017-019) must independently discover, read, and parse feature files. This is the pattern the spec's design principle 4 ("Data flows one direction") exists to prevent: plugins should receive data from the orchestrator, not scavenge it from the filesystem. The untyped `dict[str, Any]` avoids the import dependency concern while providing the pathway.
  - **Counter-argument to their position**: Spec-compliance argues spec 016 should remain dependency-free. But the field is `None` by default and optional. A spec 016 that does not mention features is a spec 016 that forces every downstream plugin to reinvent feature discovery. The framework's job is to provide infrastructure that plugins need; features are infrastructure.
  - **Proposed resolution path**: Add the untyped `features: dict[str, Any] | None = None` field. Document that the orchestrator populates it when feature extraction is available (spec 015 is implemented). Plugins that need typed access import FeatureSet themselves. The synthesizer should decide.

- **Dispute: Named plugin class resolution — now vs. defer**
  - **My claim**: Adding an optional `class_name` field to plugin config is a low-cost improvement that prevents the first-found ambiguity. Cite: plugin-architect R-4.
  - **Opposing position(s)**: Schema-engineer T-3 argues this should be deferred until a real multi-class package exists. The current one-plugin-per-package convention works.
  - **Why I will not concede**: The first-found behavior via `dir()` iteration is nondeterministic: `dir()` returns names in alphabetical order, so the class loaded depends on naming. A module with `AlphaPlugin` and `BetaPlugin` always loads `AlphaPlugin`, regardless of which the config intends. This is a correctness bug, not a feature request.
  - **Counter-argument to their position**: "Wait for a real case" is reasonable for new features but not for correctness fixes. The first-found behavior is incorrect by construction when a module has multiple Plugin subclasses.
  - **Proposed resolution path**: Add `class_name: str | None = None` to PluginConfigEntry. When present, `_find_plugin_class()` uses `getattr(module, class_name)` instead of `dir()` iteration. The synthesizer should decide.

---

## Convergence

- **Converged: Engine integration is the critical deliverable**
  - **Shared position**: The engine must call `load_plugins()` at startup and `execute_hooks()` at each lifecycle hook point. This moves FR-001, FR-003, and FR-006 to MET.
  - **Agreeing agents**: All three reviewers.
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1.

- **Converged: Amend FR-012 package naming to conversus.plugins**
  - **Shared position**: The spec should reference `conversus.plugins`, not `conversus-plugins`.
  - **Agreeing agents**: All three reviewers.
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1.

- **Converged: Remove config parameter from Plugin.execute()**
  - **Shared position**: Simplify to `execute(self, state: DeliberationState) -> PluginResult`. Plugins use `self.plugin_config` and `state.config`.
  - **Agreeing agents**: plugin-architect (R-2 revised), schema-engineer (NR-1), spec-compliance (NR-1)
  - **Strength**: Unanimous
  - **Path to convergence**: Plugin-architect proposed in Phase 1; schema-engineer and spec-compliance independently endorsed in Phase 3.

- **Converged: Remove dead AgentState.positions field**
  - **Shared position**: The field is never populated and is superseded by the features pathway. Remove it.
  - **Agreeing agents**: plugin-architect (R-8 revised), schema-engineer (R-4 revised, O-1), spec-compliance (T-2)
  - **Strength**: Unanimous
  - **Path to convergence**: Schema-engineer identified as dead in Phase 1; all agreed in Phase 3.

- **Converged: Validate Plugin.name and Plugin.hooks at instantiation**
  - **Shared position**: Add validation in Plugin.__init__ to catch missing class attributes early.
  - **Agreeing agents**: schema-engineer (R-2), plugin-architect (T-1 agreement)
  - **Strength**: Bilateral
  - **Path to convergence**: Schema-engineer proposed in Phase 1; plugin-architect agreed in Phase 2.

---

## Final Position Statement

**Non-Negotiables**:
- Engine integration (R-5). The plugin system without engine wiring is a framework without a runtime. FR-006 is NOT MET without it.
- Remove config parameter from execute() (R-2 revised). The triple-config pattern is confusing and every cross-review agrees the simplification is correct.

**Flexibility**:
- FeatureSet field typing. I prefer `dict[str, Any]` for dependency-free feature passing, but will accept deferral to spec 017 if the synthesizer decides spec 016 should remain features-agnostic.
- Named class resolution (R-4). I believe it is a correctness fix, but will accept deferral if the synthesizer considers it scope creep.
