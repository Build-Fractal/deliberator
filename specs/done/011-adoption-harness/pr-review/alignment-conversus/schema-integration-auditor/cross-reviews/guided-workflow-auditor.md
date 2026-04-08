# Cross-Review: Schema Integration Auditor reviewing Guided Workflow Auditor

**Reviewer perspective**: schema-integration-auditor
**Reviewed**: guided-workflow-auditor
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1. Dual-execution-path finding has schema integration implications

The guided-workflow-auditor identifies that SKILL.md handlers and the Python engine are parallel implementations of the same pipeline. The schema-integration-auditor's review assumes the engine is the programmatic entry point and schemas would integrate through it. If SKILL.md handlers are the primary execution path for guided workflow, then schema integration (spec 014+) would need to expose game form context to SKILL.md handlers, not just to the engine. The guided-workflow-auditor's finding invalidates the schema-integration-auditor's assumption that bridging schemas to the engine is sufficient.

### DC-2. Mode alignment framing: single source of truth vs current correctness

The guided-workflow-auditor rates mode alignment as P3 (R7), noting "this is currently aligned" and suggesting a shared constants module as a future-proofing measure. The schema-integration-auditor rates mode registry unification as P1 (R2), calling the dual definition a "critical" consistency risk. The guided-workflow-auditor's evidence -- that the values are identical and have never drifted -- undermines the P1 classification. If mode values are already correct, unification is a maintenance improvement, not a critical fix.

### DC-3. MCP tool priorities diverge on direction

The guided-workflow-auditor recommends `conversus_gate` (R5), `conversus_cost` (R6), and public dispute-parsing API (R4) -- all aimed at enabling SKILL.md handlers to delegate to the engine. The schema-integration-auditor recommends `conversus_validate_schema` (R7) -- aimed at editor-time validation of game definitions. These pull the MCP surface in orthogonal directions. The guided-workflow-auditor's tools address an immediate architectural gap (delegation seam); the schema-integration-auditor's tool addresses a future spec-014+ workflow. Implementing schema validation tools before delegation tools would be sequencing the lower-impact work first.

---

## Tensions

### T-1. Config surface expansion: guided workflow fields vs game form fields

The guided-workflow-auditor's R1-R3 (P1) push for `timing`, `influence`, and Phase 6-only entry points on the config/engine surface. The schema-integration-auditor's R5 (P2) pushes for `game_form` on the config surface. Both are additive to `EngineConfig`, but they compete for the same config design attention. The guided-workflow-auditor's fields have immediate behavioral impact; the schema-integration-auditor's field is informational-only in the current engine.

### T-2. 011a decomposition relevance

The schema-integration-auditor flags 011a (SKILL.md decomposition) as P2 and partially implemented. The guided-workflow-auditor does not mention 011a at all. The schema-integration-auditor's concern is that a monolithic SKILL.md affects context window costs; the guided-workflow-auditor's concern is delegation mechanics. These are different problems. The guided-workflow-auditor's silence on 011a suggests it is irrelevant to the guided-workflow-to-engine delegation question.

### T-3. Engine's config parser extensibility assessment

The schema-integration-auditor notes `parse_config()` is extensible because Pydantic's default does not set `extra = "forbid"` (section 4), framing this as a positive. The guided-workflow-auditor notes that `parse_config()` "silently drops" `timing`/`influence` (R1), framing the same behavior as a bug. Both are describing the same Pydantic behavior -- one sees extensibility, the other sees silent data loss.

### T-4. Cost estimation as an integration concern

The guided-workflow-auditor identifies cost estimation duplication between SKILL.md and `engine.cost.estimate_cost()` as a missed opportunity (#4). The schema-integration-auditor does not mention cost estimation. From the schema perspective, cost estimation is outside the schema/engine integration boundary. But the guided-workflow-auditor's finding suggests that ANY formula duplicated between SKILL.md and the engine is an integration debt, which could apply to schema-related concepts too (e.g., mode-to-form mapping logic duplicated in templates and schemas).

---

## Safe Agreements

### SA-1. `timing` and `influence` are the top engine gap

Both auditors agree. The guided-workflow-auditor frames it as blocking guided workflow execution; the schema-integration-auditor frames it as an engine gap surfaced during schema audit. Same finding, same recommendation.

### SA-2. Engine correctly does not parse or depend on SKILL.md

Both auditors confirm the engine's `find_templates_dir()` and `_find_conversus_root()` heuristics are unaffected by SKILL.md changes. The guided-workflow-auditor explicitly notes the engine "does not interfere with other subcommands."

### SA-3. Zero import dependency between engine and schemas is correct

The guided-workflow-auditor does not mention the schemas package at all, which is itself evidence of correct isolation. The schema-integration-auditor confirms this isolation by checking all import paths.
