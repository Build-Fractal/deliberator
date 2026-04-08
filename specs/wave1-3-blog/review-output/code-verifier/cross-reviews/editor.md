# Cross-Review of Technical Editor's Review

**Cross-reviewer**: code-verifier
**Date**: 2026-04-03
**Reviewing**: `review-output/editor/review.md`
**Method**: Compared editor's claims against source code and my own verified findings.

---

## Overall Assessment

The editor's review is thorough and well-structured. The narrative and style assessments (Sections 1, 3, 4, 6) are outside my verification scope -- those are editorial judgments. My evaluation focuses on the technical accuracy claims (Section 2), code block assessment (Section 7), and the frontmatter validation (Section 5).

**Verdict**: The editor's P1/P2 issues are largely well-grounded, with one significant omission.

---

## Issue-by-Issue Evaluation

### ISSUE 2.1 (P1): "pip install not on PyPI" -- ACCURATE

The editor says Post 04 implies `pip install conversus` works today, and a reader would get a 404. Confirmed: `https://pypi.org/pypi/conversus/json` returns HTTP 404. The package is not published. The build script (`scripts/build-packages.sh`) builds local wheels only. The qualifying sentence the editor quotes ("PyPI publication is a separate step") is indeed buried at the end after multiple unqualified `pip install` references.

**Agreement**: Full. This is a legitimate P1. The editor's recommendation (callout box or framing change) is reasonable.

### ISSUE 2.2 (P2): AMPL claims -- ACCURATE

The editor says "AMPL infrastructure exists" is correctly qualified but potentially confusing. My review independently verified this: `conversus/plugins/optimizer/` contains the config optimizer infrastructure (6 files including `ampl_model.py`, `ampl_solver.py`), but no per-mode game-form templates exist yet. The editor's recommended clarifying sentence is helpful and consistent with my findings.

**Agreement**: Full.

### ISSUE 2.3 (P2): Kalman filter claim -- ACCURATE

The editor correctly notes this is properly qualified and flags the risk of code removal before publication. My review confirmed `conversus/plugins/nashopt/kalman.py` exists. The editor's "flagging for awareness" posture is appropriate.

**Agreement**: Full.

### ISSUE 2.4 (P1): "43 specs" count -- ACCURATE BUT CURRENTLY CORRECT

The editor says "43 specs" may be stale by publication. I counted 43 folders in `specs/done/` today, so the claim is currently accurate. The editor is right that spec counts drift quickly (there are 5 additional numbered specs in the active pipeline: 040-044). This is a valid publication-time verification step, but calling it P1 "must fix before publishing" slightly overstates the current severity. It is not wrong today; it is a freshness risk.

**Slight disagreement**: P2 (verify at publication time) would be more appropriate than P1, since the claim is factually correct as of today.

### ISSUE 3.2 (P2): Tonal shift -- EDITORIAL JUDGMENT

Outside my technical verification scope. The observation about "enterprise-grade" language is a style call, not a code-verifiable claim.

### ISSUE 5.1 (P2): Same-date posts -- ACCURATE

MkDocs Material will indeed render both posts on the same index date. This is a configuration fact, not a code claim. Valid.

### ISSUE 7.1 (P3): `FileNotFoundError(...)` placeholder -- ACCURATE

The actual code (`conversus/paths.py` line ~82) has a full error message. The blog truncates it to `...`. This is standard blog practice; the editor correctly rates it P3.

### ISSUE 7.2 (P2): Missing context for `RoundFeatures` -- REASONABLE

The editor suggests adding a one-line comment explaining `RoundFeatures`. This is an editorial recommendation about reader experience, not a factual error. Reasonable at P2.

### ISSUE 8.1 (P1): Post 05 missing explicit CTA -- EDITORIAL JUDGMENT

Not a code-verifiable claim. The editor's observation that Post 05 has no closing install/quickstart link is a structural assessment. Reasonable recommendation.

---

## Critical Omission: Entry Point Bug

**The editor's review does not flag the `core.toml` entry point issue at all.** This is the most significant gap in the editor's review.

The synthesis document's Section 4 identifies P1-3: `pyproject.toml` declares `engine.cli:cli` while `packages/core.toml` declares `engine.cli:main`. My review (Section 8) confirmed this is a build-breaking bug: the committed version of `core.toml` (commit `df70d95`) has `conversus = "engine.cli:main"`, but no `main` function exists anywhere in `engine/cli/`. A `pip install conversus` built from the committed `core.toml` would produce a non-functional CLI.

Note: There is an uncommitted local fix (`git diff -- packages/core.toml` shows the change from `engine.cli:main` to `engine.cli:cli`), which means the working copy is now correct. But the committed state is broken. This fix must be committed before any wheel is published.

The editor's review covers accuracy, consistency, style, frontmatter, code blocks, and CTA -- but skips the doc fix dependency chain's P1-3 entirely. Given the editor evaluated Section 4 of the synthesis (they reference it in Section 3 and call the dependency correctly: "doc fixes -> blog publication"), the entry point bug should have appeared in the P1 table.

---

## Agreement Between Editor and Code-Verifier Reviews

| Topic | Editor | Code-Verifier | Agreement |
|---|---|---|---|
| PyPI not live | P1 (Issue 2.1) | Not separately flagged (blog content scope) | Aligned -- editor caught it |
| AMPL qualification | P2 (Issue 2.2) | PASS with "properly qualified" note | Aligned |
| Kalman qualification | P2 (Issue 2.3) | PASS with existence confirmed | Aligned |
| 43 specs freshness | P1 (Issue 2.4) | Not flagged | Editor is more cautious; I agree on the risk but call it P2 |
| Entry point bug | NOT FLAGGED | P1 blocking (Section 8) | **Divergence** -- editor missed it |
| `core.toml` exclusion simplification | Not flagged | Non-blocking note | No conflict |
| "All 8 modes" CLI subset | Not flagged | Non-blocking note (9c) | No conflict |
| Payoff formula accuracy | Verified correct list (Section 2) | PASS -- all 8 verified | Aligned |
| 31 split tests | Verified correct (Section 2) | PASS -- exact match | Aligned |
| Code block syntax | P3 notes (Section 7) | Not separately assessed | No conflict |
| Post 05 CTA | P1 (Issue 8.1) | Not in scope | No conflict |
| Tonal shift | P2 (Issue 3.2) | Not in scope | No conflict |

---

## Summary

The editor's review is well-executed for its scope (narrative quality, accuracy of claims, cross-post consistency, style matching, frontmatter). The PyPI concern (Issue 2.1) is fully accurate and important. The AMPL and Kalman qualifications are correctly assessed.

The one material gap is the omission of the `core.toml` entry point bug. This is the only issue across both reviews that would cause a runtime failure for end users, and it needs to be on the P1 list regardless of which reviewer catches it. The uncommitted fix on disk indicates someone already addressed it, but it has not been committed -- publication depends on that fix shipping.

**Recommendation**: Merge the editor's P1 table with my Section 8 finding. The combined P1 list for publication readiness is:

1. PyPI availability framing (editor Issue 2.1)
2. Entry point fix must be committed (code-verifier Section 8)
3. Post 05 CTA (editor Issue 8.1)
4. Spec count verification at publication time (editor Issue 2.4, suggest downgrade to P2)
