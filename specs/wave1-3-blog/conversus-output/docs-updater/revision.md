# Docs Updater Revised Gap Analysis

**Original review**: 2026-04-03
**Revised**: 2026-04-03
**Inputs**: Cross-reviews from technical-writer and storyteller; own cross-reviews of both.

---

## What changed in this revision

The original review identified six gaps at the right severity levels. Cross-reviews from the technical-writer and storyteller surfaced corrections and additions that materially improve the analysis:

1. **Gap 1 reframed**: The missing `pip install` path was not an oversight -- it was deliberately removed by the earlier 55-agent review (blog post 3) because the package was not yet published. Now that spec 032 has shipped, the fix direction reverses. This revision reflects the correct chronology.
2. **New P0 gap added**: `Architecture` blog category not in `mkdocs.yml` `categories_allowed`. Build will fail.
3. **Three storyteller-identified gaps added**: SDK import path (`from engine` vs `from conversus`), CLI reference `uv sync`-first framing, web UI install path.
4. **Python version handling corrected**: Not a blanket "reconcile to 3.11+" -- the two numbers serve different contexts (published package vs dev environment).
5. **Entry point inconsistency added**: `pyproject.toml` declares `engine.cli:cli`, `core.toml` declares `engine.cli:main`.
6. **Priority reordering**: Index + quickstart + SDK as a single coordinated critical-path change.

---

## P0 -- Must fix before publishing (build-breaking or trust-breaking)

### P0-1: `docs/index.md` -- Restore `pip install` as primary install path

**Status**: The index page shows `git clone` + `uv sync` as the only install method. Blog Post 1's entire narrative culminates in "`pip install conversus` is a real thing." If a reader visits the index page after reading the blog, they see a direct contradiction.

**Correction from technical-writer**: This is not a gap that was "missed." The earlier 55-agent documentation review (blog post 3, line 59) deliberately changed the index page FROM `pip install conversus` TO `git clone` + `uv sync` because the package was not yet published to PyPI. That fix was correct at the time. Now that spec 032 (build-time package splitting) has shipped, the fix direction reverses: `pip install conversus` should be restored as the primary path.

**Correction from technical-writer on `[all]` extra**: The proposed text should clarify that `pip install conversus[all]` pulls in three sub-packages (`conversus-solvers`, `conversus-scenarios`, `conversus-swe`), not just solvers. This matches `packages/core.toml` line 20.

**Required change** (replaces index.md lines 28-31):
```markdown
## Quick Install

```bash
pip install conversus                    # Free: engine + 8 modes + templates + CLI
pip install conversus-solvers            # Paid: equilibrium scoring, convergence (optional)
pip install conversus[all]               # All sub-packages: solvers, scenarios, swe (optional)
```

!!! tip "Development setup"
    To work on conversus itself (Python 3.12+ required):
    ```bash
    git clone https://github.com/Build-Fractal/conversus.git && cd conversus
    uv sync
    ```
```

### P0-2: `docs/index.md` -- Three stale `clariti-care` org references + wrong license label

**Status**: Unchanged from original review. `mkdocs.yml` lines 3-5 already use `Build-Fractal`. Three URLs in `docs/index.md` still reference `clariti-care`. License badge says "proprietary" but `core.toml` declares `license = "MIT"` for the free tier.

**Required changes**:
- Line 10: Tests badge URL `clariti-care` -> `Build-Fractal`
- Line 11: License badge `clariti-care` -> `Build-Fractal`, label `proprietary` -> `MIT`
- Line 29: Clone URL `clariti-care` -> `Build-Fractal`

### P0-3: `mkdocs.yml` -- `Architecture` not in `categories_allowed` (NEW)

**Source**: Technical-writer cross-review, Missed Gap A.

**Status**: Blog Post 2 uses `Architecture` as a category in its frontmatter. `mkdocs.yml` lines 40-43 only allow three categories: `Engineering`, `Process`, `Release`. The MkDocs blog plugin will either error at build time or silently drop the post.

**Required change**: Add `Architecture` to `categories_allowed` in `mkdocs.yml`:
```yaml
categories_allowed:
  - Engineering
  - Process
  - Release
  - Architecture
```

---

## P1 -- Critical path: Ship as a single coordinated update

The storyteller's cross-review made a key observation: the index page, quickstart, and SDK page form a single reader journey. A reader who hits `pip install conversus` on the index will immediately visit the quickstart and then the SDK page. All three must be consistent. These should ship as one coordinated change.

### P1-1: `docs/user-guide/quickstart.md` -- Add PyPI install as primary path

**Status**: Unchanged from original review. The quickstart shows only the dev workflow (`git clone` + `uv sync`).

**Correction from technical-writer on Python version**: The original review said "reconcile to 3.11+." This was too simple. The two version numbers serve different contexts:
- `packages/core.toml` says `requires-python = ">=3.11"` -- this is the published package, with lighter dependencies (pydantic, pyyaml, click). 3.11 support is plausible.
- Root `pyproject.toml` says `requires-python = ">=3.12"` -- this is the development environment with all dependencies (anthropic, fastapi, supabase, etc.).

The quickstart should distinguish:
- `pip install conversus`: Python 3.11+
- Development from source (`uv sync`): Python 3.12+

**Required change** (replaces quickstart.md lines 9-20):
```markdown
## Install

### From PyPI (recommended)

```bash
pip install conversus              # Python 3.11+
```

This installs the free engine with all 8 deliberation modes, templates, presets, CLI, and MCP server.

For solver plugins (equilibrium scoring, convergence prediction):

```bash
pip install conversus-solvers      # Paid: nashopt, Kalman, AMPL (optional)
```

### From source (development)

```bash
git clone https://github.com/Build-Fractal/conversus.git && cd conversus
uv sync                            # Python 3.12+ required
uv sync --extra solvers            # nashopt + kalman + AMPL (optional)
```
```

### P1-2: `docs/user-guide/sdk.md` -- `from engine` import path is misleading (NEW)

**Source**: Storyteller cross-review, Missed Gap B.

**Status**: The SDK page (line 18) shows:
```python
from engine import Deliberation, Result, validate
```

A reader who just ran `pip install conversus` will try `from conversus import Deliberation` and get an ImportError. The note on line 12 ("The `engine` package will be renamed to `conversus` in a future release") is buried and insufficient.

The blog posts present the package as `conversus`. The build configs produce a package named `conversus`. But the actual Python import path is `engine`.

**Required change**: Add a prominent warning at the top of the SDK page, before any code examples:

```markdown
!!! warning "Import path"
    The Python package is installed as `conversus` but the import namespace is currently `engine`:
    ```python
    from engine import Deliberation, Result, validate  # correct
    # from conversus import ...                        # not yet — see roadmap
    ```
    The `engine` namespace will be renamed to `conversus` in a future release.
```

### P1-3: Entry point inconsistency between dev and published package (NEW)

**Source**: Own cross-review of storyteller (section 4h).

**Status**: The development `pyproject.toml` line 24 declares the CLI entry point as `engine.cli:cli`, while `packages/core.toml` line 23 declares it as `engine.cli:main`. These are different callables. If `cli` is a Click group and `main` is a wrapper that calls `cli()`, they may behave identically. But if they differ, a pip-installed user gets different CLI behavior than a dev-installed user.

**Required change**: Verify that `engine.cli:cli` and `engine.cli:main` resolve to the same behavior. If they do, align both files to use the same entry point string for consistency. If they differ, document which is canonical.

---

## P2 -- Should fix before publishing

### P2-1: `docs/user-guide/config-reference.md` -- No free/paid boundary callout

**Status**: Unchanged from original review. The `plugins:` section shows `equilibrium-scorer` and `scenario-runner` examples without indicating these require the paid `conversus-solvers` package.

**Improvement from technical-writer**: The callout should cross-reference the existing graceful-failure documentation at line 175 ("If a `package` cannot be imported, a warning is logged and that plugin is skipped"):

```markdown
!!! info "Premium Feature"
    The `equilibrium-scorer` and `scenario-runner` plugins require the paid
    `conversus-solvers` package. Install with `pip install conversus-solvers`.
    Without it, these plugins are skipped (see note above) and the deliberation
    completes normally without scoring.
```

### P2-2: `docs/user-guide/cli.md` -- Install note assumes `uv sync` as primary (NEW)

**Source**: Storyteller cross-review, Missed Gap A; technical-writer cross-review, Missed Gap B.

**Status**: CLI reference line 5-6 says:
> If you installed via `uv sync` (recommended), prefix commands with `uv run`. If you installed via `pip install -e .`, use `conversus` directly.

After Wave 3, the framing should be inverted: `pip install` as primary (bare `conversus` command), `uv sync` as the dev/contributor path (with `uv run` prefix).

**Required change**: Rewrite the install note:
```markdown
If you installed via `pip install conversus` (recommended), run commands directly:
`conversus run config.yml`. If you're developing from source with `uv sync`,
prefix commands with `uv run`.
```

### P2-3: Solver install extras not documented anywhere

**Source**: Technical-writer cross-review, Inconsistency 3.

**Status**: Blog Post 2 shows `pip install conversus-solvers[ampl]` and `pip install conversus-solvers[nashopt]`. These extras match `packages/solvers.toml` lines 17-19. But no docs page documents the per-extra install syntax. The quickstart bundles everything as `uv sync --extra solvers`.

**Required change**: Add the extras to either the quickstart install section or the config reference:
```markdown
For specific solver backends:
```bash
pip install conversus-solvers[nashopt]    # Nash equilibrium (jax)
pip install conversus-solvers[ampl]       # AMPL/HiGHS optimization
```
```

---

## P3 -- Nice to have

### P3-1: `docs/web.md` -- Web UI install path for pip users (NEW)

**Source**: Storyteller cross-review, Missed Gap C.

**Status**: Blog Post 1 lists "CLI, MCP server, web UI" as part of the free tier. `docs/web.md` line 29 shows only `uv sync --group web`. The pip path is `pip install conversus[web]` (per `core.toml` optional dependencies), but this is not documented.

**Required change**: Add pip install option to the web docs page:
```markdown
### From PyPI
```bash
pip install conversus[web]          # Adds FastAPI + Uvicorn
```

### From source
```bash
uv sync --group web
```
```

### P3-2: `docs/stylesheets/fractal.css` -- Design system undocumented

**Status**: Unchanged from original review. `fractal.css` is the active design system but is not mentioned in any docs page. Purely internal contributor concern with no blog-reader impact.

### P3-3: `conversus/paths.py` not in architecture docs

**Source**: Technical-writer cross-review, Missed Gap C.

**Status**: Blog Post 1 describes `conversus/paths.py` as the central path resolution module (the key deliverable of Wave 2). `docs/developer-guide/architecture.md` does not mention it. Developer-facing, low urgency.

### P3-4: Blog Post 1 test count verification

**Source**: Technical-writer cross-review, Missed Gap D.

**Status**: Blog Post 1 claims "31 tests" in `test_package_split.py`. Own cross-review of storyteller verified the parametrized count totals approximately 31 (section 1d: 8 + 2 + 3 + 8 + 6 + 3 = 30, plus potential edge cases in collection). Acceptable.

---

## Gap removed from original review

### Gap 5 (modes.md payoff functions) -- NO ACTION

Confirmed complete in original review. All four new payoff formulas match the source code. Cross-reviews agree.

---

## Summary table

| Priority | # | File | Gap | Source |
|----------|---|------|-----|--------|
| P0 | 1 | `docs/index.md` | Restore `pip install` (deliberately removed earlier, now needs restoring) | Original, reframed per tech-writer |
| P0 | 2 | `docs/index.md` | Three `clariti-care` URLs + "proprietary" license label | Original |
| P0 | 3 | `mkdocs.yml` | `Architecture` not in `categories_allowed` | Tech-writer cross-review |
| P1 | 1 | `docs/user-guide/quickstart.md` | Still shows only dev install; needs dual Python version context | Original, corrected per tech-writer |
| P1 | 2 | `docs/user-guide/sdk.md` | `from engine` import path contradicts `pip install conversus` | Storyteller cross-review |
| P1 | 3 | `pyproject.toml` / `core.toml` | Entry point `engine.cli:cli` vs `engine.cli:main` | Own cross-review of storyteller |
| P2 | 1 | `docs/user-guide/config-reference.md` | No free/paid boundary callout | Original, improved per tech-writer |
| P2 | 2 | `docs/user-guide/cli.md` | Install note assumes `uv sync` as primary | Storyteller + tech-writer |
| P2 | 3 | Quickstart or config reference | Solver extras syntax undocumented | Tech-writer cross-review |
| P3 | 1 | `docs/web.md` | Web UI pip install path missing | Storyteller cross-review |
| P3 | 2 | Contributing guide | Design system undocumented | Original |
| P3 | 3 | Architecture docs | `conversus/paths.py` absent | Tech-writer cross-review |

## Critical path for pre-publication

Ship P0-1 + P0-2 + P0-3 + P1-1 + P1-2 as a **single coordinated commit**. These five changes close the gap between what the blog posts promise and what the docs deliver. P1-3 (entry point consistency) requires investigation first. P2 items can follow immediately after.

The sequence matters: a reader arrives at the index, clicks to the quickstart, then opens the SDK page. If any of those three contradict the blog's `pip install conversus` narrative, the reader's trust breaks at that point. All three must be consistent before the blog posts go live.
