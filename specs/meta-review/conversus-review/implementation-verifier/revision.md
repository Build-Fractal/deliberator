# Phase 3 Revision: implementation-verifier

**Date**: 2026-04-01

---

## Cross-Reviews Received From

- **consistency-auditor**: 3 DCs, 4 Ts, 4 SAs
- **dependency-auditor**: 3 DCs, 4 Ts, 3 SAs
- **test-coverage-auditor**: 3 DCs, 4 Ts, 4 SAs

---

## Recommendation Dispositions

### Fix 1: `DomainScore.variables` not populated
**Status**: MAINTAINED — unanimously confirmed by all 4 reviews. The most validated finding in the meta-review. Accept the test-coverage-auditor's DC-2 that a failing test should be written first. **Amended sequencing: write failing test -> apply one-line fix -> verify test passes.**

### Fix 2: `HAS_AMPL` guard missing highspy check
**Status**: MAINTAINED — unanimously confirmed. Dependency-auditor confirms fix is dependency-safe. Test-coverage-auditor confirms no test for highspy presence. **Amended: write failing test (import highspy check) first.**

### Fix 3: Innovation sequence discarded in Kalman filter
**Status**: MAINTAINED — no reviewer challenged the finding. The consistency-auditor's CSI-3 adds context (eq_score discontinuity), but the innovation storage fix is independent of the eq_score wiring. Test-coverage-auditor confirms no test exists. **Amended: the fix is a 3-step process: (a) add `innovation` field to `KalmanState`, (b) store the innovation in `kalman_update()`, (c) update `detect_fixed_point()` to use innovation magnitude. Steps a/b can land first with a test; step c depends on spec 022 Remediation 1 design decision.**

### Fix 4: Plugin config Q/R not wired
**Status**: MAINTAINED — no reviewer challenged the finding. Dependency-auditor confirms all files are within `plugins/nashopt/` (dependency-safe). **No amendment needed.**

### Fix 5: BayesianGame prior key validation
**Status**: MAINTAINED — no reviewer challenged the finding. Test-coverage-auditor confirms the gap. **No amendment needed.**

### Correction 6: Spec 021 DC-2/DC-3 line references
**Status**: MAINTAINED WITH CLARIFICATION — the consistency-auditor (DC-1) agrees that the `PluginResult` construction is in the plugin wrapper, not `solver.py`. The dependency-auditor (DC-1) confirms this is intra-package (no boundary violation). **Amended: explicitly note that the 021 synthesis should reference `equilibrium_scorer.py` (or equivalent plugin wrapper), not `solver.py`, for `PluginResult` error-path findings.**

### Correction 7: Spec 029 P1-1 attribution
**Status**: MAINTAINED — the consistency-auditor (CSI-2) confirms the base class `DomainPlugin.score()` correctly passes `variables=variables` at line 469. The bug is only in `CodeReviewDomain.score()` override. **No amendment needed.**

### Architecture 8: Base class `score()` `.json` hardcoding fix
**Status**: MAINTAINED — all 4 reviews confirm this. The consistency-auditor identifies it as CSI-1. The test-coverage-auditor confirms no YAML scaffold loading test exists. **Accept the consistency-auditor's sequencing: R-1 (this fix) must land before R-3 (delegate to super()).**

### Architecture 9: `_matches_filters` silent ignore
**Status**: MAINTAINED — the consistency-auditor (T-3 in cross-review) and dependency-auditor (T-2) both note this is within the domains boundary. No reviewer elevated the severity. **No amendment needed.**

### Architecture 10: AMPL model `.mod` file extraction
**Status**: MAINTAINED WITH CAVEAT — the dependency-auditor (T-3) correctly notes this introduces a filesystem dependency. **Amended: if extracted, the `.mod` file must be co-located with the Python module and loaded via `importlib.resources` (not a filesystem path) to avoid deployment dependency issues.**

---

## New Recommendations

### Fix-NEW-1: Update executive summary to match corrected verification count

The test-coverage-auditor (T-4) correctly identifies that my executive summary says "17 VERIFIED, 3 INACCURATE, 1 STALE" while the corrected count is 18/2/0. The footnote correction is insufficient. **Fix the executive summary to read "18 VERIFIED, 2 INACCURATE, 0 STALE" and remove the footnote.**

### Fix-NEW-2: Classify "inaccurate" findings as "mislocated"

Accept the consistency-auditor's T-2: the 2 inaccurate findings in spec 021 describe real bugs attributed to the wrong file, not phantom bugs. Reclassifying as "mislocated" is more precise and avoids overstating synthesis unreliability. **The corrected summary becomes: "18 VERIFIED, 2 MISLOCATED, 0 STALE."**

### Architecture-NEW-1: Add cross-boundary change annotation to fix list

Accept the dependency-auditor's DC-2: the immediate fix list should distinguish single-file fixes from cross-boundary changes. Fixes 1-5 are within single packages. Architecture improvement 8 (scaffold extension) modifies `base.py` which is imported by `code_review/domain.py` — this requires testing in both the base and subclass.

---

## Position Summary

The cross-reviews validated my core methodology: line-by-line code verification is reliable and complementary to the other audit approaches. The main adjustments are:

1. **Test-first sequencing**: The test-coverage-auditor's DC-2 convinced me that all 5 immediate fixes should have failing tests written before the code changes. This is a process improvement that makes the fixes more robust.

2. **Terminology precision**: Changing "INACCURATE" to "MISLOCATED" for the spec 021 findings (consistency-auditor's suggestion). The bugs are real; only the file attribution is wrong.

3. **Self-correction on executive summary**: The verification count discrepancy between my executive summary and detailed table was caught by the test-coverage-auditor. This is an embarrassing internal inconsistency in a review that checks for exactly this kind of error in others.

4. **Ordering dependency acknowledged**: The consistency-auditor's R-1/R-3 sequencing requirement is a real constraint I missed. The scaffold extension fix must precede the delegation refactor.

My confidence in the 18 verified findings is unchanged. My confidence in the fix recommendations is higher because the sequencing constraints are now explicit, and the test-first approach ensures each fix is validated.
