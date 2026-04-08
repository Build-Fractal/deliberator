# Phase 1 Review: architect

**Spec**: 030-domain-plugin-architecture
**Agent**: architect
**Focus**: DomainPlugin ABC design, generic scoring, store protocol, API router factory, coupling rules

---

## Overall Assessment

The domain plugin base layer is well-architected. It successfully implements the core thesis of spec 030: any real-world problem domain can be formulated as an optimization problem by providing extractors and scaffolds, while scoring, persistence, trend analysis, and API endpoints are fully generic. The separation into `base.py` (models + ABC + scoring), `store.py` (protocol + implementations), and `api.py` (router factory) is clean and follows the spec's coupling rules.

**Verdict**: PASS with medium concerns.

---

## Detailed Findings

### 1. DomainPlugin ABC Design (base.py, lines 377-503) -- WELL DESIGNED

The ABC correctly captures the extract-score-persist lifecycle from spec section 2. Key design strengths:

- `get_extractors()` is the only abstract method -- domains only need to supply extractors. `extract()`, `score()`, and `create_record()` are all generic.
- The `score()` method accepts either a scaffold name (string) or a `Scaffold` object, providing both convenience and testability.
- `create_record()` serializes the context to a summary dict rather than storing the full `DomainContext`, which avoids Path serialization issues.
- Failed extractors are logged and skipped (line 420-426), which is correct resilience behavior for a plugin system.

**Concern A (Medium)**: The spec's `DomainPlugin` contract (section 2) includes `gate()` and `get_router()` methods, but the implementation omits both. The `gate()` method should return `GateResult | None` (default: skip gating). The `get_router()` method should return `APIRouter | None`. Without `gate()`, the spec's step 4 (gate) in the lifecycle is not represented in the ABC. The API router factory in `api.py` exists but is not integrated into the ABC.

**Concern B (Low)**: The `scaffold_dir` attribute is declared on the class but not enforced as abstract. A subclass that forgets to set `scaffold_dir` will get an `AttributeError` at score time, not at instantiation time. Consider adding a `__init_subclass__` check or making it a required constructor parameter.

### 2. Generic Scoring (base.py, lines 207-369) -- CORRECT

The scoring pipeline is a clean chain of pure functions:

1. `_compute_weighted_score()` -- weighted average with [0,1] clamping. Handles missing variables by skipping them (correct behavior for optional dimensions).
2. `_check_hard_blocks()` -- string-based condition evaluation with 5 operators. Missing variables are skipped (safe default).
3. `_determine_verdict()` -- hard blocks override everything, then thresholds trigger "revise", else "pass".
4. `_build_recommendations()` -- sorted by impact (weight * gap), descending.

The composition in `DomainPlugin.score()` (lines 429-471) correctly chains these functions.

**Concern C (Medium)**: `_check_hard_blocks()` uses string-based condition parsing (`"variable_name < threshold"`). This is fine for scaffold files authored by humans, but there is no validation that scaffold hard block strings are syntactically valid at scaffold load time. A typo like `"safety <0.2"` (missing space) silently produces no hard block because `split()` returns 2 parts instead of 3. The `load_scaffold()` function should validate hard block syntax.

**Concern D (Low)**: `_compute_weighted_score()` silently ignores variables that are missing from the weights dict. If a scaffold declares weights for dimensions that no extractor produces, the overall score will be based on a subset of the intended dimensions. This is acceptable for optional dimensions but could mask configuration errors.

### 3. DomainStore Protocol (store.py, lines 44-133) -- CLEAN

The protocol is well-defined with 5 methods: `append`, `get`, `query`, `trend`, `aggregate`. The `@runtime_checkable` decorator enables `isinstance` checks, which the test suite correctly exercises.

**Concern E (Medium)**: The `get()` method on both `JSONLStore` and `SQLiteStore` searches ALL domain files/tables to find a record by ID. For `JSONLStore`, this means scanning every `.jsonl` file in the store directory. For `SQLiteStore`, it queries every `domain_*` table. This is O(domains * records) per get. In the common case where the caller knows the domain, this is wasteful. The protocol should either accept an optional `domain` parameter in `get()`, or the store should maintain an ID-to-domain index.

**Concern F (Low)**: `JSONLStore._read_all()` reads the entire file into memory. For <10K records (as documented), this is fine. But the docstring's scalability note should be on the class-level docstring, not just the module docstring, so consumers see it.

### 4. API Router Factory (api.py, lines 97-225) -- REUSABLE

The `create_domain_router()` factory cleanly encapsulates the closure pattern: `domain` and `store` are captured by the endpoint functions. Each domain gets 5 endpoints (submit, record, health, trends, scaffolds).

**Concern G (Medium)**: The spec requires 6 standard endpoints per domain (section 4): submit, get, health, trends, **gate**, scaffolds. The implementation has 5 -- the `/gate/{id}` endpoint is missing. This is the same gap as Concern A: the gate lifecycle step is not implemented.

**Concern H (Low)**: The `/submit` endpoint runs extraction synchronously. For domains with expensive extractors (e.g., running coverage tools, security scanners), this could time out. The spec does not require async, but the architecture should document that long-running extractions may need a job queue.

### 5. Coupling Rules (all files) -- ENFORCED

All three modules (`base.py`, `store.py`, `api.py`) correctly avoid importing from `engine/`, `linter/`, `web/`, or `mcp_server`. Each file has an explicit docstring documenting this constraint. The `__init__.py` only re-exports from `base` and `store`.

`store.py` imports `_linear_slope` from `base.py` (a private function). This is acceptable since both are in the same package, but a cleaner approach would be to extract `_linear_slope` into a `conversus.domains.utils` module.

### 6. Scaffold System (base.py, lines 126-171) -- ADEQUATE

The `Scaffold` model is frozen Pydantic with weights, thresholds, and hard blocks. The `load_scaffold()` function supports both JSON and YAML (lazy import of PyYAML).

**Concern I (Low)**: The `load_scaffold()` function only looks for `.yml`, `.yaml`, and `.json` extensions. The spec says scaffolds are YAML files (FR-018), but `DomainPlugin.score()` constructs scaffold paths with `.json` extension only (line 447). There is an inconsistency: the loader supports YAML but the score method hard-codes JSON. Domains that ship YAML scaffolds would need to override `score()`.

---

## Summary of Concerns

| # | Severity | Item |
|---|----------|------|
| A | Medium | `gate()` and `get_router()` missing from ABC; spec lifecycle step 4 not represented |
| B | Low | `scaffold_dir` not enforced at subclass instantiation |
| C | Medium | Hard block condition strings not validated at scaffold load time |
| E | Medium | `get()` searches all domains; O(domains * records) per lookup |
| G | Medium | `/gate/{id}` API endpoint missing; spec requires 6 endpoints |
| D | Low | Missing-from-scaffold variables silently ignored |
| F | Low | Scalability note not on class docstring |
| H | Low | Synchronous extraction in API could timeout |
| I | Low | `score()` hard-codes `.json` extension; `load_scaffold()` supports YAML |

---

## Recommendation

Accept with follow-up. The architecture is sound and the generic scoring pipeline is correct. The missing gate integration (Concerns A, G) should be addressed as a near-term follow-up since it is a core lifecycle step in the spec. The hard block validation (Concern C) should be added to prevent silent scaffold misconfiguration.
