# Spec Compliance Auditor — Revision

**Agent**: spec-compliance-auditor
**Phase**: 3 (Revision after cross-review)
**Date**: 2026-03-24

---

## Recommendation Dispositions

### R01. Add `timing` and `influence` fields to `ArbiterConfig` — SURVIVING (P1)

**Status**: Unchanged. Universal agreement across all four auditors. This is the anchor recommendation of the entire deliberation.

### R02. Pass `INFLUENCE_LEVEL` in `build_arbitration_context()` — SURVIVING (P1)

**Status**: Unchanged. Universal agreement. All four auditors cite the same code path and mechanism.

### R03. Fix arbiter output directory name: `arbiter/` to `arbitration/` — MODIFIED (P1 -> P1 pending verification)

**Original**: P1, claiming `arbiter/` vs `arbitration/` mismatch causes path failures.
**Modification**: Retaining P1 classification IF the mismatch is confirmed, but flagging for ground truth verification. The guided-workflow-auditor's cross-review (DC-1) challenges the impact scope: SKILL.md handlers produce their own output and do not read from the engine's output directory. The arbitration-auditor's review claims output paths "match spec 006 US-4," directly contradicting this review's finding. The arbitration-auditor's cross-review (DC-1) calls for ground truth verification.

The impact assessment is revised: if the mismatch exists, it affects engine-direct consumers (MCP tools, SDK, tests checking output structure) but NOT guided workflow handlers (which produce their own output via Agent tool calls). The P1 classification is maintained for engine consumers because a path mismatch is a concrete failure, not a theoretical risk. But the claim that `/conversus arbitrate` would fail is withdrawn -- the guided-workflow-auditor correctly demonstrates that the handler does not read engine-produced output.

### R04. Populate `PRIOR_ARBITRATION_SECTION` in review context builders — SURVIVING (P1)

**Status**: Unchanged. The arbitration-auditor rates this P1 (their R4). The guided-workflow-auditor originally rated it P3 but upgraded to P1 in revision, accepting the arbitration-auditor's argument. Three of four auditors now agree on P1.

### R05. Populate `PRIOR_ROUND_SECTION` in review context builders — MODIFIED (P1 -> P2)

**Original**: P1, "Runtime Failure or Silent Incorrectness."
**Modification**: Downgraded to P2. The arbitration-auditor's cross-review (DC-2) correctly notes this is a round-awareness concern (spec 004), not a post-merge spec-006 gap. The guided-workflow-auditor's cross-review (DC-2) notes the engine passes `PRIOR_SYNTHESIS_PATH` and `PRIOR_ROUND_DIR` as separate fields, so agents may still receive prior-round context through individual path variables even when `PRIOR_ROUND_SECTION` is empty. The schema-integration-auditor's cross-review (DC-3) notes that if templates reference individual variables alongside the composite section, the agent still has access to prior-round information.

The P1 rating was based on "silent incorrectness," but the incorrectness is partial (individual path variables are populated) and pre-dates the spec 006-013 merge. This is a pre-existing gap, not a regression. P2 is appropriate.

### R06. Implement inter-round arbitration in `run_pipeline()` — MODIFIED (P2 -> P2, refined)

**Original**: P2, "Functional Gaps -- Not Crashes, But Missing Behavior."
**Modification**: Retaining P2 but refining the justification. The arbitration-auditor originally rated this P1 (their R2) but has downgraded to P2 in revision based on the sequencing argument: R01 must ship before R06 has any effect. The guided-workflow-auditor also moved from P1 to P2. Consensus is now P2 across all four auditors.

The refinement: R06 should ship atomically with or immediately after R01. A parsed `timing: inter-round` field with no behavioral effect is marginally worse than a silently dropped field -- it gives users a false sense that their configuration is honored.

### R07. Implement influence-aware dispute counting — SURVIVING (P2)

**Status**: Unchanged. The arbitration-auditor's R5 provides detailed per-influence-level semantics that align with this recommendation. The guided-workflow-auditor subsumes this under inter-round arbitration generally. No dissent on P2.

### R08. Warn on unknown config fields — MODIFIED (P2 -> withdrawn)

**Original**: P2, interim warning until R01 is implemented.
**Modification**: Withdrawn. R01 is purely additive with defaults matching current behavior. If R01 ships promptly, the interim warning is unnecessary overhead. The arbitration-auditor originally rated a similar recommendation P3 (their R10) and has also withdrawn it. The guided-workflow-auditor favors direct implementation over interim measures. If R01 is delayed, this can be revisited, but it should not be tracked as a separate work item that competes for implementation attention.

### R09. Document engine integration notes for guided workflow commands — MODIFIED (P3, expanded)

**Original**: P3, documenting that guided workflow commands are SKILL.md-native.
**Modification**: Expanded scope per the guided-workflow-auditor's R9. The documentation should cover not just "what the engine does NOT do" but also the dual-execution-path architecture: SKILL.md handlers and the Python engine are parallel implementations of the same pipeline, changes must be made in both places (or a convergence path must be chosen). The guided-workflow-auditor's framing is more complete and actionable.

### R10. Validate `PRIOR_ARBITRATION_SECTION` template references against engine population — SURVIVING (P3)

**Status**: Unchanged. No cross-reviewer contested this test recommendation. It provides regression protection for R04.

---

## New Recommendations

### N1. Correct STATUS.md to reflect schemas implementation status (P2)

**Triggered by**: schema-integration-auditor cross-review DC-1.

This review stated the schemas package "does not exist on disk yet" based on STATUS.md. The schema-integration-auditor demonstrates the package IS implemented with working tests. STATUS.md is out of date, and this review's Missed Opportunity #4 was based on an incorrect premise. STATUS.md should be corrected, and this review's schema-related observations should be revisited against the actual implementation.

### N2. Verify `arbiter/` vs `arbitration/` ground truth (P1 -- blocking verification)

**Triggered by**: arbitration-auditor's cross-review DC-1 and guided-workflow-auditor's N1.

The arbitration-auditor claims output paths "match spec 006 US-4." This review claims they do not match SKILL.md. Both claims cannot be simultaneously correct unless spec 006 and SKILL.md use different directory names. Ground truth verification requires checking three sources:
1. `engine/output.py` -- the actual directory name constant
2. SKILL.md -- the documented output path convention
3. Spec 006 -- the user story output path references

If all three agree on `arbitration/` and the engine uses `arbiter/`, R03 stands at P1. If spec 006 says `arbiter/` and SKILL.md says `arbitration/`, there is a spec-vs-SKILL.md discrepancy that needs its own resolution.

---

## Position Summary

The spec-compliance-auditor's central position -- that the engine is a faithful extraction of pre-spec-006 SKILL.md with concrete gaps in the post-merge additions -- is validated by the cross-review process. The most significant adjustment is accepting the dual-execution-path architecture identified by the guided-workflow-auditor. The original review treated the engine as the sole execution path, which led to over-classification of some gaps as P1 "runtime failures" when the affected code paths are only exercised by engine-direct callers, not by guided workflow handlers.

The `PRIOR_ROUND_SECTION` downgrade (P1 to P2) reflects acceptance that this is a pre-existing gap with partial mitigation through individual path variables. The `arbiter/` vs `arbitration/` naming remains P1 pending verification -- this is the most contentious finding in the deliberation, with two auditors making contradictory claims about the codebase. The interim warning recommendation (R08) is withdrawn in favor of direct implementation (R01), accepting the consensus that additive field addition is safer and faster than warning-then-implement.

The most embarrassing finding is the STATUS.md reliance: this review stated schemas "do not exist on disk yet" without checking the filesystem. The schema-integration-auditor's correction is accepted. STATUS.md maintenance should be tracked as a separate concern to prevent future audits from repeating this error.
