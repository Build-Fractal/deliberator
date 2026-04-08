# Game Engine Advocate — Revision After Cross-Reviews

**Reviewer role**: game-engine-advocate (spec 007)
**Revision iteration**: 1
**Date**: 2026-03-21

---

## Recommendation Dispositions

### Recommendation 1: Add a plugin variable namespace to the schema (was P1)

**Disposition: DEFERRED — withdraw from spec 005 scope, defer to spec 007 implementation phase.**

The integration-architect's cross-review correctly identifies that this competes with the `config_condition` field for the same extension surface, and that `config_condition` serves the nearer-term spec 006 need. The functional-typing cross-review reinforces this by noting that my P1 items are speculative — they address a spec not yet implemented — while spec 005 has concrete quality defects today.

I was right that plugins will need a mechanism to register variables without modifying core schema files. But I was wrong to demand it in spec 005. Spec 005's scope is the variable contract for the existing template system. Plugin namespaces are a spec 007 concern that should be designed alongside the plugin API, not retrofitted into the schema layer before the plugin interface is defined.

The integration-architect's sequencing is correct: implement `config_condition` for spec 006 first, then design the plugin namespace in spec 007 to compose with it. Designing both extension mechanisms together avoids the "ad-hoc accumulation of conditional axes" I warned about in my cross-review of the integration-architect.

**Revised priority**: Not applicable to spec 005. Becomes a spec 007 Phase 1 deliverable.

---

### Recommendation 2: Create an extensible TemplateContext variant (was P1)

**Disposition: MODIFIED — narrow scope from `extra = "allow"` to a scoped `plugin_data` field; defer implementation to spec 007, but document the extension contract in spec 005.**

Both cross-reviews landed decisive hits on the `extra = "allow"` proposal:

- functional-typing correctly identifies that `dict[str, Any]` contradicts Constitution Principle IX's prohibition on `Any` "unless wrapping an untyped third-party API." A plugin context is not an untyped third-party API — it is a known extension point that should have its own typed model.
- integration-architect correctly distinguishes between spec 006's variables (known types, known phases — they belong as explicit `Optional` fields) and spec 007's plugin variables (unknown at schema-definition time — they need a different mechanism). Conflating the two was my error.

functional-typing's proposed resolution — a separate `PluginContext(BaseModel)` composed alongside `TemplateContext` rather than inherited from it — is the right architecture. Plugins populate `PluginContext` with their own typed Pydantic models. The orchestrator passes both objects to template rendering. This satisfies immutability (functional-typing), type safety (Constitution Principle IX), and extensibility (spec 007) without any single model serving both purposes.

I withdraw the `extra = "allow"` proposal entirely. `extra = "forbid"` should remain on all core `TemplateContext` models.

**What survives**: Spec 005 should document that the `TemplateContext` hierarchy is designed for core variables only and that plugin-contributed data will flow through a parallel composition mechanism (to be defined in spec 007). This is recommendation 9 (document extension contracts), elevated in importance by this concession.

**Revised priority**: P3 for documentation in spec 005. Composition architecture is a spec 007 Phase 1 deliverable.

---

### Recommendation 3: Make VALID_MODES a registry, not a frozen set (was P1)

**Disposition: MODIFIED — downgrade to P2; adopt file-scanning approach; reframe as a spec 005 internal consistency fix rather than a spec 007 dependency.**

The integration-architect's cross-review correctly identifies an internal inconsistency in my own review: I call this "easily fixable" with "low impact" (Missed Opportunities, item 7) but assign it P1 (Recommendation 3). The integration-architect's resolution is right — this is P2, not P1. It is a correctness fix for spec 005's own stated goals (SC-003 and US-3 AC-2 describe adding modes via YAML alone), not primarily a spec 007 concern.

functional-typing's counter-proposal to use `Literal` types for modes is the most dangerous recommendation across all reviews. A `Literal["cooperative", "red-blue", "winner-take-all", "prisoners-dilemma"]` type is strictly worse than the current `frozenset` because it bakes the closed enum into the type system itself, where it cannot be relaxed at runtime. The `frozenset` can at least be replaced with a function; a `Literal` requires source code modification to add any value. This directly contradicts spec 005's own SC-003 and US-3 AC-2. I stand by my cross-review of functional-typing on this point: the `@field_validator` pattern should be kept and made to read from a dynamically constructed set.

The `main()` function in `validate.py` (L323-325) already derives mode lists by scanning `schema/modes/*.yml` files. The `ModeSchema.validate_mode` validator (L115-122) should do the same rather than checking against a hardcoded frozenset.

**Revised priority**: P2. Fix for spec 005 internal consistency, independent of spec 007.

---

### Recommendation 4: Add a float/number variable type (was P2)

**Disposition: WITHDRAWN — defer to spec 007 implementation.**

The integration-architect's cross-review is persuasive: adding a type that no current or near-term variable uses is premature abstraction. Neither spec 005 nor spec 006 produces floating-point template variables. The one-line change to `VALID_VARIABLE_TYPES` should happen when the first variable needs it, not speculatively.

My original rationale (spec 007's feature extraction pipeline produces continuous values) remains valid, but those values are plugin output, not template variables. Plugin output goes to `{output}/plugins/` as JSON (spec 007 `spec.md`, L116-127), not through the template variable system. The assumption that plugin-produced numerical data would flow as template variables was wrong — it flows through the plugin output path.

If a future spec does need a float template variable, the change is trivial and can be made at that time.

**Revised priority**: Not applicable. Defer to the spec that first needs it.

---

### Recommendation 5: Add schema version field (was P2)

**Disposition: MAINTAINED at P2 — but adopt the integration-architect's justification (spec 006 schema evolution) over my original justification (scenario replay).**

Both cross-reviews agree schema versioning is needed. The disagreement was on priority (my P2 vs. integration-architect's P3) and justification. The integration-architect's cross-review makes the strongest case neither of us originally stated: spec 006 will add variables to the schema, and a version bump is the conventional signal that the contract changed. This is more immediate and concrete than my scenario replay argument, which is a spec 007 Phase 2+ concern.

I maintain P2 because the version field should exist before the first schema evolution (spec 006 adding `PRIOR_ARBITRATION_PATH` and `ARBITRATION_RULINGS`), not after. If spec 006 ships first and the schema evolves without versioning, retroactively adding versioning is harder than including it from the start.

**Revised priority**: P2, justified by spec 006 schema evolution rather than spec 007 scenario replay.

---

### Recommendation 6: Derive MODE_PRESENCE from schema rather than hardcoding (was P2)

**Disposition: MODIFIED — adopt the integration-architect's static YAML declaration approach; reject my own template-scanning proposal.**

The integration-architect's cross-review is correct and I concede: deriving MODE_PRESENCE by scanning templates is actively harmful. It makes the linter's behavior dependent on template content, meaning a template bug (accidentally omitting `{MODE}`) would silently change validation rules. The linter validates templates against the schema, not the other way around. Template-scanning derivation creates exactly the circularity spec 005 was designed to break.

functional-typing's proposal (derive from the `condition` field in `variables.yml` via a pure function) is clean but incomplete — the `condition` field is currently free-text (`"rounds > 1"`) and not machine-parseable for this purpose. The MODE variable's condition is not a simple config condition but a complex per-mode, per-phase truth table.

The integration-architect's solution (encode `mode_presence` in mode schema YAML files) is the right approach. Each mode schema already declares its variables and structural requirements; adding phase-level MODE presence is a natural extension. When spec 007 introduces new modes via plugins, the plugin's mode schema file declares its own MODE presence — no modification of core files required.

I offered "derive automatically, allow explicit override" in my cross-review of the integration-architect as a compromise. I withdraw that compromise. Explicit declaration is better. Convention-over-configuration is the wrong principle here — the linter needs an explicit contract, not inferred behavior.

**Revised priority**: P2 (unchanged), but the implementation approach changes from template scanning to YAML declaration in mode schemas.

---

### Recommendation 7: Add an extensions section to ModeSchema (was P2)

**Disposition: DEFERRED — withdraw from spec 005 scope.**

Neither cross-review directly challenged this recommendation, but the integration-architect's broader argument about deferring spec 007 extensibility work applies here too. The `extensions` field on `ModeSchema` is a spec 007 concern — it exists to attach objective function template references, which are a game engine concept.

The integration-architect's `config_condition` on `VariableDefinition` faces the same "adds extension surface for a downstream spec" criticism, but it has a concrete near-term use case (spec 006's `PRIOR_ARBITRATION_PATH` conditional on `arbiter.timing`). The ModeSchema `extensions` field has no use case before spec 007.

I maintain that the mode schema is the natural attachment point for per-mode plugin configuration, but this should be designed during spec 007 Phase 1 when the objective function template library defines what fields mode schemas need. Adding a generic `extensions: dict[str, Any]` now would be a formless escape hatch with no defined semantics — the antithesis of spec 005's structured schema approach.

**Revised priority**: Deferred to spec 007. Noted in extension contracts documentation (recommendation 9).

---

### Recommendation 8: Make VALID_PHASES extensible (was P3)

**Disposition: MAINTAINED at P3 — reframe as a consistency fix aligned with recommendation 3.**

The same logic that applies to `VALID_MODES` (recommendation 3) applies here, at lower urgency. If `VALID_MODES` becomes a dynamic registry scanning `schema/modes/*.yml`, `VALID_PHASES` should follow the same pattern for consistency. The phases could be derived from the keys of `PHASE_CONTEXT_MODELS` or from the union of all phases declared in `variables.yml`.

functional-typing's recommendation to mark `PHASE_CONTEXT_MODELS` as `Final` is in tension with this, but the tension is manageable: `PHASE_CONTEXT_MODELS` can be `Final` in the core module while a plugin system provides its own registration mechanism at a higher layer. The core's phase set is genuinely closed from the core's perspective; plugin-contributed phases are a plugin-layer concern. I partially concede to functional-typing on `Final`: the annotation communicates intent to plugin authors ("do not mutate this dict directly") and does not prevent a plugin registry wrapper at a higher layer.

**Revised priority**: P3 (unchanged).

---

### Recommendation 9: Document the extension contract in spec 005 (was P3)

**Disposition: ELEVATED to P2 — becomes more important given the deferrals above.**

Since recommendations 1, 2, 7, and 10 are all deferred to spec 007, the need for documented extension contracts in spec 005 increases. Without documentation, spec 007 implementers will not know:

- Which parts of the schema are intended to be extended (mode schemas, variable definitions) vs. which are genuinely closed (template syntax, structural markers)
- The intended composition pattern for plugin data alongside core data
- Where the boundary is between "add explicit Optional fields" (spec 006 approach) and "use a plugin namespace" (spec 007 approach)

The documentation does not require implementation. It is a section in spec 005's implementation notes stating: "The following are extension points for downstream specs: (a) new variables via schema addition, (b) new modes via YAML file creation, (c) plugin-contributed data via a parallel composition mechanism (spec 007). The following are NOT extension points: `extra = "forbid"` on TemplateContext, the template syntax `{VARIABLE}`, structural markers."

The integration-architect's cross-review implicitly supports this: "Documenting the intended extension surface before downstream specs implement against it is prudent and low-cost."

**Revised priority**: P2 (elevated from P3).

---

### Recommendation 10: Reserve schema/objectives/ directory in project structure (was P3)

**Disposition: WITHDRAWN — premature for spec 005.**

This was speculative directory reservation for a spec 007 Phase 2+ feature. Neither cross-reviewer addressed it, which is itself a signal that it falls outside spec 005's reasonable scope. Spec 007 can create whatever directory structure it needs when it ships.

**Revised priority**: Not applicable. Spec 007 concern.

---

## New Recommendations

### N1: Adopt the integration-architect's programmatic validation API, with a plugin-variables parameter (Priority: P1)

**Source**: My cross-review of the integration-architect identified that the proposed `validate_all()` function would reject plugin-contributed variables as unknown. The integration-architect's cross-review proposed a scoped `plugin_data` field. Combining both positions:

The programmatic API (`validate_all(root, mode) -> ValidationResult`) is needed for spec 008's orchestrator and should be designed with a `known_plugin_variables: frozenset[str] = frozenset()` parameter from the start. When the orchestrator calls validation without plugins, the parameter is empty and behavior is identical to today. When spec 007 ships, the plugin loader populates this set and passes it to validation. Plugin-contributed variables in this set are not flagged as unknown.

This is the minimal forward-looking change that prevents the programmatic API from becoming a blocker for spec 007 without requiring any plugin infrastructure in spec 005. The default value (`frozenset()`) means existing callers are unaffected.

### N2: Fix the bare import pattern in linter/ before downstream specs import from it (Priority: P2)

**Source**: My cross-review of the integration-architect identified that `validate.py` uses `from models import ...` (bare imports, L24-28), which prevents clean package imports like `from conversus.linter.models import TemplateContext`. Both spec 008 (programmatic validation API) and spec 007 (plugin extension of models) need to import from this package.

The fix: convert bare imports to package-relative imports (`from .models import ...` or `from conversus.linter.models import ...`) and ensure `linter/` has a proper `__init__.py` with exports. This aligns with the integration-architect's `pyproject.toml` recommendation but is more fundamental — the entry point is useless if the imports are broken.

### N3: Formalize the condition field syntax in variables.yml (Priority: P3)

**Source**: The MODE_PRESENCE discussion across all three reviews revealed that the `condition` field (e.g., `"rounds > 1"`) is free-text and not machine-parseable. If MODE_PRESENCE is to be derived from schema data (all reviews agree on this), and if the integration-architect's `config_condition` extension is adopted for spec 006, the condition syntax needs formalization so the linter can interpret it rather than treating it as documentation-only prose.

A minimal formalization: define a small grammar for conditions (e.g., `config_key operator value`) and validate condition strings against it in the linter. This prevents conditions from becoming arbitrary prose that the linter cannot interpret, and it serves both the MODE_PRESENCE derivation and the `config_condition` extension.

---

## Position Summary

After reading both cross-reviews, I concede significant ground on timing and scope while maintaining my core architectural position.

**What I was wrong about:**

1. **Scope inflation.** Seven of my ten recommendations were spec 007 concerns dressed as spec 005 feedback. The functional-typing and integration-architect cross-reviews both correctly identified this. Spec 005's job is to establish the variable schema and linter for the existing template system. Plugin extensibility is spec 007's job.

2. **`extra = "allow"` on TemplateContext.** Both cross-reviews converge: this abandons typo-catching for all fields, not just plugin fields. The composition approach (separate `PluginContext` alongside `TemplateContext`) is architecturally superior. I withdraw `extra = "allow"` entirely.

3. **Template-scanning for MODE_PRESENCE.** This creates the exact circularity the linter is designed to prevent. The integration-architect's argument is decisive: the linter validates templates against the schema, not the other way around. Explicit YAML declaration in mode schemas is correct.

4. **Float type and directory reservation.** Premature abstraction. No current or near-term variable needs `float`. Plugin output uses JSON, not template variables. Add these when a concrete use case arrives.

**What I was partially right about:**

1. **VALID_MODES as a frozen set.** The fix is justified by spec 005's own SC-003 and US-3 AC-2, not by spec 007. But the priority was wrong (P1 -> P2), and the justification should be spec 005 self-consistency, not forward compatibility.

2. **Schema versioning.** Needed, but for spec 006 schema evolution (integration-architect's justification), not for scenario replay (my original justification). P2 is the right priority for the right reason.

3. **Extension contract documentation.** Becomes more important, not less, because the implementation work is deferred. Five of my recommendations are deferred to spec 007 — documenting what spec 005 intends to be extensible prevents spec 007 from guessing. Elevated from P3 to P2.

**What survives scrutiny:**

1. **The core architectural tension is real.** Spec 005 builds a closed system. Spec 007 needs it to be open. The cross-reviews do not dispute this — they correctly argue that the resolution belongs in spec 007, not in spec 005. The integration-architect's proposed sequencing (spec 006 variables first, then spec 007 extensibility) is the right order of operations.

2. **Literal types for modes would be harmful.** functional-typing's recommendation to use `Literal` for `ModeSchema.mode` is the single most dangerous recommendation across all reviews. It contradicts spec 005's own user stories (US-3 AC-2: adding "auction" mode by creating a YAML file) and makes the extensibility problem strictly harder by encoding the closed enum at the type-definition level rather than the runtime-validation level. The `@field_validator` pattern is preferable and should be preserved.

3. **The programmatic API must be designed with plugin awareness from the start.** Adding a `known_plugin_variables: frozenset[str] = frozenset()` parameter costs nothing today and prevents a breaking redesign when spec 007 ships. This is the one forward-looking change that genuinely belongs in spec 005.

4. **`PHASE_CONTEXT_MODELS` should not be marked `Final`.** functional-typing's `Final` recommendation and my extensibility concern can coexist: `Final` in the core module is acceptable if the plugin system extends at a higher layer. But marking it `Final` before defining that higher layer risks signaling "this is permanently closed" rather than "this is closed at this layer." The `Final` decision should wait for spec 007 Phase 1 to define the extension architecture.

**The fundamental correction**: Spec 005's job is to be a correct, well-structured foundation. Making it extensible is spec 007's job. My original review confused "foundation that does not prevent extension" (correct ask) with "foundation that provides extension mechanisms" (premature ask). The cross-reviews drew this distinction clearly, and I accept it.

**Revised priority ordering for spec 005, from the game-engine-advocate perspective:**

1. P1: Programmatic validation API with plugin-variables parameter (N1)
2. P2: Schema versioning (rec 5, justified by spec 006 readiness)
3. P2: VALID_MODES as dynamic registry (rec 3, spec 005 self-consistency)
4. P2: MODE_PRESENCE as YAML declaration in mode schemas (rec 6, modified approach)
5. P2: Document extension contracts (rec 9, elevated from P3)
6. P2: Fix bare imports for package importability (N2)
7. P3: VALID_PHASES extensibility (rec 8, unchanged)
8. P3: Formalize condition field syntax (N3)
9. Deferred to spec 007: Plugin variable namespace (rec 1)
10. Deferred to spec 007: PluginContext composition architecture (rec 2)
11. Deferred to spec 007: ModeSchema extensions section (rec 7)
12. Withdrawn: Float type (rec 4)
13. Withdrawn: Reserved schema/objectives/ directory (rec 10)
