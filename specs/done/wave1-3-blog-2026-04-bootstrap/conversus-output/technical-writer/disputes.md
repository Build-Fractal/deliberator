# Remaining Disputes After Revision

**Filed by**: technical-writer
**Date**: 2026-04-03
**Inputs**: Revised positions from technical-writer, storyteller, docs-updater

---

## Dispute 1: Post 2 category — `Architecture` vs `Process`

**What it is about**: Blog Post 2 needs a second category alongside `Engineering`. The storyteller's revision uses `AI` (not in `categories_allowed`). The technical-writer changed the category to `Process`. The docs-updater proposed adding `Architecture` to `mkdocs.yml`'s `categories_allowed` list.

**Technical-writer position**: Post 2's category should be `Process`. The post describes a design methodology (mode selection drives solver selection drives optimization formulation). That is a process concern. Using `Process` requires zero config changes and avoids scope creep in the category taxonomy.

**Storyteller position**: Post 2's category should be `AI`. The post is about applying game theory to AI agent output. `AI` is the audience-facing framing. (Note: `AI` is also not in `categories_allowed`, so this has the same build-breaking problem as `Architecture`.)

**Docs-updater position**: Post 2 used `Architecture` in its original draft. The docs-updater flagged this as P0 build-breaking (not in `categories_allowed`) but proposed fixing it by adding `Architecture` to `mkdocs.yml` rather than changing the post's category.

**Assessment**: Three agents, three different categories. The technical-writer revision already ships `Process` in the revised Post 2 frontmatter and the build will succeed as-is. The storyteller's `AI` and docs-updater's `Architecture` both require `mkdocs.yml` changes. The substantive question is which category best serves readers browsing the blog archive.

**Does this block publishing?**: No. The technical-writer's revised Post 2 uses `Engineering` + `Process`, both of which are in `categories_allowed`. The build will succeed. If the team prefers `Architecture` or `AI`, that requires a one-line `mkdocs.yml` edit plus a frontmatter change -- a post-merge fix, not a blocker.

---

## Dispute 2: Post 2 title and framing — technical depth vs audience breadth

**What it is about**: The three agents produced substantially different Post 2 titles and opening framings, reflecting different target audiences.

**Technical-writer position**: Title is "Natural Language Game Theory Enforced with Optimization Modeling." Opens with the output stability problem framed in terms of the scoring tier's thesis. Targets readers who already know what multi-agent deliberation is and want to understand the solver architecture. Post 2 is explicitly the technical companion to Post 1.

**Storyteller position**: Title is "Why Your AI Agents Give Different Answers Every Time (And How to Fix It)." Opens with a relatable scenario (three agents, same review, different answers). Targets a broader audience -- anyone building with AI agents who has experienced inconsistency. The game theory and optimization content is positioned as the solution to a felt problem, not as the subject of the post.

**Docs-updater position**: No revised Post 2 content (docs-updater's role is gap analysis, not content authorship). However, the docs-updater's gap analysis implicitly aligns with the storyteller's broader framing by emphasizing that the blog posts set reader expectations for the docs site -- a broader audience touchpoint.

**Assessment**: This is a genuine editorial disagreement, not a factual error. The technical-writer's version is more precise and serves the developer-docs audience. The storyteller's version is more accessible and serves top-of-funnel discovery. Both are factually sound after revisions. The choice depends on whether the blog's primary goal is documentation (technical-writer) or marketing (storyteller).

**Does this block publishing?**: No. Either version can publish. This is an editorial call for the human stakeholder, not a correctness issue.

---

## Dispute 3: How much AMPL/solver-tier detail belongs in Post 2

**What it is about**: The three agents agree that the solver tiers (heuristic, AMPL/HiGHS, nashopt/JAX) should appear in Post 2, but disagree on how much detail and what caveats are needed.

**Technical-writer position**: Post 2 includes a full section per tier with code-level detail on what each tier provides, explicit install commands (`pip install conversus-solvers[ampl]`, `pip install conversus-solvers[nashopt]`), a fallback chain diagram, and a table mapping each game form to what each tier provides. The AMPL per-mode model templates are explicitly qualified as specified in specs 043-044 but not yet implemented.

**Storyteller position**: Post 2 includes the three-tier fallback but keeps the description shorter and higher-level. No per-mode AMPL mapping table. The storyteller's revision softened the Kalman convergence claim to "the architecture supports" language and toned down tunability to note that `gamma` in PD mode is currently the only tunable parameter.

**Docs-updater position**: The docs-updater's original review flagged AMPL claims as needing toning down. The revised gap analysis does not object to the technical-writer's qualified language ("per-mode AMPL model templates are specified in specs 043 and 044 and will ship in a future wave") but does not explicitly endorse the full mapping table either.

**Assessment**: The technical-writer and storyteller converged on the key factual qualification (AMPL infrastructure exists, per-mode templates are future work). The remaining difference is volume: the technical-writer includes a 6-row table mapping game forms to solver tiers, while the storyteller omits it. The table adds precision but also length. Given that the storyteller's revision already acknowledged the three-tier architecture, the disagreement is about editorial density, not accuracy.

**Does this block publishing?**: No. Both versions correctly qualify what exists vs. what is planned. The table is additive detail, not a correctness concern.

---

## Dispute 4: Post 1 title style — descriptive vs narrative

**What it is about**: Minor but visible: the two content agents produced different Post 1 titles.

**Technical-writer position**: "From Heuristics to pip install -- How We Got Conversus Ready for Users." Emphasizes the end state (ready for users) and the technical range (heuristics to packaging).

**Storyteller position**: "From Heuristics to pip install: How We Made a Monolith Portable in Three Waves." Emphasizes the arc (monolith to portable) and the structure (three waves).

**Assessment**: Both titles are accurate. The storyteller's title foregrounds the three-wave structure that both posts use as their organizing principle. The technical-writer's title foregrounds the user-facing outcome. The storyteller's use of "monolith portable" is slightly more specific and aligns with the monolith/portable/monetizable labels both agents adopted.

**Does this block publishing?**: No. Pure editorial preference.

---

## Dispute 5: Docs-updater P0-3 resolution — add category vs change frontmatter

**What it is about**: The docs-updater identified `Architecture` not being in `categories_allowed` as a P0 build blocker. The proposed fix was to add `Architecture` to `mkdocs.yml`. The technical-writer's fix was to change the frontmatter to `Process` instead.

**Technical-writer position**: Change the post's category to `Process`. Adding new categories to `mkdocs.yml` is scope creep. The category taxonomy should be expanded deliberately, not as a side effect of publishing a blog post.

**Docs-updater position**: Add `Architecture` to `mkdocs.yml`. The post is about architecture (solver tiers, game-form mappings, fallback chains). `Architecture` is a natural category for this content and will be useful for future posts.

**Assessment**: Both fixes resolve the build blocker. The technical-writer's fix is more conservative (no config changes). The docs-updater's fix is more forward-looking (expands the taxonomy). This is a governance question: who owns the category list?

**Does this block publishing?**: No. The technical-writer's revised Post 2 already uses `Process`, so the build succeeds without any `mkdocs.yml` change. The docs-updater's proposal can be adopted later if the team wants `Architecture` as a permanent category.

---

## Summary

| # | Dispute | Agents | Blocks Publishing? |
|---|---------|--------|--------------------|
| 1 | Post 2 category (`Process` vs `Architecture` vs `AI`) | All three | No -- `Process` is already in revised frontmatter |
| 2 | Post 2 title/framing (technical depth vs broad audience) | technical-writer vs storyteller | No -- editorial choice |
| 3 | AMPL/solver detail level in Post 2 | technical-writer vs storyteller | No -- both factually correct |
| 4 | Post 1 title wording | technical-writer vs storyteller | No -- editorial choice |
| 5 | How to fix category build error (change frontmatter vs expand config) | technical-writer vs docs-updater | No -- already resolved in revision |

**Conclusion**: No remaining disputes block publishing. All factual disagreements were resolved during revision. The five disputes above are editorial preference questions (title wording, audience framing, detail density, category taxonomy governance) that require a human editorial decision, not further agent deliberation.
