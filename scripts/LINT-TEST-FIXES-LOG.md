# Lint-Test-Fixes False-Positive Tracking Log

**Origin**: spec 071 §11 Q1 — `scripts/lint-test-fixes.py` (PR #49) ships
in advisory mode (`continue-on-error: true`) until its false-positive
rate stabilizes. This log is the data-collection mechanism that
informs the advisory → blocking promotion decision.

## Tracker

- **Lint introduced**: 2026-04-29 (PR #49 merged Principle XXVIII
  enforcement scaffolding)
- **Earliest promotion review**: 2026-07-29 (3 months from intro)
- **Latest promotion review**: 2026-10-29 (6 months from intro)
- **Promotion criteria** (ALL must hold):
  - ≥ 30 PRs have triggered the lint OR should have triggered it
    (sufficient sample size)
  - False-positive rate ≤ 10%
  - No false-negatives where reviewers determine "lint should have
    caught it"
  - No outstanding issues against the lint script's correctness

If criteria aren't met by 2026-10-29, file a new issue documenting why
the lint stays advisory (e.g., insufficient sample, FP rate too high,
heuristic needs revision).

## How to log a verdict

When a PR triggers the lint, append a row to the table below:

| PR | Date | Verdict | Notes |
|----|------|---------|-------|
| #N | YYYY-MM-DD | `true-positive` / `false-positive` / `true-negative` / `false-negative` | (brief description if non-trivial) |

**Verdict definitions** (from spec 071 §11 Q1):

- **true-positive**: lint flagged a real Principle XXVIII violation
  (skip-discipline gap or diff-shape inconsistency that the lint
  caught and a human reviewer confirmed).
- **false-positive**: lint flagged something that a human reviewer
  determined was legitimate (e.g., a fix that looked like
  skip-discipline-skip but was actually a deletion of an obsolete
  test).
- **true-negative**: lint was silent on a clean PR (no test-fix
  changes, or test-fix changes that genuinely satisfied the
  discipline). These are the common case and usually don't need
  logging unless the PR was illuminating in some way.
- **false-negative**: PR contained a Principle XXVIII violation that
  the lint did not flag. Surfaced after-the-fact by code review or
  bug investigation.

## Log

| PR | Date | Verdict | Notes |
|----|------|---------|-------|
<!-- New entries appended here. Maintain reverse-chronological order: most recent first. -->

## Periodic review checklist

When a maintainer reviews this log for promotion eligibility, verify:

1. Sample size ≥ 30 PRs triggering or that should have triggered.
2. FP rate ≤ 10% (count `false-positive` ÷ total flagged PRs).
3. No false-negatives that the maintainer judges "should have been
   caught."
4. No outstanding lint-correctness issues open against
   `scripts/lint-test-fixes.py`.

If all four hold, file a follow-up PR promoting `continue-on-error:
true` → `false` in `.github/workflows/lint-test-fixes.yml`. Update this
log's "Lint introduced" section with the promotion date.

## Cross-refs

- Spec 071 §11 Q1 — the deferred promotion question
- PR #49 — introduced the lint in advisory mode
- PR #46 — Principle XXVIII ratification (constitution v2.4.0 → v2.5.0)
- Issue #57 — this log's tracker
