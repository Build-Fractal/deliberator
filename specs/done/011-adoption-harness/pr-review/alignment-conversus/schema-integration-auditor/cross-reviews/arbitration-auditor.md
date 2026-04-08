# Cross-Review: Schema Integration Auditor reviewing Arbitration Auditor

**Reviewer perspective**: schema-integration-auditor
**Reviewed**: arbitration-auditor
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1. Output directory naming: "matches spec 006" vs discrepancy

The arbitration-auditor states "Output directory layout matches spec 006 US-4" (What the engine gets right, item 5) and praises `get_arbitration_path(round_base=...)`. The spec-compliance-auditor (for reference) flags that the engine uses `arbiter/` while SKILL.md uses `arbitration/`. The schema-integration-auditor observes that `OutputManager` path methods were not checked against the SKILL.md text in the arbitration-auditor's review. If the directory name truly diverges from SKILL.md, the arbitration-auditor's "matches" claim is inaccurate. This matters for schema integration because any future schema-aware output (e.g., game form metadata alongside arbitration output) must know the correct directory name.

### DC-2. Arbitration-only scope misses mode registry drift risk

The arbitration-auditor does not mention the `VALID_MODES` duplication between `engine/config.py` and `conversus/schemas/objectives.py`. The schema-integration-auditor identifies this as P1 (R2). From the schema perspective, mode validation is upstream of arbitration: if modes drift, the engine could accept configs with modes that the schema package rejects (or vice versa), affecting which arbitration templates load. The arbitration-auditor's scope exclusion means this coupling is unexamined.

### DC-3. No discussion of schema-arbitration interaction paths

The arbitration-auditor's review is entirely engine-internal. It does not consider how `conversus/schemas/` game form models could provide game-theoretic context to arbitration templates. The schema-integration-auditor notes that the engine treats mode as a template-directory selector with no game-form awareness. For arbitration specifically, this means the arbiter receives mode-specific templates but no formal game structure (Nash equilibria, Pareto frontiers) that could inform arbitration decisions. The arbitration-auditor's recommendations focus on `timing`/`influence` mechanics without questioning whether the arbiter's decision framework is complete.

---

## Tensions

### T-1. Scope of `ArbiterConfig` extension

The arbitration-auditor recommends adding only `timing` and `influence` to `ArbiterConfig` (R1). The schema-integration-auditor's review implies that `ArbiterConfig` could also benefit from an optional `game_form` reference for game-theoretic arbitration context. These are different extension vectors for the same model. The arbitration-auditor's additions are spec-006-mandated; the schema-integration-auditor's would be spec-014+ preparation. They are compatible but compete for config surface design attention.

### T-2. Pydantic `extra` field handling strategy

The arbitration-auditor assumes the fix is to ADD fields (R1). The schema-integration-auditor recommends ALSO setting `extra = "forbid"` (R3) to prevent future silent drops. From the schema perspective, `extra = "forbid"` is a principled approach that prevents any config key from being silently ignored. The arbitration-auditor's approach handles the known gaps but leaves the door open for future fields to be silently dropped.

### T-3. Template variable completeness

The arbitration-auditor identifies 7 specific missing template variable behaviors (What the engine gets wrong, items 5-6). The schema-integration-auditor identifies the same `INFLUENCE_LEVEL` gap but does not trace through all template variables. The arbitration-auditor's depth reveals that the gap extends beyond just the arbitration context to review context, cross-round synthesis context, and stagnation detection -- a broader surface than the schema-integration-auditor examined.

### T-4. Test strategy divergence

The arbitration-auditor recommends an integration test for `timing: inter-round` + `influence: advisory` (R8). The schema-integration-auditor recommends a cross-package mode-set assertion test (R8). Both are P3 test recommendations targeting different failure modes. From the schema perspective, mode-set consistency is a fundamental invariant; from the arbitration perspective, behavioral correctness under complex configuration is more valuable.

---

## Safe Agreements

### SA-1. `timing` and `influence` must be added to `ArbiterConfig`

Both auditors agree this is the most critical fix. The arbitration-auditor provides detailed per-field semantics; the schema-integration-auditor provides the config-parser extensibility assessment confirming the change is safe.

### SA-2. Pydantic defaults mask the `timing`/`influence` gap

Both auditors note that the engine silently falls back to `final`/`binding` behavior when these fields appear in config. Both agree this is problematic -- either the fields should be implemented or the engine should reject them.

### SA-3. Linter/schema layer is ahead of the engine

Both auditors confirm that `linter/models.py` already has `InfluenceLevel`, `ArbiterTiming`, and the template variable fields. The schema layer is also complete (game forms, objectives). The engine is the lagging component. This convergence on "engine needs to catch up" is shared.
