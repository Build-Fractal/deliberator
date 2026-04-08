# Defense Revision -- Round 2

**Role**: Blue Team (Defender)
**Round**: 2 of 3
**Date**: 2026-03-20
**Target**: Spec 004 -- Universal Rounds, Stagnation Detection, and Arbitration

---

## Preamble: Honest Accounting

This revision addresses a significant factual error in the defender's Round 2 review. The review's central argument for THREAT-10 MEDIUM severity -- that "Phase 6 trigger evaluation runs BEFORE the cross-round synthesis is written" (review L34) -- is wrong. SKILL.md defines the execution sequence unambiguously: cross-round synthesis is produced at L502-527, Phase 6 runs at L529-598, and Phase 6 reads `{output}/summary/final.md` which IS the cross-round synthesis for multi-round runs (L540). The defender misread the round termination check (which occurs after each round's Phase 5 and reads per-round synthesis) and conflated it with the Phase 6 trigger evaluation (which occurs after the cross-round synthesis and reads the definitive synthesis).

This is structurally parallel to the Round 1 population-vs-consumption error. In Round 1, the defender verified that the orchestrator populates variables without verifying that templates consume them. In Round 2, the defender verified which files the round termination check reads without verifying which file the Phase 6 trigger reads. Both errors involve verifying one consumer of the Dispute-Parsing Subsystem and incorrectly generalizing to all consumers.

The downstream consequences of this error are material. The "zero functional impact on current code paths" conclusion for THREAT-10, the dismissal of Phase 6 as a consumer of cross-round synthesis, and the absence of any counter-argument for THREAT-05's Phase 6 trigger vector all trace to this single misreading. The revision below recalibrates accordingly.

---

## Defense 1: THREAT-10 -- Cross-Round Synthesis Templates Lack Structural Markers

**Round 2 review position**: MEDIUM
**Classification**: **Withdrawn.** Conceding HIGH.

### Why the MEDIUM defense is withdrawn

The MEDIUM argument rested on three claims:

1. The cross-round synthesis is a "terminal artifact, not an intermediate input" to Phase 6.
2. The missing markers have "zero functional impact on current code paths."
3. The only affected consumers are humans and hypothetical future systems.

All three claims depend on the execution ordering assertion that Phase 6 runs before the cross-round synthesis is written. That assertion is factually incorrect per SKILL.md L502-540. With the ordering corrected:

- Phase 6 reads the cross-round synthesis (L540). The cross-round synthesis IS an intermediate input to Phase 6 trigger evaluation and `{REMAINING_DISPUTES}` extraction, not a terminal artifact.
- Every multi-round arbitration path falls to the degraded heading-based fallback for dispute extraction. This is a guaranteed degradation on a current code path, not zero functional impact.
- Phase 6 is a current, defined consumer that is affected. This is not hypothetical.

The attacker's authorship argument is also correct and was not addressed in the Round 2 review. Three of the four cross-round synthesis templates were created by spec 004. The per-round synthesis templates in the same mode directories contain the markers. Spec 004 had both a flawed reference (cooperative cross-round, no markers) and a correct reference (per-round synthesis templates, with markers) and replicated the flawed pattern. This is a spec 004 authorship error for three templates and an inherited gap for one.

The attacker's reliability-class-change argument (review L63) is legitimate. The degradation moves dispute extraction from a template-controlled deterministic interface to an LLM-output-dependent probabilistic interface. This is a meaningful change in the reliability characteristics of the Phase 6 trigger and extraction path.

**Revised position**: HIGH. The gap guarantees degraded parsing on every multi-round arbitration path. The execution ordering error in the Round 2 review was the analytical foundation for MEDIUM, and that foundation is gone.

---

## Defense 2: THREAT-02 -- Missing `{REMAINING_DISPUTES}` in Non-Cooperative Arbitration Templates

**Round 2 review position**: LOW
**Classification**: **Modified.** Moving to MEDIUM for WTA; maintaining LOW for red-blue and prisoners-dilemma, yielding a net assessment of MEDIUM.

### What survives from the Round 2 defense

The prose instruction analysis (review L61-67) is factually accurate and was accepted by the attacker's cross-review (Section 2.2: "The prose instructions are real and correctly quoted. The defense is factually accurate."). The red-blue and prisoners-dilemma arbitration templates direct the arbiter to the correct section by name twice -- once in reading instructions and once in binding-decisions instructions. For these two modes, prose instructions are a genuine and adequate single-layer mitigation.

The argument that the compound interaction with THREAT-10 does not add marginal harm (defender cross-review of attacker, Section "Mitigated Threats") also stands. When THREAT-02 fires independently, the extracted content is discarded. When THREAT-10 + THREAT-02 fire together, the approximate extraction is discarded. The arbiter's information state is identical in both cases: no pre-extracted disputes, prose instructions pointing to the correct section, full synthesis available. The compound framing is analytically equivalent to THREAT-02 alone for the arbiter's actual inputs.

### What does not survive

The blanket LOW classification across all three modes does not survive. The attacker identified a mode-specific sub-problem that the Round 2 review did not address: the WTA arbitration template's prose instruction directs the arbiter to the "Runner-Up" section and "Conditions for reconsideration," not to a disputes section. The red-blue arbiter is told to look at "Disputed Risks." The prisoners-dilemma arbiter is told to look at "Disputed Boundaries." The WTA arbiter is told to look at competitive ranking analysis, not disputed positions.

This is not a consequence of the compound interaction -- it is an independent WTA-specific prose design issue. Even if THREAT-10 were fully remediated and markers were added to all cross-round synthesis templates, the WTA arbitration template would still direct the arbiter to the runner-up analysis rather than to remaining disputes.

The attacker's defensive-depth asymmetry argument (cooperative has three layers, non-cooperative has one) is valid at the architectural level. The cooperative template's own design -- adding `{REMAINING_DISPUTES}` and the empty-case fallback on top of prose instructions -- demonstrates that the system author judged prose instructions alone to be insufficient. This is a legitimate design-intent argument. However, I note that the cooperative template's three-layer design could also reflect over-engineering rather than minimum-necessary-redundancy. The question is whether one layer (prose) is adequate or whether two+ layers are required. For red-blue and prisoners-dilemma, where the prose correctly names the disputes section, I maintain one layer is adequate. For WTA, where the prose names the wrong section, one layer is inadequate.

**Revised position**: MEDIUM (net). The WTA arbitration template has a genuine prose direction gap that makes the missing `{REMAINING_DISPUTES}` more consequential for that mode. Red-blue and prisoners-dilemma have adequate prose mitigation (LOW individually). The overall threat is MEDIUM because the WTA path has a real quality gap, and the fix (adding `{REMAINING_DISPUTES}` + empty-case fallback + WTA-specific prose correction) should apply uniformly to all three templates.

---

## Defense 3: THREAT-05 -- WTA Fallback Heading Causes False Stagnation/Triggering

**Round 2 review position**: LOW
**Classification**: **Modified.** Moving to MEDIUM.

### What survives from the Round 2 defense

The between-round stagnation detection analysis survives intact. The attacker explicitly accepted the three-condition probability argument (attacker review L157-159, attacker cross-review Section 3.1). The per-round synthesis templates contain markers. The stagnation detector reads per-round synthesis files. The three-condition requirement (LLM drops markers + WTA mode + rounds > 1) is correct for the stagnation detection consumer, and each condition independently reduces probability. For the between-round stagnation path specifically, LOW remains the appropriate severity.

The non-destructive failure characterization also survives. The attacker accepted (cross-review Section 3.4) that premature termination produces "complete and correct" per-round output with no data loss or artifact corruption. The attacker's argument is about operational waste and ambiguous deliberation records, not data integrity.

### What does not survive

The Round 2 review treated THREAT-05 as having a single attack vector: between-round stagnation detection. It does not. The attacker identified a second, distinct consumer of the Dispute-Parsing Subsystem: the Phase 6 trigger evaluation path.

The defender's Round 2 review failed to address this second consumer because of the execution ordering error analyzed in the preamble. With the ordering corrected, the Phase 6 trigger vector is:

1. Phase 6 trigger evaluation reads the cross-round synthesis (SKILL.md L540).
2. The WTA cross-round synthesis template lacks `DISPUTES_BEGIN`/`DISPUTES_END` markers (THREAT-10).
3. The Dispute-Parsing Subsystem falls to heading-based fallback.
4. The WTA fallback heading is `## Runner-Up` (SKILL.md L675).
5. `## Runner-Up` is always present in the WTA cross-round synthesis template (L84).
6. Therefore `has_disputes = true` always, regardless of actual dispute state.
7. WTA with `trigger: disputes_remain` degrades to `trigger: always` for multi-round runs.

This vector is non-conditional. It does not require LLM marker-dropping (the cross-round template never instructs markers). It does not require any coincidence of conditions beyond the configuration itself (WTA + multi-round + `trigger: disputes_remain`). The defender has no counter-argument for this vector.

The comparison to THREAT-04 in the Round 2 review (L107) also does not survive. The review argued that if THREAT-04 is MEDIUM for documentation drift with zero runtime impact, THREAT-05 should not also be MEDIUM for a conditional runtime impact. The attacker's cross-review correctly reversed this: the Phase 6 trigger path has guaranteed runtime waste for a specific-but-real configuration, which is more severe than THREAT-04's zero runtime impact, not less. The comparison inadvertently supports MEDIUM for THREAT-05.

### The remediation dependency

The attacker's observation that THREAT-05's Phase 6 trigger vector resolves automatically when THREAT-10 is fixed is architecturally sound. If markers are added to the WTA cross-round synthesis template (THREAT-10 P2 fix), the primary marker-based path succeeds, and the `## Runner-Up` fallback heading is never consulted for Phase 6 trigger evaluation. The THREAT-05 P3 fix (changing the fallback heading) becomes defense-in-depth. This dependency should be documented in the remediation plan.

**Revised position**: MEDIUM. The Phase 6 trigger vector is a valid, non-conditional attack surface that the Round 2 review did not address. The between-round stagnation vector remains LOW (three-condition requirement accepted by both teams). The combined assessment is MEDIUM because the Phase 6 trigger vector is sufficient to elevate the threat above LOW on its own.

---

## Summary: Revised Severity Positions

| THREAT-ID | Description | Round 2 Review Position | Revised Position | Classification | Key Factor |
|-----------|-------------|------------------------|-----------------|----------------|------------|
| THREAT-10 | Cross-round synthesis templates lack structural markers | MEDIUM | **HIGH** | **Withdrawn** | Execution ordering error invalidated the entire MEDIUM argument. Phase 6 reads the cross-round synthesis. Every multi-round arbitration path degrades to heading-based fallback. Three of four templates are spec 004 authorship. |
| THREAT-02 | Missing `{REMAINING_DISPUTES}` in non-cooperative arbitration templates | LOW | **MEDIUM** | **Modified** | Red-blue and PD prose instructions are adequate (LOW individually). WTA prose direction to "Runner-Up" instead of disputes section is a genuine gap. Net assessment elevated to MEDIUM. |
| THREAT-05 | WTA fallback heading causes false stagnation/triggering | LOW | **MEDIUM** | **Modified** | Between-round stagnation path remains LOW (three-condition argument accepted by both teams). Phase 6 trigger path is a new, non-conditional vector that the Round 2 review failed to address due to the execution ordering error. Net assessment elevated to MEDIUM. |

---

## Convergence Assessment

With these revisions, the defender and attacker now agree on severity for all three disputed threats:

| THREAT-ID | Attacker Position | Defender Revised Position | Status |
|-----------|------------------|--------------------------|--------|
| THREAT-10 | HIGH | HIGH | **Converged** |
| THREAT-02 | MEDIUM | MEDIUM | **Converged** |
| THREAT-05 | MEDIUM | MEDIUM | **Converged** |

The remaining nuances where the teams differ are analytical framing rather than severity classification:

- **THREAT-02**: The defender maintains that the compound interaction with THREAT-10 does not add marginal harm (the arbiter's information state is identical whether extraction was precise-and-discarded or approximate-and-discarded). The attacker frames the compound interaction as amplifying severity. Both arrive at MEDIUM through different reasoning.
- **THREAT-05**: Both teams agree the between-round stagnation path is LOW-probability and the Phase 6 trigger path is the primary concern. The defender would note for the synthesizer that the Phase 6 trigger vector has a remediation dependency on THREAT-10 -- fixing THREAT-10 incidentally resolves THREAT-05's Phase 6 vector.

---

## Updated Remediation Plan

| Priority | Threat | Severity | Fix | Notes |
|----------|--------|----------|-----|-------|
| P1 | THREAT-01 | CRITICAL | Add `{PRIOR_ROUND_SECTION}` to non-cooperative review templates | Blocking gate. Unchanged. |
| P2 | THREAT-10 | HIGH | Add `DISPUTES_BEGIN`/`DISPUTES_END` markers to all four cross-round synthesis templates | Conceded at HIGH. Incidentally resolves THREAT-05 Phase 6 vector. |
| P2 | THREAT-02 | MEDIUM | Add `{REMAINING_DISPUTES}` + empty-case fallback to all three non-cooperative arbitration templates; add WTA-specific prose instruction to check "Remaining Disputes" section | Elevated from LOW. WTA prose direction gap is the primary driver. |
| P3 | THREAT-04 | MEDIUM | Update spec.md FR-009 heading table | Unchanged. |
| P3 | THREAT-05 | MEDIUM | Change WTA fallback heading from `## Runner-Up` to `### Remaining Disputes` in SKILL.md L675 | Elevated from LOW. Defense-in-depth after THREAT-10 fix. Dependency on THREAT-10 should be documented. |

---

## Methodological Lessons

### Round 1 Error: Population-vs-consumption
The defender verified that the orchestrator populates variables without verifying that templates consume them. This caused the defense to miss THREAT-01.

### Round 2 Error: Consumer conflation
The defender verified which files the round termination check reads (per-round synthesis) and incorrectly generalized to all consumers of the Dispute-Parsing Subsystem, including Phase 6 trigger evaluation (which reads the cross-round synthesis). This caused the defense to dismiss the functional impact of THREAT-10 and to miss the Phase 6 trigger vector for THREAT-05.

### Pattern
Both errors share the same structure: verifying one instance of a category and generalizing to the entire category without checking. The round termination check and Phase 6 trigger evaluation are both "consumers of the Dispute-Parsing Subsystem," but they read different files at different points in the execution sequence. The defender treated them as interchangeable. They are not.

### Correction applied
This revision independently verified the SKILL.md execution sequence (L502-540) and confirmed the attacker's ordering claim. The defender's cross-review of the attacker (written after the Round 2 review) already identified this error and conceded THREAT-10 at HIGH and THREAT-05 at MEDIUM for the Phase 6 vector. This revision formalizes those concessions.
