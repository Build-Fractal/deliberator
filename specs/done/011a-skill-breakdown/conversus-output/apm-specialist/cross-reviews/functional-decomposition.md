# Cross-Review of functional-decomposition's Review

Reviewer: **apm-specialist**
Target: functional-decomposition's Phase 1 review of spec 011a (conversus SKILL.md breakdown)

---

## Dangerous Contradictions

### 1. Per-subcommand reference files vs. sub-skill promotion — two incompatible deployment models

functional-decomposition recommends extracting each subcommand handler into its own `references/` file within the conversus skill directory (Rec 1, 2), relying on conditional load instructions in SKILL.md to tell the agent when to read each file. My review (apm-specialist Rec 1) recommends creating `.apm/skills/` sub-skills that APM promotes to independent top-level entries under `.github/skills/`, `.claude/skills/`, etc.

These are mutually exclusive structural choices. The `references/` model keeps everything inside one skill directory — the agent loads the root SKILL.md and then conditionally reads sibling files. The sub-skill model creates independent skill directories that agent runtimes discover separately — each sub-skill has its own SKILL.md and its own activation boundary. You cannot have both: a `references/gate-handler.md` inside `conversus/` and a standalone `.github/skills/conversus-gate/SKILL.md` would create duplicate specifications. If a future contributor follows one model while the other is partially implemented, the skill system diverges into two conflicting sources of truth.

The danger is real because both reviews present their approach as the obvious decomposition strategy without acknowledging the alternative. functional-decomposition cites `agentskills-spec.md` L379-387 (keep SKILL.md under 500 lines, use references/) while I cite APM's sub-skill promotion docs (skills guide, "Sub-skill Promotion" section). Both are correct about their respective systems, but they solve the same problem with incompatible file layouts. A decision must be made: either conversus decomposes via agentskills `references/` (staying within the single-skill model) or via APM `.apm/skills/` (becoming a multi-skill package). Attempting both will produce a maintenance nightmare.

### 2. Conditional load instructions assume reliable agent compliance — APM sub-skills enforce it structurally

functional-decomposition's entire decomposition strategy depends on conditional load triggers: "When `/conversus gate` is invoked, read `references/gate-handler.md`" (Rec 1), "If config `rounds` > 1, read `references/multi-round-orchestration.md`" (Rec 4). The agent must parse these instructions from the root SKILL.md and then decide to load additional files. My review notes that APM sub-skill promotion creates structurally separate skill directories that agent runtimes discover independently — no conditional loading required.

The contradiction is about trust in the agent runtime. functional-decomposition acknowledges the risk ("Without explicit triggers, agents may either load all reference files eagerly or fail to load necessary references," Rec 8) but treats well-written triggers as sufficient mitigation. My review implicitly assumes that structural separation is more reliable than instructional separation. Neither review provides empirical evidence for their position. However, the agentskills best practices document that functional-decomposition cites is a specification for agent behavior, not a guarantee of agent compliance. If the agent ignores a conditional load instruction — which is a known failure mode for long SKILL.md files where instructions compete for attention — the extracted handler simply does not execute. With APM sub-skills, the agent runtime loads the relevant skill directory at activation time based on the invocation command, making the loading mechanism structural rather than advisory.

This is dangerous because it determines whether the decomposition actually reduces context load in practice. If agents eagerly load all `references/` files (the pessimistic case functional-decomposition warns about), the decomposition achieves zero context reduction despite the structural work. The choice between advisory and structural loading is the single most consequential architectural decision in this spec.

### 3. "Retain the run engine core in SKILL.md" vs. "Create a conversus-engine sub-skill"

functional-decomposition recommends keeping ~265 lines of run engine core in SKILL.md after extraction (Rec 7), arguing that over-extraction would force `/conversus run` to load 3-4 reference files. My review (apm-specialist Rec 1) recommends creating a `conversus-engine` sub-skill containing the run command, template system, dispute parsing, and multi-round execution as one unit.

The disagreement is about what constitutes "always needed" context. functional-decomposition treats the run engine as the gravitational center that all other subcommands orbit — converge and gate delegate to it, so it must always be loaded. My review groups the engine with its dependencies (templates, dispute parsing, multi-round) into a single sub-skill that loads as a unit when any run-dependent command activates. functional-decomposition's model results in a ~345-line root SKILL.md with conditional references; my model results in a ~100-150 line root SKILL.md (dispatch table + dependency graph) with a ~600-800 line engine sub-skill.

The danger is that functional-decomposition's retained core (~265 lines) plus the dispatch table, shared notes, and the conditional load instructions for 6+ reference files may still exceed the 500-line budget once the load triggers, interface contracts, and cross-reference documentation are added. The "retain in SKILL.md" approach creates pressure to keep adding "just one more section" to the root file because it is "always needed." My model has the opposite risk: the engine sub-skill could grow unchecked because it is "only loaded when needed." Both approaches need a governance mechanism — functional-decomposition proposes a token budget document (Rec 9), while my review defers governance to APM's version management. Neither governance mechanism is currently implemented.

---

## Tensions

### 1. Token budget analysis vs. structural packaging — different optimization targets

functional-decomposition frames the problem as conditional relevance: the ratio of relevant tokens to loaded tokens per subcommand (Off-Base Assumptions, third point). This drives a fine-grained decomposition where even 75-line blocks (preset resolution, Rec 5) and 30-line blocks (dispute parsing, Rec 3) warrant extraction. My review frames the problem as distribution boundaries: what is a coherent unit that can be independently versioned, deployed, and loaded by an agent runtime?

These are not contradictory but they produce different decomposition granularity. functional-decomposition's analysis yields 8+ reference files optimized for minimal per-invocation token load. My analysis yields 3 sub-skills optimized for packaging coherence. The tension is between context efficiency (functional-decomposition's metric) and maintenance burden (my metric). Eight reference files with conditional load triggers require eight correct trigger conditions that must be maintained as the SKILL.md evolves. Three sub-skills require three SKILL.md files that must be kept internally consistent. The right granularity depends on how frequently conversus's specification changes — in active spec development (011a and counting), fewer larger units are easier to maintain; in a stable system, finer granularity provides better context efficiency.

### 2. The `references/` directory already exists with five files — but neither review addresses migration

functional-decomposition notes that "The agentskills `references/` directory is already part of the conversus skill structure (it exists at `conversus/references/` with five files)" (Off-Base Assumptions, second point). My review notes that "no `.apm/skills/` directory has been created yet" (Missed Opportunities, first point). Both identify the gap between current state and proposed state, but neither addresses the migration path for the five existing reference files.

If functional-decomposition's approach is adopted, the existing `references/` files (agentskills-best-practices.md, agentskills-spec.md, and others) must coexist with new handler-specific reference files (gate-handler.md, handler-define.md, etc.). The naming conventions and load trigger patterns for existing files may conflict with the new extraction pattern. If my approach is adopted, the existing `references/` directory stays within the root skill while sub-skills get their own `references/` directories. Neither review proposes a concrete migration plan that accounts for the existing content.

### 3. Dispute-Parsing Subsystem: shared reference file vs. APM context primitive

functional-decomposition recommends extracting the Dispute-Parsing Subsystem to `references/dispute-parsing.md` (Rec 3), loaded on demand by its four consumers. My review recommends extracting it to `.apm/context/dispute-parsing.context.md` (Rec 4), making it an APM context primitive discoverable through APM's context linking system.

Both achieve the same immediate goal — separating the subsystem from the run engine — but they have different downstream implications. A `references/` file is skill-internal: only agents that have loaded the conversus skill can access it. An APM context primitive is project-scoped: any primitive in the project can link to it, and APM's compilation system can include it in AGENTS.md. If other skills or instructions in the monorepo ever need to understand conversus's dispute-parsing contract (e.g., a CI/CD skill that interprets gate results), the context primitive model makes it accessible without loading the full conversus skill. functional-decomposition's model is simpler and self-contained; my model is more extensible but adds APM-specific coupling.

### 4. Validation consolidation: structural extraction vs. scripted enforcement

functional-decomposition identifies duplicated validation logic across five handlers and recommends a `references/validation-contract.md` (Rec 6) that defines the shared algorithm once. My review recommends a PostToolUse hook running `linter/validate.py` (Rec 6) to enforce validation automatically.

These address different layers of the same problem. functional-decomposition's approach reduces specification duplication — agents read one validation contract instead of five handler-specific validation blocks. My approach automates enforcement — the linter runs automatically after template writes, catching violations without relying on the agent to read and follow validation instructions. The tension is that specification consolidation (functional-decomposition) and automated enforcement (apm-specialist) are complementary but the reviews present them as alternative solutions. The strongest outcome would combine both: consolidate the validation specification into a single reference and automate enforcement via a hook.

### 5. Timing of decomposition — now vs. after spec stabilization

functional-decomposition presents all recommendations as immediately actionable, with P1 items (gate extraction, guided handler extraction, dispute-parsing extraction) framed as current blockers. My review (Rec 8) explicitly recommends deferring full APM distribution "until spec suite stabilizes," noting that "every SKILL.md structural change during this phase would require version bumps."

This tension is about the cost of premature structure. functional-decomposition's reference-file approach has lower restructuring cost (moving sections between markdown files) than my sub-skill approach (creating new directories, SKILL.md files, and maintaining APM manifest metadata). However, even functional-decomposition's approach has a maintenance cost: every new spec that modifies a subcommand handler requires updating both the reference file and the load trigger in the root SKILL.md. The question is whether the context-reduction benefits outweigh the maintenance drag during active development. functional-decomposition implicitly assumes yes; my review explicitly argues for structural preparation now with distribution later.

---

## Safe Agreements

### 1. The gate handler is the strongest extraction candidate

functional-decomposition identifies the gate handler (L1881-2178, ~300 lines) as "the most self-contained handler" and the highest-priority extraction target (Rec 1). My review identifies it as "architecturally independent" with "a clean extraction boundary" (Alignment, third point) and includes it as part of the first recommendation (conversus-gate sub-skill). Both reviews agree on the reasoning: the gate handler has no interactive prompts, no shared state beyond the Dispute-Parsing Subsystem and run engine delegation, and is invoked only for `/conversus gate` — a CI/CD-focused command that most interactive users never trigger. Regardless of whether the extraction uses `references/` or `.apm/skills/`, the gate handler should be the first piece extracted.

### 2. The current monolithic structure imposes unacceptable context cost

functional-decomposition quantifies the problem as "every `/conversus define` invocation loads 31k tokens but uses ~2k" (Off-Base Assumptions, third point) and calculates 60-75% context reduction from extraction (Executive Summary). My review frames it as exceeding "any reasonable context window budget for a single skill" (Alignment, first point). Both reviews agree that the status quo is not viable: 2200+ lines in a single SKILL.md degrades agent performance on every invocation regardless of which subcommand is called. The agentskills spec recommends under 500 lines / 5,000 tokens; the current file is 4.4x the line budget and ~6x the token budget. Neither review defends the monolithic structure, and both provide concrete paths to reduce per-invocation context load. The disagreement is about mechanism (references vs. sub-skills), not about whether decomposition is necessary.

### 3. The Dispute-Parsing Subsystem must be extracted as a standalone, referenceable unit

functional-decomposition recommends `references/dispute-parsing.md` (Rec 3). My review recommends `.apm/context/dispute-parsing.context.md` (Rec 4). The destination differs but the rationale is identical: the subsystem is a pure function with a stable interface contract, used by four consumers across different subcommands, and currently buried in the run engine section where consumers in other handlers must navigate past unrelated orchestration logic to find it. Both reviews cite the subsystem's own self-declaration as a "stable interface" as evidence that it was designed for extraction. The physical form (reference file vs. context primitive) is a detail subordinate to the shared conviction that this cross-cutting concern must be independently addressable.
