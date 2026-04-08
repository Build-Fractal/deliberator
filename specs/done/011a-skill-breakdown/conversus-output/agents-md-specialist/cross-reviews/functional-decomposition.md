# Cross-Review of functional-decomposition's Review

**Reviewer:** agents-md-specialist
**Reviewing:** functional-decomposition's Phase 1 review of spec 011a (SKILL.md breakdown)

---

## Dangerous Contradictions

### 1. Execution logic extraction into reference files risks creating a second monolith problem

**functional-decomposition** recommends extracting all six non-core handlers, multi-round orchestration, preset resolution, the Dispute-Parsing Subsystem, and validation logic into `references/` files (recommendations 1-6), estimating the residual SKILL.md at ~345 lines. The review treats `references/` files as functionally equivalent to inline SKILL.md content: "Reference files in `references/` are first-class citizens of the skill specification — they are not second-class or less authoritative" (Off-Base Assumptions, bullet 1).

**agents-md-specialist** identifies that SKILL.md's execution specification and AGENTS.md's contribution guidance serve fundamentally different audiences and runtimes (Executive Summary, paragraph 2). The concern extends to reference files: the agentskills `references/` mechanism depends on the agent runtime correctly interpreting conditional load triggers. If an agent fails to load a reference (due to ambiguous triggers, context limits, or runtime bugs), the execution specification becomes incomplete. Unlike inline content that is guaranteed to be in context, reference files introduce a dependency on the agent's load behavior.

**The contradiction:** functional-decomposition treats reference file loading as a solved, reliable mechanism and plans the entire decomposition around it. agents-md-specialist's analysis of the AGENTS.md ecosystem reveals that even the simplest file-loading semantics (nearest-file-wins in AGENTS.md) are subject to misinterpretation across runtimes (Off-Base Assumptions, bullet 3). Applying this caution to `references/`: a decomposition that moves 1400+ lines of execution logic into 8-10 conditional reference files creates a fragile load graph where a single missed trigger silently degrades execution. The functional-decomposition review acknowledges this risk only in recommendation 8 ("Without explicit triggers, agents may... fail to load necessary references") but does not treat it as a structural concern that should constrain the decomposition scope.

**Resolution needed:** The decomposition should be staged — extract the most self-contained handlers first (gate, then one guided handler), validate that conditional loading works reliably in practice, and only then proceed to extract tightly coupled subsystems like Dispute-Parsing and multi-round orchestration.

### 2. The Dispute-Parsing Subsystem extraction contradicts the "always in context" principle for cross-cutting invariants

**functional-decomposition** recommends extracting the Dispute-Parsing Subsystem (SKILL.md L750-778) to `references/dispute-parsing.md` as a P1 priority (recommendation 3). The rationale is that it is "a pure function with a stable interface contract" used by four consumers.

**functional-decomposition** also recommends keeping "Important Notes" and "Baseline Features" in SKILL.md because they are "gotchas — the highest-value content type for skills" that "apply to all invocation paths and should always be in context" (recommendation 10). The review cites the agentskills best practices: "gotchas... the highest-value content in many skills."

**agents-md-specialist** identifies the Dispute-Parsing Subsystem as a structural invariant — its markers (`<!-- CONVERSUS:DISPUTES_BEGIN/END -->`) are declared as stable interfaces where "changes... are breaking changes and must be coordinated across all synthesis templates and the parsing subsystem" (SKILL.md L777). This is exactly the kind of cross-cutting, always-relevant content that both reviews agree should remain in context.

**The contradiction:** The Dispute-Parsing Subsystem is simultaneously a "pure function" that functional-decomposition wants to extract and a stable interface contract with breaking-change implications that functional-decomposition's own logic (recommendation 10) says should stay in SKILL.md. The subsystem's 28 lines are modest compared to the gate handler's 300 lines. The token savings from extraction (~400 tokens) do not justify the risk that a consumer handler loads without the parsing contract in context, potentially implementing a divergent parser. functional-decomposition's recommendation 3 directly contradicts its recommendation 10 when applied consistently.

**Resolution needed:** Keep the Dispute-Parsing Subsystem inline in SKILL.md. It is small (28 lines), cross-cutting (4 consumers), and its interface contract has breaking-change semantics — precisely the profile of content that should always be loaded.

### 3. Contribution guidelines treated as execution-irrelevant by functional-decomposition, but they affect execution quality

**functional-decomposition** focuses exclusively on execution-time context efficiency. Its analysis of "conditional relevance" (Off-Base Assumptions, bullet 3) frames the problem purely as: "how much of the loaded content applies to the agent's current task." Every recommendation is about reducing tokens loaded during `/conversus run`, `/conversus define`, etc. Contribution rules (template naming, preset validation, antipattern checks) are not mentioned once.

**agents-md-specialist** identifies that contribution-oriented rules are currently embedded in SKILL.md (recommendation 8): the antipattern check instruction (line 239-244), template naming conventions (line 283-289), preset file validation rules (lines 139-145), and linter invocation (line 309). These are "contribution guidelines currently embedded in an execution spec." The review proposes moving them to AGENTS.md or nested AGENTS.md files.

**The contradiction:** functional-decomposition's token budget analysis (recommendation 9) does not account for contribution-oriented content in SKILL.md because it does not distinguish between execution rules and contribution rules. Its proposed decomposition would scatter these contribution guidelines across `references/` files (preset validation into `references/preset-resolution.md`, template naming into whichever handler reference uses templates). agents-md-specialist's approach would consolidate them into AGENTS.md files where all agents can discover them. These are mutually exclusive destinations for the same content. If functional-decomposition's plan executes first, the contribution guidelines become harder to extract into AGENTS.md because they are interleaved with execution logic in reference files rather than being cleanly identifiable in the monolithic SKILL.md.

**Resolution needed:** Before executing the reference-file decomposition, identify and tag all contribution-oriented lines in SKILL.md. Extract those to AGENTS.md first (a smaller, safer operation), then decompose the remaining execution logic into reference files.

---

## Tensions

### 1. Granularity of extraction: one file per handler vs. shared patterns

**functional-decomposition** proposes one reference file per guided handler: `references/handler-define.md`, `references/handler-interests.md`, `references/handler-mode.md`, `references/handler-converge.md`, `references/handler-arbitrate.md` (recommendation 2). It also proposes a `references/guided-handler-patterns.md` for the shared workflow skeleton (Missed Opportunities, bullet 5) and a `references/validation-contract.md` for shared validation (recommendation 6).

**agents-md-specialist** proposes nested AGENTS.md files per subdirectory (`templates/AGENTS.md`, `presets/AGENTS.md`, `schema/AGENTS.md`, `linter/AGENTS.md`) for contribution guidance (recommendations 1-4).

**The tension:** If both proposals execute, the conversus skill would have ~8 reference files (execution logic) plus ~4 nested AGENTS.md files (contribution logic) plus the root AGENTS.md, SKILL.md, and README.md. This is 14+ agent-facing files for a system that currently has 3. Both reviews individually present reasonable decompositions, but their combined effect risks creating a navigation burden that replaces the monolith problem with a fragmentation problem. Neither review addresses the composite impact.

### 2. Token budget targets: 500-line SKILL.md vs. practical load paths

**functional-decomposition** cites the agentskills spec's 500-line / 5,000-token recommendation repeatedly and builds its decomposition to achieve a ~345-line SKILL.md (recommendation 7). The review's token budget (recommendation 9) shows `/conversus run` with multi-round and arbiter loading ~10.5k tokens across multiple reference files.

**agents-md-specialist** does not engage with the token budget directly but warns that execution logic must stay in SKILL.md (recommendation 6: "Do not move execution logic from SKILL.md to AGENTS.md"). The implicit position is that SKILL.md should contain whatever the execution engine needs, even if that exceeds 500 lines.

**The tension:** The 500-line target is aspirational guidance, not a hard constraint. functional-decomposition optimizes for it aggressively, but the resulting load graph for a complex invocation (`/conversus run` with rounds > 1, arbiter, presets) requires loading 4 reference files totaling ~10.5k tokens — double the 5k target for the activated body. The decomposition meets the letter of the recommendation (SKILL.md is under 500 lines) while violating its spirit (the effective loaded content for a complex run is higher than before because of reference file overhead, load-trigger instructions, and cross-reference boilerplate). agents-md-specialist's silence on token budgets means this tension is unresolved.

### 3. Who is the primary audience: agents executing conversus vs. agents contributing to conversus?

**functional-decomposition** frames the entire review around execution efficiency — reducing the context cost for agents running `/conversus run`, `/conversus define`, etc. The audience is the Claude Code agent executing the conversus skill.

**agents-md-specialist** explicitly identifies two audiences: "agents executing the conversus skill versus agents contributing to the conversus codebase" (Executive Summary, paragraph 1). The review argues that AGENTS.md serves the contribution audience while SKILL.md serves the execution audience, and that the decomposition must preserve this separation.

**The tension:** The spec (011a) does not specify which audience to optimize for. functional-decomposition assumes execution; agents-md-specialist assumes contribution is equally important. The optimal decomposition differs: execution optimization moves content into conditionally-loaded reference files; contribution optimization moves content into universally-discoverable AGENTS.md files. Some content (template naming, validation rules, preset schemas) is relevant to both audiences. The two reviews propose different destinations for this shared content, and neither provides a reconciliation framework.

### 4. Validation logic: centralize once vs. distribute to discovery points

**functional-decomposition** proposes a centralized `references/validation-contract.md` defining the shared validation algorithm, regex patterns, and error formats (recommendation 6). The rationale is DRY: five handlers implement overlapping validation that should be defined once.

**agents-md-specialist** proposes that validation rules for templates, presets, and schemas live in nested AGENTS.md files at the point of contribution (`templates/AGENTS.md`, `presets/AGENTS.md`, `schema/AGENTS.md`). The rationale is discoverability: "an agent editing a preset in Cursor or Copilot has no way to discover these constraints — they are locked inside a Claude Code-specific SKILL.md" (Missed Opportunities, bullet 2).

**The tension:** These are different facets of the same validation rules placed in different files for different audiences. The centralized reference file serves the execution engine (one place to load validation logic). The nested AGENTS.md files serve the contributing agent (validation rules at the edit point). Both are valid, but maintaining validation rules in two locations (reference file for execution, AGENTS.md for contribution) creates a synchronization burden. Neither review addresses how to keep these in sync.

### 5. Antipattern catalog: execution concern or contribution concern?

**functional-decomposition** does not mention the antipattern catalog (`antipatterns/catalog.md`) at all, despite SKILL.md line 239 requiring agents to check it before proposing changes.

**agents-md-specialist** identifies it as a contribution guideline that "belongs in AGENTS.md (or a nested `antipatterns/AGENTS.md`)" (Missed Opportunities, bullet 7) and notes it is an execution-irrelevant rule currently embedded in SKILL.md.

**The tension:** The antipattern check is invoked during execution (agents must read it during `/conversus run` phases) but its content is a contribution-style catalog (patterns to avoid when writing deliverables). This dual nature means it does not cleanly belong in either SKILL.md's execution path or AGENTS.md's contribution guide. functional-decomposition's silence leaves it in SKILL.md by default; agents-md-specialist's proposal to move it to AGENTS.md could make it invisible to the execution engine. The correct home depends on whether the antipattern check is an execution-time instruction (agents read it during deliberation) or a contribution-time instruction (agents read it when editing conversus itself).

---

## Safe Agreements

### 1. SKILL.md is too large and must be decomposed

Both reviews independently arrive at the same diagnosis. functional-decomposition: "the current SKILL.md violates the Single Responsibility Principle at every level" (Executive Summary). agents-md-specialist: "The conversus system currently maintains... `SKILL.md` (119KB, the full orchestration specification)... the decomposition discussion should preserve this separation" (Executive Summary). Neither review defends the status quo. The 2216-line, 31k-token monolith is universally agreed to be the problem.

### 2. The gate handler is the strongest extraction candidate

functional-decomposition identifies it as "the most self-contained handler" (Missed Opportunities, bullet 8) and gives it P1 priority for extraction to `references/gate-handler.md` (recommendation 1). agents-md-specialist does not propose gate-specific extraction (its focus is AGENTS.md), but its principle that execution logic should stay in SKILL.md or reference files (recommendation 6) is fully compatible with this extraction. Neither review raises concerns about the gate handler's independence. Its 300-line, zero-shared-state, no-interactive-prompt profile makes it the lowest-risk extraction target both reviews can endorse.

### 3. SKILL.md and AGENTS.md serve fundamentally different purposes and must not be conflated

agents-md-specialist states this explicitly: "AGENTS.md and SKILL.md serve fundamentally different purposes and should not be viewed as alternatives" (Executive Summary, paragraph 2). functional-decomposition implicitly agrees by never proposing AGENTS.md as a destination for any execution logic — all extraction targets are `references/` files within the agentskills framework. The spec (011a) lists both agents.md and agentskills.io as offloading targets, but both reviews correctly interpret them as complementary channels serving different audiences, not interchangeable containers.

### 4. Conditional load triggers must be explicit and unambiguous

functional-decomposition dedicates recommendation 8 to explicit load-trigger instructions, citing the agentskills best practice against vague references. agents-md-specialist makes the same point from the AGENTS.md perspective: nearest-file-wins semantics work because the trigger is unambiguous (directory proximity), and any decomposition should maintain that clarity (Off-Base Assumptions, bullet 3). Both reviews reject the idea of dumping content into reference files or AGENTS.md files without clear instructions for when and why an agent should read them.

---

## Referenced Documentation

- `conversus/specs/011a-skill-breakdown/conversus-output/functional-decomposition/review.md` — functional-decomposition's Phase 1 review
- `conversus/specs/011a-skill-breakdown/conversus-output/agents-md-specialist/review.md` — agents-md-specialist's Phase 1 review
- `conversus/SKILL.md` — the monolithic execution specification (2216 lines)
- `conversus/specs/011a-skill-breakdown/spec.md` — the decomposition spec
- `conversus/references/agents-md.md` — the agents.md community standard reference
