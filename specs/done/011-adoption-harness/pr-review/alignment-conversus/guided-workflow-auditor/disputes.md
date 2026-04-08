# Guided Workflow Auditor — Disputes

**Agent**: guided-workflow-auditor
**Phase**: 4 (Disputes after revision)
**Date**: 2026-03-24

---

## Remaining Disputes

### D1. `arbiter/` vs `arbitration/` — P1 conditional vs unconditional

**With**: spec-compliance-auditor
**Nature**: Priority disagreement, conditional on ground truth

The spec-compliance-auditor retains P1 "pending verification" for the directory naming fix (their R03). This review created N1 flagging verification as a prerequisite. The dispute is not about whether the mismatch matters -- if confirmed, both agree it affects engine-direct consumers. The dispute is about whether this should be listed as P1 in the actionable recommendations before verification occurs. The spec-compliance-auditor's approach (P1 pending verification) risks allocating implementation resources before the problem is confirmed. This review's approach (verify first, then classify) prevents wasted effort on a potentially non-existent issue.

**Recommended resolution**: Verify ground truth. If mismatch confirmed, P1 for engine consumers only (not for guided workflow handlers). If no mismatch, remove from recommendations entirely.

### D2. `PRIOR_ROUND_SECTION` — P2 vs omitted

**With**: spec-compliance-auditor
**Nature**: Scope disagreement

The spec-compliance-auditor downgraded `PRIOR_ROUND_SECTION` from P1 to P2 in revision (their R05). This review does not include `PRIOR_ROUND_SECTION` in any recommendation because it is a pre-existing gap (spec 004 era) that was not introduced by the spec 006-013 merge. Including it in a post-merge alignment review conflates pre-existing tech debt with new regressions. The spec-compliance-auditor's inclusion at P2 is defensible if the scope of the alignment review includes all engine-vs-SKILL.md gaps, not just post-merge ones.

**Recommended resolution**: Separate pre-existing gaps from post-merge gaps in the final synthesis. `PRIOR_ROUND_SECTION` belongs in a "pre-existing tech debt" section, not in the "spec 006-013 alignment" section.

### D3. MCP tool expansion — delegation-first vs no-MCP-yet

**With**: arbitration-auditor (and partially schema-integration-auditor)
**Nature**: Architectural disagreement

The arbitration-auditor's revision does not include any MCP tool recommendations. The schema-integration-auditor deferred their MCP tool (R7) to P3. This review maintains R4 (dispute parsing API), R5 (`conversus_gate`), and R6 (`conversus_cost`) at P2 as the primary mechanism for resolving the dual-execution-path architecture. Without MCP tools as the delegation bridge, the guided workflow handlers will continue to be a parallel implementation that must be maintained independently.

The dispute is architectural: should the engine expose capabilities via MCP tools for SKILL.md handler consumption, or should the guided handlers remain independent of the engine? This review's position is that MCP-mediated delegation is the convergence path; the arbitration-auditor's silence on MCP tools implies acceptance of permanent divergence.

**Recommended resolution**: The synthesis should recommend at least one MCP tool (dispute parsing, the most broadly needed) as P2 to establish the delegation pattern, with additional tools as P3.

---

## Convergence

### C1. `timing` and `influence` fields are the anchor P1 — unanimous

All four revisions agree. No auditor contested this. R1 across all reviews. This is the strongest convergence point in the deliberation.

### C2. `INFLUENCE_LEVEL` must be explicitly passed — unanimous

All four revisions agree on mechanism (read from config, map to enum, pass to `ArbitrationContext`). No dissent.

### C3. `PRIOR_ARBITRATION_SECTION` is P1 — 3 of 4

The arbitration-auditor (R4), spec-compliance-auditor (R04), and this review (R8, upgraded from P3) agree on P1. The schema-integration-auditor did not rate this item. Strong convergence.

### C4. Inter-round arbitration is P2 — unanimous

All four revisions now agree on P2 for inter-round arbitration implementation in `run_pipeline()`. The arbitration-auditor downgraded from P1; this review downgraded from P1; the spec-compliance-auditor retained P2; the schema-integration-auditor deferred to engine-focused auditors. The sequencing argument (R1 must ship first) resolved the dispute.

### C5. `VALID_MODES` unification is P3 — 3 of 4

This review (R7), the arbitration-auditor (implicit via cross-review), and the spec-compliance-auditor (implicit via non-inclusion) agree P3. The schema-integration-auditor downgraded from P1 to P3 in revision. Strong convergence after significant initial disagreement.

---

## Final Position Statement

### Non-Negotiables

1. **`timing`/`influence` fields on `ArbiterConfig`** (R1) must ship before any other recommendation. It is the dependency for R2, R5, R8, and the inter-round arbitration family.
2. **`PRIOR_ARBITRATION_SECTION` population** (R8, upgraded to P1) must be correct in engine context builders. Without this, inter-round arbitration produces agents that are blind to prior rulings.
3. **The dual-execution-path architecture is real** and must be documented. Engine improvements only benefit engine-direct callers unless MCP delegation tools are built.
4. **Ground truth verification of `arbiter/` vs `arbitration/`** before any rename work is scheduled.

### Flexibility

1. **MCP tool scope**: Willing to accept a single P2 MCP tool (dispute parsing) rather than three, if that establishes the delegation pattern for future tools.
2. **Inter-round arbitration timing**: Willing to accept R2 shipping in a separate PR from R1, as long as R1 does not ship without at least an interim warning (spec-compliance-auditor's approach) or a tracking ticket for R2.
3. **`PRIOR_ROUND_SECTION`**: Willing to accept this as out-of-scope for the post-merge alignment, tracked separately as pre-existing tech debt.
4. **`game_form` on `EngineConfig`**: Willing to defer entirely to spec 014 timeline. No objection to P3 or deferred.
