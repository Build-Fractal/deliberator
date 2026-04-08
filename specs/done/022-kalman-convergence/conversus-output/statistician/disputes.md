# Phase 4 Disputes: statistician

**Agent**: statistician
**Spec**: 022-kalman-convergence
**Date**: 2026-04-01
**Phase**: 4 (Post-revision disputes)

---

## Remaining Disputes

None. All disagreements were resolved during Phases 2-3.

---

## Resolution Summary

### Joseph form priority (originally P2, downgraded to P3)

**Resolution**: statistician accepted the downgrade after plugin-engineer and spec-compliance argued the simple form is correct for 3x3 diagonal-dominant matrices. The Joseph form remains an option if numerical issues are observed.

### Default noise validation scope (originally broad, narrowed)

**Resolution**: statistician accepted plugin-engineer's lighter approach (test for extreme inputs) and incorporated spec-compliance's observation about R[0][0] conservatism.

---

## Consensus Positions

1. **Spec amendment needed**: Remove scipy gating language, replace with round-count threshold. Unanimous.
2. **Initial covariance bias**: Document as design choice. Unanimous.
3. **Exception handling**: Differentiate logging levels for expected vs. unexpected failures. Consensus between statistician and plugin-engineer.
4. **SC-003**: MET with current test. Unanimous after revision.
5. **Observation noise documentation**: R[0][0] conservatism should be documented. Unanimous.
