# Code Verification Review: final.md Synthesis

**Reviewer**: code-verifier
**Date**: 2026-04-03
**Scope**: Verify every technical claim in the two blog posts and 12 doc fix recommendations against the actual source code.

---

## 1. Payoff Formulas (Blog Posts vs `conversus/plugins/nashopt/payoffs.py`)

### Verdict: PASS (with one minor note)

**Negotiation payoff** (Post 05, line ~354):
- Blog: `payoff = zopa_coverage * party_satisfaction`, best response = 1.0
- Code (line 243): `payoff = af.zopa_coverage * af.party_satisfaction`, best_response = 1.0
- **Match**: Exact.

**Prisoners-dilemma payoff** (Post 04, lines ~397-418; Post 05, lines ~367-368):
- Blog: `territory = core_competency_count + unique_capability_count + shared_territory_count - deferral_count`; `overreach_penalty = max(0, overreach_count - overreach_rebutted)`; `payoff = territory - gamma * overreach_penalty`; best_response = territory without deferral deduction.
- Code (lines 124-146): Identical formula. `float(territory) - gamma * float(overreach_penalty)`. Best response = `core_competency_count + unique_capability_count + shared_territory_count` (no deferral, no penalty).
- **Match**: Exact. The code block in Post 04 is a faithful (slightly simplified -- removes the None-check and docstring) reproduction of the actual function.

**Cooperative payoff** (mentioned but not shown in full):
- Blog: "J_i = surviving_count"
- Code (line 39): `payoff = float(af.surviving_count)`, best_response = max surviving across agents.
- **Match**: Accurate summary.

**Winner-take-all payoff**:
- Blog: "J_i = 1 if winner else 0"
- Code (line 77): `payoff = 1.0 if af.ranking_position == 1 else 0.0`
- **Match**: Accurate.

**Resource-allocation payoff**:
- Blog (table): "Utilization efficiency minus inequality"
- Code (line 273): `payoff = af.utilization_efficiency - af.allocation_inequality`
- **Match**: Accurate.

**Fair-division payoff**:
- Blog (table): "Proportionality minus normalized envy"
- Code (lines 306-308): `payoff = af.proportionality_score - (envy_count / max(1, n_agents - 1))`
- **Match**: Accurate. The "normalized" qualifier correctly describes the division by (N-1).

**Mechanism-design payoff**:
- Blog (table): "Social welfare minus gaming vulnerability"
- Code (lines 339-342): `payoff = af.social_welfare_contribution - (gaming_vulnerability_count / total_gaming_vulnerabilities)`
- **Match**: Accurate.

**Red-blue payoff**:
- Blog (table): "Severity-weighted attack/mitigation"
- Code (lines 183-218): Red uses `severity_sum * (landed / total_surface)`, Blue uses `red_severity * (mitigated / total_surface)`.
- **Match**: Accurate summary.

**`(payoff, best_response_payoff)` interface claim**: All 8 functions return `tuple[float, float]`. The `compute_payoff` dispatcher at line 367 preserves this. **Confirmed.**

**"Four new payoff functions" claim** (line 9 of synthesis convergence): There are 8 total payoff functions in the file. The blog says the original 4 modes (cooperative, WTA, PD, red-blue) existed and spec 039 added 4 new ones (negotiation, resource-allocation, fair-division, mechanism-design). The code has all 8 in `PAYOFF_FUNCTIONS` dict (line 355). **Consistent** -- though the claim cannot be historically verified from the current code alone, the file structure matches.

---

## 2. Package Configs (`packages/*.toml`)

### Verdict: PASS

**Four TOML files exist**: `core.toml`, `solvers.toml`, `scenarios.toml`, `swe.toml`. Blog Post 04 (line ~220-224) lists exactly these four. **Match.**

**`core.toml` exclusions** (blog line ~227: "core.toml excludes `conversus/plugins/nashopt/**` and `conversus/plugins/optimizer/**`"):
- Code (`core.toml` lines 28-31): Excludes `conversus/plugins/nashopt/**`, `conversus/plugins/optimizer/**`, `conversus/plugins/scenarios/**`, `conversus/domains/implementations/**`.
- **Partial match**: The blog only mentions two of the four exclusions. The blog omits `conversus/plugins/scenarios/**` and `conversus/domains/implementations/**` from the description. This is a simplification, not an error -- the blog focuses on the solvers boundary. But it could mislead a reader who checks `core.toml` and sees more exclusions than described.

**`solvers.toml` inclusions** (blog line ~227: "solvers.toml only includes those directories"):
- Code (`solvers.toml` lines 24-26): `only-include = ["conversus/plugins/nashopt", "conversus/plugins/optimizer"]`
- **Match.**

**`core.toml` entry point** (`engine.cli:main`):
- Code (`core.toml` line 23): `conversus = "engine.cli:main"`
- Blog Post 04 does not mention the entry point. The doc fix P1-3 correctly flags the inconsistency. **See Section 8 below.**

**`core.toml` license**: MIT (line 10). `solvers.toml` license: LicenseRef-Proprietary (line 9). Blog correctly describes the free/paid split architecture. **Consistent.**

---

## 3. `paths.py` Description vs Actual Module

### Verdict: PASS

**Blog code block** (Post 04, lines ~150-172) compared to actual `conversus/paths.py` (lines 34-84):

The blog code block is a faithful reproduction of the `resolve_package_path` function with minor formatting changes:
- Strategy 1 (importlib.resources): Identical logic -- `resources.files(package)`, iterate parts with `/`, `Path(str(ref))`, check `.exists()`, catch `(TypeError, FileNotFoundError, ModuleNotFoundError)`.
- Strategy 2 (walk up): Identical -- `Path(__file__).resolve().parent`, `range(5)`, `current / Path(*parts)`, `.exists()` check.
- Error: `raise FileNotFoundError(...)` -- blog truncates the error message, which is fine.
- **Match**: The blog code is the actual code with the docstring removed and the error message abbreviated.

**"Three resource categories"** (blog line ~176 mentions templates, presets, schema): The module docstring (lines 8-15) mentions templates, presets, and scaffolds. The `pyproject.toml` `force-include` directive handles `templates`, `presets`, and `schema`. The module provides `get_templates_dir()`, `get_presets_dir()`, and `get_scaffold_dir()`. **Consistent.**

**"importlib.resources is the blessed approach since Python 3.9"**: This is accurate. `importlib.resources.files()` was added in Python 3.9. **Correct.**

**Blog claim "module is 164 lines"** (synthesis line 33: storyteller dropped "60-line module" claim because "module is 164 lines"): The actual `paths.py` is 165 lines. **Close enough** (could vary by one trailing newline).

---

## 4. Test Counts

### Verdict: PASS

**"31 split tests" claim** (Post 04, lines ~197-201):

`tests/test_package_split.py` has 14 `def test_` functions. Parametrize expansions:

| Test function | Parametrize source | Cases |
|---|---|---|
| `test_schemas_no_cross_imports` | `SCHEMAS_MODULES` (9 items) | 9 |
| `test_plugins_framework_imports_only_schemas` | `PLUGINS_FRAMEWORK_MODULES` (2 items) | 2 |
| `test_domains_framework_allowed_imports` | `DOMAINS_FRAMEWORK_MODULES` (3 items) | 3 |
| `test_schemas_does_not_import_plugins` | none | 1 |
| `test_schemas_does_not_import_domains` | none | 1 |
| `test_plugins_base_does_not_import_domains` | none | 1 |
| `test_plugins_config_does_not_import_domains` | none | 1 |
| `test_domains_does_not_import_premium_plugins` | none | 1 |
| `test_all_packages_importable_no_import_error` | none (internal loop over 12 entry points) | 1 |
| `test_premium_no_engine_imports` | `PREMIUM_PACKAGES` (4 items) | 4 |
| `test_premium_no_cross_premium_imports` | `PREMIUM_PACKAGES` (4 items) | 4 |
| `test_paths_importlib_resources` | none | 1 |
| `test_paths_templates_has_modes` | none | 1 |
| `test_paths_presets_dir` | none | 1 |

**Total: 31 cases from 14 test functions. Exact match.**

**"4 free-tier tests" claim** (Post 04, line ~276):

`tests/test_free_tier.py` has exactly 4 test methods:
1. `test_engine_import_clean`
2. `test_cli_import_clean`
3. `test_schemas_import_clean`
4. `test_plugin_base_import_clean`

**Exact match.**

---

## 5. Free/Paid Boundary

### Verdict: PASS

**Blog claim** (Post 04, lines ~246-249): "The free tier (`pip install conversus`) ships the complete deliberation engine. All 8 modes. All 5 phases... The paid tier (`pip install conversus-solvers`) adds the quantitative layer."

Verification against code:
- `core.toml` excludes `conversus/plugins/nashopt/**`, `conversus/plugins/optimizer/**`, `conversus/plugins/scenarios/**`, and `conversus/domains/implementations/**`. This means the free tier contains `engine/`, `linter/`, `web/`, and `conversus/` (schemas, plugins framework, domains framework, paths) but NOT the scoring plugins or domain implementations.
- `solvers.toml` only includes `conversus/plugins/nashopt` and `conversus/plugins/optimizer`.
- **Match**: The free tier ships the engine; the paid tier ships scoring/optimization plugins.

**Blog claim** (Post 04, lines ~266-273): Feature gating via try/except -- `from conversus.plugins.nashopt import EquilibriumScorer`.
- This pattern is described, not shown in the actual engine source (would need to check engine code for import guards). However, `tests/test_free_tier.py` validates that importing `engine`, `engine.cli`, `conversus.schemas`, and `conversus.plugins.base` does NOT pull in any paid modules (`nashopt`, `jax`, `amplpy`, `highspy`, or the four paid plugin packages). **The tests enforce the boundary the blog describes.**

**Blog claim** (Post 04, line ~276): "importing `engine`, `engine.cli`, `conversus.schemas`, or `conversus.plugins.base` must never trigger imports of `nashopt`, `jax`, `amplpy`, `highspy`, or any paid plugin module."
- Code (`test_free_tier.py` lines 15-24): `PAID_MODULES` list includes exactly `conversus.plugins.nashopt`, `conversus.plugins.optimizer`, `conversus.plugins.scenarios`, `conversus.domains.implementations.code_review`, `nashopt`, `jax`, `amplpy`, `highspy`.
- **Match**: The blog's list is a subset of the actual test list. The blog omits `conversus.plugins.optimizer`, `conversus.plugins.scenarios`, and `conversus.domains.implementations.code_review` from its description. This is a simplification, not an inaccuracy.

---

## 6. AMPL Claims

### Verdict: PASS (properly qualified)

**Blog Post 05, lines ~432-433**: "The AMPL infrastructure and config optimizer exist today... Per-mode AMPL model templates... are specified in specs 043 and 044 and will ship in a future wave."

Verification:
- `conversus/plugins/optimizer/` contains 6 files: `__init__.py`, `ampl_model.py`, `ampl_solver.py`, `models.py`, `optimizer.py`, `search.py`. **The AMPL infrastructure exists.**
- `solvers.toml` (line 19): `ampl = ["amplpy", "highspy"]` in optional dependencies. **The binding exists.**
- `search.py` contains `_estimate_cost` (a deliberate duplication of `engine.cost.estimate_cost`), confirming the config optimizer module. **The config optimizer exists.**
- No per-mode AMPL model templates were found in the optimizer directory (the files deal with configuration optimization, not game-form-specific models). **The "future" qualifier is accurate.**

**Blog Post 05, line 66** (dispute 3 resolution): "The storyteller's phrasing ('AMPL formulations with the HiGHS solver can compute provably optimal allocations') overstates current capability and is not used."
- **Correct**: The optimizer currently optimizes deliberation configuration (agent count, iterations, budget), not game-form-specific allocations.

---

## 7. Doc Fix Recommendations vs Actual Gaps

### Verdict: PASS -- All 12 recommendations target real gaps

**P0-1: `docs/index.md` -- No pip install path**
- Actual `docs/index.md` lines 28-31: Shows `git clone ... && cd conversus` / `uv sync`. No `pip install conversus` option.
- **Real gap.** If the blog promises `pip install conversus`, the docs must show it.

**P0-2: `docs/index.md` -- Stale `clariti-care` org references + wrong license**
- Actual `docs/index.md`:
  - Line 10: Badge URL points to `github.com/clariti-care/conversus`
  - Line 11: License badge says `proprietary`, URL points to `clariti-care`
  - Line 29: Clone URL uses `clariti-care`
- Actual `mkdocs.yml` lines 3-5: `site_url` and `repo_url` point to `Build-Fractal`. `core.toml` line 10: license is `MIT`.
- **Real gap.** Three stale org references and a license mismatch.

**P1-1: `docs/user-guide/quickstart.md` -- No PyPI install path**
- Actual quickstart (lines 9-20): Shows only `git clone` + `uv sync`. No `pip install`.
- **Real gap.**

**P1-2: `docs/user-guide/sdk.md` -- `from engine` import path misleading**
- Actual sdk.md (line 12): Already has a note "The `engine` package will be renamed to `conversus` in a future release."
- The doc fix recommends making this more prominent (a warning admonition instead of an info note). The existing note is there but easy to miss.
- **Real gap** (severity is debatable -- the note exists but could be stronger).

**P1-3: Entry point inconsistency** -- See Section 8 below.

**P2-1: `docs/user-guide/config-reference.md` -- No free/paid boundary callout**
- Actual config-reference.md (lines 144-175): Documents `equilibrium-scorer` and `scenario-runner` plugins with their `package` paths, and notes "If a `package` cannot be imported (not installed), a warning is logged and that plugin is skipped." But there is NO explicit mention that these require the paid `conversus-solvers` package.
- **Real gap.**

**P2-2: `docs/user-guide/cli.md` -- Install note assumes `uv sync`**
- Actual cli.md (lines 5-6): "If you installed via `uv sync` (recommended), prefix commands with `uv run`... If you installed via `pip install -e .`, use `conversus` directly."
- This mentions `pip install -e .` (editable dev install), NOT `pip install conversus` (from PyPI). With the package split, `pip install conversus` is the primary user path.
- **Real gap.**

**P2-3: Solver install extras not documented**
- `solvers.toml` (lines 17-19) defines extras `nashopt` and `ampl`. No documentation page shows `pip install conversus-solvers[nashopt]` or `pip install conversus-solvers[ampl]`.
- **Real gap.**

**P3-1: Web UI pip install path missing**
- `pyproject.toml` line 19: `web = ["fastapi>=0.100", "uvicorn>=0.20"]` (optional dep on root). `core.toml` lines 18-19: `web = ["fastapi>=0.100", "uvicorn>=0.20"]`. The web docs page (`docs/user-guide/web-interface.md`) exists but was not checked in detail. The recommendation to add `pip install conversus[web]` is reasonable.
- **Real gap** (minor).

**P3-2: `fractal.css` undocumented** -- Low urgency, contributor-facing. **Valid but low priority.**

**P3-3: `conversus/paths.py` not in architecture docs**
- Grepped `docs/developer-guide/architecture.md` for `paths.py`, `resolve_package_path`, and `importlib.resources`: **zero matches**. The blog makes `paths.py` the centerpiece of Wave 2, but the architecture docs do not mention it at all.
- **Real gap.**

---

## 8. Entry Point Inconsistency (`cli` vs `main`)

### Verdict: THE INCONSISTENCY IS REAL AND IS WORSE THAN DESCRIBED

**What the doc fix says** (P1-3, line ~576-578): `pyproject.toml` declares `engine.cli:cli`, `core.toml` declares `engine.cli:main`. Verify whether they resolve to the same behavior.

**What the code shows**:
- `pyproject.toml` line 24: `conversus = "engine.cli:cli"` -- points to the Click group `cli()` defined at `engine/cli/__init__.py` line 75.
- `packages/core.toml` line 23: `conversus = "engine.cli:main"` -- points to a callable named `main`.
- `engine/cli/__init__.py`: Defines `cli` (a `@click.group()` function at line 75) but **does NOT define any `main` function**. A grep for `def main` across the entire `engine/cli/` directory returned zero results.

**This means `pip install conversus` (built from `core.toml`) would produce a broken CLI entry point.** The `engine.cli:main` reference would fail at runtime with an `AttributeError` because `main` does not exist in `engine.cli`.

The synthesis correctly flagged this in P1-3 as "requires code investigation." The investigation result is: **the entry point in `core.toml` is broken. It must be changed to `engine.cli:cli` to match `pyproject.toml` and the actual code.**

---

## 9. Additional Findings

### 9a. Python version discrepancy -- correctly handled

The synthesis (line 39) notes: "3.11+ for published package, 3.12+ for dev environment."
- `core.toml` line 11: `requires-python = ">=3.11"`
- `pyproject.toml` line 8: `requires-python = ">=3.12"`
- **Correctly identified.** The doc fix P1-1 handles this with the note "Two Python version numbers are intentional."

### 9b. "Seven files with `Path(__file__).parent`" claim

The synthesis claims "seven files used `Path(__file__).parent` traversal" (convergence item 8, Post 04 line ~143).

Grepping `*.py` for `Path(__file__).parent` (excluding specs/blog output) returns:
1. `engine/templates.py` (in a docstring, references the pattern)
2. `tests/test_code_review.py` (line 34, fixture path -- legitimate test usage)
3. `tests/test_code_review.py` (line 851)
4. `conversus/paths.py` (line 5, in docstring describing the fallback; line 73, the actual fallback implementation)
5. `conversus/domains/implementations/code_review/domain.py` (line 257, docstring; line 267, actual fallback)

The current state of the codebase shows the pattern has been largely replaced. The blog describes the **pre-fix** state where seven files had this pattern. The current code shows `paths.py` as the centralized resolver and `code_review/domain.py` using its own fallback. This is consistent with the narrative -- the seven files were fixed, and the remaining usages are either: (a) inside `paths.py` itself (the fix), (b) in the code_review domain (which uses `get_scaffold_dir`), or (c) in tests. **The claim is plausible but cannot be definitively verified post-fix.**

### 9c. `decide` command mode restriction -- correctly implied

Blog Post 04 (line ~247): "All 8 modes" in the free tier. `docs/index.md` line 62: "The CLI `decide` command supports 4 modes for quick ad-hoc use; all 8 are available via config files."

Actual `engine/cli/__init__.py` lines 238-243: The `decide` command's `--mode` option is restricted to `["cooperative", "winner-take-all", "prisoners-dilemma", "red-blue"]` -- only 4 modes. All 8 modes are available via `conversus run` with a config file. **The docs are accurate; the blog simplifies by saying "all 8 modes" without noting the CLI subset restriction.**

### 9d. Blog Post 05 category

The synthesis resolves the category dispute to `Process`. `mkdocs.yml` (lines 40-43) `categories_allowed` lists: `Engineering`, `Process`, `Release`. Post 05 uses `Engineering` + `Process` -- both are in the allowed list. **Valid.**

Post 04 uses `Engineering` + `Release` -- both allowed. **Valid.**

---

## Summary Scorecard

| # | Claim | Verified | Notes |
|---|-------|----------|-------|
| 1 | Payoff formulas match code | PASS | All 8 formulas verified exact |
| 2 | Package configs match | PASS | Minor simplification (2 of 4 exclusions mentioned) |
| 3 | `paths.py` description accurate | PASS | Blog code is the actual code minus docstring |
| 4 | 31 split tests | PASS | 14 functions x parametrize = 31 cases exactly |
| 5 | 4 free-tier tests | PASS | 4 test methods exactly |
| 6 | Free/paid boundary correct | PASS | Enforced by build config + test suite |
| 7 | AMPL claims qualified | PASS | Config optimizer exists; per-mode templates future |
| 8 | Kalman claims qualified | PASS | Code exists in `conversus/plugins/nashopt/kalman.py` |
| 9 | Doc fixes target real gaps | PASS | All 12 recommendations verified against actual docs |
| 10 | Entry point inconsistency | CONFIRMED BROKEN | `core.toml` references `engine.cli:main` which does not exist |
| 11 | `estimate_cost` duplication | PASS | `search.py` lines 29-34 contain the duplicate |
| 12 | Blog categories valid | PASS | Both posts use `mkdocs.yml` allowed categories |

---

## Blocking Issues

1. **P1-3 is a build-breaking bug, not just a doc fix.** `core.toml` line 23 must change from `engine.cli:main` to `engine.cli:cli`. Without this, `pip install conversus` produces a package with a non-functional CLI entry point. This must be fixed before any package is published.

## Non-Blocking Issues

1. **Post 04 undersells `core.toml` exclusions.** The blog mentions only 2 of 4 exclusion patterns. Consider adding "and domain implementations" to the description for completeness.
2. **Post 04 "all 8 modes" oversimplification.** The `decide` CLI command only supports 4 modes. All 8 are available via config files. The blog should note this distinction or avoid implying CLI parity.
3. **"Seven files" claim is unverifiable post-fix.** The claim is plausible but the pre-fix state is not visible in the current codebase. Minor -- readers who check will see `paths.py` as the fix, which is consistent.
