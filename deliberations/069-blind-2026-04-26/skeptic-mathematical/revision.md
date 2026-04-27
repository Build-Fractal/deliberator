# Phase 3 Revision: skeptic-mathematical

## Recommendation Dispositions

#### Recommendation 1: Replace "sketch in one paragraph" with "include a concrete check artifact"
- *Original position*: P1. Replace the prose sketch test with a required artifact (failing test, named CI job, file path, grep pattern, or 5-10 line pseudo-code).
- *Disposition*: **Surviving (Modified)**
- *Explanation*: This is the strongest convergence point across all three reviewers. Both cross-reviews independently flagged "sketch in one paragraph" as the gate's weakest sentence, and both proposed artifact-or-named-pointer fixes. Practitioner's framing — "named artifact location" with reduced friction — is operationally superior to my "failing test or lint rule" formulation, which Practitioner correctly notes raises the bar above what existing principles meet (XII, XIII explicitly defer to "SHOULD eventually"). I am modifying the recommendation to require *either* a named artifact location (file path, lint rule name, CI job name) *or* a 5-10 line pseudo-code outline, dropping the "failing test must exist" alternative. This preserves the artifact-vs-prose distinction without creating two-tier strictness against grandfathered principles.

#### Recommendation 2: Collapse criteria 1 and 2 into a single "Mechanical falsifiability" gate
- *Original position*: P1. Logical entailment makes the AND structure double-counting; merge into one gate.
- *Disposition*: **Withdrawn**
- *Explanation*: Practitioner's contradiction #1 is correct and I misread the operational dynamics. Logically, criterion 1 *is* a sufficient consequence of criterion 2 — if wording isn't falsifiable, no check exists. But operationally, criterion 1 is the *only* criterion that demands a content artifact; criterion 2 is a property of wording that authors self-certify. Collapsing them yields a one-criterion gate satisfied by prose alone, which is exactly the rhetorical-rather-than-operational failure mode my own review flagged. The correct fix is to keep both criteria but rewrite criterion 1 to demand the artifact (per Recommendation 1, surviving) and keep criterion 2 as the wording check. Skeptic-cross-principle's contradiction #4 also surfaces this: if criterion 1 is collapsed and criterion 3 is also redundant (their claim, plausible), the gate has zero independent criteria. Withdraw to avoid that collapse.

#### Recommendation 3: Add a worked rejection example to the gate text
- *Original position*: P1. Append a worked rejection ("code should be readable" fails criterion 2) to calibrate reviewers.
- *Disposition*: **Surviving (Modified)**
- *Explanation*: Both cross-reviewers endorse worked examples. Practitioner's tension #2 correctly notes I under-counted: the gate needs *two* worked examples — one rejection demonstrating mechanical falsifiability failure, one rejection demonstrating distinctness/composition failure. Modifying to require both. Skeptic-cross-principle's tension #1 (interaction-conflict example) is partially distinct and folds into new Recommendation R-N1 below.

#### Recommendation 4: Classify grandfathered principles into "exemplar" and "tolerated" tiers
- *Original position*: P2. Annotate I-XXVII as exemplar or tolerated to provide a calibration set.
- *Disposition*: **Withdrawn**
- *Explanation*: Both cross-reviewers attack this from different angles and both are correct. Practitioner's contradiction #2 nails it: tiering "tolerated" principles unilaterally pre-litigates migration without the migration spec the prospective-only clause requires, handing future authors a procedural cudgel to argue tolerated principles lack precedential force. Skeptic-cross-principle's contradiction #3 notes my proposal partially overlaps with their audit-by-v3.0.0 proposal but yields incoherent guidance if both ship. Practitioner's softer alternative — a footnote saying "X, XVI, prose subsections of IX should not be cited as precedent for new prose-principles" — preserves grandfathering while warning future authors. I withdraw the binary tier classification and defer to Practitioner's footnote framing in synthesis. New Recommendation R-N2 captures the residual concern.

#### Recommendation 5: Add a fourth gate for principle interaction
- *Original position*: P2. Require amendments to identify any existing principle whose contract changes and either demonstrate compatibility or propose explicit edits.
- *Disposition*: **Surviving (Modified)**
- *Explanation*: Skeptic-cross-principle's tension #2 endorses the diagnosis but disagrees on prominence (theirs: diagnostic; mine: fourth gate). Practitioner's tension #5 endorses the content-correctness but flags the friction cost: "a four-criterion gate with self-assessment and no enforcer is worse than a three-criterion gate with the same flaws." Modifying: keep the interaction check but make it a *required section in the amendment PR template* (Recommendation 10's vehicle) rather than a fourth criterion in prose. This avoids gate proliferation while preserving the compatibility check. The constitution already demonstrates this pattern in practice (XV/XXVII coordination, XXII/XXV interaction) — formalize it in the template.

#### Recommendation 6: Set a deadline for the "check does not have to exist at amendment time" debt
- *Original position*: P2. Require the check to exist by the second MINOR after introduction or auto-reclassify the principle as operational guidance.
- *Disposition*: **Withdrawn**
- *Explanation*: Practitioner's contradiction #3 is decisive: auto-reclassification bypasses the migration-spec requirement that the prospective-only clause itself mandates. "Auto-anything in governance is a contradiction with the rest of the amendment process." It also punishes principles whose checks are genuinely hard to build (XII's dead-infrastructure linter is non-trivial) by demoting them rather than tracking them as debt. Practitioner's alternative — sunset for "linter SHOULD eventually" hedges via tracking-spec citation — is the better mechanism. I withdraw the deadline and defer to Practitioner's tracking-spec approach.

#### Recommendation 7: Tighten "distinct from existing principles" with a vocabulary test
- *Original position*: P2. Require the amendment to identify at least one noun phrase or domain term not present in any existing principle's body.
- *Disposition*: **Withdrawn**
- *Explanation*: Both cross-reviewers attack this and both are correct. Skeptic-cross-principle's contradiction #2 demonstrates the test would reject legitimately distinct principles whose distinctness lies in the *predicate*, not the *vocabulary* (XI and XII both use "schema," "variable," "template" — distinguishing them is what the predicate does). Practitioner's tension #1 notes the operational hostility: amendment authors must grep all 27 principle bodies for collisions, and the test will mostly serve as a rejection lever rather than an admission test. The vocabulary test is mechanically tractable but produces wrong answers often enough that it is worse than no test. Withdraw entirely; the worked-distinctness-rejection example from Recommendation 3 (modified) does the calibration work without the false-positive rate.

#### Recommendation 8: State the false-admit / false-reject asymmetry explicitly
- *Original position*: P3. Add language stating false-rejection is recoverable, false-admission is sticky, gate errs toward strictness.
- *Disposition*: **Surviving (Modified)**
- *Explanation*: Practitioner's tension #4 endorses the idea but argues machinery beats stated bias ("reviewers ignore stated biases under pressure"). Skeptic-cross-principle's tension #3 notes my framing and theirs converge on the same diagnosis with different cures. Modifying: keep the stated asymmetry as *secondary* to the PR-template machinery (Recommendation 10), not as a substitute for it. The stated bias is cheap and adds calibration; machinery is the load-bearer. Both ship; the asymmetry text is a one-line clause, not a structural change.

#### Recommendation 9: Add a periodic re-evaluation clause for both pre- and post-gate principles
- *Original position*: P3. Every MAJOR version bump SHOULD include a constitution audit re-evaluating each principle.
- *Disposition*: **Withdrawn**
- *Explanation*: Practitioner's tension #3 argues constitutional documents earn authority precisely because they are not re-litigated every cycle, and triennial-style audits invite continual debate. This is correct. Skeptic-cross-principle's tension #5 surfaces a related issue: my proposal and their Extension-block treatment overlap, and Extension-block gating retroactively pulls grandfathered principles into the gate (which my own "prospective-only" reading should oppose). Withdraw the periodic audit. Practitioner's narrower alternative — re-evaluation triggers only when a structurally-related principle is added — could be folded into the PR-template's interaction check (Recommendation 5, modified), which is sufficient.

#### Recommendation 10: Replace the gate with a structured amendment template
- *Original position*: P3. Convert the gate into an amendment-PR template with required sections.
- *Disposition*: **Surviving (Modified, promoted to P1)**
- *Explanation*: Both cross-reviewers and my own analysis converge on this as the highest-leverage single change. Practitioner's safe agreement #2 ("the gate has no specified enforcer and this is the largest single defect") and Skeptic-cross-principle's safe agreement #3 ("the gate lacks an enforcement path") both endorse this. Practitioner's contradiction note that template-without-human-reviewer is rubber-stamping is correct — see Recommendation R-N3 below for the human-review pairing. Promoting from P3 to P1 because it is the structural vehicle through which Recommendations 1, 3, 5, and 8 land. Without the template, those recommendations are prose floating in Governance.

## New Recommendations

#### Recommendation R-N1: Add a worked interaction-conflict example to the PR template
- *Priority*: P2.
- *Source*: Skeptic-cross-principle's tension #1 surfaced this as a gap in my Recommendation 3 — a worked rejection covers intra-principle quality, but not inter-principle compatibility.
- *Proposed change*: The PR template's Compatibility section (per modified Recommendation 5) MUST include an example of a hypothetical amendment that passes criteria 1-3 yet contradicts an existing principle, with the resolution shown (either compatibility argument or proposed edits to the affected principle).
- *Rationale*: Composition redundancy and contradiction are different failure modes; an example is the only way to calibrate reviewers on the second.
- *Risk if ignored*: silent drift between e.g., a future optimization principle and VIII (Templating Engines Over Inference).

#### Recommendation R-N2: Replace "exemplar/tolerated" tiering with a non-precedential footnote
- *Priority*: P2.
- *Source*: Practitioner's contradiction #2 argued my tiering pre-litigates migration; their softer alternative preserves grandfathering while warning future authors.
- *Proposed change*: Add a single footnote to the grandfathering clause: "Pre-gate principles vary in how cleanly they would satisfy criterion 1's artifact requirement under current standards. Future amendments SHOULD be modeled on principles with named verification artifacts (XI, XII, XIII, XXII, XXIV, XXVI), not on principles whose verification path is implicit (X, XVI, prose subsections of IX). Pre-gate principles retain full ratification status; this footnote constrains modeling, not validity."
- *Rationale*: Acknowledges the calibration problem without granting future authors a procedural lever to demote pre-gate principles.
- *Risk if ignored*: future authors model new amendments on the most prose-heavy existing principle and gate drift accelerates.

#### Recommendation R-N3: Pair the PR template with a named human reviewer requirement
- *Priority*: P1.
- *Source*: My own cross-review of practitioner (contradiction #3) argued template-without-human-reviewer and human-reviewer-without-template are both half-solutions. Practitioner's recommendation 5 named the human-reviewer requirement; my Recommendation 10 named the template. Neither alone suffices.
- *Proposed change*: The amendment PR template MUST be reviewed by at least one project maintainer who is not the amendment author. The maintainer's review confirms each template section is non-empty and substantive (not just present). The template is the artifact; the maintainer is the enforcer. Both are required.
- *Rationale*: A template without a named reviewer becomes "did the bot pass" rubber-stamping. A reviewer without a template becomes "did someone approve" rubber-stamping. Pairing them creates the two-key check that gates require.
- *Risk if ignored*: the gate stays rhetorical regardless of which mechanism ships alone.

## Position Summary

My original review attacked the gate from formal coherence: criteria 1 and 2 are non-orthogonal, the "one paragraph" sketch is an author-capability proxy, grandfathering provides no calibration set. The cross-reviews from skeptic-cross-principle and practitioner reframed several of my findings in operationally critical ways. Practitioner's amendment-author lens revealed that two of my P1 recommendations (collapse criteria 1+2; vocabulary novelty test) and two of my P2 recommendations (exemplar/tolerated tiering; auto-reclassification deadline) would, if adopted, do net harm — either by removing the gate's only artifact-producing requirement, by handing future authors procedural cudgels against grandfathered principles, by bypassing the migration-spec requirement the constitution itself mandates, or by punishing principles whose checks are genuinely hard to build. Skeptic-cross-principle's corpus-consistency lens added a separate pressure: my logical-redundancy diagnosis (criterion 1 collapses into 2) and their cross-principle redundancy diagnosis (criterion 3 overlaps with XI) cannot both be acted on without leaving the gate with zero independent criteria.

I withdrew five of my ten original recommendations: the criteria 1-2 collapse (Recommendation 2), the exemplar/tolerated tiering (4), the auto-reclassification deadline (6), the vocabulary novelty test (7), and the periodic re-evaluation audit (9). I modified four of the surviving five to be operationally tighter: artifact-or-named-pointer instead of working-test (1), two worked rejection examples instead of one (3), interaction check as PR-template section instead of fourth criterion (5), false-admit/false-reject asymmetry as secondary to machinery rather than substitute (8). I promoted Recommendation 10 (structured PR template) from P3 to P1 because it is the vehicle through which 1, 3, 5, and 8 actually land — and added two new recommendations (R-N1 worked interaction example, R-N2 non-precedential footnote, R-N3 named human reviewer paired with template) that fold in the cross-reviewers' contributions where my originals were too aggressive or under-specified.

The position I now hold is narrower and more operationally honest than my original. The gate's logical redundancies are real but secondary; its missing enforcement path is primary. A coherent gate with no enforcer fails the same way an incoherent gate with no enforcer fails — by being rhetorical rather than operational. The synthesis target should be: PR template with required sections (criterion 1 artifact, criterion 2 falsifying example, criterion 3 distinctness statement with worked rejection examples, compatibility section with worked interaction example), maintainer review requirement, plus a small grandfathering footnote that warns future authors which existing principles to model on. That is enough to make the gate apply. Everything else I originally proposed was either subsumed by that change or dangerous in interaction with the rest of the amendment process.
