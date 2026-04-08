# Technical Editor Review: Posts 04 and 05

**Reviewer**: Technical Editor
**Date**: 2026-04-03
**Source**: `specs/wave1-3-blog/conversus-output/summary/final.md` (Section 3)
**Comparisons**: Posts 01-03 in `docs/blog/posts/`

---

## Verdict: Publish with revisions

Both posts are strong. They are the best-written entries in the series so far. The narrative arcs are clear, the technical depth is appropriate, and the synthesis process resolved real disputes well. The issues below are fixable in a single editing pass.

---

## 1. Quality: Narrative Structure

### Post 04: A-

Strong three-act structure (monolith / portable / monetizable). The problem-first opening ("The Two Problems Blocking Users") is effective -- it immediately tells the reader why the work matters. The wave-by-wave progression provides natural pacing. The summary table at the end ties the arc together cleanly.

**One structural issue**: The "Wave 3b: Drawing the Line" section is half the post's length. It introduces the free/paid split, the feature gating pattern, and the value argument for paid heuristics. This is conceptually a different topic from the build-system splitting in Wave 3. It feels like two posts compressed into one. Consider whether Wave 3b deserves a clearer subheading or a brief transition sentence explaining that the build-time split enabled the monetization decision that follows.

### Post 05: A

The hook is excellent -- it describes a problem every multi-agent practitioner has experienced. The progression from problem statement to scoring functions to game forms to worked example to "apply it yourself" is well-paced. The four-step closing pattern is actionable.

**Minor pacing note**: The game-form table (8 rows, 4 columns) and the solver-tier table (6 rows, 4 columns) appear back-to-back. Two dense tables in sequence can cause reader fatigue. Consider adding one sentence of connective tissue between them explaining what the second table adds beyond the first.

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

**Recommendation**: Add a callout box or bold note near the top of Post 04 (after the `<!-- more -->` tag) stating the current status: packages are buildable but not yet published to PyPI. Alternatively, change the framing from "pip install conversus is a real thing" to "pip install conversus is now buildable" or similar language that does not imply PyPI availability.

**ISSUE 2.2 (P2): Post 05 AMPL claims are correctly qualified but potentially confusing**

The three-tier solver section says "The AMPL infrastructure and config optimizer exist today" and then says per-mode templates are future (specs 043-044). This is accurate per the synthesis dispute resolution. However, a reader may not understand what "AMPL infrastructure exists" means without per-mode templates. The distinction between "the plumbing is in place" and "you can use AMPL to optimize your deliberation" is subtle.

**Recommendation**: Add one clarifying sentence: "Today, the AMPL tier optimizes deliberation configuration (rounds, agents, budget). Per-mode game-form templates -- formalizing the optimization structure for each of the eight modes -- ship in a future wave." This is already partly stated but the current phrasing requires two readings to parse.

**ISSUE 2.3 (P2): Post 05 Kalman filter claim**

The post says "the solvers package includes a Kalman filter designed for this purpose, though it is not yet documented for end users." This was correctly qualified per the synthesis dispute resolution. No action needed, but flagging for awareness -- if the Kalman code is removed or refactored before publication, this sentence becomes inaccurate.

**ISSUE 2.4 (P1): "43 specs" count**

Post 04 opens with "Forty-three specs." This was corrected from "41 specs" during synthesis. Verify the current count is still 43 at publication time. Spec counts drift quickly.

---

## 3. Consistency: Cross-Post Coherence

### Between Posts 04 and 05

The two posts tell a coherent story with clear division of labor: Post 04 covers the engineering of making the framework distributable, Post 05 covers the game-theoretic scoring that justifies the paid tier. They share overlapping concepts (the `(payoff, best_response_payoff)` interface, the free/paid split, the `gamma` parameter) but explain them at different levels of detail appropriate to each post's focus.

**ISSUE 3.1 (P3): Slight framing tension on "why heuristics are paid"**

Post 04 presents four reasons why heuristics are paid (comparability, consistency, tunability, value architecture). Post 05 restates the free/paid split but frames it as "deliberation is the creative layer, scoring is the analytical layer." These are compatible framings but a reader of both posts may notice they emphasize different justifications. This is minor -- different framing for different audiences is acceptable.

### Between Posts 04-05 and Posts 01-03

**ISSUE 3.2 (P2): Tonal shift from Posts 01-03 to Posts 04-05**

Posts 01-03 are retrospective case studies about using conversus. They describe a specific deliberation run (the docs review), its outcomes, and what shipped. The tone is observational: "here is what happened."

Posts 04-05 shift to a hybrid of technical walkthrough and product positioning. Post 04 explains engineering decisions. Post 05 argues for a methodology. Both are more assertive than Posts 01-03.

This is not a problem per se -- blog series naturally evolve. But the shift is noticeable. Posts 01-03 never mention pricing, tiers, or "enterprise-grade." Post 04 introduces monetization. Post 05 ends with "Build the scoring function. Measure equilibrium quality. Track convergence." which reads more like marketing copy than engineering reflection.

**Recommendation**: No structural changes needed. But review the closing paragraphs of both posts to ensure the tone stays technical rather than drifting into sales language. The "no nag screens, no degraded output" language is good -- it is a technical design decision. "Enterprise-grade" in Post 05 could be cut or replaced with a more specific technical claim.

### Internal consistency within the synthesis document

The synthesis document's Section 4 (Doc Fixes Required Before Publishing) identifies doc changes that must ship before the blog posts. This is well-structured and the dependency is correctly identified: if `docs/index.md` still says `git clone + uv sync` when Post 04 says `pip install conversus`, readers will hit a contradiction immediately.

---

## 4. Style: Match with Posts 01-03

### What matches well

- **Author and voice**: Same `conversus-team` author. Same first-person plural ("we").
- **Technical depth**: Posts 01-03 include YAML config blocks, tables, and specific numbers. Posts 04-05 continue this pattern with Python code blocks, TOML configs, and metrics tables.
- **Structure**: All posts use H2 sections, tables for data, and `<!-- more -->` for the fold.
- **Sentence style**: Direct, declarative sentences. Short paragraphs. No filler.

### What diverges

**ISSUE 4.1 (P3): Posts 01-03 use em dashes (--); Posts 04-05 also use em dashes but inconsistently**

Posts 01-03 consistently use ` -- ` (space-dash-dash-space) as em dashes. Posts 04-05 mostly do the same but there are a few instances of `--` without surrounding spaces (e.g., in the title "From Heuristics to pip install -- How We Made a Monolith Portable in Three Waves"). The title usage is fine (standard in titles), but check body text for consistency.

**ISSUE 4.2 (P3): Post length ratio**

| Post | Approximate word count |
|------|----------------------|
| Post 01 | ~750 |
| Post 02 | ~850 |
| Post 03 | ~800 |
| Post 04 | ~2,200 |
| Post 05 | ~2,000 |

Posts 04 and 05 are roughly 2.5x the length of Posts 01-03. This is not inherently problematic -- the topics are more complex -- but it is a noticeable jump. If the blog is meant to maintain consistent post length, consider whether Post 04 could be split (Wave 1-2 as one post, Wave 3 + monetization as another). However, this would break the arc structure, so the recommendation is to keep both posts as-is and accept the length increase.

---

## 5. Frontmatter Validation

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

**ISSUE 5.1 (P2): Two posts on the same date**

Posts 04 and 05 share the same date (2026-04-03). MkDocs Material blog plugin will render both on the same day. This is technically fine but means the blog index will show two posts for today. If publication is intended to be staggered, adjust one date. If same-day publication is intentional (e.g., a "wave 1-3 blog drop"), this is acceptable.

**ISSUE 5.2 (P3): Sequencing ambiguity**

Posts 04 and 05 do not cross-reference each other. Post 03 ends with no forward pointer to Post 04. If these are meant to be read in sequence, Post 03 should add a closing line pointing to Post 04, and Post 04 should end with a pointer to Post 05.

If they are meant to be standalone (independent of the 01-03 series), the filenames should reflect this -- currently they would presumably be `04-*.md` and `05-*.md`, implying sequence.

### Authors

Both posts use `conversus-team`. This matches Posts 01-03. No issues.

---

## 6. Length Assessment

Post 04 at ~2,200 words and Post 05 at ~2,000 words are within the normal range for engineering blog posts (1,500-3,000 words). They are longer than Posts 01-03 but the additional length is justified by the technical depth. Neither post has obvious padding or sections that could be cut without losing information.

**Recommendation**: Keep both at current length. The density is appropriate.

---

## 7. Code Blocks

### Post 04

| Block | Language | Syntactically correct? | Notes |
|-------|----------|----------------------|-------|
| `resolve_package_path` | Python | Yes | Clean, readable. Type hints present. |
| `force-include` TOML | TOML | Yes | Standard Hatch config. |
| `try/except ImportError` | Python | Yes | Minimal and clear. |
| `packages/` directory listing | Plain text | Yes | Not a code block per se, just a tree. |

**ISSUE 7.1 (P3)**: The `resolve_package_path` function ends with `raise FileNotFoundError(...)`. The `...` is a placeholder -- fine for a blog post, but the reader may wonder what the actual error message is. Consider adding a representative message string.

### Post 05

| Block | Language | Syntactically correct? | Notes |
|-------|----------|----------------------|-------|
| `payoff = zopa_coverage * party_satisfaction` | Plain text | Yes | Pseudocode, appropriate. |
| `payoff = territory_held - gamma * overreach_penalty` | Plain text | Yes | Pseudocode, appropriate. |
| `prisoners_dilemma_payoff` | Python | Yes | Full function. Type hints. Clean. |
| Solver fallback chain | Plain text | Yes | ASCII diagram, clear. |

**ISSUE 7.2 (P2)**: The `prisoners_dilemma_payoff` function references `RoundFeatures` and `af.core_competency_count` etc. without imports or type definitions. For a blog post this is standard practice (showing the relevant function, not the full module), but adding a one-line comment like `# RoundFeatures is extracted from the deliberation output` would help readers unfamiliar with the codebase.

**ISSUE 7.3 (P3)**: Post 05 uses two different code-block styles for the same concept. The negotiation payoff formula uses plain-text pseudocode (`payoff = zopa_coverage * party_satisfaction`), while the PD payoff uses a full Python function. This inconsistency is intentional (the pseudocode is introductory, the Python is the worked example), but it may confuse readers who expect the negotiation payoff to also have a Python implementation shown.

---

## 8. Call to Action: pip install

### Post 04

The post drives toward `pip install conversus` as the end state of the engineering work. The arc (monolith -> portable -> monetizable) naturally culminates in "you can install this." The feature gating section reinforces the CTA with `pip install conversus` (free) and `pip install conversus-solvers` (paid).

**Effectiveness**: Strong, but undermined by Issue 2.1 (PyPI not yet live). If the reader tries `pip install conversus` and it fails, the entire narrative collapses.

### Post 05

The post ends with a four-step pattern ("Define what 'good' means quantitatively / Write a pure scoring function / Compute best-response / Track across rounds") and then a closing paragraph that says "Build the scoring function. Measure equilibrium quality. Track convergence."

The CTA is implicit rather than explicit. The post does not end with "pip install conversus" or a link to the quickstart. The three-tier solver section mentions `pip install conversus-solvers[ampl]` and `pip install conversus-solvers[nashopt]` inline, but these are buried in the middle of the post.

**ISSUE 8.1 (P1): Post 05 has no explicit CTA**

**Recommendation**: Add a brief closing section or single line after "The Bottom Line" that points readers to the install path. Something like: "conversus is open source. `pip install conversus` gets you the deliberation engine. `pip install conversus-solvers` adds the scoring layer described above. [Quickstart guide link]." This matches the pattern in Post 03, which ends by pointing readers to specific deliverables.

---

## Summary of Issues by Priority

### P1 (Must fix before publishing)

| # | Issue | Post | Description |
|---|-------|------|-------------|
| 2.1 | PyPI availability | 04 | Post implies `pip install` works today; it does not yet |
| 2.4 | Spec count | 04 | "43 specs" may be stale by publication |
| 8.1 | Missing CTA | 05 | No explicit install/quickstart link at end |

### P2 (Should fix before publishing)

| # | Issue | Post | Description |
|---|-------|------|-------------|
| 2.2 | AMPL claim clarity | 05 | "Infrastructure exists" needs one clarifying sentence |
| 3.2 | Tonal shift | Both | "Enterprise-grade" reads as marketing; cut or replace |
| 5.1 | Same-date posts | Both | Intentional? If not, stagger dates |
| 7.2 | Missing context comment | 05 | `RoundFeatures` type unexplained in code block |

### P3 (Nice to have)

| # | Issue | Post | Description |
|---|-------|------|-------------|
| 3.1 | Framing tension | Both | Different justifications for paid tier (compatible but noticeable) |
| 4.1 | Em dash consistency | Both | Minor formatting inconsistency |
| 4.2 | Length jump | Both | 2.5x longer than Posts 01-03 (acceptable, just noting) |
| 5.2 | Sequencing pointers | Both | No forward/backward references between post series |
| 7.1 | Error message placeholder | 04 | `FileNotFoundError(...)` could use a representative message |
| 7.3 | Code block style inconsistency | 05 | Pseudocode vs. Python for similar concepts |

---

## Recommendation

Fix the three P1 issues (PyPI availability framing, spec count verification, Post 05 CTA), address the P2 issues in the same pass, and publish. The posts are ready -- the issues are refinements, not structural problems.

The synthesis document's Section 4 (Doc Fixes Required Before Publishing) must also ship before or simultaneously with the blog posts. The dependency chain is: doc fixes -> blog publication. If `docs/index.md` contradicts the blog, readers lose trust at the first click.
