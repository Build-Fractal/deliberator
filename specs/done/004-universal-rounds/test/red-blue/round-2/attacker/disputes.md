# Final Attacker Disputes -- Spec 004: Universal Rounds, Round 2

**Role**: Red Team Attacker (Final Statement)
**Date**: 2026-03-20
**Round**: 2 of 3
**Phase**: 4 -- Final disputes before cross-round synthesis

---

## Remaining Disputes

**Dispute: THREAT-02 severity -- MEDIUM vs. LOW-with-WTA-note framing (MEDIUM)**

Both teams now agree on MEDIUM severity for THREAT-02. The defender's R2 revision explicitly states: "Moving to MEDIUM for WTA; maintaining LOW for red-blue and prisoners-dilemma, yielding a net assessment of MEDIUM" (defender revision L50). The attacker also holds MEDIUM. However, the analytical framing differs and the synthesis must resolve which framing governs the remediation scope.

- **Attacker framing**: MEDIUM applies uniformly to all three non-cooperative arbitration templates because the defensive depth asymmetry (cooperative has three layers, non-cooperative has one) is an architectural consistency gap. The system author's own design decision -- adding `{REMAINING_DISPUTES}` and the empty-case fallback to the cooperative template -- demonstrates that prose instructions alone were judged insufficient. The fix (add `{REMAINING_DISPUTES}` + empty-case fallback) should apply to all three templates as a design consistency correction, not as a WTA-specific patch.

- **Defender framing**: MEDIUM is driven by the WTA-specific prose direction gap (arbiter directed to "Runner-Up" instead of disputes). Red-blue and prisoners-dilemma are individually LOW because their prose instructions correctly name the disputes section. The net assessment reaches MEDIUM only because of the WTA instance.

- **Why this matters for the synthesis**: Both framings produce the same remediation (add `{REMAINING_DISPUTES}` + empty-case fallback to all three templates, plus WTA-specific prose correction). But the attacker's framing treats the fix as a design consistency requirement (the non-cooperative templates should match the cooperative template's defensive depth), while the defender's framing treats the red-blue and prisoners-dilemma fixes as optional hardening layered on top of adequate prose mitigation. If a future implementer triages remediation by severity, the defender's framing could justify fixing only the WTA template. The attacker's framing requires fixing all three.

- **Proposed resolution**: The synthesis should note that both teams agree on MEDIUM severity and on applying the fix to all three templates. The synthesis should also note the defender's concession that the fix "should apply uniformly to all three templates" (defender revision L66), which matches the attacker's remediation scope regardless of the framing difference.

---

## Convergence

The following risks and positions are agreed by both teams entering the cross-round synthesis.

**CONV-R2-1: THREAT-10 at HIGH -- fully converged**
- Both teams agree THREAT-10 is HIGH. The defender withdrew the MEDIUM position after identifying a factual error in the R2 review about Phase 6 execution ordering (defender revision L12-16). The defender confirmed: Phase 6 reads the cross-round synthesis (SKILL.md L540), the cross-round synthesis is an intermediate input to Phase 6 (not a terminal artifact), and every multi-round arbitration path degrades to the heading-based fallback. The defender also accepted the authorship argument (three of four templates are spec 004 authored) and the reliability-class-change argument (deterministic markers to probabilistic heading parsing).
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**CONV-R2-2: THREAT-05 at MEDIUM -- fully converged**
- Both teams agree THREAT-05 is MEDIUM. The defender elevated from LOW after acknowledging the Phase 6 trigger evaluation vector that the R2 review failed to address (defender revision L83-95). Both teams agree on the two-vector decomposition: Vector A (between-round stagnation) is LOW with three-condition gating; Vector B (Phase 6 trigger evaluation) is MEDIUM and non-conditional. The net severity is MEDIUM, driven by Vector B.
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**CONV-R2-3: THREAT-02 at MEDIUM -- severity converged, framing differs**
- Both teams agree THREAT-02 is MEDIUM. The defender elevated from LOW after conceding the WTA prose direction gap (defender revision L58-66). Both teams agree the fix should apply to all three non-cooperative arbitration templates. The framing difference (architectural consistency vs. WTA-driven net assessment) does not affect remediation scope because the defender explicitly states the fix "should apply uniformly" (defender revision L66).
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous on severity and remediation; minor framing difference on analytical justification

**CONV-R2-4: THREAT-10 + THREAT-05 compound interaction is structural and confirmed**
- Both teams agree that the THREAT-10 + THREAT-05 compound is non-conditional for WTA multi-round arbitration with `trigger: disputes_remain`. Missing markers (THREAT-10) force fallback parsing. The always-present `## Runner-Up` heading (THREAT-05) causes `has_disputes = true` regardless of actual dispute state. WTA with `trigger: disputes_remain` degrades to `trigger: always`. Both teams agree this resolves automatically when THREAT-10 is fixed (markers added).
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**CONV-R2-5: THREAT-02 compound framing withdrawn**
- Both teams agree that the compound interaction of THREAT-02 with THREAT-10 does not add marginal harm to the arbiter's information state. Whether extraction was precise-and-discarded or approximate-and-discarded, the arbiter receives the same inputs: no pre-extracted disputes, prose instructions, and the full synthesis. The attacker formally withdrew the "double degradation" framing. THREAT-02 stands as an independent defensive-depth gap.
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**CONV-R2-6: Remediation plan and priorities agreed**
- Both teams agree on the following remediation plan:

| Priority | Threat | Severity | Fix |
|----------|--------|----------|-----|
| P1 | THREAT-01 | CRITICAL | Add `{PRIOR_ROUND_SECTION}` to non-cooperative review templates |
| P2 | THREAT-10 | HIGH | Add `DISPUTES_BEGIN`/`DISPUTES_END` markers to all four cross-round synthesis templates |
| P2 | THREAT-02 | MEDIUM | Add `{REMAINING_DISPUTES}` + empty-case fallback to all three non-cooperative arbitration templates; add WTA prose direction to disputes section |
| P3 | THREAT-04 | MEDIUM | Update spec.md FR-009 heading table |
| P3 | THREAT-05 | MEDIUM | Change WTA fallback heading from `## Runner-Up` to `### Remaining Disputes` in SKILL.md L675 (defense-in-depth after THREAT-10 fix) |

- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**CONV-R2-7: THREAT-05 remediation dependency on THREAT-10 documented**
- Both teams agree that THREAT-05's Phase 6 trigger vector (Vector B) resolves automatically when THREAT-10 is fixed. With markers present in the cross-round synthesis templates, the primary marker-based path succeeds and the `## Runner-Up` fallback heading is never consulted. The standalone THREAT-05 fix becomes defense-in-depth. This dependency should be documented in the remediation plan.
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**CONV-R2-8: Defender's execution ordering error acknowledged and corrected**
- Both teams agree that the defender's R2 review contained a factual error about Phase 6 execution ordering: the review claimed "Phase 6 trigger evaluation runs BEFORE the cross-round synthesis is written," but SKILL.md L502-540 specifies the opposite. The defender's R2 revision identified this as structurally parallel to the R1 population-vs-consumption error -- both involve verifying one instance of a category and incorrectly generalizing to all instances. The correction of this error was the primary driver of convergence in Round 2.
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**Prior convergence points (R1) carried forward unchanged**: CONV-1 through CONV-11 from the Round 1 synthesis remain in force. All eleven convergence points are reaffirmed. No R1 convergence point was challenged or modified in Round 2.

---

## Final Position Statement

Round 2 achieved full severity convergence on all three disputed threats. This is the strongest possible outcome for a red-blue deliberation: every severity dispute from Round 1 has been resolved through argument refinement, concession of analytical errors, and mutual acceptance of the surviving evidence.

**What was resolved in Round 2:**

1. **THREAT-10: HIGH.** The defender's R2 revision withdrew the MEDIUM position after identifying a factual error about Phase 6 execution ordering. The defender confirmed all three pillars of the attacker's argument: spec 004 authorship of three of four templates, guaranteed degradation of every multi-round arbitration path, and the reliability class change from deterministic to probabilistic dispute extraction. No remaining dispute.

2. **THREAT-05: MEDIUM.** The defender's R2 revision elevated from LOW after conceding the Phase 6 trigger evaluation vector. Both teams agree on the two-vector decomposition and the remediation dependency on THREAT-10. No remaining dispute on net severity.

3. **THREAT-02: MEDIUM.** The defender's R2 revision elevated from LOW after conceding the WTA prose direction gap. Both teams agree on remediation scope (all three templates). A minor framing difference persists (architectural consistency vs. WTA-driven net assessment) but does not affect severity classification or remediation scope.

**What the attacker conceded in Round 2:**

1. The compound interaction framing for THREAT-02 was withdrawn. The "double degradation" argument overstated the additive harm of THREAT-10 + THREAT-02 firing together. The arbiter's information state is identical whether THREAT-02 fires alone or in combination with THREAT-10.

2. The between-round stagnation vector of THREAT-05 was accepted as LOW with three-condition gating, consistent with the defender's analysis from Round 1.

**Non-negotiables for the synthesis (unchanged from Round 1, reinforced by Round 2 convergence):**

1. **THREAT-01 is a blocking gate.** Spec 004 cannot exit Draft status until `{PRIOR_ROUND_SECTION}` is present in all three non-cooperative review templates. Both teams have agreed on this since Round 1.

2. **THREAT-10 must be fixed in spec 004's scope.** Both teams now agree at HIGH. The fix applies to all four cross-round synthesis templates, including the cooperative template inherited from spec 002. Spec 004 is the spec that makes the gap consequential.

3. **The synthesis must state that spec 004's engine is correct but the template layer is incomplete.** This remains the consensus finding across both rounds. Engine: mode-agnostic, architecturally sound, no changes needed. Templates: five specific gaps, two blocking (THREAT-01 at CRITICAL, THREAT-10 at HIGH), three non-blocking (THREAT-02 at MEDIUM, THREAT-04 at MEDIUM, THREAT-05 at MEDIUM).

**The only item entering the synthesis with any remaining nuance** is the THREAT-02 framing difference described under Remaining Disputes above. Both teams agree on MEDIUM severity and on applying the fix to all three templates. The synthesis should note this convergence and resolve the framing question by observing that the defender's own language ("should apply uniformly") aligns with the attacker's remediation scope.
