# Neutral Synthesis: 013 Objective Function Templates

**Synthesizer**: neutral
**Date**: 2026-03-23
**Deliberation type**: Cooperative
**Target**: Spec 013 -- Objective Function Template Library

---

## Process Summary

| Dimension | Count |
|---|---|
| Agents | 4 (game-theorist, schema-engineer, functional-architect, spec-compliance) |
| Phase 1 reviews | 4 |
| Phase 1 recommendations (total proposed) | 40 (game-theorist: 10, schema-engineer: 10, functional-architect: 10, spec-compliance: 10) |
| Phase 3 recommendations withdrawn | 3 (schema-engineer R-2 frozenset, spec-compliance R10 computed_objective convention, functional-architect O1 ComposedObjective model) |
| Phase 3 recommendations modified | 22 (scope narrowed, priority changed, sequencing adjusted, or implementation approach revised) |
| Phase 3 recommendations maintained without change | 15 |
| Phase 3 new recommendations introduced | 11 (game-theorist: 3, schema-engineer: 3, functional-architect: 3, spec-compliance: 3) |
| Phase 4 surviving recommendations | 48 (original maintained/modified + new) |
| Phase 4 disputes | 3 primary disputes (each raised by multiple agents, yielding 10 dispute filings across all 4 agents) |
| Phase 4 convergence points | 5 confirmed convergence areas (each independently confirmed by all 4 agents) |

---

## Recommendation Scorecard

| # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Convergence | Final Status |
|---|---|---|---|---|---|---|
| GT-R1 | game-theorist | Fix sign convention inconsistency across templates | CRITICAL | Reclassified to spec amendment proposal; CRITICAL retained but target changes to spec | Converged: all agree spec amendment required first | OPEN -- pending spec amendment |
| GT-R2 | game-theorist | Fix mode-mapping.yml red-blue contradiction | HIGH | Upheld without modification | Unanimous (C1 across all agents) | RESOLVED -- apply immediately |
| GT-R3 | game-theorist | Update risk-adversarial form to include false_positive_penalty | HIGH | Upheld; sequenced after spec amendment | Converged: spec amendment first, then YAML | OPEN -- pending spec amendment |
| GT-R4 | game-theorist | Add Nash Bargaining Solution template | HIGH | Conditionally upheld; deferred to v1.1 | Unanimous deferral (C4) | DEFERRED to v1.1 |
| GT-R5 | game-theorist | Add epsilon-constraint template | MEDIUM | Conditionally upheld; deferred to v1.1 | Unanimous deferral (C4) | DEFERRED to v1.1 |
| GT-R6 | game-theorist | Add optimization_direction field to ObjectiveTemplate | HIGH | Upheld; revised to optional with default "minimize" | Disputed (D2/D3 across agents) | DISPUTED -- see Disputes |
| GT-R7 | game-theorist | Resolve endogeneity in competitive-ranking | MEDIUM | Upheld; option (a) selected: J = -score_i | No dispute | RESOLVED -- rewrite template |
| GT-R8 | game-theorist | Fix dimensional inconsistency in cooperative-fairness | MEDIUM | Upheld; sequenced after spec ratification | No dispute | OPEN -- pending spec amendment |
| GT-R9 | game-theorist | Add form_complete validator | MEDIUM | Substantially revised: scalar/integer only, warning not error | Disputed (D2/D3 across agents) | DISPUTED -- see Disputes |
| GT-R10 | game-theorist | Add incentive-compatibility constraint template | LOW | Conditionally upheld; redesign required | No dispute on deferral | DEFERRED -- pending design work |
| GT-NR1 | game-theorist | Establish spec amendment protocol for math corrections | NEW | N/A | Unanimous (C2 across all agents) | RESOLVED -- protocol adopted |
| GT-NR2 | game-theorist | Add game_form_compatibility to ConstraintTemplate | NEW | N/A | Blocked by spec-compliance (no new fields without spec amendment) | DEFERRED -- pending spec amendment |
| GT-NR3 | game-theorist | File-existence check instead of VALID_CONSTRAINTS frozenset | NEW | N/A | Unanimous (C3 across all agents) | RESOLVED -- adopted in validate_library_integrity() |
| SE-R1 | schema-engineer | Add duplicate parameter name detection | HIGH | Maintained | Unanimous (C3 across all agents) | RESOLVED -- implement immediately |
| SE-R2 | schema-engineer | Add VALID_CONSTRAINTS frozenset | MEDIUM | WITHDRAWN in favor of runtime integrity checking | Unanimous withdrawal (C2/C3) | WITHDRAWN |
| SE-R3 | schema-engineer | Standardize example format | HIGH | Maintained with clarification on computed_objective | Converged on flat format; computed_objective disposition disputed (D1/D3) | PARTIALLY DISPUTED -- see Disputes |
| SE-R4 | schema-engineer | Cross-validate example keys against parameter names | MEDIUM | Maintained; sequencing gate added (after R3, exclude function-type params) | Converged on sequencing | RESOLVED -- implement after R3 |
| SE-R5 | schema-engineer | Create RangeSpec model | MEDIUM | Maintained with type-aware extension | No dispute | RESOLVED -- implement |
| SE-R6 | schema-engineer | Add boolean to parameter type system | LOW | Elevated to MEDIUM on correctness grounds | Unanimous (C5 across all agents) | RESOLVED -- implement |
| SE-R7 | schema-engineer | Add load_objective_template() and load_constraint_template() | MEDIUM | Maintained; architecture clarified (single-file loader + separate integrity function) | Converged with functional-architect | RESOLVED -- implement |
| SE-R8 | schema-engineer | Resolve FR-011 import path discrepancy | HIGH | Maintained: amend FR-011 to match conversus.schemas | Unanimous (C2 across all agents) | RESOLVED -- spec amendment |
| SE-R9 | schema-engineer | Add empty-parameters guard | LOW | Maintained | No dispute | RESOLVED -- implement |
| SE-R10 | schema-engineer | Add model_config extra="forbid" | MEDIUM | Deferred: sequenced after YAML standardization | Converged on sequencing (C5 across all agents) | DEFERRED -- implement after SE-R3, SE-R4 |
| SE-NR1 | schema-engineer | Add empty mode_compatibility guard | NEW (HIGH) | N/A | Unanimous (confirmed across all agents) | RESOLVED -- implement immediately |
| SE-NR2 | schema-engineer | Add description as required to ConstraintTemplate with atomic YAML migration | NEW (MEDIUM) | N/A | Disputed (D1/D2 across agents) | DISPUTED -- see Disputes |
| SE-NR3 | schema-engineer | Add example_note field as prerequisite for R3/R4 | NEW (HIGH) | N/A | Disputed (D1/D3 across agents) | DISPUTED -- see Disputes |
| FA-R1 | functional-architect | Add load_objective_templates() function | HIGH | Scoped down: no cardinality assertions in loader | Converged with schema-engineer | RESOLVED -- implement (scoped) |
| FA-R2 | functional-architect | Add validate_library_integrity() function | HIGH | Maintained; scope expanded to include form heuristics | Unanimous (C3 across all agents) | RESOLVED -- implement |
| FA-R3 | functional-architect | Extend parameter type system (vector, matrix, boolean, enum) | HIGH | Scoped to boolean only for v1; remainder deferred to spec amendment | Unanimous (C5 across all agents) | PARTIALLY RESOLVED -- boolean now; rest deferred |
| FA-R4 | functional-architect | Add duplicate parameter name validation | MEDIUM | Maintained; elevated to HIGH | Unanimous (C3 across all agents) | RESOLVED -- implement immediately |
| FA-R5 | functional-architect | Add empty mode_compatibility validation | MEDIUM | Maintained | Unanimous | RESOLVED -- implement |
| FA-R6 | functional-architect | Add description field to ConstraintTemplate | MEDIUM | Maintained; revised to Optional[str] = None | Disputed (D1/D2 across agents) | DISPUTED -- see Disputes |
| FA-R7 | functional-architect | Standardize example field structure and add validation | MEDIUM | Sequencing clarified: YAML first, validator second | Converged on sequencing | RESOLVED -- implement in sequence |
| FA-R8 | functional-architect | Type the range field as a Pydantic model | LOW | Maintained | No dispute | RESOLVED -- implement |
| FA-R9 | functional-architect | Add _objective_schema_dir() helper | LOW | Maintained | No dispute | RESOLVED -- implement |
| FA-R10 | functional-architect | Export frozenset constants from __init__.py | LOW | Maintained | No dispute | RESOLVED -- implement |
| FA-NR1 | functional-architect | Add optimization_direction field paired with integrity heuristic | NEW (MEDIUM) | N/A | Disputed (D3 across agents) | DISPUTED -- see Disputes |
| FA-NR2 | functional-architect | Apply immediate YAML patches for known correctness bugs | NEW (CRITICAL) | N/A | Unanimous (C1 across all agents) | RESOLVED -- apply immediately |
| FA-NR3 | functional-architect | Establish spec policy on template additions beyond Section 2 catalog | NEW (LOW) | N/A | No dispute | RESOLVED -- establish policy |
| SC-R1 | spec-compliance | Reconcile import path (FR-011) | CRITICAL | Reclassified to HIGH; spec amendment only | Unanimous (C2 across all agents) | RESOLVED -- spec amendment |
| SC-R2 | spec-compliance | Add tests/test_objectives.py covering SC-001, SC-002, SC-003 | HIGH | Maintained; scope refined | Unanimous (C4 across all agents) | RESOLVED -- implement |
| SC-R3 | spec-compliance | Standardize example block format | HIGH | Maintained; computed_objective removed | Converged on flat format; removal vs. migration disputed (D1) | PARTIALLY DISPUTED -- see Disputes |
| SC-R4 | spec-compliance | Add examples to constraint templates (SC-005) | MEDIUM | Maintained | No dispute | RESOLVED -- implement |
| SC-R5 | spec-compliance | Update spec Section 2 to include cooperative-fairness | MEDIUM | Maintained; prerequisite: fix dimensional inconsistency first | No dispute | RESOLVED -- amend spec after fixing formula |
| SC-R6 | spec-compliance | Isolate click dependency | MEDIUM | Maintained; scope clarified | No dispute | RESOLVED -- implement |
| SC-R7 | spec-compliance | Consider adding array parameter type | LOW | Maintained; deferred to spec amendment track | Unanimous (C5 across all agents) | DEFERRED to FR-003 amendment |
| SC-R8 | spec-compliance | Add description to ConstraintTemplate | LOW | Maintained; elevated to MEDIUM | Disputed (D1/D2 across agents) | DISPUTED -- see Disputes |
| SC-R9 | spec-compliance | Implement minimal template registry | LOW | Maintained; scope elevated | Converged with FA-R1, SE-R7 | RESOLVED -- implement |
| SC-R10 | spec-compliance | Add computed_objective documentation convention | LOW | WITHDRAWN | Superseded by R3 resolution | WITHDRAWN |
| SC-NR1 | spec-compliance | Fix mode-mapping.yml red-blue/Stackelberg contradiction | NEW (HIGH) | N/A | Unanimous (C1 across all agents) | RESOLVED -- apply immediately |
| SC-NR2 | spec-compliance | Amend spec Section 2 to correct risk-adversarial form | NEW (MEDIUM) | N/A | Converged: spec amendment first | RESOLVED -- spec amendment |
| SC-NR3 | spec-compliance | Empty mode_compatibility must be rejected | NEW (LOW) | N/A | Unanimous | RESOLVED -- implement |

---

## Convergence Achieved

### 1. Mode-mapping.yml Red-Blue/Stackelberg Fix (Unanimous, Unconditional)

All four agents agree without qualification that `mode-mapping.yml` declares `red-blue: form: gnep` while all three red-blue templates correctly use `game_form: stackelberg`. The fix -- update `mode-mapping.yml` to `red-blue: form: stackelberg` -- requires no spec amendment, no schema changes, and has no sequencing dependencies. It is the highest-impact-per-effort fix identified and should be applied immediately.

Sources: game-theorist R2, schema-engineer SA-1 (cross-review), functional-architect SA-1 (cross-review), spec-compliance NR-1.

### 2. Duplicate Parameter Name Validation (Unanimous, Unconditional)

All four agents independently identified and endorsed adding a model_validator to ObjectiveTemplate (and ConstraintTemplate) that rejects templates with duplicate parameter names. Implementation is a two-line addition. The failure mode (silent shadowing of parameter definitions) is real and has no counterargument.

Sources: schema-engineer R-1, functional-architect R4, spec-compliance SA-2, game-theorist SA-3.

### 3. VALID_CONSTRAINTS Frozenset Withdrawn; Runtime Integrity Checking Adopted (Unanimous)

Schema-engineer withdrew R-2 (static frozenset) after cross-review. All agents converge on: modes and game forms are spec-defined closed sets (frozenset appropriate); constraint names are filesystem-derived open sets (runtime resolution via `validate_library_integrity()` appropriate). The file-existence check or loaded-dict lookup in `validate_library_integrity()` is the consensus mechanism.

Sources: schema-engineer R-2 revision, game-theorist NR3, functional-architect R2, spec-compliance endorsement.

### 4. Spec Amendment Protocol for Form-Field Corrections (Unanimous)

All agents converge on the principle: any correction to a template's `form` field that changes the mathematical expression requires a spec Section 2 amendment before the YAML is updated. This prevents FR-002 deviations during correction. The mode-mapping.yml fix is the sole exempt case (internal consistency fix with no spec formula to match).

Sources: game-theorist NR1, spec-compliance NR-2, functional-architect NR-2 (revised to accept protocol), schema-engineer (implicit via R-8 precedent).

### 5. Nash Bargaining and Epsilon-Constraint Templates Deferred to v1.1 (Unanimous)

All agents agree both templates are mathematically sound but cannot be implemented until the type system supports their parameter structures (`list[function]` for Nash bargaining, `vector` for epsilon-constraint). The deferral is process-based: FR-012/FR-013 thresholds are already met; the type system extension (beyond `boolean`) requires a FR-003 spec amendment.

Sources: game-theorist R4/R5 revision, functional-architect R3 scoped, schema-engineer R-6, spec-compliance R7.

### 6. FR-011 Import Path: Spec Amendment to `conversus.schemas` (Unanimous)

All four agents agree: amend FR-011 to `from conversus.schemas.objectives import ...`. No package restructuring. No compatibility alias. Severity reclassified from CRITICAL to HIGH.

Sources: schema-engineer R-8, spec-compliance R1 revision, functional-architect concession, game-theorist non-objection.

### 7. Boolean Type Addition Proceeds Without Spec Amendment (Unanimous)

All agents converge on adding `"boolean"` to `VALID_PARAMETER_TYPES` at Medium priority. The correctness hazard (`bool("false") is True` in Python) is concrete and present. The broader type extensions (`vector`, `matrix`, `enum`) require a FR-003 spec amendment and are deferred.

Sources: schema-engineer R-6 elevated, functional-architect R3 scoped, spec-compliance R7/C5, game-theorist DC-3.

### 8. Implementation Sequencing (Substantially Aligned)

Despite arriving from four different domains, all agents converge on the same broad ordering:
1. YAML correctness patches (mode-mapping.yml immediately; form corrections after spec amendment)
2. Independent model improvements (duplicate names, empty mode_compatibility, empty parameters, RangeSpec, boolean type, _objective_schema_dir(), __init__.py exports)
3. Example standardization track (resolve computed_objective disposition, standardize YAML, add example-key validator, then extra="forbid")
4. Loader and integrity infrastructure (load_objective_templates(), validate_library_integrity())
5. Test infrastructure (test_objectives.py)

Sources: functional-architect position summary priority ladder, schema-engineer sequencing chain, game-theorist C5, spec-compliance C4.

<!-- CONVERSUS:DISPUTES_BEGIN -->

## Remaining Disputes

### Dispute A: `optimization_direction` Field -- Add vs. Defer

**Positions**:

- **FOR addition (game-theorist R6, functional-architect NR-1)**: The sign convention inconsistency across templates exists because the optimization direction is implicit. Adding `optimization_direction: Literal["minimize", "maximize"] = "minimize"` as an optional field with default provides a machine-readable convention declaration for spec 014's construction pipeline. The optional-with-default design preserves FR-002 compliance for existing templates. The field should be paired with a heuristic consistency check in `validate_library_integrity()`.

- **AGAINST addition at the model level (schema-engineer)**: The field creates a second source of truth alongside the `form` string. A template author can write `optimization_direction: maximize` without adjusting the form's sign convention, creating a silent inconsistency that is formally in the schema and worse than the current implicit state. The schema layer should only enforce what can be enforced. If form-string sign consistency cannot be reliably validated, the field should not exist as a schema claim.

- **AGAINST addition without spec amendment (spec-compliance)**: FR-002 through FR-011 do not define this field. Adding it -- even as optional with a default -- instantiates a spec-vs-implementation divergence of the same category as the FR-011 import path mismatch. The field requires a spec amendment to FR-002 before implementation.

**Synthesizer assessment**: The underlying problem -- no machine-readable optimization direction -- is real and acknowledged by all parties. The disagreement is about remedy and process. Schema-engineer's two-sources-of-truth concern is mitigated (not eliminated) by game-theorist's revised framing of the field as a "declaration of intent, not a validated constraint." Spec-compliance's procedural objection is consistent with the spec amendment protocol already adopted for other changes. The strongest path forward combines both procedural requirements: propose a spec amendment to FR-002 adding the field, then implement as optional with default "minimize." This satisfies spec-compliance's process requirement without losing the field's value.

**Recommended resolution**: Propose a spec amendment to FR-002 adding `optimization_direction` as an optional field. Implement after ratification. The field should be `Optional[Literal["minimize", "maximize"]] = "minimize"`. Any consistency checking between the field and the form string lives in `validate_library_integrity()` as a best-effort heuristic, not in a model_validator. This resolves all three positions: game-theorist gets the machine-readable declaration; schema-engineer avoids a hard validation coupling between the field and the opaque form string; spec-compliance gets the spec amendment before implementation.

---

### Dispute B: `computed_objective` Disposition -- Remove vs. Migrate to `example_note`

**Positions**:

- **REMOVE entirely (spec-compliance)**: FR-002's "minimal valid parameterization" means parameter names and values only. `computed_objective` is documentation, not parameterization. It belongs in the `description` field or in the spec's Section 2 narrative. Adding `example_note` creates a model field that FR-002 does not define, which is a new spec deviation.

- **MIGRATE to `example_note: Optional[str] = None` (schema-engineer, functional-architect)**: The content in `computed_objective` (e.g., "minimize J approximately-equals quality - 0.5 * cost") is semantically distinct from the template `description` (which describes the template's purpose, not an example evaluation). `example_note` preserves the documentation value in a typed field that spec 014 can consume. The field costs one optional string.

- **REMOVE only after `optimization_direction` is added (game-theorist)**: `computed_objective` implicitly encodes optimization direction. Removing it before `optimization_direction` exists destroys machine-readable metadata without replacement. The `example_note` field carries the human-readable function; `optimization_direction` carries the machine-readable function. Both are needed before `computed_objective` can be safely removed.

**Synthesizer assessment**: The three positions represent a spectrum from strict spec fidelity (spec-compliance) through pragmatic documentation preservation (schema-engineer/functional-architect) to dependency coupling (game-theorist). Spec-compliance's point about FR-002 scope is procedurally correct: adding `example_note` without a spec amendment is the same class of deviation as the others. Game-theorist's coupling argument has merit but creates a dependency chain that blocks example standardization behind the `optimization_direction` spec amendment. The pragmatic middle ground: `computed_objective` is removed from example blocks immediately (enabling R3 standardization and R4 cross-validation to proceed), and any documentation value is absorbed into the `description` field for now. If spec 014's design reveals that a separate `example_note` field is needed, it can be proposed as a spec amendment at that time.

**Recommended resolution**: Remove `computed_objective` from all example blocks. Do not add `example_note` as a model field at this time. Absorb any documentation content into the template's `description` field where it adds value. If the `optimization_direction` field is adopted via spec amendment (see Dispute A), it absorbs the machine-readable function that `computed_objective` partially served. This unblocks the example standardization track without adding spec-unamended model fields.

---

### Dispute C: `description` on ConstraintTemplate -- Required vs. Optional

**Positions**:

- **REQUIRED with atomic YAML migration (schema-engineer NR-2)**: All six constraint YAMLs already contain description text in header comments. The migration is bounded and certain. Starting optional creates a window where spec 014 must special-case absent descriptions, and that defensive code persists permanently.

- **OPTIONAL now, required later (functional-architect R6 revised, spec-compliance R8)**: FR-007 does not mandate a description field. Making it required couples the schema change with content population in a single deployment. Optional-first decouples them and reduces risk.

**Synthesizer assessment**: Both positions lead to the same destination (required `description`). The dispute is about deployment atomicity. Schema-engineer's argument is strongest: the migration surface is six files with known content. Functional-architect's own resolution condition confirms this -- "if the six constraint YAML header comments are adequate verbatim, schema-engineer wins." Spec-compliance is flexible contingent on commit discipline. The practical question is whether the header comments are sufficient as descriptions without material rewording.

**Recommended resolution**: Add `description: str` as required to `ConstraintTemplate`, with atomic YAML migration updating all six constraint files in the same commit. The migration surface is small (six files), the content source is known (existing header comments), and this prevents spec 014 from needing to handle absent constraint descriptions. If inspection reveals that any header comment requires substantial rewording beyond extraction, fall back to `Optional[str] = None` and promote to required in a follow-on commit.

---

### Dispute D: Form-Completeness Validator -- Placement and Scope

**Positions**:

- **In the Pydantic model as a warning (game-theorist R9 revised)**: A scoped validator checking that scalar/integer parameter names appear as substrings in the `form` field, implemented as a warning-level check. This is the only mechanism that catches simultaneous form-and-example omissions (the `false_positive_penalty` class of defect).

- **In `validate_library_integrity()` as a diagnostic, not in the model (schema-engineer, functional-architect D2)**: Pydantic validators raise or pass -- they cannot emit warnings natively. The form string is semantically opaque at the schema layer. Form-completeness and sign-convention checks belong in the integrity function as structured diagnostics, not in model validators.

**Synthesizer assessment**: The positions are closer than they appear. Game-theorist's "warning" framing implicitly requires placement outside the Pydantic model, because Pydantic validators cannot emit warnings -- they must raise or be silent. Functional-architect's D2 resolution condition states this explicitly: "both live in `validate_library_integrity()` as diagnostic checks that return structured findings rather than raising exceptions." Game-theorist's substantive requirement -- that the check exists and catches the `false_positive_penalty` class of defect -- is satisfied by placement in the integrity function. Schema-engineer's non-negotiable -- that the model layer treats `form` as opaque -- is also satisfied.

**Recommended resolution**: Place the form-completeness check (scalar/integer parameter name substring presence) in `validate_library_integrity()`, not in a Pydantic model_validator. The check returns structured diagnostics (advisory findings, not hard failures). Model validators remain strict and raise only for definite structural invalidity. This preserves game-theorist's detection capability, respects schema-engineer's form-opacity boundary, and matches functional-architect's integrity function architecture.

<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

### P1 -- Must Implement

| # | Change | Source Recommendations | Rationale |
|---|---|---|---|
| P1-1 | Update `mode-mapping.yml`: `red-blue: form: stackelberg` | GT-R2, SC-NR1, FA-NR2 | Unanimous. Cross-artifact contradiction with downstream impact on spec 014. No dependencies. |
| P1-2 | Add duplicate parameter name validation to ObjectiveTemplate and ConstraintTemplate model_validators | SE-R1, FA-R4 | Unanimous. Silent shadowing is a real failure mode. Two-line addition. |
| P1-3 | Add empty `mode_compatibility` guard to ObjectiveTemplate and ConstraintTemplate | SE-NR1, FA-R5, SC-NR3 | Unanimous. Dead infrastructure prevention. One-line addition. |
| P1-4 | Amend FR-011 to `from conversus.schemas.objectives import ...` | SE-R8, SC-R1 | Unanimous. Current spec text produces ImportError. |
| P1-5 | Amend spec Section 2 to declare universal minimization convention; correct forms for `budget-constrained`, `time-constrained`, `boundary-negotiation`; then update YAML to match | GT-R1, GT-NR1 | Spec amendment protocol requires spec change first. Mathematical correctness bugs acknowledged by all agents. |
| P1-6 | Amend spec Section 2 to include complete `risk-adversarial` form with `false_positive_penalty`; then update YAML | GT-R3, SC-NR2 | Form incompleteness changes equilibrium structure. Spec amendment protocol applies. |
| P1-7 | Standardize example blocks to flat parameter-name-to-value format across all 21 templates | SE-R3, FA-R7, SC-R3 | Prerequisite for machine-parseable examples. Seven templates currently use inconsistent nested format. |
| P1-8 | Add `tests/test_objectives.py` covering SC-001, SC-002, SC-003, SC-005 | SC-R2 | No existing test coverage for objective template validation. |
| P1-9 | Add `load_objective_templates()` and `load_constraint_templates()` utilities | SE-R7, FA-R1, SC-R9 | No loader exists; SC-003 is untestable without one. Follow `game_forms.py` pattern. |
| P1-10 | Add `validate_library_integrity()` pure function | FA-R2, GT-NR3 | Cross-artifact integrity checks (constraint references, cardinality, mode coverage) have no current mechanism. |

### P2 -- Should Implement

| # | Change | Source Recommendations | Rationale |
|---|---|---|---|
| P2-1 | Add `"boolean"` to VALID_PARAMETER_TYPES; convert `normalize` parameters in weighted-sum and minimax | SE-R6, FA-R3 | `bool("false") is True` in Python -- correctness hazard. Medium priority consensus. |
| P2-2 | Create RangeSpec Pydantic model to replace `dict[str, Any]` for parameter ranges; add type-aware range rejection for non-numeric types | SE-R5, FA-R8 | Prevents silent typo acceptance and semantically incoherent range constraints on string-type parameters. |
| P2-3 | Add `description: str` to ConstraintTemplate (required, with atomic YAML migration) | SE-NR2, FA-R6, SC-R8 | Spec 014 pipeline needs machine-readable constraint descriptions. See Dispute C resolution. |
| P2-4 | Rewrite `competitive-ranking.yml` to use `J = -score_i` with rank as post-hoc derived outcome | GT-R7 | Endogeneity problem: rank depends on all agents' strategies and cannot be an input parameter. |
| P2-5 | Add example-key cross-validator to ObjectiveTemplate (after P1-7 standardization; exclude function-type parameters) | SE-R4 | Catches example/parameter mismatches. Gated on example standardization. |
| P2-6 | Amend spec Section 2 to include `cooperative-fairness` with dimensionally corrected formula | SC-R5, GT-R8 | Template exists but is not in spec catalog, and its formula has a dimensional inconsistency. |
| P2-7 | Add examples to all six constraint template YAML files | SC-R4 | SC-005 conservative reading requires example parameterizations for all templates. |
| P2-8 | Add `_objective_schema_dir()` and `_constraint_schema_dir()` helpers | FA-R9 | Prerequisite for loader functions. Follows `game_forms.py` pattern. |
| P2-9 | Export `VALID_MODES`, `VALID_PARAMETER_TYPES`, `VALID_GAME_FORMS` from `__init__.py` | FA-R10 | Consistency with game_forms.py; needed by external validators. |
| P2-10 | Add empty-parameters guard to ObjectiveTemplate | SE-R9 | Prevents vacuous templates with no parameters from passing validation. |

### P3 -- Consider

| # | Change | Source Recommendations | Rationale |
|---|---|---|---|
| P3-1 | Add `optimization_direction` field to ObjectiveTemplate via spec amendment to FR-002 | GT-R6, FA-NR1 | Machine-readable convention declaration. Requires spec amendment first (Dispute A resolution). |
| P3-2 | Isolate `click` dependency to optional extras group in pyproject.toml | SC-R6 | Packaging hygiene; Section 5 interpretation ambiguity. |
| P3-3 | Add `extra="forbid"` to all models (after P1-7 and P2-5 are complete) | SE-R10 | Prevents silent acceptance of unexpected YAML keys. Sequenced last in example standardization track. |
| P3-4 | Establish spec policy on whether template additions beyond Section 2 require spec amendments | FA-NR3 | Policy gap: `cooperative-fairness` was added without spec change; future additions need a clear rule. |
| P3-5 | Propose FR-003 spec amendment to add `vector`, `matrix`, `enum` to parameter type vocabulary | FA-R3 (deferred portion), SC-R7 | Current four-type system forces structured data into `string` type. Prerequisite for v1.1 templates. |
| P3-6 | Add `game_form_compatibility` field to ConstraintTemplate via spec amendment | GT-NR2 | Low-cost extensibility hook for spec 014 constraint selection. Requires spec amendment. |
| P3-7 | Add form-completeness diagnostic check to `validate_library_integrity()` for scalar/integer parameters | GT-R9 (revised) | Advisory heuristic catching the `false_positive_penalty` class of defect. See Dispute D resolution. |
| P3-8 | Design and add incentive-compatibility constraint template | GT-R10 | Requires `derived_from` on function-type params, parameter-compatibility design work, and possible VALID_CONSTRAINTS update. |
| P3-9 | Add Nash Bargaining Solution template (v1.1, after type system extension) | GT-R4 | Most important missing cooperative game theory form. Blocked on FR-003 amendment. |
| P3-10 | Add epsilon-constraint template (v1.1, after type system extension) | GT-R5 | Completes standard scalarization toolkit. Blocked on FR-003 amendment. |

---

## Key Concessions

### game-theorist

- **R1 (sign convention fix) reclassified from direct YAML fix to spec amendment proposal.** Accepted spec-compliance's finding that the YAML matches the spec's own Section 2 formulas, meaning the fix must target the spec first. "This is a sequencing discipline, not a retreat from the mathematical substance."
- **R4, R5, R10 (Nash bargaining, epsilon-constraint, incentive-compatibility) deferred to v1.1.** Accepted functional-architect's finding that the current type system cannot represent per-agent-indexed parameters or vectors, and schema-engineer's observation that adding templates before extending the type system instantiates the anti-pattern functional-architect warns against.
- **R9 (form_complete validator) substantially narrowed.** Accepted schema-engineer's fragility objection for function-type and string-type parameters; accepted that the validator must be scoped to scalar/integer parameters only and framed as a warning rather than hard validation error.

### schema-engineer

- **R-2 (VALID_CONSTRAINTS frozenset) withdrawn permanently.** Conceded that a hardcoded frozenset of filesystem-derived names is categorically different from a frozenset of spec-defined modes. "This was an architectural error in the original review, not a sequencing issue."
- **R-10 (extra="forbid") deferred.** Accepted that applying the guard before YAML standardization creates false confidence rather than catching real drift.
- **R-6 (boolean type) elevated from LOW to MEDIUM.** Accepted game-theorist's correctness argument (`bool("false") is True`).

### functional-architect

- **R1 (loader) scoped down.** Removed embedded cardinality assertions from the loader's contract; accepted that completeness checks belong in `validate_library_integrity()` and tests, not inside a discovery function.
- **O1 (ComposedObjective model) withdrawn.** Accepted spec-compliance's finding that bare-string constraint references are the spec's deliberate design choice, and that `validate_library_integrity()` provides sufficient referential integrity without a new model type.
- **R3 (type system extension) scoped to boolean only for v1.** Accepted spec-compliance's finding that FR-003 explicitly enumerates four types and that broader extensions require a spec amendment.
- **FR-011 omission acknowledged.** Conceded that the import path deviation is a real compliance item, not "spec noise."

### spec-compliance

- **R1 (import path) reclassified from CRITICAL to HIGH.** Accepted all three cross-reviewers' argument that mathematical correctness errors have at least equal operational severity to an import path mismatch in an unreleased library.
- **R10 (computed_objective convention) withdrawn.** Superseded by the removal resolution in R3.
- **Mathematical correctness as within-scope acknowledged.** Original review operated exclusively at the structural/compliance layer; accepted game-theorist's demonstration that schema validation and mathematical correctness are distinct verification axes, and that form-level correctness bugs have compliance-layer consequences for downstream specs.
