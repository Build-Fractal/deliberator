# Cross-Review of agentskills-specialist's Phase 1 Review

Reviewer: **apm-specialist**

---

## Dangerous Contradictions

### 1. Reference files vs. sub-skills: incompatible deployment models

agentskills-specialist recommends extracting subcommand handlers into `references/handler-run.md`, `references/handler-define.md`, etc. (Recommendation 1), with the SKILL.md dispatch table saying "Read `references/handler-define.md` when the user invokes `/conversus define`." My review recommends splitting into `.apm/skills/` sub-skills (`conversus-engine`, `conversus-wizard`, `conversus-gate`) that APM promotes to independent `.github/skills/` entries (Recommendation 1).

These two approaches are structurally incompatible. APM sub-skill promotion copies each `.apm/skills/*/SKILL.md` to `.github/skills/{name}/SKILL.md` as a top-level skill directory. The `references/` approach keeps everything under a single skill root where the agent reads additional files via the `Read` tool at runtime. If the project implements sub-skills, each sub-skill gets its own `references/` directory, and the handler files live inside their respective sub-skill, not in a flat `references/` directory under the root SKILL.md. If the project follows the agentskills `references/` pattern instead, there are no sub-skills for APM to promote, and the multi-target deployment benefit (`target: all` deploying to `.github/skills/`, `.claude/skills/`, `.cursor/skills/`) applies to only one monolithic skill entry.

The danger is implementing both models halfway: creating `references/handler-*.md` files (agentskills pattern) while also creating `.apm/skills/` directories (APM pattern), resulting in duplicated content and ambiguous routing. The decomposition model must be chosen first: either the agentskills progressive-disclosure model with a single skill and reference files, or the APM multi-skill model with sub-skill promotion. They solve the same problem (context reduction) through different mechanisms (runtime file reads vs. install-time skill separation).

### 2. Token budget targets assume different cost models

agentskills-specialist states the target should be "token-aware, not just line-aware" and that the SKILL.md exceeds the 5,000-token recommendation by roughly 6x (Off-Base Assumptions, point 4). The entire restructuring is framed around fitting the core SKILL.md under 5,000 tokens. My review frames the problem as context window cost per invocation (Executive Summary) but recommends sub-skills of 400-800 lines each (Recommendation 1), which at typical token density would be 5,000-10,000 tokens per sub-skill.

This is a real conflict. Under the agentskills model, only the core SKILL.md matters for the budget because reference files load on demand via `Read`. Under the APM sub-skill model, each sub-skill is its own SKILL.md that loads entirely when the agent activates that skill. If the conversus-engine sub-skill is 800 lines, it still blows the 5,000-token agentskills recommendation. The agentskills approach achieves a tighter core (350 lines, ~4,000 tokens) by deferring everything to references. The APM approach achieves deployment-level separation but each unit is individually larger. The project cannot optimize for both budgets simultaneously without choosing which model governs sizing.

### 3. "Presets as sub-skill" conflates a data catalog with executable instructions

My review recommends registering the presets directory as a sub-skill (`.apm/skills/conversus-presets/SKILL.md`, Recommendation 3), while also cautioning against extracting presets as independent APM packages (Off-Base Assumptions, point 1). agentskills-specialist recommends extracting preset resolution rules to `references/preset-resolution.md` (Recommendation 7), treating presets as reference material loaded when a config contains `preset:` fields.

The agentskills framing is more accurate here. Presets are YAML data files with a resolution algorithm, not agent instructions. A SKILL.md is "a meta-guide that helps AI agents understand what a package does" (APM skills guide, line 7). The preset `.yml` files are not instructions for an agent — they are configuration fragments the agent reads and interpolates. Wrapping them in a SKILL.md creates a skill whose body is essentially "here is how to resolve presets," which is a reference document, not a skill. The agentskills approach (conditional reference loading: "If any agent entry contains a `preset` field, read `references/preset-resolution.md`") matches the nature of the content. My sub-skill recommendation forced a data catalog into an executable instruction container.

### 4. Antipattern catalog placement contradicts progressive disclosure

My review recommends converting `antipatterns/catalog.md` to an APM context primitive (`.apm/context/antipatterns.context.md`, Recommendation 5), which makes it discoverable by APM's compilation system and linkable from other primitives. agentskills-specialist does not address the antipattern catalog directly, but the overall philosophy of the agentskills review is that reference material should load on demand based on specific execution-path triggers (Recommendation 9: "If the config contains an `arbiter:` block, read `references/arbitration-engine.md` before executing Phase 6").

The APM context primitive model makes the antipattern catalog available at compile time across all contexts that link to it — it becomes ambient knowledge. The agentskills model would place it as a reference loaded only when the agent needs to check its output against known antipatterns. These produce opposite context behaviors: always-present ambient knowledge (APM context) vs. conditionally-loaded reference (agentskills progressive disclosure). For a 55-line antipattern catalog, ambient loading is defensible. But the SKILL.md is being restructured precisely because ambient loading of everything is the problem. Making the antipattern catalog a context primitive that loads across all sub-skills would partially re-create the context pollution the restructuring aims to eliminate.

---

## Tensions

### 1. Single-package discipline vs. multi-consumer readiness

My review emphasizes deferring full APM distribution until the spec suite stabilizes (Recommendation 8), keeping conversus as a submodule with APM-aware internal structure. agentskills-specialist's review is entirely silent on distribution concerns — it treats the restructuring as a pure internal quality problem (reducing context window cost). This creates a tension: my recommendations add APM machinery (`.apm/skills/`, `.apm/context/`, hooks) that only pays for itself when multiple consumers exist, while agentskills-specialist's `references/` approach is zero-overhead and works today with no tooling changes. The structural investment in APM primitives is premature if conversus remains single-consumer for another 6+ months of spec development.

### 2. Dispute-Parsing Subsystem: stable interface vs. context primitive

Both reviews agree the Dispute-Parsing Subsystem should be extracted. agentskills-specialist recommends `references/dispute-parsing.md` (Recommendation 3), referenced from the core SKILL.md and from each handler that uses it. My review recommends `.apm/context/dispute-parsing.context.md` (Recommendation 4), making it an explicit context file with APM linking so changes propagate through the link graph. The agentskills approach is simpler (a markdown file read on demand) but lacks the link-graph propagation. The APM approach provides change tracking but requires APM's compilation pipeline to resolve the links. Since conversus templates already use a custom variable system (`{AGENT_NAME}`, `{CROSS_REVIEWS_OF_ME}`), adding APM's context linking syntax introduces a second resolution mechanism, increasing cognitive load for maintainers.

### 3. Handler extraction granularity

agentskills-specialist recommends seven separate handler reference files, one per subcommand (Recommendation 1). My review groups handlers into three sub-skills: engine (run + template system + disputes + arbitration), wizard (define/interests/mode/converge/arbitrate), and gate (Recommendation 1). The agentskills granularity is finer — an agent invoking `/conversus define` loads only `handler-define.md`. Under my three-skill model, an agent invoking `/conversus define` loads the entire `conversus-wizard` sub-skill, which includes five handler specifications. The agentskills approach minimizes per-invocation context more aggressively, but creates 7+ files to maintain. The APM approach creates fewer files but with coarser context boundaries. Neither review provides data on which subcommands are most frequently invoked together, which would resolve this tension empirically.

### 4. Template and schema organization

agentskills-specialist recommends moving output schema templates to `assets/` (Recommendation 6), following the agentskills best practice for templates only needed in certain cases. My review recommends registering `schema/variables.yml` and `schema/modes/*.yml` as APM context primitives (Recommendation 7). The existing `schema/` directory already serves the linter (`linter/validate.py`), which my review also recommends converting to a PostToolUse hook (Recommendation 6). This creates a three-way tension: the schema files serve the linter (machine consumer), the agent (context consumer), and the template system (runtime consumer). Reorganizing them for one consumer may break the ergonomics for the others. The agentskills `assets/` placement optimizes for agent access; the APM context primitive optimizes for discoverability; the current `schema/` placement optimizes for the linter. No single location serves all three well.

### 5. Root SKILL.md size after restructuring

agentskills-specialist targets 300-400 lines / under 5,000 tokens for the root SKILL.md (Recommendation 2). My review targets 100-150 lines for the root SKILL.md (Recommendation 10), with sub-skill dependency graph and shared interface documentation. The agentskills target includes a phase-level flow summary at one paragraph per phase, the non-negotiable multi-agent rules, and a gotchas section. My target includes only the dispatch table, dependency graph, and shared interfaces. If the non-negotiable multi-agent rules (12 lines) and phase-level flow (roughly 50 lines) must be in the always-loaded core — as agentskills-specialist argues, because they are the highest-fragility invariants — then 100-150 lines is too tight. If they can be deferred to the engine sub-skill, then 300-400 lines is too generous for a dispatcher. The right answer depends on whether those invariants apply to all subcommands (including `define`, which never runs phases) or only to `run` and `gate`.

---

## Safe Agreements

### 1. The SKILL.md is too large and must be decomposed

Both reviews agree unambiguously that 2200+ lines / 31,000 tokens is unsustainable. agentskills-specialist: "At 31k tokens, conversus consumes a significant fraction of available context on every invocation" (Executive Summary). My review: "At 119KB / 2200+ lines, this exceeds any reasonable context window budget for a single skill" (Alignment, point 1). The disagreements are about decomposition strategy, not about whether decomposition is needed.

### 2. The dispatch table is well-designed and should remain in the root

agentskills-specialist calls the dispatch table "an exemplary implementation of the 'provide defaults, not menus' pattern" (Alignment, point 2). My review preserves it in the root SKILL.md across all recommendations (Recommendation 10: "the root SKILL.md should contain the subcommand dispatch table"). Both reviews agree it is the correct anchor for the always-loaded core.

### 3. The gate subcommand is an independent extraction target

agentskills-specialist: "The gate subcommand is approximately 300 lines of CI/CD-specific specification... Extracting it to `references/handler-gate.md` reduces SKILL.md size" (Missed Opportunities, point 5). My review: "Gate reads a `gates.yml`, generates a standard `conversus.yml`, delegates to the run engine, and produces a machine-readable `gate-result.md`. Its only dependency on the rest of SKILL.md is the run engine and the Dispute-Parsing Subsystem. This is a clean extraction boundary" (Alignment, point 3). Regardless of whether gate becomes an APM sub-skill or an agentskills reference file, both reviews identify it as the cleanest, lowest-risk extraction.

### 4. The infrastructure for progressive disclosure already exists

agentskills-specialist: "The `references/` directory already exists with substantial content... The infrastructure for progressive disclosure exists; the SKILL.md simply has not been restructured to use it" (Executive Summary). My review: "The package is APM-aware. The infrastructure for sub-skill promotion exists — the issue is that no `.apm/skills/` directory has been created yet" (Missed Opportunities, point 1). Both reviews observe that conversus has laid groundwork (agentskills `references/`, APM `apm.yml` with `type: skill`) but has not used it. The first step — actually using the existing infrastructure — is uncontested.
