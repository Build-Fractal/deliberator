# Schema Engineer Disputes — 013 Objective Function Templates

**Role**: schema-engineer
**Phase**: 4 — Disputes
**Date**: 2026-03-23

---

## Remaining Disputes

### Dispute 1: optimization_direction field — two sources of truth vs. missing machine-readable convention

**Between**: schema-engineer and game-theorist / functional-architect

**The disagreement**: Game-theorist R6 and functional-architect NR-1 both advocate for adding `optimization_direction: Literal["minimize", "maximize"]` to `ObjectiveTemplate`, arguing that without it the sign convention is implicit and undeclared. Schema-engineer's revision maintains that the field creates a redundant second source of truth alongside the `form` string: a template with `form: "J = quality - beta * cost"` and `optimization_direction: maximize` is internally contradictory, but the Pydantic model cannot detect the contradiction because `form` is an opaque string.

**Game-theorist's revised position**: Make `optimization_direction` optional with default `"minimize"`. This preserves FR-002 compliance for existing templates while providing an explicit machine-readable declaration for the convention. The field's purpose shifts from enforcement to documentation — it states the intended direction without claiming to validate the form string's sign consistency.

**Functional-architect's revised position**: Add the field and pair it with a heuristic integrity check in `validate_library_integrity()` that flags templates where the declared direction appears inconsistent with the form string's sign pattern. Explicitly acknowledges the heuristic is imperfect and states it as best-effort.

**Schema-engineer's position**: The two-sources-of-truth problem is not eliminated by making the field optional with a default. A future template author who writes `optimization_direction: maximize` without adjusting the form string's signs has now introduced a silent inconsistency that is formally present in the schema and is worse than the current implicit state, because it creates false confidence. The schema layer's job is to enforce what can be enforced. If form-string sign consistency cannot be reliably validated, the field should not exist as a schema claim — it belongs in the spec's Section 2 narrative and in the template's `description` field, not as a model attribute.

**What is genuinely unresolved**: Whether the documentation value of an optional machine-readable direction field outweighs the false-confidence risk of an unenforceable schema claim. Schema-engineer concedes that the sign convention problem is real and harmful. The dispute is about whether a partially-enforceable field at the schema layer is better or worse than relying on YAML authoring discipline and the existing `validate_library_integrity()` heuristic check alone.

---

### Dispute 2: computed_objective disposition — remove vs. migrate to example_note field

**Between**: schema-engineer and spec-compliance

**The disagreement**: Spec-compliance's revision resolves the `computed_objective` question by removing it outright from all example blocks. Schema-engineer's revision proposes migrating it to a new `example_note: Optional[str] = None` field on `ObjectiveTemplate`, preserving the documentation value as a typed model attribute rather than an ad-hoc annotation key inside the example dict.

**Spec-compliance's position**: `computed_objective` is a documentation annotation, not a parameter. FR-002's "minimal valid parameterization" means parameter names and values only. The clean resolution is removal; documentation of what the objective evaluates to belongs in the `description` field or in the spec's Section 2 narrative. Promoting it to a new field adds schema surface area to preserve content that can live in existing fields.

**Schema-engineer's position**: `computed_objective`'s content — e.g., "minimize J ≈ quality - 0.5 * cost" — is distinct from the template `description` field (which describes the template's purpose and game-theoretic role, not an example evaluation). Removing it without a replacement destroys documentation value that spec 014's prompt construction will benefit from: when presenting a template to users, having a concrete illustrative evaluation is more useful than the abstract form string alone. The `example_note` field costs one optional string field on the model, resolves the DC-1 contradiction cleanly, provides a typed migration target for the YAML update, and gives spec 014 a machine-readable hook without cluttering the example dict.

**What is genuinely unresolved**: Whether `example_note` adds enough value over putting the content in `description` to justify adding a new model field. The dispute is narrow: both sides agree the content should not remain inside the example dict. The disagreement is whether removal-and-redirect-to-description or removal-and-migration-to-example_note is the better resolution. The arbiter should determine whether the downstream spec 014 use case justifies the new field.

---

### Dispute 3: description on ConstraintTemplate — required now vs. optional now with promotion later

**Between**: schema-engineer (NR-2, required) and functional-architect (R6 revised, optional now) and spec-compliance (R8, optional)

**The disagreement**: Schema-engineer's revision recommends adding `description: str` as required to `ConstraintTemplate`, with atomic YAML migration of all six constraint files in the same commit. Functional-architect and spec-compliance both recommend `Optional[str] = None` — start optional, populate YAMLs, promote to required in a follow-on commit.

**Functional-architect and spec-compliance's position**: Making it required immediately creates a forced migration in a single commit. FR-007 does not mandate a description field. Optional-now, required-later is lower risk.

**Schema-engineer's position**: The "optional now, required later" pattern has a well-documented failure mode in this codebase: optional fields that serve mandatory downstream use cases get populated lazily or not at all, because the schema never rejects their absence. All six constraint YAML files already contain the description text in header comments — the migration cost is six mechanical YAML edits, all bounded and certain. The argument against atomic migration (commit coordination complexity) is weaker than the argument for it (no window in which spec 014 must special-case constraints). If the field is optional, spec 014 must treat absent descriptions gracefully, and that defensive code never gets removed once it ships.

**What is genuinely unresolved**: The risk tolerance for atomic migration vs. incremental promotion. This is a process preference, not a fundamental architectural disagreement. The arbiter should choose one path; both are technically sound.

---

## Convergence

### C-1: mode-mapping.yml red-blue/Stackelberg fix — unconditional consensus

All four reviews agree that `mode-mapping.yml` declaring `red-blue: form: gnep` while all three red-blue templates correctly use `game_form: stackelberg` is an unambiguous cross-artifact contradiction with downstream consequences for spec 014's construction pipeline. No reviewer disputes the fix: update `mode-mapping.yml` to declare `red-blue: form: stackelberg`. No spec amendment required. No schema changes required. Apply immediately.

### C-2: VALID_CONSTRAINTS frozenset abandoned in favor of runtime library integrity checking

Schema-engineer concedes R-2 from the original review. A hardcoded frozenset of constraint names is categorically different from `VALID_MODES` and `VALID_GAME_FORMS`: modes and game forms are normatively enumerated in the spec and will not grow without a spec revision; constraints are filesystem-derived and will grow. The correct mechanism is `validate_library_integrity()` (functional-architect R2) checking that every `ObjectiveTemplate.constraints` entry resolves to a loaded `ConstraintTemplate`. Game-theorist's NR-3 (file-existence check) is compatible with this approach. All four reviews accept this resolution.

### C-3: Duplicate parameter name validation — unanimous, unconditional

Schema-engineer R-1, functional-architect R4, and spec-compliance SA-2 all independently identify this gap with nearly identical implementation code. No reviewer disputes the fix. The validator is a two-line addition to `ObjectiveTemplate`'s model_validator. This is the strongest cross-review consensus in the entire process.

### C-4: Implementation sequencing for example standardization track

The sequencing dispute between schema-engineer and functional-architect on examples is resolved: NR-3 (example_note field decision or removal decision — whichever the arbiter chooses) gates R-3 (YAML standardization), which gates R-4 (example key cross-validator, excluding function-type parameters), which gates R-10 (extra="forbid"). The sequencing is agreed; only the NR-3 content decision (Dispute 2) remains open.

### C-5: Boolean type addition at Medium priority

Schema-engineer R-6 and functional-architect R3 (scoped) and spec-compliance R7 (framed as type system gap) all converge on `"boolean"` as the minimum necessary type addition for the two `normalize` parameters. Game-theorist elevates this to Medium priority on correctness grounds (`bool("false") is True` in Python). The `vector`/`matrix`/`enum` extensions are deferred to a spec amendment for FR-003. All reviewers accept this scoping. The `"boolean"` addition proceeds without spec amendment.

---

## Final Position Statement

### Non-Negotiables

**1. The schema layer treats `form` as a semantically opaque string.**

No model validator inspects, parses, or tokenizes the `form` field's mathematical content. Form correctness is a review and authoring concern, not a schema concern. Any recommendation that requires substring matching, token extraction, or sign-pattern heuristics inside a Pydantic validator is rejected at the schema layer. Those checks belong in `validate_library_integrity()` as explicitly best-effort guards, labeled as such, not as model_validators that raise hard ValidationErrors.

This is not a concession to mathematical imprecision — it is a correct allocation of responsibility. The game-theorist identified real mathematical defects (boundary-negotiation sign, risk-adversarial form incompleteness, cooperative-fairness dimensional inconsistency). Every one of those defects is fixed by editing the YAML `form` field directly, not by adding a validator that would have caught them only under fragile naming assumptions.

**2. VALID_CONSTRAINTS as a static frozenset is withdrawn permanently.**

This was an architectural error in the original review, not a sequencing issue. The frozenset approach treats a filesystem-derived registry as a spec-defined closed vocabulary. Those are different things. `VALID_MODES` and `VALID_GAME_FORMS` are closed because the spec enumerates them and they cannot grow without a spec revision. Constraint templates can be added without spec amendment (within FR-013 thresholds). Any future recommendation to reintroduce a static constraint frozenset is rejected on the same grounds.

**3. The example-key cross-validator (R-4) must exclude function-type parameters.**

Function-type parameters appear via `derived_from` artifact references, not as concrete values in example dicts. Checking their names against example keys generates false positives for every template with function-type parameters. The validator checks only scalar and integer parameters. This scoping is non-negotiable as an implementation constraint, not a design preference.

**4. extra="forbid" is sequenced after YAML standardization, not before.**

Applying `model_config = ConfigDict(extra="forbid")` before R-3 standardization and the example-key validator are deployed does not catch the actual drift (nested example structure inside `dict[str, Any]`) and creates false confidence. The sequencing is R-3 → R-4 → R-10, in that order, with no shortcutting.

### Flexibility

**On optimization_direction (Dispute 1):** Schema-engineer will accept adding `optimization_direction: Literal["minimize", "maximize"] = "minimize"` as an optional field with default if the arbiter determines the documentation value outweighs the unenforceable-claim risk. The implementation condition is that the field must be paired with explicit spec language stating it is a declaration of intent, not a validated constraint, and that `validate_library_integrity()` treats any inconsistency check as a warning, not an error. Schema-engineer will not accept the field if it is deployed as a required field or as a model_validator-level constraint.

**On computed_objective / example_note (Dispute 2):** Schema-engineer prefers the `example_note` migration but will accept spec-compliance's removal-only resolution if the arbiter determines the downstream spec 014 use case does not justify the new field. The precondition for either path is that the decision is made before R-3 standardization begins, because the YAML migration target depends on it.

**On description as required vs. optional (Dispute 3):** Schema-engineer prefers required with atomic migration and will accept the optional-now path if the arbiter determines the process risk outweighs the optional-field failure mode. The condition for accepting optional is an explicit implementation plan committing to the promotion step within the same spec 013 delivery, not deferred to spec 014.

**On type system extension beyond boolean:** Schema-engineer accepts deferring `vector`/`matrix`/`enum` to a spec amendment for FR-003. This is not a philosophical objection to richer types — it is a scope discipline consistent with how `VALID_MODES` and `VALID_GAME_FORMS` are managed. When the spec amendment lands, schema-engineer will implement the extension without resistance.

**On loader architecture (single-file vs. bulk):** Schema-engineer accepts functional-architect's scoped-down R1 design: `load_objective_templates(path: Path | None = None) -> dict[str, ObjectiveTemplate]` as a discovery-and-validation function with no cardinality assertions embedded. Cardinality assertions belong in `validate_library_integrity()`. The `_objective_schema_dir()` naming convention (functional-architect's refinement) is adopted.
