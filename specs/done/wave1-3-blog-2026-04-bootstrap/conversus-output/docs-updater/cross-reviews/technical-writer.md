# Cross-Review of Technical Writer's Blog Posts

**Reviewer**: docs-updater
**Reviewing**: technical-writer's review (two blog posts)
**Date**: 2026-04-03
**Method**: Compared blog post claims against actual source code, package configs, existing docs pages, and test files. Evaluated whether publishing would create documentation gaps or contradict current docs.

---

## 1. Claims the Current Docs Do Not Support

### 1a. `pip install conversus` as a working install path (BOTH POSTS)

Both posts present `pip install conversus` and `pip install conversus-solvers` as the primary install mechanism. The current docs do not support this:

- `docs/index.md` lines 28-31 still show `git clone` + `uv sync` as the only install method.
- `docs/user-guide/quickstart.md` lines 9-20 show `git clone` + `uv sync` only.
- `docs/user-guide/sdk.md` line 8 shows `uv sync` or `pip install -e .` (editable install, not PyPI).
- `docs/user-guide/cli.md` line 6 references `uv sync` as the recommended install.

The blog posts will create an expectation that `pip install conversus` works from PyPI. The package TOMLs exist (`packages/core.toml`, `packages/solvers.toml`), the build script exists (`scripts/build-packages.sh`), but there is no evidence the packages are published to PyPI. The blog says "pip install conversus now works" but does not qualify whether this means from a local wheel or from a registry. My own review (Gap 1, Gap 3) flags the same docs-side issue. The technical writer's posts amplify the problem by making it a central narrative.

**Verdict**: The posts make the install path claim much more prominent than the docs can back up. Either the docs must be updated before publishing, or the posts need a qualifier that packages are locally buildable but not yet on PyPI.

### 1b. `conversus-solvers[ampl]` and `conversus-solvers[nashopt]` extras (POST 2, line 315-316)

Post 2 claims:
```
Tier 2 (AMPL)      -> pip install conversus-solvers[ampl]
Tier 3 (nashopt)   -> pip install conversus-solvers[nashopt]
```

This is verified in `packages/solvers.toml` lines 16-19:
```toml
[project.optional-dependencies]
nashopt = ["nashopt", "jax"]
ampl = ["amplpy", "highspy"]
```

However, no docs page mentions these extras. The closest is `docs/user-guide/quickstart.md` line 19 (`uv sync --extra solvers`) which bundles everything together. The per-extra install syntax is undocumented.

**Verdict**: Accurate to the package config. Creates a new doc gap -- the extras syntax should be documented in the quickstart or config reference if the posts go live.

### 1c. "5-phase pipeline" and "5-6 phases" (BOTH POSTS)

Both posts describe a "5-phase pipeline" (review, cross-review, revision, disputes, synthesis). The docs at `docs/user-guide/quickstart.md` lines 32-39 confirm this exact 5-phase list. The templates directory has 7 templates per mode (adds arbitration and cross-round-synthesis per `docs/developer-guide/architecture.md` line 42), but the standard pipeline is indeed 5 phases.

Post 1 line 149 says "All 8 modes. All 5-6 phases." The "5-6" is imprecise. The pipeline is 5 phases. Multi-round deliberations add cross-round synthesis as a 6th. The docs do not explain this distinction clearly.

**Verdict**: Mostly accurate but the "5-6" phrasing in Post 1 should be tightened to "5 phases per round (6 with cross-round synthesis in multi-round deliberations)" or simply "5 phases."

### 1d. Four package wheels from a single build (POST 1, lines 123-133)

Post 1 claims four package TOMLs:
```
packages/
  core.toml       # pip install conversus
  solvers.toml    # pip install conversus-solvers
  scenarios.toml  # pip install conversus-scenarios
  swe.toml        # pip install conversus-swe
```

Verified: all four files exist at `<HOME>/code/payer-index-mono/conversus/packages/`. The build script at `scripts/build-packages.sh` iterates over `packages/*.toml` and runs `hatch build` for each. The claim is accurate.

No docs page documents the `packages/` directory, the build script, or the multi-package build process. `docs/developer-guide/architecture.md` describes the three-layer coupling rules but does not mention the build-time splitting. `docs/developer-guide/contributing.md` presumably does not cover this either.

**Verdict**: Accurate. Creates a new doc gap -- the build-time splitting and `packages/` directory should be documented in the developer guide.

---

## 2. New Doc Gaps Publishing Would Create

### 2a. No "Pricing" or "Packages" docs page

Both posts establish a clear free/paid narrative. The current docs have exactly one mention of the tier structure: the "Three Layers" table in `docs/index.md` lines 18-22 ("Free / open-core", "Premium plugins", "Platform"). There is no dedicated page explaining:
- What is included in each pip package
- The free/paid boundary rationale
- The feature-gating mechanism (try/except import)
- How to check which tier is active

My own review (Gap 4) flagged the missing callout in the config reference. The blog posts go much further -- they present the free/paid split as a core product concept. A reader arriving from the blog will look for a "Pricing" or "Packages" page and find nothing.

**Action needed**: Create a `docs/user-guide/packages.md` or `docs/user-guide/tiers.md` page, or at minimum add a substantial section to the quickstart.

### 2b. No docs on the three-tier solver fallback (POST 2)

Post 2's entire thesis is the heuristic -> AMPL -> nashopt solver fallback chain. The existing docs describe individual solver components:
- `docs/api/plugins/nashopt.md` documents the payoff functions and module APIs
- `docs/api/plugins/optimizer.md` documents the optimizer plugin
- `docs/developer-guide/game-forms.md` documents game form to payoff mappings

But no docs page presents the three-tier fallback chain as an architectural concept. The `PluginResult.solver_used` field (`"none"`, `"heuristic"`, `"ampl-highs"`, `"nashopt"`) is not documented in the user-facing docs.

**Action needed**: Add a "Solver Architecture" section to `docs/developer-guide/architecture.md` or a dedicated page.

### 2c. No docs on `conversus/paths.py` or data file resolution (POST 1)

Post 1 explains `resolve_package_path()` and the `importlib.resources` strategy in detail. No docs page covers this. The developer guide does not mention how data files (templates, presets, schemas) are located at runtime. Contributors who need to add a new data file directory would not know the pattern.

**Action needed**: Add a section to `docs/developer-guide/contributing.md` or `docs/developer-guide/architecture.md` explaining the path resolution strategy.

### 2d. No docs on the `gamma` parameter or per-mode tuning (POST 2)

Post 2 spends significant space on `gamma` as a tuning knob. The config reference (`docs/user-guide/config-reference.md` line 154) shows `gamma: 1.0` as a plugin config value but does not explain what it does, what values are sensible, or how it affects agent behavior. The modes page (`docs/user-guide/modes.md`) describes mode dynamics but does not mention tuning parameters.

**Action needed**: Add parameter documentation to the modes page or config reference.

---

## 3. Links in the Posts That Should Point to Docs Pages That Do Not Exist

Neither post contains explicit hyperlinks to docs pages (they are standalone blog posts without internal links). However, the posts reference concepts that readers will search for:

| Concept from posts | Expected docs location | Exists? |
|---|---|---|
| `pip install conversus` | Quickstart install section | No (shows git clone only) |
| Free/paid feature matrix | Dedicated page or quickstart section | No |
| `conversus/paths.py` pattern | Developer guide | No |
| Three-tier solver fallback | Architecture or dedicated page | No |
| `gamma` and mode-specific parameters | Config reference or modes page | Partially (value shown, not explained) |
| `packages/*.toml` build system | Developer guide | No |
| `test_package_split.py` (31 tests) | Testing guide | No |
| `test_free_tier.py` | Testing guide | No |
| `estimate_cost` duplication rationale | Architecture decisions | No |

If the blog index page (`docs/blog/index.md`) links to these posts, readers clicking through will hit dead ends when they try to find the referenced concepts in the main docs.

---

## 4. Does the Technical Content Match the Actual Code/Specs?

### 4a. Payoff function formulas -- VERIFIED CORRECT

All eight payoff formulas in both posts match the actual code in `conversus/plugins/nashopt/payoffs.py`:

| Mode | Blog formula | Code (payoffs.py) | Match? |
|---|---|---|---|
| cooperative | `surviving_count` | `float(af.surviving_count)` (line 39) | Yes |
| winner-take-all | `1 if winner, 0 otherwise` | `1.0 if af.ranking_position == 1 else 0.0` (line 77) | Yes |
| prisoners-dilemma | `territory - gamma * overreach_penalty` | Lines 124-134 | Yes |
| red-blue | `severity * confirmed_ratio` | Lines 186-194 | Yes |
| negotiation | `zopa_coverage * party_satisfaction` | `af.zopa_coverage * af.party_satisfaction` (line 243) | Yes |
| resource-allocation | `utilization_efficiency - allocation_inequality` | Line 273 | Yes |
| fair-division | `proportionality_score - envy_count / max(1, N-1)` | Lines 305-308 | Yes |
| mechanism-design | `social_welfare_contribution - gaming_vuln / total` | Lines 339-342 | Yes |

### 4b. `compute_payoff()` dispatcher -- VERIFIED CORRECT

The blog's code snippet for the dispatcher matches `payoffs.py` lines 387-399. Only `prisoners-dilemma` mode passes `gamma`; all others use default signatures. Accurate.

### 4c. `resolve_package_path()` -- VERIFIED CORRECT

The blog's code snippet for `resolve_package_path()` matches `conversus/paths.py` lines 34-84. The two-strategy approach (importlib.resources first, then `__file__` traversal) is accurately described.

### 4d. `force-include` in pyproject.toml -- VERIFIED CORRECT

The blog's TOML snippet matches `packages/core.toml` lines 34-37 exactly.

### 4e. "31 tests" claim -- VERIFIED CORRECT

`tests/test_package_split.py` has 14 test functions, but 4 are parametrized over module lists (9 + 2 + 3 + 4 + 4 instances). Total parametrized instances: 9 (schemas) + 2 (plugins framework) + 3 (domains framework) + 5 (cross-layer standalone) + 1 (all-packages importable) + 4 (premium no engine) + 4 (premium no cross-premium) + 3 (paths) = 31. Claim is accurate.

### 4f. "Seven files" with path issues -- VERIFIED CORRECT

Seven files (excluding `paths.py` and the test) import `resolve_package_path`: `conversus/schemas/construction.py`, `conversus/schemas/game_forms.py`, `linter/validate.py`, `conversus/domains/implementations/code_review/domain.py`, `engine/_root.py`, `engine/config.py`, `engine/templates.py`. Matches the "seven files" claim.

### 4g. Package TOML contents -- VERIFIED CORRECT

The `core.toml` and `solvers.toml` snippets shown in the storyteller's Post 1 match the actual files. The exclude/only-include patterns are accurate.

### 4h. Entry point discrepancy -- MINOR ISSUE FOUND

Post 1 (storyteller version, line 106) shows `packages = ["engine", "linter", "web", "conversus"]` in `core.toml`. Actual `core.toml` line 26 confirms this. However, there is a discrepancy the blog does not mention: the dev `pyproject.toml` line 24 says `engine.cli:cli` while `core.toml` line 23 says `engine.cli:main`. These are different entry points. My own review flagged a related issue with the SDK namespace note. The blog posts do not discuss this -- not a factual error in the posts, but a lurking inconsistency that the "pip install" narrative papers over.

### 4i. Python version -- INCONSISTENCY ACROSS CONFIGS

Post 1 does not state a Python version requirement. My own review flagged a mismatch: `pyproject.toml` (dev) says `>=3.12`, `packages/core.toml` says `>=3.11`, `docs/user-guide/quickstart.md` says "Python 3.12+", `docs/index.md` badge says "3.12+". The blog posts do not pick a side, which is fine, but the underlying inconsistency remains unresolved.

### 4j. Game form to optimization problem mapping (POST 2) -- EDITORIALLY ACCURATE, NOT CODE-VERIFIED

Post 2's "How Game Forms Map to Optimization Problems" section (lines 358-373) describes cooperative -> Pareto optimization, zero-sum -> minimax, etc. This mapping is editorially consistent with the game theory literature and with `docs/developer-guide/game-forms.md`. However, the actual AMPL optimization models (specs 043, 044) have not shipped yet. The blog presents the mapping as if the optimization formulations exist in code -- they do not. The heuristic payoff functions exist. The AMPL/nashopt solver integration infrastructure exists. But the specific AMPL models that formalize each game form as an optimization problem are future work.

**Verdict**: The blog should make clearer that the three-tier solver chain is architecturally complete but that Tier 2 (AMPL) model templates are in specs 043-044, not yet implemented. Currently, the AMPL integration exists (amplpy + highspy are optional dependencies), but the per-mode AMPL model templates are forward-looking.

---

## 5. Agreement with My Own Review

My review identified 6 gaps. The technical writer's posts would exacerbate Gaps 1-4:

| My Gap | Impact of publishing posts |
|---|---|
| Gap 1 (no pip install in docs) | Posts make this the central narrative. Gap becomes critical. |
| Gap 2 (stale clariti-care URLs) | Posts use no org URLs, so no direct conflict, but the docs landing page still has wrong org. |
| Gap 3 (quickstart still dev-only) | Posts assume pip install as primary. Quickstart contradiction worsens. |
| Gap 4 (no free/paid callout) | Posts explain the free/paid split in detail. Docs have zero explanation. |
| Gap 5 (modes payoff docs) | Already complete. Posts align with existing docs. |
| Gap 6 (fractal.css undocumented) | Unrelated to post content. |

---

## Summary

The technical writer produced two technically accurate blog posts. Every code claim I verified against the source matched. The payoff formulas, path resolution code, package configs, test counts, and file counts are all correct.

The primary risk is not factual accuracy -- it is **documentation coverage**. Publishing these posts will set expectations the docs cannot currently meet. The most urgent items before publishing:

1. **CRITICAL**: Update `docs/index.md` and `docs/user-guide/quickstart.md` with `pip install` as the primary install path, or qualify in the posts that packages are locally buildable.
2. **HIGH**: Create documentation for the free/paid boundary (either a dedicated page or substantial additions to quickstart and config reference).
3. **HIGH**: Clarify in Post 2 that AMPL model templates (Tier 2 per-mode formulations) are specified but not yet implemented. The AMPL infrastructure exists; the per-mode models are specs 043-044.
4. **MEDIUM**: Document the `gamma` parameter and solver fallback chain in the user-facing docs.
5. **MEDIUM**: Document `packages/` directory and build-time splitting in the developer guide.
6. **LOW**: Tighten "5-6 phases" in Post 1 to "5 phases."
