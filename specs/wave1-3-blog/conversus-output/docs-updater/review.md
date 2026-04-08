# Docs Updater Review: Wave 1-3 Gaps

**Reviewed**: 2026-04-03
**Scope**: Identify documentation gaps introduced by Waves 1-3 (specs 038, 039, 032, 033, MIT-1)
**Method**: Read all source files listed in the task, compared actual docs content against shipped code and spec requirements.

---

## Gap 1: `docs/index.md` — Missing `pip install` path (CRITICAL)

**Status**: The index page still shows `git clone` + `uv sync` as the only install method. Spec 032 requires `pip install conversus` as the primary install path. The blog post 03 even notes that fixing the install path was the highest-impact onboarding change.

**Current text** (line 28-31):
```markdown
## Quick Install

```bash
git clone https://github.com/clariti-care/conversus.git && cd conversus
uv sync
```
```

**Required change**: Replace with dual-path install showing pip as primary, dev setup as secondary.

```markdown
## Quick Install

```bash
pip install conversus                    # Free: engine + 8 modes + templates
pip install conversus-solvers            # Paid: equilibrium scoring, convergence, AMPL (optional)
pip install conversus[all]               # Everything (optional)
```

!!! tip "Development setup"
    To work on conversus itself:
    ```bash
    git clone https://github.com/Build-Fractal/conversus.git && cd conversus
    uv sync
    ```
```

---

## Gap 2: `docs/index.md` — Three stale `clariti-care` org references (CRITICAL)

**Status**: The repo moved from `clariti-care` to `Build-Fractal` (confirmed in `mkdocs.yml` lines 3-5 which already use `Build-Fractal`). But `docs/index.md` still has three `clariti-care` URLs.

**Line 10** — Tests badge:
```
OLD: [![Tests](https://img.shields.io/badge/tests-1%2C302%20passed-brightgreen)](https://github.com/clariti-care/conversus)
NEW: [![Tests](https://img.shields.io/badge/tests-1%2C302%20passed-brightgreen)](https://github.com/Build-Fractal/conversus)
```

**Line 11** — License badge:
```
OLD: [![License](https://img.shields.io/badge/license-proprietary-blue)](https://github.com/clariti-care/conversus/blob/main/LICENSE)
NEW: [![License](https://img.shields.io/badge/license-MIT-brightgreen)](https://github.com/Build-Fractal/conversus/blob/main/LICENSE)
```

Note: The license badge also says "proprietary" but `packages/core.toml` declares `license = "MIT"` for the free tier. This should be updated to "MIT" to match the actual license.

**Line 29** — Clone URL:
```
OLD: git clone https://github.com/clariti-care/conversus.git && cd conversus
NEW: git clone https://github.com/Build-Fractal/conversus.git && cd conversus
```

**Also check**: `.do/app.yaml` line 10 has `repo: clariti-care/conversus` — out of scope for docs but worth noting.

---

## Gap 3: `docs/user-guide/quickstart.md` — Does not reflect new install experience (MEDIUM)

**Status**: The quickstart still shows only the dev workflow (`git clone` + `uv sync`). With spec 032 complete, users should see `pip install conversus` as the primary path.

**Current text** (lines 9-20):
```markdown
## Install

```bash
git clone <repo-url> conversus && cd conversus
uv sync                        # Python 3.12+ required
```

This installs the core engine with Anthropic, OpenAI, and mock providers. For solver plugins:

```bash
uv sync --extra solvers        # nashopt + kalman + AMPL (optional)
```
```

**Required change**: Add pip install as the primary method, keep uv sync as the dev/source method.

```markdown
## Install

### From PyPI (recommended)

```bash
pip install conversus
```

This installs the free engine with all 8 deliberation modes, templates, presets, CLI, MCP server, and web UI.

For solver plugins (equilibrium scoring, convergence prediction, AMPL optimization):

```bash
pip install conversus-solvers
```

### From source (development)

```bash
git clone https://github.com/Build-Fractal/conversus.git && cd conversus
uv sync                        # Python 3.11+ required
uv sync --extra solvers        # nashopt + kalman + AMPL (optional)
```
```

Note: The prerequisite section says "Python 3.12+" but `packages/core.toml` says `requires-python = ">=3.11"`. Should be reconciled to 3.11+.

---

## Gap 4: `docs/user-guide/config-reference.md` — No mention of free/paid boundary (MEDIUM)

**Status**: The config reference documents the `plugins:` key and shows nashopt/scenarios examples, but never explains which features require `conversus-solvers` (paid) vs what ships with core (free). Spec 033 Section 6 (FR-014) requires cross-tier links using the callout pattern.

**Required change**: Add a callout after the plugins section (after line 175):

```markdown
!!! info "Premium Feature"
    The `equilibrium-scorer` and `scenario-runner` plugins shown above require the paid `conversus-solvers` package.
    Install with `pip install conversus-solvers`.
    Without it, the deliberation runs normally — scoring is simply skipped.
```

Also, the "Three Layers" table on `docs/index.md` line 18-22 says `Free / open-core` for Engine but does not mention that the core package is MIT-licensed while solvers are commercial. A one-line addition would help:

After line 22, add:
```markdown
The engine is MIT-licensed. Solver and domain plugins are commercially licensed. See [spec 033](https://github.com/Build-Fractal/conversus) for the full free/paid feature matrix.
```

---

## Gap 5: `docs/user-guide/modes.md` — New payoff functions ARE documented (NO ACTION)

**Status**: Confirmed complete. All four new modes (negotiation, resource-allocation, fair-division, mechanism-design) include "Solver scoring" paragraphs with the correct formulas matching `payoffs.py`:

- **negotiation** (line 109): `J_i = zopa_coverage * party_satisfaction` -- matches `negotiation_payoff()` in payoffs.py line 243
- **resource-allocation** (line 132): `J_i = utilization_efficiency - allocation_inequality` -- matches `resource_allocation_payoff()` in payoffs.py line 273
- **fair-division** (line 153): `J_i = proportionality_score - envy_count / max(1, N-1)` -- matches `fair_division_payoff()` in payoffs.py line 306-308
- **mechanism-design** (line 174): `J_i = social_welfare_contribution - gaming_vulnerability_count / max(1, total_vulnerabilities)` -- matches `mechanism_design_payoff()` in payoffs.py line 340-342

This was completed in Wave 1 (spec 039). No changes needed.

---

## Gap 6: Design system (`fractal.css`) not mentioned in docs (LOW)

**Status**: `fractal.css` is loaded via `mkdocs.yml` (`extra_css: - stylesheets/fractal.css`) and is the active design system for the docs site. However, it is not mentioned in any documentation page. The developer guide and contributing docs do not explain the design system, its palette, or how to extend it.

The only references to "design system" in docs are:
- `docs/stylesheets/fractal.css` line 1 (the file itself)
- `docs/web.md` line 179 (a link to the frontend README)
- `docs/assets/images/logo.svg` line 4 (a comment)

**Required change**: Add a brief note to the developer guide contributing page or a new section in the architecture doc. Minimal addition to `docs/developer-guide/contributing.md` (or wherever the site build is documented):

```markdown
## Design System

The docs site uses the Build Fractal design system defined in `docs/stylesheets/fractal.css`.

| Token | Value | Usage |
|-------|-------|-------|
| Primary | `#53dad2` (Oxidized Teal) | Links, headings, active nav |
| Accent | `#e8a54a` (Patina Bronze) | Hover states, warnings, focus rings |
| Surface | `#1e2020` | Page background |
| Code surface | `#121414` | Code blocks, footer |

Typography: Helvetica Neue for body text, Space Grotesk for headings and code.

When adding new documentation pages, no special styling is needed — the Material theme tokens are overridden globally.
```

---

## Summary

| # | File | Gap | Severity | Action |
|---|------|-----|----------|--------|
| 1 | `docs/index.md` | No `pip install` path | CRITICAL | Add pip install as primary install method |
| 2 | `docs/index.md` | Three `clariti-care` URLs + wrong license label | CRITICAL | Replace with `Build-Fractal`; change "proprietary" to "MIT" |
| 3 | `docs/user-guide/quickstart.md` | Still shows only dev install flow | MEDIUM | Add PyPI install as primary path |
| 4 | `docs/user-guide/config-reference.md` | No free/paid boundary callout | MEDIUM | Add Premium Feature callout for solver plugins |
| 5 | `docs/user-guide/modes.md` | New payoff functions | NONE | Already complete (Wave 1) |
| 6 | `docs/stylesheets/fractal.css` | Not mentioned in any docs page | LOW | Add design system section to contributing guide |

### Additional inconsistencies found

- **Python version mismatch**: `quickstart.md` says 3.12+, `core.toml` says `>=3.11`. Reconcile to 3.11+.
- **License drift**: Index badge says "proprietary" but core package is MIT. The free/paid split means the core license is MIT and solvers are commercial — the badge should reflect the core.
- **`.do/app.yaml`**: Still references `clariti-care/conversus` (line 10). Outside docs scope but should be fixed.
- **SDK namespace note**: `docs/user-guide/sdk.md` line 12 says `engine` package "will be renamed to `conversus` in a future release." With the package split complete (032), this note should be reviewed — the CLI entry point is still `engine.cli:main` per `core.toml` line 23, so the rename has not happened yet. The note is still accurate but could reference the package split timeline.
