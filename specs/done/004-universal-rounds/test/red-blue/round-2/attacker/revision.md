# Revised Attack Position: Spec 004 — Round 2

**Role**: Red Team Attacker (Revised Position)
**Date**: 2026-03-20
**Round**: 2 of 3
**Prior documents**: attacker/review.md, defender/cross-reviews/attacker.md, attacker/cross-reviews/defender.md

---

## Threat Disposition Summary

| Threat | R1 Final Severity | R2 Review Severity | R2 Revised Severity | Disposition |
|--------|-------------------|-------------------|---------------------|-------------|
| THREAT-10 | HIGH | HIGH | **HIGH** | Surviving |
| THREAT-02 | MEDIUM | MEDIUM | **MEDIUM** | Modified |
| THREAT-05 | MEDIUM | MEDIUM | **MEDIUM** | Modified |

---

## Surviving Threats

### THREAT-10: Cross-Round Synthesis Templates Lack `DISPUTES_BEGIN`/`DISPUTES_END` Structural Markers — SURVIVING (HIGH)

**Defender's cross-review position**: Conceded at HIGH. The defender's cross-review (L38-54) explicitly states: "The defender concedes THREAT-10 at HIGH. The execution order error in the defender's R2 review was the analytical mistake that sustained the MEDIUM position."

**Why it survives unchanged**: THREAT-10 is now fully agreed by both teams. The defender's own cross-review identifies the root cause of the prior disagreement: a factual error in the defender's R2 review about Phase 6 execution ordering. The defender claimed "Phase 6 trigger evaluation runs BEFORE the cross-round synthesis is written" (defender R2 review L34). SKILL.md L502-540 specifies the opposite: cross-round synthesis production at L502-527, then Phase 6 at L529-598. The defender's cross-review acknowledges this error and traces its cascading impact through the entire MEDIUM argument.

With the execution order corrected, every element of the attacker's Round 2 argument holds without challenge:

1. **Authorship**: Three of four affected cross-round synthesis templates (red-blue, winner-take-all, prisoners-dilemma) were authored by spec 004, not inherited from spec 002. The per-round synthesis templates in the same mode directories contain the markers, proving the pattern was available. The defender's cross-review (L52) confirms: "The attacker's structural argument... that three of the four cross-round synthesis templates were authored by spec 004 -- not inherited from spec 002 -- is also correct."

2. **Guaranteed degradation**: Every multi-round arbitration path with `trigger: disputes_remain` falls to the heading-based fallback for Phase 6 trigger evaluation and `{REMAINING_DISPUTES}` extraction. The defender's cross-review (L54) confirms: "every multi-round arbitration path degrades from the deterministic marker-based primary path to the probabilistic heading-based fallback."

3. **Reliability class change**: The degradation moves dispute extraction from a template-controlled interface (deterministic HTML comment markers) to an LLM-output-dependent interface (heading-based parsing that depends on the LLM producing exact heading text). The defender's cross-review (L54) acknowledges: "The reliability class change argument... is legitimate."

**Remediation**: Add `DISPUTES_BEGIN`/`DISPUTES_END` markers to all four cross-round synthesis templates, wrapping the mode-appropriate disputes section in each:
- `templates/cooperative/cross-round-synthesis.md` L90: wrap `### Remaining Disputes`
- `templates/red-blue/cross-round-synthesis.md` L114: wrap `### Disputed Risks`
- `templates/winner-take-all/cross-round-synthesis.md` L95: wrap `### Remaining Disputes`
- `templates/prisoners-dilemma/cross-round-synthesis.md` L101: wrap `## Disputed Boundaries`

**Severity: HIGH.** Both teams now agree. No further argument needed.

---

## Modified Threats

### THREAT-02: Missing `{REMAINING_DISPUTES}` in Non-Cooperative Arbitration Templates — MODIFIED (MEDIUM, argument refined)

**Defender's cross-review position**: LOW maintained, with a WTA-specific remediation note. The defender argues (L18-26) that the compound interaction with THREAT-10 does not add marginal harm: "The net result is identical to THREAT-02 firing alone: the arbiter receives no pre-extracted disputes and must rely on prose instructions and the full synthesis."

**What I accept from the defender's cross-review**: The defender's argument about sequential vs. multiplicative compounding (L20-23) is analytically correct. When THREAT-02 fires alone, the extraction succeeds but the extracted content is discarded (no template variable to receive it). When THREAT-10 + THREAT-02 fire together, the approximate extraction is discarded. The arbiter's information state is the same in both cases: no pre-extracted disputes, prose instructions pointing to the correct section, full synthesis available. The compound framing overstated the additive harm.

**What I withdraw**: The "double degradation" framing from my R2 review (L75-78). The compound interaction does not create a failure state worse than THREAT-02 alone for the arbiter's final information state. The interaction chain is correctly traced but the net impact converges to the same endpoint.

**What I maintain**: MEDIUM severity, now resting on two independent arguments that do not depend on compound framing:

**Argument 1: Defensive depth asymmetry.** The cooperative arbitration template provides three layers of defense for dispute delivery to the arbiter:
- Layer 1: Prose instruction ("Pay special attention to the synthesis's 'Remaining Disputes' section")
- Layer 2: Pre-extracted content (`{REMAINING_DISPUTES}`)
- Layer 3: Empty-case fallback ("If this section is empty, read the full synthesis to identify any remaining disputes")

The non-cooperative arbitration templates provide one layer: prose instruction only. The cooperative template's own design demonstrates the system author's judgment that prose instructions alone are insufficient -- otherwise, why add Layers 2 and 3? The defender's cross-review (L26) concedes this: "The attacker's point about asymmetric defensive depth (cooperative has three layers, non-cooperative has one) is valid at the architectural level."

This asymmetry is a design consistency gap. It means the arbiter's reliability is mode-dependent in a way that is not architecturally justified -- there is no reason a red-blue arbiter needs less dispute context than a cooperative arbiter.

**Argument 2: WTA arbitration prose direction is semantically misaligned.** The WTA arbitration template directs the arbiter to "Pay special attention to the verdict's 'Runner-Up' section and 'Conditions for reconsideration'" (L32). It does not mention disputes, remaining contested positions, or the `### Remaining Disputes` section of the synthesis. The defender's cross-review (L88-92) concedes this is "a genuine asymmetry" and "a legitimate concern" but argues it is "WTA-specific, not a general THREAT-02 issue."

I accept that this is WTA-specific. But it elevates the WTA instance of THREAT-02 above LOW because the arbiter is not even directed to the conceptual area where disputes would be found -- they are directed to the competitive ranking assessment instead. For red-blue and prisoners-dilemma, the prose instructions name the correct section ("Disputed Risks" and "Disputed Boundaries" respectively). For WTA, the prose instruction names a structural section ("Runner-Up") that contains competitive analysis, not disputed positions.

**Why MEDIUM, not LOW**: The defender argues (L90-92) that THREAT-02 is LOW for red-blue and prisoners-dilemma because prose instructions are adequate there, and the WTA issue is a WTA-specific remediation note rather than a severity elevation. I disagree with the analytical frame. A threat that affects three modes and is fully mitigated in two of them but unmitigated in the third is not LOW overall -- it is MEDIUM with a note that two modes have partial mitigation. The WTA instance has no mitigation at all: no pre-extraction, no empty-case fallback, and no prose instruction pointing to the disputes section.

**Remediation**: Add `{REMAINING_DISPUTES}` and empty-case fallback instruction to all three non-cooperative arbitration templates. For the WTA arbitration template specifically, also add prose instruction to check "Remaining Disputes" in addition to "Runner-Up."

**Severity: MEDIUM.** The compound framing is withdrawn. The defensive depth asymmetry and WTA prose misalignment independently sustain MEDIUM.

---

### THREAT-05: WTA Fallback Heading (`## Runner-Up`) Causes False Triggering — MODIFIED (MEDIUM, scope refined)

**Defender's cross-review position**: MEDIUM conceded for the Phase 6 trigger vector. LOW maintained for the between-round stagnation vector. Net position: MEDIUM (L132).

**What I accept from the defender's cross-review**: The defender's decomposition of THREAT-05 into two distinct attack vectors -- between-round stagnation and Phase 6 trigger evaluation -- is analytically cleaner than my R2 framing. The defender correctly identifies (L94-98) that the between-round stagnation vector remains conditionally gated (three conditions: LLM drops markers, WTA mode, rounds > 1), consistent with my own R2 concession (R2 review L157-159).

**What the defender conceded**: The Phase 6 trigger evaluation vector is "non-conditional and correctly identified" (L56) and "valid MEDIUM" (L72). The defender states: "The defender has no counter-argument for this vector" (L72). The full argument chain is confirmed by the defender's cross-review:

1. Phase 6 trigger evaluation reads the cross-round synthesis (confirmed via execution order analysis, L44-48).
2. The WTA cross-round synthesis template lacks DISPUTES markers (THREAT-10, now conceded at HIGH).
3. The Dispute-Parsing Subsystem falls to heading-based fallback.
4. The WTA fallback heading is `## Runner-Up` (SKILL.md L675).
5. `## Runner-Up` is always present in the WTA cross-round synthesis template (L84).
6. Therefore `has_disputes = true` always, regardless of actual dispute state.
7. WTA with `trigger: disputes_remain` degrades to `trigger: always` for multi-round runs.

**Scope refinement**: I formally adopt the two-vector decomposition:

- **Vector A: Between-round stagnation detection** — LOW. Requires LLM marker-dropping from per-round synthesis output. Per-round synthesis templates contain markers. Three-condition gating. Non-destructive failure (premature termination with complete per-round output). Both teams agree.

- **Vector B: Phase 6 trigger evaluation** — MEDIUM. Non-conditional for WTA multi-round runs with `trigger: disputes_remain`. Does not require LLM behavior variance. The failure is structural: cross-round template lacks markers (THREAT-10) and the fallback heading is always present. Both teams agree.

**Net severity: MEDIUM.** Vector B dominates. The Phase 6 trigger path is a guaranteed false-positive for a specific but real configuration (WTA + multi-round + `trigger: disputes_remain`), causing the arbiter to run on uncontested verdicts.

**Remediation dependency**: THREAT-05's Phase 6 vector resolves automatically when THREAT-10 is fixed (markers added to cross-round synthesis templates). With markers present, the primary path succeeds and the `## Runner-Up` fallback never fires. The standalone THREAT-05 fix (changing SKILL.md L675 from `## Runner-Up` to `### Remaining Disputes`) becomes defense-in-depth rather than primary remediation. Both teams agree on this dependency (defender cross-review L74-78).

**Severity: MEDIUM.** Both teams now agree on the Phase 6 vector severity and the remediation dependency.

---

## Compound Failure Scenario — Revised

My R2 review presented a compound failure scenario (WTA multi-round arbitration with `trigger: disputes_remain`) tracing the interaction of THREAT-10, THREAT-02, and THREAT-05. The defender's cross-review challenged the compound framing for THREAT-02 specifically, arguing that the compound interaction does not add marginal harm to the arbiter's information state (cross-review L18-26).

I accept the defender's point on THREAT-02's compound contribution (see THREAT-02 revision above). The revised compound scenario is:

**THREAT-10 + THREAT-05 compound**: This interaction is non-conditional, fully confirmed by both teams, and correctly characterized. THREAT-10 (missing markers in cross-round synthesis) causes the Dispute-Parsing Subsystem to fall to the heading-based fallback. THREAT-05 (WTA fallback heading `## Runner-Up` is always present) causes the fallback to return `has_disputes = true` regardless of actual dispute state. The compound is structural, not probabilistic.

**THREAT-02's role**: Independent of the compound. The arbiter's information state is the same whether THREAT-10 fires or not: no pre-extracted disputes in the template, prose instructions pointing to the mode-appropriate section (or in WTA's case, to the wrong section). THREAT-02 is an independent defensive-depth gap, not a compound amplifier.

**Net scenario**: WTA multi-round arbitration with `trigger: disputes_remain` produces a guaranteed unnecessary arbitration resolution when no actual disputes remain. The resolution is binding but addresses no real dispute. Wasteful and potentially confusing, but not destructive.

---

## Remediation Priority — Updated

| Priority | Threat | Fix | Resolves | Notes |
|----------|--------|-----|----------|-------|
| P2 | THREAT-10 | Add `DISPUTES_BEGIN`/`DISPUTES_END` markers to all four cross-round synthesis templates | THREAT-10 (primary), THREAT-05 Vector B (side effect) | Both teams agree at HIGH. Fixes THREAT-05's Phase 6 trigger vector as a side effect. |
| P2 | THREAT-02 | Add `{REMAINING_DISPUTES}` + empty-case fallback to three non-cooperative arbitration templates. For WTA, also add prose direction to "Remaining Disputes" section. | THREAT-02 | Agreed-real by both teams; severity disputed (Red: MEDIUM, Blue: LOW with WTA-specific note). |
| P3 | THREAT-05 | Change WTA fallback heading from `## Runner-Up` to `### Remaining Disputes` in SKILL.md L675 | THREAT-05 Vector A defense-in-depth | Defense-in-depth after THREAT-10 fix. Dependency on THREAT-10 should be documented. |

Note: THREAT-01 (P1) and THREAT-04 (P3) remediation status is unchanged from Round 1. They are not disputed threats and are not part of this Round 2 revision scope.

---

## Position Summary

Round 2 produced significant convergence. The central dispute -- whether Phase 6 reads the cross-round synthesis or the per-round synthesis -- was resolved by the defender's own cross-review, which identified a factual error in the defender's R2 review about execution ordering. With that error corrected:

- **THREAT-10 at HIGH** is now agreed by both teams. No remaining dispute.
- **THREAT-05 at MEDIUM** is now agreed by both teams for the Phase 6 trigger vector. The between-round stagnation vector is agreed at LOW. No remaining dispute on net severity.
- **THREAT-02 at MEDIUM vs. LOW** remains the sole active severity dispute entering Round 3.

The THREAT-02 dispute is narrow: both teams agree the gap is real. Both teams agree `{REMAINING_DISPUTES}` and empty-case fallback should be added to non-cooperative arbitration templates. The severity question is whether the defensive depth asymmetry (three layers in cooperative, one in non-cooperative) and the WTA prose misalignment (directing the arbiter to "Runner-Up" instead of disputes) justify MEDIUM or LOW. The defender argues prose instructions are adequate for red-blue and prisoners-dilemma, making the issue WTA-specific. The attacker argues the architectural asymmetry and the WTA-specific total absence of mitigation together justify MEDIUM overall.

This is the narrowest possible dispute surface for Round 3. The compound framing has been withdrawn. The arguments are independent and testable. The remediation is agreed regardless of severity classification.
