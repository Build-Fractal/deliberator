# Phase 1 Review: storage-architect

**Spec**: 020-scenario-storage
**Reviewer**: storage-architect
**Date**: 2026-03-24
**Phase**: 1 (Initial Review)

---

## Scope

Evaluate the GameStructure/DataBindings separation, ScenarioStore protocol design, YAML serialization round-trip safety, and RunRecord append-only semantics.

---

## GameStructure / DataBindings Separation

### Design

The three-section model is cleanly implemented:
1. **GameStructure** (reusable): mode, agent_roles, rounds, stagnation, objective_template, parameters, arbiter.
2. **DataBindings** (swappable): target, agent_docs, grounding_doc.
3. **RunRecord** (append-only): timestamp, output_dir, rounds_completed, dispute_count, termination_reason, target, equilibrium_score.

The top-level `Scenario` composes all three plus metadata (name, description).

### Analysis

1. **Clean boundary**: GameStructure contains no file paths or data references. DataBindings is purely about paths. This separation is well-executed. Replaying a scenario with different data means constructing new DataBindings while reusing the GameStructure.

2. **AgentRole is minimal**: `name`, `prompt`, `role`. The prompt is part of the game structure (perspective skeleton), not data. This is correct -- the prompt defines HOW the agent reasons, not WHAT it reasons about.

3. **ArbiterSpec correctly separated**: The arbiter's behavioral config (trigger, prompt) is game structure. The grounding document is in DataBindings. Clean.

4. **Parameters in GameStructure**: `parameters: dict[str, Any]` stores objective function parameter values. This is correctly placed in game structure because parameters define the decision framework, not the data.

**Concern**: The `Scenario` model does not validate mode against a set of allowed values. While `VALID_SCENARIO_MODES` is defined, it's not used as a Pydantic validator on the `GameStructure.mode` field. Invalid modes (e.g., "invalid") would be accepted silently.

**Assessment**: Excellent separation. The only gap is mode validation.

---

## ScenarioStore Protocol (FR-019)

### Design

```python
@runtime_checkable
class ScenarioStore(Protocol):
    def save(self, scenario: Scenario) -> None: ...
    def load(self, name: str) -> Scenario: ...
    def list_scenarios(self) -> list[Scenario]: ...
    def append_run(self, name: str, record: RunRecord) -> Scenario: ...
    def delete(self, name: str) -> None: ...
```

### Analysis

1. **runtime_checkable**: Allows `isinstance()` checks, which is good for debugging and testing. Test `test_protocol_compliance` verifies `FileScenarioStore` satisfies the protocol.

2. **Method signatures**: Clean and minimal. `save`, `load`, `list`, `append_run`, `delete` cover all CRUD operations plus the domain-specific run append.

3. **Return types**: `load` and `append_run` return `Scenario`. `list_scenarios` returns `list[Scenario]`. `save` and `delete` return None. Consistent.

4. **Error model**: `ScenarioNotFoundError` for missing scenarios, `ScenarioValidationError` for invalid data. Clean exception hierarchy.

5. **Extensibility**: The protocol is backend-agnostic. A PostgreSQL or Memgraph implementation would implement the same 5 methods. The `_scenario_to_dict` and `_dict_to_scenario` helpers are implementation-specific (YAML) and correctly live outside the protocol.

**Concern**: The protocol defines `delete` but not `exists`. `FileScenarioStore` has an `exists` method, but it's not part of the protocol. Future backends would need to implement `exists` ad hoc.

**Assessment**: Well-designed protocol. The `exists` omission is minor.

---

## YAML Serialization Round-Trip Safety

### Mechanism

1. `_scenario_to_dict(scenario)` -> `scenario.model_dump(mode="json")` -> plain dict.
2. Dict -> YAML via `yaml.dump(data, default_flow_style=False, sort_keys=False)`.
3. YAML -> dict via `yaml.safe_load()`.
4. Dict -> `Scenario.model_validate(data)` -> validated model.

### Round-Trip Analysis

1. **Pydantic model_dump(mode="json")**: Converts to JSON-serializable types. Datetime becomes ISO string. None stays None. Lists and dicts pass through. This is the key serialization step.

2. **YAML safe_load**: Correctly parses YAML to Python dicts, lists, strings, numbers. Does NOT auto-parse ISO datetime strings -- they remain as strings.

3. **Scenario.model_validate(data)**: Pydantic validates and coerces types. ISO datetime strings are parsed back to datetime objects. This handles the YAML datetime gap.

4. **Test coverage**: `test_scenario_to_dict_round_trip` verifies the full cycle. `test_with_run_history` verifies RunRecord (with datetime) round-trips correctly.

**Concern**: `yaml.dump` with `sort_keys=False` preserves insertion order, which is good for human readability. However, YAML's handling of special characters in strings (colons, brackets) could cause issues with prompt text that contains YAML-significant characters. Pydantic's model_dump handles this correctly (strings are always properly quoted in YAML), but this should be verified with edge-case prompts.

**Assessment**: Round-trip safety is well-handled by the Pydantic-YAML pipeline. The datetime serialization path (model_dump -> ISO string -> YAML -> string -> model_validate -> datetime) works correctly.

---

## RunRecord Append-Only Semantics (FR-016)

### Implementation

`FileScenarioStore.append_run()`:
1. Loads the existing scenario from YAML.
2. Creates a NEW Scenario with the old history + new record: `run_history=[*scenario.run_history, record]`.
3. Saves the updated scenario (overwrites the file).
4. Returns the updated scenario.

### Analysis

1. **Immutability**: The frozen Pydantic model prevents in-place modification. A new Scenario is created on every append. This is correct.

2. **Append-only**: Old records are preserved in the new list. No code path deletes or modifies existing records. The only way to modify history is manual YAML editing (per FR-016's "intentional friction").

3. **Atomicity concern**: The append operation is not atomic. It reads the file, creates a new model, and writes the file. If the process crashes between read and write, no data is lost (the old file is intact). If it crashes during write, the file could be corrupted. YAML files are typically small, so the window is tiny, but a temp-file-then-rename pattern would be safer.

4. **Concurrent append**: Two concurrent appends would race: both read the same file, both create a new model, and the second write overwrites the first (losing the first append). Since conversus is single-process, this is academic, but the protocol design should document this limitation.

**Assessment**: Append-only semantics are correctly implemented via immutable models. Atomicity and concurrency are minor concerns for the file-based backend.

---

## Additional Model Observations

1. **All models frozen**: `model_config = {"frozen": True}` on all Pydantic models. Matches conversus conventions.

2. **Default values**: DataBindings defaults to all-None/empty. RunRecord has sensible defaults (0 rounds, 0 disputes, None for optional fields). GameStructure defaults rounds=1, stagnation="detect".

3. **equilibrium_score in RunRecord**: Optional float. Present when scorer was active, None otherwise. This satisfies SC-005 (graceful handling of presence/absence).

---

## Summary

| Area | Verdict |
|------|---------|
| GameStructure/DataBindings separation | Excellent, clean boundary |
| ScenarioStore protocol | Well-designed, extensible |
| YAML round-trip safety | Correct via Pydantic-YAML pipeline |
| RunRecord append-only | Correct via immutable models |
| Mode validation | Missing (VALID_SCENARIO_MODES not enforced) |
| File atomicity | Minor concern (no temp-file-rename) |
| exists() in protocol | Missing from protocol definition |

### Key Issues

1. **Mode validation not enforced**: `VALID_SCENARIO_MODES` defined but not used as validator.
2. **exists() not in protocol**: Only on FileScenarioStore.
3. **File write not atomic**: Theoretical corruption risk on crash during write.
