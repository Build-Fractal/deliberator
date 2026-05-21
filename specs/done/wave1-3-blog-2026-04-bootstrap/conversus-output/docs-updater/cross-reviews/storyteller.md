# Docs-Updater Cross-Review of Storyteller Posts

**Reviewer**: docs-updater
**Target**: storyteller/review.md (Post 1: "From Heuristics to pip install", Post 2: "Why Your AI Agents Give Different Answers Every Time")
**Date**: 2026-04-03
**Method**: Compared every technical claim, code example, and product promise in both posts against the actual source code, package configs, test files, and current documentation.

---

## 1. Claims the current docs do not support

### 1a. `pip install conversus` as a working command

Both posts present `pip install conversus` as a real, usable install path. Post 1 says "pip install conversus is a real thing" (line 168). Post 2 says "In our framework (conversus)..." and describes the free/paid split as operational (line 283-291).

**Docs status**: The docs do not support this claim. `docs/index.md` lines 28-31 show only `git clone` + `uv sync`. `docs/user-guide/quickstart.md` lines 9-20 show only the dev workflow. There is no mention of `pip install` anywhere in the published documentation. My own review (Gap 1, Gap 3) flagged this as CRITICAL.

**Verdict**: Publishing these posts before updating the docs would send readers to a landing page that contradicts the post's central narrative. A reader who runs `pip install conversus` after reading Post 1 will either find the package does not exist on PyPI yet, or will land on docs that tell them to `git clone` instead. This is the highest-priority gap.

### 1b. `pip install conversus-solvers` as a separate paid package

Post 1 describes the paid tier install (line 143-144). Post 2 describes the free/paid boundary (lines 283-291). The TOML configs exist (`packages/solvers.toml`), and the build-time splitting infrastructure is in place.

**Docs status**: `docs/user-guide/config-reference.md` shows nashopt and scenarios plugins in examples (lines 155-165) but never mentions that these require the paid `conversus-solvers` package. There is no "Premium Feature" callout anywhere in the docs. My own review (Gap 4) flagged this.

**Verdict**: The posts imply a clean free/paid distinction that the docs do not explain. A reader who installs `conversus` (core) and tries the plugin examples from the config reference will get silent failures with no guidance on what to install.

### 1c. "60-line module" claim for paths.py

Post 1 (line 62) calls `conversus/paths.py` "a 60-line module." The actual file is 164 lines (including docstrings, blank lines, and convenience functions). The core `resolve_package_path` function is roughly 30 lines. The storyteller likely counted only the resolver function plus imports, not the full module with its convenience wrappers (`get_templates_dir`, `get_template_path`, `get_presets_dir`, `get_scaffold_dir`).

**Verdict**: Minor inaccuracy. Not misleading about the architecture, but will look sloppy if a reader checks. Suggest changing to "a single-module path resolver" without a line count, or saying "the core resolver is ~30 lines."

### 1d. "31 package-split tests" claim

Post 1 (line 93) says "31 package-split tests verifying that each future package's import boundary held." The actual `tests/test_package_split.py` file contains 5 test classes with parametrized tests. The parametrized `SCHEMAS_MODULES` list has 8 entries, `PLUGINS_FRAMEWORK_MODULES` has 2, `DOMAINS_FRAMEWORK_MODULES` has 3, `PREMIUM_PACKAGES` has 4 entries (run through 2 parametrized tests = 8), plus 6 non-parametrized tests in `TestNoCircularDependencies`, and 3 in `TestPathsImportlibResources`. That totals approximately 8 + 2 + 3 + 8 + 6 + 3 = 30 tests. Close to 31 but depends on exact pytest collection. The claim is approximately correct.

**Verdict**: Acceptable. The number is close enough to survive scrutiny.

### 1e. "55-agent documentation review" reference

Post 1 (line 26) mentions "A 55-agent documentation review had just shipped 3 code bug fixes and 28 documentation improvements." This references the spec 031 review, which is not covered in the current docs at all. The docs do not describe what the spec review process looked like or its results.

**Verdict**: Not a docs gap per se -- this is historical context. But if readers try to find documentation of this event, they will not find it in the docs site. Low risk.

---

## 2. Expectations the posts would create that docs cannot fulfill

### 2a. Post 2 implies the scoring layer is production-ready

Post 2 is written as thought leadership aimed at practitioners building multi-agent systems. It describes the pattern in general terms ("You don't need a game theory PhD to apply this pattern") and then positions conversus as the implementation. The four steps (lines 270-279) describe a workflow that requires the scoring tier.

**Docs status**: The payoff formulas ARE documented in `docs/user-guide/modes.md` (confirmed in my review, Gap 5 -- NO ACTION needed). However, the docs do not contain a tutorial or walkthrough for using the scoring tier. There is no "Getting Started with Scoring" page. The modes page documents the formulas but not how to enable, configure, or interpret scoring output.

**Expectation gap**: A reader motivated by Post 2 to try conversus for scoring will find formulas but no instructions. They will need to reverse-engineer the plugin config from the config-reference examples. The gap between the marketing promise ("deterministic tuning knobs") and the docs experience ("here are some YAML fields") is significant.

### 2b. Kalman convergence prediction is mentioned but undocumented

Post 2 (line 247) says "If you feed equilibrium scores into a Kalman filter across rounds, you get a convergence estimate with confidence bounds." Post 1 (line 144) lists "Kalman convergence prediction" as a paid feature. The solvers.toml lists `scipy>=1.10` as a dependency (presumably for the Kalman filter).

**Docs status**: The Kalman predictor is not documented anywhere in the docs site. The modes page does not mention convergence prediction. The config reference does not show how to enable it.

**Expectation gap**: Moderate. The posts name-drop a feature that readers cannot find instructions for.

### 2c. AMPL/HiGHS integration is described in detail but the docs say nothing

The technical-writer's Post 2 goes deep on the three-tier solver fallback (heuristic, AMPL, nashopt). The storyteller's Post 2 mentions AMPL less but still references "optimization models" as the fix for inconsistency.

**Docs status**: AMPL is not mentioned in any user-facing docs page. The solvers.toml defines `ampl = ["amplpy", "highspy"]` as an optional dependency, but this is not exposed to users.

**Expectation gap**: Low for the storyteller's posts specifically (Post 2 stays general). Higher for the technical-writer's Post 2, which describes `pip install conversus-solvers[ampl]` explicitly.

---

## 3. Code example and technical claim accuracy

### 3a. `resolve_package_path` code example (Post 1, lines 64-87)

Compared line-by-line against `conversus/paths.py` lines 34-84. The code in the post is accurate. The function signature, the two strategies, the exception handling, and the fallback loop all match. The only difference: the post omits the `joined = "/".join(parts)` line and the error message text, which is appropriate for brevity.

**Verdict**: Accurate.

### 3b. `core.toml` example (Post 1, lines 103-118)

Compared against `packages/core.toml`. The post shows:
```toml
packages = ["engine", "linter", "web", "conversus"]
exclude = [
    "conversus/plugins/nashopt/**",
    "conversus/plugins/optimizer/**",
    "conversus/plugins/scenarios/**",
    "conversus/domains/implementations/**",
]
```

Actual file matches exactly. The `force-include` section also matches.

**Verdict**: Accurate.

### 3c. `solvers.toml` example (Post 1, lines 124-130)

The post shows `only-include` with nashopt and optimizer. The actual file matches. However, the post omits the `dependencies`, `optional-dependencies`, and `project` metadata. Fine for brevity.

**Verdict**: Accurate.

### 3d. Feature gating code (Post 1, lines 148-154; Post 2, implied)

The try/except import pattern is presented as the gating mechanism. This pattern is validated by `tests/test_free_tier.py`, which tests that importing engine, CLI, schemas, and plugin base does NOT trigger paid module imports. The pattern is correct and tested.

**Verdict**: Accurate.

### 3e. Payoff function formulas (Post 2, lines 225-265)

Compared the eight-mode table against `payoffs.py`:

| Mode | Post claims | Code says | Match? |
|------|------------|-----------|--------|
| cooperative | Recommendations surviving into synthesis | `surviving_count` | Yes |
| winner-take-all | Win/loss plus score differential | `1 if ranking_position == 1 else 0` | Yes |
| prisoners-dilemma | Territory held minus overreach penalty | `territory - gamma * overreach_penalty` | Yes |
| red-blue | Severity-weighted confirmed vs. mitigated findings | `severity_sum * confirmed_ratio` / `red_severity * mitigated_ratio` | Yes |
| negotiation | ZOPA coverage times party satisfaction | `zopa_coverage * party_satisfaction` | Yes |
| resource-allocation | Utilization minus inequality | `utilization_efficiency - allocation_inequality` | Yes |
| fair-division | Proportionality minus envy | `proportionality_score - envy_count / max(1, N-1)` | Yes |
| mechanism-design | Welfare contribution minus gaming vulnerabilities | `social_welfare_contribution - gaming_vulnerability_count / total_vulns` | Yes |

**Verdict**: All payoff formulas are accurate and match the source code exactly.

### 3f. `compute_payoff` dispatcher example (Post 2 is implicit; technical-writer Post 2 lines 344-351)

The storyteller's Post 2 does not show the dispatcher code, but describes the kwargs pattern correctly. The actual `compute_payoff()` in payoffs.py lines 367-399 matches the described behavior: only prisoners-dilemma passes `gamma` currently.

**Verdict**: Accurate.

### 3g. Prisoners-dilemma code example (Post 1, storyteller inline)

The storyteller's Post 1 describes `territory_held - gamma * overreach_penalty` with `gamma` as a tuning knob. The code at payoffs.py lines 102-146 matches exactly, including the default `gamma=1.0`.

**Verdict**: Accurate.

---

## 4. Does Post 2 ("Why Your AI Agents") make promises about conversus that the docs do not back up?

**Yes, in three specific ways:**

### 4a. "Deterministic tuning knobs" promise

Post 2 sells the idea that optimization models provide "deterministic tuning knobs" to control agent behavior. The `gamma` parameter example is real and documented in modes.md. But Post 2 implies a broader parameter surface than currently exists. Only `gamma` for prisoners-dilemma is implemented as a configurable parameter today. The other seven modes have no user-tunable parameters in their payoff functions.

The docs accurately reflect this -- modes.md shows the formulas but does not claim broad tunability. Post 2 creates an expectation of a rich parameter surface that does not yet exist. The post itself hedges this on line 353 ("Future specs (043, 044) will expand the parameter surface") but only in the technical-writer's version. The storyteller's Post 2 does not include this caveat.

**Risk level**: MEDIUM. A reader who installs conversus-solvers expecting per-mode tuning knobs will find that only PD mode has `gamma`. The other modes are fixed-formula.

### 4b. "Convergence prediction" promise

Post 2 (lines 246-248) describes Kalman-filter convergence prediction as a concrete capability: "This deliberation will converge in 2 more rounds with 85% confidence." The docs do not document this feature at all. The solvers.toml includes scipy (which would be needed), but there is no user-facing documentation of convergence prediction configuration or output format.

**Risk level**: MEDIUM. The feature may exist in code, but it is invisible to users through the docs.

### 4c. "No license keys. No nag screens. No degraded output." promise

Post 2 (line 156, via Post 1's description of the gating) promises a clean free/paid experience. The code supports this -- the try/except pattern is real. But the docs do not explain this boundary at all. A free-tier user who encounters scoring-related config examples in the docs will not understand why things are silently skipped. The docs need the "Premium Feature" callout that my review (Gap 4) recommended.

**Risk level**: LOW-MEDIUM. The code fulfills the promise, but the docs do not communicate it.

---

## Summary

| # | Finding | Severity | Recommendation |
|---|---------|----------|----------------|
| 1 | `pip install conversus` is the central narrative but docs show only `git clone` | CRITICAL | Must update docs/index.md and quickstart.md BEFORE publishing posts |
| 2 | Free/paid boundary described in posts but absent from docs | HIGH | Add Premium Feature callouts per Gap 4 in my review |
| 3 | `paths.py` described as "60-line" but is 164 lines | LOW | Remove line count or say "single-module resolver" |
| 4 | Post 2 implies broad parameter tunability but only `gamma` exists | MEDIUM | Add a caveat to Post 2 or document the planned parameter expansion |
| 5 | Kalman convergence prediction described as capability but undocumented | MEDIUM | Either document it or soften the claim to "planned" |
| 6 | No scoring tier tutorial exists to match Post 2's call to action | HIGH | Need a "Getting Started with Scoring" docs page before Post 2 publishes |
| 7 | `clariti-care` org references still in docs but posts imply Build-Fractal | HIGH | Fix per Gap 2 in my review |
| 8 | All code examples in both posts are accurate | -- | No action needed |
| 9 | All payoff formulas match source code exactly | -- | No action needed |
| 10 | 31-test count is approximately correct | -- | No action needed |

### Bottom line

The storyteller's posts are technically accurate in their code examples and formula references. The narrative framing is honest about what was built. The risk is not factual error -- it is **expectation mismatch**. The posts describe a product that is further along in user-facing polish than the docs currently reflect. Publishing Post 1 without updating the install docs would actively mislead readers. Publishing Post 2 without a scoring tutorial would generate interest that the docs cannot convert.

**Recommended sequencing**: Ship the docs updates from my review (Gaps 1-4) first, then publish the posts. The code is ready. The docs are not.
