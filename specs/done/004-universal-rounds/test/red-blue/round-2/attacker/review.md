# Red Team Attack Surface Analysis -- Round 2

**Attacker**: Red Team (Round 2)
**Date**: 2026-03-20
**Target**: Spec 004 -- Universal Rounds, Stagnation Detection, and Arbitration
**Spec path**: `<HOME>/code/payer-index-mono/conversus/specs/004-universal-rounds/spec.md`

---

## Executive Summary

Round 1 produced a comprehensive threat catalog. Six threats were withdrawn after Blue demonstrated they were derivative, cosmetic, or correctly defended. Three threats (THREAT-01, THREAT-04, THREAT-06) reached full agreement on severity. The remaining three (THREAT-10, THREAT-02, THREAT-05) are agreed-real with disputed severity classifications. This Round 2 review focuses on those three disputed risks with refined arguments and new evidence gathered from deeper template analysis.

The synthesizer's Round 1 framing accurately captures the state of play but systematically favors the "degraded-but-functional" framing over the "contract violation" framing for all three disputed threats. This review provides structural evidence that the three disputed threats interact as a compound failure mode that neither team fully articulated in Round 1. The combined effect is more severe than the sum of the individual parts.

---

## Disputed Threat Analysis

### THREAT-10: Cross-Round Synthesis Templates Lack `DISPUTES_BEGIN`/`DISPUTES_END` Markers

**Round 1 positions**: Red: HIGH. Blue: MEDIUM. Synthesizer: acknowledged Red's blast-radius amplification argument as "substantive."

**Round 2 position**: HIGH -- maintained, with refined structural argument.

#### New Evidence: The Contract Violation Is Not Merely Inherited

Blue's Round 1 argument rests on inheritance: spec 004 replicated an existing cooperative pattern, so the gap is inherited from spec 002 and does not constitute a regression. The synthesizer found this argument partially mitigating but noted Red's blast-radius amplification point was "substantive."

In Round 2, I present a structural argument that supersedes the inheritance framing entirely.

**Finding 1: The per-round synthesis templates DO contain the markers; the cross-round synthesis templates do NOT.**

Evidence from the template files:

- `templates/cooperative/synthesis.md` L103-113: contains `<!-- CONVERSUS:DISPUTES_BEGIN -->` and `<!-- CONVERSUS:DISPUTES_END -->`
- `templates/red-blue/synthesis.md` L113-125: contains both markers
- `templates/winner-take-all/synthesis.md` L106-110: contains both markers
- `templates/prisoners-dilemma/synthesis.md` L97-117: contains both markers
- `templates/cooperative/cross-round-synthesis.md`: **zero markers** (confirmed via search)
- `templates/red-blue/cross-round-synthesis.md`: **zero markers** (confirmed via search)
- `templates/winner-take-all/cross-round-synthesis.md`: **zero markers** (confirmed via search)
- `templates/prisoners-dilemma/cross-round-synthesis.md`: **zero markers** (confirmed via search)

This means that within each mode, the per-round synthesis templates correctly implement the stable interface contract, but the cross-round synthesis templates -- which produce the DEFINITIVE synthesis that Phase 6 reads -- do not. Spec 004 created three new cross-round synthesis templates (FR-003, FR-004, FR-005). Each was created without markers. This is not inheritance -- these are three brand-new templates that spec 004 authored, and all three violate the contract that the per-round synthesis templates in the same mode directory correctly implement.

**Finding 2: The Dispute-Parsing Subsystem reads the cross-round synthesis for both stagnation-relevant and Phase-6-relevant decisions.**

From SKILL.md L540: "If `trigger: disputes_remain` -- Read the definitive synthesis output file (`{output}/summary/final.md`). For multi-round runs, this is the cross-round synthesis."

And from SKILL.md L561: "`{SYNTHESIS_PATH}` -- absolute path to `{output}/summary/final.md` (the definitive synthesis -- cross-round synthesis for multi-round runs, Phase 5 synthesis for single-round runs)"

And from SKILL.md L569: "`{REMAINING_DISPUTES}` -- content extracted from the definitive synthesis... Primary: read content between `DISPUTES_BEGIN` and `DISPUTES_END` structural markers in the synthesis."

The primary extraction path reads the cross-round synthesis for markers. The markers are absent. The primary path fails. Every multi-round run with an arbiter falls to the degraded heading-based fallback for Phase 6 trigger evaluation AND for `{REMAINING_DISPUTES}` extraction. This is not a latent gap that "might" matter -- it is a guaranteed degradation on every multi-round arbitration path.

**Finding 3: The inheritance argument fails because spec 004 created the non-cooperative cross-round templates.**

The cooperative cross-round synthesis template (`templates/cooperative/cross-round-synthesis.md`) was created by spec 002. The fact that it lacks markers is indeed an inherited gap from spec 002. But the red-blue, winner-take-all, and prisoners-dilemma cross-round synthesis templates were created by spec 004. Spec 004 had the cooperative template (with its known marker absence) as a structural reference AND the per-round synthesis templates (which DO contain markers) as a correct-implementation reference. The spec chose to replicate the flawed pattern rather than the correct one. This is a spec 004 authorship error, not inheritance.

**Rebuttal to Blue's "degraded-but-functional" framing:**

Blue argues that a contract violation with a functional fallback is MEDIUM, not HIGH, because "the system performs its function." This framing elides the distinction between a system that performs its function reliably and one that performs it contingently. The fallback is heading-based parsing, which is LLM-output-dependent (the LLM must produce the exact heading text the parser expects). The primary marker-based path is template-controlled (the template instructs the LLM to include markers, and the markers are deterministic HTML comments that survive LLM output variation). By relying on the fallback for every multi-round arbitration, the system downgrades from a template-controlled interface to an LLM-output-dependent interface. That is a reliability class change, not a polish gap.

**Severity: HIGH.** The gap guarantees degraded parsing on every multi-round arbitration path. Three of the four affected templates were authored by spec 004, not inherited. The degradation moves dispute extraction from a deterministic primary path to a probabilistic fallback path.

---

### THREAT-02: Missing `{REMAINING_DISPUTES}` in Non-Cooperative Arbitration Templates

**Round 1 positions**: Red: MEDIUM. Blue: LOW. Synthesizer: acknowledged Blue's prose-instruction mitigation as "genuine partial mitigation."

**Round 2 position**: MEDIUM -- maintained, with a compound-failure argument that connects THREAT-02 to THREAT-10.

#### The Compound Failure: THREAT-10 + THREAT-02 Create a Double Degradation

Round 1 treated THREAT-02 and THREAT-10 as independent risks with independent mitigations. They are not. In a multi-round non-cooperative arbitration, both fire simultaneously, and their combined effect is worse than either alone.

**The interaction chain:**

1. **THREAT-10 fires first.** The cross-round synthesis template lacks `DISPUTES_BEGIN`/`DISPUTES_END` markers. The orchestrator attempts to extract `{REMAINING_DISPUTES}` from the cross-round synthesis via the primary marker-based path. The primary path fails.

2. **THREAT-10's fallback fires.** The orchestrator falls to heading-based extraction (SKILL.md L569: "Fallback (degraded): extract content under the mode-appropriate disputes heading"). This extracts some content, but it "may include preamble text or miss disputes formatted outside the heading" (SKILL.md L569). The extraction is approximate.

3. **THREAT-02 fires.** The non-cooperative arbitration templates do not contain `{REMAINING_DISPUTES}`. Even if the orchestrator successfully extracts dispute content in step 2, there is nowhere in the template to inject it. The extracted content is computed, then discarded.

4. **The arbiter operates blind to pre-extracted disputes.** The non-cooperative arbiter receives:
   - The full synthesis via `{SYNTHESIS_PATH}` -- yes.
   - Prose instructions to "Pay special attention to the synthesis's '[heading]' section" -- yes.
   - Pre-extracted dispute content in a dedicated template section -- **no** (only cooperative gets this).
   - Fallback guidance for the empty-extraction case -- **no** (only cooperative says "If this section is empty, read the full synthesis to identify any remaining disputes").

**Why this matters more than Round 1 acknowledged:**

Blue's Round 1 defense emphasized that prose instructions ("Pay special attention to the synthesis's 'Disputed Risks' section") are an adequate mitigation. I do not dispute that an LLM arbiter CAN find disputes in a full synthesis document when directed to a section name. The issue is the asymmetry in the degradation cascade:

- **Cooperative arbitration** (template L32-40): prose instruction + `{REMAINING_DISPUTES}` pre-extraction + empty-case fallback guidance. Three layers of defense.
- **Non-cooperative arbitration**: prose instruction only. One layer of defense.

The cooperative template was designed with the understanding that extraction might fail -- that is why L40 says "If this section is empty, read the full synthesis to identify any remaining disputes." The non-cooperative templates lack this defensive design. When THREAT-10 causes degraded extraction AND THREAT-02 prevents the extracted content from reaching the template, the non-cooperative arbiter is in a worse position than the cooperative arbiter facing the same extraction degradation.

**Evidence from actual template content:**

- Cooperative arbitration (`templates/cooperative/arbitration.md` L32-40):
  - L32: "Pay special attention to the synthesis's 'Remaining Disputes' section"
  - L34: "## Extracted Remaining Disputes"
  - L38: `{REMAINING_DISPUTES}`
  - L40: "If this section is empty, read the full synthesis to identify any remaining disputes."

- Red-blue arbitration (`templates/red-blue/arbitration.md` L32):
  - L32: "Pay special attention to the synthesis's 'Disputed Risks' section"
  - No `{REMAINING_DISPUTES}` variable anywhere in the template
  - No empty-case fallback instruction

- Winner-take-all arbitration (`templates/winner-take-all/arbitration.md` L32):
  - L32: "Pay special attention to the verdict's 'Runner-Up' section and 'Conditions for reconsideration'"
  - No `{REMAINING_DISPUTES}` variable anywhere in the template
  - No empty-case fallback instruction

- Prisoners-dilemma arbitration (`templates/prisoners-dilemma/arbitration.md` L32):
  - L32: "Pay special attention to the synthesis's 'Disputed Boundaries' section"
  - No `{REMAINING_DISPUTES}` variable anywhere in the template
  - No empty-case fallback instruction

**WTA arbitration has a distinct sub-problem.** The WTA arbitration template does not even direct the arbiter to a disputes section -- it directs them to the "Runner-Up" section and "Conditions for reconsideration." This is architecturally correct for WTA's decision model (the arbiter affirms or overrides the verdict), but it means the WTA arbiter has zero instruction to look for disputes per se. If the WTA cross-round synthesis contains a `### Remaining Disputes` section with contested positions, the arbiter is not directed to it.

**Severity: MEDIUM.** The compound interaction with THREAT-10 means the degradation is deeper than "missing a single variable." It is a missing defensive layer that becomes the only line of defense when THREAT-10 degrades the primary extraction path. The asymmetry with cooperative is not a polish gap -- it is a gap in defensive depth that the cooperative template's own design acknowledges is necessary (L40's empty-case fallback).

---

### THREAT-05: WTA Fallback Heading (`## Runner-Up`) Causes False Stagnation

**Round 1 positions**: Red: MEDIUM. Blue: LOW. Synthesizer: acknowledged Blue's direction-error correction and that the fallback heading choice is "suboptimal."

**Round 2 position**: MEDIUM -- maintained, with a refined argument that connects to THREAT-10 and narrows the attack surface.

#### Refined Attack: THREAT-10 Makes THREAT-05 Non-Conditional

Blue's Round 1 defense relies on a three-condition argument: THREAT-05 requires (a) LLM drops markers, (b) mode is WTA, (c) rounds > 1, and the conjunction of three conditions makes the threat LOW. In Round 2, I challenge condition (a).

**The stagnation detection path does not read the per-round synthesis template output -- it reads the per-round synthesis FILE.**

From SKILL.md L468: "Read the current round's synthesis (`{round_base}/summary/final.md`). Use the Dispute-Parsing Subsystem to determine the dispute count."

The per-round synthesis templates DO contain `DISPUTES_BEGIN`/`DISPUTES_END` markers (confirmed: `templates/winner-take-all/synthesis.md` L106-110). If the LLM follows the template instructions, the per-round synthesis output WILL contain the markers, and the primary path will succeed. In this case, THREAT-05's fallback never fires for stagnation detection.

However, consider the Phase 6 trigger evaluation path for multi-round WTA. From SKILL.md L540: the Dispute-Parsing Subsystem reads `{output}/summary/final.md`, which for multi-round runs is the cross-round synthesis. The cross-round synthesis template (`templates/winner-take-all/cross-round-synthesis.md`) does NOT contain the markers (THREAT-10). The template DOES contain `## Runner-Up` at L84. Therefore:

1. The Dispute-Parsing Subsystem reads the WTA cross-round synthesis.
2. Primary marker path: fails (no markers in cross-round synthesis template, per THREAT-10).
3. Fallback heading path: searches for `## Runner-Up` (SKILL.md L675).
4. `## Runner-Up` is ALWAYS present in the WTA cross-round synthesis (it is a mandatory structural section at L84).
5. The fallback finds the heading, returns `has_disputes = true`.

For Phase 6 trigger evaluation, this means: WTA multi-round arbitration will ALWAYS be triggered when `trigger: disputes_remain`, regardless of whether actual disputes exist. This is the "default to true" safety behavior (CONV-6 from Round 1), so both teams agreed this is the correct failure direction. But it means WTA arbitration cannot be conditionally skipped based on disputes -- the trigger is a permanent "always run."

**Clarification of the stagnation detection path (narrowing scope):**

I concede that Blue is correct on one point: the stagnation detection path (between-round comparison) reads per-round syntheses, which DO have markers. If the LLM follows the template, the primary marker path succeeds for stagnation detection. THREAT-05's false-stagnation risk for the between-round path requires the LLM to drop markers from the per-round synthesis output -- condition (a) in Blue's argument. I accept this narrowing.

But the Phase 6 trigger evaluation path is a SEPARATE consumer of the Dispute-Parsing Subsystem, and for this consumer, the failure is NOT conditional on LLM behavior. The failure is guaranteed by template structure (THREAT-10's absence of markers in the cross-round synthesis template) plus the WTA fallback heading choice (`## Runner-Up` is always present).

**The result:** WTA with `trigger: disputes_remain` degrades to `trigger: always` for multi-round runs. The arbiter always runs, even when the cross-round synthesis explicitly states "No remaining contested positions -- the final ranking is decisive across all evaluated criteria" (template L106). This wastes an agent launch and produces an arbitration resolution for a verdict that was already uncontested.

**Why this is MEDIUM, not LOW:**

Blue argues that false triggering is "operational annoyance, not quality degradation." I disagree. The arbitration resolution is a binding document. When an arbiter runs on an uncontested verdict, they must still produce a ruling -- they cannot output "nothing to do." The ruling will either:
- Affirm the verdict (correct but wasteful), or
- Override the verdict (incorrect -- no disputes justified override, but the arbiter was invoked and felt compelled to add value), or
- Produce a confused document that notes there are no disputes but still follows the template's ruling structure.

The third outcome is the most likely with an LLM arbiter. A document that says "there are no disputes to resolve" but is structured as a binding ruling creates ambiguity in the deliberation record. Is the arbitration resolution binding or vacuous? The cooperative template avoids this by providing the empty-case fallback instruction -- the non-cooperative templates do not (THREAT-02).

**Severity: MEDIUM.** The Phase 6 trigger path for WTA multi-round runs has a guaranteed false-positive due to the interaction between THREAT-10 (missing markers in cross-round synthesis) and the WTA fallback heading (`## Runner-Up`). This is not conditional on LLM behavior. I narrow the stagnation-detection scope (between-round comparison) to acknowledge Blue's three-condition argument there, but the Phase 6 trigger scope is a new, non-conditional attack vector.

---

## Round 1 Remediation Sufficiency Assessment

Round 1 produced a clear remediation plan. This section evaluates whether the proposed fixes are sufficient.

### THREAT-01 Remediation: SUFFICIENT

**Proposed fix**: Add `{PRIOR_ROUND_SECTION}` to `templates/{red-blue,winner-take-all,prisoners-dilemma}/review.md`.

This is a single variable addition to three files. The variable is already defined in SKILL.md (L368-375) and populated by the orchestrator for all modes. The cooperative template demonstrates the correct placement (L21, between `{PRIOR_FILES_SECTION}` and the "Read every file" instruction). The fix is mechanical and complete.

### THREAT-10 Remediation: INSUFFICIENT

**Proposed fix**: Add `DISPUTES_BEGIN`/`DISPUTES_END` markers to all four cross-round synthesis templates.

The fix is correct but incomplete. Adding markers to the template instructs the cross-round synthesizer LLM to include them in its output. But the cross-round synthesis templates are prompt engineering documents, not deterministic templates. The LLM must reproduce the markers in its output. The per-round synthesis templates demonstrate the pattern: they wrap the dispute section in markers (e.g., `templates/winner-take-all/synthesis.md` L106-110). The cross-round synthesis templates should use the same pattern.

**Missing remediation element**: The fix should also add markers to the cross-round synthesis template's `### Remaining Disputes` section (or mode-equivalent) in the same structural position as the per-round synthesis templates. Specifically:

- Cooperative cross-round (`templates/cooperative/cross-round-synthesis.md` L90): wrap `### Remaining Disputes` section in markers.
- Red-blue cross-round (`templates/red-blue/cross-round-synthesis.md` L114): wrap `### Disputed Risks` section in markers.
- Winner-take-all cross-round (`templates/winner-take-all/cross-round-synthesis.md` L95): wrap `### Remaining Disputes` section in markers.
- Prisoners-dilemma cross-round (`templates/prisoners-dilemma/cross-round-synthesis.md` L101): wrap `## Disputed Boundaries` section in markers.

This is what "add markers" means in practice. The proposed fix description from Round 1 is correct in intent but should be explicit about the placement pattern.

### THREAT-02 Remediation: SUFFICIENT BUT SHOULD BE EXPANDED

**Proposed fix**: Add `{REMAINING_DISPUTES}` and empty-case fallback instruction to three non-cooperative arbitration templates.

The fix is correct. The cooperative template provides the reference implementation (L34-40). Each non-cooperative template needs:
1. An "Extracted Remaining Disputes" section header.
2. The `{REMAINING_DISPUTES}` variable.
3. The empty-case fallback instruction ("If this section is empty, read the full synthesis to identify any remaining disputes").

The fix is sufficient for the variable gap. However, the WTA arbitration template has an additional issue noted in this review: it directs the arbiter to the "Runner-Up" section rather than to a disputes section. Adding `{REMAINING_DISPUTES}` to the WTA template should be accompanied by text directing the arbiter to also check the "Remaining Disputes" section of the synthesis, not just the "Runner-Up" section.

### THREAT-05 Remediation: PARTIALLY SUFFICIENT

**Proposed fix**: Change WTA fallback heading from `## Runner-Up` to `### Remaining Disputes` in SKILL.md L675.

This fix addresses the stagnation detection fallback path (between-round comparison). It does NOT address the Phase 6 trigger evaluation path for multi-round WTA runs, because the Phase 6 trigger path reads the cross-round synthesis, which lacks markers regardless of the fallback heading fix. If THREAT-10 is also fixed (markers added to cross-round synthesis templates), then THREAT-05's Phase 6 trigger issue is also resolved as a side effect.

**Dependency**: THREAT-05's full remediation depends on THREAT-10 being fixed first. The Round 1 remediation plan correctly prioritizes THREAT-10 as P2 and THREAT-05 as P3, but should note the dependency explicitly.

### THREAT-04 Remediation: SUFFICIENT

**Proposed fix**: Update spec.md FR-009 heading table to match SKILL.md/template headings.

No additional concerns.

---

## Compound Failure Scenario

Round 1 treated each threat independently. This section describes a compound failure mode that emerges from the interaction of THREAT-10, THREAT-02, and THREAT-05.

### Scenario: WTA Multi-Round Arbitration with `trigger: disputes_remain`

**Configuration**: `mode: winner-take-all`, `rounds: 3`, `stagnation: detect`, `arbiter: { trigger: disputes_remain }`

**Execution path**:

1. Rounds 1-3 execute. Per-round syntheses contain markers (per-round synthesis templates are correct). Stagnation detection uses the primary marker path. No false stagnation.

2. Cross-round synthesis is produced at `{output}/summary/final.md`. The WTA cross-round synthesis template lacks markers (THREAT-10). The LLM produces a synthesis with `## Runner-Up` (mandatory section) and `### Remaining Disputes` (with content "No remaining contested positions -- the final ranking is decisive across all evaluated criteria").

3. Phase 6 trigger evaluation: Dispute-Parsing Subsystem reads the cross-round synthesis. Primary marker path fails (no markers). Fallback heading path searches for `## Runner-Up`. Finds it (always present). Returns `has_disputes = true`. Phase 6 is triggered.

4. Phase 6 template variable population: Orchestrator extracts `{REMAINING_DISPUTES}` from the cross-round synthesis. Primary marker path fails (no markers, same as step 3). Fallback heading path extracts content under `## Runner-Up`. The extracted content is the runner-up analysis, NOT the actual disputes section. The extraction is semantically wrong -- it contains "Why they lost" and "Conditions for reconsideration," not contested positions.

5. The WTA arbitration template does not contain `{REMAINING_DISPUTES}` (THREAT-02). Even the semantically wrong extraction from step 4 is never injected. The arbiter receives the full synthesis and prose instructions to read the "Runner-Up" section.

6. The arbiter produces a resolution affirming or overriding the verdict. The verdict was uncontested. The resolution is binding but addresses no actual dispute.

**Net effect**: A wasteful, potentially confusing arbitration resolution is produced for an uncontested verdict. No data is corrupted, no decisions are invalidated, but the deliberation record contains a binding arbitration resolution that resolves nothing. A human reader must determine whether the resolution is substantive or vacuous.

**Severity of compound scenario**: MEDIUM. It is wasteful and confusing but not destructive. However, it demonstrates that the three disputed threats are not independent -- they form a degradation cascade where each compounds the next.

---

## Updated Threat Scorecard

| ID | Threat | Round 1 Severity | Round 2 Severity | Change | Argument |
|----|--------|-----------------|-----------------|--------|----------|
| THREAT-10 | Cross-round synthesis templates lack markers | HIGH | HIGH | Maintained | Three of four affected templates are spec 004 authorship, not inherited. Per-round synthesis templates in the same mode directories DO have markers, proving the pattern was available. |
| THREAT-02 | Missing `{REMAINING_DISPUTES}` in non-cooperative arbitration | MEDIUM | MEDIUM | Maintained | Compound interaction with THREAT-10 creates double degradation. WTA arbiter directed to Runner-Up section, not disputes section. |
| THREAT-05 | WTA fallback heading causes false stagnation/triggering | MEDIUM | MEDIUM | Refined scope | Narrowed stagnation-detection scope (Blue's three-condition argument accepted). Widened Phase 6 trigger scope (non-conditional, guaranteed false-positive for WTA multi-round with `trigger: disputes_remain`). |

---

## Recommendations for Round 2

1. **Accept THREAT-10 at HIGH.** The inheritance argument does not hold for spec-004-authored templates. The contract violation is not latent -- it fires on every multi-round arbitration path.

2. **Accept THREAT-02 at MEDIUM.** The compound interaction with THREAT-10 means the missing variable is the missing second line of defense, not just a missing convenience feature.

3. **Accept THREAT-05 at MEDIUM.** The Phase 6 trigger evaluation path is a non-conditional attack vector that does not require LLM marker-dropping. The between-round stagnation path is conditionally gated (Blue's argument accepted there).

4. **Note the THREAT-10 to THREAT-05 fix dependency.** THREAT-05's Phase 6 trigger issue resolves automatically when THREAT-10 is fixed. The remediation plan should reflect this dependency.

5. **Expand WTA arbitration template remediation.** When adding `{REMAINING_DISPUTES}`, also add a prose instruction directing the arbiter to check the "Remaining Disputes" section, not just the "Runner-Up" section.
