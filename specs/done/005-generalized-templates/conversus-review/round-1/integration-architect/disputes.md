# Integration Architect — Final Disputes and Convergence

**Reviewer**: integration-architect
**Phase**: 4 (Final Disputes)
**Date**: 2026-03-21

---

## Remaining Disputes

### Dispute 1: `plugin_data: dict[str, Any]` on core TemplateContext models

**Disputed with**: functional-typing (who rejects it as a Principle IX violation), game-engine-advocate (who withdrew `extra = "allow"` but implicitly supports a scoped escape hatch)

In my revision (N4), I proposed adding `plugin_data: dict[str, Any] = {}` to `TemplateContext` as the compromise between `extra = "forbid"` (which I defend) and spec 007's need for plugin-contributed data. functional-typing correctly identifies that `dict[str, Any]` violates Constitution Principle IX's prohibition on `Any` "unless wrapping an untyped third-party API." game-engine-advocate withdrew `extra = "allow"` and endorsed the separate `PluginContext` composition model that functional-typing proposed.

I concede this dispute. The composition approach — a separate `PluginContext(BaseModel)` passed alongside `TemplateContext` to the rendering layer — is architecturally superior. It preserves `extra = "forbid"` on core models without introducing an untyped escape hatch. The `plugin_data` field was a pragmatic shortcut that would have created exactly the kind of untyped bag that Principle IX is designed to prevent. Plugin-contributed data should flow through its own typed model, not through a generic dict on the core model.

**Resolution**: Withdraw N4's `plugin_data` field. Adopt functional-typing's composition model: `PluginContext` alongside `TemplateContext`, designed during spec 007 Phase 1. `extra = "forbid"` remains on all core models without exception.

---

### Dispute 2: Programmatic API parameter design — `known_plugin_variables` vs. `ValidationConfig`

**Disputed with**: game-engine-advocate (who proposes `known_plugin_variables: frozenset[str] = frozenset()` on `validate_all()`)

game-engine-advocate's new recommendation N1 proposes adding a `known_plugin_variables: frozenset[str]` parameter to the programmatic `validate_all()` API from the start, so plugin-contributed variables are not flagged as unknown. My revision proposed the API accept either `**kwargs` or a `ValidationConfig` model for extensibility, without committing to plugin-specific parameters before spec 007 exists.

I maintain my position, narrowed. The `validate_all()` function should accept a `ValidationConfig` Pydantic model (not `**kwargs` — that was poorly stated and violates Principle IX). A `ValidationConfig(BaseModel)` with `root: Path`, `mode: Optional[str] = None`, and no plugin-specific fields is the correct initial signature. When spec 007 ships, it can add `known_plugin_variables: frozenset[str] = frozenset()` to `ValidationConfig` without breaking the API. game-engine-advocate's proposal adds a plugin-shaped parameter to an API that has no plugin callers — it is a one-line change that costs nothing today, but it also communicates nothing today. The parameter's existence would suggest plugin support is implemented, which it is not.

This is a minor dispute. The difference is whether a parameter that no caller uses appears in the initial signature. I prefer not, because it creates a documentation burden ("what is this for?") and a testing burden (the parameter must be tested even with no real callers). But I acknowledge this is a judgment call, not a correctness issue.

**Resolution**: Ship `validate_all(config: ValidationConfig) -> ValidationResult` with `ValidationConfig` containing `root` and `mode` only. Document in `ValidationConfig`'s docstring that spec 007 will extend it with plugin-aware fields. Do not add `known_plugin_variables` until there is a caller.

---

### Dispute 3: Structured error type — `Literal` enum vs. open `str` for `error_type`

**Disputed with**: game-engine-advocate (who argues `Literal` with 5 hardcoded values cannot represent plugin-contributed error types)

In my revision (Recommendation 8), I proposed `ValidationError` with `error_type: Literal["missing_variable", "unknown_variable", "missing_heading", "missing_marker", "missing_mode_variable"]`. game-engine-advocate argues that spec 007 plugins will produce their own validation error types and a closed `Literal` cannot accommodate them.

I maintain this position. The `Literal` provides type safety and autocompletion for the five error types that exist today. When spec 007 introduces plugin validation, it has two clean options: (a) add new values to the `Literal` (a minor code change), or (b) define a `PluginValidationError` subclass with its own `Literal` for plugin error types. Using `str` for `error_type` now — to preemptively support plugins that do not exist — sacrifices the type safety that is the entire motivation for moving from `list[str]` to structured errors.

This dispute is exactly the `Literal` debate from functional-typing's Recommendation 3, but applied to a different surface. The key difference is that `error_type` values are program-internal classifications (the linter defines them, the orchestrator consumes them), not user-facing schema extensions. Adding a new error type requires modifying the linter code regardless — unlike adding a new mode, which spec 005's SC-003 promises can be done via YAML alone. The YAML-only extensibility argument that correctly defeated `Literal` for modes does not apply to error types.

**Resolution**: Keep `error_type: Literal[...]` for the five known values. Document in the `ValidationError` docstring that this enum will be expanded when plugin validation is introduced. This is a maintainable, type-safe position.

---

### Dispute 4: Schema versioning priority — P2 timing relative to spec 006

**No dispute remaining.** All three reviewers now converge on P2 for schema versioning, justified by spec 006's schema evolution. game-engine-advocate provides the strongest urgency argument: the version field should exist before the first schema evolution event, not after. I fully agree. This was P3 in my original review; I upgraded it to P2 in my revision and stand by that upgrade.

This is noted here only to confirm that the original disagreement (my P3 vs. game-engine-advocate's P2) is resolved.

---

## Convergence

The following items have reached full or near-full convergence across all three reviewers. These should proceed to synthesis without further debate.

### 1. Purify schema-loading functions (unanimous P1)

All three reviewers agree: `load_variables_schema`, `load_mode_schema`, and `find_project_root` must raise `SchemaLoadError` instead of calling `sys.exit(2)`. The CLI `main()` catches the exception and exits. This is a prerequisite for the programmatic API and for any downstream spec that imports from the linter package.

functional-typing identified the defect. I identified the consequence (programmatic API cannot be built on top of process-terminating functions). game-engine-advocate identified the downstream need (spec 007 plugin validation imports). The diagnosis is unanimous and the fix is trivial.

### 2. Extract programmatic validation API (unanimous P1)

All three reviewers agree that `validate_all()` returning structured results is needed for spec 008's orchestrator. The disagreement on parameter design (Dispute 2 above) is minor and does not block the core recommendation.

### 3. MODE_PRESENCE derived from mode schema YAML (unanimous P2)

All three reviewers converge on encoding `mode_presence` (or `mode_in_phases`) in mode schema YAML files. I retracted my contradictory Alignment endorsement of the hardcoded table. functional-typing conceded their `condition`-field derivation approach. game-engine-advocate withdrew their template-scanning proposal. The implementation approach is clear: add a `mode_in_phases` field to each mode schema YAML listing phases where `{MODE}` is expected. The linter reads this declaration. The hardcoded 28-entry dict is deleted.

### 4. PathList type alias for path-list fields (converged P1/P2)

functional-typing and I converge on a `PathList` custom type with Pydantic serializer: `list[Path]` internally, newline-separated string for template substitution. functional-typing's revised Recommendation 2 adopts my `PathList` proposal. game-engine-advocate did not dispute it. New fields (spec 006's `ARBITRATION_PATHS`) must use this type from the start.

### 5. Mandate Python in spec Implementation Notes (unanimous P2)

All reviewers agree. The spec's Section 6 currently says "Python or shell." The implementation is Python with Pydantic. The spec language should match. Editorial fix, no architectural impact.

### 6. Document `required: True` default in spec (unanimous P3)

All reviewers agree. The `VariableDefinition.required` field defaults to `True`, but the spec does not document this. Add the default to Section 3.

### 7. VALID_MODES should be dynamically derived (converged P2)

game-engine-advocate (who proposed it) and I agree: `VALID_MODES` should be derived from `schema/modes/*.yml` files at load time, consistent with spec 005's own SC-003 (adding a mode via YAML alone). functional-typing withdrew their `Literal` counter-proposal, which was the only opposition. The `main()` function already scans `schema/modes/*.yml` for the mode list (`validate.py`, L323-325); the `ModeSchema.validate_mode` validator should do the same instead of checking against a hardcoded `frozenset`.

### 8. Fix bare imports for package importability (converged P2)

game-engine-advocate (N2) and I (Recommendation 5) converge: `validate.py`'s bare imports (`from models import ...`) must become package-relative imports (`from .models import ...`). Both spec 008 and spec 007 need `from conversus.linter.models import TemplateContext` to work. This is a prerequisite for the `pyproject.toml` entry point.

### 9. frozen=True on TemplateContext (converged P2)

functional-typing proposed it, I endorsed it. game-engine-advocate conceded it for core models. Plugin extensibility is handled by the separate `PluginContext` composition, not by relaxing immutability on core models. Spec 005 freezes; spec 007 composes.

### 10. Document extension contracts in spec 005 (converged P2)

game-engine-advocate elevated this from P3 to P2 because their substantive spec-007 recommendations were deferred. I agree. Spec 005 should document which surfaces are extension points (mode schemas, variable definitions) and which are closed (`extra = "forbid"`, template syntax, structural markers). This costs nothing and gives spec 007 implementers a clear contract.

### 11. Schema versioning before spec 006 (unanimous P2)

All reviewers agree: add `schema_version: "1.0.0"` to `variables.yml` before spec 006 adds its variables. The first schema evolution event should be versioned from the start.

### 12. Fix AGENT_DOCS type discrepancy in spec (unanimous P3)

All reviewers agree: the spec says `path-list`, the implementation says `extracted-content`. The implementation is correct. Update the spec. Editorial fix.

### 13. Add spec 006 variables to context models (P1, integration-architect driven)

Neither cross-reviewer disputed the substance of adding `PRIOR_ARBITRATION_PATH`, `ARBITRATION_PATHS`, and `ARBITRATION_RULINGS` to the context models. functional-typing's concern was about typing (use `Path`/`PathList`, not `str`), which is addressed by convergence item 4. game-engine-advocate's concern was about precedent (core vs. plugin variables), which is addressed by my N3 (namespace rule documentation).

### 14. config_conditions with typed ConfigCondition model (P1, integration-architect driven)

My original `dict[str, str]` typing was correctly challenged by functional-typing. I accept the refinement: `ConfigCondition(BaseModel)` with `field: str` and `value: str`. game-engine-advocate deferred their plugin conditionality axis to spec 007, which is the correct sequencing.

---

## Final Position Statement

### Non-Negotiables

These are positions I will not compromise on. They are grounded in the integration requirements of specs 006, 008, and the overall system architecture.

1. **`extra = "forbid"` on all core TemplateContext models.** This is the single most important safety property in the linter's type system. It catches typos (`AGENT_NMAE`), prevents undeclared variables from silently passing validation, and enforces the schema-first contract. game-engine-advocate withdrew their `extra = "allow"` proposal. functional-typing's composition model resolves the plugin tension without weakening this constraint. There is no remaining justification for relaxing it.

2. **Spec 006 variables as explicit typed fields, not plugin-mechanism variables.** `PRIOR_ARBITRATION_PATH`, `ARBITRATION_PATHS`, and `ARBITRATION_RULINGS` are known variables with known types produced by the core orchestrator. They belong as explicit `Optional` fields on the context models, using `Path` and `PathList` types. They must not be deferred to spec 007's plugin mechanism — that would delay a concrete integration need behind a speculative extensibility design.

3. **Schema-loading functions must be purified before any downstream spec ships.** If spec 008's orchestrator calls `validate_all()` and the underlying schema loader calls `sys.exit(2)`, the orchestrator crashes instead of handling the error. If spec 007's plugin loader imports from `conversus.linter.models` and the import path is broken (bare imports), the plugin system cannot function. These are blocking prerequisites, not nice-to-haves.

4. **Structured `ValidationError` with `Literal` error types.** `list[str]` errors are not programmatically actionable. Spec 008's orchestrator needs to distinguish between a missing structural marker (blocking — the template cannot produce parseable output) and an unknown variable (potentially a warning in plugin contexts). `Literal` provides type safety for the known error taxonomy without foreclosing expansion.

5. **Sequencing discipline: spec 006 concrete needs first, spec 007 speculative extensibility second.** The review process has correctly identified that many of game-engine-advocate's original P1 recommendations were spec 007 concerns dressed as spec 005 feedback. game-engine-advocate conceded this in their revision. The correct implementation order is: (a) fix spec 005's internal quality issues (impure loaders, bare imports, hardcoded MODE_PRESENCE), (b) add spec 006's concrete variables and schema evolution infrastructure, (c) design spec 007's extension mechanisms with full knowledge of the hardened spec 005 foundation.

### Yielded Positions

For the record, the positions I have yielded during this review process:

- **`plugin_data: dict[str, Any]`** — Withdrawn. The composition model is better.
- **`dict[str, str]` for config_conditions** — Replaced with typed `ConfigCondition` model. functional-typing was right.
- **MODE_PRESENCE Alignment endorsement** — Retracted. The hardcoded table is not "the right approach"; the schema-first YAML declaration is.
- **Schema-loading purity** — I failed to identify that `sys.exit()` in schema loaders contradicts my own programmatic API recommendation. functional-typing correctly caught this blind spot. Purifying the loaders is now part of Recommendation 2's scope.
- **Schema versioning at P3** — Upgraded to P2. game-engine-advocate's argument that versioning should precede the first schema evolution event is correct.

### Priority Ordering (Final)

| Priority | Recommendation | Source |
|----------|---------------|--------|
| P1 | Purify schema loaders + extract programmatic `validate_all()` API | Rec 2 (modified) |
| P1 | Add `config_conditions` with typed `ConfigCondition` model | Rec 1 (modified) |
| P1 | Add spec 006 variables (`PRIOR_ARBITRATION_PATH`, `ARBITRATION_PATHS`, `ARBITRATION_RULINGS`) using `Path`/`PathList` types | Rec 3 + 4 (modified) |
| P2 | Schema versioning (`schema_version: "1.0.0"` in `variables.yml`) | Rec 9 (upgraded) |
| P2 | Move MODE_PRESENCE to mode schema YAML declarations | Rec 7 (modified) |
| P2 | Structured `ValidationError` with `Literal` error types | Rec 8 (modified) |
| P2 | `pyproject.toml` packaging + fix bare imports | Rec 5 (modified) |
| P2 | Schema evolution regression tests | Rec 6 (retained) |
| P2 | `frozen=True` on `TemplateContext` hierarchy | Adopted from functional-typing |
| P2 | Document extension contracts in spec 005 | Adopted from game-engine-advocate |
| P2 | `PathList` custom type with Pydantic serializer | Adopted from functional-typing + self |
| P2 | VALID_MODES as dynamic registry from `schema/modes/*.yml` | Adopted from game-engine-advocate |
| P2 | Mandate Python in spec Section 6 | Adopted from functional-typing |
| P3 | Document core-variable vs. plugin-variable namespace rule | N3 (new) |
| P3 | Fix `AGENT_DOCS` type discrepancy in spec | Rec 10 (retained) |
| P3 | Document `required: True` default in spec | Adopted from functional-typing |

### Assessment of the Review Process

This four-phase review (review, cross-review, revision, disputes) has materially improved the recommendations. The most significant corrections were:

1. **game-engine-advocate's scope discipline.** Seven of their ten original recommendations were spec 007 concerns. The cross-review and revision process correctly identified and deferred them. The remaining three (VALID_MODES, MODE_PRESENCE, schema versioning) are genuine spec 005 internal consistency fixes.

2. **functional-typing's purity enforcement.** Their identification of the `sys.exit()` impurity in schema loaders exposed a blind spot in my own review — I proposed a programmatic API without verifying that its foundation was composable. This is the single most valuable correction in the entire process.

3. **The MODE_PRESENCE convergence.** Three reviewers with different perspectives (functional purity, plugin extensibility, integration architecture) arrived at the same solution (mode schema YAML declarations) through different reasoning paths. This convergence, reached through genuine intellectual correction rather than compromise, is the strongest signal that the solution is correct.

The spec 005 foundation is solid. The improvements identified through this review will make it a reliable substrate for specs 006, 007, and 008.

---

### Referenced Documentation

- `linter/models.py` — L23-35 (frozen sets), L108-122 (mode validation), L129-140 (TemplateContext with `extra = "forbid"`), L262-270 (PHASE_CONTEXT_MODELS)
- `linter/validate.py` — L24-28 (bare imports), L35-67 (schema loading with `sys.exit()`), L108-144 (MODE_PRESENCE hardcoded table), L299-305 (error concatenation as `list[str]`)
- `specs/005-generalized-templates/spec.md` — L71 (SC-003, adding modes via YAML), L362 (implementation notes saying "Python or shell")
- `specs/006-inter-round-arbitration/spec.md` — FR-009 (PRIOR_ARBITRATION_PATH), FR-013 (ARBITRATION_PATHS), FR-014 (Resolution Attribution)
- `specs/008-executable-conversus/001-executable-conversus.md` — programmatic orchestration requiring importable linter
- All three revised positions: `functional-typing/revision.md`, `game-engine-advocate/revision.md`, `integration-architect/revision.md`
