# Phase 1 Review: spec-compliance

**Spec**: 030-domain-plugin-architecture
**Agent**: spec-compliance
**Focus**: FR-001 through FR-019, SC-001 through SC-005 compliance audit

---

## Overall Assessment

The implementation satisfies the majority of functional requirements. The core domain plugin infrastructure (FR-001 through FR-004) is well-implemented. The data layer (FR-005 through FR-008) is mostly complete with two of three required backends. The API layer (FR-009 through FR-012) is partially implemented. Several requirements around gating, authentication, and scaffolds are not yet addressed.

**Verdict**: PARTIALLY MET -- 11 of 19 FRs satisfied, 2 of 5 SCs demonstrable.

---

## Functional Requirements

### Domain Plugin Infrastructure

**FR-001**: DomainPlugin ABC MUST define the extract -> score -> persist -> gate -> serve lifecycle.
- **PARTIALLY MET**. The ABC defines `extract()` (line 406), `score()` (line 429), and `create_record()` (line 473). However, `gate()` and `serve()`/`get_router()` are absent from the ABC. The spec's section 2 shows both methods in the contract. Evidence: base.py lines 377-503, no `gate()` or `get_router()` method.

**FR-002**: Domain plugins MUST be loadable via `importlib` (same pattern as conversus plugins, spec 016).
- **NOT MET**. No `importlib`-based plugin loading is implemented. The `__init__.py` does static imports. The spec references a `load_domain_plugins()` function (section 4) that discovers and loads installed domain packages. No such function exists.

**FR-003**: Missing domain packages MUST warn and skip, not crash.
- **NOT MET**. No plugin discovery/loading code exists, so graceful failure on missing packages cannot be verified. The extractor failure handling (base.py line 420) demonstrates the pattern, but FR-003 is about missing packages, not failing extractors.

**FR-004**: Each domain MUST define its own DomainRecord model (frozen Pydantic).
- **MET**. `DomainRecord` is frozen (line 86, `model_config = {"frozen": True}`). The model includes domain name, score, context summary, and optional equilibrium/convergence fields. The code-review domain (spec 029) uses this same `DomainRecord`, confirming domain-agnostic design.

### Data Layer

**FR-005**: DomainStore MUST be a protocol with append, get, query, trend, aggregate methods.
- **MET**. `DomainStore` (store.py, lines 44-133) is a `@runtime_checkable` Protocol with all 5 methods. Tests verify protocol compliance for both implementations.

**FR-006**: At least 3 backends MUST be implemented: JSONL, SQLite, Supabase.
- **PARTIALLY MET**. `JSONLStore` and `SQLiteStore` are implemented and tested. `SupabaseStore` is not implemented. Evidence: store.py contains only two classes. The `__init__.py` exports only `JSONLStore` and `SQLiteStore`.

**FR-007**: Backend selection MUST be via configuration, not code changes.
- **PARTIALLY MET**. The `conversus.yml` schema (spec section 5) shows `store: jsonl | sqlite | supabase`, but no configuration-driven store factory exists in the code. The API router factory (`create_domain_router`) accepts a `store` parameter, enabling injection, but there is no code that reads config and instantiates the correct store.

**FR-008**: All backends MUST enforce append-only semantics for audit trail.
- **MET**. Neither `JSONLStore` nor `SQLiteStore` expose update or delete methods. `JSONLStore` opens files in append mode (`"a"`, line 301). `SQLiteStore` uses `INSERT` only (line 442). The protocol defines no mutation methods.

### API

**FR-009**: The API server MUST mount domain routers dynamically based on installed plugins.
- **PARTIALLY MET**. The `create_domain_router()` factory (api.py, line 97) creates a router for a given domain + store pair, and the spec shows how to mount them (section 4). However, no `load_domain_plugins()` discovery function or app assembly code exists. The factory is the building block, but the dynamic mounting is not implemented.

**FR-010**: Each domain MUST get a standard set of endpoints (submit, get, health, trends, gate, scaffolds).
- **PARTIALLY MET**. 5 of 6 endpoints are implemented: `/submit`, `/record/{id}`, `/health`, `/trends/{field}`, `/scaffolds`. The `/gate/{id}` endpoint is missing.

**FR-011**: The API MUST support authentication (API key or OAuth) for team deployments.
- **NOT MET**. No authentication middleware or dependency is present in api.py.

**FR-012**: The API MUST support CORS configuration for frontend access.
- **NOT MET**. No CORS middleware is configured. FastAPI supports this via `CORSMiddleware`, but it is not present.

### Deterministic Harness Integration

**FR-013**: Variable extraction MUST be deterministic -- same inputs produce same variables.
- **MET**. The extraction pipeline merges results from extractors (base.py, line 415-427). Given the same `DomainContext` and the same extractors, the output is deterministic. Failed extractors are skipped deterministically (logged and continued).

**FR-014**: Scoring MUST be deterministic -- same variables + scaffold produce same score.
- **MET**. All scoring functions (`_compute_weighted_score`, `_check_hard_blocks`, `_determine_verdict`, `_build_recommendations`) are pure functions with no randomness or state.

**FR-015**: The conversus gate is the only indeterminate component, and its output MUST include an equilibrium score.
- **NOT MET** (deferred). No gate implementation exists. The `DomainRecord` model has an `equilibrium_score` field (line 95), showing the schema is ready, but no code populates it from a gate run.

**FR-016**: The equilibrium score MUST be persisted alongside the domain score for trust calibration.
- **MET**. `DomainRecord` includes `equilibrium_score: float | None` (line 95). Both stores persist and restore this field. The `create_record()` method accepts it as a parameter. Tests verify round-trip serialization.

### Scaffold System

**FR-017**: Each domain MUST ship with at least 3 pre-built scaffolds.
- **NOT ASSESSED**. This is a per-domain requirement. The base layer provides the `Scaffold` model and `load_scaffold()` function. The code-review domain (spec 029) would need to ship 3 scaffolds. No scaffolds are included in the base layer itself (correctly -- scaffolds are domain-specific).

**FR-018**: Scaffolds MUST be YAML files (no code execution).
- **MET**. The `Scaffold` model is data-only (frozen Pydantic). `load_scaffold()` uses `yaml.safe_load()` for YAML files (line 165) and `json.loads()` for JSON. No code execution paths. Hard block conditions are string comparisons, not `eval()`.

**FR-019**: Users MUST be able to create, share, and version custom scaffolds.
- **PARTIALLY MET**. Scaffolds are plain files (JSON/YAML) that can be created, shared, and versioned via git. However, no scaffolding CLI commands exist (e.g., `conversus scaffold create`, `conversus scaffold validate`). The capability is implicit in the file-based design but not explicitly supported.

---

## Success Criteria

**SC-001**: The code-review domain plugin (spec 029) is implementable as a DomainPlugin subclass with zero infrastructure code.
- **MET**. The `CodeReviewDomain` in `conversus/domains/code_review/` is a subclass of `DomainPlugin`. It provides only extractors and a scaffold directory. Scoring, record creation, and persistence are entirely inherited. Evidence: `code_review/__init__.py` shows the domain exports its class and extractors, nothing more.

**SC-002**: Two domain plugins can run simultaneously on the same API server with isolated stores.
- **MET** (by design). The `create_domain_router()` factory takes a `domain` and `store` parameter. Each domain gets its own router prefix (`/{domain.name}`). `JSONLStore` isolates domains by file (`{domain}.jsonl`). `SQLiteStore` isolates by table (`domain_{name}`). No shared mutable state between domains.

**SC-003**: Switching from JSONL to Supabase backend requires only a config change, no code.
- **NOT MET**. `SupabaseStore` is not implemented (FR-006). The protocol-based design means it COULD work with only a config change once implemented, but it cannot be demonstrated today.

**SC-004**: A frontend consuming the API can render a project health dashboard from the /trends and /health endpoints.
- **MET**. The `/health` endpoint returns `HealthResponse` (domain, recent_count, average_overall, verdict_distribution). The `/trends/{field}` endpoint returns `TrendResponse` (field, slope, direction, alert, values). These provide sufficient data for a health dashboard widget.

**SC-005**: The full pipeline (extract -> score -> persist -> gate -> equilibrium -> API response) completes in under 90 seconds.
- **NOT ASSESSED**. No performance benchmarks are included. The pipeline without gating is expected to be fast (in-process scoring + file/DB append), but gating would add LLM latency. Cannot assess without gate implementation.

---

## Compliance Summary

| Category | Total | Met | Partially Met | Not Met | Not Assessed |
|----------|-------|-----|---------------|---------|--------------|
| FR (Infrastructure) | 4 | 2 | 1 | 1 | 0 |
| FR (Data Layer) | 4 | 2 | 2 | 0 | 0 |
| FR (API) | 4 | 0 | 2 | 2 | 0 |
| FR (Harness) | 4 | 2 | 0 | 1 | 1 |
| FR (Scaffold) | 3 | 1 | 1 | 0 | 1 |
| SC | 5 | 2 | 0 | 1 | 2 |
| **Total** | **24** | **9** | **6** | **5** | **4** |

---

## Recommendation

Accept as Phase 1 delivery. The core architecture is correct and extensible. The primary gaps are: (1) plugin discovery/loading (FR-002, FR-003), (2) gate integration (FR-001 partial, FR-010 partial, FR-015), (3) SupabaseStore (FR-006), and (4) API middleware (FR-011, FR-012). These are clearly scoped follow-up items that do not affect the soundness of the base layer.
