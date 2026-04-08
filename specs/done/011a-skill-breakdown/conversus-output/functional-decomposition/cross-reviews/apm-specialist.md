# Cross-Review of apm-specialist — by functional-decomposition

## Dangerous Contradictions

### 1. Sub-skill promotion vs. conditional reference loading — incompatible context reduction mechanisms

apm-specialist's central recommendation is to split SKILL.md into three APM sub-skills (`conversus-engine`, `conversus-wizard`, `conversus-gate`) deployed independently to `.github/skills/` via APM's sub-skill promotion (apm-specialist Rec #1). My review recommends extracting subcommand handlers into `references/` files with conditional load triggers (functional-decomposition Recs #1, #2, #8).

These are mutually exclusive strategies. APM sub-skill promotion copies each sub-skill as a whole file to `.github/skills/{name}/SKILL.md`. The agent runtime then loads the *entire* sub-skill when it activates. This means `conversus-engine` (estimated 400-800 lines per apm-specialist) loads fully on every `/conversus run` invocation — including multi-round orchestration, preset resolution, and arbitration logic that may not apply to the current config. The `references/` approach achieves finer-grained conditional loading: the agent reads only `references/multi-round-orchestration.md` when `rounds > 1`, only `references/preset-resolution.md` when presets are configured, etc.

The danger: if the team implements APM sub-skills as the primary decomposition, they forfeit the conditional loading benefits within each sub-skill. The `conversus-engine` sub-skill becomes a ~600-line file that still violates the 500-line / 5,000-token recommendation from the agentskills spec (agentskills-best-practices.md, L154-156). apm-specialist acknowledges this indirectly ("reducing per-invocation context load from 2200 lines to ~400-800 per sub-skill") but does not address that 800 lines is still 60% over the recommended maximum. My review's `references/`-based approach achieves ~345 lines for the always-loaded core (functional-decomposition Rec #7), with additional content loaded conditionally.

**Resolution needed**: Either the `references/` pattern must be applied *within* each APM sub-skill (making them complementary rather than alternative strategies), or one approach must be chosen as primary. The reviews do not acknowledge this tension.

### 2. Context files (`.apm/context/`) vs. reference files (`references/`) — competing homes for the same content

apm-specialist recommends moving mode specifications into `.apm/context/modes/cooperative.context.md` (Rec #2), the Dispute-Parsing Subsystem into `.apm/context/dispute-parsing.context.md` (Rec #4), the antipattern catalog into `.apm/context/antipatterns.context.md` (Rec #5), and schema files into `.apm/context/template-schema.context.md` (Rec #7). My review recommends extracting these same logical units into `references/` files: `references/dispute-parsing.md` (Rec #3), `references/multi-round-orchestration.md` (Rec #4), `references/validation-contract.md` (Rec #6).

The danger is a split-brain outcome. APM context files (`.apm/context/`) are processed by APM's compilation system and distributed via `applyTo` targeting. The agentskills `references/` directory is loaded on demand by the agent runtime via explicit triggers in SKILL.md. If the Dispute-Parsing Subsystem lives in `.apm/context/`, its loading is governed by APM's context optimizer. If it lives in `references/`, its loading is governed by the SKILL.md's explicit trigger instructions. These are different load-time behaviors with different guarantees. Placing the same content in both creates drift. Choosing one without acknowledging the other leaves a gap.

The reviews never directly address which mechanism should own shared subsystem content. apm-specialist assumes APM context linking; my review assumes agentskills `references/` loading. Both cannot be canonical for the same content.

### 3. "Defer full APM distribution" vs. "Create `.apm/skills/` directory immediately" — contradictory urgency signals

apm-specialist's Rec #8 says to "defer full APM distribution until spec suite stabilizes," citing the active evolution of the spec suite (011a is current) and the maintenance drag of version bumps. Yet Rec #1 says to "create `.apm/skills/` directory with three sub-skills immediately." These send contradictory signals about implementation timing.

Creating `.apm/skills/` is not a zero-cost structural change as claimed. It introduces APM's sub-skill promotion machinery, which requires the sub-skills to conform to APM's SKILL.md format, triggers deployment to `.github/skills/`, `.claude/skills/`, and `.cursor/skills/` on `apm install`, and means that subsequent SKILL.md structural changes during the active spec development phase (specs 012-020 are queued per the git log) will require updating the sub-skill boundaries. My review's `references/` approach (functional-decomposition Recs #1-6) is genuinely zero-cost — it requires no tooling integration, no manifest changes, and no deployment machinery. It is pure content reorganization within the existing skill structure.

The danger: if "immediately" is taken literally for Rec #1 while "defer" is applied to Rec #8, the team gets the worst of both worlds — APM structural overhead during active spec evolution, without the distribution benefits that justify that overhead.

### 4. Presets as APM sub-skill vs. presets as self-contained resolution function

apm-specialist recommends registering the presets directory as a sub-skill (`.apm/skills/conversus-presets/SKILL.md`, Rec #3) while correctly noting in the Off-Base section that "extracting presets as fully independent APM packages is premature." My review identifies preset resolution as a pure function (functional-decomposition, Alignment section) and recommends extracting it to `references/preset-resolution.md` (Rec #5) loaded conditionally when any agent uses `preset:`.

The contradiction: apm-specialist's sub-skill approach means presets get their own SKILL.md deployed to `.github/skills/conversus-presets/`. This SKILL.md would need to document the preset schema, resolution rules, composition templates, and available presets — essentially becoming an always-loaded specification for a feature that many conversus configs do not use (my review notes "many conversus configs use inline prompts with no presets"). The `references/` approach loads preset resolution only when presets are actually configured, paying zero context cost otherwise.

Making presets a sub-skill also creates an activation question: what triggers the `conversus-presets` skill? It has no subcommand of its own. It is a dependency of `conversus-engine`, `conversus-gate`, and `conversus-wizard` (for mode handler preset matching). This is a support library, not an independently activatable skill. APM's sub-skill model is designed for units that activate independently, not for shared utilities consumed by other sub-skills.

## Tensions

### 1. APM's compilation benefits vs. agentskills' runtime loading model

apm-specialist identifies several APM compilation benefits: `applyTo` targeting for mode-specific instructions (Missed Opportunities #6), context optimization across consuming projects (Alignment #5), and lifecycle hooks for template validation (Missed Opportunities #9). My review operates entirely within the agentskills runtime model: `references/` files loaded on demand, conditional triggers in SKILL.md, progressive disclosure via explicit instructions.

These are not contradictory — a skill can use both APM packaging and agentskills `references/` conventions. But they represent different optimization targets. APM compilation optimizes for *install-time* placement: which content goes where in the project tree. Agentskills `references/` optimizes for *invocation-time* loading: which content enters the context window for a given task. Both matter, but for the immediate problem (SKILL.md is too large for effective agent processing), invocation-time optimization has a more direct impact. apm-specialist's install-time optimizations are valuable for multi-consumer scenarios but do not reduce per-invocation context load within a single consuming project.

This tension does not need resolution — both can coexist. But the reviews should be explicit about which optimization target each recommendation serves.

### 2. Three sub-skills vs. seven+ reference files — granularity mismatch

apm-specialist proposes three sub-skills: `conversus-engine`, `conversus-wizard`, `conversus-gate`. My review proposes seven or more reference files: `gate-handler.md`, `handler-define.md`, `handler-interests.md`, `handler-mode.md`, `handler-converge.md`, `handler-arbitrate.md`, `dispute-parsing.md`, `multi-round-orchestration.md`, `preset-resolution.md`, `validation-contract.md`.

The tension: apm-specialist's three-unit split groups five guided handlers into a single `conversus-wizard` sub-skill. This means `/conversus define` loads the entire wizard sub-skill — including the mode handler, converge handler, and arbitrate handler — even though it needs only the define handler. My review treats each handler as independently loadable. The wizard sub-skill would be approximately 1100 lines (functional-decomposition Rec #2 estimates), which is 2.2x the recommended maximum.

apm-specialist's grouping is motivated by a valid concern: "the guided workflow (define/interests/mode/converge/arbitrate) is a coherent unit" (Alignment #4). These commands do form a linear prerequisite chain. But "coherent unit" in the domain model does not mean "should share a context window." A user running `/conversus define` is at the beginning of the chain and does not need the converge or arbitrate specifications.

### 3. PostToolUse hook for template validation vs. existing linter instruction

apm-specialist recommends adding a PostToolUse hook (`.apm/hooks/template-validation.json`) to automatically run `linter/validate.py` when template files are modified (Rec #6). My review does not address the linter at all — it focuses on decomposing the SKILL.md content, not on the supporting toolchain.

The tension: the current SKILL.md already instructs agents to "run `uv run python linter/validate.py`" after template modifications. Adding an APM hook automates this, which is an improvement. But it also introduces a dependency on APM's hook infrastructure being deployed and functional in the consuming project. If APM hooks fail silently or are not installed, the validation guard disappears without warning. The current explicit instruction in SKILL.md is less elegant but more robust — the agent reads it and executes it regardless of hook infrastructure.

This is a classic automation-vs-explicitness tension. Both approaches are defensible, but the tradeoff should be acknowledged.

### 4. Version pinning between SKILL.md and templates vs. structural co-location

apm-specialist identifies the lack of version pinning between SKILL.md and templates as a missed opportunity (Missed Opportunities #7), suggesting APM's version management could enforce the template variable contract. My review implicitly addresses this through the validation contract reference (Rec #6), which centralizes the shared heading check algorithm and name pattern regex.

The tension: version pinning is a distribution concern (ensuring consumers get compatible SKILL.md and templates). Structural co-location is a decomposition concern (ensuring the variable contract is defined in one place and referenced by all consumers). For a single-project framework (which both reviews acknowledge conversus currently is), version pinning adds ceremony without benefit — there is only one "consumer" and it always uses HEAD. The structural co-location approach provides the same correctness guarantee (single source of truth for the contract) without the versioning overhead.

### 5. "Overhead calculus" framing vs. "conditional relevance" framing

apm-specialist frames the core decision as an overhead calculus: "APM packaging adds `apm.yml` manifests, version management, dependency resolution... That machinery pays for itself when multiple consumers exist" (Executive Summary). My review frames it as conditional relevance: "how much of the loaded content applies to the agent's current task" (Off-Base #3).

These framings lead to different urgency assessments. Under the overhead calculus, most structural changes should wait until a second consumer appears. Under the conditional relevance framing, decomposition is urgent now because every invocation wastes 80%+ of its context budget on irrelevant content. Both framings are valid, but they produce different implementation timelines.

## Safe Agreements

### 1. The gate handler is the strongest extraction candidate

Both reviews identify the gate handler as architecturally independent and the highest-priority extraction target. apm-specialist: "Gate reads a `gates.yml`, generates a standard `conversus.yml`, delegates to the run engine, and produces a machine-readable `gate-result.md`. Its only dependency on the rest of SKILL.md is the run engine and the Dispute-Parsing Subsystem. This is a clean extraction boundary" (Alignment #3). My review: "The gate handler (L1881-2178, ~300 lines) is entirely self-contained... It is the strongest candidate for full extraction" (Missed Opportunities #8, Rec #1).

The reviews differ on *where* to extract it (APM sub-skill vs. `references/` file) but agree unanimously that it should be extracted first and that the boundary is clean.

### 2. The Dispute-Parsing Subsystem has a stable, cross-cutting interface that warrants standalone specification

Both reviews identify the Dispute-Parsing Subsystem as a stable interface used by multiple consumers. apm-specialist: "It has defined inputs (synthesis file path), outputs (boolean + integer), parsing rules (structural markers, heading fallback, defaults), and a stable interface contract. This is a reusable component that any conversus consumer or extension needs" (Missed Opportunities #4). My review: "The subsystem declares explicit inputs, outputs, parsing rules in priority order, and a stable interface contract. This is a pure function with a well-defined contract — exactly the kind of unit that composes well across callers" (Alignment #2).

Both agree it should be extracted from its inline position in the run engine section. The destination differs (`.apm/context/` vs. `references/`) but the diagnosis and boundary are shared.

### 3. The current monolithic SKILL.md is unambiguously too large and decomposition is warranted

Both reviews agree without qualification that 2200+ lines / 31k tokens in a single SKILL.md exceeds any reasonable context budget. apm-specialist: "At 119KB / 2200+ lines, this exceeds any reasonable context window budget for a single skill" (Alignment #1). My review: "The current SKILL.md violates the Single Responsibility Principle at every level: the file is simultaneously a dispatch table, an execution engine, a validation framework, an interactive UX guide, and a reference manual for output schemas" (Executive Summary).

There is no disagreement that decomposition is needed, only about the mechanism and granularity. This shared diagnosis means the team can proceed with confidence that the direction is correct, even while the implementation strategy is debated.

### 4. Premature full-package distribution should be avoided

Both reviews explicitly caution against distributing conversus as an independent APM package at this stage. apm-specialist: "Defer full APM distribution (separate `apm install conversus` package) until spec suite stabilizes" (Rec #8). My review: "The spec assumes decomposition requires code or scripting changes... the most impactful decomposition requires no tooling changes — it is purely structural" (Off-Base #2).

Both reviews converge on the principle that internal structural reorganization should precede external distribution, and that the active spec development phase (specs 012-020 queued) makes distribution overhead premature. The disagreement is about how much APM infrastructure to adopt internally (sub-skills and context primitives vs. plain `references/` files), not about whether to publish.
