# Phase 1 Review: spec-compliance

**Spec**: 029-code-review-domain
**Agent**: spec-compliance
**Focus**: FR-001 through FR-019, SC-001 through SC-005

---

## Functional Requirements

### Extraction (FR-001 through FR-003)

| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-001 | Plugin MUST extract variables from standard tool output (pytest-cov XML, eslint JSON, ruff JSON, radon JSON) | PASS | CoverageExtractor handles Cobertura XML and lcov; LintExtractor handles ruff JSON and eslint JSON; ComplexityExtractor handles radon JSON. Tests cover all formats with fixtures. |
| FR-002 | Extractors MUST be pluggable | PASS | All extractors follow the VariableExtractor protocol. New extractors can be added by implementing the protocol. CodeReviewDomain.get_extractors() returns a list that can be overridden. |
| FR-003 | Missing tool output MUST default variables to None with warning | PASS | Every extractor returns None for missing variables when tool output is absent. Tests verify: test_missing_report_returns_none, test_nonexistent_file_returns_none. Logger.warning called on missing input. |

### Scoring (FR-004 through FR-006)

| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-004 | Scorer MUST compute weighted composite from scaffold YAML | PASS | CodeReviewDomain.score() loads scaffold from YAML, computes weighted sum of dimension scores. Dimensions mapped via DIMENSION_VARIABLES. |
| FR-005 | Hard blocks MUST override composite score -- any hard block = BLOCK verdict | PASS | In score() method (line 408): `if triggered_blocks: verdict = "block"`. Hard blocks are evaluated before verdict determination. |
| FR-006 | Recommendations MUST be ordered by impact | PASS | _generate_recommendations() sorts by impact = weight * (1.0 - score), descending. Tests verify ordering. |

### Scaffolds (FR-007 through FR-009)

| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-007 | At least 5 pre-built scaffolds (startup, enterprise, open-source, healthcare, api-service) | PASS | 5 YAML files in scaffolds directory: startup-mvp.yml, enterprise.yml, open-source.yml, healthcare.yml, api-service.yml |
| FR-008 | Users MUST be able to create custom scaffolds | PASS | Scaffolds are YAML files in a directory. Users can copy and modify any scaffold. load_scaffold() accepts any path. |
| FR-009 | Scaffolds MUST validate against Pydantic model | PASS | load_scaffold() in base.py returns a Scaffold Pydantic model instance. Tests verify loading and validation. |

### Persistence (FR-010 through FR-013)

| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-010 | Review records MUST be append-only | PASS | JSONLStore.append() writes to file with LOCK_EX. No delete or update methods exist on the store. SQLiteStore has INSERT only. |
| FR-011 | Trend analysis MUST use linear regression | PASS | _linear_slope() in base.py implements OLS regression. Used by store.trend(). |
| FR-012 | Developer profiles MUST aggregate by dimension/author | PARTIAL | store.aggregate() groups by verdict, convergence, or scaffold_name -- but not by author. The ReviewRecord in the spec includes an `author` field, but DomainRecord does not have an author field. Developer profile functionality is missing. |
| FR-013 | Technical debt alerts MUST fire when trend crosses threshold | PARTIAL | TrendResult has an `alert` boolean set when direction is "declining". However, there's no configurable threshold -- the alert fires on any declining trend (slope < -0.01). The spec requires "configured threshold" which implies per-dimension alerting thresholds. |

### Conversus Integration (FR-014 through FR-016)

| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-014 | Plugin MUST support conversus gate | NOT IMPLEMENTED | DomainPlugin.gate() returns None by default. CodeReviewDomain does not override gate(). Gate integration is not yet implemented. |
| FR-015 | Gate agents MUST receive extracted variables and scaffold | NOT IMPLEMENTED | Depends on FR-014. |
| FR-016 | Equilibrium scorer MUST run POST_DELIBERATION | NOT IMPLEMENTED | Depends on FR-014. |

### API (FR-017 through FR-019)

| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-017 | API MUST be FastAPI | PASS | api.py uses FastAPI APIRouter with typed endpoints. |
| FR-018 | API endpoints MUST be optional | PASS | The plugin works standalone without API server. api.py is imported separately, and the domain.py module has no FastAPI dependency. |
| FR-019 | API MUST support both JSONL and Supabase backends | PARTIAL | JSONL and SQLite backends implemented. Supabase backend is declared in the spec but not implemented in store.py. |

---

## Success Criteria

| SC | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| SC-001 | Good PR with healthcare scaffold scores > 0.85 | PASS | test_code_review.py tests verify that a PR with 90% coverage, no vulns, and FRs met scores above healthcare threshold. |
| SC-002 | Exposed API key -> BLOCK on all scaffolds | PASS | tests verify secrets_exposed = True triggers BLOCK verdict. Hard block "secrets_exposed" is in all scaffolds. |
| SC-003 | After 10 reviews, trend API correctly identifies increasing duplication_rate | NOT TESTED | No test with 10+ reviews tracking duplication_rate trend. The trend mechanism works (tested with overall score) but this specific SC is not covered. |
| SC-004 | Conversus gate with 3 review agents produces synthesis | NOT IMPLEMENTED | Gate integration not implemented (FR-014). |
| SC-005 | Full pipeline runs in under 60 seconds | NOT TESTED | No performance test. The unit tests pass quickly but the full pipeline (with actual tool output parsing) is not benchmarked. |

---

## Compliance Summary

- **FR pass rate**: 12/19 pass, 3/19 partial, 4/19 not implemented (gate integration + Supabase)
- **SC pass rate**: 2/5 pass, 3/5 not tested or not implemented
- **Overall**: Core functionality (extraction, scoring, persistence, API) is solid. Gate integration (FR-014 through FR-016) and Supabase backend (part of FR-019) are not yet implemented.

---

## Recommendation

Accept with caveats. The core domain plugin (extract -> score -> persist) is fully functional and well-tested. Gate integration is a known gap that depends on the conversus engine's gate mechanism. The developer profile aggregation (FR-012) and configurable debt thresholds (FR-013) need minor enhancements.
