# Arbitration Auditor — Disputes

**Agent**: arbitration-auditor
**Phase**: 4 (Disputes after revision)
**Date**: 2026-03-24

---

## Remaining Disputes

### D1. Atomicity of R1 + R2 — ship together or ship separately?

**With**: spec-compliance-auditor, guided-workflow-auditor
**Nature**: Implementation sequencing disagreement

All four auditors now agree R1 (fields) is P1 and R2 (inter-round behavior) is P2. The dispute is about the gap between them. This review's revision states R1 and R2 should ship together because a parsed `timing: inter-round` with no behavioral effect is worse than silent ignore -- it gives users a false sense their config is honored. The spec-compliance-auditor's revision agrees ("should ship atomically with or immediately after R01") but does not make this a hard constraint. The guided-workflow-auditor is flexible on separate PRs with a tracking ticket.

The risk: if R1 ships without R2, users will write `timing: inter-round` configs, see no validation error, and assume inter-round arbitration is active. The engine will silently behave as `timing: final`. This is a correctness trap.

**Recommended resolution**: Ship R1 + R2 atomically in one PR. If that is infeasible, ship R1 with a code-level assertion or warning: `if config.arbiter.timing == "inter-round": logger.warning("Inter-round arbitration not yet implemented; behaving as final")`.

### D2. Phase 6-only entry point priority — P2 vs not addressed

**With**: spec-compliance-auditor, schema-integration-auditor
**Nature**: Omission dispute

The guided-workflow-auditor rates the Phase 6-only entry point as P2 (their R3, downgraded from P1). This review's N2 acknowledges it as "complementary" to R2. The spec-compliance-auditor does not include a Phase 6-only entry point in any recommendation. The schema-integration-auditor does not mention it. Only two of four auditors (guided-workflow-auditor and this review) consider it. Yet this is the key to resolving the dual-execution-path architecture: without a Phase 6-only entry point, the `/conversus arbitrate` handler cannot delegate to the engine and must remain a parallel implementation.

**Recommended resolution**: Include the Phase 6-only entry point as P2 in the synthesis. It is the bridge between the engine and the guided workflow for arbitration specifically.

### D3. Cross-round synthesis arbitration context — P2 vs omitted

**With**: guided-workflow-auditor, spec-compliance-auditor
**Nature**: Scope disagreement

This review's R6 (pass `arbitration_paths` and `arbitration_rulings` to `build_cross_round_synthesis_context`) is P2. The guided-workflow-auditor does not mention it. The spec-compliance-auditor does not mention it. The schema-integration-auditor does not mention it. This is an engine-internal gap that only surfaces when multi-round deliberation with inter-round arbitration produces a cross-round synthesis. It is a real gap: the function signature already has the parameters, the caller just does not pass them.

**Recommended resolution**: Include as P2 in the synthesis, grouped with the inter-round arbitration family. It is low-hanging fruit (the plumbing exists, only the wiring is missing).

---

## Convergence

### C1. `timing`/`influence` on `ArbiterConfig` — unanimous P1

The strongest convergence point. Four of four auditors. No disagreement on fields, defaults, validation rules, or code location.

### C2. `INFLUENCE_LEVEL` explicit passing — unanimous P1

Four of four auditors agree the Pydantic default is insufficient. Identical mechanism identified.

### C3. `PRIOR_ARBITRATION_SECTION` population — 3 of 4 P1

The arbitration-auditor (R4), spec-compliance-auditor (R04), and guided-workflow-auditor (R8 upgraded) agree on P1. The guided-workflow-auditor's upgrade from P3 to P1 was the most significant position change in the revision phase.

### C4. Inter-round arbitration is P2 — unanimous

The sequencing argument resolved the P1/P2 split. R1 must ship before R2 has meaning.

### C5. `arbiter/` vs `arbitration/` requires ground truth verification — 3 of 4

The arbitration-auditor (N1), guided-workflow-auditor (N1), and spec-compliance-auditor (N2) all created new recommendations for ground truth verification. Only the schema-integration-auditor did not address this, as it is outside their scope. This is a new convergence point that emerged from the cross-review process.

---

## Final Position Statement

### Non-Negotiables

1. **R1 (`timing`/`influence` fields) is the gate for all other arbitration work.** Nothing else in the spec 006 family can proceed without it.
2. **R3 (`INFLUENCE_LEVEL` passing) and R4 (`PRIOR_ARBITRATION_SECTION` population) must ship with or immediately after R1.** These are the template-level manifestations of the config fields. Fields without template population are useless.
3. **R2 (inter-round arbitration) must not be deferred indefinitely.** The P2 downgrade was a sequencing concession, not a priority concession. If R1 ships without a committed timeline for R2, the engine will have fields with no behavior -- a silent correctness trap.
4. **Cross-round synthesis must receive arbitration context** (R6). The plumbing exists. Only the wiring is missing. This is the lowest-effort, highest-impact fix after R1/R3/R4.

### Flexibility

1. **R2 implementation approach**: Willing to accept Phase 6 running either inside `_run_single_round` or in the round loop outside it, as long as it fires after Phase 5 and before the termination check.
2. **R7 (`PipelineResult` type change)**: Willing to defer to after R2 ships, since the type only matters when per-round arbitration tracking is needed.
3. **R8/R9 (tests and heading validation)**: P3, can be prioritized by the implementation team.
4. **MCP tools**: No objection to the guided-workflow-auditor's dispute-parsing API as P2. Arbitration correctness does not depend on MCP tools, but the delegation architecture benefits from them.
