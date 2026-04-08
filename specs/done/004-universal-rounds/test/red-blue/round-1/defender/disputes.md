# Final Defender Disputes: Spec 004 — Universal Rounds

**Role**: Blue Team Defender (Final Position)
**Date**: 2026-03-20
**Phase**: Final disputes before synthesis

---

### Remaining Disputes

**Dispute: THREAT-10 severity should be MEDIUM, not HIGH.**

Red rates THREAT-10 (cross-round synthesis templates lacking `DISPUTES_BEGIN`/`DISPUTES_END` markers) as HIGH. The defense disputes this severity for two reasons:

1. **The gap is inherited, not introduced by spec 004.** The cooperative cross-round synthesis template (from spec 002) also lacks these markers. Spec 004's three new cross-round synthesis templates are structurally consistent with the existing cooperative template. Calling this HIGH implies spec 004 introduced a regression when it actually replicated the established pattern. If the cooperative cross-round synthesis template was acceptable without markers in spec 002, the same pattern in spec 004 templates should carry the same severity.

2. **The three-tier fallback prevents functional failure.** Red concedes that the default-to-true failure mode means Phase 6 is never skipped. Red's own revision states: "The functional safety net works." The remaining concern is extraction quality degradation (heading-based vs. marker-based parsing). Quality degradation with a working fallback is MEDIUM, not HIGH. HIGH should be reserved for threats where the system fails to perform its function, not where it performs it with reduced precision.

The fix is agreed upon (P2: add markers to all four cross-round synthesis templates, including cooperative). The dispute is strictly about severity classification: MEDIUM for a quality gap with a functional safety net on an inherited pattern, not HIGH.

---

**Dispute: THREAT-02 severity should be LOW, not MEDIUM.**

Red downgraded THREAT-02 from HIGH to MEDIUM, but the defense argues LOW is more appropriate given the totality of mitigations:

1. **Prose instructions are present and specific.** Each non-cooperative arbitration template explicitly directs the arbiter to the correct synthesis section by name ("Pay special attention to the synthesis's 'Disputed Risks' section" for red-blue, etc.). This is not a vague hint; it is a named-section reference.

2. **The full synthesis is provided as a readable document.** The arbiter receives `{SYNTHESIS_PATH}` pointing to the complete synthesis. An LLM arbiter instructed to "pay special attention to" a named section in a document it has full access to will reliably locate and process that section.

3. **The asymmetry with cooperative is a polish gap, not a correctness gap.** The cooperative template's `{REMAINING_DISPUTES}` pre-extraction saves the arbiter from locating the section itself. This is a convenience optimization. The non-cooperative templates achieve the same outcome through prose direction. The difference affects arbiter prompt efficiency, not arbiter decision quality.

The fix is still agreed upon (P2: add `{REMAINING_DISPUTES}` to non-cooperative arbitration templates). The dispute is whether the current state is MEDIUM (implying material quality impact) or LOW (implying a polish improvement with no measurable quality delta).

---

**Dispute: THREAT-05 severity should be LOW, not MEDIUM.**

Red maintains THREAT-05 (WTA fallback heading causing false stagnation) at MEDIUM because "the fallback IS the safety net, and a broken safety net is a real concern." The defense disputes this for two reasons:

1. **The primary path works correctly.** Both teams agree: when structural markers are present (the primary path), WTA stagnation detection is correct. The WTA per-round synthesis template includes `DISPUTES_BEGIN`/`DISPUTES_END` markers around `### Remaining Disputes`, and the marker-based path counts entries correctly. The fallback is the degraded path, not the primary path.

2. **The probability of the fallback firing is low and decreasing.** The fallback fires only when the LLM drops structural markers from its synthesis output. These are HTML comments (`<!-- CONVERSUS:DISPUTES_BEGIN -->`) that LLMs reliably preserve because they are not visible content the LLM would want to edit. The marker upgrade is tracked as a continuation item (SKILL.md L569), meaning the system is moving toward marker-first parsing, not away from it.

3. **The failure mode is conservative, not dangerous.** False stagnation (premature termination at Round 2) is wasteful but not harmful. The system produces fewer rounds than configured, but each round's output is complete and correct. No data is corrupted; no incorrect decisions are produced. The user can re-run with `stagnation: ignore` to bypass the issue. This is a LOW-severity operational annoyance, not a MEDIUM-severity quality degradation.

The fix is agreed upon (P3: change WTA fallback heading). The dispute is severity classification.

---

### Convergence

The following threat assessments are agreed upon by both teams:

1. **THREAT-01 — CRITICAL.** Missing `{PRIOR_ROUND_SECTION}` in non-cooperative review templates. Both teams agree this is the highest-priority finding, the fix is straightforward (add the variable to three review templates), and it must be remediated before non-cooperative multi-round runs are production-ready. No dispute on severity or priority.

2. **THREAT-04 — MEDIUM.** Spec FR-009 heading table diverges from SKILL.md/template reality. Both teams agree this is documentation drift with no runtime impact. The spec is Draft status and should be updated before finalization. P3 fix.

3. **THREAT-06 — LOW.** WTA dispute counting lacks a named entry pattern. Both teams agree the primary marker-based path handles this adequately via binary content detection, and the fallback concern is already captured in THREAT-05.

4. **THREAT-03, 07, 08, 09, 11, 12 — WITHDRAWN.** Red withdrew six threats after Blue's defenses. These are fully resolved with no remaining dispute.

5. **Engine mode-agnosticism.** Both teams confirm the round loop, stagnation detection algorithm, Phase 6 trigger evaluation, template loading, and variable population are mode-agnostic. No engine changes are needed beyond removing two validation guards and adding Phase 6 heading rows.

6. **Cooperative backward compatibility.** Both teams confirm no cooperative-mode artifact was modified. The SKILL.md validation table change was additive. All existing cooperative behavior is preserved.

7. **Default-to-true failure mode.** Both teams agree the Dispute-Parsing Subsystem's default behavior (return true when parsing fails) is the correct failure mode for Phase 6 triggering. Running an unnecessary arbitration is preferable to skipping a necessary one.

8. **Remediation priority order.** Both teams agree on the priority ranking:
   - P1: `{PRIOR_ROUND_SECTION}` in non-cooperative review templates (THREAT-01)
   - P2: Structural markers in cross-round synthesis templates (THREAT-10)
   - P2: `{REMAINING_DISPUTES}` in non-cooperative arbitration templates (THREAT-02)
   - P3: WTA fallback heading fix (THREAT-05)
   - P3: Spec FR-009 heading table update (THREAT-04)

9. **No engine-level changes required.** All remediation items are template-layer edits or documentation updates. The engine architecture is validated.

10. **Template completeness is the correctness condition.** Both teams agree that when templates carry all mode-specific behavior, template completeness determines feature completeness. This was the defense's architectural thesis and the attack's most productive critique applied to the same thesis.

---

### Final Position Statement

#### Non-Negotiables

1. **THREAT-01 is CRITICAL and must be P1.** No dispute. This is the single most important finding. Non-cooperative multi-round runs are non-functional without `{PRIOR_ROUND_SECTION}` in review templates. The fix is a single variable addition to three files and must be applied before any non-cooperative multi-round execution.

2. **The engine is correct and requires no structural changes.** All six surviving/modified threats are template-layer or documentation issues. The engine's mode-agnostic architecture is validated by both teams. No remediation item touches engine logic beyond the already-specified validation guard removal (FR-001) and Phase 6 heading table addition (FR-009).

3. **All five remediation items are accepted.** The defense concedes every gap identified. The dispute is not about WHETHER to fix these issues, but about how to CLASSIFY their severity for prioritization. All five fixes should be applied.

4. **Cross-round synthesis marker gap (THREAT-10) predates spec 004.** The cooperative cross-round synthesis template from spec 002 also lacks markers. Spec 004 replicated an existing pattern. The fix should apply to all four templates (including cooperative), and the remediation should be attributed to the inherited gap, not to spec 004 as a regression.

#### Flexibility

1. **THREAT-10 severity: willing to accept MEDIUM-HIGH as a compromise.** The defense argues MEDIUM (functional safety net works, inherited pattern). Red argues HIGH (stable interface contract violation). A MEDIUM-HIGH classification acknowledging that the contract violation is real but the functional impact is limited by the three-tier fallback would be acceptable. The priority (P2) is not in dispute.

2. **THREAT-02 severity: willing to accept MEDIUM if synthesis captures the prose-instruction mitigation.** If the final synthesis explicitly notes that the non-cooperative arbitration templates DO contain prose instructions directing the arbiter to the correct section, the defense can accept MEDIUM. The concern is that a bare "MEDIUM" classification without context implies the arbiter receives no guidance, which is factually incorrect.

3. **THREAT-05 severity: willing to accept MEDIUM if synthesis captures the conditional nature.** If the final synthesis explicitly notes that this threat only manifests when (a) the LLM drops structural markers AND (b) the mode is winner-take-all AND (c) rounds > 1, the defense can accept MEDIUM. The threat requires three conditions to fire simultaneously. A bare "MEDIUM" without the conditional framing overstates the real-world likelihood.

4. **Remediation ordering is flexible within priority tiers.** P2 items (THREAT-10 and THREAT-02) can be done in either order. P3 items (THREAT-05 and THREAT-04) can be done in either order. Only P1 (THREAT-01) is strictly first.

5. **Spec 004 status classification is flexible.** The defense's position is that spec 004 is "architecturally correct but template-incomplete." If the synthesis prefers "spec 004 has five identified gaps requiring remediation before non-cooperative multi-round readiness," that is acceptable. The defense objects only to characterizations that imply the engine design is flawed or that the spec's approach was wrong. The template-first approach is correct; the templates were not finished.
