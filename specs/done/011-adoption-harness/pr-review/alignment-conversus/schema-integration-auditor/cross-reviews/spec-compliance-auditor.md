# Cross-Review: Schema Integration Auditor reviewing Spec Compliance Auditor

**Reviewer perspective**: schema-integration-auditor
**Reviewed**: spec-compliance-auditor
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1. Schema package existence claim

The spec-compliance-auditor states in Missed Opportunity #4: "This package does not exist on disk yet." However, the schema-integration-auditor's review confirms `conversus/schemas/` EXISTS with `game_forms.py`, `objectives.py`, `__init__.py`, and working tests (`tests/test_game_forms.py`, `tests/test_objectives.py`). The spec-compliance-auditor appears to have checked `STATUS.md` (which says specs 012-013 are "Not started") rather than the filesystem. This factual error could lead to incorrect prioritization -- dismissing schema integration work that is already implementable.

### DC-2. `arbiter/` vs `arbitration/` -- path mismatch severity

The spec-compliance-auditor rates this as P1 (R03). The schema-integration-auditor does not flag this because the schema package has no dependency on output directory names. However, if the directory name is indeed wrong, it affects future schema integration: any tool that writes game-form metadata alongside arbitration output needs to know the correct directory name. The spec-compliance-auditor's finding is valid but the P1 rating assumes consumers of the output exist today. The schema-integration-auditor's silence reflects that schemas do not consume output paths.

### DC-3. `PRIOR_ROUND_SECTION` as a P1 concern

The spec-compliance-auditor flags `PRIOR_ROUND_SECTION` always being empty as P1 (R05). The schema-integration-auditor does not mention this variable at all. From the schema perspective, `PRIOR_ROUND_SECTION` is a template orchestration concern with no schema impact. The P1 rating seems calibrated to "silent incorrectness" but the incorrectness only manifests when multi-round deliberations use templates that reference this variable. If the templates also pass `PRIOR_SYNTHESIS_PATH` and `PRIOR_ROUND_DIR` as separate variables, agents may still receive prior-round context through those individual paths.

---

## Tensions

### T-1. Comprehensiveness vs focus

The spec-compliance-auditor's review covers the entire engine surface: config parsing, template loading, template filling, pipeline orchestration, dispute parsing, output layout, events, SDK, and MCP. The schema-integration-auditor is focused on engine-schema boundaries. The spec-compliance-auditor's breadth is valuable for overall confidence but means each finding gets less depth. The schema-integration-auditor's mode-duplication finding, for instance, has detailed analysis of tuple vs frozenset types that the spec-compliance-auditor's review does not reach.

### T-2. Schema package integration framing

The spec-compliance-auditor frames the schema package as a future concern: "specs 012 and 013 are 'Not started' per STATUS.md." The schema-integration-auditor's review shows the package IS implemented and has tests. This status discrepancy affects priority: the spec-compliance-auditor correctly notes no engine integration exists, but incorrectly implies the schemas themselves are not yet built. Integration work could begin now.

### T-3. `VALID_MODES` duplication visibility

The schema-integration-auditor elevates `VALID_MODES` duplication to P1. The spec-compliance-auditor mentions mode validation passing correctly: "mode validation" in the Strong Alignment section. By confirming mode validation works, the spec-compliance-auditor implicitly agrees the values are currently consistent, but does not flag the duplication risk. The tension: one auditor sees working validation as "aligned," the other sees dual definitions as a ticking time bomb.

### T-4. MCP tool recommendations

The spec-compliance-auditor does not recommend any new MCP tools. The schema-integration-auditor recommends `conversus_validate_schema` (R7, P3). The spec-compliance-auditor's silence on MCP tool expansion may reflect a "fix existing behavior first" philosophy, while the schema-integration-auditor wants to prepare the tool surface for future schema workflows.

---

## Safe Agreements

### SA-1. `timing` and `influence` are the top-priority engine gap

Both auditors rate this as P1 with the same recommendation. The spec-compliance-auditor's R01 and the schema-integration-auditor's R1 are functionally identical.

### SA-2. Engine handles core pipeline correctly

Both auditors agree the engine is a faithful extraction of pre-spec-006 SKILL.md. The spec-compliance-auditor's "Areas of Strong Alignment" section confirms config parsing, template loading/filling, pipeline orchestration, and dispute parsing are correct. The schema-integration-auditor's config-parser extensibility analysis (section 4) reaches the same conclusion.

### SA-3. Engine does not need game form awareness for current modes

The spec-compliance-auditor notes "The engine has no integration points for [schemas], which is correct since both specs are 'Not started' per STATUS.md." The schema-integration-auditor reaches the same conclusion via a different path: "Game forms become necessary only when modes need parametric configuration (spec 019) or when new modes are added." Both agree the current four modes work without game-form context.
