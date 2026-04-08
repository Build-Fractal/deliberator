# Cross-Review of kalman-mathematician

**Reviewer**: spec-compliance
**Reviewing**: kalman-mathematician's Phase 1 review

---

## Agreements

- All 10 findings (F-1 through F-10) are accurate.
- Priority assessments are reasonable.
- The suggestion to add Q/R dimension assertion is valid.

## Challenges

### On F-9 priority (Q/R dimension mismatch)

The mathematician rates this P2. I find this should be P1 based on the crash analysis: a dimension mismatch would cause `_mat_mul` to raise `IndexError`, which is an unhandled crash in the Kalman path. While the OLS fallback would catch it (convergence.py:733), the error message would be unhelpful. An explicit assertion with a clear error message is P1 defense-in-depth.

**Align with plugin-integration-engineer**: Upgrade to P1.

### On F-8 (3D e2e test)

The mathematician correctly flags this. The spec explicitly requires M-1 and SC-004. If the test does not exist, this is a P2 gap (not blocking, but required for success criteria).

## Additions

### test_2d_with_all_zero_eq_scores inversion (from C-3)

The spec says "Invert test `test_2d_with_all_zero_eq_scores`." The mathematician's open question #1 asks whether this was done. This is a spec compliance gap that I should have caught: if the test still uses the old `!= 0.0` logic, it will pass incorrectly. The test should be updated to verify that `0.0` enters the 3D path.

**Priority**: P2 — test correctness.

## Overall Assessment

The kalman-mathematician's review is excellent on filter correctness. All findings verified.
