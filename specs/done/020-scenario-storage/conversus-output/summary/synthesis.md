# Phase 5 Synthesis: Spec 020 -- Scenario Storage

**Spec**: 020-scenario-storage
**Date**: 2026-03-24
**Agents**: storage-architect, plugin-engineer, spec-compliance

---

## Overall Assessment

The Scenario Storage implementation provides a well-designed data layer with clean architectural separation (GameStructure/DataBindings/RunRecord), a sound ScenarioStore protocol for backend extensibility, and correct YAML serialization round-trip safety. The Plugin ABC conformance is complete. The primary gaps are: many FRs are NOT VERIFIED because they pertain to CLI commands not yet implemented, FR-017 (cross-run analysis) is NOT IMPLEMENTED, and the RunRecord model diverges from the spec's field definitions. The data layer is solid; the presentation layer is absent.

---

## Consensus Findings

### 1. GameStructure/DataBindings Separation Excellent (Consensus)

**Unanimous**. The three-section model (reusable game structure, swappable data bindings, append-only run history) is cleanly implemented with appropriate boundaries. Agent roles capture the reasoning framework without data references. Bindings default to null in stored scenarios.

### 2. FR-002 PARTIALLY MET -- Mode Validation Missing (Consensus)

**Unanimous after revision**. `VALID_SCENARIO_MODES` is defined in models.py but not used as a Pydantic validator on `GameStructure.mode`. Invalid mode strings are accepted silently. The fix is to add a Pydantic `field_validator` that checks against `VALID_SCENARIO_MODES`.

### 3. Missing Error Handling for Store Operations (Consensus)

**Unanimous**. The plugin's `execute()` calls `store.save()` and `store.append_run()` without try/except. If the scenarios directory is unwritable or YAML serialization fails, the exception propagates and the plugin crashes. This violates the principle of graceful plugin degradation.

**Recommendation**: Wrap store operations in try/except and return an advisory error PluginResult on failure.

### 4. RunRecord Field Divergence (Consensus)

**Unanimous**. The spec's Section 2.3 defines run history fields that differ from the RunRecord model:
- `outcome` (spec) vs `termination_reason` (model) -- different semantics
- `agents_launched` -- present in spec, absent from model
- `date` (spec) vs `timestamp` (model) -- acceptable rename
- `rounds_used` (spec) vs `rounds_completed` (model) -- acceptable rename

**Recommendation**: Rename `termination_reason` to `outcome` and add `agents_launched: int = 0` to the RunRecord model.

### 5. FR-017 NOT IMPLEMENTED -- Cross-Run Analysis (Consensus)

**Unanimous**. No analysis computation exists. The spec requires that with 3+ runs, `/conversus scenarios <name> --analysis` reports outcome consistency, average metrics, and equilibrium score trend. Neither the data layer nor the CLI implements this.

**Recommendation**: Implement analysis methods on the data layer (could be a static function that takes a Scenario and produces analysis dict).

### 6. ScenarioStore Protocol Well-Designed (Consensus)

**Unanimous**. The `runtime_checkable` protocol with 5 methods (save, load, list_scenarios, append_run, delete) is clean and extensible. FileScenarioStore satisfies the protocol. The design enables future PostgreSQL or Memgraph backends.

### 7. `exists()` Not in Protocol (Consensus)

**Unanimous**. The plugin calls `store.exists()` which is implemented on `FileScenarioStore` but not part of the `ScenarioStore` protocol. Future backends must implement it ad hoc.

**Recommendation**: Add `exists(name: str) -> bool` to the ScenarioStore protocol.

### 8. YAML Round-Trip Safety Correct (Consensus)

**Unanimous**. The Pydantic model_dump -> YAML dump -> YAML safe_load -> Pydantic model_validate pipeline handles all type conversions correctly, including datetime serialization.

### 9. RunRecord Append-Only Correct (Consensus)

**Unanimous**. Frozen Pydantic models prevent in-place modification. `append_run()` creates a new Scenario instance with the extended history list. Manual YAML editing is the only way to modify history (intentional friction per FR-016).

### 10. CLI Commands NOT VERIFIED (Consensus)

**Unanimous**. FR-004, FR-005, FR-008, FR-009, FR-010, FR-012, FR-013 pertain to CLI commands (/conversus save, replay, scenarios) that are not implemented in the reviewed code. The data layer provides the foundation but the CLI wiring is absent.

---

<!-- DISPUTES_BEGIN -->

## Unresolved Disputes

None. All disagreements were resolved during the cross-review phase. Full consensus was achieved on all findings, including the FR-002 revision from MET to PARTIALLY MET.

<!-- DISPUTES_END -->

---

## Compliance Summary

| Requirement | Status | Notes |
|-------------|--------|-------|
| FR-001 | MET | |
| FR-002 | PARTIALLY MET | Mode validation missing |
| FR-003 | MET | |
| FR-004 | NOT VERIFIED | CLI layer |
| FR-005 | NOT VERIFIED | CLI layer |
| FR-006 | MET | |
| FR-007 | MET | Record appended; field names differ |
| FR-008 | NOT VERIFIED | CLI layer |
| FR-009 | NOT VERIFIED | CLI layer |
| FR-010 | NOT VERIFIED | CLI layer |
| FR-011 | MET (by design) | |
| FR-012 | NOT VERIFIED | CLI layer |
| FR-013 | NOT VERIFIED | CLI layer |
| FR-014 | MET | |
| FR-015 | MET | |
| FR-016 | MET | |
| FR-017 | **NOT IMPLEMENTED** | No analysis |
| FR-018 | N/A | |
| FR-019 | MET | |
| SC-001 | MET | |
| SC-002 | NOT VERIFIED | |
| SC-003 | NOT IMPLEMENTED | |
| SC-004 | MET | |
| SC-005 | MET | |

**MET**: 9/19 FR, 3/5 SC
**PARTIALLY MET**: 1 FR
**NOT MET**: 0
**NOT IMPLEMENTED**: 1 FR, 1 SC
**NOT VERIFIED**: 7 FR, 1 SC
**N/A**: 1 FR

---

## Recommended Actions

1. Add mode validation: Use `VALID_SCENARIO_MODES` as a Pydantic validator on `GameStructure.mode`.
2. Add error handling: Wrap store operations in plugin's `execute()` with try/except.
3. Fix RunRecord fields: Rename `termination_reason` to `outcome`, add `agents_launched`.
4. Add `exists()` to ScenarioStore protocol.
5. Implement cross-run analysis (FR-017): Static function on Scenario data.
6. Add execute_hooks() integration test for ScenarioPlugin.
7. Explicitly set `advisory=True` in PluginResult constructor for consistency.
8. Implement CLI commands (save, replay, scenarios) to resolve NOT VERIFIED FRs.
