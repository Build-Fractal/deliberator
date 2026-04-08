# Game-Theorist Cross-Review of Functional-Architect's Review
## Target: 013 Objective Function Templates

**Cross-Reviewer**: game-theorist
**Reviewing**: functional-architect's review (`conversus-output/functional-architect/review.md`)
**Own Review**: `conversus-output/game-theorist/review.md`
**Date**: 2026-03-23

---

## Dangerous Contradictions

### DC-1. Sign Convention Inconsistency Is an Equilibrium Correctness Problem, Not a Formatting Issue

Functional-architect's review does not mention the sign convention inconsistency across templates at all. The review treats the `form` field primarily as a documentation concern — noting in M6 (example field validation) and O3 (form-as-string limitation) that the field is hard to machine-parse, and in M9 (YAML example inconsistency) that nested examples violate Single Source of Truth. Nowhere does functional-architect flag that `budget-constrained` and `time-constrained` use a maximization convention (`J = quality - beta * cost`) while all mode-specific templates use a minimization convention (`J = -benefit + penalty`).

This omission is dangerous because the functional-architect's R1 recommendation — add `load_objective_templates()` — would succeed silently for both conventions. A loader that passes Pydantic validation and returns a `dict[str, ObjectiveTemplate]` treats sign-inconsistent templates identically to sign-consistent ones. The guided construction pipeline (spec 014) would then receive templates with contradictory optimization directions and produce inverse behavior (maximizing cost, minimizing quality) for templates with the wrong convention. This is not a schema gap; it is a correctness failure that functional-architect's proposed loader and validation functions would not detect.

Game-theorist's R1 and R6 directly address this: R1 calls for a global sign convention fix across four specific templates, R6 proposes adding `optimization_direction: Literal["minimize", "maximize"]` to the Pydantic model. Functional-architect's R2 (`validate_library_integrity()`) validates cross-references and mode coverage counts but does not validate mathematical consistency. The two reviews are not complementary here — functional-architect's proposed validation infrastructure would pass a structurally broken library.

**Resolution needed**: The `ObjectiveTemplate` model must include an `optimization_direction` field (game-theorist R6), and the `validate_library_integrity()` function (functional-architect R2) must cross-check all forms against the declared direction. Neither review alone is sufficient.

---

### DC-2. The Type System Critique Conflicts Directly with Game-Theorist's Mathematical Recommendations

Functional-architect's M2 and R3 argue that `string` is a "type-theoretic junk drawer" and recommend extending `VALID_PARAMETER_TYPES` to include `vector`, `matrix`, `boolean`, and `enum`. This is structurally correct. However, game-theorist's R4 and R5 propose new templates (`cooperative-nash-bargaining`, `epsilon-constraint`) whose parameter definitions do not fit cleanly into the extended type system:

- Nash Bargaining Solution requires `utility_i - disagreement_i` where both terms are derived from deliberation artifacts — modeled as `function` type, but the product `prod_i(...)` requires a variable-length list of function-typed parameters (one per agent), which is not representable as a single `function` or `vector` entry.
- The epsilon-constraint template's `epsilon` parameter is described as "upper bounds for secondary objectives" and typed as `string` in game-theorist's R5 YAML snippet — exactly the "junk drawer" use of `string` that functional-architect's M2 targets.

If functional-architect's R3 is implemented first (extending the type system and making `string` invalid for structured data), game-theorist's R5 template as written would fail Pydantic validation on the `epsilon` parameter. The two recommendations are in direct conflict over what the type system should accept and what new templates should declare.

**Resolution needed**: Game-theorist's new template proposals must be revised to use the extended type system. The `epsilon` parameter should be typed as `vector` (a vector of bounds), not `string`. The Nash bargaining utility list requires either a `list[function]` type extension or a separate `agent_indexed` flag on function-type parameters. Implementing functional-architect's R3 without updating game-theorist's R5 would break the new template at validation.

---

### DC-3. Constraint References as Bare Strings: Architecture-Level Disagreement Masked as Omission

Functional-architect's M1 and O1 identify `ObjectiveTemplate.constraints: list[str]` as an unresolved reference pattern and call it "an architectural assumption that downstream can handle unresolved references, which contradicts the Templating Engines Over Inference principle (Constitution VIII)." The proposed fix is a `ComposedObjective` model or `resolve_constraints()` function that validates all references at load time.

Game-theorist's review does not address the constraints reference pattern at all. However, game-theorist's R10 proposes adding an `incentive-compatibility` constraint template and cross-referencing it from prisoners-dilemma templates — which would add one more unresolved bare string reference to the existing list. If functional-architect's O1 is correct that bare string references are architecturally broken, then game-theorist's R10 (implemented naively) makes the architecture worse.

More significantly, functional-architect's proposed `validate_library_integrity()` (R2) checks that every constraint name in every `ObjectiveTemplate.constraints` list exists in the constraint dict. Game-theorist's R10's `incentive-compatibility` template references agent `true_type` and `reporting_space` parameters that have no corresponding objective-side parameters — making parameter compatibility validation (functional-architect M1, third bullet) fail for any objective that references it. The incentive-compatibility constraint template, as specified, is not compatible with the resolution mechanism functional-architect is proposing.

**Resolution needed**: Game-theorist's R10 must define which objective templates reference `incentive-compatibility` and verify parameter compatibility before the constraint template is added to the library. Alternatively, functional-architect's R2 must explicitly carve out "mechanism design constraints" as a separate category that does not require parameter-level compatibility. The two reviews cannot both be implemented without one overriding the other on this point.

---

### DC-4. The `form` Field: Transparency vs. Parseability — Irreconcilable Without a Schema Decision

Functional-architect's O3 describes the `form` field as "human-readable but not machine-parseable" and correctly notes that spec 014 will eventually need to map parameter names to positions in the mathematical expression. The assessment is that this is "not necessarily wrong for v1, but the assumption that `form` as a string is the long-term representation should be explicit." Functional-architect treats this as a documented limitation, not a blocking issue.

Game-theorist's R3 takes a harder position: the `risk-adversarial` form field is affirmatively wrong (it omits `false_positive_penalty` from the declared form), and game-theorist's R9 recommends a cross-field validator that checks whether parameter names appear as tokens in the form string. R9 is premised on the form string being parseable enough to extract parameter name tokens — treating the form as a restricted expression language, not free text.

These positions create a contradiction: functional-architect accepts the `form` field as documentary, while game-theorist's R9 proposes to enforce it as a constrained machine-readable artifact. If functional-architect's O3 concern is valid (form is inherently unparseable long-term), then game-theorist's R9 token-extraction approach is fragile and will break on any form using Greek letters, function notation, or subscripted variables. If game-theorist's R9 is implemented, forms must be constrained to use parameter names as literal tokens — which contradicts the mathematical notation used throughout the library (e.g., `J_red = -confirmed_risks + false_positive_penalty * failed_claims` works, but `J = (1/2) x^T Q x + p^T x` does not, since `x`, `Q`, and `p` are parameter names but `x^T` is not a simple token match).

**Resolution needed**: A decision on form field semantics must precede either recommendation. Either (a) forms are free text and game-theorist's R9 is dropped in favor of functional-architect's O3 documentary treatment, or (b) a restricted expression grammar is defined and both the existing templates and game-theorist's new template proposals must conform to it.

---

## Tensions

### T-1. Loader Function Scope: Minimal vs. Comprehensive

Functional-architect's R1 specifies a loader that validates library completeness at load time: "at least 20 templates, every mode has 3+ templates, 5+ cross-mode templates." This bundles discovery, validation, and completeness checking into a single function. Game-theorist's review does not address loader design but implicitly assumes that new templates (Nash bargaining, epsilon-constraint, incentive-compatibility, Kalai-Smorodinsky) will be added to the library — which would change the completeness counts that functional-architect's loader enforces.

The tension is about coupling: functional-architect's loader hardcodes library size invariants into the loading function, which means that adding game-theorist's proposed templates requires updating the loader's hardcoded thresholds. A cleaner separation would put completeness thresholds in `validate_library_integrity()` (functional-architect R2) and keep the loader purely as a discovery and validation function. As specified, functional-architect's R1 creates a maintenance burden whenever the library grows.

### T-2. Mathematical Rigor vs. Practical Completeness in Template Additions

Game-theorist's M1 (Nash bargaining), M4 (Kalai-Smorodinsky), M5 (Bayesian games), M6 (incentive compatibility), M7 (regret minimization) all identify standard game-theoretic forms missing from the library. These are mathematically well-motivated. Functional-architect's review takes no position on library content completeness — it treats the existing 21 templates as given and focuses on schema validity.

The tension is one of scope prioritization. Functional-architect's recommendations (R1-R10) are exclusively schema-layer improvements that would benefit any library content. Game-theorist's additions would expand the library but add templates that may be incompatible with the current schema (as DC-2 shows). Implementing game-theorist's new templates before functional-architect's schema improvements risks adding mathematically correct but schema-invalid content; implementing functional-architect's schema improvements first may require game-theorist's new templates to be redesigned.

### T-3. Example Field: Validation Depth

Functional-architect's M6 and R7 call for validating that every parameter without a default appears as a key in the example dict, and that example values for typed parameters satisfy range constraints. This is schema-layer validation.

Game-theorist's M9 (YAML example inconsistency between flat and nested forms) is related but different: the issue is not whether examples are valid, but whether they are consistently structured. Game-theorist's review implies the flat form is correct (consistent with the spec's "minimal valid parameterization" language) but does not explicitly recommend a standardization fix.

These are compatible but ordered: functional-architect's R7 standardization recommendation must precede example field validation, because validating examples against parameter names only works if all examples use the flat parameter-values format. The reviews agree on the problem but do not agree on which fix is prerequisite to the other. Functional-architect's R7 actually addresses both issues (standardize + validate), making game-theorist's structural observation redundant — but game-theorist's observation provides the motivating rationale for why standardization is needed in the first place.

### T-4. The `boundary-negotiation` Sign Error: Scope of Fix

Game-theorist's M9 identifies a sign reversal bug in `boundary-negotiation.yml`: the form `J = -boundary_violations + sigma * clarity` incorrectly maximizes violations under the minimization convention. Game-theorist's R1 recommends the corrected form `J = boundary_violations - sigma * clarity`.

Functional-architect's review never flags this error, but functional-architect's R9 (game-theorist's equivalent: add a form completeness validator) would not catch it either — a sign error is a semantic mistake, not a missing-parameter problem. Functional-architect's proposed `validate_library_integrity()` (R2) also would not catch it.

The tension is that game-theorist found a concrete correctness bug that functional-architect's entire validation infrastructure would miss. Functional-architect's approach to validation is structural (references resolve, mode counts are met, parameter names are unique), while game-theorist's approach is semantic (mathematical forms are self-consistent). Both are necessary, but they are not substitutes for each other. The bug in `boundary-negotiation` demonstrates that structural validation alone is insufficient for a mathematically curated library.

### T-5. ConstraintTemplate Description Field: Missing vs. Unnecessary

Functional-architect's M7 and R6 call for adding a `description: str` field to ConstraintTemplate, citing Constitution XVI (Mathematical Transparency). The functional architect's argument is that the guided construction pipeline needs programmatic access to constraint descriptions for user-facing prompts.

Game-theorist's review implicitly takes the opposite position: the constraint templates referenced in M6 (incentive-compatibility) and R10 include `description` as an inline field on individual parameters, not on the constraint template as a whole. Game-theorist's proposed `incentive-compatibility.yml` snippet in R10 omits a top-level `description` field entirely.

This is a tension rather than a contradiction because game-theorist's R10 is a new template proposal rather than a position statement on the existing schema. But if functional-architect's R6 is implemented (adding `description` as a required field to ConstraintTemplate), game-theorist's R10 template proposal as written would fail validation. The reviews implicitly disagree about what constraint templates must document.

---

## Safe Agreements

### SA-1. GNEP Is the Correct Game Form for Cooperative Templates

Both reviews agree that cooperative templates correctly use GNEP with coupled constraints. Functional-architect's A4 ("cooperative templates use GNEP (shared constraints)") and game-theorist's A1 ("the GNEP form explicitly models exactly this structure: `J_i(x_i, x_{-i})` with coupled constraints") reach the same conclusion from different directions — functional-architect from schema consistency with mode-mapping.yml, game-theorist from the mathematical structure of shared constraints. This is firm ground: the cooperative-GNEP correspondence is correct and does not require remediation.

### SA-2. The mode-mapping.yml Red-Blue Contradiction Must Be Fixed

Functional-architect's A4 notes that red-blue templates use Stackelberg form and that this is "internally consistent with the mode-mapping schema from spec 012." This is precisely wrong — game-theorist's O1 demonstrates that mode-mapping.yml actually declares `red-blue: form: gnep`, which directly contradicts the Stackelberg assignment in all three red-blue templates. Functional-architect misread the alignment here.

However, both reviews agree on the correct answer: the templates are right and the mapping file is wrong. Functional-architect's A4 (though misstating the current mapping) and game-theorist's O1 and R2 converge on the same fix: mode-mapping.yml should declare `red-blue: form: stackelberg`. This correction is unambiguous and non-controversial.

### SA-3. Duplicate Parameter Name Validation and Empty mode_compatibility Are Clear Gaps

Functional-architect's M4 (duplicate parameter names) and M5 (empty mode_compatibility) identify two model_validator additions that are straightforwardly correct. Game-theorist's review does not address these gaps but raises no objection to them either. Both represent dead or non-deterministic infrastructure that the Pydantic model should prevent. These are additive fixes with no interaction with game-theorist's mathematical recommendations and can be implemented immediately without resolving any of the tensions or contradictions above.

### SA-4. The false_positive_penalty Form Incompleteness Is a Real Bug

Game-theorist's O3 finds that `risk-adversarial.yml` declares `form: "J_red = -confirmed_risks; J_blue = -mitigated"` while a `false_positive_penalty` parameter exists that modifies `J_red` but is absent from the declared form. Functional-architect's O3 (form field as free text) acknowledges that the form cannot be machine-validated — but does not dispute that the form field should accurately represent the actual objective. Functional-architect's M6 (example field validation) implies that examples should correspond to declared parameters; the same principle applies to the form field. Both reviews, approached from different angles, support the fix in game-theorist's R3: the `risk-adversarial` form should be updated to `J_red = -confirmed_risks + false_positive_penalty * failed_claims`.
