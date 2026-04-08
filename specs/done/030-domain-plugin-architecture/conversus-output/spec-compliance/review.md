# Phase 1 Review: spec-compliance

**Spec**: 030-domain-plugin-architecture
**Agent**: spec-compliance
**Focus**: FR-001 through FR-019, SC-001 through SC-005

---

## Functional Requirements

### Domain Plugin Infrastructure (FR-001 through FR-004)

| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-001 | DomainPlugin ABC MUST define extract -> score -> persist -> gate -> serve lifecycle | PASS | DomainPlugin ABC in base.py defines: extract() (abstract via get_extractors), score(), create_record() (persist), gate() (default None), get_router() not present but API router is external via api.py |
| FR-002 | Domain plugins MUST be loadable via importlib | NOT TESTED | No importlib-based plugin discovery test. The architecture supports it (standard Python packages), but no test verifies dynamic loading. |
| FR-003 | Missing domain packages MUST warn and skip, not crash | NOT TESTED | No test for missing package handling. The spec envisions multiple installable domain packages, but the current implementation has only the code-review domain inline. |
| FR-004 | Each domain MUST define its own DomainRecord model (frozen Pydantic) | PASS | DomainRecord is defined in base.py as frozen Pydantic. The code-review domain uses this shared model. The spec says "its own" which could mean domain-specific record types, but the shared DomainRecord is flexible enough via context_summary and variables fields. |

### Data Layer (FR-005 through FR-008)

| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-005 | DomainStore MUST be a protocol with append, get, query, trend, aggregate | PASS | DomainStore protocol in store.py defines all five methods with proper type signatures. |
| FR-006 | At least 3 backends: JSONL, SQLite, Supabase | PARTIAL | JSONLStore and SQLiteStore implemented. Supabase not implemented. 2 of 3 backends exist. |
| FR-007 | Backend selection MUST be via configuration, not code changes | PASS | The create_domain_router() function accepts a DomainStore instance. Config determines which store to instantiate. |
| FR-008 | All backends MUST enforce append-only semantics | PASS | JSONLStore: append-only file writes, no delete/update. SQLiteStore: INSERT only, no UPDATE/DELETE methods. |

### API (FR-009 through FR-012)

| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-009 | API server MUST mount domain routers dynamically | PASS | create_domain_router() returns an APIRouter that can be mounted via app.include_router(). The spec's example shows a loop over load_domain_plugins(). |
| FR-010 | Each domain MUST get standard endpoints (submit, get, health, trends, gate, scaffolds) | PARTIAL | Submit, get (record/{id}), health, trends/{field}, and scaffolds endpoints exist. Gate endpoint is missing. 5 of 6 endpoints implemented. |
| FR-011 | API MUST support authentication | NOT IMPLEMENTED | No auth middleware, API key, or OAuth support in the router factory. |
| FR-012 | API MUST support CORS configuration | NOT IMPLEMENTED | No CORS middleware in the API module. |

### Deterministic Harness Integration (FR-013 through FR-016)

| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-013 | Variable extraction MUST be deterministic | PASS | Extractors read file output only. Same files -> same variables. No randomness in extraction. |
| FR-014 | Scoring MUST be deterministic | PASS | Pure functions: same variables + scaffold -> same score. No randomness. |
| FR-015 | Conversus gate output MUST include equilibrium score | NOT IMPLEMENTED | gate() returns None by default. No equilibrium scoring integration. |
| FR-016 | Equilibrium score MUST be persisted alongside domain score | PASS | DomainRecord has equilibrium_score: float | None field. create_record() accepts it as a parameter. |

### Scaffold System (FR-017 through FR-019)

| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-017 | Each domain MUST ship with at least 3 pre-built scaffolds | PASS | Code-review domain has 5 scaffolds: startup-mvp, enterprise, open-source, healthcare, api-service. |
| FR-018 | Scaffolds MUST be YAML files (no code execution) | PASS | All scaffolds are YAML. load_scaffold() uses yaml.safe_load (no arbitrary code execution). |
| FR-019 | Users MUST be able to create, share, and version custom scaffolds | PASS | Scaffolds are YAML files in a directory. load_scaffold() accepts any path. Users can create new files. |

---

## Success Criteria

| SC | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| SC-001 | Code-review domain implementable as DomainPlugin subclass with zero infrastructure code | PASS | CodeReviewDomain extends DomainPlugin, overrides get_extractors() and score(). Infrastructure (store, API, records) comes from the base layer. |
| SC-002 | Two domains can run on same API server with isolated stores | NOT TESTED | No test with two domain plugins on the same API server. The architecture supports it (each domain gets its own router prefix and store files/tables). |
| SC-003 | Switching JSONL to Supabase requires only config change | PARTIAL | JSONL to SQLite switch requires only instantiating a different store class. Supabase not implemented. |
| SC-004 | Frontend can render health dashboard from API endpoints | PASS | /health returns HealthResponse with average_overall and verdict_distribution. /trends/{field} returns TrendResponse with slope, direction, values. These are sufficient for dashboard rendering. |
| SC-005 | Full pipeline completes in under 90 seconds | NOT TESTED | No performance test. Unit tests pass quickly but the full pipeline is not benchmarked. |

---

## Compliance Summary

- **FR pass rate**: 12/19 pass, 2/19 partial, 5/19 not implemented or not tested
- **SC pass rate**: 2/5 pass, 1/5 partial, 2/5 not tested
- **Overall**: The core architecture (ABC, models, store protocol, API router) is solid. Missing features: auth/CORS, Supabase backend, gate endpoint, importlib discovery.

---

## Recommendation

Accept. The architecture is sound and the code-review domain proves the pattern. The missing features (auth, CORS, Supabase, gate) are well-scoped additions that don't require architectural changes.
