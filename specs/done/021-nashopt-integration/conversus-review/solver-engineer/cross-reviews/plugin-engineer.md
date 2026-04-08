# Cross-Review of plugin-engineer's Review

**Cross-reviewer**: solver-engineer
**Reviewing**: plugin-engineer's review of Spec 021 (nashopt Solver Integration)
**Date**: 2026-04-01

---

## Dangerous Contradictions

### DC-1: FR-008 violation severity is understated

plugin-engineer identifies the missing `solver` key on two error paths as P1-1 and correctly cites FR-008. However, plugin-engineer frames this as a `KeyError` risk for consumers and proposes adding `"solver": "unavailable"` or `"solver": "error"`. My review (Alignment, FR-008 bullet) states that both the solver and heuristic paths *do* set `data["solver"]` and that backward-compatibility tests confirm the field is always present. The contradiction: plugin-engineer found paths I did not flag. But the proposed fix is too conservative. Adding a third sentinel value (`"unavailable"` or `"error"`) changes the consumer contract from a binary enum (`"nashopt" | "heuristic"`) to a ternary one. Any downstream consumer that does `if result.data["solver"] == "nashopt"` will silently ignore error cases rather than explicitly handling them. The safer fix is to include `"solver": "heuristic"` on error paths (since no solver ran) or to ensure the error paths never reach consumers at all (raise or short-circuit earlier). A new sentinel without updating the spec's enum is a latent contract violation.

### DC-2: Timeout test criticism is correct but the proposed fix is incomplete

plugin-engineer's P1-2 correctly identifies that the timeout test patches the solver to raise `TimeoutError` directly rather than exercising `future.result(timeout=)`. My review (Off-Base Assumptions, item 2) goes further: I identify that even the production code's `ThreadPoolExecutor.__exit__` calls `shutdown(wait=True)`, meaning the `with` block will block until the timed-out thread finishes, negating the timeout entirely. plugin-engineer's proposed fix (mock with `time.sleep(5)` and a 0.01s timeout) would actually expose my concern, because the test would hang at the `with` block exit. The two findings are complementary but the contradiction is this: plugin-engineer treats the timeout test as a testing gap to fix, while my review identifies the timeout mechanism itself as broken in production. Fixing only the test (as plugin-engineer recommends) without fixing the executor shutdown semantics (as my review recommends in P1-4) would create a test that correctly demonstrates the production bug but does not resolve it. Both fixes are needed together or neither is useful.

### DC-3: Red-blue matrix and winner-take-all shape concerns are absent from plugin-engineer's review

plugin-engineer's review finds that `_build_rb_matrix` has a dead `total_surface` variable (P1-3) and that the cooperative diagonal uses `surviving_count` over agreement data (P3-2). These are real but secondary issues. My review (Missed Opportunities, items 1-3) identifies that the winner-take-all builder produces an N x 1 vector instead of a valid payoff matrix, and that the red-blue builder collapses N agents into 2 rows while the post-processing loop iterates over N agents, causing dimension mismatches. These are structural correctness bugs that will cause runtime failures when nashopt is actually present. plugin-engineer's silence on matrix shape validity is dangerous because it implicitly signals these builders are correct. The dead variable (plugin-engineer P1-3) is cosmetic; the invalid matrix shapes (my review P1-1, P1-2) are crash-or-silent-misattribution bugs. Prioritizing the dead variable as P1 while missing the shape bugs inverts the severity ranking.

---

## Tensions

### T-1: Cooperative diagonal -- agreement on the problem, disagreement on severity

Both reviews flag the cooperative diagonal issue. plugin-engineer lists it as P3-2 ("Consider") with the suggestion to "add a comment explaining why." My review (Missed Opportunities, item 4) classifies it as a semantic inconsistency that "mixes two different payoff semantics in the same matrix, which can produce a non-interpretable game." The tension is in severity: plugin-engineer treats it as a documentation gap; I treat it as a numerical correctness risk. The spec does not define which source is authoritative for self-pair payoffs. Until that is resolved, the implementation is making an undocumented game-theoretic choice that affects solver output.

### T-2: Per-agent payoff zeros -- same finding, different priority

plugin-engineer flags `_score_from_solver` hardcoding `payoff: 0.0` as a Missed Opportunity (item 4) and recommends output parity (P2-1). My review (Missed Opportunities, item 6) flags the same issue but connects it to a broader concern: the information loss "undermines the value of the exact solver" because downstream consumers cannot display gap-to-best-response. My P2-7 recommends computing actual payoffs from the matrix. The tension is that plugin-engineer frames this as an output format inconsistency (fixable by documenting the zero contract), while I frame it as a functional regression (the solver path is strictly less informative than the heuristic path). If we only "document the zero-value contract" as plugin-engineer suggests, we lock in an information deficit that makes the premium solver path less useful than the free heuristic.

### T-3: Integration testing -- aligned goal, different mechanisms

plugin-engineer recommends a `pytest.importorskip` conditional test (P2-2) to validate that "the mock contract matches the real nashopt API." My review (P3-10) recommends an integration test with a known-equilibrium game (e.g., Prisoner's Dilemma with known Nash solution) to verify end-to-end correctness. These are complementary but in tension: plugin-engineer's test validates API shape compatibility, mine validates numerical correctness. Both are needed, but if only one is implemented, mine catches more bugs (a shape-compatible API that returns wrong results would pass plugin-engineer's test but fail mine).

### T-4: Strategy profile dimension mismatch goes unaddressed

My review (Missed Opportunities, item 3) identifies that the fallback strategy profile is a fixed 4-element vector while payoff matrices have mode-dependent action dimensions (N x N, N x 1, 2 x K). This mismatch will cause runtime errors when nashopt validates input dimensions. plugin-engineer's review does not address strategy profile construction at all. This is not a contradiction but a significant gap: the payoff matrix validation plugin-engineer suggests at P3-1 ("validate payoff matrix shape before passing to nashopt") would catch the symptom, but the root cause is that strategy profiles and payoff matrices are constructed independently without shared knowledge of the action space.

### T-5: Score incomparability between solver and heuristic paths

My review (Missed Opportunities, item 5) identifies that the heuristic scores as `agents_at_eq / total_agents` (discrete fraction) while the solver scores as `1.0 - distance` (continuous metric), making scores discontinuously jump on timeout fallback. plugin-engineer's review does not address score comparability. This is a consumer-facing issue: any dashboard or threshold that consumes the score will behave unpredictably when the solver path times out mid-session and the scoring regime changes.

---

## Safe Agreements

### SA-1: `PluginResult.data["solver"]` must be present on all paths

Both reviews agree this field must always be populated per FR-008. plugin-engineer found it missing on two error paths (P1-1); my review confirmed it present on the two happy paths (Alignment, FR-008). Combining both findings: the field is present on happy paths and absent on error paths. This is a clear spec violation that both reviews independently confirm must be fixed.

### SA-2: The import guard and heuristic fallback are correctly implemented

plugin-engineer's Alignment table marks FR-001 and FR-002 as PASS. My review (Alignment, first bullet) confirms the `HAS_NASHOPT` flag pattern and seamless fallback. Both reviews agree the spec 017 backward-compatibility contract is fully preserved: same plugin name, same hooks, same output fields, byte-identical behavior when nashopt is absent.

### SA-3: Degenerate case handling is sound

plugin-engineer's Alignment table marks FR-006 as PASS. My review (Alignment, FR-006 bullet) confirms n=0, n=1, and zero-variance are all handled before the nashopt call with sensible trivial-equilibrium results and adequate test coverage. Neither review found issues with the degenerate path logic itself.

---

## Summary

plugin-engineer's review is thorough on plugin architecture concerns (flag patterns, dispatch, backward compatibility, import safety) and catches real issues (missing solver key, dead variable, timeout test gap). The dangerous gap is the absence of any analysis of payoff matrix shape validity and strategy profile dimensionality -- these are the issues most likely to cause production failures when nashopt is actually installed and exercised. The timeout analysis stops at the test layer without recognizing that the production mechanism itself is broken. Severity calibration should be adjusted: the dead `total_surface` variable (plugin-engineer P1-3) is at most P3; the matrix shape bugs (my P1-1, P1-2) and executor shutdown semantics (my P1-4) should be the true P1 priorities.
