# Phase 4 Disputes: schema-engineer

**Spec**: 030-domain-plugin-architecture

---

## Surviving Disputes

### DISPUTE 1: Gate lifecycle step absent (High)

**Status**: Surviving -- all three agents reached consensus.

I concur with the architect and spec-compliance agent. The gate is the architectural centerpiece. The DomainPlugin ABC lacks `gate()`, and the API router lacks `/gate/{id}`. The dependency injection pattern for resolving the engine coupling tension should be documented.

### DISPUTE 2: Plugin discovery not implemented (Medium)

**Status**: Surviving -- consensus across all agents.

I concur. The absence of `importlib`-based loading means domains cannot be discovered at runtime. This blocks the "install a package, it appears in the API" workflow described in spec section 5.

### DISPUTE 3: score() hard-codes .json extension (Medium)

**Status**: Surviving -- consensus across all agents.

I upgraded this from the architect's original Low to Medium in my cross-review, and all agents now agree. The contradiction with FR-018 is clear: the spec says YAML, the code says JSON.

### DISPUTE 4: Hard block validation and non-numeric variable handling (Medium)

**Status**: Surviving -- I identified the non-numeric gap (Concern A), the architect identified the hard block validation gap (Concern C). Both are facets of the same issue: the scoring path has silent failure modes.

From a schema perspective, the fix requires two changes:
1. `_compute_weighted_score()`: Wrap `float(raw)` in try/except, log warning, skip variable (matching the pattern in `_check_hard_blocks()`).
2. `load_scaffold()`: Validate hard block syntax before returning the Scaffold instance.

### DISPUTE 5: Silent failure in query/trend path (Medium)

**Status**: Surviving -- I identified this (Concern F), the architect confirmed in cross-review, spec-compliance did not dispute.

Unknown filter keys in `_matches_filters()` and unknown field names in `_extract_field_value()` produce silent degradation. A typo in a filter key returns all records. A typo in a trend field returns an empty trend. Neither produces a warning.

**Recommended resolution**: Add `logger.warning()` calls for unknown filter keys and unknown field names. Do not raise exceptions (backward compatibility), but log so users can diagnose issues.

## Withdrawn Disputes

- **Zero total weight edge case**: Downgraded to Low after architect and spec-compliance cross-reviews. Belongs in scaffold validation.
- **Exact threshold boundary behavior**: Downgraded to Info. Standard math operators, documentation concern only.
- **Workspace path validation**: Downgraded to Info. Intentional design -- extractors handle non-existent paths.
- **Record ID as str not UUID**: Maintained Low, not a dispute.

## Non-Disputed Observations (for synthesis)

- YAML scaffold loading branch has no test coverage. Should be addressed with a test that creates a `.yml` file and loads it.
- `DomainScore.variables` dict is mutable despite frozen model config -- known Pydantic limitation, not fixable without custom types.
- `SQLiteStore` uses `check_same_thread=False` -- correct for FastAPI but would need connection pooling at scale.
- Default weight of 1.0 for dimensions in thresholds but not in weights -- undocumented but reasonable default.
