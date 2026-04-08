# Cross-Review of agentskills-specialist

Reviewer: agents-md-specialist

## Dangerous Contradictions

### 1. Handler extraction assumes AGENTS.md irrelevance to the decomposition

agentskills-specialist recommends extracting all seven subcommand handlers into `references/handler-*.md` files, producing a 300-400 line SKILL.md core (Recommendation 1). This treats the decomposition as entirely internal to the agentskills.io progressive disclosure model. My review identifies that contribution-oriented content -- template naming conventions (SKILL.md ~line 283), preset validation rules (lines 139-145), linter invocation (line 309), and antipattern checks (line 239) -- is currently embedded in SKILL.md and should migrate to AGENTS.md or nested AGENTS.md files because it serves agents *contributing to* conversus, not agents *executing* it (my Recommendation 8). If agentskills-specialist's handler extraction proceeds without first triaging which content is contribution guidance versus execution specification, the extracted `references/handler-*.md` files will carry contribution rules that belong in AGENTS.md. The result: two parallel systems of contribution documentation (AGENTS.md for some rules, reference files for others), discoverable by different agents under different conditions. An agent editing presets in Cursor reads `presets/AGENTS.md` but never sees the validation rules locked inside `references/handler-run.md`. The extraction must triage before splitting.

### 2. The proposed reference file count risks a different kind of bloat

agentskills-specialist proposes 14 reference files (Recommendation 10: 7 handler files plus dispute-parsing, template-variables, validation-rules, preset-resolution, arbitration-engine, multi-round-execution, and operational-notes) plus 3 asset files. My review warns that AGENTS.md files should stay under 100 lines each (my Recommendation 9), implicitly applying a minimalism principle. The same principle applies to reference file proliferation. The agentskills.io best practices document warns that overly fragmented reference structures can hurt when the agent must read multiple files to assemble a complete picture. For the `run` subcommand, the agent would need to load `references/handler-run.md` plus potentially `references/template-variables.md`, `references/validation-rules.md`, `references/preset-resolution.md`, `references/dispute-parsing.md`, `references/multi-round-execution.md`, and `references/arbitration-engine.md` -- seven reference reads for a single subcommand invocation. The token savings from not loading the other six handlers may be partially offset by the overhead of conditional file reads and the risk of incomplete context assembly. The conditional loading instructions (Recommendation 9) mitigate this but also add their own complexity to the core SKILL.md. A flatter structure with fewer, larger reference files (e.g., one `references/handler-run.md` that inlines its own template variables and validation rules) would trade some token efficiency for reliability.

### 3. "Omit what the agent already knows" applied to agent count formulas misreads the audience

agentskills-specialist's Off-Base Assumption 3 argues that agent count formulas (lines 2186-2196) are redundant because "any LLM can derive from the phase structure" the arithmetic `N^2 + 2N + 1`. My review takes no position on removing these formulas, but the agentskills-specialist's reasoning is dangerous. The formulas serve a runtime safety function: the pre-execution estimate (lines 315-322) uses them to warn the user before launching potentially dozens of agents. If the formulas are removed and the agent must derive them, any derivation error means the estimate is wrong and the user gets no accurate warning before a resource-intensive run. The formulas are not documentation of "what the agent already knows" -- they are the authoritative contract for a user-facing estimate. An agent that derives `N^2 + N + 1` instead of `N^2 + 2N + 1` (a plausible off-by-one for the dispute phase count) produces a silently incorrect estimate. The formulas should remain somewhere in the reference material as the canonical source of truth, even if they are moved out of the always-loaded core.

### 4. No acknowledgment that SKILL.md and AGENTS.md serve overlapping-but-distinct agent populations

agentskills-specialist's entire review treats the decomposition as a SKILL.md-internal restructuring. There is no mention of AGENTS.md, the existing 51-line `conversus/AGENTS.md`, or the cross-agent contribution scenario. My review's central thesis is that SKILL.md and AGENTS.md serve complementary audiences (my Executive Summary, paragraphs 2-3): SKILL.md is an executable specification for Claude Code; AGENTS.md is a universal contribution guide readable by Copilot, Cursor, Windsurf, Junie, and others. By ignoring this dimension entirely, agentskills-specialist's recommendations optimize token budget for one agent runtime while leaving contribution guidance locked inside a format that only one runtime can parse. The spec (spec.md line 4) explicitly lists agents.md as one of the decomposition targets. A restructuring that addresses only agentskills.io progressive disclosure misses half the spec's intent.

## Tensions

### 1. Granularity of reference extraction

agentskills-specialist advocates fine-grained extraction: separate files for dispute-parsing (~30 lines), validation-rules, template-variables, preset-resolution, arbitration-engine, and multi-round-execution. My review advocates a different kind of granularity: nested AGENTS.md files per subdirectory (`templates/AGENTS.md`, `presets/AGENTS.md`, `schema/AGENTS.md`, `linter/AGENTS.md`). Both approaches decompose the monolith, but along different axes. The agentskills.io approach decomposes by *execution concern* (what the engine needs per phase). The AGENTS.md approach decomposes by *directory location* (what a contributing agent needs per edit site). These are orthogonal and can coexist, but the combined file count (14 reference files + 4-5 nested AGENTS.md files) needs coordination to avoid rule duplication. For example, preset validation rules would appear in both `references/preset-resolution.md` (for the runtime) and `presets/AGENTS.md` (for contributors). Both reviews should acknowledge that a single source of truth strategy is needed.

### 2. Whether the SKILL.md can realistically reach the 5,000 token target

agentskills-specialist sets an explicit target: "300-400 lines, under 5,000 tokens" (Recommendation 2). My review does not contest this target but also does not endorse it. The dispatch table, non-negotiable multi-agent rules, phase flow summary, gotchas, and conditional loading instructions for 14+ reference files will produce dense specification prose. agentskills-specialist acknowledges this tension in Off-Base Assumption 4 ("even aggressive restructuring to 500 lines would likely still exceed the 5,000 token recommendation if those lines are dense specification prose") but then proceeds to recommend a 300-400 line target anyway. The realistic outcome may be closer to 8,000-10,000 tokens for a SKILL.md that retains enough context for the agent to route correctly and load the right references. This tension is unresolved in both reviews.

### 3. Where the Dispute-Parsing Subsystem belongs

agentskills-specialist recommends extracting the Dispute-Parsing Subsystem to `references/dispute-parsing.md` (Recommendation 3), noting its stable interface and use by three handlers. My review identifies that the structural markers used by the dispute parser (`<!-- CONVERSUS:DISPUTES_BEGIN/END -->`) are also template contribution rules that belong in `templates/AGENTS.md` (my Recommendation 1). The subsystem thus has dual citizenship: its interface contract is execution logic (SKILL.md/references territory) and its structural markers are contribution conventions (AGENTS.md territory). Neither review addresses how to keep these two representations synchronized.

### 4. The role of the existing `schema/` directory

agentskills-specialist notes that "template variable contracts are already externalized" in `schema/variables.yml` (Alignment point 4) but still recommends creating a separate `references/template-variables.md` for prose explanation (Recommendation 4). My review recommends a `schema/AGENTS.md` to explain the schema contribution workflow (Recommendation 3). These are three representations of the same domain: `schema/variables.yml` (machine-readable), `references/template-variables.md` (prose for the runtime agent), and `schema/AGENTS.md` (contribution guide for editing agents). The relationship between these three needs explicit definition, or they will drift. agentskills-specialist partially addresses this ("can complement the existing `schema/variables.yml`") but does not define which is authoritative when they conflict.

### 5. Urgency of cross-agent compatibility

My review argues that nested AGENTS.md files are high-value because they surface contribution rules to agents that cannot read SKILL.md (Missed Opportunity 2: "an agent editing a preset in Cursor or Copilot has no way to discover these constraints"). agentskills-specialist's review does not consider this scenario at all. The tension is about priority: agentskills-specialist treats SKILL.md token reduction as the primary deliverable; my review treats cross-agent discoverability as equally important. In practice, conversus is currently a Claude Code skill with no evidence of contributions from other agents. My own Off-Base Assumption 2 acknowledges this ("the audience is narrower than implied"). The tension is genuine but the urgency depends on the project's contributor base, which neither review empirically assesses.

## Safe Agreements

### 1. The SKILL.md is too large and must be decomposed

Both reviews agree without reservation that 2216 lines / 31k tokens is far beyond sustainable. agentskills-specialist frames this as a violation of the agentskills.io specification's 500-line / 5,000-token recommendation. My review frames it as an obstacle to both execution efficiency and contribution discoverability. The diagnosis is shared; only the decomposition strategy differs. Both reviews cite the same evidence: the agent pays full context cost regardless of which subcommand is invoked, and subcommand handlers are largely independent.

### 2. The existing infrastructure supports decomposition without new capabilities

agentskills-specialist's Off-Base Assumption 1 states: "the agent is already doing file I/O on every run. Adding `references/handler-run.md` to the read list is not a new capability -- it is a refinement of existing behavior." My review makes the parallel observation that the `references/` directory already exists with substantial content and the `schema/` directory demonstrates the project understands contract externalization (agentskills-specialist Alignment point 4, my Alignment point 1). Both reviews agree that no new tooling, directory structure, or agent capabilities are needed -- the decomposition uses existing infrastructure.

### 3. Execution logic must not migrate to contribution-oriented formats

My review explicitly states: "Do not move execution logic from SKILL.md to AGENTS.md" (Recommendation 6). agentskills-specialist implicitly agrees by never proposing AGENTS.md as a target for any execution content -- the entire extraction goes to `references/` files and `assets/`, all within the agentskills.io ecosystem. Both reviews preserve the boundary between executable specification (SKILL.md + references) and contribution guidance (AGENTS.md), even though they disagree on how much attention the contribution side deserves.

### 4. The subcommand dispatch table is well-designed and should remain in the always-loaded core

agentskills-specialist praises the dispatch table as "an exemplary implementation of the 'provide defaults, not menus' pattern" (Alignment point 2). My review does not analyze the dispatch table's design but implicitly preserves it by never proposing to move it. Both reviews agree it belongs in the always-loaded SKILL.md core, serving as the routing layer that determines which reference files to load.

## Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus/specs/011a-skill-breakdown/conversus-output/agentskills-specialist/review.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/011a-skill-breakdown/conversus-output/agents-md-specialist/review.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/SKILL.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/011a-skill-breakdown/spec.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/references/agents-md.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/AGENTS.md`
