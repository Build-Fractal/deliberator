# Cross-Review of integration-specialist — by apm-specialist

## Dangerous Contradictions

### 1. Where the run engine lives determines whether APM sub-skill promotion works or breaks

integration-specialist recommends keeping the run engine core in the root SKILL.md (~400-500 lines) alongside the dispatch table and multi-agent isolation rules (Recommendation 1). I recommended splitting into three sub-skills under `.apm/skills/` — `conversus-engine`, `conversus-wizard`, `conversus-gate` — with the root SKILL.md as a lightweight dispatcher (~100-150 lines) (my Recommendation 1).

These proposals are structurally incompatible. APM's sub-skill promotion copies each `.apm/skills/*/SKILL.md` to `.github/skills/{sub-skill-name}/` as an independent entry. If the run engine stays in the root SKILL.md (integration-specialist's model), it is promoted as the *parent* skill to `.github/skills/conversus/SKILL.md`, meaning every agent invocation loads the full engine regardless of which subcommand is being executed. This defeats the context-reduction goal both reviews agree on. Conversely, if the engine moves to `.apm/skills/conversus-engine/SKILL.md` (my model), it becomes independently loadable — but integration-specialist is correct that the engine's phase loop, round loop, and output path computation are tightly coupled and must remain a single unit. The disagreement is not about cohesion (we agree the engine is cohesive) but about *where* that cohesive unit is housed — root vs. sub-skill — and this has direct consequences for APM deployment behavior.

**Resolution needed**: Define whether the root SKILL.md is a "fat dispatcher" (integration-specialist) or a "thin router" (apm-specialist), because APM's promotion mechanics produce different deployment artifacts for each choice.

### 2. Reference files vs. sub-skills are not interchangeable decomposition strategies

integration-specialist proposes extracting handlers to `references/handler-{name}.md` files (Recommendations 2, 3) — these are plain markdown files within the skill's bundled resources that the orchestrating agent loads on demand via file reads. I proposed extracting handlers as sub-skills under `.apm/skills/` that APM promotes to independent `.github/skills/` entries.

These are fundamentally different runtime models. Reference files require the agent to already be executing the parent skill and then explicitly read supplementary files from disk. Sub-skills are independently discoverable by agent runtimes — Copilot, Claude, and Cursor each scan `.github/skills/` (or their equivalent) and can route to a sub-skill without ever loading the parent. Reference files preserve the "one skill, many parts" model; sub-skills create a "many skills, coordinated" model.

integration-specialist's reference-file approach is safer for internal coherence (no risk of a sub-skill being invoked without its dependencies), but it means *every* conversus invocation must first load the root SKILL.md and *then* read the relevant reference file — two file reads, with the root file still being the context bottleneck. My sub-skill approach reduces first-load context but creates a risk that an agent loads `conversus-gate` without understanding the engine's dispute-parsing contract.

**Resolution needed**: Determine whether conversus handlers should be independently invocable (sub-skills) or always mediated through the dispatcher (reference files), because this constrains which APM primitive model applies.

### 3. The dependency map creates a maintenance burden that contradicts the "defer APM distribution" agreement

integration-specialist's Recommendation 10 proposes a dependency map table in the root SKILL.md showing which reference file depends on which other reference file and which call sites invoke it. My Recommendation 10 proposes a similar dependency graph for sub-skills. Both reviews independently converge on the need for explicit dependency documentation — but integration-specialist's map (reference files with file-mediated coupling) and my map (sub-skills with APM-level dependencies) describe different dependency topologies.

The danger is that maintaining this map manually is exactly the kind of documentation drift that integration-specialist's own Missed Opportunity about linter scope (Recommendation 8) identifies as a risk. If the map is in the root SKILL.md and a new handler is added, the map must be updated alongside the handler reference file, the dispatch table, and potentially the linter scope. This is three coordination points for a single change. My recommendation to defer APM distribution (Recommendation 8) is in tension with integration-specialist's detailed dependency map — if we defer packaging, we also defer the tooling (APM's dependency graph resolution) that could automate map maintenance. We are both proposing manual dependency tracking for a system we both acknowledge is drift-prone.

**Resolution needed**: Either commit to APM packaging now (so dependency tracking is automated) or accept that the dependency map is aspirational documentation that will drift (and design the linter to catch it).

### 4. Context file placement for mode specifications conflicts with the run engine's template variable resolution

I recommended moving mode specifications into `.apm/context/modes/cooperative.context.md` etc. (my Recommendation 2), arguing this eliminates the need for agents to process all four modes when only one is active. integration-specialist does not address mode-specific extraction at all — the implicit position is that mode specifications remain in the run engine core within the root SKILL.md.

This is dangerous because the run engine's template variable contracts (lines 401-517 in SKILL.md) are mode-dependent. The variables available in Phase 2 (cross-review) differ by mode — cooperative mode provides `{CROSS_REVIEWS_OF_ME}` while winner-take-all provides `{ALL_REVIEWS}`. If mode specifications are extracted to APM context files, the run engine must reference them at execution time, but APM context files are not loaded dynamically per-invocation — they are compiled into AGENTS.md or placed in `.apm/context/` for agent discovery. The engine would need to instruct the agent to read a specific context file based on the active mode, which reintroduces the file-read overhead that integration-specialist's reference-file model already accounts for, but without integration-specialist's coherent "reference files are always loaded through the parent" contract.

**Resolution needed**: Clarify whether mode specifications are compile-time context (APM context primitives) or runtime reference material (reference files loaded by the engine), because APM's context primitive model does not support conditional loading.

## Tensions

### 1. "Do not decompose" boundaries vs. the 500-line target

integration-specialist's Recommendation 7 defines explicit "do not decompose" boundaries around the round loop, iteration loop, output path computation, and termination check (lines 346-580), estimating the root SKILL.md at ~400-500 lines. My review acknowledges the engine's tight coupling but proposes it as a single sub-skill (`conversus-engine`). Both reviews respect the engine's internal cohesion, but integration-specialist's "do not decompose" framing combined with keeping the engine in root creates a root SKILL.md that consumes the entire 500-line budget on the engine alone, leaving zero room for the dispatch table, multi-agent isolation rules, and any future additions. My sub-skill approach sidesteps this by moving the engine out of root entirely, but at the cost of the coherence guarantees integration-specialist values.

This is a tension rather than a contradiction because both positions are internally consistent — they just optimize for different constraints (context-load reduction vs. coherence safety).

### 2. Linter expansion scope

integration-specialist's Recommendation 8 mandates expanding `linter/validate.py` to check reference file consistency (variable existence, error message matching, interface contract alignment). My Recommendation 6 proposes a PostToolUse hook that triggers `linter/validate.py` on template file modifications. These are complementary but create tension around scope: integration-specialist wants the linter to become a comprehensive integration test suite (checking reference files, error catalogs, call-site consistency), while my hook proposal keeps the linter focused on template validation triggered by file writes.

If both are adopted, the linter becomes both a CI-time integration test (integration-specialist's scope) and a real-time hook (my scope). These are different execution contexts with different performance constraints — a comprehensive integration test that checks all reference files is too slow for a PostToolUse hook that fires on every file write.

### 3. Naming conventions serve different audiences

integration-specialist proposes `references/handler-{name}.md`, `references/subsystem-{name}.md`, `references/contract-{name}.md` (Recommendation 9). My recommendations use APM's directory conventions: `.apm/skills/`, `.apm/context/`. These naming schemes serve different audiences — integration-specialist's convention is optimized for human readability ("I can see the dependency graph from `ls references/`"), while APM's conventions are optimized for tool discovery ("APM CLI knows to promote anything in `.apm/skills/`").

The tension is that both cannot occupy the same directory. If handlers go into `references/`, APM cannot auto-promote them. If they go into `.apm/skills/`, the clean type-prefixed naming (`handler-`, `subsystem-`, `contract-`) is lost because APM sub-skill directories are just named for the skill, not categorized by type.

### 4. Antipattern catalog placement

integration-specialist identifies the antipattern catalog interaction as a missed opportunity but does not propose a specific location. I recommend converting it to `.apm/context/antipatterns.context.md` (my Recommendation 5). The tension is that integration-specialist views the antipattern check as an orchestrator-level concern that belongs near the dispatch table ("does each handler need its own check, or is this orchestrator-level?"), while I view it as a knowledge artifact best handled by APM's context primitive model. If it is orchestrator-level, it stays in or near root SKILL.md. If it is an APM context primitive, it is discoverable by any agent regardless of whether they are executing a conversus subcommand. Both placements are defensible for different reasons.

### 5. Timing of structural changes relative to spec stability

integration-specialist does not address timing — the review implicitly assumes decomposition happens now, during spec 011a. My Recommendation 8 explicitly argues for deferring full APM distribution until the spec suite stabilizes. This creates tension around implementation sequencing: integration-specialist's detailed structural proposals (9 reference files, naming conventions, dependency maps, linter expansion) represent significant structural investment that could be disrupted by specs 012-020 (which are queued per the recent commit messages). If the structural split happens now and a future spec reorganizes the run engine, all reference files and their interface contracts must be updated. If we defer, the monolith continues to impose context-load costs on every conversus invocation.

## Safe Agreements

### 1. The dispatch table is the correct root anchor

Both reviews agree that the subcommand dispatch table (lines 22-44) must remain in the root SKILL.md as the entry point contract. integration-specialist: "Decomposition proposals that preserve this table as the entry point in the root SKILL.md, with handlers referenced rather than inlined, align with progressive disclosure." My review: "the root SKILL.md should contain the subcommand dispatch table." This is uncontested and should be treated as a fixed constraint for any decomposition proposal.

### 2. The guided workflow's file-mediated coupling is the safest decomposition seam

Both reviews identify the guided workflow prerequisite chain (define -> interests -> mode -> converge) as the lowest-risk extraction target. integration-specialist: "Each handler reads the previous handler's output file... This file-mediated coupling is the safest form of inter-handler dependency." My review: "These five commands form a linear prerequisite chain... that represents a distinct user journey from the raw run engine." We disagree on *where* to put the extracted handlers (reference files vs. sub-skills) but agree that extraction is safe precisely because inter-handler coupling is mediated by filesystem artifacts, not in-memory state.

### 3. The gate handler is architecturally independent and a clean extraction candidate

Both reviews identify the gate handler as having the least coupling to the rest of the system. integration-specialist: "The gate handler has a distinct concern (CI/CD integration) with its own configuration schema, result schema, exit code contract, and re-run behavior" (Recommendation 3). My review: "the gate subcommand with its configuration schema, result schema, and CI/CD integration" is one of the three proposed sub-skills (Recommendation 1c). The gate handler's only dependency on the engine is "generate a conversus.yml and invoke Steps 1-5" — a clean, narrow interface that survives any decomposition strategy.

### 4. Existing stable seams (schema/variables.yml, linter, templates) validate that decomposition works for conversus

Both reviews point to `schema/variables.yml`, `linter/validate.py`, and the `templates/{mode}/` directory tree as evidence that conversus can sustain interface boundaries without regression. integration-specialist: "the schema has been decoupled from SKILL.md since spec 009 without breaking the orchestrator." My review: "The `schema/` directory (variables.yml, modes/*.yml) is a natural APM context artifact." These existing seams have been operating across multiple specs without drift, providing empirical evidence that further decomposition along similar lines (explicit interface contracts, validation tooling) will succeed.
