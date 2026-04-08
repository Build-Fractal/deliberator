# Cross-Review: Guided Workflow Auditor reviewing Schema Integration Auditor

**Reviewer perspective**: guided-workflow-auditor
**Reviewed**: schema-integration-auditor
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1. Schemas "no conflicts" verdict vs guided workflow delegation gaps

The schema-integration-auditor concludes "No conflicts. No regressions. But no integration either." This framing misses that the guided workflow handlers are the *primary consumers* of engine output, and the schema package's isolation means it cannot help bridge the delegation gap between SKILL.md handlers and the engine. The guided-workflow-auditor identifies the dual-execution-path problem as fundamental; the schema-integration-auditor's clean-isolation finding obscures the fact that schemas are irrelevant to the most pressing architectural gap.

### DC-2. Priority of mode registry unification

The schema-integration-auditor elevates the `VALID_MODES` duplication to P1 (R2: "Create a canonical mode list consumed by both packages"). The guided-workflow-auditor flags mode alignment as P3 (R7) -- noting the values are currently identical and the risk is theoretical drift. The P1 classification is disproportionate: mode drift has never occurred and would be caught immediately by any test, while the missing `timing`/`influence` fields cause silent incorrect behavior today.

### DC-3. 011a decomposition priority

The schema-integration-auditor rates 011a SKILL.md decomposition as P2 (R4). The guided-workflow-auditor does not recommend 011a decomposition at all -- the review notes the engine does not parse SKILL.md, so decomposition has zero engine impact. From the guided-workflow perspective, 011a is a context-window optimization, not an alignment concern. Elevating it to P2 in an alignment review conflates operational convenience with correctness.

---

## Tensions

### T-1. `extra = "forbid"` on ArbiterConfig

The schema-integration-auditor recommends setting `extra = "forbid"` on `ArbiterConfig` (R3) so that unknown fields like `timing` and `influence` are rejected rather than silently ignored. The guided-workflow-auditor recommends the opposite approach: *add* the fields (R1) so they are parsed and used. Both are valid but the sequencing matters -- if `extra = "forbid"` lands first, existing configs with `timing`/`influence` would start failing before the engine can handle them.

### T-2. Game form awareness as a config extension

The schema-integration-auditor recommends adding `game_form` as an optional auto-resolved field on `EngineConfig` (R5). The guided-workflow-auditor does not mention game forms at all. From the guided-workflow perspective, the `/conversus mode` handler generates configs based on mode choice, not game-theoretic form. Adding `game_form` to the config surface creates a field that guided-workflow handlers would need to understand and possibly populate, adding complexity without guided-workflow benefit.

### T-3. MCP tool surface area

The schema-integration-auditor recommends a `conversus_validate_schema` MCP tool (R7). The guided-workflow-auditor recommends `conversus_gate`, `conversus_cost`, and a public dispute-parsing API (R4-R6). The two auditors are expanding the MCP surface in different directions with no discussion of priority ordering. The guided-workflow tools address immediate delegation gaps; the schema tools address future spec-014+ needs.

### T-4. Spec 013 import path discrepancy

The schema-integration-auditor flags that spec 013 says `from conversus_schemas.objectives import ...` but implementation uses `from conversus.schemas.objectives import ...` (O1). The guided-workflow-auditor does not mention import paths. This is a documentation-only issue with no guided-workflow impact, but it reveals that the schema-integration-auditor is reviewing against spec text while the guided-workflow-auditor reviews against runtime behavior.

---

## Safe Agreements

### SA-1. `timing` and `influence` are the top-priority engine gap

Both auditors identify the missing `ArbiterConfig` fields as the most critical finding. The schema-integration-auditor's R1 and the guided-workflow-auditor's R1 are the same recommendation with the same code location.

### SA-2. Engine and schemas are correctly isolated

Both auditors agree the zero-import-dependency between `engine/` and `conversus/schemas/` is by design and correctly implemented. The guided-workflow-auditor notes the engine does not need schema awareness for current modes; the schema-integration-auditor confirms this matches spec 012's constraint.

### SA-3. Engine does not parse SKILL.md

Both auditors agree that SKILL.md is a human/agent-facing document and the engine's runtime behavior is independent of SKILL.md's structure. The 011a decomposition has no engine impact.
