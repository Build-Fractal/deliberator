# plugin-engineer Cross-Review of spec-compliance

**Cross-reviewer**: plugin-engineer
**Reviewing**: spec-compliance Phase 1 review of spec 023
**Date**: 2026-04-01

---

## Agreements

### 1. FR-012 PARTIALLY MET for gap hardcoding

All three reviewers converge on this issue. The gap should be extracted from HiGHS rather than hardcoded. This is the top finding.

### 2. SC-004 MET

The grid search identity tests are thorough. `test_grid_search_result_matches_direct_call` verifies field-by-field equality between the dispatch path and direct grid search. No disagreements.

### 3. FR-005 MET for infeasibility handling

The two-stage approach (AMPL detects, grid search reports) is correctly classified as meeting the requirement. The spec says "returning the same infeasibility report as the grid search" -- the grid search generates the report, so the output is identical by construction.

---

## Tensions

### 1. SC-001 classification

spec-compliance marks SC-001 as NOT VERIFIED (runtime). optimization-engineer argues it is MET by mathematical construction (both algorithms solve the same problem over the same data). I lean toward optimization-engineer's position: the MIP formulation selects from the same grid points with the same costs and qualities, so the optimal point must be the same. This is a proof, not a runtime test.

However, the proof assumes the AMPL model is correctly parsed and solved. A parse bug or solver bug could produce a different result. Runtime verification would confirm the end-to-end correctness. Compromise: mark SC-001 as MET (mathematical proof) with a P2 recommendation for runtime integration tests.

### 2. Constraint verification for .mod file storage

spec-compliance does not verify the constraint "The AMPL model must be readable/editable by users (stored as .mod file)." The model is stored as a Python string constant. optimization-engineer's cross-review of spec-compliance raises this. I agree: the constraint's letter says ".mod file" but the implementation uses a Python string. The constraint's intent (readability) is met but the mechanism is not.

This is a minor gap. The Python string is well-formatted AMPL syntax and is readable/editable in context. Adding a `write_config_model()` helper (my MO-1 in the optimization-engineer cross-review) would satisfy the constraint fully.

---

## Missed Opportunities

### 1. No assessment of test quality

spec-compliance counts tests and maps them to requirements but does not assess test quality. Key questions:

- The mock AMPL tests use `_make_mock_ampl()` which returns a mock that always selects `chosen_idx=1`. This means the tests always verify the first grid point. A more thorough test would verify the last grid point or a grid point in the middle.
- The timeout test uses `side_effect = TimeoutError("solver timed out")`. But the actual timeout comes from HiGHS's `time_limit`, which would produce a different exception path (AMPL would report a solve result of "limit" or "stopped"). The test mocks the wrong failure mode.
- The infeasibility test mocks `solve_with_ampl` returning None but does not verify that AMPL's "infeasible" solve result is correctly handled in the non-mocked path.

### 2. No cross-reference of D007 formula

spec-compliance verifies the cost formula matches search.py but does not independently verify D007. If both implementations have the same bug, the tests pass but the formula is wrong. A reference to the D007 definition (in a spec or design doc) would close this gap.
