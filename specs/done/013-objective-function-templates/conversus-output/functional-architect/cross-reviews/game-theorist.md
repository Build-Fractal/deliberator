# Functional Architect Cross-Review of Game-Theorist Review
# Spec 013 — Objective Function Templates

**Cross-reviewer**: functional-architect
**Reviewing**: game-theorist's review
**Date**: 2026-03-23

---

## Overview

The game-theorist review is technically rigorous where it focuses: sign convention bugs, mode-mapping contradictions, and equilibrium-structural issues are all correctly identified and well-evidenced. The review is strongest on mathematical correctness and weakest on implementation architecture — it largely treats objectives.py as a passive validation artifact rather than the active schema boundary it is. Where the two reviews overlap, they mostly converge on the same surface bugs via different routes; where they diverge, the nature of the disagreement is substantive and worth resolving before spec 014 begins.

---

## Dangerous Contradictions

### DC1. game-theorist R6 (add `optimization_direction` field) conflicts with functional-architect O3 (form as string is already insufficient)

The game-theorist recommends adding `optimization_direction: Literal["minimize", "maximize"]` to `ObjectiveTemplate` as the canonical fix for the sign convention inconsistency (R6, citing O4). The functional-architect's O3 acknowledges the `form` field is a plain string that is not machine-parseable, and notes this dependency explicitly: "spec 014 will eventually need to map parameter names to positions in the mathematical expression."

These two recommendations are in tension that could become a contradiction. If `optimization_direction` is added as a scalar field, it creates a second source of truth about the objective's mathematical behavior alongside the `form` string. A template could declare `optimization_direction: minimize` while its `form` uses the maximization convention (`J = quality - beta * cost`) — exactly the inconsistency the field is meant to fix, now formalized as a cross-field validation problem instead of resolved. The functional-architect's M2 (parameter type system) and R8 (typed range) establish the pattern: when the schema cannot validate a field's semantics, the field should be typed more precisely, not annotated with a parallel field. Adding `optimization_direction` without simultaneously making `form` machine-parseable re-introduces the drift risk at a higher level.

**Resolution needed**: Before adding `optimization_direction`, the teams must agree on whether `form` will remain a human-readable string (in which case `optimization_direction` is the only enforcement mechanism, and validator R9 is essential) or eventually become a structured expression (in which case the direction is derivable). If string for v1, add both `optimization_direction` and game-theorist's R9 (`form_complete` validator) together. Implementing one without the other leaves the gap open.

### DC2. game-theorist R4 (add Nash bargaining template) conflicts with functional-architect M2 (type system cannot support it)

The game-theorist recommends creating `cooperative-nash-bargaining.yml` with form `J = -prod_i(utility_i - disagreement_i)` (R4, citing M1). The proposed template would require `utility` and `disagreement` parameters of type `function`. This is fine. But the Nash product involves a product over agents (`prod_i`), and the `utility_i` and `disagreement_i` notation implies per-agent indexing — the parameter is a vector-valued function, not a scalar function.

Under the current type system (functional-architect M2), `prod_i(utility_i - disagreement_i)` cannot be represented: `utility` would be declared as type `function`, but the cardinality (one value per agent) is not expressible. A downstream consumer parsing the `form` string to extract parameter names would find `utility_i` and `disagreement_i` as tokens, not `utility` as defined in the parameters list — a name mismatch the functional-architect R9 (game-theorist) / M6 (functional-architect) validators would flag as a gap but cannot resolve. Adding the template before extending the type system instantiates the exact anti-pattern the functional-architect review warns against: template structure that the schema layer cannot validate.

**Resolution needed**: Extend the parameter type system (functional-architect R3) before or simultaneously with adding Nash bargaining and other game-theoretic templates (game-theorist R4, M4). The Nash bargaining template is correct game theory but premature schema design given the current type system state.

### DC3. game-theorist O2 (rank is endogenous, rewrite objective in terms of score) conflicts with functional-architect A4 (game_form-to-mode correspondence is correct)

The game-theorist's O2 identifies a conceptual circularity in `competitive-ranking`: rank is used as an input to the objective but is itself an outcome of the game, and recommends rewriting as `J = -score` with rank derived post-hoc (R7). The functional-architect's A4 affirms that competitive templates correctly use normal-form game assignments and treats the template library as structurally sound.

This is a genuine disagreement about whether `competitive-ranking.yml` is correct as filed. The functional-architect's A4 is based on game_form assignment (normal-form for simultaneous selection), not on the internal consistency of the objective's parameter structure. The game-theorist is pointing at a deeper problem: the `rank_position` parameter's `derived_from: "evaluation rubric rank ordering"` means the ranking rule is treated as exogenous mechanism input, but rank is jointly determined by all agents' strategies, making it endogenous. The functional-architect's O1 (constraint references as bare strings) and M6 (example field unvalidated) are both downstream manifestations of the same root issue: the schema layer does not validate relationships between parameter values and the game's joint outcome structure. A4's affirmation of correctness is therefore too broad — it is correct at the game_form level but misses the intra-template structural problem O2 identifies.

**Resolution needed**: The functional-architect should not affirm `competitive-ranking` as correct without addressing O2. R7 (rewrite as `J = -score`) is the simpler and more correct fix. If adopted, the functional-architect's R7 (standardize example field) would also need updating to reflect the revised parameter structure.

### DC4. game-theorist M9 (boundary-negotiation sign reversal is a bug) vs. functional-architect O3 (form is not machine-parseable — cannot detect sign bugs)

The game-theorist identifies a specific sign error in `boundary-negotiation.yml`: `J = -boundary_violations + sigma * clarity` under minimization would maximize violations rather than minimize them (M9, R1). The functional-architect's O3 acknowledges that `form` is a plain string and that "the assumption that `form` as a string is the long-term representation should be explicit." The functional-architect review does not identify the sign bug.

The reason is architectural: the functional-architect review evaluates whether the schema layer can detect sign convention problems, and correctly concludes it cannot. The game-theorist review evaluates the mathematical expressions themselves and catches the bug directly. This creates a procedural contradiction: the functional-architect review's R8 (type the `range` field) and M4 (duplicate parameter names) aim to make the schema layer enforce more invariants, but the most critical invariant — sign convention consistency — is invisible to any purely structural validator on a free-text `form` field.

**Resolution needed**: game-theorist R1 (fix sign conventions, CRITICAL) should be applied immediately as a YAML patch. It does not require schema layer changes. The functional-architect's O3 and game-theorist's R6 collectively explain why the schema layer alone cannot prevent recurrence — both R6 (optimization_direction) and a structured form representation are needed for durable enforcement.

---

## Tensions

### T1. game-theorist M6 (add incentive-compatibility constraint template) vs. functional-architect M5 (empty mode_compatibility is silently accepted)

The game-theorist recommends adding an `incentive-compatibility` constraint template with `mode_compatibility: [cooperative, prisoners-dilemma]` (R10, citing M6). The functional-architect recommends adding a validator that rejects templates with empty `mode_compatibility` (M5, R5). These are not contradictory — the incentive-compatibility template would have a non-empty mode list — but they reveal a sequencing tension: the functional-architect's M5 validator should be added before new constraint templates, because without it, a misconfigured `incentive-compatibility.yml` with an accidentally empty `mode_compatibility` would pass validation silently. The game-theorist's template recommendation implicitly assumes the schema layer is more robust than it currently is.

More broadly, the game-theorist review generates eight new template recommendations (M1-M7, R4, R5, R10) while the functional-architect review identifies that the existing template loader, reference resolver, and library integrity checker do not exist yet (M3, R1, R2). Adding templates to a library whose integrity cannot be programmatically verified trades correctness for coverage. The functional-architect's loader work (R1, R2) should gate the game-theorist's library expansion recommendations.

### T2. game-theorist R9 (form_complete validator checks parameter names appear in form string) vs. functional-architect M6 (example field unvalidated)

Both reviews identify that the `form` string is an underutilized validation surface. The game-theorist's R9 proposes checking that parameter names appear as tokens in the `form` string to catch cases like `false_positive_penalty` (O3 — defined as a parameter but absent from the declared form). The functional-architect's M6 proposes checking that parameter names appear as keys in the `example` dict.

These two recommendations are compatible and complementary but have a common failure mode: they both depend on string matching against `form`, and `form` strings use mathematical subscript notation (`J_red`, `x_{i,r}`, `utility_i`) that does not match Python identifier conventions. A parameter named `false_positive_penalty` may appear in `form` as `fp_penalty` or `fpp` without either validator catching the mismatch. The game-theorist's R9 acknowledges this implicitly ("extract parameter names from the `form` string") but does not specify the tokenization strategy. The functional-architect's M6 has the same problem for the example validator. Both recommendations are directionally correct but require a naming convention decision: parameter names in `form` strings must match the `name` field in `ParameterDefinition` exactly, with no aliasing.

**Resolution needed**: Add a naming convention requirement to the spec: every parameter name must appear verbatim in the `form` string. Then implement both R9 (game-theorist) and M6 (functional-architect) validators in tandem.

### T3. game-theorist O4 (cross-mode templates use maximization convention) vs. functional-architect A1 (templates as immutable data, not computation)

The game-theorist's O4 identifies that `budget-constrained` and `time-constrained` use `J = quality - beta * cost` (maximization convention) while mode-specific templates use `J = -benefit + penalty` (minimization convention). The recommendation is to standardize to minimization (R1). The functional-architect's A1 affirms that templates are immutable YAML artifacts validated but never mutated by the schema layer.

There is a tension in how this fix should be applied. If templates are truly immutable data (functional-architect A1), then correcting `budget-constrained.yml` and `time-constrained.yml` is a breaking change to the template data contracts. Downstream consumers that already interpret these forms under maximization would break silently. The functional-architect review notes "this is a breaking change to the template schema but the library is v1 and unreleased" (R3 note) — the same reasoning applies here. The game-theorist's R1 is correct that the fix is needed; the functional-architect's architecture adds the requirement that the fix be accompanied by a changelog entry and that the `optimization_direction` field (if added per DC1 resolution) be set to `"minimize"` on all templates simultaneously.

### T4. game-theorist A4 (red-blue templates correctly use Stackelberg) affirms what O1 contradicts in mode-mapping.yml

The game-theorist notes that `mode-mapping.yml` declares `red-blue: form: gnep` but all three red-blue templates use `game_form: stackelberg`, calling this "a direct contradiction" and recommending the mapping be updated (O1, R2). The functional-architect's A4 affirms that "red-blue uses stackelberg (leader-follower)" as correct and consistent with spec 012.

These two reviews agree on the substance — Stackelberg is correct for red-blue — but the game-theorist identifies a concrete artifact (mode-mapping.yml) that contradicts this while the functional-architect misses it. The functional-architect's M3 (no loader function) and O1 (constraint references as bare strings) are both symptoms of the same gap: the schema layer has no cross-artifact integrity check that would surface the mode-mapping.yml discrepancy programmatically. The functional-architect's R2 (`validate_library_integrity()`) would, if implemented, catch exactly this type of cross-file contradiction. The game-theorist's R2 (fix mode-mapping.yml) is the immediate patch; the functional-architect's R2 is the systemic prevention.

### T5. game-theorist M8 (cooperative-fairness dimensional inconsistency) vs. functional-architect M2 (string type cannot be validated) — scope disagreement

The game-theorist's M8 identifies that `cooperative-fairness` mixes dimensionally incompatible terms: `-min_i(allocation_i)` is in allocation units and `phi * variance(allocation)` is in allocation-squared, making `phi` scale-dependent. The fix (R8) is to use a dimensionless measure like coefficient of variation or Gini coefficient.

The functional-architect's M2 identifies that the `string` type is semantically overloaded but does not address dimensional analysis. The type extension recommended (add `vector`, `matrix`, `boolean`, `enum`) would not detect the dimensional inconsistency in the fairness template because both `min_i(allocation_i)` and `variance(allocation)` would be `function`-type parameters — the dimension mismatch is in the mathematical relationship between them, not in any individual parameter's type.

This is a scope disagreement: the game-theorist's M8 requires semantic understanding of the `form` field that no structural Pydantic validator can provide. The functional-architect's O3 (form is not machine-parseable) implicitly explains why. Both reviews are correct within their respective scopes; neither contradicts the other. But the game-theorist's M8 fix (use coefficient of variation) is a YAML-level patch that can be applied immediately without schema changes, while the functional-architect's type extension is a schema change that does not prevent the dimensional problem from recurring.

---

## Safe Agreements

### SA1. Both reviews agree the mode-mapping.yml red-blue entry is wrong and Stackelberg is correct

The game-theorist identifies the contradiction explicitly (O1, R2). The functional-architect affirms Stackelberg as correct for red-blue (A4). The fix is unambiguous: update `mode-mapping.yml` to `red-blue: form: stackelberg`. No design tradeoffs involved.

### SA2. Both reviews agree the `form` field as a free-text string is the root cause of multiple validation gaps

The game-theorist's O4 (sign convention inconsistency invisible to the parser), O3 (form incomplete for risk-adversarial), M9 (sign reversal bug), and R9 (form_complete validator) all stem from the form field being an uninterpreted string. The functional-architect's O3 names this directly: "the assumption that `form` as a string is the long-term representation should be explicit." Both reviews converge on the same architectural liability from different angles. Any long-term resolution (structured expression format, named-term decomposition) needs to be designed jointly.

### SA3. Both reviews agree that the schema layer has no cross-artifact integrity validation and this is the primary structural gap

The game-theorist's O1 (mode-mapping contradiction), O3 (form incompleteness), and the lack of a game_form-to-mathematical-form compatibility check all describe failures to validate relationships between artifacts. The functional-architect's M1 (no composability between ObjectiveTemplate and ConstraintTemplate), M3 (no loader), R1 (load_objective_templates), and R2 (validate_library_integrity) all address the same gap from the implementation side. The two reviews are describing the same elephant from different ends. The functional-architect's loader and integrity functions (R1, R2) are the prerequisite infrastructure for any cross-artifact check the game-theorist recommends.

### SA4. Both reviews agree on the priority ordering: fix existing bugs before expanding the template library

The game-theorist's CRITICAL label on R1 (sign conventions) and R2 (mode-mapping) implicitly prioritizes correctness of existing templates over new additions. The functional-architect's R1 (loader, Priority: High) and R2 (library integrity, Priority: High) similarly front-load infrastructure before coverage. The library expansion recommendations (game-theorist M1-M7, R4, R5, R10) and the type system extension (functional-architect R3) are both scoped as improvements that build on a correct foundation. Both reviews would agree that the current library has correctness bugs (sign conventions, form incompleteness, dimensional inconsistency, mode-mapping contradiction) that should be resolved before adding Nash bargaining, epsilon-constraint, or Kalai-Smorodinsky templates.

---

## Referenced Documents

| Document | Path |
|---|---|
| game-theorist review | `conversus/specs/013-objective-function-templates/conversus-output/game-theorist/review.md` |
| functional-architect review | `conversus/specs/013-objective-function-templates/conversus-output/functional-architect/review.md` |
| Pydantic models | `conversus/conversus/schemas/objectives.py` |
| Spec 013 | `conversus/specs/013-objective-function-templates/spec.md` |
| mode-mapping.yml | `conversus/schema/game-forms/mode-mapping.yml` |
| cooperative-fairness.yml | `conversus/schema/objective-functions/cooperative-fairness.yml` |
| competitive-ranking.yml | `conversus/schema/objective-functions/competitive-ranking.yml` |
| risk-adversarial.yml | `conversus/schema/objective-functions/risk-adversarial.yml` |
| budget-constrained.yml | `conversus/schema/objective-functions/budget-constrained.yml` |
| time-constrained.yml | `conversus/schema/objective-functions/time-constrained.yml` |
| boundary-negotiation.yml | `conversus/schema/objective-functions/boundary-negotiation.yml` |
