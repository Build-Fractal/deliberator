# APM Specialist — Revision (Iteration 1)

## Recommendation Dispositions

### Original Recommendation 1: Create `.apm/skills/` directory with three sub-skills immediately
**REVISED: Withdraw as primary decomposition strategy. Adopt `references/` as primary, retain sub-skills only for gate.**

Every cross-reviewer converged on the same structural critique: APM sub-skill promotion copies each sub-skill's full SKILL.md to `.github/skills/{name}/`, meaning the agent loads the entire sub-skill body on activation. This does not solve the progressive disclosure problem — it replaces one monolith with several smaller monoliths. The functional-decomposition and agentskills-specialist reviews both demonstrated that a `conversus-engine` sub-skill at 600-800 lines still exceeds the 500-line / 5,000-token agentskills recommendation by 60%+. The integration-specialist identified a harder problem: APM sub-skills have no sibling dependency mechanism, so `conversus-gate` loading without `conversus-engine` is a silent failure mode that APM cannot currently express or enforce.

I was wrong to frame sub-skill promotion as the primary decomposition axis. Sub-skills solve a distribution problem (different consumers need different capabilities). Conversus has a context window problem (one consumer needs different details at different moments). The agentskills `references/` model — conditional file loading triggered by runtime state — directly addresses the actual problem.

**Revised position**: Use the agentskills `references/` pattern as the primary decomposition mechanism within a single conversus skill. The one exception is gate: it serves a categorically different audience (CI/CD pipelines vs. interactive users), has a self-contained config and output schema, and is the only subcommand that could plausibly be activated independently. Gate warrants consideration as an APM sub-skill. The remaining handlers (define, interests, mode, converge, arbitrate, run) should be reference files loaded conditionally from the root SKILL.md dispatch table.

### Original Recommendation 2: Move mode specifications into separate APM context files
**REVISED: Withdraw. Mode specifications should become `references/` files, not APM context primitives.**

The agents-md-specialist and integration-specialist both identified the core flaw: APM context files (`.apm/context/`) are discovered at compile/install time and placed based on `applyTo` file-path glob patterns. They have no runtime conditional loading mechanism. There is no way to express "load `cooperative.context.md` only when `mode: cooperative` appears in `conversus.yml`" — `applyTo` matches filesystem paths, not YAML config field values.

The agentskills-specialist made this concrete: mode specifications are not reference documentation for agent awareness — they are runtime execution logic the orchestrating agent must follow during active phases. Extracting them to context files downgrades them from "instructions the agent must execute" to "information the agent should be aware of." APM's context primitive model does not carry execution authority.

**Revised position**: Extract mode-specific sections to `references/mode-cooperative.md`, `references/mode-winner-take-all.md`, etc. The root SKILL.md dispatch table should instruct: "After parsing `conversus.yml`, read `references/mode-{mode}.md` for the active mode." This achieves the same context reduction (agents load only the active mode's specification) through a mechanism that is triggered by runtime state, not filesystem position.

### Original Recommendation 3: Register presets as a sub-skill
**REVISED: Withdraw. Presets should be a conditionally-loaded reference file.**

The agentskills-specialist landed the decisive argument: presets are YAML data files with a resolution algorithm, not agent instructions. A SKILL.md is a meta-guide that helps agents understand what a package does. Wrapping preset resolution in a SKILL.md creates a skill whose body is "here is how to resolve presets" — a reference document forced into an executable instruction container. The functional-decomposition review added the activation problem: a `conversus-presets` sub-skill has no subcommand of its own — nothing triggers it independently. It is a support library consumed by the engine, gate, and interests handlers.

My own Off-Base Assumptions section already acknowledged that "presets are tightly coupled to conversus's composition template system" and "a preset outside conversus has no meaning." I should have followed that reasoning to its conclusion rather than splitting it from the recommendation.

**Revised position**: Extract preset resolution rules to `references/preset-resolution.md`, loaded conditionally when any agent entry in `conversus.yml` contains a `preset` field. The preset `.yml` data files remain in `presets/` as bundled resources. This pays zero context cost when presets are not used.

### Original Recommendation 4: Extract Dispute-Parsing Subsystem into `.apm/context/dispute-parsing.context.md`
**REVISED: Keep extraction, change destination to `references/dispute-parsing.md`.**

All four cross-reviewers agreed this subsystem warrants extraction — the boundary, interface contract, and multi-consumer dependency are uncontested. The agents-md-specialist raised the strongest objection to the APM context primitive placement: dispute parsing is an algorithm the executing agent must follow step-by-step when processing synthesis outputs. Converting it to a context file downgrades it from executable instruction to ambient awareness. The integration-specialist reinforced this — dispute parsing directly determines whether rounds continue or terminate, making execution fidelity critical.

I concede the placement. The subsystem's stable interface makes it a textbook extraction candidate, but its nature as executable logic (not background knowledge) means it belongs in the agentskills `references/` directory where the SKILL.md explicitly instructs the agent to load and follow it.

**Revised position**: Extract to `references/dispute-parsing.md` with the same interface contract (inputs, outputs, parsing rules, defaults). The root SKILL.md and each handler that invokes dispute parsing should contain an explicit load trigger: "Read `references/dispute-parsing.md` before processing synthesis outputs."

### Original Recommendation 5: Convert antipattern catalog to APM context primitive
**REVISED: Withdraw APM context placement. Keep as a reference file with explicit load trigger.**

The agentskills-specialist's progressive disclosure principle applies: the antipattern catalog should load when the agent needs to check output against known antipatterns, not as ambient knowledge consuming tokens across all contexts. The agents-md-specialist correctly noted that if antipatterns are always-loaded as a context primitive compiled into CLAUDE.md, this partially re-creates the context pollution the restructuring aims to eliminate.

However, the agents-md-specialist's proposal to put antipatterns in AGENTS.md files is also wrong — antipatterns are checked by the conversus engine at runtime, not by contributing agents at edit time. They are execution-path content, not contribution guidance.

**Revised position**: The antipattern catalog stays as `antipatterns/catalog.md` (its current location works) and is referenced from the SKILL.md as a pre-execution check. The load trigger is explicit: "Before writing a synthesis, read `antipatterns/catalog.md` and verify your output does not exhibit any cataloged pattern." This is a reference-file access pattern without the overhead of APM context primitives or the misplacement of AGENTS.md.

### Original Recommendation 6: Add PostToolUse hook for template validation
**REVISED: Withdraw. Keep explicit linter instruction in SKILL.md.**

Three reviewers identified problems with the hook approach. The agentskills-specialist demonstrated the trigger mismatch: templates are read during deliberation phases and outputs are written to the output directory — a PostToolUse hook on `templates/` writes fires during skill development, not during execution. The agents-md-specialist identified the scope limitation: APM hooks only protect Claude Code users; agents in Cursor, Copilot, or Junie would not benefit. The integration-specialist raised the scope expansion problem: after decomposition, the linter needs to validate cross-file consistency (reference files vs. call sites), which a single-file PostToolUse trigger cannot capture.

The current explicit instruction ("run `uv run python linter/validate.py`") is less elegant but more robust — the agent reads it and executes it regardless of hook infrastructure, and it fires at the right time (after template modification during development, not during execution).

**Revised position**: Keep the existing linter instruction in SKILL.md. If the linter's scope expands to cover reference file consistency (as the integration-specialist recommends), document the expanded invocation alongside the existing instruction. Do not automate via APM hooks at this stage.

### Original Recommendation 7: Add schema files as APM context primitives
**REVISED: Withdraw. Schema files work fine in their current location.**

The integration-specialist made the strongest case: `schema/variables.yml` has been decoupled from SKILL.md since spec 009 and has operated successfully without APM packaging. Wrapping a working artifact in a context primitive adds discoverability at the cost of indirection and drift risk. If someone updates `schema/variables.yml` but not the `.apm/context/template-schema.context.md` reference, agents trust a stale reference while the authoritative file goes undiscovered.

The schema files serve three consumers (the linter, the agent, and the template system). No single APM primitive placement serves all three well. The current direct-reference model, where the linter reads the file and the SKILL.md points agents to it, is simpler and has proven stable.

**Revised position**: Leave schema files in `schema/`. If agents need to reference them during template work, the root SKILL.md or the relevant handler reference file should contain a direct file path reference. No APM context wrapper needed.

### Original Recommendation 8: Defer full APM distribution until spec suite stabilizes
**MAINTAINED: This recommendation was correct and is reinforced by the cross-review consensus.**

All four cross-reviewers independently agreed that full APM distribution is premature. Conversus is a single-project, actively-evolving framework (specs 012-020 queued). The distribution overhead — version bumps, dependency resolution, multi-target deployment testing — is not justified until a second consumer appears or the spec suite stabilizes.

This recommendation was the most universally supported position across all reviews. No revision needed.

### Original Recommendation 9: Use `target: all` to validate sub-skill deployment
**REVISED: Scope down to gate sub-skill only, if gate is extracted as a sub-skill.**

With the withdrawal of the three-sub-skill model, this recommendation's scope narrows. If gate is extracted as an APM sub-skill (the one case where sub-skill promotion may be appropriate), validate that `apm install` correctly promotes it to `.github/skills/conversus-gate/`, `.claude/skills/conversus-gate/`, etc. For the remaining reference-file-based decomposition, no APM deployment validation is needed because reference files are bundled resources that stay in the skill directory.

### Original Recommendation 10: Document the sub-skill dependency graph in root SKILL.md
**REVISED: Replace with a reference dependency map in root SKILL.md.**

The concept is sound — the root SKILL.md should document which content lives where and what depends on what — but the shape changes with the decomposition model. Instead of a sub-skill dependency graph, the root SKILL.md should contain a reference map showing: (a) which reference file handles which subcommand, (b) which reference files are shared subsystems (dispute parsing, preset resolution), and (c) which handlers depend on which shared subsystems. This serves the same navigational purpose without assuming APM sub-skill topology.

The integration-specialist's naming convention (`handler-`, `subsystem-`, `contract-`) for reference files is a strong pattern that makes the dependency map self-documenting from a directory listing. I adopt this.

## New Recommendations

### N1. Use APM sub-skill promotion only for gate, and only after the reference-file decomposition is complete

Gate is the one subcommand with a genuinely independent audience (CI/CD pipeline authors), a self-contained configuration format (`gates.yml`), and a self-contained output format (`gate-result.md`). After extracting gate to `references/handler-gate.md` first (proving the boundary works), consider promoting it to `.apm/skills/conversus-gate/SKILL.md` so that APM deploys it as an independently discoverable skill alongside the main conversus skill. This lets CI/CD-focused agents load only the gate specification without the interactive deliberation machinery.

This is the only sub-skill that passes both tests: (1) it serves a different audience, and (2) it can be activated independently without requiring sibling sub-skills. Defer this promotion until after the reference-file restructuring proves stable across at least two spec iterations.

### N2. Ensure reference files within the skill use explicit load triggers, not `applyTo` or other APM mechanisms

The key architectural insight from this review cycle is the distinction between install-time placement (APM's `applyTo` and context linking) and invocation-time loading (agentskills' conditional file reads). For conversus, invocation-time loading is the correct optimization target because the relevant content varies by runtime state (which subcommand, which mode, whether presets are used), not by filesystem position.

Every reference file extracted from SKILL.md must have a corresponding explicit load trigger in the root SKILL.md or in the handler that calls it. The trigger must reference a runtime condition, not a file path pattern. Examples: "If the user invokes `/conversus gate`, read `references/handler-gate.md`." "If the config specifies `rounds > 1`, read `references/multi-round-orchestration.md`." "Before processing synthesis outputs, read `references/dispute-parsing.md`."

Without these explicit triggers, agents may either eagerly load all references (defeating the purpose) or fail to load necessary ones (breaking execution). The functional-decomposition review correctly identified this as the critical success factor for the entire decomposition.

### N3. APM's role in conversus is structural preparation, not active packaging

Revising my overall position: APM's value for conversus at this stage is not in its packaging, distribution, or compilation machinery. It is in the structural conventions that make future packaging low-friction. The `apm.yml` manifest, the `type: skill` declaration, and the `target: all` setting are correct and should remain. The `.apm/` directory can hold the gate sub-skill if/when it is promoted. But the primary decomposition should use agentskills conventions (`references/` files with conditional load triggers) that work today without any APM toolchain dependency.

This is not a retreat from APM — it is a correct sequencing. APM packaging becomes valuable when conversus has multiple consumers or when the `references/` structure needs to be distributed to projects that do not have conversus as a submodule. That day is not today, and the structural preparation (well-defined reference boundaries, stable interface contracts, the dispatch table as the single entry point) makes the future APM packaging straightforward when the time comes.

## Position Summary

My original review overreached by proposing APM sub-skills as the primary decomposition axis. The cross-reviews collectively demonstrated that APM sub-skill promotion solves a distribution problem while conversus has a context window problem. These require different mechanisms: install-time skill separation vs. invocation-time conditional loading.

**Revised architecture**: A single conversus skill with a lean root SKILL.md (~350-400 lines containing the dispatch table, multi-agent isolation rules, and phase-level flow summary) plus 7-10 reference files loaded conditionally based on runtime state. The gate subcommand is the sole candidate for eventual APM sub-skill promotion, deferred until the reference-file restructuring proves stable.

**What I concede**:
- Sub-skill promotion is wrong as the primary decomposition strategy for conversus at this stage. The agentskills `references/` pattern is the correct primary mechanism.
- APM context primitives (`.apm/context/`) are wrong for mode specifications, dispute parsing, and antipatterns. These are runtime execution content, not ambient awareness content. `applyTo` patterns cannot express runtime conditionals.
- The PostToolUse hook is wrong for template validation — it fires on the wrong trigger, covers only Claude Code, and removes agent-visible reasoning about validation failures.
- Presets as a sub-skill is wrong — presets are a data catalog with a resolution algorithm, not independently activatable agent instructions.
- Schema files as context primitives add indirection without benefit when the current direct-reference model has been stable since spec 009.

**What I maintain**:
- Full APM distribution should be deferred until the spec suite stabilizes and a second consumer appears. This was unanimously supported.
- Gate is architecturally independent and the strongest extraction candidate, regardless of mechanism. Also unanimously supported.
- The dispatch table is the correct root anchor and should remain in the always-loaded core. Unanimously supported.
- APM structural preparation (manifest, type declaration, target setting) is correct to maintain — it creates optionality for future packaging without imposing current overhead.
- The Dispute-Parsing Subsystem must be extracted as a standalone, referenceable unit. The boundary and interface contract are uncontested; only the destination changes (from `.apm/context/` to `references/`).

**What I add**:
- The distinction between install-time optimization (APM's domain) and invocation-time optimization (agentskills' domain) is the key architectural insight. Conversus needs invocation-time optimization now. APM's install-time optimization becomes relevant when distribution to multiple consumers is needed.
- Reference files must have explicit load triggers tied to runtime conditions. This is the critical success factor — without it, the decomposition achieves nothing.
- The integration-specialist's naming convention for reference files (`handler-`, `subsystem-`, `contract-`) should be adopted for self-documenting directory structure.
