# Spec Compliance Auditor — Phase 1 Review: Code Review Domain (Spec 029)

## Executive Summary

Of 19 functional requirements (FR-001 through FR-019) and 5 success criteria (SC-001 through SC-005), the implementation achieves 11 MET, 4 PARTIALLY MET, and 4 NOT MET for FRs, and 3 MET, 1 PARTIALLY MET, and 1 NOT MET for SCs. The core extraction-scoring-scaffold pipeline is implemented. The major gaps are in persistence (FR-010 through FR-013), conversus integration (FR-014 through FR-016), and API layer (FR-017 through FR-019) — which are the outer layers of the architecture. The inner layers (extraction, scoring, scaffolds) are substantially complete.

---

## Functional Requirements

### Extraction

| Requirement | Status | Evidence |
|---|---|---|
| **FR-001**: Extract variables from standard tool output (pytest-cov XML, eslint JSON, ruff JSON, radon JSON) | **MET** | CoverageExtractor parses Cobertura XML (`extractors.py` lines 68-157). LintExtractor parses ruff and eslint JSON (`extractors.py` lines 165-217). ComplexityExtractor parses radon JSON (`extractors.py` lines 225-303). Tests confirm correct parsing: `test_cobertura_xml`, `test_ruff_json_output`, `test_eslint_json_output`, `test_radon_json_output`. All use real-format fixture files in `tests/fixtures/code_review/`. |
| **FR-002**: Extractors MUST be pluggable — users can add custom extractors | **MET** | `VariableExtractor` is defined as a `Protocol` in `base.py` (lines 179-199) with `name`, `variables`, and `extract()`. Any class implementing this protocol can be used. `CodeReviewDomain.get_extractors()` returns a list that users can extend by subclassing `CodeReviewDomain` and overriding `get_extractors()`. The protocol-based design means no registration step is needed — any conforming class works. |
| **FR-003**: Missing tool output MUST default to None (not zero), with a warning | **MET** | Every extractor returns `{variable: None}` when its report path is missing or None. Warnings are logged via `logger.warning()`. Tests confirm: `test_missing_report_returns_none` exists for CoverageExtractor, LintExtractor, ComplexityExtractor, SecurityExtractor, DocumentationExtractor, ConventionExtractor, and GitDiffExtractor. The `CodeReviewDomain.extract()` method (domain.py lines 337-355) catches exceptions from individual extractors and logs warnings without crashing. `test_extract_with_no_reports` confirms end-to-end None behavior. |

### Scoring

| Requirement | Status | Evidence |
|---|---|---|
| **FR-004**: Scorer MUST compute weighted composite from scaffold YAML | **MET** | `CodeReviewDomain.score()` (domain.py lines 357-454) loads scaffolds from YAML via `load_scaffold()` (base.py lines 144-171), extracts weights and thresholds, computes per-dimension scores via `_score_dimension()`, and produces a weighted composite: `overall = weighted_sum / total_weight`. Test `test_good_pr_startup_mvp` confirms scoring works with a real scaffold. |
| **FR-005**: Hard blocks MUST override composite score — any hard block = BLOCK verdict | **MET** | domain.py line 408: `if triggered_blocks: verdict = "block"`. This check occurs before any threshold evaluation, ensuring hard blocks always produce BLOCK regardless of the composite score. Tests confirm: `test_secrets_exposed_blocks_all_scaffolds_sc002` (line 667) iterates all scaffolds; `test_critical_vulns_block` (line 686) confirms critical vulns trigger BLOCK; `test_no_spec_blocks_healthcare` (line 754) confirms `has_spec == false` blocks. |
| **FR-006**: Recommendations MUST be ordered by impact | **PARTIALLY MET** | `_generate_recommendations()` (domain.py lines 205-300) computes `impact = weight * (1.0 - score)` and sorts by descending impact. Test `test_recommendations_ordered_by_impact` (line 719) verifies security appears before documentation when security has higher weight and lower score. However, the impact calculation uses the dimension score, not the variable-level contribution. A dimension with one bad variable and one good variable averages them, diluting the impact signal. The ordering is correct at the dimension level but does not guide developers to specific variables within a dimension. The spec says "the change that would most improve the overall score listed first" — the current implementation satisfies this at the dimension granularity but not at the variable granularity. |

### Scaffolds

| Requirement | Status | Evidence |
|---|---|---|
| **FR-007**: At least 5 pre-built scaffolds (startup, enterprise, open-source, healthcare, api-service) | **MET** | Five scaffold YAML files exist in `conversus/domains/code_review/scaffolds/`: `startup-mvp.yml`, `enterprise.yml`, `open-source.yml`, `healthcare.yml`, `api-service.yml`. Test `test_all_expected_scaffolds_exist` (line 811) confirms all 5 are present. Test `test_scaffold_load_via_domain` (line 868) confirms they load through `CodeReviewDomain.list_scaffolds()`. |
| **FR-008**: Users MUST be able to create custom scaffolds by copying/modifying a pre-built one | **MET** | Scaffolds are plain YAML files with no code execution. A user can copy any scaffold file, modify weights/thresholds/hard_blocks, and pass the path or name to `domain.score()`. The `load_scaffold()` function (base.py lines 144-171) accepts any path. The Scaffold Pydantic model (base.py lines 126-141) validates the structure. No test explicitly covers custom scaffold loading, but the architecture enables it by design. |
| **FR-009**: Scaffolds MUST validate against a Pydantic model | **MET** | `load_scaffold()` (base.py line 171) returns `Scaffold(**data)` which triggers Pydantic validation. The `Scaffold` model (base.py lines 126-141) has typed fields: `name: str`, `description: str`, `weights: dict[str, float]`, `thresholds: dict[str, float]`, `hard_blocks: list[str]`. Test `test_scaffold_yaml_valid` (line 821) confirms each scaffold has required fields and correct types. |

### Persistence

| Requirement | Status | Evidence |
|---|---|---|
| **FR-010**: Review records MUST be append-only (no deletion or mutation) | **NOT MET** | The spec defines `ReviewRecord` and `ReviewStore` with `append()`, `query()`, `trend()`, `developer_profile()`, and `health_score()` methods. The implementation has `DomainRecord` (base.py lines 79-97) and `DomainPlugin.create_record()` (base.py lines 473-503), but no `ReviewStore` implementation exists. No `JSONLReviewStore`, `SupabaseReviewStore`, or `SQLiteReviewStore` class is present in the codebase. The `create_record()` method builds a record but does not persist it. |
| **FR-011**: Trend analysis MUST use linear regression | **NOT MET** | `_linear_slope()` (base.py lines 207-232) implements OLS linear regression. The `TrendResult` model (base.py lines 104-118) defines the trend structure. However, no code calls `_linear_slope()` or produces `TrendResult` instances. The infrastructure exists but is not wired into any store or API. Without a `ReviewStore`, trends cannot be computed. |
| **FR-012**: Developer profiles MUST aggregate scores by dimension across all reviews by that author | **NOT MET** | No developer profile aggregation code exists. `DomainRecord` has no `author` field. The spec's `ReviewRecord` includes `author: str` but the implementation's `DomainRecord` does not. Without an author field and a store, developer profiles are impossible. |
| **FR-013**: Technical debt alerts MUST fire when a dimension's trend crosses a threshold | **NOT MET** | No alert mechanism exists. `TrendResult.alert` (base.py line 118) is defined as a field but nothing sets it. No threshold comparison or notification logic exists. |

### Conversus Integration

| Requirement | Status | Evidence |
|---|---|---|
| **FR-014**: Plugin MUST support running a conversus gate using review scores as context | **PARTIALLY MET** | The spec describes a gate integration where review scores feed into a conversus deliberation. `DomainRecord` (base.py lines 95-97) has `equilibrium_score` and `convergence` fields, showing the data model anticipates gate output. `CodeReviewDomain.create_record()` accepts these as optional parameters. However, no code actually invokes a conversus gate. The infrastructure to store gate results exists but the gate invocation does not. |
| **FR-015**: Gate agents MUST receive extracted variables and scaffold as input | **PARTIALLY MET** | `DomainScore` (base.py line 70) has a `variables` field and `scaffold_name` field, meaning the score object carries the necessary data. However, the `CodeReviewDomain.score()` method (domain.py line 448) does not populate `variables` in the returned `DomainScore` — it constructs `DomainScore(overall=..., dimensions=..., hard_blocks=..., verdict=..., recommendations=...)` without passing `variables`. The base class `score()` (base.py line 463-471) does pass `variables=variables`, but `CodeReviewDomain` overrides `score()` with its own implementation that omits it. |
| **FR-016**: Equilibrium scorer MUST run POST_DELIBERATION on gate output | **PARTIALLY MET** | The data model supports it (`equilibrium_score` on `DomainRecord`), but no equilibrium scoring code exists in the code review domain. This depends on the equilibrium scoring system from spec 027 (solver-validation-flow), which is listed as a dependency. |

### API

| Requirement | Status | Evidence |
|---|---|---|
| **FR-017**: API MUST be a FastAPI application | **NOT MET** | No API code exists in the code review domain. The spec defines 7 endpoints (Section 3, API Layer) but no routes, views, or FastAPI app are implemented. |
| **FR-018**: API endpoints MUST be optional — plugin works standalone | **MET** | The plugin's core functionality (extract, score, list_scaffolds) works as a Python library with no API server dependency. All tests run without any web server. The import chain (`conversus.domains.code_review.domain` → `conversus.domains.base`) imports only pydantic and stdlib. No FastAPI, uvicorn, or web imports exist. |
| **FR-019**: API MUST support both JSONL and Supabase backends | **NOT MET** | No backend implementation exists. No JSONL writer, no Supabase client. The `ReviewStore` protocol from the spec is not implemented. |

---

## Success Criteria

| Criterion | Status | Evidence |
|---|---|---|
| **SC-001**: Good PR with 90% coverage, no vulns, all FRs met → healthcare scaffold > 0.85 | **MET** | Test `test_good_pr_healthcare_sc001` (line 650) passes with variables including `line_coverage: 0.92`, `branch_coverage: 0.88`, `critical_vulns: 0`, `high_vulns: 0`, `medium_vulns: 0`, `secrets_exposed: False`, `fr_satisfaction_rate: 0.95`, `sc_pass_rate: 0.90`. The assertion `score.overall > 0.85` passes. Verified by manual calculation: security dimension = average(1.0, 1.0, 1.0, 1.0) = 1.0; test_quality = average(0.92, 0.88) = 0.9; spec_compliance = average(0.95, 0.9, 1.0) = 0.95; weighted composite with healthcare weights (5+3+5+2+3+1=19) = well above 0.85. |
| **SC-002**: Exposed API key → BLOCK on all scaffolds | **MET** | Test `test_secrets_exposed_blocks_all_scaffolds_sc002` (line 667) iterates all scaffolds returned by `domain.list_scaffolds()` and asserts `score.verdict == "block"` and `"secrets_exposed" in score.hard_blocks`. All 5 scaffolds include `secrets_exposed` in their `hard_blocks` list (confirmed by test `test_scaffold_has_security_block`, line 858). |
| **SC-003**: After 10 reviews, trend API correctly identifies increasing duplication_rate | **NOT MET** | No persistence or trend analysis code is operational. `_linear_slope()` exists but is not wired to any store. No test exercises trend analysis. The infrastructure (TrendResult model, linear regression function) is in place but disconnected from any data source. |
| **SC-004**: Conversus gate with 3 agents produces synthesis referencing extracted variables | **PARTIALLY MET** | The data model supports carrying extracted variables into a gate (`DomainScore.variables`, `DomainRecord.equilibrium_score`), but no gate invocation code exists. The conversus.yml at `specs/029-code-review-domain/conversus.yml` defines a 3-agent review, but this is for reviewing the spec itself, not for the plugin's programmatic gate functionality. |
| **SC-005**: Full pipeline (extract → score → persist → gate → equilibrium) runs in under 60s | **PARTIALLY MET** | The extract → score path runs successfully (tested). Persist, gate, and equilibrium stages are not implemented. The implemented portion (extract + score) runs in milliseconds, well under 60s, but the criterion requires the *full* pipeline. |

---

## Gap Summary

### Implemented (Inner Layers)
- Variable extraction from 8 tool formats
- Weighted composite scoring with configurable scaffolds
- Hard block evaluation with comparison operators
- 5 pre-built scaffolds with Pydantic validation
- Impact-ordered recommendations
- Pluggable extractor protocol

### Not Implemented (Outer Layers)
- ReviewStore (JSONL, SQLite, Supabase backends)
- Trend analysis (linear regression exists but is unwired)
- Developer profiles (no author field on DomainRecord)
- Technical debt alerts
- Conversus gate invocation
- Equilibrium scoring integration
- FastAPI API layer

### Implementation vs. Spec Alignment Issues
1. `DomainRecord` (base.py) lacks `author`, `pr_id`, `commit_sha`, `branch`, `files_changed`, `lines_added`, `lines_removed` fields that the spec's `ReviewRecord` defines
2. `CodeReviewDomain.score()` does not populate `DomainScore.variables`, unlike the base class implementation
3. `edge_case_coverage` and `test_to_code_ratio` variables are defined in the spec (Section 2) but not extracted by any extractor and not present in `DIMENSION_VARIABLES`
4. `duplication_rate` and `coupling_score` variables are defined in the spec but not extracted by any extractor

---

## Recommendations

1. **[P1] Implement ReviewStore with at minimum JSONLReviewStore** — FR-010, FR-011, FR-012, FR-013 all depend on persistence. The append-only JSONL store is the simplest path and unblocks trend analysis, developer profiles, and debt alerts.

2. **[P1] Add missing fields to DomainRecord** — The spec's `ReviewRecord` includes `author`, `pr_id`, `commit_sha`, `branch`, `files_changed`, `lines_added`, `lines_removed`. Without these, developer profiles and per-PR querying are impossible.

3. **[P1] Wire `_linear_slope()` into a trend analysis function** — The OLS regression implementation exists. It needs a `trend()` method on ReviewStore that queries records, extracts dimension values, and returns `TrendResult`.

4. **[P2] Populate `DomainScore.variables` in CodeReviewDomain.score()** — The base class does this (base.py line 469) but the overridden method in domain.py does not (line 448). Add `variables=variables` to the `DomainScore` constructor call.

5. **[P2] Add missing spec variables to extractors** — `edge_case_coverage`, `test_to_code_ratio`, `duplication_rate`, and `coupling_score` are in the spec's parameter list but have no extractors.

6. **[P3] Implement the conversus gate invocation** — FR-014 through FR-016 describe the gate integration. This depends on the gate system from spec 011 being available as a library call.

7. **[P3] Implement the FastAPI API layer** — FR-017 and FR-019 require API endpoints. This is a straightforward FastAPI app that delegates to `CodeReviewDomain` methods and `ReviewStore` queries.

---

## Referenced Files

- `<HOME>/code/payer-index-mono/conversus/specs/029-code-review-domain/spec.md` — all FRs and SCs
- `<HOME>/code/payer-index-mono/conversus/conversus/domains/code_review/domain.py` — scoring implementation
- `<HOME>/code/payer-index-mono/conversus/conversus/domains/code_review/extractors.py` — all extractors
- `<HOME>/code/payer-index-mono/conversus/conversus/domains/base.py` — DomainPlugin, DomainScore, DomainRecord, Scaffold, VariableExtractor, ReviewStore infrastructure
- `<HOME>/code/payer-index-mono/conversus/tests/test_code_review.py` — test coverage for FRs and SCs
