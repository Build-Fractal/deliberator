# Code Verification Review: Revision

**Reviewer**: code-verifier
**Date**: 2026-04-03
**Revision basis**: Original review + cross-reviews from user-advocate and editor
**Scope**: Verify every technical claim in the two blog posts and 12 doc fix recommendations against the actual source code. Revised to incorporate cross-reviewer feedback and correct one factual error in the original review.

---

## Correction Notice

**The original review's Section 8 ("Entry Point Inconsistency") contained a factual error.** The original review stated that `packages/core.toml` line 23 declares `conversus = "engine.cli:main"`, which does not exist, and classified this as a build-breaking bug. Subsequent cross-review work (code-verifier cross-review of user-advocate) discovered that `core.toml` now reads `conversus = "engine.cli:cli"`, matching `pyproject.toml`. The synthesis document's P1-3 was based on a stale reading. The fix is present in the working copy. **P1-3 is CLOSED -- no inconsistency exists in the current code.**

---

## 1. Payoff Formulas (Blog Posts vs `conversus/plugins/nashopt/payoffs.py`)

### Verdict: PASS

All 8 payoff formulas verified exact against source code. No changes from original review.

| Payoff function | Blog claim | Code match |
|---|---|---|
| Negotiation | `zopa_coverage * party_satisfaction` | Exact (line 243) |
| Prisoners-dilemma | `territory - gamma * overreach_penalty` | Exact (lines 124-146) |
| Cooperative | `surviving_count` | Exact (line 39) |
| Winner-take-all | `1 if winner else 0` | Exact (line 77) |
| Resource-allocation | `utilization_efficiency - allocation_inequality` | Exact (line 273) |
| Fair-division | `proportionality - normalized_envy` | Exact (lines 306-308) |
| Mechanism-design | `social_welfare - gaming_vulnerability` | Exact (lines 339-342) |
| Red-blue | Severity-weighted attack/mitigation | Exact (lines 183-218) |

**`(payoff, best_response_payoff)` interface**: All 8 return `tuple[float, float]`. The `compute_payoff` dispatcher (line 367) preserves this. Confirmed.

**Cross-reviewer note (user-advocate)**: The formulas are accurate but opaque to non-specialist readers. The user-advocate correctly observes that "technically accurate" does not mean "reader-ready." A reader who has not taken a game theory course will not know what ZOPA coverage means or why `party_satisfaction` matters. The code-verifier's PASS means the blog does not lie; it does not mean the blog teaches. This distinction matters for editorial decisions -- the payoff formulas section needs pedagogical work even though it needs no factual corrections.

---

## 2. Package Configs (`packages/*.toml`)

### Verdict: PASS (with simplification note)

No changes from original review. Four TOML files exist and match the blog's description. Two findings carry forward:

**`core.toml` exclusions**: Blog mentions 2 of 4 exclusion patterns (`nashopt`, `optimizer`), omitting `scenarios` and `domains/implementations`. This is a simplification, not a falsehood. However, the user-advocate and editor both note that simplifications a reader can easily verify erode trust when the reader finds discrepancies. Recommend adding "and other premium modules" or listing all four.

**Entry point**: Both `pyproject.toml` (line 24) and `core.toml` (line 23) now declare `conversus = "engine.cli:cli"`. No inconsistency. P1-3 is CLOSED.

---

## 3. `paths.py` Description vs Actual Module

### Verdict: PASS

No changes from original review. Blog code is the actual code with docstring removed and error message abbreviated. "importlib.resources since Python 3.9" is correct. Module is 165 lines (blog said 164; difference is a trailing newline).

---

## 4. Test Counts

### Verdict: PASS

No changes from original review. 31 split tests (14 functions, parametrize expansion) and 4 free-tier tests verified exact.

**Cross-reviewer note (user-advocate)**: The test count verification is internally valuable but reader-irrelevant. Nobody will expand parametrize decorators. The editorial question is whether a reader knows what a "split test" is testing, not whether 31 is the right number.

---

## 5. Free/Paid Boundary

### Verdict: PASS (with simplification note)

No changes from original review. The blog's free-tier module list is a subset of the actual `PAID_MODULES` test list (5 modules named vs 8 tested). This is the same simplification pattern noted in Section 2. Individually minor; as the user-advocate points out, the pattern suggests the posts were verified for accuracy but not for verifiability.

---

## 6. AMPL Claims

### Verdict: PASS (properly qualified)

No changes from original review. AMPL infrastructure exists. Config optimizer exists. Per-mode model templates do not exist yet. The blog's "future" qualifier is load-bearing and accurate.

---

## 7. Doc Fix Recommendations vs Actual Gaps

### Verdict: PASS -- All 12 recommendations target real gaps

No changes from original review for P0-1, P0-2, P1-1, P1-2, P2-1 through P2-3, P3-1 through P3-3. All verified against actual docs.

**P1-3 update**: CLOSED. The entry point is consistent across both files. The synthesis P1-3 was based on a stale reading. No code fix or doc fix needed.

**NEW FINDING -- README is unaddressed in doc fixes.** The 12 doc fix recommendations cover `docs/index.md`, `docs/user-guide/quickstart.md`, `docs/user-guide/sdk.md`, `docs/user-guide/config-reference.md`, `docs/user-guide/cli.md`, and architecture docs. They do not address `README.md`, which has its own set of issues:

- Line 5: "four competition modes" -- but line 13 lists 8 modes. Internal inconsistency within the README itself.
- Line 29: `git clone <repo-url>` -- generic placeholder, does not use the Build-Fractal org URL that `mkdocs.yml` declares.
- Line 51: `uv sync` -- no `pip install conversus` path, same gap as `docs/index.md` (P0-1).
- Line 58: Links to `docs/cli.md` -- may not resolve correctly depending on the reading surface (GitHub vs MkDocs).

The user-advocate cross-review (Section 6, recommendations table) flags "Address README separately" as a valid gap not caught by other reviews. The editor cross-review does not mention it. Since the README is the first thing a GitHub visitor sees, its gaps deserve at least a P2 doc fix recommendation.

---

## 8. Entry Point Inconsistency (`cli` vs `main`)

### Verdict: CLOSED -- NO INCONSISTENCY EXISTS

**Original review claimed**: `core.toml` references `engine.cli:main`, which does not exist, making this a build-breaking bug.

**Revised finding**: Both `pyproject.toml` line 24 and `packages/core.toml` line 23 declare `conversus = "engine.cli:cli"`. The `cli` callable is the Click group defined at `engine/cli/__init__.py` line 75. There is no inconsistency and no broken entry point.

The original review's error was inherited from the synthesis document's P1-3, which was based on a stale or incorrect reading of `core.toml`. The code-verifier's cross-review of the user-advocate (Section 4b) identified this error. The editor's cross-review (Section 4a) notes that commit `df70d95` had `engine.cli:main` but an uncommitted fix changed it to `engine.cli:cli` -- meaning the fix was in the working copy at the time of the original review but was not the committed state. Regardless, the current state is correct.

**P1-3 is closed. No action required.**

---

## 9. Additional Findings

### 9a. Python version discrepancy -- correctly handled

No change. `core.toml` requires `>=3.11`, `pyproject.toml` requires `>=3.12`. The doc fix P1-1 handles this with the note "Two Python version numbers are intentional."

### 9b. "Seven files with `Path(__file__).parent`" claim

No change. Unverifiable post-fix but plausible and consistent with the narrative.

### 9c. `decide` command mode restriction -- PROMOTED TO STANDALONE FINDING

**Original review**: Listed as non-blocking issue #2.
**Revised assessment**: Promoted based on user-advocate and editor cross-reviews.

The `decide` CLI command (`engine/cli/__init__.py` lines 240-242) restricts `--mode` to 4 choices:

```python
type=click.Choice(
    ["cooperative", "winner-take-all", "prisoners-dilemma", "red-blue"],
    case_sensitive=False,
),
```

All 8 modes are available via `conversus run` with a config file, as `docs/index.md` line 62 correctly notes: "The CLI `decide` command supports 4 modes for quick ad-hoc use; all 8 are available via config files."

The blog (Post 04, line ~247) says: "The free tier (`pip install conversus`) ships the complete deliberation engine. All 8 modes."

This is technically true at the engine level but misleading at the CLI surface. A reader who installs the free tier and runs `conversus decide --mode negotiation` will get a Click error. The user-advocate calls this a "first-run failure caused directly by the blog's claim" and recommends reclassifying from non-blocking to blocking. The editor recommends promoting to P2 with a one-sentence fix: "All 8 modes are available via config files; the `decide` CLI command supports the original four for quick ad-hoc use."

**The `linter/validate.py` CLI (line 435) has the same 4-mode restriction**, confirming this is a deliberate design choice, not an oversight. The 4 new modes (negotiation, resource-allocation, fair-division, mechanism-design) are config-file-only. This makes the blog's "all 8 modes" claim accurate for the engine but inaccurate for the CLI experience a reader will try first.

Additionally, the `README.md` (line 5) says "four competition modes" while line 13 lists all 8. This internal inconsistency within the README compounds the confusion.

### 9d. Blog Post categories

No change. Both posts use valid `mkdocs.yml` categories.

---

## Revised Summary Scorecard

| # | Claim | Verdict | Change from original |
|---|-------|---------|---------------------|
| 1 | Payoff formulas match code | PASS | Unchanged. Added note: accurate but not reader-ready. |
| 2 | Package configs match | PASS | Unchanged. Simplification note carries forward. |
| 3 | `paths.py` description accurate | PASS | Unchanged. |
| 4 | 31 split tests | PASS | Unchanged. |
| 5 | 4 free-tier tests | PASS | Unchanged. |
| 6 | Free/paid boundary correct | PASS | Unchanged. |
| 7 | AMPL claims qualified | PASS | Unchanged. |
| 8 | Kalman claims qualified | PASS | Unchanged. |
| 9 | Doc fixes target real gaps | PASS | Unchanged. README gap added. |
| 10 | Entry point inconsistency | **CLOSED** | **Changed from CONFIRMED BROKEN.** No inconsistency in current code. |
| 11 | `estimate_cost` duplication | PASS | Unchanged. |
| 12 | Blog categories valid | PASS | Unchanged. |
| 13 | `decide` CLI 4/8 modes | **NEW** | Blog says "all 8 modes"; CLI only accepts 4. |

---

## Revised Blocking Issues

**None.** The original blocking issue (entry point) is resolved.

## Revised Non-Blocking Issues (prioritized)

1. **`decide` CLI 4/8 mode discrepancy (P2).** The blog says "all 8 modes" in the free tier. The `decide` CLI accepts only 4. A reader's first CLI experiment after reading the blog may fail. Add one sentence clarifying that `decide` supports 4 modes while `conversus run` supports all 8 via config files.

2. **README not addressed in doc fixes (P2).** The README has stale content ("four competition modes" vs 8 listed), a generic clone URL, and no `pip install` path. The 12 doc fix recommendations do not cover it. Add a P2 recommendation for README alignment.

3. **`core.toml` exclusion simplification (P3).** Blog mentions 2 of 4 exclusion patterns. Add "and other premium modules" or list all four.

4. **Free-tier module list simplification (P3).** Blog names 5 paid modules; tests check 8. Same simplification pattern as #3.

5. **"Seven files" claim unverifiable (P3).** Pre-fix state not visible in current code. Plausible and consistent but cannot be confirmed.

---

## Response to Cross-Reviews

### To user-advocate

The user-advocate's central argument -- that "technically accurate" does not mean "reader-ready" -- is correct and well-articulated. The original review operated on the assumption that accuracy equals quality. It does not. The revised review preserves the accuracy verdicts but adds explicit notes where accuracy and comprehensibility diverge (Sections 1 and 4). The recommendation to reclassify the "all 8 modes" oversimplification has been adopted (Section 9c, promoted to standalone finding). The point about simplification-as-trust-erosion (Sections 2 and 5 of the cross-review) is acknowledged as a pattern -- the two simplification findings are individually minor but together suggest the posts were not reviewed for verifiability.

The user-advocate is right that the code-verifier's clean scorecard should not be read as "ready to publish." A synthesis team needs both accuracy (code-verifier) and accessibility (user-advocate) to pass.

### To editor

The editor's cross-review correctly identifies that the entry point bug is a code fix, not a blog fix, and that the dependency chain tightens. With the entry point now fixed in the working copy, the dependency chain reverts to: (1) commit the `core.toml` fix, (2) ship doc fixes P0-1/P0-2/P1-1/P1-2, (3) publish blog posts. The editor's promotion of the "all 8 modes" issue to P2 is adopted. The editor's observation that the seven-files claim is "editorially acceptable" (before/after narratives are normal in blog posts) is agreed.
