# Guided Workflow Auditor — Revision

**Agent**: guided-workflow-auditor
**Phase**: 3 (Revision after cross-review)
**Date**: 2026-03-24

---

## Recommendation Dispositions

### R1. Add `timing` and `influence` fields to `ArbiterConfig` and `EngineConfig` — SURVIVING (P1)

**Status**: Unchanged. All three cross-reviewers agree this is the top-priority gap. The arbitration-auditor's exhaustive spec 006 traceability strengthens the case. The schema-integration-auditor confirms the change is safe (Pydantic additive, defaults match current behavior). No dissent from any reviewer.

### R2. Add inter-round arbitration to `run_pipeline()` — MODIFIED (P1 -> P2)

**Original**: P1, framed as blocking correct guided workflow execution.
**Modification**: Downgraded to P2. The arbitration-auditor rates this P1, the spec-compliance-auditor rates it P2. Upon reflection, the spec-compliance-auditor's reasoning is more precise: inter-round arbitration is a feature addition for a config value (`timing: inter-round`) that no user can currently set (because R1 has not shipped). The fields (R1) must exist before the behavior matters. However, the arbitration-auditor is correct that once R1 ships, a parsed `timing: inter-round` with no behavioral effect is worse than the current silent drop. Resolution: R1 and R2 should ship together, but R2 is sequentially dependent on R1, making it P2 in implementation order.

Additionally, the cross-reviews surfaced that the arbitration-auditor and this review disagree on the insertion point. The arbitration-auditor wants Phase 6 outside `_run_single_round` but inside the round loop; this review cited SKILL.md lines 519-540 implying it fires within the round's execution. The arbitration-auditor's approach is architecturally cleaner: `_run_single_round` handles Phases 1-5, the round loop handles Phase 6 conditionally. Accepting the arbitration-auditor's insertion point.

### R3. Expose a Phase 6-only execution entry point — SURVIVING (P1 -> P2)

**Original**: P1, framed as critical for `/conversus arbitrate`.
**Modification**: Downgraded to P2. The cross-reviews (particularly from the arbitration-auditor) correctly note that this is a feature addition for the guided workflow delegation seam, not a correctness fix. The `/conversus arbitrate` handler works today by running Phase 6 inline via SKILL.md instructions. The Phase 6-only entry point enables future convergence of the dual execution paths but does not block current functionality. Retaining as the highest P2 item because it is the key to resolving the dual-execution-path architecture.

### R4. Expose dispute-parsing as a public API — SURVIVING (P2)

**Status**: Unchanged. No cross-reviewer contested this. The arbitration-auditor's review reinforces it: `_extract_remaining_disputes` is used internally but not exposed for the `converge`, `arbitrate`, and `gate` handlers.

### R5. Add a `conversus_gate` MCP tool — SURVIVING (P2)

**Status**: Unchanged. The schema-integration-auditor's cross-review notes MCP tool priorities diverge (delegation tools vs schema validation tools), but agrees delegation tools address a more immediate gap. No dissent on the substance.

### R6. Add `conversus_cost` MCP tool — SURVIVING (P2)

**Status**: Unchanged. The spec-compliance-auditor's cross-review notes this as a "genuine gap" they missed. No dissent.

### R7. Align `VALID_MODES` with SKILL.md — MODIFIED (P3, resisting P1 escalation)

**Original**: P3, noting values are currently aligned and suggesting a shared constants module.
**Modification**: Retaining P3. The schema-integration-auditor escalated this to P1 (their R2), calling the dual definition "critical." Three cross-reviews (arbitration-auditor, spec-compliance-auditor, and this review's own cross-review of schema-integration-auditor) challenged the P1 rating. The values are identical, have never drifted, and would be caught by any test. Mode drift is a maintenance concern, not a correctness concern. A shared constants module is good practice but not urgent. P3 is appropriate.

### R8. Add `PRIOR_ARBITRATION_SECTION` template variable support — MODIFIED (P3 -> P1)

**Original**: P3, framed as a consistency improvement.
**Modification**: Upgraded to P1. The arbitration-auditor's cross-review makes a compelling case: if the engine runs inter-round arbitration (after R2) but does not inject prior arbitration context into round 2+ reviews, agents make decisions without awareness of prior rulings. The original P3 rating was based on the assumption that SKILL.md handlers compose this block themselves. However, the arbitration-auditor correctly notes this assumption only holds if the handlers NEVER use the engine. Since the goal is convergence (guided handlers eventually delegating to the engine), the engine's context builders must be correct. Accepting the arbitration-auditor's P1 rating.

### R9. Document the dual-execution-path architecture — SURVIVING (P3)

**Status**: Unchanged. The spec-compliance-auditor's cross-review offers a complementary framing (document what the engine does NOT do). Both perspectives should be included in the documentation. The arbitration-auditor's concern that documenting the parallel path "endorses divergence" is noted but rejected: the divergence exists regardless of documentation, and undocumented divergence is more dangerous.

### R10. Add `influence`-aware heading validation to engine Phase 6 — SURVIVING (P3)

**Status**: Unchanged. No cross-reviewer contested this. Low priority but valid.

---

## New Recommendations

### N1. Verify `arbiter/` vs `arbitration/` directory naming ground truth (P1 -- verification)

**Triggered by**: spec-compliance-auditor R03 (P1) and arbitration-auditor cross-review DC-1.

The spec-compliance-auditor claims the engine uses `arbiter/` while SKILL.md uses `arbitration/`. The arbitration-auditor claims "output directory layout matches spec 006 US-4." These are contradictory claims about the codebase. This review did not independently verify the directory name in `OutputManager`. Before any rename is implemented, the ground truth must be checked: what does `engine/output.py` actually produce, and what does SKILL.md actually specify? If there is a genuine mismatch, it is P1 for engine-only consumers (MCP tools, SDK). It is NOT P1 for guided workflow handlers (which produce their own output).

### N2. Ship R1 + `extra = "forbid"` atomically (sequencing constraint)

**Triggered by**: schema-integration-auditor R3 and arbitration-auditor cross-review DC-2.

The schema-integration-auditor recommends `extra = "forbid"` on `ArbiterConfig`. The arbitration-auditor's cross-review correctly identifies this as sequencing-incompatible with R1 if applied separately. Resolution: if `extra = "forbid"` is adopted, it MUST be applied in the same commit as R1 (adding `timing` and `influence` fields). Otherwise, existing configs with these fields will break. This is a sequencing constraint, not a new recommendation per se, but it must be tracked to prevent a breaking change.

---

## Position Summary

The guided-workflow-auditor's central finding -- that SKILL.md handlers and the Python engine are parallel implementations of the same pipeline -- has been validated by the cross-review process. The spec-compliance-auditor, arbitration-auditor, and schema-integration-auditor all wrote cross-reviews that acknowledged this dual-execution-path architecture as real and architecturally significant. However, the cross-reviews also correctly challenged the implication that engine gaps are therefore lower priority. The arbitration-auditor made the strongest case: if the goal is eventual convergence (guided handlers delegating to the engine), then engine correctness matters even when the guided handlers currently bypass it.

The primary adjustment is to the `PRIOR_ARBITRATION_SECTION` priority (P3 to P1), accepting the arbitration-auditor's argument that engine context builders must be correct for convergence to work. The inter-round arbitration implementation (R2) is downgraded to P2 based on sequencing reality: the fields must exist before the behavior. The Phase 6-only entry point (R3) is also downgraded to P2, acknowledging it enables future convergence rather than fixing current breakage.

The `VALID_MODES` P1 escalation from the schema-integration-auditor is rejected. Three separate cross-reviews challenged it, and the evidence supports P3. The `arbiter/` vs `arbitration/` directory naming requires ground truth verification before any priority can be assigned -- two auditors made contradictory claims about the codebase, and neither provided a file-line citation for the directory name constant.
