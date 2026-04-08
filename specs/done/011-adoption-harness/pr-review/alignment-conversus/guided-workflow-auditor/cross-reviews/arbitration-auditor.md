# Cross-Review: Guided Workflow Auditor reviewing Arbitration Auditor

**Reviewer perspective**: guided-workflow-auditor
**Reviewed**: arbitration-auditor
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1. Severity of `timing`/`influence` gap: blocking vs additive

The arbitration-auditor calls the missing `timing`/`influence` fields a P1 "must-fix: blocks spec 006 correctness." The guided-workflow-auditor also flags this as P1 but frames it differently -- as blocking correct *guided workflow execution*, not spec 006 correctness per se. The danger: the arbitration-auditor's framing implies the engine is broken today for any arbitration config, while the guided-workflow-auditor recognizes that the defaults (`final`/`binding`) mean the engine works correctly for the default case. The arbitration-auditor's R1 recommendation is the same fix, but the justification overstates urgency for users who have not written `timing: inter-round` configs.

### DC-2. Inter-round arbitration insertion point

The arbitration-auditor recommends adding inter-round arbitration "after `_run_single_round` returns and before the stagnation/termination check" (R2), calling `_run_single_round` "the right extraction boundary." The guided-workflow-auditor's R2 says to add it "inside the round loop, after each round's Phase 5 synthesis AND before the termination check." These are subtly different: the arbitration-auditor wants Phase 6 *outside* `_run_single_round` but inside the loop, while the guided-workflow-auditor's SKILL.md citation (lines 519-540) implies it fires within the round's execution. If Phase 6 runs outside `_run_single_round`, the round-level output directory may already be finalized.

### DC-3. Scope of review vs scope of impact

The arbitration-auditor's review is tightly scoped to spec 006 and does not address the dual-execution-path problem (SKILL.md handlers vs Python engine). The guided-workflow-auditor identifies this as a fundamental architectural concern (Off-Base Assumption #1). The arbitration-auditor's recommendations assume the engine is THE execution path, while the guided-workflow-auditor documents that SKILL.md handlers bypass the engine entirely. Implementing the arbitration-auditor's R2 (inter-round arbitration in `run_pipeline`) would not benefit the SKILL.md `arbitrate` handler, which runs Phase 6 inline.

---

## Tensions

### T-1. Priority of `PRIOR_ARBITRATION_SECTION` assembly

Both auditors flag this gap. The arbitration-auditor gives it P1 status (R4), while the guided-workflow-auditor bundles it under P3 (R8) as a "correctness and consistency improvement." The arbitration-auditor's higher priority reflects that spec 006 FR-014 explicitly requires this. The guided-workflow-auditor's lower priority reflects that the guided workflow handlers do not use the Python engine's context builders.

### T-2. Cross-round synthesis arbitration context

The arbitration-auditor flags that `build_cross_round_synthesis_context` is called without `arbitration_paths` or `arbitration_rulings` (R6, P2). The guided-workflow-auditor does not mention this gap at all. From the guided-workflow perspective, cross-round synthesis is part of the engine's internal pipeline that the SKILL.md handlers do not use directly. The tension is whether engine-internal completeness matters when the guided workflow bypasses the engine.

### T-3. `PipelineResult.arbitration_ran` type

The arbitration-auditor recommends changing this from `bool` to a richer type (R7, P2) to support per-round arbitration tracking. The guided-workflow-auditor does not address `PipelineResult` at all. From the guided-workflow perspective, the result type matters only if the guided handlers consume it -- which they currently do not (they parse output files directly).

---

## Safe Agreements

### SA-1. `timing` and `influence` must be added to `ArbiterConfig`

Both auditors agree this is the highest-priority fix. Both recommend adding the fields with defaults matching current behavior (`final`/`binding`). Both cite the same code location (`engine/config.py`, lines 45-55).

### SA-2. `INFLUENCE_LEVEL` must be passed in `build_arbitration_context`

Both auditors agree the engine must pass `INFLUENCE_LEVEL` from config rather than relying on the Pydantic default. The arbitration-auditor's R3 and the guided-workflow-auditor's R1 reference both identify this as the mechanism by which influence reaches templates.

### SA-3. Engine's existing arbitration plumbing is structurally sound

Both auditors agree the engine's Phase 6 trigger logic, `PRIOR_ARBITRATION_PATH` threading, failure handling, and output directory layout are correct. The gaps are additive (missing fields, missing inter-round insertion point), not structural.
