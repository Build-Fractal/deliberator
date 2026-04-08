# Cooperative Revision — agents-md-specialist (Iteration 1)

## Recommendation Dispositions

### Original Recommendation 1: Create `templates/AGENTS.md` with template contribution rules
**Disposition: REVISED — Scope narrowed to pointers and contribution-only content**

All four cross-reviewers converge on the same critique: the template naming convention, structural markers, and variable syntax I proposed putting inline in `templates/AGENTS.md` are not purely contribution guidelines — they are runtime validation contracts enforced by the conversus engine during execution (integration-specialist Dangerous Contradiction 1; apm-specialist Dangerous Contradiction 1; agentskills-specialist Dangerous Contradiction 1; functional-decomposition Dangerous Contradiction 2). I accept this correction. The preset validation rules, template naming invariants, and structural markers (`<!-- CONVERSUS:TEMPLATE_STATUS: draft -->`, `<!-- CONVERSUS:DISPUTES_BEGIN/END -->`) are enforced at runtime. Duplicating them in AGENTS.md creates two sources of truth with no synchronization mechanism.

Revised position: `templates/AGENTS.md` should still exist, but it should contain only (a) a pointer to the authoritative source for template contracts (whichever reference file or SKILL.md section owns the rules), (b) the linter command (`uv run python linter/validate.py`) as a pre-contribution check, and (c) the file listing convention (7 files per mode directory) framed as "what to expect" rather than restating the enforcement rules. Estimated scope: 20-30 lines. This avoids the dual-source-of-truth problem while still giving non-Claude-Code agents a useful entry point when editing templates.

### Original Recommendation 2: Create `presets/AGENTS.md` with preset contribution rules
**Disposition: REVISED — Reduced to pointer file with linter reference**

The same dual-ownership problem applies here. integration-specialist (Dangerous Contradiction 1) correctly identifies that preset validation rules (name matching filename, category matching parent directory, composition limits) are enforced at runtime from three execution sites. apm-specialist (Dangerous Contradiction 1) reinforces this: the rules are runtime contracts, not contribution conventions. I was wrong to classify them as contribution-only.

Revised position: `presets/AGENTS.md` should be a minimal file (15-20 lines) that describes the directory structure, points to the authoritative validation source, and tells agents to run the linter before committing. It should not restate the validation rules themselves.

### Original Recommendation 3: Create `schema/AGENTS.md` with schema contribution rules
**Disposition: REVISED — Narrowed similarly**

The workflow for adding a variable (update `variables.yml`, update `modes/{mode}.yml`, run linter) is contribution guidance that is safe for AGENTS.md. The schema structure and variable contract definitions, however, are runtime-relevant. Revised to contain only the contribution workflow and a pointer to `schema/variables.yml` as the authoritative contract. Estimated scope: 15-25 lines.

### Original Recommendation 4: Create `linter/AGENTS.md` with development workflow
**Disposition: MAINTAINED — This is the strongest AGENTS.md recommendation**

All four cross-reviewers explicitly agree that the linter is under-documented for contributing agents (functional-decomposition Safe Agreement 4; integration-specialist Safe Agreement 4; apm-specialist Safe Agreement 2; agentskills-specialist Safe Agreement 3). The linter is a developer-facing command, not a runtime contract. Its invocation (`uv run python linter/validate.py`), test command (`uv run pytest linter/`), and setup instructions (`uv sync`) are pure contribution guidance with no dual-ownership risk. This is the one nested AGENTS.md where inline content is unambiguously correct.

I accept apm-specialist's complementary proposal for a PostToolUse hook (apm-specialist Tension 3) but note that the hook only protects Claude Code users. The AGENTS.md covers all other agents. Both can coexist.

### Original Recommendation 5: Update root `conversus/AGENTS.md` to reference nested files and fix staleness
**Disposition: MAINTAINED with scope constraint**

All cross-reviewers agree the root AGENTS.md is stale (functional-decomposition Safe Agreement 2; integration-specialist Safe Agreement 3). The structure section listing `tasks/` (nonexistent) and omitting `schema/`, `linter/`, `presets/`, `antipatterns/` is independently verifiable as wrong. This fix is low-risk and should proceed immediately regardless of decomposition strategy.

However, I accept functional-decomposition's and integration-specialist's warnings about scope creep (functional-decomposition Tension 3; integration-specialist Dangerous Contradiction 4). My original recommendation proposed adding testing, commit conventions, file relationships, antipattern references, and nested-file pointers — which would push the 51-line file well past my own 100-line guideline. Revised scope: fix the stale structure section, add the linter as a pre-contribution check, and add one line noting that subdirectories with their own AGENTS.md have directory-specific guidance. Total addition: ~15 lines, keeping the file under 70 lines.

### Original Recommendation 6: Do not move execution logic from SKILL.md to AGENTS.md
**Disposition: MAINTAINED — Universally agreed**

This is the load-bearing agreement across all five reviews. Every cross-reviewer affirmed this boundary. No revision needed.

### Original Recommendation 7: Add a "Relationship between files" section to root AGENTS.md
**Disposition: WITHDRAWN**

integration-specialist (Dangerous Contradiction 4) and functional-decomposition (Tension 3) correctly point out that this section, combined with the other proposed additions, would push the root AGENTS.md past my own 100-line guideline. The file-relationship information is also proposed for the root SKILL.md by both integration-specialist (Recommendation 10) and apm-specialist (Recommendation 10). Having it in both places creates a maintenance surface with no synchronization. The SKILL.md is the more natural home because the relationships are primarily about execution routing. I withdraw this recommendation and defer to whichever SKILL.md-based navigational hub the other reviewers converge on.

### Original Recommendation 8: Extract contribution-oriented content from SKILL.md into AGENTS.md
**Disposition: REVISED — Narrowed to exclude runtime-enforced rules**

This was the most contested recommendation. All four cross-reviewers identified that my classification of preset validation rules, template naming conventions, and the antipattern check as "contribution guidelines" was at least partly wrong — several of these are runtime-enforced contracts (integration-specialist Dangerous Contradiction 1; apm-specialist Dangerous Contradiction 1; agentskills-specialist Dangerous Contradiction 1; functional-decomposition Dangerous Contradiction 2).

I accept the correction on the specific items:
- **Preset validation rules** (name matches filename, category matches directory, composition limits): runtime contracts, not contribution guidelines. Must stay in SKILL.md or its reference files.
- **Template naming convention** (files must match phases): enforced by the linter and the template-loading subsystem at runtime. Must stay in SKILL.md or its reference files.
- **Antipattern check instruction**: dual-natured. It is both a pre-execution step (the engine checks the catalog) and a contribution guideline (agents should check the catalog). I now agree it should remain in SKILL.md for the execution path, with a mention (not duplication) in the root AGENTS.md.
- **Linter invocation** (`uv run python linter/validate.py`): this is the one item all reviewers agree is safe to surface in AGENTS.md. It is a developer command, not a runtime contract.

Revised estimate: the extractable contribution content is even smaller than my original 200-400 token estimate — closer to the linter command and a handful of "see also" pointers. I accept that AGENTS.md extraction is not a meaningful SKILL.md size-reduction strategy. It is an independent improvement for cross-agent contribution discoverability, and must not be framed as addressing the spec's core size problem.

### Original Recommendation 9: Keep AGENTS.md files under 100 lines each
**Disposition: MAINTAINED — Now easier to achieve given narrowed scope**

functional-decomposition (Dangerous Contradiction 3) and integration-specialist (Dangerous Contradiction 4) noted that my original content prescriptions for nested AGENTS.md files would strain the 100-line budget. With the revised scope (pointers + linter commands, not inline rule restatement), each nested file should be 15-30 lines — well within the guideline.

### Original Recommendation 10: Consider `antipatterns/AGENTS.md` if the catalog grows
**Disposition: MAINTAINED as conditional**

No cross-reviewer objected to this as a future consideration. It remains appropriately conditional.

## New Recommendations

### New Recommendation A: Establish a "single source of truth" convention with explicit pointers

The dominant cross-review theme is the dual-ownership problem: if rules exist in both AGENTS.md and SKILL.md (or its reference files), they drift. functional-decomposition (Tension 1), integration-specialist (Dangerous Contradiction 2, Tension 5), apm-specialist (Dangerous Contradiction 2), and agentskills-specialist (Tension 2) all independently identify this without proposing a resolution.

I propose a convention: **AGENTS.md files use "See [file] for authoritative rules" pointers, never inline rule restatement, for any content that is also enforced at runtime.** The AGENTS.md adds value by telling agents *that* rules exist and *where* to find them, plus the linter command to validate compliance. It does not duplicate the rules themselves. This is the reconciliation framework that was missing from both my original review and the cross-reviews.

The pointer format should be concrete: "Preset naming rules are enforced at runtime. See `SKILL.md` section [Preset Resolution] for the authoritative contract. Run `uv run python linter/validate.py` to check compliance before committing."

### New Recommendation B: Sequence AGENTS.md work after reference file extraction, not before

functional-decomposition (Dangerous Contradiction 1 and Tension 5), integration-specialist (Tension 4), and apm-specialist (Dangerous Contradiction 3) all warn that AGENTS.md creation could consume implementation budget while leaving the actual size problem unaddressed. I initially did not address sequencing, which was an oversight.

Revised position: the reference-file decomposition of SKILL.md (the agentskills-specialist and functional-decomposition proposals) should execute first, because it addresses the spec's core problem (SKILL.md is too large). Once reference files establish the authoritative locations for runtime contracts, the AGENTS.md files can be created with accurate pointers to those locations. Creating AGENTS.md files that point to the monolithic SKILL.md is less valuable than creating them after the content has been organized into reference files with clear boundaries.

The one exception is the root AGENTS.md staleness fix (Recommendation 5) — this is a 15-minute maintenance task that should proceed immediately.

### New Recommendation C: The linter should validate AGENTS.md accuracy as a stretch goal

agentskills-specialist (Dangerous Contradiction 2) makes a compelling point: `references/` files that are loaded at runtime fail visibly when they drift; AGENTS.md files fail silently. integration-specialist (Tension 2) envisions expanding the linter's scope for post-decomposition consistency checking.

I propose that once nested AGENTS.md files exist, the linter should include a lightweight check: verify that any files or directories referenced in AGENTS.md actually exist. This does not validate rule accuracy (that would require duplicating the rules), but it catches the most common staleness failure — referencing directories or files that have been renamed or removed. This directly addresses the staleness problem I identified in my original review (the root AGENTS.md listing nonexistent `tasks/`) by making it detectable.

## Position Summary

My original review overestimated the amount of SKILL.md content that qualifies as "contribution guidelines" and underestimated how many of the rules I proposed for AGENTS.md are actually runtime-enforced contracts. The cross-reviews from all four specialists converged on this correction with remarkable consistency.

My revised position is:

1. **AGENTS.md and SKILL.md serve different audiences** — this is the universal safe agreement across all five reviews and remains the foundational constraint.

2. **Nested AGENTS.md files are still valuable but must be pointer-based, not rule-restating.** The original proposal for 40-60 line inline rule documents creates dual sources of truth. The revised proposal: 15-30 line pointer files that tell contributing agents *where* rules live and *how* to validate compliance (the linter command). This preserves the cross-agent discoverability benefit while eliminating the drift risk.

3. **AGENTS.md is not a SKILL.md size-reduction strategy.** I accept this correction from all four cross-reviewers. The extractable contribution content is minimal. AGENTS.md creation is an independent improvement for cross-agent contribution discoverability, orthogonal to the decomposition spec's core goal. It should be framed and prioritized accordingly.

4. **The root AGENTS.md staleness fix should proceed immediately.** The structure section is wrong today. This is the lowest-risk, highest-certainty-of-value change in my entire recommendation set.

5. **`linter/AGENTS.md` is the strongest nested AGENTS.md recommendation** because the linter is unambiguously a developer tool, not a runtime contract. Its documentation in AGENTS.md creates no dual-ownership problem.

6. **Sequencing matters.** Reference file extraction first (establishes authoritative locations), then AGENTS.md creation (pointers to those locations). Not the reverse.

7. **The single-source-of-truth pointer convention** is the missing reconciliation mechanism. Every instance where AGENTS.md and SKILL.md cover overlapping territory should follow the pattern: SKILL.md (or its reference files) owns the rule, AGENTS.md points to it and provides the linter command.
