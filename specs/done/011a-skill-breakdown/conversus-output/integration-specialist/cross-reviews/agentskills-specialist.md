# Cross-Review of agentskills-specialist

Reviewer: **integration-specialist**

---

## Dangerous Contradictions

### DC-1: Run Engine Scope — Monolithic Core vs. Handler-Level Extraction

agentskills-specialist recommends extracting the run engine's detailed phase execution mechanics into `references/handler-run.md` (Recommendation 1), treating `run` as just another handler alongside `define`, `interests`, etc. My review explicitly identifies the run engine as the shared foundation that both `converge` and `gate` delegate into, and recommends keeping the run engine's phase loop in the root SKILL.md (Recommendation 1, 7). These positions directly contradict on where the run engine lives after decomposition.

This matters because agentskills-specialist's approach creates a transitive dependency problem: `handler-converge.md` and `handler-gate.md` would both need to instruct the agent to "also read `handler-run.md`," making the run engine a hidden prerequisite behind two layers of file reads. My review flags that the round loop, iteration loop, output path computation, and termination logic (lines 346-580) form a tightly coupled state machine that does not benefit from extraction. If the run engine goes into a reference file, every invocation path that touches deliberation execution pays a two-file-read tax, and the agent must mentally compose instructions from `SKILL.md` + `handler-run.md` + any subsystem references the run engine calls.

**Risk if unresolved:** If the run engine is extracted as a handler, the root SKILL.md becomes a dispatch table with invariants but no execution semantics. An agent loading SKILL.md for `/conversus converge` would see the dispatch table, load `handler-converge.md`, discover it delegates to the run engine, then load `handler-run.md` — three files before execution begins. This reference-chasing degrades the progressive disclosure model into a scavenger hunt.

### DC-2: Token Budget Target vs. Engine Retention

agentskills-specialist targets a root SKILL.md of "~350 lines, under 5,000 tokens" (Recommendation 2, proposed layout). My review targets "~400-500 lines covering dispatch + invariants + engine" (Recommendation 1). These are incompatible targets. The run engine's phase execution alone (lines 346-580) is approximately 235 lines. Combined with the dispatch table (~25 lines), multi-agent rules (~15 lines), and gotchas, keeping the engine in SKILL.md pushes the root file to 400-500 lines and likely 6,000-8,000 tokens — well above the 5,000 token ceiling agentskills-specialist derives from the specification.

agentskills-specialist's token analysis (Off-Base Assumptions, point 4) correctly notes that token density matters more than line count. But this insight cuts both ways: if the root SKILL.md must stay under 5,000 tokens, then the run engine cannot stay in it. If the run engine must stay in it (for the coupling reasons I identify), then the 5,000 token target is not achievable. One of these constraints must yield.

**Risk if unresolved:** Pursuing both goals simultaneously produces either a root SKILL.md that exceeds the token budget (violating agentskills-specialist's primary recommendation) or a root SKILL.md that lacks engine semantics (creating the transitive dependency problem I flag). The implementation team needs an explicit decision on which constraint takes priority.

### DC-3: Template Variables — Eliminate Redundancy vs. Preserve Co-location

agentskills-specialist recommends consolidating all template variable documentation into `references/template-variables.md` (Recommendation 4), noting that the current inline documentation is "duplicative with `schema/variables.yml`." My review recommends extracting template variable documentation to `references/contract-template-variables.md` (Recommendation 6) but frames it as a companion to the schema, not a replacement for inline phase-specific context. More critically, my review identifies that the run engine's phase execution depends on knowing which variables are available in each phase — this is not reference material but execution context.

If template variables are fully extracted, an agent executing Phase 2 must: (a) read the phase template from `templates/{mode}/phase2_cross_review.md`, (b) read `references/template-variables.md` to know which variables to fill, (c) read `schema/variables.yml` for the machine-readable contract. This is three files to fill one template. Currently the agent reads the SKILL.md (which lists phase-specific variables inline) and the template file — two reads.

**Risk if unresolved:** Full extraction saves tokens on activation but adds per-phase file reads during execution. Since conversus runs 5-6 phases with multiple agents per phase, the cumulative file-read cost during a single deliberation could be substantial. The variable extraction must be evaluated on execution-time cost, not just activation-time token savings.

### DC-4: Antipattern Check Placement After Decomposition

agentskills-specialist's review does not address the `antipatterns/catalog.md` integration at all. My review (Missed Opportunities, point 3) flags that the Antipattern Check (lines 237-244) is a pre-execution step that reads from a separate catalog file, and asks whether each extracted handler needs its own antipattern check or whether this is an orchestrator-level concern. This is not merely a missed topic — it is a decomposition decision that changes the handler interface contract.

If antipattern checking stays in the root SKILL.md as an orchestrator concern, then every handler reference file assumes it has already been run. If it moves into handler files, then some handlers (like `define`, which does not run the full engine) would gain an antipattern check they currently lack. agentskills-specialist's proposed layout (Recommendation 10) does not include antipatterns in any reference file or address their placement.

**Risk if unresolved:** After decomposition, an agent loading `handler-run.md` directly (bypassing the root SKILL.md dispatch flow due to context or error) could skip the antipattern check entirely. The placement must be explicit in the decomposition plan.

---

## Tensions

### T-1: Prescriptive File Layout vs. Organic Seam Discovery

agentskills-specialist proposes a comprehensive 14-reference-file layout (Recommendation 10) derived top-down from the agentskills.io specification's progressive disclosure model. My review proposes a smaller set of extractions (7 handler files + 3 subsystem files + 1 contract file) derived bottom-up from analyzing the SKILL.md's internal coupling. The agentskills-specialist layout includes files my review does not recommend (`multi-round-execution.md`, `operational-notes.md`, `arbitration-engine.md` as a separate file from the handler), while my review includes a dependency map (Recommendation 10) that agentskills-specialist's layout does not.

Both approaches have merit. The top-down approach ensures compliance with agentskills.io best practices. The bottom-up approach ensures decomposition boundaries align with actual coupling seams. The tension is whether to decompose until the standard is met or decompose until the seams are exhausted.

### T-2: Naming Convention — Flat vs. Typed Prefixes

agentskills-specialist proposes flat naming in `references/`: `handler-run.md`, `dispute-parsing.md`, `template-variables.md`, `preset-resolution.md` (Recommendation 1, 3, 4, 7). My review proposes typed prefixes: `handler-{name}.md`, `subsystem-{name}.md`, `contract-{name}.md` (Recommendation 9). Both reviews agree on extracting the same content to the same directory; they disagree on whether the file name should encode the file's role in the dependency graph.

My convention makes the dependency topology legible from `ls references/` — you can immediately see which files are entry points (handlers), which are shared subsystems, and which are contracts. agentskills-specialist's convention is simpler and avoids a taxonomy that may not scale. The tension is readability-of-structure vs. simplicity-of-naming.

### T-3: Linter Expansion — Integration Test vs. Documentation Companion

My review (Recommendation 8) mandates expanding `linter/validate.py` to validate reference file consistency after decomposition — checking that variables in handler files match `schema/variables.yml`, error messages match a canonical catalogue, and subsystem interfaces are consistent with call sites. agentskills-specialist does not address the linter's post-decomposition role at all, instead recommending that the existing `schema/variables.yml` and `linter/validate.py` serve as evidence that decomposition works (Alignment, point 4).

These are complementary but in tension on scope. agentskills-specialist treats the linter as proof that stable seams exist; I treat it as the mechanism that prevents decomposition from introducing drift. If the linter scope is not expanded, the new reference files become untested — exactly the kind of specification-without-validation that the existing linter was created to prevent.

### T-4: Error Message Contracts — Implicit vs. Explicit

My review (Missed Opportunities, point 6) raises error message strings as an interface contract concern: if validation logic moves to reference files, exact error message formats become part of the cross-file interface. agentskills-specialist proposes consolidating validation rules into `references/validation-rules.md` (Recommendation 5) but frames this as eliminating repetition, not as defining an interface contract.

The tension: agentskills-specialist sees shared validation as a deduplication opportunity (reducing SKILL.md size). I see it as an interface contract that must be explicitly versioned and tested. Both are true, but the implementation differs — deduplication suggests a shared reference file, while contract management suggests the linter should enforce it.

### T-5: What "Progressive Disclosure" Means for Multi-Phase Execution

agentskills-specialist frames progressive disclosure as subcommand-level: load the handler you need, skip the rest (Recommendation 1, 9). My review frames it as layer-level: the engine is always loaded because every execution path uses it, while handlers are loaded on demand (Recommendation 1). This reflects a deeper tension about what the "unit of disclosure" is for conversus.

For most agentskills.io skills, the unit is the subcommand — the user picks one, the agent loads its instructions. For conversus, the `run` engine is not a subcommand peer but a shared runtime that multiple subcommands invoke. agentskills-specialist's model works if each handler is self-contained; my model works if handlers are thin wrappers around a shared core. The SKILL.md's actual structure (where `converge` and `gate` both delegate to the run engine) supports the layered model, but the agentskills.io specification was written for the handler model.

---

## Safe Agreements

### SA-1: Subcommand Handlers Should Be Extracted to Reference Files

Both reviews agree without reservation that the seven subcommand handlers (define, interests, mode, converge, arbitrate, gate, and the run handler's non-engine portions) should become individual reference files loaded on demand from the dispatch table. agentskills-specialist: "Extract each subcommand handler to its own reference file" (Recommendation 1). My review: "Extract each guided workflow handler... to `references/handler-{name}.md`" (Recommendations 2, 3). The handlers have clean interfaces (file inputs, file outputs, no shared in-memory state), making this the lowest-risk decomposition.

### SA-2: Multi-Agent Isolation Rules Must Remain in Root SKILL.md

Both reviews identify the non-negotiable multi-agent rules (lines 324-336) as the highest-fragility content that must be front-loaded in every agent's context. agentskills-specialist: "The non-negotiable multi-agent rules correctly apply 'match specificity to fragility'" and recommends keeping them in the core (Recommendation 2c). My review: "These rules should remain in the root SKILL.md rather than being buried in a reference file, because they are the most important constraint an implementing agent must internalize" (Alignment, point 6; Recommendation 1). No disagreement exists on this point.

### SA-3: The Dispute-Parsing Subsystem Is a Natural Extraction Candidate

Both reviews identify the Dispute-Parsing Subsystem (lines 750-778) as having an explicitly documented stable interface that makes it a textbook reference file candidate. agentskills-specialist: "It has a declared 'stable interface contract'... This is a textbook candidate for extraction" (Missed Opportunities, point 2). My review: "This subsystem already has an explicitly documented stable interface... it is called from three sites" (Alignment, point 4; Recommendation 4). Both reviews agree on the interface boundaries (input: synthesis path; output: boolean + integer) and that the extraction is low-risk.

### SA-4: The Dispatch Table Is the Correct Anchor for Root SKILL.md

Both reviews agree that the subcommand dispatch table (lines 22-44) should remain as the entry point in the root SKILL.md, serving as the routing contract that directs agents to the appropriate handler reference file. agentskills-specialist calls it "an exemplary implementation of the 'provide defaults, not menus' pattern" (Alignment, point 2). My review calls it "the correct anchor for SKILL.md" (Alignment, point 1). The dispatch table is the one structure both reviews treat as settled.

---

## Referenced Documentation

- agentskills-specialist review: `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/conversus-output/agentskills-specialist/review.md`
- integration-specialist review: `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/conversus-output/integration-specialist/review.md`
- Target SKILL.md: `<HOME>/code/payer-index-mono/conversus/SKILL.md`
- Spec 011a: `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/spec.md`
- Conversus README: `<HOME>/code/payer-index-mono/conversus/README.md`
