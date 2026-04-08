# Cross-Review of spec-compliance's Review

**Cross-reviewer**: plugin-engineer
**Reviewing**: spec-compliance's review of Spec 021 (nashopt integration)
**Date**: 2026-04-01

---

## Dangerous Contradictions

### DC-1: FR-005 assessment diverges on severity

spec-compliance marks FR-005 as **PARTIALLY MET** and identifies the blanket "all agents not at equilibrium" fallback (solver.py line 438) as a violation of the precision requirement. I marked FR-005 as **PASS**. On reflection, spec-compliance is correct and my assessment was too lenient. The spec says the solver "MUST report which agents are NOT at their best response." The blanket fallback is a lossy over-report that violates the MUST. My review acknowledged the `best_responses` data was available (Off-Base Assumptions #2, where I noted the dual int/str lookup) but did not connect it to the FR-005 compliance question. spec-compliance's P1-3 recommendation to derive per-agent status from `best_responses` is the right fix. Adopting their PARTIALLY MET verdict here strengthens the overall assessment.

### DC-2: FR-008 -- spec-compliance says MET, I say PARTIAL

spec-compliance marks FR-008 as **MET** ("PluginResult.data includes solver field") based on the happy-path and heuristic-path evidence. My review identifies two error-path `PluginResult` returns (unknown-mode at line 371-378, computation-failure at line 394-401) that omit the `solver` key entirely, and I filed this as P1-1. FR-008 uses MUST language ("The `PluginResult.data` dict MUST include `solver`"), and error-path returns are still `PluginResult` instances that consumers will receive. spec-compliance's evidence section focuses exclusively on the `_score_from_solver` and `_compute_equilibrium_score_heuristic` code paths, which do set the field. The error paths are not mentioned. This is a real compliance gap -- consumers that unconditionally access `result.data["solver"]` will get a `KeyError`. The MET verdict should be downgraded to PARTIAL.

### DC-3: SC-001/SC-002 -- agreement on NOT MET but conflicting remediation scope

spec-compliance recommends adding tests that either mock nashopt to return a realistic low distance OR run the heuristic path with converged features. My P1 recommendations do not include SC-001/SC-002 threshold tests at all -- I focused on plugin architecture issues and treated success criteria testing as outside my scope. The contradiction is not in the diagnosis but in the implied priority. spec-compliance correctly identifies these as P1 ("must fix before ship") because they are the spec's primary acceptance criteria. If we ship without SC-001/SC-002 tests, the two most important spec guarantees are unverified. I should have included these in my review. Adopting spec-compliance's P1 recommendation for threshold tests.

---

## Tensions

### T-1: Timeout test -- same diagnosis, different fix specificity

Both reviews identify that the timeout test (`test_timeout_falls_back_to_heuristic`, line 623) does not exercise the real `concurrent.futures` timeout mechanism. spec-compliance recommends a real-timeout integration test (Missed Opportunities #1, P2-4) with a blocking callable. My review (P1-2) recommends patching `check_equilibrium_nashopt` to `time.sleep(5)` with a 0.01s timeout. The tension: I filed this as P1 (must fix), spec-compliance filed it as P2 (should fix). The spec itself does not mandate integration-level timeout testing -- it says SC-004 requires "solver timeout produces a heuristic fallback score, not an error," which the mock test does verify at the behavioral level. The real question is whether the futures-specific code path is critical enough to block ship. I lean toward P1 because the mock tests a fundamentally different exception propagation path than reality, but spec-compliance's P2 classification is defensible if the behavioral guarantee is considered sufficient.

### T-2: Per-agent payoff zeros -- same finding, different framing

Both reviews flag that `_score_from_solver` hardcodes `payoff: 0.0` for all agents (scorer.py line 173). spec-compliance frames this as "information loss" and a data shape difference between solver and heuristic paths (Missed Opportunities #5, P2-5). I frame it as an output parity issue that could "break downstream analytics" (Missed Opportunities #4, P2-1). The underlying concern is identical. The tension is that spec-compliance treats it as a documentation issue ("add a note field") while I treat it as a data contract issue ("populate real values or document the zero-value contract"). The spec does not mandate per-agent payoff values in FR-008 or elsewhere -- it only requires `score`, `agents_at_equilibrium`, and `solver`. So this is technically outside the spec's compliance scope. Both of us should acknowledge that this is a quality-of-life issue, not a compliance gap.

### T-3: Dead variable in `_build_rb_matrix` -- flagged by me, absent from spec-compliance

My review identifies a dead `total_surface` variable in `_build_rb_matrix` (lines 255-259) and files it as P1-3. spec-compliance does not mention it. This is not a compliance issue -- the spec does not dictate implementation details of the matrix builder internals. However, dead variables in payoff construction code are dangerous because they suggest an incomplete normalization step. If `total_surface` was intended to normalize payoffs (as the `max_k > 0` branch does with severity-weighted ratios), its absence may produce scale-inconsistent matrices that affect solver behavior. The tension: is this a P1 code quality issue (my view) or below the compliance threshold (spec-compliance's implicit view by omission)?

### T-4: nashopt API surface assumptions

spec-compliance flags two assumptions about the nashopt API: (1) the code checks for `agents_not_at_equilibrium` which is not in the documented API (Off-Base #1), and (2) `best_responses` keys may be ints or strings with dual-lookup (Off-Base #2). My review does not flag the `agents_not_at_equilibrium` assumption at all -- I missed it. I do implicitly touch the `best_responses` question in the context of the cooperative matrix builder semantics, but I do not address the API surface mismatch. spec-compliance is more thorough here. The tension is in scope: spec-compliance reads the spec's API surface table (Section 2) literally and finds the code expects more than the spec documents. My review takes the code at face value without cross-checking against the spec's API contract. spec-compliance's approach is more rigorous for a compliance review.

### T-5: ThreadPoolExecutor resource leakage

spec-compliance raises the concern that a timed-out solver thread continues running in the background (Off-Base #3, P3-7), potentially holding GPU resources with JAX. My review does not mention this at all. This is a real operational concern -- in production with JAX on GPU, a runaway solver thread could exhaust GPU memory. The spec says "capped at a configurable timeout" but does not address cancellation. The tension: spec-compliance correctly identifies this as a P3, but for a JAX-heavy deployment it could be a P1 operational risk. Neither review fully explores the severity.

---

## Safe Agreements

### SA-1: FR-001 through FR-004 and FR-006 are correctly implemented

Both reviews agree that the core solver dispatch (FR-001), heuristic fallback (FR-002), payoff matrix construction (FR-003), score normalization (FR-004), and degenerate case handling (FR-006) are all correctly implemented with adequate test coverage. Neither review identifies any gap in these requirements. The code evidence is consistent across both reviews (same line numbers, same test classes).

### SA-2: SC-003 and SC-004 are met

Both reviews agree that backward compatibility (SC-003) is fully preserved and that timeout fallback (SC-004) produces a heuristic result rather than an error. The test evidence is consistent: `TestScorerHeuristicFallback`, `TestBackwardCompatibility`, and `TestTimeoutFallback` collectively verify these criteria. The disagreement on timeout test mechanism quality (T-1) does not affect the SC-004 verdict -- both agree the behavioral contract is met.

### SA-3: A real-nashopt integration test is needed

Both reviews independently recommend a conditional integration test that exercises the actual nashopt API when available. spec-compliance recommends it in Missed Opportunities #1 as a real-timeout integration test. I recommend it in P2-2 as a `pytest.importorskip` guarded test. The specific implementation differs, but the underlying need -- validating that the mock contract matches the real nashopt API -- is unanimously agreed upon.
