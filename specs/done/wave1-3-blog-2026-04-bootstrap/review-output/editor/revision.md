# Technical Editor Review: Posts 04 and 05 (Revised)

**Reviewer**: Technical Editor
**Date**: 2026-04-03
**Source**: `specs/wave1-3-blog/conversus-output/summary/final.md` (Section 3)
**Comparisons**: Posts 01-03 in `docs/blog/posts/`
**Revision basis**: Cross-reviews from code-verifier and user-advocate

---

## Verdict: Publish with revisions

Both posts are the best-written entries in the series so far. The narrative arcs are clear, the technical depth is appropriate, and the synthesis process resolved real disputes well. The revision scope below reflects both my original findings and valid escalations from cross-reviewers -- particularly the entry point bug I missed entirely and the audience-accessibility concerns the user-advocate surfaced.

---

## 1. Quality: Narrative Structure

### Post 04: A-

Strong three-act structure (monolith / portable / monetizable). The problem-first opening ("The Two Problems Blocking Users") is effective -- it immediately tells the reader why the work matters. The wave-by-wave progression provides natural pacing. The summary table at the end ties the arc together cleanly.

**One structural issue**: The "Wave 3b: Drawing the Line" section is half the post's length. It introduces the free/paid split, the feature gating pattern, and the value argument for paid heuristics. This is conceptually a different topic from the build-system splitting in Wave 3. Consider whether Wave 3b deserves a clearer subheading or a brief transition sentence explaining that the build-time split enabled the monetization decision that follows.

### Post 05: A-

The hook is excellent -- it describes a problem every multi-agent practitioner has experienced. The progression from problem statement to scoring functions to game forms to worked example to "apply it yourself" is well-paced. The four-step closing pattern is actionable.

**Pacing and comprehension issue (revised)**: The game-form table (8 rows, 4 columns) and the solver-tier table (6 rows, 4 columns) appear back-to-back. My original review treated this as a pacing problem (reader fatigue from two dense tables in sequence). The user-advocate correctly identified the deeper issue: the game-form table is a comprehension barrier, not just a pacing problem. Terms like "Bayesian Nash equilibrium," "Core stability," "Envy-freeness," and "Incentive compatibility" are presented without definitions. A reader who builds multi-agent systems but does not have a game-theory background -- which is a large share of the target audience -- cannot parse that table at all. See Issue 9.2 below for the specific fix.

---

## 2. Accuracy: Claims vs. Reality

### Verified correct

- `resolve_package_path` dual-strategy approach (importlib.resources + fallback)
- `force-include` TOML directives
- `(payoff, best_response_payoff)` interface across all payoff functions
- 31 split tests (14 parametrized functions)
- Seven files with `Path(__file__).parent`
- `estimate_cost` duplication as coupling fix
- gamma as the only tunable parameter today
- "Two calendar days" timeline

### Issues found

**ISSUE 2.1 (P1): Post 04 implies PyPI publication is imminent**

The post says `pip install conversus` repeatedly as if it works today. The closing paragraph says "Packages are locally buildable via `scripts/build-packages.sh`; PyPI publication is a separate step that follows when the distribution channel is ready." This single qualifying sentence is insufficient given how many times `pip install conversus` appears as if it is a live command. A reader skimming the post will try `pip install conversus` and get a 404.

Beyond the factual inaccuracy, the user-advocate correctly notes this is also a narrative collapse: the entire arc of Post 04 -- "we made a monolith portable" -- culminates in an action the reader cannot take. The story has no payoff if the reader cannot try the thing the story was building toward.

**Recommendation**: Add a callout box or bold note near the top of Post 04 (after the `<!-- more -->` tag) stating the current status: packages are buildable but not yet published to PyPI. Alternatively, change the framing from "pip install conversus is a real thing" to "pip install conversus is now buildable" or similar language that does not imply PyPI availability.

**ISSUE 2.2 (P2): Post 05 AMPL claims are correctly qualified but potentially confusing**

The three-tier solver section says "The AMPL infrastructure and config optimizer exist today" and then says per-mode templates are future (specs 043-044). This is accurate per the synthesis dispute resolution. However, a reader may not understand what "AMPL infrastructure exists" means without per-mode templates. The distinction between "the plumbing is in place" and "you can use AMPL to optimize your deliberation" is subtle.

**Recommendation**: Add one clarifying sentence: "Today, the AMPL tier optimizes deliberation configuration (rounds, agents, budget). Per-mode game-form templates -- formalizing the optimization structure for each of the eight modes -- ship in a future wave." This is already partly stated but the current phrasing requires two readings to parse.

**ISSUE 2.3 (P2): Post 05 Kalman filter claim**

The post says "the solvers package includes a Kalman filter designed for this purpose, though it is not yet documented for end users." This was correctly qualified per the synthesis dispute resolution. No action needed, but flagging for awareness -- if the Kalman code is removed or refactored before publication, this sentence becomes inaccurate.

**ISSUE 2.4 (P2, downgraded from P1): "43 specs" count**

Post 04 opens with "Forty-three specs." This was corrected from "41 specs" during synthesis. Verify the current count is still 43 at publication time. Spec counts drift quickly.

*Revision note*: Both cross-reviewers correctly argued this is P2, not P1. The count is accurate today. The code-verifier confirmed 43 folders in `specs/done/`. The user-advocate notes that a reader does not care whether the number is 43 or 45 -- it establishes scale, not a precise claim. Verify at publication time, but do not treat this as a blocker.

---

## 3. Entry Point Bug (NEW -- from code-verifier cross-review)

**ISSUE 3.0 (P1): `core.toml` entry point mismatch -- ACKNOWLEDGED**

My original review missed this entirely. The code-verifier identified that `packages/core.toml` declares the CLI entry point as `engine.cli:main`, while `pyproject.toml` declares `engine.cli:cli`. No `main` function exists in `engine/cli/`. A wheel built from the committed `core.toml` would produce a non-functional CLI.

The code-verifier confirmed an uncommitted local fix exists (changing `engine.cli:main` to `engine.cli:cli`), which means the working copy is now correct. But the committed state is broken. This fix must be committed before any wheel is published.

This is the only issue across all reviews that would cause a runtime failure for end users. It belongs at the top of the P1 list. I should have caught this when I evaluated Section 4 of the synthesis document (Doc Fixes Required Before Publishing) -- I correctly identified the dependency chain ("doc fixes -> blog publication") but failed to verify the specific fixes listed in that section against the actual codebase.

---

## 4. Consistency: Cross-Post Coherence

### Between Posts 04 and 05

The two posts tell a coherent story with clear division of labor: Post 04 covers the engineering of making the framework distributable, Post 05 covers the game-theoretic scoring that justifies the paid tier. They share overlapping concepts (the `(payoff, best_response_payoff)` interface, the free/paid split, the `gamma` parameter) but explain them at different levels of detail appropriate to each post's focus.

**ISSUE 4.1 (P3): Slight framing tension on "why heuristics are paid"**

Post 04 presents four reasons why heuristics are paid (comparability, consistency, tunability, value architecture). Post 05 restates the free/paid split but frames it as "deliberation is the creative layer, scoring is the analytical layer." These are compatible framings but a reader of both posts may notice they emphasize different justifications. This is minor -- different framing for different audiences is acceptable.

### Between Posts 04-05 and Posts 01-03

**ISSUE 4.2 (P1, upgraded from P2): Tonal shift and "enterprise-grade" language**

Posts 01-03 are retrospective case studies about using conversus. They describe a specific deliberation run (the docs review), its outcomes, and what shipped. The tone is observational: "here is what happened."

Posts 04-05 shift to a hybrid of technical walkthrough and product positioning. Post 04 explains engineering decisions. Post 05 argues for a methodology. Both are more assertive than Posts 01-03.

This tonal shift matters more than I originally assessed. The user-advocate makes a compelling argument: a reader who came for technical insight and encounters marketing language will mentally reclassify the entire post from "useful engineering content" to "vendor blog." That reclassification is sticky -- it colors how they read everything that came before.

**Specifically**: "Enterprise-grade" should be cut, not merely reviewed. "No nag screens, no degraded output" -- which I correctly noted is good in the original review -- makes the same point without the sales register. The closing of Post 05 ("Build the scoring function. Measure equilibrium quality. Track convergence.") reads more like marketing copy than engineering reflection and should be revised to stay in technical register.

**Recommendation**: Cut "enterprise-grade" everywhere it appears. Review and revise closing paragraphs of both posts to ensure they stay in the technical register established by Posts 01-03.

*Revision note*: Promoted from P2 to P1. The user-advocate is right that this has more reader impact than the spec count issue I originally classified as P1. A reader who dismisses the posts as vendor marketing will not reach the CTA, rendering the other fixes moot.

### Internal consistency within the synthesis document

The synthesis document's Section 4 (Doc Fixes Required Before Publishing) identifies doc changes that must ship before the blog posts. This is well-structured and the dependency is correctly identified: if `docs/index.md` still says `git clone + uv sync` when Post 04 says `pip install conversus`, readers will hit a contradiction immediately.

---

## 5. Style: Match with Posts 01-03

### What matches well

- **Author and voice**: Same `conversus-team` author. Same first-person plural ("we").
- **Technical depth**: Posts 01-03 include YAML config blocks, tables, and specific numbers. Posts 04-05 continue this pattern with Python code blocks, TOML configs, and metrics tables.
- **Structure**: All posts use H2 sections, tables for data, and `<!-- more -->` for the fold.
- **Sentence style**: Direct, declarative sentences. Short paragraphs. No filler.

### What diverges

**ISSUE 5.1 (P3): Posts 01-03 use em dashes (--); Posts 04-05 also use em dashes but inconsistently**

Posts 01-03 consistently use ` -- ` (space-dash-dash-space) as em dashes. Posts 04-05 mostly do the same but there are a few instances of `--` without surrounding spaces (e.g., in the title "From Heuristics to pip install -- How We Made a Monolith Portable in Three Waves"). The title usage is fine (standard in titles), but check body text for consistency.

**ISSUE 5.2 (P3): Post length ratio**

| Post | Approximate word count |
|------|----------------------|
| Post 01 | ~750 |
| Post 02 | ~850 |
| Post 03 | ~800 |
| Post 04 | ~2,200 |
| Post 05 | ~2,000 |

Posts 04 and 05 are roughly 2.5x the length of Posts 01-03. This is not inherently problematic -- the topics are more complex -- but it is a noticeable jump. Keeping both posts as-is is the right call; the length increase is justified by technical depth.

---

## 6. Frontmatter Validation

### mkdocs.yml `categories_allowed`

```yaml
categories_allowed:
  - Engineering
  - Process
  - Release
```

| Post | Categories | Valid? |
|------|-----------|--------|
| Post 04 | `Engineering`, `Release` | Yes |
| Post 05 | `Engineering`, `Process` | Yes |

All categories are valid per `mkdocs.yml`.

### Dates

| Post | Date | Valid? |
|------|------|--------|
| Post 04 | `2026-04-03` | Yes (today's date) |
| Post 05 | `2026-04-03` | Yes (today's date) |
| Post 01 | `2026-04-02` | Reference (yesterday) |
| Post 02 | `2026-04-02` | Reference (yesterday) |
| Post 03 | `2026-04-02` | Reference (yesterday) |

**ISSUE 6.1 (P2): Two posts on the same date -- formalize two-track promotion**

Posts 04 and 05 share the same date (2026-04-03). MkDocs Material blog plugin will render both on the same index date. Rather than treating this as a "stagger or not" question, the recommendation is to formalize a two-track promotion strategy:

- **Post 05 first (LinkedIn)**: The game-theoretic scoring post has a stronger hook for practitioner audiences. Lead with it on LinkedIn where multi-agent practitioners will see it.
- **Post 04 second (Hacker News)**: The packaging/distribution post is a better fit for HN's engineering audience. Publish or promote it 2-3 days after Post 05.

If both remain dated 2026-04-03 on the blog itself, that is fine -- blog dates establish when the content was ready, not when it was promoted. But the promotional order should be deliberate.

**ISSUE 6.2 (P3): Sequencing ambiguity**

Posts 04 and 05 do not cross-reference each other. Post 03 ends with no forward pointer to Post 04. If these are meant to be read in sequence, Post 03 should add a closing line pointing to Post 04, and Post 04 should end with a pointer to Post 05.

If they are meant to be standalone (independent of the 01-03 series), the filenames should reflect this -- currently they would presumably be `04-*.md` and `05-*.md`, implying sequence.

### Authors

Both posts use `conversus-team`. This matches Posts 01-03. No issues.

---

## 7. Length Assessment

Post 04 at ~2,200 words and Post 05 at ~2,000 words are within the normal range for engineering blog posts (1,500-3,000 words). They are longer than Posts 01-03 but the additional length is justified by the technical depth. Neither post has obvious padding or sections that could be cut without losing information.

**Recommendation**: Keep both at current length. The density is appropriate.

---

## 8. Code Blocks

### Post 04

| Block | Language | Syntactically correct? | Notes |
|-------|----------|----------------------|-------|
| `resolve_package_path` | Python | Yes | Clean, readable. Type hints present. |
| `force-include` TOML | TOML | Yes | Standard Hatch config. |
| `try/except ImportError` | Python | Yes | Minimal and clear. |
| `packages/` directory listing | Plain text | Yes | Not a code block per se, just a tree. |

**ISSUE 8.1 (P3)**: The `resolve_package_path` function ends with `raise FileNotFoundError(...)`. The `...` is a placeholder -- fine for a blog post, but the reader may wonder what the actual error message is. Consider adding a representative message string.

### Post 05

| Block | Language | Syntactically correct? | Notes |
|-------|----------|----------------------|-------|
| `payoff = zopa_coverage * party_satisfaction` | Plain text | Yes | Pseudocode, appropriate. |
| `payoff = territory_held - gamma * overreach_penalty` | Plain text | Yes | Pseudocode, appropriate. |
| `prisoners_dilemma_payoff` | Python | Yes | Full function. Type hints. Clean. |
| Solver fallback chain | Plain text | Yes | ASCII diagram, clear. |

**ISSUE 8.2 (P2)**: The `prisoners_dilemma_payoff` function references `RoundFeatures` and `af.core_competency_count` etc. without imports or type definitions. For a blog post this is standard practice (showing the relevant function, not the full module), but adding a one-line comment like `# RoundFeatures is extracted from the deliberation output` would help readers unfamiliar with the codebase.

**ISSUE 8.3 (P3)**: Post 05 uses two different code-block styles for the same concept. The negotiation payoff formula uses plain-text pseudocode (`payoff = zopa_coverage * party_satisfaction`), while the PD payoff uses a full Python function. This inconsistency is intentional (the pseudocode is introductory, the Python is the worked example), but it may confuse readers who expect the negotiation payoff to also have a Python implementation shown.

---

## 9. Audience Accessibility (NEW -- from user-advocate cross-review)

My original review evaluated the posts as writing. The user-advocate correctly identified that I did not evaluate them as a new reader's first encounter with the framework. This section addresses that gap.

**ISSUE 9.1 (P1): Game-form table is a comprehension barrier, not just a pacing issue**

The 8-row game-form table presents equilibrium concepts (Bayesian Nash, Core stability, Envy-freeness, Incentive compatibility) without definitions. A reader who builds multi-agent AI systems but does not have a game-theory background cannot parse this table. This is not the same as the pacing problem I originally identified (two dense tables back-to-back). The pacing problem assumes the reader can parse each table individually. The comprehension problem is that many readers cannot.

**Recommendation**: Either (a) trim the table to 3-4 rows covering the most commonly used game forms, with a link to a full reference page, or (b) add a "when to use" column with plain-language descriptions that do not require game-theory prerequisites. Option (a) is preferred -- it reduces cognitive load and gives the reference page a reason to exist.

**ISSUE 9.2 (P2): Jargon density as a systemic concern**

The user-advocate catalogued eleven terms used without sufficient explanation across both posts. My original review caught one instance (Issue 8.2: `RoundFeatures` unexplained in code block) but did not identify the systemic pattern. Terms like Nash equilibrium, ZOPA, payoff function, and best-response are used as if the reader already knows them.

The posts already assume the reader builds multi-agent AI systems and knows Python packaging -- those are reasonable audience constraints. Adding a game-theory prerequisite on top narrows the audience significantly.

**Recommendation**: Add inline definitions or a brief glossary box for Nash equilibrium, ZOPA, and payoff function at first use. Three sentences would widen the funnel meaningfully without adding bloat.

---

## 10. Call to Action: pip install

### Post 04

The post drives toward `pip install conversus` as the end state of the engineering work. The arc (monolith -> portable -> monetizable) naturally culminates in "you can install this." The feature gating section reinforces the CTA with `pip install conversus` (free) and `pip install conversus-solvers` (paid).

**Effectiveness**: Strong, but undermined by Issue 2.1 (PyPI not yet live). If the reader tries `pip install conversus` and it fails, the entire narrative collapses.

### Post 05

The post ends with a four-step pattern ("Define what 'good' means quantitatively / Write a pure scoring function / Compute best-response / Track across rounds") and then a closing paragraph that says "Build the scoring function. Measure equilibrium quality. Track convergence."

The CTA is implicit rather than explicit. The post does not end with "pip install conversus" or a link to the quickstart. The three-tier solver section mentions `pip install conversus-solvers[ampl]` and `pip install conversus-solvers[nashopt]` inline, but these are buried in the middle of the post.

**ISSUE 10.1 (P1): Post 05 has no explicit CTA**

**Recommendation**: Add a brief closing section or single line after "The Bottom Line" that points readers to the install path. Something like: "conversus is open source. `pip install conversus` gets you the deliberation engine. `pip install conversus-solvers` adds the scoring layer described above. [Quickstart guide link]." This matches the pattern in Post 03, which ends by pointing readers to specific deliverables.

The user-advocate identifies this as the highest-ROI single change across both posts: one sentence converts a reader who is already convinced into someone who actually tries the product.

---

## Summary of Issues by Priority

### P1 (Must fix before publishing)

| # | Issue | Post | Description |
|---|-------|------|-------------|
| 3.0 | Entry point bug | Build | `core.toml` declares `engine.cli:main`; no such function exists. Uncommitted fix on disk -- must be committed. (From code-verifier; missed in original review.) |
| 2.1 | PyPI availability | 04 | Post implies `pip install` works today; it does not yet. Also a narrative collapse, not just factual inaccuracy. |
| 4.2 | "Enterprise-grade" language | Both | Marketing register breaks reader trust. Cut "enterprise-grade"; keep closing paragraphs in technical register. (Upgraded from P2 per user-advocate.) |
| 9.1 | Game-form table comprehension | 05 | 8-row table with undefined game-theory terms is incomprehensible to target audience without GT background. Trim to 3-4 rows or add plain-language column. (New, from user-advocate.) |
| 10.1 | Missing CTA | 05 | No explicit install/quickstart link at end. Highest-ROI single fix. |

### P2 (Should fix before publishing)

| # | Issue | Post | Description |
|---|-------|------|-------------|
| 2.2 | AMPL claim clarity | 05 | "Infrastructure exists" needs one clarifying sentence |
| 2.4 | Spec count freshness | 04 | "43 specs" is correct today; verify at publication time. (Downgraded from P1 per both cross-reviewers.) |
| 6.1 | Publication strategy | Both | Formalize two-track promotion: Post 05 first (LinkedIn), Post 04 second (HN) |
| 8.2 | Missing context comment | 05 | `RoundFeatures` type unexplained in code block |
| 9.2 | Jargon density | 05 | Nash equilibrium, ZOPA, payoff function used without inline definitions. Systemic pattern, not just one instance. (New, from user-advocate.) |

### P3 (Nice to have)

| # | Issue | Post | Description |
|---|-------|------|-------------|
| 2.3 | Kalman filter claim | 05 | Correctly qualified; verify code still exists at publication |
| 4.1 | Framing tension | Both | Different justifications for paid tier (compatible but noticeable) |
| 5.1 | Em dash consistency | Both | Minor formatting inconsistency |
| 5.2 | Length jump | Both | 2.5x longer than Posts 01-03 (acceptable, just noting) |
| 6.2 | Sequencing pointers | Both | No forward/backward references between post series |
| 8.1 | Error message placeholder | 04 | `FileNotFoundError(...)` could use a representative message |
| 8.3 | Code block style inconsistency | 05 | Pseudocode vs. Python for similar concepts |

---

## Recommendation

Fix the five P1 issues: commit the entry point fix, reframe PyPI availability, cut "enterprise-grade" language, trim or annotate the game-form table, and add an explicit CTA to Post 05. Address the P2 issues in the same editing pass. Then publish.

The two-track promotion order -- Post 05 to LinkedIn first, Post 04 to Hacker News second -- should be decided before publication so dates and cross-references can be finalized accordingly.

The synthesis document's Section 4 (Doc Fixes Required Before Publishing) must also ship before or simultaneously with the blog posts. The dependency chain is: entry point fix committed -> doc fixes shipped -> blog publication. If `docs/index.md` contradicts the blog, readers lose trust at the first click.

---

## Revision Changelog

Changes from original `review.md` based on cross-reviews:

1. **Entry point bug acknowledged (from code-verifier)**: Added Issue 3.0 as P1. This is the only issue that causes a runtime failure. I missed it despite evaluating the synthesis document's Section 4 -- a gap in my review process.
2. **"Enterprise-grade" promoted to P1 (from user-advocate)**: Issue 4.2 upgraded from P2. Marketing register has more reader impact than spec count accuracy.
3. **Jargon density added as P2 (from user-advocate)**: Issue 9.2 is new. My original review caught one instance (`RoundFeatures`); the user-advocate identified the systemic pattern.
4. **Two-track promotion formalized**: Issue 6.1 now recommends Post 05 first (LinkedIn), Post 04 second (HN), rather than just asking whether same-day publication is intentional.
5. **Game-form table trimming added as P1 (from user-advocate)**: Issue 9.1 is new. My original review treated this as a pacing problem; the user-advocate correctly identified it as a comprehension barrier for the target audience.
6. **"43 specs" downgraded to P2 (from both cross-reviewers)**: Issue 2.4 moved from P1. The count is correct today and reader decisions do not depend on exactness.
7. **Post 05 grade adjusted to A-**: Reflects the comprehension barrier in the game-form table, which is a structural issue not just a polish item.
