# User Advocate Review: First-Encounter Evaluation (Revised)

**Reviewer**: New-user persona (no prior knowledge of conversus)
**Date**: 2026-04-03
**Revision basis**: Original review revised per cross-reviews from code-verifier and editor

---

## Revision Summary

This revision incorporates three substantive corrections and two strategic reframings from cross-reviews:

1. **Adopted**: Editor's two-track promotion strategy. Post 04 should NOT be rewritten as a pitch -- it is an engineering retrospective that serves a different audience at a different funnel stage. Post 05 goes to LinkedIn first; Post 04 goes to Hacker News / Python communities second.
2. **Adopted**: Code-verifier's finding that the `decide` CLI only supports 4 of 8 modes (cooperative, winner-take-all, prisoners-dilemma, red-blue). The blog's "all 8 modes" claim creates a concrete expectation gap for new users.
3. **Corrected**: Entry point inconsistency (P1-3) is a non-issue. Code-verifier confirmed both `pyproject.toml` and `core.toml` declare `engine.cli:cli`. The original review inherited this error from the synthesis.
4. **Accepted**: Editor's reframing of Post 04's weakness -- it does not need a product-pitch opening; it needs a single context sentence and a different promotion channel.
5. **Accepted**: Editor's nuance on LinkedIn word count -- the issue is the density cliff in the middle, not total word count.

---

## 1. Post 04 ("From Heuristics to pip install") -- Engineering retrospective, not acquisition post

**Original verdict**: "I would understand what the team *did*, but not what the product *is*."

**Revised verdict**: The original verdict stands, but the recommendation changes. Post 04 is a well-constructed engineering retrospective. The editor's cross-review correctly argues that rewriting it as a product pitch would weaken it for its natural audience -- developers who discover it through search terms like "monolith to pip install," "build-time package splitting," or Python packaging communities.

The correct response is not to rewrite Post 04 but to route it to the right audience through the right channels:

| Post | Funnel stage | Promotion channel | Reader expectation |
|------|-------------|-------------------|-------------------|
| 05 | Awareness / top-of-funnel | LinkedIn, Twitter, AI newsletters | "I have this problem, show me a pattern" |
| 04 | Consideration / mid-funnel | Hacker News, Python communities, dev.to | "I am evaluating this tool, show me the engineering" |

Post 05 publishes first (by at least 24 hours). Post 04 follows with a single context sentence after the feature-inventory opening -- not a product pitch, just enough for a cold reader to follow the engineering narrative:

> conversus is an open-source framework that runs structured debates between AI agents and scores the results with game theory. The feature list above is what we needed to package.

This closes the comprehension gap without converting the post into something it is not.

**Specific problems from the original review that still apply:**

- The `pip install` promise is buried at ~70% of the post. The code-verifier notes this is the chronological climax of the narrative, not a buried CTA, which is fair -- but a reader scanning for "how do I try this" will still abandon before reaching it. The two-track promotion strategy resolves this: readers arriving from HN or Python communities expect engineering narratives and will read through.
- Dense jargon (Nash equilibrium quality, ZOPA coverage, stagnation detection) remains unexplained. This is acceptable for the mid-funnel engineering audience but means Post 04 should never be the first link shared to a general audience.

---

## 2. Post 05 ("Why Your AI Agents Give Different Answers") -- Strong entry point with a density cliff in the middle

**Verdict: Unchanged. This is the stronger entry point, but the middle section loses readers.**

The opening remains excellent. The problem framing is concrete and relatable. The four-step "apply this to your own system" closing is the section that earns shares.

**Revised concerns (incorporating cross-review feedback):**

- **The game-form table is a comprehension barrier, not just a pacing issue.** The editor's cross-review upgraded my "wall" assessment: this is not reader fatigue, it is a point where readers who do not know game theory cannot continue. The code-verifier confirms the terms are all used correctly -- the issue is pedagogical, not factual. Recommendation stands: reduce to 4 rows (cooperative, winner-take-all, prisoner's dilemma, negotiation), link the full 8-mode table as a reference page.

- **NEW: The "all 8 modes" claim creates a concrete expectation gap.** The code-verifier found that the `decide` CLI command restricts `--mode` to 4 choices: cooperative, winner-take-all, prisoners-dilemma, red-blue. All 8 modes are available via `conversus run` with a config file, but a new user who reads "all 8 modes" in the blog and tries `conversus decide --mode negotiation` will get an error. This is not just a jargon problem -- it is a broken promise at the CLI level. The blog should either clarify ("all 8 modes via config; 4 via quick-start CLI") or the `decide` command should be extended before publication.

- **The three-tier solver section is reference documentation in a blog post.** Recommendation unchanged: collapse to a single paragraph. "The heuristic payoffs ship with `conversus-solvers`. For constrained optimization or game-theoretic proofs, optional extras are available. See the solver documentation for details."

- **The worked example needs one context sentence.** Both the editor and this review independently identified the gap: the `prisoners_dilemma_payoff` function uses `features` (a `RoundFeatures` object) without explaining where it comes from. A single sentence ("Conversus extracts these features automatically from agent output during the cross-review phase") closes the gap.

- **Word count is not the real issue -- the density cliff is.** The editor correctly notes that LinkedIn blog-post shares are links with preview cards; readers click through expecting a full article. The problem is not 2,500 words total but the abrupt shift from accessible narrative to reference-table density in the middle. The first three paragraphs survive the click-through. The game-form table does not.

---

## 3. After reading the posts, does docs/index.md match what the posts promised?

**Verdict: Unchanged. The gap is jarring.**

All findings from the original review were confirmed by the code-verifier against source files:

- docs/index.md shows `git clone + uv sync` while the blog says `pip install conversus` -- confirmed
- Badge URLs point to `clariti-care` while the repo is at `Build-Fractal` -- confirmed
- License badge says "proprietary" while `packages/core.toml` and `LICENSE` both say MIT -- confirmed
- Quickstart assumes `uv sync` as the only install method -- confirmed

**Correction: Entry point inconsistency is a non-issue.**

The original review's gap table included "Entry point inconsistency" (P1-3) with status "needs code verification." The code-verifier has now verified: both `pyproject.toml` and `core.toml` declare `conversus = "engine.cli:cli"`. There is no inconsistency. The synthesis P1-3 was based on a stale or incorrect reading. This item is closed.

**NEW finding from code-verifier: PyPI availability ambiguity.**

The original review assumed the blog's `pip install conversus` promise was real and evaluated the docs gap on that basis. The code-verifier raises the question of whether `pip install conversus` actually resolves on PyPI today. Post 04's closing sentence qualifies this ("Packages are locally buildable via `scripts/build-packages.sh`; PyPI publication is a separate step"), but this qualification is easy to miss. If `pip install conversus` returns a 404, the blog itself is making a promise it cannot keep -- the trust gap runs in both directions, not just from blog to docs.

---

## 4. Jargon and assumptions that would lose a new reader

**Revised table (incorporating code-verifier corrections):**

| Term | Where | Problem | Code-verifier note |
|------|-------|---------|--------------------|
| Nash equilibrium | Both posts | Introduced before gloss appears. Gloss ("no agent can improve its score by changing strategy alone") exists in Post 05 but comes after several unglossed uses. | Correctly used throughout. Issue is pedagogical, not factual. |
| ZOPA | Post 05 | Acronym expanded but concept unexplained. | -- |
| Payoff function | Both posts | Used as if self-evident. | Post 05 does explain it ("a mathematical function that scores agent output... takes extracted features and returns a number"). The original review's concern is partially addressed by the existing text. |
| Payoff matrix | Original review | Flagged as jargon. | Code-verifier notes this term does not actually appear in the blog posts. Removed from the jargon list. |
| Pareto optimality / envy-freeness / incentive compatibility | Post 05 table | Six equilibrium concepts with no definitions. | All correctly used. Reducing the table to 4 rows (Section 2 recommendation) resolves the worst of this. |
| Hatch / force-include / wheel | Post 04 | Python packaging jargon. | Acceptable for Post 04's engineering audience. The two-track promotion strategy means general readers will not encounter this post first. |
| importlib.resources | Post 04 | Deep stdlib knowledge. | Same as above -- acceptable for the target audience. |
| MCP server | Both posts, README, docs | Never defined. | Confirmed: no expansion or explanation anywhere. Should be glossed at least once ("Model Context Protocol -- the protocol that lets AI assistants call external tools"). |

**Narrowed audience assumptions (revised):**

- The reader is building multi-agent AI systems -- reasonable for Post 05, and Post 04 no longer needs to serve a broader audience under the two-track strategy.
- The reader knows Python packaging -- acceptable for Post 04's target audience (HN, Python communities). Not acceptable if Post 04 were the entry point, but it is not.
- The reader has encountered agent inconsistency -- the strongest assumption. Widely relatable. Post 05 leads with this.
- The reader knows what game theory offers to AI agent evaluation -- both posts still assume this. Post 05's opening bridges the gap well; the middle section (game-form table) does not.

---

## 5. Would I share Post 05 on LinkedIn?

**Rating: 7/10 -- unchanged, but the path to 9/10 is clearer.**

**Strengths (unchanged):**

- The title is a genuine hook.
- The opening three paragraphs are concrete and relatable.
- The four-step closing is framework-agnostic and useful even without installing conversus.
- "Generate with LLMs, score with math" is memorable and quotable.

**Weaknesses (revised):**

- The density cliff in the middle (game-form table, three-tier solver section) is the primary weakness. This is not a word-count problem (the editor correctly notes LinkedIn shares are link previews, not native posts) but a comprehension-barrier problem.
- The post never gives the reader a single command to try. Both the editor (Issue 8.1) and this review identify the missing CTA. The editor's proposed closing line is exactly right: "conversus implements this pattern. `pip install conversus` gets you the deliberation engine. `pip install conversus-solvers` adds the scoring layer. Get started with the quickstart guide."

**What would make it a 9/10 share (revised to match editor's specifics):**

1. Reduce the game-form table to 4 rows (cooperative, winner-take-all, prisoner's dilemma, negotiation). Link the full table as a reference page.
2. Collapse the three-tier solver section to a single paragraph with a docs link.
3. Add the CTA after the four-step pattern.
4. Add one sentence before the worked example explaining where `RoundFeatures` comes from.

---

## 6. Gap analysis after all proposed fixes ship

**Revised table (correcting entry point item, adding mode-count gap):**

| Gap | Severity | Status |
|-----|----------|--------|
| No `pip install` on docs index | Critical | Fixed by P0-1 |
| Wrong org URL / license | Critical | Fixed by P0-2 |
| PyPI availability -- does `pip install conversus` actually resolve? | Critical | Flagged by code-verifier; must verify before blog publication |
| No `pip install` in quickstart | High | Fixed by P1-1 |
| SDK import path confusion | High | Fixed by P1-2 |
| ~~Entry point inconsistency~~ | ~~High~~ | ~~Closed -- code-verifier confirmed no inconsistency exists~~ |
| "All 8 modes" claim vs 4-mode `decide` CLI | High | NEW -- code-verifier finding. Blog must clarify or CLI must be extended |
| Free/paid language mismatch between blog and docs | Low | Downgraded per editor: compatible framings, not contradictory claims |
| README contradicts both blog and docs | Medium | Not addressed in synthesis fixes |
| No "what is this" sentence for cold readers | Medium | Not addressed in synthesis fixes |
| Game-form table inaccessible to new readers | Medium | Blog content edit, not a docs fix |

---

## Overall Assessment (Revised)

**Post 05 is the right first-contact post.** This is confirmed by all three reviews. It names a real problem, explains the pattern, and gives actionable advice. With the four edits in Section 5 (table reduction, solver collapse, CTA, context sentence), it is strong LinkedIn material.

**Post 04 is a good engineering-credibility post for a different audience.** The original review's recommendation to add a product-pitch opening was wrong. The editor's two-track promotion strategy is the correct response: Post 05 goes to LinkedIn and newsletters as the awareness post; Post 04 goes to Hacker News and Python communities as the engineering post. Post 04 needs only a single context sentence, not a rewrite.

**The `decide` CLI mode restriction is a new high-severity finding.** The blog says "all 8 modes." The CLI offers 4. A new user who tries `conversus decide --mode negotiation` after reading the blog gets an error. This must be resolved before publication -- either by clarifying the blog text or extending the CLI.

**The entry point inconsistency (P1-3) is closed.** Both config files declare `engine.cli:cli`. No fix needed.

**The doc fixes remain the hard dependency.** P0 and P1 fixes must ship before either blog post goes live. The PyPI availability question is now elevated to critical: if `pip install conversus` does not resolve, the blog's central promise is broken regardless of what the docs say.

**The remaining gaps (README alignment, cold-reader onboarding sentence) are medium-severity and should ship alongside P2 fixes.** The free/paid language mismatch is downgraded to low -- the editor is right that these are compatible framings, not contradictions.

**Publication sequence**: Post 05 first (LinkedIn, newsletters). Post 04 at least 24 hours later (HN, Python communities, dev.to). Cross-link both posts. This is the single most impactful change the editorial plan can make.
