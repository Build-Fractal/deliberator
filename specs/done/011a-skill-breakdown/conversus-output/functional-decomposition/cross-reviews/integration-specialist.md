# Cross-Review: functional-decomposition reviewing integration-specialist

## Dangerous Contradictions

### 1. Run engine in SKILL.md: ~400-500 lines (integration-specialist) vs ~265 lines (functional-decomposition)

Integration-specialist recommends keeping the full run engine core — including the multi-round loop, the phase execution block, and the round-aware output path computation — in the root SKILL.md (Actionable Recommendation 1: "run engine's phase loop (Phases 1-6, round loop, iteration loop, termination conditions) has tight internal coupling that does not benefit from decomposition. Estimate: root SKILL.md at ~400-500 lines"). Functional-decomposition recommends extracting multi-round orchestration (~360 lines) and preset resolution (~75 lines) out of the run engine into conditional references, leaving a ~265-line engine core in SKILL.md (Recommendations 4, 5, 7).

These estimates produce radically different root files. Integration-specialist's approach yields a ~400-500 line SKILL.md before adding the dispatch table, notes, and frontmatter — potentially hitting 550-600 lines, still above the 500-line recommendation. Functional-decomposition's approach yields ~345 lines total. If the implementation follows integration-specialist, the decomposition may not meaningfully reduce per-invocation context load for the common single-round case (where ~360 lines of multi-round logic are irrelevant). If it follows functional-decomposition, integration-specialist's concern about splitting tightly coupled state (round counters, output path formulas, termination logic) becomes a real integration risk — a bug in the handoff between SKILL.md and `references/multi-round-orchestration.md` could produce incorrect output paths.

This is the most consequential disagreement. It determines whether the decomposition achieves its stated goal (context reduction) or merely reorganizes code at the margins.

### 2. Dispute-Parsing Subsystem: extract to reference (functional-decomposition P1) vs extract but keep as "do not further decompose" boundary (integration-specialist)

Both reviews agree on extracting the Dispute-Parsing Subsystem to `references/`. However, integration-specialist treats it as a self-contained stable-interface unit with a "do not decompose" marker on its internals (Actionable Recommendation 4: "Mark these as breaking-change boundaries"), while functional-decomposition treats it as a pure function that should be loaded on demand with a clear trigger ("when you need to count disputes in a synthesis file, read `references/dispute-parsing.md`" — Recommendation 3).

The contradiction is in the loading model. Integration-specialist implies the subsystem reference is loaded whenever any consumer needs it — and the consumer list spans the run engine, the converge handler, and the gate handler. If three different reference files all contain the instruction "read `references/dispute-parsing.md`," the agent may load it three times, or may load it in one handler's context but not have it available when another handler's logic within the same run needs it. Functional-decomposition's on-demand trigger model assumes the agent can selectively load mid-execution, but if the run engine itself is in SKILL.md (not a reference file), the load-trigger for dispute parsing would need to be embedded in the always-loaded SKILL.md body — partially defeating the extraction.

### 3. Guided handler shared patterns: extract shared skeleton (functional-decomposition) vs keep handlers independent (integration-specialist)

Functional-decomposition identifies a missed opportunity: the five guided handlers all implement an identical workflow skeleton (check prerequisites, ingest input, validate, present for confirmation, write, post-write validate, report) and proposes a `references/guided-handler-patterns.md` to define the shared pattern once (Missed Opportunities, bullet 5). Integration-specialist explicitly frames the handlers as independent units with no shared in-memory state, proposing each as a standalone `references/handler-{name}.md` without a shared pattern reference (Recommendation 2: "Each handler has a clean interface... There is no shared in-memory state between handlers").

If both proposals are implemented naively, each extracted handler reference would need to either (a) duplicate the workflow skeleton inline, creating the validation drift that functional-decomposition warns about, or (b) reference `guided-handler-patterns.md`, creating a two-level reference chain (SKILL.md dispatch -> handler reference -> pattern reference) that integration-specialist does not account for in the dependency map (Recommendation 10). A two-level reference chain means the agent must load two files to execute a single guided command, and the pattern reference becomes a hidden coupling point between handlers that integration-specialist's architecture treats as independent.

### 4. Validation contract centralization vs handler independence

Functional-decomposition recommends a shared `references/validation-contract.md` that centralizes heading checks, name pattern regex, and post-write validation across all handlers (Recommendation 6). Integration-specialist does not mention validation consolidation and instead proposes that error message contracts be addressed at the interface level (Missed Opportunities: "If validation logic moves to reference files, these error messages become part of the interface contract").

These approaches conflict on where validation logic lives. Functional-decomposition's centralized validation contract creates a dependency from every handler reference file to a shared validation reference — a fan-in pattern that contradicts integration-specialist's handler-independence model. Integration-specialist's error-message-as-interface approach implies each handler owns its own validation, with consistency enforced by the linter (Recommendation 8) rather than by structural sharing. If the centralized contract is adopted, the linter's scope narrows (it validates one file, not N copies). If the distributed model is adopted, the linter must validate N independent implementations against a canonical spec — which is the harder engineering problem but preserves handler isolation.

## Tensions

### 1. "Change isolation" framing (integration-specialist) vs "conditional relevance" framing (functional-decomposition)

Integration-specialist frames the primary benefit of decomposition as change isolation: "any change to the gate handler requires re-reading the full run engine" (Off-Base Assumptions). Functional-decomposition frames the primary benefit as conditional relevance: "a `/conversus define` invocation loads 31k tokens but uses ~2k" (Off-Base Assumptions). Both are valid but optimize for different stakeholders — change isolation serves the developer editing SKILL.md, conditional relevance serves the agent executing at runtime. A decomposition optimized for change isolation might keep the multi-round logic in SKILL.md (it changes rarely, and co-locating it prevents engine-level drift) even though it wastes context. A decomposition optimized for conditional relevance would aggressively extract anything not needed for the current invocation, even at the cost of more reference-file boundaries to maintain.

These framings are not mutually exclusive but they pull in different directions when deciding borderline cases like multi-round orchestration.

### 2. Layered architecture (integration-specialist) vs flat dispatch (functional-decomposition)

Integration-specialist identifies a layered architecture: "the run engine is the foundation; the guided workflow is a UX layer... the gate handler is a CI/CD layer" (Off-Base Assumptions). Functional-decomposition treats all subcommands as peers routed through a flat dispatch table. This tension surfaces in how the converge and gate handlers are modeled — integration-specialist says they are thin wrappers that delegate to the engine (implying the engine is a dependency they call down into), while functional-decomposition treats them as self-contained units that happen to invoke the run engine as a subroutine.

The practical impact: if a future spec adds a new layer (e.g., a "monitor" layer that watches run engine execution), integration-specialist's model would place it alongside gate and converge as an upper-layer consumer. Functional-decomposition's model would add it as another peer handler with its own reference file and dispatch entry. The layered model is more prescriptive about what can depend on what; the flat model is more flexible but provides less guidance on dependency direction.

### 3. Naming convention prescriptiveness

Integration-specialist proposes a three-tier naming convention: `handler-{name}.md` for subcommands, `subsystem-{name}.md` for shared subsystems, `contract-{name}.md` for interface contracts (Recommendation 9). Functional-decomposition uses a simpler two-tier convention: `handler-{name}.md` for subcommands and descriptive names for everything else (`dispute-parsing.md`, `preset-resolution.md`, `validation-contract.md`, `multi-round-orchestration.md`).

The tension is between navigability and simplicity. Integration-specialist's convention makes the dependency graph legible from directory listing alone — you can immediately tell which files are handlers, which are shared subsystems, and which are contracts. Functional-decomposition's convention is lighter weight but requires reading the files (or the SKILL.md dependency map) to understand their roles. For a system with 8-10 reference files, the navigability benefit is modest. If the reference directory grows to 15-20 files, the prefix convention becomes more valuable.

### 4. Linter scope expansion: integration test (integration-specialist) vs not addressed (functional-decomposition)

Integration-specialist recommends expanding the linter to validate cross-file consistency after decomposition — checking that handler reference files' variables match `schema/variables.yml`, error messages match a canonical catalogue, and subsystem interface contracts match call sites (Recommendation 8). Functional-decomposition does not address linter expansion, instead treating the existing `linter/validate.py` and `schema/variables.yml` as proven stable seams that already handle cross-artifact consistency.

The tension: integration-specialist's proposal adds significant scope to the linter, turning it from a template-variable validator into a full integration test suite for the decomposed SKILL.md. This is engineering work that the spec (011a) does not scope and that functional-decomposition does not require. If the linter is not expanded, integration-specialist's concern about decomposition-induced drift is valid — but if it is expanded, the linter itself becomes a maintenance burden that must be updated every time a reference file is added or modified.

### 5. Token budget documentation (functional-decomposition P3) vs dependency map (integration-specialist)

Functional-decomposition recommends documenting expected token load per invocation path (Recommendation 9), making the 5,000-token-per-invocation target verifiable. Integration-specialist recommends a dependency map table showing which reference files depend on which (Recommendation 10). Both are documentation artifacts added to the decomposed SKILL.md, but they serve different purposes — token budgets enable performance regression detection, dependency maps enable circular-dependency detection. Including both adds ~20-30 lines of non-instructional content to SKILL.md, which tensions with the goal of keeping the root file lean.

## Safe Agreements

### 1. Subcommand dispatch table stays in SKILL.md; handlers extract to references

Both reviews agree that the dispatch table (L22-44) is the correct anchor for the root SKILL.md and that each subcommand handler should be extracted to its own reference file. Integration-specialist: "Decomposition proposals that preserve this table as the entry point in the root SKILL.md, with handlers referenced rather than inlined, align with progressive disclosure" (Alignment, bullet 1). Functional-decomposition: "Extract each to its own reference file... SKILL.md dispatch table entries become: 'When `/conversus define` is invoked, read `references/handler-define.md`'" (Recommendation 2). The naming convention (`handler-{name}.md`) and the file-mediated coupling model (handlers communicate via disk artifacts, not in-memory state) are also consistent across both reviews.

### 2. Multi-agent isolation rules must stay in the always-loaded root SKILL.md

Both reviews independently identify the NON-NEGOTIABLE MULTI-AGENT RULES (L324-336) as content that must not be extracted. Integration-specialist: "These rules should remain in the root SKILL.md rather than being buried in a reference file, because they are the most important constraint an implementing agent must internalize" (Alignment, bullet 6). Functional-decomposition: "These five rules are cross-cutting invariants that apply to all phases... This is a gotchas section — the highest-value content type" (Alignment, bullet 5). Both cite the agentskills best practices principle that gotchas belong in the always-loaded body.

### 3. Gate handler is the strongest extraction candidate

Both reviews identify the gate handler as the highest-priority extraction target. Integration-specialist: "Extract the gate handler to `references/handler-gate.md`... its only coupling to the run engine is 'generate a `conversus.yml` and invoke Step 1-5'" (Recommendation 3). Functional-decomposition: "The gate handler is the most self-contained handler... the strongest candidate for full extraction" (Missed Opportunities, bullet 8) and Recommendation 1 (P1). The gate handler's self-containment, its 298-line size, and its CI/CD-focused use case (rarely invoked during interactive workflows) make this a safe, high-impact extraction with no disagreement on boundaries or interface contracts.

### 4. The Dispute-Parsing Subsystem is a natural extraction boundary with a proven stable interface

Both reviews agree that the Dispute-Parsing Subsystem (L750-778) should be extracted to a reference file, that its stable interface contract (markers + headings) defines the extraction boundary, and that changes to markers or headings constitute breaking changes. The disagreement noted in Dangerous Contradictions above is about the loading model, not about whether extraction is appropriate. The subsystem's pure-function nature (input: path, output: boolean + integer) and its explicit stability declaration make it the lowest-risk shared-subsystem extraction in the entire decomposition.
