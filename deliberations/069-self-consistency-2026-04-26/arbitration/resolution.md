# Spec 069 Self-Consistency Arbitration — Constitutional Inclusion Criteria (v2.4.0)

**Arbiter**: spec-069-arbiter
**Persona**: balanced-arbiter (impartial; weighs all perspectives equally; binding rulings grounded in declared principles)
**Subject**: `/Users/business-daddy/code/payer-index-mono/conversus-oss/deliberations/069-self-consistency-2026-04-26/CONSTITUTION-v2.4.0-candidate.md`
**Acceptance bar (per spec 067 §4.4)**: 0 ACCEPT-level findings on the spec 069 amendment specifically.

---

## Process Note

- **Trigger**: `always` — this arbitration runs unconditionally on the spec 069 self-consistency deliberation, not gated on a dispute-count threshold.
- **Disputes remaining (per Phase 5 synthesis)**: 3.
  1. Criterion 1 AND-coupling vs. partial-OR substitution.
  2. Verification deliberation acceptance bar — substantive zero-disputes vs. documented-disputes.
  3. Precedent log — derived index vs. authoritative log; build-moment specification.
- **Agents**: governance-skeptic, strictness-skeptic, practitioner.
- **Mode**: cooperative with subject arbitration. Each agent contributed reviews, cross-reviews, revisions, and disputes; the synthesis flagged the three above as load-bearing residuals. A fourth narrower issue (Sync Impact Report grandfathering disclosure as load-bearing) substantively converged in Phase 4 and is treated as part of the convergent P1 set, not as a remaining dispute requiring arbitration.
- **Scope**: rulings bind on the candidate v2.4.0 amendment as written; they do not bind on future amendments except through the text those rulings produce.

---

## Decision Framework

The following principles from the candidate v2.4.0 constitution bear directly on the three remaining disputes. Each is cited by line range in the candidate file.

- **[Spec-Implementation Parity (XIV)]**: Specs and implementations MUST agree on what was built; drift is a bug in the spec, not the implementation. (lines 391-413) — bears on whether the candidate file's missing v2.4.0 Sync Impact Report and `CONTRIBUTING.md` reference are spec defects.

- **[Single Source of Truth + Registry-First Declaration (XI)]**: Every piece of information has exactly one authoritative source; derived representations must not be maintained independently. (lines 298-322, 324-342) — bears on whether the precedent log is a duplicate authoritative artifact (XI violation) or a derived projection of per-amendment Sync Impact Reports (XI compliant).

- **[Observable Deliberation (V)]**: Every phase reports progress; output validation catches malformed results without silently swallowing errors; "Malformed output is better than no output." (lines 134-144) — bears on the verification-deliberation acceptance bar: V's "warnings, not blocks" stance governs *output validation*, not amendment process, but the underlying philosophy (preserve prior phase results, fail loud not silent) frames the dispute.

- **[Documentation Is the Product (IV)]**: SKILL.md and constitutional text carry the same weight as code; the constitution must be a single source of truth for governance behavior; agents must not rely on conventions not written in the document. (lines 118-132) — bears on whether the verification-deliberation requirement and precedent-log build moment must be codified textually or may be left to follow-up tooling.

- **[Constitutional Inclusion Criteria itself (Governance §)]**: Three criteria — mechanical verification capability, falsifiable scope, distinctness — applied prospectively; existing principles I-XXVII grandfathered; gate calibration is an explicit invariant of the constitution. (lines 872-905) — the subject of arbitration; the gate's own three criteria constrain what the arbiter may add to it.

- **[Versioning rule (Governance §)]**: MAJOR for principle removals/redefinitions, MINOR for new principles or material expansions, PATCH for clarifications. (lines 870-871) — bears on whether disputed elements (verification deliberation, precedent-log build moment) are MINOR-class additions (must land with v2.4.0 to avoid drift) or PATCH/follow-up class.

- **[Plugin Isolation (XV) + Operator-Configurable Tool Surface (XXVII) coordination pattern]**: Two principles bracket the registry's read/write contract via explicit cross-reference, not duplication. (lines 415-446, 791-825) — bears on Dispute 1: the XV/XXVII pattern is the constitution's own precedent for how legitimate refinements coordinate without freezing categorical lists.

---

## Binding Decisions

### Dispute: Criterion 1 AND-coupling vs. partial-OR substitution

**Positions:**
- **Strictness-skeptic** (Non-Negotiable 1): require criteria 2 AND 3, with criterion 1 substitutable via mechanical sketch OR named peer-review-rubric, bounded by a closed list (VI, X, XVI, XVII, XVIII). Argues the gate as drafted excludes form-constraint and taste-level principles by construction (3 of 27 grandfathered principles fail), and that the practitioner's evidence-triggered trigger threshold (≥3 rejections) sits above the historical reject-on-criterion-1 rate, so retrospective triggers fire too late.
- **Governance-skeptic** (Non-Negotiable 1): retain AND-coupling; pair with retrospective calibration triggers keyed to ≥3 rejections-on-criterion-1 within a MAJOR cycle. Argues a closed list operationalizes "form constraint" as "one of {VI, X, XVI, XVII, XVIII}" — a tautology, not a category — and that grandfathering already absorbs the corpus-asymmetry concern.
- **Practitioner** (NR-1): reject prospective categorical loosening; adopt evidence-triggered calibration via the derived precedent log. Closed-list freezes special-case status without empirical evidence and produces a two-tier constitution.

**Synthesizer's assessment** (quoted): "2-versus-1 cooperative balance favors evidence-triggered deferral, but the 1 (strictness) holds the only argument that engages the empirical evidence (3 of 27 fail) directly. Strictness-skeptic's closed-list narrowing is a real concession from the open-class R-3/R-7. Practitioner's NR-1 trigger threshold (≥3) is genuinely higher than the historical rejection rate — strictness's 'fires too late' point is correct on its own terms."

**Ruling:** **REJECT** strictness-skeptic's structural restructure (R-1 closed-list partial-OR). **ACCEPT** the convergent retrospective-calibration-trigger machinery (governance-skeptic NR-1 + practitioner NR-1, sequenced with strictness-skeptic R-10) — but that machinery is already on the convergent P2 list, not part of this dispute. v2.4.0 ships with AND-coupling unchanged.

**Grounding citation:** Constitutional Inclusion Criteria itself (criterion 2: falsifiable scope) + Single Source of Truth (XI).

**Rationale:** Strictness-skeptic's closed-list move makes the proposal weaker against criterion 2, not stronger. A closed enumeration of five existing principles operationalizes "form constraint" as "one of {VI, X, XVI, XVII, XVIII}" — which is precisely the scope vagueness the gate prohibits. The category cannot be defined forward; it can only be enumerated backward. Encoding that asymmetry as a partial-OR creates a category whose membership rule is "is one of the principles already in the list," which is tautological and runtime-uninferrable, exactly what criterion 2 rejects. Furthermore, the closed list violates Single Source of Truth: it duplicates information (which principles fail criterion 1) that the v2.4.0 Sync Impact Report's grandfathering disclosure already publishes — and once duplicated, the two will drift. The Sync Impact Report's enumeration (P1 #2 below) is the correct home for that evidence.

The strictness-skeptic empirical observation (3 of 27 fail) is accepted as evidence and made permanent by the SIR grandfathering disclosure. What is rejected is the structural concession to that evidence at amendment time. Retrospective calibration triggers (governance NR-1 + practitioner NR-1, P2 #4 below) are the constitution's mechanism for converting accumulated rejection evidence into recalibration; they do not require the closed-list pre-resolution. Strictness-skeptic's "fires too late" objection is real but correctly addressed by lowering the trigger threshold or by the v3.0.0 sunset on calibration targets (P3 #1 below), not by structural restructuring. Strictness-skeptic's own R-5 sequencing principle ("calibrate before enforcing harder") cuts against R-1's prospective restructure: prospective categorical loosening before evidence is theory-first, which strictness-skeptic explicitly opposes elsewhere in the deliberation. Practitioner's NR-1 framing of this contradiction is correct.

**Rejected position:** strictness-skeptic R-1 (closed-list partial-OR). The empirical observation it rests on is preserved and made load-bearing by the SIR grandfathering disclosure; the structural restructure is rejected as criterion-2-violating and as Single-Source-of-Truth-violating duplication.

**Required changes:** none in v2.4.0. AND-coupling at lines 872-893 is unchanged. The retrospective calibration trigger lands as P2 #4 (already convergent across all three roles per the synthesis); it is not a corrective edit for this dispute, only a paired companion to it.

---

### Dispute: Verification deliberation acceptance bar — substantive zero-disputes vs. documented-disputes

**Positions:**
- **Governance-skeptic** (Non-Negotiable 2): substantive zero-disputes bar with a narrow unanimous-out-of-scope escape hatch and panel-composition disclosure as the gameability mitigation. Argues v2.3.1 evidence is asymmetric (one zero-disputes catch, zero documented-disputes catches); Principle V governs output validation, not amendment process; "documented in SIR" reliably converges to "ignored after 90 days."
- **Practitioner** (R5 amended): documented-disputes bar — every dispute either incorporated or documented in the SIR with non-incorporation rationale. Avoids single-veto failure modes; preserves accountability without creating a chokepoint.
- **Strictness-skeptic** (SA-2): implicitly endorses documented-disputes via SA-2 ("variance-reducer not bug-catcher" critique of zero-disputes).

**Synthesizer's assessment** (quoted): "1-versus-2 against governance-skeptic on the headline question, but governance-skeptic's narrow unanimous-out-of-scope escape hatch is a meaningful synthesis position nobody else proposed. Practitioner's Flexibility F-3 (verification deliberation can move to v2.5.0) is an alternative resolution path that defers the dispute entirely."

**Ruling:** **DEFER**. v2.4.0 does NOT codify the verification-deliberation acceptance bar (neither zero-disputes nor documented-disputes). The verification-deliberation requirement and its acceptance bar are deferred to a v2.5.0 follow-up amendment, recorded as a load-bearing TODO in the v2.4.0 Sync Impact Report's Follow-up section.

**Grounding citation:** Versioning rule (Governance §) + Documentation Is the Product (IV).

**Rationale:** All three positions on this dispute are coherent on their own terms, but none of them belongs in v2.4.0 because v2.4.0's stated scope is the inclusion gate itself, not the verification mechanism that enforces the gate substantively. Bundling the verification-deliberation requirement into v2.4.0 expands the amendment from "add three-criterion gate" to "add three-criterion gate + codify the deliberation venue + define its acceptance bar," which is two MINOR amendments compressed into one. Practitioner's Flexibility F-3 explicitly recognizes this scope concern and offers the deferral path; it is the cooperative position nobody else fully owned, and it dissolves the dispute without choosing between the substantive and procedural bars.

The asymmetric-evidence argument (one zero-disputes catch versus zero documented-disputes catches) is real but single-datapoint, and the v2.3.1 incident is itself a self-consistency deliberation — it does not generalize cleanly to all amendment classes. Resolving the bar substantively at v2.4.0 risks calcifying an under-evidenced choice; deferring to v2.5.0 buys a second deliberation cycle's worth of evidence (panel composition, dispute frequency, override patterns) before the bar is set.

The deferral is conditioned on practitioner's NR-2 mitigation: the v2.4.0 Sync Impact Report's Follow-up section MUST list verification-deliberation codification as a v2.5.0 obligation, not an aspiration. Without that anchor, the deferral degenerates into "the gate's substantive enforcement never lands," which is the real risk practitioner correctly flagged. With it, the gate ships with its enforcement chain explicitly incomplete and explicitly committed to.

In the interim, the form-only CI lint (P1 #7 below) and the SIR self-assessment requirement (P1 #6) supply procedurally enforceable structure for amendment PRs. Substantive review continues to occur via the existing deliberation pipeline (this very arbitration is an example), governed by the same conventions that produced v2.3.0 and v2.3.1, until v2.5.0 codifies it textually.

**Rejected position:** governance-skeptic Non-Negotiable 2 (substantive zero-disputes bar in v2.4.0). The substantive case for zero-disputes is preserved as a candidate for v2.5.0 codification, with the unanimous-out-of-scope escape hatch and panel-composition disclosure on record as governance-skeptic's contribution to that future amendment.

Practitioner's R5 (documented-disputes bar) is also not adopted in v2.4.0 — but the deferral does not reject the documented-disputes framing; it defers the choice between bars to v2.5.0.

**Required changes:** none in v2.4.0 gate text. P1 #2 (Sync Impact Report) MUST include in its Follow-up section: "Verification-deliberation codification deferred to v2.5.0; acceptance bar (substantive zero-disputes vs. documented-disputes) to be resolved at that amendment with the v2.4.0 panel-composition disclosure and unanimous-out-of-scope escape hatch as candidate inputs."

---

### Dispute: Precedent log — derived index vs. authoritative log; build-moment specification

**Positions:**
- **Practitioner** (R8 amended): derived index built on demand from each amendment's SIR self-assessment by the speckit pipeline; constitution does not maintain it. Treats the log as load-bearing infrastructure that should be referenced explicitly in gate text.
- **Governance-skeptic**: SIR self-assessment is authoritative; precedent log is a derived index, but the operational question of WHO runs the build and WHEN is unspecified. Proposes the rebuild MUST run as part of every MINOR/MAJOR amendment's PR-time CI, output as a build artifact visible in the PR diff.
- **Strictness-skeptic** (SA-2): pairs log with retrospective review at each MINOR; implies log is queried at MINOR amendments.

**Synthesizer's assessment** (quoted): "this is the smallest of the three remaining disputes and has a clean cooperative path. All three positions are compatible; the disagreement is whether v2.4.0 specifies the build moment explicitly or leaves it to follow-up tooling. Practitioner explicitly flagged 'rebuilt on demand by speckit pipeline' but did not specify a triggering CI step; governance-skeptic's specification fills that gap without disagreeing on substance."

**Ruling:** **ACCEPT** the cooperative cooperative composition. v2.4.0 codifies the precedent log as a derived index (practitioner R8) with the build moment specified at every MINOR/MAJOR amendment's PR-time CI (governance-skeptic addition), output to a designated path and visible in the PR diff. Strictness-skeptic's retrospective-review pairing follows naturally and need not be separately codified.

**Grounding citation:** Single Source of Truth (XI) + Documentation Is the Product (IV) + Spec-Implementation Parity (XIV).

**Rationale:** All three positions are substantively compatible; the synthesizer's "clean cooperative path" assessment is correct, and this dispute is the cheapest of the three to resolve correctly. Single Source of Truth (XI) requires that the precedent log be derived rather than maintained — which is practitioner's framing and which strictness-skeptic and governance-skeptic both accept. Documentation Is the Product (IV) requires that infrastructure load-bearing for the recalibration triggers (governance NR-1, practitioner NR-1, strictness R-10) be specified in the constitution rather than left to convention; otherwise, by Spec-Implementation Parity (XIV), the spec promises a recalibration mechanism the implementation does not produce.

Governance-skeptic's specific contribution — the build moment is "PR-time CI for every MINOR/MAJOR amendment, output as a build artifact in the PR diff" — closes the operational gap without contradicting practitioner's derived-index design. The synthesizer's recommended resolution path is adopted as written.

**Rejected position:** none. All three positions converge under the cooperative composition; no agent's framing is rejected.

**Required changes:** edits to the candidate file (line numbers refer to the v2.4.0 candidate as read):

1. In the new `### Constitutional Inclusion Criteria` subsection (per P1 #1 below), add a sub-bullet under the routing/operational-guidance section:

   > "**Precedent log**: a derived index of per-amendment Inclusion Criteria Self-Assessments, rebuilt as part of every MINOR or MAJOR amendment's PR-time CI alongside the form-check lint. The rebuild output is written to `deliberations/governance-decisions.md` as a build artifact, visible in the PR diff. The log is the authoritative input to the retrospective calibration trigger; the per-amendment Sync Impact Report self-assessments remain the single source of truth, and the log is a derivation."

2. In the v2.4.0 Sync Impact Report (per P1 #2 below), include in the Follow-up section: "Precedent log build step lands as part of the form-check lint CI in the same PR sequence as v2.4.0; if the lint ships before the rebuild step, the rebuild MUST be added as a follow-up CI change before the next MINOR amendment opens."

---

## Summary of Changes Required

The arbitration produces **0 ACCEPT-level findings on the spec 069 amendment as drafted in the candidate file** (Disputes 1 rejected; Dispute 2 deferred; Dispute 3 accepted with edits that compose with the convergent P1/P2 changes already on the synthesis's Actionable Spec Changes list).

Per spec 067 §4.4, the acceptance bar is "0 ACCEPT-level findings on the spec 069 amendment specifically." Dispute 3's ACCEPT ruling is on a *cooperative composition* of all three agents' positions — it does not flag a defect *in* the candidate amendment but rather operationalizes a convergent recommendation that the synthesis already had in P2. This is consistent with the bar: ACCEPT findings of the spec-067 type signal "the candidate has a defect that must be fixed before merge"; the Dispute 3 ruling instead signals "the candidate is correct as far as it goes, and the cooperative composition completes the operational specification of an item all three agents already agreed upon."

To make this distinction explicit and auditable, the changes below are listed at their original synthesis priority (P1/P2/P3) without reclassification. None of them is a defect-correction edit triggered by the arbitration; the arbitration confirms the existing prioritization.

### P1 — required for v2.4.0 merge (already on the Phase 5 synthesis list; arbitration confirms)

1. Lift gate to subsection `### Constitutional Inclusion Criteria` (governance R1, strictness R-12, practitioner SA-3 — unanimous).
2. Add v2.4.0 Sync Impact Report at top of file with grandfathering disclosure enumerating VI, X, XVI per spec 069 §5; **arbitration adds**: include in the Follow-up section (a) the verification-deliberation v2.5.0 deferral note from Dispute 2, and (b) the precedent-log build-step note from Dispute 3.
3. Replace `CONTRIBUTING.md` with `AGENTS.md` at line 896 (strictness R-13; unanimous in Phase 4).
4. Withdraw fixed check-type taxonomy from criterion 1 (unanimous Phase 3 withdrawal).
5. Withdraw PATCH carve-out; SIR self-assessment accepts "N/A — typo fix / cross-reference update" answers (unanimous).
6. Add SIR self-assessment requirement (governance R2, practitioner R1 amended).
7. Add form-only CI lint on amendment PRs (practitioner R2 amended; strictness R-9 sharpened; governance R2 modified).
8. Cross-link gate → Principle XVII (governance R10, practitioner R10 amended).
9. Fix criterion 2 wording per practitioner R7 adopted; add criterion 3 sentence on cross-reference coordination (XV/XXVII pattern).

### P2 — strongly recommended (already on the Phase 5 synthesis list; arbitration confirms; Dispute 3 fold-in)

1. Define extension semantics with subset-of-scope carve-out (governance R3 modified).
2. Versioning sub-bullet on extensions (governance R8 modified).
3. Distinctness tie-breaker (governance R5 modified, strictness R-4 compatible).
4. Retrospective calibration trigger (governance NR-1, practitioner NR-1, strictness R-6/R-10) — **arbitration confirms this as the convergent companion to Dispute 1's REJECT ruling**; without it, the AND-coupling-unchanged decision lacks its calibration counterweight.
5. Disambiguate `SKILL.md` from operational guidance (governance R9).
6. Define promotion path symmetric to demotion (strictness R-8).
7. Expedited path with rollback authority (practitioner R9 amended).
8. Panel-composition disclosure (practitioner NR-3) — **arbitration elevates relevance**: this lands in v2.4.0 specifically so the v2.5.0 verification-deliberation amendment has the disclosure machinery in place.
9. Derived precedent log with explicit build moment (practitioner R8 + governance Dispute 3 resolution) — **per Dispute 3 ACCEPT ruling above**.

### P3 — nice-to-have (already on the Phase 5 synthesis list; arbitration confirms)

1. Calibration target with sunset at v3.0.0 (strictness R-5 modified, [80%, 90%] band).
2. 14-day amendment cooling-off (practitioner NR-2; drop if NR-3 lands).
3. Routing table for operational-guidance destinations (practitioner R3 amended).

---

## Confidence Assessment

| Dispute | Ruling | Confidence | Basis |
|---|---|---|---|
| 1. Criterion 1 AND-coupling vs. partial-OR | REJECT (gate unchanged) | High | Strictness-skeptic's closed list violates criterion 2 (scope vagueness) and XI (single source of truth duplicating SIR enumeration); 2-of-3 cooperative balance favors deferral; practitioner's framing of the strictness-skeptic-internal contradiction (R-5 sequencing vs. R-1 prospective restructure) is dispositive. The "fires too late" empirical objection is acknowledged and addressed by P3 #1 sunset, not by structural concession. |
| 2. Verification-deliberation acceptance bar | DEFER (to v2.5.0) | Medium-high | All three positions are coherent; choosing among them at v2.4.0 calcifies an under-evidenced choice. Practitioner's F-3 (deferral) is the cooperative escape route the synthesizer flagged; it dissolves the dispute without picking sides. The deferral's risk (v2.5.0 stalls; substantive enforcement never lands) is mitigated by anchoring the obligation in the v2.4.0 SIR's Follow-up section. The Medium-high (not High) reflects acknowledged residual risk that v2.5.0 may slip; this is the only ruling where a future-amendment commitment is load-bearing. |
| 3. Precedent log — derived index + build moment | ACCEPT (cooperative composition) | High | All three agents' positions are substantively compatible per the synthesizer's own assessment; Single Source of Truth + Documentation Is the Product + Spec-Implementation Parity together require codifying the build moment to prevent the precedent-log infrastructure from rotting. The required edits are mechanical and small; no agent's framing is rejected. |

The deliberation produced unusually high cooperative-mode quality for a self-consistency target. Five convergences are unanimous (per Phase 5 §"Convergence Achieved") and were earned through Phase 2 cross-reviews and Phase 3 revisions, not assumed. Two of the three remaining disputes (1 and 3) had clean structural resolutions visible in the deliberation record itself; the third (Dispute 2) is genuinely under-determined and the deferral ruling reflects that under-determination honestly rather than forcing a choice. The agents executed concession discipline well: governance-skeptic withdrew R4 and R6, practitioner withdrew R4 and amended R5, strictness-skeptic narrowed R-3/R-7 to a closed list and modified R-5 and R-10. Each concession was made for principled reasons cited from the cross-review evidence, not for political balancing.

The single weakness in the deliberation is the asymmetric evidence base for the verification-deliberation bar (one v2.3.1 incident; no independent corroboration). The DEFER ruling on Dispute 2 is, in part, a refusal to convert that single datapoint into a constitutional commitment. If a second deliberation cycle produces additional evidence on either side of the substantive-vs-procedural bar question, v2.5.0 should be informed by that evidence; if not, v2.5.0 should consider whether codifying the verification-deliberation requirement at all is premature.

The arbiter's overall reading: the candidate v2.4.0 amendment is shippable as drafted, with the convergent P1/P2 changes from the Phase 5 synthesis applied as already prioritized, plus the small Dispute 3 edits enumerated above. None of the three disputes surfaces a defect *in the candidate amendment* that the synthesis had not already addressed; Disputes 1 and 2 were genuine theoretical disagreements among the agents that the candidate's drafted text correctly punts to retrospective machinery (Dispute 1) or future amendment (Dispute 2), and Dispute 3 was an operational gap in a convergent recommendation that the cooperative composition fills.

---

**SPEC-069 SELF-CONSISTENCY VERDICT: PASS WITH FIXES**
