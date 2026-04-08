# Game-Theorist Revision — 013 Objective Function Templates

**Reviewer**: game-theorist
**Revision iteration**: 1
**Date**: 2026-03-23

---

## Recommendation Dispositions

### R1. Fix sign convention inconsistency across templates (originally CRITICAL)

**Disposition**: Partially upheld, scope narrowed, sequencing clarified.

The mathematical substance is correct: `budget-constrained`, `time-constrained`, and `boundary-negotiation` have sign conventions that contradict their stated intent when interpreted under minimization. R1 remains actionable for those three specific templates.

However, spec-compliance raises a legitimate procedural objection (DC-2, DC-1 in their cross-review): the cross-mode templates' current forms match the spec's own Section 2 catalog exactly. Applying R1 to `budget-constrained` and `time-constrained` at the YAML layer, without first amending the spec, would create a spec-vs-implementation divergence — precisely the kind of deviation that spec-compliance is designed to catch. The same applies to `boundary-negotiation`.

Furthermore, spec-compliance's analysis of the boundary-negotiation sign diagnosis (DC-1) surfaces a genuine complication: the proposed corrected form `J = boundary_violations - sigma * clarity` has a symmetric structure to the original under consistent interpretation, and the argument for which is "correct" depends on whether sigma is positive — the same issue the review identified in the original. The cleaner diagnostic is that the current form is ambiguous in its minimization semantics, not that one form is obviously right and the other is obviously wrong.

**Revised action**: R1 is reclassified from a direct YAML fix to a spec amendment proposal. The correct sequence is (1) amend the spec's Section 2 catalog to declare a universal minimization convention and provide corrected forms for the affected templates, (2) update the YAML to match. The CRITICAL classification is retained but the target artifact changes from the YAML files to the spec itself.

The boundary-negotiation case specifically should be resolved in the spec amendment with explicit reasoning about the minimization semantics and the expected sign of sigma, rather than assuming one form is uniquely correct.

---

### R2. Fix the mode-mapping.yml contradiction for red-blue

**Disposition**: Upheld without modification.

All three cross-reviews agree this is the highest-priority structural fix (schema-engineer SA-1, functional-architect SA-1, spec-compliance SA-1). No reviewer disputes that the templates are correct (Stackelberg) and the mapping file is wrong (GNEP). This is the rarest kind of finding: unanimous and unambiguous. The fix — update `mode-mapping.yml` to declare `red-blue: form: stackelberg` — requires no schema changes, no spec amendment, and no sequencing dependencies. It should be applied immediately.

---

### R3. Update the risk-adversarial form to include the false_positive_penalty

**Disposition**: Upheld in substance, sequencing adjusted.

Spec-compliance's cross-review correctly identifies (DC-3) that the `risk-adversarial` YAML form matches the spec's own Section 2 formula — the incompleteness originates in the spec, not in an implementation deviation. Applying R3 to the YAML before amending the spec would create a new FR-002 deviation.

The mathematical finding stands: the `false_positive_penalty` parameter changes the game's equilibrium structure (from "always claim everything" to a precision-recall tradeoff), so omitting it from the form field is a substantive mathematical error, not a cosmetic one.

**Revised action**: The spec's Section 2 entry for `risk-adversarial` must be amended to include the complete form, and the YAML updated to match. As with R1, the sequencing runs through the spec amendment first. The corrected form `J_red = -confirmed_risks + false_positive_penalty * failed_claims; J_blue = -mitigated` remains correct.

---

### R4. Add a Nash Bargaining Solution template for cooperative mode

**Disposition**: Conditionally upheld, deferred pending type system readiness.

Functional-architect's cross-review identifies a genuine blocking dependency (DC2): the Nash product `prod_i(utility_i - disagreement_i)` requires per-agent-indexed parameters — a `list[function]` or `agent_indexed` type extension that the current four-type system (`scalar`, `function`, `string`, `integer`) cannot represent. The template as proposed in R4 would either declare `utility` as a single `function` (losing the per-agent cardinality) or as `string` (the type-system junk-drawer problem functional-architect identifies in their own review).

Schema-engineer's cross-review notes (DC-1) that adding the template before extending the type system instantiates the exact anti-pattern the functional-architect warns against.

**Revised position**: The Nash Bargaining Solution template is mathematically correct and the most important missing cooperative form. However, it should be tracked as a v1.1 addition contingent on functional-architect's R3 (type system extension) landing first. The v1 library is explicitly curated and the spec's FR-013 minimum counts are already met. This is not withdrawal of the recommendation — it is sequencing it correctly behind infrastructure readiness.

---

### R5. Add an epsilon-constraint template for multi-objective optimization

**Disposition**: Conditionally upheld, same sequencing dependency as R4.

Functional-architect's cross-review raises the same type-system objection: the epsilon-constraint template's `epsilon` parameter was proposed with `type: string`, which is precisely the junk-drawer usage functional-architect's type extension targets. If functional-architect's R3 is implemented, `epsilon` should be typed as `vector` (a vector of upper bounds on secondary objectives).

Spec-compliance correctly notes (T-1) that the spec's v1 library is explicitly scoped to its catalog and FR-012/FR-013 thresholds are already met. Adding templates not listed in the spec creates undocumented additions — the same problem spec-compliance flagged for `cooperative-fairness`.

**Revised position**: Epsilon-constraint is a legitimate addition that completes the standard scalarization toolkit. It should be proposed via a spec amendment to Section 2 (adding it to the catalog) concurrent with the type system extension. Defer to v1.1.

---

### R6. Add an explicit optimization_direction field to the ObjectiveTemplate model

**Disposition**: Upheld in intent, implementation approach refined.

This recommendation generated the most substantive cross-review disagreement. Schema-engineer argues (DC-2) that `optimization_direction` creates a second source of truth alongside `form`, making them a contradictory pair. Functional-architect argues (DC1) that adding the field without simultaneously making `form` machine-parseable re-introduces drift risk at a higher level. Spec-compliance argues (DC-4) that adding it as a required field breaks FR-002 compliance for all existing templates (none currently include the field).

All three objections have merit. However, the underlying problem they are reacting to — that templates currently have no machine-readable declaration of their optimization direction — is real and harmful. The sign convention inconsistency exists precisely because the optimization direction is implicit.

**Revised position**: Add `optimization_direction: Literal["minimize", "maximize"] = "minimize"` as an optional field with default `"minimize"`. This preserves FR-002 compliance for existing templates (they implicitly inherit `minimize`) while making the convention explicit for templates that use the maximization convention. The field's presence enables the spec 014 construction pipeline to handle templates uniformly without string-parsing the `form` field.

The co-dependency with R1 is real: R1 (sign convention fix) and R6 (optimization_direction field) should be implemented together, not independently. Once templates with maximization convention are corrected via spec amendment (R1), all templates will correctly default to `"minimize"` and the field becomes documentation for the convention rather than a divergence point.

The co-dependency with schema-engineer's R-10 (extra="forbid") is also real: adding this field to the model must precede enabling extra="forbid", otherwise existing templates without the field would fail validation during the transition window.

---

### R7. Resolve the endogeneity problem in competitive-ranking

**Disposition**: Upheld, option (a) selected.

Schema-engineer's cross-review (DC-3) correctly identifies that option (b) — adding a `mechanism` field — requires a non-trivial model extension with unresolved semantics about what the field contains and how it is validated. Functional-architect's cross-review (DC3) correctly identifies that option (a) — rewriting as `J = -score` with rank derived post-hoc — is the simpler and more correct fix.

However, both cross-reviews raise the same residual concern: if score is substituted for rank, is `score` itself exogenous? The spec's FR-005 requires function-type parameters to specify `derived_from` pointing to a deliberation artifact. The `score` would be `derived_from: "evaluation rubric scorecard"`, which is a genuine artifact produced during deliberation and is exogenous to the player's strategy in the sense that the rubric is fixed before strategies are chosen. This is meaningfully different from rank, which is jointly determined by all scores. Option (a) resolves the endogeneity problem.

**Revised action**: Rewrite `competitive-ranking.yml` to use `J = -score_i` where `score_i` is a function-type parameter with `derived_from: "evaluation rubric scorecard"`, and document that rank is a post-hoc derived outcome. No model changes required.

---

### R8. Fix the dimensional inconsistency in cooperative-fairness

**Disposition**: Upheld, implementation sequenced after spec ratification.

Spec-compliance's cross-review (T-3) identifies that `cooperative-fairness` is already flagged as an undocumented addition. The correct sequencing is to ratify the template in the spec (spec-compliance's fix) and simultaneously fix the dimensional inconsistency (game-theorist's fix). They are not independent tracks — adding a dimensionally inconsistent formula to the spec catalog creates a spec-level mathematical error. The fix (replace raw variance with coefficient of variation or Gini coefficient) is bounded to a single YAML file and does not require model changes. This remains a clear, correctly diagnosed defect.

---

### R9. Add a form_complete or form_includes_all_terms validator

**Disposition**: Substantially revised — validator must be scoped to scalar parameters only.

Schema-engineer's cross-review raises the strongest objection (DC-4): the `form` field is a free-text string with mathematical notation, and token-matching parameter names against form strings is inherently fragile — `false_positive_penalty` might appear as `fp_penalty` or a positional subscript in different valid mathematical expressions. Schema-engineer correctly identifies this as a heuristic that produces false positives and false negatives.

My own cross-review of schema-engineer identified a critical scoping issue (DC-4 in game-theorist's cross-review of schema-engineer): the validator must exclude function-type parameters from the token-presence check. Function-type parameters appear via their `derived_from` artifacts, not as literal tokens in the form expression. Including them in the check generates false positives for every template with function-type parameters.

**Revised position**: The validator should be scoped to scalar and integer parameters only, checking that every non-default scalar/integer parameter name appears as a substring in the `form` field. Function-type and string-type parameters are excluded. This still catches the `false_positive_penalty` gap (it is a scalar parameter absent from the form) without generating false positives for function-type parameters like `rank_position`. The validator is best framed as a warning, not a validation error, given the free-text form field's limitations.

The functional-architect correctly notes (DC4 in their cross-review) that this creates a naming convention dependency: parameter names must appear verbatim as substrings in the form string for the validator to function. This should be stated explicitly as a library authoring convention.

---

### R10. Add an incentive-compatibility constraint template

**Disposition**: Conditionally upheld, redesign required before implementation.

Schema-engineer's cross-review identifies (T-5) that the proposed `incentive-compatibility.yml` template as written omits `derived_from` on its function-type parameters, which means it would fail the existing `validate_parameter` validator. This is a correctness problem with the template design, not with the underlying concept.

Functional-architect's cross-review raises a deeper concern (DC-3): the parameter compatibility model that functional-architect's `validate_library_integrity()` would enforce requires that constraint template parameters be compatible with the objective templates that reference them. The incentive-compatibility constraint references `true_type` and `reported_type` — parameters that have no corresponding entries in any current objective template's parameter list. This creates a one-sided reference that the library integrity check cannot validate.

Spec-compliance notes (T-1) that adding new constraint templates requires updating the VALID_CONSTRAINTS set if schema-engineer's R-2 is adopted — creating a deployment dependency.

**Revised position**: The incentive-compatibility constraint remains the right mechanism design element to add to the library. The template design must be revised to: (1) add `derived_from` for all function-type parameters (`true_type` should be `derived_from: "agent capability assessment"`, `reported_type` should be `derived_from: "agent submitted review content"`), (2) document which objective templates are expected to reference it (cooperative-integration and territory-claiming are the primary candidates), (3) resolve the parameter compatibility question with functional-architect's constraint resolution model. Defer until that design work is completed.

---

## New Recommendations

### NR1. Establish a spec amendment protocol before applying mathematical corrections

The cross-review process surfaces a recurring pattern: game-theorist identifies a mathematical defect in a YAML file, but spec-compliance correctly notes the YAML matches the spec's own formula, meaning the fix should target the spec first. This is not a dispute about whether the math is wrong — it is a protocol question about the correct artifact chain for corrections.

A spec amendment protocol should be explicitly established for spec 013: any correction to a template's `form` field that would change the mathematical expression (not merely format or wording) requires a spec amendment to Section 2 before the YAML is updated. Sign convention corrections (R1), form completeness corrections (R3), and dimensional inconsistency corrections (R8) all fall under this protocol. This avoids creating FR-002 deviations during the correction process and ensures that spec-compliance validators continue to function as intended.

This recommendation has no direct technical artifact — it is a process recommendation for how the spec 013 defects identified across all reviews should be tracked and resolved.

---

### NR2. Add game_form_compatibility to ConstraintTemplate as a low-cost extensibility hook

My cross-review of spec-compliance identified (T-4) that distinguishing GNEP-compatible constraints from Stackelberg-compatible constraints would enable spec 014's guided construction pipeline to select appropriate constraints by game form. Spec-compliance's existing recommendation to add an optional `description` field to ConstraintTemplate is a useful but insufficient extension.

Adding an optional `game_form_compatibility: list[str]` field to `ConstraintTemplate` — with no validation against VALID_GAME_FORMS for now, just presence — gives template authors a way to document which game forms a constraint is appropriate for. For example, the `budget` constraint would declare `game_form_compatibility: [gnep, parametric]`, while a future Stackelberg-specific constraint would declare `game_form_compatibility: [stackelberg]`. This field costs nothing to add and eliminates a permanent information gap before spec 014 consumes the constraint library.

---

### NR3. Gate schema-engineer's VALID_CONSTRAINTS approach on a file-existence check, not a closed frozenset

My cross-review of schema-engineer identified (DC-2) that a closed frozenset blocks library growth by requiring a code change for every new constraint template. The correct mechanism for referential integrity is a file-existence check: verify that every constraint name in `ObjectiveTemplate.constraints` resolves to a file in the `constraints/` directory.

This is not a pure theoretical preference — it is a practical consequence of the reviews' collective recommendations. If even one of R10 (incentive-compatibility), NR2 (game_form_compatibility), or the spec-compliance recommendation to ratify `cooperative-fairness` results in a new or renamed constraint template, the frozenset creates a deployment coupling. A file-existence check at validation time is referentially complete, handles library growth transparently, and satisfies schema-engineer's core goal of catching dangling constraint references without the maintenance burden. The file-existence check should be implemented in the `validate_library_integrity()` function (functional-architect's R2) rather than as a static frozenset in the Pydantic model.

---

## Position Summary

The core mathematical findings from the original review hold under cross-review scrutiny: the mode-mapping.yml contradiction (O1), the `false_positive_penalty` gap in `risk-adversarial` (O3), the sign convention inconsistency across cross-mode templates (O4), the endogeneity problem in `competitive-ranking` (O2), and the dimensional inconsistency in `cooperative-fairness` (M8) are all real defects that no cross-reviewer disputed on mathematical grounds.

The primary correction to my original position is procedural: several recommendations that I framed as direct YAML fixes should first run through a spec amendment — because the YAML currently matches the spec, and correcting the YAML without correcting the spec creates FR-002 deviations that spec-compliance would correctly flag. This is a sequencing discipline, not a retreat from the mathematical substance.

On library expansion (R4, R5, R10), the cross-reviews correctly identify that the current type system cannot represent the parameter structures required by Nash bargaining and epsilon-constraint templates, and that new constraint templates have unresolved parameter-compatibility dependencies. These additions remain mathematically correct and important, but they belong in a v1.1 track gated on functional-architect's type system extension work.

On R6 (optimization_direction field), the cross-reviews surface legitimate concerns about creating a redundant source of truth alongside the free-text `form` field. The revised approach — optional field with default `"minimize"` — addresses the FR-002 compliance concern while preserving the field's value as an explicit machine-readable convention declaration.

On R9 (form_complete validator), the revised scope — scalar/integer parameters only, warning-not-error, verbatim substring matching with explicit naming convention documentation — addresses the false-positive problem with function-type parameters while preserving the validator's value for catching the `false_positive_penalty`-class of gap.

The three new recommendations address gaps that emerged from the cross-review interactions themselves: the need for an explicit spec amendment protocol (NR1), a low-cost game_form_compatibility field on ConstraintTemplate (NR2), and a file-existence-based alternative to the closed VALID_CONSTRAINTS frozenset that avoids blocking library growth (NR3).

The overall verdict is unchanged: the mathematical framework is sound at the structural level, but has several correctness defects in specific template forms and a high-priority cross-artifact contradiction in mode-mapping.yml. The library is not ready for spec 014 consumption until the mode-mapping contradiction (R2) and the form completeness issues (R3, R1 for boundary-negotiation) are resolved at the spec level.
