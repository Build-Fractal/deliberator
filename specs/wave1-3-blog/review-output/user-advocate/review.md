# User Advocate Review: First-Encounter Evaluation

**Reviewer**: New-user persona (no prior knowledge of conversus)
**Date**: 2026-04-03
**Inputs**: `final.md` (synthesis with Posts 04 and 05), `docs/index.md`, `docs/user-guide/quickstart.md`, `README.md`

---

## 1. Post 04 ("From Heuristics to pip install") -- Would I understand what conversus does and want to try it?

**Verdict: No. I would understand what the team *did*, but not what the product *is*.**

Post 04 is an engineering retrospective. It assumes I already know what conversus is and care about how it was packaged. The opening paragraph -- "Forty-three specs. A deliberation engine that runs 8 competition modes across a 5-phase pipeline..." -- is a feature inventory, not a value proposition. A new reader hitting this cold has no answer to the question "why would I use this?"

Specific problems for a first-encounter reader:

- **No problem statement I can relate to.** The two problems described ("the scoring gap" and "the path problem") are internal engineering problems. They tell me the team had packaging issues, not what pain conversus solves for me.
- **Dense jargon with no onramp.** "Nash equilibrium quality," "EquilibriumScorer," "ZOPA coverage," "prisoner's dilemma mode" -- these are introduced without any explanation of why a reader building AI agents should care. The post assumes familiarity with game theory as a tool for multi-agent systems.
- **The `pip install` promise is buried.** The post title says "pip install" but the actual install commands do not appear until the Wave 3 section, roughly 70% of the way through the post. A new user scanning for "how do I try this" will give up before reaching it.
- **Would I share it?** Only if I were already in the conversus community. It reads as a good internal changelog or dev blog for existing contributors. It does not convert new users.

**Recommendation**: Post 04 should not be the first post a new user encounters. It works as a "behind the build" post for people who already understand the product. If it is meant to attract new users, it needs a 2-3 sentence opening that explains what conversus does for the reader before diving into what the team did for the codebase.

---

## 2. Post 05 ("Why Your AI Agents Give Different Answers") -- Would I understand the value proposition without prior context?

**Verdict: Yes, mostly. This is the stronger entry point, but it has a cold-start problem in the middle.**

The opening is excellent. "You run three AI agents on the same code review. Agent A says the auth module needs a rewrite. Agent B says it's fine with minor patches." -- I have had exactly this experience. I am now reading. The problem framing ("without a quantitative measure of output quality, you cannot compare runs") is clear and relatable. I am nodding along through the first three sections.

Then the post loses me:

- **The game-form table is a wall.** The 8-mode table with "Bayesian Nash equilibrium," "Core stability," "Envy-freeness," and "Incentive compatibility" is a reference table for someone who already knows the framework. For a new reader, it is eight rows of terms I have never seen in the context of AI agents. I do not know why I would choose "coalitional (Shapley)" over "cooperative." The table needs either a one-sentence "when to use this" column or a preamble explaining that most users start with cooperative or winner-take-all and the rest are there when they need them.
- **The three-tier solver section is premature.** I have not yet decided to try conversus. The post is now explaining three different install extras (`[ampl]`, `[nashopt]`) and a fallback chain. This is reference documentation embedded in a blog post. For a first read, "there are heuristic scorers included, and more powerful solvers available if you need them" is sufficient.
- **The worked example code is good but unexplained in context.** The `prisoners_dilemma_payoff` function is clear Python. But the reader has no way to know: where does `features` come from? Who calls this function? Is this something I write, or something the framework provides? A single sentence ("Conversus extracts these features automatically from agent output during the cross-review phase") would close the gap.
- **"Apply This to Your Own System" section is strong.** The four steps are actionable and framework-agnostic. This is the section that would make me bookmark the post.

**Would I share it on LinkedIn?** Conditionally yes. The title is strong clickbait in the best sense -- it names a real pain point. The opening hooks. I would share it if the middle section did not make me feel like I need a game theory textbook to understand the product. The current version is shareable to a technical audience (ML engineers, platform teams building agent systems). It is not shareable to the broader "AI-curious engineering leader" audience that the title promises.

---

## 3. After reading the posts, does docs/index.md match what the posts promised?

**Verdict: No. The gap is jarring.**

Post 05 repeatedly says `pip install conversus`. The docs index says:

```bash
git clone https://github.com/clariti-care/conversus.git && cd conversus
uv sync
```

This is a trust-breaking mismatch. A reader who arrives at the docs after reading the blog will immediately wonder: "Did I misread the blog? Is pip install not actually supported? Is this a different project?"

Additional mismatches:

- **The org is wrong.** The docs reference `clariti-care`. The synthesis notes this should be `Build-Fractal`. A reader clicking through gets a 404 or the wrong repo.
- **The license badge says "proprietary."** Post 04 implies an open-core model with a free tier. "Proprietary" on the landing page contradicts that framing.
- **No mention of the free/paid split.** Both posts make the "deliberation is free, scoring is paid" line a centerpiece. The docs index has a "Three Layers" table that sort of maps to this, but uses "Free / open-core," "Premium plugins," and "Platform" labels that do not match the blog's language. "Free / open-core" is not the same message as "deliberation is free, scoring is paid."
- **The quickstart assumes `uv sync` as the only install method.** A pip-install user following the quickstart will be confused by `uv run conversus decide ...` -- they would just run `conversus decide ...`.

The synthesis document's P0 and P1 doc fixes (Section 4) correctly identify these gaps. If those fixes ship, the experience is substantially better. But they must ship before the blog posts go live -- otherwise every reader who clicks through from the blog hits a contradiction on the first page.

---

## 4. Jargon and assumptions that would lose a new reader

**Terms used without sufficient explanation:**

| Term | Where | Problem |
|------|-------|---------|
| Nash equilibrium | Both posts | Introduced as if readers know what it means in a multi-agent AI context. A one-sentence gloss ("no agent can improve its score by changing strategy alone") appears in Post 05 but only after several earlier uses without explanation. |
| ZOPA (zone of possible agreement) | Post 05 | Acronym from negotiation theory. Parenthetical expansion is present but the concept itself is not explained. |
| Payoff function / payoff matrix | Both posts | Game theory terminology used as if self-evident. Many ML engineers will not have this vocabulary. |
| Pareto optimality / envy-freeness / incentive compatibility | Post 05 table | Six different equilibrium concepts in a table with no definitions. A reader who does not already know these cannot evaluate the table. |
| Hatch / force-include / wheel | Post 04 | Python packaging jargon. Reasonable for a Python-developer audience, but excludes polyglot readers. |
| importlib.resources | Post 04 | Deep Python standard library knowledge. Not a term a typical "should I try this tool" reader knows. |
| MCP server | Both posts, README, docs | Never defined. "MCP-compatible editor" is used without explaining what MCP is. |
| Stagnation detection / multi-round convergence | Post 04 opening | Feature names that mean nothing without context. |

**Assumptions that narrow the audience:**

- The reader is building multi-agent AI systems (reasonable for Post 05, but limiting for Post 04).
- The reader knows Python packaging (Post 04 is incomprehensible without this).
- The reader has encountered agent inconsistency as a problem (Post 05 -- this is the best assumption of the three; it is widely relatable).
- The reader knows what game theory offers to AI agent evaluation (both posts).

---

## 5. Would I share Post 05 on LinkedIn?

**Rating: 7/10 -- likely share with caveats.**

**Strengths for sharing:**

- The title is a genuine hook. "Why Your AI Agents Give Different Answers Every Time" is a problem statement, not a product announcement. It earns the click.
- The opening three paragraphs are concrete and relatable. No jargon, no product pitch -- just a description of a real pain point.
- The four-step "apply this to your own system" closing is framework-agnostic and useful even if the reader never installs conversus. This is the kind of content that gets shared because it is *helpful*, not because it is promotional.
- The "generate with LLMs, score with math" one-liner at the end is memorable and quotable.

**Weaknesses for sharing:**

- The middle section (game-form table, three-tier solver architecture) reads like documentation, not a blog post. The energy drops. A LinkedIn reader scanning on mobile will lose interest here.
- The post is long. LinkedIn audiences respond to 800-1200 word posts. This is closer to 2500 words. The value is there, but it needs tighter editing or a clear "you can stop here" break after the first worked example.
- The implicit pitch is subtle enough to work, but the post never gives the reader a single command to try. Post 05 ends with "build the scoring function" as generic advice. A closing like "conversus implements this pattern -- `pip install conversus` to try it" would convert interest into action without feeling salesy.

**What would make it a 9/10 share:**

1. Cut the game-form table to 3-4 rows (cooperative, winner-take-all, prisoner's dilemma, negotiation) and move the full table to a "deep dive" link.
2. Add a "try it" CTA after the four-step pattern.
3. Trim the three-tier solver section to a single paragraph with a link to full docs.

---

## 6. Do the doc fixes close the expectation gap between blog and docs?

**Verdict: The P0 and P1 fixes close the critical gaps. P2 fixes are necessary for a polished experience. The blog posts themselves still need minor edits.**

**What the doc fixes get right:**

- P0-1 (restore `pip install` as primary path) is the single most important fix. Without it, the blog-to-docs journey is broken on arrival.
- P0-2 (org and license corrections) prevents 404s and trust contradictions.
- P1-1 (quickstart adds PyPI path) means the second page a reader visits also works.
- P1-2 (SDK import path warning) prevents the confusing `from engine import Deliberation` surprise when the package is called `conversus`.
- P1-3 (entry point investigation) is correctly flagged as a code issue, not a docs issue. If `pip install conversus` gives a different CLI entry point than `uv sync`, users will file bugs.

**What the doc fixes miss:**

- **The docs index "Three Layers" table does not use the blog's language.** The blog says "deliberation is free, scoring is paid." The docs table says "Engine / Free open-core" and "Solvers / Premium plugins." These are not the same framing. A reader arriving from the blog expects to see the phrase they just read. This is not in any P-level fix.
- **The README is not addressed at all.** The README uses `git clone <repo-url>` (not even a real URL) and `from engine import Deliberation`. A reader who lands on the GitHub repo page instead of the docs site gets a completely different experience. The README should either match the docs index or redirect to it.
- **No fix addresses the "what is conversus" gap.** The docs index opens with "Competitive multi-agent deliberation framework" -- this is a category label, not a value proposition. The blog posts invest hundreds of words building up to why this matters. The docs index assumes you already know. A single sentence after the tagline ("Ask a question, get a structured debate between AI agents with different perspectives, walk away with a battle-tested decision") would bridge this.

**Summary of gaps after all proposed fixes ship:**

| Gap | Severity | Status |
|-----|----------|--------|
| No `pip install` on docs index | Critical | Fixed by P0-1 |
| Wrong org URL / license | Critical | Fixed by P0-2 |
| No `pip install` in quickstart | High | Fixed by P1-1 |
| SDK import path confusion | High | Fixed by P1-2 |
| Entry point inconsistency | High | Flagged as P1-3, needs code verification |
| Free/paid language mismatch between blog and docs | Medium | Not addressed |
| README contradicts both blog and docs | Medium | Not addressed |
| No "what is this" sentence for cold readers | Medium | Not addressed |
| Game-form table in Post 05 is inaccessible to new readers | Low | Blog content, not a docs fix |

---

## Overall Assessment

**Post 05 is the right first-contact post.** It names a real problem, explains the pattern, and gives actionable advice. With the edits suggested in Section 5, it is strong LinkedIn material.

**Post 04 is a good second post** for readers who are already interested and want to understand the engineering. It should not be the entry point for new users.

**The doc fixes in the synthesis are necessary and well-prioritized.** The P0 and P1 fixes must ship before the blog posts go live. Without them, every click-through from blog to docs damages credibility.

**The remaining gaps (free/paid language consistency, README, cold-reader onboarding sentence) are medium-severity and should be addressed in the same wave as P2 fixes.** They do not block publishing but they weaken the reader journey at the margins.

**The biggest risk is not the content -- it is the sequencing.** If the blog posts publish before the doc fixes land, readers will encounter contradictions within minutes. The synthesis correctly identifies this. The recommendation to ship P0+P1 as a single coordinated commit before blog publication is the right call.
