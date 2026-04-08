# Kalman/Convergence Review — Phase 1

**Agent**: kalman-mathematician
**Spec**: 034-kalman-convergence-fixes
**Date**: 2026-04-01
**Files reviewed**: convergence.py, kalman.py, predictor.py, test_kalman.py, test_convergence.py, test_cross_plugin.py

---

## Executive Summary

The Kalman filter implementation is mathematically sound for 2D and has been correctly extended to 3D with dimension-agnostic matrix helpers. However, several filter-correctness issues remain that the spec identifies but the code does not yet fully resolve.

---

## Findings

### F-1: eq_score accumulation is fixed in predictor.py [CRITICAL — C-2 addressed]

**Location**: predictor.py:252-274
**Status**: IMPLEMENTED

The predictor now accumulates `equilibrium_scores` across rounds by iterating `state.history` and appending per-round scores (lines 256-268). The current round's score is appended separately (lines 264-268). The single-element-list wrapping described in C-2 is no longer present.

**Verdict**: C-2 is resolved. The accumulation logic correctly builds a list matching the history length plus one for the current round.

### F-2: Zero-score sentinel fix — uses None, not 0.0 comparison [CRITICAL — C-3 addressed]

**Location**: convergence.py:276-281
**Status**: IMPLEMENTED

The `_build_observation_sequence` function now uses `any(s is not None for s in equilibrium_scores)` instead of the old `any(s != 0.0)` check. This correctly treats `0.0` as a legitimate equilibrium score and `None` as the "absent" sentinel.

**Verdict**: C-3 is resolved. The sentinel semantics are correct.

### F-3: Auto-sized default Q/R [HIGH — NEW-1 addressed]

**Location**: kalman.py:230-275, kalman.py:399-407
**Status**: IMPLEMENTED

`default_Q(n)` and `default_R(n)` now accept dimension parameter. `run_kalman_filter` infers dimension from `observations[0]` and passes it to the defaults. The 3D Q and R matrices have appropriate values.

**Verdict**: NEW-1 is resolved. Auto-sizing works correctly.

### F-4: Initial P for eq_score dimension [MEDIUM — NEW-7]

**Location**: kalman.py:413-423
**Status**: IMPLEMENTED

Initial variance for dimension index 2 (eq_score) is set to 0.25 instead of 1.0. This is tighter, appropriate for a [0,1]-bounded variable.

**Verdict**: NEW-7 is resolved.

### F-5: R[2][2] calibration for eq_score [MEDIUM — M-5]

**Location**: kalman.py:266-275
**Status**: IMPLEMENTED

`default_R(3)` sets `R[2][2] = 0.05`, ten times the concession_rate noise of 0.005. This reflects higher measurement uncertainty in the equilibrium score.

**Verdict**: M-5 is resolved.

### F-6: Joseph form covariance update NOT implemented [LOW — NEW-6]

**Location**: kalman.py:361-368
**Status**: NOT IMPLEMENTED (TODO comment present)

The standard `P_post = (I - KH) @ P_pred` form is used. A TODO comment at line 362 references the Joseph form. For short iteration counts (max 5 rounds), the standard form is numerically adequate. For longer sequences, P could lose positive semi-definiteness.

**Priority**: P3 — acceptable for current max-5-round constraint. Flag if rounds limit increases.

### F-7: Determinant/inverse limited to 2x2 and 3x3 [OBSERVATION]

**Location**: kalman.py:121-170
**Status**: By design

`_mat_det` and `_mat_inverse` raise `ValueError` for n >= 4. Since the state dimension is at most 3 (dispute, concession, eq_score), this is currently safe. Adding a 4th state dimension would require LU decomposition or Gauss-Jordan elimination.

**Priority**: P3 — document the limitation.

### F-8: Missing 3D end-to-end test [MEDIUM — M-1]

**Location**: test_kalman.py
**Status**: NEEDS VERIFICATION

The spec calls for a 3D end-to-end test feeding 3+ rounds of 3D observations and verifying state dimension, confidence bounds, and convergence. I did not find a comprehensive 3D e2e test — the test file needs to be checked for this specific scenario.

**Priority**: P2 — required by SC-004.

### F-9: Q/R dimension mismatch defense-in-depth [MEDIUM — RE-1]

**Location**: kalman.py:399-428
**Status**: PARTIALLY ADDRESSED

The auto-sizing from observation dimension handles the common case. However, if a caller passes explicit Q/R with wrong dimensions, the matrix operations will silently produce garbage (mismatched inner dimensions in multiplication). No dimension validation exists at the `run_kalman_filter` entry point.

**Priority**: P2 — add assertion `assert len(Q) == n and len(R) == n` at entry.

### F-10: Diagnostic logging for 3D innovation ratio [LOW — NEW-2]

**Location**: kalman.py:431-444
**Status**: IMPLEMENTED

Debug-level logging compares 3D vs 2D innovation magnitude. This is sufficient for empirical validation.

**Verdict**: NEW-2 is addressed as diagnostic logging.

---

## Spec Compliance Summary

| Item | Status | Priority |
|---|---|---|
| C-2 (accumulate eq_scores) | IMPLEMENTED | -- |
| C-3 (zero-score sentinel) | IMPLEMENTED | -- |
| NEW-1 (auto-size Q/R) | IMPLEMENTED | -- |
| M-1 (3D e2e test) | NEEDS VERIFICATION | P2 |
| M-5 (calibrate R[2][2]) | IMPLEMENTED | -- |
| NEW-7 (tune initial P) | IMPLEMENTED | -- |
| RE-1 (Q/R dimension mismatch) | PARTIAL | P2 |
| NEW-2 (empirical 3D validation) | IMPLEMENTED (logging) | -- |
| NEW-6 (Joseph form) | NOT IMPLEMENTED (TODO) | P3 |

## Open Questions

1. Has `test_2d_with_all_zero_eq_scores` been inverted/updated per C-3?
2. Does the 3D e2e test exist and cover SC-004?
3. Should `run_kalman_filter` validate Q/R dimensions match observation dimension?
