# Schema Engineer Cross-Review of Functional Architect's Review
# Spec 013 — Objective Function Templates

**Cross-Reviewer**: schema-engineer
**Reviewing**: functional-architect's review
**Date**: 2026-03-23

---

## Dangerous Contradictions

### DC-1: Library-level loader scope vs. single-file loader — incompatible contracts

Functional-architect's R1 specifies `load_objective_templates()` returning `dict[str, ObjectiveTemplate]` from a bulk directory scan, with embedded completeness assertions (at least 20 templates, every mode has 3+ templates, 5+ cross-mode). Schema-engineer's R-7 specifies `load_objective_template(path: Path) -> ObjectiveTemplate` as a single-file loader plus a separate `load_all_objective_templates(directory: Path | None)` that returns `list[ObjectiveTemplate]` with no cardinality assertions baked in.

These are not stylistic variations — they produce incompatible public APIs. The functional-architect's design embeds library-integrity assertions inside the loader, making the loader fail if the library is incomplete. The schema-engineer's design separates loading from integrity checking (the single-file loader is pure, bulk loading returns a list, and integrity would live separately). If both reviewers' recommendations are implemented, spec 014's pipeline will see two differently-typed entry points and cannot rely on either.

The functional-architect's position is that completeness validation belongs inside the loader (R1 step 5, R2 "a pure function that takes `dict`…"). The schema-engineer's position is that a single-file utility is the atomic unit and bulk loading is a convenience wrapper — cardinality enforcement is out of scope for a schema module (schema-engineer R-7: "Eliminates boilerplate for downstream consumers and establishes a canonical loading path"). These are irreconcilable without an architectural decision: does `objectives.py` own library-level invariants, or does that belong to a higher-level orchestration layer?

**Risk**: If functional-architect's design is adopted and the library later ships with 19 templates during incremental development, the loader throws on import. If schema-engineer's design is adopted, SC-003 ("filtering templates by mode_compatibility returns at least 3 cooperative-specific templates") becomes untestable via the schema module alone. One design or the other must be chosen.

**Citing**: functional-architect R1 (steps 1–5), R2; schema-engineer R-7.

---

### DC-2: VALID_CONSTRAINTS frozenset vs. file-system resolution — mutually exclusive validation strategies

Schema-engineer's R-2 proposes adding `VALID_CONSTRAINTS: frozenset[str]` as a hardcoded closed set mirroring `VALID_MODES` and `VALID_GAME_FORMS`, so constraint references on ObjectiveTemplate are validated against that set. Functional-architect's R1 and R2 implicitly require file-system resolution: `validate_library_integrity()` takes loaded `dict[str, ConstraintTemplate]` and checks cross-references against actual loaded constraint instances, not a hardcoded set.

These two approaches are not additive — they are in tension about what "valid constraint reference" means. The frozenset approach validates at parse time with a hardcoded registry (schema-engineer: "At minimum, a `VALID_CONSTRAINTS` frozenset mirroring `VALID_MODES` and `VALID_GAME_FORMS` would catch typos," M-2). The functional-architect's approach validates at library-load time against actual file contents (functional-architect R2: "Every constraint name referenced in any ObjectiveTemplate.constraints exists in the constraint dict"). If both are implemented, the frozenset becomes an unmaintained parallel data structure that will drift from the actual YAML files, producing false positives when constraints are added or renamed. If only the frozenset is implemented, adding a new constraint YAML requires a code change, violating the "data-driven" principle established for VALID_MODES.

**Risk**: The frozenset strategy breaks extensibility — adding a new constraint YAML silently invalidates valid templates until the frozenset is also updated. The file-resolution strategy requires a loaded library, making model_validate-time checking impossible. Choosing both produces drift. The architectural question — is the constraint registry data or code? — is unresolved between the two reviews.

**Citing**: functional-architect R2, M1, O1; schema-engineer R-2, M-2.

---

### DC-3: `extra="forbid"` on models vs. example field standardization — sequencing dependency that produces a breakage window

Schema-engineer's R-10 recommends adding `model_config = ConfigDict(extra="forbid")` to ObjectiveTemplate, ConstraintTemplate, and ParameterDefinition to reject extraneous YAML keys. Schema-engineer's R-3 separately recommends standardizing all YAML examples to flat format, noting that seven of 21 templates use nested example structures containing `name`, `form`, `game_form`, `parameters`, and `computed_objective` keys.

These two recommendations interact in a way that neither review explicitly flags: the nested example structure does not inject extra top-level keys into ObjectiveTemplate (the example is a `dict[str, Any]` field, not a flat expansion), so `extra="forbid"` on ObjectiveTemplate does not directly reject nested example content. However, if `extra="forbid"` is applied before the example structure is standardized, templates with `computed_objective` inside the example dict would still parse (it is inside the dict, not a top-level key). The false sense of safety from `extra="forbid"` could cause engineers to believe the model is rejecting format drift when the actual drift (nested example structure) is invisible to that guard.

The functional-architect does not address `extra="forbid"` at all. The functional-architect's R7 addresses example standardization only in terms of YAML content convention (M9: "flat parameter-values-only form"), without noting the model-level enforcement implication. The schema-engineer does not note that `extra="forbid"` does not protect against the example inconsistency it is implicitly assumed to catch.

**Risk**: Both recommendations can be implemented in sequence, but the breakage window — `extra="forbid"` deployed before YAML examples are standardized — may reject valid templates if any extraneous top-level keys exist in current YAML files that neither review catalogued. This must be verified against all 21 objective templates and 6 constraint templates before `extra="forbid"` is activated.

**Citing**: schema-engineer R-10, R-3, M-3; functional-architect M9, R7.

---

### DC-4: Extending the type system to `vector`/`matrix`/`boolean`/`enum` vs. minimal `boolean` addition — scope disagreement with downstream coupling

Functional-architect's R3 argues for adding `vector`, `matrix`, `boolean`, and `enum` to `VALID_PARAMETER_TYPES`, along with an `allowed_values: list[str]` field on ParameterDefinition for enum parameters, calling the current `string` type "a type-theoretic junk drawer" (M2). Schema-engineer's R-6 adds only `boolean`, scoped to the two `normalize` parameters in weighted-sum and minimax, explicitly marking vector/matrix as a design limitation rather than a bug (M-7: "a design limitation of the four-type system rather than a bug").

The disagreement is not stylistic — it determines whether ParameterDefinition's schema becomes a discriminated union (different fields for different types) or remains a flat model with type-specific validators. Functional-architect's `enum` addition requires `allowed_values: list[str]` as a new optional field on ParameterDefinition, meaning the ParameterDefinition model must grow a field that is only semantically valid for one type. If implemented, a `float`-typed parameter could carry a non-empty `allowed_values` without error unless an additional model_validator is added. The functional-architect's design is correct about the semantic gap but creates model complexity that the schema-engineer's minimal addition avoids at the cost of leaving `string`-as-vector unaddressed.

**Risk**: If the functional-architect's full extension is adopted and the YAML templates are migrated to `vector`/`matrix` types, that is a breaking change to all downstream consumers (spec 014 pipeline, any existing template authoring tooling) that schema-engineer's bounded `boolean`-only addition avoids. Conversely, schema-engineer's minimal addition leaves spec 014 unable to infer parsing logic for `weights: "0.5, 0.3, 0.2"` from the schema alone.

**Citing**: functional-architect M2, R3; schema-engineer M-7, M-8, R-6.

---

## Tensions

### T-1: Model-level example validation vs. YAML standardization first

Functional-architect's R7 recommends adding a model_validator that checks every required parameter appears in the example dict and that float/integer values satisfy range constraints. Schema-engineer's R-4 recommends the same cross-validation (example keys must match parameter names). Both agree this is desirable. The tension is in ordering: schema-engineer emphasizes that standardization must precede validation (R-3 must happen before R-4 is implementable), while functional-architect bundles both as a single recommendation without flagging the sequencing dependency.

If the model_validator is added before seven of 21 templates are standardized, those templates will fail `model_validate()` because their nested examples contain `name`, `form`, `game_form`, etc. as keys that do not correspond to any parameter name. This is a real sequencing risk that neither review flags as a deployment concern. The functional-architect's unified R7 is conceptually cleaner but operationally riskier.

**Citing**: functional-architect R7, M6; schema-engineer R-3, R-4, M-3, M-4.

---

### T-2: Empty mode_compatibility validation priority

Functional-architect's R5 flags empty `mode_compatibility: []` as a medium-priority gap creating unreachable dead infrastructure (M5), and provides the exact validator code. Schema-engineer's review does not mention this gap at all. This is an asymmetric blind spot: the schema-engineer reviewed the same ConstraintTemplate and ObjectiveTemplate models and did not identify this as a missing invariant. The functional-architect is correct — a template with no compatible modes is a degenerate case the model should prevent, analogous to the schema-engineer's own R-9 (empty `parameters: []`). The silence from schema-engineer here does not mean disagreement, but it means the gap was not identified through structural model analysis, only through thinking about downstream reachability.

The tension is in how to frame the fix: functional-architect frames it as "dead infrastructure" (Constitution XII language), schema-engineer would likely frame it as "degenerate template" (same as R-9). Both land at the same implementation but via different conceptual routes.

**Citing**: functional-architect M5, R5; schema-engineer R-9 (analogous empty-parameters guard, same pattern applied differently).

---

### T-3: `description` on ConstraintTemplate — optional vs. required field

Both reviews recommend adding `description` to ConstraintTemplate (functional-architect R6, schema-engineer M-6/O-3). The tension is in whether it should be required or optional. Functional-architect states `description: str` as a required field ("Add `description: str` to ConstraintTemplate," R6), justified by Constitution XVI (mathematical transparency). Schema-engineer's M-6 uses "optional `description` field" and marks it as a lower-concern gap (listed as missed opportunity, not off-base assumption). Schema-engineer's O-3 notes the asymmetry more strongly but still does not mandate required.

Making it required is a breaking change to all six existing constraint YAML files (none include a `description` field). Making it optional preserves backward compatibility but means the field can be absent when spec 014 needs it for LLM prompt construction. The practical resolution depends on whether the constraint YAML files are updated atomically with the model change — functional-architect assumes they will be, schema-engineer hedges.

**Citing**: functional-architect M7, R6; schema-engineer M-6, O-3.

---

### T-4: `_objective_schema_dir()` helper necessity and timing

Functional-architect's R9 marks `_objective_schema_dir()` as low priority but necessary as a prerequisite for R1's loader function (M8: "any future loader function will need to re-derive the path"). Schema-engineer's R-7 assumes this path resolution is handled implicitly within the loader utility but does not define `_schema_dir()` explicitly, using a placeholder `_schema_dir()` in the code snippet that would shadow or conflict with game_forms.py's function of the same name.

This is a minor but real tension: schema-engineer's R-7 code references `_schema_dir()` without qualification, which would either shadow the game_forms.py helper or cause a name conflict at import time if both modules are imported into the same namespace. Functional-architect's approach of naming it `_objective_schema_dir()` avoids this collision. The functional-architect's naming convention is more correct.

**Citing**: functional-architect R9, M8; schema-engineer R-7 (code snippet, `_schema_dir()` reference).

---

### T-5: Scope of `RangeSpec` model — what types may carry a range?

Both reviews recommend replacing `range: Optional[dict[str, Any]]` with a typed `RangeSpec` model (functional-architect R8; schema-engineer R-5). They agree on the structure (`min: Optional[float]`, `max: Optional[float]`, `extra="forbid"`). The tension is in whether to add a cross-field validator that rejects range specifications on non-numeric types. Functional-architect R8 explicitly recommends: "Add a model_validator to ParameterDefinition that skips range validation for non-numeric types (string, function)." Schema-engineer R-5 does not mention type-aware range validation — the RangeSpec model is presented as structurally typed but semantically agnostic.

The functional-architect is correct about the current incoherence: `budget.yml`'s `cost` parameter has `type: string` and `range: {min: 0}`, which is semantically meaningless. The schema-engineer's structural fix (typed model) would not catch this incoherence. The functional-architect's recommended cross-validator would. This is a genuine gap in schema-engineer's R-5 that the functional-architect's R8 catches.

**Citing**: functional-architect R8, O2; schema-engineer R-5, M-5.

---

## Safe Agreements

### SA-1: Both reviews agree the `string` type is overloaded and the four-type system is incomplete

Both reviewers independently identified that `string` encodes at least four structurally distinct data shapes: comma-separated numeric vectors, nested matrix literals, booleans, and enumeration values. Functional-architect catalogues this in M2 (calling it "a type-theoretic junk drawer") and recommends a full extension (R3). Schema-engineer catalogues it in M-7 (vectors/matrices as a design limitation) and M-8 (booleans as a parsing burden). The diagnosis is the same; only the prescribed cure differs in scope.

Both reviews also agree that the minimum necessary addition is `boolean` to cover the `normalize` parameter pattern. This is safe common ground: adding `"boolean"` to `VALID_PARAMETER_TYPES` and converting the two affected parameters is a backward-compatible, low-risk improvement that neither review disputes.

**Citing**: functional-architect M2, R3; schema-engineer M-7, M-8, R-6.

---

### SA-2: Both reviews agree duplicate parameter name validation is missing and must be added

Schema-engineer R-1 and functional-architect R4 provide nearly identical implementation code for detecting duplicate parameter names within a template's `parameters` list. Both flag it as a silent data corruption risk. The code patterns are equivalent (compare name lists against their set-deduplicated length, raise ValueError with sorted duplicate names). This is the strongest consensus between the two reviews: the invariant is clearly missing from the model, the fix is unambiguous, and neither reviewer has a reason to dispute the other's framing.

**Citing**: functional-architect M4, R4; schema-engineer M-1, R-1.

---

### SA-3: Both reviews agree a loader function following the `load_mode_mapping` pattern is missing and needed

Despite the scope disagreement in DC-1, both reviewers independently identified the absence of any loader utility as a gap against the established pattern in game_forms.py. Functional-architect M3 and schema-engineer M-9 arrive at identical diagnoses: the `load_mode_mapping()` precedent exists, objectives.py does not follow it, and downstream consumers (spec 014 guided construction pipeline) will need a canonical entry point. The dispute in DC-1 is about what the loader's contract should be — bulk vs. single-file, with or without completeness assertions — not about whether a loader should exist. A loader of some kind is unambiguously needed.

**Citing**: functional-architect M3, R1; schema-engineer M-9, R-7.

---

### SA-4: Both reviews agree the FR-011 import path mismatch is a real defect requiring resolution

Functional-architect does not call out FR-011 explicitly (it is not in the functional-architect's review, which focused on composability and type safety rather than spec-to-implementation drift). Schema-engineer O-1 and R-8 do call it out: the actual import path is `from conversus.schemas.objectives import ...`, not `from conversus_schemas.objectives import ...` as FR-011 requires. Functional-architect's R10 (export frozenset constants from `__init__.py`) implicitly assumes the `conversus.schemas` namespace is the correct one, which aligns with schema-engineer's diagnosis that amending FR-011 (not renaming the package) is the lower-risk resolution.

Both reviews, in aggregate, support option (b) from schema-engineer R-8: amend FR-011 to match the actual `conversus.schemas` namespace. No reviewer is arguing for renaming the package directory.

**Citing**: schema-engineer O-1, R-8; functional-architect R10 (implicit namespace assumption).
