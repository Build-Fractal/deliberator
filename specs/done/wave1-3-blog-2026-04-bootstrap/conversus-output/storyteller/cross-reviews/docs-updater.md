# Storyteller Cross-Review of Docs-Updater

**Reviewer**: storyteller
**Reviewing**: docs-updater
**Date**: 2026-04-03

---

## Overall Assessment

The docs-updater's gap analysis is thorough and technically accurate. Every gap identified is real, and the severity rankings are defensible. But the review is written from inside the codebase looking out. My cross-review evaluates the gaps from outside looking in -- specifically, from the perspective of a reader who just finished the Wave 1-3 blog posts and is now navigating the docs for the first time.

That reader journey is the one that matters. The blog posts make specific promises. The docs must deliver on them.

---

## 1. Do the doc gaps align with the story the blog posts tell?

Yes, but incompletely. The docs-updater caught the two structural gaps that the blog posts directly expose:

- **Gap 1 (no `pip install` path)**: Blog Post 1 opens with "we needed to turn this into something you could `pip install`" and ends with "`pip install conversus` is a real thing." The index page still says `git clone`. This is a direct contradiction of the blog's central narrative.

- **Gap 4 (no free/paid boundary callout)**: Blog Post 1 devotes its entire final third to the free/paid split. Blog Post 2 structures the whole argument around "deliberation is free, scoring is paid." The config reference shows `equilibrium-scorer` and `scenario-runner` plugin examples without explaining that these require a separate paid package. A reader who just learned the free/paid distinction in the blog will find the config reference strangely silent on the topic.

The docs-updater also caught the `clariti-care` org references (Gap 2), which is important for basic link integrity but is not something the blog posts would expose -- the blogs use no GitHub URLs. Still a valid gap, just not a narrative-driven one.

---

## 2. Would a reader who reads the blog posts and then visits the docs be confused by the gaps?

Yes, and the confusion has a specific shape. The blog posts establish a three-act story:

1. **Act 1**: The engine was monolith-only, half the modes lacked scoring.
2. **Act 2**: Path resolution was fixed, import boundaries were verified.
3. **Act 3**: `pip install conversus` now works; free tier is complete, paid tier extends it.

A reader arriving at `docs/index.md` after reading this story will:

- Look for `pip install conversus` and find `git clone`. **Immediate trust break.** The blog said the hard part is done. The docs say it never happened.
- Look for the free/paid distinction in the quickstart or config reference and find nothing. The blog spent thousands of words explaining why "deliberation is free, scoring is paid" matters. The docs treat conversus as a single undifferentiated package.
- Try running `conversus decide ...` (as shown in the quickstart) and wonder whether they need `uv run` prefix or not, because the CLI reference says one thing and the quickstart implies another. The blog posts sidestep this by only showing `pip install`, which makes the bare `conversus` command correct.

The confusion is not just "something is missing." It is "the blog told me one thing and the docs tell me the opposite." That is worse than a gap. It is a contradiction that undermines the credibility of both the blog and the docs.

---

## 3. Are there gaps the updater missed that the blog posts would expose?

Three.

### Missed Gap A: The CLI reference assumes `uv sync`, not `pip install`

The docs-updater flagged the quickstart (Gap 3) but did not flag `docs/user-guide/cli.md`. Line 6 says:

> If you installed via `uv sync` (recommended), prefix commands with `uv run`

After Wave 3, `pip install conversus` is the recommended install method for users. The CLI reference should reflect this. A pip-installed user runs `conversus run config.yml` directly -- no `uv run` prefix. The blog posts describe a world where `pip install` is primary. The CLI reference describes a world where `uv sync` is primary. These are incompatible.

The note should be inverted: `pip install` as primary (bare `conversus` command), `uv sync` as the dev/contributor path (with `uv run` prefix).

**Severity**: MEDIUM. Every pip-install user will see this note and wonder whether they're using the tool wrong.

### Missed Gap B: The SDK page's `from engine import ...` namespace

The docs-updater mentioned this in passing (the "SDK namespace note" bullet in "Additional inconsistencies") but did not classify it as a gap. It should be.

Blog Post 1 describes the package as `conversus`. The build configs produce a package named `conversus`. But `docs/user-guide/sdk.md` line 18 shows:

```python
from engine import Deliberation, Result, validate
```

A reader who just `pip install`-ed `conversus` will try `from conversus import Deliberation` and get an ImportError. The note on line 12 ("The `engine` package will be renamed to `conversus` in a future release") is honest but insufficient. It should be a prominent warning at the top of the SDK page, not a buried aside, and it should explicitly tell the user what to import.

**Severity**: HIGH. The SDK page is the second place a developer goes after the quickstart. The import path must match the package name the blog posts advertise.

### Missed Gap C: The web UI install path

Blog Post 1 mentions "CLI, MCP server, web UI" as part of the free tier. `docs/web.md` line 29 shows:

```bash
uv sync --group web
```

There is no mention of how a pip-install user gets the web UI. `core.toml` lists `web = ["fastapi>=0.100", "uvicorn>=0.20"]` as an optional dependency, which means the pip path is `pip install conversus[web]`. But the web docs page does not say this.

A blog reader who sees "web UI" in the free tier description and then visits the web docs will find only the dev install path.

**Severity**: LOW. Most users will not start with the web UI. But it is a gap the blog creates and the docs do not fill.

---

## 4. Which gaps matter most for the user journey (blog -> docs -> pip install)?

Ranked by impact on the first-contact experience:

| Priority | Gap | Why |
|----------|-----|-----|
| **1** | Gap 1 -- no `pip install` on index page | This is the single promise the blog makes most loudly. If the landing page contradicts it, the reader bounces. |
| **2** | Missed Gap B -- SDK imports say `from engine` | The second thing a developer does after install is write code. If the import path is wrong, they think the install is broken. |
| **3** | Gap 3 -- quickstart still shows dev-only install | The quickstart is the first page linked from the index. It must match the index. |
| **4** | Missed Gap A -- CLI reference assumes `uv sync` | Every CLI user sees this note. It should not contradict the install method. |
| **5** | Gap 4 -- no free/paid callouts in config reference | A blog reader will look for the boundary. Not finding it is confusing but not blocking. |
| **6** | Gap 2 -- stale `clariti-care` URLs | Broken links are bad but not contradictions. A reader who clicks through gets a 404, not misinformation. |
| **7** | Missed Gap C -- web UI install path missing | Niche audience. Low urgency. |
| **8** | Gap 6 -- design system undocumented | Internal contributor concern, not user-facing. |

---

## Summary for Synthesis

The docs-updater's review is accurate and actionable. Four of its six gaps are correctly identified and correctly prioritized. Gap 5 (modes.md already complete) is a useful confirmation. Gap 6 (design system) is genuine but irrelevant to the blog-to-docs user journey.

The review misses three gaps that the blog posts directly create: the CLI reference's `uv sync`-first framing, the SDK page's `from engine` import path, and the web UI install path. Of these, the SDK import path is the most dangerous because it will cause an immediate failure for any developer who follows the blog's `pip install conversus` advice and then tries to use the SDK.

The docs-updater's proposed fixes are well-structured and ready to implement. The priority ordering should be adjusted to front-load the changes that close the gap between what the blog promises and what the docs deliver. The index page (`pip install`), the SDK page (`from engine` warning), and the quickstart (dual install paths) should ship as a single coordinated update. The config reference callouts and CLI note inversion can follow.
