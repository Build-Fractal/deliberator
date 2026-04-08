# Phase 3 Revision: storage-architect

**Spec**: 020-scenario-storage
**Reviewer**: storage-architect
**Date**: 2026-03-24
**Phase**: 3 (Revised Review After Cross-Review)

---

## Revisions Based on Cross-Review Feedback

### From plugin-engineer

1. **`exists()` in protocol needs resolution**: plugin-engineer notes the plugin calls `store.exists()` which is not part of the ScenarioStore protocol. If a future backend implements only the protocol, the plugin will fail. **Updated assessment**: Either add `exists()` to the protocol or refactor the plugin to use `try: store.load(); except ScenarioNotFoundError`.

2. **File atomicity and concurrent append**: Both confirmed as minor concerns. Document these limitations for FileScenarioStore.

### From spec-compliance

1. **FR-002 PARTIALLY MET accepted**: After spec-compliance agreed to revise FR-002 based on my mode validation finding, this is now consensus. `VALID_SCENARIO_MODES` should be used as a Pydantic validator on `GameStructure.mode`.

2. **RunRecord field divergence**: plugin-engineer's detailed mapping reveals `outcome` vs `termination_reason` and missing `agents_launched`. I missed this in Phase 1 because I focused on the data architecture, not field-by-field spec compliance. **Updated assessment**: Add to my findings as a model-spec divergence.

---

## Updated Key Issues

1. **Mode validation not enforced (medium)**: `VALID_SCENARIO_MODES` defined but not used. FR-002 PARTIALLY MET.
2. **`exists()` not in protocol (medium, elevated)**: Plugin depends on it. Protocol should include it.
3. **RunRecord field divergence (medium, new)**: `outcome` vs `termination_reason`, missing `agents_launched`.
4. **Missing error handling for store ops (medium, new from plugin-engineer)**: Plugin should wrap store operations in try/except.
5. **File atomicity (low)**: No temp-file-rename pattern.
6. **Concurrent append race (low)**: Document as limitation.

---

## Unchanged Assessments

- GameStructure/DataBindings separation: Excellent.
- ScenarioStore protocol: Well-designed.
- YAML round-trip safety: Correct.
- RunRecord append-only: Correct via immutable models.
