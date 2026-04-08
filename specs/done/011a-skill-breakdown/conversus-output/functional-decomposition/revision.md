# Functional Decomposition — Revision 1

## Recommendation Dispositions

### Recommendation 1: Extract gate handler to references/ (was P1)

**Original position:** Move L1881-2178 (~300 lines) to `references/gate-handler.md`, replacing it with a one-line load trigger in the dispatch table.

**Disposition:** Surviving.

**Explanation:** This recommendation received universal agreement across all four cross-reviews. integration-specialist calls it a Safe Agreement ("the highest-value extraction target"). apm-specialist identifies it as "architecturally independent" with "a clean extraction boundary." agentskills-specialist calls it "the highest-priority extraction candidate." agents-md-specialist confirms "its 300-line, zero-shared-state, no-interactive-prompt profile makes it the lowest-risk extraction target." No reviewer challenged the extraction boundary, the naming, the trigger mechanism, or the priority. This is the single recommendation with zero dissent.

---

### Recommendation 2: Extract guided handlers (define, interests, mode, converge, arbitrate) to references/ (was P1)

**Original position:** Extract each to its own reference file (`references/handler-define.md`, etc.), with dispatch-table load triggers.

**Disposition:** Surviving, with one modification.

**Explanation:** All four cross-reviews agree that subcommand handlers are primary extraction candidates (integration-specialist Safe Agreement 1, agentskills-specialist Safe Agreement 1). The modification concerns the `converge` handler specifically. integration-specialist's Tension 5 correctly identifies that converge's post-execution report (~75 lines) overlaps with the run engine's Step 5 report, creating drift risk if both are in separate files without a shared report vocabulary. agentskills-specialist's Tension 2 raises the related concern that converge and arbitrate are thin wrappers that delegate to the run engine, creating a two-file chain. I accept the drift risk is real for converge but maintain extraction is still correct — the alternative (keeping converge inline) means every `/conversus define` invocation pays for converge's 210 lines. The modification: the converge handler reference file must include an explicit cross-reference to the run engine's Step 5 report format, documenting which report fields it shares and which it extends. This addresses the drift risk without sacrificing the extraction benefit.

---

### Recommendation 3: Extract Dispute-Parsing Subsystem to a shared reference (was P1)

**Original position:** Move L750-778 (~28 lines) to `references/dispute-parsing.md`, with load triggers in each consumer.

**Disposition:** Modified — downgraded to P2 and made conditional on empirical validation of handler extractions.

**Explanation:** agents-md-specialist's Dangerous Contradiction 2 changed my position. The cross-review correctly identifies that I simultaneously argued (a) in Recommendation 10 that gotchas and cross-cutting invariants with breaking-change implications "should always be in context," and (b) in Recommendation 3 that the Dispute-Parsing Subsystem — which declares its structural markers as a stable interface where changes are breaking changes — should be extracted to a reference file. This is internally inconsistent. The subsystem is 28 lines. The token savings (~400 tokens) are negligible. The subsystem's four consumers span the run engine, converge, gate, and Phase 6 — meaning it is relevant to the majority of invocation paths. integration-specialist's Dangerous Contradiction 2 adds that if the run engine is in SKILL.md but dispute parsing is in a reference file, the load-trigger must be embedded in the always-loaded body, "partially defeating the extraction."

However, I do not fully withdraw. The architectural value of making the interface contract physically addressable remains real — as I noted in my own cross-review of agentskills-specialist (Tension 2), the value is not token savings but eliminating a cross-cutting inline dependency buried in the run engine section. The modified recommendation: defer this extraction until after handler extractions (Recs 1-2) are implemented and validated. If the handler extractions succeed and the agent reliably follows conditional load triggers, extract dispute-parsing as a P2 item. If the handler extractions reveal that agents struggle with reference loading, keep dispute-parsing inline as a 28-line gotcha.

---

### Recommendation 4: Extract multi-round orchestration to a conditional reference (was P2)

**Original position:** Move L248-610 (~360 lines) to `references/multi-round-orchestration.md`, loaded conditionally when `rounds > 1`.

**Disposition:** Modified — now contingent on resolving the single-round/multi-round dependency.

**Explanation:** integration-specialist's Dangerous Contradiction 1 is the strongest critique any reviewer made of any recommendation. The cross-review identifies that the multi-round block contains output path formulas, retroactive Round 1 directory moves, and termination conditions that the single-round path depends on for its negative-case definitions. Extracting multi-round means the single-round path must "restate what 'no round directories' means without referencing the round directory logic it is opting out of." agentskills-specialist's Tension 5 independently raises the same concern: "Neither review performs a dependency analysis to verify that the multi-round logic can be extracted without duplicating single-round path references."

I accept that my original recommendation treated the multi-round extraction boundary as cleaner than it is. The modified recommendation: before extracting, perform an explicit dependency analysis of lines 248-610 to identify which elements the single-round path references (even by negation). If the dependency analysis reveals that single-round and multi-round share fewer than 20 lines of interface, extract with the shared interface duplicated in both SKILL.md and the reference file. If the shared interface exceeds 20 lines, keep multi-round orchestration in SKILL.md and accept the ~360-line context cost, per integration-specialist's position.

integration-specialist's Dangerous Contradiction 2 also correctly notes that even with extraction, the per-invocation total for a multi-round run would be ~8k tokens — exceeding the 5k guideline regardless. Both reviews should acknowledge that conversus, as an orchestration engine, may legitimately exceed the 500-line / 5k-token guideline for the run engine. I accept this framing.

---

### Recommendation 5: Extract preset resolution to a conditional reference (was P2)

**Original position:** Move L126-200 (~75 lines) to `references/preset-resolution.md`, loaded when any agent uses `preset:`.

**Disposition:** Surviving.

**Explanation:** No cross-review challenged the extraction boundary or the conditional trigger. integration-specialist's Dangerous Contradiction 3 raises a valid concern about mid-execution conditional loading being riskier than pre-invocation dispatch routing. I accept the distinction (addressed in New Recommendation 1 below) but maintain that preset resolution is a clean extraction because: (a) the trigger fires during config parsing, before execution begins, not mid-execution; (b) 75 lines is modest but the composition template blocks (L153-190) are particularly noisy for presetless configs; (c) apm-specialist agrees on extraction (to a different destination) and agentskills-specialist proposes the same trigger condition. The only tension is where it lives (`references/` vs `.apm/context/`), which is resolved by the broader strategy decision between agentskills references and APM sub-skills. I maintain the `references/` approach as the lower-overhead option during active spec development.

---

### Recommendation 6: Create a shared validation contract reference (was P2)

**Original position:** Create `references/validation-contract.md` defining shared heading checks, name pattern regex, path existence verification, and post-write validation patterns.

**Disposition:** Modified — now a consolidation reference rather than a standalone load target.

**Explanation:** Three cross-reviews raised concerns about this recommendation from different angles. integration-specialist's Tension 2 notes that a shared validation reference file and an expanded linter create a synchronization burden — "maintaining both creates a synchronization burden." apm-specialist's Tension 4 makes the same point: specification consolidation and automated enforcement are complementary but the reviews present them as alternatives. agentskills-specialist's Dangerous Contradiction 4 identifies that if the validation file is referenced from SKILL.md directly, it may load eagerly on every invocation, partially negating decomposition benefits.

The modification: the validation contract should not be a standalone reference file loaded via SKILL.md. Instead, validation rules should be embedded within each handler reference file (co-located with the handler they serve), with a brief "canonical validation patterns" section in the run engine core (~10-15 lines) that defines the shared algorithm once. Each handler reference file then says "Apply the canonical validation pattern from SKILL.md core" rather than loading a separate file. This addresses agentskills-specialist's eager-loading concern, integration-specialist's synchronization concern, and my original goal of reducing validation drift — the canonical definition lives in the always-loaded core, and handlers reference it without a separate file load.

---

### Recommendation 7: Retain the run engine core (~265 lines) in SKILL.md (was P2)

**Original position:** Keep the single-round run engine core (~265 lines after multi-round, preset, and dispute-parsing extraction) in SKILL.md.

**Disposition:** Modified — the retained core will likely be larger than originally estimated.

**Explanation:** agentskills-specialist's Dangerous Contradiction 1 proposes extracting the run engine itself to `references/handler-run.md`, leaving only a one-paragraph-per-phase summary. My cross-review of agentskills-specialist (Dangerous Contradiction 2) explains why this is dangerous: converge and gate both delegate to the run engine, creating a fragile two-hop loading dependency. I maintain that the run engine core must stay in SKILL.md.

However, the retained core size depends on the disposition of Recommendation 4 (multi-round extraction). If the dependency analysis from Rec 4 shows that multi-round orchestration cannot be cleanly extracted, the retained run engine core grows from ~265 lines to ~625 lines. Combined with dispatch table, notes, and frontmatter, the SKILL.md would be ~700-750 lines — exceeding the 500-line guideline. I accept integration-specialist's framing (Dangerous Contradiction 2): conversus may legitimately exceed the 500-line / 5k-token guideline for the root SKILL.md, and the token budget should document this as an acknowledged exception rather than a failure to decompose.

The modified position: the run engine core stays in SKILL.md regardless of its size. The target is the smallest correct core, not a fixed line count. If multi-round extracts cleanly, ~345 lines. If it does not, ~700 lines with a documented exception.

---

### Recommendation 8: Add explicit load-trigger instructions for each reference file (was P2)

**Original position:** Every extracted reference file must have an unambiguous one-line conditional load instruction.

**Disposition:** Modified — now distinguishes two classes of load triggers.

**Explanation:** integration-specialist's Dangerous Contradiction 3 makes a distinction I failed to draw: dispatch-table triggers fire at invocation time before execution begins (safe), while conditional subsystem triggers fire mid-execution based on config inspection (risky). I treated both as equivalent ("conditional load trigger is clean and unambiguous"), but they have different failure modes. apm-specialist's Dangerous Contradiction 2 reinforces this: structural separation (APM sub-skills) is more reliable than instructional separation (conditional triggers in SKILL.md).

The modified recommendation distinguishes two classes:
- **Class A — Pre-invocation dispatch triggers**: "When `/conversus gate` is invoked, read `references/gate-handler.md`." These fire before execution, are unambiguous, and have no failure mode beyond the reference file being missing. All subcommand handler extractions (Recs 1-2) use Class A triggers.
- **Class B — Config-conditional triggers**: "If any agent entry has a `preset` field, read `references/preset-resolution.md`." These require the agent to inspect config before loading. Class B triggers must include explicit fallback behavior: "If `references/preset-resolution.md` cannot be loaded, halt and report the error — do not attempt to resolve presets without the reference." Class B triggers should be minimized; prefer embedding content in the always-loaded core if the alternative is a fragile mid-execution load.

This classification credit goes to integration-specialist.

---

### Recommendation 9: Estimate and document the token budget per invocation path (was P3)

**Original position:** Add a "Context Budget" section documenting expected token load per invocation path.

**Disposition:** Surviving, with scope adjustment.

**Explanation:** agentskills-specialist's Tension 1 correctly observes that maintaining token counts after every edit creates operational overhead. integration-specialist's Dangerous Contradiction 2 notes that both reviews' targets are incompatible with run engine retention — the per-invocation total for complex runs will exceed 5k regardless. I accept the framing from integration-specialist: the budget should document an acknowledged exception for the run engine, not pretend the 5k target is achievable for all paths.

The scope adjustment: document the token budget once at decomposition time as a baseline. Include an explicit exception for `/conversus run` paths ("this skill's orchestration engine legitimately exceeds the 5,000-token guideline; the target is proportional reduction, not absolute compliance"). Revisit the budget during major structural revisions, not after every content edit.

---

### Recommendation 10: Preserve "Important Notes" and "Baseline Features" in SKILL.md (was P3)

**Original position:** Keep both sections in their entirety in the always-loaded SKILL.md core.

**Disposition:** Modified — per-item classification rather than blanket retention.

**Explanation:** agentskills-specialist's Dangerous Contradiction 3 correctly challenges my blanket retention. The cross-review distinguishes between genuine gotchas (overwrite semantics, background dispatch, model selection) and derivable reference material (agent count formulas, worked examples). My cross-review of agentskills-specialist (Tension 4) countered that the agent count formula requires correctly interpreting Phase 2 cross-review combinatorics, which is error-prone — but this is an empirical question, not an architectural one.

The modified recommendation: classify each item individually.
- **Retain in SKILL.md** (genuine gotchas): overwrite semantics ("re-running conversus overwrites existing output files without warning"), model selection ("all subagents use the orchestrator's model"), rounds/iterations orthogonality ("rounds and iterations are orthogonal dimensions"), background dispatch semantics.
- **Move to reference file** (derivable/informational): worked formula examples ("For 3 agents without arbiter: 16 total agent launches"), baseline feature inventory, detailed orthogonality explanation.

Credit to agentskills-specialist for forcing the per-item analysis.

---

## New Recommendations

### New Recommendation A: Separate contribution-oriented content from execution logic before decomposition

agents-md-specialist's Dangerous Contradiction 3 identifies content in SKILL.md that is contribution guidance rather than execution logic: antipattern check instructions (L239-244), template naming conventions (L283-289), preset file validation rules (L139-145), and linter invocation instructions (L309). My review did not distinguish these two categories and would have scattered contribution guidelines across `references/` files, making them harder to extract into AGENTS.md later.

**Recommendation:** Before executing the reference-file decomposition, tag all contribution-oriented lines in SKILL.md. Move them to the root AGENTS.md or nested AGENTS.md files (per agents-md-specialist's recommendations). Then decompose the remaining execution logic into references. This ordering prevents the contribution-execution interleaving that agents-md-specialist warns about. The effort is small (agents-md-specialist estimates 200-400 tokens of contribution content), and it establishes the SKILL.md/AGENTS.md boundary cleanly before the larger structural work begins.

**Priority:** P1 — this should happen before Recommendations 1-2, as a preparatory step.

### New Recommendation B: Stage the decomposition with empirical validation between phases

agents-md-specialist's Dangerous Contradiction 1 proposes staging: "extract the most self-contained handlers first (gate, then one guided handler), validate that conditional loading works reliably in practice, and only then proceed to extract tightly coupled subsystems." apm-specialist's Tension 5 raises the same timing concern: active spec development creates restructuring drag.

**Recommendation:** Execute the decomposition in three phases with validation gates:
1. **Phase 1**: Extract gate handler (Rec 1) + one guided handler (define, as the simplest). Validate that the agent correctly loads the reference files, follows the triggers, and produces correct output.
2. **Phase 2**: If Phase 1 succeeds, extract remaining guided handlers (Rec 2). If Phase 1 reveals load-trigger failures, adjust the trigger mechanism before proceeding.
3. **Phase 3**: If Phase 2 succeeds, extract conditional subsystems (preset resolution, multi-round if dependency analysis permits). If Phase 2 reveals that multiple reference files degrade agent performance, consolidate rather than further decomposing.

This staging addresses the concern — shared across integration-specialist, agents-md-specialist, and apm-specialist — that the decomposition is being planned as an all-or-nothing structural change without empirical validation.

**Priority:** P1 — this is a process recommendation that governs the execution of all other recommendations.

### New Recommendation C: Adopt type-prefixed naming for reference files

integration-specialist's Tension 3 (naming convention scope) and my cross-review of integration-specialist (Tension 3) identified a divergence: I used ad-hoc names (`dispute-parsing.md`, `multi-round-orchestration.md`) while integration-specialist proposed `handler-{name}.md`, `subsystem-{name}.md`, `contract-{name}.md`. At 8-10 reference files, the navigability benefit is modest. But with the staged decomposition (New Rec B), the reference directory will grow incrementally, and type prefixes make the dependency graph legible from a directory listing alone without requiring agents or contributors to read each file.

**Recommendation:** Adopt integration-specialist's three-tier naming convention: `handler-{name}.md` for subcommand handlers, `subsystem-{name}.md` for shared subsystems (dispute-parsing, if extracted), `notes-{name}.md` for informational reference material (operational-notes, if extracted). This is a minor convention but worth establishing before the first extraction to avoid retroactive renames.

**Priority:** P3 — naming convention, low urgency but should be decided before Phase 1 execution.

---

## Position Summary

Of the 10 original recommendations, 4 survive unchanged (Recs 1, 5, 8-concept, 9), 5 are modified (Recs 2, 3, 4, 6, 7, 8, 10 — several with significant scope changes), and 0 are withdrawn. Three new recommendations were added: separating contribution content before decomposition (New A), staging with empirical validation (New B), and type-prefixed naming (New C).

The most significant change is the disposition of Recommendation 4 (multi-round extraction). integration-specialist's critique that the single-round and multi-round paths share a state machine with negative-case dependencies was the strongest argument in any cross-review. I originally treated the `rounds > 1` boundary as a clean extraction seam, but the dependency analysis has not been done, and the extraction may split a tightly coupled state machine. This concession has cascading effects: if multi-round stays in SKILL.md, Recommendation 7's retained core grows from ~265 to ~625 lines, the root SKILL.md lands at ~700 lines (exceeding the 500-line guideline), and the token budget (Rec 9) must document an acknowledged exception rather than claiming compliance. I accept this outcome. A 700-line SKILL.md that correctly preserves its internal state machine is better than a 345-line SKILL.md that silently breaks the round/iteration logic through an unvalidated extraction boundary.

The highest-priority surviving recommendation remains Recommendation 1 (extract gate handler), now preceded by New Recommendation A (separate contribution content) and governed by New Recommendation B (staged execution with validation gates). The gate handler extraction is zero-risk, universally endorsed, and removes 300 lines from every invocation. It should be the first structural change implemented, serving as both a meaningful improvement and an empirical test of the reference-loading mechanism that all subsequent extractions depend on.
