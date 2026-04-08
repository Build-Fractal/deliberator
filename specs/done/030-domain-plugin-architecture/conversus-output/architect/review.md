# Phase 1 Review: architect

**Spec**: 030-domain-plugin-architecture
**Agent**: architect
**Focus**: DomainPlugin ABC design, scoring generality, Store protocol, API router factory

---

## Overall Assessment

The domain plugin architecture is well-designed and achieves its primary goal: standardizing how vertical applications are built on the conversus engine. The DomainPlugin ABC defines a clear lifecycle (extract -> score -> persist -> gate -> serve), the DomainStore protocol is generic and extensible, and the API router factory produces consistent endpoints for any domain. The code-review domain (spec 029) validates the architecture.

**Verdict**: PASS with design observations.

---

## Detailed Findings

### 1. DomainPlugin ABC (base.py, lines 377-503) -- WELL-DESIGNED

The ABC requires subclasses to implement only `get_extractors()`. The base class provides:
- `extract()` -- runs all extractors and merges results, handling failures gracefully
- `score()` -- generic weighted scoring from variables + scaffold
- `create_record()` -- DomainRecord construction with context serialization

This is a clean separation: domains provide **what** to extract, the base class provides **how** to score. The scoring is generic -- it works for any domain given variables and a scaffold.

**Design note**: The `scaffold_dir` attribute on DomainPlugin is declared but not initialized in the ABC. Subclasses must set it, but there's no `__init_subclass__` or `__init__` enforcement. If a subclass forgets to set `scaffold_dir`, `score()` with a string scaffold name will fail with a confusing error. Consider adding a class-level check or making `scaffold_dir` abstract.

### 2. Scoring Generality -- GOOD

The scoring functions in base.py are pure and domain-agnostic:
- `_compute_weighted_score()` -- weighted average with clamping
- `_check_hard_blocks()` -- evaluates condition strings against variables
- `_determine_verdict()` -- block > revise > pass logic
- `_build_recommendations()` -- ordered by impact (weight * gap)

These functions work for any domain's variables and scaffold. The code-review domain uses a more specialized scorer (in domain.py) with dimension-aware normalization, but the base scoring is available for simpler domains.

**Observation**: There's a dual scoring path -- base.py has generic scoring and CodeReviewDomain has specialized scoring. This is intentional (domains can override `score()`), but the base scoring in DomainPlugin.score() uses different hard block parsing than CodeReviewDomain.score(). The base uses `_check_hard_blocks()` which requires 3-part conditions (`"var op threshold"`), while CodeReviewDomain uses `_evaluate_hard_block()` which also supports bare variable names as truthy checks. This inconsistency could confuse future domain authors.

### 3. DomainStore Protocol (store.py) -- CLEAN

The protocol defines five methods: append, get, query, trend, aggregate. Both JSONLStore and SQLiteStore implement all five. The protocol is @runtime_checkable, which enables isinstance checks in tests.

**Design note**: The `query()` signature accepts `filters: dict[str, Any] | None` with three supported filter keys (verdict, min_overall, max_overall). This is a basic filtering mechanism. For more complex queries, domain-specific stores may need to extend beyond the protocol. The current design is appropriate for the first iteration.

### 4. JSONLStore (store.py) -- SOLID

Append-only with fcntl file locking. One JSONL file per domain. Thread-safe writes. Query via line-by-line scan (suitable for < 10K records per domain as documented).

**Performance note**: `get()` scans ALL domain files to find a record by ID. For multi-domain deployments, this is O(domains * records). Consider adding a secondary index (ID -> domain mapping) for efficient lookups. This is a known limitation for the JSONL backend.

### 5. SQLiteStore (store.py) -- SOLID

One table per domain with indexed columns. WAL mode for concurrent reads. SQL-based filtering for common queries with Python fallback for general cases.

**Security note**: Table names are derived from domain names via character substitution. The bracket-quoted `[{table}]` SQL syntax protects against injection. Column names in WHERE clauses use parameterized queries. This is safe.

### 6. API Router Factory (api.py) -- WELL-DESIGNED

The `create_domain_router()` function takes a DomainPlugin and DomainStore and produces a FastAPI APIRouter with standard endpoints (submit, record/{id}, health, trends/{field}, scaffolds). The closure pattern captures domain and store references cleanly.

**Observation**: The scaffolds endpoint (line 208) globs `*.json` files. The code-review domain uses `*.yml` scaffold files. This means the API scaffolds endpoint would return empty for the code-review domain unless JSON scaffolds also exist. The `load_scaffold()` function in base.py handles both YAML and JSON, but the glob pattern in the API only looks for JSON.

This is a **bug**: the scaffolds endpoint should glob `*.json`, `*.yml`, and `*.yaml`.

### 7. Deterministic Harness Integration

The spec describes the deterministic harness (section 3) as the core architectural insight. The implementation supports this:
- Variable extraction is deterministic (same tool output -> same variables)
- Scoring is deterministic (same variables + scaffold -> same score)
- DomainRecord includes equilibrium_score and convergence fields for the indeterminate part

The equilibrium_score field persisted alongside domain scores (FR-016) enables trust calibration.

---

## Concerns

| # | Severity | Item |
|---|----------|------|
| 1 | Medium | API scaffolds endpoint globs *.json but scaffolds may be *.yml |
| 2 | Low | scaffold_dir not enforced on ABC -- confusing error if not set |
| 3 | Low | Dual scoring paths (base vs CodeReview) with different hard block parsing |
| 4 | Low | JSONLStore.get() scans all domain files (O(domains * records)) |
| 5 | Info | DomainStore protocol filter keys are limited |

---

## Recommendation

Accept. The architecture is sound and extensible. The scaffolds endpoint glob pattern bug (Concern #1) should be fixed promptly. The other concerns are design observations for iterative improvement.
