# Spec-Compliance Revision: Spec 023 -- AMPL Config Optimizer

**Reviewer**: spec-compliance
**Revision iteration**: 1
**Date**: 2026-04-01

---

## Recommendation Dispositions

### Recommendation 1: Align FR-004 spec text with implementation (was P1)

**Disposition: MAINTAINED**

solver-engineer's cross-review argues FR-004 should be rated "PASS on correctness, FAIL on approach" rather than PARTIAL PASS. plugin-engineer's cross-review did not address FR-004 (solver formulation concern). I accept solver-engineer's more precise framing -- the requirement specifies both a tolerance and a technique, and only the tolerance is satisfied.

The fix is editorial: amend FR-004 to describe what was built (exact enumeration) rather than what was originally envisioned (PWL approximation). This eliminates the spec-implementation mismatch without changing the code.

**Revised recommendation**: Unchanged. Amend FR-004 to reflect exact enumeration. Priority: P1 (spec-implementation alignment is a first-order compliance concern).

---

### Recommendation 2: Store config model as `.mod` file (was P2)

**Disposition: MAINTAINED**

Three-way convergence. solver-engineer Rec 4, spec-compliance Rec 2, plugin-engineer acceptance. No challenges received.

**Revised recommendation**: Unchanged. Priority: P2.

---

### Recommendation 3: Revise SC-002 (was P2)

**Disposition: MAINTAINED**

solver-engineer Rec 6 converges. plugin-engineer did not address SC-002 (solver performance concern). Two of three reviewers agree SC-002 is not achievable with the current formulation. The success criterion should describe what the formulation actually provides.

**Revised recommendation**: Revise SC-002 to: "AMPL optimizer correctly identifies infeasibility and delegates to grid search for the detailed infeasibility report. For search spaces larger than the current 135-point grid, the MIP formulation enables LP-relaxation-based pruning." Priority: P2.

---

### Recommendation 4: Extract real MIP gap (was P2)

**Disposition: MAINTAINED**

Three-way convergence. solver-engineer Rec 3, spec-compliance Rec 4, plugin-engineer acceptance. The hardcoded `gap: 0.0` satisfies FR-012's letter but not its spirit. The gap value should reflect the solver's actual optimality assessment.

**Revised recommendation**: Unchanged. Priority: P2.

---

### Recommendation 5: Integration tests with real solver (was P3)

**Disposition: MAINTAINED**

plugin-engineer's cross-review raises a valid CI concern: integration tests only run where amplpy is installed. The recommendation is to use `@pytest.mark.skipunless(HAS_AMPL)`, which is the standard pattern for optional-dependency tests. CI that does not install amplpy skips these tests; developer machines and dedicated integration CI jobs run them.

solver-engineer's cross-review accepts this finding. Two of three reviewers agree.

**Revised recommendation**: Unchanged. Add `@pytest.mark.skipunless(HAS_AMPL)` integration tests that solve the real problem and verify against grid search. Priority: P3.

---

## New Recommendations

### New Recommendation A: Check for both amplpy and highspy in HAS_AMPL (Priority: P2)

Raised in my FR-001 analysis as a note, escalated by plugin-engineer's cross-review to a concrete recommendation. solver-engineer's revision adopts the same finding. Three-way convergence.

FR-001 says "amplpy AND highspy are importable." The implementation checks only amplpy. The fix: `try: from amplpy import AMPL; import highspy; HAS_AMPL = True`.

**Recommendation**: Align the HAS_AMPL guard with FR-001's wording. Priority: P2.

### New Recommendation B: Remove dead `solver` config key from docstring (Priority: P3)

plugin-engineer's revised Rec 2 proposes removing the undocumented `solver` config key from `ConfigOptimizer`'s docstring. The spec does not define this config key, and the code does not read it. The docstring promises a feature that does not exist.

From a compliance perspective, documentation that claims capabilities beyond the spec is a form of spec drift. The docstring should only describe features that the spec defines and the code implements.

**Recommendation**: Remove `solver (str)` from the `ConfigOptimizer` docstring. If solver pinning is needed, add a requirement to the spec first. Priority: P3.

---

## Updated Compliance Summary

After cross-review, I update the compliance assessments:

| Requirement | Previous | Revised | Change Reason |
|---|---|---|---|
| FR-001 | PASS | PASS* | Note: should check highspy too |
| FR-004 | PARTIAL | PARTIAL | Confirmed by solver-engineer |
| FR-008 | PASS* | PASS* | Documentation gap confirmed |
| FR-009 | PARTIAL | PARTIAL | Config model still Python string |
| FR-012 | PASS* | PASS* | Gap hardcode confirmed |
| SC-002 | WEAK | WEAK | Confirmed by solver-engineer |

All other assessments unchanged. The asterisks now carry higher confidence: three reviewers converge on the same gaps.

---

## Position Summary

**Maintained** (5):
- FR-004 spec alignment (Rec 1) -- confirmed by solver-engineer's cross-review.
- `.mod` file (Rec 2) -- three-way convergence.
- SC-002 revision (Rec 3) -- convergence with solver-engineer.
- Gap extraction (Rec 4) -- three-way convergence.
- Integration tests (Rec 5) -- accepted by two reviewers.

**New** (2):
- Both-dependency import check (New Rec A) -- three-way convergence.
- Remove dead docstring (New Rec B) -- adopted from plugin-engineer's revised Rec 2.

No recommendations were withdrawn or fundamentally modified. The cross-reviews strengthened existing positions rather than challenging them. The most significant new finding is the `HAS_AMPL` import guard gap (New Rec A), which aligns the code with FR-001's explicit "amplpy AND highspy" wording.

---

### Referenced Documentation

- Cross-reviews received: solver-engineer and plugin-engineer cross-reviews of spec-compliance
- Cross-reviews written: spec-compliance cross-reviews of solver-engineer and plugin-engineer
- `specs/done/023-ampl-config-optimizer/spec.md` -- FR-001 ("amplpy AND highspy"), FR-004, FR-012, SC-002
- `conversus/plugins/optimizer/ampl_model.py` -- L29-34 (HAS_AMPL guard)
- `conversus/plugins/optimizer/optimizer.py` -- L38-39 (solver docstring)
