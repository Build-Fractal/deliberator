# Arbitration Resolution — Spec 011a: SKILL.md Breakdown

---

## Process Note

This Phase 6 subject arbitration was triggered by the `disputes_remain` condition in the Phase 5 synthesis. Four distinct dispute clusters survived the full 5-phase cooperative deliberation among 5 agents (functional-decomposition, integration-specialist, apm-specialist, agentskills-specialist, agents-md-specialist). The deliberation produced 20 cross-reviews, 5 revisions, and 5 dispute documents before synthesis.

I am conversus — the system under review. My rulings are grounded in my own architectural invariants as documented in the README.md (the grounding document). I have binding decision authority over these four disputes.

---

## Decision Framework

The following principles from the conversus grounding document (README.md) govern these rulings:

**Principle 1 — One Agent Per Output (Architectural Invariant).** "Every output file MUST be produced by its own independent subagent. This is non-negotiable." The corollary: any decomposition that increases the risk of an agent operating with an incomplete specification during execution — thereby producing silently degraded output — violates the spirit of this invariant. The invariant exists because "a single agent writing 6 cross-reviews produces internally consistent but artificially harmonized outputs." The same logic applies to the engine itself: an agent executing a multi-phase deliberation with a one-paragraph summary instead of the full engine specification produces silently degraded orchestration.

**Principle 2 — Phase Boundaries Are Hard Barriers.** "Sequential phases, parallel within." The run engine enforces this through the round/iteration state machine, output path computation, and termination conditions. Any decomposition that risks the agent misunderstanding phase boundaries — because it loaded a summary instead of the full specification — is a safety violation, not a token optimization.

**Principle 3 — Templates Contain Mode-Specific Prompt Engineering.** "The skill just fills variables." The run engine is the variable-filling orchestrator. It must have complete knowledge of the phase pipeline, output schemas, and mode-specific template selection at execution time. Incomplete engine context produces incorrect variable resolution, which produces incorrect prompts, which produces agents that argue from the wrong frame.

**Principle 4 — The Run Engine Is the Core.** "Everything else is UX wrapping or CI/CD integration." This principle establishes a hierarchy: the engine is not a peer of the guided handlers — it is the substrate they compose. Architectural decisions about the engine carry higher stakes than decisions about handlers. The failure mode of a missing handler is a clear error ("unknown subcommand"). The failure mode of a partially loaded engine is silent degradation across an entire multi-agent run.

**Principle 5 — Competition Dynamics Must Be Explicit and Configurable.** "Conversus makes those dynamics explicit and configurable." The system's value proposition depends on the engine correctly implementing the configured competition mode. An agent that proceeds without the full mode-specific execution logic cannot produce genuinely adversarial positions — it produces approximations. This is worse than failure because it looks like success.

**Principle 6 — Staged Validation Is Consistent with Conversus's Own Process.** The 6-phase pipeline itself is a staged validation: each phase builds on the outputs of the previous phase, with the synthesis only running after all dispute documents are complete. Applying the same principle to the decomposition — extract, validate, proceed — is architecturally self-consistent.

---

## Binding Decisions

### Dispute A: Run Engine Placement — Root SKILL.md vs. references/handler-run.md

**Positions:**
- **Engine in SKILL.md** (agentskills-specialist, functional-decomposition, apm-specialist as conditional): The run engine core stays in the always-loaded SKILL.md, producing a root of ~500-700 lines (6,000-8,000 tokens). This eliminates two-hop reference chains. The 5,000-token guideline is acknowledged as an acceptable exception for an orchestration engine.
- **Engine in references/handler-run.md** (integration-specialist): The engine moves to a reference file (~450-550 lines), keeping the root at ~300-350 lines (under 5,000 tokens). A mandatory Class A-style load trigger in handler-converge.md and handler-gate.md instructs the agent to load the engine before proceeding.
- **Conditional on empirical validation** (apm-specialist): Accepts either outcome based on the results of the staged validation gates.

**Synthesizer's assessment:** Both positions have legitimate structural arguments. The root-retention camp correctly identifies the two-hop chain violation and the silent failure mode. The extraction camp correctly identifies the context cost imposed on non-engine subcommands. The dispute is genuinely empirical. The synthesizer recommended root SKILL.md retention as the initial implementation, with empirical testing after Phase 2 of staged decomposition.

**Ruling:** The run engine core stays in SKILL.md as the binding initial implementation. Extraction to a reference file is permitted only after empirical testing demonstrates that two-hop chain loading produces no observable degradation in `/conversus converge` output fidelity.

**Grounding citation:** Principle 4 (the run engine is the core) and Principle 1 (silent degradation is the worst failure mode). The engine is not a handler — it is the substrate. Handlers are UX wrapping; the engine is the execution specification. Treating the engine as a peer of the guided handlers by placing it in the same `references/handler-*.md` namespace misrepresents the architectural hierarchy.

**Rationale:** agentskills-specialist's challenge is decisive: "Name the loading trigger for handler-run.md without it being always-loaded or a two-hop chain." integration-specialist could not answer this cleanly. The engine is not dispatched from the dispatch table — it is composed by converge, gate, and the bare `run` invocation. There is no natural Class A trigger because the engine is not a subcommand. Making it always-loaded via a synthetic trigger eliminates the token savings that motivated extraction. The asymmetry integration-specialist identifies (non-engine subcommands paying 6,000 tokens) is real but acceptable: the engine is what conversus exists to execute, and the guided handlers are lightweight preparatory steps. Penalizing the common case (engine execution) to optimize the uncommon case (standalone define/interests/mode) inverts the priority. The 6,000-8,000 token root is an acknowledged, documented exception to the agentskills sizing guideline.

**Rejected position:** Engine extraction to `references/handler-run.md`. This position correctly identifies the token cost asymmetry but underestimates the severity of the silent failure mode. integration-specialist's argument that "the delegation point is explicit and the loading is sequential, not nested discovery" is architecturally reasonable but empirically unvalidated. The risk is asymmetric: if extraction works, we save tokens on lightweight subcommands; if it fails, we silently degrade multi-agent deliberations. The downside outweighs the upside at this stage. integration-specialist's position is not wrong — it is premature. If empirical testing after Phase 2 demonstrates reliable two-hop loading, this ruling should be revisited.

**Required changes:**
1. The run engine (Steps 1-8 of Run: Execution, including the full round/iteration state machine, output path computation, template selection, mode-specific phase instructions, and termination logic) remains in SKILL.md.
2. Document an explicit exception to the agentskills 500-line / 5,000-token guideline in SKILL.md, with the rationale: "conversus is an orchestration engine, not a typical skill; the engine specification must be present in full for any execution path."
3. After Phase 2 of staged decomposition (all guided handlers extracted and validated), execute a controlled comparison test: run `/conversus converge` with the engine in SKILL.md and again with the engine in `references/handler-run.md`. Compare output fidelity. If fidelity is equivalent, file a follow-on change to extract the engine. If degradation is observed, confirm root retention permanently.
4. The per-invocation token budget table (P3.1 in synthesis) must record the engine's presence in the always-loaded core as a documented cost, not hide it.

---

### Dispute B: Multi-Round Extraction — Conditional Reference vs. Inline Retention

**Positions:**
- **No extraction** (integration-specialist, agentskills-specialist): The round/iteration state machine is a cohesive unit. Single-round behavior is defined as the negation of multi-round behavior. Splitting them creates two sources of truth.
- **Conditional on dependency analysis** (functional-decomposition): Perform an explicit dependency analysis of the shared interface. If fewer than 20 lines, extract with controlled duplication. If more, retain inline.
- **Extract with conditional loading** (agentskills-specialist's directory layout included `references/multi-round-execution.md`, though the revision kept the engine in SKILL.md).

**Synthesizer's assessment:** integration-specialist's negation-definition argument is "the strongest single argument in the entire deliberation." The single-round path's termination conditions, directory structure, and output paths are all defined relative to multi-round behavior. The synthesizer recommended retaining multi-round orchestration inline with the run engine.

**Ruling:** Multi-round orchestration is retained inline with the run engine in SKILL.md. No extraction. No dependency analysis is required as a gate for this decision.

**Grounding citation:** Principle 2 (phase boundaries are hard barriers). The round/iteration state machine is what enforces phase boundaries across rounds. Splitting the state machine across files means the single-round agent must either (a) load the multi-round file to understand what it is opting out of, or (b) carry duplicated definitions of what "round 1 only" means. Both options violate the hard-barrier principle: in case (a), the boundary enforcement depends on a conditional load; in case (b), the boundary is defined in two places with no synchronization mechanism.

**Rationale:** I endorse integration-specialist's negation-definition argument without reservation. The single-round path is not a standalone specification — it is "the multi-round loop with rounds = 1." The output path logic (`{output}/` vs. `{output}/round-{N}/`), the stagnation detection (disabled vs. enabled), the reconvergence trigger (absent vs. present), and the retroactive Round 1 rename are all defined by their relationship to multi-round behavior. functional-decomposition's 20-line threshold is a reasonable heuristic for additive subsystems but is the wrong tool for a state machine defined by negation. You cannot count shared lines when the sharing is semantic (defined by absence) rather than syntactic (defined by reference). The 360-line cost is real, but the coupling is architectural, not incidental. The "do not decompose" constraint — unanimously agreed by all 5 agents — applies unconditionally here.

**Rejected position:** Conditional extraction pending dependency analysis. functional-decomposition's proposal is methodologically sound for additive subsystems but misapplied to a negation-defined state machine. The dependency analysis would measure syntactic sharing (shared lines) but miss semantic sharing (concepts defined by their absence in the single-round path). I reject the dependency analysis as a gate not because the analysis is wrong, but because its result would not capture the actual coupling. apm-specialist correctly identified this: "a dependency analysis that counts shared lines will undercount shared semantics."

**Required changes:**
1. The multi-round orchestration block (round loop, iteration loop, stagnation detection, reconvergence triggers, retroactive directory moves, cross-round synthesis) remains in SKILL.md within the run engine section. It is not extractable to a reference file.
2. Add a "do not decompose" annotation as a comment or documentation note at the beginning of the round/iteration state machine section, explaining that single-round semantics are defined as the negation of multi-round behavior and cannot be split without duplication.
3. Remove `references/multi-round-execution.md` from any proposed directory layouts.
4. If a future spec requires the run engine to shrink further, the path is extracting the entire engine (per Dispute A's empirical test), not splitting the state machine internally.

---

### Dispute C: Naming Convention — Two-Tier vs. Three-Tier vs. Flat

**Positions:**
- **Two-tier** (`handler-`, `subsystem-`): integration-specialist, functional-decomposition, apm-specialist.
- **Three-tier** (`handler-`, `subsystem-`, `notes-`): agentskills-specialist's final flexibility position accepts this.
- **Flat (handler- only, plain names for rest)**: functional-decomposition's proposed compromise.

**Synthesizer's assessment:** Low-stakes convention decision. The `handler-` prefix is universally agreed. The dispute is about non-handler files. The synthesizer recommended three-tier naming.

**Ruling:** Adopt the two-tier naming convention: `handler-` for subcommand handlers and `subsystem-` for shared subsystems. Do not adopt `notes-` as a third tier at this time.

**Grounding citation:** Principle 4 (the run engine is the core; everything else is UX wrapping or CI/CD integration). The architectural hierarchy has two layers: execution substrate (the engine, shared subsystems) and interface handlers (subcommands). The naming convention should reflect this hierarchy, not introduce a third category that blurs it.

**Rationale:** The two-tier convention maps directly to the architectural hierarchy that all agents agreed on: dispatch targets (`handler-`) and shared dependencies (`subsystem-`). The `handler-` prefix is the most important distinction — it marks files that are dispatch targets from the SKILL.md dispatch table. The `subsystem-` prefix marks files that are loaded conditionally from within handlers or the engine (Class B triggers). This is a complete taxonomy of the reference files that will exist after the decomposition described in this spec. The three-tier `notes-` category was proposed to cover informational reference material like `operational-notes.md`, but at the current file count, only one such file is anticipated. Adding a naming tier for a single file is premature. If informational reference files proliferate in future specs, the `notes-` prefix can be adopted then. agentskills-specialist's movement toward accepting three-tier naming is noted and appreciated — the two-tier ruling is closer to that position than to the flat alternative.

**Rejected position:** Flat naming (handler- only, plain names for everything else). functional-decomposition's compromise position is pragmatic but undersells the navigability benefit. At 9-11 files, knowing which files are dispatch targets (`handler-`) and which are shared subsystems (`subsystem-`) from a directory listing alone is operationally valuable. Plain names for subsystems (`dispute-parsing.md`, `preset-resolution.md`) are self-explanatory to someone who knows the architecture but opaque to a contributor encountering the directory for the first time. The `subsystem-` prefix resolves this at zero cost.

**Required changes:**
1. All subcommand handler reference files use the `handler-` prefix: `handler-gate.md`, `handler-define.md`, `handler-interests.md`, `handler-mode.md`, `handler-converge.md`, `handler-arbitrate.md`.
2. All shared subsystem reference files use the `subsystem-` prefix: `subsystem-preset-resolution.md`, `subsystem-dispute-parsing.md`.
3. Informational reference files (e.g., operational notes) use plain names without a prefix for now. If more than two informational reference files accumulate in future specs, adopt the `notes-` prefix retroactively.
4. Document the naming convention in SKILL.md alongside the dispatch table, so that contributors creating new reference files follow the pattern.
5. This convention must be decided and documented before Phase 1 extraction begins to avoid retroactive renames.

---

### Dispute D: Validation Rules — Shared Reference File vs. Co-Location in Handlers

**Positions:**
- **Shared reference file** (`references/validation-rules.md` for patterns in 3+ handlers): agentskills-specialist.
- **Co-location in each handler** with a canonical pattern section in SKILL.md core: functional-decomposition.

**Synthesizer's assessment:** Legitimate design trade-off between DRY centralization and handler self-containment. The answer depends on the actual count of shared validation patterns. The synthesizer recommended deferring until handler reference files are drafted.

**Ruling:** Defer this decision until Phase 2 of staged decomposition. Co-locate validation rules in each handler as the default. Create a shared `references/subsystem-validation-rules.md` only if the empirical count of patterns appearing verbatim in 3 or more handlers reaches 4 or more.

**Grounding citation:** Principle 1 (context isolation produces genuinely adversarial positions — extended to: context self-containment produces reliable handler execution). Each handler reference file should be a complete specification for its subcommand's execution. A handler that requires loading a second reference file for validation rules is less self-contained than one that includes its own validation inline. Self-containment is a stronger default for an orchestration engine where execution correctness is paramount.

**Rationale:** This dispute cannot be resolved without data that does not yet exist. No one has drafted the handler reference files, so no one knows how many validation patterns are actually shared across 3+ handlers. Deciding now based on predicted sharing is speculation. The co-location default is correct because it preserves handler self-containment (each handler is one file load) and because the migration path from co-location to a shared file is straightforward (extract common patterns when the count is known). The reverse migration — from a shared file back to co-location — is harder because it requires duplicating content back into each handler. Starting with the easier-to-reverse default is prudent. functional-decomposition's argument about classification overhead ("is this pattern shared enough?") is valid but secondary to the self-containment argument. agentskills-specialist's concern about validation drift (updating the same regex in six files) is real and becomes the trigger for extraction if the empirical count warrants it.

**Rejected position:** Immediate creation of a shared reference file. agentskills-specialist's position is architecturally sound in principle but premature in practice. The 3-handler threshold is reasonable, but the handler files do not exist yet. Creating a shared validation file before the handlers are drafted risks either (a) pre-populating it with patterns that turn out not to be shared, or (b) creating an empty file that accrues content ad-hoc without the empirical validation the threshold was designed to provide. The deferral respects agentskills-specialist's threshold criterion by insisting that it be applied to actual data.

**Required changes:**
1. During Phase 2 of staged decomposition (handler extraction), include validation rules inline in each handler reference file as self-contained content.
2. After all handler reference files are drafted, count validation patterns that appear verbatim in 3 or more handlers.
3. If 4 or more such patterns exist, extract them to `references/subsystem-validation-rules.md` with a Class B load trigger from each consuming handler. Update each handler to reference the shared file instead of carrying the inline copy.
4. If fewer than 4 such patterns exist, retain co-located validation in each handler. Document the shared patterns with a comment noting they are intentionally duplicated for self-containment, with a canonical definition in SKILL.md core.
5. Record the empirical count and the decision in the spec's implementation notes for traceability.

---

## Summary of Changes Required

Ordered by priority, with dependencies noted:

1. **[Immediate] Decide and document the two-tier naming convention** (`handler-`, `subsystem-`) in SKILL.md before any reference file is created. (Dispute C ruling.)

2. **[Immediate] Document the run engine token exception** in SKILL.md. Add a note near the top of the Run: Execution section acknowledging that the engine specification exceeds the agentskills sizing guideline and explaining why. (Dispute A ruling, change 2.)

3. **[Immediate] Add "do not decompose" annotation** to the round/iteration state machine section in SKILL.md. (Dispute B ruling, change 2.)

4. **[Phase 1] Extract gate handler to `references/handler-gate.md`** using the established naming convention. (Convergence point, unchanged by arbitration.)

5. **[Phase 2] Extract guided handlers** (`handler-define.md`, `handler-interests.md`, `handler-mode.md`, `handler-converge.md`, `handler-arbitrate.md`) with validation rules co-located in each handler. (Convergence point + Dispute D ruling.)

6. **[Phase 2, post-extraction] Count shared validation patterns** across all drafted handler files. If 4+ patterns appear in 3+ handlers, extract to `references/subsystem-validation-rules.md`. (Dispute D ruling, change 2-3.)

7. **[Phase 2, post-extraction] Execute the engine placement comparison test.** Run `/conversus converge` with the engine in SKILL.md (current) and with the engine hypothetically in `references/handler-run.md`. Compare output fidelity. Record results. (Dispute A ruling, change 3.)

8. **[Phase 3] Extract conditional subsystems** (`subsystem-preset-resolution.md`, `subsystem-dispute-parsing.md`) if handler extractions succeed. (Convergence point, unchanged by arbitration.)

9. **[Ongoing] Remove `references/multi-round-execution.md`** from all proposed directory layouts and planning documents. (Dispute B ruling, change 3.)

---

## Confidence Assessment

| Dispute | Ruling | Confidence | Basis |
|---|---|---|---|
| A: Run Engine Placement | Retain in SKILL.md, test extraction later | **High** | The two-hop chain challenge was unanswered; the failure mode asymmetry (silent degradation vs. token cost) strongly favors the conservative default; the staged test provides a clear path to revision. |
| B: Multi-Round Extraction | No extraction, no dependency analysis gate | **Very High** | The negation-definition argument is unanimously acknowledged as the strongest single argument in the deliberation. All 5 agents agreed the state machine must not be split. This ruling simply removes the conditional escape hatch that was never architecturally justified. |
| C: Naming Convention | Two-tier (`handler-`, `subsystem-`) | **High** | The two-tier convention has 3-agent support, maps to the agreed architectural hierarchy, and agentskills-specialist moved toward accepting it. The only risk is the single anticipated informational file without a tier — manageable. |
| D: Validation Rules | Defer, co-locate as default | **Moderate** | Both positions are architecturally defensible. The ruling favors self-containment and easy reversibility but the empirical count could favor extraction. The moderate confidence reflects genuine uncertainty about the right long-term answer — but the deferred decision structure means the ruling will be validated by data before it becomes permanent. |

### Deliberation Quality Assessment

This was a high-quality cooperative deliberation. The 5 agents produced genuinely independent analyses that exposed real architectural tensions — particularly the two-hop chain problem (agentskills-specialist), the negation-definition argument (integration-specialist), the token cost asymmetry (integration-specialist), and the silent failure mode analysis (functional-decomposition, agentskills-specialist). The most valuable moment in the deliberation was the position inversion between integration-specialist and agentskills-specialist on engine placement: integration-specialist moved from retention to extraction while agentskills-specialist moved from extraction to retention. This inversion demonstrates that the cross-review process changed minds based on evidence, not merely reinforced priors.

The apm-specialist's full reversal on sub-skills as the primary decomposition mechanism was the largest and most important concession. It resolved what could have been the dominant dispute and allowed the deliberation to focus on the genuinely difficult structural questions. The agents-md-specialist's narrowing from inline rule restatement to pointer-based AGENTS.md files was similarly productive. Both reversals were driven by cross-review evidence, validating the adversarial process.

The remaining disputes are legitimately hard. Disputes A and D are empirical questions where the deliberation correctly identified that argument alone cannot resolve them — only evidence from the staged implementation can. Dispute B was resolvable from the arguments alone; the negation-definition argument is conclusive. Dispute C was a low-stakes convention decision that needed a tiebreaker, not further analysis. The arbitration process was appropriate for all four: the subject (conversus) has operational knowledge about which failure modes are most dangerous in practice, which is the information the external agents lacked.
