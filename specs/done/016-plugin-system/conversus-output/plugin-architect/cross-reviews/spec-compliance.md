# Plugin Architect Cross-Review of Spec Compliance
# Spec: 016-plugin-system

**Cross-reviewer**: plugin-architect
**Reviewing**: spec-compliance's review at `conversus-output/spec-compliance/review.md`
**My review**: `conversus-output/plugin-architect/review.md`
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1: Engine integration — missing wiring vs. intentional separation

Spec-compliance marks FR-001, FR-003, and FR-006 as PARTIALLY MET because the engine does not yet call plugin loading or execution functions. My review O-1 flags the same gap. The contradiction is in the assessment: spec-compliance treats this as a partial-compliance gap; I frame it as a missing implementation piece that is the central deliverable of this spec.

**Resolution**: Both assessments are correct from different angles. The plugin framework (loading, execution, output writing) is fully implemented. The engine integration (wiring hooks into the pipeline) is not. The spec should explicitly list engine integration as a required deliverable, not assume it already exists.

### DC-2: FR-012 package naming

Spec-compliance marks FR-012 as NOT MET because the package is `conversus.plugins` not `conversus-plugins`. My review does not address packaging. This parallels the same issue in spec 015 (FR-014). The resolution should be consistent: amend FR-012 to match the actual namespace.

---

## Tensions

### T-1: FR-011 empty plugins/ directory

Spec-compliance notes the caveat that `plugins/` directory creation changes the output structure. My review does not flag this. The tension is in the severity: spec-compliance treats it as a minor FR-011 concern; I consider the `plugins/` directory to be outside the scope of "core output" (it is in a plugin-specific namespace). The spec's FR-011 says "Core deliberation output MUST be identical" -- the `plugins/` directory is not core deliberation output.

**My position**: FR-011 is MET without caveat. The `plugins/` directory is plugin output infrastructure, not core output. If this interpretation is disputed, the fix (schema-engineer's R-7: only create dir when plugins succeed) is trivial.

### T-2: Integration test priority

Spec-compliance R-3 recommends an integration test at P1. My review R-5 also recommends engine integration at P1. These are aligned on priority. The tension is in scope: spec-compliance's integration test runs a full deliberation pipeline; my engine integration defines where hooks fire. The integration test depends on the engine integration being done first.

---

## Safe Agreements

- **SA-1: FR-002 (empty plugins) is fully MET** -- Both reviews confirm identical behavior with no/empty plugins config.

- **SA-2: FR-005 (missing package resilience) is MET** -- Both reviews confirm warning-only, no crash.

- **SA-3: FR-007 (sequential execution) is MET** -- Both reviews confirm declaration-order execution.

- **SA-4: FR-008 (exception isolation) is MET** -- Both reviews confirm plugin failures are logged and skipped.

- **SA-5: All five success criteria are MET** -- Both reviews agree SC-001 through SC-005 pass.

- **SA-6: FR-013 (minimal dependencies) is MET** -- Both reviews confirm pydantic + stdlib only.

- **SA-7: FR-015 (Constitution Principle XV) is MET** -- Both reviews confirm structural enforcement of the five design principles.
