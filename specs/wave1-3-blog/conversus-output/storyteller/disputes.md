# Remaining Disputes -- Storyteller Assessment

**Agent**: storyteller
**Date**: 2026-04-03
**Scope**: All disputes identified after reading revised positions from technical-writer, storyteller, and docs-updater.

---

## Dispute 1: Post 2 Category -- `Architecture` vs `Process`

**What it is about**: Blog Post 2's frontmatter category. The storyteller revision uses `AI` as a category. The technical-writer changed `Architecture` to `Process`. The docs-updater flagged `Architecture` as not in `mkdocs.yml`'s `categories_allowed` list (only `Engineering`, `Process`, `Release` are permitted).

**Storyteller position**: Post 2's revised frontmatter uses `categories: Engineering, AI`. The `AI` category is also not in `categories_allowed`. The post's subject -- game-theoretic scoring applied to multi-agent systems -- is more about the engineering approach than about internal process. If we must pick from the allowed list, `Engineering` alone covers it. Adding a second category should only happen if the category actually exists in the build config.

**Technical-writer position**: Changed to `Engineering` + `Process`, arguing the post's focus on design methodology and solver selection workflow fits `Process`.

**Docs-updater position**: Flagged the `Architecture` category as build-breaking (P0-3) and proposed adding `Architecture` to `categories_allowed` in `mkdocs.yml`.

**Resolution needed**: Three options are on the table: (a) use only `Engineering` (safe, no mkdocs change), (b) use `Engineering` + `Process` (technical-writer's pick, also safe), (c) add `Architecture` or `AI` to `categories_allowed` and use it. The storyteller's `AI` category and the original `Architecture` category both break the build unless mkdocs.yml is updated. The technical-writer's `Process` is defensible but loose -- the post is not about team process, it is about system design. The cleanest fix is `Engineering` alone; adding `Process` is acceptable but not necessary.

**Blocks publishing**: Yes -- if the category is not in `categories_allowed`, the MkDocs blog plugin will reject the post at build time.

---

## Dispute 2: Post 2 Title and Framing -- Technical vs Accessible

**What it is about**: The title, tone, and target audience of Blog Post 2.

**Storyteller position**: Title is "Why Your AI Agents Give Different Answers Every Time (And How to Fix It)". The framing is accessible, problem-first, addressed to any engineer building with multi-agent systems. Game theory terminology is introduced gently through worked examples. The post opens with a relatable scenario (three agents, same input, different answers) and builds to the optimization model as the solution. The closing four-step pattern is meant to be actionable for readers outside the conversus ecosystem.

**Technical-writer position**: Title is "Natural Language Game Theory Enforced with Optimization Modeling". The framing is precise, domain-specific, and aimed at readers who already know what game theory is. The table mapping all 8 modes to game forms, equilibrium concepts, and solver formulations is front-loaded. Code examples include the full `prisoners_dilemma_payoff` function with parameter documentation. The closing "apply this to your own system" section was added in revision to match the storyteller's actionable pattern.

**Docs-updater position**: No explicit position on title/framing. The gap analysis is neutral on tone, focused on factual accuracy.

**Assessment**: These are genuinely different posts for different audiences. The storyteller version trades precision for reach. The technical-writer version trades reach for precision. Both are factually accurate after revision. The storyteller version's title is better for discoverability (people search for "AI agents inconsistent results", not "natural language game theory"). The technical-writer version's depth is better for developer credibility. The final published version should pick one framing or the other -- hybridizing will produce a post that satisfies neither audience.

**Blocks publishing**: No. Either version is publishable. But the choice determines who reads the post.

---

## Dispute 3: AMPL Tier -- Current Capability vs Forward-Looking

**What it is about**: How to describe what the AMPL/HiGHS solver tier can do today versus what is planned.

**Storyteller position**: The revision describes Tier 2 as existing infrastructure that handles "modes that map to formal optimization problems" today, with a note that mode-specific AMPL model templates are planned. The language ("AMPL formulations with the HiGHS solver can compute provably optimal allocations") implies current capability for at least some modes, particularly resource allocation and fair division.

**Technical-writer position**: The revision explicitly qualifies that "the AMPL infrastructure and config optimizer exist today" but "per-mode AMPL model templates -- formalizing each game form's specific optimization structure -- are specified in specs 043 and 044 and will ship in a future wave." The current AMPL tier handles configuration optimization (how many agents, how many rounds given a budget), not mode-aware game-theoretic optimization.

**Docs-updater position**: Flagged this in the original review. Cross-review accepted the technical-writer's qualification as sufficient.

**Assessment**: The technical-writer's version is more accurate. The AMPL infrastructure (amplpy + HiGHS binding) exists, and the config optimizer uses it. But the per-mode AMPL model templates that would formalize cooperative games as Pareto optimization or fair-division as envy-free allocation do not exist yet. The storyteller's Tier 2 description ("AMPL formulations with the HiGHS solver can compute provably optimal allocations") overstates current capability. The published version should use the technical-writer's future-oriented phrasing for per-mode AMPL formulations and present-tense only for config optimization.

**Blocks publishing**: No, but publishing the storyteller's version without the technical-writer's qualification risks a credibility gap if a reader installs `conversus-solvers[ampl]` and finds that per-mode optimization is not yet available.

---

## Dispute 4: Kalman Convergence Prediction -- Documented Feature vs Architectural Capability

**What it is about**: Whether to present the Kalman convergence predictor as a user-facing feature or an internal architectural capability.

**Storyteller position**: The revision uses "the architecture supports" language and notes the solvers package "includes a Kalman filter designed for this purpose, though it is not yet documented for end users." This is a softened claim that acknowledges the code exists but the user-facing documentation does not.

**Technical-writer position**: Post 2 describes it as a concrete downstream consumer of PluginResult data: "The Kalman convergence predictor -- adapt their confidence bounds based on solver fidelity." Post 1 does not mention it. The technical-writer treats it as an implementation detail that exists and works, without qualifying its documentation status.

**Docs-updater position**: Original review flagged this as specced but not in user docs. Accepted the storyteller's softened language in cross-review.

**Assessment**: The storyteller's "architecture supports" framing with the documentation caveat is the safer position. If the Kalman filter works but has no user-facing docs, calling it a feature in a blog post creates a support burden -- readers will ask how to use it and find no documentation. The technical-writer's passing mention in a technical context (PluginResult consumers) is fine because it does not promise user-facing functionality. Both approaches are acceptable, but the storyteller's explicit caveat is more honest.

**Blocks publishing**: No. This is a tone/expectation-setting issue, not a factual error.

---

## Dispute 5: Post 1 Title -- Descriptive vs Narrative

**What it is about**: The title of Blog Post 1.

**Storyteller position**: "From Heuristics to pip install: How We Made a Monolith Portable in Three Waves" -- uses a colon, includes the arc language, focuses on the transformation narrative.

**Technical-writer position**: "From Heuristics to pip install -- How We Got Conversus Ready for Users" -- uses a dash, names the product, focuses on user readiness.

**Assessment**: Minor. The storyteller title is more descriptive of the post's structure (three waves). The technical-writer title is more product-focused (names conversus, centers the user). Both are accurate. The storyteller's "Monolith Portable" phrasing echoes the post's arc labels, which both versions now use. The technical-writer's "Ready for Users" is a stronger value statement. Neither is wrong.

**Blocks publishing**: No.

---

## Dispute 6: `gamma` as the Only Tunable Parameter vs Broader Tunability

**What it is about**: Whether to present `gamma` as a representative example of a tunable parameter surface or as the only current knob.

**Storyteller position**: Explicitly states "Today, `gamma` in PD mode is the one tunable parameter; the other seven modes use fixed formulas. The parameter surface will expand as the framework matures." This is the most conservative and accurate framing.

**Technical-writer position**: The tunability section in Post 2 discusses `gamma` as an example, then says "Future specs (043, 044) will expand the parameter surface." This is accurate but the section's length and depth (gamma at 0.0, at 2.0, domain examples) might imply broader current tunability than exists.

**Docs-updater position**: Flagged this in original review. Accepted both revisions as sufficient.

**Assessment**: The storyteller's one-sentence caveat ("Today, `gamma` in PD mode is the one tunable parameter") is the clearest formulation. The technical-writer's version is not inaccurate but could leave a reader thinking there are more knobs to turn today. The storyteller's phrasing should be adopted in whichever version publishes.

**Blocks publishing**: No.

---

## Summary

| # | Dispute | Blocks Publishing | Recommendation |
|---|---------|-------------------|----------------|
| 1 | Post 2 category (`AI` / `Process` / `Architecture`) | **Yes** | Use `Engineering` alone or `Engineering` + `Process`. Do not use `AI` or `Architecture` without updating mkdocs.yml. |
| 2 | Post 2 title and framing (accessible vs technical) | No | Pick one audience. The storyteller version has better discoverability; the technical-writer version has more depth. |
| 3 | AMPL tier current vs planned capability | No | Adopt the technical-writer's qualification. Config optimization exists; per-mode AMPL templates do not. |
| 4 | Kalman convergence -- feature vs architecture | No | Adopt the storyteller's "architecture supports" caveat. |
| 5 | Post 1 title phrasing | No | Minor preference. Either works. |
| 6 | `gamma` as only parameter vs broader tunability | No | Adopt the storyteller's explicit "one tunable parameter" caveat. |

**One dispute blocks publishing** (category). The remaining five are editorial choices that affect tone, audience, and precision but do not prevent the posts from going live. All factual disagreements from the first round have been resolved in revision.
