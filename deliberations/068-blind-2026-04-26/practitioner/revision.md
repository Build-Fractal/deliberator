# Practitioner Revision — Constitution v2.3.2 (blind), Iteration 1

**Reviewer**: practitioner (developer ergonomics lens)
**Phase**: Phase 3 revision
**Inputs**: original review, two cross-reviews of me, two cross-reviews I wrote of skeptic-mathematical and skeptic-cross-principle, target constitution v2.3.2-blind.

The cross-reviews surfaced three substantive corrections to my original position (template-versioning, solver-substitution wording, V-emission for user audit) and one structural fork I underweighted (the "fold-into-VII vs split-XVI vs collapse-and-keep" decision is more consequential than I framed it). My revision keeps the operational-language core of my original recommendations but accepts skeptic-mathematical's template-version inclusion in the cache key, accepts skeptic-cross-principle's solver-substitution softening, and adds an explicit V-emission requirement so transparency is auditable in run output, not just enforceable in CI.

---

### Recommendation Dispositions

**Original Rec 1 — Rewrite XVI as 4–6 lines focused on parameter-pinning. KEEP, slightly revised.**
Both cross-reviews agree the current XVI does too many jobs and the clarification block is a tell. skeptic-cross-principle pushed back that a tight rewrite without fixing VII's "non-negotiable" framing leaves VII's absolutism standing — fair point, addressed in revised Rec 10. skeptic-mathematical's split-into-XVI-A/XVI-B alternative is structurally cleaner but adds a principle number; my preference remains "tight standalone XVI" because constitutional density has a real cost and the parameter-pinning rule and the plain-language rule are tightly coupled (both protect "the user understands what is being optimized"). I'll defer to the deliberation if the room prefers a split, but I'm not retracting the collapse direction.

**Original Rec 2 — Replace "within-run determinism" / "cross-run reproducibility" with operational language. KEEP.**
skeptic-cross-principle argued the within-run/cross-run distinction is "XVI's actual technical contribution" and replacement loses it. I disagree — the *concept* survives in operational language ("called at most once per parameter per run; cached for the rest of the run"), what gets dropped is the academic vocabulary. The concept is what matters; the vocabulary obscures it.

**Original Rec 3 — Resolve VII↔XVI tension. KEEP, sharpened.**
skeptic-mathematical pointed out my (a)/(b) framing didn't engage with template versioning; if templates change between runs, "same config" no longer produces the same parameter set even if pinning is correct. Real gap. The fix needs to be broader than I framed it. Revised: "VII MUST acknowledge that cross-run reproducibility is conditional on (config, template version, registered capability set) being unchanged. XVI's pinning rule is the within-run guarantee; VII's reproducibility promise must explicitly enumerate its pre-conditions." This pulls skeptic-mathematical's Rec 8 into the VII fix rather than leaving it as a XVI-only patch.

**Original Rec 4 — Add a verification mechanism (contract test). KEEP, sequenced.**
skeptic-mathematical noted my framing assumed the test would exist; today it doesn't. Sequencing fix: the constitutional principle MUST point at a test contract, but the amendment that adds the principle MUST land in the same PR as the test, not in a future PR. Otherwise we ship a constitutional pointer to a missing artifact. I'll restate the rec as: "The PR amending XVI MUST also add `tests/test_parameter_pinning.py::test_no_within_run_drift` (or equivalent name) and the principle text MUST reference the test by path."

**Original Rec 5 — Move plain-language rule into Principle X. WITHDRAW.**
skeptic-cross-principle made a real point I underweighted: X is about *output formatting*, IV is about *spec product surface*. The plain-language gloss requirement is half-and-half — `description:` fields on templates are spec-author content (IV territory), runtime output strings ("87% of agents are at their best possible position") are output-formatting content (X territory). Splitting it across X and IV would scatter a coherent rule. Better to keep the plain-language requirement inside a tightened XVI as one consolidated location. Withdrawing this recommendation.

**Original Rec 6 — Move template-documentation rule into spec 013. KEEP, narrowed.**
The detailed *form* of template documentation belongs in spec 013. The constitutional invariant — "every objective function template documents its parameters in plain language" — stays in XVI. This is a calibration of my original wording, not a withdrawal.

**Original Rec 7 — Consider removing XVI entirely. WITHDRAW.**
Both cross-reviewers and my own cross-reviews of them converged on this being the wrong move. skeptic-cross-principle was right that removing XVI without fixing VII leaves VII's absolutism unchallenged and the next stochastic-LLM principle has to bolt on its own clarification block. My own cross-review of skeptic-mathematical also flagged that removal would discard the only operationally crisp gate against re-resolving parameters mid-run. Withdrawing this option entirely; XVI stays, tightened.

**Original Rec 8 — Rename XVI. KEEP, weakly.**
"Pinned Parameter Discipline" or "Optimization Reproducibility Contract" remain my preferred renames. skeptic-cross-principle didn't surface this; skeptic-mathematical implicitly endorsed renaming via the XVI-A/XVI-B split. Lower-priority than the structural fixes but still worth doing.

**Original Rec 9 — CI hook for template description fields. KEEP.**
skeptic-mathematical's cross-review noted this complements their cache-key framing — agreed. This is the linter that operationalizes the plain-language rule. Independent of the structural fork.

**Original Rec 10 — Cross-reference VII↔XVI. KEEP, expanded.**
skeptic-cross-principle made the strongest point of either cross-review here: "VII says 'deterministic orchestration is non-negotiable' and XVI defines an exception, so calling it an exception is accurate." Their framing is more constitutionally honest than mine ("stochastic-input handling"). Adopting their wording: VII gets a back-reference acknowledging XVI as the **sole sanctioned exception** to deterministic orchestration, scoped to LLM gap-filling for parameter resolution.

---

### New Recommendations (added in revision)

**New Rec 11 — Add a V-emission clause to XVI.**
skeptic-cross-principle correctly flagged that my original review was silent on Principle V (Observable Deliberation). A pinned parameter set that is enforceable in CI but invisible in run output fails XVI's user-transparency promise on its own terms — the user can't audit what got pinned. New clause: "Pinned parameter values MUST be emitted in deliberation output (e.g., `optimization/pinned_parameters.yml` or equivalent) so the user can audit which parameter values their objective function was assembled from." This is the V↔XVI bridge that was missing.

**New Rec 12 — Soften the solver-substitution claim per skeptic-cross-principle.**
My original review treated "Changing solvers MUST NOT change what is being optimized" as one of the three operationally useful rules in XVI. skeptic-cross-principle was right that the current wording promises numerical equivalence two solvers cannot deliver. Adopting their softening: "Changing solvers MUST NOT change the objective function, its parameters, or its parameter semantics. Numerical results MAY differ within solver-tolerance bounds; the contract is on the function, not the answer." This preserves the gate I cared about (objective function as stable interface) without promising bit-identical output that real solvers cannot deliver.

**New Rec 13 — Anchor template-version dependency in VII, not just XVI.**
skeptic-mathematical's Rec 8 (template version in the cache key) is a real gap, but the gap is broader than XVI. VII's "same config produces same output" promise silently depends on template files being unchanged. The amendment should add to VII: "Reproducibility is conditional on (config, template registry, capability registry) being byte-identical between runs. Changes to any of these constitute a different input set." This formalizes what users assume but the constitution doesn't currently say.

---

### Position Summary

My core position from the original review survives the cross-review round: XVI as written is a documentation paragraph posing as a constitutional principle, and the practitioner-facing fix is to collapse it to the operational rules that actually gate PRs (parameter pinning, plain-language requirement, solver-as-implementation-detail). The cross-reviews sharpened three things I got wrong or underweighted. First, removing XVI entirely would leave VII's "non-negotiable" absolutism intact with no carved-out exception, which is strictly worse than the status quo — I withdrew that option. Second, the solver-substitution claim as currently worded promises numerical equivalence two solvers cannot deliver; softening to "objective function as contract, numerical results may differ within tolerance" preserves the gate I valued without overpromising. Third, template versioning is a real gap that affects VII more than XVI — the fix belongs in VII's reproducibility pre-conditions, not as a XVI-only patch.

The structural fork between "tight standalone XVI" (my path) and "XVI as VII extension" (skeptic-cross-principle's path) and "split into XVI-A/XVI-B" (skeptic-mathematical's path) is genuine and the deliberation needs to pick one before tightening individual clauses. I'm not retracting my preference for tight-standalone, but I'm explicit that the deliberation should treat this as a binary choice with downstream consequences for cache-key formality, V-emission placement, and CI-hook ownership. The wording fixes will have to be redone if the structural decision lands differently.

What I would not concede: the operational-language reframe (drop "within-run determinism" / "cross-run reproducibility" academic vocabulary in favor of "called at most once per parameter per run") remains the right call for practitioner ergonomics. skeptic-cross-principle argued the academic terms are XVI's technical contribution; I argue the *concept* is the contribution and the *vocabulary* is incidental. A developer reviewing a PR diff thinks "does this re-call the LLM mid-run?" not "does this preserve within-run determinism?" The constitution should phrase the invariant in the language of code review, not numerical-methods textbooks.
