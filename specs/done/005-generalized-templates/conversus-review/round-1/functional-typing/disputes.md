# Functional-Typing Final Disputes: Spec 005 — Generalized Template Schema, Variables, and Linter

**Reviewer**: functional-typing
**Phase**: 4 (Final Disputes and Convergence)
**Date**: 2026-03-21

---

## Remaining Disputes

### Dispute 1: `plugin_data: dict[str, Any]` on core models violates Constitution Principle IX

**Parties**: functional-typing vs. integration-architect (N4)

integration-architect's revised position (N4) proposes adding `plugin_data: dict[str, Any] = {}` to `TemplateContext` as a "typed escape hatch" for spec 007 plugins. This directly contradicts Constitution Principle IX, which prohibits `Any` "unless wrapping an untyped third-party API" (`constitution.md`, L183-184). A plugin extension point is not an untyped third-party API -- it is a known, designable boundary that should receive its own typed model.

game-engine-advocate's revised position concedes this same point: "functional-typing correctly identifies that `dict[str, Any]` contradicts Constitution Principle IX's prohibition on `Any`." game-engine-advocate further accepts that the composition approach (separate `PluginContext` alongside `TemplateContext`) is superior.

Two of three reviewers converge on composition over escape hatches. integration-architect stands alone in proposing `dict[str, Any]`. The dispute is whether spec 005 should introduce an `Any`-typed field to accommodate a spec that does not yet exist. My position: it should not. The `extra = "forbid"` constraint should remain uncompromised in spec 005. Spec 007 designs its own typed `PluginContext` model at that time.

**Status**: Active dispute. I will not accept `dict[str, Any]` on any core model under any framing.

---

### Dispute 2: Programmatic API parameter design -- `known_plugin_variables` vs. clean initial interface

**Parties**: functional-typing vs. game-engine-advocate (N1)

game-engine-advocate's revised position (N1) proposes that the programmatic `validate_all()` API should accept a `known_plugin_variables: frozenset[str] = frozenset()` parameter from the start, so spec 007 does not need to extend the signature later. integration-architect's revised position takes a middle path: design the API to be extensible (`**kwargs` or a `ValidationConfig` model) without explicitly naming plugin variables.

I dispute the inclusion of `known_plugin_variables` in the initial API. This is speculative interface design -- adding a parameter for a consumer that does not exist, based on assumptions about how spec 007 will integrate with validation. The parameter is free (has a default, changes nothing when empty), but it communicates a contract promise to plugin authors before the contract is designed. If spec 007's plugin system works differently than anticipated (e.g., plugins register their own validators rather than whitelisting variable names), the parameter becomes misleading API surface that must be maintained for backward compatibility.

The cleaner approach: `validate_all(root: Path, mode: Optional[str] = None) -> ValidationResult`. When spec 007 ships, it extends the interface based on actual needs. If the extension is a parameter, it adds one. If the extension is a `ValidationConfig` model (as integration-architect suggests), it replaces the parameter list. Neither change is breaking because the programmatic API has no external consumers until spec 008.

integration-architect's `ValidationConfig` model suggestion is acceptable as a future extension mechanism but should not be implemented in spec 005.

**Status**: Active dispute. The initial API should be minimal and correct, not speculatively forward-compatible.

---

### Dispute 3: Schema version field -- timing relative to spec 006

**Parties**: functional-typing vs. integration-architect (Rec 9) and game-engine-advocate (Rec 5)

Both integration-architect and game-engine-advocate upgraded schema versioning to P2, arguing it should exist before spec 006's schema changes. integration-architect frames this as the strongest argument: "Adding versioning before that event means the first schema change is already versioned."

I do not dispute the value of schema versioning. I dispute the P2 priority within spec 005's scope. The version field has no consumer today -- no code reads it, no tooling checks it, no contract depends on it. Adding `schema_version: "1.0.0"` to `variables.yml` is a one-line YAML change with zero validation logic. It can be added at the same time as spec 006's schema changes without any additional cost. The argument "do it first so the first change is versioned" conflates temporal ordering with implementation coupling. Both changes (version field + spec 006 variables) can ship in the same commit.

If the version field must exist before spec 006, it is a P3 editorial addition -- a line of YAML with no linter enforcement, no Pydantic model field, and no validation logic. Elevating it to P2 implies implementation work that does not exist.

**Status**: Minor dispute. I accept the recommendation but dispute the priority elevation. P3 is correct for a field with no consumer.

---

## Convergence

### Full convergence (all three reviewers agree)

1. **Purify schema-loading functions (Rec 1)**: All three reviewers agree that `load_variables_schema`, `load_mode_schema`, and `find_project_root` must raise `SchemaLoadError` instead of calling `sys.exit(2)`. The CLI `main()` catches the exception. This is a prerequisite for the programmatic API. Priority: P1.

2. **Move MODE_PRESENCE to mode schema YAML files**: All three reviewers converge on encoding `mode_presence` (or `mode_in_phases`) in mode schema YAML files rather than maintaining the hardcoded 28-entry dict in `validate.py`. The linter derives the lookup at load time. integration-architect retracted the contradictory Alignment endorsement. game-engine-advocate withdrew the template-scanning alternative. I withdrew the `condition`-field derivation approach. Priority: P2.

3. **Mandate Python in spec Implementation Notes (Rec 6)**: Unanimous. The spec's Section 6 should say "Python script following Constitution Principle IX," not "Python or shell." Priority: P2.

4. **Document the `required: True` default (Rec 9)**: Unanimous. Editorial addition to spec Section 3. Priority: P3.

5. **Do not use `Literal` types for mode or variable type enums (Rec 3 withdrawal)**: All three reviewers agree that `Literal` types for `ModeSchema.mode` and `VariableDefinition.type` would conflict with the spec's extensibility story (SC-003). The `@field_validator` pattern is correct. I accept this withdrawal of my original recommendation.

6. **Do not mark `PHASE_CONTEXT_MODELS` as `Final` (Rec 8 withdrawal)**: All three reviewers agree this is a registry that spec 007 needs to extend, not an immutable constant. I accept this withdrawal.

7. **Structured `LintError` Pydantic model for error returns**: All three reviewers agree that `list[str]` is the wrong error representation. Validation errors should be Pydantic models with typed fields (`error_type`, `file_path`, `variable_name`, `phase`, `mode`, `message`, `suggestion`). The remaining minor disagreement (integration-architect uses `Literal` for `error_type`; game-engine-advocate prefers `str` for extensibility) is a spec 007 concern, not a spec 005 one. For spec 005 scope, `Literal` with the known error types is correct.

8. **`extra = "forbid"` preserved on all core `TemplateContext` models**: All three reviewers converge on maintaining `extra = "forbid"`. game-engine-advocate withdrew `extra = "allow"`. The remaining disagreement is about the escape hatch mechanism (see Dispute 1), not about the core constraint.

9. **Bare imports must be fixed**: All three reviewers agree that `from models import ...` in `validate.py` must become package-relative imports for the linter to function as an importable package. Priority: P2.

10. **Programmatic validation API**: All three reviewers agree that `validate_all()` should exist as a function returning structured results, decoupled from the Click CLI. The disagreement is about parameter design (Dispute 2), not about the API's existence. Priority: P1.

### Convergence between two reviewers

1. **`PathList` custom type** (functional-typing + integration-architect): Both agree on a Pydantic custom type that stores `list[Path]` internally and serializes to newline-separated strings for template substitution. game-engine-advocate does not dispute this but did not explicitly address the serialization concern. This is the correct resolution of Rec 2 (path-list fields).

2. **`frozen=True` on `TemplateContext`** (functional-typing + integration-architect): Both agree that `frozen=True` is correct for spec 005's core models. game-engine-advocate's concern about plugin extensibility is addressed by the composition pattern (separate `PluginContext`), which all three accept for spec 007. The disagreement is resolved: freeze now, compose later.

3. **New fields use typed patterns** (functional-typing + integration-architect): Both agree that any new path or path-list fields (spec 006's `PRIOR_ARBITRATION_PATH`, `ARBITRATION_PATHS`) must use `Path` and `PathList` types, not `Optional[str]`. game-engine-advocate does not dispute this.

4. **`config_conditions` with typed `ConfigCondition` model** (functional-typing + integration-architect): Both agree that integration-architect's `config_conditions` field should use a typed Pydantic model rather than `dict[str, str]`. game-engine-advocate defers this to spec 007 Phase 1 but does not dispute the typed approach.

---

## Final Position Statement

### Non-Negotiables

These positions reflect constitutional mandates or architectural correctness that I will not compromise on:

1. **No `Any` types on core models.** Constitution Principle IX prohibits `Any` except for wrapping untyped third-party APIs. `plugin_data: dict[str, Any]` is not an untyped third-party API -- it is a designable extension point. The composition pattern (`PluginContext` alongside `TemplateContext`) satisfies both type safety and extensibility. If the synthesizer includes `dict[str, Any]` on a core model, I record a constitutional violation.

2. **Schema-loading functions must be pure.** Functions labeled "pure functions" in their comment header (`validate.py`, L31-33) that call `sys.exit()` and `click.echo()` are impure. They must raise `SchemaLoadError`. The CLI catches it. This is not a style preference -- it is the prerequisite for every downstream integration (programmatic API, spec 008 orchestrator, spec 007 plugin validation). All three reviewers agree.

3. **Error returns must be typed Pydantic models.** Constitution Principle IX mandates Pydantic models for "ALL data structures" (`constitution.md`, L175-176). Validation errors are unambiguously a data structure. `list[str]` is not acceptable as the programmatic return type. The human-readable string formatting belongs in the CLI layer, not in the validation functions.

4. **`frozen=True` on `TemplateContext` and subclasses.** Immutability of context objects is architecturally correct: context construction is complete before template substitution begins. Mutation after construction is a bug category that `frozen=True` eliminates at the type level. This does not conflict with plugin extensibility because plugins use a separate composition model, not inheritance from frozen core models.

5. **`extra = "forbid"` on all core `TemplateContext` models, with no escape hatches in spec 005.** The typo-catching safety of `extra = "forbid"` is the entire reason the model hierarchy exists. Any weakening of this constraint (whether `extra = "allow"` or `dict[str, Any]` fields) must be designed as part of the extension system that needs it (spec 007), not pre-emptively added to spec 005.

### Flexibility

These positions I hold but will defer to the synthesizer if the majority disagrees:

1. **Schema version priority.** I accept that `schema_version` should be added. I prefer P3 (it is one line of YAML with no validation logic) but will accept P2 if the synthesizer determines that temporal ordering relative to spec 006 justifies the elevation.

2. **Programmatic API parameter design.** I prefer a minimal initial signature (`root: Path, mode: Optional[str]`) over a speculatively forward-compatible one (`known_plugin_variables: frozenset[str]`). But if the synthesizer determines that the cost of the parameter is truly zero and the signal to spec 007 implementers is worth it, I will accept the extended signature with the `frozenset()` default.

3. **`__all__` exports timing.** I deferred this to post-spec-007 in my revision. If the synthesizer determines that defining `__all__` now provides value (e.g., preventing accidental reliance on internal symbols), I will accept it with the understanding that the export list will need revision when spec 007 ships.

4. **`Literal` for `ValidationError.error_type`.** I agree with integration-architect that `Literal` is correct for the known error types in spec 005's scope. If game-engine-advocate's concern about plugin error types prevails and the synthesizer prefers `str`, I will accept it -- the constitution's `Literal` guidance applies to "precise type narrowing" and a case can be made that error types are an open set.

5. **`config_conditions` scope.** integration-architect assigns P1 to this as a spec 006 prerequisite. game-engine-advocate defers it to spec 007. I lean toward integration-architect's position (the use case is concrete and near-term) but will accept deferral if the synthesizer determines that spec 006 can ship without it.

6. **Condition field formalization (game-engine-advocate N3).** Formalizing the free-text `condition` field syntax is a good idea at P3. It serves both the MODE_PRESENCE derivation and the `config_condition` mechanism. I will support this if the synthesizer includes it, but I do not consider it essential for spec 005.

---

### Referenced Documentation

- `.specify/memory/constitution.md` -- L149-151 (pure functions), L153-154 (no mutable global state), L162-164 (immutable data structures), L171 (non-negotiable explicit typing), L175-177 (Pydantic mandate), L182-184 (Literal/Optional/Union, `Any` prohibition)
- `specs/005-generalized-templates/spec.md` -- L71 (SC-003, adding "auction" mode), L362 (implementation notes)
- `linter/models.py` -- L140 (model_config extra=forbid), L262-270 (PHASE_CONTEXT_MODELS)
- `linter/validate.py` -- L31-33 (mislabeled "pure functions" header), L35-67 (schema loading with sys.exit), L108-144 (MODE_PRESENCE), L299-305 (error concatenation)
- Revised positions: functional-typing/revision.md, game-engine-advocate/revision.md, integration-architect/revision.md
