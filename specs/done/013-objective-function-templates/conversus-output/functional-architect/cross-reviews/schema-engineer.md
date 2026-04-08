# Functional Architect Cross-Review of Schema Engineer's Review
# Spec 013: Objective Function Templates

**Cross-reviewer**: functional-architect
**Reviewing**: schema-engineer's review
**Date**: 2026-03-23

---

## Dangerous Contradictions

### DC-1: R4 (add VALID_CONSTRAINTS frozenset) conflicts with the composability architecture

Schema-engineer's R-2 proposes a `VALID_CONSTRAINTS` frozenset hardcoded in `objectives.py` to validate constraint references:

> "Add a `VALID_CONSTRAINTS` frozenset and validate constraint references" — schema-engineer R-2

This directly contradicts the architectural pattern established in this reviewer's M1 and R2. A static frozenset of constraint names is a maintenance trap: every new constraint YAML file requires a manual code change to `VALID_CONSTRAINTS`, and the set will inevitably drift from the actual contents of `schema/objective-functions/constraints/`. The correct resolution mechanism is dynamic — a `validate_library_integrity()` function that resolves constraint references against a loaded `dict[str, ConstraintTemplate]` at runtime. Hardcoding valid constraint names into the schema module conflates the schema layer (structural validation) with the library layer (referential integrity), violating the separation of concerns that makes `VALID_MODES` and `VALID_GAME_FORMS` safe to hardcode (those closed sets are defined by the spec, not by filesystem contents).

The schema-engineer's recommendation would make the library resistant to extension without providing any benefit that a dynamic loader would not provide more safely.

### DC-2: R-3 (standardize example format) and R-4 (cross-validate example keys) are sequentially dependent, but the schema-engineer treats them as independent

Schema-engineer's R-3 recommends standardizing all YAML examples to flat parameter-values format, and R-4 recommends adding a model_validator that checks example keys against parameter names. However, R-4 is formulated as a validator that fires at parse time — against the current YAML files, most of which use the nested format that R-3 wants to eliminate. If R-4 is implemented before R-3's YAML standardization is applied, it will cause mass validation failures across the seven templates using nested example structures (`weighted-sum`, `minimax`, `lexicographic`, `budget-constrained`, `time-constrained`, `general-linear`, `general-quadratic`). Both reviews agree on the end state, but neither flags this sequencing risk explicitly.

This reviewer's R7 frames the same two changes as a single atomic operation: standardize first, add validator second, and document the convention in the spec. Schema-engineer's treatment as two independent recommendations risks a breaking intermediate state where the validator is live but the YAML files have not been updated, which is particularly dangerous in a library where parsing failures silently block template loading.

### DC-3: Schema-engineer's O-2 frames the `example` field's loose typing as an "off-base assumption," but this reviewer's M6 frames it as a missed validation opportunity — the distinction matters for remediation priority

Schema-engineer O-2 states:

> "FR-002 says the example should be a 'minimal valid parameterization.' The current `dict[str, Any]` type admits anything... The spec implies the example should be a mapping from parameter names to concrete values, which is a much tighter contract than what the model enforces." — schema-engineer O-2

This reviewer's M6 agrees on the diagnosis but frames it as a validation gap, not a spec misread:

> "ObjectiveTemplate.example is `dict[str, Any]` -- a completely untyped bag... the example is opaque." — this review M6

The remediation priority diverges meaningfully. Schema-engineer categorizes this under "Off-Base Assumptions," implying it is a spec interpretation problem (fix the model to match the spec's intent). This reviewer categorizes it under "Missed Opportunities" with a Medium priority recommendation (R7), implying it is an incremental improvement. If the schema-engineer's framing is correct that this is a spec mismatch, then the example validation gap is High priority because all 21 existing templates may fail against a corrected validator. If this reviewer's framing is correct, it is a forward-looking improvement. The distinction is material: spec mismatch requires a breaking change; missed opportunity does not. The schema-engineer's framing is more accurate given FR-002's explicit language.

### DC-4: Schema-engineer's M-7 and M-8 (string-typed parameters masking structured data, boolean as string) conflict with this reviewer's R3 on the scope of the type system extension

Schema-engineer M-7 and M-8 identify `string` as a semantic junk drawer for vectors, matrices, and booleans, and schema-engineer R-6 recommends adding only `boolean` to the type system. This reviewer's R3 recommends adding `vector`, `matrix`, `boolean`, and `enum`:

> "Extend VALID_PARAMETER_TYPES to include at least `vector`, `matrix`, `boolean`, and `enum`." — this review R3

The schema-engineer's narrower extension (boolean only) is presented as a Low priority change affecting two parameters. This reviewer's broader extension is presented as High priority. The conflict is substantive: if `vector` and `matrix` are not added, the guided construction pipeline (spec 014) must parse comma-separated strings and bracket-notation matrices with no schema guidance, which this reviewer characterizes as a violation of Constitution VIII (Templating Engines Over Inference). The schema-engineer does not address `vector` and `matrix` types at all, which means their review implicitly accepts that the pipeline will handle these by convention. That is an architectural assumption with downstream consequences that the schema-engineer's review does not surface.

---

## Tensions

### T-1: Schema-engineer's M-9 (add loader utility) and this reviewer's M3 and R1 agree on the what but diverge on the how

Both reviews independently identify the absence of a `load_objective_template()` function as a gap (schema-engineer M-9, this review M3/R1). However, the schema-engineer's recommendation mirrors the existing `load_mode_mapping()` signature — a function that loads a single template by path — while this reviewer's R1 proposes a higher-level `load_objective_templates()` returning `dict[str, ObjectiveTemplate]` that loads the entire library and validates completeness (FR-012 through FR-015). The schema-engineer's single-file loader is simpler and safer to implement incrementally. This reviewer's library-level loader is necessary for SC-003 testability. Both are needed. The tension is in priority framing: schema-engineer rates this Medium, this reviewer rates it High because library-level loading is a prerequisite for the spec's own success criteria.

### T-2: Schema-engineer's R-10 (extra="forbid" on all models) conflicts with this reviewer's incremental stance on model strictness

Schema-engineer R-10 recommends adding `model_config = ConfigDict(extra="forbid")` to ObjectiveTemplate, ConstraintTemplate, and ParameterDefinition. This reviewer does not address this recommendation. The practical consequence is immediate: several existing YAML templates include `computed_objective` keys inside their nested example structures. With `extra="forbid"`, loading these templates would fail at the ObjectiveTemplate level if `computed_objective` is a top-level key, or silently succeed if it is nested inside the `example` dict (because `example: dict[str, Any]` absorbs it). The schema-engineer's R-10 is under-specified about whether `extra="forbid"` applies to nested dict fields. If it does not (and it cannot, because `example` is typed as `dict[str, Any]`), then R-10 provides partial strictness that might give false confidence.

This tension is not a contradiction — both reviews would benefit from extra strictness — but the schema-engineer's R-10 needs to be scoped precisely to be safe.

### T-3: Schema-engineer M-6 (no description on ConstraintTemplate) and this reviewer M7 agree on the fix but disagree on the constitutional grounding

Both reviews recommend adding `description: str` to ConstraintTemplate (schema-engineer M-6, this review M7/R6). Schema-engineer grounds this in "self-documentation parity with ObjectiveTemplate." This reviewer grounds it in Constitution XVI (Mathematical Transparency), specifically that the guided construction pipeline needs plain-language constraint explanations for user-facing prompts. The disagreement is consequential: if the grounding is mere parity, this is a style improvement; if the grounding is pipeline functionality, this is a functional requirement. Spec 014 (guided construction) will need to present constraint descriptions to users in gap-filling prompts. The functional grounding is correct, which raises this from schema-engineer's implicit Low priority to this reviewer's explicit Medium priority (R6).

### T-4: Schema-engineer's O-1 (FR-011 import path mismatch) is a real finding that this reviewer's review does not address

Schema-engineer O-1 identifies that FR-011 specifies `from conversus_schemas.objectives import ...` but the actual package is `conversus.schemas`. This reviewer's review does not mention the FR-011 import path at all. The schema-engineer's recommendation R-8 (amend FR-011 to match actual path) is the low-risk resolution. This reviewer's omission is notable because the import path is an observable API contract (Constitution II: Stable Interfaces), and a spec-to-code mismatch at the import level is exactly the kind of drift that this reviewer's alignment section emphasizes. The schema-engineer's finding stands without contradiction — it is simply a gap in this reviewer's coverage.

### T-5: Schema-engineer's M-5 (RangeSpec model) and this reviewer's R8 agree on the solution but differ on semantic coherence scope

Both reviews recommend replacing `range: Optional[dict[str, Any]]` with a typed model (schema-engineer R-5, this review R8). This reviewer goes further in M-5 / R8 by noting that `budget.yml` applies a numeric `range: {min: 0}` to a `string`-typed `cost` parameter, which is semantically incoherent:

> "A range could contain `{min: 0, max: 5, banana: true}` and pass validation. Worse, `budget.yml` has `range: {min: 0}` on a string-type parameter (`cost`), which is semantically incoherent." — this review O2

The schema-engineer's M-5 identifies the structural problem (unstructured dict) but not the semantic incoherence across type boundaries. A RangeSpec model alone does not fix the cross-type problem; the model_validator on ParameterDefinition must also skip or reject range validation for non-numeric types. This reviewer's R8 captures this nuance; the schema-engineer's R-5 does not.

---

## Safe Agreements

### SA-1: Both reviews agree that empty mode_compatibility should fail validation — this reviewer names it explicitly (M5/R5), schema-engineer's M-6 description agrees implicitly

This reviewer's M5 and R5 are explicit: a template with `mode_compatibility: []` is unreachable dead infrastructure and should raise a ValueError. Schema-engineer M-6 does not mention empty mode_compatibility, but both reviews' overall framing of the mode validation as a closed-set membership check implies that an empty list — which trivially passes `set([]) - VALID_MODES == set()` — is a gap. Both reviews would endorse R5's fix. This is a straightforward addition to the existing model_validator that carries no design controversy.

### SA-2: Both reviews independently identify the same three high-priority gaps without coordination

The three gaps both reviews flag as highest priority align precisely:
1. No duplicate parameter name validation (schema-engineer M-1/R-1, this review M4/R4)
2. No loader function for the template library (schema-engineer M-9/R-7, this review M3/R1)
3. Inconsistent example field structures across YAML templates (schema-engineer M-3/R-3, this review M9/R7)

The independent convergence on these three findings from different analytical frames (structural correctness vs. composability and functional architecture) is strong evidence that these are genuine gaps, not reviewer bias. Any remediation plan should address all three before addressing type system extensions or import path corrections.

### SA-3: Both reviews agree that the core model structure is sound and the functional decomposition is correct

Schema-engineer A-1 through A-6 and this reviewer's A1 through A6 agree that the four-type parameter system, frozenset constants, model_validator pattern, and constraint/objective separation are all well-implemented. Neither review recommends restructuring the model hierarchy. Both treat the existing implementation as a correct foundation that needs targeted additions, not a redesign. This is an important point of convergence: the implementation should be evolved, not replaced.

### SA-4: Both reviews agree on adding `description` to ConstraintTemplate

Schema-engineer M-6 and this reviewer M7/R6 both call for adding `description: str` to ConstraintTemplate. The YAML constraint files already include descriptive header comments; the fix is straightforward. The only divergence is in priority framing (this reviewer assigns it higher priority for functional pipeline reasons), but the remediation itself is unambiguous and uncontroversial. This is safe to implement immediately.
