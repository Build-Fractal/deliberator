# Cross-Review: schema-engineer reviewing spec-compliance

**Spec**: 030-domain-plugin-architecture

---

## Agreement

The compliance audit is methodical and well-evidenced. I agree with the majority of assessments:

- **FR-004 (frozen DomainRecord)**: MET -- confirmed. All model_config entries verified.
- **FR-005 (DomainStore protocol)**: MET -- the protocol is clean and runtime-checkable.
- **FR-008 (append-only)**: MET -- no mutation methods, append-mode file opens, INSERT-only SQL.
- **FR-013 (deterministic extraction)**: MET -- pure function composition.
- **FR-014 (deterministic scoring)**: MET -- no randomness in scoring functions.
- **FR-016 (equilibrium score persisted)**: MET -- field exists, both stores handle it.
- **FR-018 (YAML scaffolds, no code execution)**: MET -- `yaml.safe_load()`, no eval/exec.

The SC-002 (simultaneous domains) analysis is correct: domain isolation is by file (JSONL) or table (SQLite), with router prefix separation in the API.

## Disagreements

### 1. FR-001 should be NOT MET, not PARTIALLY MET

The spec-compliance agent says FR-001 is "PARTIALLY MET" because `extract()`, `score()`, and `create_record()` exist but `gate()` and `get_router()` are missing. I believe this should be **NOT MET**. The requirement says the ABC "MUST define the extract -> score -> persist -> gate -> serve lifecycle." The word "lifecycle" is the key -- it is a sequence of steps, and two steps are entirely absent. Implementing 3 of 5 lifecycle steps is not partial compliance with a lifecycle requirement; it is non-compliance with the lifecycle as a whole, while meeting individual step requirements.

However, I acknowledge this is a judgment call. The fact that the 3 implemented steps work correctly is valuable regardless of classification.

### 2. FR-012 (CORS) -- agree NOT MET, but note it is trivial

CORS configuration in FastAPI is a single middleware addition:
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)
```
This is NOT MET by the letter of the requirement, but it is a 3-line fix with no architectural implications. Flagging it as NOT MET gives it equal weight with FR-002 (plugin discovery), which is architecturally significant. The compliance table could benefit from a priority/effort annotation.

### 3. SC-004 assessment -- I agree it is MET

The spec-compliance agent rates SC-004 as MET. I confirm from a schema perspective: `HealthResponse` provides `average_overall` and `verdict_distribution` (sufficient for a pie chart + trend number), and `TrendResponse` provides `values` and `slope` (sufficient for a sparkline + direction arrow). A frontend could render a meaningful dashboard from these two endpoints alone.

## Additions

The spec-compliance agent did not evaluate the test coverage against the FRs. The test file (`test_domains.py`) covers:
- FR-001 (partial): extraction, scoring, record creation tested. Gate not tested (not implemented).
- FR-005: Protocol compliance tested for both stores.
- FR-008: Implicitly tested via append/get/query cycle -- no mutation paths exist to test.
- FR-013/FR-014: Determinism tested implicitly (same inputs produce same outputs in test assertions).
- FR-016: `test_create_record_with_equilibrium` explicitly tests equilibrium_score persistence.

Missing test coverage for:
- FR-006: No Supabase store tests (not implemented).
- FR-010: API tests cover 5 endpoints; no gate endpoint test.
- FR-018: `test_load_scaffold` covers JSON only, not YAML loading.

The YAML scaffold loading path is untested. `load_scaffold()` imports `yaml` inside the function, but no test exercises the `.yml`/`.yaml` branch. If PyYAML is not installed, the import would fail at runtime with no coverage to catch it.
