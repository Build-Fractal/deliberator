<!--
PR template for deliberator.

The "Test fixes" section is BINDING for any PR that modifies a test
file (Principle XXVIII, ratified v2.5.0; see CONSTITUTION.md and
spec 071). The lint at `scripts/lint-test-fixes.py` reads the
machine-readable marker in that section.

Other sections are conventions. Delete what you don't need.
-->

## Summary

<!-- 1-3 bullets: what changed and why. -->

## Test plan

- [ ] <!-- test plan items -->

## Test fixes (required if any test file is modified)

If this PR fixes a failing test (Principle XXVIII), declare the
category in the machine-readable marker below. If multiple test
fixes span different categories, list one marker per fix.

<!-- test-fix-category: fixture-drift | production-bug | legitimate-test-bug | defunct-test -->

Self-check (each box must be ticked or the PR violates Principle
XXVIII; `scripts/lint-test-fixes.py` reads the marker above to
verify diff-shape consistency):

- [ ] The category marker above declares each test fix
- [ ] The diff shape matches the declared category
  - **fixture-drift**: only test files modified
  - **production-bug**: ≥1 production-source file modified
  - **legitimate-test-bug**: only test files modified + PR body cites the test-side bug
  - **defunct-test**: test deletion (not modification) + PR body explains why the behavior is no longer relevant
- [ ] Any newly added `pytest.skip` / `@pytest.mark.skip` cites the
  bug (issue or PR number) + remediation timeline
- [ ] Assertion-fidelity discipline (Principle IX behavior-over-shape)
  preserved; loosened assertions, if any, are justified inline
- [ ] If `scripts/lint-test-fixes.py` flagged anything, the flag is
  justified

If no test files are modified, mark this section N/A and proceed.
