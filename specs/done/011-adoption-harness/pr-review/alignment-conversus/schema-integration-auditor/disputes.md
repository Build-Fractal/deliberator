# Schema Integration Auditor — Disputes

**Agent**: schema-integration-auditor
**Phase**: 4 (Disputes after revision)
**Date**: 2026-03-24

---

## Remaining Disputes

### D1. MODE registry unification — P3 vs permanent deferral

**With**: No specific auditor (position reconciliation)
**Nature**: Priority acceptance with process concern

This review accepted the P3 downgrade for `VALID_MODES` unification (R2). The dispute is not about the priority but about the tracking mechanism. P3 items risk being permanently deferred. The mode duplication is a maintenance invariant that becomes more dangerous as the mode set grows (spec 019 config optimizer may introduce new modes). If P3 items have no tracking mechanism, the unification will never happen and the risk will materialize silently.

**Recommended resolution**: Include in the synthesis as P3 with a trigger condition: "escalate to P2 when a new mode is added to either package." This converts a static priority into a conditional that activates when the risk becomes non-theoretical.

### D2. STATUS.md accuracy — systemic concern

**With**: spec-compliance-auditor
**Nature**: Process concern, not technical dispute

The spec-compliance-auditor accepted the STATUS.md error (their N1) and called it "the most embarrassing finding." But the underlying issue is systemic: STATUS.md is a manually maintained file that can silently diverge from reality. The spec-compliance-auditor's methodology (checking STATUS.md rather than the filesystem) is reasonable -- status files exist to save auditors from inspecting every directory. The fix is not just updating STATUS.md once but establishing a process for keeping it current.

**Recommended resolution**: Include STATUS.md accuracy as a systemic finding in the synthesis. The immediate fix is updating specs 012/013 status. The systemic fix is either automated status tracking or a convention that STATUS.md is verified against the filesystem at the start of any audit.

### D3. Schema integration path accounting for dual execution — architectural concern

**With**: guided-workflow-auditor
**Nature**: Future architecture disagreement

The guided-workflow-auditor's dual-execution-path finding (N2 in this review) has implications for schema integration that no other auditor addresses. If SKILL.md handlers are the primary execution path for guided workflow, then spec 014+ schema integration cannot simply bridge schemas to the engine Python API. It must also expose game form context through SKILL.md-accessible channels (MCP tools, file-based lookups). The guided-workflow-auditor's MCP tool recommendations (R4-R6) address delegation broadly, but none specifically address schema-to-SKILL.md bridging. This review's `conversus_validate_schema` MCP tool (R7, P3) is the closest, but it validates schemas rather than exposing game form context to agents.

**Recommended resolution**: The synthesis should note that spec 014 planning must account for both execution paths when designing the schema-to-execution bridge. No immediate action required, but the architectural constraint should be documented.

---

## Convergence

### C1. `timing`/`influence` on `ArbiterConfig` — unanimous P1

Strongest convergence point. Four of four auditors, unchanged through revision.

### C2. Engine-schema isolation is correct and should be maintained — unanimous

All four auditors agree `engine/` and `conversus/schemas/` should have zero import dependencies. The schema-integration-auditor's original finding is universally accepted.

### C3. `VALID_MODES` values are currently correct — unanimous

All auditors who examined mode values confirm the four modes are identical across engine and schemas. The dispute was never about current correctness but about future drift risk. The values are aligned today.

### C4. `arbiter/` vs `arbitration/` requires verification — 3 of 4

Three auditors created ground-truth verification recommendations. The directory naming issue is the most significant factual disagreement in the deliberation.

### C5. STATUS.md must be updated for specs 012/013 — 2 of 4 explicit

The spec-compliance-auditor (N1) and this review (N1) explicitly recommend STATUS.md correction. The arbitration-auditor and guided-workflow-auditor do not address it (outside their scope). No disagreement exists -- just scope differences.

---

## Final Position Statement

### Non-Negotiables

1. **Schema-engine isolation must be preserved.** No changes to `engine/` should introduce imports from `conversus/schemas/`. The bridge, when built (spec 014+), must use a separate integration layer.
2. **STATUS.md must reflect reality.** Auditors who trust STATUS.md (as the spec-compliance-auditor reasonably did) will reach incorrect conclusions if it is stale.
3. **`VALID_MODES` unification must have a trigger condition.** P3 is acceptable today. Permanent deferral is not. The trigger is "when a new mode is added."

### Flexibility

1. **All P1 and P2 engine items** (timing/influence fields, INFLUENCE_LEVEL passing, PRIOR_ARBITRATION_SECTION, inter-round arbitration): fully defer to the arbitration-auditor and spec-compliance-auditor's expertise. No schema-specific concerns with any of these recommendations.
2. **`game_form` on `EngineConfig`** (R5, now P3): willing to defer entirely to spec 014 timeline.
3. **`conversus_validate_schema` MCP tool** (R7, P3): willing to defer to after delegation MCP tools (guided-workflow-auditor's R4-R6) are established.
4. **Import path fix** (R6, P2): low-effort documentation fix that can be included in any spec 013 PR.
5. **011a decomposition**: fully deferred, accepted as out-of-scope for alignment review.
