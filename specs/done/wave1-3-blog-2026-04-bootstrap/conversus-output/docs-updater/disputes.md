# Remaining Disputes After Revision

**Author**: docs-updater (documentation engineer)
**Date**: 2026-04-03
**Input**: All three revised positions (technical-writer, storyteller, docs-updater)

---

## Dispute 1: Storyteller Post 2 uses `AI` category -- build will break

**What the dispute is about**: The storyteller's revised Post 2 frontmatter declares `categories: [Engineering, AI]`. The `mkdocs.yml` `categories_allowed` list permits only `Engineering`, `Process`, and `Release`. The technical-writer caught this class of problem for the `Architecture` category and fixed their own Post 2 to use `Process`. The storyteller's revision introduces the same problem with a different invalid category.

**My position**: `AI` must be changed to a permitted category or added to `mkdocs.yml`. Since the technical-writer already chose `Process` for Post 2 (which fits -- the post is about a scoring methodology, not a release), the storyteller should align. Alternatively, add `AI` to `categories_allowed`, but that requires a deliberate product decision about the blog taxonomy, not a last-minute patch.

**Storyteller's position**: Not explicitly stated -- the storyteller did not mention the category choice in their revision notes. They likely carried it over from their original draft without noticing the `mkdocs.yml` constraint.

**Blocks publishing**: Yes. The MkDocs blog plugin will either error at build time or silently drop the post. This is a P0.

---

## Dispute 2: Which version of Post 2 is canonical?

**What the dispute is about**: The technical-writer and the storyteller each produced a full revised Post 2. These are substantially different documents -- different titles, different structures, different depth of technical content. No agent's revision designates which Post 2 is the one that ships.

- **Technical-writer's Post 2**: Title "Natural Language Game Theory Enforced with Optimization Modeling." Deep technical treatment. Includes the full `prisoners_dilemma_payoff` code block, the 8-mode game-form mapping table with equilibrium concepts, the three-tier solver description with `pip install` extras syntax, the AMPL forward-looking qualifier, and a 4-step "apply this to your own system" section.
- **Storyteller's Post 2**: Title "Why Your AI Agents Give Different Answers Every Time (And How to Fix It)." Audience-first framing. Lighter on implementation detail. Shorter code blocks. Broader framing around multi-agent consistency problems. Also includes the three-tier fallback and the 4-step pattern, but at a higher level.

**My position**: This is not a documentation-blocking dispute. Both versions are factually compatible with the docs after the P0/P1 fixes ship. However, the two versions target different audiences. The storyteller's version is more accessible to a general technical audience; the technical-writer's version serves readers who want to understand the implementation. The choice is editorial, not factual. The responsible action is to flag it for the human editor and not merge either until one is designated canonical.

**Technical-writer's position**: Their revision notes adopt several storyteller suggestions (table-driven structure, "apply this" section, toned-down AMPL claims) and present their version as the final draft.

**Storyteller's position**: Their revision notes also present their version as the final draft, incorporating technical-writer feedback (three-tier fallback, toned-down tunability, Kalman qualifier).

**Blocks publishing**: Yes, but only because you cannot publish two conflicting versions of the same post. Once one is chosen, the content itself does not block. Neither version makes claims the docs cannot support after the P0/P1 fixes.

---

## Dispute 3: AMPL tier description -- "config optimization" vs "formal optimization"

**What the dispute is about**: The three agents describe the AMPL Tier 2 capabilities differently.

- **Technical-writer** (Post 2, Tier 2 section): "The AMPL infrastructure and config optimizer exist today. Per-mode AMPL model templates -- formalizing each game form's specific optimization structure -- are specified in specs 043 and 044 and will ship in a future wave. The current AMPL tier handles configuration optimization; the upcoming templates will add mode-aware objective functions."
- **Storyteller** (Post 2, Tier 2 paragraph): "For modes that map to formal optimization problems -- resource allocation maps to linear programming, fair division maps to envy-free allocation -- AMPL formulations with the HiGHS solver can compute provably optimal allocations."

The storyteller's phrasing implies per-mode AMPL formulations exist and can "compute provably optimal allocations" today. The technical-writer explicitly qualifies that per-mode templates are future work (specs 043-044).

**My position**: The technical-writer's version is correct. The `packages/solvers.toml` declares `amplpy` and `highspy` as optional dependencies, and the config optimizer module exists, but no per-mode AMPL model templates have shipped. The storyteller's language ("AMPL formulations with the HiGHS solver can compute provably optimal allocations") overstates what is currently available. If we publish the storyteller's version, the docs would need to document per-mode AMPL formulations that do not yet exist. The technical-writer's qualified language ("The current AMPL tier handles configuration optimization; the upcoming templates will add mode-aware objective functions") is what the codebase supports.

**Storyteller's position**: Not explicitly defended in revision notes. The three-tier section was added in response to technical-writer feedback ("Post 2 never mentions AMPL or nashopt tiers") and the language appears to be the storyteller's interpretation of the capability.

**Blocks publishing**: Conditionally. If the storyteller's Post 2 is chosen as canonical, this specific phrasing must be qualified to match the technical-writer's treatment. If the technical-writer's Post 2 is chosen, no issue -- their language already carries the correct qualifier. The docs cannot support a claim of per-mode AMPL formulations without documentation for something that does not yet exist.

---

## Dispute 4: Kalman convergence predictor -- "ships with" vs "architecture supports"

**What the dispute is about**: Both revised posts reference Kalman convergence prediction, but with different confidence levels.

- **Technical-writer** (Post 1, Wave 3b): "Kalman convergence prediction" listed as a paid-tier feature with no qualifier.
- **Storyteller** (Post 2, tunability section): "the architecture supports more sophisticated approaches (the solvers package includes a Kalman filter designed for this purpose, though it is not yet documented for end users)."

The storyteller softened this claim in their revision. The technical-writer did not.

**My position**: The storyteller's qualified phrasing is better. The `solvers.toml` declares `scipy` as a dependency (which Kalman would use), and the package description says "convergence prediction," so the code likely exists. But no docs page describes the Kalman filter for end users. The technical-writer's Post 1 listing of "Kalman convergence prediction" as a simple bullet in the paid tier implies it is a documented, user-facing feature. It is not. The blog should use the storyteller's hedged language: the capability exists in code but is not yet documented for end users.

**Storyteller's position**: Explicitly addressed in revision notes item 8: "Changed from a concrete capability description to 'the architecture supports' language."

**Technical-writer's position**: Not addressed in revision notes for this specific item. Their Post 1 Wave 3b section lists "Kalman convergence prediction" as a straightforward paid-tier feature.

**Blocks publishing**: No. This is a precision issue, not a factual error. The feature likely exists in code. But it would be better practice to qualify it. If the technical-writer's Post 1 is used, the Kalman mention in the paid-tier feature list should add "(not yet documented for end users)" or similar.

---

## Dispute 5: Entry point inconsistency -- unresolved by all agents

**What the dispute is about**: `pyproject.toml` line 24 declares the CLI entry point as `engine.cli:cli`. `packages/core.toml` line 23 declares it as `engine.cli:main`. These are different Python callables. The docs-updater identified this in their revised gap analysis (P1-3). Neither the technical-writer nor the storyteller addressed it.

**My position**: This is a code inconsistency, not a blog dispute. However, it affects the blog's credibility: both posts describe `pip install conversus` as production-ready. If the published package has a different CLI entry point than the development environment, users will encounter different behavior. This needs investigation before publishing -- if `cli` and `main` resolve to the same behavior (e.g., `main` calls `cli()`), document that and align the strings. If they differ, fix the code.

**Technical-writer's position**: Not addressed.

**Storyteller's position**: Not addressed.

**Blocks publishing**: No, but it should block the P0/P1 doc fixes. The doc fixes proposed in the gap analysis assume `pip install conversus` produces a working CLI. If the entry point is wrong in `core.toml`, it does not. Verify before shipping the doc changes.

---

## Summary: Do the revised blog posts make claims the docs cannot support?

After reading all three revisions against the actual docs and source code:

**Technical-writer's posts**: After the P0/P1 doc fixes ship, no. The technical-writer's versions carry appropriate qualifiers on AMPL (future work), on pip install (locally buildable, PyPI separate step), and on the 31-test count. One minor issue: the Kalman mention in Post 1 should be qualified.

**Storyteller's posts**: Two issues remain. (1) The AMPL Tier 2 description in Post 2 implies per-mode formulations exist today -- the docs cannot support that claim. (2) Post 2 uses the `AI` category, which will break the build.

**Are the doc fixes sufficient to publish?** The P0 and P1 fixes identified in the docs-updater revision are necessary and sufficient to close the gap between the blog posts and the documentation, provided:

1. One canonical version of each post is chosen (Dispute 2).
2. The `AI` category is resolved (Dispute 1).
3. If the storyteller's Post 2 is chosen, the AMPL language is qualified (Dispute 3).
4. The entry point inconsistency is verified as benign before the doc fixes ship (Dispute 5).

If those four conditions are met, the blog posts and documentation will be consistent and publishable.

---

## Decision matrix

| # | Dispute | Blocks publishing? | Resolution path |
|---|---------|-------------------|-----------------|
| 1 | `AI` category in storyteller Post 2 | **Yes** | Change to `Process` or add `AI` to `mkdocs.yml` |
| 2 | Two competing Post 2 drafts | **Yes** | Human editor picks one |
| 3 | AMPL tier overstated in storyteller Post 2 | **Conditional** | Qualify if storyteller version chosen |
| 4 | Kalman listed without qualifier in tech-writer Post 1 | No | Add "(not yet user-documented)" hedge |
| 5 | Entry point `cli` vs `main` inconsistency | No (blocks doc fixes) | Verify code, align strings |
