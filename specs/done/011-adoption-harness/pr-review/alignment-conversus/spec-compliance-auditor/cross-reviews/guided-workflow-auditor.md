# Cross-Review: Spec Compliance Auditor reviewing Guided Workflow Auditor

**Reviewer perspective**: spec-compliance-auditor
**Reviewed**: guided-workflow-auditor
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1. Engine relevance: authoritative execution path vs parallel implementation

The spec-compliance-auditor treats the engine as the authoritative extraction of SKILL.md's execution model. The guided-workflow-auditor reveals that SKILL.md handlers are a parallel, independent implementation: `/conversus converge` continues executing SKILL.md's Phase 1-5 instructions within the same agent conversation rather than calling `run_pipeline()`. This is a fundamental framing disagreement. The spec-compliance-auditor's P1 items (R01-R05) assume engine correctness is critical for all execution paths. The guided-workflow-auditor's finding that the engine is bypassed by guided handlers means engine bugs only affect `run_engine()` and MCP tool callers, not the guided workflow commands.

### DC-2. `arbiter/` vs `arbitration/` impact scope

The spec-compliance-auditor flags this as P1 (R03), claiming it would cause `/conversus arbitrate` to fail. The guided-workflow-auditor explicitly states the `arbitrate` handler "runs Phase 6 inline" using Agent tool calls. It does not read from the engine's `arbiter/` directory. The P1 claim that `/conversus arbitrate` would "look in the wrong directory" is contradicted by the guided-workflow-auditor's finding that the handler writes its own output independently. The directory naming mismatch affects only consumers of engine-produced output (MCP tools, SDK), not SKILL.md handlers.

### DC-3. `PRIOR_ROUND_SECTION` -- P1 gap vs not mentioned

The spec-compliance-auditor flags `PRIOR_ROUND_SECTION` as P1 (R05). The guided-workflow-auditor does not mention it at all. If the guided workflow handlers compose this block themselves (per SKILL.md instructions), then the engine's empty value is irrelevant for guided execution. The contradiction: the spec-compliance-auditor assumes the engine's context builders are the sole source of template variables, while the guided-workflow-auditor demonstrates that SKILL.md handlers build their own context.

---

## Tensions

### T-1. Priority framework divergence

The spec-compliance-auditor uses "Runtime Failure or Silent Incorrectness" as the P1 criterion. The guided-workflow-auditor uses "blocks correct guided workflow execution." These criteria yield different P1 sets because the guided workflow largely bypasses the engine. The spec-compliance-auditor should consider whether "runtime failure" is the right framing when the primary execution path (guided workflow) does not use the failing code.

### T-2. MCP tools as delegation bridge

The guided-workflow-auditor identifies 3 new MCP tools needed for guided-workflow-to-engine delegation (R4-R6, P2): dispute parsing, gate execution, cost estimation. The spec-compliance-auditor does not recommend any MCP tool additions. The tension: the guided-workflow-auditor sees MCP tools as the solution to the dual-execution-path problem, while the spec-compliance-auditor focuses on fixing the engine's internal correctness without addressing how the guided handlers would leverage those fixes.

### T-3. Phase 6-only entry point

The guided-workflow-auditor identifies the need for standalone Phase 6 invocation (R3, P1) as critical for the `/conversus arbitrate` handler. The spec-compliance-auditor does not flag this -- the review focuses on inter-round arbitration inside `run_pipeline()` (R06, P2). The guided-workflow-auditor's finding that `arbitrate` needs Phase 6-only execution is a unique contribution that the spec-compliance-auditor's SKILL.md-vs-engine comparison did not surface.

### T-4. Documentation of dual-execution-path

The guided-workflow-auditor recommends documenting the parallel implementation architecture (R9, P3). The spec-compliance-auditor recommends documenting that guided workflow commands are "SKILL.md-native" (R09, P3). The guided-workflow-auditor's framing is more complete: it does not just say what the engine does NOT do, it explains that there are two implementations of the same pipeline that must evolve in tandem.

### T-5. Cost estimation duplication

The guided-workflow-auditor flags this as a missed opportunity (M4) and proposes `conversus_cost` MCP tool. The spec-compliance-auditor does not mention cost estimation at all. This is a genuine gap in the spec-compliance review: if SKILL.md's cost formula and `engine.cost.estimate_cost()` diverge, the user sees different estimates depending on execution path.

---

## Safe Agreements

### SA-1. `timing` and `influence` are the top-priority gap

Both auditors agree these fields must be added to `ArbiterConfig` with the same defaults and validation rules.

### SA-2. `INFLUENCE_LEVEL` must be explicitly set from config

Both auditors agree that relying on the Pydantic default masks the gap. Both cite `build_arbitration_context()`.

### SA-3. Inter-round arbitration is missing from `run_pipeline()`

Both auditors agree the engine only runs Phase 6 after the final round. Both agree `timing: inter-round` requires Phase 6 inside the loop.
