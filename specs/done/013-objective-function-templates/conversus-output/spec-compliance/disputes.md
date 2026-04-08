# Spec Compliance Disputes: 013-objective-function-templates

**Role**: spec-compliance
**Phase**: 4 — Disputes
**Date**: 2026-03-23

---

## Remaining Disputes

### D1 — `computed_objective` / `example_note` disposition

**Positions in conflict**: spec-compliance vs. schema-engineer

spec-compliance's revision (R3) resolves the `computed_objective` question by removal: the key is documentation, not parameterization, and belongs in the template's `description` field or the spec's Section 2 narrative. It should not appear in the machine-readable `example` block in any form — not as `computed_objective`, not as a renamed `example_note` field.

schema-engineer's NR-3 and revised R-3 take the opposite position: `computed_objective` should be migrated to `example_note: Optional[str] = None` on the `ObjectiveTemplate` model, preserving the documentation value while isolating it from the R-4 example-key cross-validator.

The dispute is substantive. Adding `example_note` as a model field:

1. Creates a field that FR-002 does not define. The spec's Section 2 describes "minimal valid parameterization" for the `example` block. It does not describe or anticipate an `example_note` field anywhere. Adding it without a spec amendment is a new FR-deviation of the same kind as the cooperative-fairness catalog omission.
2. Contradicts the rationale for removing `computed_objective` in the first place. If the documentation value is worth preserving in a typed field, it should be in `description` (which already exists and is human-readable) or in Section 2 prose. A parallel semi-typed field on the same model doubles the documentation surface without doubling precision.
3. Preempts the spec owner's decision. Whether the annotation is worth a dedicated model field is a design decision that belongs in a spec amendment, not in an implementation choice made during library standardization.

**spec-compliance position**: `computed_objective` is removed from example blocks. No `example_note` field is added to the model. Documentation of what an objective evaluates to for a given parameterization belongs in `description` or in the spec's Section 2. If schema-engineer believes the documentation value warrants a dedicated model field, the correct path is a spec amendment to FR-002 defining the field before implementation.

---

### D2 — `description` on `ConstraintTemplate`: required vs. optional

**Positions in conflict**: schema-engineer (NR-2, required from day one) vs. functional-architect (R6 revised, optional with follow-on migration) vs. spec-compliance (R8, optional)

schema-engineer's NR-2 argues that making `description` required immediately, with an atomic commit updating all six constraint YAML files simultaneously, is the correct approach because an optional field absent on all existing YAMLs is functionally equivalent to no field at all for spec 014's guided construction pipeline.

functional-architect's revised R6 and spec-compliance's R8 both favor `Optional[str] = None` on the grounds that FR-007 does not require a description field and that a required field breaks existing templates during the transition window.

The positions differ on risk tolerance and on whether the migration is truly "atomic." In practice, a commit updating six YAML files and promoting the field to required in the same commit is operationally atomic — it does not create a window where the model is strict but the YAMLs are not. If the commit discipline can be enforced, schema-engineer's position is architecturally cleaner: it prevents spec 014 from being written to special-case absent descriptions, which would create permanent conditional logic in the pipeline.

**spec-compliance position**: schema-engineer's atomic-migration approach is preferred if the commit discipline can be confirmed. If the six YAML files cannot be updated in a single coordinated commit (e.g., because template authorship is distributed across agents), then optional is the fallback. This is not a hard non-negotiable — it is a sequencing preference contingent on execution realism.

---

### D3 — `optimization_direction` field: game-theorist + functional-architect (NR-1/R6) vs. schema-engineer and spec-compliance

**Positions in conflict**: game-theorist (R6, optional field with default "minimize") and functional-architect (NR-1, required field paired with form-string heuristic validator) vs. schema-engineer (opposed as second source of truth) and spec-compliance (not addressed in original review; no spec basis for the field)

The `optimization_direction` field is proposed by game-theorist and extended by functional-architect as a machine-readable convention declaration. schema-engineer's revision raises the two-sources-of-truth objection: the `form` field already encodes direction implicitly through sign convention, and adding a parallel explicit declaration creates a field that can diverge from the form string.

spec-compliance observes a structural problem the other reviews have not foregrounded: FR-002 through FR-011 do not define an `optimization_direction` field on `ObjectiveTemplate`. Adding it — whether optional or required — is a schema extension that requires a spec amendment. The field is not merely an implementation convenience; it changes what the `ObjectiveTemplate` model represents. A library consumer following the spec would not know to populate or read this field.

game-theorist's revised R6 addresses the FR-002 compliance concern by making the field optional with default `"minimize"`, arguing that existing templates implicitly inherit the convention without schema changes. This is correct at the Pydantic layer: an optional field with a default does not break existing YAML parsing. But it does not address the spec-amendment gap: the spec does not know this field exists, so spec 014 cannot reliably depend on it without a spec update.

**spec-compliance position**: `optimization_direction` should not be added to the model without a spec amendment. The field's value as a machine-readable convention declaration is acknowledged — it is a legitimate design idea. But the implementation-first approach, even with an optional default, instantiates a spec-vs-implementation divergence of the same category as the FR-011 import path mismatch. Propose a spec amendment to FR-002 first; implement after ratification. This is a non-negotiable for spec-compliance.

---

## Convergence

### C1 — YAML correctness patches are the highest-priority immediate action

All four revisions agree, without qualification, that three YAML-level bugs should be patched before any schema work:

- `mode-mapping.yml`: `red-blue: form: gnep` → `red-blue: form: stackelberg`
- `risk-adversarial.yml`: form field updated to include `false_positive_penalty` (pending spec amendment to Section 2 per the agreed sequencing)
- Sign convention corrections for `budget-constrained`, `time-constrained`, and `boundary-negotiation` (pending spec amendment per game-theorist's NR1 protocol)

The `mode-mapping.yml` fix is the only one with no sequencing dependency — all four reviews confirm it can and should be applied immediately. The other two require spec amendment first (game-theorist NR1, endorsed by spec-compliance NR-2).

### C2 — FR-011 import path resolution is a spec amendment, not a package restructure

All four revisions converge on the identical resolution: amend FR-011 to read `from conversus.schemas.objectives import ...`. No reviewer advocates restructuring the package directory. No reviewer advocates a compatibility alias. The spec amendment is the only action.

spec-compliance's reclassification from CRITICAL to HIGH is accepted by the field: game-theorist did not contest the finding; schema-engineer and functional-architect both agree the import path mismatch is real and the fix is amendment-only. This is a closed question.

### C3 — `validate_library_integrity()` as a pure function is the correct constraint resolution mechanism

schema-engineer's R-2 revision (drop the VALID_CONSTRAINTS frozenset in favor of runtime resolution) and functional-architect's R2 (the function itself) and game-theorist's NR3 (file-existence check over closed frozenset) converge on the same implementation pattern. spec-compliance's cross-reviews of schema-engineer and functional-architect both endorsed this direction. The function handles referential integrity, SC-003 cardinality checks, and mode-coverage invariants. It is reusable by spec 014. The loader (`load_objective_templates()`) does discovery only; the integrity function checks constraints.

### C4 — Test infrastructure is prerequisite to further library work

All four revisions identify `tests/test_objectives.py` covering SC-001, SC-002, SC-003 as the most urgently actionable shared finding. The sequencing established across all revisions: fix mathematical errors in templates first (C1), resolve the import path (C2), standardize example format (after the D1 dispute is resolved), then build the test file. Tests written against structurally inconsistent content will need immediate rework. The test file should call `validate_library_integrity()` rather than inlining fixture logic — this is consensus across game-theorist SA-1, functional-architect SA-1, schema-engineer SA-4, and spec-compliance R2 refined.

### C5 — Type system extensions beyond `boolean` require a spec amendment to FR-003

All four revisions converge: `boolean` addition is safe and proceeds. `vector`, `matrix`, and `enum` require a spec amendment to FR-003's explicit four-type enumeration before implementation. game-theorist's sequencing (type system readiness gates Nash bargaining and epsilon-constraint template additions) is consistent with functional-architect's R3 scoped down and schema-engineer's R-6 elevated. spec-compliance's R7 and the cross-review treatment of functional-architect's R3 all point the same direction. This is a closed question for v1.

---

## Final Position Statement

### Non-Negotiables

**No model field additions without a spec amendment.** `optimization_direction` (game-theorist R6, functional-architect NR-1), `example_note` (schema-engineer NR-3), and `game_form_compatibility` on ConstraintTemplate (game-theorist NR2) are all schema extensions that FR-002 through FR-011 do not define. They may be correct design ideas; they are not implementable without spec amendments. An optional field with a default is not a workaround for a missing spec definition — it is a silent deviation of the same kind as the FR-011 import path mismatch. spec-compliance will flag any of these fields added to the implementation without a corresponding spec update as an FR-002 deviation.

**`computed_objective` is removed, not migrated.** The `example_note` field proposal is rejected. Documentation of what an objective evaluates to belongs in `description` or in Section 2 prose. The spec's `example` block is a machine-readable parameterization; adding a documentation annotation field alongside it requires a spec amendment, not an implementation decision. This closes D1 in spec-compliance's favor.

**Spec amendment before YAML correction for form-string changes.** game-theorist's NR1 protocol — amend the spec's Section 2 catalog before updating YAML form fields — is adopted as binding. The `risk-adversarial` form incompleteness and the sign convention corrections for `budget-constrained`, `time-constrained`, and `boundary-negotiation` must run through a spec amendment first. The `mode-mapping.yml` fix is the only YAML correction exempt from this protocol (it is an internal consistency fix with no spec formula to match against).

**Empty `mode_compatibility` must be rejected at validation time.** This is consensus (schema-engineer NR-1, functional-architect R5, spec-compliance NR-3). A template with no compatible modes is dead infrastructure that the model must not allow. The one-line validator addition is unambiguous, backward-compatible, and has no sequencing dependency. It is a non-negotiable correctness requirement.

**The `validate_library_integrity()` function, not a static frozenset, resolves constraint references.** schema-engineer's original VALID_CONSTRAINTS frozenset is withdrawn by schema-engineer itself. The file-existence-check approach (game-theorist NR3) implemented inside `validate_library_integrity()` is the consensus mechanism. spec-compliance endorses this and will treat any static frozenset implementation as an architectural regression from the agreed design.

### Flexibility

**`description` on ConstraintTemplate: required vs. optional.** spec-compliance is flexible on whether the field starts required (schema-engineer NR-2) or optional (functional-architect R6 revised). If the six constraint YAML files can be updated in a single coordinated commit, required is preferable. If commit coordination is impractical, optional with a clear promotion plan is acceptable. spec-compliance does not treat this as a compliance issue either way — FR-007 does not require the field, so neither implementation violates the spec.

**Loader placement.** Whether `load_objective_templates()` lives in `objectives.py` alongside the Pydantic models (schema-engineer's R-7 architecture preference, citing the `game_forms.py` pattern) or in a separate module is an implementation choice spec-compliance does not govern. The function's contract — discovery and per-file validation, no cardinality assertions — is fixed. Placement is the implementer's call.

**Sequencing of independent tracks.** The recommendations that are genuinely independent (duplicate parameter name validation, empty-parameters guard, empty `mode_compatibility` guard, RangeSpec model, `boolean` type addition, `_objective_schema_dir()` helper) can proceed in any order and in parallel with the spec amendment track. spec-compliance has no ordering preference among these. The implementation priority ladder in functional-architect's revised position summary is a reasonable guide but is not binding from a compliance standpoint.

**`form_complete` validator scope and framing.** game-theorist's revised R9 (scalar/integer parameters only, warning not error, verbatim substring matching with explicit naming convention) is a reasonable scoping for a heuristic that spec-compliance did not originally require. spec-compliance's compliance framework does not mandate this validator; if implemented, the scalar-only scoping with warning-level output is the correct framing. If it is not implemented, spec-compliance has no objection.
