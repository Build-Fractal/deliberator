# Cross-Review: spec-compliance on game-theorist
## Spec 013 — Objective Function Template Library

**Cross-reviewer**: spec-compliance
**Reviewing**: game-theorist's review
**Date**: 2026-03-23

---

## Dangerous Contradictions

### DC-1. The boundary-negotiation sign diagnosis is inverted — the template may be correct

game-theorist (O9) concludes that `J = -boundary_violations + sigma * clarity` has "signs reversed" and recommends `J = boundary_violations - sigma * clarity`. The reasoning offered is: "minimizing `-boundary_violations` means maximizing `boundary_violations`." This is correct as stated. game-theorist then asserts the current form is wrong and the intent is to minimize violations and maximize clarity.

However, game-theorist's proposed fix `J = boundary_violations - sigma * clarity` also has a problem under minimization: minimizing `boundary_violations` is correct, but minimizing `-sigma * clarity` maximizes clarity only when sigma > 0, which is the same sign relationship game-theorist criticized in the original. Both the original form and the proposed fix have equivalent structural issues once you account for sign conventions consistently.

More critically, the spec's Section 2 entry for `boundary-negotiation` reads: `J = -boundary_violations + sigma * clarity`. The implementation matches the spec exactly. game-theorist's finding O9 and recommendation R1 for this template would change the implementation to deviate from the spec's own declared formula — this is a spec-compliance violation, not a fix. The correct remediation, if the formula is genuinely wrong, is to amend the spec first, not the implementation. spec-compliance's review did not flag this formula because it matches the spec; game-theorist's recommendation to fix it at the implementation layer without spec amendment is the wrong intervention point.

**Impact**: Accepting R1 as written for `boundary-negotiation` would introduce a spec-vs-implementation divergence that spec-compliance would then flag as a deviation.

### DC-2. The cross-mode sign convention finding directly contradicts spec-compliance's compliance call

game-theorist (O4, R1) identifies that `budget-constrained` and `time-constrained` use `J = quality - beta * cost` and `J = quality - tau * rounds_used` and characterizes this as a sign convention inconsistency that "will cause confusion or bugs." game-theorist recommends changing these to `J = -quality + beta * agent_cost`.

spec-compliance reviewed these same templates and found FR-002 MET — the forms in the implementation match the spec's Section 2 catalog exactly: `budget-constrained: J = quality - beta * agent_cost` and `time-constrained: J = quality - tau * rounds_used`. The spec does not declare a minimization-only convention; it does not include a `convention` field; and the cross-mode templates' formulas are deliberately written for maximization. game-theorist's finding treats an implicit convention as an explicit requirement and proposes a breaking change that would flip the sign on spec-mandated formulas.

spec-compliance's review explicitly verified these forms against the spec and found no deviation. The two reviews reach opposite conclusions on the same evidence. Accepting game-theorist's O4/R1 without a spec amendment would cause the implementation to fail FR-002, which requires that each template define the form as described. The spec is the authoritative source on sign convention for cross-mode templates unless it is amended.

**Impact**: If game-theorist's R1 is applied to cross-mode templates, spec-compliance's FR-002 alignment finding becomes a deviation. These cannot both be correct simultaneously.

### DC-3. game-theorist's O3 (false_positive_penalty) identifies a real gap but misattributes its severity relative to spec compliance

game-theorist (O3) flags that `risk-adversarial`'s declared form `J_red = -confirmed_risks; J_blue = -mitigated` omits the `false_positive_penalty` parameter that shapes the actual equilibrium. This is a valid mathematical observation. game-theorist treats it as a critical structural flaw affecting equilibrium analysis.

spec-compliance did not flag this gap because the spec's Section 2 entry for `risk-adversarial` reads exactly: `J_red = -confirmed_risks; J_blue = -mitigated`. The implementation's `form` field matches the spec. The `false_positive_penalty` is a parameter that modifies the objective in practice, but the spec's own formula omits it. game-theorist's R3 recommends updating the `form` field in the YAML — but the YAML correctly reflects the spec's formula. The underlying issue is that the spec's formula is incomplete, not that the implementation diverges from the spec.

This is a meaningful distinction: game-theorist correctly identifies a mathematical incompleteness, but recommends fixing the symptom (the YAML) rather than the cause (the spec formula in Section 2). A spec amendment to Section 2's `risk-adversarial` entry is the prerequisite action; only then should the YAML be updated. spec-compliance's review, which found the form field aligned with the spec, is not wrong — it is operating at the correct layer of analysis.

**Impact**: Applying R3 directly to the YAML without amending the spec creates a new spec-vs-implementation deviation on the exact field (FR-002 `form`) that spec-compliance verified as compliant.

### DC-4. game-theorist's R6 adds an `optimization_direction` field that conflicts with the Pydantic model's current spec-mandated structure

game-theorist (R6) recommends adding `optimization_direction: Literal["minimize", "maximize"]` to the `ObjectiveTemplate` Pydantic model. This is a schema change. FR-002 defines the eight required fields for `ObjectiveTemplate` exhaustively; `optimization_direction` is not among them. Adding it as a required field would mean all existing YAML templates fail validation (none include this field). Adding it as optional with a default of `"minimize"` is less disruptive but still modifies the model beyond what FR-008 specifies.

spec-compliance found FR-008 MET in its review. If `optimization_direction` were added as required, spec-compliance's FR-008 finding would immediately flip to FAILED. This is not a minor tension — it is a model-breaking change that cannot be adopted without a corresponding spec amendment to FR-002 and FR-008. game-theorist's recommendation, taken at face value, would invalidate the implementation's most clearly passing compliance requirement.

---

## Tensions

### T-1. Missing game-theoretic forms: legitimate enrichment or scope creep?

game-theorist (M1–M7) identifies seven absent templates: Nash Bargaining Solution, potential game / congestion game, epsilon-constraint method, Kalai-Smorodinsky solution, Bayesian game form, incentive-compatibility constraint, and regret-minimization. These are mathematically well-motivated and game-theorist argues compellingly for each.

spec-compliance did not flag any of these as gaps because the spec's FR-012 threshold (>= 20 templates) is met (21 exist), FR-013 requires >= 3 per mode (met), and the spec's Section 5 states "The v1 library is curated and mathematically validated (decision Q6). Automated generation is a future concern." The spec deliberately scoped v1 to its catalog.

The tension is real: game-theorist is evaluating mathematical completeness while spec-compliance evaluates spec conformance. Both are legitimate review axes. The resolution depends on which frame takes precedence. For v1 acceptance, the spec's explicit scoping to a curated library means the missing forms are out of scope — they belong in a spec 013b or future backlog item. The concern is that game-theorist's recommendations R4, R5, R10 imply creating new YAML files not listed in the spec's catalog, which would create the same kind of undocumented-addition issue that spec-compliance flagged for `cooperative-fairness` (point 6 in spec-compliance's missed opportunities). These additions would be additions rather than corrections.

### T-2. Mode-mapping.yml GNEP vs. Stackelberg contradiction: severity assessment differs

game-theorist (O1, R2) identifies that `mode-mapping.yml` declares `red-blue: form: gnep` while all three red-blue templates use `game_form: stackelberg`. game-theorist rates this as a significant structural misalignment and recommends fixing `mode-mapping.yml`. spec-compliance did not flag this contradiction independently.

The tension is in severity framing. spec-compliance's review found the individual template `game_form` fields correct against FR-002 — each red-blue template uses `stackelberg`, which is the right game form. The `mode-mapping.yml` file is a supporting artifact; whether it is a spec-required artifact or an implementation-added convenience determines whether this is a spec deviation or an internal consistency issue. If `mode-mapping.yml` is not a spec-mandated file, its contradiction with the templates is an implementation quality issue, not a compliance failure. game-theorist's framing is stronger than the spec warrants, but the underlying observation is sound: the contradiction should be fixed regardless of which review frame is applied.

### T-3. Dimensional inconsistency in cooperative-fairness: mathematical vs. compliance lenses

game-theorist (M8) flags that `cooperative-fairness` combines a maximin term (units of allocation) with a raw variance term (units of allocation-squared), making the penalty weight phi scale-dependent. game-theorist's R8 recommends replacing raw variance with coefficient of variation, Gini coefficient, or normalized variance.

spec-compliance flagged `cooperative-fairness` as an undocumented addition not in the spec's Section 2 catalog (point 6) and recommended updating the spec to include it. The dimensional inconsistency is not a compliance issue spec-compliance would independently raise, because it is a mathematical quality concern within a template that spec-compliance is already flagging as needing spec ratification.

These two findings point to the same template but through different lenses: game-theorist says "the formula is dimensionally unsound," spec-compliance says "the template isn't in the spec." The correct sequencing is: first ratify the template by adding it to the spec (spec-compliance's fix), then fix the dimensional issue in the formula (game-theorist's fix). Neither review alone gives the complete picture.

### T-4. Competitive-ranking endogeneity (O2): valid game theory, absent from spec compliance scope

game-theorist (O2) identifies that `competitive-ranking`'s use of `rank_position` as a `derived_from` parameter creates a conceptual circularity: rank is an outcome of the joint strategy profile, not an exogenous input. This is a well-posed game theory concern that has real implications for equilibrium analysis.

spec-compliance did not raise this because FR-005 requires function-type parameters to specify `derived_from` — the template does exactly that, citing "evaluation rubric rank ordering." From a compliance perspective, the template satisfies FR-005 correctly. The endogeneity problem is a semantic concern about whether the `derived_from` artifact can logically be independent of the game's outcome, which FR-005 does not address. game-theorist's finding is correct within its domain but operates outside spec-compliance's scope. Resolution would require either amending FR-005 to prohibit endogenous `derived_from` references, or adding a new requirement about exogeneity. This is a gap in the spec that neither review fully resolves.

### T-5. `click` dependency and Section 5 constraint: scope of "the library"

spec-compliance (Off-Base Assumption 1) flags that `click` is listed as a project-level dependency and Section 5 states "Must NOT depend on any library beyond pydantic and pyyaml." game-theorist does not address this at all.

The tension is not between the two reviews but between spec-compliance's finding and how the spec's Section 5 constraint should be read. The phrase "templates are pure schema" in Section 5 suggests the constraint applies to the schema library itself, not the entire `conversus` package. The linter CLI (`conversus-lint`) is a developer tool, not part of the schema package. The question of whether the Section 5 constraint applies at the package level or the module level is genuinely ambiguous and the two reviews implicitly apply different readings — spec-compliance takes the strict reading, game-theorist ignores the dependency entirely. This deserves an explicit spec clarification.

---

## Safe Agreements

### SA-1. The mode-mapping.yml red-blue/Stackelberg contradiction must be fixed

Both reviews independently arrive at the same conclusion that the red-blue templates correctly use Stackelberg while `mode-mapping.yml` incorrectly declares GNEP. game-theorist makes this finding explicitly (O1, R2). spec-compliance implicitly confirmed that the individual template `game_form` fields are correct. The contradiction in `mode-mapping.yml` is real, consensus-validated, and actionable without requiring a spec amendment — updating `mode-mapping.yml` to declare `stackelberg` for red-blue is a straightforward internal consistency fix.

### SA-2. Tests for SC-001, SC-002, SC-003 are absent and must be added

spec-compliance (Missed Opportunities 4, 5) identifies that no `tests/test_objectives.py` exists and that SC-001 through SC-003 are unverifiable in CI. game-theorist (R9) independently recommends adding a `form_complete` validator that would also require test infrastructure to validate. Both reviews implicitly agree that the current test coverage is insufficient. The absence of tests for the Pydantic models is the most straightforward structural gap that neither review disputes and that requires no spec interpretation debate to resolve.

### SA-3. The false_positive_penalty gap in risk-adversarial reflects a real incompleteness

Both reviews identify that the `risk-adversarial` template's declared form does not reflect the full objective that the `false_positive_penalty` parameter encodes. spec-compliance's review confirms the form matches the spec's own Section 2 formula, which means the incompleteness originates in the spec itself. game-theorist's R3 correctly identifies the fix (update the form to include the penalty term) even if the review layer is wrong (the spec, not the YAML, needs amending first). Both reviews effectively agree that the form is incomplete as a description of the game's actual equilibrium structure; they differ only on where the fix should be applied. The shared conclusion — that the form and the parameters must be coherent with each other — is sound and actionable.

### SA-4. The `cooperative-fairness` template needs formal ratification

spec-compliance explicitly flags `cooperative-fairness` as an undocumented addition beyond the spec's Section 2 catalog (Missed Opportunity 6). game-theorist (M8) independently identifies a dimensional inconsistency in the same template's formula. Both reviews, from independent directions, flag `cooperative-fairness` as requiring attention: spec-compliance on provenance grounds, game-theorist on mathematical grounds. The convergence confirms that this template needs both a spec amendment (to add it to the catalog) and a formula correction (to address the dimensional mismatch) before it can be considered fully accepted. No reviewer contests the template's value or purpose — only its current ratification and correctness status.
