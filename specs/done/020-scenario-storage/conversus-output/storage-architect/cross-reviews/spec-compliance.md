# Phase 2 Cross-Review: storage-architect reviews spec-compliance

**Spec**: 020-scenario-storage
**Reviewer**: storage-architect
**Reviewing**: spec-compliance's Phase 1 review
**Date**: 2026-03-24

---

## Agreement

1. **NOT VERIFIED for CLI commands**: Correct assessment. FR-004, FR-005, FR-008, FR-009, FR-010, FR-012, FR-013 are all CLI-layer concerns not implemented in the plugin or data layer under review. The data layer (models + storage + plugin) provides the foundation, but the CLI commands that wire it together are absent.

2. **FR-017 NOT IMPLEMENTED**: No cross-run analysis exists. This is a genuine feature gap, not a "not verified" -- the data layer does not provide analysis methods either.

3. **FR-019 MET**: The protocol is well-designed and FileScenarioStore passes the runtime_checkable test.

4. **SC-005 MET**: The equilibrium_score optional field is correctly handled.

## Points to Add

1. **FR-016 append-only verification**: spec-compliance marks FR-016 as MET. I want to add evidence: the frozen Pydantic model makes in-place modification impossible. `append_run()` creates a new Scenario object. The only write path is `save()` which overwrites the entire file. This is the correct implementation of append-only semantics -- the file is replaced, but the new file always contains all previous records plus the new one.

2. **FR-014 human-readable qualification**: spec-compliance marks FR-014 as MET. I want to note that `default_flow_style=False` ensures block-style YAML, but `sort_keys=False` means key order follows the model field declaration. This is deterministic and readable, but reordering model fields would change the YAML layout. Using an explicit field ordering would be more robust.

3. **FR-002 validation scope**: spec-compliance marks FR-002 as MET. The Pydantic model validates types and required fields, but does NOT validate mode against `VALID_SCENARIO_MODES`. I identified this in my Phase 1 review. A scenario with mode="invalid" would pass Pydantic validation. spec-compliance should note this gap.

## Disagreement

**FR-002 should be PARTIALLY MET, not MET**: The Pydantic model validates structure but not mode values. `VALID_SCENARIO_MODES` is defined in models.py but not used as a validator. Invalid modes are accepted silently.
