# Phase 3 Revision: optimization-engineer

**Agent**: optimization-engineer
**Spec**: 023-ampl-config-optimizer
**Date**: 2026-04-01
**Inputs**: plugin-engineer cross-review, spec-compliance cross-review

---

## Disposition of Original Recommendations

### P1-1. Document MIP-vs-grid-search performance trade-off -- MODIFIED to P2

**Original**: Document that MIP overhead likely exceeds grid search for the current 135-point search space.

**Cross-review challenges**:
- plugin-engineer argues the priority is too high (P1 -> P2) since users do not choose between backends.
- spec-compliance classifies performance documentation as P3 (not a compliance concern).

**Revised position**: I accept the downgrade. The dispatch layer handles backend selection transparently. Users do not need to know about the performance trade-off. However, developers extending the optimizer should understand why both backends exist and when MIP becomes advantageous. P2 for developer documentation.

**Priority**: Downgraded to P2.

---

### P2-1. Add model validation to solve_ampl() -- MODIFIED

**Original**: Add basic model validation (non-empty check, parse error catch).

**Cross-review response (plugin-engineer T-1)**: plugin-engineer argues against reimplementing AMPL's parser. Instead, catch AMPL's parse errors and wrap them:

```python
try:
    ampl.eval(model)
except Exception as e:
    raise ValueError(f"AMPL model parse error: {e}") from e
```

**Revised position**: I accept plugin-engineer's approach. Wrapping AMPL's error is better than pre-validating. Add the non-empty check as a fast-fail before creating the AMPL instance.

**Priority**: Remains P2.

---

### P2-2. More robust .mod file detection -- MAINTAINED

**Original**: Consider separating the model parameter into model_string vs. model_file.

**Cross-review response**: No direct challenges. plugin-engineer mentions model distribution as a related concern.

**Priority**: Remains P2.

---

### P3-1. Parameterizable quality model -- MAINTAINED

No cross-review comments.

**Priority**: Remains P3.

---

## New Recommendations from Cross-Reviews

### N-1. Check highspy in HAS_AMPL flag (from plugin-engineer P1-1)

All three reviewers agree. HAS_AMPL should verify both amplpy and highspy are importable. This prevents false-positive dispatch that fails at runtime.

**Priority**: P1 (adopted from plugin-engineer).

---

### N-2. Extract actual optimality gap from HiGHS (from spec-compliance P1-1, plugin-engineer P1-2)

Both spec-compliance and plugin-engineer identify the gap hardcoding. For the dispatch layer, the fix is to check AMPL's `solve_result_num` to determine if HiGHS proved optimality. For the general-purpose API, include the MIP gap in the returned dict.

**Priority**: P1 (consensus).

---

### N-3. Amend spec for grid-point lookup approach (from spec-compliance MO-1)

spec-compliance notes the spec describes "piecewise linear approximation" but the implementation uses grid-point lookup (binary selection). The implementation is better (exact match, no approximation). The spec should be amended.

**Priority**: P2 (spec hygiene).

---

### N-4. SC-001 is MET by mathematical construction

optimization-engineer argued this in the spec-compliance cross-review. The binary selection MIP and grid search solve the same problem over the same data. The optimal point must be identical. plugin-engineer's compromise (MET with P2 runtime test) is acceptable.

**Priority**: Informational (SC-001 status upgrade from NOT VERIFIED to MET).

---

### N-5. Model readability constraint (from spec-compliance, plugin-engineer)

The AMPL model is a Python string, not a .mod file. The constraint says "stored as .mod file." Add a `write_config_model()` function to satisfy the constraint fully.

**Priority**: P2.
