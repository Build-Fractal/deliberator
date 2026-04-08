# Cross-Review: Arbitration Auditor reviewing Spec Compliance Auditor

**Reviewer perspective**: arbitration-auditor
**Reviewed**: spec-compliance-auditor
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1. `arbiter/` vs `arbitration/` directory name -- P1 claim vs unmentioned

The spec-compliance-auditor flags the `arbiter/` vs `arbitration/` directory naming as P1 (R03), claiming it causes path mismatches for SKILL.md workflows. The arbitration-auditor does not flag this issue at all. The arbitration-auditor's review explicitly checks `OutputManager` paths and states "Output directory layout matches spec 006 US-4" (What the engine gets right, item 5), noting that `get_arbitration_path(round_base=...)` supports per-round paths. This is a direct contradiction: the spec-compliance-auditor says the paths are wrong, the arbitration-auditor says they match. One auditor checked against SKILL.md text (`arbitration/`), the other checked against spec 006 user stories. The ground truth needs verification.

### DC-2. `PRIOR_ROUND_SECTION` as a P1 issue

The spec-compliance-auditor flags `PRIOR_ROUND_SECTION` always being empty as P1 (R05). The arbitration-auditor does not mention `PRIOR_ROUND_SECTION` at all -- the review focuses exclusively on `PRIOR_ARBITRATION_SECTION`. From the arbitration perspective, `PRIOR_ROUND_SECTION` is a round-awareness concern (spec 004), not an arbitration concern (spec 006). Elevating it to P1 in an alignment review that should be focused on post-merge spec gaps conflates pre-existing round-awareness behavior with newly introduced arbitration gaps.

### DC-3. Number of P1 items: 5 vs 4

The spec-compliance-auditor has 5 P1 recommendations (R01-R05). The arbitration-auditor has 4 P1 recommendations (R1-R4). They overlap on `timing`/`influence` (R01/R1), `INFLUENCE_LEVEL` passing (R02/R3), and `PRIOR_ARBITRATION_SECTION` (R04/R4). The spec-compliance-auditor adds `arbiter/`-vs-`arbitration/` (R03) and `PRIOR_ROUND_SECTION` (R05). The arbitration-auditor adds inter-round arbitration in `run_pipeline()` (R2). The inter-round arbitration gap is arguably more impactful than a directory naming issue, yet the spec-compliance-auditor relegates it to P2 (R06) while keeping the naming issue at P1.

---

## Tensions

### T-1. Inter-round arbitration priority: P1 vs P2

The arbitration-auditor rates implementing inter-round arbitration in `run_pipeline()` as P1 (R2). The spec-compliance-auditor rates it as P2 (R06), noting it is "a significant feature addition." The arbitration-auditor's perspective: without inter-round arbitration, the `timing: inter-round` config value is parsed (after R01) but has no effect, which is worse than the current state where it is silently ignored. The spec-compliance-auditor's perspective: the field must exist before the behavior can be implemented. Both are correct about sequencing, but they disagree on urgency.

### T-2. Influence-aware dispute counting granularity

The arbitration-auditor provides detailed per-influence-level semantics for dispute counting (R5): binding subtracts addressed disputes, recommended subtracts provisionally, advisory does not adjust. The spec-compliance-auditor groups this under R07 with less granularity: "binding subtracts addressed disputes from the count, recommended subtracts provisionally, advisory does not adjust." The recommendations are identical in content but the arbitration-auditor frames it as requiring a new helper function to parse arbitration output, while the spec-compliance-auditor frames it as a modification to the termination check. The implementation approach differs.

### T-3. Warning vs implementing unknown fields

The spec-compliance-auditor recommends an interim warning when `timing`/`influence` appear in config (R08, P2). The arbitration-auditor goes straight to implementation (R1, P1) with no interim warning. The tension: a warning is safer to ship quickly but creates a user-facing behavior change (warnings where there were none); direct implementation is correct but takes longer.

### T-4. Scope of template variable coverage

The spec-compliance-auditor provides a comprehensive "Areas of Strong Alignment" section covering config parsing, template loading, template filling, pipeline orchestration, dispute parsing, output layout, events, SDK, and MCP. The arbitration-auditor does not audit these areas -- the review is spec-006-scoped. The spec-compliance-auditor's broader scope gives higher confidence that non-arbitration features are correct, but the arbitration-auditor's narrower scope gives deeper confidence on arbitration-specific issues.

---

## Safe Agreements

### SA-1. `timing` and `influence` fields are the top-priority gap

Both auditors rate this as P1 with identical recommendations: add to `ArbiterConfig`, parse in `_resolve_arbiter`, validate inter-round/rounds cross-constraint.

### SA-2. `INFLUENCE_LEVEL` must be explicitly passed in `build_arbitration_context`

Both auditors agree the default-reliance approach is insufficient. Both cite the same code path.

### SA-3. Engine's core pipeline is a faithful extraction of pre-spec-006 SKILL.md

Both auditors agree the engine correctly implements phases 1-6, multi-round, stagnation, presets, and trigger evaluation as they existed before spec 006. The gaps are all in post-spec-006 additions.

### SA-4. `PRIOR_ARBITRATION_SECTION` must be populated for round 2+ reviews

Both auditors flag this (arbitration-auditor R4 at P1, spec-compliance-auditor R04 at P1). They agree the engine has the path (`PRIOR_ARBITRATION_PATH`) but never constructs the influence-aware block.
