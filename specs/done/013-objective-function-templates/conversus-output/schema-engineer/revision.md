# Schema Engineer Revision: 013 Objective Function Templates

**Reviewer**: schema-engineer
**Revision iteration**: 1
**Date**: 2026-03-23

---

## Recommendation Dispositions

### R-1: Add duplicate parameter name detection — MAINTAIN

All three cross-reviews explicitly agree this is correct and uncontroversial (game-theorist SA-1, functional-architect SA-2, spec-compliance SA-4). No reviewer disputes the implementation. The validator code stands as written in the original review. This is the strongest consensus finding across all four reviews.

### R-2: Add VALID_CONSTRAINTS frozenset — REVISE

The frozenset approach is opposed on compelling grounds by two cross-reviewers. Game-theorist DC-2 correctly observes that a static closed set would block every new constraint (including game-theorist's own `incentive-compatibility` proposal) before the YAML file even exists. Functional-architect DC-2 makes the same point architecturally: a hardcoded frozenset becomes a parallel data structure that drifts from the `constraints/` directory, violating the data-driven principle already established for `VALID_MODES`. Both cross-reviews propose runtime resolution against actual file contents instead.

The revised position: **drop the static frozenset**. The correct mechanism is a `validate_library_integrity()` function (as functional-architect R2 proposes) that cross-references `ObjectiveTemplate.constraints` against a loaded `dict[str, ConstraintTemplate]` at library-load time. This provides referential completeness without hardcoding the constraint namespace. The frozenset is architecturally wrong for a field whose valid values are determined by filesystem contents, not by a spec-defined closed set (unlike `VALID_MODES` and `VALID_GAME_FORMS`, which are normatively enumerated in the spec itself and will not grow without a spec revision).

### R-3: Standardize example format — MAINTAIN WITH CLARIFICATION

All cross-reviews agree that the flat parameter-name-to-value format is correct and that the nested structure in seven templates is wrong. The sole point of contention (spec-compliance DC-1, game-theorist T-1) is the disposition of `computed_objective`. The original review proposed migrating it to an `example_note` field; that proposal is upheld as the correct resolution to the DC-1 contradiction: `computed_objective` is documentation, not parameterization, and belongs in a distinct field rather than being removed entirely or tolerated as an undeclared annotation key. This resolves spec-compliance's concern about premature R-4 application while preserving the documentation value.

### R-4: Cross-validate example keys against parameter names — MAINTAIN WITH SEQUENCING GATE

The validator is correct in principle. The cross-reviews surface a critical sequencing constraint: R-4 must not be deployed until (a) R-3 YAML standardization is complete across all 21 templates, and (b) the `computed_objective`/`example_note` migration is complete. Game-theorist DC-1 also correctly notes that R-4 must follow resolution of mathematical bugs in `boundary-negotiation` and `budget-constrained` templates, because tightening the validator around incorrect content makes later correction harder. The sequencing dependency is: YAML corrections → YAML standardization → example_note migration → then R-4 validator. This ordering is now explicit.

Additionally, as game-theorist DC-4 observes, the validator must exclude function-type parameters from the example key check — function-type parameters represent derivation anchors, not concrete values, and cannot be meaningfully represented as example keys. The validator should check only scalar-typed parameters (float, integer, string, boolean) against the example dict.

### R-5: Create RangeSpec model — MAINTAIN WITH TYPE-AWARE EXTENSION

The structural fix is correct and uncontested. Functional-architect T-5 adds a necessary refinement: the `ParameterDefinition` model_validator must skip or reject range application for non-numeric types (string, function). The `budget.yml` cost parameter with `type: string` and `range: {min: 0}` is semantically incoherent, and the RangeSpec model alone does not catch it. The fix is to add: when `range` is present and `type` is `string` or `function`, raise a ValueError explaining that range constraints apply only to numeric parameters. This closes the incoherence gap functional-architect R8 identifies.

### R-6: Add boolean to parameter type system — ELEVATE PRIORITY TO MEDIUM

Game-theorist DC-3 makes a correctness argument, not merely an aesthetics argument, for this change: `bool("false") is True` in Python, meaning string-encoded booleans create a silent misinterpretation hazard for downstream consumers. The original "Low" priority was wrong. The change remains bounded to two parameters and is backward-compatible, but the correctness risk warrants Medium priority. The change is also explicitly linked to sign-convention normalization (game-theorist R1) as the two fixes together close a compounding error surface.

Type system extension scope: functional-architect R3 proposes adding `vector`, `matrix`, and `enum` as well. The original review's position (M-7) framed vectors and matrices as a design limitation rather than a bug. That position is maintained for v1: `vector` and `matrix` are spectrally correct observations but are out of scope for this spec, which does not enumerate these types and whose FR-003 leaves the four-type system as the normative vocabulary. A future spec should address them. The `boolean` addition is the only type extension adopted here.

### R-7: Add load_objective_template() and load_constraint_template() utilities — MAINTAIN WITH ARCHITECTURE CLARIFICATION

All reviews agree that a loader utility is needed. The scope dispute between functional-architect DC-1 (library-level loader with completeness assertions) and the original review's single-file loader is resolved as follows: the two are not mutually exclusive. The single-file `load_objective_template(path) -> ObjectiveTemplate` is the atomic unit (matching `load_mode_mapping()` precedent). A separate `validate_library_integrity(objectives, constraints)` pure function handles cross-reference and completeness checks — this keeps `objectives.py` as a schema module with an optional I/O helper, while library-level invariants live in a callable that can be invoked independently. Cardinality assertions (SC-003) belong in the integrity function, not baked into the bulk loader.

The function name `_schema_dir()` in the original code snippet would shadow game_forms.py's helper. Functional-architect's suggestion of `_objective_schema_dir()` is adopted.

### R-8: Resolve FR-011 import path discrepancy — MAINTAIN

All four reviews are in unanimous agreement: amend FR-011 to match the actual `conversus.schemas.objectives` namespace. No reviewer advocates renaming the package directory. The spec-compliance cross-review's compatibility alias option is noted but not adopted — a compatibility alias adds maintenance surface for a package that has not yet had a public release. The spec amendment is sufficient.

### R-9: Add empty-parameters guard — MAINTAIN

No review contradicts this. Functional-architect SA-1 implicitly endorses it via the parallel finding on empty `mode_compatibility` (functional-architect R5). Both guards address the same pattern: degenerate templates that pass validation but produce vacuous or unreachable mathematical objects. Adding empty `mode_compatibility: []` validation (functional-architect R5) is also adopted as part of this recommendation — it was a blind spot in the original review that functional-architect correctly surfaces.

### R-10: Add model_config extra="forbid" to all models — REVISE TO DEFERRED

Two cross-reviews (functional-architect T-2, spec-compliance T-4) correctly identify that this recommendation has sequencing dependencies that make immediate application dangerous. The `extra="forbid"` guard does not protect against the primary inconsistency it is implicitly supposed to catch (nested example content, which lives inside `dict[str, Any]` and is invisible to model-level extra-field checking). Applying it before R-3 YAML standardization and the `example_note` migration is complete would either silently fail to catch the real drift or cause false-positive validation failures on currently-valid top-level YAML keys.

Revised position: `extra="forbid"` is deferred until after R-3 standardization and R-4 example-key validation are fully deployed. At that point, `extra="forbid"` adds a genuine correctness layer for future template authoring errors. The implementation sequencing is: R-3 → R-4 → R-10.

---

## New Recommendations

### NR-1: Add empty mode_compatibility guard to both ObjectiveTemplate and ConstraintTemplate

Functional-architect R5 correctly identifies a gap the original review missed: a template with `mode_compatibility: []` trivially passes the current VALID_MODES membership check (the empty set minus VALID_MODES is still empty) but produces a template that is unreachable by any mode — dead infrastructure by construction. The validator should add:

```python
if not self.mode_compatibility:
    raise ValueError("mode_compatibility must contain at least one valid mode.")
```

This parallels the already-recommended empty-parameters guard (R-9) and applies to both `ObjectiveTemplate` and `ConstraintTemplate`. The fix is unambiguous, backward-compatible with all existing templates (none have empty mode_compatibility), and closes a degenerate case the original review's model inspection missed.

**Priority**: High. The existing closed-set membership check gives false confidence that mode assignment is fully validated when the empty-list case bypasses it entirely.

### NR-2: Add description field to ConstraintTemplate as required, with atomic YAML migration

The original review's M-6 and O-3 recommended adding `description` to `ConstraintTemplate` as optional. Three cross-reviews (game-theorist T-3, functional-architect T-3 and SA-4, spec-compliance SA-3) push back on the optional framing. The functional-architect grounding is correct: spec 014's guided construction pipeline will consume constraint templates in prompts alongside objective templates. An optional field that will be absent on all six current constraint YAMLs is not meaningfully different from no field at all for that downstream consumer.

The revised recommendation: add `description: str` as **required** to `ConstraintTemplate`, with the six constraint YAML files updated atomically in the same commit. The header comments in all six files already contain the description text; the migration cost is bounded and certain. Making it required now avoids the asymmetry that would force spec 014 to special-case constraints.

**Priority**: Medium. Blocked only by the commit coordination to update the YAML files simultaneously.

### NR-3: Resolve computed_objective disposition before R-3 and R-4 are implemented

The cross-reviews surface a previously unacknowledged gap: the original review proposed removing `computed_objective` from example blocks (R-3) and implied it should move to `example_note`, but did not define `example_note` as a model field or specify its type. Spec-compliance DC-1 and game-theorist T-1 both flag this omission. The gap must be closed before R-3 standardization work begins, because the standardization target depends on knowing whether `computed_objective` becomes a typed field, is silently dropped, or is renamed.

The recommendation: add `example_note: Optional[str] = None` to `ObjectiveTemplate`. This field carries the informal optimization-direction annotation currently embedded in example blocks (e.g., "minimize J ≈ quality - 0.5 * cost"). The field is optional and string-typed — not a Pydantic-validated mathematical expression. This satisfies spec-compliance's desire to preserve the documentation value, resolves the DC-1 contradiction between both reviews, and provides a clear migration target for all seven nested-example templates.

The `example` field then contains only parameter-name-to-value mappings, making R-4's cross-validator well-defined. Function-type parameters are excluded from the R-4 key check (per the revised R-4 disposition above), so Nash-bargaining-style templates with function-type parameters can still produce meaningful examples without breaking the validator.

**Priority**: High. This is a prerequisite decision that gates both R-3 and R-4. It should be resolved first in any implementation plan.

---

## Position Summary

The original review's structural analysis was sound. The Pydantic models correctly implement the core FR requirements, and the ten recommendations addressed real gaps. The revision process sharpens three positions:

**Concessions**: The VALID_CONSTRAINTS frozenset (R-2) is withdrawn in favor of runtime library integrity checking. This was the clearest architectural error in the original review — hardcoding a registry of filesystem-derived names is categorically different from hardcoding a registry of spec-defined modes. The game-theorist and functional-architect both made this point persuasively. The `extra="forbid"` recommendation (R-10) is deferred pending YAML standardization, not abandoned — the sequencing concern from both cross-reviews is valid. The `description` field on `ConstraintTemplate` is upgraded from optional to required.

**Maintained positions**: The schema layer's treatment of `form` as a semantically opaque string is correct and cannot be abandoned without introducing brittle heuristic validators. The game-theorist's form-completeness validator (R9) is correctly characterized as unimplementable without fragile substring matching. The form field's correctness is a review and YAML-authoring concern, not a schema concern. The `boolean` type addition is maintained and elevated to Medium priority on correctness grounds.

**New ground**: Three new recommendations address gaps the original review missed: the empty `mode_compatibility` guard (NR-1, borrowed from functional-architect), the `description`-as-required field with atomic YAML migration (NR-2, synthesizing three cross-reviews), and the explicit `example_note` field definition as a prerequisite for R-3 and R-4 (NR-3, resolving the DC-1 contradiction across game-theorist and spec-compliance cross-reviews).

The implementation sequencing that emerges from the revision process is: NR-3 (example_note field decision) → R-3 (YAML standardization) → R-4 (example key validator, excluding function-type params) → R-10 (extra="forbid"). All other recommendations (R-1, NR-1, NR-2, R-5 with type-aware extension, R-6, R-7 with architectural clarification, R-8, R-9) are independent and can proceed in parallel with the example standardization track.
