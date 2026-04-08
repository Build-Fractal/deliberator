# Cross-Review: Arbitration Auditor reviewing Guided Workflow Auditor

**Reviewer perspective**: arbitration-auditor
**Reviewed**: guided-workflow-auditor
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1. Engine as THE execution path vs parallel implementation

The arbitration-auditor treats the engine as the authoritative execution path for all deliberation phases. The guided-workflow-auditor reveals that SKILL.md handlers are a parallel implementation: `/conversus converge` orchestrates phases via Agent tool calls, NOT via `run_pipeline()`. This is a foundational disagreement. The arbitration-auditor's entire R2 (inter-round arbitration in `run_pipeline()`) would not benefit `/conversus arbitrate` or `/conversus converge` because those handlers never call `run_pipeline()`. The arbitration-auditor's recommendations are valid for the engine in isolation but miss the architectural reality.

### DC-2. Phase 6-only entry point -- framed as new need vs missing seam

The arbitration-auditor does not identify a Phase 6-only entry point as a gap. The review focuses on inter-round arbitration within `run_pipeline()` (Phase 6 firing inside the round loop). The guided-workflow-auditor explicitly calls out the need for a Phase 6-only execution path (R3, P1) because the `/conversus arbitrate` handler needs to run ONLY Phase 6 on existing output. The arbitration-auditor's recommendation to add Phase 6 inside the loop is correct for `timing: inter-round`, but the separate need for standalone Phase 6 invocation (for the `arbitrate` command) is missed.

### DC-3. Priority of `PRIOR_ARBITRATION_SECTION` construction

The arbitration-auditor rates `PRIOR_ARBITRATION_SECTION` as P1 (R4), essential for spec 006 compliance. The guided-workflow-auditor rates the same issue as P3 (R8), framing it as a consistency improvement. From the arbitration-auditor's perspective, this is dangerous: if the engine runs inter-round arbitration but does not inject the prior arbitration context into round 2+ reviews, agents will make decisions without awareness of prior rulings. The guided-workflow-auditor's lower priority reflects the assumption that SKILL.md handlers compose this block themselves, but that assumption only holds if the handlers NEVER use the engine.

---

## Tensions

### T-1. Scope of arbitration coverage

The arbitration-auditor's review is exhaustively focused on spec 006: every FR is checked, every template variable is traced, every influence level is analyzed. The guided-workflow-auditor's review spans specs 007-011 with arbitration as one concern among many. This means the arbitration-auditor finds granular issues (e.g., `arbitration_rulings` not passed to cross-round synthesis, `PipelineResult.arbitration_ran` type) that the guided-workflow-auditor does not mention.

### T-2. Influence-aware stagnation detection

The arbitration-auditor dedicates R5 (P2) to influence-aware dispute counting for stagnation detection, with detailed per-influence-level semantics (binding subtracts, advisory does not). The guided-workflow-auditor mentions influence-aware dispute counting (R2 discussion of SKILL.md lines 534-538) but does not separate it as a distinct recommendation. The tension: the arbitration-auditor sees this as a discrete, testable requirement; the guided-workflow-auditor sees it as part of the broader inter-round arbitration implementation.

### T-3. MCP tool expansion direction

The guided-workflow-auditor recommends `conversus_gate`, `conversus_cost`, and public dispute-parsing APIs (R4-R6, P2). The arbitration-auditor does not recommend any MCP tool changes. From the arbitration perspective, MCP tools are outside spec 006's scope. The tension: the guided-workflow-auditor sees MCP tools as the delegation bridge between SKILL.md handlers and the engine, while the arbitration-auditor sees the engine as a self-contained Python pipeline with no need for MCP-mediated invocation.

### T-4. Dual-execution-path documentation

The guided-workflow-auditor recommends documenting the dual-execution-path architecture (R9, P3). The arbitration-auditor does not mention this concern. From the arbitration perspective, the engine IS the pipeline, and documenting a parallel SKILL.md execution path could be seen as endorsing an undesirable divergence rather than driving convergence.

### T-5. Cost estimation duplication

The guided-workflow-auditor flags cost estimation duplication (Missed Opportunity #4) between SKILL.md and `engine.cost.estimate_cost()`. The arbitration-auditor does not discuss cost estimation. This reflects their different scopes: the guided-workflow-auditor cares about the full UX surface, while the arbitration-auditor cares only about arbitration correctness.

---

## Safe Agreements

### SA-1. `timing` and `influence` fields must be added to `ArbiterConfig`

Both auditors rate this as the top-priority P1 fix. Both specify the same field definitions, defaults, and code location.

### SA-2. Engine's existing Phase 6 logic is structurally sound

Both auditors agree the trigger evaluation, `PRIOR_ARBITRATION_PATH` threading, failure handling, and output layout are correct. The gaps are additive.

### SA-3. `INFLUENCE_LEVEL` must be explicitly passed from config

Both auditors agree the Pydantic default masks the fact that the engine ignores the influence setting. Both cite `build_arbitration_context()` as the fix point.
