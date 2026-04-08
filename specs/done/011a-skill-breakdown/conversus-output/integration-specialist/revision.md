# Integration Specialist — Revised Position (Iteration 1)

## Recommendation Dispositions

### Original Recommendation 1: Keep dispatch table, multi-agent isolation rules, and run engine core in root SKILL.md (~400-500 lines)

**MODIFIED.** This was the most contested recommendation. All four cross-reviewers challenged keeping the full run engine in the root SKILL.md. The arguments fall into two categories:

*Token budget violation.* agentskills-specialist and functional-decomposition both demonstrate that 400-500 lines of dense specification prose translates to 6,000-8,000 tokens, exceeding the agentskills.io 5,000-token recommendation. My original review dismissed the token target as secondary to change isolation, but the cross-reviews correctly argue that an agent invoking `/conversus define` should not pay 6,000+ tokens for run engine internals it will never execute. I underweighted the per-invocation cost for non-engine subcommands.

*Co-location does not require root-level placement.* agentskills-specialist makes a sharp point: "the solution is to keep those tightly coupled elements together in `references/handler-run.md`, not to keep them in the root SKILL.md." I concede this. My "do not decompose" argument was about internal cohesion within the engine, not about the engine's position in the file hierarchy. The round loop, iteration loop, output path computation, and termination logic must remain a single unit, but that unit can be a reference file rather than root-level content.

**Revised position:** The root SKILL.md retains the dispatch table, multi-agent isolation rules, a phase-level summary of the run engine (one paragraph per phase, not full template variable specs), and gotchas/important notes. Target: ~300-350 lines, under 5,000 tokens. The full run engine specification moves to `references/handler-run.md` as a cohesive unit. I withdraw the claim that the engine must live in root but maintain the claim that the engine must not be further decomposed internally.

**Constraint preserved:** The round loop + iteration loop + output path computation + termination check remain together in `references/handler-run.md`. The "do not decompose" boundary applies within that file, not at the root level. This addresses functional-decomposition's multi-round extraction proposal: I still oppose splitting multi-round logic from single-round logic, because the single-round path is defined in terms of what the multi-round path omits. But that cohesive unit now lives in a reference file, not in root.

### Original Recommendation 2: Extract guided workflow handlers to `references/handler-{name}.md`

**SUSTAINED.** Universal agreement across all cross-reviews. The file-mediated coupling between handlers (define writes problem.md, interests reads it) makes this the safest decomposition boundary. No reviewer challenged the handler extraction itself, only secondary concerns about shared patterns.

**Refinement based on functional-decomposition's cross-review:** functional-decomposition proposes a `references/guided-handler-patterns.md` to define the shared workflow skeleton (check prerequisites, ingest input, validate, present for confirmation, write, post-write validate, report). I initially framed the handlers as fully independent. I now accept that the shared skeleton is real and creates validation drift risk if duplicated across five files. However, I oppose a two-level reference chain (SKILL.md dispatch -> handler reference -> pattern reference) because it requires the agent to load two files for a single guided command. Instead, the shared skeleton should be inlined at the top of each handler reference file as a brief preamble (5-10 lines stating the pattern), with handler-specific logic following. This is controlled duplication that keeps each handler self-contained while acknowledging the shared structure. The linter (Recommendation 8) can verify that the preamble is consistent across handlers.

### Original Recommendation 3: Extract gate handler to `references/handler-gate.md`

**SUSTAINED.** Every reviewer identified the gate handler as the single cleanest extraction target. No modifications needed.

### Original Recommendation 4: Extract Dispute-Parsing Subsystem to `references/subsystem-dispute-parsing.md`

**SUSTAINED with loading model clarification.** Both the extraction boundary and interface contract are universally agreed. functional-decomposition's cross-review raises a valid concern about the loading model: if three different reference files all contain "read `references/dispute-parsing.md`," the agent may load it redundantly.

**Clarification:** The dispute-parsing reference file should be loaded by the run engine handler (`references/handler-run.md`), not by individual consumer handlers. The run engine is the execution context for Phase 6 trigger evaluation, round termination, and post-execution reporting. The converge and gate handlers delegate to the run engine, so they inherit its dispute-parsing dependency transitively. The load instruction belongs in `references/handler-run.md`, not in `references/handler-converge.md` or `references/handler-gate.md`. This keeps loading one-level deep from the dispatch and avoids redundant reads.

### Original Recommendation 5: Extract preset resolution to `references/subsystem-preset-resolution.md`

**SUSTAINED.** All reviewers agree on the extraction boundary, interface contract (input: preset name; output: resolved agent config; errors: not found, ambiguous, not composable), and the three call sites. apm-specialist's alternative of registering presets as a sub-skill creates a dependency triangle that APM cannot currently express; the reference file approach avoids this. No modifications needed.

### Original Recommendation 6: Extract template variable documentation to `references/contract-template-variables.md`

**MODIFIED based on agentskills-specialist's execution-cost analysis.** agentskills-specialist's cross-review (DC-3) correctly identifies that full extraction of template variable documentation forces an agent executing Phase 2 to read three files (phase template, variable reference, schema). My original recommendation was framed as a deduplication exercise, but the execution-time cost of per-phase file reads in a 5-6 phase deliberation with multiple agents is significant.

**Revised position:** Do not create a standalone `references/contract-template-variables.md`. Instead, template variable documentation moves into `references/handler-run.md` alongside the phase execution logic it supports. The variables are co-located with the phases that consume them, preserving the current two-file-read pattern (SKILL.md for dispatch + handler-run.md for execution) rather than adding a third file. The `schema/variables.yml` remains the machine-readable contract; the handler-run.md prose is the human-readable companion. The root SKILL.md's phase summary does not list variables, only references handler-run.md.

### Original Recommendation 7: Define explicit "do not decompose" boundaries

**MODIFIED.** The "do not decompose" principle survives but the scope changes. The round loop + iteration loop + output path computation + termination check remain a cohesive unit, but that unit now lives in `references/handler-run.md` (per the Recommendation 1 revision), not in the root SKILL.md. The "do not decompose" designation is an internal annotation within handler-run.md, not a root-level constraint.

I also withdraw the blanket characterization of all engine internals as "do not decompose." functional-decomposition's preset resolution extraction (which my Recommendation 5 already agrees with) proves that some engine subsystems can be cleanly separated. The "do not decompose" boundary applies specifically to the state machine (round/iteration counters, output path formulas, termination conditions, retroactive directory moves) where separation would create an interface boundary through the middle of coupled state transitions.

### Original Recommendation 8: Mandate linter expansion for reference file consistency

**MODIFIED in scope.** apm-specialist and agentskills-specialist both raise concerns about linter scope creep. agentskills-specialist correctly notes that validating reference file consistency against SKILL.md call sites "requires the linter to parse Markdown prose for semantic intent, which is a significantly harder problem than validating YAML schemas." apm-specialist notes that a comprehensive integration test is too heavy for a PostToolUse hook.

**Revised position:** The linter should expand incrementally, not comprehensively. Phase 1 (achievable now): validate that every template variable referenced in `references/handler-run.md` exists in `schema/variables.yml`. This is a mechanical check similar to the existing template validation. Phase 2 (deferred until reference files stabilize): validate that reference file headers match the dispatch table entries. Phase 3 (aspirational): error message catalogue consistency. The full integration test suite I originally proposed is directionally correct but should not block the decomposition. Start with what the linter already knows how to validate (variable existence) and expand as reference files prove stable.

### Original Recommendation 9: Establish naming convention for reference files

**SUSTAINED with simplification.** Multiple reviewers noted the tension between my three-tier naming (`handler-`, `subsystem-`, `contract-`) and simpler alternatives. I maintain the `handler-{name}.md` prefix for subcommand handlers (universally agreed) and the `subsystem-{name}.md` prefix for shared subsystems (dispute-parsing, preset-resolution). I withdraw the `contract-` prefix since Recommendation 6 has been revised to eliminate the standalone contract file. The convention is now two-tier: handlers and subsystems.

This aligns with agentskills-specialist's observation that the distinction matters for navigability at 8-10 files but is not worth a third category. The directory listing now reads: `handler-arbitrate.md`, `handler-converge.md`, `handler-define.md`, `handler-gate.md`, `handler-interests.md`, `handler-mode.md`, `handler-run.md`, `subsystem-dispute-parsing.md`, `subsystem-preset-resolution.md`. Nine files, two prefixes, legible from `ls`.

### Original Recommendation 10: Add dependency map to root SKILL.md

**WITHDRAWN.** agentskills-specialist's cross-review (DC-3) makes a persuasive case that the dispatch table already serves as the dependency map for handlers, and that each handler reference file should declare its own dependencies. A redundant centralized map creates a second source of truth that drifts from actual reference file contents. apm-specialist's cross-review reinforces this: maintaining the map manually is "exactly the kind of documentation drift" that the linter expansion is meant to prevent, yet no tooling validates the map.

**Replacement:** Each handler reference file includes a brief "Dependencies" section at the top listing what it requires (e.g., handler-converge.md declares "Depends on: handler-run.md, subsystem-dispute-parsing.md"). The dispatch table in root SKILL.md provides the top-level routing. Together, these are the dependency graph, distributed across the files that own the dependencies rather than centralized in a table that nobody updates. This follows the agentskills-specialist's "conditional loading triggers" pattern and keeps dependency information co-located with dependent content.

---

## New Recommendations

### N1: Address the agents-md-specialist's dual-audience concern for multi-agent isolation rules

agents-md-specialist raises a legitimate point I did not consider: if multi-agent isolation rules live only in SKILL.md, non-Claude-Code contributors editing templates can unknowingly violate the isolation contract. The rules have two audiences: the runtime executor (SKILL.md) and the template contributor (AGENTS.md or equivalent).

**Recommendation:** The multi-agent isolation rules remain in the root SKILL.md as execution invariants (unchanged from my original position). Additionally, a brief contribution-oriented restatement belongs in `templates/AGENTS.md` (per agents-md-specialist's nested AGENTS.md proposal), framed as: "Templates must not assume cross-agent visibility. Each template will be executed by an independent agent that cannot see other agents' outputs except as explicitly provided via template variables." This is not duplication of the runtime rule; it is a contribution constraint derived from the runtime rule. The SKILL.md version governs execution behavior; the AGENTS.md version governs authoring behavior. Both are necessary, and they are different enough in framing that drift is unlikely.

### N2: Clarify two classes of reference loading

functional-decomposition's cross-review identifies an important distinction I failed to make: dispatch-table triggers (pre-invocation, safe) vs. conditional subsystem triggers (mid-execution, riskier). My original review treated all reference loading as equivalent.

**Recommendation:** The decomposition should distinguish two loading classes:

- **Class A (dispatch routing):** The agent reads one handler reference file before beginning execution, routed by the dispatch table. This is safe, analogous to function call dispatch. All handler references are Class A.
- **Class B (conditional subsystem loading):** The agent encounters a condition mid-execution (e.g., `preset:` field in config, `rounds > 1` in config) and reads a subsystem reference file. This requires explicit fallback behavior: what does the agent do if the file is missing? What is the minimal behavior if loading fails?

Currently, both subsystem references (dispute-parsing, preset-resolution) are Class B. The handler-run.md file should specify the conditional triggers and fallback behaviors for each Class B load. This prevents the "scavenger hunt" problem I identified in my cross-review of agentskills-specialist.

### N3: Resolve the AGENTS.md vs. reference file authority question

agents-md-specialist's nested AGENTS.md proposal and my reference file proposal compete for the same content (preset rules, template conventions, validation patterns). My cross-review identified this but did not resolve it.

**Recommendation:** Reference files are authoritative for runtime behavior; AGENTS.md files are authoritative for contribution workflow. Where content overlaps (e.g., preset naming conventions are both a runtime validation rule and a contribution convention), the reference file contains the canonical specification, and the AGENTS.md file contains a human-oriented summary with an explicit pointer: "For the full specification including error conditions and composition rules, see `references/subsystem-preset-resolution.md`." Non-Claude-Code agents that cannot follow SKILL.md reference links get an 80% summary from AGENTS.md; Claude Code agents executing the runtime get the full specification from the reference file. The linter validates that the reference file is consistent with the schema; AGENTS.md summaries are maintained manually but are lower stakes because they are contribution guidance, not execution contracts.

### N4: Antipattern check placement after decomposition

My original review raised this question without answering it. After considering agents-md-specialist's framing (contribution guideline) and my own framing (orchestrator-level concern), I now have a position.

**Recommendation:** The antipattern check remains an orchestrator-level pre-execution step in the root SKILL.md, executed before the dispatch table routes to a handler. This means all subcommands inherit the check, including guided workflow handlers that currently do not trigger it. This is a minor scope expansion, but it prevents a decomposition gap where adding a handler reference file accidentally bypasses the antipattern check. The `antipatterns/catalog.md` interaction is documented in the root SKILL.md's pre-dispatch section, not in individual handler files. agents-md-specialist's proposal to also surface it in AGENTS.md as a contribution guideline is compatible and should proceed independently.

---

## Position Summary

The most significant revision is conceding the run engine's placement. My original position -- full engine in root SKILL.md -- was defensible on coherence grounds but produced a root file that exceeded the token budget and imposed unnecessary context load on non-engine subcommands. The cross-reviews from agentskills-specialist and functional-decomposition demonstrated that internal cohesion can be preserved in a reference file just as well as in root. The revised architecture is:

**Root SKILL.md (~300-350 lines, under 5,000 tokens):**
- Frontmatter and metadata
- Subcommand dispatch table with file references
- Multi-agent isolation rules (gotchas)
- Antipattern check (pre-dispatch)
- Phase-level engine summary (one paragraph per phase, no template variables)
- Important notes and baseline features

**Handler reference files (7 files, Class A loading):**
- `handler-run.md` (~450-550 lines): full engine specification including phase execution, template variables, round/iteration state machine, and the "do not decompose" core
- `handler-define.md` (~150 lines)
- `handler-interests.md` (~200 lines)
- `handler-mode.md` (~180 lines)
- `handler-converge.md` (~210 lines)
- `handler-arbitrate.md` (~160 lines)
- `handler-gate.md` (~180 lines)

**Subsystem reference files (2 files, Class B loading from handler-run.md):**
- `subsystem-dispute-parsing.md` (~80 lines)
- `subsystem-preset-resolution.md` (~120 lines)

**Total reference files:** 9 files in `references/`, two-tier naming convention (`handler-`, `subsystem-`).

**Key architectural principles preserved:**
1. The run engine's internal state machine is never split across files.
2. The dispatch table is the single routing authority.
3. Multi-agent isolation rules are front-loaded in every activation.
4. Handler reference files are self-contained with declared dependencies.
5. Subsystem reference files are loaded conditionally from handler-run.md, not from root.
6. Reference files are authoritative for runtime; AGENTS.md files are authoritative for contribution.

**Key concessions made:**
1. The run engine moves to a reference file (conceding to agentskills-specialist, functional-decomposition, apm-specialist).
2. The dependency map is withdrawn in favor of per-file dependency declarations (conceding to agentskills-specialist).
3. The template variable contract file is eliminated; variables stay co-located with the engine (conceding to agentskills-specialist's execution-cost analysis).
4. The linter expansion is phased rather than comprehensive (conceding to apm-specialist, agentskills-specialist).
5. AGENTS.md files have a legitimate complementary role for contribution guidance (conceding to agents-md-specialist).

**Key positions maintained:**
1. The round/iteration state machine must not be further decomposed, even within handler-run.md.
2. Reference files (not APM sub-skills) are the correct decomposition primitive because conversus handlers are not independently invocable.
3. The two-tier naming convention (`handler-`, `subsystem-`) provides sufficient navigability without over-engineering.
4. Multi-round logic and single-round logic must not be separated, because the single-round path is defined as the negation of multi-round behavior.
5. Conditional subsystem loading (Class B) needs explicit fallback behavior to prevent silent failures.
