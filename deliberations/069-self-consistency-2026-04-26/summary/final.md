# Spec 069 Self-Consistency Synthesis — Constitutional Inclusion Criteria (v2.4.0)

**Methodology**: cooperative self-consistency, single round, 3 agents (governance-skeptic, strictness-skeptic, practitioner). Subject arbitration to follow.
**Target**: `/Users/business-daddy/code/payer-index-mono/conversus-oss/deliberations/069-self-consistency-2026-04-26/CONSTITUTION-v2.4.0-candidate.md`

---

### Process Summary

- **Agents**: 3 (governance-skeptic, strictness-skeptic, practitioner).
- **Total artifacts**: 15 (3 reviews + 6 cross-reviews + 3 revisions + 3 disputes).
- **Per-phase counts**: Phase 1 = 3 reviews, Phase 2 = 6 cross-reviews, Phase 3 = 3 revisions, Phase 4 = 3 disputes.
- **Recommendations proposed (Phase 1)**: 30 (governance-skeptic 10 + strictness-skeptic 10 + practitioner 10).
- **Withdrawn at Phase 3**: 3 (governance-skeptic R4 fixed-taxonomy, governance-skeptic R6 override path, practitioner R4 PATCH carve-out).
- **Modified at Phase 3**: ~14 across the three revisions (notable: governance-skeptic R2/R3/R5/R7/R8; strictness-skeptic R1/R3/R5/R7/R9/R10; practitioner R1/R2/R3/R5/R7/R8/R9/R10).
- **Surviving unchanged**: ~9 (governance-skeptic R1/R9/R10; strictness-skeptic R6/R8; practitioner R6 strengthened).
- **Newly added at Phase 3**: 8 (governance-skeptic NR-1/NR-2; strictness-skeptic R-11/R-12/R-13; practitioner NR-1/NR-2/NR-3).
- **Disputes remaining after Phase 4**: 3 (criterion-1 AND-coupling vs. partial-OR; verification-deliberation acceptance bar; precedent-log authority/build-moment). A fourth narrower dispute (Sync Impact Report grandfathering disclosure as load-bearing) is held by strictness-skeptic alone but the substance largely converged.
- **Convergence points**: 5 unanimous (subsection lift, v2.4.0 Sync Impact Report, PATCH-carveout-replaced-by-N/A, fixed-taxonomy withdrawal, gate→XVII cross-link); plus a strictness-skeptic-introduced unanimous fix on `AGENTS.md` replacing `CONTRIBUTING.md`.

---

### Recommendation Scorecard

| # | Agent | Recommendation | P1 Priority | P3 Disposition | Challenged By | Convergence | Final Status |
|---|---|---|---|---|---|---|---|
| 1 | governance-skeptic | Lift gate to subsection | P1 | Surviving | none | unanimous | Accepted |
| 2 | governance-skeptic | Wire gate via SIR self-assessment | P1 | Modified (add CI lint) | strictness DC-2; practitioner T-2 | partial | Accepted-Modified |
| 3 | governance-skeptic | Define extension semantics (subject to gate) | P1 | Modified (subset-of-scope carve-outs) | strictness DC-1; practitioner T-1 | flexibility | Disputed-flex |
| 4 | governance-skeptic | Tighten criterion 1 with fixed taxonomy | P2 | Withdrawn | strictness DC-3; practitioner DC-1 | unanimous | Rejected |
| 5 | governance-skeptic | 80/20 burden-of-proof tie-breaker for crit. 3 | P2 | Modified (cleanliness wording) | strictness T-3; practitioner T-3 | partial | Accepted-Modified |
| 6 | governance-skeptic | Documented override path (≥3 agents) | P2 | Withdrawn | practitioner DC-2; strictness T-4 | unanimous | Rejected |
| 7 | governance-skeptic | Harmonize MUST/SHOULD/MAY in Governance | P2 | Modified (scale, don't exempt) | practitioner DC-3 | converged | Accepted-Modified |
| 8 | governance-skeptic | Versioning sub-bullet (extension = MINOR) | P3 | Modified (consumer-impact discriminator) | strictness DC-4; practitioner T-3 | converged | Accepted-Modified |
| 9 | governance-skeptic | Disambiguate `SKILL.md` from operational guidance | P3 | Surviving | none | endorsed | Accepted |
| 10 | governance-skeptic | Cross-reference Principle XVII (gate→XVII) | P3 | Surviving | none (direction confirmed) | unanimous | Accepted |
| 11 | governance-skeptic | NR-1: retrospective calibration trigger (≥3 rejections) | new | Added | strictness R-10 (compatible) | converged | Accepted |
| 12 | governance-skeptic | NR-2: add v2.4.0 Sync Impact Report | new | Added | none | unanimous | Accepted |
| 13 | strictness-skeptic | R-1: AND→partial-OR on crit. 1/3 (crit. 2 required) | high | Kept w/ revision | governance DC-1; practitioner NR-1 | DISPUTED | Disputed |
| 14 | strictness-skeptic | R-2: weaken crit. 1 sketch (admit peer-review rubric) | high | Kept w/ qualifier | governance DC-3; practitioner T-3 | partial | Disputed |
| 15 | strictness-skeptic | R-3: meta-principle carve-out → closed list | medium | Modified (closed list VI/X/XVI/XVII/XVIII) | practitioner DC-2 (against open class) | partial | Disputed |
| 16 | strictness-skeptic | R-4: criterion 3 "cleanliness" qualifier | medium | Kept; compatible w/ governance 80/20 | governance T-3 | converged | Accepted-Modified |
| 17 | strictness-skeptic | R-5: calibrate ≥90% retroactive admission | medium | Modified (≥85%, sunset at v3.0.0) | practitioner DC-3 | partial | Accepted-Modified |
| 18 | strictness-skeptic | R-6: retrospective review at each MINOR | medium | Surviving | none | unanimous | Accepted |
| 19 | strictness-skeptic | R-7: form/behavioral split | medium | Folded into R-3 closed list | practitioner DC-2 | partial | Disputed |
| 20 | strictness-skeptic | R-8: define promotion path | medium | Surviving | none | unanimous | Accepted |
| 21 | strictness-skeptic | R-9: criterion-1 sketch-OR-named-rubric | medium | Kept, sharpened | governance T-4 | converged | Accepted-Modified |
| 22 | strictness-skeptic | R-10: gate falsifiable (auto-loosen after 3 incidents) | medium | Modified (sequenced behind override frequency) | governance DC-2 | converged | Accepted-Modified |
| 23 | strictness-skeptic | R-11 (new): SIR enumerate grandfathered failures | new | Added | none | unanimous on substance | Accepted |
| 24 | strictness-skeptic | R-12 (new): lift to subsection | new | Added | none | unanimous (matches governance R1) | Accepted |
| 25 | strictness-skeptic | R-13 (new): replace `CONTRIBUTING.md` w/ `AGENTS.md` | new | Added | none | unanimous | Accepted |
| 26 | practitioner | R1: self-assessment template w/ worked examples | high | Amended (host in SIR; 3 examples) | strictness T-1; governance T-1 | partial | Accepted-Modified |
| 27 | practitioner | R2: CI lint requiring template | high | Amended (form-only, accept N/A) | strictness DC-1 | converged | Accepted-Modified |
| 28 | practitioner | R3: routing table for op-guidance destinations | high | Amended (5-way + constitutional remand) | strictness T-2; governance T-4 | partial | Accepted-Modified |
| 29 | practitioner | R4: PATCH carve-out from self-assessment | high | Withdrawn | governance DC-1; strictness DC-3 | unanimous | Rejected |
| 30 | practitioner | R5: mandatory verification deliberation w/ zero disputes | high | Amended (documented-disputes bar) | governance DC-2; strictness DC-2 | DISPUTED | Disputed |
| 31 | practitioner | R6: add v2.4.0 Sync Impact Report | medium | Strengthened (enumerate failures) | none | unanimous | Accepted |
| 32 | practitioner | R7: rewrite criterion 2 "interpretation" wording | medium | Adopted w/ extension (XV/XXVII coordination) | strictness T-4 | converged | Accepted-Modified |
| 33 | practitioner | R8: precedent log at deliberations/governance-decisions.md | medium | Amended (derived index) | governance T-4 | DISPUTED (build moment) | Disputed |
| 34 | practitioner | R9: expedited security/regulatory path | medium | Amended (rollback authority) | governance DC-3 | converged | Accepted-Modified |
| 35 | practitioner | R10: cross-link XVII | medium | Amended (direction reversed: gate→XVII) | governance DC-4 | unanimous | Accepted-Modified |
| 36 | practitioner | NR-1: evidence-triggered crit. 1 calibration | new | Added | strictness (rejects deferral) | DISPUTED (alt to R-1) | Disputed |
| 37 | practitioner | NR-2: 14-day amendment cooling-off | new | Added | none direct | weak | Accepted-Flex |
| 38 | practitioner | NR-3: panel-composition disclosure | new | Added | none direct | converged | Accepted |

---

### Dangerous Contradictions Found

#### Resolved Contradictions

1. **Governance-skeptic's fixed check-type taxonomy (R4) vs. strictness-skeptic's R-2 / practitioner's velocity concern.** Resolved by unanimous withdrawal at Phase 3. Governance-skeptic conceded that the enumerated taxonomy (CI lint, parity test, structural assertion, schema validation, contract test, meta-test) baked in a behavioral bias against form/taste-level principles. Substance preserved by retaining the substantive sketch requirement inside the SIR self-assessment without the closed taxonomy.
2. **Practitioner's PATCH carve-out (R4) vs. governance-skeptic's bypass concern + strictness-skeptic's structural-backwardness concern.** Resolved by unanimous withdrawal. Replaced with "N/A — typo fix / cross-reference update" as a permitted answer in the SIR self-assessment, scaling cost to materiality without exempting a version-bump class.
3. **Governance-skeptic's documented override path (R6) vs. practitioner's "≥3 converged agents IS the normal pattern."** Resolved by withdrawal. Practitioner's observation that every existing principle was ratified by converged deliberation made the override criterion a tautology. Recalibration moved to retrospective triggers (NR-1 / R-6 / R-10 sequenced).
4. **Practitioner's R10 (XVII→gate cross-reference direction) vs. governance-skeptic's reference-topology argument.** Resolved by direction reversal at Phase 3. The constitution's reference topology flows newer→older; cross-link now goes gate→XVII.
5. **Practitioner's R5 zero-disputes bar vs. both reviewers' panel-composition / variance-lock-in critiques.** Practitioner amended to "documented-disputes" bar; governance-skeptic disputes this further (see Unresolved). Strictness-skeptic accepts the documented form, citing it favorably as SA-2.

#### Unresolved Contradictions

1. **Theory-first structural loosening (strictness R-1 + closed list) vs. evidence-first deferral (governance + practitioner NR-1).** Synthesizer assessment: this is the deepest substantive disagreement and is genuinely two different theories of what the gate IS. Strictness-skeptic treats grandfathering as evidence the gate is mis-calibrated NOW; the other two treat grandfathering as a stability mechanism with retrospective recalibration. Both positions are coherent; they cannot both fully land. Practitioner's NR-1 has independent support (governance-skeptic NR-1 is structurally identical), tipping the cooperative balance toward evidence-triggered loosening — but strictness-skeptic's closed-list narrowing of R-3 is a real concession that should be acknowledged in the resolution.
2. **Substantive zero-disputes bar (governance) vs. documented-disputes bar (practitioner + strictness implied).** Synthesizer assessment: governance-skeptic's narrow unanimous-out-of-scope escape hatch is a genuine compromise position that nobody else proposed. Practitioner's evidentiary argument (one example of zero-disputes catching a v2.3.1 bug; zero examples of documented-with-rationale catching a bug) is asymmetric but governance-skeptic's reading of Principle V's scope (output validation, not amendment process) is also defensible.
3. **Precedent-log build-moment specification.** Synthesizer assessment: this is the smallest of the three remaining disputes and has a clean cooperative path — practitioner's "derived from SIRs" + governance-skeptic's "rebuild at every MINOR/MAJOR amendment's PR-time CI" composes naturally. Both reviewers explicitly flagged compatibility; the dispute is about whether v2.4.0 specifies the build moment or leaves it to follow-up tooling work.

---

### Systemic Contradictions

1. **Pattern: enforcement-versus-calibration sequencing collision.**
   - **Manifests in**: practitioner R2 (CI lint) vs. strictness DC-1 ("hard enforcement before recalibration cements the wrong gate"); governance R2 (SIR self-assessment) vs. strictness DC-2 ("amplifies miscalibration into procedural force").
   - **Root cause**: two of three reviewers (governance + practitioner) treat enforcement as the missing piece; one (strictness) treats calibration as the missing piece. They optimize for different failure modes.
   - **Implication**: any synthesis that adopts both enforcement and calibration mechanisms must sequence them so enforcement targets only the form (lint accepts N/A) while substance flexibility comes from retrospective triggers — which is approximately where Phase 3 landed.

2. **Pattern: open-class category proliferation as gate-evasion.**
   - **Manifests in**: strictness R-3 / R-7 (meta-principle, form constraint) attacked by practitioner DC-2 (open-class becomes laundry path); governance R-5 (80/20 quantification) attacked by strictness T-3 / practitioner T-3 (numeric thresholds create new litigation).
   - **Root cause**: every attempt to fix criterion vagueness by introducing a new category creates a new vagueness at the category boundary.
   - **Implication**: closed enumerations (strictness's revised R-3 closed list) and operational tests (governance's revised R-5 "runtime-inferred coordination") are more robust than parametric categories — the synthesis trends in this direction.

3. **Pattern: aspirational governance language without forcing function.**
   - **Manifests in**: original gate's "MUST" verbs without enforcement hook (all three reviewers flag); practitioner R5 zero-disputes (engineerable via panel composition); governance R6 override (satisfied by definition). Multiple instances of "the gate says X but nothing makes X happen."
   - **Root cause**: the constitution describes contracts but lacks a procedural surface for amendment-time enforcement.
   - **Implication**: every "MUST" added to the gate needs a paired mechanical or procedural artifact (lint, SIR section, build step). The Phase 3 convergence on form-only CI lint + SIR self-assessment is the cooperative outcome of three independent diagnoses of this pattern.

4. **Pattern: grandfathering as disputed evidence.**
   - **Manifests in**: strictness MO-5 ("calibration confession") vs. governance Alignment 4 ("correctly scoped") vs. practitioner Alignment 2 ("usable boundary").
   - **Root cause**: the same artifact (3 of 27 principles fail the new gate) admits three different readings. Strictness reads it as a bug; the others read it as feature.
   - **Implication**: the unanimous convergence on enumerating these failures in the v2.4.0 SIR (governance NR-2, strictness R-11, practitioner R6 strengthened) is not just hygiene — it is the deliberation's mechanism for letting future authors confront the evidence directly without committing to one reading at amendment time.

5. **Pattern: extensions as the most-exploitable surface.**
   - **Manifests in**: governance-skeptic flagged it explicitly (R3); practitioner did not address it (governance flagged practitioner's blind spot in cross-review); strictness raised the inverse risk (extensions face a freeze).
   - **Root cause**: the gate's grandfathering boundary draws a line at v2.4.0, but the existing extension mechanism (Extension/Clarification headers in principle bodies) routes around the line.
   - **Implication**: the synthesis must treat extensions as gate-bound but with subset-of-scope carve-outs (governance R3 modified) so legitimate refinements aren't frozen. This is partially resolved but listed as Flexibility in disputes.

---

### Convergence Achieved

Ordered by strength of agreement:

1. **Lift gate to its own subsection (`### Constitutional Inclusion Criteria`).** All three agents independently and unanimously. Evidence: governance-skeptic R1 (P1, surviving), strictness-skeptic R-12 (newly added in revision but matches), practitioner SA-3 / Phase 2 endorsement. Pre-existing: convergent across reviews; not earned through dispute.

2. **Add v2.4.0 Sync Impact Report at top of file with grandfathered-failures enumeration (VI, X, XVI per spec 069 §5).** Unanimous, with strictness-skeptic adding the explicit grandfathering disclosure as load-bearing. Evidence: governance-skeptic NR-2, strictness-skeptic R-11, practitioner R6 strengthened. Pre-existing on adding the SIR; earned on enumerating failures (strictness escalation accepted by both other agents).

3. **Withdraw fixed check-type taxonomy from criterion 1.** Unanimous withdrawal at Phase 3. Evidence: governance-skeptic withdrew R4; strictness-skeptic DC-3 against; practitioner DC-1 against. Earned through Phase 2 cross-reviews.

4. **Replace PATCH carve-out with lightweight "N/A — typo fix" answer in SIR self-assessment.** Unanimous. Evidence: practitioner withdrew R4; governance-skeptic R7 modified ("scale, don't exempt"); strictness-skeptic DC-3 (anti-PATCH-carveout). Earned through cross-reviews.

5. **Cross-link gate→XVII (newer-references-older direction).** Unanimous after practitioner accepted governance-skeptic's reference-topology correction at Phase 3. Evidence: governance-skeptic R10 (surviving), strictness-skeptic SA-4, practitioner R10 amended. Earned (direction was contested and resolved).

6. **Replace `CONTRIBUTING.md` with `AGENTS.md` in operational-guidance routing.** Unanimous in the disputes/convergence sections of Phase 4 (practitioner explicitly adopts strictness's R-13; governance-skeptic doesn't object). Evidence: strictness-skeptic R-13, practitioner Convergence 5 in disputes. The candidate text references a file that does not exist; Principle XVII routes contribution rules to `AGENTS.md`. Earned in Phase 3 (only strictness flagged in revision; others accepted).

7. **Form-only CI lint with structured N/A acceptance.** Strong convergence with one open detail. Evidence: practitioner R2 amended; governance-skeptic R2 modified (two enforcement surfaces, lint enforces form); strictness-skeptic R-9 sharpened (rubric must be specifically named). Earned through cross-review.

8. **Verification deliberation as a practice (not the bar question).** All three agree some verification mechanism should run on amendments; they only dispute the merge bar. Evidence: practitioner R5 amended; strictness-skeptic accepted documented form (SA-2); governance-skeptic non-negotiable on substantive bar but agrees mechanism is needed. Earned partial.

---

### Arbiter-Resolved Disputes (Prior Rounds)

N/A — single round.

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes

#### Dispute: Criterion 1 AND-coupling vs. partial-OR substitution

- **Positions**:
  - **Strictness-skeptic** (Non-Negotiable 1): require criterion 2 AND criterion 3, with criterion 1 substitutable via mechanical sketch OR peer-review-rubric operationalization. Bound by closed list of relaxed-criterion-1 principles tied to existing VI, X, XVI, XVII, XVIII; expansion of the list itself requires a future MINOR amendment.
  - **Governance-skeptic** (Non-Negotiable 1): retain AND-coupling unchanged from candidate v2.4.0. Pair with retrospective calibration triggers (NR-1) keyed to ≥3 criterion-1-only rejections within a MAJOR cycle.
  - **Practitioner** (NR-1, Dispute 1): reject strictness's structural restructure as "theory-first loosening that imports new vagueness"; adopt evidence-triggered calibration via the derived precedent log. Closed-list freezes special-case status at v2.4.0 without empirical evidence.
- **Arguments**:
  - Strictness: gate as drafted excludes the form-constraint / taste-level / meta-principle category by construction; rejecting 3 of 27 grandfathered principles is structural failure visible in the document; the trigger threshold (≥3) is set above the historical reject-on-this-criterion rate so retrospective triggers cannot fire fast enough; cost per rejection is multi-week.
  - Governance: closed list is "an admission that we cannot articulate the category in a forward-applicable way" — tautological ("form constraint" = "one of {VI, X, XVI, XVII, XVIII}"). The grandfathering clause already absorbs corpus asymmetry; loosening structurally before evidence accumulates substitutes theory for evidence.
  - Practitioner: closed list creates a two-tier constitution (special-case principles vs. all future principles); evidence-triggered loosening produces the same outcome (criterion 1 loosens when evidence accumulates) without freezing the special-case list at amendment time; strictness-skeptic's R-1 violates strictness-skeptic's own R-5 sequencing principle.
- **Synthesizer assessment**: 2-versus-1 cooperative balance favors evidence-triggered deferral, but the 1 (strictness) holds the only argument that engages the empirical evidence (3 of 27 fail) directly. Strictness-skeptic's closed-list narrowing is a real concession from the open-class R-3/R-7. Practitioner's NR-1 trigger threshold (≥3) is genuinely higher than the historical rejection rate — strictness's "fires too late" point is correct on its own terms. Both governance-skeptic and practitioner have parallel retrospective triggers (governance NR-1, practitioner NR-1, strictness R-10 sequenced) which suggests the recalibration mechanism itself is converged; the dispute is whether to ALSO take a structural step now.
- **Recommended resolution**: arbiter to choose between (a) ship gate with AND-coupling unchanged + adopt all three retrospective triggers (governance + practitioner) as the cooperative majority outcome, or (b) ship gate with strictness's revised closed-list partial-OR (criterion 2 AND 3 required, criterion 1 substitutable via rubric for the closed list only) PLUS retrospective triggers, with sunset at v3.0.0. Option (a) preserves substantive AND-coupling; option (b) addresses the empirical 3-of-27 evidence directly. Practitioner explicitly marks acceptance of (b) with sunset annotation as Flexibility F-1.

#### Dispute: Verification deliberation acceptance bar — substantive zero-disputes vs. documented-disputes

- **Positions**:
  - **Governance-skeptic** (Non-Negotiable 2): substantive zero unresolved disputes from the verification panel before merge, with a narrow unanimous-out-of-scope escape hatch (disputes that the panel unanimously categorizes as out-of-scope for this amendment). Panel-composition disclosure (practitioner NR-3) supplies the gameability mitigation.
  - **Practitioner** (R5 amended, Dispute 3): "every dispute has either been incorporated into the amendment or documented in the Sync Impact Report with a rationale for non-incorporation." Avoids single-veto failure modes consistent with Principle V's "warnings, not blocks" stance.
  - **Strictness-skeptic** (SA-2, Convergence 3 in disputes): implicitly endorses practitioner's documented-disputes bar via SA-2.
- **Arguments**:
  - Governance: zero-disputes preserves substantive bug-catching contract; documented-disputes converts it into procedural audit-trail contract; v2.3.1 evidence is asymmetric (one zero-disputes catch, zero documented-disputes catches); Principle V governs output validation not amendment process; "documented in SIR" reliably converges to "ignored after 90 days." Panel-composition disclosure (NR-3) defangs gameability without weakening the bar.
  - Practitioner: zero-disputes is engineerable via panel composition; single-veto failure modes are anti-democratic; documented-disputes preserves accountability without creating a chokepoint; one v2.3.1 datapoint is insufficient to claim asymmetric evidence.
  - Strictness: zero-disputes "locks in deliberating agents' disposition"; variance-reducer not bug-catcher.
- **Synthesizer assessment**: 1-versus-2 against governance-skeptic on the headline question, but governance-skeptic's narrow unanimous-out-of-scope escape hatch is a meaningful synthesis position nobody else proposed. Practitioner's Flexibility F-3 (verification deliberation can move to v2.5.0) is an alternative resolution path that defers the dispute entirely.
- **Recommended resolution**: arbiter chooses between (a) documented-disputes bar with panel-composition disclosure (cooperative majority), (b) substantive zero-disputes bar with governance-skeptic's unanimous-out-of-scope escape hatch (governance position), or (c) defer verification deliberation codification to v2.5.0 (practitioner F-3). Option (a) tracks the majority and the v2.3.1 evidence asymmetry is single-datapoint; option (b) preserves bug-catching for amendment-introduced defects; option (c) reduces v2.4.0 scope.

#### Dispute: Precedent log — derived index vs. authoritative log; build-moment specification

- **Positions**:
  - **Practitioner** (R8 amended, Dispute 2): derived index built on demand from each amendment's SIR self-assessment by the speckit pipeline; constitution does not maintain it. Treats log as load-bearing infrastructure that should be referenced explicitly in gate text.
  - **Governance-skeptic** (Dispute on precedent-log build-moment): SIR self-assessment is authoritative; precedent log is a derived index, but the operational question of WHO runs the build and WHEN is unspecified in all three Phase 3 revisions. Proposes the rebuild MUST run as part of every MINOR/MAJOR amendment's PR-time CI alongside the form-check lint.
  - **Strictness-skeptic** (SA-2 endorsement): pairs log with retrospective review at each MINOR; implies log is queried at MINOR amendments specifically.
- **Arguments**:
  - Practitioner: gate text should reference the log explicitly so its construction is mandatory not optional; without that, recalibration triggers (mine, governance-skeptic's, strictness's R-10) have no source data.
  - Governance: "rebuilt on demand" is operationally underspecified — without designated owner and build moment, the log might not exist when the calibration trigger fires; CI step at every MINOR/MAJOR amendment writes the rebuilt log to `deliberations/governance-decisions.md` as a build artifact, makes it visible in PR diff, and triggers recalibration automatically.
  - Strictness: aligns with both — "rebuild at each MINOR" matches retrospective-review pairing.
- **Synthesizer assessment**: this is the smallest of the three remaining disputes and has a clean cooperative path. All three positions are compatible; the disagreement is whether v2.4.0 specifies the build moment explicitly or leaves it to follow-up tooling. Practitioner explicitly flagged "rebuilt on demand by speckit pipeline" but did not specify a triggering CI step; governance-skeptic's specification fills that gap without disagreeing on substance.
- **Recommended resolution**: adopt practitioner's derived-index design + governance-skeptic's explicit CI-build-moment specification (rebuild runs at every MINOR/MAJOR amendment's PR-time CI, output to a designated path, visible in PR diff, triggers recalibration when ≥3-on-same-criterion threshold met). Strictness's retrospective-review-at-MINOR pairing is a natural consequence and need not be separately codified.
<!-- CONVERSUS:DISPUTES_END -->

---

### Actionable Spec Changes

#### P1 — required for v2.4.0 merge

1. **Lift gate to subsection.** Promote the new "Constitutional Inclusion Criteria" content from a third bullet under §Governance to a sibling subsection `### Constitutional Inclusion Criteria`. Source: governance-skeptic R1, strictness-skeptic R-12, practitioner SA-3.

2. **Add v2.4.0 Sync Impact Report at top of file with grandfathering disclosure.** Insert a new SIR block above the existing v2.3.0→v2.3.1 block. The new block MUST contain (a) version-bump rationale (the new gate), (b) reflexive self-assessment of the gate against its own three criteria, and (c) explicit enumeration of grandfathered principles (per spec 069 §5: VI, X, XVI) that fail under each criterion, with one-sentence justification per principle. Source: governance-skeptic NR-2, strictness-skeptic R-11, practitioner R6 strengthened.

3. **Replace `CONTRIBUTING.md` with `AGENTS.md`.** In line 896 (operational-guidance destination list), substitute `AGENTS.md` for `CONTRIBUTING.md`. The latter does not exist in this repo and contradicts Principle XVII's content classification. Source: strictness-skeptic R-13, practitioner Convergence 5.

4. **Withdraw fixed check-type taxonomy.** Do NOT add the (CI lint, parity test, structural assertion, schema validation, contract test, meta-test) enumeration to criterion 1. The substantive sketch requirement is preserved by the SIR self-assessment without taxonomy. Source: governance-skeptic R4 withdrawn, strictness-skeptic DC-3, practitioner DC-1.

5. **Withdraw PATCH carve-out; add N/A acceptance to self-assessment.** No version-bump-class exemption from the gate. The SIR self-assessment MUST accept "N/A — typo fix / cross-reference update / wording refinement" as a valid one-line answer for amendments that don't add or redefine principles. Source: practitioner R4 withdrawn, governance-skeptic R7 modified, strictness-skeptic DC-3.

6. **Add SIR self-assessment requirement.** Amend the §Amendments bullet (or new subsection) to require that amendments proposing a new principle or extension to an existing principle MUST include an "Inclusion Criteria Self-Assessment" section in the Sync Impact Report addressing each of the three criteria. "N/A — justified because" is permitted per #5. Source: governance-skeptic R2 modified, practitioner R1 amended.

7. **Add form-only CI lint on amendment PRs.** A grep-based lint that fails the PR if the four required SIR sub-headings (Mechanical Verification, Falsifiable Scope, Distinctness, Routing Decision) are missing or empty. Substance evaluation remains reviewer work. Source: practitioner R2 amended, governance-skeptic R2 modified (mechanical-form half), strictness-skeptic R-9 sharpened.

8. **Cross-link gate→Principle XVII.** Add to the new subsection: "Constitutional Inclusion Criteria inherits Principle XVII's Content Classification vocabulary; routing decisions to operational guidance follow XVII's execution-logic vs. contribution-guidelines distinction." Direction is gate→XVII, not the reverse. Source: governance-skeptic R10, practitioner R10 amended (direction corrected).

9. **Fix criterion 2 wording.** Replace "without requiring 'interpretation'" with "the principle's wording MUST define its own scope and terms explicitly. A reviewer applying the principle to a hypothetical PR MUST be able to determine whether the principle applies without consulting external definitions. Application within scope MAY require judgment; scope determination MUST NOT." Add to criterion 3: "Coordination with an existing principle via explicit cross-reference (per the XV/XXVII pattern) is a permitted form of distinctness; near-duplication with no coordination is rejected." Source: practitioner R7 adopted with extension.

#### P2 — strongly recommended

1. **Define extension semantics with subset-of-scope carve-out.** Extensions to grandfathered principles ARE subject to the gate, with two carve-outs: (a) criterion 3 is automatically satisfied for an extension when the extension's scope is a strict subset of the host principle's scope and identifies the host sentence(s) it refines; (b) pure clarification headers ("Clarification (vN.N.N):") that add no new normative content require SIR rationale but not full self-assessment. Source: governance-skeptic R3 modified.

2. **Versioning sub-bullet on extensions.** "An extension that adds new normative content to an existing principle is MINOR ('material expansion'). An extension that only refines wording, adds cross-references, or clarifies scope without changing what the principle requires of consumers is PATCH ('clarification'). The classification is determined by consumer impact, not author intent — if a previously-passing artifact would now fail under the extension, the extension is MINOR." Source: governance-skeptic R8 modified.

3. **Distinctness tie-breaker.** Replace candidate text on criterion 3 with: "When distinctness is contested, the amendment author MUST identify the existing principle(s) closest to the proposed scope and EITHER (a) demonstrate that composition of those principles cannot produce the same operational guarantee without runtime-inferred coordination, OR (b) propose the principle as an extension of the closest existing principle. If neither option is satisfied, the amendment is not yet ready for the gate." Source: governance-skeptic R5 modified, strictness-skeptic R-4 compatible.

4. **Retrospective calibration trigger.** Add to the new subsection: "If three or more proposed principles are rejected by this gate within a single MAJOR version cycle, the next MINOR amendment MUST include a calibration review of the rejections — concretely, evaluating whether the rejected proposals would have been admitted under the gate's intended bar, and proposing gate-text revisions if the rejection rate exceeds the gate's intended discrimination." Source: governance-skeptic NR-1, practitioner NR-1, strictness-skeptic R-6 / R-10.

5. **Disambiguate `SKILL.md` from operational guidance.** Add parenthetical noting that `SKILL.md` content is runtime-enforced; placing a rule there strengthens it relative to the constitution's descriptive prose. Source: governance-skeptic R9 surviving.

6. **Define promotion path symmetric to demotion.** Operational guidance items MAY be promoted to constitutional principles if they (a) are cited as authoritative in three or more specs, (b) survive a deliberation review, and (c) pass the inclusion gate. Promotion requires the same MINOR amendment process as new principles. Source: strictness-skeptic R-8 surviving.

7. **Expedited path with rollback authority.** Amendments responding to security disclosures, license-compliance issues, or regulatory changes MAY merge without verification deliberation pre-merge but MUST trigger a verification deliberation within 14 days post-merge with explicit rollback authority — verification findings of material issues automatically revert the expedited amendment. Source: practitioner R9 amended.

8. **Panel-composition disclosure.** Every SIR for MINOR or MAJOR amendments MUST document (a) personas/agents in the proposal deliberation, (b) personas/agents in the verification deliberation (which MUST differ from the proposal panel by ≥1 persona), (c) any persona that recused or was recused. Source: practitioner NR-3.

9. **Derived precedent log with explicit build moment.** A precedent log derived from per-amendment SIR self-assessments, rebuilt as part of every MINOR/MAJOR amendment's PR-time CI; output as a build artifact visible in the PR diff; triggers recalibration when ≥3 rejections on same criterion. Source: practitioner R8 amended + governance-skeptic dispute resolution.

#### P3 — nice-to-have

1. **Calibration target with sunset.** Adopt strictness-skeptic R-5 modified: "the gate is calibrated such that it would admit at least 85% of the grandfathered principles I-XXVII if applied retroactively; the calibration target sunsets at v3.0.0." Acceptable in [80%, 90%] band. Source: strictness-skeptic R-5 with practitioner DC-3 concession.

2. **14-day amendment cooling-off.** MINOR amendments adding new principles sit at PR stage for 14 calendar days minimum after verification deliberation completes. Source: practitioner NR-2 (Flexibility F-2 — drop if NR-3 lands).

3. **Routing table for operational-guidance destinations.** Five-way decision tree (per practitioner R3 amended) with explicit "constitutional remand" branch for form constraints/meta-principles that don't fit any operational-guidance destination cleanly. Source: practitioner R3 amended.

---

### Key Concessions

**Governance-skeptic conceded**:
- Withdrew R4 (fixed check-type taxonomy) on Phase 3, explicitly crediting strictness-skeptic for the withdrawal. Reason: enumerated taxonomy bakes behavioral bias against form/taste-level principles; Principle X "Zen of Python Output" cannot satisfy any taxonomy entry.
- Withdrew R6 (override path) on Phase 3, accepting practitioner DC-2 ("≥3 converged agents IS the normal pattern"). Reason: override criterion is satisfied by definition for any principle reaching the constitution; override would not function as override but as default.
- Modified R2 to add CI lint surface (originally only proposed SIR self-assessment). Reason: practitioner T-2 correctly identified that SIR carries substance but cannot be mechanically enforced; lint enforces form, reviewer audits substance.
- Adopted practitioner NR-3 (panel-composition disclosure) into Flexibility 2 of disputes. Reason: NR-3 directly addresses the gameability critique that motivated governance's own dispute on the verification-deliberation acceptance bar.

**Strictness-skeptic conceded**:
- Modified R-3 / R-7 from open-class "meta-principle" / "form constraint" categories to a closed list (VI, X, XVI, XVII, XVIII). Reason: practitioner DC-2 correctly flagged that open classes import the very vagueness criterion 2 prohibits and become a laundry path.
- Modified R-5 from ≥90% to ≥85% retroactive admission target with v3.0.0 sunset. Reason: practitioner DC-3 identified one-way ratchet (calibrating to a corpus authored under looser standards encodes those standards forever).
- Modified R-10 from incident-keyed loosening to override-frequency-keyed loosening. Reason: governance-skeptic DC-2 correctly identified that per-amendment override fires first, preventing R-10's incident counter from ever reaching three; sequencing them resolves the redundancy.
- Sharpened R-9 (rubric must be specifically named, not generic). Reason: practitioner T-4 correctly flagged that OR-of-OR construction makes criterion 1 trivially satisfiable.

**Practitioner conceded**:
- Withdrew R4 (PATCH carve-out) on Phase 3. Reason: governance-skeptic DC-1 (exploitable bypass via PATCH reclassification) and strictness-skeptic DC-3 (structurally backward — relaxes the gate where it does no work) converged from independent angles. Replacement: "N/A — justified because" branches in SIR self-assessment.
- Amended R5 from zero-disputes to documented-disputes acceptance bar. Reason: governance-skeptic DC-2 (engineerable via panel composition) and strictness-skeptic DC-2 (variance-reducer locks in disposition). Maintains a residual dispute (governance-skeptic still prefers substantive zero-disputes with narrow escape hatch).
- Amended R10 cross-link direction (XVII→gate to gate→XVII). Reason: governance-skeptic DC-4 — the constitution's reference topology flows newer→older.
- Amended R2 CI lint to form-only (originally proposed full template enforcement). Reason: strictness-skeptic DC-1 correctly identified that hardening a mis-calibrated gate before calibration debate resolves creates a one-way ratchet.
- Conceded R-1 closed-list as Flexibility F-1 (acceptable if Dispute 1 cannot be resolved by evidence-triggered loosening). Reason: closed list is worse than evidence-triggered but better than no provision for form-constraint and meta-principle categories.
