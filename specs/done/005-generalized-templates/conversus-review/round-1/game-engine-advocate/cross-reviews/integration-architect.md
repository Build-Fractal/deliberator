# Cross-Review: integration-architect's Phase 1 Review

**Cross-reviewer**: game-engine-advocate (spec 007)
**Reviewing**: integration-architect's review of spec 005
**Date**: 2026-03-21

---

## Dangerous Contradictions

### 1. Runtime linter framing vs. plugin-extensible linter

Integration-architect correctly identifies that the spec's framing of the linter as a "development-time-only tool" is wrong (Off-Base Assumptions, item 1), noting that SKILL.md Step 3 already treats validation as a mandatory pre-execution step. Their recommendation (Rec #2) proposes a programmatic `validate_all()` API returning structured `ValidationResult` objects, oriented toward spec 008's orchestrator.

My review takes a fundamentally different position on what that programmatic API must support. I identify that `extra = "forbid"` on `TemplateContext` blocks plugin-injected variables (Missed Opportunities, item 2) and that the linter has no concept of plugin-contributed variables (Missed Opportunities, item 1). Integration-architect's proposed `validate_all()` function inherits these constraints -- it would validate against a closed variable set and reject any template containing a plugin-defined variable like `{CONVERGENCE_SCORE}` or `{EQUILIBRIUM_QUALITY}`.

**The contradiction**: Integration-architect's programmatic API is designed for a closed system (spec 008 invoking validation against the known schema). My requirements demand an open system (plugins registering variables the linter must accept). If we build the programmatic API per integration-architect's Rec #2 without simultaneously addressing plugin namespaces (my Rec #1), spec 008's orchestrator will have a clean API that actively prevents spec 007 plugins from functioning. The structured `ValidationError` types integration-architect proposes (`missing_variable`, `unknown_variable`) would produce false positives for every plugin-contributed variable. This is worse than the current state -- a well-designed API that enforces the wrong contract is harder to fix than a CLI wrapper.

**Resolution**: The programmatic validation API must accept a `plugin_variables: frozenset[str]` parameter (or equivalent registry) so that plugin-contributed variables are treated as known. This must be designed into the API from the start, not bolted on after spec 008 ships.

### 2. `config_condition` field vs. plugin-conditional variables

Integration-architect's highest-priority recommendation (Rec #1) proposes adding `config_conditions: Optional[dict[str, str]]` to `VariableDefinition` so that spec 006's `PRIOR_ARBITRATION_PATH` can be declared as conditional on `arbiter.timing: inter-round`. This is a sound proposal for the spec 006 use case.

However, my review identifies a broader problem: spec 007 plugins inject variables that are conditional on plugin presence, not config values (Off-Base Assumptions, item 1). A convergence predictor plugin injects `{CONVERGENCE_SCORE}` only when the plugin is active. This is not expressible as a `config_condition` -- there is no config field `convergence_predictor.enabled: true` in `conversus.yml` that the linter can check. Plugin presence is determined at runtime by scanning `plugins:` declarations and loading packages.

**The contradiction**: Integration-architect's `config_condition` mechanism solves the "variable depends on config value" case (spec 006). My requirements add a second conditional axis: "variable depends on plugin presence" (spec 007). If we implement only `config_conditions` per Rec #1, we create a false sense of completeness -- the extensibility story appears solved but only for the spec 006 case. Spec 007 would need yet another conditional mechanism (`plugin_condition`? `provided_by`?) creating an ad-hoc accumulation of conditional axes rather than a unified model.

**Resolution**: Design the variable conditionality system with three axes from the start: `modes` (existing), `config_conditions` (integration-architect's proposal), and `provided_by` or `plugin` (declaring which plugin contributes the variable). The linter skips plugin-provided variables when no plugin context is available (development-time), and validates them when plugin declarations are known (runtime via spec 008).

### 3. Structured errors assume a closed error taxonomy

Integration-architect's Rec #8 proposes `ValidationError` with `error_type: Literal["missing_variable", "unknown_variable", "missing_heading", "missing_marker", "missing_mode_variable"]`. This enum is a closed set -- the same pattern my review criticizes for `VALID_MODES` and `VALID_PHASES` (Off-Base Assumptions, items 2 and 3).

My review's Rec #7 proposes an `extensions` section on `ModeSchema` so plugins can declare mode-specific configuration. If a plugin adds a custom validation rule (e.g., "objective function template must reference at least 2 parameters"), the error taxonomy must accommodate it. A `Literal` type with 5 hardcoded values cannot represent plugin-contributed error types.

**The contradiction**: Integration-architect's structured error system is designed for completeness within the current scope. Spec 007's plugin validation needs would require modifying the `Literal` type every time a plugin introduces a new validation rule -- exactly the kind of core-file modification my review identifies as the central problem (Missed Opportunities, item 1: "every plugin must fork `variables.yml`").

**Resolution**: Use `str` for `error_type` instead of `Literal`, or define the `Literal` as a union of a core enum and a plugin-extensible enum. Alternatively, define a `PluginValidationError` subclass that plugins can extend independently.

---

## Tensions

### 1. Schema versioning: same conclusion, different urgency

Both reviews recommend adding schema versioning (integration-architect Rec #9, P3; my Rec #5, P2). Integration-architect motivates it from schema migration during rolling updates (spec 008). I motivate it from scenario replay (spec 007 Section 12) -- a stored scenario references a specific variable set, and schema drift between the original run and the replay run produces silent failures.

**The tension**: I rate this P2; integration-architect rates it P3. The difference matters. Schema versioning is a prerequisite for scenario replay, which is a Phase 2+ feature of spec 007. If versioning ships as P3 (last priority), scenario replay will either need to work around its absence or be blocked until it ships. Integration-architect's rationale (migration during rolling updates) is valid but less urgent than mine (reproducibility of stored game configurations).

**Resolution required**: Determine whether scenario replay is in spec 007's Phase 1 scope. If yes, schema versioning should be P2. If no, P3 is acceptable but the version field format should be designed now so it does not need to change when scenarios arrive.

### 2. MODE_PRESENCE: agreement on the problem, divergent solutions

Both reviews identify `MODE_PRESENCE` as problematic (integration-architect Rec #7, P2; my Rec #6, P2). Integration-architect proposes adding `mode_presence` declarations to mode schema YAML files. I propose either scanning templates at linter initialization or encoding the information in mode schemas.

**The tension**: Integration-architect's solution (static YAML declaration) requires mode schema authors to manually declare which phases use `{MODE}`. My solution (template scanning) is fully automatic. The YAML approach is more explicit and self-documenting; the scanning approach scales to plugin-introduced modes without schema changes.

For spec 007's pluggable modes, a plugin that introduces a new mode would need to either: (a) declare `mode_presence` in its mode schema YAML (integration-architect's approach, workable but requires plugin authors to know about this undocumented contract), or (b) let the linter derive it automatically (my approach, zero plugin author burden but less explicit).

**Resolution required**: These are genuinely different design philosophies. Integration-architect prefers "explicit is better than implicit" (Constitution Principle II, Stable Interfaces). I prefer "convention over configuration" for plugin ergonomics. The right answer may be: derive automatically as default, allow explicit override in the mode schema. The YAML declaration becomes an optional optimization, not a requirement.

### 3. `ARBITRATION_RULINGS` variable: valid but creates a precedent

Integration-architect's Rec #4 proposes an `ARBITRATION_RULINGS` variable carrying extracted content from arbitration resolutions into cross-round synthesis. The rationale (Constitution Principle VIII: Templating Engines Over Inference) is sound -- the orchestrator should extract and inject, not delegate parsing to agents.

**The tension**: This variable carries processed plugin-relevant data (arbitration resolution content) that spec 007's equilibrium scorer would also need. If `ARBITRATION_RULINGS` is a core variable in `variables.yml`, it sets the precedent that computed/extracted data belongs in the core schema. Spec 007's feature extraction pipeline produces similar derived data (concession rates, severity scores, position vectors) that should NOT be core variables -- they belong in the plugin namespace.

The distinction is: `ARBITRATION_RULINGS` is produced by the core orchestrator (Phase 6 is a core phase). Plugin-derived features are produced by plugins. But the boundary blurs when plugins analyze arbitration rulings and inject their analysis back into templates. If the core establishes that "extracted content from core outputs is a core variable," plugins may expect the same treatment for their extracted content.

**Resolution required**: Establish a clear rule: core variables carry data produced by the core orchestrator. Plugin variables carry data produced by plugins. `ARBITRATION_RULINGS` is correctly a core variable because the orchestrator extracts it. Plugin-derived scores like `{EQUILIBRIUM_QUALITY}` are plugin variables because a plugin produces them. Document this distinction in the schema so plugin authors know which namespace their variables belong to.

### 4. `pyproject.toml` entry points: same direction, different scope

Integration-architect's Rec #5 proposes `[project.scripts]` with `conversus-lint` as the first entry point, establishing the pattern for spec 008's `conversus run`. My review does not address packaging directly but implies it through Rec #1 (plugin variable namespace) and Rec #2 (extensible TemplateContext), which both require the package to be importable by plugins.

**The tension**: Integration-architect scopes the packaging fix to the linter entry point. Spec 007 needs the package to export `conversus.plugins` (Plugin base class, HookPoint enum, DeliberationState model) for plugin development. The package structure decision made now (flat `linter/` with bare imports like `from models import ...`) affects whether plugins can `from conversus.linter.models import TemplateContext` to extend it. If the bare-import pattern persists, plugins cannot import from the package cleanly.

**Resolution required**: The `pyproject.toml` fix should establish proper package-relative imports (`from conversus.linter.models import ...`) now, not just add an entry point. This is a prerequisite for both spec 008 (importing linter programmatically) and spec 007 (importing models for plugin extension).

---

## Safe Agreements

### 1. Phase coverage is complete and supports downstream specs

Both reviews agree that the schema's 7-phase coverage is correct and well-aligned with downstream needs. Integration-architect notes this supports spec 006's Phase 6 inter-round execution. My review notes the same phase set provides the execution points where spec 007's lifecycle hooks attach. No conflict.

### 2. Pydantic model hierarchy is the right foundation

Both reviews affirm that the typed `TemplateContext` hierarchy with per-phase subclasses is architecturally sound. Integration-architect cites Constitution Principle IX compliance. My review cites the `PHASE_CONTEXT_MODELS` registry as the exact pattern spec 007 needs for registering plugin-contributed context models. The foundation is correct; the disagreement is only about how to extend it (my Rec #2 for `extra = "allow"` variant vs. the current `extra = "forbid"`).

### 3. Linter's composable validation architecture is extensible

Both reviews agree that the pure-function validation composition (`check_unknown_variables`, `check_missing_required_variables`, etc. composed in `validate_template`) is the right pattern. Integration-architect proposes wrapping it in a structured API. My review notes a plugin could contribute its own validation function composed alongside existing ones. These are compatible extensions of the same architecture.

### 4. Mode schema separation maps to per-mode plugin configuration

Integration-architect notes that mode schemas capture the dispute-parsing subsystem interface needed by spec 006 (FR-005). My review notes that mode schemas are the natural attachment point for spec 007's per-mode objective function template references. Both reviews treat mode schemas as the extensibility surface for their respective downstream specs. The schemas serve both purposes without conflict.

### 5. `AGENT_DOCS` type discrepancy must be fixed

Integration-architect's Rec #10 identifies that the spec says `path-list` while the implementation says `extracted-content` for `AGENT_DOCS`. My review (Alignment, item 1) notes that the structured type metadata is foundational for spec 007's feature extraction pipeline. If the spec says `path-list`, a spec 007 implementer would build a file-reading feature extractor; if the implementation says `extracted-content`, they'd build a content-parsing extractor. These produce completely different feature vectors. Both reviews agree the implementation (`extracted-content`) is correct and the spec must be updated.

### 6. Schema evolution tests are needed

Integration-architect's Rec #6 proposes `TestSchemaEvolution` covering new variables, new phases, and new mode schemas. My review does not explicitly call for schema evolution tests but my Rec #3 (make `VALID_MODES` a registry) and Rec #8 (make `VALID_PHASES` extensible) both implicitly require them -- if the sets become dynamic, tests must verify that dynamic extension works correctly. Both reviews converge on the same need from different angles.

---

## Summary of Required Resolutions

| # | Issue | Integration-Architect Position | Game-Engine-Advocate Position | Resolution Needed |
|---|-------|-------------------------------|------------------------------|-------------------|
| 1 | Programmatic API scope | Closed variable set | Must accept plugin variables | Design plugin-aware API from start |
| 2 | Variable conditionality | `config_conditions` for spec 006 | Also need `provided_by` for plugins | Unified multi-axis conditionality model |
| 3 | Error type taxonomy | `Literal` with 5 types | Must be extensible for plugins | Use `str` or extensible enum |
| 4 | Schema versioning priority | P3 | P2 (scenario replay prerequisite) | Depends on spec 007 Phase 1 scope |
| 5 | MODE_PRESENCE derivation | Static YAML declaration | Automatic template scanning | Derive automatically, allow override |
| 6 | Package structure | Add entry point | Also needs package-relative imports | Fix imports alongside entry point |

---

## Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus/specs/005-generalized-templates/conversus-review/integration-architect/review.md` -- Full review text, Recs #1-10, Off-Base Assumptions, Alignment section
- `<HOME>/code/payer-index-mono/conversus/specs/005-generalized-templates/conversus-review/game-engine-advocate/review.md` -- Full review text, Recs #1-10, Off-Base Assumptions, Missed Opportunities
- `<HOME>/code/payer-index-mono/conversus/linter/models.py` -- L23-35 (frozen sets), L105-123 (ModeSchema), L129-140 (TemplateContext with extra=forbid), L262-270 (PHASE_CONTEXT_MODELS)
- `<HOME>/code/payer-index-mono/conversus/linter/validate.py` -- L108-144 (MODE_PRESENCE), L281-305 (validate_template composition), L312-371 (CLI entry point)
- `<HOME>/code/payer-index-mono/conversus/specs/005-generalized-templates/spec.md` -- L71 (US-3 AC-2 auction mode), L353 (SC-003 new mode), Section 6 (development-time framing)
- `<HOME>/code/payer-index-mono/conversus/specs/007-game-engine/spec.md` -- L96-112 (lifecycle hooks), L131-157 (plugin API), L138-146 (DeliberationState), L335-336 (plugin isolation constraint), L412-448 (objective function templates), L509-608 (scenario storage)
- `<HOME>/code/payer-index-mono/conversus/specs/007-game-engine/ideation-context.md` -- L86-115 (objective function pipeline), L129-152 (scenario storage ideation)
