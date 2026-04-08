# Schema Engineer Cross-Review of Game-Theorist Review
## Spec: 013 Objective Function Templates

**Reviewer**: schema-engineer
**Cross-reviewing**: game-theorist
**Date**: 2026-03-23

---

## Dangerous Contradictions

### DC-1: Game-form/mathematical-structure compatibility is unenforceable at the schema layer — and game-theorist's proposed fix conflates the layers

Game-theorist's primary gap finding (Executive Summary, O2, R7) is that the Pydantic model "does not enforce the structural compatibility between an objective's mathematical form and its declared game form." This frames schema validation as the right place to catch mathematical mis-assignments. That claim is dangerous for the schema layer.

The `form` field is a free-form string (`form: str` in `objectives.py` line 143). To enforce the structural correspondence game-theorist demands — e.g., that a template declaring `game_form: stackelberg` must exhibit a `J_red`/`J_blue` leader-follower split in its form string — the model would need to parse mathematical notation embedded in an unstructured string. This is not achievable with Pydantic validators without encoding brittle substring heuristics. Game-theorist's R9 ("Add a `form_complete` or `form_includes_all_terms` validator") operates on exactly this principle: extract parameter names from the `form` string and check for token presence. This approach would produce false positives on equivalent mathematical notation (e.g., `J_leader` vs `J_red`) and false negatives on trivially reformulated forms. Schema-engineer's review correctly treats `form` as opaque at the model layer and never attempts to validate its internal structure.

The genuine enforcement gap is at a different level: the mode-mapping.yml contradiction (game-theorist O1) is a YAML data inconsistency that can and should be caught by validating the mode-mapping file against the actual template `game_form` fields using a cross-file loader — precisely the kind of utility schema-engineer's R-7 would enable (`load_all_objective_templates()` feeding a cross-reference check). Game-theorist identifies the contradiction correctly but proposes fixing the wrong artifact (the mapping file) when the deeper fix is a cross-file validator that would catch any future drift automatically.

### DC-2: Game-theorist's sign convention recommendations (R1) would break existing validation if applied without schema-layer changes

Game-theorist's R1 recommends changing `budget-constrained` from `J = quality - beta * agent_cost` to `J = -quality + beta * agent_cost`. This is mathematically sound. However, game-theorist's R6 separately recommends adding an `optimization_direction: Literal["minimize", "maximize"]` field to the ObjectiveTemplate model. These two recommendations are presented as independent, but they are co-dependent in a dangerous way: if R1 is applied first (flipping form signs), all seven affected templates become inconsistent with R6's proposed default of `"minimize"` until R6 is implemented. Applied in isolation, R1 creates a window where the `example` dict values (e.g., `{quality: 100, beta: 0.5, agent_cost: 20}`) are disconnected from a negated form in a way that no current validator catches — and schema-engineer's M-4/R-4 (cross-validating example keys against parameter names) would not help because the mismatch is semantic, not structural.

Schema-engineer's review does not recommend adding an `optimization_direction` field at all, because the optimization direction is a property of the mathematical form's sign convention, not an independent schema field. Having both a `form` string and an `optimization_direction` field creates a redundant and potentially contradictory pair: `J = quality - beta * cost` with `optimization_direction: minimize` would produce a maximization objective despite the declared direction. Any Pydantic validator that tried to reconcile these would face the same free-string parsing problem noted in DC-1.

### DC-3: Game-theorist treats `competitive-ranking`'s endogeneity as a template defect; the schema model has no mechanism to express endogenous vs. exogenous parameters, making this recommendation unactionable

Game-theorist's O2 and R7 correctly identify that `rank_position` is endogenous (determined by the joint strategy profile) but is declared as a `derived_from: "evaluation rubric rank ordering"` function-type parameter — treating it as exogenous. The recommended fix (option a: rewrite in terms of underlying score; option b: add a `mechanism` field) both require either restructuring the template's YAML or extending the schema model.

Option b ("add a `mechanism` field to the template schema") is the more principled solution, but schema-engineer's review makes no provision for a `mechanism` field and the existing model's `ObjectiveTemplate` class (`objectives.py` lines 127–166) has no `mechanism` field. Game-theorist presents this as a simple YAML authoring choice, but option b in fact requires a non-trivial model extension: defining what a mechanism field contains, whether it is validated, and how it interacts with the parametric/normal-form game form assignment. Option a is simpler but represents a semantic change to the template library that may conflict with the spec's FR-003 requirement that function-type parameters bridge deliberation artifacts. If rank is no longer a function-type parameter (because we replace it with an underlying score), the artifact linkage game-theorist is partially correct about ("rank is endogenous") is replaced by a new problem: the underlying score is not an artifact either — it is also computed from the strategy profile.

### DC-4: Game-theorist's R9 (form-completeness validator) is in direct tension with schema-engineer's R-10 (extra="forbid") and would require a new unstructured-string parser to work at all

Game-theorist's R9 proposes detecting when parameters define terms not present in the `form` string. Schema-engineer's R-10 proposes `model_config = ConfigDict(extra="forbid")` across all models to reject unexpected YAML keys. These two recommendations are not directly contradictory, but they address adjacent problems in incompatible ways.

R9 requires parsing the `form` field's string content to extract mathematical tokens. This is inherently fragile: `false_positive_penalty` appears in a parameter name but the form may write it as `fp_penalty`, `false_pos_penalty`, or a positional subscript. Schema-engineer's review does not propose any string-parsing logic because it correctly identifies `form: str` as semantically opaque at the Pydantic layer. Adding R9 would introduce a heuristic token-matching function with no clear specification of what constitutes a "match" — precisely the kind of brittle validator that R-10's strict-mode approach avoids. The right fix for the `risk-adversarial` incompleteness game-theorist identifies in O3 is to correct the YAML `form` field directly (as R3 recommends), not to add a validator that would catch it only if the parameter name happens to appear verbatim in the form string.

---

## Tensions

### T-1: Scope of "missing" items — game-theorist wants seven new templates; schema-engineer wants zero new templates and better validation of existing ones

Game-theorist's Missed Opportunities section (M1–M7) recommends adding seven new templates or constraint templates: Nash bargaining solution, potential game form, epsilon-constraint, Kalai-Smorodinsky, Bayesian game, incentive-compatibility constraint, and regret-minimization. Schema-engineer's Missed Opportunities are entirely about improving the validation model for the 21 existing templates: uniqueness enforcement, constraint reference validation, example standardization, RangeSpec, loader utilities.

These are not contradictory but they have a sequencing tension: schema-engineer's R-2 (VALID_CONSTRAINTS frozenset) would immediately block adding game-theorist's proposed `incentive-compatibility` constraint template unless the frozenset is updated simultaneously. If both reviewers' recommendations were applied, the VALID_CONSTRAINTS set would need to be extended to include any new constraint names, making it a maintenance burden rather than a stable closed set. The current design treats VALID_CONSTRAINTS as an enumeration of known-good values — game-theorist's expansions work against the closed-set discipline schema-engineer proposes.

### T-2: Dimensional inconsistency (game-theorist M8) vs. structural opaqueness of the form field (schema-engineer throughout)

Game-theorist's M8 identifies a genuine problem: `cooperative-fairness` mixes allocation units with allocation-squared units in a single objective. The recommended fixes (coefficient of variation, Gini coefficient, normalized variance) are mathematically sound. But schema-engineer's review consistently treats the `form` field as an unstructured string that the Pydantic model does not inspect. Catching dimensional inconsistency would require dimensional analysis of the form string — which is even harder than the token-matching game-theorist proposes in R9.

This creates a tension about what layer owns dimensional correctness. Schema-engineer implicitly assigns it to the template author and the review process (like this one). Game-theorist implicitly assumes it should be machine-enforceable. Both cannot be right simultaneously without a significant investment in a form-parsing subsystem that neither review proposes building. In the absence of such a subsystem, schema-engineer's position is the only practically achievable one: dimensional correctness is a review concern, not a schema concern.

### T-3: The import path discrepancy (schema-engineer O-1) is orthogonal to all game-theorist recommendations, but game-theorist's new templates would inherit the broken import

Schema-engineer's O-1 and R-8 flag that FR-011 requires `from conversus_schemas.objectives import ...` but the actual package is `conversus.schemas.objectives`. This is a spec-vs-implementation gap that affects all consumers of the schema. Game-theorist's recommendations (R4, R5, R10) propose creating new templates and a new constraint template, but do not address how these would be loaded or imported. If the import path discrepancy is not resolved first, any consumer following FR-011 would fail to load not just the existing templates but also any new ones game-theorist proposes. Game-theorist's review is silent on this issue, treating template authoring (YAML files) and model consumption (Python imports) as independent concerns. Schema-engineer's review correctly identifies them as coupled.

### T-4: Game-theorist's `optimization_direction` field (R6) vs. schema-engineer's example-standardization requirement (R-3)

Game-theorist's R6 adds `optimization_direction: Literal["minimize", "maximize"]` to the ObjectiveTemplate model. Schema-engineer's R-3 standardizes the `example` dict to contain only parameter-name-to-value mappings, removing the nested `computed_objective` annotation that currently appears in cross-mode template examples. These recommendations have a tension: if cross-mode templates currently encode their optimization convention implicitly through the `computed_objective` annotation in the example (e.g., `computed_objective: "minimize J"`), removing that annotation (R-3) and adding a dedicated `optimization_direction` field (R6) is a net improvement. But R-3 removes information that currently serves as an informal convention marker, and R6 is the only proposed replacement. Applied independently, R-3 removes the informal marker without R6 being in place, leaving templates with no expressed optimization direction at all.

### T-5: Game-theorist's incentive-compatibility constraint (R10) vs. the empty-parameters guard (schema-engineer R-9)

Game-theorist's proposed `incentive-compatibility.yml` constraint template has an unusual parameter structure: it references `true_type_i` and `reported_type_i` as function-type parameters, but also includes `reporting_space` as a string parameter describing the set of possible reports. This is structurally valid under the current schema. However, schema-engineer's R-9 adds a guard requiring at least one parameter per template, and game-theorist's proposed constraint already satisfies that. The tension is softer here: both recommendations are independently reasonable, but game-theorist's constraint would also need a `derived_from` for its function-type parameters under schema-engineer's existing A-2 validation — and the proposed template in R10 omits `derived_from` for the `true_type` and `reported_type` parameters. Game-theorist's template as written would fail the existing `validate_parameter` validator (`objectives.py` lines 65–89), which schema-engineer correctly identifies as one of the model's strongest invariants.

---

## Safe Agreements

### SA-1: The mode-mapping.yml red-blue/GNEP contradiction must be fixed

Both reviews independently arrive at the same conclusion: the `mode-mapping.yml` declaration of `red-blue: form: gnep` conflicts with all three red-blue templates using `game_form: stackelberg`. Game-theorist's O1 and R2 identify this as a direct YAML data contradiction. Schema-engineer's review does not explicitly call out this file but does observe (A-3) that the VALID_GAME_FORMS set correctly contains `stackelberg` as a valid form. A cross-file loader of the kind schema-engineer's R-7 proposes would surface this contradiction programmatically. The fix is unambiguous: update mode-mapping.yml to declare `red-blue: form: stackelberg`. Neither reviewer disagrees on the substance; only game-theorist flags it while schema-engineer's tooling would detect it automatically.

### SA-2: The `risk-adversarial` form field is incomplete and must be corrected

Game-theorist's O3 and R3 identify that `risk-adversarial`'s declared form `J_red = -confirmed_risks; J_blue = -mitigated` omits the `false_positive_penalty` term that the template's own parameter list defines. Schema-engineer's R-4 proposes cross-validating example keys against defined parameter names, which is a weaker version of the same check. Both reviewers agree on the diagnosis — the `form` field does not faithfully represent the objective — and the fix is to correct the `form` string in the YAML template. Game-theorist gives the exact corrected form; schema-engineer's validator would catch structural mismatches between parameters and examples, providing a complementary safety net once R-4 is implemented.

### SA-3: The `VALID_CONSTRAINTS` gap is real and closing it requires a closed enumeration

Schema-engineer's M-2 and R-2 call for a `VALID_CONSTRAINTS` frozenset to validate constraint references in `ObjectiveTemplate.constraints`. Game-theorist's R10 proposes adding a new `incentive-compatibility` constraint template, which would require updating this frozenset. Both reviewers thus agree — from different angles — that the constraint namespace must be explicitly managed: schema-engineer by formalizing the current six constraints, game-theorist by demonstrating that the namespace is open to extension. The practical implication is that `VALID_CONSTRAINTS` should be maintained alongside the constraint YAML files, updated atomically whenever a new constraint is added, and enforced in the ObjectiveTemplate validator.

### SA-4: The `cooperative-fairness` dimensional inconsistency is a real defect that belongs in the YAML template, not the schema model

Game-theorist's M8 identifies the dimensional mismatch between `min_i(allocation_i)` (allocation units) and `variance(allocation)` (allocation-squared units). Schema-engineer's review correctly identifies `form` as a free-form string that the Pydantic model does not inspect for dimensional consistency. Both reviews therefore agree — implicitly — that correcting this defect requires editing the `cooperative-fairness.yml` template's `form` field (to use coefficient of variation, Gini, or normalized variance as game-theorist recommends), not adding a model validator. The fix is bounded to a single YAML file and does not require any model changes. This is a clear, uncontested correction.
