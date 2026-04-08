# Cross-Review: consistency-auditor reviewing implementation-verifier

**Date**: 2026-04-01
**Phase**: 2 — Cross-Reviews

---

## Dangerous Contradictions

### DC-1: Spec 021 inaccuracies weaken cross-spec findings that depend on 021's claims

The implementation-verifier found 2 inaccuracies in spec 021 (both involving file/line misattributions for `PluginResult` error paths). My review (CSI-3, CSI-4) identifies two cross-spec concerns rooted in spec 021: the heuristic-vs-solver score discontinuity (CSI-3, affecting spec 022) and the solver provenance key pattern (CSI-4, affecting spec 023). If the 021 synthesis mislocates where `PluginResult` is constructed, then CSI-4's recommendation to "standardize solver provenance keys across plugins" (R-8) may need to target a different file than `solver.py`. The implementation-verifier's correction is essential: the provenance fix belongs in the plugin wrapper (`equilibrium_scorer.py`), not in `solver.py`.

### DC-2: Implementation-verifier confirms the scaffold bug but misattributes the 029 synthesis's understanding

The implementation-verifier states: "Spec 029 synthesis assumes `CodeReviewDomain.score()` uses the base class `score()` method" (Off-Base Assumption #3). This is partially incorrect. The 029 synthesis explicitly identifies that `CodeReviewDomain.score()` is a full override — the P1-1 bug (missing `variables=variables`) is attributed to the override, not the base class. What spec 029 misses (and what my CSI-1 finds) is the *architectural problem*: the override should not exist in its current form. The implementation-verifier and I agree on the bug, but the implementation-verifier's characterization of the 029 synthesis's assumption is inaccurate.

### DC-3: Innovation sequence gap severity assessment diverges

The implementation-verifier flags the innovation sequence discard (`kalman.py:289`) as an "immediate fix" and notes the equilibrium score third dimension is "effectively reducing the 3D filter to a 2D filter." My review (CSI-3) connects this to spec 021: when equilibrium scores are eventually wired through (spec 022 Remediation 6), the discontinuity from spec 021's heuristic-vs-solver switching will corrupt the Kalman state. The implementation-verifier treats innovation storage and eq_score wiring as independent fixes; I treat them as causally linked. Both fixes are needed, but the order matters: fix the discontinuity (021) before wiring eq_scores (022).

---

## Tensions

### T-1: Verification sample size and confidence

The implementation-verifier checked 3 claims per synthesis (21 total, 18 verified). This is a spot check, not exhaustive. My review focuses on cross-spec claims, which are inherently higher-risk because they span review boundaries. The implementation-verifier's 86% accuracy rate (18/21) is strong but could be lower for cross-spec claims that no single synthesis fully owns. Neither of us verified claims that exist only in the intersection of two specs.

### T-2: "Inaccurate" vs. "mislocated" distinction

The implementation-verifier calls spec 021's DC-2 and DC-3 "INACCURATE." I would classify them as "mislocated" — the bugs are real, but attributed to the wrong file. This distinction matters: "inaccurate" suggests the synthesis found phantom bugs, while "mislocated" means the bugs exist elsewhere. The implementation-verifier's corrected total (18/21) implicitly acknowledges this, but the executive summary's framing ("The weakest is 021 where two of three checked claims contain inaccuracies") overstates the problem.

### T-3: `_matches_filters` silent ignore severity

The implementation-verifier flags `_matches_filters` silently ignoring unknown filter keys as a data integrity concern in the persistence layer. My review does not flag this because it is within a single spec (030). However, if domain queries are composed from cross-spec parameters (e.g., a gate system query using filter keys defined in different specs), a typo in one spec's filter key would silently return unfiltered data. The severity depends on whether cross-domain queries exist — which neither of us verified.

### T-4: Corrected verification count

The implementation-verifier's executive summary says "17 VERIFIED, 3 INACCURATE, 1 STALE" but the detailed table and correction note produce 18 VERIFIED, 2 INACCURATE, 0 STALE. The correction is buried in a footnote. The executive summary should be updated to match.

---

## Safe Agreements

### SA-1: The scaffold `.json` hardcoding in `base.py:447` is a confirmed P1 bug

Both reviews independently identify and confirm this. The implementation-verifier verified it against the actual code. My review (CSI-1) identifies the cross-spec impact (blocks spec 030's architectural promise). The bug is real, the fix is known, and both reviews agree on P1 priority.

### SA-2: `DomainScore.variables` omission in `CodeReviewDomain.score()` is confirmed

The implementation-verifier initially marked this INACCURATE then corrected to VERIFIED. My review (CSI-2) identifies the cross-spec root cause (pipeline reimplementation). Both agree this is P1 and needs a one-line fix plus a larger architectural refactor.

### SA-3: Mathematical correctness assessments are reliable

The implementation-verifier confirms Shapley formula, Kalman mechanics, and potential game diagnostic are all correctly assessed. My review relies on these mathematical claims (e.g., CSI-3 depends on the Kalman filter behavior being as described). The implementation-verifier's confirmation strengthens my cross-spec findings.

### SA-4: The `HAS_AMPL` guard gap is confirmed across both reviews

The implementation-verifier verified the missing `highspy` check at `ampl_model.py:29-34`. My review (R-4) independently recommends this fix at P1. Both agree on the bug and the fix.
