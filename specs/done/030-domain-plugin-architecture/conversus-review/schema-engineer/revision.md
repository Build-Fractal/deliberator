# Phase 3 Revision: schema-engineer

**Spec**: 030-domain-plugin-architecture

---

## Position Changes After Cross-Review

### Modified: Concern A (non-numeric variable handling) -- MAINTAINED at Medium, scope clarified

Both cross-reviewers agree this is genuine. The architect confirms the asymmetry between `_compute_weighted_score()` and `_check_hard_blocks()`. The fix is straightforward: wrap the `float(raw)` call in `_compute_weighted_score()` (line 256) in a try/except, log a warning, and skip the variable. This matches the pattern already established in `_check_hard_blocks()` (lines 309-313).

### Modified: Concern C (zero total weight) -- DOWNGRADED to Low

The architect argues this should be caught at scaffold load time, not at scoring time. The spec-compliance agent also rates it Low. I accept the downgrade. The scorer returning 0.0 for degenerate input is a safe default. The fix belongs in `load_scaffold()` as a validation warning.

### Modified: Concern D (exact threshold boundary) -- DOWNGRADED to Info

The spec-compliance agent rates this Info, arguing the operators are standard mathematical comparisons and the scaffold author explicitly chooses. I accept. The concern is documentation, not code. Moving to Info.

### Surviving: Concern F (silent filter key ignoring) -- MAINTAINED at Medium

No cross-reviewer disputed the severity. The architect adds that `_extract_field_value()` has the same silent failure pattern for unknown field names. This confirms a systemic issue: the query/trend path silently degrades on bad input. The fix: log a warning for unknown filter keys in `_matches_filters()` and unknown field names in `_extract_field_value()`.

### Surviving: Concern B (Record ID as str) -- MAINTAINED at Low

Both reviewers agree Low is appropriate.

### Surviving: Concern E (default weight 1.0 undocumented) -- MAINTAINED at Low

No cross-reviewer disputed.

### Modified: Concern H (workspace path validation) -- DOWNGRADED to Info

The spec-compliance agent explains this is intentional: extractors may handle non-existent workspaces. The API should validate syntactic correctness but not existence. I accept this reasoning and downgrade to Info.

### New: JSON vs YAML extension inconsistency

The architect's Concern I, which I independently confirmed and upgraded in cross-review: `DomainPlugin.score()` hard-codes `.json` extension (line 447) while `load_scaffold()` supports YAML. This contradicts FR-018. I rate this **Medium** and agree with the architect's proposed resolution: search `.yml` first, then `.yaml`, then `.json`.

### New: YAML scaffold loading path untested

From my cross-review of spec-compliance: the YAML branch of `load_scaffold()` is not exercised by any test. The test `test_load_scaffold` creates a `.json` file. If PyYAML is not installed, the YAML path would fail at runtime with no test to catch it. This is a **Medium** test coverage gap.

### New: SQLiteStore check_same_thread=False

From my cross-review of the architect: the `SQLiteStore` uses `check_same_thread=False` for FastAPI compatibility. This is correct for the expected scale but would need a connection pool for high-concurrency production use. Rating: **Info** -- architectural note, not a code fix.
