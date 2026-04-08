# Functional Architect Disputes: 013 Objective Function Templates

**Reviewer**: functional-architect
**Phase**: 4 — Cooperative Disputes
**Date**: 2026-03-23

---

## Remaining Disputes

### D1. `description` on ConstraintTemplate: Required vs. Optional

**Parties**: functional-architect (R6 revised) vs. schema-engineer (NR-2)

**The gap**: Schema-engineer revised upward to `description: str` as required, with atomic YAML migration in a single commit. Functional-architect revised downward to `description: Optional[str] = None`, with a separate follow-on promotion step. Spec-compliance (R8) also holds `Optional[str] = None`.

**Schema-engineer's argument**: The six constraint YAMLs already contain the description text in header comments, making the migration cost bounded and certain. Starting optional defers a fix that can be done atomically, and creates an asymmetry that forces spec 014's guided construction pipeline to special-case constraints that lack descriptions.

**Functional-architect's argument**: Making `description` required in the same commit as adding the field is a larger atomic unit that couples two distinct concerns — model schema change and YAML content population — into one deployment. If anything delays the YAML updates (authoring review, correctness verification of the constraint description text), the entire change is blocked. Optional-first decouples the schema change from the content migration and lets the model land immediately.

**Why this remains a real dispute**: Both approaches acknowledge the same destination (`description` will be required by the time spec 014 consumes the library). The dispute is purely about path: one commit vs. two commits. Schema-engineer's atomic-migration argument is stronger when the migration surface is small and mechanical. Functional-architect's decoupled argument is stronger when description text quality requires human review beyond header-comment verbatim extraction. The six constraint YAMLs have not been inspected for description quality in any revision — if the header comments are summary-sufficient, schema-engineer wins; if they require rewording or expansion, functional-architect wins.

**Resolution condition**: Inspect the six constraint YAML header comments. If all six contain adequate plain-language descriptions ready to promote verbatim, schema-engineer's `required` approach should be adopted. If any requires material authoring work, `Optional[str] = None` lands first.

---

### D2. Form-Completeness Validator: Warning vs. Error Severity, and Exclusion Scope

**Parties**: game-theorist (R9 revised) vs. functional-architect (NR-1 extended scope)

**The gap**: Game-theorist revised R9 to a scalar/integer-only substring validator, explicitly framed as a warning-not-error, with a naming convention requirement documented as a library authoring standard. Functional-architect's NR-1 calls for a heuristic `validate_library_integrity()` check on form strings keyed to the `optimization_direction` field — also explicitly acknowledged as imperfect. These two proposals approach the same problem from different angles and interact: game-theorist's validator checks parameter-name presence; functional-architect's checks sign-convention consistency.

**The remaining tension**: Game-theorist frames the form validator as a warning because the free-text form field resists reliable token matching. Functional-architect accepts the same fragility but characterizes it as "best-effort guard, not a proof." These positions are compatible in substance but differ in implementation implication: a Pydantic validator that emits a warning (not raising ValueError) requires a non-standard implementation pattern that Pydantic's model_validator does not natively support — validators either pass or raise. The practical choice is between a validator that raises (error) or a standalone utility function called outside the model layer (warning-equivalent).

**Why this remains a real dispute**: If the form-completeness check is placed inside a `model_validator`, it must raise or it does nothing. If it is a standalone check in `validate_library_integrity()`, it can log or return structured diagnostics rather than fail. The placement question (model_validator vs. integrity function) determines the severity framing. Game-theorist's "warning" framing implicitly requires placement outside the Pydantic model. Functional-architect's placement in `validate_library_integrity()` is consistent with game-theorist's intent but was not stated as such — functional-architect described the check as a heuristic within `validate_library_integrity()`, not as a Pydantic model_validator. These are actually compatible if stated explicitly.

**Resolution condition**: Adopt a shared position: the form-completeness check (scalar/integer parameter name substring presence) and the sign-convention heuristic (optimization_direction vs. form pattern) both live in `validate_library_integrity()` as diagnostic checks that return structured findings rather than raising exceptions. Model validators remain strict (raise on definite structural invalidity); integrity function provides advisory findings. Game-theorist's "warning" framing and functional-architect's "heuristic in integrity function" framing converge here.

---

### D3. `computed_objective` Disposition: Remove vs. Migrate to `example_note`

**Parties**: spec-compliance (R3 revised) vs. schema-engineer (NR-3)

**The gap**: Spec-compliance's revised R3 calls for outright removal of `computed_objective` from all example blocks, with the documentation value absorbed into the template's `description` field or the spec's Section 2 narrative. Schema-engineer's NR-3 calls for adding `example_note: Optional[str] = None` to `ObjectiveTemplate` as an explicit migration target, preserving the documentation value in a typed field.

**This is a genuine remaining dispute from functional-architect's perspective**: Functional-architect's revision did not directly adjudicate this because it was framed as a sequencing clarification (standardize YAML first, add validator second). But the underlying question — whether `computed_objective`-style content deserves a typed home — has a direct impact on whether the example-key cross-validator (schema-engineer R-4, now with function-type parameter exclusions) produces false positives or needs additional exclusion logic.

**Spec-compliance's argument**: FR-002's "minimal valid parameterization" language means the example block should contain parameter values only. `computed_objective` is a derived output, not a parameter. Keeping it anywhere in the machine-readable block conflates inputs and outputs.

**Schema-engineer's argument**: The information currently in `computed_objective` (e.g., "minimize J ≈ quality - 0.5 * cost") is useful for spec 014's prompt construction — it tells the pipeline what the optimization is actually trying to achieve in concrete terms, supplementing the abstract `form` field. Discarding it loses information that cannot be reliably recovered from the description field alone.

**Functional-architect's position**: `example_note: Optional[str] = None` is the correct resolution. The `description` field is the template's general-purpose explanation. `example_note` is specific to what the example parameterization demonstrates — a distinct semantic function. Spec-compliance's preference for absorbing this into `description` collapses two different concerns into one field. However, this position is held with medium confidence — if spec 014's prompt construction does not distinguish template-level description from example-specific annotation, the distinction is moot in practice.

---

## Convergence

### C1. YAML Correctness Patches Apply Immediately, Spec Amendment Sequencing for Form Changes

All four reviewers converge on a two-tier structure for mathematical corrections. Tier 1: `mode-mapping.yml` red-blue/Stackelberg fix applies immediately, no spec amendment required, no sequencing dependency. This has unanimous support (game-theorist R2, schema-engineer SA-1, functional-architect SA-1, spec-compliance NR-1). Tier 2: corrections to template `form` fields that change the mathematical expression require spec amendment first, then YAML update. Game-theorist's revised R1 and R3, spec-compliance's NR-2, and functional-architect's NR-2 all adopt this sequencing. The original functional-architect NR-2 framing ("apply YAML patches today") was too aggressive for the form-field corrections — only the mode-mapping fix is truly amendment-free. This is a material convergence from a position that was disputed across all four original reviews.

### C2. VALID_CONSTRAINTS Frozenset is Withdrawn; Runtime Integrity Checking is the Pattern

Schema-engineer's R-2 (frozenset) is withdrawn by schema-engineer itself in the revision. Game-theorist's NR3, functional-architect's R2 (ongoing), and spec-compliance's implicit endorsement of runtime checking all converge on: constraint referential integrity belongs in `validate_library_integrity()` via file-existence or loaded-dict lookup, not in a static frozenset. The distinction between spec-defined closed sets (VALID_MODES, VALID_GAME_FORMS — will not grow without spec revision) and filesystem-derived open sets (constraint names — can grow without schema changes) is now a shared architectural principle across all four reviewers.

### C3. Duplicate Parameter Name Validation Proceeds Immediately

All four reviewers endorse this without reservation. Functional-architect (R4 elevated to High), schema-engineer (R-1 maintained), spec-compliance (SA-2 confirmed), game-theorist (SA-3 endorsed). This is the strongest consensus finding in the entire process. It is a two-line model_validator addition, the failure mode is real, and implementation should not wait for any other decision.

### C4. `optimization_direction` Field: Optional with Default "minimize"

Game-theorist revised R6 to `optimization_direction: Literal["minimize", "maximize"] = "minimize"` (optional, defaulting to minimize). Functional-architect's NR-1 independently arrived at the same field structure. Spec-compliance's DC-4 objection (breaks FR-002 for existing templates without the field) is addressed by the optional-with-default design — existing templates remain valid. Schema-engineer's two-sources-of-truth concern (DC-2) is addressed by both revised positions explicitly framing the field as a documentation/machine-readability aid for spec 014, not a validator that must agree with the form string. The cross-field consistency heuristic lives in `validate_library_integrity()` (functional-architect NR-1, game-theorist R9 revised, now converged in D2 above), not in a Pydantic field_validator that would create a strict dependency between a free-text field and a typed enum. This is stable enough to implement.

### C5. Example Standardization Sequencing: YAML First, Validator Second, `extra="forbid"` Last

The sequencing chain is now agreed across all four reviewers: resolve `computed_objective` disposition (see D3) → standardize YAML example blocks → add example-key cross-validator (excluding function-type parameters) → defer `extra="forbid"` until both prior steps are complete. Schema-engineer revised R-10 to deferred. Spec-compliance's R3 provides the same sequencing. Functional-architect's R7 explicitly named the same dependency order. Game-theorist's DC-4 identified the function-type parameter exclusion that makes step 2 well-defined. The only remaining uncertainty is D3 (whether `computed_objective` becomes `example_note` or is dropped), which gates step 1.

---

## Final Position Statement

### Non-Negotiables

**1. `validate_library_integrity()` must exist as a standalone function.**
The cross-review process surfaced multiple classes of defects — cross-artifact reference validity, sign convention heuristics, mode-mapping contradictions, cardinality counts, form-completeness checks — that are all invisible to the Pydantic model layer. Embedding any of these checks inside the loader, inside individual model_validators, or inside test fixtures creates fragmented, uncallable integrity logic. The function must be a named, importable pure function callable by spec 014 independently of any test setup. This is not negotiable because spec 014's construction pipeline requires it as an entry point; a loader-only or test-only approach forecloses that.

**2. The form-completeness and sign-convention checks must live in `validate_library_integrity()`, not in Pydantic model_validators.**
Both checks are explicitly acknowledged as heuristic and imperfect. Pydantic validators raise on failure — appropriate for definite structural invalidity (duplicate parameter names, empty mode_compatibility, incoherent range types). For advisory findings where false positives are acknowledged, validators are the wrong mechanism. These checks return structured diagnostics. Model validators remain strict. This boundary is architecturally non-negotiable.

**3. The `boolean` type addition to VALID_PARAMETER_TYPES proceeds without a spec amendment.**
Schema-engineer and functional-architect both converged on `boolean` as a safe, backward-compatible, correctness-improving addition. Spec-compliance correctly identifies that the broader type extensions (`vector`, `matrix`, `enum`) require FR-003 amendment. `boolean` is distinguishable: the two affected `normalize` parameters are currently typed as `string`, and `bool("false") is True` in Python — this is an active correctness hazard for downstream consumers, not a type-vocabulary design preference. The spec amendment process is appropriate for additions that expand the vocabulary; it is disproportionate for correcting a type that is provably wrong in its current encoding. The `boolean` addition proceeds.

**4. Mode-mapping.yml fix applies before any schema work begins.**
The red-blue/Stackelberg contradiction is unambiguous, requires no schema changes, and has the highest downstream impact of any finding. It cannot be gated on any other decision. Any implementation plan that begins schema work before this one-line YAML fix is inverted in priority.

**5. NR-3 (spec policy on template additions) must be resolved before the library expands.**
`cooperative-fairness` exists without spec ratification. Game-theorist's R4 and R5 (Nash bargaining, epsilon-constraint) are proposed additions. Schema-engineer's NR-2 (incentive-compatibility constraint) is a proposed addition. Whether these additions require spec amendments is a policy question that determines whether spec-compliance validators will flag them. A non-decision here means every future library expansion triggers a spec-compliance finding. The policy must be stated before additions are made, not retroactively applied.

### Flexibility

**1. `description` on ConstraintTemplate (D1): willing to accept required-with-atomic-migration.**
The functional-architect position (Optional first) was a risk-management choice, not a principled objection to required. If schema-engineer can confirm that the six constraint YAML header comments are adequate verbatim and no authoring review is needed, the atomic required approach is the better outcome for spec 014. Functional-architect will not hold this position if the migration surface is genuinely clean.

**2. `computed_objective` handling (D3): `example_note` is the preferred resolution but removal is acceptable.**
The `example_note: Optional[str] = None` field preserves information that spec 014 may find useful. However, functional-architect acknowledges this is a medium-confidence preference. If the spec 013 owner determines that FR-002's "minimal valid parameterization" language forecloses any non-parameter content in example blocks — including in separate fields — then clean removal is the right outcome. The functional-architect will not block progress on example standardization over this question.

**3. Form-completeness validator scope (D2): game-theorist's scalar/integer exclusion criterion is accepted.**
The functional-architect's NR-1 heuristic did not specify parameter type exclusions explicitly. Game-theorist's revised R9 (scalar/integer parameters only, function-type excluded) is the correct scoping. Functional-architect adopts this as the implementation criterion for the integrity function's form-completeness check. The warning-vs-error framing is resolved by placement in `validate_library_integrity()` rather than in a model_validator — both reviewers' intent is preserved.

**4. Nash bargaining and epsilon-constraint additions (game-theorist R4, R5): sequencing deference is complete.**
Functional-architect's type system extension work (R3, `boolean` first, `vector`/`matrix`/`enum` via spec amendment) is the prerequisite. Game-theorist's sequencing of R4 and R5 behind type system readiness is accepted without qualification. Functional-architect will not advocate for adding these templates before the type system supports their parameter structures.

**5. FR-011 spec amendment path: functional-architect's earlier overstatement is withdrawn.**
The functional-architect revision acknowledged that the `conversus.schemas` vs. `conversus.objectives` path deviation is a real compliance item, not "spec noise." The spec amendment to FR-011 is the correct resolution, not a compatibility alias, and not dismissal. Functional-architect will support the spec amendment as the necessary documentation step even if the runtime impact is low for an unreleased library.
