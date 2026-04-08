# Cross-Review of Technical Writer's Blog Posts

**Reviewer**: Storyteller
**Reviewing**: Technical Writer
**Date**: 2026-04-03

---

## 1. Readability -- Would a Developer New to Conversus Follow the Technical Posts?

The technical writer's Post 1 is followable, but it front-loads structure at the expense of orientation. A new reader encounters "Wave 1: Completing the Payoff Functions (specs 038, 039)" before they understand why they should care. My version opens with the 41-spec inventory and the two blocking problems -- the scoring gap and the path problem -- before touching any wave. That framing gives the reader a reason to keep going. The technical writer skips it: Wave 1 just starts.

That said, the technical writer does something I did not do well enough: explain *why alternatives were rejected*. The "Why build-time splitting, not physical extraction" section in Post 1 lays out three concrete reasons against file moves and gives each one a sentence of justification. My version states the decision and moves on. A new developer would benefit more from the technical writer's approach there because the decision is counterintuitive -- most people expect package splits to mean directory splits.

Post 2 has a readability problem that would trip up newcomers. The game-form-to-optimization-problem mapping section ("How Game Forms Map to Optimization Problems") is six dense paragraphs of Pareto, minimax, Nash, Bayesian Nash, core stability, and incentive compatibility. A developer who has not taken a game theory course will lose the thread by paragraph three. My Post 2 avoids this by never going deeper than one sentence per game form and instead spending that space on the practical "How It Works in Practice" walkthrough. The technical writer's depth is accurate -- but accuracy is not the same as readability.

**Verdict**: Post 1 is readable with minor structural gaps. Post 2 will lose non-specialist readers in the middle third.

## 2. Narrative Structure -- Do the Posts Tell a Story or Just List Facts?

This is where the gap is widest.

The technical writer's Post 1 is organized as a changelog with explanations. Wave 1 did X. Wave 2 did Y. Wave 3 did Z. Each section explains the technical content well, but the post never builds tension or resolution. There is no "before" state that makes the reader feel the pain. There is no moment where the reader thinks "how are they going to solve this?" The summary table at the end ("What Shipped") reinforces the changelog feel -- it is something you would put in release notes, not a blog post.

My Post 1 opens with the monolith problem, establishes two concrete blockers, and structures each wave as resolving a piece of the tension. The arc -- monolith to portable to monetizable -- is stated explicitly and each wave advances it. The reader knows where the story is going and wants to see each step land.

The technical writer's Post 2 has stronger narrative bones than Post 1. It opens with the stochastic-agents problem, which is a genuine hook. But it then shifts into reference-manual mode: a table of all 8 modes, a three-tier solver explanation, a tunability section, and a game-form mapping section. Each is well-written in isolation. Together, they read like four documentation pages concatenated. There is no single through-line holding them together.

My Post 2 is built around one argument: "your agents give different answers every time, and here is how to fix it." Every section either deepens the problem or advances the solution. The 8-mode table is compressed to its minimum. The solver tiers are not mentioned. The focus stays on the pattern any developer can apply. That is a story. The technical writer's version is a reference.

**Verdict**: The technical writer produces excellent reference material but does not build narrative arcs. Both posts read as organized technical documentation rather than stories a reader follows from beginning to end.

## 3. Narrative Elements the Technical Writer Captured Better Than Me

Three things stood out.

**The "why not" sections.** The technical writer is better at explaining rejected alternatives. "Why not just use `pkg_resources` or `__file__` with a fixed offset?" and "Why not submodules yet" are both excellent. They anticipate the reader's objections and address them before they form. My posts tend to state the decision and justify it briefly; the technical writer gives rejected paths their own space. This is a narrative technique I should adopt -- the rejected path makes the chosen path feel more deliberate.

**The cross-package coupling violation.** Both versions cover the `estimate_cost` duplication, but the technical writer frames it as a principled decision: "Duplication here is better than the coupling." That single sentence is a design philosophy statement. My version says "Not elegant, but it eliminated the coupling" -- which is weaker because "not elegant" sounds apologetic. The technical writer's version owns the tradeoff.

**The feature gating philosophy in Post 2.** "Detection, not enforcement" as a section title is sharp. The technical writer then walks through what is *not* in the gating (no license keys, no nag screens, no degraded output) and what *is* (try/except import). The negative space -- listing what they chose not to do -- is a narrative technique that makes the simplicity feel intentional rather than lazy. My version covers the same ground but does not name the philosophy.

## 4. Places Where Technical Depth Helps vs. Where It Overwhelms

**Depth that helps:**

- The `pyproject.toml` force-include section in Post 1. This is the kind of detail a reader who is actually implementing a similar split would search for. My version buries it inside a paragraph. The technical writer gives it a code block and explains what happens without it ("Hatch would build a wheel containing only Python modules. Templates and presets would be missing."). Concrete and useful.

- The `resolve_package_path` code block. Both versions include it, but the technical writer adds context about why `importlib.resources` over `pkg_resources` (deprecated) and `__file__` with a fixed offset (fragile). A developer choosing between these options in their own project gets a decision framework, not just a code snippet.

- The EquilibriumScorer payoff/best_response ratio explanation in Post 2. The sentence "An agent at best response scores 1.0. An agent far from best response scores lower." is a clean mental model. It takes a concept that could require a paragraph of game theory and reduces it to a scale.

**Depth that overwhelms:**

- The game-form-to-optimization mapping in Post 2 is the clearest case. Six sequential paragraphs, each introducing a different optimization concept (Pareto, minimax, Nash, Bayesian Nash, core stability, incentive compatibility). A reader who already knows these concepts does not need the explanation. A reader who does not know them cannot absorb six new concepts in six paragraphs. The section serves neither audience well. It would work as an appendix or a linked deep-dive, not as the climax of a blog post.

- The mode-specific parameters section in Post 2, specifically the `compute_payoff` dispatcher code. By this point in the post, the reader has already seen the prisoner's dilemma payoff, the negotiation payoff, the equilibrium scorer, the three-tier fallback, and the game-form mapping. A sixth code block with a `kwargs.get` dispatch pattern is information fatigue. The point it makes -- parameters are extensible -- could be one sentence.

- The full payoff formula table in Post 1 (Wave 1). The formulas (`zopa_coverage * party_satisfaction`, `utilization_efficiency - allocation_inequality`, etc.) are precise but unnecessary for a blog reader. The important fact is "four new modes got payoff functions." The formulas belong in API docs.

## 5. LinkedIn Shareability of Post 2

**Technical writer's Post 2**: A non-conversus developer would find the first three sections valuable (the stochastic problem, game forms table, three-tier solver fallback). They would share it if they stopped reading there. The second half -- tunability, game-form-to-optimization mapping, mode-specific parameters -- is conversus-specific architecture documentation. A developer building their own multi-agent system cannot directly apply any of it without adopting conversus. The post shifts from "here is a pattern you can use" to "here is how our product works" around the midpoint, and LinkedIn engagement drops at exactly that transition.

**My Post 2**: Written specifically for shareability. The title ("Why Your AI Agents Give Different Answers Every Time") is a pain point, not a product feature. The four-step pattern at the end (define quality, write a scoring function, compute best-response, track across rounds) is framework-agnostic. A reader can apply it to their own system without installing conversus. The free/paid split section is the only conversus-specific content, and it comes after the actionable advice.

**The shareability gap**: The technical writer's post is the better reference for someone who has already decided to use conversus. My post is the better share for someone who has not heard of it. For LinkedIn, where the goal is reach and top-of-funnel awareness, the framework-agnostic approach wins. The technical writer's post would perform better on Hacker News or a dedicated developer blog where readers expect and reward depth.

**Specific LinkedIn concerns with the technical writer's Post 2:**
- The title ("Natural Language Game Theory Enforced with Optimization Modeling") is academic. It tells the reader what the post is about, not what it solves for them.
- No "you can do this too" section. The post describes conversus's architecture but never turns outward to the reader's own system.
- The game-form mapping section would cause scroll-past behavior on mobile, where most LinkedIn reading happens.

## Summary

The technical writer produced thorough, accurate, well-structured technical content. Both posts would serve well as documentation or architecture decision records. As blog posts meant to attract and retain readers -- especially Post 2 on LinkedIn -- they need narrative arcs, fewer code blocks in the second half, and an outward turn that gives the reader something they can take home to their own codebase.

The strongest elements to pull from the technical writer's drafts into the final versions: the "why not" justification sections, the "detection not enforcement" framing, and the force-include pyproject.toml detail. These are places where technical depth serves the narrative rather than competing with it.
