# Game Engine Advocate — Final Disputes and Convergence

**Reviewer role**: game-engine-advocate (spec 007)
**Target**: spec 005 — Generalized Template Schema, Variables, and Linter
**Phase**: 4 (Final Disputes)
**Date**: 2026-03-21

---

## Remaining Disputes

### Dispute 1: The programmatic validation API must accept a plugin-variables parameter from day one

**Disputed with**: integration-architect

The integration-architect's revised position on the programmatic API (`validate_all(root, mode) -> ValidationResult`) explicitly rejects plugin awareness at the API boundary: "a `plugin_variables: frozenset[str]` parameter on `validate_all()` is a spec 007 concern. The API should be designed to be extensible (accepting `**kwargs` or a `ValidationConfig` model), but the initial implementation need not include plugin awareness."

I dispute this. The distinction between "designed to be extensible" and "includes a typed parameter" is the difference between a vague intention and an enforceable contract. `**kwargs` is not a design; it is the absence of a design. A `ValidationConfig` model is acceptable only if its schema includes `known_plugin_variables: frozenset[str] = frozenset()` from the start. The parameter costs nothing -- its default is the empty frozenset, making behavior identical to a version without it. But omitting it means spec 007 must either (a) add a parameter to a public API, which is a breaking change if anyone has written code against the original signature, or (b) work around the API by pre-filtering validation results, which is fragile.

This is not speculative. Spec 007 Phase 1 is plugin infrastructure. The first thing a plugin does after registration is declare its variables. The first thing the linter does is reject those variables as unknown. The API must have a mechanism to suppress that rejection. A typed frozenset parameter is the minimal, zero-cost, forward-compatible solution.

I do not accept `**kwargs` or "extensible in spirit" as a substitute for a concrete parameter.

**Non-negotiable**: The programmatic API signature must include a mechanism for callers to declare additional known variables. `known_plugin_variables: frozenset[str] = frozenset()` or a `ValidationConfig` model containing that field.

---

### Dispute 2: `plugin_data: dict[str, Any]` on TemplateContext violates the same principle it claims to serve

**Disputed with**: integration-architect

The integration-architect's new recommendation N4 proposes: "add a scoped `plugin_data: dict[str, Any]` field on `TemplateContext` (with a default of empty dict). This preserves `extra = 'forbid'` for all core fields while providing a typed escape hatch for plugins."

This is not a typed escape hatch. `dict[str, Any]` is the definition of an untyped escape hatch. Constitution Principle IX (`constitution.md`, L183-184) prohibits `Any` "unless wrapping an untyped third-party API." Plugin data is not an untyped third-party API -- it is a known extension point under our control. The integration-architect correctly rejected `extra = "allow"` on the grounds that it sacrifices type safety, but then proposed `plugin_data: dict[str, Any]`, which sacrifices the same type safety in a slightly different location.

functional-typing's revised position correctly identifies this same problem and proposes the right architecture: a separate `PluginContext(BaseModel)` composed alongside `TemplateContext`, where plugins register their own typed Pydantic models. I agree with functional-typing on this point.

However, this architecture belongs to spec 007, not spec 005. The correct spec 005 action is: do not add `plugin_data` to `TemplateContext`. Leave the models as they are. Document (per my recommendation 9) that plugin-contributed data will flow through a parallel composition mechanism designed in spec 007. Do not pre-build a `dict[str, Any]` escape hatch that will need to be removed when the proper typed mechanism arrives.

**Non-negotiable**: No `dict[str, Any]` field on any core TemplateContext model. If a plugin extension point is added to spec 005, it must be typed. If it cannot be typed yet (because the plugin interface is not designed), defer it entirely to spec 007.

---

### Dispute 3: `ValidationError.error_type` should use `str`, not `Literal`, for forward compatibility

**Disputed with**: integration-architect

The integration-architect's revised recommendation 8 proposes: `error_type: Literal["missing_variable", "unknown_variable", "missing_heading", "missing_marker", "missing_mode_variable"]`. They explicitly reject `str` on the grounds that it would "sacrifice the type safety that is the entire point of the recommendation."

This is the same argument functional-typing originally made for `Literal` on `ModeSchema.mode`, which all three reviewers -- including the integration-architect -- now agree was wrong. The logic is identical: a `Literal` type is a compile-time closed enum. When spec 007 adds plugin validation rules, a plugin that produces a `ValidationError` with `error_type = "invalid_plugin_config"` will fail Pydantic validation because that string is not in the `Literal` set. The integration-architect acknowledges this ("the `Literal` can be expanded or a `PluginValidationError` subclass can be added") but "expanding a Literal" means modifying core source code, which is exactly the extensibility anti-pattern we agreed to avoid for modes.

The resolution is the same one functional-typing adopted for modes: use `str` with a `@field_validator` that checks against a known set. The known set can be expanded at runtime when plugins register their error types. Alternatively, use `Annotated[str, AfterValidator(...)]` for Pydantic-level runtime validation that keeps the type nominally open.

The integration-architect's own argument from the mode discussion applies here: the question is not whether the set changes frequently, but whether the change path requires source code modification or runtime registration. Plugin-contributed validation rules require runtime registration. Therefore `Literal` is wrong for the same reason it was wrong for modes.

**Non-negotiable**: `error_type` must not be a `Literal`. Use `str` with runtime validation against an extensible set, consistent with the mode validation pattern.

---

### Dispute 4: Bare import fix (N2) must be sequenced before or alongside the programmatic API, not treated as a separate P2

**Disputed with**: integration-architect (sequencing)

The integration-architect treats the `pyproject.toml` / import path fix as a P2 recommendation, independent of the P1 programmatic API. This sequencing is wrong. The programmatic API is useless if the package cannot be imported. `from conversus.linter.models import TemplateContext` fails today because `validate.py` uses bare imports (`from models import ...`, L24-28). Building `validate_all()` on top of a non-importable module produces a function that exists but cannot be called from outside the `linter/` directory.

This is not a P2 enhancement; it is a prerequisite for the P1 programmatic API, the same way schema-loader purification is a prerequisite. The integration-architect correctly identified that purifying loaders is part of the same unit of work as the programmatic API (revised recommendation 2). The import fix is equally prerequisite.

**Position**: The import fix must be part of the P1 programmatic API unit of work, not a separate P2 item.

---

## Convergence

### Convergence 1: `VALID_MODES` must be derived from filesystem scanning, not hardcoded (unanimous)

All three reviewers converge on this. functional-typing withdrew the `Literal` proposal. The integration-architect agrees the hardcoded frozenset contradicts SC-003 and US-3 AC-2. My original recommendation (P1) was correctly downgraded to P2 by the integration-architect's observation that this is a spec 005 internal consistency fix, not an urgent spec 007 dependency. The implementation approach is clear: the `validate_mode` field validator reads from `schema/modes/*.yml` at load time, exactly as `main()` already does at L323-325 of `validate.py`.

**Converged position**: P2. Derive `VALID_MODES` by scanning `schema/modes/*.yml`. The `@field_validator` pattern is preserved; only the source of the valid set changes.

---

### Convergence 2: `MODE_PRESENCE` belongs in mode schema YAML files as explicit declarations (unanimous)

All three reviewers converge on this after a productive three-way debate. functional-typing conceded that the `condition` field is not machine-parseable for this purpose. I conceded that template scanning creates circular validation. The integration-architect retracted the contradictory Alignment endorsement of the hardcoded table. The resolution is clear: each mode schema YAML file declares a `mode_in_phases` (or `mode_presence`) field listing the phases where `{MODE}` is expected. A pure function derives the lookup table from these declarations at load time.

**Converged position**: P2. Add `mode_presence` or `mode_in_phases` to mode schema YAML. Derive lookup via pure function. Delete the hardcoded 28-entry dict.

---

### Convergence 3: Schema loaders must be purified as a prerequisite for the programmatic API (unanimous)

All three reviewers agree that `load_variables_schema`, `load_mode_schema`, and `find_project_root` calling `sys.exit(2)` and `click.echo()` is incoherent with a composable programmatic API. The resolution is unanimously `SchemaLoadError` exceptions, caught by `main()` at the CLI boundary. This is P1 and prerequisite for any downstream consumption of the linter as a library.

**Converged position**: P1. Replace `sys.exit()` / `click.echo()` with `SchemaLoadError`. CLI `main()` catches and exits.

---

### Convergence 4: `frozen=True` on core TemplateContext models is correct for spec 005 (functional-typing + game-engine-advocate)

functional-typing maintains `frozen=True` on core models. I accept this for spec 005's scope. My original `extra = "allow"` proposal was correctly rejected by both cross-reviewers. The right architecture is composition: a separate `PluginContext` alongside frozen core models, designed in spec 007. I withdraw all objections to `frozen=True` on spec 005 models.

**Converged position**: Apply `frozen=True`. Plugin extensibility is spec 007's concern, addressed via composition, not inheritance or relaxation.

---

### Convergence 5: Schema versioning before spec 006's first schema evolution (integration-architect + game-engine-advocate)

Both the integration-architect and I agree on P2 for schema versioning, justified by spec 006's imminent addition of `PRIOR_ARBITRATION_PATH` and `ARBITRATION_PATHS`. Adding `schema_version: "1.0.0"` before the first schema change means the change is versioned from the start. functional-typing defers this to spec 008, but the spec 006 argument is more concrete: spec 006 is the first consumer that changes the schema contract.

**Converged position**: P2. Add `schema_version: "1.0.0"` to `variables.yml` before spec 006 ships.

---

### Convergence 6: Structured `LintError` / `ValidationError` Pydantic model for error returns (unanimous)

All three reviewers agree that `list[str]` is the wrong error representation. functional-typing withdrew the `itertools.chain` suggestion. The integration-architect proposed `ValidationError` with structured fields. I agree on the model structure. The sole remaining dispute is the `error_type` field's type (`Literal` vs `str` -- see Dispute 3 above), not the existence of the model itself.

**Converged position**: P2. Define a `LintError` or `ValidationError` Pydantic model with `error_type`, `file_path`, `phase`, `mode`, `variable_name`, `message`, and `suggestion` fields. Replace `list[str]` returns with `list[LintError]`.

---

### Convergence 7: Extension contract documentation in spec 005 (all three reviewers)

All reviewers agree that documenting which parts of spec 005 are extension points and which are closed is low-cost and high-value. My deferral of recommendations 1, 2, and 7 to spec 007 makes this documentation more important, not less. The integration-architect's cross-review supports it. functional-typing does not object.

**Converged position**: P2. Add a section to spec 005's implementation notes documenting: (a) new variables via schema addition, (b) new modes via YAML file creation, (c) plugin-contributed data via parallel composition (spec 007). Document that `extra = "forbid"`, template syntax, and structural markers are NOT extension points.

---

### Convergence 8: Mandate Python in spec implementation notes (unanimous)

All three reviewers agree. The spec's "Python or shell" language is stale relative to the Pydantic-based implementation. This is an editorial fix.

**Converged position**: P2. Spec Section 6 should state: "The linter MUST be a Python script following Constitution Principle IX."

---

### Convergence 9: `PathList` custom type for path-list fields (functional-typing + integration-architect, accepted by game-engine-advocate)

functional-typing's `PathList` type with a custom Pydantic serializer (stores `list[Path]` internally, renders as newline-separated strings for template substitution) is the right design. The integration-architect proposed this resolution during cross-review and functional-typing adopted it. I accept it as correct and add that `PathList` should be exported from `models.py` as a reusable type for plugin developers.

**Converged position**: P1. Define `PathList` with Pydantic validator/serializer. Apply to existing path-list fields. Require for new fields.

---

## Final Position Statement

After four phases of review, cross-review, revision, and now disputes, my position has narrowed from ten original recommendations to four remaining disputes and nine convergence points.

### What I conceded and why

I entered this review advocating aggressively for spec 007's future needs inside spec 005. The cross-review process demonstrated that seven of my ten original recommendations were scope inflation -- spec 007 concerns that do not belong in spec 005's implementation. I conceded: plugin variable namespaces (rec 1), `extra = "allow"` on TemplateContext (rec 2), float/number types (rec 4), ModeSchema extensions (rec 7), directory reservation (rec 10), and template-scanning for MODE_PRESENCE (rec 6). Each concession was earned by a specific, concrete argument from the other reviewers, not by appeals to scope hygiene alone.

The deepest correction was on `extra = "allow"`. functional-typing demonstrated that `dict[str, Any]` violates Constitution Principle IX, and the composition pattern (separate `PluginContext` alongside frozen `TemplateContext`) is architecturally superior. I withdraw `extra = "allow"` without reservation.

### What survives and why

My four remaining disputes are not speculative future concerns. They are concrete, implementable positions with zero-cost defaults:

1. **Plugin-variables parameter on the API** -- a `frozenset[str]` defaulting to empty. Costs nothing. Prevents a breaking API change when spec 007 ships.

2. **No `dict[str, Any]` on TemplateContext** -- this is a principle dispute, not a feature request. The integration-architect's `plugin_data` field violates the same Constitution Principle IX we all cite. Either type the extension point or defer it.

3. **`error_type` as `str`, not `Literal`** -- consistency with the mode validation decision. The argument that won for modes applies identically to error types: if the set is extended by plugins, `Literal` requires source code modification, which contradicts the extensibility contract.

4. **Import fix as P1 prerequisite** -- this is a sequencing correction, not a new requirement. The programmatic API cannot function without importable packages.

### Non-negotiables

If I had to reduce my entire review to a single requirement that must survive into the final synthesis, it is this:

**The programmatic validation API must include a typed mechanism for declaring additional known variables.** This is the one point where omission in spec 005 creates a concrete, measurable cost in spec 007: a breaking API change, a workaround hack, or a redesign. Every other spec 007 concern can be addressed when spec 007 ships. This one cannot, because the API signature is a public contract.

Everything else I originally asked for -- plugin namespaces, extensible context models, float types, directory reservations, ModeSchema extensions -- can be built in spec 007 without modifying spec 005. The API signature is the exception. Once published, changing it has a cost. Including `known_plugin_variables: frozenset[str] = frozenset()` has no cost. The asymmetry is clear.

---

### Priority summary (game-engine-advocate final position)

| Priority | Item | Status |
|----------|------|--------|
| P1 | Programmatic API with `known_plugin_variables` parameter | Disputed (Dispute 1) |
| P1 | Schema loader purification (`SchemaLoadError`) | Converged |
| P1 | `PathList` custom type for path-list fields | Converged |
| P1 | Import fix as prerequisite for programmatic API | Disputed (Dispute 4) |
| P2 | `VALID_MODES` as dynamic registry from filesystem | Converged |
| P2 | `MODE_PRESENCE` as YAML declarations in mode schemas | Converged |
| P2 | Schema versioning (`schema_version: "1.0.0"`) | Converged |
| P2 | Structured `LintError` model (with `str` error_type) | Partially converged (Dispute 3) |
| P2 | Extension contract documentation | Converged |
| P2 | Mandate Python in spec | Converged |
| P2 | No `dict[str, Any]` on TemplateContext | Disputed (Dispute 2) |
| Deferred | Plugin variable namespace | Deferred to spec 007 |
| Deferred | PluginContext composition architecture | Deferred to spec 007 |
| Deferred | ModeSchema extensions section | Deferred to spec 007 |
| Withdrawn | Float/number variable type | Withdrawn |
| Withdrawn | Reserve `schema/objectives/` directory | Withdrawn |

---

### Referenced Documentation

- `linter/models.py` -- L23-35 (frozen sets), L108-122 (mode validation), L129-140 (TemplateContext config), L262-270 (PHASE_CONTEXT_MODELS)
- `linter/validate.py` -- L24-28 (bare imports), L35-67 (schema loading with sys.exit), L108-144 (MODE_PRESENCE), L323-325 (filesystem mode scanning)
- `specs/005-generalized-templates/spec.md` -- L71 (SC-003), L362 (implementation notes)
- `specs/007-game-engine/spec.md` -- L66-70 (design principles), L96-112 (lifecycle hooks), L129-158 (plugin API), L216-221 (Phase 1 scope)
- `.specify/memory/constitution.md` -- L175-177 (Pydantic mandate), L183-184 (Any prohibition)
- Revised positions: functional-typing/revision.md, integration-architect/revision.md, game-engine-advocate/revision.md
