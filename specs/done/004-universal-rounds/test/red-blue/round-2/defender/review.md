# Defense Brief — Round 2

**Role**: Blue Team (Defender)
**Round**: 2 of 3
**Date**: 2026-03-20
**Target**: Spec 004 — Universal Rounds, Stagnation Detection, and Arbitration

---

## Engagement with Round 1 Synthesis

The Round 1 synthesis produced a thorough and fair assessment. The defense concedes the following from the synthesis without further contest:

- **THREAT-01 (CRITICAL)**: Fully conceded. Missing `{PRIOR_ROUND_SECTION}` in non-cooperative review templates is a blocking gate. The defense's population-vs-consumption analysis error was the root cause of missing this in Round 1. No further argument.
- **THREAT-04 (MEDIUM)**: Agreed. Spec FR-009 heading table is stale documentation, not a functional risk. Both teams and the synthesizer agree.
- **THREAT-06 (LOW)**: Agreed. WTA primary marker-based path handles dispute counting adequately. Both teams converged.

This Round 2 brief focuses exclusively on the three severity disputes the synthesizer identified as unresolved: **THREAT-10**, **THREAT-02**, and **THREAT-05**.

---

## Disputed Risk 1: THREAT-10 — Cross-Round Synthesis Templates Lack Structural Markers

**Red's position**: HIGH
**Blue's position**: MEDIUM
**Synthesizer's Round 1 assessment**: Both agree on the gap and P2 fix. Dispute is severity only. Synthesizer notes Red's argument about blast-radius amplification is "substantive."

### Strengthened Defense for MEDIUM

The defense accepts the synthesizer's observation that spec 004 amplifies the blast radius by extending cross-round synthesis to three additional modes. That is a legitimate analytical point. However, amplification of blast radius does not change the failure severity when the failure mode itself is degraded-quality-with-functional-fallback.

**New evidence — the per-round synthesis templates DO have markers**: All four per-round `synthesis.md` templates contain `DISPUTES_BEGIN`/`DISPUTES_END` markers (verified: cooperative L103-113, red-blue L113-125, winner-take-all L106-110, prisoners-dilemma L97-117). The cross-round synthesis templates are the only gap. This means the dispute-parsing subsystem's primary path works correctly for the stagnation detection use case, which reads per-round synthesis files (`{output}/round-N/summary/final.md`). The cross-round synthesis is only read by Phase 6 trigger evaluation and by human consumers.

**Reframing the attack surface**: Red argues the gap is consequential because "Phase 6 reads the cross-round synthesis." But Phase 6 trigger evaluation runs BEFORE the cross-round synthesis is written. The orchestrator's Phase 6 trigger evaluation (SKILL.md Step 4) reads the LAST ROUND's per-round synthesis, not the cross-round synthesis, to determine whether to launch the arbiter. The cross-round synthesis is written by a cross-round synthesizer agent that runs AFTER all rounds complete. Phase 6 (if triggered) then runs. The cross-round synthesis is the FINAL artifact, not an intermediate input to Phase 6.

This means the missing markers in cross-round synthesis templates affect:
1. **Human readability** — humans reading the cross-round synthesis cannot use marker-based tools to extract disputes. This is a documentation quality issue.
2. **Hypothetical future consumers** — if a future system reads the cross-round synthesis for automated dispute extraction, it would fall to the heading-based fallback. This is speculative.

The missing markers do NOT affect:
- Stagnation detection (reads per-round synthesis, which HAS markers)
- Phase 6 trigger evaluation (reads per-round synthesis, which HAS markers)
- Phase 6 arbiter prompt (receives `{REMAINING_DISPUTES}` from orchestrator extraction, not from reading the cross-round synthesis)

**The contract violation argument**: Red frames this as a violation of SKILL.md L683's stable interface contract. The defense acknowledges the contract language includes cross-round synthesis templates. However, a contract violation with zero functional impact and a working fallback is a documentation gap, not a system risk. The stable interface contract exists to prevent breaking changes — the markers were never present in cross-round synthesis templates, so there is nothing to break.

**Severity framework**: HIGH severity should be reserved for threats where the system fails to perform a declared function, produces incorrect results, or creates a pathway to data loss or corruption. THREAT-10 causes none of these. The system performs correctly — disputes are detected, stagnation is detected, Phase 6 fires when it should. The only degradation is that the cross-round synthesis document itself lacks machine-parseable markers, which affects no current consumer.

**Conclusion**: MEDIUM. The gap is real, the fix is warranted (P2), but the functional impact is zero on all current code paths. Blast-radius amplification does not promote a zero-impact gap to HIGH.

---

## Disputed Risk 2: THREAT-02 — Missing `{REMAINING_DISPUTES}` in Non-Cooperative Arbitration Templates

**Red's position**: MEDIUM
**Blue's position**: LOW
**Synthesizer's Round 1 assessment**: Both agree the gap is real and P2 priority. Synthesizer notes the non-cooperative templates contain prose instructions as a "genuine partial mitigation."

### Strengthened Defense for LOW

**New evidence — the non-cooperative arbitration templates contain targeted prose guidance**: The Round 1 synthesis noted that non-cooperative templates contain prose instructions. Let me be precise about what each template says:

- **Red-blue** (`templates/red-blue/arbitration.md` L32): "Pay special attention to the synthesis's 'Disputed Risks' section — those are the risk assessments you must resolve."
- **Winner-take-all** (`templates/winner-take-all/arbitration.md` L32): "Pay special attention to the verdict's 'Runner-Up' section and 'Conditions for reconsideration' — these indicate where the decision was closest and where your operational knowledge matters most."
- **Prisoners-dilemma** (`templates/prisoners-dilemma/arbitration.md` L32): "Pay special attention to the synthesis's 'Disputed Boundaries' section — those are the boundary conflicts you must resolve."

Each template names the exact section heading the arbiter should focus on. Furthermore, each template's "Binding Decisions" section (red-blue L58, WTA L68, PD L57) reinforces this by instructing the arbiter to address "EACH disputed risk/boundary identified in the synthesis's '[Section Name]' section."

**The asymmetry is narrower than claimed**: The cooperative template provides two things the non-cooperative templates lack:
1. `{REMAINING_DISPUTES}` — pre-extracted dispute content.
2. Empty-case fallback instruction ("If this section is empty, read the full synthesis to identify any remaining disputes.").

Red's argument focuses on item 2: without the fallback instruction, a non-cooperative arbiter "may conclude there are no disputes" if extraction fails. But this argument assumes the arbiter would ignore the preceding prose instruction ("Pay special attention to the synthesis's '[Section]' section") and the Binding Decisions section instruction ("For EACH disputed [risk/boundary] identified in the synthesis's '[Section]' section"). An LLM arbiter receiving the full synthesis text via `{SYNTHESIS_PATH}` and instructed twice to focus on a named section will not conclude there are no disputes simply because a pre-extracted variable is absent.

**The empty-case scenario is further attenuated**: The empty-case fallback matters when the orchestrator's extraction finds no disputes to populate `{REMAINING_DISPUTES}`. But if extraction finds no disputes, Phase 6 would not have triggered in the first place — the Phase 6 trigger evaluation (SKILL.md Step 4) requires disputes to exist. The only scenario where Phase 6 runs AND extraction returns empty is if the trigger evaluation and the extraction use different parsing paths. Given both use the same Dispute-Parsing Subsystem, this is a narrow edge case.

**Severity framework**: The distinction between MEDIUM and LOW is whether the gap causes quality degradation (MEDIUM) or is a polish/robustness improvement (LOW). The non-cooperative templates already direct the arbiter to the correct section by name, twice. Adding `{REMAINING_DISPUTES}` would be a convenience improvement — pre-extracting content the arbiter is already instructed to read. This is polish, not quality.

**Conclusion**: LOW. The prose instructions are a genuine and sufficient mitigation. The pre-extracted content and empty-case fallback are robustness improvements, not corrections to a quality gap.

---

## Disputed Risk 3: THREAT-05 — WTA Fallback Heading (`## Runner-Up`) Causes False Stagnation

**Red's position**: MEDIUM
**Blue's position**: LOW
**Synthesizer's Round 1 assessment**: Both agree the primary path works. Both agree the fallback heading should be changed (P3). Synthesizer notes Blue's original direction-of-failure analysis was wrong.

### Strengthened Defense for LOW

**Acknowledging the Round 1 error**: The defense fully concedes the direction-of-failure error from Round 1. The fallback does not "miss stagnation" — it "always detects stagnation," causing premature termination at Round 2. The corrected failure mode is wasteful (terminates early), not dangerous (misses real stagnation).

**New evidence — the WTA cross-round synthesis template contains `### Remaining Disputes` at L95**: The WTA cross-round synthesis template (`templates/winner-take-all/cross-round-synthesis.md` L95) contains a `### Remaining Disputes` heading that is distinct from the `## Runner-Up` heading at L84. This heading is the correct target for dispute counting. The `## Runner-Up` heading is a SKILL.md fallback definition issue (SKILL.md L675), not a template structural error.

**Three conditions must coincide for the failure**: As identified in Round 1, THREAT-05 requires:
1. The LLM drops structural markers from its synthesis output. (The per-round synthesis template instructs the LLM to include `DISPUTES_BEGIN`/`DISPUTES_END` markers at L106-110 of the WTA synthesis template.)
2. The mode is winner-take-all specifically.
3. The run uses rounds > 1.

**Each condition reduces probability**:
- Condition 1: LLMs follow structural marker instructions with high fidelity, especially HTML comments that are trivial to copy from the template. The markers are explicitly placed in the template surrounding the dispute section. Marker-dropping is possible but not the expected behavior.
- Condition 2: WTA is one of four modes. The threat applies to 25% of mode configurations.
- Condition 3: Rounds > 1 is the new capability introduced by spec 004. Most initial usage will be single-round (no stagnation detection at all).

**The failure consequence is bounded**: Even when all three conditions coincide, the result is premature termination — the deliberation ends after Round 2 instead of continuing. Each completed round's output is complete and correct. No data is lost, no artifacts are corrupted, no incorrect decisions are rendered. The user observes "stagnation detected" earlier than expected and can re-run with `stagnation: ignore` if they want additional rounds.

**Comparison to MEDIUM-severity threats**: THREAT-04 (spec heading table divergence) is MEDIUM by agreement, and it has zero runtime impact — it is pure documentation drift. THREAT-05 has a conditional runtime impact (premature termination under a triple-coincidence scenario) that is bounded and non-destructive. If THREAT-04 is MEDIUM for documentation drift alone, THREAT-05 should not also be MEDIUM for a conditional, bounded, non-destructive operational annoyance. The severity scale should discriminate between guaranteed documentation inaccuracy (MEDIUM) and conditional operational waste (LOW).

**The fix is trivial and agreed**: Both teams agree SKILL.md L675 should change from `## Runner-Up` to `### Remaining Disputes` as the WTA fallback heading. This is a P3 single-line edit. The severity classification does not change the fix or its priority.

**Conclusion**: LOW. The threat requires three simultaneous conditions, produces a bounded non-destructive failure (premature termination with complete per-round output), and has a trivial agreed-upon fix. This is an operational annoyance under narrow conditions, not a quality degradation.

---

## Summary: Severity Positions for Round 2

| THREAT-ID | Description | Red Position | Blue Position (Round 2) | Round 1 Synthesizer | Blue's Key Argument |
|-----------|-------------|-------------|------------------------|--------------------|--------------------|
| THREAT-10 | Cross-round synthesis templates lack structural markers | HIGH | **MEDIUM** | Acknowledged Red's blast-radius point as substantive | Zero functional impact on current code paths. Per-round synthesis templates (used by stagnation detection and Phase 6 trigger) have markers. Cross-round synthesis is a terminal artifact, not an intermediate input. |
| THREAT-02 | Missing `{REMAINING_DISPUTES}` in non-cooperative arbitration templates | MEDIUM | **LOW** | Acknowledged Blue's prose instructions as genuine partial mitigation | Each non-cooperative template names the exact section twice — once in reading instructions, once in binding-decisions instructions. Pre-extraction is convenience, not correction. |
| THREAT-05 | WTA fallback heading causes false stagnation | MEDIUM | **LOW** | Both agree primary path works; both agree on P3 fix | Triple-coincidence requirement. Non-destructive bounded failure (premature termination with complete output). Each condition independently reduces probability. |

---

## Defensive Methodology Improvement: Round 2

The Round 1 synthesis correctly identified the defense's population-vs-consumption category error as the root cause of missing THREAT-01. In Round 2, the defense has applied the lesson: every argument above traces the complete data flow from template instruction through orchestrator behavior to consumer outcome. No argument relies solely on "the orchestrator populates X" without verifying "template Y consumes X" and "consumer Z reads Y."

Specifically:
- THREAT-10: Traced which files the stagnation detector and Phase 6 trigger actually read (per-round synthesis, not cross-round synthesis).
- THREAT-02: Identified the exact prose instructions in each non-cooperative arbitration template that serve as the consumption mechanism for dispute information.
- THREAT-05: Traced the fallback heading lookup path through SKILL.md L675 and confirmed the template structural context (WTA cross-round synthesis L84 vs L95).
