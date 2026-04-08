# Functional Architect Revision: 013 Objective Function Templates

**Reviewer**: functional-architect
**Iteration**: 1
**Date**: 2026-03-23

---

## Recommendation Dispositions

### R1. Add a `load_objective_templates()` function — SCOPED DOWN

Original priority: High. Revised position: accept the loader as needed, but withdraw the embedded completeness assertions from the loader's contract.

Three cross-reviewers raised the same concern from three different angles. Game-theorist (T-1) and schema-engineer (DC-1) both flag that hardcoding cardinality thresholds ("at least 20 templates, every mode has 3+ templates") inside the loader couples the discovery function to library-state invariants, creating a maintenance burden whenever the library grows. Spec-compliance (DC-1) raises the stronger objection: FR-016 limits spec 013's deliverable to templates and Pydantic validation models; a runtime loader with embedded completeness checks is a system component that spec 013 does not authorize.

The objection is well-founded. Completeness thresholds belong in `validate_library_integrity()` (R2) and in tests, not inside a loader. The loader should be a pure discovery and validation function: find YAML files, load them through `model_validate()`, return the dict. Completeness checks are a separate concern. The architectural value of a loader function is not disputed by any reviewer — schema-engineer and spec-compliance both converge on the same gap (their SA-3 and SA-4 respectively). Revised scope: `load_objective_templates(path: Path | None = None) -> dict[str, ObjectiveTemplate]` — discovery and per-file validation only, no cardinality assertions.

### R2. Add a `validate_library_integrity()` function — MAINTAINED

No reviewer objects to the existence of this function, and the cross-reviews strengthen the case for it. Game-theorist (DC-3, T-4) demonstrates that the mode-mapping.yml red-blue contradiction and the boundary-negotiation sign error both escape the schema layer entirely — cross-artifact integrity checks are the only mechanism that can catch them programmatically. Schema-engineer (DC-2) raises the VALID_CONSTRAINTS frozenset as an alternative to dynamic resolution; that alternative is rejected for the reasons stated in my cross-review of schema-engineer (DC-1 there): a static frozenset drifts from filesystem contents and conflates the schema layer with the library layer. Dynamic resolution via `validate_library_integrity()` is the correct approach.

One concrete expansion to the function's scope: game-theorist (DC-1) correctly notes that `validate_library_integrity()` as specified would pass a library with sign-inconsistent forms, because it checks references and counts but not mathematical consistency. Adding a check that all templates with a declared `optimization_direction` field use the corresponding sign convention in their form string is now in scope for this function — contingent on the `optimization_direction` field being added (see New Recommendation NR-1 below).

### R3. Extend the parameter type system — SCOPED DOWN, PRIORITY REVISED TO MEDIUM

Original priority: High. Revised: Medium, with `boolean` as the minimum necessary addition and `vector`/`matrix`/`enum` as tracked extensions.

Spec-compliance (DC-2) is correct that FR-003 explicitly enumerates four types (`float`, `integer`, `string`, `function`). Adding `vector`, `matrix`, `boolean`, and `enum` without a spec amendment overrides an explicit spec clause — this is scope beyond what an implementer can authorize unilaterally. Schema-engineer (DC-4) identifies the same conflict and recommends `boolean`-only as a backward-compatible, low-risk improvement. Game-theorist (DC-2) demonstrates the concrete downstream impact: the proposed Nash bargaining template's epsilon parameter, typed as `string`, would fail validation under the extended system without first being redesigned.

The minimum necessary change — adding `"boolean"` to `VALID_PARAMETER_TYPES` and converting the two `normalize` parameters — is safe to implement now and is consensus across all three cross-reviewers. The broader extension (`vector`, `matrix`, `enum`) should be proposed as a spec amendment to FR-003 for the spec owner's decision before implementation. R3 is maintained at reduced scope; the `"boolean"` addition is uncontroversial and should proceed.

### R4. Add duplicate parameter name validation — MAINTAINED, PRIORITY HIGH

This recommendation has full cross-reviewer consensus. Schema-engineer (SA-2) provides nearly identical implementation code independently. Spec-compliance (SA-2) flags this as missed. Game-theorist (SA-3) endorses it without objection. The validator is a two-line addition to existing model_validators, the failure mode (silent shadowing) is real, and no reviewer disputes the fix. Priority is elevated from Medium to High given the unanimous convergence.

### R5. Add empty mode_compatibility validation — MAINTAINED

No cross-reviewer objects. Schema-engineer (T-2) and spec-compliance (T-5) both note that the omission is a genuine gap — a template with no compatible modes is dead infrastructure that the model should prevent. Spec-compliance raises the useful point that this could be framed as a FR-008 amendment ("a template must apply to at least one mode") rather than purely a Constitution XII application; that framing is compatible with the fix. The validator implementation is unchanged from the original recommendation.

### R6. Add `description` field to ConstraintTemplate — MAINTAINED, FIELD MADE OPTIONAL

Original recommendation: `description: str` (required). Revised: `description: Optional[str] = None` for now, with a separate task to populate all six constraint YAML files and promote the field to required in a follow-on commit.

Schema-engineer (T-3) and spec-compliance (T-3) both flag the migration cost: making `description` required immediately breaks all six existing constraint YAML files, none of which carry a top-level description field. Spec-compliance also notes that FR-007 does not require a description field, so required-from-day-one is stronger than the spec mandates. The guided construction pipeline argument (Constitution XVI) is still valid — spec 014 will need machine-readable constraint descriptions — but the implementation sequence should be: add optional field, populate YAML files, promote to required. Starting optional avoids a forced migration in a single commit.

### R7. Standardize example field structure and add validation — SEQUENCING CLARIFIED

The sequencing dependency is now explicit, following schema-engineer (T-1) and spec-compliance (T-3, SA-2): standardize YAML files first, add model_validator second. These are not bundled as a single atomic operation; they are two sequential steps with the YAML standardization as the gate. The additional point from spec-compliance (DC-4) is also accepted: a spec clarification on FR-002's "minimal valid parameterization" intent should precede adding a validator that enforces the flat format. The model_validator should not be the spec's interpretation — the spec owner should state the intent, and the validator implements it.

### R8. Type the `range` field as a Pydantic model — MAINTAINED

Schema-engineer (T-5) agrees on the structure and adds the useful refinement that `extra="forbid"` on the RangeSpec model would prevent extraneous keys like `banana: true`. The cross-type coherence check — rejecting numeric ranges on non-numeric types — is an addition that schema-engineer's R-5 does not include but does not dispute. This cross-type check should be part of R8's implementation. Priority remains Low.

### R9. Add `_objective_schema_dir()` helper — MAINTAINED

Schema-engineer (T-4) confirms the naming distinction matters: their code snippet references an unqualified `_schema_dir()` that would conflict with game_forms.py at import time. The `_objective_schema_dir()` naming convention in R9 is the correct choice. No controversy.

### R10. Export frozenset constants from `__init__.py` — MAINTAINED

No cross-reviewer objects. This is the established pattern from game_forms.py and is straightforwardly correct.

### O1. Constraint references as bare strings — POSITION REVISED

Original framing: bare string references are architecturally insufficient and contradict Constitution VIII. Revised framing: the reference-by-name pattern is the spec's deliberate design choice (FR-002 uses the word "references" intentionally; FR-006/FR-007 define constraint templates as separate files); resolution is explicitly scoped to spec 014.

Spec-compliance (DC-3) is correct here. The functional-architect review over-reached by calling the spec's own design decision "architecturally broken." Constitution VIII (Templating Engines Over Inference) applies to the guided construction pipeline's behavior, not to how objective templates reference constraint templates within the same schema library. The resolution mechanism (`validate_library_integrity()` checking that referenced names exist in the loaded constraint dict) is still the right approach — but it is an integrity check at library-load time, not a structural refactoring of the template schema. The `ComposedObjective` model proposal is withdrawn; it is unnecessary given that `validate_library_integrity()` serves the same referential-integrity purpose without requiring a new model type.

### Concession: FR-011 import path mismatch

The functional-architect review did not mention the FR-011 import path deviation. Schema-engineer identified it; spec-compliance (T-1) rates it CRITICAL. My cross-review of spec-compliance (DC-1) argued the severity was overclassified and that `conversus.schemas` is strictly superior for a v1 library. That argument was overstated. The correct position is: the deviation from FR-011 is real, the spec-amendment path (amend FR-011 to match `conversus.schemas`) is the low-risk resolution, and this should be documented as a compliance item even if CRITICAL is an overstatement for an unreleased library. The omission from the original review was a gap in coverage.

### Concession: Sign convention bugs are invisible to the structural schema layer

Game-theorist's cross-review (DC-1, T-4) is correct that the boundary-negotiation sign reversal and the budget-constrained/time-constrained maximization-vs-minimization inconsistency are mathematical correctness bugs that my entire proposed validation infrastructure would not detect. The `load_objective_templates()` loader, `validate_library_integrity()` cross-reference checker, duplicate-name validator, and empty-mode validator are all structural; they are blind to sign conventions in free-text form strings. The boundary-negotiation bug is real, requires an immediate YAML patch, and demonstrates that structural validation is necessary but not sufficient. This is now acknowledged explicitly rather than left as the implicit "documented limitation" treatment in O3.

---

## New Recommendations

### NR-1. Add `optimization_direction: Literal["minimize", "maximize"]` to ObjectiveTemplate (Priority: Medium)

Game-theorist's R6 and my cross-review of game-theorist (DC-1) converge on a joint requirement: sign convention enforcement requires both a declared direction field and a cross-field consistency check. Neither alone is sufficient. Adding `optimization_direction` without a form-consistency check formalizes two sources of truth that can diverge. Adding a form-string token validator (game-theorist R9) without a declared direction field gives the validator nothing to check against.

The joint implementation: add `optimization_direction: Literal["minimize", "maximize"]` to `ObjectiveTemplate`, set all existing templates to `"minimize"` (correcting budget-constrained and time-constrained from their current implied maximization convention simultaneously), and extend `validate_library_integrity()` with a heuristic check: for templates declared `minimize`, the form string should not use the maximization pattern (positive benefit terms without a leading minus). This heuristic is imperfect — game-theorist's cross-review (DC-4) correctly notes that form strings using Greek letters and subscripts resist token matching — but it catches the class of errors present in the existing library. The form-string validator is a best-effort guard, not a proof.

**Constitution alignment**: XVI (mathematical transparency — optimization direction is part of the template's mathematical specification), V (observable behavior — the direction is machine-readable, not inferred from sign convention).

### NR-2. Apply immediate YAML patches for known correctness bugs before any schema changes (Priority: Critical)

Game-theorist identified three YAML-level bugs that do not require schema changes and should not wait for schema work to land:

1. `boundary-negotiation.yml`: `J = -boundary_violations + sigma * clarity` should be `J = boundary_violations - sigma * clarity` (sign reversal under minimization convention).
2. `risk-adversarial.yml`: `J_red = -confirmed_risks; J_blue = -mitigated` should be `J_red = -confirmed_risks + false_positive_penalty * failed_claims` (form incompleteness — parameter declared but absent from form).
3. `mode-mapping.yml`: `red-blue: form: gnep` should be `red-blue: form: stackelberg` (contradicts all three red-blue templates and Stackelberg's mathematical suitability for leader-follower structures).

These are correctness bugs, not schema gaps. They can be applied as a YAML patch commit today, independent of any Pydantic model work. Deferring them until schema improvements land leaves a demonstrably incorrect library in production state. All four cross-reviews (game-theorist O1/M9/O3, functional-architect cross-review of game-theorist SA-1/SA-2, schema-engineer SA-2, spec-compliance SA-2) agree on the facts; no reviewer disputes these three fixes.

**Constitution alignment**: XIV (spec-implementation parity — the templates are the spec's primary deliverable and must be mathematically correct).

### NR-3. Establish a spec policy on template additions beyond the Section 2 catalog (Priority: Low)

Spec-compliance (T-1) and my cross-review of spec-compliance (T-1) both identify a genuine policy gap: `cooperative-fairness` was added to the library without a spec amendment, and there is no established policy on whether new templates require explicit spec updates or can be added as long as they satisfy structural requirements. My original review treated the cooperative templates as a group without flagging this. Spec-compliance correctly identified it.

The recommendation is not to remove `cooperative-fairness` — it is structurally correct and mathematically motivated — but to document the spec owner's intent: either (a) the Section 2 template catalog is exhaustive and additions require spec amendments, or (b) the catalog is illustrative and templates satisfying FR-002 through FR-011 can be added without spec changes. Whichever policy is chosen, `cooperative-fairness` should be added to Section 2 and the policy documented in the spec's scope section. This is a spec maintenance item, not a code change.

**Constitution alignment**: XI (single source of truth — the spec should be the authoritative catalog, not an approximation of it), XIV (spec-implementation parity).

---

## Position Summary

The original review's core findings hold: the type system is doing too little work, the library has no loader or integrity validation infrastructure, and several model_validator gaps leave structurally invalid templates undetected. The cross-review process has sharpened three aspects of the position significantly.

First, scope corrections: the `load_objective_templates()` loader should not embed cardinality assertions (those belong in `validate_library_integrity()`); the constraint resolution design is the spec's deliberate choice (not an architectural failure); and the type system extension should follow a spec amendment process for the `vector`/`matrix`/`enum` additions while `boolean` proceeds immediately.

Second, additions from cross-review: the `optimization_direction` field (NR-1) is now a joint recommendation that incorporates game-theorist's R6 in a way that avoids the two-sources-of-truth problem. The YAML correctness patches (NR-2) are the highest-priority practical action regardless of all schema debates. The spec policy on template additions (NR-3) addresses the `cooperative-fairness` omission that spec-compliance correctly surfaced.

Third, concessions: the FR-011 import path omission was a real coverage gap in the original review. The boundary-negotiation sign bug demonstrates that structural validation is necessary but not sufficient, and O3's treatment of form-string limitations as a "documented limitation" understated the severity — mathematical correctness bugs visible only to game-theoretic analysis require human review of form strings, not just structural validators.

The priority ordering for implementation:

1. YAML patches (NR-2) — no schema work required, correctness bugs, apply now
2. Duplicate parameter name validation (R4) — universal consensus, two-line addition
3. Empty mode_compatibility validation (R5) — no controversy, straightforward
4. `_objective_schema_dir()` helper (R9) — prerequisite for R1
5. `load_objective_templates()` loader, scoped (R1 revised) — prerequisite for test coverage
6. `description: Optional[str]` on ConstraintTemplate (R6 revised) — unblock spec 014 pipeline
7. `optimization_direction` field + integrity check extension (NR-1)
8. `validate_library_integrity()` (R2 extended)
9. `boolean` addition to VALID_PARAMETER_TYPES (R3 scoped)
10. RangeSpec typed model (R8)
11. FR-011 spec amendment
12. Spec policy on template additions (NR-3)
13. `vector`/`matrix`/`enum` type extension, pending spec amendment (R3 remainder)
14. Example field standardization (R7 step 1) then model_validator (R7 step 2), pending spec clarification on FR-002
