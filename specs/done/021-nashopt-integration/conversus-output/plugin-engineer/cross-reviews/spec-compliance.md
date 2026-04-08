# plugin-engineer Cross-Review of spec-compliance

**Cross-reviewer**: plugin-engineer
**Reviewing**: spec-compliance Phase 1 review of spec 021
**Date**: 2026-04-01

---

## Agreements

### 1. Compliance matrix is clear and useful

The FR-by-FR and SC-by-SC breakdown with status codes (MET, PARTIALLY MET, NOT VERIFIED) provides a clear audit trail. The evidence column links each status to specific code or test artifacts. This format should be used for all premium solver specs.

### 2. FR-001 and FR-002 are correctly classified as MET

The HAS_NASHOPT pattern is standard, tested, and correctly implements both requirements. No disagreement.

### 3. SC-003 assessment is correct

The heuristic code is unchanged. The dispatcher tests confirm identical behavior. MET is the right classification.

---

## Tensions

### 1. FR-007 NOT VERIFIED vs. PARTIALLY MET

spec-compliance says NOT VERIFIED because the timeout code is not in solver.py. I believe this is too conservative. The test file (which IS in the review artifacts) contains explicit timeout tests:
- `TestTimeoutFallback` tests that solver timeout produces heuristic fallback.
- The test uses `concurrent.futures.ThreadPoolExecutor` to simulate timeout.

Tests are evidence. If the tests pass and they test the correct behavior, the feature is at least partially implemented. NOT VERIFIED should be reserved for features where no evidence exists at all.

That said, spec-compliance's point is valid: without the production code, we cannot verify that the tests are testing the *actual* implementation vs. a test-only mock. This is a fair epistemological distinction. I would compromise: classify as PARTIALLY MET with a note that full verification requires scorer.py.

### 2. Constraint verification omission

spec-compliance does not verify the 4 constraints listed in spec section 6. These are not functional requirements -- they are architectural constraints that restrict implementation choices. But they are testable:
- **No core dependency**: Check `pyproject.toml` does not list nashopt/jax.
- **No interface change**: Verify Plugin interface method signatures are unchanged.
- **No heuristic breakage**: Run existing heuristic tests.
- **Independent testability**: Verify solver.py's pure functions work without nashopt.

spec-compliance should include constraint verification in the compliance matrix.

---

## Missed Opportunities

### 1. No assessment of test quality

spec-compliance counts tests per requirement but does not assess test quality. For example:
- Are the cooperative matrix tests sufficient? They test 2 agents. What about 3+ agents?
- Are the red-blue tests robust? They test the severity vector path but the no-severity-vector fallback test uses only 1 red + 1 blue agent.
- Are the degenerate case tests complete? Zero agents, single agent, zero-variance are covered. What about a 2-agent game where both agents have identical features?

Test count is a poor proxy for test quality. A compliance reviewer should assess whether the tests exercise the boundary conditions of each requirement.

### 2. No assessment of error message quality

Several requirements produce error messages (ValueError for unknown modes, RuntimeError for missing nashopt). spec-compliance verifies that errors are raised but does not assess whether the error messages are actionable. "No payoff matrix builder for mode 'unknown-mode'" is good (names the bad input and lists valid options). "nashopt is not installed" is adequate but could include installation instructions.
