# Cross-Review: docs-updater's Gap Analysis

**Reviewer**: technical-writer
**Reviewing**: docs-updater/review.md
**Date**: 2026-04-03

---

## Overall Assessment

The docs-updater's review is thorough and well-evidenced. All six gaps are grounded in actual file contents with correct line references. The severity ratings are reasonable. I agree with the overall direction and have three corrections, two additions, and one priority reordering to propose.

---

## Gap-by-Gap Evaluation

### Gap 1: Missing `pip install` path (CRITICAL) -- AGREE WITH CORRECTION

The gap is real. `docs/index.md` line 28-31 still shows `git clone` + `uv sync` as the only install method.

However, there is an important nuance the docs-updater missed. Blog Post 3 ("31 Fixes From a 55-Agent Review") line 59 says the *opposite* fix was shipped:

> **Install path fix** -- Index page changed from `pip install conversus` to `git clone` + `uv sync`

This means the current state of `docs/index.md` is the **intentional result** of the earlier documentation review. The earlier review caught that `pip install conversus` was on the index page *before the package was actually published to PyPI*, and correctly changed it to the source install to avoid misleading users.

Now that spec 032 (build-time package splitting) has shipped, the fix direction reverses: `pip install conversus` should become the primary path again. But the docs-updater's framing -- that this was simply "missed" -- is wrong. It was deliberately changed *away* from pip install, and needs to be deliberately changed *back* now that the packaging infrastructure is in place.

The proposed replacement text is good. One correction: the docs-updater's example shows `pip install conversus-solvers` and `pip install conversus[all]`, but `packages/core.toml` line 20 defines the `all` extra as depending on three separate packages (`conversus-solvers`, `conversus-scenarios`, `conversus-swe`). The proposed text should clarify that `conversus[all]` pulls in all sub-packages, not just solvers.

### Gap 2: Stale `clariti-care` org references (CRITICAL) -- AGREE FULLY

Confirmed. `mkdocs.yml` lines 3-5 already use `Build-Fractal`. The three `clariti-care` URLs in `docs/index.md` (lines 10, 11, 29) are stale. The `.do/app.yaml` line 10 is also stale.

The license badge fix ("proprietary" to "MIT") is correct: `packages/core.toml` line 10 declares `license = "MIT"` for the free tier, while `packages/solvers.toml` line 9 declares `license = "LicenseRef-Proprietary"` for the paid tier. The index badge should reflect the core package license.

I have nothing to add here. This is a straightforward find-and-replace.

### Gap 3: Quickstart install path (MEDIUM) -- AGREE WITH CORRECTION

The gap is real. The quickstart still shows only the dev workflow.

Correction on Python version: the docs-updater says to reconcile to "3.11+" because `packages/core.toml` says `>=3.11`. But the root `pyproject.toml` (the development config) says `requires-python = ">=3.12"`. The two files serve different purposes:

- `pyproject.toml` (root): development install, includes all dependencies (anthropic, fastapi, supabase, etc.)
- `packages/core.toml`: published `pip install conversus` package, minimal dependencies

It is plausible that the core package genuinely supports 3.11 (its dependencies are lighter: pydantic, pyyaml, click) while the full development environment requires 3.12. The quickstart should distinguish:

- `pip install conversus`: Python 3.11+
- Development from source (`uv sync`): Python 3.12+

The docs-updater's blanket "reconcile to 3.11+" is too simple. Both numbers may be correct for their respective contexts.

### Gap 4: No free/paid boundary callout in config-reference.md (MEDIUM) -- AGREE

The gap is real. The `plugins:` section at line 144-175 shows `equilibrium-scorer` and `scenario-runner` examples without any indication that these require a separate paid package. The blog posts (both Post 1 and Post 2) explain the free/paid boundary in detail, but the config reference -- the page users actually consult when writing configs -- says nothing about it.

The proposed callout text is good. I would make one adjustment: the callout should also mention that plugin import failures are gracefully handled (this is already documented at line 175: "If a `package` cannot be imported (not installed), a warning is logged and that plugin is skipped"), so the callout can cross-reference that behavior:

```
!!! info "Premium Feature"
    The `equilibrium-scorer` and `scenario-runner` plugins require the paid
    `conversus-solvers` package. Install with `pip install conversus-solvers`.
    Without it, these plugins are skipped (see note above) and the deliberation
    completes normally without scoring.
```

### Gap 5: modes.md payoff functions (NO ACTION) -- AGREE

Confirmed complete. I verified all four formulas against the actual code:

- `negotiation_payoff()` at payoffs.py line 225 -- matches
- `resource_allocation_payoff()` at payoffs.py line 255 -- matches
- `fair_division_payoff()` at payoffs.py line 285 -- matches
- `mechanism_design_payoff()` at payoffs.py line 320 -- matches

Note: the docs-updater's line references for payoffs.py are slightly off (they cite 243, 273, 306, 340 -- these may be from an earlier version of the file). The modes.md line references are also slightly off from what I see in the current file (e.g., negotiation scoring is at line 109, not line 109 -- OK, that one matches). Regardless, the content is correct.

### Gap 6: Design system not documented (LOW) -- AGREE, DEPRIORITIZE

The gap exists. The proposed addition to the contributing guide is well-structured. I would deprioritize this further -- it has no bearing on blog post accuracy and is a nice-to-have for contributor onboarding.

---

## Gaps the Docs-Updater Missed

### Missed Gap A: Blog Post 2 uses disallowed MkDocs category (MEDIUM)

Blog Post 2 (the technical writer's review file, which contains the draft blog posts) uses `Architecture` as a category:

```yaml
categories:
  - Engineering
  - Architecture
```

But `mkdocs.yml` line 40-43 only allows three categories: `Engineering`, `Process`, `Release`. The MkDocs blog plugin will either error or silently drop the post if `Architecture` is not in `categories_allowed`. This must be fixed before publishing -- either add `Architecture` to `mkdocs.yml` or change the category to one of the allowed values.

### Missed Gap B: CLI reference install note is stale (LOW)

`docs/user-guide/cli.md` line 5-6 says:

> If you installed via `uv sync` (recommended), prefix commands with `uv run`. If you installed via `pip install -e .`, use `conversus` directly.

With the package split shipped, this should mention `pip install conversus` (not just `pip install -e .`). After a PyPI install, users run `conversus` directly -- no `uv run` prefix needed. This is a minor consistency fix but reinforces the new install path.

### Missed Gap C: `conversus/paths.py` not documented in architecture.md (LOW)

Blog Post 1 describes `conversus/paths.py` as the central path resolution module -- the key deliverable of Wave 2 (MIT-1). But `docs/developer-guide/architecture.md` does not mention it. The architecture page lists every package and its contents (lines 34-44) but `conversus/paths.py` is absent from the `conversus/` row. For developers extending the codebase, knowing about `resolve_package_path()` is important -- it is the required mechanism for locating data files and replaces `Path(__file__).parent` traversal.

### Missed Gap D: Blog Post 1 test count may be inaccurate (INFORMATIONAL)

Blog Post 1 claims "31 tests prove independence" in `test_package_split.py`. The file has 14 test functions, expanded via `@pytest.mark.parametrize` to more cases. The actual parametrized count depends on the module lists (`SCHEMAS_MODULES`, `PLUGINS_FRAMEWORK_MODULES`, etc.) and may or may not total 31. This should be verified before publishing to avoid a factual error in the blog.

---

## Inconsistencies Between Blog Posts and Docs

### 1. Install path narrative contradiction

Blog Post 3 says the install path was changed FROM `pip install` TO `git clone` + `uv sync`. Blog Post 1 says the goal of the entire Wave 2-3 effort was to make `pip install conversus` work. These are chronologically consistent (Post 3 describes earlier work, Post 1 describes later work) but a reader encountering both posts will find it confusing without a bridging sentence. Blog Post 1 should acknowledge that the docs were previously corrected to remove a premature `pip install` reference, and now the pip path is being restored because the packaging work is complete.

### 2. Python version in blog vs. docs

Blog Post 1 does not specify a minimum Python version. The quickstart says 3.12+. The core package says 3.11+. The index badge says 3.12+. Blog Post 2 does not address this. If the blog posts reference Python version requirements, they should use the core package's 3.11+ figure since they describe the pip-installable package.

### 3. Solver fallback chain description vs. install commands

Blog Post 2 describes the three-tier solver fallback and shows install commands:

```
Tier 2 (AMPL)      -> pip install conversus-solvers[ampl]
Tier 3 (nashopt)   -> pip install conversus-solvers[nashopt]
```

These extras match `packages/solvers.toml` lines 17-19 (`nashopt = [...]`, `ampl = [...]`). But nowhere in the docs is this extras syntax documented. The config reference shows the plugin config but not how to install the specific solver backends. This should be added to either the config reference or the modes page alongside the "Solver scoring" paragraphs.

---

## Priority Ranking for Pre-Publication Fixes

Ordered by impact on reader trust if the blog posts go live with the current docs state:

| Priority | Item | Why |
|----------|------|-----|
| P0 | Gap 2: `clariti-care` URLs | Readers who click any badge link or try to clone from the blog's context hit a wrong org. Trivial fix. |
| P0 | Missed Gap A: Blog Post 2 category | `Architecture` not in `categories_allowed`. MkDocs build will fail or silently drop the post. |
| P1 | Gap 1: Add `pip install` to index | Blog Post 1's entire narrative culminates in "pip install conversus now works." If a reader visits the index page and sees `git clone`, the blog's credibility is undermined. |
| P1 | Gap 3: Quickstart install path | Same reasoning as Gap 1 -- the quickstart is the second page new readers visit. |
| P2 | Gap 4: Free/paid callout in config reference | Blog Post 1 explains the boundary clearly. The config reference should match, but the mismatch is less likely to cause confusion for readers coming from the blog. |
| P2 | Inconsistency 3: Solver install extras not documented | Blog Post 2 shows `pip install conversus-solvers[ampl]` which has no corresponding docs page. Readers will look for documentation on the extras syntax. |
| P3 | Missed Gap B: CLI reference install note | Minor consistency fix. |
| P3 | Missed Gap C: `paths.py` not in architecture docs | Developer-facing, low reader impact. |
| P3 | Gap 6: Design system docs | Purely internal, no blog reader impact. |
| P3 | Missed Gap D: Test count verification | Factual accuracy of a specific number in the blog text. |

---

## Summary

The docs-updater identified the right gaps at the right severity levels. The two critical gaps (pip install path, org URL references) are correctly prioritized. I add one P0 item (the MkDocs category issue that will break the build) and three lower-priority gaps. The main correction is on Gap 1's framing: the current docs state was intentional from an earlier fix, not an oversight, and the Python version discrepancy between root pyproject.toml and core.toml needs nuanced handling rather than blanket reconciliation.
