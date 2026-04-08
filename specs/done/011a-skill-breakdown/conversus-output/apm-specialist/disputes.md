# APM Specialist — Disputes (Phase 4)

## Remaining Disputes

### Dispute 1: Run Engine Placement — Reference File vs. Root SKILL.md

**The unresolved split:** integration-specialist and agentskills-specialist landed in opposite final positions on where the run engine core lives, and neither position is fully stable after their revisions.

agentskills-specialist revised to keep the run engine in root SKILL.md (~500 lines, 6,000-8,000 tokens), citing the two-hop reference chain problem: `/conversus converge` would require SKILL.md → `handler-converge.md` → `handler-run.md`. functional-decomposition accepted this and also revised to keep the run engine in root. integration-specialist, however, moved in the opposite direction — revised to extract the run engine to `references/handler-run.md` (~450-550 lines) and keep root SKILL.md at ~300-350 lines. integration-specialist's explicit argument: "the solution is to keep those tightly coupled elements together in `references/handler-run.md`, not to keep them in the root SKILL.md." Three reviewers moved one direction; one moved the other.

**My position:** The two-hop chain argument is correct in principle but overstated in practice for the converge case. Converge's delegation to the run engine is explicitly documented in the handler reference file — any agent reading `references/handler-converge.md` is already being instructed to run the engine. The agent is not left to infer the dependency; the load trigger is explicit. This is materially different from an undocumented implicit dependency.

The more important factor is what integration-specialist correctly identifies: a root SKILL.md at 6,000-8,000 tokens imposes that cost on every single conversus activation, including the lightweight guided handlers (define, interests, mode) that have no relationship to the run engine whatsoever. An agent invoking `/conversus define` pays 6,000 tokens to read the full round-iteration state machine it will never execute. This is the context pollution problem the decomposition is meant to solve, applied to the root file itself.

**Remaining dispute:** agentskills-specialist and functional-decomposition's position creates a 500-line root that is 60% over the agentskills recommendation and grows if multi-round extraction fails. integration-specialist's position creates a two-hop chain for converge. Neither camp has shown empirically that their failure mode (performance degradation vs. context bloat) is less costly in practice.

**What I need resolved:** Does the two-hop chain for converge actually cause observable failures in agent execution, or is it a theoretical concern? If empirical testing shows agents follow two-hop loads reliably, integration-specialist's architecture is correct. If it shows failures, agentskills-specialist's architecture is correct. This dispute cannot be resolved by argument alone — it requires functional-decomposition's staged validation (New Rec B) to produce actual evidence.

---

### Dispute 2: Dispute-Parsing Subsystem — Always-Loaded vs. Reference File

**The unresolved split:** functional-decomposition revised to downgrade the dispute-parsing extraction to P2 and make it conditional on empirical validation of handler extractions. Integration-specialist sustained extraction to `references/subsystem-dispute-parsing.md`. agentskills-specialist maintained extraction to `references/dispute-parsing.md`. I revised to extract to `references/dispute-parsing.md`.

functional-decomposition's argument for deferral: the subsystem is only 28 lines (~400 tokens), it is relevant to the majority of invocation paths (run, converge, gate, Phase 6), and the load trigger must be embedded in the always-loaded SKILL.md body anyway — "partially defeating the extraction." Additionally, functional-decomposition identified an internal inconsistency: I cannot simultaneously argue that cross-cutting invariants with breaking-change implications should always be in context (their Rec 10) and that dispute-parsing — whose structural markers are a stable interface where changes are breaking changes — should be extracted.

**My position after reviewing all revisions:** The internal inconsistency functional-decomposition identified is real, but the conclusion does not fully follow. The claim that "cross-cutting invariants should always be in context" applies to gotchas about overwrite semantics, model selection, and round/iteration orthogonality — behavioral surprises that are relevant on every invocation regardless of path. Dispute-parsing is different: it is only invoked when synthesis outputs exist, which means it is only invoked during Phase 6 of a run or converge operation. An agent invoking `/conversus gate` loads dispute-parsing to detect gates consensus — that is a genuine use case. An agent invoking `/conversus define` has no synthesis outputs to parse.

The 400-token savings figure is correct but understates the cumulative effect: with 3-5 consumers, each invocation of the dispute-parsing subsystem means the agent has already loaded it as always-present context, removing the opportunity for any future conditional optimization. If the always-loaded core grows over time (as it will during specs 012-020), each always-loaded element becomes harder to remove.

**Remaining dispute:** I maintain extraction is correct, but I accept functional-decomposition's sequencing argument. Extract dispute-parsing after handler extractions are validated, not before. The order resolves the empirical dependency: if conditional load triggers fail in practice, keep dispute-parsing inline. If they succeed, dispute-parsing is a natural second extraction that proves the pattern scales to subsystems.

**What I need resolved:** Are the 28 lines of dispute-parsing content genuinely boundary-stable enough to warrant a standalone reference interface today, given that specs 012-020 may add new dispute markers or parsing rules? If the interface is expected to evolve, extraction creates a reference file that needs to be updated alongside SKILL.md content — the synchronization cost may exceed the token savings until the interface stabilizes.

---

### Dispute 3: Multi-Round Extraction — Dependency Analysis Prerequisite

**The unresolved split:** functional-decomposition revised from proposing unconditional extraction to proposing extraction contingent on an explicit dependency analysis — if shared interface exceeds 20 lines, keep multi-round inline. Integration-specialist maintained opposition to splitting multi-round from single-round on grounds that "the single-round path is defined as the negation of multi-round behavior." agentskills-specialist revised to propose extracting `references/multi-round-execution.md` loaded conditionally when `rounds > 1`.

**My position:** Integration-specialist's negation argument is the strongest case made by any reviewer on any topic in this deliberation. The single-round path is not a standalone positive specification — it is what happens when the multi-round conditions do not apply. Separating the positive conditions (multi-round execution) from the negative baseline (single-round defaults) produces a specification where the single-round path must be understood by reference to what is absent. This is a silent failure mode: the agent must read the reference file to know what it is opting out of.

From an APM perspective, this is the structurally distinct case. Sub-skill promotion would not help here — the multi-round and single-round paths are not audience-separated in the way gate and interactive handlers are. They are execution-path-separated, which is the domain agentskills handles. And agentskills' conditional loading model works well when the loaded content is additive. It fails when the unloaded content defines the baseline for the loaded content's negation.

**Remaining dispute:** The 360-line size of the multi-round block is real, and keeping it inline pushes the run engine core (whether in root or in `handler-run.md`) toward 700 lines. Functional-decomposition's 20-line interface threshold is the right framing, but the analysis has not been done. I do not dispute the threshold — I dispute whether anyone in this deliberation has done the work to know which side of it the actual interface falls on.

**What I need resolved:** The dependency analysis. Until someone reads lines 248-610 of SKILL.md and traces exactly which elements the single-round path references from the multi-round block (including negative-case definitions), this dispute is theoretical on both sides.

---

### Dispute 4: APM Sub-skill Gate Promotion — Timing and Criteria

**The unresolved split:** I proposed gate as the sole candidate for eventual APM sub-skill promotion, deferred until after reference-file restructuring proves stable. The other four reviewers did not directly contest this, but integration-specialist's revised architecture places gate in `references/handler-gate.md` within the main conversus skill, not in `.apm/skills/conversus-gate/`. The implicit assumption in integration-specialist's final architecture is that gate stays as a reference file, not a sub-skill.

**My position:** This is not a contradiction — reference file first, sub-skill promotion second, is the sequencing I proposed. What I want to surface as a remaining dispute is the criteria question: what evidence would trigger sub-skill promotion after the reference-file structure is stable?

I proposed two criteria: (1) a second consumer appears that needs gate but not the deliberation engine, and (2) the reference-file structure has proven stable across two spec iterations. But no other reviewer engaged with the criteria question. This matters for APM because sub-skill promotion is a structural commitment — once conversus-gate is distributed as an independent skill, downstream consumers have a dependency on its SKILL.md format and interface. Changes to `references/handler-gate.md` can happen freely during active development; changes to a promoted `.apm/skills/conversus-gate/SKILL.md` require version bumps and dependency coordination.

**Remaining dispute:** Is the "second consumer" criterion the right trigger, or should gate be promoted based on stability alone? A CI/CD author who wants only the gate specification has a legitimate use case today — they exist as soon as the spec is published. The question is whether APM's distribution overhead (version management, multi-target deployment) is justified by one additional consumer with a narrower use case.

My view: the stability criterion should take precedence over the audience criterion. A stable, well-bounded reference file that serves both audiences (via the parent skill) is better than a premature sub-skill split that locks in an interface before the spec suite has stabilized. The audience criterion matters only when the audience cannot access the parent skill — which is not currently the case for any conversus consumer.

---

## Convergence

### Convergence 1: The `references/` Model Is the Primary Decomposition Mechanism

All five reviewers converge on this. Sub-skills solve distribution problems. Reference files solve invocation-time context problems. Conversus has a context window problem, not a distribution problem. The `references/` architecture using conditional load triggers is the correct primary decomposition mechanism for conversus at this stage. APM's role is structural preparation, not active packaging. This is no longer disputed.

The specific architecture: dispatch table routes to handler reference files (Class A triggers, pre-invocation); handler reference files conditionally load subsystem reference files (Class B triggers, config-conditional). The root SKILL.md contains the always-loaded core — the exact size of that core is still disputed (see Dispute 1), but the structure is not.

### Convergence 2: Gate Handler Is the Highest-Priority Extraction Target

Universal agreement, zero dissent. Gate's 300 lines, zero shared state, clean boundary, and independent audience make it the clearest extraction candidate. It should be extracted first, serving as both a meaningful improvement and an empirical test of the reference-loading mechanism. This also serves as the APM sub-skill promotion candidate if and when the criteria are met (Dispute 4).

### Convergence 3: Full APM Distribution Deferred Until Spec Suite Stabilizes

Universal agreement sustained from the original round. Conversus is in active development (specs 012-020 queued). Distribution overhead — version management, multi-target deployment testing, downstream dependency coordination — is not justified until a second consumer appears or the spec suite stabilizes. APM structural preparation (manifest, type declaration, target setting) is correct to maintain as optionality, but active packaging is premature.

### Convergence 4: Staged Decomposition with Empirical Validation Gates

functional-decomposition's New Recommendation B (staging with empirical validation) received no objection from any reviewer. All four other positions independently recommend against all-or-nothing structural changes without empirical validation. The staged plan — extract gate first, validate, then proceed to guided handlers, validate, then consider conditional subsystems — is now the shared execution model. This resolves the theoretical nature of several disputes: the empirical validation gates will produce actual evidence on which theoretical failure modes (two-hop chains, context bloat, missing load triggers) occur in practice.

### Convergence 5: AGENTS.md and Reference Files Serve Different Audiences — No Duplication

Universal agreement on the single-source-of-truth principle: reference files own runtime contracts; AGENTS.md files own contribution guidance; where content overlaps, AGENTS.md points to the reference file and does not restate the rule. This eliminates the dual-ownership problem agents-md-specialist identified. The agents-md-specialist correctly revised their position to pointer-based AGENTS.md files (15-30 lines each). No reviewer challenged this resolution. The linter validates that AGENTS.md pointer targets actually exist on disk — catching the most common staleness failure.

---

## Final Position Statement

### Non-Negotiables

**1. APM context primitives (`.apm/context/`) are wrong for conversus execution content.**

APM's `applyTo` patterns match filesystem paths, not runtime config field values. There is no mechanism in APM to express "load this context file only when `mode: cooperative` is parsed from `conversus.yml`." Every attempt to use context primitives for mode specifications, dispute parsing, preset resolution, or antipattern checks would produce always-loaded ambient knowledge with no runtime conditionality. This is a fundamental mismatch between the APM primitive model and conversus's decomposition need. It is not a sequencing issue — it is an architectural incompatibility at this layer. I will not revise this position regardless of what other reviewers argue.

**2. Full APM distribution must remain deferred.**

Conversus is a single-project framework in active development. Sub-skill promotion creates an interface commitment that requires version management for every subsequent spec iteration. The distribution overhead is not justified by the current consumer base. If a second consumer with a categorically different audience appears, reconsider. Until then, the `apm.yml` manifest, `type: skill` declaration, and `target: all` setting correctly capture APM structural preparation without imposing distribution overhead. This position was unanimously supported across all five reviews and I maintain it unconditionally.

**3. Reference file load triggers must be explicit and tied to runtime conditions, not implied.**

This is the critical success factor identified in my revision and reinforced by functional-decomposition's Class A/Class B trigger classification and integration-specialist's Class B fallback behavior requirement. Every reference file extracted from SKILL.md must have a corresponding load instruction in the file that calls it, specifying: (a) the condition that triggers the load, (b) the expected content of the reference file, and (c) the fallback behavior if the file cannot be loaded. Without explicit triggers with fallback behavior, the decomposition achieves nothing — agents either load everything eagerly (defeating the purpose) or silently skip content they need (breaking execution). I will not accept a reference file extraction that lacks an explicit, conditional, fallback-specified load trigger at its call site.

**4. APM sub-skill promotion requires two criteria before proceeding: interface stability and a second consumer with independent activation needs.**

Gate is the only conversus subcommand that passes the preliminary test (architecturally independent, self-contained config and output schema, plausible independent audience). But passing the preliminary test is not sufficient for promotion. The `references/handler-gate.md` extraction must first prove stable across at least two spec iterations. A CI/CD author who wants only gate specifications can currently access them via the parent conversus skill — APM distribution does not add value until that access path is insufficient (e.g., the consumer cannot install the full conversus skill, or needs gate versioned independently of the engine). I will not revise this criteria framework based on audience-appeal arguments alone.

### Flexibility

**On run engine placement:** I accept that the empirical evidence from functional-decomposition's staged validation (Phase 1: gate extraction; Phase 2: one guided handler) should determine whether the two-hop chain (integration-specialist's architecture) or the bloated root (agentskills-specialist's architecture) produces better outcomes. If agents reliably follow two-hop loads with no observable failure, integration-specialist's ~300-line root architecture is correct and I support it. If two-hop loads produce missed content or silent failures, agentskills-specialist's ~500-line root architecture is the correct fallback. I do not have strong convictions on which failure mode is more common in practice — this is an empirical question.

**On dispute-parsing extraction timing:** I accept functional-decomposition's sequencing argument. Extract dispute-parsing after handler extractions are validated. The 28-line size and majority-path relevance make deferral reasonable during the first extraction phase. If the staged validation confirms that conditional load triggers work reliably, dispute-parsing becomes a natural second-phase extraction. If it reveals that agents struggle with reference loading, dispute-parsing should remain inline as a 28-line always-loaded gotcha. My revision recommended extraction; I now agree the timing should be contingent on Phase 1 and Phase 2 empirical results.

**On multi-round extraction boundary:** I accept that the dependency analysis is a prerequisite before any position on extraction is defensible. Functional-decomposition's 20-line threshold is a reasonable criterion. If the analysis shows fewer than 20 lines of shared interface between the single-round and multi-round paths, extraction with controlled duplication is viable. If it shows more than 20 lines — particularly if the single-round path is substantially defined by what the multi-round path omits — integration-specialist's position (keep together, document as acknowledged exception to the 500-line guideline) is correct. I do not dispute the criterion; I am waiting for the analysis.

**On naming conventions:** integration-specialist's two-tier naming (`handler-`, `subsystem-`) is a reasonable convention I adopt without reservation. The `contract-` prefix I originally supported was withdrawn by integration-specialist after the template variable contract file was eliminated. The two-tier model produces a legible directory from `ls` alone, which is the practical standard for self-documenting structure.

**On the linter's expanded scope:** Integration-specialist's phased linter expansion is the right approach. Phase 1 (variable references in handler files match `schema/variables.yml`) is mechanical and achievable immediately. Phase 2 (reference file headers match dispatch table entries) is achievable after the first extraction. Phase 3 (error message catalogue consistency) is aspirational. I support phased expansion over apm-specialist's originally proposed PostToolUse hook — the hook fires at the wrong time, covers only Claude Code users, and removes agent-visible reasoning about validation. The explicit linter instruction in SKILL.md is more robust than hook automation for this case.
