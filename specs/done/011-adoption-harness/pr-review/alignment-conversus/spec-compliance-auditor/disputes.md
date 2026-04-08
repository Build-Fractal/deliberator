# Spec Compliance Auditor — Disputes

**Agent**: spec-compliance-auditor
**Phase**: 4 (Disputes after revision)
**Date**: 2026-03-24

---

## Remaining Disputes

### D1. `arbiter/` vs `arbitration/` — impact scope after dual-execution-path acknowledgment

**With**: guided-workflow-auditor
**Nature**: Impact scope disagreement

This review retains P1 for the directory naming fix (R03, pending verification). The guided-workflow-auditor challenges the impact scope: guided handlers produce their own output and do not read engine output, so the mismatch does not affect them. This review accepts that point -- the claim that `/conversus arbitrate` would fail is withdrawn. However, the P1 classification stands for engine-direct consumers: MCP tool users, SDK programmatic callers, and any test that validates output structure against SKILL.md conventions. These are real consumers, not theoretical ones.

The guided-workflow-auditor's position (verify first, then classify) is reasonable but this review's position (classify P1 pending verification) is also reasonable: if the mismatch is confirmed, it should already be tracked at P1 to prevent it from being deprioritized during the verification step.

**Recommended resolution**: Verify ground truth immediately. If confirmed, implement the rename as P1 for engine consumers. The dispute over "P1 pending" vs "verify first" is procedural, not substantive.

### D2. MCP delegation tools — P2 vs unaddressed

**With**: arbitration-auditor
**Nature**: Architectural scope disagreement

The guided-workflow-auditor recommends three MCP delegation tools (R4-R6) at P2. This review did not recommend any MCP tools in the original review or revision. The arbitration-auditor also did not recommend MCP tools. The dispute: should the synthesis include MCP tools as part of the gap-closure plan?

This review's position is that engine correctness must come before engine accessibility. The R01-R04 family (fields, INFLUENCE_LEVEL, PRIOR_ARBITRATION_SECTION) fixes what the engine does. MCP tools fix how the engine is invoked. The former must precede the latter. However, the guided-workflow-auditor's argument that without MCP tools the dual-execution-path divergence is permanent is architecturally sound.

**Recommended resolution**: Include one MCP tool (dispute parsing, the most broadly needed) as P2 in the synthesis, acknowledging it as the first step in the delegation bridge. Defer `conversus_gate` and `conversus_cost` to P3.

### D3. Pre-existing gaps in scope — `PRIOR_ROUND_SECTION` tracking

**With**: guided-workflow-auditor
**Nature**: Scope boundary disagreement

The guided-workflow-auditor argues `PRIOR_ROUND_SECTION` is a pre-existing gap (spec 004 era) and should not be in the post-merge alignment review. This review downgraded it to P2 in revision but retains it in the recommendation list. The rationale: the alignment review's scope is "engine vs SKILL.md post-merge," and SKILL.md post-merge includes the `{PRIOR_ROUND_SECTION}` variable in review templates. The engine's failure to populate it is detectable against the current SKILL.md text, regardless of when the gap was introduced.

**Recommended resolution**: Include `PRIOR_ROUND_SECTION` in the synthesis under a "pre-existing gaps surfaced during alignment" category, distinct from post-merge regression items. This respects the guided-workflow-auditor's scope concern while not losing the finding.

---

## Convergence

### C1. `timing`/`influence` on `ArbiterConfig` — unanimous P1

Four of four auditors. The anchor of the entire deliberation.

### C2. `INFLUENCE_LEVEL` explicit passing — unanimous P1

Four of four auditors. No dispute on mechanism or priority.

### C3. `PRIOR_ARBITRATION_SECTION` — 3 of 4 P1

The arbitration-auditor, this review, and the guided-workflow-auditor (upgraded in revision) agree on P1. Strong convergence.

### C4. Inter-round arbitration — unanimous P2

The sequencing argument resolved the P1/P2 split. All four auditors now agree.

### C5. `arbiter/` vs `arbitration/` requires verification — 3 of 4

Three auditors created verification recommendations. The factual disagreement must be resolved by checking the codebase.

---

## Final Position Statement

### Non-Negotiables

1. **`timing`/`influence` fields** (R01) must be the first implementation item. All other spec 006 work depends on it.
2. **`INFLUENCE_LEVEL` passing** (R02) and **`PRIOR_ARBITRATION_SECTION` population** (R04) must ship with or immediately after R01. These are the template-level manifestations.
3. **`arbiter/` vs `arbitration/` must be verified and resolved.** If the mismatch is confirmed, it is a P1 rename. The engine's output paths must match the authoritative specification.
4. **Engine correctness precedes engine accessibility.** The R01-R04 family must ship before MCP delegation tools are built. Building delegation bridges to an incorrect engine is counterproductive.

### Flexibility

1. **MCP tools**: Willing to accept one P2 MCP tool (dispute parsing) per the guided-workflow-auditor's argument, with others deferred to P3.
2. **`PRIOR_ROUND_SECTION`**: Willing to categorize as "pre-existing gap" rather than "post-merge regression," as long as it is tracked somewhere.
3. **Inter-round arbitration atomicity**: Willing to accept R01 shipping separately from R06 if R06 has a committed timeline and R01 includes a warning when `timing: inter-round` is parsed but not yet implemented.
4. **STATUS.md**: Willing to accept the schema-integration-auditor's N1 as a separate housekeeping task.
5. **`VALID_MODES` unification**: Willing to accept P3 with trigger condition (schema-integration-auditor's proposal).
