# Code Verifier Cross-Review: User Advocate

**Cross-reviewer**: code-verifier
**Date**: 2026-04-03
**Subject**: User advocate review of Posts 04, 05, docs/index.md, quickstart.md, README.md

---

## Overall Assessment

The user-advocate review is well-structured, identifies real reader-journey problems, and correctly prioritizes the doc-fix dependency chain. Most claims hold up against the source code. There are three areas where the advocate's concerns need qualification from a technical accuracy standpoint, one area where the advocate caught something the code-verifier review missed, and one area where both reviews inherited an error from the synthesis.

---

## 1. Claims the User Advocate Got Right

### 1a. docs/index.md vs blog install path mismatch (Section 3) -- CONFIRMED

The advocate says the docs show `git clone + uv sync` while the blog says `pip install conversus`. Verified:

- `docs/index.md` lines 28-31: `git clone https://github.com/clariti-care/conversus.git && cd conversus` / `uv sync`
- Blog Post 04 and Post 05: `pip install conversus` as the primary install command

The gap is real and the advocate is correct that this is trust-breaking for any reader who clicks through from the blog.

### 1b. Stale org references (Section 3) -- CONFIRMED

The advocate says the docs reference `clariti-care` while the repo has moved to `Build-Fractal`. Verified:

- `docs/index.md` line 10: badge URL points to `github.com/clariti-care/conversus`
- `docs/index.md` line 11: license badge points to `clariti-care`
- `docs/index.md` line 29: clone URL uses `clariti-care`
- `mkdocs.yml` lines 3-5: `repo_url` points to `Build-Fractal`
- `LICENSE` file: "Copyright (c) 2026 Build Fractal"

The advocate is correct: a reader clicking the badge gets a 404 or wrong repo.

### 1c. License badge says "proprietary" (Section 3) -- CONFIRMED

- `docs/index.md` line 11: badge label is `proprietary`
- `packages/core.toml` line 10: license is `MIT`
- `LICENSE` file: MIT License

The advocate correctly identifies this as contradicting the open-core framing in both blog posts.

### 1d. quickstart.md assumes `uv sync` as only install method (Section 3) -- CONFIRMED

- `docs/user-guide/quickstart.md` lines 9-14: shows only `git clone <repo-url>` + `uv sync`
- No `pip install conversus` option is presented

The advocate's concern that a pip-install user would be confused by `uv run conversus decide ...` is valid. A user who installed via `pip install conversus` would run `conversus decide ...` directly.

### 1e. README contradicts blog and docs (Section 6, "What the doc fixes miss") -- CONFIRMED

The advocate identifies that the README is not addressed in any P-level doc fix. Verified:

- `README.md` line 50: `git clone <repo-url> conversus && cd conversus` -- uses a placeholder URL, not even a real URL
- `README.md` line 77: `from engine import Deliberation` -- uses the `engine` namespace, which is the current reality but contradicts the blog's `conversus` framing

The advocate is correct that a reader landing on the GitHub repo page gets a different experience than either the blog or the docs. This gap is not addressed in the synthesis doc fixes.

### 1f. "Three Layers" table language mismatch (Section 6) -- CONFIRMED

The advocate says the docs table uses "Free / open-core," "Premium plugins," "Platform" while the blog uses "deliberation is free, scoring is paid." Verified:

- `docs/index.md` lines 18-22: "Engine / Free / open-core", "Solvers / Premium plugins", "Domains / Platform"
- Blog Post 04 line 245-249: "deliberation is free, scoring is paid"

These are different framings. A reader arriving from the blog expects the language they just read. The advocate is correct that this mismatch is not addressed in any P-level fix.

### 1g. MCP is never defined (Section 4, jargon table) -- CONFIRMED

The advocate flags that "MCP server" and "MCP-compatible editor" are used without defining MCP. Verified across the blog posts in the synthesis: MCP appears in Post 04 lines 105 and 247. Neither instance expands the acronym or explains what MCP is. The `quickstart.md` line 74 says "MCP-compatible editor" but does not define it either.

For a blog post targeting readers beyond the Claude Code ecosystem, this is a valid accessibility concern. "Model Context Protocol" or even "(MCP -- the protocol that lets AI assistants call external tools)" would close the gap.

---

## 2. Claims the User Advocate Got Right That the Code Verifier Missed

### 2a. No "what is conversus" sentence in docs/index.md for cold readers

The advocate's Section 6 says: "The docs index opens with 'Competitive multi-agent deliberation framework' -- this is a category label, not a value proposition." The code-verifier review focused on verifying technical claims in the blog posts and doc fix recommendations but did not evaluate whether the docs/index.md tagline serves a cold reader.

The advocate is right. The docs index assumes the reader already knows what multi-agent deliberation is. A single plain-language sentence after the tagline would help. This is a content gap, not a technical inaccuracy, but it is the kind of gap that undermines the entire blog-to-docs funnel.

---

## 3. Claims That Are Valid Concerns But Technically Overstated

### 3a. Game-form table jargon (Section 2 and Section 4)

The advocate says the 8-mode table with "Bayesian Nash equilibrium," "Core stability," "Envy-freeness," and "Incentive compatibility" is inaccessible to new readers. This is a valid UX concern.

However, the advocate frames these as terms the reader has "never seen in the context of AI agents." From a technical accuracy standpoint, these terms are standard game theory concepts with precise definitions, and the blog post uses them correctly:

- **Nash equilibrium**: correctly glossed in Post 05 ("no agent can improve its score by changing strategy alone" -- the advocate acknowledges this gloss exists but says it appears too late).
- **Pareto optimality**: correctly applied to the cooperative mode where the goal is that no agent can improve without making another worse off.
- **Envy-freeness**: correctly applied to fair-division, where it means no agent prefers another's allocation.
- **Incentive compatibility**: correctly applied to mechanism design, where it means agents' best strategy is to report truthfully.

The advocate's recommendation to add a "when to use this" column or a preamble is sound advice for readability. But the terms themselves are accurately used, and the mapping from deliberation mode to game form is technically correct. The issue is pedagogical, not factual.

### 3b. "Payoff function / payoff matrix" as jargon (Section 4)

The advocate flags "payoff function" and "payoff matrix" as game theory terminology used as if self-evident. These terms are used correctly throughout both posts. Post 05 does explain what a payoff function does: "a mathematical function that scores agent output... takes extracted features from the output and returns a number" (lines 339-341 of the synthesis). The term "payoff matrix" does not actually appear in the blog posts -- the advocate may be conflating it with the game-form table.

### 3c. "Hatch / force-include / wheel" as jargon (Section 4)

The advocate flags these as Python packaging jargon that excludes polyglot readers. This is true, but Post 04 is explicitly about Python packaging engineering. The post's title includes "pip install." Its audience is Python developers or people evaluating a Python framework. Expecting a packaging-focused post to avoid packaging terminology would gut the technical content. The advocate's own assessment acknowledges this: "Reasonable for a Python-developer audience, but excludes polyglot readers."

---

## 4. Claims That Are Technically Incorrect or Need Correction

### 4a. "pip install promise is buried" at 70% of the way through Post 04 (Section 1)

The advocate says: "The actual install commands do not appear until the Wave 3 section, roughly 70% of the way through the post."

This is partially inaccurate. Post 04's opening paragraph (line 107 of the synthesis) says: "We needed to turn this into something you could `pip install`." The `pip install` framing appears at the top as the goal of the work. The specific commands (`pip install conversus`, `pip install conversus-solvers`) appear in the Wave 3b section, which is indeed in the latter half of the post. But the post's narrative arc is building toward that moment -- it is not "buried" so much as it is the climax of a chronological story. The advocate is applying blog-post UX expectations (CTA early and often) to an engineering retrospective that structures information chronologically.

That said, the advocate's recommendation (Post 04 should not be the first post a new user encounters) is correct regardless of this framing point.

### 4b. Entry point inconsistency claim (Section 6, inherited from synthesis)

The advocate's gap table (Section 6) includes "Entry point inconsistency" with status "Flagged as P1-3, needs code verification." This was inherited from the synthesis document (P1-3), which claimed `pyproject.toml` declares `engine.cli:cli` while `core.toml` declares `engine.cli:main`.

**This claim is incorrect.** Both files declare the same entry point:

- `pyproject.toml` line 24: `conversus = "engine.cli:cli"`
- `packages/core.toml` line 23: `conversus = "engine.cli:cli"`

There is no inconsistency. The synthesis P1-3 was based on a stale or incorrect reading of `core.toml`. The code-verifier review (my own Section 8) amplified this error by claiming the inconsistency was "WORSE THAN DESCRIBED" and that `engine.cli:main` does not exist. While it is true that no `main` function exists in `engine/cli/__init__.py`, the premise was wrong -- `core.toml` never references `main`.

**Impact**: The user-advocate's gap table correctly marks this as "needs code verification." The verification result is: no inconsistency exists. P1-3 can be closed as not applicable.

---

## 5. Accuracy Issues the User Advocate Missed

### 5a. "All 8 modes" oversimplification in Post 04

Post 04 (synthesis line 247) says: "The free tier (`pip install conversus`) ships the complete deliberation engine. All 8 modes."

The `decide` CLI command (`engine/cli/__init__.py` lines 238-243) restricts `--mode` to 4 choices: cooperative, winner-take-all, prisoners-dilemma, red-blue. All 8 modes are available via `conversus run` with a config file, as correctly noted in `docs/index.md` line 62.

A new user who reads "All 8 modes" in the blog, installs via `pip install conversus`, and tries `conversus decide --mode negotiation` will get an error. The user-advocate review focuses on jargon and reader journey but does not catch this specific expectation gap. The editor review flags this as Issue 2.1/2.4 territory but does not call out the mode-count discrepancy specifically. The code-verifier review catches this in Section 9c.

### 5b. Post 04 mentions only 2 of 4 core.toml exclusion patterns

The blog says `core.toml` excludes `conversus/plugins/nashopt/**` and `conversus/plugins/optimizer/**`. The actual file also excludes `conversus/plugins/scenarios/**` and `conversus/domains/implementations/**`. This means the free tier excludes more than the blog describes. A reader who checks `core.toml` after reading the blog will see two additional exclusion patterns that were not mentioned.

This is a simplification, not a falsehood, but the user-advocate review does not flag it. The code-verifier review catches this in Section 2.

### 5c. PyPI publication status ambiguity

The editor review catches this as Issue 2.1 (P1), but the user-advocate review does not directly address whether `pip install conversus` actually works today. The advocate assumes the blog's promise is real and evaluates the docs gap on that basis. If `pip install conversus` currently returns a 404 on PyPI, the advocate's entire Section 3 analysis ("trust-breaking mismatch") applies in both directions -- the blog is also making a promise it cannot keep, not just the docs.

Post 04's closing sentence (synthesis line 292) qualifies this: "Packages are locally buildable via `scripts/build-packages.sh`; PyPI publication is a separate step that follows when the distribution channel is ready." This qualification exists but is easy to miss, and the advocate does not flag the risk that the blog itself overpromises.

---

## 6. Assessment of the User Advocate's Recommendations

### Recommendations that are sound from a technical accuracy standpoint

| Recommendation | Assessment |
|---|---|
| Post 05 should be the first-contact post, not Post 04 | Correct. Post 05 names a problem; Post 04 narrates a solution to an engineering challenge. |
| Cut the game-form table to 3-4 rows for the blog | Reasonable. The full 8-row table is technically accurate but pedagogically overwhelming. |
| Add a "try it" CTA after the four-step pattern in Post 05 | Correct. The editor review independently identifies this as Issue 8.1 (P1). |
| P0 and P1 doc fixes must ship before blog publication | Correct. Both the code-verifier and editor reviews agree. |
| Add "what is conversus" sentence for cold readers in docs/index.md | Valid gap not caught by other reviews. |
| Address README separately | Valid gap not caught by other reviews. |

### Recommendations that need qualification

| Recommendation | Qualification |
|---|---|
| Trim the three-tier solver section to a single paragraph | The three-tier section contains install commands that are the only documentation of solver extras. If trimmed, this information must appear somewhere else (e.g., the quickstart or a dedicated install page). |
| Move the full game-form table to a "deep dive" link | The table is the only place in the blog posts that documents which equilibrium concept maps to which mode. If moved, verify the linked page exists and is accessible. |

---

## 7. Summary

The user-advocate review is accurate in its core thesis: the reader journey from blog to docs is broken, and the jargon level in Post 05's middle section is a barrier for non-specialist readers. The technical claims flagged as jargon are all used correctly in the blog -- the issue is pedagogical, not factual. The advocate catches three gaps (README, "what is conversus" sentence, Three Layers language mismatch) that neither the code-verifier nor the editor reviews flag.

The advocate inherits one error from the synthesis (the entry point inconsistency P1-3), which code verification shows does not exist -- both `pyproject.toml` and `core.toml` declare `engine.cli:cli`. The code-verifier review also inherited and amplified this same error, which is corrected here.

The advocate misses the "all 8 modes" CLI restriction (only 4 are available via `decide`), the `core.toml` exclusion simplification, and does not evaluate whether `pip install conversus` actually resolves on PyPI today.

**Net assessment**: The user-advocate review is a strong complement to the code-verifier and editor reviews. It identifies the right gaps for the right reasons. Its technical accuracy is high, with the caveats noted above.
