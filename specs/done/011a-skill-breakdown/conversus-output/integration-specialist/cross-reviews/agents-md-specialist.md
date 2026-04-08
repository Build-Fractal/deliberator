# Cross-Review of agents-md-specialist — by integration-specialist

## Dangerous Contradictions

### 1. Contribution guidance extraction vs. runtime invariant integrity

agents-md-specialist recommends extracting contribution-oriented content from SKILL.md into AGENTS.md files (Actionable Recommendation 8: "the antipattern check instruction, the template naming convention, the preset file validation rules, and the linter invocation"). My review identifies the antipattern check (lines 237-244) as a pre-execution step that the run engine performs before launching agents, and preset validation (lines 139-200) as a shared subsystem called from three execution sites (run engine config parsing, interests handler, gate handler agent expansion — my Missed Opportunities, bullet 5).

The contradiction: agents-md-specialist treats these as "contribution guidelines currently embedded in an execution spec." They are not. Preset validation rules are enforced at runtime — the engine halts with specific error messages when `name` does not match filename, when `category` does not match parent directory, when `composable: false` blocks composition. Moving these to `presets/AGENTS.md` creates a dangerous split: the canonical validation rules would live in AGENTS.md (a file no runtime reads), while the execution engine in SKILL.md would need to either duplicate them or reference an AGENTS.md file (which violates the AGENTS.md standard's own scope — it is read by IDEs at edit time, not by skill runtimes at execution time, as agents-md-specialist correctly notes in Off-Base Assumptions, bullet 3). The result is either drift between the two copies or a runtime that silently loses validation rules.

The linter invocation (`uv run python linter/validate.py`) is safe to surface in AGENTS.md because it is a developer command, not a runtime contract. But the validation rules themselves — the exact error messages, the field constraints, the composition limits — are interface contracts that my review identifies as requiring explicit "do not decompose" boundaries (my Actionable Recommendation 7). Extracting them to AGENTS.md undermines that boundary.

### 2. Nested AGENTS.md files as decomposition vs. reference files as decomposition

agents-md-specialist proposes four nested AGENTS.md files (`templates/`, `presets/`, `schema/`, `linter/`) as the primary decomposition mechanism for surfacing rules to contributing agents. My review proposes reference files (`references/handler-*.md`, `references/subsystem-*.md`, `references/contract-*.md`) as the primary decomposition mechanism for reducing SKILL.md's size while preserving runtime coherence.

These are not complementary — they compete for the same content. Consider preset resolution rules: agents-md-specialist puts them in `presets/AGENTS.md` (Recommendation 2), while my review puts them in `references/subsystem-preset-resolution.md` (Recommendation 5). The preset composition templates, the disambiguation logic, the error message contracts — where do they live? If both files exist, one is authoritative and the other is a stale summary. If only AGENTS.md exists, the runtime cannot reference it (SKILL.md's `@references` mechanism points to `.md` files in the `references/` directory, not to AGENTS.md files in subdirectories). If only the reference file exists, non-Claude-Code agents cannot discover the rules at edit time.

This is a genuine architectural tension: the AGENTS.md approach optimizes for cross-agent discoverability at the cost of runtime integration, while the reference file approach optimizes for runtime coherence at the cost of cross-agent reach. agents-md-specialist does not acknowledge this trade-off. Neither does my review. Resolving it requires an explicit decision about which file is authoritative and which is derivative — and a mechanism (likely the linter) to keep them in sync.

### 3. "Modest" SKILL.md size reduction vs. the spec's stated goal

agents-md-specialist estimates "200-400 tokens" of savings from SKILL.md by moving contribution guidelines to AGENTS.md (Recommendation 8). My review estimates ~900 lines extracted via handler reference files (Recommendation 2) plus ~180 lines for the gate handler (Recommendation 3) plus ~50-100 lines for subsystem extractions (Recommendations 4-6), totaling roughly 1100-1200 lines — bringing the root SKILL.md from 2216 lines to ~400-500 lines.

The contradiction: the spec's problem statement is that SKILL.md is too large (2216 lines, 4x the agentskills.io recommendation). agents-md-specialist's approach does not meaningfully address this. A 200-400 token reduction on a 31k-token file is cosmetic. agents-md-specialist acknowledges this indirectly ("AGENTS.md can reduce SKILL.md's size only by absorbing contribution guidelines — a modest but real saving," Off-Base Assumptions, bullet 1) but then frames AGENTS.md as a primary decomposition strategy rather than a complementary one. The risk: if AGENTS.md creation is treated as addressing the spec's goal, it could delay or displace the reference file decomposition that actually solves the size problem. agents-md-specialist should have been explicit that AGENTS.md is orthogonal to the size reduction goal and should not be counted toward it.

### 4. File-relationship documentation placement contradicts agents-md-specialist's own 100-line guideline

agents-md-specialist recommends keeping each AGENTS.md under 100 lines (Recommendation 9) and also recommends adding a "Relationship between files" section to the root AGENTS.md (Recommendation 7), updating the structure section to cover all subdirectories (Recommendation 5), adding testing sections, commit conventions, and references to nested files (Recommendation 5). The current root AGENTS.md is 51 lines. Adding all proposed content — file relationships, updated structure (adding 5 directories), testing section, commit conventions, antipattern catalog mention, nested file references — would push it well past 100 lines. Meanwhile, my review proposes a dependency map table in the root SKILL.md (Recommendation 10), which serves a similar purpose (documenting how files relate) but in the file that the runtime actually reads.

The contradiction is internal to agents-md-specialist's review: the 100-line guideline conflicts with the cumulative scope of their own recommendations for the root AGENTS.md. It also conflicts externally with my recommendation: if both a dependency map in SKILL.md and a relationship section in AGENTS.md exist, they will drift apart because they serve different audiences (runtime vs. contribution) and will be updated at different times.

## Tensions

### 1. Cross-agent compatibility as a primary vs. secondary concern

agents-md-specialist frames cross-agent compatibility as valuable but secondary (Off-Base Assumptions, bullet 2: "The cross-agent benefit is for agents contributing to the conversus codebase, not agents using conversus"). My review does not address cross-agent compatibility at all — it focuses entirely on the conversus runtime's internal coherence. These positions are compatible in principle but create a prioritization tension in practice: when a decomposition decision requires choosing between runtime coherence (my priority) and cross-agent discoverability (agents-md-specialist's priority), which wins? For example, should preset validation rules be documented where the runtime can reference them (reference file) or where all agents can discover them (nested AGENTS.md)? Neither review establishes a hierarchy.

### 2. Linter scope expansion expectations

agents-md-specialist proposes the linter as a contribution validation tool, surfaced in `linter/AGENTS.md` (Recommendation 4). My review proposes expanding the linter's scope to validate reference file consistency after decomposition (Recommendation 8: checking variable references, error message strings, and interface contract consistency). These are different expectations: agents-md-specialist sees the linter as a developer-facing command to document; I see it as an integration test that must grow with the decomposition. The tension is that expanding linter scope (my recommendation) changes the content of the `linter/AGENTS.md` file (agents-md-specialist's recommendation) — the development workflow documented there becomes a moving target during decomposition.

### 3. The antipattern check as contribution guideline vs. orchestrator-level concern

agents-md-specialist classifies the antipattern check (SKILL.md lines 237-244) as a "contribution guideline, not an execution rule" that "belongs in AGENTS.md" (Missed Opportunities, bullet 7). My review asks an unanswered question: "If each handler becomes a reference file, does each handler need its own antipattern check, or is this an orchestrator-level concern?" (Missed Opportunities, bullet 3). The tension: the antipattern check is currently both. It is a pre-execution step (the run engine checks the catalog before launching agents) and a contribution guideline (agents proposing changes should check the catalog). agents-md-specialist resolves this by classifying it as purely contribution-oriented, but that ignores its runtime role. My review leaves it unresolved. The correct answer likely involves surfacing it in both places — AGENTS.md for contributors and SKILL.md for the runtime — but then the synchronization problem reasserts itself.

### 4. Scope of "decomposition" itself

agents-md-specialist interprets spec 011a's decomposition goal as "how to make conversus rules discoverable across agent ecosystems." My review interprets it as "how to break SKILL.md into smaller files that preserve integration contracts." These are different problems with different solutions. agents-md-specialist's solution (nested AGENTS.md files) does not reduce SKILL.md's token count in any meaningful way. My solution (reference files) does not improve cross-agent discoverability. Both are valid responses to the spec, but they answer different questions. The tension materializes when implementation begins: which work is prioritized? If nested AGENTS.md files are created first, the team may perceive progress on the spec without having addressed the core size problem. If reference files are created first, cross-agent discoverability remains unaddressed.

### 5. Whether AGENTS.md files should contain rules or pointers

agents-md-specialist's nested AGENTS.md proposals are rule-bearing: `templates/AGENTS.md` would contain the actual naming convention, variable syntax, structural marker list, and validation command (Recommendation 1, estimated 40-60 lines). My decomposition approach would put those same rules in `references/contract-template-variables.md` and `references/subsystem-preset-resolution.md`. The tension: if the reference files are authoritative (as my review assumes), the AGENTS.md files should contain pointers to them, not duplicates of the rules. But pointer-only AGENTS.md files ("see references/subsystem-preset-resolution.md for preset rules") are nearly useless for agents that cannot follow agentskills.io reference file links (Copilot, Cursor). agents-md-specialist's whole value proposition depends on the rules being inline, not referenced.

## Safe Agreements

### 1. SKILL.md and AGENTS.md serve fundamentally different purposes

Both reviews agree that SKILL.md is an executable specification and AGENTS.md is a contribution guide, and that these roles should not be conflated. agents-md-specialist states this explicitly: "SKILL.md is an executable specification — it has YAML frontmatter, activation logic, tool permissions, and a runtime contract. AGENTS.md is a universal contribution guide" (Executive Summary). My review does not use AGENTS.md at all, implicitly confirming that the runtime decomposition is a SKILL.md-internal concern. Neither review proposes moving execution logic into AGENTS.md. This shared boundary is safe and should be preserved as a design constraint for implementation.

### 2. The subcommand dispatch table should remain in the root SKILL.md

agents-md-specialist does not propose moving the dispatch table to AGENTS.md — it is acknowledged as a SKILL.md concern (Alignment, bullet 4: "SKILL.md's frontmatter has no AGENTS.md equivalent"). My review explicitly recommends keeping it as the entry point contract (Recommendation 1). Both reviews agree this is the anchor of the root SKILL.md. This is safe because the dispatch table is pure runtime routing — it has no contribution-oriented content that would benefit from AGENTS.md exposure.

### 3. The existing AGENTS.md structure section is stale and needs updating

agents-md-specialist identifies staleness (Alignment, bullet 6: "lists `tasks/` (no longer present) and omits `schema/`, `linter/`, `presets/`, `antipatterns/`, and `.specify/`"). My review does not address the existing AGENTS.md content, but my observation that the `references/` directory conflates external docs with internal subsystem specs (Missed Opportunities, bullet 7) is a parallel instance of the same problem — documentation not keeping up with directory evolution. Both reviews agree that the current state of directory documentation is inadequate. This is a low-risk fix that can proceed independently of the decomposition decision.

### 4. The linter is critical infrastructure for any decomposition approach

agents-md-specialist recommends documenting the linter in a dedicated `linter/AGENTS.md` (Recommendation 4) and referencing it as a pre-contribution check (Recommendation 5). My review recommends expanding the linter's scope to validate reference file consistency (Recommendation 8). Both reviews position the linter as the primary mechanism for preventing decomposition-induced drift. This agreement is safe and actionable: regardless of whether the decomposition proceeds via AGENTS.md files, reference files, or both, the linter must be the integration test that catches inconsistencies.
