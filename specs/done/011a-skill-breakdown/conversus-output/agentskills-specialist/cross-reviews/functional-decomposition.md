# Cross-Review: functional-decomposition

Reviewer: **agentskills-specialist**
Target: functional-decomposition's Phase 1 review of spec 011a (SKILL.md breakdown)

---

## Dangerous Contradictions

### 1. Whether to extract the run engine core or keep it in SKILL.md

functional-decomposition recommends keeping approximately 265 lines of run engine core in SKILL.md (recommendation 7: "Retain the run engine core (~400 lines) in SKILL.md"), arguing that over-extraction would "force `/conversus run` to load 3-4 reference files on every invocation, potentially causing the agent to miss critical orchestration rules." My review (agentskills-specialist, recommendation 1) proposes extracting each subcommand handler -- including the run handler -- to its own reference file (`references/handler-run.md`), leaving only the dispatch table, invariants, phase-level summary, and gotchas in SKILL.md.

This is a genuine conflict in decomposition strategy. functional-decomposition's approach yields a SKILL.md of approximately 345 lines with 265 lines of run engine detail that loads on every invocation regardless of subcommand. My approach yields a SKILL.md of approximately 300 lines with run engine details loading only when `/conversus run` is invoked. The agentskills specification says "under 500 lines" and "under 5,000 tokens" (agentskills-spec.md, L384-387). functional-decomposition's 345-line SKILL.md likely meets the line target but may exceed the token target due to the density of the retained run engine prose. My approach meets both targets but requires one additional file read on `/conversus run` invocations.

The risk on functional-decomposition's side: `/conversus define` and `/conversus interests` users pay context cost for 265 lines of run engine orchestration they never use. The risk on my side: the run engine is the only handler that `/conversus converge` and `/conversus gate` both delegate into, so extracting it adds a mandatory reference load to three invocation paths. This tension must be resolved by measuring whether the retained run engine core pushes the SKILL.md body above the 5,000-token recommendation. If it does, extraction wins. If the 265 lines fit under 5,000 tokens, functional-decomposition's approach is more conservative and defensible.

### 2. Whether output schema templates should move to assets/ or stay in handler reference files

My review (agentskills-specialist, recommendation 6) proposes moving output schema templates (problem.md schema, interests.md schema, gate-result.md schema) to `assets/` as separate files, following the agentskills best practices guidance: "Short templates can live inline in SKILL.md; for longer templates, or templates only needed in certain cases, store them in `assets/`" (agentskills-best-practices.md, L283). functional-decomposition does not mention `assets/` at all. Its recommendation 2 extracts the guided handlers to `references/handler-*.md` files, which implicitly bundles each handler's output schema within its reference file.

This is a structural disagreement about granularity. functional-decomposition treats each handler as the atomic extraction unit -- the handler reference file contains everything the handler needs, including its output schemas. My approach further decomposes the handler into instructions (in `references/`) and templates (in `assets/`), which means the handler reference file must cross-reference an asset file, adding a second file read per invocation.

functional-decomposition's approach is simpler and keeps each handler self-contained. My approach follows the agentskills specification's directory semantics more literally (`assets/` for templates, `references/` for instructions) and enables schema reuse if multiple handlers share output structures. However, the conversus handlers do not currently share output schemas -- each produces a unique artifact. If no sharing exists, the additional indirection is overhead without benefit. I concede that functional-decomposition's implicit bundling is more pragmatic for the current state of the codebase, though my approach would become necessary if schemas begin to be shared.

### 3. Treatment of "Important Notes" and agent count formulas

functional-decomposition (recommendation 10) says to preserve the entire "Important Notes" and "Baseline Features" sections in SKILL.md, calling them "gotchas -- the highest-value content type for skills." My review (agentskills-specialist, recommendations 2 and 8) distinguishes between genuine gotchas (re-run overwrites, background dispatch semantics) that should stay in SKILL.md and reference material (agent count formulas, round/iteration orthogonality explanation, worked examples) that should move to `references/operational-notes.md`. My Off-Base Assumptions section specifically flags the inline formulas: "The worked examples ('For 3 agents without arbiter: 16 total agent launches') are helpful for human readers of the spec but redundant for an agent executing the skill."

This is a disagreement about what constitutes a gotcha versus reference material. functional-decomposition correctly identifies that gotchas belong in SKILL.md per agentskills-best-practices.md L255-279 ("Keep gotchas in SKILL.md where the agent reads them before encountering the situation"). But it applies this classification too broadly. The agent count formula `N^2 + 2N + 1` is derivable arithmetic, not an environment-specific fact that defies reasonable assumptions. The best practices definition of gotchas is explicit: "concrete corrections to mistakes the agent will make without being told otherwise" (L257). An LLM will not incorrectly compute agent counts from a phase structure it is currently executing -- this is not a gotcha, it is documentation. Keeping derivable formulas in the always-loaded core wastes tokens on every invocation. However, functional-decomposition has a legitimate counter-argument: if the formulas are removed and the agent miscounts, the consequences (launching wrong number of agents) are severe. The resolution depends on empirical testing of whether the agent correctly derives counts without the formulas.

### 4. Whether validation rules warrant their own reference file

Both reviews identify validation duplication as a problem. functional-decomposition (recommendation 6) proposes `references/validation-contract.md` defining shared heading checks, name pattern regex, path existence checks, and post-write validation patterns. My review (agentskills-specialist, recommendation 5) proposes `references/validation-rules.md` with essentially the same content. However, the contradiction lies in the scope and the load trigger.

functional-decomposition scopes it as a "contract" that handlers reference to specify only their unique schema, implying the validation file is loaded on every handler invocation. My review scopes it as a consolidation that each handler file references: "Apply the standard validation rules from `references/validation-rules.md`." In functional-decomposition's model, the validation contract loads alongside the handler reference file -- two files per invocation. In my model, it loads on demand from within the handler reference file -- potentially the same two files, but with the trigger embedded in the handler rather than in SKILL.md.

The danger is subtle: if validation-rules.md is referenced from SKILL.md directly (as functional-decomposition implies with "handlers reference the shared contract and specifies only its unique schema"), it may load eagerly on every invocation. If it is referenced from each handler reference file (my approach), it loads only when a handler invocation triggers it. The agentskills best practices are clear that load triggers should be specific, not generic (L156). functional-decomposition's framing risks making the validation file part of the always-loaded set, which partially negates the decomposition benefit.

---

## Tensions

### 1. Token budget analysis: aspiration versus enforcement

functional-decomposition (recommendation 9) proposes documenting a "Context Budget" section in the decomposed SKILL.md with per-invocation-path token estimates. My review does not propose a token budget section but does note (Off-Base Assumptions, point 4) that "The target should be token-aware, not just line-aware." We agree on the importance of tokens over lines, but disagree on the mechanism. functional-decomposition wants a documented budget that humans maintain; I implicitly rely on the agentskills specification's 5,000-token guideline as the enforcement mechanism.

functional-decomposition's approach is more rigorous: a documented budget makes regressions visible and provides a concrete target for future additions. My approach is lighter but depends on someone remembering to check. The tension is between operational overhead (maintaining token counts across every reference file after every edit) and correctness (knowing when you have exceeded the budget). A reasonable middle ground would be to document the budget once at decomposition time and check it during major revisions, rather than maintaining it as a living document.

### 2. Extraction granularity: seven handler files versus fewer logical groupings

functional-decomposition proposes extracting five handlers to references (define, interests, mode, converge, arbitrate) plus the gate handler, yielding six new handler reference files alongside the retained run engine core. My review proposes seven handler reference files (including handler-run.md). Beyond the run engine disagreement (addressed in Dangerous Contradictions 1), there is a subtler tension: functional-decomposition implicitly groups the guided workflow handlers as peers but does not explore whether any of them could be merged.

The converge handler is a thin wrapper around the run engine -- it reads config, validates prerequisites, delegates to `/conversus run`, and produces a post-execution report. The arbitrate handler similarly delegates to the run engine with arbiter-specific configuration. If these are extracted to their own reference files, the agent loads `references/handler-converge.md`, which says "now run the run engine" -- and the agent must then also have the run engine in context. functional-decomposition addresses this by keeping the run engine in SKILL.md, so it is always available. My approach requires converge and arbitrate to trigger loading of handler-run.md, creating a two-file chain. Neither review explores the option of embedding converge and arbitrate instructions within handler-run.md as subsections, which would reduce file count at the cost of loading arbitrate logic on pure run invocations.

### 3. The Dispute-Parsing Subsystem's location relative to the run engine

Both reviews agree on extracting the Dispute-Parsing Subsystem to `references/dispute-parsing.md`. The tension is in how this interacts with the run engine. functional-decomposition keeps the run engine core in SKILL.md and extracts dispute parsing to a reference, meaning the run engine's Phase 6 trigger logic must reference an external file for the dispute detection algorithm. My review extracts the entire run handler, so dispute parsing is one of several reference files the run handler loads.

In functional-decomposition's model, the always-loaded SKILL.md says something like "evaluate disputes using references/dispute-parsing.md" at the Phase 6 trigger point within the retained run engine core. This is clean but creates an asymmetry: most of the run engine is inline, but one subsystem is external. In my model, the run handler reference file references dispute-parsing.md, creating a two-level reference chain (SKILL.md -> handler-run.md -> dispute-parsing.md). The agentskills specification does not prohibit chained references, but it also does not explicitly endorse them. The tension is between uniformity (everything referenced from one level) and the practical observation that the Dispute-Parsing Subsystem is a shared concern used by four consumers at different levels of the reference hierarchy.

### 4. How to handle preset resolution's conditional trigger

Both reviews propose extracting preset resolution to `references/preset-resolution.md`. functional-decomposition specifies the trigger as: "If any agent entry (or arbiter entry) has a `preset` field, read `references/preset-resolution.md`." My review specifies: "If any agent entry contains a `preset` field, read `references/preset-resolution.md` for resolution rules." These are nearly identical, but the tension emerges in where the trigger instruction lives.

functional-decomposition places it in the config parsing section of the retained SKILL.md run engine core. My review, having extracted the run engine, would place it in `references/handler-run.md`. If the gate handler also uses presets (it generates a `conversus.yml` that may contain preset references), the trigger must also appear in `references/handler-gate.md`. functional-decomposition's centralized approach means the trigger appears once in SKILL.md; my distributed approach means it appears in each handler reference that might encounter presets. The centralized approach is DRY but only works if the config parsing section is always in context (which functional-decomposition achieves by keeping the run engine in SKILL.md). The distributed approach is repetitive but robust to handler-specific invocation paths.

### 5. Whether the multi-round extraction boundary is clean enough

Both reviews agree on extracting multi-round orchestration to `references/multi-round-orchestration.md`. The tension is in how cleanly the multi-round logic separates from the single-round logic. functional-decomposition identifies lines 248-610 (~360 lines) as the extraction target. But the run engine's Phase 5 synthesis (which produces the dispute input for the Dispute-Parsing Subsystem) references round-specific directory structures even in single-round mode (retroactive Round 1 moves, per functional-decomposition's own analysis). If Phase 5 synthesis logic is interleaved with multi-round concerns, the extraction boundary is not as clean as both reviews assume.

Neither review performs a dependency analysis to verify that the multi-round logic can be extracted without duplicating single-round path references. If the extraction requires duplicating directory management rules in both the retained SKILL.md and the multi-round reference file, the decomposition creates maintenance risk: changes to directory structure must be synchronized across two files. This is the same drift risk both reviews warn about for validation rules, but neither applies the concern to the multi-round extraction.

---

## Safe Agreements

### 1. The gate handler is the highest-priority extraction candidate

functional-decomposition identifies this as recommendation 1 (P1 priority) and calls it "the strongest candidate for full extraction to `references/gate-handler.md`." My review identifies it as a missed opportunity and includes it in recommendation 1's comprehensive handler extraction. Both reviews cite the same evidence: the gate handler is approximately 300 lines, entirely self-contained, serves a different audience (CI/CD pipeline authors), has no interactive prompts, shares no state with guided handlers, and is invoked only on `/conversus gate`. Both reviews agree the load trigger is unambiguous. The agentskills best practices support this unanimously: the gate handler is reference material that should load on demand.

### 2. The dispatch table and non-negotiable multi-agent rules must remain in SKILL.md

functional-decomposition (Alignment section, recommendations 7 and 10) and my review (Alignment section, recommendation 2) both identify the dispatch table (lines 22-44) and the non-negotiable multi-agent rules (lines 324-336) as content that must remain in the always-loaded SKILL.md core. Both reviews cite the same agentskills best practices rationale: these are high-fragility invariants that apply to every invocation path and would be dangerous to externalize. The dispatch table is the routing mechanism; removing it would prevent the skill from functioning. The multi-agent rules are the highest-fragility instructions in the skill; violating them produces correlated outputs that defeat the deliberation's purpose. Neither review suggests extracting either of these, and both cite the same best practices guidance on matching specificity to fragility.

### 3. Conditional load triggers must be specific, not generic

functional-decomposition (recommendation 8) and my review (recommendation 9) both insist that every extracted reference file must have an unambiguous, specific load trigger. Both cite agentskills-best-practices.md L156: "'Read `references/api-errors.md` if the API returns a non-200 status code' is more useful than a generic 'see references/ for details.'" Both provide concrete examples of well-formed triggers (e.g., "When `/conversus gate` is invoked, read `references/gate-handler.md`" and "If config `rounds` > 1, read `references/multi-round-execution.md`"). This agreement is important because it establishes the quality standard for the decomposition's load instructions -- the restructuring only works if every reference file has a trigger that is both necessary and sufficient.

### 4. The decomposition is a content reorganization, not a technology migration

functional-decomposition (Off-Base Assumptions, point 2) explicitly states: "the most impactful decomposition requires no tooling changes -- it is purely structural, moving sections of SKILL.md into `references/` files and adding conditional load instructions." My review (Off-Base Assumptions, point 1) makes the same observation: "The agent is already doing file I/O on every run. Adding `references/handler-run.md` to the read list is not a new capability -- it is a refinement of existing behavior." Both reviews reject spec 011a's framing that external tooling (apm, openspec.dev) is needed to address the SKILL.md size problem. The infrastructure for progressive disclosure already exists in the conversus skill structure; the `references/` directory contains five files. The decomposition leverages existing agentskills.io patterns with no new dependencies.
