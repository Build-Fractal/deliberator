# Conversus Final Synthesis: 030-domain-plugin-architecture

**Agents**: architect, schema-engineer, spec-compliance
**Phases completed**: P1 (review) -> P2 (cross-review) -> P3 (revision) -> P4 (dispute) -> P5 (synthesis)

---

## Verdict: PASS

The domain plugin base layer is architecturally sound. The core premise -- that any domain can be formulated as an optimization problem by providing extractors and scaffolds while inheriting generic scoring, persistence, and API endpoints -- is correctly implemented. The DomainPlugin ABC, DomainStore protocol, and API router factory form a clean, decoupled foundation. All state models are frozen Pydantic. Scoring is deterministic. Coupling rules are enforced. The test suite provides thorough coverage of the implemented surface.

The primary gap is the absent gate lifecycle step, which is the architectural differentiator of conversus. This is a scoped follow-up, not a blocker for the base layer.

---

## Consensus Points

1. **DomainPlugin ABC is well-designed**: The abstract base class correctly captures the extract-score-persist lifecycle. The `get_extractors()` abstraction means domains only supply extractors; all scoring and persistence logic is inherited. Failed extractors are handled gracefully.

2. **Generic scoring is correct**: The weighted composite scoring pipeline (`_compute_weighted_score` -> `_check_hard_blocks` -> `_determine_verdict` -> `_build_recommendations`) is mathematically sound, pure-functional, and domain-agnostic. The test suite verifies all operators, edge cases, and impact-ordered recommendations.

3. **DomainStore protocol is clean**: The `@runtime_checkable` protocol with 5 methods (append, get, query, trend, aggregate) is well-defined. Both `JSONLStore` and `SQLiteStore` implement it correctly. Protocol compliance is verified by tests.

4. **Coupling rules are enforced**: All three modules (`base.py`, `store.py`, `api.py`) import nothing from `engine/`, `linter/`, `web/`, or `mcp_server`. The API layer is optional -- domains work as libraries without FastAPI.

5. **All state models are frozen**: `DomainContext`, `DomainScore`, `DomainRecord`, `TrendResult`, and `Scaffold` all use `model_config = {"frozen": True}`. Tests verify immutability for each.

6. **Section 8 constraints satisfied**: Domain independence, core-to-domain decoupling, optional API, data-only scaffolds, deterministic scoring.

7. **SC-001 and SC-002 pass**: The code-review domain (spec 029) is implementable as a subclass with zero infrastructure code. Two domains can run simultaneously with isolated stores.

---

## DISPUTES_BEGIN

### DISPUTE 1: Gate lifecycle step absent from ABC and API
- **Severity**: High
- **Agents**: All three (consensus)
- **Description**: The `DomainPlugin` ABC does not define `gate()` or `get_router()` methods. The API router factory does not include a `/gate/{id}` endpoint. This means FR-001 (lifecycle definition), FR-010 (standard endpoints), and FR-015 (gate output with equilibrium score) are not met. The gate is the architectural differentiator -- the "deterministic harness around indeterminate AI" described in spec section 3.
- **Architectural tension**: The domains package must not import from `engine/` (coupling rule), but the gate needs the engine. Resolution: dependency injection -- the gate runner is provided by the API server assembly code, not imported by the domains package.
- **Recommendation**: (1) Add `gate()` and `get_router()` as non-abstract default methods returning `None`. (2) Add `/gate/{id}` endpoint to the router factory, accepting an optional gate runner dependency. (3) Document the injection pattern.
- **Disposition**: SURVIVING

### DISPUTE 2: Plugin discovery/loading not implemented
- **Severity**: Medium
- **Agents**: All three (consensus)
- **Description**: No `importlib`-based plugin loading exists. FR-002 (loadable via importlib) and FR-003 (missing packages warn and skip) are NOT MET. The spec's `load_domain_plugins()` function (section 4) and configuration-driven discovery (section 5) are not implemented. Without this, the "install a package, it appears in the API" workflow cannot be realized.
- **Recommendation**: Implement `load_domain_plugins()` using `importlib.metadata.entry_points()`. Handle missing packages with warning + skip. Add config-driven store factory for FR-007.
- **Disposition**: SURVIVING

### DISPUTE 3: score() hard-codes .json extension, contradicting FR-018
- **Severity**: Medium
- **Agents**: All three (consensus)
- **Description**: `DomainPlugin.score()` constructs scaffold paths as `self.scaffold_dir / f"{scaffold}.json"` (base.py line 447). FR-018 says "Scaffolds MUST be YAML files." Domains following the spec would ship YAML scaffolds that the generic `score()` method cannot find.
- **Recommendation**: Change `score()` to search for `{scaffold}.yml`, `.yaml`, then `.json`. The `load_scaffold()` function already supports all three formats.
- **Disposition**: SURVIVING

### DISPUTE 4: Hard block validation + non-numeric variable handling
- **Severity**: Medium
- **Agents**: architect, schema-engineer (consensus); spec-compliance concurs
- **Description**: Two silent failure modes in the scoring path: (1) Malformed hard block strings (e.g., missing space) are silently skipped at scoring time -- no validation in `load_scaffold()`. (2) Non-numeric variable values cause `ValueError` in `_compute_weighted_score()` -- no try/except (unlike `_check_hard_blocks()` which has one).
- **Recommendation**: (1) Add hard block syntax validation in `load_scaffold()`. (2) Add try/except + warning in `_compute_weighted_score()` for non-numeric values, matching the pattern in `_check_hard_blocks()`.
- **Disposition**: SURVIVING

### DISPUTE 5: Silent failure in query/trend path
- **Severity**: Medium
- **Agents**: schema-engineer, architect (consensus); spec-compliance concurs
- **Description**: Unknown filter keys in `_matches_filters()` and unknown field names in `_extract_field_value()` produce silent degradation. A typo in a filter key returns all records (no filtering). A typo in a trend field returns an empty trend. No warnings are logged.
- **Recommendation**: Add `logger.warning()` for unknown filter keys and unknown field names. Do not raise (backward compatibility), but log for diagnostics.
- **Disposition**: SURVIVING

## DISPUTES_END

---

## Action Items

| Priority | Action | Owner | FRs Affected |
|----------|--------|-------|--------------|
| High | Add `gate()` and `get_router()` to ABC; add `/gate/{id}` endpoint with injectable gate runner | architect | FR-001, FR-010, FR-015 |
| Medium | Implement `load_domain_plugins()` via importlib entry_points | architect | FR-002, FR-003, FR-009 |
| Medium | Fix `score()` to search .yml/.yaml/.json in order | schema-engineer | FR-018 |
| Medium | Validate hard block syntax in `load_scaffold()` | schema-engineer | Robustness |
| Medium | Add try/except for `float()` in `_compute_weighted_score()` | schema-engineer | Robustness |
| Medium | Add warnings for unknown filter keys and trend fields | schema-engineer | Robustness |
| Medium | Add test for YAML scaffold loading path | schema-engineer | FR-018 test coverage |
| Low | Implement config-driven store factory | architect | FR-007 |
| Low | Implement SupabaseStore | architect | FR-006, SC-003 |
| Low | Add CORS and auth middleware to API | architect | FR-011, FR-012 |
| Low | Add optional `domain` parameter to `store.get()` | architect | Performance |
| Info | Document scaffold format for users | spec-compliance | FR-019 |

---

## Compliance Summary

| Category | Total | Met | Partially Met | Not Met | Not Assessed |
|----------|-------|-----|---------------|---------|--------------|
| FR (Infrastructure) | 4 | 1 | 0 | 3 | 0 |
| FR (Data Layer) | 4 | 2 | 1 | 1 | 0 |
| FR (API) | 4 | 0 | 2 | 2 | 0 |
| FR (Harness) | 4 | 2 | 0 | 1 | 1 |
| FR (Scaffold) | 3 | 1 | 1 | 0 | 1 |
| SC | 5 | 3 | 0 | 1 | 1 |
| **Total** | **24** | **9** | **4** | **8** | **3** |

The 9 MET requirements cover the core architectural foundation: frozen models, deterministic scoring, append-only stores, protocol compliance, decoupled modules, and domain isolation. The 8 NOT MET requirements are clearly scoped follow-up items (gate integration, plugin discovery, SupabaseStore, API middleware) that do not compromise the soundness of the delivered base layer.
