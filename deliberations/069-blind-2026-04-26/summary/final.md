# Spec 069 BLIND Verification — Final Synthesis

**Target**: `CONSTITUTION-v2.4.0-blind.md`, Governance section, "Constitutional Inclusion Criteria" subsection (lines 811-844). Blind methodology — agents reviewed without knowing this subsection was the recent addition.

**Mode**: Cooperative.

---

## Process Summary

- **Agents (3)**: skeptic-mathematical, skeptic-cross-principle, practitioner.
- **Phases**: 1 (Review) → 2 (Cross-Review) → 3 (Revision) → 4 (Disputes). Single round (no arbitration).
- **Total artifacts**: 15 — 3 reviews, 6 cross-reviews, 3 revisions, 3 disputes.
- **Recommendations**:
  - Proposed in Phase 1: 30 (10 per agent).
  - Withdrawn in Phase 3: 9 — skeptic-mathematical withdrew 5 (Rec 2 collapse, 4 tiering, 6 deadline, 7 vocabulary, 9 audit); skeptic-cross-principle withdrew 2 (Rec 1 merge-into-XI, 10 fold-into-XII); practitioner withdrew 3 (Rec 3 delete-Criterion-1, 6 footnote, 9 body-bloat).
  - Modified in Phase 3: 8 — recommendations refined under cross-review pressure.
  - Surviving recommendations (with revisions): 21.
  - New recommendations added in Phase 3: 6 (skeptic-mathematical R-N1/R-N2/R-N3; skeptic-cross-principle N1/N2/N3; practitioner #11/#12).
- **Disputes remaining after Phase 4**: 3 substantive disputes — all on the gate (in scope for spec 069).
- **Convergence points**: 5 strong, 2 moderate.

---

## Recommendation Scorecard

| # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Challenged By | Convergence | Final Status |
|---|-------|----------------|------------------|---------------------|----------------|-------------|--------------|
| SM-1 | skeptic-mathematical | Replace "sketch in one paragraph" with concrete check artifact | P1 | Surviving (modified — "named pointer or 5-10 line pseudo-code") | practitioner: too strict | Convergent with SCP-2, Pr-2 | **Adopt (P1)** |
| SM-2 | skeptic-mathematical | Collapse criteria 1+2 into single "Mechanical Falsifiability" gate | P1 | Withdrawn | practitioner cont. #1 | All agreed withdraw | **Withdrawn** |
| SM-3 | skeptic-mathematical | Add worked rejection example | P1 | Surviving (modified — two examples) | none | Convergent with Pr-4 | **Adopt (P1)** |
| SM-4 | skeptic-mathematical | Classify grandfathered principles into exemplar/tolerated tiers | P2 | Withdrawn | practitioner cont. #2; SCP cont. #3 | All agreed withdraw | **Withdrawn** |
| SM-5 | skeptic-mathematical | Add fourth gate for principle interaction | P2 | Surviving (modified — PR template section, not 4th criterion) | practitioner tension #5 | Partial convergence | **Adopt (P2)** |
| SM-6 | skeptic-mathematical | Deadline + auto-reclassification for unverified principles | P2 | Withdrawn | practitioner cont. #3 | All agreed withdraw | **Withdrawn** |
| SM-7 | skeptic-mathematical | Vocabulary novelty test for Criterion 3 | P2 | Withdrawn | SCP cont. #2; practitioner tension #1 | All agreed withdraw | **Withdrawn** |
| SM-8 | skeptic-mathematical | State false-admit/false-reject asymmetry | P3 | Surviving (modified — secondary to machinery) | practitioner: machinery beats stated bias | None | **Adopt (P3)** |
| SM-9 | skeptic-mathematical | Periodic re-evaluation at every MAJOR | P3 | Withdrawn | practitioner tension #3 | All agreed withdraw | **Withdrawn** |
| SM-10 | skeptic-mathematical | Replace gate with structured PR template | P3 → **P1** | Surviving (promoted) | none | Strong convergence | **Adopt (P1)** |
| SM-RN1 | skeptic-mathematical | Worked interaction-conflict example | P2 (new) | Surviving | none | Aligned with Pr-4 | **Adopt (P2)** |
| SM-RN2 | skeptic-mathematical | Non-precedential footnote (positive modeling guidance) | P2 (new) | Surviving | SCP dispute #1 | Practitioner conditional accept | **Disputed** |
| SM-RN3 | skeptic-mathematical | Pair PR template + named human reviewer | P1 (new) | Surviving | none | Strong convergence | **Adopt (P1)** |
| SCP-1 | skeptic-cross-principle | Merge criterion 3 into Principle XI | P1 | Withdrawn | practitioner cont. #2; SM cont. | All agreed withdraw | **Withdrawn** |
| SCP-2 | skeptic-cross-principle | Tighten criterion 1 to structured `Verification:` block | P1 | Surviving (strengthened) | none | Strong convergence | **Adopt (P1)** |
| SCP-3 | skeptic-cross-principle | Demote criterion 2 to one-sentence Governance note | P1 | Surviving | practitioner cont. #4; SM disagreed | None | **Disputed** |
| SCP-4 | skeptic-cross-principle | Tiered classification (exemplar/tolerated/migration-candidate) + v3.0.0 audit | P1 | Surviving (revised) | practitioner cont. #3; SM withdrew counterpart | None | **Disputed** |
| SCP-5 | skeptic-cross-principle | Identify migration candidates (VI, X, XVI, XX, XXI) | P1 | Surviving | none | Convergence on candidate list | **Defer to follow-up** |
| SCP-6 | skeptic-cross-principle | Specify gate's enforcement path | P1 | Surviving | none | Strong convergence | **Adopt (P1)** |
| SCP-7 | skeptic-cross-principle | Clarify versioning for migrations | P2 | Surviving | none | None | **Adopt (P2)** |
| SCP-8 | skeptic-cross-principle | Extension blocks ARE amendments and MUST satisfy gate | P2 | Surviving | practitioner: silent | None | **Disputed** |
| SCP-9 | skeptic-cross-principle | Cross-reference antipatterns catalog as migration destination | P2 | Surviving | none | Convergent with SM gap | **Adopt (P2)** |
| SCP-10 | skeptic-cross-principle | Remove gate entirely; fold criterion 1 into Principle XII | P3 | Withdrawn | SM cont. #2; practitioner cont. #1 | All agreed withdraw | **Withdrawn** |
| SCP-N1 | skeptic-cross-principle | Structured `Existing-Principle-Distinctness:` block | P2 (new) | Surviving | SM dispute #2 | None | **Disputed** |
| SCP-N2 | skeptic-cross-principle | Acknowledge gate-vs-grandfathered enforcement asymmetry | P2 (new) | Surviving | none | Aligned with SM-8 | **Adopt (P2)** |
| SCP-N3 | skeptic-cross-principle | Define maintainer via CODEOWNERS | P1 (new) | Surviving | none | Strong convergence | **Adopt (P1)** |
| Pr-1 | practitioner | Mechanize gate via PR template + CI lint | P1 | Surviving (strengthened) | none | Strong convergence | **Adopt (P1)** |
| Pr-2 | practitioner | Replace "sketch in one paragraph" with named-artifact requirement | P1 | Surviving (refined — adopts `Verification:` block) | none | Strong convergence | **Adopt (P1)** |
| Pr-3 | practitioner | Remove Criterion 1 entirely | P1 | Withdrawn | SCP cont. #1; SM cross-review | All agreed withdraw | **Withdrawn** |
| Pr-4 | practitioner | Add worked example for Criterion 3 | P2 | Surviving (expanded — two examples incl. accepted scope-extension) | none | Strong convergence | **Adopt (P2)** |
| Pr-5 | practitioner | Specify enforcer (mandate non-author maintainer review) | P2 | Surviving (conditional on maintainer-role definition) | SCP cont. #4 | Strong convergence | **Adopt (P1)** |
| Pr-6 | practitioner | Footnote disclaiming X/XVI/IX-prose as precedent | P2 | Withdrawn | both skeptics | All agreed withdraw | **Withdrawn** |
| Pr-7 | practitioner | Migration spec must identify receiving file's current owner | P2 | Surviving | none | None | **Adopt (P2)** |
| Pr-8 | practitioner | Sunset clause for "linter SHOULD eventually" hedges | P2 | Surviving | SCP tension #3 | Convergence on prospective scope | **Adopt (P2)** |
| Pr-9 | practitioner | Permit new principles when extension > 1 paragraph | P3 | Withdrawn | SCP cont. #3; SM cross-review | All agreed withdraw | **Withdrawn** |
| Pr-10 | practitioner | Reorder gate to lead with enforcement | P3 | Surviving | none | Convergent | **Adopt (P3)** |
| Pr-11 | practitioner | Establish maintainer role as prerequisite amendment | P1 (new) | Surviving | SCP-N3 alternate path | Convergent | **Adopt (P1)** |
| Pr-12 | practitioner | Ship template + maintainer review as non-separable bundle | P1 (new) | Surviving | none | Strong convergence | **Adopt (P1)** |

---

## Dangerous Contradictions Found

### Resolved Contradictions

1. **Which criterion is redundant?** SM said criteria 1+2 collapse; SCP said criterion 3 collapses into XI. If both correct, gate has zero independent criteria. **Resolution**: both withdrew their respective collapse proposals. Phase 3 convergence: keep all three criteria, mechanize via PR template, fix the artifact requirement in Criterion 1.
   - Source: SM revision Disposition 2 (withdrawn); SCP revision Disposition 1 (withdrawn).

2. **Eliminate gate vs. mechanize gate.** SCP Rec 10 (fold criterion 1 into XII) and SM Rec 10 (PR template) pointed in opposite architectural directions. **Resolution**: SCP withdrew the fold-into-XII path because it overstretches XII's data-duplication scope; gate retained as a discrete construct in Governance, mechanized via template.
   - Source: SCP revision Disposition 10; SM revision (template promoted to P1).

3. **Vocabulary-novelty test vs. body-bloat permissiveness.** SM-7 would reject extensions that share vocabulary; Pr-9 would encourage spawning new principles when extensions exceed one paragraph. Mutually exclusive. **Resolution**: both withdrew. Worked examples replace both as the calibration mechanism.
   - Source: SM revision Disposition 7; practitioner revision Disposition 9.

4. **Aggressive simplification (delete Criterion 1) vs. retention.** Pr-3 and SM-2 each proposed different deletions. **Resolution**: all three agents converged that Criterion 1 is the load-bearing artifact-producing requirement; deleting it inverts the gate's value proposition.
   - Source: practitioner revision Disposition 3; SM revision Disposition 2; SCP cross-review of practitioner.

### Unresolved Contradictions

1. **Grandfathering disposition (3-way disagreement after Phase 4).** SM proposes a non-precedential footnote (R-N2). SCP proposes a tiered classification (exemplar / tolerated / migration-candidate) with v3.0.0 audit for migration-candidates only. Practitioner withdrew their own footnote and now wants the entire disposition deferred to a separate follow-up amendment. **Synthesizer assessment**: each position has a coherent rationale and they cannot all be true simultaneously. The practitioner's defer-to-follow-up is the most procedurally honest (avoids pre-litigating migration in this amendment); SM's footnote is the lowest-friction acknowledgment; SCP's tiering is the only forcing mechanism. See Remaining Disputes §1.

2. **Criterion 3 mechanism (3-way disagreement after Phase 4).** SCP-N1 wants a structured `Existing-Principle-Distinctness:` block (cite 2-3 closest principles + novel predicate + why Extension insufficient). SM disputes that this inherits the same satisfy-mechanically failure mode as the withdrawn vocabulary test. Practitioner sits between, supporting Governance criteria + worked examples + lighter template structure. **Synthesizer assessment**: SCP's block adds enforcement surface but its outputs are author self-certifications. Worked examples bind reviewers but do not bind authors. The two are complementary, not exclusive. See Remaining Disputes §2.

3. **Extension-block treatment (silent disagreement).** SCP-8 holds that Extension blocks landing post-ratification MUST satisfy the gate even when extending grandfathered principles. SM and practitioner did not engage with this in Phase 3. **Synthesizer assessment**: this is a real loophole — pre-gate principles like IX, XI, XV already carry post-ratification Extension subsections. Without explicit treatment, every grandfathered principle becomes a backdoor admission channel for prose-only additions. See Remaining Disputes §3.

---

## Systemic Contradictions

1. **Pattern: prospective-only design is partially retroactive in practice.**
   - *Manifests in*: SM revision (withdrawn periodic audit Rec 9); SCP Off-Base Assumption 2 (Phase 1); SCP-8 Extension-block gating; SM tension #5 with SCP.
   - *Root cause*: the constitution is long-lived and grandfathered principles get extended, modified, and referenced over time. A purely prospective gate cannot stay clean of the pre-gate corpus.
   - *Implication*: the synthesizer must pick whether the gate touches grandfathered principles' future extensions (SCP position) or stays strictly prospective (SM/Practitioner position). Either choice is coherent; the current gate text is silent and that silence is the bug.

2. **Pattern: self-assessment criteria become rubber stamps without external enforcement.**
   - *Manifests in*: practitioner Missed Opportunities #2/#5 (Phase 1); SCP Off-Base Assumption #4; SM Rec 10 promoted to P1; convergence on PR template + maintainer review.
   - *Root cause*: criteria written as "the principle MUST satisfy X" with no specified actor, no PR template field, no CI hook reduce to "the author asserts it satisfies X."
   - *Implication*: every other recommendation depends on enforcement landing. The non-separable bundle (template + CODEOWNERS reviewer + CI lint) is the floor.

3. **Pattern: judgment-recursion in falsifiability checks.**
   - *Manifests in*: "concrete enough to sketch in one paragraph" sub-clause (all three reviews flag it); practitioner Off-Base Assumption #2; SM Off-Base Assumption #1; SCP Missed Opportunity #5.
   - *Root cause*: the gate uses author-capability proxies (writing fluency) as content tests. A skilled writer can make any principle sound verifiable; an unskilled writer fails to articulate genuine verifiability.
   - *Implication*: the fix is structural (named artifact, check type, failure signal), not lexical. Convergent across all three reviewers.

4. **Pattern: redundancy with existing principles is structural, not coincidental.**
   - *Manifests in*: SCP Alignment #3 (criterion 3 vs XI); SM Rec 2 (criterion 1 vs criterion 2); SCP Rec 10 alternate (criterion 1 vs XII).
   - *Root cause*: the gate was authored to capture invariants (verifiability, falsifiability, distinctness) that the constitution already partially encodes via Principles II, XI, XII, XIV. Some redundancy is reinforcing; some is genuine duplication.
   - *Implication*: pure simplification (collapse-into-existing) breaks the gate's separability; pure retention preserves the appearance of independence without substance. The Phase 3 consensus (retain three criteria, fix Criterion 1's artifact, demote redundancy concerns to wording) is the workable compromise.

5. **Pattern: governance auto-anything contradicts the migration discipline.**
   - *Manifests in*: SM withdrew auto-reclassification deadline (Rec 6); SM withdrew periodic audit (Rec 9); practitioner cont. #3 against SM.
   - *Root cause*: the constitution mandates that migration to operational guidance is "a separate, intentional act" with a migration spec. Any automation (deadline-driven demotion, time-boxed reclassification) bypasses that.
   - *Implication*: enforcement mechanisms must be procedural (template + reviewer), not temporal (deadlines + auto-demotion). Strong convergence.

---

## Convergence Achieved

1. **Position: Replace "sketch in one paragraph" with structured `Verification:` block.**
   - *Agreed recommendation*: Criterion 1's bar is restated as a structured block requiring (a) check type from {schema validation, parity test, lint rule, structural assertion, contract test}, (b) artifact (file path, lint name, parity test name, named CI job, or 5-10 line pseudo-code), (c) failure signal. If artifact does not exist at amendment time, a tracking issue/spec MUST be cited within the block.
   - *Supporting agents*: skeptic-mathematical (Rec 1), skeptic-cross-principle (Rec 2), practitioner (Rec 2).
   - *Evidence basis*: independent triangulation across formal-coherence lens, corpus-consistency lens, and amendment-author lens.
   - *Pre-existing or earned*: **earned** in Phase 2 cross-reviews; further refined in Phase 3.

2. **Position: PR template + named CODEOWNER reviewer + CI lint ship as a non-separable bundle.**
   - *Agreed recommendation*: the gate is enforced by (a) a `/speckit.constitution` PR template requiring filled `Verification:`, falsifying-example, and distinctness sections, (b) a CI lint that fails when sections are empty on PRs that add new principle headings, AND (c) review sign-off from at least one CODEOWNER of `constitution.md` who is not the amendment author. The constitution text MUST state the pairing — neither alone counts as gate enforcement.
   - *Supporting agents*: skeptic-mathematical (Rec 10 promoted to P1, R-N3), skeptic-cross-principle (Rec 6, N3), practitioner (Rec 1, Rec 5, Rec 12).
   - *Evidence basis*: all three agents independently identified the missing-enforcer defect as the largest single defect.
   - *Pre-existing or earned*: **earned** — strongest convergent finding of the deliberation.

3. **Position: Maintainer role grounded in CODEOWNERS, not phantom designation.**
   - *Agreed recommendation*: cite an existing CODEOWNERS file or named GitHub team as the source of authoritative reviewer identity. If neither exists in the repo today, the gate amendment is paired with a prerequisite amendment establishing the role.
   - *Supporting agents*: skeptic-cross-principle (N3, explicit CODEOWNERS), practitioner (Rec 11, prerequisite amendment if missing), skeptic-mathematical (R-N3, implies but does not name artifact — consistent).
   - *Evidence basis*: independent identification of phantom-role enforcement loophole.
   - *Pre-existing or earned*: **earned** in Phase 2.

4. **Position: At least two worked examples in the gate text.**
   - *Agreed recommendation*: ship at least two worked rejection examples — one demonstrating mechanical-falsifiability failure (e.g., "code should be readable" → no automated check), one demonstrating distinctness/composition failure (e.g., "all template variables must be lowercase" → composes from IX + XI). Practitioner adds a third positive example (XXVII as accepted scope-extension precedent); SM-RN1 adds a third interaction-conflict example.
   - *Supporting agents*: skeptic-mathematical (Rec 3 modified, R-N1), skeptic-cross-principle (N1 partial), practitioner (Rec 4 expanded).
   - *Evidence basis*: convergent diagnosis that the gate without worked examples becomes a fresh interpretive negotiation each application.
   - *Pre-existing or earned*: **earned**.

5. **Position: Withdraw governance auto-anything (deadlines, periodic audits, auto-reclassification).**
   - *Agreed recommendation*: do not adopt time-boxed automatic demotion of principles whose checks are not built within N versions; do not require constitution audits at every MAJOR bump. Migration to operational guidance is a separate intentional act per the prospective-only clause.
   - *Supporting agents*: skeptic-mathematical (withdrew Rec 6, Rec 9), practitioner (Rec 8 prospective-only). SCP softened but did not fully withdraw the v3.0.0 deadline (see Remaining Disputes §1).
   - *Evidence basis*: auto-anything contradicts the constitution's own migration-spec discipline.
   - *Pre-existing or earned*: **earned** — strong consensus on auto-reclassification, partial consensus on tiering deadline.

6. **Position: Aggressive simplification of the three-criterion structure is rejected.**
   - *Agreed recommendation*: the gate retains three criteria. Criterion 1 stays load-bearing (with `Verification:` block fix). Criterion 2 is not collapsed into Criterion 1, not absorbed into II. Criterion 3 is not absorbed into XI, not folded into XII. Variant simplifications all break the gate's separability.
   - *Supporting agents*: all three (each withdrew their own simplification proposal under cross-review pressure).
   - *Evidence basis*: each simplification path was tried and found to remove the gate's only novel contribution or weaken an existing principle.
   - *Pre-existing or earned*: **earned** through symmetric withdrawals in Phase 3.

7. **Position: "Linter SHOULD eventually" hedge is debt; future amendments must cite tracking spec.**
   - *Agreed recommendation*: amendments using the "linter SHOULD eventually check" form MUST cite a tracking spec or issue. The rule applies prospectively (matches the gate's own grandfathering discipline). Existing principles XII, XIII, XXVI are not retroactively required to ship the linter via this amendment.
   - *Supporting agents*: practitioner (Rec 8), skeptic-mathematical (withdrew automatic deadline; aligned on prospective scope), skeptic-cross-principle (narrowed to migration-candidates only).
   - *Evidence basis*: convergent identification of debt-sink pattern; convergence on prospective scope as the right floor.
   - *Pre-existing or earned*: **earned**, with residual disagreement on retroactivity.

---

## Arbiter-Resolved Disputes (Prior Rounds)

N/A — single round.

<!-- CONVERSUS:DISPUTES_BEGIN -->
## Remaining Disputes

### Dispute: Grandfathering Disposition

- *Positions*:
  - **skeptic-mathematical (R-N2)**: a non-precedential footnote naming well-modeled principles (XI, XII, XIII, XXII, XXIV, XXVI) as positive guidance, with explicit text stating pre-gate principles retain full ratification status. No demotion of any principle.
  - **skeptic-cross-principle (revised Rec 4)**: tiered classification *now* (exemplar / tolerated / migration-candidate); migration-candidates (VI, X, XVI, XX, XXI) bound to a v3.0.0 disposition deadline; tolerated principles persist with documented permanent exception listing failing criteria.
  - **practitioner (revised, withdrew #6)**: defer the entire disposition to a follow-up amendment. This amendment ships the gate prospectively-only and stops there. Will accept SM's footnote as fallback if maintainer judges deferral unacceptable; will NOT accept SCP's tiering.

- *Arguments*:
  - SM: forcing mechanisms (deadlines, tiers) pre-litigate migration without the migration spec the constitution itself mandates. A footnote is the lowest-friction acknowledgment of the precedent risk that does not hand future authors a procedural cudgel.
  - SCP: without a deadline, "tolerated" status is permanent and the two-tier constitution never collapses. A footnote without a forcing mechanism is the constitutional equivalent of a `# TODO` comment.
  - Practitioner: shipping ANY grandfathering disposition with this amendment expands the blast radius from "add a gate" to "audit the corpus." The amendment-author cost is high; the constitutional discipline cost is also high. Defer to a follow-up amendment whose only job is grandfathering disposition.

- *Synthesizer assessment*: the practitioner's defer-to-follow-up is procedurally cleanest — it respects the migration-spec discipline and keeps this amendment's blast radius narrow. SM's footnote is acceptable as a calibration aid if the maintainer judges deferral unacceptable. SCP's tiered classification with deadline is the only proposal with a forcing mechanism, but it is also the only proposal that pre-litigates migration. Two of three reviewers (SM in Phase 3 revision, practitioner in Phase 4) preferred not to ship a forcing mechanism with this amendment.

- *Recommended resolution*: **adopt the practitioner's defer-to-follow-up posture as default; allow SM's footnote (R-N2) as opt-in if the maintainer wants explicit calibration guidance shipped with the gate.** Reject SCP's tiered classification with deadline for this amendment — defer it to the follow-up grandfathering disposition spec where it can be properly debated alongside migration-candidate selection.

### Dispute: Criterion 3 Operational Test (Distinctness Block vs. Worked Examples)

- *Positions*:
  - **skeptic-cross-principle (N1)**: structured `Existing-Principle-Distinctness:` block in the PR template citing (a) 2-3 closest existing principles, (b) the novel predicate, (c) why an Extension block on a cited principle would be insufficient. Block as enforcement, examples as calibration.
  - **skeptic-mathematical (modified Rec 3 + R-N1)**: free-form distinctness statement plus two worked rejection examples in the gate text. Examples bind reviewers; a structured block becomes mechanically satisfiable boilerplate (same failure mode as the withdrawn vocabulary-novelty test).
  - **practitioner (Rec 4 expanded)**: criteria stay in Governance prose with mandated structural blocks; PR template requires filled blocks. Two worked examples (one rejection + one accepted scope-extension citing XXVII as precedent). Acceptable middle ground: structured block lighter than SCP's three-part form.

- *Arguments*:
  - SCP: free-form prose is satisfiable by self-certification. The block forces authors to enumerate proximate principles and articulate the predicate, which is harder to fake than free-form prose.
  - SM: SCP's block inherits the satisfy-mechanically failure mode in a different costume — authors will list three principles, assert a predicate, assert insufficiency, and ship. The block adds procedural surface that does not catch the error mode it targets. Worked examples in gate text constrain reviewers, which is what calibration actually requires.
  - Practitioner: both surfaces ship together — Governance prose names the invariants, template enforces them. Worked examples are non-negotiable (floor: two); the structured block is acceptable in a lighter form than SCP's full (a)/(b)/(c).

- *Synthesizer assessment*: the block and examples are not mutually exclusive — practitioner's middle-ground correctly identifies that. The disagreement is about how rigid the block should be. SCP's three-part form is the strongest enforcement surface but introduces "show your work" overhead that may produce ritualized compliance. SM's free-form is the lightest but provides no enforcement floor beyond "section non-empty." Practitioner's lighter structured form (name closest principle + one sentence on insufficiency) is the operational sweet spot.

- *Recommended resolution*: **ship two worked examples in the gate text (one mechanical-falsifiability rejection, one distinctness/composition rejection — practitioner's accepted scope-extension example deferred or shipped as flexibility lever). Require the PR template's distinctness section to name the closest existing principle and state in one sentence why an Extension would be insufficient — without SCP's three-part (a)/(b)/(c) sub-structure.** This adopts practitioner's middle ground; SCP's full block can be revisited if the lighter form proves insufficient in practice.

### Dispute: Extension-Block Treatment

- *Positions*:
  - **skeptic-cross-principle (Rec 8, retained)**: Extension blocks landing after the gate's ratification date MUST satisfy criteria 1, 2, 3 even when extending a grandfathered principle. Without this, every grandfathered principle becomes a backdoor admission channel for prose-only additions.
  - **skeptic-mathematical**: silent in Phase 3 revision (withdrew their related periodic-audit recommendation). Cross-review tension #5 noted Extension-block gating retroactively pulls grandfathered principles into the gate, destabilizing the prospective-only design.
  - **practitioner**: silent in Phase 3. Sidestepped the question; cross-review of SCP acknowledged SCP's position is more rigorous and theirs more permissive.

- *Arguments*:
  - SCP: the constitution already shows the pattern in practice — IX has a v2.3.0 Extension (behavior-over-shape testing); XI has a v2.3.0 Extension (registry-first declaration); XV has a v2.3.1 Clarification. These postdate the gate's ratification. If they don't satisfy the gate, the prospective rule has a hole.
  - SM (implicit): retroactivity tension — Extension-block gating effectively converts grandfathering from "existing principles retain ratified status" to "existing principles retain ratified status only until next touched." That is a different and stricter rule than the constitution currently states.
  - Practitioner (implicit): broadening this amendment's scope to cover Extension blocks expands its blast radius; defer to a follow-up if Extension blocks become a measurable problem.

- *Synthesizer assessment*: SCP's diagnosis is correct — without explicit treatment, Extension blocks are a loophole. The other two agents did not engage substantively, so the dispute is asymmetric: one reviewer pressing, two silent. The right resolution is somewhere between SCP's "MUST satisfy gate" and silent default. Treating Extension blocks as full amendments (subject to all three criteria) is structurally sound but strict; treating them as out-of-scope leaves the loophole.

- *Recommended resolution*: **adopt a middle position — Extension blocks landing post-ratification MUST include the `Verification:` block (Criterion 1) when introducing new normative requirements; Criterion 3 (distinctness) is implicitly satisfied by being an extension to the parent principle, but the extension MUST declare why it belongs in the parent's body rather than a new principle. This narrows SCP's full-gate requirement to Criterion 1's artifact requirement (the load-bearing piece) without retroactively gating wording-level extensions.** If the synthesizer judges the corpus-coherence cost of even this narrower rule too high, defer Extension-block treatment entirely to the follow-up grandfathering disposition spec.
<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

**Important blind-methodology distinction**: All findings below are on the Governance "Constitutional Inclusion Criteria" subsection (in scope for spec 069). Findings on other principles (X, XVI, IX, XII, XIII, XVIII, XX, XXI, XXV, XXVI, etc.) surfaced incidentally as calibration cases or precedent concerns — those are flagged separately at the bottom and **deferred to follow-up specs**.

### P1 (must ship with the gate amendment to be operational)

1. **Replace "concrete enough that an engineer reading the principle can sketch the check in one paragraph" with a structured `Verification:` block.** The block MUST contain: (a) check type from {schema validation, parity test, lint rule, structural assertion, contract test}, (b) artifact (file path, lint name, parity test name, named CI job, or 5-10 line pseudo-code), (c) failure signal. If the working artifact does not exist at amendment time, a tracking issue or spec MUST be cited within the block. — *Source*: SM-1 modified, SCP-2 strengthened, Pr-2 refined; convergence point #1.

2. **Add PR template + CI lint as gate enforcement.** The `/speckit.constitution` PR template MUST require filled `Verification:`, falsifying-example, and distinctness sections corresponding to each criterion. A CI lint MUST fail PRs that add new principle headings (`### N. Principle Name`) without filling these sections. — *Source*: SM-10 promoted, SCP-6 kept, Pr-1; convergence point #2.

3. **Mandate non-author CODEOWNER review.** Amendment review requires sign-off from at least one CODEOWNER of `constitution.md` who is not the amendment author. The amendment text MUST cite the existing CODEOWNERS file (or named GitHub team) by name. If neither exists in the repo today, the gate amendment is paired with a prerequisite amendment establishing the role. — *Source*: SM-RN3, SCP-N3, Pr-5/Pr-11; convergence point #3.

4. **State the PR-template + maintainer-review pairing as non-separable.** The constitution text MUST explicitly state that gate enforcement is the conjunction of (a) PR template, (b) CI lint, and (c) CODEOWNER review. Each one alone is rubber-stamping; only all three together count as enforcement. — *Source*: Pr-12, SM-RN3, SCP-N3; convergence point #2.

### P2 (should ship; substantive but not load-bearing)

5. **Add at least two worked examples to the gate text.** One mechanical-falsifiability rejection ("code should be readable" → no automated check). One distinctness/composition rejection ("all template variables must be lowercase" → composes from IX + XI; refinement belongs in IX's body). — *Source*: SM-3 modified, Pr-4 expanded, SCP-N1 partial; convergence point #4.

6. **Require PR-template Distinctness section to name closest existing principle.** Free-form statement plus a one-sentence explanation of why an Extension block on the cited principle would be insufficient. (Practitioner's middle-ground form; not SCP's full three-part block.) — *Source*: dispute #2 recommended resolution.

7. **Require PR-template Compatibility section with worked interaction-conflict example.** Include in the gate text a worked interaction-conflict example demonstrating an amendment that passes criteria 1-3 yet contradicts an existing principle, with the resolution shown (compatibility argument or proposed edits). — *Source*: SM-5 modified, SM-RN1.

8. **Acknowledge gate-vs-grandfathered enforcement asymmetry in Governance.** Add language stating: "The Constitutional Inclusion Criteria are enforced strictly because they govern the standard for every other principle. Existing principles that defer their verification mechanism retain their grandfathered status; the gate does not retroactively require them to ship." — *Source*: SCP-N2, SM-8 modified.

9. **Specify versioning for gate-related migrations.** Migrating an existing principle to operational guidance is MAJOR (removal). Adding a verification mechanism to a grandfathered principle without changing its body is PATCH. Adopting the gate itself is MINOR (new principle/material expansion of Governance). — *Source*: SCP-7.

10. **Cross-reference the antipatterns catalog as a migration destination.** Name `antipatterns/catalog.md` alongside CONTRIBUTING.md, specs, SKILL.md, and reference documents as the appropriate destination for principles that fail the gate when their content is a recurring failure pattern. — *Source*: SCP-9.

11. **Sunset clause for "linter SHOULD eventually" hedges.** Future amendments using this hedge MUST cite a tracking spec or issue. Prospective only — existing principles XII, XIII, XXVI are not retroactively required to ship the linter. — *Source*: Pr-8.

12. **Migration spec must identify receiving file's current owner.** The receiving document's maintainer must acknowledge the addition in the migration PR. — *Source*: Pr-7.

### P3 (nice to have; calibration / wording)

13. **State the false-admit / false-reject asymmetry.** Add one-line clause: "When in doubt, the gate errs toward operational guidance. False-rejection is recoverable; false-admission is harder to reverse because of the prospective-only migration rule." — *Source*: SM-8 modified.

14. **Reorder the section to lead with enforcement, not criteria.** Rename "Constitutional Inclusion Criteria" to lead with the PR template and enforcer identity. — *Source*: Pr-10, SM-10 implicit.

### Disputed (do not ship until resolved)

- **Grandfathering disposition** — defer to follow-up spec per Remaining Disputes §1 (synthesizer recommendation: adopt practitioner's defer-to-follow-up; opt-in to SM's footnote if calibration is judged urgent; reject SCP's tiered classification for this amendment).
- **Extension-block treatment** — narrow to Criterion 1 only (synthesizer recommendation per Remaining Disputes §3) or defer entirely to follow-up spec.

### Out-of-scope findings (deferred to follow-up specs, NOT for spec 069)

These findings surfaced incidentally during blind review of other principles. They are valid but belong to their own follow-up specs:

- **Principle X (Zen of Python Output)** would fail Criterion 1 if proposed today (irreducibly subjective). — Deferred.
- **Principle XVI (Mathematical Transparency)** plain-language explanation requirement is unverifiable. — Deferred.
- **Principle IX (Functional Programming and Clean Code)** prose subsections (clean-code aesthetics) would fail Criterion 1. — Deferred.
- **Principle VI (Scripts Over Markdown)** judgment-laden ("when the artifact drives behavior"). — Deferred.
- **Principle XX (Decomposition Mechanism Precedence)** and **XXI (Extraction Ordering)** read as workflow heuristics rather than invariants. — Deferred.
- **Principle XVIII (Progressive Disclosure Contract)** embeds operational tuning (8-12k token budget). — Deferred.
- **Principle XXV (Live Test Cost Discipline)** contains operational CI configuration. — Deferred.
- **Migration-candidate list** (VI, X, XVI, XX, XXI) — proper home is the follow-up grandfathering disposition spec, not this amendment.

---

## Key Concessions

### skeptic-mathematical

- **Withdrew Rec 2 (collapse criteria 1+2)** — practitioner's contradiction #1 demonstrated that operationally, criterion 1 is the only artifact-producing requirement; collapsing yields a one-criterion gate satisfied by prose alone. Logical entailment was real but operational dynamics inverted. — *Revision Disposition 2.*
- **Withdrew Rec 4 (exemplar/tolerated tiering)** — practitioner's contradiction #2 nailed it: tiering "tolerated" principles unilaterally pre-litigates migration without the migration spec the prospective-only clause requires, handing future authors a procedural cudgel. — *Revision Disposition 4.*
- **Withdrew Rec 6 (auto-reclassification deadline)** — "auto-anything in governance is a contradiction with the rest of the amendment process." — *Revision Disposition 6.*
- **Withdrew Rec 7 (vocabulary-novelty test)** — both cross-reviewers demonstrated it would reject legitimately distinct principles whose distinctness lies in the predicate, not the vocabulary. — *Revision Disposition 7.*
- **Withdrew Rec 9 (periodic re-evaluation)** — practitioner's tension #3 noted constitutions earn authority by NOT being re-litigated every cycle; triennial-style audits invite continual debate. — *Revision Disposition 9.*

### skeptic-cross-principle

- **Withdrew Rec 1 (merge criterion 3 into XI)** — practitioner's contradiction #2 caught a genuine error: the proposed XI extension would convert XI from a *data-duplication* principle (its origin: MODE_PRESENCE / FR-018, detectable by parity tests) into a *prose-duplication* principle, which is exactly the unverifiable kind of rule the gate is meant to exclude. — *Revision Disposition 1.*
- **Withdrew Rec 10 (remove gate; fold criterion 1 into XII)** — folding into XII would weaken XII (XII's origin is dead variables/Pydantic fields, not constitutional rules); conceptual stretch too far. — *Revision Disposition 10.*
- **Revised Rec 4 (grandfathering)** — softened from open-ended audit to tiered classification + v3.0.0 audit for migration-candidates only, reflecting practitioner's contradiction #3 that combining a time-boxed audit with a permanent footnote produces contradictory posture. (Still disputed; see Remaining Disputes §1.) — *Revision Disposition 4.*

### practitioner

- **Withdrew Rec 3 (delete Criterion 1)** — SCP's contradiction #1 demonstrated Criterion 1 is the only criterion that adds something the constitution does not already encode; deleting it inverts the gate's value proposition. — *Revision Disposition 3.*
- **Withdrew Rec 6 (footnote disclaiming X/XVI/IX-prose as precedent)** — both skeptics flagged this as worse than the disease: optimizes for amendment-author UX at the cost of constitutional coherence; codifies a permanent two-tier constitution that contradicts XI's anti-duplication logic and the prospective-only carve-out's purpose. — *Revision Disposition 6.*
- **Withdrew Rec 9 (body-bloat threshold)** — SCP's contradiction #3 was sharper than initially credited: the "more than one paragraph" threshold is itself unfalsifiable, the trap Criterion 2 was meant to prevent, and re-opens the door Criterion 3 was designed to close. — *Revision Disposition 9.*

### Net concessions across deliberation

Nine of thirty original recommendations withdrawn; eight modified under cross-review pressure. Three new recommendations added that fold in cross-reviewers' contributions where originals were too aggressive or under-specified. Convergence achieved on enforcement mechanism, artifact requirement, maintainer role, and structural simplicity rejection. Three substantive disputes survive — all on the gate (in scope for spec 069), none requiring arbitration since each has a clear synthesizer-recommended resolution path.
