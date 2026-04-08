# Phase 4 Disputes: implementation-verifier

**Date**: 2026-04-01

---

## Remaining Disputes

### Dispute 1: CSI-3 severity — P3 (consistency-auditor revised) vs. "do not track until Remediation 6" (my preference)

The consistency-auditor downgraded CSI-3 (equilibrium score discontinuity) from P2 to P3 with a "re-evaluate at Remediation 6" note. The test-coverage-auditor proposed a CSI-3 characterization test (pass non-zero eq_scores through the Kalman filter). I maintain that tracking a dormant bug in code that does not yet exist adds noise to the priority list.

**My position**: CSI-3 should be recorded as a **design note** attached to spec 022 Remediation 6, not as a standalone P3 recommendation. When Remediation 6 is scheduled, the design note surfaces automatically as a prerequisite. Tracking it as a P3 in the meta-review creates an item that no one can act on until another item (Remediation 6) is started. The test-coverage-auditor's characterization test is interesting but tests hypothetical behavior (non-zero eq_scores) that the codebase does not currently produce.

**Concession path**: If the meta-review summary includes a "preconditions" section linking future work items to their prerequisites, I will accept P3. Otherwise, the item will be lost in a priority list where everything above P3 is more actionable.

### Dispute 2: Whether "mislocated" should replace "inaccurate" in my verification summary

My revision adopted the consistency-auditor's suggestion to reclassify the 2 spec 021 findings from "INACCURATE" to "MISLOCATED." The test-coverage-auditor (T-4) noted the executive summary/detail mismatch but did not explicitly address the terminology change. The dependency-auditor did not comment.

**My position**: I maintain the terminology change. "INACCURATE" implies the synthesis fabricated a finding; "MISLOCATED" correctly conveys that the finding is real but attributed to the wrong file. This is important for stakeholder communication: spec 021's synthesis is not unreliable, it just confused two files within the same package. No remaining dispute — this is converged.

---

## Convergence

### Full convergence on:

1. **18 VERIFIED, 2 MISLOCATED, 0 STALE**: The corrected verification summary is accepted by all. The executive summary correction is my responsibility.

2. **Test-first for all P1 fixes**: All 4 reviews now agree that failing tests should be written before code changes for P1 bugs. This is the strongest process convergence from the deliberation.

3. **R-1 -> R-3 sequencing**: The scaffold extension fix must precede the delegation refactor. No dispute.

4. **Fix list should annotate cross-boundary changes**: My new recommendation (Architecture-NEW-1) is accepted by the dependency-auditor and not challenged by others.

5. **The `.mod` file extraction should use `importlib.resources`**: My caveat about avoiding filesystem deployment dependencies was not challenged.

6. **Mathematical correctness assessments are reliable**: No reviewer challenged the Shapley, Kalman, or potential game verifications. The mathematical foundations are the highest-confidence area across all 4 reviews.

7. **Specs 025/026 are the healthiest**: Unanimous across all 4 reviews — all claims verified, all SC tests pass, clean dependencies, no cross-spec issues.

8. **Spec 021 is the weakest**: Unanimous. Mislocated findings, most untested P1s, missing acceptance criteria tests, source of cross-spec inconsistencies.

9. **The `DomainScore.variables` bug is the consensus exemplar**: Four independent reviews converged on this single bug from four different angles (cross-spec impact, code verification, dependency safety, test gap). This validates the multi-perspective meta-review process.

10. **Plugin wrappers are the correct target for `PluginResult` changes**: The consistency-auditor, dependency-auditor, and I all agree that provenance keys and error-path behavior belong in the plugin wrapper layer, not the pure function layer.

---

## Final Position

My verification methodology proved robust through the deliberation. The 18 verified findings are unchallenged, and the 2 mislocated findings were correctly identified by both me and the consistency-auditor (who traced the misattribution to its cross-spec consequence).

The deliberation's main contribution to my work was:

1. **Test-first principle**: I now recommend failing tests for all 5 immediate fixes, not just the fixes themselves. This is a process improvement that makes each fix self-validating.

2. **Terminology precision**: "MISLOCATED" is more accurate than "INACCURATE" for the spec 021 findings.

3. **Sequencing constraints**: The R-1/R-3 dependency and the cross-boundary annotation for the scaffold fix are implementation details I should have captured in Phase 1.

4. **Severity calibration**: I agree with the consistency-auditor that CSI-3 is either P3 or a design note. The bug is real but dormant and contingent on future work.

My remaining dispute (CSI-3 as design note vs. P3) is minor and does not affect any current work item. I defer to the synthesis author's judgment on formatting.
