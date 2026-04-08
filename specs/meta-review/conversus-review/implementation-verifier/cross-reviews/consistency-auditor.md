# Cross-Review: implementation-verifier reviewing consistency-auditor

**Date**: 2026-04-01
**Phase**: 2 — Cross-Reviews

---

## Dangerous Contradictions

### DC-1: CSI-2 root cause attribution differs from verified code behavior

The consistency-auditor (CSI-2) states that spec 030's `DomainPlugin.score()` at `base.py:469` passes `variables=variables` to `DomainScore`, while spec 029's `CodeReviewDomain.score()` at `domain.py:448` does not. I verified this exact claim (spec 029, claim #1) and confirmed the bug. However, the consistency-auditor's recommendation R-3 ("refactor `CodeReviewDomain.score()` to delegate to `super().score()`") implies that the base class scoring pipeline is production-ready for subclass delegation. My verification found that the base class `score()` hard-codes `.json` scaffold extensions (base.py:447). If `CodeReviewDomain` delegated to `super().score()`, it would break because code review scaffolds are `.yml`. **R-1 (fix scaffold extension) must land before R-3 (delegate to super) is feasible.** The consistency-auditor's recommendations are individually correct but have an implicit ordering dependency that is not stated.

### DC-2: CSI-4 (solver provenance pattern) targets the wrong file

The consistency-auditor identifies that spec 023's `solve_with_ampl()` returns `None` for failures while spec 021 establishes a `solver` provenance key pattern. The recommendation (R-8) is to "standardize solver provenance keys across plugins." I found (Off-Base Assumption #1) that the `solver` key lives on `PluginResult`, not on `SolverResult` in `solver.py`. The consistency-auditor's R-8 does not specify which files to modify. If the standardization targets `solver.py` and `ampl_model.py` (the pure function modules), it would be mislocated — the provenance keys belong in the plugin wrappers (`equilibrium_scorer.py`, `config_optimizer.py`). The consistency-auditor correctly identifies the cross-spec gap but lacks the file-level precision to guide implementation.

### DC-3: MO-1 (game form / payoff matrix integration) overstates the gap

The consistency-auditor notes that spec 025 adds 5 new game forms but `solver.py:build_payoff_matrix()` only supports 4 modes. I verified the solver code and confirm the 4-mode limitation. However, the consistency-auditor frames this as a "missed opportunity to plan the integration surface." In practice, the new game forms (coalitional, congestion, bayesian, repeated, mechanism design) have fundamentally different solution concepts than the payoff-matrix approach used by `build_payoff_matrix()`. Coalitional games use Shapley values (already implemented in `solvers.py`), not payoff matrices. Bayesian games use type-conditional strategies. Only congestion games might map naturally to a payoff matrix. The "integration surface" would be a new solver dispatch, not extensions to `build_payoff_matrix()`.

---

## Tensions

### T-1: Recommendation ordering

The consistency-auditor presents R-1 through R-10 in priority order (P1 first), but R-3 (refactor to `super().score()`) depends on R-1 (fix scaffold extension) landing first. My verification reveals this dependency. The recommendations should be explicitly sequenced, not just prioritized.

### T-2: "Off-base" vs. "future concern"

The consistency-auditor labels OBA-2 (Kalman confidence calibration) as an "off-base assumption." I verified the formula at `kalman.py:385-410` and confirm the initialization dependence. However, the spec 022 synthesis acknowledges this (consensus finding #4, remediation 4) and tracks it as a known limitation. Calling it "off-base" implies the synthesis is making an error; "known limitation with tracked remediation" would be more accurate.

### T-3: CSI-3 severity

The consistency-auditor rates CSI-3 (heuristic-vs-solver score discontinuity affecting Kalman filter) as P2. I would rate it lower because: (a) the equilibrium score is currently hardcoded to 0.0, so there is no discontinuity today, (b) fixing the discontinuity before wiring eq_scores is a prerequisite tracked in the spec 022 synthesis, and (c) my verification confirms the filter is effectively 2D right now. The bug is real but dormant and already tracked.

### T-4: Level of detail in cross-spec dependency mapping

The consistency-auditor's R-10 proposes a cross-spec dependency matrix. I support this but note that the matrix should distinguish between verified dependencies (confirmed in code) and aspirational dependencies (mentioned in syntheses but not implemented). Several entries in R-10 mix these: "Spec 029 FR-014/FR-016 depends on spec 011 (gate system)" is aspirational, while "Spec 029 SC-004 depends on spec 030 (domain plugin base layer)" is verified.

---

## Safe Agreements

### SA-1: The 4 cross-spec inconsistencies are real

I verified the code behind CSI-1 (scaffold extension: confirmed at base.py:447 and domain.py:375), CSI-2 (DomainScore.variables: confirmed at domain.py:448), and CSI-4 (solver provenance: confirmed as different return patterns). CSI-3 is verified as a correct architectural concern, even if dormant. The consistency-auditor's cross-spec lens found real bugs that no single-spec synthesis fully captured.

### SA-2: R-4 (highspy import guard) is confirmed

Both my verification and the consistency-auditor's review independently confirm the missing `highspy` check at `ampl_model.py:29-34`. This is a clear, unambiguous bug with a known fix.

### SA-3: The optional-import pattern is consistent but not formalized

I verified the pattern in specs 021, 022, 023. The consistency-auditor recommends formalizing it (R-5). Both agree the pattern works correctly as-is; formalization is quality improvement.
