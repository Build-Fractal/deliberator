# Arbitration Auditor — Revision

**Agent**: arbitration-auditor
**Phase**: 3 (Revision after cross-review)
**Date**: 2026-03-24

---

## Recommendation Dispositions

### R1. Add `timing` and `influence` fields to `ArbiterConfig` — SURVIVING (P1)

**Status**: Unchanged. Universal agreement across all four auditors. This is the single highest-priority recommendation in the entire deliberation. No dissent.

### R2. Implement inter-round arbitration in `run_pipeline()` — MODIFIED (P1 -> P2)

**Original**: P1, "must-fix: blocks spec 006 correctness."
**Modification**: Downgraded to P2. The spec-compliance-auditor's cross-review makes the sequencing argument clearly: inter-round arbitration is a feature addition that depends on R1 (the fields must exist before the behavior). The guided-workflow-auditor's cross-review adds that the guided handlers bypass `run_pipeline()` entirely, so this fix only benefits engine-direct callers (MCP tools, SDK). While spec 006 defines inter-round arbitration as a core requirement, the implementation is sequentially dependent on R1. P2 is the correct classification for implementation ordering, with the understanding that R1 without R2 creates a "parsed but inert" field -- which is worse than silent ignore only in the sense that it is more explicit. The spec-compliance-auditor's interim warning recommendation (their R08) would bridge this gap.

The insertion point discussion is resolved: Phase 6 fires after `_run_single_round` returns, inside the round loop, before the stagnation/termination check. This keeps `_run_single_round` focused on Phases 1-5 and the round loop responsible for Phase 6 dispatch.

### R3. Pass `INFLUENCE_LEVEL` from config in `build_arbitration_context` — SURVIVING (P1)

**Status**: Unchanged. All four auditors agree. The spec-compliance-auditor and guided-workflow-auditor both cite the same mechanism (read from `config.arbiter.influence`, map to `InfluenceLevel` enum). No dissent.

### R4. Construct `PRIOR_ARBITRATION_SECTION` in `build_review_context` — SURVIVING (P1)

**Status**: Upgraded in cross-review consensus. Originally P1 in this review. The guided-workflow-auditor originally rated it P3 but has now accepted P1 after the cross-review argument that engine context builders must be correct for convergence. The spec-compliance-auditor independently rated it P1. Three of four auditors now agree on P1.

### R5. Implement influence-aware dispute counting for stagnation detection — SURVIVING (P2)

**Status**: Unchanged. The spec-compliance-auditor's R07 mirrors this recommendation. The guided-workflow-auditor subsumes it under R2 rather than treating it separately. Retaining as a discrete P2 item because the implementation is a distinct code change (new helper function to parse arbitration output and count addressed disputes) that can be tested independently.

### R6. Pass `arbitration_paths` and `arbitration_rulings` to cross-round synthesis — SURVIVING (P2)

**Status**: Unchanged. The guided-workflow-auditor's cross-review notes this is engine-internal and not relevant to guided handlers. Accepted: this is engine-completeness, not guided-workflow-critical. But it is still P2 because cross-round synthesis without arbitration context produces incomplete output.

### R7. Change `PipelineResult.arbitration_ran` from `bool` to richer type — SURVIVING (P2)

**Status**: Unchanged. The spec-compliance-auditor's cross-review notes this is an internal API concern. Accepted: it does not affect SKILL.md-specified behavior. But it blocks correct reporting of per-round arbitration when inter-round arbitration is implemented (R2). Retaining P2 as a dependency of R2.

### R8. Add integration test for `timing: inter-round` + `influence: advisory` — SURVIVING (P3)

**Status**: Unchanged. The schema-integration-auditor's cross-review notes their R8 (mode-set assertion test) targets a different concern. Both tests should exist, but the behavioral integration test has higher value for catching regressions in the complex arbitration path.

### R9. Add validation for influence-adjusted arbitration output headings — SURVIVING (P3)

**Status**: Unchanged. The guided-workflow-auditor's R10 mirrors this. No dissent. Low priority but valid parity improvement.

### R10. Log warning when `timing`/`influence` are present but unimplemented — MODIFIED (P3 -> withdrawn in favor of R1)

**Original**: P3, interim measure until R1 is implemented.
**Modification**: Withdrawn. R1 (adding the fields) should be the immediate action. The spec-compliance-auditor recommends a P2 warning as an interim step, but given that R1 is purely additive (defaults match current behavior), the warning is unnecessary if R1 ships promptly. If R1 is delayed, the spec-compliance-auditor's interim warning (their R08) can be adopted. This review defers to the implementation team's shipping timeline.

---

## New Recommendations

### N1. Verify `arbiter/` vs `arbitration/` directory naming (P1 -- verification)

**Triggered by**: spec-compliance-auditor R03 and guided-workflow-auditor cross-review DC-1.

This review stated "Output directory layout matches spec 006 US-4" based on checking `OutputManager.get_arbitration_path()` and spec 006 user stories. The spec-compliance-auditor claims the engine uses `arbiter/` while SKILL.md uses `arbitration/`. If the spec-compliance-auditor is correct, this review's "matches" claim is wrong. The ground truth must be verified by inspecting `engine/output.py` for the actual directory name constant and comparing against both SKILL.md text and spec 006 text. If there is a mismatch, it is P1 for any consumer of engine output.

### N2. Acknowledge dual-execution-path architecture in arbitration recommendations (position adjustment)

**Triggered by**: guided-workflow-auditor's cross-review DC-1 and DC-3.

The guided-workflow-auditor correctly identifies that this review's recommendations assume the engine is THE execution path. The `/conversus arbitrate` handler runs Phase 6 inline via SKILL.md instructions, not via `run_pipeline()`. This means R2 (inter-round arbitration in `run_pipeline()`) benefits engine-direct callers but not the guided `arbitrate` command. The guided-workflow-auditor's R3 (Phase 6-only entry point) addresses the delegation seam that would let the guided handler use the engine. These are complementary: R2 makes the engine correct, R3 makes the engine accessible to guided handlers. Both are needed for full spec 006 compliance across execution paths.

---

## Position Summary

The arbitration-auditor's core position -- that spec 006 compliance requires `timing`, `influence`, `INFLUENCE_LEVEL`, and `PRIOR_ARBITRATION_SECTION` in the engine -- is fully validated by the cross-review process. All four auditors agree on R1 (add fields) and R3 (pass `INFLUENCE_LEVEL`). Three of four now agree on R4 (`PRIOR_ARBITRATION_SECTION` at P1), with the guided-workflow-auditor upgrading from P3 to P1.

The primary concession is downgrading R2 (inter-round arbitration) from P1 to P2. The spec-compliance-auditor's sequencing argument is sound: the fields must exist before the behavior. The guided-workflow-auditor's dual-execution-path finding adds weight: implementing inter-round arbitration in `run_pipeline()` alone does not benefit the guided workflow handlers. Full spec 006 compliance requires both engine-side implementation (R2) and a delegation seam (guided-workflow-auditor's R3) so that guided handlers can leverage it.

The `arbiter/` vs `arbitration/` directory naming discrepancy is the most significant new finding from the cross-review process. This review's claim that output paths "match spec 006" may be incorrect. Ground truth verification is required before either this review or the spec-compliance-auditor's claim can be confirmed.
