# Cross-Round Synthesis: Spec 004 -- Universal Rounds

**Synthesizer**: Neutral (cross-round)
**Date**: 2026-03-20
**Rounds completed**: 2 of 3
**Termination reason**: Converged (all disputes resolved)
**Target**: Spec 004 -- Universal Rounds, Stagnation Detection, and Arbitration
**Spec path**: `<HOME>/code/payer-index-mono/conversus/specs/004-universal-rounds/spec.md`

---

## Process Summary

| Metric | Round 1 | Round 2 | Cumulative |
|--------|---------|---------|------------|
| Phases completed | 4 | 4 | 8 |
| Artifacts produced | 10 | 8 | 18 |
| Threats proposed | 12 | 0 (new) | 12 |
| Threats withdrawn | 6 | 0 | 6 |
| Threats surviving | 6 | 6 | 6 |
| Severity disputes open | 3 | 0 | 0 |
| Convergence points | 11 | 8 (new) | 19 |
| Factual errors identified | 1 (Blue: population-vs-consumption) | 1 (Blue: Phase 6 execution ordering) | 2 |

The deliberation ran two rounds. Round 1 established the threat catalog: 12 proposed threats were triaged to 6 surviving (1 CRITICAL, 1 HIGH, 2 MEDIUM, 1 LOW, plus 1 MEDIUM documentation issue), with 6 withdrawn as derivative, cosmetic, speculative, or correctly designed behavior. Round 1 ended with three severity disputes -- THREAT-10 (HIGH vs. MEDIUM), THREAT-02 (MEDIUM vs. LOW), and THREAT-05 (MEDIUM vs. LOW).

Round 2 resolved all three disputes. The Defender self-identified a factual error about Phase 6 execution ordering (claiming Phase 6 trigger evaluation runs before the cross-round synthesis is written, contradicted by SKILL.md L502-540). This self-correction cascaded into three concessions: THREAT-10 elevated to HIGH, THREAT-02 elevated to MEDIUM, and THREAT-05 elevated to MEDIUM. The Attacker also made two concessions: the compound "double degradation" framing for THREAT-02 was withdrawn, and THREAT-05's between-round stagnation scope was accepted as LOW-probability. The deliberation terminated at convergence with zero severity disputes remaining.

---

## Risk Trajectory

This section tracks how each surviving threat evolved across rounds, documenting the analytical progression that produced the final risk register.

### THREAT-01: Missing `{PRIOR_ROUND_SECTION}` in non-cooperative review templates

| Dimension | Round 1 | Round 2 |
|-----------|---------|---------|
| Severity | CRITICAL (agreed) | CRITICAL (reaffirmed) |
| Dispute status | None | None |
| Key development | Blue conceded fully; identified as blocking gate | No change; both teams reaffirmed |

**Trajectory**: Stable from first contact. This was the deliberation's clearest finding -- both teams agreed immediately on its criticality. The non-cooperative review templates omit the `{PRIOR_ROUND_SECTION}` variable that the cooperative template contains. Without it, Round 2+ agents in red-blue, winner-take-all, and prisoners-dilemma modes receive no instruction to engage with prior-round output. Multi-round runs produce parallel independent analyses instead of iterative deepening, defeating the spec's core purpose. Blue's concession was notable: the defense's own architectural thesis ("all mode-specific behavior lives in templates") predicted the attack's strongest finding.

### THREAT-10: Cross-round synthesis templates lack `DISPUTES_BEGIN`/`DISPUTES_END` markers

| Dimension | Round 1 | Round 2 |
|-----------|---------|---------|
| Severity | Disputed (Red: HIGH, Blue: MEDIUM) | HIGH (converged) |
| Dispute status | Open | Resolved |
| Key development | Red argued blast-radius amplification; Blue argued inherited gap with functional fallback | Blue's Phase 6 ordering error self-corrected; conceded to HIGH |

**Trajectory**: This was the deliberation's most analytically productive dispute. In Round 1, the disagreement centered on whether a contract violation with a functional fallback constitutes HIGH (Red's framing) or MEDIUM (Blue's "degraded-but-functional" framing). Neither team could definitively prevail on that conceptual question alone.

Round 2 broke the deadlock on factual grounds. The Defender introduced a new argument -- that Phase 6 trigger evaluation runs before the cross-round synthesis is written, making the cross-round synthesis a "terminal artifact" with zero functional impact. The Attacker refuted this with SKILL.md L502-540, which documents the opposite ordering: cross-round synthesis production at L502-527, then Phase 6 at L529-598, with Phase 6 reading `{output}/summary/final.md` (L540). The Defender identified this error in their own cross-review and self-corrected, explicitly withdrawing the MEDIUM position. The factual resolution also revealed that three of four affected templates were authored by spec 004, undermining the "inherited gap" argument from Round 1.

### THREAT-02: Missing `{REMAINING_DISPUTES}` in non-cooperative arbitration templates

| Dimension | Round 1 | Round 2 |
|-----------|---------|---------|
| Severity | Disputed (Red: MEDIUM, Blue: LOW) | MEDIUM (converged) |
| Dispute status | Open | Resolved |
| Key development | Blue argued prose instructions are adequate mitigation | Defender conceded WTA prose direction gap; Attacker withdrew compound framing |

**Trajectory**: Both rounds contributed distinct analytical findings. Round 1 established the defensive-depth asymmetry: cooperative arbitration has three layers (prose instruction, pre-extracted `{REMAINING_DISPUTES}`, empty-case fallback) while non-cooperative templates have one (prose instruction only). Blue argued prose instructions ("Pay special attention to the synthesis's 'Disputed Risks' section") are adequate for an LLM arbiter.

Round 2 introduced two developments. The Attacker proposed a compound failure argument (THREAT-10 + THREAT-02 as "double degradation"), which the Defender successfully rebutted -- the arbiter's information state is identical whether extraction is precise-and-discarded or approximate-and-discarded. The Attacker accepted this and withdrew the compound framing. Simultaneously, the Defender conceded a WTA-specific gap: the WTA arbitration template directs the arbiter to "Runner-Up" and "Conditions for reconsideration" rather than to any disputes section, providing zero mitigation for WTA. This concession elevated the overall threat to MEDIUM.

A minor analytical framing difference remains recorded: the Attacker views MEDIUM as an architectural consistency requirement (all three non-cooperative modes equally affected); the Defender views it as WTA-driven (red-blue and prisoners-dilemma individually LOW). This difference does not affect severity, priority, or remediation scope -- both teams agree the fix applies uniformly to all three templates.

### THREAT-05: WTA fallback heading causes false triggering

| Dimension | Round 1 | Round 2 |
|-----------|---------|---------|
| Severity | Disputed (Red: MEDIUM, Blue: LOW) | MEDIUM (converged) |
| Dispute status | Open | Resolved |
| Key development | Blue's direction-of-failure analysis corrected (from "may miss stagnation" to "always detects stagnation") | Attacker decomposed into two vectors; Defender conceded Phase 6 vector |

**Trajectory**: This threat underwent the most significant analytical refinement across rounds. In Round 1, Blue's original Phase 1 analysis of the failure direction was wrong -- stating the WTA `## Runner-Up` fallback heading "may miss stagnation" when the actual failure mode is "always detects stagnation" (premature termination). Blue corrected this in their Round 1 revision but maintained LOW severity on the basis that the failure requires three conditions simultaneously (LLM drops markers, mode is WTA, rounds > 1).

Round 2 produced a breakthrough decomposition. The Attacker split THREAT-05 into two distinct attack vectors by consumer: Vector A (between-round stagnation detection, which reads per-round synthesis files that DO contain markers) and Vector B (Phase 6 trigger evaluation, which reads the cross-round synthesis that LACKS markers per THREAT-10). The Attacker conceded Vector A as LOW (accepting the three-condition gating). The Defender conceded Vector B as MEDIUM -- it is non-conditional and produces deterministic degradation: WTA with `trigger: disputes_remain` degrades to `trigger: always` for every multi-round run. Critically, Vector B resolves automatically when THREAT-10 is fixed.

### THREAT-04: Spec FR-009 heading table stale

| Dimension | Round 1 | Round 2 |
|-----------|---------|---------|
| Severity | MEDIUM (agreed) | MEDIUM (reaffirmed) |
| Dispute status | None | None |

**Trajectory**: Stable. The spec's FR-009 heading table uses different headings than SKILL.md and the actual templates. SKILL.md and templates agree with each other; only the spec document is wrong. Documentation drift with no runtime impact. SKILL.md L594 directs maintainers to templates as the source of truth. Both teams agreed on MEDIUM in Round 1; no Round 2 dispute.

### THREAT-06: WTA lacks named dispute entry pattern

| Dimension | Round 1 | Round 2 |
|-----------|---------|---------|
| Severity | LOW (agreed) | LOW (reaffirmed) |
| Dispute status | None | None |

**Trajectory**: Stable. The primary marker-based path handles WTA dispute counting adequately via binary content detection. The fallback concern is captured by THREAT-05. Both teams agreed on LOW in Round 1; no Round 2 dispute.

---

## Defense Effectiveness Progression

### Round 1 Defense Performance

The Defender's Round 1 performance was mixed. The defense successfully eliminated 6 of 12 threats through precise rebuttals:

- **Strong defenses**: THREAT-11 reframing (stagnation + arbitration as intentional design sequence), THREAT-12 verification (no cooperative artifact modified), THREAT-09 (parsing target identification -- Dispute-Parsing Subsystem reads Phase 5, not Phase 4), THREAT-03 (derivative of THREAT-01, not independent).
- **Critical failure**: Missing THREAT-01 entirely. The defense verified that the engine populates round-aware variables without verifying that templates consume them. This population-vs-consumption error was the root cause of the defense's biggest miss and became a recurring methodological lesson.
- **Severity underestimation**: Defended THREAT-10, THREAT-02, and THREAT-05 at one severity level below the final consensus. The defense relied on "functional fallback exists" as a blanket mitigation, underweighting contract violation and blast-radius amplification arguments.

### Round 2 Defense Performance

The Defender's Round 2 performance showed marked improvement in intellectual honesty despite introducing a new factual error:

- **Self-correction**: The Defender identified their own Phase 6 execution ordering error in cross-review of the Attacker -- a methodological improvement over Round 1, where errors were only identified by Red. The self-correction was explicit and immediate.
- **Pattern recognition**: The Defender identified the recurring analytical pattern across both rounds (verifying one instance of a category and incorrectly generalizing to all instances) and acknowledged it explicitly.
- **Concession quality**: All three Round 2 concessions were substantive and well-reasoned rather than reluctant capitulations.
- **Persistent weakness**: The initial Phase 6 ordering claim ("Phase 6 trigger evaluation runs BEFORE the cross-round synthesis is written") was a factual assertion made without source verification -- the same category of error as Round 1's population-vs-consumption gap.

### Round 2 Attack Performance

The Attacker's Round 2 performance demonstrated disciplined narrowing:

- **Vector decomposition**: The two-vector decomposition of THREAT-05 (between-round stagnation vs. Phase 6 trigger) was the analytical highlight of Round 2, separating a conditional low-probability path from a deterministic degradation path.
- **Concession discipline**: The Attacker withdrew the compound "double degradation" framing for THREAT-02 when the Defender demonstrated it did not add marginal harm. The Attacker also accepted the three-condition gating argument for THREAT-05 Vector A. These concessions narrowed the attack surface to its strongest structural arguments.
- **No overreach**: The Attacker proposed zero new threats in Round 2, focusing entirely on resolving the disputed severities with sharper evidence. This focus was appropriate for the deliberation's state.

---

## Final Risk Register

| ID | Threat | Severity | Priority | Fix | Blocking? | Convergence Round |
|----|--------|----------|----------|-----|-----------|-------------------|
| THREAT-01 | Missing `{PRIOR_ROUND_SECTION}` in non-cooperative review templates | **CRITICAL** | P1 | Add variable to `templates/{red-blue,winner-take-all,prisoners-dilemma}/review.md` | **Yes** -- spec 004 cannot exit Draft | R1 |
| THREAT-10 | Cross-round synthesis templates lack `DISPUTES_BEGIN`/`DISPUTES_END` markers | **HIGH** | P2 | Add markers to all four `cross-round-synthesis.md` templates (including cooperative). Also resolves THREAT-05 Vector B. | **Yes** -- guaranteed degradation on every multi-round arbitration path | R2 |
| THREAT-02 | Missing `{REMAINING_DISPUTES}` in non-cooperative arbitration templates | **MEDIUM** | P2 | Add variable + empty-case fallback to three non-cooperative arbitration templates. WTA: add prose direction to "Remaining Disputes" section. | No | R2 |
| THREAT-05 | WTA fallback heading causes false triggering | **MEDIUM** | P3 | Change WTA fallback heading from `## Runner-Up` to `### Remaining Disputes` in SKILL.md L675. Dependency: THREAT-10 fix resolves Phase 6 vector; this fix is defense-in-depth. | No | R2 |
| THREAT-04 | Spec FR-009 heading table stale | **MEDIUM** | P3 | Update spec.md FR-009 heading table to match SKILL.md/template headings | No | R1 |
| THREAT-06 | WTA lacks named dispute entry pattern | **LOW** | -- | No immediate fix; primary marker path adequate; fallback concern captured by THREAT-05 | No | R1 |

### Remediation Dependencies

```
THREAT-01 (P1, CRITICAL) -- independent, no dependencies
    |
THREAT-10 (P2, HIGH) -- independent
    |--- resolves THREAT-05 Vector B (Phase 6 trigger) as side effect
    |
THREAT-02 (P2, MEDIUM) -- independent
    |
THREAT-04 (P3, MEDIUM) -- independent
    |
THREAT-05 (P3, MEDIUM) -- defense-in-depth; primary fix is THREAT-10
```

### Confirmed Compound Failure Scenario

Both teams verified and agree on the following structural interaction for WTA multi-round arbitration with `trigger: disputes_remain`:

1. Cross-round synthesis template lacks markers (THREAT-10).
2. Phase 6 trigger evaluation reads the cross-round synthesis (SKILL.md L540).
3. Dispute-Parsing Subsystem primary path fails; heading-based fallback fires.
4. WTA fallback heading `## Runner-Up` is always present (THREAT-05).
5. `has_disputes = true` always, regardless of actual dispute state.
6. WTA with `trigger: disputes_remain` degrades to `trigger: always`.
7. Arbiter produces a binding resolution for an uncontested verdict.

Net effect: wasteful and potentially confusing but not destructive. Resolves when THREAT-10 is fixed.

### Overall Assessment

Spec 004's engine changes (removing validation guards, adding Phase 6 heading rows) are correct and safe. The engine is mode-agnostic as the spec claims. The template layer has five identified gaps requiring remediation, two of which (THREAT-01 at CRITICAL, THREAT-10 at HIGH) are blocking gates for spec acceptance. All fixes are template-layer edits or documentation corrections -- no engine changes are needed. This assessment was consistent across both rounds and reinforced by Round 2's deeper analysis of execution ordering and attack vector decomposition.

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Disputed Risks

No disputed risks remain. All severity disputes were resolved in Round 2.

One minor analytical framing difference is recorded for completeness but does not constitute a dispute:

THREAT-02's MEDIUM severity is interpreted differently by the two teams -- the Attacker frames it as an architectural consistency requirement across all three non-cooperative modes, while the Defender frames it as driven specifically by the WTA prose direction gap. Both framings produce identical outcomes: MEDIUM severity, P2 priority, and the fix applied uniformly to all three non-cooperative arbitration templates. No action required.
<!-- CONVERSUS:DISPUTES_END -->

---

## Termination Assessment

### Convergence Justification

The deliberation terminated after Round 2 with the termination reason "converged (all disputes resolved)." This assessment is justified:

1. **Zero severity disputes remain.** Round 1 ended with three contested severities. Round 2 resolved all three through a combination of factual correction (Phase 6 execution ordering), analytical decomposition (THREAT-05 two-vector split), and mutual concession (THREAT-02 compound framing withdrawal). Both teams explicitly recommended that no Round 3 adjudication is needed.

2. **No new threats emerged.** Round 2 introduced zero new threats. The Attacker focused entirely on resolving disputed severities with sharper evidence. The one new attack vector identified (THREAT-05 Phase 6 trigger vector) was a decomposition of an existing threat, not a novel discovery.

3. **The threat catalog is stable.** Six threats withdrawn in Round 1 remained withdrawn throughout Round 2. No withdrawal was challenged or reopened. The six surviving threats have agreed severities, priorities, and remediations.

4. **Both teams conceded material positions.** Convergence was not one-sided. The Attacker withdrew the compound framing for THREAT-02 and accepted the three-condition gating for THREAT-05 Vector A. The Defender elevated three threats and self-corrected a factual error. This mutual movement indicates genuine analytical convergence rather than exhaustion.

### Value of Round 2

Round 2 was productive. Without it:

- THREAT-10 would remain at disputed severity (HIGH vs. MEDIUM), lacking the Phase 6 execution ordering analysis that proved the cross-round synthesis is read by Phase 6.
- THREAT-05 would not have the two-vector decomposition that separates the conditional low-probability path from the deterministic degradation path.
- THREAT-02 would lack the WTA-specific prose direction gap that elevated it from LOW to MEDIUM.
- The compound failure scenario (THREAT-10 + THREAT-05 Vector B) would not have been identified and documented.
- The remediation dependency between THREAT-10 and THREAT-05 would not have been established.

### Round 3 Assessment

A third round is not warranted. The threat register has reached full convergence on severity, priority, and remediation. The sole remaining analytical difference (THREAT-02 framing) is explicitly acknowledged by both teams as producing no difference in any actionable decision. Further deliberation would not improve the quality of the risk register or change any remediation plan.
