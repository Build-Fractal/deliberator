# Cross-Review of apm-specialist by integration-specialist

## Dangerous Contradictions

### 1. Sub-Skill Promotion vs. Run Engine Cohesion

**apm-specialist** recommends splitting SKILL.md into three APM sub-skills (`conversus-engine`, `conversus-wizard`, `conversus-gate`) deployed independently to `.github/skills/`, `.claude/skills/`, etc. (Rec #1). **integration-specialist** identifies the run engine's phase loop, round loop, iteration loop, output path computation, and termination logic as a tightly coupled state machine that must remain a single cohesive unit (Rec #7, "do not decompose" boundary).

The contradiction: APM sub-skill promotion deploys each sub-skill as a standalone file that agent runtimes load independently. But the `converge` handler and `gate` handler both delegate to the run engine. If the engine is sub-skill `conversus-engine` and gate is sub-skill `conversus-gate`, an agent loading `conversus-gate` must also load `conversus-engine` -- yet APM sub-skills have no declared dependency graph between siblings. The agent runtime has no mechanism to know that loading `conversus-gate` requires also loading `conversus-engine`. This creates a silent failure mode: an agent loads the gate sub-skill, attempts to invoke the run engine, and finds no specification for it. The reference-file model (integration-specialist Rec #2-5) avoids this because reference files are loaded on demand from within the same SKILL.md context, not deployed as independent artifacts. APM's sub-skill model introduces a cross-sub-skill dependency that it cannot currently express or enforce.

### 2. Mode Specifications as Context Files vs. Mode Specifications as Part of the Engine

**apm-specialist** recommends moving mode specifications into separate APM context files (`.apm/context/modes/cooperative.context.md`, etc., Rec #2), arguing agents should not process all four modes when only one is active. **integration-specialist** keeps mode-specific logic (phase differences, review sections, cross-review sections, scoring rules) within the root SKILL.md as part of the run engine core (Rec #1), because the run engine's template variable expansion, dispute parsing headings, and synthesis output format all vary by mode.

The contradiction is about load-time isolation. APM context files are discoverable but not conditionally loaded -- an agent either has context files available or it does not. There is no mechanism in APM's compilation or promotion system that says "load `cooperative.context.md` only when `mode: cooperative` appears in `conversus.yml`." The SKILL.md orchestrator needs all four mode specs available at parse-time because it only learns the mode after reading the config file. Extracting modes into context files forces one of two bad outcomes: (a) the agent loads all four context files anyway, gaining no token savings, or (b) the agent loads only one and breaks when a user changes modes between runs. The integration-specialist's approach of keeping modes in the engine avoids this because mode-specific sections are adjacent to the mode-switching logic that references them.

### 3. Presets as APM Sub-Skill vs. Presets as Run Engine Dependency

**apm-specialist** recommends registering presets as a sub-skill `.apm/skills/conversus-presets/SKILL.md` (Rec #3), with actual `.yml` files as bundled resources. **integration-specialist** identifies preset resolution as a shared subsystem called from three sites (run engine config parsing, interests handler, gate agent expansion) and recommends extracting it to `references/subsystem-preset-resolution.md` (Rec #5).

The dangerous part: an APM sub-skill for presets implies presets are a self-contained capability an agent can load independently. But preset resolution is not independently useful -- it exists only to produce agent config fragments consumed by the run engine's Step 1 (Parse Config). If an agent loads the presets sub-skill without the engine sub-skill, it has a resolution algorithm with no consumer. Conversely, the engine sub-skill references preset names in `conversus.yml` but would need the presets sub-skill co-loaded to resolve them. This is the same cross-sub-skill dependency problem from Contradiction #1, compounded: now three sub-skills (engine, gate, presets) form a dependency triangle that APM cannot express. The reference-file approach keeps preset resolution as an internal subsystem of the SKILL.md, avoiding dependency management that the packaging system cannot enforce.

### 4. PostToolUse Hook for Template Validation vs. Linter as Integration Test

**apm-specialist** recommends adding a PostToolUse hook that triggers `linter/validate.py` when template files are modified (Rec #6). **integration-specialist** recommends expanding the linter's scope to validate reference file consistency after decomposition and treating it as an integration test (Rec #8).

The contradiction is about timing and scope. A PostToolUse hook runs after every individual file write to `templates/`. The linter validates templates against `schema/variables.yml`. But after decomposition, the linter also needs to validate consistency between reference files and their call sites in SKILL.md -- a cross-file concern that a single-file PostToolUse trigger cannot capture. If an agent modifies `references/handler-gate.md` to add a new template variable, the PostToolUse hook on `templates/` will not fire, and the inconsistency between the reference file and the schema goes undetected. The integration-specialist's model (linter as integration test) requires deliberate invocation that covers all artifact types. The APM hook model covers only one artifact type and creates a false sense of validation completeness.

## Tensions

### 1. Internal Structural Split Now vs. Full APM Distribution Later

**apm-specialist** explicitly recommends deferring full APM distribution (Rec #8) but implementing APM-aware internal structure (`.apm/` directory, sub-skills, context primitives) immediately. **integration-specialist** does not reference APM primitives at all, proposing plain `references/` files with a naming convention (Rec #9).

The tension: both agree the time for full distribution is not now. But apm-specialist's "APM-aware internal structure" is an intermediate state that introduces APM directory conventions (`apm/skills/`, `.apm/context/`) without the benefits of APM's install/compile/promote toolchain. An agent working in the conversus repo encounters `.apm/` directories that look like they should be managed by `apm install` but are hand-maintained. The integration-specialist's approach uses a flat `references/` directory that makes no promises about external toolchain compatibility. The question is whether the APM-aware structure creates useful preparatory scaffolding or confusing half-integrated artifacts.

### 2. Context Linking vs. Dependency Map

**apm-specialist** proposes that sub-skills reference shared interfaces via APM's context linking mechanism (Rec #2: "The engine sub-skill references these via APM's context linking"). **integration-specialist** proposes an explicit dependency map table in the root SKILL.md (Rec #10) that documents which reference file depends on which other reference files and is called by which dispatch entries.

The tension: APM context linking is a machine-readable reference mechanism, while the dependency map is a human-readable table. They serve different consumers. But during active spec development (the current phase), the human-readable table is more valuable because it can be validated by visual inspection during code review. The machine-readable context links require APM tooling to validate. If the project later adopts full APM distribution, the dependency map becomes redundant with APM's link graph. During the current phase, investing in context links that no toolchain validates is premature; investing in a dependency map that becomes obsolete is wasteful. Neither review addresses this lifecycle tension directly.

### 3. Antipattern Catalog Placement

**apm-specialist** recommends converting the antipattern catalog to an APM context primitive (`.apm/context/antipatterns.context.md`, Rec #5). **integration-specialist** notes the catalog is already operating as a reference-file pattern (Missed Opportunity #3) and questions whether the antipattern check is an orchestrator-level concern or a per-handler concern after decomposition.

The tension: both agree the catalog needs formal integration, but they disagree on the mechanism. APM context primitives are discoverable by any agent in the repo; a `references/` file is discoverable only by agents reading the conversus SKILL.md. The antipattern check is currently a pre-execution step that the orchestrator runs before Phase 1. If handlers are extracted to reference files, does each handler inherit the antipattern check from the orchestrator (integration-specialist's implied model) or does each handler independently reference the context primitive (apm-specialist's model)? The answer affects whether antipattern violations are caught once at dispatch time or redundantly in every handler.

### 4. Schema Files as Context Primitives vs. Schema as Proven Stable Seam

**apm-specialist** recommends adding `schema/variables.yml` and `schema/modes/*.yml` as APM context primitives (Rec #7). **integration-specialist** identifies `schema/variables.yml` as an already-proven stable seam that has operated successfully without APM packaging since spec 009 (Alignment #2).

The tension: wrapping a working artifact in a new primitive type adds discoverability at the cost of indirection. Currently, `schema/variables.yml` is referenced directly by the linter and by template authors who know to look for it. Making it an APM context primitive adds a layer: agents discover it through APM's context system rather than by reading the directory listing. If the context primitive and the actual file drift (e.g., someone updates `schema/variables.yml` but not the `.apm/context/template-schema.context.md` reference), you get the worst of both worlds -- an authoritative file that agents do not find, and a stale reference that agents trust. The integration-specialist's caution about not creating new seams unnecessarily applies here.

### 5. Root SKILL.md Target Size

**apm-specialist** targets a root SKILL.md of ~100-150 lines (Rec #10: "lightweight dispatcher"). **integration-specialist** targets ~400-500 lines (Rec #1: dispatch + invariants + engine core).

The tension: the 300-350 line gap represents the run engine. apm-specialist wants the engine in a sub-skill; integration-specialist wants it in the root. This is the fundamental architectural disagreement between the two reviews. apm-specialist prioritizes minimal per-invocation context load (each sub-skill ~400-800 lines). integration-specialist prioritizes engine cohesion (the phase loop, round loop, and state machine must be co-located with the dispatch table that invokes them). Both positions are defensible; the right answer depends on whether the conversus orchestrator is more often invoked for a specific subcommand (favoring apm-specialist's approach) or for the full deliberation cycle (favoring integration-specialist's approach). Current usage patterns -- `/conversus run` and `/conversus converge` are the dominant invocations -- suggest the engine is loaded on nearly every call, weakening the case for extracting it to a separate sub-skill.

## Safe Agreements

### 1. The Gate Handler Is a Clean Extraction Target

**apm-specialist** identifies the gate subcommand as "architecturally independent" with its only dependency being the run engine and dispute-parsing subsystem (Alignment #3). **integration-specialist** recommends extracting the gate handler to `references/handler-gate.md` with a distinct CI/CD concern, its own configuration schema, and result schema (Rec #3).

Both reviews agree: gate is the single cleanest extraction boundary in the SKILL.md. It has a self-contained configuration format (`gates.yml`), a self-contained output format (`gate-result.md`), and a thin delegation to the run engine. The only disagreement is packaging (APM sub-skill vs. reference file), not the boundary itself. This extraction should proceed regardless of which packaging model is chosen.

### 2. The Dispute-Parsing Subsystem Warrants Standalone Documentation

**apm-specialist** recommends extracting it to `.apm/context/dispute-parsing.context.md` with explicit stable-interface documentation (Rec #4). **integration-specialist** recommends extracting it to `references/subsystem-dispute-parsing.md` with the same interface contract (Rec #4).

Both reviews identify identical interface boundaries: input (synthesis file path), outputs (boolean + integer), parsing rules (structural markers, heading fallback, mode-specific headings, default-to-triggered), and stable-interface designation (markers and headings are breaking-change boundaries). The packaging mechanism differs, but the content and boundary are identical. This extraction is safe and ready to implement.

### 3. The Guided Workflow Handlers Are Extractable Along File-Mediated Boundaries

**apm-specialist** identifies the guided workflow as a "coherent unit" with a "linear prerequisite chain" (Alignment #4) and recommends it as a sub-skill. **integration-specialist** identifies the same prerequisite chain as "file-mediated coupling" -- the safest form of inter-handler dependency (Alignment #3) -- and recommends extracting each handler to a separate reference file (Rec #2).

Both reviews agree that the five guided workflow handlers (`define`, `interests`, `mode`, `converge`, `arbitrate`) communicate through output files on disk (`problem.md` -> `interests.md` -> `conversus.yml`), not through shared in-memory state. This makes them safe extraction candidates regardless of granularity (one unit vs. five files). The file-mediated interface means decomposition cannot introduce coupling that does not already exist.

### 4. Premature Full Distribution Should Be Deferred

**apm-specialist** explicitly states: "Defer full APM distribution until spec suite stabilizes" (Rec #8), noting that versioning overhead during active spec development creates maintenance drag. **integration-specialist** does not propose any distribution mechanism, implicitly treating conversus as a submodule-internal concern.

Both reviews agree that packaging conversus for external consumption is premature. The framework is used by one project, the spec suite is actively evolving (011a is the current spec), and the decomposition should serve internal coherence first. External compatibility standards (APM, agents.md, agentskills.io) should inform but not drive the internal decomposition boundaries.
