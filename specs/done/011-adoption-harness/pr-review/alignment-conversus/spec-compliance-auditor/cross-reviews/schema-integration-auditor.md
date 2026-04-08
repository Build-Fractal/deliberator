# Cross-Review: Spec Compliance Auditor reviewing Schema Integration Auditor

**Reviewer perspective**: spec-compliance-auditor
**Reviewed**: schema-integration-auditor
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1. Schema package existence: "Not started" vs implemented

The spec-compliance-auditor states in Missed Opportunity #4 that the `conversus/schemas/` package "does not exist on disk yet," relying on STATUS.md which says specs 012-013 are "Not started." The schema-integration-auditor's review demonstrates the package IS implemented: `conversus/schemas/game_forms.py`, `conversus/schemas/objectives.py`, `conversus/schemas/__init__.py`, with working tests (`tests/test_game_forms.py`, `tests/test_objectives.py`). The spec-compliance-auditor's factual error means recommendations about schema integration (or lack thereof) are based on an incorrect premise. STATUS.md appears to be out of date.

### DC-2. `VALID_MODES` duplication priority

The schema-integration-auditor rates mode registry unification as P1 (R2). The spec-compliance-auditor does not flag `VALID_MODES` duplication at all -- the review notes mode validation works correctly and moves on. The spec-compliance-auditor's "Areas of Strong Alignment" section includes mode validation as a positive finding. The schema-integration-auditor sees the same correct behavior but flags the underlying duplication as a risk. The spec-compliance-auditor's silence on this point may reflect that mode drift has never been observed and current correctness is confirmed.

### DC-3. `extra = "forbid"` recommendation absent from spec-compliance review

The schema-integration-auditor recommends `model_config = {"frozen": True, "extra": "forbid"}` on `ArbiterConfig` (R3, P1). The spec-compliance-auditor does not recommend this and instead recommends a P2 warning for unknown fields (R08). These are different approaches: `extra = "forbid"` causes hard failures for unknown fields; a warning allows the behavior to continue with a notice. The spec-compliance-auditor's warning approach is less disruptive but less safe. The schema-integration-auditor's approach is safer but could break existing configs if applied before `timing`/`influence` are added.

---

## Tensions

### T-1. Forward-looking vs present-focused analysis

The schema-integration-auditor's review is forward-looking: it evaluates config extensibility, mode-mapping preparation, game-form-to-config bridges, and spec-014+ readiness. The spec-compliance-auditor's review is present-focused: it evaluates what the engine does today against what SKILL.md specifies today. Both are valid perspectives, but they produce different priority lists. The schema-integration-auditor recommends `game_form` on `EngineConfig` (R5, P2) and `conversus_validate_schema` MCP tool (R7, P3) -- neither of which the spec-compliance-auditor would recommend because they address future specs, not current compliance.

### T-2. 011a decomposition assessment

The schema-integration-auditor flags 011a as P2 (R4), noting the `references/` directory exists but contains only agentskills documentation. The spec-compliance-auditor notes SKILL.md's current structure in passing but does not make 011a a recommendation. The spec-compliance-auditor's focus on engine-SKILL.md alignment means SKILL.md's internal structure (monolithic vs decomposed) is not relevant -- the engine does not parse SKILL.md.

### T-3. Test strategy

The schema-integration-auditor recommends a cross-package mode-set assertion test (R8, P3). The spec-compliance-auditor recommends a template-variable population test (R10, P3). Both are regression tests but for different invariants. The schema-integration-auditor's test catches mode drift; the spec-compliance-auditor's test catches template-context gaps. Both should exist, but the spec-compliance-auditor's test is more directly tied to the P1 findings.

### T-4. Import path discrepancy

The schema-integration-auditor flags that spec 013 says `from conversus_schemas.objectives import ...` but implementation uses `from conversus.schemas.objectives import ...` (O1). The spec-compliance-auditor does not mention this. The spec-compliance-auditor relied on STATUS.md ("Not started") rather than checking the actual implementation, which explains why this discrepancy was missed. This is a documentation-only issue but reveals a methodology gap.

---

## Safe Agreements

### SA-1. `timing` and `influence` are the top engine gap

Both auditors agree. The spec-compliance-auditor's R01 and the schema-integration-auditor's R1 are identical in substance.

### SA-2. Engine and schemas should remain isolated for now

Both auditors agree the zero-dependency separation is correct. The spec-compliance-auditor notes "no integration points... which is correct." The schema-integration-auditor confirms "cleanly isolated with zero import dependencies."

### SA-3. The engine's core pipeline is sound

Both auditors confirm the engine correctly implements phases 1-6, presets, multi-round, stagnation, and output structure for the pre-spec-006 feature set. The gaps are in the post-spec-006 additions (inter-round arbitration, influence, timing).
