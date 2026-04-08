# Spec Compliance Review: 015 Feature Extraction Pipeline

**Reviewer**: spec-compliance
**Spec**: 015-feature-extraction
**Date**: 2026-03-24

---

## Executive Summary

Spec 015 defines 16 functional requirements (FR-001 through FR-016) and 5 success criteria (SC-001 through SC-005). The implementation in `conversus/schemas/extraction.py` and `conversus/schemas/features.py` satisfies the core requirements with notable strength in determinism (FR-001), structural parsing (FR-002), graceful degradation (FR-003), and multi-round support (FR-004). However, several requirements are only partially met: the package structure diverges from FR-014's `conversus-features` naming, the CLI entry point required by FR-012 does not exist, the per-mode YAML feature schema files required by FR-005 are absent, and two declared feature fields (territory_claim_vector, confirmed_count) are not populated by extraction logic despite being defined in the spec. All five success criteria are achievable with the current implementation, with SC-005 being the most ambiguous due to packaging questions.

---

## Functional Requirement Compliance

### FR-001: Deterministic extraction — MET

**Evidence**: `extract_features()` uses no randomness and makes no LLM calls. All regex patterns are compiled constants. File reading is deterministic (UTF-8 encoding specified). `_discover_agent_names()` uses `sorted()` on directory iteration to ensure consistent ordering. `write_features()` uses `sort_keys=True` for deterministic JSON output. Test `test_sc002_same_input_same_output` confirms byte-identical output across runs.

### FR-002: Structural parsing of conversus output format — MET

**Evidence**: The module defines 25+ compiled regex patterns targeting structural markers (`DISPUTES_BEGIN/END`), heading patterns (`### Remaining Disputes`), and disposition labels (`Withdrawn`, `Modified`, `Surviving`). The `_count_disputes_from_synthesis()` function implements the primary marker-based approach with heading-based fallback, exactly matching the spec's description. All four mode extractors use structured parsing exclusively.

### FR-003: Graceful handling of missing phases — MET

**Evidence**: `_read_file()` returns empty string when a file is missing, with a `warnings.warn()` call. All numeric features default to zero (AgentFeatures defaults). Test `test_sc004_missing_disputes_defaults_to_zero` confirms no crash and zero defaults. Missing synthesis, missing revision, and missing review are all handled gracefully in tests.

### FR-004: Multi-round deliberation support — MET

**Evidence**: `_detect_rounds()` detects `round-N/` subdirectories. `extract_features()` iterates over round directories and produces a list of per-round `RoundFeatures`. Round numbers are correctly overridden for multi-round runs (lines 896-903). The `FeatureSet.rounds` list structure enables time-series analysis.

### FR-005: Per-mode YAML feature schemas — NOT MET

**Evidence**: The spec requires "Each mode MUST have a feature schema defined in `schema/features/{mode}.yml`." No such YAML files exist in the repository. Feature schemas are defined exclusively in Pydantic models (`features.py`). While the Pydantic models serve the same validation purpose, the requirement specifically calls for YAML schema files with explicit field names: "feature names, types (scalar, vector, matrix), extraction source (phase, file pattern), and extraction rule (parsing logic reference)." The Pydantic models do not document extraction source or extraction rule metadata.

### FR-006: Pydantic models for validation — MET

**Evidence**: `AgentFeatures`, `RoundFeatures`, and `FeatureSet` are Pydantic BaseModel subclasses with type annotations, defaults, and a model_validator on FeatureSet. All models are frozen. Test `TestFeatureModels` verifies construction, immutability, and validation behavior.

### FR-007: Extensible feature schemas — PARTIALLY MET

**Evidence**: Adding new features is possible by adding fields to the existing models (all fields have defaults, so additions are backward-compatible). However, the flat structure of AgentFeatures (22 fields across all modes) means adding features for a new mode requires modifying a shared model rather than creating a new one. The spec says "new features can be added without breaking existing consumers" -- this is technically met because new fields have defaults, but the god-object design makes extension error-prone (risk of name collisions, growing surface area).

### FR-008: Output format as features.json — MET

**Evidence**: `write_features()` serializes a FeatureSet to JSON with mode, round number, per-agent features, and aggregate features. The function writes to a specified path with `indent=2, sort_keys=True` for deterministic output. The FeatureSet model contains all required fields: mode, rounds (with agent_features, dispute_count, convergence_count).

### FR-009: FeatureSet Pydantic model for plugin validation — MET

**Evidence**: `FeatureSet` is defined in `features.py` and re-exported through `conversus/schemas/__init__.py`. Plugins can import it: `from conversus.schemas import FeatureSet`. The model validates on construction.

### FR-010: Multi-round features as list — MET

**Evidence**: `FeatureSet.rounds: list[RoundFeatures]` directly implements this requirement. Each RoundFeatures has `round_number`, `agent_features`, and aggregate metrics.

### FR-011: Python API — MET

**Evidence**: `extract_features(output_dir: Path, mode: str) -> FeatureSet` is defined and exported. The signature matches the spec exactly (with an additional optional `agent_names` parameter that is backward-compatible).

### FR-012: CLI invocation — NOT MET

**Evidence**: The spec requires `conversus-features extract --output-dir <path> --mode <mode>`. No CLI entry point exists. No `__main__.py` or click/argparse CLI module is defined in the schemas package. No `[project.scripts]` entry in `pyproject.toml` references a `conversus-features` command.

### FR-013: Pre-write validation — PARTIALLY MET

**Evidence**: FeatureSet validates mode on construction (model_validator). AgentFeatures validates types through Pydantic type checking. However, there is no explicit validation step between extraction and writing: `write_features()` serializes without re-validation. A manually-constructed FeatureSet with invalid data could be written without validation if it bypasses the model constructor (e.g., using `model_construct()`).

### FR-014: Package as conversus-features — NOT MET

**Evidence**: The extraction pipeline ships as part of the `conversus.schemas` package within the main conversus project, not as a standalone `conversus-features` pip package. The import path is `from conversus.schemas.extraction import extract_features`, not `from conversus_features import extract_features` as FR-016 specifies. There is no separate `pyproject.toml` for a `conversus-features` package.

### FR-015: Minimal dependencies — MET

**Evidence**: The extraction module imports only `json`, `logging`, `re`, `warnings`, `pathlib`, `typing` (all stdlib), and `pydantic` plus `conversus.schemas.features` (internal). No yaml, numpy, torch, or ML dependencies. `features.py` imports only `pydantic` and `typing`.

### FR-016: Importable by plugins — PARTIALLY MET

**Evidence**: The spec requires `from conversus_features import extract_features, FeatureSet`. The actual import path is `from conversus.schemas import extract_features, FeatureSet` or `from conversus.schemas.extraction import extract_features`. The functionality is importable, but the import path diverges from the spec.

---

## Success Criteria Compliance

### SC-001: Cooperative mode produces valid FeatureSet — MET

**Evidence**: Test `test_sc001_produces_valid_feature_set` confirms that cooperative output produces a FeatureSet with position vectors and concession rates for each agent. Position vectors have length matching recommendation count. Concession rate is correctly calculated as (withdrawn + modified) / total.

### SC-002: Byte-identical features.json — MET

**Evidence**: Tests `test_sc002_same_input_same_output` and `test_sc002_byte_identical_json` both confirm deterministic output. `write_features()` uses `sort_keys=True` and consistent indentation.

### SC-003: Red-blue severity encoding — MET

**Evidence**: Test `test_sc003_severity_vector_encoding` confirms `severity_vector == [4, 3, 2, 1]` for critical/high/medium/low findings.

### SC-004: Missing Phase 4 graceful handling — MET

**Evidence**: Test `test_sc004_missing_disputes_defaults_to_zero` confirms no crash and zero defaults when disputes files are removed. Warning is emitted via `warnings.warn()`.

### SC-005: Clean pip install dependencies — NOT DIRECTLY VERIFIABLE

**Evidence**: The extraction pipeline does not ship as a standalone `conversus-features` package (see FR-014). Within the current package structure, the extraction modules import only pydantic and stdlib, satisfying the spirit of the requirement. A formal SC-005 test would require a standalone package with its own `pyproject.toml` declaring only `pyyaml`, `pydantic`, and `conversus-schemas` as dependencies. Note: the current implementation does not import `pyyaml` at all -- YAML feature schema files (FR-005) are not implemented.

---

## Actionable Recommendations

1. **Create per-mode YAML feature schema files** (Priority: P1)
   - Create `schema/features/cooperative.yml`, `schema/features/winner-take-all.yml`, etc. per FR-005. Include feature names, types, extraction source, and extraction rule references. These serve as human-readable documentation and machine-readable contracts.

2. **Implement CLI entry point** (Priority: P1)
   - Create a `conversus/schemas/cli.py` or `conversus_features/__main__.py` with `conversus-features extract --output-dir <path> --mode <mode>` per FR-012. Add a `[project.scripts]` entry to `pyproject.toml`.

3. **Resolve package naming: conversus.schemas vs. conversus-features** (Priority: P1)
   - FR-014 and FR-016 specify a standalone `conversus-features` package. The current implementation lives in `conversus.schemas`. Either: (a) amend the spec to match the actual namespace, or (b) extract the feature pipeline into a standalone package. Given that `conversus.schemas` already contains game_forms and objectives, option (a) is more pragmatic -- amend FR-014/FR-016 to use the actual `conversus.schemas` namespace.

4. **Implement territory_claim_vector extraction for PD mode** (Priority: P2)
   - The spec defines this feature and the model declares the field, but extraction logic does not populate it. Implement binary territory claims from Phase 1 review section headers.

5. **Implement confirmed_count extraction for red-blue mode** (Priority: P2)
   - Same gap as above: declared in spec and model, not extracted.

6. **Add explicit pre-write validation** (Priority: P2)
   - Add a `FeatureSet.model_validate(feature_set.model_dump())` call in `write_features()` before serialization to satisfy FR-013's "validate before writing" requirement.

7. **Add pyyaml dependency or remove YAML schema reference** (Priority: P3)
   - If FR-005 YAML schemas are implemented, pyyaml will be needed at validation time. If the spec is amended to use Pydantic-only schemas, remove the pyyaml reference from FR-015.
