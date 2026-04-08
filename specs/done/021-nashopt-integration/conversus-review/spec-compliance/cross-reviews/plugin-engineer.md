# Cross-Review of plugin-engineer's Review

**Cross-reviewer**: spec-compliance
**Reviewing**: plugin-engineer's review of spec 021-nashopt-integration
**Date**: 2026-04-01

---

## Dangerous Contradictions

### DC-1: plugin-engineer marks FR-008 as PARTIAL; the gap is wider than stated

plugin-engineer identifies two error-path `PluginResult` returns that lack the `solver` key (P1-1) and marks FR-008 as PARTIAL. My review marked FR-008 as MET because I traced `_score_from_solver` and `_compute_equilibrium_score_heuristic`, which both set the field. plugin-engineer is correct and I missed the error-path returns entirely. The contradiction matters because FR-008 uses the word "MUST" and "always" -- the spec says the field MUST be present so consumers know which path ran. If error paths omit it, consumers that unconditionally access `result.data["solver"]` crash. plugin-engineer's `"solver": "error"` recommendation is the right fix. I am upgrading my assessment of FR-008 from MET to PARTIALLY MET.

**Resolution**: Accept plugin-engineer's finding. FR-008 is violated on error paths.

### DC-2: Timeout test assessment -- same conclusion, different severity

Both reviews identify the timeout test as not exercising the real `ThreadPoolExecutor` mechanism. However, plugin-engineer classifies this as P1 (Must Fix) while I classified it as P2 (Should Fix). The disagreement is about severity, not substance. plugin-engineer's argument is that the test "is testing the wrong code path" -- the mock raises `TimeoutError` inside the callable rather than from `future.result()`. My argument was that SC-004 is technically met because the fallback behavior is verified even if the trigger mechanism is mocked. From a spec-compliance perspective, SC-004 says "Solver timeout produces a heuristic fallback score, not an error" -- the test does confirm the fallback score is produced, but it does not confirm the timeout triggers correctly. The real danger is a production regression where the `ThreadPoolExecutor` timeout path has a bug (e.g., wrong exception type caught) that goes undetected.

**Resolution**: plugin-engineer's P1 classification is warranted. A test that does not exercise the actual code path it claims to test creates false confidence. Upgrade to P1.

### DC-3: Dead `total_surface` variable vs. potential normalization bug

plugin-engineer flags the dead `total_surface` variable in `_build_rb_matrix` as P1 (P1-3) and notes the `max_k == 0` branch returns raw counts while `max_k > 0` returns severity-weighted ratios (P3-3). My review did not catch this at all. This is dangerous because the scale mismatch between the two branches means nashopt receives payoff matrices with fundamentally different magnitudes depending on whether severity vectors are present. A dead variable that was likely intended to normalize the fallback branch suggests the implementer planned normalization and forgot to apply it. This is not just dead code cleanup -- it may be a correctness bug in the payoff matrix that affects equilibrium computation.

**Resolution**: Accept plugin-engineer's finding but escalate P3-3 to P2. The scale inconsistency between branches is a potential correctness issue for equilibrium computation, not merely a style concern.

### DC-4: Missing SC-001/SC-002 tests -- plugin-engineer's review omits this gap entirely

My review identifies the absence of SC-001 (cooperative convergence >= 0.9) and SC-002 (3+ disputes < 0.5) tests as P1 findings. plugin-engineer's review does not mention success criteria testing at all -- the alignment table only covers FR-001 through FR-008, not SC-001 through SC-004. The spec defines four success criteria as acceptance gates. Without tests for SC-001 and SC-002, the implementation cannot demonstrate it meets its own acceptance criteria. plugin-engineer's review is focused on code-level correctness and misses the spec-level validation gap.

**Resolution**: This is a gap in plugin-engineer's review scope, not a factual contradiction. The SC-001/SC-002 test gap remains P1 per my original assessment.

---

## Tensions

### T-1: FR-005 best-response accuracy -- different root causes identified

Both reviews flag FR-005 as imprecise. I identified the core issue as the blanket "all agents not at equilibrium" fallback at line 438, noting that the `best_responses` dict is already available and could be used to derive accurate per-agent status. plugin-engineer identifies the same fallback but frames it as an "off-base assumption" about the nashopt API surface -- the code checks for `agents_not_at_equilibrium` as an attribute, which is not in the spec's documented API. These are complementary observations pointing at the same problem from different angles. The tension is in the fix: I recommend comparing best responses against current strategies (using data already available), while plugin-engineer's P3-2 focuses on the cooperative diagonal semantics as a separate concern. The actual fix path should address both -- use `best_responses` for per-agent accuracy, and stop relying on an undocumented attribute.

### T-2: Per-agent payoff `0.0` in solver path -- same finding, different priority

Both reviews identify that `_score_from_solver` hardcodes `payoff: 0.0` for all agents. plugin-engineer lists this as P2-1 with a recommendation to either populate real values or document the zero-value contract. I listed it as P2 item 5 with a recommendation to extract payoffs from the payoff matrix or add a `"note"` field. The tension is subtle: plugin-engineer frames the asymmetry as a consumer-facing problem (downstream analytics break), while I frame it as a data fidelity loss (silent zero values). Both are valid, but the consumer-facing framing is more actionable because it identifies who gets hurt.

### T-3: Matrix shape validation -- plugin-engineer raises a concern my review missed

plugin-engineer's P3-1 recommends validating payoff matrix shape before passing to nashopt, noting that different modes produce different shapes (NxN, Nx1, 2xK) and an opaque JAX error would result from shape mismatches. My review did not raise this. The tension is whether this is a real risk: the spec's matrix structure table (Section 2) explicitly documents heterogeneous shapes per mode, and nashopt's `check_equilibrium` signature accepts `np.ndarray` without shape constraints. If nashopt silently produces garbage for non-square matrices rather than raising, this is a correctness issue, not just a usability issue. This deserves at least a P3 in my assessment as well.

### T-4: Conditional integration test -- same recommendation, different framing

plugin-engineer (P2-2) recommends a `pytest.importorskip`-guarded test to validate the mock contract against real nashopt. I listed this under Missed Opportunities (item 1 from plugin-engineer's review maps to my Missed Opportunity 1). The difference is that plugin-engineer frames it as validating "the mock contract matches the real nashopt API" while I frame it as ensuring "the actual timeout path works end-to-end." Both framings are correct and the same test fixture addresses both.

### T-5: ThreadPoolExecutor resource leakage -- only my review raises this

My Off-Base Assumptions item 3 and P3 item 7 flag that a timed-out solver thread continues running in the background, potentially holding GPU/JAX resources. plugin-engineer does not mention this. The spec says nothing about cancellation semantics, so this is not a spec violation, but it is a production risk that a plugin-engineer review should surface. The tension is about review scope: plugin-engineer stayed closer to code correctness while I extended into operational concerns.

---

## Safe Agreements

### SA-1: HAS_NASHOPT flag pattern and heuristic fallback are correctly implemented

Both reviews confirm FR-001 and FR-002 are fully met. The `try/except ImportError` guard, the `HAS_NASHOPT` boolean flag, the `_try_solver` dispatch returning `None` to trigger heuristic fallback, and the backward compatibility with spec 017 are all structurally sound. Neither review found any issue with the import safety or dispatch logic on the happy path.

### SA-2: Degenerate case handling is complete

Both reviews confirm FR-006 is met. Zero-agent, single-agent, and zero-variance cases are all handled before the nashopt call, returning trivial equilibrium results. The test coverage for degenerate cases is adequate in both assessments.

### SA-3: SC-003 and SC-004 are met

Both reviews agree that SC-003 (heuristic behavior unchanged without nashopt) and SC-004 (timeout produces fallback, not error) are met. The caveat on SC-004's test quality is noted in Tensions above, but the behavioral guarantee itself is verified.

### SA-4: Distance normalization formula is correct

Both reviews confirm FR-004 is met. The `max(0.0, min(1.0, raw_distance))` clamping followed by `1.0 - distance` matches the spec formula exactly. Boundary tests for clamping are present and correct.
