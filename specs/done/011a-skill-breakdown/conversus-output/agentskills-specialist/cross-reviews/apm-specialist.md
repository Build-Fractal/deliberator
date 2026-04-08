# Cross-Review of apm-specialist's Review

Reviewer: **agentskills-specialist**
Target: apm-specialist's Phase 1 review of conversus SKILL.md extractability

---

## Dangerous Contradictions

### 1. Sub-skill promotion does not solve the progressive disclosure problem -- it replaces one monolith with several monoliths

apm-specialist's central recommendation (Recommendation 1) is to "create `.apm/skills/` directory with three sub-skills immediately" -- `conversus-engine`, `conversus-wizard`, and `conversus-gate`. The claim is that this "reduces per-invocation context load from 2200 lines to ~400-800 per sub-skill." This contradicts a structural reality of the agentskills.io specification that my review addressed directly.

APM sub-skill promotion copies each sub-skill's SKILL.md to `.github/skills/`, `.claude/skills/`, etc. Each sub-skill then loads its *entire* SKILL.md body when activated. The `conversus-engine` sub-skill would still be 800+ lines containing all four competition mode specifications, all template variable contracts, the Dispute-Parsing Subsystem, preset resolution rules, and multi-round execution mechanics -- loaded on every `/conversus run` invocation regardless of which mode, whether presets are used, or whether it is a single-round run.

My review (Missed Opportunities, items 1-3) identified that the right decomposition axis is not *sub-skill splitting* but *progressive disclosure within a single skill*. The agentskills.io specification explicitly recommends: "Keep your main SKILL.md under 500 lines. Move detailed reference material to separate files." The mechanism is conditional file loading (`"Read references/handler-run.md if the user invokes /conversus run"`), not sub-skill activation. Sub-skills solve a *distribution* problem (different consumers need different capabilities). Progressive disclosure solves the *context window* problem (one consumer needs different details at different moments). Conversus has a context window problem, not a distribution problem.

**Risk**: Implementing three sub-skills without progressive disclosure within each sub-skill yields three 400-800 line SKILL.md files that each individually violate the 500-line / 5,000-token recommendation. The context reduction is real but insufficient, and the implementation path is more complex (three `apm.yml` manifests, sub-skill dependency graph, dispatch routing between sub-skills) than the simpler path of reference file extraction within a single skill.

### 2. APM context primitives and agentskills.io reference files are competing mechanisms for the same content

apm-specialist recommends (Recommendations 2, 4, 5, 7) creating `.apm/context/` files for modes, dispute-parsing, antipatterns, and template schemas. My review recommends `references/` files for the same content. These are not two names for the same thing -- they are two different systems with different loading semantics, different directory locations, and different toolchain dependencies.

APM context primitives (`.apm/context/*.context.md`) are compiled by `apm compile` into the target's CLAUDE.md or equivalent, governed by `applyTo` patterns and distribution scoring. They load based on *file path matching*, not *agent execution state*. An `.apm/context/modes/cooperative.context.md` with `applyTo: "**/cooperative/**"` would load when the agent is working in a directory that matches that glob -- which may or may not correlate with the agent actually running a cooperative-mode deliberation.

agentskills.io reference files (`references/*.md`) load when the SKILL.md body explicitly instructs the agent to read them, based on *runtime conditions*: "If the config specifies `mode: cooperative`, read `references/mode-cooperative.md`." The loading trigger is the actual execution state, not a filesystem path pattern.

My review (Recommendation 9) specified conditional loading triggers for each reference: "If the config contains an `arbiter:` block, read `references/arbitration-engine.md`." apm-specialist's context primitive approach cannot express these runtime conditionals -- `applyTo` patterns match file paths, not YAML config field values.

**Risk**: Implementing both systems simultaneously (APM context primitives for "compile-time" and agentskills references for "runtime") creates two parallel inventories of the same content that drift independently. An update to `references/dispute-parsing.md` would not automatically propagate to `.apm/context/dispute-parsing.context.md`, and vice versa.

### 3. The PostToolUse hook recommendation misunderstands the linter's role in the conversus execution model

apm-specialist recommends (Recommendation 6) creating a PostToolUse hook that triggers `linter/validate.py` when files in `templates/` are modified. This contradicts how conversus templates are actually used during deliberation execution.

Templates are *read* during Phase 1-6 execution -- the agent fills template variables and writes the *output* to the output directory, not to the templates directory. The templates themselves are modified only during skill development (adding new modes, changing phase structure), not during deliberation runs. A PostToolUse hook on `templates/` writes would fire during development, not during execution.

More importantly, my review (Off-Base Assumptions, item 1) noted that the SKILL.md already instructs the agent to run the linter as a validation step. The agentskills.io best practices explicitly recommend "validation loops" as a pattern: "do the work, run a validator, fix any issues, repeat until validation passes." This is an *agent-directed* validation loop, not a *hook-triggered* one. Converting it to an APM hook moves the validation from agent-visible (the agent sees the linter output and can self-correct) to hook-invisible (the hook runs silently and may block the tool call without the agent understanding why).

**Risk**: The hook fires on the wrong trigger (template writes during development instead of output writes during execution) and removes the agent's ability to reason about validation failures.

### 4. Treating presets as a sub-skill conflates discoverability with execution context

apm-specialist's Recommendation 3 proposes `.apm/skills/conversus-presets/SKILL.md` that "documents the preset schema, resolution rules, composition templates, and lists available presets by category." This would be loaded whenever an agent activates the `conversus-presets` sub-skill. But my review (Missed Opportunities, item 8) identified that preset resolution rules are only needed "when a config contains `preset:` fields" -- a runtime condition, not an activation-time decision.

The agentskills.io progressive disclosure model distinguishes between *activation cost* (full SKILL.md body loads) and *reference cost* (file loads on demand). Making presets a sub-skill means the full preset schema, all composition templates, and the complete preset catalog load whenever the sub-skill activates. Making preset resolution a reference file means it loads only when the specific config being processed uses presets.

apm-specialist's own Off-Base Assumptions section acknowledges that "presets are tightly coupled to conversus's composition template system" and "a preset outside conversus has no meaning." If presets are tightly coupled to the run engine and only meaningful within conversus, they are reference material for the run handler, not an independent skill.

**Risk**: A `conversus-presets` sub-skill loads the full preset specification on activation even when the current deliberation does not use presets, wasting context tokens on the exact problem the spec (011a) aims to solve.

---

## Tensions

### 1. Timing of structural changes: "immediately" vs "after stabilization"

apm-specialist's Recommendation 1 says "create `.apm/skills/` directory with three sub-skills *immediately*" but Recommendation 8 says "defer full APM distribution until spec suite stabilizes." My review did not address timing -- it focused on the target state architecture. There is a genuine tension here: the SKILL.md is too large *now*, but the framework is actively evolving (11+ specs).

apm-specialist resolves this by separating structure (do now) from distribution (do later). This is a reasonable approach, but the "immediate" sub-skill split creates a structural commitment that may need revision as specs 012-020 (queued per recent commit messages) introduce new subcommands or modify existing ones. The agentskills.io reference file approach I recommended has lower structural commitment -- adding or reorganizing reference files does not require changing the sub-skill graph.

### 2. Where the dispatch table lives

Both reviews agree the dispatch table is well-designed and should remain in the always-loaded core. But apm-specialist's sub-skill model requires the dispatch table to route to *sub-skills* ("which sub-skill handles which subcommand"), while my reference-file model routes to *reference files* ("read `references/handler-define.md` when the user invokes `/conversus define`").

The sub-skill dispatch model introduces a layer of indirection: the root SKILL.md dispatches to a sub-skill, which then dispatches to its internal handler. This means the agent loads the root SKILL.md (to get the dispatch table), then loads the sub-skill SKILL.md (to get the handler). That is two activation costs. The reference-file model is one activation (root SKILL.md) plus one file read (the handler reference). The token cost may be comparable, but the agent's reasoning path is simpler with one skill plus references than with a skill-to-sub-skill handoff.

### 3. The role of the schema directory

apm-specialist (Recommendation 7) wants `schema/variables.yml` and `schema/modes/*.yml` as APM context primitives. My review (Alignment, item 4) noted that these files already exist and serve a machine-checkable contract function. The tension is whether the schema files are *developer documentation* (best served by APM context primitives that compile into CLAUDE.md for developers working on conversus) or *agent execution references* (best served by agentskills.io references that the agent reads when filling templates).

They are arguably both. A developer modifying templates needs the schema to know what variables are available. An agent executing a deliberation needs the schema to fill variables correctly. The two audiences have different loading triggers (file path matching for developers, runtime config parsing for agents), which is why the two systems handle them differently.

### 4. The antipattern catalog's classification

apm-specialist (Recommendation 5) classifies `antipatterns/catalog.md` as an APM context primitive. My review did not address the antipattern catalog directly. The tension is whether antipattern awareness should be *always loaded* (context primitive compiled into the base CLAUDE.md) or *conditionally loaded* (reference file read when the agent is about to write a synthesis or review).

The agentskills.io best practices state: "Keep gotchas in SKILL.md where the agent reads them before encountering the situation." Antipatterns are a form of gotcha -- patterns the agent should avoid during synthesis writing. If they are only loaded as a reference file, the agent must be told *when* to read them, and a missed trigger means the antipatterns are not in context during the synthesis phase. If they are compiled into the base CLAUDE.md, they are always available but always consuming tokens. This is a genuine tradeoff that neither review fully resolved.

### 5. Version pinning between SKILL.md and templates

apm-specialist (Missed Opportunities, item 7) flags the lack of version pinning between SKILL.md template variable contracts and actual template files, noting that "drift is caught only by the linter, not by the package system." My review did not address version pinning. The tension is whether package-level version enforcement adds value when the linter already catches drift.

The linter catches drift at development time (when someone runs `uv run python linter/validate.py`). APM version pinning would catch it at install time (when a consumer runs `apm install`). For a single-project framework with no external consumers, install-time checking adds nothing over development-time checking. If conversus gains external consumers, the calculus changes. This aligns with apm-specialist's own Recommendation 8 about deferring distribution.

---

## Safe Agreements

### 1. The SKILL.md is too large and must be decomposed

Both reviews agree unambiguously. apm-specialist: "At 119KB / 2200+ lines, this exceeds any reasonable context window budget for a single skill." My review: "At 31k tokens, the SKILL.md is roughly 6x the recommended token budget." We also agree on the *why*: the agent pays the full context cost regardless of which subcommand is invoked, and most of that context is irrelevant to any single invocation.

### 2. The Dispute-Parsing Subsystem should be extracted to its own file

apm-specialist (Recommendation 4): "Extract the Dispute-Parsing Subsystem into `.apm/context/dispute-parsing.context.md`." My review (Recommendation 3): "Extract the Dispute-Parsing Subsystem to `references/dispute-parsing.md`." We disagree on the file location and loading mechanism (see Dangerous Contradiction 2), but we agree completely that this subsystem -- with its stable interface, three-handler dependency, and approximately 30 lines of specification -- is a clear extraction candidate that should not be inline in the run engine section.

### 3. The gate subcommand is architecturally independent and should be separated from the interactive subcommands

apm-specialist: "Gate reads a `gates.yml`, generates a standard `conversus.yml`, delegates to the run engine, and produces a machine-readable `gate-result.md`. Its only dependency on the rest of SKILL.md is the run engine and the Dispute-Parsing Subsystem. This is a clean extraction boundary." My review: "The gate subcommand is approximately 300 lines of CI/CD-specific specification including exit codes, gate-result.md schemas, re-run behavior, and full output preservation rules. This is a coherent unit that serves a different audience."

Both reviews identify the gate as the cleanest extraction target, and for the same reason: it serves a distinct audience (CI/CD pipeline authors vs. interactive deliberation users) and has minimal coupling to the rest of the skill.

### 4. Template variable contracts should be consolidated rather than scattered across phases

apm-specialist (Missed Opportunities, item 2): "Templates are not leveraging APM's resource bundling model... mode-specific prompt engineering." My review (Recommendation 4): "Consolidate all phase-specific variable definitions, path-list formatting rules, round-aware path variables, and the variable expansion rules into a single reference."

We agree that the current scatter of template variable definitions across multiple phases creates redundancy and makes the variable contract difficult to audit. The consolidation target differs (APM resource bundles vs. agentskills reference file), but the diagnosis is the same.
