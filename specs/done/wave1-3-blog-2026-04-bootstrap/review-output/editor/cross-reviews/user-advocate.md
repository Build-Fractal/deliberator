# Editor Cross-Review: User Advocate's Review

**Cross-reviewer**: Technical Editor
**Reviewing**: User Advocate (first-encounter evaluation)
**Date**: 2026-04-03

---

## Summary of User Advocate's Core Claims

1. Post 04 does not convert new users. It is an engineering retrospective that assumes prior knowledge of conversus.
2. Post 05's middle section (game-form table, three-tier solver architecture) is too dense and loses the reader who was hooked by the opening.
3. Post 05 is the correct first-contact post; Post 04 should follow, not lead.
4. The doc fixes in the synthesis are necessary but incomplete (free/paid language mismatch, README gap, cold-reader onboarding sentence).

---

## Where I Agree

### Post 04 is not an acquisition post

The user advocate is right. My review graded Post 04 at A- on narrative structure, which is accurate *for its genre* -- it is a well-constructed engineering retrospective. But I did not evaluate whether that genre serves the publication goal. The user advocate did, and the finding is clear: Post 04 does not answer "why should I care" for someone who has never heard of conversus. The opening paragraph is a feature inventory ("43 specs, 8 competition modes, 5-phase pipeline...") that rewards familiarity rather than building it.

My Issue 2.1 (PyPI availability framing) and the user advocate's "pip install promise is buried" observation reinforce each other. Post 04 has a structural problem where the deliverable the title promises -- `pip install` -- does not appear until Wave 3, which is roughly 70% into the post. Even if PyPI were live today, a reader scanning for "how do I try this" would abandon the post before finding it.

### The game-form table is a wall

My review noted this as a "minor pacing note" (two dense tables back-to-back cause reader fatigue). The user advocate is more blunt and more correct: the 8-row table with "Bayesian Nash equilibrium," "Core stability," "Envy-freeness," and "Incentive compatibility" is a reference table for existing users, not an onboarding device for new ones. Calling this a pacing issue underweights the problem. It is a comprehension barrier. A reader who does not already know what envy-freeness means in a game-theoretic context cannot evaluate the table and will either skip it (losing the thread) or abandon the post.

### The three-tier solver section is premature in a blog context

I flagged AMPL claim clarity as P2 (Issue 2.2). The user advocate makes the stronger point: the entire three-tier section is reference documentation embedded in a blog post. The reader has not yet decided to try conversus. Explaining three different install extras (`[ampl]`, `[nashopt]`) and a fallback chain is answering a question the reader has not asked. "There are heuristic scorers included, and more powerful solvers available if you need them" is sufficient for a first read.

I should have caught this in my structural review rather than treating it purely as a claim-accuracy question.

---

## Where I Partially Agree

### Post ordering (05 before 04)

The user advocate says Post 05 is the correct first-contact post and Post 04 should follow. The editorial logic is sound: Post 05 names a problem ("your AI agents give different answers"), offers a pattern, and provides actionable steps. Post 04 explains engineering decisions that matter only after the reader cares about the product.

However, the posts share a publication date (2026-04-03), and my Issue 5.2 already flagged the lack of cross-references and sequencing ambiguity. The question is not just "which comes first" but "are these part of the same series or independent?" If independent, reordering is trivial -- just promote Post 05 and let Post 04 exist for organic discovery. If they are a series (implied by the 04/05 numbering), the blog index will show them in filename order, and most blog engines render newest-first or alphabetical. The editorial plan needs to explicitly declare:

- **If same-day publication**: Post 05 should have a lower filename number or an earlier timestamp so it renders first in the blog index. A blog index showing Post 04 (the engineering retrospective) above Post 05 (the problem-statement hook) is the wrong funnel.
- **If staggered publication**: Post 05 publishes first (by at least 24 hours). Post 04 publishes second with an opening line like "In the previous post, we described the scoring pattern. This post covers how we made the framework distributable." This gives Post 04 the context bridge the user advocate correctly identifies as missing.

My preference: stagger by at least one day. Same-day dual publication dilutes both posts in social feeds.

### LinkedIn shareability at 7/10

The user advocate rates Post 05 at 7/10 for LinkedIn sharing and identifies three changes to reach 9/10: trim the game-form table, add a "try it" CTA, and condense the solver section. These align with my Issue 8.1 (missing CTA). The specific suggestions are actionable and well-calibrated.

Where I push back slightly: the user advocate says the post is "closer to 2,500 words" and LinkedIn audiences respond to 800-1,200 words. This is true for LinkedIn *native* posts (the text box). But blog post shares on LinkedIn are links with a preview card -- the word count of the destination page matters less than the hook text in the share and the first-screen experience when the reader clicks through. The first three paragraphs of Post 05 are strong enough to survive the click-through. The issue is not total length but the density cliff in the middle, which is the same problem the user advocate identified from a different angle.

---

## Where I Disagree or Add Nuance

### Post 04 does not need to convert new users -- it needs a different promotion strategy

The user advocate frames Post 04's weakness as "it doesn't convert new users" and recommends adding a 2-3 sentence opening that explains what conversus does. I think this is the wrong fix for the right diagnosis.

Post 04 is an engineering-decision post. Its natural audience is developers who find it through search ("monolith to pip install," "build-time package splitting," "importlib.resources wheel"), Hacker News, or Python packaging communities. These readers do not need a "what is conversus" preamble -- they are reading for the engineering pattern, and the product is incidental context. Adding a product-pitch opening would weaken the post for this audience.

The correct editorial response is not to rewrite Post 04 but to acknowledge it serves a different funnel stage and promote it accordingly:

| Post | Funnel stage | Promotion channel | Reader expectation |
|------|-------------|-------------------|-------------------|
| 05 | Awareness / top-of-funnel | LinkedIn, Twitter, AI newsletters | "I have this problem, show me a pattern" |
| 04 | Consideration / mid-funnel | Hacker News, Python communities, dev.to | "I am evaluating this tool, show me the engineering" |

This reframing resolves the user advocate's concern without weakening either post. Post 05 is the acquisition post. Post 04 is the credibility post. They serve different readers at different stages. The editorial plan should make this explicit rather than trying to make Post 04 do both jobs.

### The doc-gap analysis is thorough but slightly overweighted

The user advocate's Section 6 identifies three gaps not covered by the synthesis P-level fixes: free/paid language mismatch between blog and docs, README not addressed, and no "what is conversus" sentence for cold readers. These are real gaps. But the user advocate rates them all as "medium severity" and says they "should be addressed in the same wave as P2 fixes."

I would de-prioritize the free/paid language mismatch. The blog says "deliberation is free, scoring is paid." The docs table says "Engine / Free open-core" and "Solvers / Premium plugins." These are different framings of the same boundary, not contradictory claims. A reader who understands one will not be confused by the other. Harmonizing the language is a nice-to-have, not a medium-severity issue.

The README gap and the missing "what is conversus" sentence are legitimately medium-severity. The README is the first thing a GitHub visitor sees, and if it contradicts both the blog and the docs, it is a third inconsistent surface. That should be addressed alongside P1 fixes.

---

## Impact on the Editorial Plan

The user advocate's two central claims -- Post 04 does not convert, Post 05's middle is too dense -- have concrete implications for the editorial plan:

### 1. Publication sequence must change

**Current plan**: Posts 04 and 05 publish same-day (2026-04-03), with no explicit ordering.

**Revised plan**: Post 05 publishes first. Post 04 publishes 1-2 days later. Post 05 is the social-promotion post (LinkedIn, Twitter, newsletters). Post 04 is the organic-discovery post (search, HN, Python communities). The editorial calendar should reflect this by assigning different promotion strategies to each post, not just different dates.

### 2. Post 05 needs a mid-post edit, not a restructure

The user advocate's suggestions for the game-form table and solver section are correct in direction. The specific edit:

- **Game-form table**: Reduce to 4 rows (cooperative, winner-take-all, prisoner's dilemma, negotiation). Add a footnote or link: "The full 8-mode table with equilibrium concepts is in the [game forms reference]." This preserves the depth for readers who want it without blocking readers who do not.
- **Three-tier solver section**: Collapse to a single paragraph. "The heuristic payoffs ship with `conversus-solvers`. For constrained optimization (AMPL/HiGHS) or game-theoretic proofs (nashopt/JAX), optional extras are available. See the [solver documentation] for details." The current three-paragraph, two-table treatment is documentation, not blog content.
- **Worked example**: Add one sentence before the `prisoners_dilemma_payoff` code block explaining where `RoundFeatures` comes from. This was in my Issue 7.2 and the user advocate's Section 2, bullet 3. Both reviews independently identified the same gap.

These are line edits, not structural changes. Post 05's architecture (hook -> problem -> pattern -> example -> apply it yourself) is correct. The middle just needs thinning.

### 3. Post 05 needs an explicit CTA

My Issue 8.1 and the user advocate's Section 5 both identify this. The post ends with inspirational imperative ("Build the scoring function. Measure equilibrium quality. Track convergence.") but never says "here is how to start." Add after the closing paragraph:

> conversus implements this pattern. `pip install conversus` gets you the deliberation engine. `pip install conversus-solvers` adds the scoring layer described above. [Get started with the quickstart guide.]

This is a one-line addition. It converts the post from "interesting pattern" to "interesting pattern you can try right now."

### 4. Post 04 does not need a product-pitch opening -- but it needs a context sentence

The user advocate recommends a 2-3 sentence opening explaining what conversus does. I recommend a single sentence instead, placed after the feature inventory paragraph:

> conversus is an open-source framework that runs structured debates between AI agents and scores the results with game theory. The feature list above is what we needed to package.

This gives a cold reader just enough context to follow the engineering narrative without converting the post into a product pitch. It respects the engineering-audience expectation while closing the comprehension gap the user advocate identified.

### 5. Promotion strategy should be formalized

Neither my review nor the user advocate's review explicitly addressed promotion strategy, but the user advocate's analysis implies one. The editorial plan should include:

| Action | Post 05 | Post 04 |
|--------|---------|---------|
| LinkedIn share text | Problem-statement hook ("Your AI agents give different answers...") | Not promoted on LinkedIn at launch |
| Twitter/X | Thread summarizing the 4-step pattern | Thread on build-time splitting technique |
| Newsletter | Primary feature | Mentioned as "behind the build" companion |
| Hacker News | Not submitted (too product-focused for HN) | Submitted as engineering post |
| Cross-link | Links to Post 04 as "how we built this" | Links to Post 05 as "the scoring pattern this enables" |

This two-track promotion strategy addresses the user advocate's core concern (Post 04 does not convert new users) without requiring Post 04 to become something it is not.

---

## Revised Priority List (Incorporating User Advocate Findings)

Merging my original priority list with the user advocate's findings:

### P0 (Must fix before publishing)

| # | Issue | Source | Description |
|---|-------|--------|-------------|
| -- | Doc fixes P0-1, P0-2 | Synthesis | `pip install` on docs index, org/license corrections |
| 2.1 | PyPI availability framing | Editor | Post 04 implies `pip install` works today |
| NEW | Publication sequence | User Advocate + Editor | Post 05 must publish before Post 04 |

### P1 (Must fix before publishing)

| # | Issue | Source | Description |
|---|-------|--------|-------------|
| -- | Doc fixes P1-1 through P1-3 | Synthesis | Quickstart PyPI path, SDK import, entry point |
| 8.1 | Missing CTA | Editor | Post 05 needs explicit install/quickstart link |
| 2.4 | Spec count | Editor | Verify "43 specs" at publication time |
| NEW | Game-form table reduction | User Advocate | Reduce to 4 rows, link full table |
| NEW | Solver section collapse | User Advocate | Single paragraph, link to docs |
| NEW | `RoundFeatures` context line | Editor + User Advocate | One sentence explaining where features come from |

### P2 (Should fix before publishing)

| # | Issue | Source | Description |
|---|-------|--------|-------------|
| 2.2 | AMPL claim clarity | Editor | "Infrastructure exists" needs clarifying sentence |
| 3.2 | Tonal shift | Editor | "Enterprise-grade" reads as marketing |
| 5.1 | Same-date posts | Editor | Stagger dates (resolved by new sequence) |
| NEW | Post 04 context sentence | User Advocate + Editor | Single sentence after feature inventory |
| NEW | README alignment | User Advocate | README contradicts blog and docs |

### P3 (Nice to have)

All P3 items from my original review remain. The user advocate's free/paid language mismatch drops to P3 (compatible framings, not contradictory claims).

---

## Conclusion

The user advocate's review is the strongest input into the editorial plan because it tests something the other reviews do not: whether the content works for a reader who has never heard of conversus. My review evaluated quality, accuracy, and consistency within the existing frame. The user advocate evaluated whether the frame itself serves the goal.

The two central findings -- Post 04 does not convert, Post 05's middle is too dense -- are correct and actionable. The response is not to rewrite either post but to (a) sequence them correctly, (b) thin Post 05's middle section, (c) add a CTA to Post 05, and (d) formalize different promotion strategies for each post. Post 05 is the front door. Post 04 is the engineering credibility that readers find once they are already interested.

The doc fixes remain the hard dependency. Neither post should publish until P0 and P1 doc fixes are live. The user advocate and I agree on this without qualification.
