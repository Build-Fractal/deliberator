# Revision — agentskills-specialist (Iteration 1)

## Recommendation Dispositions

### Recommendation 1: Extract each subcommand handler to its own reference file
**Status: REVISED**

Original: Extract all seven subcommand handlers including the run handler to `references/handler-*.md`, leaving only the dispatch table, invariants, phase-level summary, and gotchas in SKILL.md.

Revised: Extract six subcommand handlers (define, interests, mode, converge, arbitrate, gate) to `references/handler-*.md`. **Do not extract the run engine core.** The run engine's single-round phase loop (Phases 1-5, output path computation, agent dispatch mechanics, termination conditions) remains in SKILL.md.

Three cross-reviews converged on this point with compelling arguments I now accept. functional-decomposition (DC-2) demonstrated that extracting the run engine creates a two-hop reference chain where `/conversus converge` requires loading SKILL.md, then `handler-converge.md`, then `handler-run.md` -- a progressive-disclosure chain depth of 2 that the agentskills specification cautions against. integration-specialist (DC-1) identified that the run engine is not a peer handler but a shared runtime that `converge` and `gate` both delegate into, making it architecturally distinct from the self-contained guided handlers. apm-specialist (DC-2) correctly noted that my 350-line / 5,000-token target is incompatible with retaining the engine.

I was wrong to treat the run engine as just another handler. The six guided handlers and gate have clean entry/exit interfaces (file inputs, file outputs, no shared in-memory state). The run engine is a state machine that converge and gate compose, not call. Extracting it forces every execution path through two reference reads, and if the agent fails to follow the chain, it attempts multi-phase orchestration with only a one-paragraph summary -- a high-fragility silent failure mode.

The revised handler extraction still removes approximately 1,400 lines from SKILL.md (six handlers instead of seven), which is the majority of the savings. The run engine core adds approximately 235 lines to the always-loaded SKILL.md body.

### Recommendation 2: Define the always-loaded SKILL.md core content
**Status: REVISED**

Original: Target 300-400 lines / under 5,000 tokens. Keep frontmatter, dispatch table, multi-agent rules, one-paragraph-per-phase summary, and gotchas.

Revised: Target 450-550 lines / 6,000-8,000 tokens. Keep: (a) frontmatter, (b) dispatch table with file references for the six extracted handlers, (c) non-negotiable multi-agent rules, (d) the single-round run engine core (phase loop, output path computation, agent dispatch mechanics, template filling flow), (e) operational gotchas that constrain config interpretation, (f) conditional loading triggers for subsystem references.

I concede the 5,000-token target. functional-decomposition (DC-4) correctly distinguished between the SKILL.md body budget and the per-invocation total budget. integration-specialist (DC-2) demonstrated the arithmetic: the run engine core alone is ~235 lines at ~14 tokens/line (~3,300 tokens), and combined with dispatch, multi-agent rules, and gotchas, the root SKILL.md reaches 6,000-8,000 tokens. The 5,000-token recommendation in the agentskills specification is a guideline for typical skills. Conversus is not a typical skill -- it is an orchestration engine that dispatches multi-agent deliberations. A 6,000-8,000 token core that never requires two-hop reference chains is better than a 5,000-token core that creates fragile loading dependencies.

The specification says "under 500 lines and 5,000 tokens" as recommendations, not hard ceilings. Exceeding the token recommendation by 20-60% while reducing it from 31,000 tokens (the current state) by 75-80% is a massive improvement that preserves execution safety. The alternative -- hitting 5,000 tokens by summarizing the run engine to one paragraph per phase -- creates the silent degradation failure mode that functional-decomposition identified.

### Recommendation 3: Extract the Dispute-Parsing Subsystem to `references/dispute-parsing.md`
**Status: MAINTAINED**

All four cross-reviews agree this is a natural extraction candidate. The stable interface contract, three-handler dependency, and ~30 lines of specification make this the lowest-risk subsystem extraction. agents-md-specialist raised a valid point that the structural markers (`<!-- CONVERSUS:DISPUTES_BEGIN/END -->`) have dual citizenship as both execution logic and contribution conventions. The resolution: the authoritative interface definition lives in `references/dispute-parsing.md` (execution), and any AGENTS.md mention of the markers points to that file as the canonical source. No duplication of the contract itself.

integration-specialist's naming suggestion of `subsystem-dispute-parsing.md` is a tension I considered but reject. The agentskills specification does not define file-type prefixes for references. Adding a taxonomy (`handler-`, `subsystem-`, `contract-`) imposes classification overhead that may not scale. The file name `dispute-parsing.md` is self-explanatory. The load trigger in SKILL.md provides all the context the agent needs about the file's role.

### Recommendation 4: Extract template variable contracts to `references/template-variables.md`
**Status: REVISED**

Original: Consolidate all phase-specific variable definitions, path-list formatting rules, round-aware path variables, and variable expansion rules into a single reference file.

Revised: Keep per-phase variable lists inline in the run engine core (they are part of the phase execution specification the agent needs during each phase). Extract only the cross-cutting variable expansion rules, path-list formatting rules, and the variable resolution algorithm to `references/template-variables.md`. Load trigger: "Before filling the first template in any phase, read `references/template-variables.md` for the variable resolution algorithm."

integration-specialist (DC-3) correctly identified that full extraction forces the agent into a three-file dance during each phase: read template, read template-variables reference, then fill. The per-phase variable lists are execution context, not reference material -- the agent needs to know which variables are available *while executing that phase*, not as a separate lookup. The cross-cutting rules (how variables expand, what `{PATH_LIST:...}` means, how round-aware paths work) are genuine reference material that applies identically across all phases and does not need to be in context until template filling begins.

### Recommendation 5: Extract validation rules to `references/validation-rules.md`
**Status: REVISED**

Original: Consolidate all validation patterns (agent name regex, heading validation, path checks, post-write validation) into one reference file.

Revised: Consolidate only the shared validation patterns that appear in three or more handlers into `references/validation-rules.md`. Handler-specific validation (e.g., gate-result.md schema validation) stays in its handler reference file. The shared reference file contains: agent name regex, heading validation rules (case-insensitive matching), path existence check patterns, and the standard error message format.

functional-decomposition raised a valid concern about whether this file loads eagerly or on demand. The load trigger is embedded in each handler reference file, not in the root SKILL.md: "Apply the standard validation rules from `references/validation-rules.md`." This ensures the file loads only when a handler activates, not on every SKILL.md activation. agents-md-specialist (DC-2) warned that fine-grained extraction risks requiring the run handler to load seven reference files. By limiting this file to genuinely shared patterns (those appearing in 3+ handlers), the cross-reference overhead is justified by the deduplication.

### Recommendation 6: Move output schema templates to `assets/`
**Status: WITHDRAWN**

functional-decomposition (DC-3) persuaded me. The conversus output schemas (problem.md, interests.md, gate-result.md) are not reusable fill-in-the-blank templates -- they are structural contracts with required headings and validation rules tightly coupled to their handler specifications. Separating the schema from the handler that produces it and the validation rules that check it creates a drift seam. Each schema should stay co-located with its handler in the handler's reference file (`references/handler-define.md` contains the problem.md schema, `references/handler-gate.md` contains the gate-result.md schema). This keeps each handler self-contained: one file load gives the agent everything it needs for that subcommand.

The agentskills best practices quote about `assets/` applies to templates the agent fills with variable content and reuses across invocations. The conversus output schemas are per-handler contracts, not reusable templates. The distinction matters.

### Recommendation 7: Move preset resolution to `references/preset-resolution.md`
**Status: MAINTAINED**

apm-specialist's cross-review (DC-3) actually reinforced this recommendation by conceding that the agentskills framing is more accurate: "Presets are YAML data files with a resolution algorithm, not agent instructions. [...] The agentskills approach (conditional reference loading) matches the nature of the content." The load trigger remains: "If any agent entry contains a `preset` field, read `references/preset-resolution.md` for resolution rules."

agents-md-specialist raised the question of whether preset validation rules are contribution guidance or execution logic. They are execution logic -- the run engine enforces `composable: false`, the 3-preset composition limit, and name-filename matching at config parsing time. The destination is the reference file, not AGENTS.md. If a contributing agent editing preset YAML files needs to know the schema, a brief pointer in `presets/AGENTS.md` (if one is created) should reference `references/preset-resolution.md` as the canonical source rather than duplicating the rules.

### Recommendation 8: Restructure the "Important Notes" section
**Status: REVISED**

Original: Keep 3-5 genuine gotchas in SKILL.md. Move agent count formulas, worked examples, round/iteration orthogonality, and baseline feature inventory to `references/operational-notes.md`.

Revised: Classify each item individually per functional-decomposition's resolution proposal (DC-1).

**Stays in SKILL.md (config-interpretation constraints):**
- Rounds and iterations are orthogonal (constrains config parsing)
- All subagents use the orchestrator's model (constrains agent dispatch)
- Re-running overwrites previous output (constrains user expectations)
- Use `run_in_background: true` for Phases 1-4 (constrains dispatch mechanics)

**Stays in SKILL.md (canonical execution formula):**
- Agent count formulas (`N^2 + 2N + 1` without arbiter, `N^2 + 2N + 2` with arbiter). agents-md-specialist (DC-3) made a persuasive argument I now accept: these formulas serve a runtime safety function in the pre-execution estimate. An agent that derives `N^2 + N + 1` instead of `N^2 + 2N + 1` (a plausible off-by-one for the dispute phase count) produces a silently incorrect user-facing estimate. The formulas are authoritative contracts, not derivable documentation. I was wrong to classify them as "what the agent already knows."

**Moves to `references/operational-notes.md`:**
- Worked examples ("For 3 agents without arbiter: 16 total agent launches") -- these are human-readable illustrations of the formulas, not execution contracts.
- Baseline feature inventory -- this is a capability listing, not an operational constraint.

### Recommendation 9: Add conditional loading instructions to each reference
**Status: REVISED**

Original: Use specific triggers like "If the config contains an `arbiter:` block, read `references/arbitration-engine.md`."

Revised: Use a two-tier trigger model.

**Tier 1 -- Subcommand-based triggers (in the dispatch table):**
- "When `/conversus define` is invoked, read `references/handler-define.md`."
- "When `/conversus gate` is invoked, read `references/handler-gate.md`."

These are unambiguous -- the dispatch table routes to exactly one handler.

**Tier 2 -- Config-based triggers (in the run engine core or handler reference files):**
- "If any agent entry contains a `preset` field, read `references/preset-resolution.md`."
- "If `rounds > 1`, read `references/multi-round-execution.md`."
- "If the config contains an `arbiter:` block, the arbitration-specific logic in Phase 6 applies."

functional-decomposition (T-5) correctly identified the sequencing problem with config-based triggers: the agent must parse the config to know which references to load, but it needs the reference material to parse the config correctly. The resolution: config-based triggers appear *after* the initial config read in the run engine's execution flow, at the point where the relevant config fields have been identified but the detailed processing has not begun. The SKILL.md run engine core includes enough context to identify `preset:` fields and `arbiter:` blocks without loading their detailed reference files. The reference files provide the detailed resolution and execution rules, not the detection logic.

### Recommendation 10: Proposed directory layout
**Status: REVISED**

```
conversus/
├── SKILL.md                          # ~500 lines: frontmatter + dispatch + run engine core + invariants + gotchas
├── references/
│   ├── handler-define.md             # Define: problem definition workflow + problem.md schema
│   ├── handler-interests.md          # Interests: interest discovery workflow + interests.md schema
│   ├── handler-mode.md               # Mode: mode selection and config generation
│   ├── handler-converge.md           # Converge: guided execution wrapper (delegates to run engine in SKILL.md)
│   ├── handler-arbitrate.md          # Arbitrate: guided arbitration workflow
│   ├── handler-gate.md               # Gate: CI/CD consensus gates + gate-result.md schema
│   ├── dispute-parsing.md            # Dispute-Parsing Subsystem (stable interface)
│   ├── template-variables.md         # Variable resolution algorithm, path-list formatting, expansion rules
│   ├── validation-rules.md           # Shared validation patterns (agent name, heading, path checks)
│   ├── preset-resolution.md          # Preset resolution, composition, and override rules
│   ├── multi-round-execution.md      # Round loop, stagnation detection, cross-round synthesis
│   ├── operational-notes.md          # Worked examples, baseline feature inventory
│   ├── agentskills-spec.md           # (existing)
│   ├── agentskills-best-practices.md # (existing)
│   ├── agentskills-quickstart.md     # (existing)
│   ├── agentskills-what.md           # (existing)
│   └── agents-md.md                  # (existing)
├── schema/                           # (existing, unchanged)
├── templates/                        # (existing, unchanged)
├── presets/                          # (existing, unchanged)
├── linter/                           # (existing, unchanged)
└── antipatterns/                     # (existing, unchanged)
```

Changes from original:
- Removed `handler-run.md` -- the run engine stays in SKILL.md.
- Removed `arbitration-engine.md` -- Phase 6 arbitration logic stays in the run engine core (it is part of the phase loop, not a separable subsystem).
- Removed three `assets/` files -- output schemas stay co-located in their handler reference files.
- SKILL.md target changed from ~350 lines to ~500 lines, from under 5,000 tokens to 6,000-8,000 tokens.
- Reference file count reduced from 14 to 11 (7 handler files reduced to 6, 3 asset files eliminated).

---

## New Recommendations

### New Recommendation A: Triage contribution-oriented content before extraction

agents-md-specialist (DC-1, DC-4) identified a dimension my original review entirely missed: some content in SKILL.md is contribution guidance, not execution specification. The antipattern check instruction (line 239), template naming conventions (line 283), and linter invocation guidance (line 309) serve agents *contributing to* conversus, not agents *executing* it. Before extracting handlers to reference files, triage each section: execution logic goes to `references/handler-*.md`; contribution guidance is noted for potential AGENTS.md coverage.

However, I reject the proposal to *move* this content to AGENTS.md. agents-md-specialist's own Recommendation 6 states "do not move execution logic from SKILL.md to AGENTS.md," and several of the identified items (preset validation rules at lines 139-145) are runtime execution logic, not contribution guidance. The correct approach: if an item serves both audiences, the authoritative version stays in the execution specification (SKILL.md or a reference file), and AGENTS.md may point to it. Never duplicate the contract.

### New Recommendation B: Expand the linter's post-decomposition role

integration-specialist (T-3) raised an important point my original review did not address: decomposition increases the surface area for drift between reference files, and the existing linter should be expanded to catch it. Specifically, after decomposition, the linter should validate:
- Template variables referenced in handler files match `schema/variables.yml`.
- Subsystem interface references (e.g., dispute-parsing input/output) are consistent across all files that reference them.
- Conditional load triggers in SKILL.md name reference files that actually exist.

This is a mechanical check, not a prose-parsing exercise. The linter already validates YAML schema consistency; extending it to check Markdown file references and variable name consistency is a natural expansion of its existing capability.

### New Recommendation C: Document per-invocation token budgets

functional-decomposition (T-1 in their cross-review) proposed documenting expected token load per invocation path. This is the right framing for post-decomposition token management. The SKILL.md should include a brief budget section:

- `/conversus define`: ~8,500 tokens (core ~7,000 + handler-define ~1,500)
- `/conversus run` (single-round, no presets, no arbiter): ~9,500 tokens (core ~7,000 + template-variables ~1,500 + dispute-parsing ~500 + validation-rules ~500)
- `/conversus run` (multi-round + arbiter + presets): ~13,000 tokens (core + template-variables + dispute-parsing + validation-rules + multi-round + preset-resolution)
- `/conversus gate`: ~10,000 tokens (core ~7,000 + handler-gate ~2,500 + dispute-parsing ~500)

These are order-of-magnitude estimates to be calibrated after decomposition. The value is making regressions visible: if a reference file grows beyond its budget, the SKILL.md budget table becomes stale and flags the issue during review. This addresses integration-specialist's concern (T-3) about specification drift without requiring a complex linting pipeline.

### New Recommendation D: Address the antipattern catalog placement

integration-specialist (DC-4) and apm-specialist (DC-4) both flagged that my review did not address the antipattern check placement. The antipattern check (SKILL.md line 239) is a pre-execution step that reads `antipatterns/catalog.md`. After decomposition, this instruction belongs in the run engine core within SKILL.md, not in any handler reference file, because it applies to every `run` and `converge` invocation before Phase 1 begins. It is an orchestrator-level concern, not a handler-level concern. The agent loading `handler-define.md` does not need the antipattern check (define does not produce deliberation output); the agent running the engine always needs it. Placing it in the run engine core ensures it cannot be skipped by an agent that bypasses a handler reference.

---

## Position Summary

The cross-reviews produced three material corrections to my original position:

**1. The run engine is not extractable.** My original recommendation treated all seven subcommands as peer handlers that could be uniformly extracted to reference files. Three reviewers (functional-decomposition, integration-specialist, apm-specialist) independently demonstrated that the run engine is architecturally distinct: it is a shared runtime that `converge` and `gate` compose, not a self-contained handler. Extracting it creates a two-hop reference chain that violates the progressive disclosure model's one-level-deep principle and introduces a high-fragility silent failure mode. I accept this correction fully. The six guided handlers and gate remain cleanly extractable; the run engine stays in SKILL.md.

**2. The 5,000-token target is not achievable without sacrificing execution safety.** My original review cited the agentskills specification's 5,000-token recommendation as though it were a hard ceiling. It is a guideline for typical skills. Retaining the run engine core pushes the SKILL.md to 6,000-8,000 tokens, but this is a 75-80% reduction from the current 31,000 tokens. The alternative -- summarizing the run engine to fit under 5,000 tokens -- creates the exact failure mode the best practices warn against: "the agent struggles to extract what's relevant." A SKILL.md that is 60% over the token guideline but requires zero multi-hop reference loads for any execution path is better than one that meets the guideline but forces three-file assembly for the most common invocation path.

**3. Agent count formulas are authoritative contracts, not derivable arithmetic.** agents-md-specialist correctly identified that the `N^2 + 2N + 1` formula serves a runtime safety function in the pre-execution user-facing estimate. A derivation error produces a silently incorrect warning before a resource-intensive run. The formula is a gotcha, not documentation. I was wrong to classify it as "what the agent already knows."

The remaining recommendations are maintained or incrementally revised to accommodate these corrections. The core decomposition strategy is unchanged: progressive disclosure via `references/` files with specific conditional loading triggers. The scope is modestly reduced (6 handler extractions instead of 7, 11 reference files instead of 14, no `assets/` directory), and the SKILL.md core is larger (500 lines / 7,000 tokens instead of 350 lines / 4,500 tokens), but the structural approach is the same.

The decomposition remains a content reorganization, not a technology migration. It uses existing infrastructure (`references/` directory, `Read` tool approval, file I/O patterns the agent already performs). It is orthogonal to and composable with agents-md-specialist's AGENTS.md recommendations and apm-specialist's APM structural recommendations. The agentskills progressive disclosure model addresses the context window problem; AGENTS.md and APM address distribution and contribution discoverability. These are complementary layers, and the progressive disclosure restructuring should proceed first because it delivers the largest impact (26,000 to 24,000 token reduction in per-invocation context) with the lowest structural commitment (reference files, not sub-skills or context primitives).

## Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus/SKILL.md`
- `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/spec.md`
- `<HOME>/code/payer-index-mono/conversus/references/agentskills-spec.md`
- `<HOME>/code/payer-index-mono/conversus/references/agentskills-best-practices.md`
- `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/conversus-output/agentskills-specialist/review.md`
- `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/conversus-output/functional-decomposition/cross-reviews/agentskills-specialist.md`
- `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/conversus-output/integration-specialist/cross-reviews/agentskills-specialist.md`
- `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/conversus-output/apm-specialist/cross-reviews/agentskills-specialist.md`
- `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/conversus-output/agents-md-specialist/cross-reviews/agentskills-specialist.md`
