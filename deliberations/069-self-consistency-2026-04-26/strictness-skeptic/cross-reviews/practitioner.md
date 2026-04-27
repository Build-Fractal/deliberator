# Cross-Review: strictness-skeptic on practitioner

**Reviewer**: strictness-skeptic
**Target**: practitioner's review of Constitution v2.4.0 candidate
**Position carried forward**: the v2.4.0 gate is too strict and structurally mis-calibrated; criterion 1's AND-coupling and "concrete one-paragraph sketch" bar systematically rejects form constraints, meta-principles, and cross-cutting taste invariants.

The practitioner agrees the gate is "directionally correct" but operationally fragile, and proposes 10 recommendations that focus almost entirely on *enforcement* (templates, CI lints, decision trees, precedent logs) rather than *calibration*. This review treats those proposals seriously and finds that several of them, if adopted as written, would actively worsen the over-strictness problem my own review identified. Three concrete contradictions, four tensions, and three safe agreements follow.

---

### Dangerous Contradictions

**DC-1. Practitioner's Recommendation #2 (CI lint requiring the self-assessment template) actively converts a soft, calibration-correctable gate into a hard, calibration-locked one.**

The practitioner writes: "Codify a CI lint for amendment PRs that requires the self-assessment template to be filled in. ... A simple grep that fails the PR if `## Mechanical Verification` is missing or empty." The practitioner frames this as the "minimum credible enforcement hook."

This is the most dangerous proposal in the practitioner's review, and it directly contradicts the calibration argument my review developed. Here is the chain: my review (MO-1, MO-2, MO-7) shows that criterion 1 systematically rejects form constraints (Principles VI, X, XVI) — a class that constitutes ~33% of the grandfathered corpus. The practitioner's own Recommendation #1 admits the gate "is *retrodictively justified* — if applied earlier, [it] would have caught real bugs" — but the practitioner does not address that the *same retrodictive lens* shows the gate would have *also* rejected three live, load-bearing principles. The retrodictive lens cuts both ways and the practitioner only cites one side.

Adding a CI lint *now* (before the calibration miscalibration is fixed) creates a one-way ratchet: every PR that proposes a form constraint or meta-principle gets a hard CI failure on `## Mechanical Verification`, the author either invents a sketch (rewarding the rhetorical-confidence loophole my review's MO-9 flagged) or routes to operational guidance (compounding my review's MO-8 degradation problem). Once the lint exists, removing it requires its own MAJOR-tier amendment fight, because by then enforcement-loving reviewers will treat the lint as constitutional precedent.

The contradiction is sharp: the practitioner wants enforcement *because* the gate is "near-zero [value] if it remains advisory." My review wants the gate to *remain* advisory — or at minimum optional for form constraints — until the AND→partial-OR restructure (R-1) and the form-constraint carve-out (R-7) land. Hard enforcement before recalibration cements the wrong gate.

**Resolution**: defer practitioner's Recommendation #2 until after my review's R-1, R-2, and R-7 are accepted. Or scope the lint narrowly to *behavioral* principles (per my R-7 categorization) and exempt form/meta principles. The practitioner has not considered that "force-include discipline" (Principle XXII, which the practitioner cites approvingly) works because XXII is a behavioral invariant — applying the same pattern to a gate that mis-calibrates against form constraints amplifies the miscalibration.

**DC-2. Practitioner's Recommendation #5 (mandatory verification deliberation for MINOR/MAJOR amendments) compounds the "self-consistency methodology produces consistent over-strictness, not calibrated strictness" problem (my OB-4).**

The practitioner writes: "Lift from spec 066 §7 into Governance: 'MINOR and MAJOR amendments MUST be validated by a verification deliberation (separate from the proposal deliberation) against the amended text. Zero disputes from the verification deliberation is the acceptance bar before merge.'"

The premise of this recommendation is that the v2.3.1 PATCH cycle "demonstrated catches real bugs." That is true for the *omission* fix (the XV half of the XV/XXVII coordination). But the same blind verification deliberation produced this v2.4.0 candidate gate — which, by spec 069 §5's own admission, would reject 3 of 27 grandfathered principles. The practitioner treats the verification deliberation as a strict bug-catcher; my review (OB-4) treats it as a variance-reducer that locks in the deliberating agents' disposition.

If the deliberating agents skew toward strictness (and this constitution's history of one-way principle accumulation, force-include discipline, and three-layer defense suggests they do), then a "zero disputes" acceptance bar from a verification deliberation will reliably ratify the strictness. The bar does not catch the calibration error; it canonizes it. The practitioner's recommendation institutionalizes the procedure that produced the very gate my review argues is mis-calibrated.

This is doubly dangerous because the practitioner pairs "zero disputes" with "MUST" — a verification deliberation that produces *any* dispute blocks the amendment. Combined with criterion 3's "addressable by composing existing principles" rejection trigger (my MO-4), a sufficiently determined verification agent can object to nearly any new principle, blocking the amendment. The mandatory verification deliberation thus becomes a *fourth* gate criterion in disguise, and one that admits no appeal.

**Resolution**: the verification deliberation is a useful *advisory* practice but cannot be the merge bar. Replace "zero disputes" with "all disputes documented and addressed in the Sync Impact Report." This preserves the bug-catching benefit (the v2.3.1 fix) without creating a single-veto failure mode. Or restrict mandatory verification to MAJOR amendments only — MINOR amendments are reversible by their own criterion (the gate's grandfather-after-merge mechanism).

**DC-3. Practitioner's Recommendation #4 (PATCH carve-out from the three-criterion self-assessment) appears to *loosen* the gate but actually *hardens* it for the cases where loosening matters most.**

The practitioner writes: "PATCH amendments (clarifications to existing principles, cross-reference updates, wording refinements) are exempt from the three-criterion self-assessment but MUST still document the clarification rationale in the Sync Impact Report. MINOR and MAJOR amendments — those adding, removing, or redefining principles — MUST satisfy all three criteria."

On its face this sounds reasonable: don't make typo fixes throat-clear three paragraphs of self-assessment. But the carve-out is structured around *version-bump category*, not *content category*. The version-bump rules in the existing constitution say "MINOR for new principles or material expansions" — so any new principle, including a form constraint that should be admitted, requires the full three-criterion self-assessment. The carve-out only relaxes the gate where the gate already does no work (PATCH = clarification = no new principle = nothing to gate against).

This is a structurally backward concession. The cases where loosening matters are exactly the MINOR cases: a form-constraint principle (HF-3 in my review's hypothetical-future-principles section) needs criterion 1 relaxed, but the practitioner's PATCH carve-out doesn't help because adding a new principle is MINOR by definition. The practitioner has carved out the cases where the gate is already a no-op and left the gate fully active where it actually rejects valuable content.

Worse, the recommendation creates an incentive to mis-classify: an author who knows their form-constraint principle won't pass criterion 1 has a perverse incentive to frame it as a "clarification of an existing principle" (PATCH) rather than a new principle (MINOR), to dodge the gate. This both pollutes the version-bump signal and compresses content into existing principles' bodies — a form of category fraud the gate's criterion 3 specifically tries to prevent (the "fold into existing" instruction).

**Resolution**: carve out by *content category*, not version-bump category. Form constraints (per my R-7 categorization), meta-principles (per my R-3), and coordinative-clarification principles (per my MO-4 sharpening of criterion 3) get a relaxed criterion 1; behavioral principles get the full gate. This aligns the carve-out with the cases where it does work.

---

### Tensions

**T-1. Practitioner's Recommendation #1 (self-assessment template with worked examples) is good in spirit but the proposed examples reinforce the strictness skew.**

The practitioner proposes: "The example for criterion 1 could be Principle XXVI's meta-test pattern. The example for criterion 3 could be the XV/XXVII split rationale."

XXVI is the *easiest* possible pass for criterion 1 — it is a mechanical, concrete, lint-able principle by construction (the principle's own text says "the trigger is mechanical, not discretionary"). Anchoring the worked example on XXVI sets the implicit bar for criterion 1 at "mechanical and concrete *like XXVI*." A future author drafting a form constraint will read the worked example, conclude their proposal is far less mechanical than XXVI, and self-route to operational guidance. The worked example becomes a Schelling point for over-rejection.

The practitioner's own Off-Base Assumption #2 acknowledges this risk indirectly when it notes "self-assessment is treated as a viable enforcement mode" but the recommendation does not propose worked *failure* examples. A balanced template would show: (a) criterion 1 PASS via mechanical sketch (XXVI), (b) criterion 1 PASS via peer-review rubric (a hypothetical form constraint), (c) criterion 1 FAIL example. Without (b), authors will think only (a) qualifies.

This is a tension rather than a contradiction because the practitioner agrees worked examples are needed; we disagree on which examples and what they imply. Adopt Recommendation #1, but the worked-example set must include a form constraint that legitimately passes criterion 1 via peer-review-rubric (my R-2) — otherwise the template enshrines the over-strict reading.

**T-2. Practitioner's Recommendation #3 (routing table for operational-guidance destinations) treats the routing as a solved problem the constitution can codify; my review's OB-2 argues the destinations themselves are underspecified.**

The practitioner proposes a clean routing table: "Fails criterion 1 (no mechanical check) AND is a contribution rule → `AGENTS.md`. Fails criterion 1 AND is a runtime-enforced rule → `SKILL.md` or references."

My review's OB-2 noted that `CONTRIBUTING.md` does not exist in this repo, `SKILL.md` is structured around runtime orchestration not contribution rules, and `AGENTS.md` (per Principle XVII) is the actual contribution-rules home. The practitioner's routing table partially fixes this by replacing `CONTRIBUTING.md` with `AGENTS.md` — good. But the table does not address the deeper problem: a form constraint (Zen of Python Output) does not fit *any* of these destinations cleanly. It is not a contribution rule, not a runtime-enforced rule, not domain-specific. Its current home is the constitution itself. If Principle X were proposed today and routed to `AGENTS.md`, it would lose its load-into-deliberation status and degrade to a contributor suggestion.

The tension is not that the practitioner is wrong about needing a routing table; it is that the table assumes every gate-failed proposal has a clean home. For form constraints and meta-principles, the home is the constitution — which is exactly why my review's R-1 (AND→partial-OR) and R-7 (form-constraint carve-out) are necessary upstream of the routing table. Routing precedes calibration, and the practitioner's recommendation order has them backward.

**T-3. Practitioner's Recommendation #6 (v2.4.0 sync impact report) is correct on its own terms but undersells its consequences.**

The practitioner notes the v2.4.0 candidate has no sync impact report for its own version bump and recommends adding one. My review agrees this is a real omission. But the practitioner frames the sync impact report as a *documentation* fix, listing what's new, what's grandfathered, and what templates need updating.

A complete sync impact report would have to enumerate *which grandfathered principles fail the new gate* — spec 069 §5 lists three (VI, X, XVI). The practitioner's recommendation would, if executed, force the constitution to publicly document that ~11% of its corpus would fail the new gate. That documentation is the empirical anchor my review's MO-5 calls for: it makes the calibration argument legible to every future amendment author, not just the deliberation participants who happen to read spec 069.

The tension: practitioner treats this as a small documentation fix; I treat it as the single highest-leverage transparency move available, because it forces the calibration debate to be permanent and visible. We agree on the action; we disagree on its weight. Adopt the recommendation, but include the failed-grandfathered-principles list explicitly (not buried in a follow-up TODO).

**T-4. Practitioner's Recommendation #7 (rewording criterion 2 to clarify "interpretation") fixes one wording bug while leaving the structural one intact.**

The practitioner proposes: "the principle's wording MUST define its own scope and terms explicitly. ... Application within scope MAY require judgment; scope determination MUST NOT."

This is a real improvement: it preserves criterion 2's gating function while admitting principles like XXIV that legitimately require scoped judgment. My review (MO-1) treats criterion 2 as the *correct* primary gate — so I agree with the wording fix.

The tension is that the practitioner's recommendation suggests this fix is sufficient for criterion 2's coherence. But criterion 2 is being asked to do work that the AND-structure of the gate prevents it from doing alone: my MO-1 argues that *because* criterion 2 is the load-bearing one, criteria 1 and 3 should become an OR, leaving criterion 2 as the unconditional bar. The practitioner's wording fix to criterion 2 *strengthens the case for* my structural fix — a sharper criterion 2 makes the AND-coupling with the weaker criteria 1 and 3 even more wasteful. We agree on the fix; the practitioner has not noticed it implies the structural change.

**T-5. Practitioner's Recommendation #10 (cross-link the gate from Principle XVII) introduces a symmetry that makes the gate's miscalibration more visible.**

The practitioner proposes adding a one-line cross-reference in XVII: "See Governance / Constitutional Inclusion Criteria for the parallel rule applied to constitutional amendments."

This is a genuinely good recommendation in isolation — XVII does the same routing job within the codebase that the gate does within the constitution. But XVII has a clean two-way split (execution logic → SKILL.md, contribution → AGENTS.md). The gate has a four-way (or arguably uncategorized) split. Cross-linking them invites reviewers to ask: "Why does XVII have a clean dichotomy and the constitutional gate has a fuzzy four-way fan-out?" The honest answer is that XVII is calibrated against its corpus (every codebase artifact fits one of the two destinations cleanly) and the gate is not. The cross-link would, over time, force a calibration of the gate's routing — which is fine, but the practitioner does not flag this consequence.

The tension: cross-linking is good but accelerates the reckoning my review wants. Worth adopting; just be ready for the downstream pressure.

---

### Safe Agreements

**SA-1. Both reviews agree the gate as currently written has no enforcement hook and the "self-assessment" framing is structurally weak.**

My review's OB-4 ("self-consistency methodology eliminates reviewer bias toward strictness") and the practitioner's Off-Base Assumption #2 ("self-assessment is treated as a viable enforcement mode") converge on the same finding: the gate, as written, has no second-pair-of-eyes mechanism, no parser-level validation independent of the schema, and no contract test reproducing the failure scenario. Both reviews note this is inconsistent with Principle XXIV's three-layer defense pattern that the constitution applies elsewhere. We disagree on the *fix* (the practitioner wants a CI lint; I want calibration first), but agreement on the *diagnosis* is solid and useful.

**SA-2. Both reviews agree the gate needs a precedent-tracking discipline.**

My review's R-6 (retrospective review at each MINOR amendment, checking citation rate and gate-pass status of prior new principles) and the practitioner's Recommendation #8 (precedent log at `deliberations/governance-decisions.md` indexed by criterion) attack the same problem from different sides: without accumulated precedent, every amendment re-litigates the criteria from scratch, and there is no mechanism to detect when the gate has been interpreted inconsistently across amendments. The two recommendations are complementary — adopt both. The practitioner's log captures *individual* decisions; my retrospective review captures *cohort* trends. Together they produce the audit trail the gate currently lacks.

**SA-3. Both reviews agree the v2.4.0 sync impact report is missing and is a self-consistency violation.**

The practitioner's Off-Base Assumption #1 ("the version-bump rule treats this as MINOR but doesn't have a sync impact report") and my MO-5 (calibration evidence belongs in the sync impact report) converge: the constitution requires sync impact reports for amendments, this amendment lacks one for its own version bump, and the absence is itself a violation of the document's stated discipline. Adopting the practitioner's Recommendation #6 closes a gap that my review also flags; this is a clean, low-cost agreement with no downstream risk.

---

### Synthesis

The practitioner and I agree the gate has problems and disagree on the *direction* of the fix. The practitioner wants to make the gate *operationally enforceable* — templates, CI lints, decision trees, mandatory verification deliberations. I want to make the gate *correctly calibrated* — AND→partial-OR, form-constraint carve-out, sketch-or-rubric loosening of criterion 1.

The practitioner's recommendations, executed in isolation, would harden a mis-calibrated gate. My recommendations, executed in isolation, would calibrate a gate that nobody enforces. Combined in the right order — calibrate first (R-1, R-2, R-7), then enforce (practitioner's #1, #2, #3, #5) — they produce a gate that is both correctly tuned and reliably applied. Combined in the wrong order — enforce first, then calibrate — they produce three to six MINOR amendments worth of fight to walk back the lint, the mandatory verification deliberation, and the worked-example skew before the recalibration can land.

The practitioner's review is meticulous, identifies real friction, and is wrong about sequencing. The three dangerous contradictions above (DC-1, DC-2, DC-3) are concrete enough that the practitioner's recommendations should be amended to defer enforcement until calibration lands. The remaining tensions are negotiable; the safe agreements are immediate wins.

**Bottom line on the cross-review**: the practitioner is solving the wrong problem first. Enforcement of an over-strict gate amplifies the over-strictness. Calibrate, then enforce. If the gate is loosened per my R-1 + R-2 + R-7 first, the practitioner's enforcement recommendations become safe and valuable. Until then, every enforcement hook is a tightening loop.
