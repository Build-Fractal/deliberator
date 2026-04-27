# Strictness-Skeptic Revision (Phase 3, iteration 1)

**Role**: strictness-skeptic
**Methodology**: self-consistency
**Target**: `/Users/business-daddy/code/payer-index-mono/conversus-oss/deliberations/069-self-consistency-2026-04-26/CONSTITUTION-v2.4.0-candidate.md`
**Position carried forward**: the v2.4.0 gate is too strict and structurally mis-calibrated. Cross-reviews from governance-skeptic and practitioner have sharpened — but not refuted — that diagnosis. The core load-bearing claim (criterion 1's AND-coupling and "concrete one-paragraph sketch" bar systematically rejects form constraints, meta-principles, and cross-cutting taste invariants) survives both critiques intact.

---

### Recommendation Dispositions

**R-1 (AND on criteria 1 and 3 → criterion 2 required + (1 OR 3))** — **KEEP, with sequencing clarification.**

Both cross-reviews flagged R-1 as the most contested fix. Governance-skeptic's DC-1 argued that loosening criterion 3 enables a "near-duplicate principle with a sketched lint" arbitrage path; practitioner's DC-1 argued the partial-OR contradicts a CI lint that grep-checks each section. Both critiques are real but addressable without dropping R-1.

The arbitrage critique (governance-skeptic) is answered by retaining criterion 3 as the *substantive* check while making criterion 1 the *substitutable* one. Replace R-1's wording with: "satisfies criterion 2 (falsifiable scope) AND criterion 3 (distinct from existing) AND at least one of (a) criterion 1 (mechanical verification) OR (b) demonstrated peer-review-rubric operationalization." This preserves the anti-duplication function governance-skeptic is right to defend, while opening the form-constraint and meta-principle path I flagged in MO-2 / MO-7. The CI-lint critique (practitioner) is answered by structured N/A branches in the self-assessment template — the lint can require *either* a sketched check *or* a cited rubric, and accept either as a valid fill. Practitioner's own DC-1 conceded this resolution path.

**R-2 (weaken criterion 1's "one-paragraph sketch" to "amenable to mechanical detection, peer-review rubric, or test-against-historical-incident")** — **KEEP, with qualifier.**

Practitioner's T-3 proposed an alternative ("show me a pass example and a fail example") and preferred theory-conservative loosening. I find that recommendation insufficient: worked examples calibrate the *bar* but do not address the *category exclusion* problem (form constraints have no mechanical sketch even with calibrated examples). However, practitioner's instinct toward evidence-first loosening is valid. Revised position: keep R-2 but pair it with practitioner's worked-example requirement (their #1) — the template MUST include both a mechanical-sketch PASS example and a peer-review-rubric PASS example. Without both, the gate enshrines the over-strict reading.

Governance-skeptic's DC-3 argued R-2 contradicts their P2 #4 enumerated check-type list (CI lint / parity test / structural assertion / schema validation / contract test / meta-test). The contradiction is real and resolves in R-2's favor: governance-skeptic's enumeration is itself the over-strict reading my entire review documents. Their list contains zero entries for form constraints — confirming, not refuting, MO-7.

**R-3 (meta-principle carve-out: "evaluated against criterion 1 by their citation in the construction of mechanically-checkable artifacts")** — **REVISE, narrow to closed list.**

Practitioner's DC-2 was the strongest critique I received: "meta-principle" as an open class becomes a laundry path for over-strict rejection avoidance, importing the very vagueness criterion 2 prohibits. Practitioner is right. Revised position: replace open-class "meta-principles" with a closed enumeration tied to existing principles — VI (Scripts Over Markdown), X (Zen of Python Output), XVI (Mathematical Transparency), XVII (Content Classification), XVIII (Progressive Disclosure Contract). Future expansion of the closed list requires its own MINOR amendment with worked-example justification. Governance-skeptic's T-3 raised an independent concern about Sync Impact Report timing for meta-principles; closed-list enumeration solves that too — the Sync Impact Report cites the closed list, not a forward-looking artifact-citation commitment.

**R-4 (criterion 3 "cleanliness" qualifier)** — **KEEP, but accept governance-skeptic's burden-of-proof rule as compatible alternative.**

Governance-skeptic's T-3 / P2 #5 burden-of-proof rule (≥80% / ≥20% scope decomposition) is mechanically enforceable where my "cleanliness" qualifier is judgment-laden. I argued in my cross-review of governance-skeptic that 80/20 is biased toward the existing corpus; that critique stands. But the two formulations are not actually exclusive: 80/20 can be the *first-pass* test, with the cleanliness qualifier as the override path for explicit-coordination principles (XV ↔ XXVII). Revised wording: "the proposed principle covers concerns where existing principles compose to ≥80% of scope only if the residual <20% does not require explicit reviewer-runtime coordination; otherwise the residual constitutes a coordination concern and qualifies as distinct."

**R-5 (calibrate against corpus, ≥90% retroactive admission)** — **KEEP, but lower bar in light of practitioner's DC-3.**

Practitioner's DC-3 identified a real one-way-ratchet: if grandfathering protects a stricter past *because* the corpus was authored under looser standards, retroactive calibration to that corpus encodes the looser standards forever. I conceded in my cross-review of practitioner that this is a genuine load-bearing tension. Revised position: change ≥90% to ≥85%, and add a sunset clause — "the calibration target sunsets after v3.0.0; subsequent constitutions calibrate against principles authored under v2.4.0+ gate, not the grandfathered corpus." This admits practitioner's correct framing (the corpus IS looser) while preserving R-5's anchoring function for the v2.4.0–v2.99.0 transition window.

**R-6 (retrospective review at each MINOR)** — **KEEP unchanged.**

Both cross-reviews endorsed this. Governance-skeptic's SA-3 noted it composes cleanly with their Sync Impact Report self-assessment (admission moment + retrospective moment = complete audit trail). Practitioner's T-5 noted it pairs with pre-merge verification deliberation. No revision needed.

**R-7 (form/behavioral split, criterion 1 relaxed for form constraints)** — **REVISE, fold into R-3's closed list.**

Practitioner's DC-2 against open-class "meta-principle" applies equally to open-class "form constraint" — the classification step itself becomes contested terrain. Governance-skeptic's DC-3 raised the same concern about competing definitions of "check." Revised position: drop the parametrized form/behavioral split; instead, treat the closed list from revised R-3 as the exhaustive set of relaxed-criterion-1 principles. New principles outside that list face the full criterion 1 bar. Adding to the closed list is itself a constitutional amendment subject to worked-example justification.

**R-8 (define promotion path symmetric to demotion path)** — **KEEP unchanged.**

Both cross-reviews endorsed. Governance-skeptic's SA-2 paired it with their P3 #9 (clarify destination semantics); practitioner's T-4 explicitly called both fixes compatible. The asymmetry concern (one-way demotion ratchet) survives both critiques.

**R-9 (close criterion 1's loophole: require sketched check OR cited rubric)** — **KEEP, but acknowledge internal tension with R-2.**

Practitioner's T-4 (cross-review of governance-skeptic, by extension) noted the OR-of-OR construction makes criterion 1 nearly trivially satisfiable. Revised position: R-9's "(a) sketched check OR (b) cited rubric" remains, but the rubric MUST be specifically named (file path or PR-merged precedent) and operationalize a *named failure mode*, not a generic "peer review will catch this." This sharpens the rubric branch enough to prevent the trivial-satisfaction failure mode practitioner correctly identified.

**R-10 (gate falsifiable on its own terms — auto-loosen after 3 false rejections)** — **REVISE, sequence with governance-skeptic's override.**

Governance-skeptic's DC-2 was the most surgical critique of R-10: their per-amendment override fires first and prevents R-10's incident counter from ever reaching three. Practitioner's DC-4 raised a complementary concern: "validated by real-world incidents" is judgment-laden and requires a precedent log to even be coherent. Both critiques resolve cooperatively. Revised position: adopt governance-skeptic's per-amendment override as the front-line escape hatch; R-10's loosening trigger fires only when ≥3 *override invocations* across consecutive MINOR amendments converge on the same criterion (i.e., the same criterion has been overridden 3+ times). This makes R-10 a meta-trigger keyed to override frequency rather than a parallel detection mechanism. Practitioner's precedent log (their #8) supplies the necessary tracking infrastructure.

---

### New Recommendations

**R-11. The candidate document MUST publish its own Sync Impact Report enumerating the failed-grandfathered-principles list explicitly.**

Practitioner's T-3 surfaced this with appropriate weight. The v2.4.0 candidate violates its own discipline — it lacks a Sync Impact Report for its own version bump, even though Principle XII / Versioning rules require one. The omission is a self-consistency failure visible in the document itself. Spec 069 §5 enumerates VI, X, XVI as failing the new gate; that enumeration belongs in the Sync Impact Report at the top of the constitution, not buried in a deliberation spec. Adopting this recommendation forces the calibration debate to be permanent and visible to every future amendment author, anchoring R-5 empirically rather than rhetorically.

**R-12. The "Constitutional Inclusion Criteria" block MUST be lifted from a Governance bullet to its own subsection (`### Constitutional Inclusion Criteria`).**

Governance-skeptic's P1 #1 raised this; both cross-reviews endorsed it. A meta-rule of this scope buried as a third bullet in §Governance is structurally misleading. Lifting it to a subsection improves discoverability for `/speckit.constitution check` (which can grep for headers), preserves audit-trail integrity, and is harmless to the strictness debate. The recommendation is independent of any of R-1 through R-10 and can land first.

**R-13. The gate's `CONTRIBUTING.md` reference in the operational-guidance routing block MUST be replaced with `AGENTS.md`.**

OB-2 in my original review noted that `CONTRIBUTING.md` does not exist in this repo and that Principle XVII (Content Classification) routes contribution rules to `AGENTS.md`. Practitioner's T-2 proposed a routing table; governance-skeptic's P3 #10 proposed a Principle XVII cross-reference. Both fixes assume the destination is correct; it isn't. The simplest fix — change the destination — is independent of the larger calibration debate and prevents an internal inconsistency from shipping with v2.4.0.

---

### Position Summary

The cross-reviews sharpened my position more than they undermined it. Both governance-skeptic and practitioner agreed that the gate as written is not deployable (their SA-1, our convergence on grandfathering as informative, our convergence on the missing enforcement hook). They diverged from me on *direction* — governance-skeptic toward tightening, practitioner toward enforcement — but not on *diagnosis*. The three-way convergence on diagnosis is itself evidence: three independent reviewers from different priors landed on "the gate needs material revision before merge," which is precisely the double-confirmation pattern v2.3.1's blind verification demonstrated. The substantive disagreement is about *which* revisions, not *whether*.

The most consequential revision in this pass is the closed-list enumeration replacing the open-class "meta-principle" / "form constraint" categories. Practitioner's DC-2 was correct that open classes import the very vagueness the gate claims to police; governance-skeptic's DC-3 was correct that competing definitions of "check" produce arbitrage paths. Both critiques resolve by collapsing R-3 and R-7 into a closed enumeration tied to existing principles VI, X, XVI, XVII, XVIII. This preserves the form-constraint and meta-principle protection my review argues for, while denying future amendment authors the laundry-path that practitioner correctly flagged. The sequencing question — calibrate first, then enforce — also survives both cross-reviews intact: practitioner's enforcement recommendations (their #1, #2, #5) become safe and valuable *after* R-1, R-2, and the closed-list R-3/R-7 land, and dangerous before.

The gate's purpose is to filter principles, not to filter the *kind* of principles a constitution can express. v2.4.0 as written would have passed Principles I, II, VII, VIII, IX, XI, XII, XIII, XIV, XV, XVII, XVIII, XIX, XX, XXI, XXII, XXIII, XXIV, XXV, XXVI, XXVII — and rejected VI, X, XVI. That rejection set is structurally informative: the gate excludes the form-constraint, taste-level, and meta-principle category. That category is what distinguishes a constitution from a linter ruleset. Adopt R-1 (criterion 2 + 3 required, criterion 1 substitutable), R-2 (sketch-or-rubric loosening), R-3/R-7 collapsed to closed-list enumeration, R-5 with sunset clause, R-9 sharpened, R-10 sequenced behind override, R-11/R-12/R-13 as low-cost transparency fixes, and the gate becomes a calibrated filter that approximates the historical reviewer rather than imposing a stricter forward filter than the constitution has ever survived.
