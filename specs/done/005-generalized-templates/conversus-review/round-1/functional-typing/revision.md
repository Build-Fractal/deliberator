# Functional-Typing Revision: Spec 005 — Generalized Template Schema, Variables, and Linter

**Reviewer**: functional-typing
**Revision iteration**: 1
**Date**: 2026-03-21

---

## Recommendation Dispositions

### Recommendation 1: Purify schema-loading functions (was P1)

**Disposition: MAINTAINED**

Both cross-reviewers agree this is necessary. game-engine-advocate rates it P1 for integration safety (plugins calling `load_variables_schema` as a library function cannot tolerate `sys.exit(2)`). integration-architect rates it P1 for the programmatic API (Recommendation 2 in their review) and correctly observes that building a `validate_all()` function on top of loaders that call `sys.exit()` is incoherent. integration-architect's cross-review of my work identifies the tension that their own Recommendation 1 (`config_condition`) might be sequenced first, but concedes both are independently actionable.

I accept integration-architect's point that exceptions are more Pythonic than a `Result[T, str]` type. The FP HOWTO does not prohibit exceptions in Python; it advocates for pure functions, and a function that raises a domain exception (`SchemaLoadError`) is purer than one that calls `sys.exit()`. The caller handles the exception; the function does not control process lifecycle. My original wording of "Result type" was aspirational; `SchemaLoadError` is the practical fix and both cross-reviewers converge on it.

**Revised recommendation**: `load_variables_schema`, `load_mode_schema`, and `find_project_root` should raise `SchemaLoadError` on failure. The `main()` CLI function catches it and calls `sys.exit(2)`. Priority remains P1.

---

### Recommendation 2: Replace raw `str` path-list fields with `list[Path]` (was P1)

**Disposition: MAINTAINED with modification**

integration-architect's cross-review identifies a real cascading concern: changing path-list fields to `list[Path]` affects the template substitution system, which uses `{VARIABLE}` string replacement. A `list[Path]` cannot be directly substituted into a template string. Their suggested resolution -- a `PathList` type alias with a custom Pydantic serializer that renders as newline-separated strings -- is the correct design. The model stores `list[Path]` internally for type safety; template substitution uses a `render()` method or `__str__` override.

game-engine-advocate's cross-review adds that the `PathList` type should be exported as a reusable type from `models.py` so plugin developers can use it. This is an additive extension of my recommendation, not a contradiction.

integration-architect's cross-review also flags that their own Recommendation 3 (adding `PRIOR_ARBITRATION_PATH`, `ARBITRATION_PATHS` for spec 006) would perpetuate the raw-string pattern if implemented first. I agree these should be done simultaneously: new fields should use the typed pattern from the start.

**Revised recommendation**: Define a `PathList` custom type with a Pydantic validator that parses newline-separated strings into `list[Path]` and a serializer that renders back to newline-separated strings for template substitution. Export it from `models.py` as a reusable type. Apply to all existing path-list fields and require its use for any new path-list fields (including spec 006 additions). Priority remains P1.

---

### Recommendation 3: Use `Literal` types for constrained string enumerations (was P2)

**Disposition: WITHDRAWN for modes; WITHDRAWN for variable types**

game-engine-advocate's cross-review delivers the strongest challenge in either cross-review. The argument is decisive: a `Literal` type for `ModeSchema.mode` is mutually exclusive with spec 005's own SC-003, which envisions adding an "auction" mode by creating a YAML file alone. A `Literal` type is a compile-time fixed enumeration -- changing the set of valid modes requires modifying source code, which contradicts the schema-first extensibility story. The `@field_validator` pattern can be loosened to read from a dynamic set; a `Literal` type cannot.

integration-architect's cross-review reaches a nuanced middle position: use `Literal` for modes (rarely changing) but keep runtime validation for variable types (still evolving, given `extracted-content` was a late addition). However, game-engine-advocate's argument applies even to rarely-changing sets: the point is not frequency of change but whether the change path requires a code modification or a YAML addition. The spec explicitly promises the YAML-only path.

For `VariableDefinition.type`, the extensibility concern is equally present: spec 007 may need `float`/`number`, and `extracted-content` was itself a late addition. Applying `Literal` to variable types would create the same friction for schema evolution that game-engine-advocate identifies for modes. The constitution's instruction to use `Literal` for "precise type narrowing" (`constitution.md`, L182-184) must be read in context: it applies when the valid values are defined by the program itself, not when they are defined by external schema files that the program reads.

game-engine-advocate's suggested alternative -- `Annotated[str, AfterValidator(...)]` -- preserves runtime validation while keeping the type open. This is the right pattern for both `mode` and `type`.

**Revised recommendation**: Withdraw the `Literal` recommendation for both `ModeSchema.mode` and `VariableDefinition.type`. Keep the `@field_validator` pattern. For improved tooling support without closing the enum, consider `Annotated[str, AfterValidator(...)]`. Priority: N/A (withdrawn).

---

### Recommendation 4: Make `TemplateContext` models frozen (was P2)

**Disposition: MAINTAINED with scope qualification**

game-engine-advocate's cross-review raises a real concern: `frozen=True` combined with `extra = "forbid"` creates "the maximally hostile surface for plugin extensibility." Their proposed resolution -- a `CoreTemplateContext(frozen=True, extra="forbid")` and a `PluginTemplateContext(frozen=True, extra="allow")` split, or a `plugin_data: dict[str, Any]` field -- addresses a legitimate future need.

However, I maintain that `frozen=True` is correct for the core models in spec 005's scope. integration-architect's cross-review agrees: "Accept `frozen=True`. It enforces the discipline that context construction is complete before template substitution begins, which is architecturally correct." The orchestrator should use a builder function that returns a complete dict, then calls `ContextModel.model_validate(complete_dict)`.

game-engine-advocate's concern about plugin extensibility is valid but belongs to spec 007's design phase. The correct sequence is: freeze the core models now (spec 005), then design the extension mechanism (spec 007 Phase 1) with full knowledge of the frozen constraint. Relaxing immutability now to accommodate a speculative plugin interface would violate the principle of making the current system correct before extending it.

I reject the `plugin_data: dict[str, Any]` escape hatch -- Constitution Principle IX prohibits `Any` "unless wrapping an untyped third-party API" (`constitution.md`, L183-184). game-engine-advocate's own alternative -- a separate `PluginContext` composed alongside `TemplateContext` -- is the right direction for spec 007 but is out of scope for spec 005.

**Revised recommendation**: Apply `frozen=True` to `TemplateContext` and all subclasses. Document in a code comment that spec 007 will introduce a separate `PluginContext` model for extension data, composed alongside (not inherited from) the frozen core models. Priority remains P2.

---

### Recommendation 5: Derive `MODE_PRESENCE` from schema data (was P2)

**Disposition: MODIFIED -- adopt mode schema YAML approach**

This recommendation received the most substantive cross-review challenges. integration-architect's cross-review of my work identifies a genuine contradiction: their Alignment section calls the hardcoded table "the right approach" while their Recommendation 7 proposes moving it to mode schema YAML files. My cross-review of integration-architect correctly flagged this internal contradiction. However, integration-architect's self-contradiction does not validate my original approach.

My original proposal -- derive from `variables.yml`'s `condition` field via a pure function -- has a flaw that integration-architect identifies: the `condition` field is free-text (e.g., `"rounds > 1"`), not machine-parseable in a way that would produce the 28-entry boolean mapping. To make my approach work, the `condition` field syntax would need to be formalized into a machine-readable DSL. This is tractable but adds specification work that neither the spec nor the constitution mandates.

game-engine-advocate proposes encoding mode presence in mode schema files as `mode_in_phases`. integration-architect's Recommendation 7 converges on the same location. Both argue from the plugin perspective: when a plugin introduces a new mode, it provides a mode schema file, and that file should declare where `MODE` is expected. Asking plugin authors to modify core `variables.yml` defeats plugin isolation.

I concede this point. The mode schema is the more natural home for mode-presence data. Each mode schema already declares its variables and templates; adding `mode_in_phases: [synthesis, arbitration, cross-round-synthesis]` is a minimal, schema-coherent extension. The linter derives the lookup table from mode schemas at load time via a pure function -- satisfying my functional programming concern without the free-text parsing problem.

**Revised recommendation**: Add a `mode_in_phases` field to mode schema YAML files listing phases where `MODE` is expected. Derive the `MODE_PRESENCE` lookup at load time via a pure function `compute_mode_presence(mode_schemas: list[ModeSchema]) -> dict[tuple[str, str], bool]`. Delete the hardcoded 28-entry dict. Priority remains P2.

---

### Recommendation 6: Mandate Python in spec Implementation Notes (was P2)

**Disposition: MAINTAINED**

All three reviewers agree, explicitly or implicitly. game-engine-advocate's cross-review states "functional-typing's recommendation to mandate Python in the spec is correct and compatible with spec 007's requirements." integration-architect's cross-review agrees: "The linter is already implemented in Python with Pydantic models. The spec language is outdated relative to the implementation. Updating it is editorial, not architectural."

No modification needed. The spec's Section 6 should say: "The linter MUST be a Python script following Constitution Principle IX (functional programming, explicit typing, Pydantic models)."

**Revised recommendation**: Unchanged. Priority remains P2.

---

### Recommendation 7: Add `__all__` exports to `models.py` (was P3)

**Disposition: DEFERRED**

game-engine-advocate's cross-review raises a valid concern: `__all__` restricts the public API surface, and spec 007 may need to import internal types (the `TemplateContext` hierarchy, `VariableDefinition`, the frozenset constants) for plugin validation. Defining `__all__` before knowing the plugin interface needs is premature API lockdown.

integration-architect's cross-review does not challenge this recommendation directly but notes it competes with higher-value work (schema evolution tests).

I accept game-engine-advocate's argument. `__all__` is a good practice for stable, closed modules, but `models.py` is about to become a shared foundation for a plugin ecosystem. The `__all__` decision should be made after spec 007 Phase 1 defines which symbols are core-stable vs plugin-extensible. This is not a withdrawal -- the recommendation is correct in principle -- but it should be deferred until the public API surface is known.

**Revised recommendation**: Defer `__all__` to post-spec-007-Phase-1 when the extension contract is defined. Priority: deferred.

---

### Recommendation 8: Type `PHASE_CONTEXT_MODELS` as `Final` (was P3)

**Disposition: WITHDRAWN**

game-engine-advocate identifies `PHASE_CONTEXT_MODELS` as "the exact pattern spec 007 needs for registering plugin-contributed context models" and envisions plugins extending it at load time. Marking it `Final` tells type checkers and developers that it must not be modified -- which is exactly what plugins need to do.

My cross-review of game-engine-advocate acknowledged this tension but did not resolve it. On reflection, game-engine-advocate is right: `PHASE_CONTEXT_MODELS` is a registry, not a constant. The `frozenset` pattern is correct for genuinely immutable data (like `VALID_VARIABLE_TYPES` in its current closed scope), but a mapping from phase names to context model classes is exactly the kind of binding that an extension system needs to augment. Marking it `Final` would force spec 007 to work around the type system rather than with it.

integration-architect's cross-review offers weak agreement with my position ("Both reviews value immutability of the mapping") but at medium confidence. The game-engine concern is more concrete: there is a named spec (007) that needs this to be extensible.

**Revised recommendation**: Withdraw. Do not mark `PHASE_CONTEXT_MODELS` as `Final`. If immutability is desired before plugin loading, use a runtime freeze pattern (deep-copy and freeze after plugin registration) rather than a compile-time `Final` annotation.

---

### Recommendation 9: Document the `required: True` default in the spec (was P3)

**Disposition: MAINTAINED**

Both cross-reviewers agree. integration-architect's cross-review rates this at high confidence: "This is an editorial fix with no implementation cost and direct documentation value." game-engine-advocate's cross-review agrees: "This is a spec-quality concern unrelated to game-engine extensibility. No contradiction; it should be addressed."

No modification needed.

**Revised recommendation**: Unchanged. Add to spec Section 3: "Variables default to `required: true` when the field is omitted. Set `required: false` explicitly for optional variables." Priority remains P3.

---

## New Recommendations

### New Recommendation A: Replace `list[str]` error returns with structured Pydantic models (Priority: P2)

integration-architect's cross-review of my work correctly identifies that my `itertools.chain.from_iterable` suggestion (original Missed Opportunity #5) optimizes the concatenation of the wrong abstraction. The real issue is not how error lists are concatenated but that errors are untyped strings. integration-architect's Recommendation 8 proposes a `ValidationError` Pydantic model with `error_type`, `variable_name`, `phase`, `mode`, and `suggestion` fields.

This is correct. My original review praised `list[str]` as a pure return type (Alignment #2) but did not question whether strings are the right error representation. They are not. Constitution Principle IX mandates Pydantic models for "ALL data structures" (`constitution.md`, L175-176), and validation error results are unambiguously a data structure. Spec 008's orchestrator will need to programmatically distinguish error types (missing marker is blocking; unknown variable may be a warning). String parsing for programmatic decisions is precisely the fragility the linter was built to prevent.

I withdraw my `itertools.chain.from_iterable` suggestion (original Missed Opportunity #5). Once errors are Pydantic models, the aggregation mechanism is irrelevant -- list concatenation, `itertools.chain`, or a container type all work equivalently for typed objects.

**Recommendation**: Define a `LintError(BaseModel)` with fields: `error_type: str`, `file_path: str`, `variable_name: Optional[str]`, `phase: str`, `mode: str`, `message: str`, `suggestion: Optional[str]`. Change all `check_*` functions to return `list[LintError]`. The CLI `main()` formats these for human display; the programmatic API returns them directly.

### New Recommendation B: Ensure new spec 006 fields use typed patterns from the start (Priority: P2)

My cross-review of integration-architect's work identified a sequencing risk: integration-architect's Recommendation 3 (add `PRIOR_ARBITRATION_PATH`, `ARBITRATION_PATHS`, `ARBITRATION_RULINGS`) would introduce new `Optional[str]` fields that perpetuate the raw-string path-list pattern. integration-architect's cross-review of my work confirms this tension and agrees on the resolution: "Define a `PathList` type alias with a custom Pydantic serializer."

This is a coordination recommendation, not a new code change. When spec 006 fields are added to the context models, they must use `Optional[Path]` (for single paths) and `Optional[PathList]` (for path lists), not `Optional[str]`. This prevents introducing new instances of the pattern being corrected by Recommendation 2.

**Recommendation**: Any spec that adds path or path-list fields to context models must use the `Path` and `PathList` types established by Recommendation 2. Document this as a contribution guideline in `models.py`.

### New Recommendation C: Fix `AGENT_DOCS` type discrepancy in the spec (Priority: P3)

Raised by integration-architect's review (Recommendation #10) and acknowledged in their cross-review of my work (Safe Agreement #4). The spec's data model (Section 3, L171-174) shows `AGENT_DOCS` as `type: path-list`, but the implementation correctly uses `extracted-content`. The spec should be updated to match the implementation. I did not flag this in my original review -- an oversight, since it is a straightforward spec-implementation consistency issue.

**Recommendation**: Update spec Section 3 to show `AGENT_DOCS` as `type: extracted-content` to match the implementation in `models.py`.

---

## Position Summary

After reading all cross-reviews, my position has shifted materially on three recommendations and held firm on six:

**Withdrawn** (2):
- `Literal` types for modes and variable types (Rec 3) -- game-engine-advocate demonstrated this conflicts with spec 005's own extensibility story (SC-003). The `@field_validator` pattern preserves runtime validation while keeping the type open. The constitution's `Literal` guidance applies to program-defined enumerations, not schema-defined ones.
- `Final` on `PHASE_CONTEXT_MODELS` (Rec 8) -- game-engine-advocate correctly identifies this as a registry that spec 007 needs to extend, not a constant. A runtime freeze pattern after plugin registration is the right alternative.

**Modified** (3):
- `MODE_PRESENCE` derivation (Rec 5) -- I concede the mode schema YAML approach over my original `condition`-field derivation. integration-architect correctly identified that the `condition` field is not machine-parseable for this purpose, and both other reviewers converge on mode schemas as the natural location.
- `list[Path]` for path-list fields (Rec 2) -- integration-architect's `PathList` type with custom serializer addresses the template substitution cascading concern I did not anticipate.
- `__all__` exports (Rec 7) -- deferred rather than withdrawn, pending spec 007's definition of the extension contract.

**Maintained** (4):
- Purify schema-loading functions (Rec 1) -- unanimous agreement across all reviewers, confirmed as prerequisite for integration-architect's programmatic API.
- `frozen=True` on `TemplateContext` (Rec 4) -- maintained with scope qualification. integration-architect agrees it enforces correct construction discipline. Plugin extensibility is spec 007's concern, not spec 005's.
- Mandate Python in spec (Rec 6) -- unanimous.
- Document `required: True` default (Rec 9) -- unanimous.

**New** (3):
- Structured `LintError` Pydantic model for error returns (New Rec A) -- adopted from integration-architect's Recommendation 8, which correctly identifies that my `itertools.chain` suggestion optimized the wrong abstraction.
- Ensure spec 006 fields use typed patterns (New Rec B) -- coordination recommendation arising from the cross-review dialogue.
- Fix `AGENT_DOCS` type discrepancy in spec (New Rec C) -- editorial fix flagged by integration-architect that I missed.

The deepest intellectual correction is on `Literal` types (Rec 3). My original review applied Constitution Principle IX's `Literal` mandate (`constitution.md`, L182-184) without weighing it against the spec's own extensibility requirements (SC-003: adding a mode via YAML alone). game-engine-advocate demonstrated that these two mandates are in direct tension, and the extensibility story must win -- the spec is the contract, and the type system should support the contract's promises rather than constraining them. This is a case where constitutional principles must be read in context: `Literal` is prescribed for "precise type narrowing" but not for data whose valid values are defined by external schema files rather than by the program itself.

---

### Referenced Documentation

- `.firecrawl/python-functional-howto.md`
- `.specify/memory/constitution.md` -- L149-151 (pure functions), L153-154 (no mutable global state), L162-164 (immutable data structures), L171 (non-negotiable explicit typing), L175-177 (Pydantic mandate), L182-184 (Literal/Optional/Union)
- `specs/005-generalized-templates/spec.md` -- L71 (SC-003, adding "auction" mode), L171-174 (AGENT_DOCS type), L362 (implementation notes)
- `linter/models.py` -- L108-122 (mode validation), L140 (model_config), L262-270 (PHASE_CONTEXT_MODELS)
- `linter/validate.py` -- L35-67 (schema loading with sys.exit), L108-144 (MODE_PRESENCE), L299-305 (error concatenation)
- Cross-reviews received: game-engine-advocate and integration-architect cross-reviews of functional-typing
- Cross-reviews written: functional-typing cross-reviews of game-engine-advocate and integration-architect
