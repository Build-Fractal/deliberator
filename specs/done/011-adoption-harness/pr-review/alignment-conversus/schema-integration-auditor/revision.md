# Schema Integration Auditor — Revision

**Agent**: schema-integration-auditor
**Phase**: 3 (Revision after cross-review)
**Date**: 2026-03-24

---

## Recommendation Dispositions

### R1. Add `timing` and `influence` fields to `ArbiterConfig` — SURVIVING (P1)

**Status**: Unchanged. Universal agreement. This was flagged as "engine gap, not schema issue but surfaces during this audit" in the original review. The cross-review process confirmed it is the single highest-priority item across all four auditors.

### R2. Create a canonical mode list consumed by both packages — MODIFIED (P1 -> P3)

**Original**: P1, "critical" consistency risk from dual `VALID_MODES` definitions.
**Modification**: Downgraded to P3. Three cross-reviews challenged the P1 rating:
- The guided-workflow-auditor's cross-review notes the values are identical, have never drifted, and would be caught by any test (DC-2).
- The arbitration-auditor's cross-review calls this "theoretical risk with zero current impact" while spec 006 gaps "cause silent incorrect behavior today" (DC-1).
- The spec-compliance-auditor's cross-review notes they confirmed mode validation works correctly and did not flag duplication as a concern (T-3).

The P1 rating was disproportionate. Mode drift is a maintenance concern, not a correctness concern. A shared constants module or consumption of the existing `mode-mapping.yml` remains good practice but is not urgent. Accepting the consensus that P3 is appropriate.

### R3. Validate or reject unknown arbiter config fields — MODIFIED (P1 -> sequencing constraint on R1)

**Original**: P1, recommending `extra = "forbid"` on `ArbiterConfig`.
**Modification**: Withdrawn as an independent recommendation. Absorbed into a sequencing constraint: if `extra = "forbid"` is adopted, it MUST ship in the same commit as R1 (adding `timing` and `influence` fields). The arbitration-auditor's cross-review (DC-2) and the guided-workflow-auditor's cross-review (T-1) both identify that applying `extra = "forbid"` before adding the fields would break existing configs. The spec-compliance-auditor recommends an interim warning (their R08) as a less disruptive alternative. Deferring to the implementation approach: add the fields with `extra = "forbid"` atomically, or add the fields without `extra = "forbid"` and add it later.

### R4. Implement the 011a SKILL.md decomposition — MODIFIED (P2 -> P4/deferred)

**Original**: P2, noting `references/` directory exists but contains no handler extractions.
**Modification**: Deferred. Two cross-reviews challenged the P2 rating:
- The guided-workflow-auditor's cross-review calls 011a "a context-window optimization, not an alignment concern" (DC-3).
- The spec-compliance-auditor's cross-review notes the engine does not parse SKILL.md, so decomposition has no engine impact (T-2).

Both are correct. 011a decomposition is operational (reduces context window costs for agents reading SKILL.md) but has zero impact on engine alignment, schema integration, or runtime correctness. It does not belong in an alignment review's priority list. Deferring to the 011a spec's own implementation timeline.

### R5. Add `game_form` as optional auto-resolved field on `EngineConfig` — SURVIVING (P2 -> P3)

**Original**: P2, preparation for spec 014.
**Modification**: Downgraded to P3. The guided-workflow-auditor's cross-review (T-2) correctly notes this adds complexity to the config surface without guided-workflow benefit. The arbitration-auditor's cross-review (T-2) notes game forms are "completely orthogonal to arbitration correctness." The field would be informational-only in the current engine with no behavioral change. P3 for future readiness is more appropriate than P2 for importance.

### R6. Fix spec 013 FR-011 import path — SURVIVING (P2)

**Status**: Unchanged. The spec-compliance-auditor's cross-review (DC-1) revealed they checked STATUS.md instead of the filesystem and believed the schemas package did not exist. This import path discrepancy will confuse anyone reading the spec. Documentation-only fix, low effort, high clarity value. Retaining P2.

### R7. Add `conversus_validate_schema` MCP tool — SURVIVING (P3)

**Status**: Unchanged. The guided-workflow-auditor's cross-review correctly notes delegation tools (their R4-R6) address more immediate gaps than schema validation tools. Accepted: this is future-facing and appropriately P3.

### R8. Create cross-package mode-set assertion test — SURVIVING (P3)

**Status**: Unchanged. The arbitration-auditor's cross-review recommends a behavioral integration test (their R8) targeting a different concern. Both tests should exist. The mode-set assertion test is a 10-line regression guard. Retaining P3.

### R9. Add `conversus/schemas` to project AGENTS.md — SURVIVING (P3)

**Status**: Unchanged. No cross-reviewer contested this. Straightforward documentation update.

### R10. Document zero-dependency contract in `conversus/schemas/__init__.py` — SURVIVING (P3)

**Status**: Unchanged. No cross-reviewer contested this. Makes the architectural boundary explicit in code.

---

## New Recommendations

### N1. Correct STATUS.md to reflect schemas implementation status (P2)

**Triggered by**: spec-compliance-auditor cross-review DC-1 and the spec-compliance-auditor's own Missed Opportunity #4.

The spec-compliance-auditor stated the schemas package "does not exist on disk yet," relying on STATUS.md which says specs 012-013 are "Not started." The schemas package IS implemented with working tests. STATUS.md is out of date. This caused the spec-compliance-auditor to dismiss schema integration opportunities based on an incorrect premise. STATUS.md should be updated to reflect the actual implementation state of specs 012 and 013.

### N2. Dual-execution-path implications for schema integration (architectural note)

**Triggered by**: guided-workflow-auditor's cross-review DC-1 and the schema-integration-auditor's own cross-review of the guided-workflow-auditor.

The guided-workflow-auditor's finding that SKILL.md handlers are a parallel execution path invalidates the assumption that bridging schemas to the engine is sufficient for guided workflow access. If guided handlers are the primary execution path, schema integration (spec 014+) must expose game form context through SKILL.md-accessible channels (e.g., MCP tools, file-based lookups), not just through engine Python APIs. This is a future architecture note, not an immediate action item, but it should be recorded as a constraint for spec 014 planning.

---

## Position Summary

The schema-integration-auditor's central finding -- that schemas and engine are cleanly isolated with no conflicts but no integration -- remains valid. The cross-review process did not challenge the isolation finding or the "no regressions" verdict. The primary adjustments are to priority ratings, not to the substance of findings.

The most significant concession is downgrading `VALID_MODES` unification from P1 to P3. The original P1 rating was disproportionate given that the values are identical and the risk is theoretical. Three independent cross-reviews challenged it, and the evidence supports P3. The `extra = "forbid"` recommendation (R3) is absorbed into a sequencing constraint rather than standing alone, because applying it before R1 would break configs. The 011a decomposition (R4) is deferred entirely as it has no alignment impact.

The most valuable new insight from the cross-review process is the dual-execution-path architecture identified by the guided-workflow-auditor. This has direct implications for schema integration planning: the bridge between schemas and the execution layer must account for both the Python engine and the SKILL.md handler path. This does not change any immediate recommendation but reshapes the architectural assumptions for specs 014+.
