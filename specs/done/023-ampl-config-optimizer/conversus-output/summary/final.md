# Phase 5 Synthesis: Spec 023 -- AMPL Config Optimizer

**Spec**: 023-ampl-config-optimizer
**Date**: 2026-04-01
**Agents**: optimization-engineer, plugin-engineer, spec-compliance

---

## Overall Assessment

The AMPL config optimizer is well-implemented. The MIP formulation correctly encodes the optimization problem as a binary selection over pre-computed grid points, achieving exact quality and cost match with the grid search at all integer grid points (0% error, exceeding the spec's 5% threshold). The dispatch layer cleanly routes between AMPL/HiGHS and the grid search fallback. The general-purpose `solve_ampl()` API is well-designed with file/string model support and proper lifecycle management. Infeasibility is handled gracefully via delegation to grid search. The primary gaps are: (1) HAS_AMPL checks only amplpy, not highspy (false-positive dispatch risk), (2) FR-012's optimality gap is hardcoded to 0.0 rather than extracted from HiGHS, and (3) the AMPL model is stored as a Python string rather than a .mod file (constraint partially unmet). Full consensus was achieved with no remaining disputes.

---

## Consensus Findings

### 1. Quality and Cost Models Match Grid Search Exactly (Consensus)

**Unanimous**. The `_quality_score()` and `_total_cost()` functions in ampl_model.py use the identical formulas as search.py. Tests verify 0% error at all grid points (5 rounds x 3 iterations x up to 9 agents = 135 points). FR-004's "within 5%" requirement is exceeded. The arbiter cost contribution (one launch per round) is correctly handled.

### 2. HAS_AMPL Must Check Both amplpy and highspy (Consensus)

**Unanimous P1**. The current flag checks only `from amplpy import AMPL`. If amplpy is installed without highspy, HAS_AMPL is True but the solver will fail at runtime. The fix:

```python
try:
    from amplpy import AMPL
    import highspy  # noqa: F401
    HAS_AMPL = True
except ImportError:
    HAS_AMPL = False
```

### 3. Optimality Gap Must Be Extracted from HiGHS (Consensus)

**Unanimous P1**. FR-012 requires `gap` in the result. The dispatch layer hardcodes `gap: 0.0`. While this is correct for the binary selection problem (trivially optimal), it should be read from AMPL's solve result for correctness and for the general-purpose API which may solve non-trivial MIPs.

### 4. MIP Formulation Is Correct but Equivalent to Grid Search (Consensus)

**Unanimous**. The binary selection MIP is mathematically equivalent to the grid search. For the current search space (up to 135 points), grid search is likely faster. The MIP's value is extensibility: new constraints, continuous relaxations, and larger search spaces can be added without rewriting the search algorithm.

### 5. Infeasibility Handling Is Correct (Consensus)

**Unanimous**. The two-stage approach (AMPL presolve detects infeasibility, grid search generates the human-readable report) is clean and correct. Minor improvement: metadata should distinguish `infeasibility_detected_by` and `report_generated_by`.

### 6. Add write_config_model() for .mod File Constraint (Consensus)

**Unanimous P2**. The spec constrains the AMPL model to be "readable/editable by users (stored as .mod file)." The model is stored as a Python string constant. Adding a `write_config_model(path)` function satisfies the constraint and improves usability.

### 7. Amend Spec for Grid-Point Lookup Approach (Consensus)

**Unanimous P2**. The spec describes "piecewise linear approximation" but the implementation uses binary selection over grid points (exact, not approximate). The spec should be amended to describe the actual approach.

### 8. SC-001 MET by Mathematical Construction (Consensus)

**Unanimous after discussion**. The MIP and grid search solve the same problem over the same data with the same costs and qualities. The optimal point must be identical. Runtime integration tests are recommended (P2) as an end-to-end safety net.

### 9. Grid Search Fallback Fully Preserved (Consensus)

**Unanimous**. SC-004 is MET. When HAS_AMPL is False, grid search runs directly with identical results. Tests verify field-by-field equality.

### 10. General-Purpose API Well-Designed (Consensus)

**Unanimous**. The `solve_ampl()` function supports string models, .mod files, scalar and indexed parameters, and arbitrary solvers. AMPL instances are always closed via try/finally. Minor improvements: wrap parse errors in ValueError, note AMPLSolverResult is unused.

---

<!-- DISPUTES_BEGIN -->

## Unresolved Disputes

None. All disagreements were resolved during the cross-review and revision phases. The specific resolutions:

- **Performance documentation priority**: Downgraded from P1 to P2 by consensus. Users do not choose between backends.
- **Model validation approach**: Resolved by consensus to wrap AMPL errors rather than pre-validate.
- **Python-level timeout**: Downgraded from P2 to P3. HiGHS time_limit satisfies FR-006.
- **AMPL licensing**: Withdrawn. FR-010 addresses this.
- **SC-001 classification**: Upgraded from NOT VERIFIED to MET by mathematical construction.

<!-- DISPUTES_END -->

---

## Compliance Summary

| Requirement | Status | Action |
|------------|--------|--------|
| FR-001 | MET | Add highspy to HAS_AMPL check |
| FR-002 | MET | None |
| FR-003 | MET | None |
| FR-004 | MET | None (exceeds 5% requirement) |
| FR-005 | MET | Clarify infeasibility metadata |
| FR-006 | MET | None |
| FR-007 | MET | None |
| FR-008 | MET | None |
| FR-009 | MET | None |
| FR-010 | MET | None |
| FR-011 | MET | None |
| FR-012 | PARTIALLY MET | Extract gap from HiGHS |
| SC-001 | MET | Add runtime integration test (P2) |
| SC-002 | NOT VERIFIED | Performance criterion, needs runtime |
| SC-003 | PARTIALLY MET | Add runtime integration test (P2) |
| SC-004 | MET | None |
| Constraints | 3/4 MET | Add write_config_model() for .mod file |

---

## Recommended Actions (Priority Order)

1. **P1**: Add highspy import check to HAS_AMPL flag.
2. **P1**: Extract actual optimality gap from HiGHS for FR-012 and general-purpose API.
3. **P2**: Add `write_config_model()` function to satisfy .mod file constraint.
4. **P2**: Amend spec: replace "piecewise linear approximation" with "grid-point binary selection."
5. **P2**: Clarify infeasibility metadata (infeasibility_detected_by vs. report_generated_by).
6. **P2**: Wrap AMPL parse errors in ValueError with descriptive message in solve_ampl().
7. **P2**: Add `@pytest.mark.skipif(not HAS_AMPL)` runtime integration tests.
8. **P2**: Document MIP-vs-grid-search performance trade-off for developers.
9. **P3**: Add Python-level timeout wrapper for general-purpose API defense-in-depth.
10. **P3**: Address AMPLSolverResult (document as forward declaration or remove).
11. **P3**: Consider dynamic solver name in FR-011 metadata (`"ampl-{solver}"`).
