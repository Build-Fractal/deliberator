# Defender Final Statement -- Round 2 Phase 4

**Role**: Blue Team (Defender)
**Round**: 2 of 3
**Phase**: 4 -- Disputes (Final Statement Before Synthesis)
**Date**: 2026-03-20

---

## Remaining Disputes

**Dispute: THREAT-02 Severity -- MEDIUM vs. LOW (Analytical Framing)**

Both teams now agree on MEDIUM as the net severity for THREAT-02. The dispute that remains is not about severity classification but about the analytical framing that justifies it, which may affect how the synthesizer characterizes the risk.

The attacker's MEDIUM rests on two independent arguments: (1) the defensive depth asymmetry across all three non-cooperative modes (cooperative has three layers, non-cooperative has one), and (2) the WTA prose misalignment (arbiter directed to "Runner-Up" instead of disputes). The attacker argues that the architectural asymmetry is itself a MEDIUM-level concern even where prose instructions name the correct section.

The defender's MEDIUM rests on a mode-differentiated assessment: LOW for red-blue and prisoners-dilemma (where prose instructions twice name the correct section by name and constitute adequate single-layer mitigation), elevated to MEDIUM overall solely by the WTA prose direction gap (where the arbiter is directed to the competitive ranking analysis rather than to any disputes section). The defender does not accept that one-layer mitigation is inherently insufficient for red-blue and prisoners-dilemma; the cooperative template's three-layer design may reflect over-engineering rather than minimum-necessary-redundancy.

This framing difference does not affect severity, priority, or remediation. Both teams agree THREAT-02 is MEDIUM, P2, and requires adding `{REMAINING_DISPUTES}` + empty-case fallback to all three non-cooperative arbitration templates with WTA-specific prose correction. The synthesizer should note the convergence on outcome and record the framing difference as an analytical nuance rather than a contested position.

---

## Convergence

Round 2 achieved complete severity convergence across all three disputed threats from Round 1. The following risks are now agreed by both teams.

### Severity-Converged Threats

1. **THREAT-01 -- CRITICAL (unchanged from Round 1).** Missing `{PRIOR_ROUND_SECTION}` in non-cooperative review templates. Blocking gate for spec acceptance. Both teams agreed in Round 1; no Round 2 dispute.

2. **THREAT-10 -- HIGH (converged in Round 2).** Cross-round synthesis templates lack `DISPUTES_BEGIN`/`DISPUTES_END` structural markers. The defender concedes HIGH. The MEDIUM defense was built on a factual error about Phase 6 execution ordering (defender claimed Phase 6 runs before the cross-round synthesis is written; SKILL.md L502-540 specifies the opposite). With the ordering corrected: Phase 6 reads the cross-round synthesis, every multi-round arbitration path falls to the degraded heading-based fallback, and three of four affected templates are spec 004 authorship (not inherited from spec 002). The reliability class change from deterministic marker-based extraction to probabilistic heading-based extraction is legitimate. P2 remediation: add markers to all four cross-round synthesis templates.

3. **THREAT-02 -- MEDIUM (converged in Round 2).** Missing `{REMAINING_DISPUTES}` in non-cooperative arbitration templates. The defender elevated from LOW to MEDIUM. The WTA arbitration template directs the arbiter to "Runner-Up" and "Conditions for reconsideration" rather than to any disputes section -- a genuine prose direction gap that exists independently of all other threats. Red-blue and prisoners-dilemma have adequate prose mitigation (naming the correct section twice), but the WTA path has no mitigation at all: no pre-extraction, no empty-case fallback, no prose instruction pointing to disputes. The attacker withdrew the "double degradation" compound framing, which the defender agrees was analytically equivalent to THREAT-02 alone. P2 remediation: add `{REMAINING_DISPUTES}` + empty-case fallback to all three non-cooperative arbitration templates; add WTA-specific prose instruction to check "Remaining Disputes."

4. **THREAT-05 -- MEDIUM (converged in Round 2).** WTA fallback heading (`## Runner-Up`) causes false triggering. The defender elevated from LOW to MEDIUM. The threat decomposes into two vectors:
   - **Vector A (between-round stagnation detection)**: LOW. Requires LLM marker-dropping from per-round synthesis output. Per-round templates contain markers. Three-condition gating. Non-destructive failure. Both teams agree.
   - **Vector B (Phase 6 trigger evaluation)**: MEDIUM. Non-conditional for WTA multi-round runs with `trigger: disputes_remain`. The cross-round synthesis template lacks markers (THREAT-10), fallback fires, `## Runner-Up` is always present, so `has_disputes = true` always. WTA with `trigger: disputes_remain` degrades to `trigger: always`. Both teams agree.
   - **Remediation dependency**: THREAT-05 Vector B resolves automatically when THREAT-10 is fixed (markers added to cross-round synthesis templates make the primary path succeed; the `## Runner-Up` fallback never fires). The standalone THREAT-05 fix (changing SKILL.md L675 from `## Runner-Up` to `### Remaining Disputes`) is defense-in-depth. P3 remediation.

5. **THREAT-04 -- MEDIUM (unchanged from Round 1).** Spec FR-009 heading table diverges from SKILL.md/template reality. Documentation drift, no runtime impact. P3 remediation. Both teams agreed in Round 1; no Round 2 dispute.

6. **THREAT-06 -- LOW (unchanged from Round 1).** WTA lacks named dispute entry pattern. Primary marker-based path is adequate. Fallback concern captured by THREAT-05. No immediate fix needed. Both teams agreed in Round 1; no Round 2 dispute.

### Structural Agreements

7. **The compound failure scenario (THREAT-10 + THREAT-05) is confirmed.** For WTA multi-round arbitration with `trigger: disputes_remain`, the interaction is non-conditional and structural: missing markers (THREAT-10) cause fallback; always-present `## Runner-Up` heading (THREAT-05) causes guaranteed false-positive; arbiter runs on uncontested verdicts. Both teams agree on the mechanism and the net effect (unnecessary but non-destructive arbitration resolution).

8. **THREAT-02 is independent of the compound scenario.** The attacker withdrew the "double degradation" framing. When THREAT-02 fires alone, extracted content is discarded (no template variable to receive it). When THREAT-10 + THREAT-02 fire together, approximate extraction is discarded. The arbiter's information state is identical in both cases. THREAT-02 stands on its own merits (defensive depth asymmetry and WTA prose misalignment), not as a compound amplifier.

9. **The THREAT-10 remediation resolves THREAT-05 Vector B as a side effect.** Adding markers to cross-round synthesis templates makes the primary marker-based path succeed for Phase 6 trigger evaluation, eliminating the fallback to `## Runner-Up`. Both teams agree this dependency should be documented in the remediation plan.

10. **All remediation is template-layer or documentation -- no engine changes needed.** The engine is mode-agnostic and architecturally correct. Template completeness is the correctness condition for a template-first architecture. Both teams agree, consistent with Round 1 convergence points CONV-1, CONV-2, and CONV-11.

11. **The attacker's compound framing for THREAT-02 was correctly withdrawn.** Both teams agree the compound interaction does not create a failure state worse than THREAT-02 alone for the arbiter's final information state. The interaction is sequential, not multiplicative.

### Withdrawn/Resolved Threats (Unchanged from Round 1)

THREAT-03, THREAT-07, THREAT-08, THREAT-09, THREAT-11, THREAT-12 remain withdrawn per Round 1 consensus.

---

## Final Position Statement

Round 2 was defined by a single factual error and its correction. The defender's Round 2 review misread the SKILL.md execution sequence, claiming Phase 6 trigger evaluation runs before the cross-round synthesis is written. SKILL.md L502-540 specifies the opposite: cross-round synthesis is produced first, then Phase 6 reads it. This error was the analytical foundation for the MEDIUM defense on THREAT-10 and the LOW defense on THREAT-05's Phase 6 vector. Once identified -- by the defender's own cross-review of the attacker -- both positions became unsustainable and were withdrawn.

The error follows the same structural pattern as the Round 1 population-vs-consumption mistake: verifying one consumer of a subsystem and incorrectly generalizing to all consumers. In Round 1, the defender verified that the orchestrator populates variables without verifying that templates consume them. In Round 2, the defender verified which file the round termination check reads (per-round synthesis) without verifying which file the Phase 6 trigger reads (cross-round synthesis). Both errors involve treating distinct consumers of the Dispute-Parsing Subsystem as interchangeable when they are not.

The correction produces complete severity convergence. Both teams now agree on CRITICAL for THREAT-01, HIGH for THREAT-10, MEDIUM for THREAT-02, THREAT-04, and THREAT-05, and LOW for THREAT-06. The only remaining analytical difference is whether THREAT-02's MEDIUM severity derives from an architectural asymmetry across all three non-cooperative modes (attacker's framing) or from the WTA-specific prose direction gap alone (defender's framing). This difference does not affect severity classification, priority ordering, or remediation scope.

The remediation plan is fully agreed:

| Priority | Threat | Severity | Fix |
|----------|--------|----------|-----|
| P1 | THREAT-01 | CRITICAL | Add `{PRIOR_ROUND_SECTION}` to three non-cooperative review templates |
| P2 | THREAT-10 | HIGH | Add `DISPUTES_BEGIN`/`DISPUTES_END` markers to all four cross-round synthesis templates |
| P2 | THREAT-02 | MEDIUM | Add `{REMAINING_DISPUTES}` + empty-case fallback to three non-cooperative arbitration templates; add WTA-specific prose direction to "Remaining Disputes" |
| P3 | THREAT-04 | MEDIUM | Update spec.md FR-009 heading table to match SKILL.md/templates |
| P3 | THREAT-05 | MEDIUM | Change WTA fallback heading from `## Runner-Up` to `### Remaining Disputes` in SKILL.md L675 (defense-in-depth; primary fix is THREAT-10) |

The defender recommends the synthesizer record full convergence and proceed to remediation. There are no severity disputes requiring Round 3 adjudication.
