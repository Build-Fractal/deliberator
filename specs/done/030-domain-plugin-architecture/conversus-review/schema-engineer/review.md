# Phase 1 Review: schema-engineer

**Spec**: 030-domain-plugin-architecture
**Agent**: schema-engineer
**Focus**: Pydantic model correctness, type safety, edge cases, store query robustness, API models

---

## Overall Assessment

The Pydantic models are well-crafted. All state models are frozen, field constraints are appropriate, and the type flow from extraction through scoring to persistence is clean. The test suite covers the main paths and several edge cases. There are some gaps in edge case handling for scoring and query filtering that should be addressed.

**Verdict**: PASS with minor concerns.

---

## Detailed Findings

### 1. Frozen Models -- ALL CORRECT

All five state models correctly use `model_config = {"frozen": True}`:

- `DomainContext` (line 41) -- frozen, Path workspace + list[Path] changed_files
- `DomainScore` (line 63) -- frozen, with `ge=0.0, le=1.0` constraint on `overall`
- `DomainRecord` (line 86) -- frozen, auto-generated UUID + UTC timestamp
- `TrendResult` (line 116) -- frozen, with direction as `Literal["improving", "declining", "stable"]`
- `Scaffold` (line 135) -- frozen, weights/thresholds/hard_blocks

The test suite verifies immutability for `DomainScore`, `DomainRecord`, `DomainContext`, `TrendResult`, and `Scaffold` -- comprehensive.

### 2. Type Safety in Extract-Score-Persist Flow -- GOOD WITH GAPS

The type flow:
```
DomainContext -> dict[str, Any] (extract) -> DomainScore (score) -> DomainRecord (create_record) -> str (store.append)
```

**Concern A (Medium)**: The `extract()` method returns `dict[str, Any]`, which means the scoring functions must handle arbitrary types. `_compute_weighted_score()` calls `float(raw)` on each variable (line 256), which will raise `TypeError` for non-numeric values (e.g., if an extractor returns a string). The catch-all in `DomainPlugin.extract()` only protects individual extractor failures; it does not protect against extractors returning non-numeric values for dimensions that the scaffold expects to be numeric.

**Mitigation**: `_check_hard_blocks()` wraps `float()` in a try/except (lines 309-313), but `_compute_weighted_score()` does not. A `ValueError` from `float("not_a_number")` would propagate to the caller.

**Concern B (Low)**: `DomainRecord.id` uses `str(uuid.uuid4())` as a default factory. This is correct but means the ID field accepts any string, not just UUIDs. The `store.get()` method does string comparison, so this works, but a `UUID` type would provide validation.

### 3. Edge Cases in Scoring -- PARTIALLY COVERED

**Covered by tests:**
- All variables missing from weights (test_weighted_score_empty)
- Variables clamped to [0,1] (test_weighted_score_clamps)
- Hard block operators (<, >, <=, >=, ==) (test_hard_blocks_operators)
- Missing variable in hard block condition (test_hard_blocks_missing_variable)
- Empty recommendations (test_recommendations_empty_when_all_pass)

**NOT covered:**

**Concern C (Medium)**: When ALL scaffold weights are zero, `_compute_weighted_score()` returns `(0.0, {})` because `total_weight == 0.0`. This is mathematically correct (no information = 0) but could surprise users. No test covers this.

**Concern D (Medium)**: When a variable value equals a hard block threshold exactly, the behavior depends on the operator. `"safety < 0.2"` with `safety = 0.2` does NOT trigger (correct: 0.2 is not less than 0.2). But the spec says hard blocks are conditions that "force a block verdict" -- users might expect `safety = 0.2` to trigger `"safety < 0.2"`. The distinction between `<` and `<=` is correct but should be documented in the scaffold format specification.

**Concern E (Low)**: `_build_recommendations()` uses `weights.get(dim, 1.0)` as the default weight when computing impact. This means dimensions in thresholds but not in weights get a default weight of 1.0. This is reasonable but undocumented.

### 4. Store Query Filtering -- ADEQUATE BUT RIGID

The filter system supports 3 keys: `verdict`, `min_overall`, `max_overall`. Both `JSONLStore` and `SQLiteStore` implement these identically.

**Concern F (Medium)**: Unknown filter keys are silently ignored. If a caller passes `{"verdikt": "pass"}` (typo), the filter returns all records with no error or warning. This violates the principle of least astonishment. The `_matches_filters()` function should either warn on unknown keys or raise.

**Concern G (Low)**: The `query()` method signature uses `filters: dict[str, Any] | None = None`, but the protocol signature uses `filters: dict[str, Any]` without the `| None`. The `JSONLStore` and `SQLiteStore` implementations accept `None` but the protocol does not declare it. The protocol should be updated to match the implementations.

Wait -- actually checking the protocol (store.py line 74-77), the signature is:
```python
def query(self, domain: str, filters: dict[str, Any] | None = None, limit: int = 100) -> list[DomainRecord]:
```
This is correct. Withdrawing Concern G.

### 5. API Request/Response Models (api.py) -- COMPLETE

The models are well-defined:
- `SubmitRequest` includes workspace, changed_files, metadata, scaffold, and optional equilibrium/convergence
- `SubmitResponse` includes record_id, verdict, overall, hard_blocks, recommendations, dimensions
- `HealthResponse` includes domain, recent_count, average_overall, verdict_distribution
- `TrendResponse` includes field, slope, direction, alert, values
- `ScaffoldInfo` includes name, description, dimensions, hard_block_count

**Concern H (Low)**: `SubmitRequest.workspace` is `str` rather than `Path`. This is correct for JSON serialization, but the endpoint converts it with `Path(request.workspace)` without validation. An empty string or non-existent path would create a `DomainContext` with an invalid workspace. The `DomainContext` model does not validate that the workspace exists (nor should it -- extractors handle that), but the API should validate the input.

### 6. Serialization Round-Trip (store.py) -- CORRECT

The `_record_to_dict()` / `_dict_to_record()` pair correctly handles:
- Timestamp serialization (`.isoformat()`) and deserialization (`datetime.fromisoformat()`)
- Timezone-naive timestamps are promoted to UTC (lines 162-163)
- Nested `DomainScore` is serialized via `model_dump()` and deserialized via `DomainScore(**data)`

The test `test_serialization_roundtrip` verifies this path. One gap: the round-trip test does not include `convergence` -- only `equilibrium_score`. This is a minor test gap; the serialization code handles both fields identically.

---

## Summary of Concerns

| # | Severity | Item |
|---|----------|------|
| A | Medium | `_compute_weighted_score()` raises on non-numeric variable values; no try/except |
| C | Medium | Zero total weight edge case untested |
| D | Medium | Exact threshold boundary behavior undocumented for scaffold authors |
| F | Medium | Unknown filter keys silently ignored; typos produce wrong results |
| B | Low | Record ID accepts any string, not validated as UUID |
| E | Low | Default weight of 1.0 for dimensions in thresholds but not weights undocumented |
| H | Low | API does not validate workspace path before creating DomainContext |

---

## Recommendation

Accept. The model design is solid and the type flow is clean. Concern A (non-numeric variable handling) should be addressed with a try/except in `_compute_weighted_score()` for robustness. Concern F (silent filter key ignoring) should emit a warning. The boundary behavior documentation (Concern D) belongs in the scaffold format docs, not necessarily in code.
