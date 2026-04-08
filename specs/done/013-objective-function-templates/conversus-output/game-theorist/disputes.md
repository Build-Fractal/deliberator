# Game-Theorist Disputes — 013 Objective Function Templates

**Role**: game-theorist
**Phase**: 4 — Disputes
**Date**: 2026-03-23

---

## Remaining Disputes

### D1. computed_objective Removal vs. example_note Field

**Dispute is with**: spec-compliance (R3 disposition), schema-engineer (NR-3)

spec-compliance's revised R3 calls for removing `computed_objective` from example blocks entirely and placing any documentation of what the objective evaluates to in the template's `description` field or the spec's Section 2 narrative. schema-engineer's NR-3 resolves the same question by adding an explicit `example_note: Optional[str] = None` field to `ObjectiveTemplate`, giving the documentation a typed home in the model rather than orphaning it to prose.

Game-theorist holds that spec-compliance's removal-only resolution is incomplete. The `computed_objective` annotation in cross-mode template examples performs two functions simultaneously: it annotates the numeric result of the example parameterization (documentation), and it implicitly encodes the optimization direction of the form (mathematical metadata). Removing it without replacement eliminates that second function. schema-engineer's `example_note` preserves the string, but as a free-text field it does not give the guided construction pipeline (spec 014) any machine-readable handle on optimization direction either.

The game-theorist's `optimization_direction` field (R6, now also functional-architect NR-1) is the correct replacement for the mathematical-metadata function of `computed_objective`. The `example_note` field can carry the human-readable annotation. The two together are strictly superior to either removal alone or `example_note` alone. The remaining dispute is whether the implementation plan makes this coupling explicit: `computed_objective` should not be removed until `optimization_direction` exists on the model to absorb its semantic content. spec-compliance's R3 implementation plan does not include this gate.

**Game-theorist's position**: Remove `computed_objective` from example blocks only after `optimization_direction` is added to `ObjectiveTemplate`. The `example_note` field (schema-engineer NR-3) is useful documentation but does not substitute for machine-readable optimization direction. The sequencing gate is non-negotiable.

---

### D2. optimization_direction Field: Optional Default vs. Explicit Requirement

**Dispute is with**: functional-architect (NR-1), schema-engineer (NR-3 adjacent)

There is now broad consensus that `optimization_direction: Literal["minimize", "maximize"]` should be added to `ObjectiveTemplate`. The remaining dispute is whether the field should be optional with a default of `"minimize"` (game-theorist R6 revised position) or required with no default (functional-architect NR-1 revised position).

Functional-architect's NR-1 sets all existing templates to `"minimize"` in the same commit, making required feasible. However, this requires coordinating YAML edits across all 21 objective templates atomically — the same coordination burden that functional-architect's R6 revision of ConstraintTemplate `description` was revised downward to avoid (start optional, promote to required later). It is inconsistent to apply different atomicity standards to the two fields.

The game-theorist's optional-with-default approach is the architecturally correct choice for the same reason schema-engineer deferred `extra="forbid"`: applying a required field before all existing templates are updated creates a transition window where valid templates fail validation. The default of `"minimize"` is not arbitrary — it is the stated universal convention after the sign normalization work in R1. An optional field with a sound default documents the convention, allows gradual adoption, and does not break any existing template. Making it required is a v1.1 migration after all templates are confirmed correct.

**Game-theorist's position**: `optimization_direction` should be `Optional[Literal["minimize", "maximize"]] = "minimize"`. The required promotion follows after R1's sign normalization is applied across all 21 templates and confirmed correct. Functional-architect's atomicity argument is strong for new templates but creates an unacceptable transition risk for the existing library.

---

### D3. form_complete Validator: Warning vs. Error, and Scope Boundary

**Dispute is with**: schema-engineer (R-3/R-4 interaction), spec-compliance (R3 disposition), functional-architect (DC-4 from cross-review)

The form_complete validator (game-theorist R9 revised position) is now scoped to scalar and integer parameters only, framed as a warning rather than a validation error. schema-engineer's position is that the `form` field is semantically opaque and any token-matching validator is too fragile to be in the schema layer — the cross-validate-example-keys approach (schema-engineer R-4) is the correct substitute. spec-compliance's revised R3 resolves `computed_objective` by removal, which clears the path for schema-engineer's R-4 but does not address the form-parameter linkage problem.

The remaining dispute is narrow: schema-engineer holds that form-completeness checking belongs entirely outside the Pydantic model (in review processes and YAML-authoring conventions). Game-theorist holds that a scoped, warning-level, substring-match check on scalar parameters is better than nothing. The `false_positive_penalty` case is the concrete demonstration: it is a scalar parameter, its name is a verbatim string that would appear as a token in any reasonable form expression, and its absence from `risk-adversarial`'s `form` field was not caught by any structural validator. Schema-engineer's R-4 (example-key cross-validation) would have caught it in the example block — but only if the example block included `false_positive_penalty`. If the example block also omits it, R-4 passes and the incompleteness is invisible.

The game-theorist's validator is the only proposed mechanism that independently catches this class of defect regardless of whether the example block is also incomplete. Framing it as a warning (not a hard validation error) directly addresses schema-engineer's concern about false positives. Schema-engineer has not argued that a warning-level heuristic is affirmatively harmful — the objection is to a hard validator. A warning that fires for scalar parameters whose names are absent from the form string, implemented as a `@model_validator(mode="after")` that appends to a `warnings: list[str]` field rather than raising, satisfies both positions.

**Game-theorist's position**: The form_complete warning-level check on scalar/integer parameters should be implemented in the Pydantic model, appended to an optional `warnings` field rather than raising. It is not a substitute for schema-engineer's R-4; it is the only check that catches simultaneous form-and-example omissions. Schema-engineer's objection to a hard validator is accepted; the objection to a warning is not sustained by the cross-review evidence.

---

## Convergence

### C1. Mathematical Correctness Bugs Are Pre-Schema-Work Prerequisites

All four reviewers reach the same implementation-ordering conclusion by different paths. Functional-architect's NR-2 is the clearest statement: the three YAML-level bugs (mode-mapping.yml red-blue/Stackelberg contradiction, risk-adversarial form incompleteness, boundary-negotiation sign reversal) should be patched before any schema changes land. Game-theorist held this throughout (R2, R3, R1 respectively). Spec-compliance added NR-1 and NR-2 to its revised recommendations agreeing on both. Schema-engineer's R-4 sequencing note explicitly gates example-key validation behind mathematical correction.

The convergence is complete: correctness patches first, schema tightening second. No reviewer advocates implementing schema improvements against a library with known mathematical errors.

**Agreed action**: Apply the three YAML patches as a standalone commit, independent of all Pydantic model work. This is now the highest-priority action across all four reviewers without dispute.

---

### C2. Spec Amendment Protocol Is Required Before Form-Field Corrections

Game-theorist's NR1 (spec amendment protocol) is implicitly ratified by all three other reviewers. Spec-compliance's NR-2 makes the same protocol concrete for `risk-adversarial`. Functional-architect's NR-3 extends it to the `cooperative-fairness` catalog inclusion. Schema-engineer's revised R-8 (amend FR-011 to match `conversus.schemas`) follows the same logic.

The convergence is on the principle: any correction to a template's `form` field that changes the mathematical expression requires a spec Section 2 amendment before the YAML is updated. All four reviewers, starting from their own domain concerns, arrive at this protocol as the correct artifact-change ordering. The cross-review process collectively closed the gap that existed in Round 1 — where game-theorist proposed YAML fixes that spec-compliance would have flagged as FR-002 deviations if applied directly.

**Agreed action**: Establish the spec amendment protocol as explicit procedure. The sequence for form-expression corrections is: (1) spec Section 2 amendment, (2) YAML update to match. No reviewer disputes this ordering.

---

### C3. VALID_CONSTRAINTS Frozenset Is Withdrawn; File-Existence Check Is Consensus

Schema-engineer's revised R-2 withdraws the frozenset entirely in favor of runtime library integrity checking. Game-theorist's NR3 independently proposes file-existence checking as the correct mechanism. Functional-architect's R2 (`validate_library_integrity()`) was always framed as dynamic resolution. Spec-compliance's NR-3 (empty mode_compatibility) confirms the empty-list rejection pattern, which is structurally compatible with dynamic resolution.

All four reviewers now agree: static frozensets are appropriate for spec-defined closed sets (VALID_MODES, VALID_GAME_FORMS) because those sets will not grow without a spec amendment. Constraint names are filesystem-derived, not spec-enumerated, and must be validated dynamically at library-load time. The convergence is complete.

**Agreed action**: Implement constraint name validation in `validate_library_integrity()` via file-existence check against the `constraints/` directory. No frozenset. This is implemented in functional-architect's R2 scope, not in the Pydantic model layer.

---

### C4. Nash Bargaining Solution and Epsilon-Constraint Templates Are Deferred to v1.1

All four reviewers converge on the deferral of game-theorist's R4 and R5 to v1.1, contingent on type system extension. Game-theorist's revised position accepts the deferral explicitly. Functional-architect's R3 (scoped to `boolean` now, `vector`/`matrix`/`enum` pending spec amendment) establishes the type system track that would unblock Nash bargaining's `list[function]` requirement and epsilon-constraint's `vector` requirement. Schema-engineer's revised R-6 maintains the same scope boundary. Spec-compliance's R7 identifies the same gap and routes it through a FR-003 spec amendment.

No reviewer disputes the mathematical motivation for either template. The deferral is unanimous and process-based: the type system cannot represent the required parameter structures at v1.

**Agreed action**: Track R4 (Nash bargaining) and R5 (epsilon-constraint) as v1.1 additions, gated on FR-003 spec amendment and functional-architect R3 (type system extension). The v1 spec closure is not affected — FR-012/FR-013 thresholds are already met by existing templates.

---

### C5. Implementation Sequencing Across All Reviewers Is Substantially Aligned

Despite arriving from different starting positions (mathematical correctness, schema integrity, functional composition, spec compliance), all four revised positions converge on a common implementation ordering:

1. YAML correctness patches (game-theorist R1/R2/R3, functional-architect NR-2, spec-compliance NR-1/NR-2) — no model work required
2. Spec amendments for corrected forms (game-theorist NR1 protocol, spec-compliance NR-2)
3. Duplicate parameter name validation and empty mode_compatibility guard (schema-engineer R-1, NR-1; functional-architect R4, R5) — universal consensus, no sequencing dependencies
4. `example_note` field decision (schema-engineer NR-3) as prerequisite for example standardization
5. Example format standardization (schema-engineer R-3, functional-architect R7, spec-compliance R3)
6. Example-key cross-validator (schema-engineer R-4), gated on example standardization
7. `optimization_direction` field (game-theorist R6, functional-architect NR-1), coordinated with R1 sign normalization
8. `validate_library_integrity()` (functional-architect R2), incorporating game-theorist NR3 (file-existence constraint check)
9. `extra="forbid"` on models (schema-engineer R-10, deferred), gated on example standardization and optimization_direction field

Items 3 through 9 represent the schema work that follows the correctness patches. No reviewer disputes this broad ordering.

---

## Final Position Statement

### Non-Negotiables

**1. Mathematical correctness before schema correctness.**
The three YAML bugs (mode-mapping.yml red-blue/GNEP contradiction, risk-adversarial form incompleteness, boundary-negotiation sign reversal) must be patched before any Pydantic model changes are deployed. A schema that validates mathematically incorrect content with equal authority as correct content is worse than no schema — it creates a false confidence signal. This is the game-theorist's primary axiom and it is now consensus across all four reviewers.

**2. Spec Section 2 amendment before any form-field correction.**
Correcting a template's `form` expression without first amending the spec creates a FR-002 deviation. The game-theorist identified this sequencing requirement in its cross-reviews of spec-compliance and the revised position formalizes it as NR1. Any implementation plan that applies sign convention corrections, form completeness corrections, or dimensional consistency corrections to YAML without a concurrent spec amendment is out of sequence and will produce a compliant-by-schema but spec-deviant library.

**3. mode-mapping.yml must be corrected immediately.**
This is the one fix that does not require a spec amendment (the mapping file is internal to the implementation), does not interact with any sequencing dependency, and has unanimous cross-review consensus. It is the highest-impact-per-effort fix in the entire review. Leaving it uncorrected means spec 014's construction pipeline will assign GNEP to red-blue deliberations and produce structurally incorrect games. There is no argument for delay.

**4. optimization_direction field must accompany, not follow, the sign convention correction.**
Correcting the form expressions in `budget-constrained`, `time-constrained`, and `boundary-negotiation` without simultaneously adding `optimization_direction` to the model means the corrected forms have no machine-readable declaration of their convention. The field and the correction are logically coupled: the correction establishes that all v1 templates minimize, and the field makes that convention explicit and machine-readable. Implementing one without the other is an incomplete fix.

**5. The form_complete warning-level validator scope is not negotiable downward.**
Scoping the validator to scalar/integer parameters only, as a warning rather than a hard validation error, already represents the game-theorist's maximum concession to schema-engineer's fragility objection. The validator must remain in scope because it is the only proposed mechanism that catches simultaneous form-and-example omissions. Removing it entirely leaves the `false_positive_penalty` class of defect invisible to all automated checks.

---

### Flexibility

**1. optional vs. required for optimization_direction.**
Game-theorist holds that optional-with-default is correct for the v1 transition. If functional-architect can demonstrate that coordinating the `optimization_direction` field across all 21 objective YAML files is feasible in a single atomic commit alongside the sign-convention correction, the required approach is acceptable. The argument against required is purely about transition-window risk; if the risk is eliminated by atomicity, the objection is moot.

**2. example_note field design.**
Game-theorist accepts schema-engineer's `example_note: Optional[str] = None` as a suitable home for the human-readable documentation function of `computed_objective`. The game-theorist's interest is in `optimization_direction` absorbing the machine-readable function. If the spec owner decides to combine both into a single structured field rather than two separate ones, that decision does not create a game-theorist objection.

**3. Sequencing of R4/R5 (Nash bargaining, epsilon-constraint) within v1.1.**
Game-theorist defers to functional-architect and schema-engineer on the specific order in which the type system extension enables these templates. The mathematical designs for both templates are stable; the implementation sequencing within the v1.1 track is a schema-engineering and spec-amendment concern, not a game-theory concern.

**4. validate_library_integrity() ownership and placement.**
Game-theorist's NR3 advocates for file-existence checking in `validate_library_integrity()` rather than a static frozenset. If schema-engineer or functional-architect determine that a different function name or module placement better fits the established `game_forms.py` pattern, game-theorist accepts any placement that preserves the file-existence semantics. The architecture is the constraint; the naming and module assignment are flexible.

**5. Cooperative-fairness dimensional correction approach.**
Game-theorist's R8 proposes using the coefficient of variation or Gini coefficient as a dimensionally sound replacement for raw variance in `cooperative-fairness`. If a spec amendment process produces a different dimensionally consistent form that the spec owner prefers, game-theorist accepts it. The constraint is dimensional consistency (the multiplied terms must have the same units); the specific form is not mandated.
