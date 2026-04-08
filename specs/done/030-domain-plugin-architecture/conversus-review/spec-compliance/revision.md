# Phase 3 Revision: spec-compliance

**Spec**: 030-domain-plugin-architecture

---

## Position Changes After Cross-Review

### Modified: FR-001 -- RECONSIDERED to NOT MET

The schema-engineer argues FR-001 should be NOT MET rather than PARTIALLY MET. The argument: the requirement says the ABC "MUST define the extract -> score -> persist -> gate -> serve lifecycle." A lifecycle is a sequence, and 2 of 5 steps are absent. I accept this reasoning. Implementing 3 of 5 steps is strong progress, but the lifecycle as a whole is not defined.

**Revised assessment**: NOT MET. The ABC defines extract, score, and persist. Gate and serve are absent.

### Modified: FR-007 -- UPGRADED to NOT MET

The architect argues FR-007 should be NOT MET because "dependency injection readiness is not the same as configuration-driven selection." This is correct. The store is instantiated in code (`JSONLStore(path)` or `SQLiteStore(path)`). No configuration file is read. No factory function maps config values to store types.

**Revised assessment**: NOT MET.

### Modified: FR-019 -- RECONSIDERED, MAINTAINED at PARTIALLY MET

The architect argues FR-019 should be NOT MET because the file-based capability is not exposed or documented. I partially accept: the lack of tooling and documentation is a gap. However, the Scaffold model's fields (name, description, weights, thresholds, hard_blocks) constitute a schema that a knowledgeable user could follow. The JSON serialization format is standard. I maintain PARTIALLY MET -- the capability exists but is not user-facing.

### Surviving: All other FR assessments -- MAINTAINED

- FR-002 (NOT MET), FR-003 (NOT MET), FR-006 (PARTIALLY MET), FR-009 (PARTIALLY MET), FR-010 (PARTIALLY MET), FR-011 (NOT MET), FR-012 (NOT MET), FR-015 (NOT MET): all maintained.
- FR-004, FR-005, FR-008, FR-013, FR-014, FR-016, FR-018: all MET, maintained.

### Surviving: SC assessments -- MAINTAINED

- SC-001 (MET), SC-002 (MET), SC-003 (NOT MET), SC-004 (MET), SC-005 (NOT ASSESSED): all maintained.

### New: Section 8 constraint compliance

From my cross-review of the architect: the section 8 constraints are all satisfied:
- "Domain plugins MUST NOT depend on each other" -- MET. Code-review domain only imports from base layer.
- "The core conversus package MUST NOT depend on any domain plugin" -- MET. `__init__.py` imports only from `base` and `store`.
- "The API server is optional" -- MET. `base.py` and `store.py` have no FastAPI dependency.
- "Scaffolds are data, not code" -- MET. `yaml.safe_load()`, no eval/exec.
- "The deterministic harness is the value proposition -- don't compromise it" -- MET for what is implemented. Scoring is fully deterministic.

### New: Test coverage against FRs

From the schema-engineer's cross-review: the test file covers FR-001 (partial), FR-005, FR-008, FR-013, FR-014, FR-016. Missing coverage for FR-006 (SupabaseStore), FR-010 (gate endpoint), FR-018 (YAML scaffold loading). The YAML scaffold loading gap is notable because it is a tested function (`load_scaffold`) with an untested branch.

### Updated Compliance Summary

| Category | Total | Met | Partially Met | Not Met | Not Assessed |
|----------|-------|-----|---------------|---------|--------------|
| FR (Infrastructure) | 4 | 1 | 0 | 3 | 0 |
| FR (Data Layer) | 4 | 2 | 1 | 1 | 0 |
| FR (API) | 4 | 0 | 2 | 2 | 0 |
| FR (Harness) | 4 | 2 | 0 | 1 | 1 |
| FR (Scaffold) | 3 | 1 | 1 | 0 | 1 |
| SC | 5 | 3 | 0 | 1 | 1 |
| **Total** | **24** | **9** | **4** | **8** | **3** |
