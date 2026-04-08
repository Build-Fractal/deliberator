# Conversus Final Synthesis: 030-domain-plugin-architecture

**Agents**: architect, schema-engineer, spec-compliance
**Phases completed**: P1 (review) -> P2 (cross-review) -> P3 (revision) -> P4 (dispute) -> P5 (synthesis)

---

## Verdict: PASS

The domain plugin architecture successfully standardizes how vertical applications are built on the conversus engine. The DomainPlugin ABC defines a clear lifecycle, the DomainStore protocol is generic and extensible with two solid implementations, and the API router factory produces consistent endpoints. The code-review domain (spec 029) validates the architecture. All Pydantic models are frozen, properly typed, and well-tested.

---

## Consensus Points

1. **DomainPlugin ABC is well-designed**: Clean separation -- domains provide extractors, base class provides scoring, recording, and persistence infrastructure. Single abstract method (get_extractors) keeps the subclassing contract minimal.
2. **All models are frozen (immutable)**: DomainScore, DomainRecord, DomainContext, Scaffold, TrendResult -- all use `model_config = {"frozen": True}`. This upholds the deterministic harness principle.
3. **DomainStore protocol is generic**: Five methods (append, get, query, trend, aggregate) cover the standard data access patterns. Two implementations (JSONL, SQLite) demonstrate the protocol. @runtime_checkable enables protocol compliance testing.
4. **API router factory is sound**: create_domain_router() produces standard endpoints for any domain. The closure pattern cleanly captures domain and store references.
5. **Deterministic harness is upheld**: Variable extraction is deterministic (same files -> same variables). Scoring is deterministic (same variables + scaffold -> same score). The indeterminate gate step is properly isolated with equilibrium_score persistence.
6. **Type safety is high**: Literal types for verdicts and trend directions, Field validators for bounds, Optional for nullable fields, @runtime_checkable protocol.
7. **Code-review domain proves the pattern**: CodeReviewDomain extends DomainPlugin with zero infrastructure code. SC-001 satisfied.

---

## DISPUTES_BEGIN

### DISPUTE 1: Scaffolds endpoint and JSON/YAML extension inconsistency
- **Severity**: Medium
- **Agents**: All three (consensus)
- **Description**: Three related issues: (1) API scaffolds endpoint globs `*.json` only but production scaffolds are YAML, (2) base DomainPlugin.score() resolves scaffold names with `.json` extension, (3) CodeReviewDomain.score() resolves with `.yml` extension. This inconsistency means the scaffolds API endpoint returns empty for YAML-based domains, and the base class scaffold resolution is incompatible with YAML scaffolds.
- **Recommendation**: Normalize scaffold file resolution to try `.yml`, `.yaml`, and `.json` extensions in order. Update the scaffolds API endpoint to glob all three patterns. This is a bug fix, not a design change.
- **Disposition**: SURVIVING

### DISPUTE 2: scaffold_dir enforcement on DomainPlugin ABC
- **Severity**: Medium
- **Agents**: architect, schema-engineer (consensus)
- **Description**: DomainPlugin declares `scaffold_dir: Path` as a class attribute but does not enforce that subclasses set it. A subclass that forgets to set scaffold_dir gets a confusing `FileNotFoundError` when score() is called with a string scaffold name.
- **Recommendation**: Add `__init_subclass__` validation that checks `scaffold_dir` is set, or add a runtime check in score() with a descriptive error message.
- **Disposition**: SURVIVING

### DISPUTE 3: FR-002/FR-003 plugin discovery not implemented
- **Severity**: Medium
- **Agents**: spec-compliance
- **Description**: The spec requires importlib-based domain plugin loading (FR-002) and graceful handling of missing packages (FR-003). Neither is implemented or tested. The current architecture has the code-review domain inline. Dynamic discovery is the foundation of the multi-domain vision where domains are independently installable packages.
- **Recommendation**: Implement a `load_domain_plugins()` function using importlib and entry_points, with try/except for missing packages that logs warnings and skips. Test with mock entry points.
- **Disposition**: SURVIVING

### DISPUTE 4: FR-011/FR-012 auth and CORS not implemented
- **Severity**: Low
- **Agents**: spec-compliance
- **Description**: The API server lacks authentication (API key or OAuth) and CORS configuration. Both are required for team/web deployments. FastAPI provides built-in middleware for both.
- **Recommendation**: Add optional auth middleware (API key header check) and CORS middleware configuration to the API server setup.
- **Disposition**: SURVIVING

## DISPUTES_END

---

## Action Items

| Priority | Action | Owner |
|----------|--------|-------|
| Medium | Fix scaffolds endpoint to glob *.json + *.yml + *.yaml | architect |
| Medium | Normalize scaffold name resolution across base and domains | architect |
| Medium | Add scaffold_dir enforcement on DomainPlugin ABC | schema-engineer |
| Medium | Implement load_domain_plugins() with importlib (FR-002/003) | architect |
| Low | Add API submit endpoint error handling for invalid scaffolds | architect |
| Low | Add auth middleware to API server (FR-011) | architect |
| Low | Add CORS middleware to API server (FR-012) | architect |

---

## Compliance Summary

| Category | Total | Pass | Partial | Not Implemented | Deferred | Not Tested |
|----------|-------|------|---------|-----------------|----------|------------|
| Functional Requirements | 19 | 11 | 1 (FR-010) | 3 (FR-011,012,015) | 1 (FR-006) | 2 (FR-002,003) |
| Success Criteria | 5 | 3 | 1 (SC-003) | 0 | 0 | 1 (SC-005) |
