# Cross-Review: game-engine-advocate's Review of Spec 005

**Cross-reviewer**: integration-architect
**Reviewing**: game-engine-advocate's Phase 1 review
**Date**: 2026-03-21

---

## Dangerous Contradictions

### 1. MODE_PRESENCE: "Correct hardcoded table" vs. "Derive from schema"

The game-engine-advocate review simultaneously praises MODE_PRESENCE as a pattern spec 007 can extend ("the exact pattern spec 007 needs for registering plugin-contributed context models" -- Alignment, re: `PHASE_CONTEXT_MODELS`) and then calls the hardcoded `MODE_PRESENCE` table a missed opportunity that "does not scale to plugin-introduced modes" (Missed Opportunities, item 9; Recommendation #6, Priority P2).

My review explicitly defends the hardcoded table: "The hardcoded truth table for which (phase, mode) pairs require `{MODE}` prevents false positives... This is the right approach" (integration-architect, Alignment, bullet 6). However, I also recommend moving it into the mode schema YAML (integration-architect, Recommendation #7, Priority P2) -- not to make it dynamically derivable from template scanning, but to make the contract explicit and maintainable.

**Why this is dangerous**: These are three different proposals masquerading as one problem. The game-engine-advocate's recommendation to "compute MODE presence by scanning existing templates at linter initialization" (Recommendation #6) is actively harmful -- it makes the linter's behavior dependent on the current template content rather than the declared contract, meaning a template bug (accidentally omitting `{MODE}`) would silently change the validation rules. My recommendation to encode it in mode schema YAML preserves the contract-first approach. The game-engine-advocate's alternative ("or encode the information in the mode schema files") aligns with mine but is buried as a secondary option. If implementers follow the primary recommendation (scan templates), they will build a fragile system where linter correctness depends on template correctness -- exactly the circularity spec 005 was designed to break.

**Resolution**: Encode `mode_presence` in the mode schema YAML files (my Recommendation #7). Reject template-scanning derivation. The linter validates templates against the schema, not the other way around.

---

### 2. `extra = "forbid"` -- Safety net vs. extensibility blocker

The game-engine-advocate identifies `extra = "forbid"` on `TemplateContext` as a P1 blocker for spec 007 plugins (Missed Opportunities, item 2; Recommendation #2) and proposes either a `PluginTemplateContext` with `extra = "allow"` or a `plugin_data: dict[str, Any]` escape hatch.

My review defends `extra = "forbid"` as "exactly the safety net that spec 006 and 008 need" (integration-architect, Alignment, bullet 3) and instead argues for adding explicit `Optional` fields for known downstream variables like `PRIOR_ARBITRATION_PATH` (integration-architect, Recommendation #3, Priority P1).

**Why this is dangerous**: These two positions are incompatible and cannot both be implemented. If spec 005 adopts `extra = "allow"` for plugin extensibility (game-engine-advocate), it loses the typo-catching safety that both reviews agree is valuable. If spec 005 adds explicit fields for every downstream spec's variables (integration-architect), it creates a dependency inversion where the foundational spec must know about all future specs.

The deeper issue: spec 006's variables (`PRIOR_ARBITRATION_PATH`, `ARBITRATION_PATHS`) are not plugin-injected -- they are core orchestrator variables with known types, known phases, and known conditions. They belong in the schema as first-class fields, not in a plugin namespace. The game-engine-advocate's plugin extensibility concern is real but applies to spec 007, not spec 006. Conflating "new core variables from spec 006" with "plugin-injected variables from spec 007" leads to a design that serves neither well.

**Resolution**: For spec 006 variables, add explicit `Optional` fields to the context models (my Recommendation #3). For spec 007 plugin variables, add a scoped `plugin_data: dict[str, Any]` field on `TemplateContext` that preserves `extra = "forbid"` for core fields while providing a typed escape hatch for plugins. Do not use `extra = "allow"` on any core model.

---

### 3. Schema extensibility model: config-condition vs. plugin namespace

The game-engine-advocate's primary recommendation is a plugin variable namespace (Recommendation #1, P1). My primary recommendation is a `config_condition` field on `VariableDefinition` (integration-architect, Recommendation #1, P1). These address different problems but compete for the same extension surface in the schema.

**Why this is dangerous**: A `config_condition` field (e.g., `config_conditions: {"arbiter.timing": "inter-round"}`) handles spec 006's known-at-schema-time conditional variables. A `plugin_variables` namespace handles spec 007's unknown-at-schema-time injected variables. If only one is implemented, the other spec is blocked. If both are implemented without coordination, the schema has two orthogonal extension mechanisms with unclear interaction semantics. Can a plugin variable have a config_condition? Can a config-conditioned variable be in the plugin namespace? The spec says nothing about this.

**Resolution**: Implement `config_condition` first (it serves spec 006, which is closer to implementation). Design the plugin namespace (spec 007) to support `config_condition` as well, so the two mechanisms compose rather than conflict. The game-engine-advocate's recommendation should be deferred to spec 007's implementation phase, not added to spec 005 now.

---

## Tensions

### 1. Linter as development-time tool vs. runtime dependency

Both reviews identify this tension. My review calls it an off-base assumption: "The spec assumes the linter is a development-time tool... But SKILL.md Step 3 already integrates validation as a mandatory pre-execution step" (integration-architect, Off-Base Assumptions, item 1). The game-engine-advocate frames it as a compatibility concern: "The linter as development-time validation is compatible with spec 007's need for plugin-aware validation" (Alignment, bullet 4).

The game-engine-advocate does not directly call for a programmatic API, though they acknowledge that "a plugin that introduces new template variables could provide its own validation function composed alongside the existing ones" -- which implicitly requires a composable programmatic API, not a CLI. My review explicitly calls for `validate_all(root, mode) -> ValidationResult` (integration-architect, Recommendation #2, P1).

**Tension**: The game-engine-advocate treats the linter's CLI nature as fine for spec 007 (validation functions are composable regardless of CLI wrapper), while my review treats the CLI coupling as a P1 blocker for spec 008. Both are correct for their respective downstream specs, but the priority depends on which spec ships first. If spec 008 ships before spec 007, the programmatic API is a prerequisite. If spec 007 ships first, plugin-aware validation composition matters more.

**Assessment**: Spec 008 is more foundational (it makes conversus executable at all), so the programmatic API should be prioritized. The game-engine-advocate's composable validation functions are not threatened by extracting a programmatic API -- they benefit from it.

---

### 2. Frozen sets: "easily fixable" vs. architectural decision

The game-engine-advocate calls `VALID_MODES` being a frozen set "easily fixable" (Missed Opportunities, item 7, Impact: low) and recommends replacing it with a function that scans `schema/modes/*.yml` file names (Recommendation #3, P1 -- contradicting the "low impact" assessment).

My review does not call out the frozen sets as a problem, because from the spec 006/008 perspective they are not: spec 006 adds no new modes, and spec 008 inherits whatever modes exist. The game-engine-advocate's concern is valid only for spec 007's long-term vision of engine-recommended modes.

**Tension**: The priority assignment is inconsistent within the game-engine-advocate's own review. An "easily fixable" item with "low impact" should not be P1. But the argument for fixing it is strong: spec 005's own SC-003 and US-3 AC-2 describe adding modes via YAML alone, and the implementation contradicts this. The contradiction between the spec's stated goals and its implementation is real and worth fixing regardless of spec 007.

**Assessment**: Make `VALID_MODES` a registry (scan `schema/modes/*.yml` at load time) -- but classify it as P2, not P1. It is a correctness fix for spec 005's own stated goals, not a spec 007 dependency.

---

### 3. Schema versioning: consensus on need, divergence on urgency

Both reviews recommend schema versioning. The game-engine-advocate cites spec 007's scenario replay system as the driver (Recommendation #5, P2). My review cites spec 008's migration support as the driver (integration-architect, Recommendation #9, P3).

**Tension**: The game-engine-advocate assigns higher priority (P2) because scenario replay requires version-aware deserialization. My review assigns lower priority (P3) because spec 008 can function without versioning initially. Neither review addresses the simplest argument for versioning: spec 006 will add variables to the schema, and a version bump is the conventional signal that the contract changed.

**Assessment**: P2 is appropriate. Implement before spec 006 adds variables, so the first schema evolution is already versioned. The scenario replay justification (game-engine-advocate) is forward-looking but speculative; the spec 006 justification is immediate.

---

### 4. Numerical types: needed now vs. premature

The game-engine-advocate recommends adding `float`/`number` to `VALID_VARIABLE_TYPES` (Recommendation #4, P2) for spec 007's feature extraction pipeline. My review does not mention this because neither spec 006 nor spec 008 produces or consumes floating-point template variables.

**Tension**: Adding a type that no current or near-term variable uses is premature abstraction. The game-engine-advocate acknowledges that this is for plugin-contributed variables, which are a spec 007 Phase 2+ concern. Adding the type now is harmless but sets a precedent that the type system expands speculatively rather than in response to concrete needs.

**Assessment**: Defer to spec 007 implementation. When the first variable needs `float`, add it then. The one-line change to a frozenset is not worth designing for now.

---

### 5. Missing spec 006 variables: convergence from different angles

Both reviews identify missing variables for spec 006, but from different angles. My review lists specific missing fields: `PRIOR_ARBITRATION_PATH` on Phase 1-5 context models (Recommendation #3), `ARBITRATION_PATHS` on `CrossRoundSynthesisContext` (Recommendation #3), and `ARBITRATION_RULINGS` as a new variable entirely (Recommendation #4). The game-engine-advocate does not mention any spec 006 variables -- their review is exclusively focused on spec 007's needs.

**Tension**: This is not a contradiction but a coverage gap. The game-engine-advocate's review is thorough for spec 007 but does not cross-reference spec 006 at all, despite spec 006 being closer to implementation and having more concrete, near-term schema requirements. The plugin namespace and `extra = "allow"` recommendations are designed for spec 007's hypothetical future variables while ignoring spec 006's concrete, defined-today variables.

**Assessment**: Spec 006 variable additions (my Recommendations #3 and #4) should be implemented before any spec 007 extensibility work. The variables are known, typed, phase-scoped, and condition-scoped -- they exercise exactly the extension mechanisms (adding fields to context models, adding entries to `variables.yml`) that spec 005 should support as a baseline, before any plugin-aware extensions.

---

## Safe Agreements

### 1. Variable registry as structured data is foundational

Both reviews agree that `schema/variables.yml` as a machine-readable variable contract is the right design. The game-engine-advocate calls it "foundational" for spec 007's feature extraction pipeline (Alignment, bullet 1). My review agrees it "will become the foundational contract for all template variables" (integration-architect, Executive Summary). No disagreement on the value of the schema itself.

### 2. Mode schema separation maps to downstream needs

Both reviews agree that per-mode YAML schemas are the correct granularity. The game-engine-advocate maps them to spec 007's per-mode payoff function definitions (Alignment, bullet 2). My review maps them to spec 006's dispute-parsing subsystem interface (integration-architect, Alignment, bullet 2). The mode schema serves both downstream specs without modification -- it is the right abstraction boundary.

### 3. Pydantic model hierarchy is correct

Both reviews endorse the Pydantic model layer. The game-engine-advocate notes that phase context models "capture exactly the data the feature extraction pipeline needs" (Alignment, bullet 3). My review notes they "enforce Constitution Principle IX rigorously" (integration-architect, Alignment, bullet 3). The model hierarchy is sound; disagreements are about how to extend it, not whether it should exist.

### 4. Linter composition architecture is correct

Both reviews endorse the pure-function validation composition. The game-engine-advocate says "a plugin could provide its own validation function composed alongside the existing ones" (Alignment, bullet 4). My review says the linter is "well-structured with pure validation functions composed into a single `validate_template` entrypoint" (integration-architect, Executive Summary). The architecture is extensible by design.

### 5. `PHASE_CONTEXT_MODELS` registry pattern is reusable

Both reviews identify the `PHASE_CONTEXT_MODELS` dict as an extensible registry pattern. The game-engine-advocate calls it "the exact pattern spec 007 needs" (Alignment, bullet 5). My review implicitly depends on it when recommending new context fields for spec 006. This registry should remain a dict (not a frozen mapping) to support runtime extension.

### 6. Schema versioning is needed

Both reviews recommend schema versioning, differing only on priority (P2 vs. P3) and justification (scenario replay vs. migration support). See Tension #3 above. The recommendation itself is uncontroversial.

### 7. AGENT_DOCS type discrepancy must be fixed

Only my review calls this out explicitly (integration-architect, Recommendation #10, P3), but the game-engine-advocate's review implicitly depends on correct type metadata for the feature extraction pipeline: "Having structured metadata about what each variable contains (type: `path-list` vs `extracted-content` vs `string`) lets the feature extractor know what to parse" (Alignment, bullet 1). If the spec says `path-list` but the implementation says `extracted-content`, the feature extractor built from the spec will mishandle `AGENT_DOCS`. Both reviews agree the type metadata must be accurate; mine identifies a specific inaccuracy.

### 8. Extension contracts should be documented

The game-engine-advocate recommends documenting extension contracts in spec 005 (Recommendation #9, P3). My review does not make this recommendation explicitly but the `config_condition` and programmatic API recommendations implicitly define extension contracts. Documenting the intended extension surface before downstream specs implement against it is prudent and low-cost.

---

## Summary

The most dangerous contradiction is around `extra = "forbid"` -- the game-engine-advocate wants to relax it for plugin extensibility, while my review defends it as a safety mechanism and proposes explicit fields instead. The resolution is to use both: explicit fields for known downstream variables (spec 006), a scoped `plugin_data` dict for unknown plugin variables (spec 007), and `extra = "forbid"` preserved on all core fields.

The reviews have complementary blind spots: the game-engine-advocate covers spec 007 extensibility thoroughly but does not address spec 006's concrete variable needs at all. My review covers spec 006 and spec 008 integration requirements but does not address plugin extensibility. Together, they provide full coverage of the downstream dependency surface.

Priority ordering for spec 005 changes, synthesizing both reviews:
1. Add `config_condition` to `VariableDefinition` + spec 006 variables to context models (my P1s)
2. Extract programmatic validation API (my P1)
3. Make `VALID_MODES` a registry scanning `schema/modes/*.yml` (game-engine-advocate P1, downgraded to P2)
4. Add schema versioning (consensus P2)
5. Structured error objects (my P2)
6. Document extension contracts (game-engine-advocate P3)
7. Plugin namespace and `extra = "allow"` variant (game-engine-advocate P1, deferred to spec 007)
8. `float` type addition (game-engine-advocate P2, deferred to spec 007)
