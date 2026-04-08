# Cross-Review: Arbitration Auditor reviewing Schema Integration Auditor

**Reviewer perspective**: arbitration-auditor
**Reviewed**: schema-integration-auditor
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1. P1 priority allocation: mode registry vs inter-round arbitration

The schema-integration-auditor elevates `VALID_MODES` duplication to P1 (R2), calling it "critical." The arbitration-auditor's P1 list is entirely spec-006-focused: `timing`/`influence` fields, inter-round arbitration dispatch, `INFLUENCE_LEVEL` passing, and `PRIOR_ARBITRATION_SECTION` construction. Mode registry drift is a theoretical risk with zero current impact. Spec 006 gaps cause silent incorrect behavior today for any config specifying non-default arbitration settings. Calling mode duplication P1-critical while inter-round arbitration is the actual blocking gap distorts priority ordering.

### DC-2. `extra = "forbid"` recommendation conflicts with field-addition approach

The schema-integration-auditor recommends `model_config = {"frozen": True, "extra": "forbid"}` on `ArbiterConfig` (R3). The arbitration-auditor recommends adding `timing` and `influence` fields (R1). If `extra = "forbid"` is applied before the fields are added, configs written per SKILL.md will start raising validation errors -- a breaking change. The arbitration-auditor's approach (add the fields with defaults) is non-breaking. These two recommendations are sequencing-incompatible: R3 must come AFTER R1, or they must be applied atomically.

### DC-3. Schema isolation framing obscures arbitration gaps

The schema-integration-auditor's executive summary focuses on the `conversus/schemas/` package being "an island" and recommends bridge work for spec 014+. This is a forward-looking concern. The arbitration-auditor's review reveals that the engine has gaps in its *existing* arbitration pipeline that affect correctness today. The schema-integration-auditor mentions `timing`/`influence` as a "schema-relevant" observation (section 8) but positions it as incidental to the schema audit rather than the primary finding. From the arbitration perspective, this framing buries the most impactful finding.

---

## Tensions

### T-1. Scope of `timing`/`influence` concern

The arbitration-auditor dedicates 8 specific findings to the `timing`/`influence` gap (What the engine gets wrong, items 1-7, plus the Off-Base Assumptions). The schema-integration-auditor mentions it in one section (section 8) with three bullet points. The depth difference is appropriate given their scopes, but the schema-integration-auditor's brevity could lead readers to underestimate the implementation complexity.

### T-2. Game form integration as a future concern vs irrelevant

The schema-integration-auditor spends significant attention on game form awareness, mode-to-form mapping, and config extensibility for `game_form` (sections 3-4, R5). The arbitration-auditor does not mention game forms at all. From the arbitration perspective, game forms are completely orthogonal to arbitration correctness. The tension: the schema-integration-auditor sees the config surface as needing expansion in the game-form direction, while the arbitration-auditor sees it needing expansion in the arbitration-field direction. These are independent but compete for implementation attention.

### T-3. Test isolation vs cross-package regression testing

The schema-integration-auditor notes clean test isolation between schema tests and engine tests (section 7) and recommends a cross-package mode-set assertion test (R8). The arbitration-auditor recommends an integration test for `timing: inter-round` + `influence: advisory` (R8). Both are P3 test recommendations but target completely different concerns. The arbitration test has higher value: it catches behavioral regressions in a complex scenario, while the mode-set test catches a drift that has never occurred.

### T-4. MCP tool expansion scope

The schema-integration-auditor recommends `conversus_validate_schema` for game form validation (R7, P3). The arbitration-auditor does not recommend any MCP changes. From the arbitration perspective, the MCP surface should prioritize arbitration-related capabilities (e.g., a tool for running Phase 6 independently) before adding schema validation tools for unimplemented features.

---

## Safe Agreements

### SA-1. `timing` and `influence` must be added to `ArbiterConfig`

Both auditors identify this as the most critical engine gap. The schema-integration-auditor's R1 and the arbitration-auditor's R1 are functionally identical recommendations.

### SA-2. Engine and schemas are correctly isolated

Both auditors confirm zero import dependencies between `engine/` and `conversus/schemas/`. The arbitration-auditor's review does not reference the schemas package at all, which is itself evidence of correct isolation.

### SA-3. Pydantic defaults mask the gap

Both auditors note that `ArbiterConfig` silently drops `timing`/`influence` because Pydantic does not reject extra fields by default. The schema-integration-auditor frames this as a validation concern; the arbitration-auditor frames it as a correctness concern. Both agree it is problematic.
