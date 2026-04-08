# Disputes — agentskills-specialist (Phase 4)

## Remaining Disputes

### Dispute 1: Run engine placement — SKILL.md core vs. references/handler-run.md

This is the sharpest structural disagreement remaining after revision. integration-specialist revised their position to move the full run engine to `references/handler-run.md` (~450-550 lines), leaving SKILL.md at ~300-350 lines under 5,000 tokens. My revised position is the opposite: the run engine core stays in SKILL.md (~500 lines, 6,000-8,000 tokens), and no handler-run.md file is created.

The disagreement is architectural, not aesthetic. integration-specialist now argues that internal cohesion within the engine is preserved regardless of file position — the engine can stay together in `references/handler-run.md` just as well as in SKILL.md. I accept the internal cohesion argument is valid but reject its conclusion for a reason integration-specialist's revised position does not address: `converge` and `gate` both delegate to the run engine, and both are dispatched from the root SKILL.md. If the agent invokes `/conversus converge`, it reads SKILL.md (Class A dispatch), then reads `references/handler-converge.md`, and that file must say "this command delegates execution to the run engine — read `references/handler-run.md`." That is a two-hop reference chain for the most common invocation path. The agentskills specification states explicitly: "Keep file references one level deep from SKILL.md. Avoid deeply nested reference chains."

integration-specialist's revised architecture lists `handler-run.md` as a Class A load — but Class A means triggered at invocation time via the dispatch table. The dispatch table routes to one handler per subcommand. `/conversus converge` routes to `handler-converge.md`. There is no dispatch table entry for `handler-run.md` because run is not a top-level subcommand — it is the engine that converge and gate compose. If handler-run.md is Class A, when does it load? If it loads with every invocation, it is not progressive disclosure — it is a mandatory two-file read on every run. If it loads conditionally from within handler-converge.md, it is a two-hop chain.

My position: the run engine belongs in SKILL.md not because reference files cannot preserve cohesion, but because the engine's call graph — converge dispatches to it, gate dispatches to it, both dispatch from SKILL.md — makes SKILL.md the architecturally correct home. A 6,000-8,000 token SKILL.md that eliminates two-hop chains for the most common paths is better than a 5,000-token SKILL.md that requires them.

**What I need from integration-specialist**: a concrete answer to the loading trigger for handler-run.md. If it is Class A (pre-invocation), what dispatch condition fires it independently of converge and gate? If it is loaded from within handler-converge.md, acknowledge this is a two-hop chain and explain why the agentskills specification's one-level-deep constraint does not apply.

---

### Dispute 2: Multi-round extraction — conditional reference vs. inline retention

functional-decomposition revised their position to make multi-round extraction contingent on a dependency analysis: if the shared interface between single-round and multi-round paths exceeds 20 lines, retain multi-round inline. This is a sensible empirical gate, but it defers a decision that affects the entire SKILL.md size estimate. My position remains that multi-round orchestration should not be extracted regardless of line count, for a reason the dependency analysis does not resolve.

The issue is not whether single-round and multi-round share interface lines — it is that single-round behavior is defined negatively against multi-round behavior throughout the run engine. The single-round path is "the multi-round loop with `rounds = 1`." The output path logic, directory structure, and retroactive Round 1 rename (which happens when rounds are expanded later) are all part of the same state machine. A dependency analysis that counts shared lines will undercount shared semantics: the single-round path's termination condition is not just "rounds = 1" — it is "rounds = 1 and no stagnation and no reconvergence trigger." Splitting the file at the `if rounds > 1:` boundary orphans the negative-case definitions.

functional-decomposition's 20-line threshold is a heuristic, not an architectural boundary. My position is that the threshold is wrong for a state machine defined by negation: the shared interface for a negative-case definition cannot be measured by counting shared lines, because the single-round path references multi-round concepts by their absence, not by calling shared code.

**What I need from functional-decomposition**: if the dependency analysis shows fewer than 20 shared lines and extraction proceeds, how does the SKILL.md describe single-round termination without referencing the multi-round termination conditions that give it meaning? If the answer is "duplicate the relevant multi-round definitions in SKILL.md," that is two sources of truth for the same conditions.

---

### Dispute 3: File naming — flat names vs. type-prefixed convention

integration-specialist and functional-decomposition both converged on a two-tier naming convention: `handler-{name}.md` for subcommand handlers, `subsystem-{name}.md` for shared subsystems. My revised position uses flat names for subsystem references (`dispute-parsing.md`, `preset-resolution.md`) without the `subsystem-` prefix.

This is a lower-stakes dispute than the two above, but it has a real consequence: the naming convention affects whether the directory listing is self-documenting. At 9-11 reference files, a flat listing mixes handlers, subsystems, and informational references without visual grouping. The `handler-` prefix is universally agreed. The `subsystem-` prefix is where I diverged.

My original objection: the agentskills specification defines no file-type taxonomy for references. Adding a `subsystem-` category imposes classification overhead. This objection survives but weakens when I consider that I already use `handler-` for six files — at that point the directory has a partial taxonomy whether I name it or not. An ungrouped `dispute-parsing.md` in a directory of six `handler-*.md` files will read as a malformed entry, not a deliberately flat name.

I am prepared to accept `subsystem-` for dispute-parsing and preset-resolution if the counter-proposal addresses one concern: the `subsystem-` prefix implies the file is a shared dependency. If future reference files are informational (e.g., `operational-notes.md`), they are neither handlers nor subsystems. The taxonomy needs a third category or a convention for uncategorized files. functional-decomposition's `notes-{name}.md` prefix for informational references closes this gap.

**My revised position on naming**: accept the three-tier convention — `handler-`, `subsystem-`, `notes-` — proposed collectively by integration-specialist (two tiers) and functional-decomposition (adding `notes-`). This is the one area where I am moving toward full convergence pending the other parties' confirmation.

---

### Dispute 4: Token budget documentation — per-invocation table vs. single acknowledged exception

functional-decomposition and I both recommend documenting the token budget, but with different shapes. My New Recommendation C proposes a per-invocation table listing expected token loads for each invocation path. functional-decomposition's Recommendation 9 revision proposes documenting the budget once at decomposition time with a single acknowledged exception for the run engine, revisited only during major structural revisions.

The dispute is about operational utility. A per-invocation table tells reviewers immediately whether a reference file has grown beyond its budget — the table becomes stale and flags the issue. functional-decomposition's one-time snapshot requires someone to remember to check the budget during major revisions, which is a weaker enforcement mechanism.

My position: the per-invocation table has value proportional to how often SKILL.md and reference files are edited. If conversus is actively developed (specs 012-020 queued), the table will be referenced frequently enough to justify its maintenance cost. If conversus is stable, the table collects dust regardless of its format. The question is not which format is better in principle — it is whether the maintenance cost exceeds the detection benefit during active development.

I accept functional-decomposition's concern that a per-invocation table updated after every content edit is operational overhead. My revised position: document the budget as a table at decomposition time, with a note that it should be updated when reference files are created or significantly revised, not on every content change. This is a middle ground that preserves detection value without requiring per-edit maintenance.

---

## Convergence

### Convergence 1: Progressive disclosure via references/ is the correct primary mechanism

All five agents agree: the agentskills `references/` model with conditional load triggers is the correct decomposition strategy for conversus. APM sub-skills are wrong as the primary decomposition axis (apm-specialist concedes this fully). AGENTS.md is wrong for execution logic (agents-md-specialist concedes this). The dispute is entirely about which content belongs in the always-loaded SKILL.md core and what granularity of reference extraction is appropriate. The mechanism is settled.

### Convergence 2: Handler extraction is universally agreed — six handlers, one boundary question

Gate, define, interests, mode, arbitrate, and (with caveats) converge are all agreed extraction targets. The extraction boundaries, load triggers, and file names (`references/handler-{name}.md`) are agreed across all four other agents and my revised position. The only open question is whether converge's extraction creates a two-hop chain via the run engine — which is the subject of Dispute 1 above. The handler extraction itself is not disputed; only whether converge's handler file requires a second file read to complete execution.

### Convergence 3: AGENTS.md is contribution guidance only, never execution contracts

All five agents agree that execution logic must not live in AGENTS.md, that AGENTS.md files should contain pointers to authoritative sources rather than inline rule restatement, and that nested AGENTS.md files should be 15-30 lines each. agents-md-specialist accepted the correction from all four cross-reviewers and revised scope accordingly. This is a complete convergence that removes a significant area of contention from earlier phases.

### Convergence 4: Dispute-Parsing Subsystem warrants extraction as a stable interface

All five agents agree the Dispute-Parsing Subsystem has a stable enough interface, a sufficiently bounded scope (~28 lines), and enough architectural independence to warrant physical extraction. The remaining question is loading: whether it should be a Class B trigger from within handler-run.md (integration-specialist) or a Class B trigger from SKILL.md directly (my position). This is a second-order question about which file contains the load instruction, not about whether the extraction should happen.

The practical consequence: if the run engine stays in SKILL.md (my position), the load trigger lives in SKILL.md. If the run engine moves to handler-run.md (integration-specialist's position), the load trigger lives in handler-run.md. Both produce the same file on disk. The extraction is agreed; only the trigger location varies with the Dispute 1 outcome.

### Convergence 5: Full APM distribution is premature and should be deferred

All five agents agree that APM packaging for distribution is premature until the spec suite stabilizes and a second consumer appears. apm-specialist proposed this originally and all four cross-reviewers endorsed it. This is one of the strongest convergence points in the entire deliberation — unanimous and well-reasoned.

---

## Final Position Statement

### Non-Negotiables

**1. The run engine core must be fully present in the always-loaded context for any execution path that invokes it.**

The agentskills specification's one-level-deep reference constraint is not a style preference — it is an architectural principle that prevents silent degradation. An agent that reads SKILL.md and then must read a second reference file before beginning run engine execution is working with an incomplete specification during the gap between reads. For an orchestration engine managing multi-agent deliberations, that gap produces incorrect phase sequencing, wrong output path computation, and missed termination conditions. The question of whether "fully present" means "in SKILL.md" or "in a reference file always loaded alongside SKILL.md" is where integration-specialist and I diverge — but the underlying requirement is not negotiable: the agent must have the full run engine specification before Phase 1 begins, without a mid-execution conditional load.

**2. The round/iteration state machine must not be split across files.**

The single-round path is defined as the multi-round loop with termination at round 1. Splitting single-round and multi-round logic across a file boundary creates two sources of truth for the termination conditions and forces either duplication or a cross-file reference inside the run engine itself. This applies whether the run engine lives in SKILL.md or in a reference file — the internal state machine is a decomposition constraint, not a placement preference.

**3. The agent count formulas are authoritative contracts, not derivable documentation.**

`N^2 + 2N + 1` (without arbiter) and `N^2 + 2N + 2` (with arbiter) must appear verbatim in the always-loaded SKILL.md core. A derivation error in the pre-execution estimate produces a silently wrong user-facing warning before a resource-intensive multi-agent run. The formulas are gotchas, not reference material. They must be front-loaded.

**4. Conditional load triggers must be unambiguous and must specify fallback behavior for Class B loads.**

Every reference file extracted from SKILL.md must have a load trigger that names a runtime condition, not a file path pattern. Class B triggers (mid-execution, config-conditional) must include explicit fallback behavior: what the agent does if the file is missing or cannot be read. This is not a documentation preference — it is a safety requirement for an orchestration engine that may run dozens of subagent invocations. A silent failure in preset resolution or dispute parsing mid-run is not recoverable without restarting from scratch.

### Flexibility

**A. I accept two-tier naming with the addition of `notes-` for informational references.**

I withdraw my objection to `subsystem-` as a prefix for dispute-parsing and preset-resolution. Combined with functional-decomposition's `notes-` proposal for informational references, the three-tier taxonomy (`handler-`, `subsystem-`, `notes-`) closes the ungrouped-file problem without over-engineering. I would accept this naming convention in the final implementation even if my preferred architecture (run engine in SKILL.md) does not carry.

**B. I accept phased decomposition with empirical validation gates.**

functional-decomposition's New Recommendation B (staged execution with validation gates) is correct process design. Extract gate handler first, validate that conditional loading works in practice, then proceed. If the mechanism fails empirically — agents miss load triggers or produce incorrect output after extraction — the staging catches this before the full decomposition is committed. I accept this ordering. My architecture preferences should not override empirical evidence from Phase 1 execution.

**C. I accept the linter expansion as a phased rather than comprehensive undertaking.**

My New Recommendation B (expand the linter post-decomposition) was directionally correct but integration-specialist's phased approach (Phase 1: variable existence checks; Phase 2: reference file headers vs. dispatch table; Phase 3: error message catalogue) is the right scope for each stage. I do not need comprehensive linter coverage before decomposition begins.

**D. I accept token budget documentation as a one-time baseline with targeted update triggers.**

Rather than maintaining a per-invocation table after every edit (my New Recommendation C) or a single snapshot revisited only during major revisions (functional-decomposition's position), the appropriate middle ground is: document the budget at decomposition time as a table, and specify the update trigger as "when a reference file is created, significantly expanded, or removed." This provides detection value during active development without requiring per-edit maintenance.

**E. The run engine placement dispute is resolvable by answering the two-hop chain question.**

If integration-specialist can demonstrate that `handler-run.md` is loaded via a Class A trigger that does not require converge or gate to name it as a dependency — that is, if there is a loading mechanism that ensures handler-run.md is always present when any execution path that uses the engine is active — I will accept moving the run engine to a reference file. The non-negotiable is not SKILL.md placement specifically; it is zero-hop access to the full engine specification from any execution path that uses it. If that can be achieved with handler-run.md as a near-mandatory Class A load, the file placement is secondary.
