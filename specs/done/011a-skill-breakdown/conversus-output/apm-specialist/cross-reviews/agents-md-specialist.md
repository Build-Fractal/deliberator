# Cross-Review of agents-md-specialist

Reviewer: **apm-specialist**

---

## Dangerous Contradictions

### 1. AGENTS.md as an extraction target for SKILL.md content misunderstands the delivery mechanism

agents-md-specialist recommends extracting contribution-oriented content from SKILL.md into AGENTS.md files (Recommendation 8: "Extract contribution-oriented content from SKILL.md into AGENTS.md"). The specific items cited -- antipattern check instructions, template naming conventions, preset file validation rules, linter invocation -- are characterized as "contribution guidelines currently embedded in an execution spec."

My review (Actionable Recommendation 1) proposes splitting SKILL.md into sub-skills under `.apm/skills/`, where each sub-skill is independently promoted to `.github/skills/`, `.claude/skills/`, and `.cursor/skills/` via APM's sub-skill promotion mechanism. These are two fundamentally different decomposition strategies with incompatible outcomes.

The danger: if contribution rules are moved into AGENTS.md files (which are read at edit time by IDE agents), they are removed from the skill execution path. But several of these rules are not purely contribution guidelines -- they are runtime validation contracts. The preset validation rules (name matches filename, category matches parent directory, max 3 composable presets) are enforced by the conversus engine during `/conversus run`. If an agent reads them only in AGENTS.md and the engine's SKILL.md no longer states them, the engine's behavior becomes undocumented at the execution layer. The content must exist in both places, or only in the authoritative execution spec with AGENTS.md pointing to it. agents-md-specialist's Recommendation 6 ("Do not move execution logic from SKILL.md to AGENTS.md") acknowledges this boundary in principle, but Recommendation 8 crosses it in practice by treating preset validation and template naming as purely contribution concerns.

**Resolution**: Content that the conversus engine enforces at runtime must remain in SKILL.md (or a sub-skill's SKILL.md). AGENTS.md files should reference the authoritative location rather than duplicate or extract it. The decomposition target for SKILL.md size reduction is APM sub-skills, not AGENTS.md.

### 2. Nested AGENTS.md files duplicate what APM context primitives already solve

agents-md-specialist's highest-priority recommendations (1-4) propose creating four nested AGENTS.md files: `templates/AGENTS.md`, `presets/AGENTS.md`, `schema/AGENTS.md`, and `linter/AGENTS.md`. My review (Recommendations 4, 5, 7) proposes `.apm/context/` primitives for the same directories: `dispute-parsing.context.md`, `antipatterns.context.md`, `template-schema.context.md`.

These are competing mechanisms for the same problem -- making subdirectory-level knowledge discoverable to agents. The contradiction is not merely aesthetic. AGENTS.md files are read by proximity-based discovery (the nearest AGENTS.md to the file being edited). APM context primitives are resolved via context linking from any primitive that references them, and are deployed to all target directories during `apm install` and `apm compile`. The two systems have different resolution semantics, different update mechanisms, and different agent compatibility profiles.

If both are implemented, an agent editing `templates/cooperative/review.md` would receive context from: (a) the nested `templates/AGENTS.md`, (b) any APM context primitive linked from the active skill, and (c) the root AGENTS.md via inheritance. This creates three potentially contradictory sources of truth for the same rules. Drift between them is inevitable given that conversus is in active spec development (011a and counting).

**Resolution**: Choose one mechanism per knowledge domain. AGENTS.md files for cross-agent contribution rules that non-Claude agents need (linter commands, file naming). APM context primitives for execution-layer knowledge that the skill references (template variable contracts, dispute parsing interface). Do not create parallel representations.

### 3. The "200-400 token savings" estimate trivializes the actual decomposition problem

agents-md-specialist's Recommendation 8 estimates that extracting contribution content from SKILL.md to AGENTS.md would save "200-400 tokens from SKILL.md (modest, but these are the lines most relevant to AGENTS.md's purpose)." My review identifies the SKILL.md as 2200+ lines / 119KB and proposes sub-skill decomposition that would reduce per-invocation context load from 2200 lines to 400-800 lines per sub-skill.

The dangerous implication is that the agents-md-specialist's approach could be seen as a sufficient response to the spec's core problem (SKILL.md has grown too large). A 200-400 token reduction on a 119KB file is noise. The spec explicitly frames the problem as "our conversus/SKILL.md has grown quite large" -- the solution must achieve an order-of-magnitude context reduction, not a fractional one. If the team implements the AGENTS.md extraction strategy and considers the decomposition problem addressed, the actual context pollution remains unchanged.

**Resolution**: AGENTS.md creation and SKILL.md decomposition are separate workstreams. The AGENTS.md work improves contribution discoverability for non-Claude agents. The SKILL.md decomposition (via APM sub-skills or reference files) addresses the actual size problem. Neither substitutes for the other, and the AGENTS.md work should not be framed as a size-reduction strategy.

---

## Tensions

### 1. Cross-agent compatibility priority vs. single-consumer reality

agents-md-specialist frames nested AGENTS.md files as high-value because they are readable by "Claude Code, Copilot, Cursor, Windsurf, Junie" (Missed Opportunities, first bullet). My review notes that conversus is currently used by one project and the spec suite is actively evolving (Recommendation 8: "Defer full APM distribution until spec suite stabilizes").

agents-md-specialist partially acknowledges this tension (Off-Base Assumptions, second bullet: "the audience is narrower than implied") but still prioritizes multi-agent accessibility in the recommendations. The tension is real: investing in cross-agent discoverability for `templates/AGENTS.md` and `presets/AGENTS.md` has near-zero return today (no evidence of non-Claude agents contributing to conversus), but has nonzero maintenance cost (4 new files to keep synchronized with evolving SKILL.md). My review similarly proposes structural changes (sub-skills, context primitives) that have near-zero return until a second consumer appears.

Both reviews are making investments against a future state. The question is which investment has a better effort-to-optionality ratio. I maintain that APM structural changes (`.apm/skills/`, `.apm/context/`) are lower maintenance because they are consumed by the same toolchain that already manages the package, while AGENTS.md files require manual synchronization.

### 2. Contribution guidance scope: templates only vs. full codebase

agents-md-specialist's Recommendation 9 advocates keeping each AGENTS.md under 100 lines. My review proposes sub-skills at 400-800 lines each. These reflect different assumptions about how much context an agent needs to work effectively in a subdirectory.

For `templates/AGENTS.md`, agents-md-specialist scopes content to: required files per mode, variable syntax, structural markers, validation commands. This is contribution-level knowledge. But an agent modifying a template also needs to understand the phase orchestration that determines when the template is invoked, the variable expansion that populates template variables, and the mode-specific review sections that govern template content. That execution-level context lives in SKILL.md (or a sub-skill) and cannot be surfaced in a 40-60 line AGENTS.md without either duplicating it or leaving the agent with an incomplete picture.

The tension: lean AGENTS.md files are maintainable but incomplete; comprehensive ones drift toward SKILL.md territory. Neither review fully resolves this.

### 3. Linter as AGENTS.md documentation vs. APM hook

agents-md-specialist recommends documenting the linter in `linter/AGENTS.md` (Recommendation 4) with commands to run tests and validation. My review proposes a PostToolUse APM hook (Recommendation 6) that triggers `linter/validate.py` automatically on template file writes.

These are not contradictory -- both could coexist. But they represent different philosophies. AGENTS.md documentation requires the agent to know it should validate and to do so voluntarily. An APM hook enforces validation without agent cooperation. For Claude Code (the primary consumer), the hook is strictly superior. For non-Claude agents that cannot process APM hooks, the AGENTS.md documentation is the only path.

The tension is about where to invest effort first. agents-md-specialist optimizes for the broadest agent compatibility. My review optimizes for the deepest integration with the primary runtime.

### 4. Root AGENTS.md as a "relationship between files" map vs. lightweight entry point

agents-md-specialist's Recommendation 7 proposes adding a "Relationship between files" section to the root AGENTS.md explaining the roles of SKILL.md, AGENTS.md, README.md, and CLAUDE.md. This is architecturally sound but creates a meta-documentation layer that itself requires maintenance. My review proposes the root SKILL.md become a lightweight dispatcher (~100-150 lines) with a dependency graph (Recommendation 10).

Both recommend a navigational hub but place it in different files for different audiences. The AGENTS.md version serves contributing agents. The SKILL.md version serves the execution runtime. If both exist, the navigational information is duplicated across two files with different update cadences. This is manageable but should be acknowledged as a maintenance surface.

### 5. Staleness as evidence for or against centralization

agents-md-specialist notes the existing AGENTS.md is "already slightly outdated" (lists `tasks/`, omits `schema/`, `linter/`, `presets/`) and uses this as evidence that "nested AGENTS.md files in subdirectories would be more maintainable than a monolithic root-level structure map" (Alignment, sixth bullet).

My review implicitly assumes the opposite: that structural information should be centralized in APM-managed artifacts (context primitives, sub-skill SKILL.md files) because APM's compilation and installation pipeline provides a single update mechanism. Decentralized AGENTS.md files are more likely to go stale precisely because no toolchain manages them -- they rely on human diligence or agent awareness.

Both positions have merit. Nested files reduce the blast radius of staleness (only the stale file is wrong, not the entire project guide). Centralized APM primitives reduce the probability of staleness (one toolchain, one update path). The right answer likely depends on whether conversus adopts active APM compilation or remains a submodule with manual maintenance.

---

## Safe Agreements

### 1. SKILL.md execution logic must not migrate to AGENTS.md

Both reviews converge on this boundary. agents-md-specialist states: "AGENTS.md cannot replace any part of SKILL.md's execution specification" (Off-Base Assumptions, first bullet) and "Do not move execution logic from SKILL.md to AGENTS.md" (Recommendation 6). My review states: "The guided workflow is not separable from the run engine at the APM level" (Off-Base Assumptions, third bullet) and frames all SKILL.md decomposition as internal structural splits, not cross-format migrations.

This agreement is load-bearing. The spec's framing ("opportunities to offload some of the work") could be read as suggesting AGENTS.md absorb execution content. Both reviews reject this reading and agree that AGENTS.md and SKILL.md serve categorically different purposes: contribution guidance vs. execution specification.

### 2. The linter and validation workflow are under-documented for contributing agents

agents-md-specialist identifies that the linter is only documented in SKILL.md (Missed Opportunity, sixth and seventh bullets) and that the root AGENTS.md lacks any mention of validation as a pre-contribution requirement. My review identifies the linter as a candidate for an APM hook (Recommendation 6) and the schema as a natural APM context artifact (Recommendation 7).

Both reviews agree the gap exists and that it impacts contribution quality. The disagreement is on mechanism (AGENTS.md documentation vs. APM hook), not on diagnosis. Any implementation that surfaces the linter's existence and invocation to contributing agents -- whether through AGENTS.md, APM hooks, or both -- addresses the identified gap.

### 3. The conversus codebase needs subdirectory-level guidance for contributors

agents-md-specialist proposes nested AGENTS.md files in `templates/`, `presets/`, `schema/`, and `linter/`. My review proposes APM context primitives in `.apm/context/` covering modes, dispute parsing, antipatterns, and template schema. The mechanism differs, but the underlying diagnosis is identical: the monolithic root-level documentation (whether SKILL.md or AGENTS.md) does not adequately guide agents working within specific subdirectories.

Both reviews independently arrived at the same list of directories needing dedicated guidance: templates, presets, schema, linter. This convergence validates the decomposition boundaries even if the implementation vehicle remains under debate.
