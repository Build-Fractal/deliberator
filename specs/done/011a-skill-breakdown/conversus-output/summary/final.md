# Neutral Synthesis — Spec 011a: SKILL.md Breakdown

---

## Process Summary

- **Agents:** 5 (functional-decomposition, integration-specialist, apm-specialist, agentskills-specialist, agents-md-specialist)
- **Phase 1 Reviews:** 5
- **Phase 2 Cross-Reviews:** 20 (each agent reviewed 4 others)
- **Phase 3 Revisions:** 5
- **Phase 4 Dispute Documents:** 5

**Recommendation counts across all agents:**
- Phase 1 recommendations proposed: 50 (10 per agent)
- Phase 3 dispositions: 18 surviving/maintained, 22 modified/revised, 5 withdrawn, 5 new recommendations added (total new: 17 across all agents)
- Phase 4 surviving disputes: 4 distinct dispute clusters (run engine placement, dispute-parsing extraction timing, naming convention, multi-round extraction)
- Phase 4 convergence points: 5 unanimous or near-unanimous

**Deliberation mode:** Cooperative

---

## Recommendation Scorecard

| # | Agent | Recommendation | P1 Priority | P3 Disposition | Challenged By | Convergence | Final Status |
|---|-------|---------------|-------------|----------------|---------------|-------------|--------------|
| F1 | functional-decomposition | Extract gate handler to references/ | P1 | Surviving | None | Unanimous (all 5) | **Accepted** |
| F2 | functional-decomposition | Extract guided handlers to references/ | P1 | Surviving (modified — converge cross-ref) | integration-specialist (converge drift risk) | Unanimous | **Accepted-Modified** |
| F3 | functional-decomposition | Extract Dispute-Parsing Subsystem | P1 | Modified — downgraded to P2, conditional | agents-md-specialist, functional-decomposition self-correction | Majority (4 support extraction, 1 defers) | **Accepted-Modified** |
| F4 | functional-decomposition | Extract multi-round orchestration | P2 | Modified — contingent on dependency analysis | integration-specialist (state machine coupling) | Disputed | **Disputed** |
| F5 | functional-decomposition | Extract preset resolution | P2 | Surviving | None | Unanimous | **Accepted** |
| F6 | functional-decomposition | Shared validation contract reference | P2 | Modified — consolidation reference, not standalone | integration-specialist, agentskills-specialist, apm-specialist | Partial convergence | **Accepted-Modified** |
| F7 | functional-decomposition | Retain run engine core in SKILL.md | P2 | Modified — core size may be larger | agentskills-specialist (extract), integration-specialist (extract) | Disputed | **Disputed** |
| F8 | functional-decomposition | Explicit load-trigger instructions | P2 | Modified — two-class trigger model | integration-specialist (Class A/B distinction) | Majority (4/5) | **Accepted-Modified** |
| F9 | functional-decomposition | Document token budget per invocation | P3 | Surviving (scope adjusted) | agentskills-specialist (maintenance overhead) | Majority | **Accepted-Modified** |
| F10 | functional-decomposition | Preserve Important Notes in SKILL.md | P3 | Modified — per-item classification | agentskills-specialist (formula redundancy) | Converged on per-item triage | **Accepted-Modified** |
| FA | functional-decomposition | Separate contribution content before decomp (NEW) | P1 | New | agents-md-specialist (sequencing dispute) | Majority | **Accepted-Modified** |
| FB | functional-decomposition | Staged decomposition with validation gates (NEW) | P1 | New | None | Unanimous | **Accepted** |
| FC | functional-decomposition | Adopt type-prefixed naming (NEW) | P3 | New | agentskills-specialist (partial) | Disputed (minor) | **Disputed** |
| I1 | integration-specialist | Keep engine + dispatch + rules in root SKILL.md | — | Modified — concedes engine extraction | agentskills-specialist, functional-decomposition | Disputed | **Disputed** |
| I2 | integration-specialist | Extract guided workflow handlers | — | Sustained | None | Unanimous | **Accepted** |
| I3 | integration-specialist | Extract gate handler | — | Sustained | None | Unanimous | **Accepted** |
| I4 | integration-specialist | Extract Dispute-Parsing Subsystem | — | Sustained (loading model clarified) | functional-decomposition (timing) | Majority | **Accepted-Modified** |
| I5 | integration-specialist | Extract preset resolution | — | Sustained | None | Unanimous | **Accepted** |
| I6 | integration-specialist | Extract template variable documentation | — | Modified — stays co-located with engine | agentskills-specialist (execution cost) | Converged | **Accepted-Modified** |
| I7 | integration-specialist | Define "do not decompose" boundaries | — | Modified — applies within handler-run.md | agentskills-specialist (root placement not required) | Unanimous (principle) | **Accepted-Modified** |
| I8 | integration-specialist | Mandate linter expansion | — | Modified — phased scope | apm-specialist, agentskills-specialist | Converged | **Accepted-Modified** |
| I9 | integration-specialist | Naming convention for reference files | — | Sustained (simplified to two-tier) | agentskills-specialist | Majority (4/5) | **Accepted-Modified** |
| I10 | integration-specialist | Add dependency map to root SKILL.md | — | Withdrawn | agentskills-specialist (redundant with dispatch table) | — | **Rejected** |
| IN1 | integration-specialist | Dual-audience multi-agent rules (NEW) | — | New | None | Converged | **Accepted** |
| IN2 | integration-specialist | Two-class reference loading (NEW) | — | New | None | Unanimous (4/5 explicit) | **Accepted** |
| IN3 | integration-specialist | AGENTS.md vs reference file authority (NEW) | — | New | None | Unanimous | **Accepted** |
| IN4 | integration-specialist | Antipattern check placement (NEW) | — | New | None | Converged | **Accepted** |
| A1 | apm-specialist | Create 3 APM sub-skills immediately | — | Revised — withdraw as primary strategy | All 4 cross-reviewers | Unanimous reversal | **Rejected** |
| A2 | apm-specialist | Mode specs as APM context files | — | Revised — withdraw, use references/ | integration-specialist, agents-md-specialist | Unanimous reversal | **Rejected** |
| A3 | apm-specialist | Presets as APM sub-skill | — | Revised — withdraw, use references/ | agentskills-specialist, functional-decomposition | Unanimous reversal | **Rejected** |
| A4 | apm-specialist | Dispute-Parsing to APM context | — | Revised — keep extraction, change to references/ | All 4 | Converged on references/ | **Accepted-Modified** |
| A5 | apm-specialist | Antipattern catalog as APM context | — | Revised — withdraw, keep current location | agentskills-specialist, agents-md-specialist | Converged | **Rejected** |
| A6 | apm-specialist | PostToolUse hook for template validation | — | Revised — withdraw | agentskills-specialist, agents-md-specialist, integration-specialist | Unanimous reversal | **Rejected** |
| A7 | apm-specialist | Schema files as APM context primitives | — | Revised — withdraw | integration-specialist | Converged | **Rejected** |
| A8 | apm-specialist | Defer full APM distribution | — | Maintained | None | Unanimous | **Accepted** |
| A9 | apm-specialist | Validate sub-skill deployment | — | Revised — scope to gate only | — | — | **Accepted-Modified** |
| A10 | apm-specialist | Document sub-skill dependency graph | — | Revised — reference dependency map | — | Converged | **Accepted-Modified** |
| AN1 | apm-specialist | Gate as sole sub-skill candidate (NEW) | — | New | None (timing questioned) | Majority | **Accepted** |
| AN2 | apm-specialist | Explicit load triggers, not applyTo (NEW) | — | New | None | Unanimous | **Accepted** |
| AN3 | apm-specialist | APM role is structural preparation (NEW) | — | New | None | Unanimous | **Accepted** |
| S1 | agentskills-specialist | Extract each handler to reference file | — | Revised — exclude run engine | functional-decomposition, integration-specialist (two-hop chain) | Disputed (run engine portion) | **Accepted-Modified** |
| S2 | agentskills-specialist | Define always-loaded SKILL.md core | — | Revised — 450-550 lines, 6-8k tokens | integration-specialist (target too low) | Disputed | **Disputed** |
| S3 | agentskills-specialist | Extract Dispute-Parsing Subsystem | — | Maintained | functional-decomposition (timing) | Majority | **Accepted** |
| S4 | agentskills-specialist | Extract template variable contracts | — | Revised — split inline/reference | integration-specialist (co-location) | Converged | **Accepted-Modified** |
| S5 | agentskills-specialist | Extract validation rules | — | Revised — shared patterns only (3+ handlers) | functional-decomposition (co-location preference) | Disputed (minor) | **Disputed** |
| S6 | agentskills-specialist | Move output schemas to assets/ | — | Withdrawn | functional-decomposition (co-locate with handler) | — | **Rejected** |
| S7 | agentskills-specialist | Move preset resolution to references/ | — | Maintained | None | Unanimous | **Accepted** |
| S8 | agentskills-specialist | Restructure Important Notes | — | Revised — per-item classification | functional-decomposition, agents-md-specialist | Converged | **Accepted-Modified** |
| S9 | agentskills-specialist | Conditional loading instructions | — | Revised — two-tier trigger model | functional-decomposition (sequencing) | Converged | **Accepted-Modified** |
| S10 | agentskills-specialist | Proposed directory layout | — | Revised — no handler-run.md, fewer files | Multiple | Converged (partially) | **Accepted-Modified** |
| SA | agentskills-specialist | Triage contribution content (NEW) | — | New | None | Converged | **Accepted** |
| SB | agentskills-specialist | Expand linter post-decomposition (NEW) | — | New | None | Converged | **Accepted** |
| SC | agentskills-specialist | Document per-invocation token budgets (NEW) | — | New | functional-decomposition (format) | Converged | **Accepted-Modified** |
| SD | agentskills-specialist | Antipattern check in run engine core (NEW) | — | New | None | Converged | **Accepted** |
| M1 | agents-md-specialist | Create templates/AGENTS.md | — | Revised — pointer-based only | All 4 (runtime contract concern) | Converged | **Accepted-Modified** |
| M2 | agents-md-specialist | Create presets/AGENTS.md | — | Revised — pointer file | All 4 | Converged | **Accepted-Modified** |
| M3 | agents-md-specialist | Create schema/AGENTS.md | — | Revised — narrowed | All 4 | Converged | **Accepted-Modified** |
| M4 | agents-md-specialist | Create linter/AGENTS.md | — | Maintained | None | Unanimous | **Accepted** |
| M5 | agents-md-specialist | Update root AGENTS.md | — | Maintained (scope constrained) | functional-decomposition (scope creep) | Unanimous | **Accepted-Modified** |
| M6 | agents-md-specialist | Do not move execution logic to AGENTS.md | — | Maintained | None | Unanimous | **Accepted** |
| M7 | agents-md-specialist | File relationship section in AGENTS.md | — | Withdrawn | integration-specialist, functional-decomposition | — | **Rejected** |
| M8 | agents-md-specialist | Extract contribution content from SKILL.md | — | Revised — narrowed to exclude runtime rules | All 4 | Converged | **Accepted-Modified** |
| M9 | agents-md-specialist | Keep AGENTS.md under 100 lines | — | Maintained | None | Unanimous | **Accepted** |
| M10 | agents-md-specialist | Consider antipatterns/AGENTS.md | — | Maintained (conditional) | None | Accepted | **Accepted** |
| MA | agents-md-specialist | Single-source-of-truth pointer convention (NEW) | — | New | None | Unanimous | **Accepted** |
| MB | agents-md-specialist | Sequence AGENTS.md after reference extraction (NEW) | — | New | functional-decomposition (timing nuance) | Majority | **Accepted** |
| MC | agents-md-specialist | Linter validates AGENTS.md accuracy (NEW) | — | New | None (silence) | Not contested | **Accepted** |

---

## Dangerous Contradictions Found

### Resolved Contradictions

1. **APM sub-skills vs. agentskills references/ as primary decomposition mechanism.** apm-specialist's original central recommendation (three APM sub-skills) conflicted with all other agents' references/ approach. **Resolved:** apm-specialist fully reversed position in Phase 3, conceding that sub-skills solve distribution problems while conversus has a context window problem. The references/ model is unanimously adopted.

2. **APM context primitives vs. references/ for dispute parsing, mode specs, and antipatterns.** apm-specialist proposed `.apm/context/` files; all others proposed `references/`. **Resolved:** apm-specialist conceded that APM context files lack runtime conditional loading (`applyTo` matches paths, not config values). All execution content goes to `references/`.

3. **PostToolUse hook vs. explicit linter instruction.** apm-specialist proposed APM hook; three agents identified the trigger mismatch (hook fires on template writes during development, not execution), Claude-Code-only scope, and scope limitation. **Resolved:** apm-specialist withdrew. Explicit linter instruction in SKILL.md retained.

4. **AGENTS.md duplicating runtime contracts.** agents-md-specialist originally proposed inline rule restatement in nested AGENTS.md files. All four cross-reviewers identified that preset validation, template naming, and structural markers are runtime-enforced contracts. **Resolved:** agents-md-specialist revised to pointer-only AGENTS.md files (15-30 lines each) that reference authoritative locations.

5. **Output schemas in assets/ vs. co-located with handlers.** agentskills-specialist proposed `assets/` directory; functional-decomposition argued schemas are structural contracts, not reusable templates. **Resolved:** agentskills-specialist withdrew. Schemas stay co-located in handler reference files.

6. **Dependency map table in root SKILL.md.** integration-specialist proposed; agentskills-specialist argued it duplicates the dispatch table and creates a drift surface. **Resolved:** integration-specialist withdrew. Each handler declares its own dependencies at the top of its reference file.

7. **Template variable documentation as standalone reference.** integration-specialist proposed `references/contract-template-variables.md`; agentskills-specialist identified three-file read cost per phase. **Resolved:** integration-specialist revised. Per-phase variable lists stay co-located with the run engine; only cross-cutting resolution rules go to a reference file.

### Unresolved Contradictions

1. **Run engine placement: SKILL.md core vs. references/handler-run.md.** agentskills-specialist and functional-decomposition hold the engine in root SKILL.md (producing 500-700 lines, 6,000-8,000 tokens); integration-specialist proposes extraction to a reference file (producing 300-350 line root). See Disputes section.

2. **Multi-round extraction feasibility.** No dependency analysis has been performed. functional-decomposition requires one before deciding. integration-specialist and agentskills-specialist oppose extraction on principle. See Disputes section.

---

## Systemic Contradictions

1. **Token target compliance vs. execution safety.** Every agent invoking the run engine needs the full engine specification. The agentskills recommendation of 500 lines / 5,000 tokens cannot be met while keeping the engine in the always-loaded body. The deliberation exposed a structural tension between the agentskills spec's sizing guidance (designed for typical skills) and conversus's nature as an orchestration engine. All agents ultimately acknowledged this as an acceptable exception, but the two camps diverge on where to pay the cost: in the root SKILL.md (larger root, simpler loading) or in a mandatory reference file (smaller root, two-hop chain).

2. **Progressive disclosure depth vs. execution fidelity.** The agentskills specification recommends one-level-deep references. The converge and gate handlers both delegate to the run engine. If the engine is a reference file, converge requires dispatch -> handler-converge -> handler-run (two levels). This pattern will recur any time a wrapper subcommand delegates to core execution logic. The deliberation revealed no clean resolution -- only trade-offs between loading depth and root file size.

3. **Conditional loading reliability as an empirical unknown.** Every agent's decomposition depends on agents reliably following conditional load triggers in SKILL.md. No agent provided empirical evidence that this works reliably. The entire architecture rests on an untested assumption. functional-decomposition's staged validation (New Rec B) was the closest to addressing this, proposing empirical gates before committing to full decomposition.

4. **Dual-audience content (contribution vs. execution) lacks a synchronization mechanism.** The deliberation established that AGENTS.md uses pointers rather than duplicating runtime rules. But no automated mechanism ensures the pointers remain valid beyond the proposed (but not yet implemented) linter expansion. The pointer convention is a policy, not a technical enforcement.

5. **Active spec development creates restructuring drag.** Conversus has specs 012-020 queued. Any decomposition today may need adjustment as new subcommands, modes, or subsystems are added. The staged decomposition (gate first, then guided handlers, then subsystems) mitigates but does not eliminate this risk. This is a timing tension between "the monolith hurts now" and "structural commitments are expensive to change during rapid evolution."

---

## Convergence Achieved

1. **The agentskills `references/` model is the correct primary decomposition mechanism.** (Unanimous, all 5 agents.) APM sub-skills are withdrawn. AGENTS.md is contribution guidance only. The references/ directory with conditional load triggers is the architecture. apm-specialist's full reversal in Phase 3 sealed this.

2. **The gate handler is the first extraction target.** (Unanimous, all 5 agents.) Zero dissent across all phases. 300 lines, zero shared state, self-contained config/output schema, distinct audience (CI/CD). Extraction to `references/handler-gate.md` proceeds first and serves as the empirical validation test for the reference-loading mechanism.

3. **SKILL.md and AGENTS.md serve fundamentally different purposes; execution logic never moves to AGENTS.md; AGENTS.md uses pointers, not rule restatement.** (Unanimous, all 5 agents.) The single-source-of-truth pointer convention eliminates the dual-ownership problem that dominated cross-review. Reference files own runtime contracts. AGENTS.md files point to them.

4. **Full APM distribution deferred until spec suite stabilizes and a second consumer appears.** (Unanimous, all 5 agents.) The strongest consensus point. APM structural preparation (manifest, type declaration) is maintained; active packaging is premature.

5. **Staged decomposition with empirical validation gates.** (Unanimous, all 5 agents.) Extract gate first, validate loading works, then remaining handlers, then conditional subsystems. No all-or-nothing structural replacement.

6. **The run engine's internal state machine (round/iteration loop, output paths, termination) must not be split across files.** (Unanimous, all 5 agents.) The "do not decompose" constraint applies to the round/iteration state machine wherever it lives. Single-round and multi-round paths are not separately extractable because single-round semantics are defined as the negation of multi-round behavior.

7. **Two-class load trigger model (Class A dispatch vs. Class B config-conditional).** (Majority, 4 of 5 agents.) Class A triggers fire at invocation time from the dispatch table. Class B triggers fire mid-execution based on config inspection and require explicit fallback behavior. Originated by functional-decomposition, adopted by integration-specialist, agentskills-specialist, and apm-specialist.

8. **The dispatch table is the correct anchor for root SKILL.md.** (Unanimous, all 5 agents.) No agent proposed extracting or modifying the dispatch table.

<!-- CONVERSUS:DISPUTES_BEGIN -->
## Remaining Disputes

### Dispute A: Run Engine Placement — Root SKILL.md vs. references/handler-run.md

**Positions:**
- **Engine in SKILL.md** (agentskills-specialist, functional-decomposition): The run engine core stays in the always-loaded SKILL.md, producing a root of ~500-700 lines (6,000-8,000 tokens). This eliminates two-hop reference chains for converge and gate. The 5,000-token guideline is acknowledged as an acceptable exception for an orchestration engine.
- **Engine in references/handler-run.md** (integration-specialist): The engine moves to a reference file (~450-550 lines), keeping the root at ~300-350 lines (under 5,000 tokens). Internal cohesion is preserved within the reference file. A mandatory Class A-style load trigger in handler-converge.md and handler-gate.md instructs the agent to load the engine before proceeding.
- **Conditional on empirical validation** (apm-specialist): Accepts either outcome based on the results of the staged validation gates. If two-hop loading works reliably in practice, the reference file is correct. If it fails, root retention is correct.

**Arguments:**
- agentskills-specialist: The agentskills specification states "keep file references one level deep from SKILL.md." Converge routing to handler-converge.md which then loads handler-run.md is a two-hop chain. The failure mode (agent executes multi-phase orchestration with only a summary) is silent and severe.
- integration-specialist: A `/conversus define` invocation should not pay 6,000 tokens for run engine internals. Co-location within a reference file is as safe as co-location in root. The load trigger in handler-converge.md is explicit and mandatory, not conditional.
- functional-decomposition: The resolution is empirical, not architectural. Phase 1 validation (gate extraction) should test whether two-hop loading works. Agrees with root retention as the default until evidence supports extraction.

**Synthesizer assessment:** Both positions have legitimate structural arguments. The root-retention camp correctly identifies that the two-hop chain violates the agentskills one-level-deep principle and that the failure mode is silent. The extraction camp correctly identifies that non-engine subcommands pay an unnecessary 6,000-token context cost. The dispute is genuinely empirical: it depends on whether agent runtimes reliably follow mandatory load triggers across reference files. Neither camp has evidence. functional-decomposition's staged validation is the correct resolution mechanism.

**Recommended resolution:** Accept **root SKILL.md retention as the initial implementation** (agentskills-specialist/functional-decomposition position), with a documented exception to the 500-line guideline. After Phase 1 (gate extraction) and Phase 2 (guided handler extraction) succeed, execute a controlled test: run `/conversus converge` with the engine in a reference file and compare output fidelity against the root-retained configuration. If the test passes, migrate the engine to the reference file. If it fails, the root retention is confirmed. The staged validation gates make this a zero-risk resolution path.

---

### Dispute B: Multi-Round Extraction — Conditional Reference vs. Inline Retention

**Positions:**
- **No extraction** (integration-specialist, agentskills-specialist): The round/iteration state machine is a cohesive unit where single-round behavior is defined as the negation of multi-round behavior. Splitting them requires one to restate what it is opting out of, creating two sources of truth.
- **Conditional on dependency analysis** (functional-decomposition): Before deciding, perform an explicit dependency analysis of SKILL.md lines 248-610. If the shared interface between single-round and multi-round paths is fewer than 20 lines, extract with controlled duplication. If it exceeds 20 lines, retain inline.
- **Extract with conditional loading** (agentskills-specialist's directory layout includes `references/multi-round-execution.md`, though the revision kept the engine in SKILL.md): Lists the file in the proposed layout, loaded when `rounds > 1`.

**Arguments:**
- integration-specialist: Single-round path is "the multi-round loop with rounds = 1." Splitting at the `if rounds > 1:` boundary orphans negative-case definitions. No dependency analysis has been done.
- agentskills-specialist: Single-round runs (the default) should not load 360 lines of multi-round logic. But if the engine stays in SKILL.md, the multi-round block stays with it.
- functional-decomposition: The 20-line threshold is a practical heuristic. The analysis has not been performed. This is an empirical question.

**Synthesizer assessment:** integration-specialist's negation-definition argument is the strongest single argument in the entire deliberation. The single-round path's termination conditions, directory structure, and output paths are all defined relative to multi-round behavior. A clean split requires the single-round specification to either duplicate multi-round definitions or reference them across a file boundary inside the run engine itself. No agent performed the dependency analysis that would resolve this.

**Recommended resolution:** **Retain multi-round orchestration inline with the run engine, wherever the engine lives.** The "do not decompose" constraint applies. The 360-line cost is real but the coupling is too tight for clean extraction without duplication. This aligns with the unanimous convergence point that the round/iteration state machine must not be split across files. If the dependency analysis is performed later and reveals a clean boundary (fewer than 20 shared lines), this decision can be revisited.

---

### Dispute C: Naming Convention — Two-Tier vs. Three-Tier vs. Flat

**Positions:**
- **Two-tier** (`handler-`, `subsystem-`): integration-specialist, functional-decomposition (New Rec C), apm-specialist.
- **Three-tier** (`handler-`, `subsystem-`, `notes-`): agentskills-specialist's final flexibility position accepts this.
- **Flat (handler- only, plain names for rest)**: functional-decomposition's proposed compromise.

**Arguments:**
- integration-specialist: At 9-11 files, type prefixes make the directory listing self-documenting.
- agentskills-specialist: The agentskills specification defines no file-type taxonomy. Classification overhead may not scale. Accepts three-tier as a compromise.
- functional-decomposition: `handler-` prefix is the most important distinction (dispatch targets vs. everything else).

**Synthesizer assessment:** This is a low-stakes convention decision. The `handler-` prefix is universally agreed. The dispute is about whether non-handler files also get type prefixes. At 9-11 files, the navigability benefit of `subsystem-` is modest but real. The three-tier approach (`handler-`, `subsystem-`, `notes-`) closes the ungrouped-file gap agentskills-specialist identified.

**Recommended resolution:** Adopt **three-tier naming** (`handler-`, `subsystem-`, `notes-`). The convention costs nothing, provides navigability at the current file count, and has been accepted (at least as flexibility) by all agents. Decide before Phase 1 extraction to avoid retroactive renames.

---

### Dispute D: Validation Rules — Shared Reference File vs. Co-Location in Handlers

**Positions:**
- **Shared reference file** (`references/validation-rules.md` for patterns in 3+ handlers): agentskills-specialist.
- **Co-location in each handler** with a canonical pattern section in SKILL.md core: functional-decomposition.

**Arguments:**
- agentskills-specialist: Centralization avoids validation drift. If agent name regex changes, update one file, not six.
- functional-decomposition: Co-location keeps handlers self-contained (one file per invocation). The 3+ threshold creates classification overhead. Defer decision until handler files are drafted and actual shared patterns counted.

**Synthesizer assessment:** This is a legitimate design trade-off between DRY centralization and handler self-containment. The answer depends on the actual count of shared validation patterns across the six handler drafts. functional-decomposition's proposal to defer until the count is empirically known is reasonable.

**Recommended resolution:** **Defer until handler reference files are drafted (Phase 2 of staged decomposition).** Count shared validation patterns. If 4+ patterns appear verbatim in 3+ handlers, create `references/validation-rules.md`. If fewer, co-locate in each handler with a brief canonical definition in the SKILL.md core. This is an empirical question that should not be decided before the data exists.

<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

### P1 — Must Implement

**P1.1: Extract gate handler to `references/handler-gate.md`.**
Traces to: F1, I3, all agents unanimously.
Move SKILL.md lines ~1881-2178 (~300 lines) to `references/handler-gate.md`. Replace in SKILL.md dispatch table with: "When `/conversus gate` is invoked, read `references/handler-gate.md` and follow the instructions there." The gate handler includes its own output schema (`gate-result.md`), configuration schema (`gates.yml`), exit code contract, and re-run behavior. This is the first structural change and the empirical validation test for the reference-loading mechanism.

**P1.2: Extract guided handlers (define, interests, mode, converge, arbitrate) to `references/handler-{name}.md`.**
Traces to: F2, I2, S1.
Extract each to its own reference file: `handler-define.md` (~150 lines), `handler-interests.md` (~200 lines), `handler-mode.md` (~180 lines), `handler-converge.md` (~210 lines), `handler-arbitrate.md` (~160 lines). Each handler file includes its own output schema co-located (problem.md schema in handler-define, interests.md schema in handler-interests). handler-converge.md must include an explicit cross-reference to the run engine's Step 5 report format for drift prevention. Dispatch table entries become Class A load triggers.

**P1.3: Staged execution with empirical validation gates.**
Traces to: FB, all agents.
Execute decomposition in three phases: (1) Extract gate handler + one guided handler (define). Validate that the agent correctly loads reference files and produces correct output. (2) If Phase 1 succeeds, extract remaining guided handlers. (3) If Phase 2 succeeds, extract conditional subsystems (preset resolution, dispute-parsing if deferred). Each phase is gated on the previous phase's success.

**P1.4: Fix root AGENTS.md staleness.**
Traces to: M5, agents-md-specialist, integration-specialist.
Remove `tasks/` from the structure section. Add `schema/`, `linter/`, `presets/`, `antipatterns/`. Add the linter as a pre-contribution check. Add one line noting that subdirectories with their own AGENTS.md have directory-specific guidance. Total addition: ~15 lines, keeping the file under 70 lines. This is a 15-minute maintenance task that should proceed immediately, independent of all other work.

**P1.5: Create `linter/AGENTS.md`.**
Traces to: M4, unanimous.
Content: Python version requirement, environment setup (`uv sync`), linter command (`uv run python linter/validate.py`), test command (`uv run pytest linter/`), what the linter checks, how to interpret failures. Estimated scope: 30-45 lines. This is the canonical example of contribution guidance with zero dual-ownership risk.

**P1.6: Establish the two-class load trigger model.**
Traces to: F8, IN2, S9.
All handler reference files use Class A triggers (fired from the dispatch table at invocation time). All subsystem reference files use Class B triggers (fired mid-execution based on config inspection, with explicit fallback: "If this file cannot be loaded, halt and report the error"). Document both classes in the root SKILL.md.

### P2 — Should Implement

**P2.1: Extract preset resolution to `references/subsystem-preset-resolution.md`.**
Traces to: F5, I5, S7, A4 (revised).
Move preset resolution algorithm (~75 lines including single-preset resolution, composition templates, inline overrides, caching) to a reference file. Class B trigger: "If any agent entry (or arbiter entry) has a `preset` field, read `references/subsystem-preset-resolution.md` and apply its resolution rules before validation." Include explicit fallback.

**P2.2: Extract Dispute-Parsing Subsystem to `references/subsystem-dispute-parsing.md`.**
Traces to: F3 (modified), I4, S3, A4 (revised).
Move the subsystem's ~28 lines to a reference file. This extraction should occur after handler extractions are validated (Phase 2 or Phase 3 of staged decomposition). The load trigger lives in whatever file contains the run engine (SKILL.md or handler-run.md, depending on Dispute A resolution). If handler extractions reveal that agents struggle with reference loading, keep dispute-parsing inline as a 28-line always-loaded gotcha.

**P2.3: Adopt three-tier naming convention for reference files.**
Traces to: FC, I9, agentskills-specialist flexibility.
Convention: `handler-{name}.md` for subcommand handlers, `subsystem-{name}.md` for shared subsystems (dispute-parsing, preset-resolution), `notes-{name}.md` for informational reference material (operational-notes). Decide before Phase 1 extraction to avoid retroactive renames.

**P2.4: Per-item classification of "Important Notes" section.**
Traces to: F10, S8.
Retain in SKILL.md: overwrite semantics, model selection, rounds/iterations orthogonality, background dispatch semantics, agent count formulas (`N^2 + 2N + 1`, `N^2 + 2N + 2`). Move to `references/notes-operational.md`: worked formula examples, baseline feature inventory, detailed orthogonality explanation.

**P2.5: Phased linter expansion.**
Traces to: I8, SB.
Phase 1 (now): validate that template variables in handler reference files match `schema/variables.yml`. Phase 2 (after reference files stabilize): validate that reference file headers match dispatch table entries and that AGENTS.md file references point to existing files. Phase 3 (aspirational): error message catalogue consistency.

**P2.6: Single-source-of-truth pointer convention for AGENTS.md.**
Traces to: MA, IN3, M6.
Convention: AGENTS.md files use "See [file] for authoritative rules" pointers, never inline rule restatement, for any content also enforced at runtime. Format: "Preset naming rules are enforced at runtime. See `references/subsystem-preset-resolution.md` for the authoritative contract. Run `uv run python linter/validate.py` to check compliance before committing."

**P2.7: Antipattern check as orchestrator-level pre-dispatch step.**
Traces to: IN4, SD.
The antipattern check remains in the root SKILL.md, executed before the dispatch table routes to a handler. This ensures all subcommands inherit the check, including guided handlers. AGENTS.md may also mention it as a contribution guideline.

### P3 — Consider

**P3.1: Document per-invocation token budget.**
Traces to: F9, SC.
Document the budget once at decomposition time as a table in SKILL.md. Include an explicit exception for the run engine path. Specify the update trigger as "when a reference file is created, significantly expanded, or removed." Example: `/conversus define` loads core (~5-8k) + handler-define (~2k). `/conversus run` (single-round, no presets) loads core + engine + dispute-parsing + validation.

**P3.2: Create nested pointer AGENTS.md files for templates/, presets/, schema/.**
Traces to: M1, M2, M3 (all revised).
15-30 lines each. Pointer to authoritative reference file, linter command for compliance, brief structural orientation ("what to expect in this directory"). Create after reference file extraction is complete so pointers target stable locations.

**P3.3: Consider gate as APM sub-skill candidate after reference structure stabilizes.**
Traces to: AN1, A8.
Gate is the only subcommand that passes both sub-skill criteria: (1) serves a categorically different audience (CI/CD), (2) can be activated independently. Defer promotion until reference file structure has proven stable across two spec iterations and a second consumer with independent activation needs appears.

**P3.4: Resolve run engine placement via empirical testing.**
Traces to: Dispute A.
After Phase 2 of staged decomposition succeeds, test two configurations side-by-side: (a) engine in SKILL.md with guided handlers in references, (b) engine in `references/handler-run.md` with phase summary in SKILL.md. Execute `/conversus converge` in both and compare output fidelity. The configuration where converge reliably produces correct multi-phase output is correct.

**P3.5: Multi-round extraction dependency analysis.**
Traces to: Dispute B, F4.
If a future spec needs the run engine to shrink further, perform the dependency analysis of SKILL.md lines 248-610 to determine the shared interface between single-round and multi-round paths. If fewer than 20 lines, extraction with controlled duplication is viable. If more, retain inline permanently.

---

## Key Concessions

**apm-specialist:** Made the largest concession of any agent. Withdrew sub-skills as primary decomposition strategy (Rec 1), mode specs as context files (Rec 2), presets as sub-skill (Rec 3), dispute-parsing as context primitive (Rec 4), antipattern catalog as context primitive (Rec 5), PostToolUse hook (Rec 6), schema as context primitive (Rec 7). Retained only the deferral of full distribution (Rec 8) and structural preparation positioning (N3). Conceded that APM solves distribution problems while conversus has a context window problem.

**integration-specialist:** Conceded the run engine's placement -- originally argued it must stay in root SKILL.md, then reversed to allow extraction to `references/handler-run.md`. Also withdrew the centralized dependency map (Rec 10) and accepted that template variable documentation should stay co-located with the engine rather than in a standalone contract file.

**agentskills-specialist:** Reversed on run engine extraction -- originally proposed extracting it, then in revision kept it in SKILL.md after three agents demonstrated the two-hop chain problem. Conceded that the 5,000-token guideline is not achievable for conversus. Withdrew the assets/ directory proposal. Accepted that agent count formulas are authoritative contracts, not derivable arithmetic.

**agents-md-specialist:** Narrowed nested AGENTS.md scope from 40-60 line inline rule documents to 15-30 line pointer files. Accepted that preset validation, template naming, and structural markers are runtime contracts, not contribution guidelines. Withdrew the file-relationship section for the root AGENTS.md. Accepted that AGENTS.md is not a SKILL.md size-reduction strategy.

**functional-decomposition:** Downgraded Dispute-Parsing extraction from P1 to P2 conditional. Modified the multi-round extraction from unconditional to contingent on dependency analysis. Accepted that the run engine core may be larger than originally estimated. Added the staged decomposition recommendation after cross-review pressure.
