# Integration Specialist — Phase 4 Disputes

## Remaining Disputes

### Dispute 1: Run Engine Placement — Reference File vs. Root SKILL.md

**The unresolved split:** My revised position concedes that the run engine can move to `references/handler-run.md` as a cohesive unit. agentskills-specialist's revised position holds it in root SKILL.md. functional-decomposition's revised position leaves it conditional on a dependency analysis of the multi-round/single-round boundary.

These three positions are not reconciled. My revision represents the largest concession of any reviewer in this process: I originally argued the run engine must stay in root and fully retracted that to allow `references/handler-run.md`. agentskills-specialist went the opposite direction — originally proposing extraction, then revising to retention. We are now inverted from our original positions.

**What I concede fully:** The run engine's internal state machine (round/iteration counters, output path formulas, termination conditions, retroactive directory moves) must remain a single cohesive unit regardless of where it lives. This is the "do not decompose" constraint I introduced and all reviewers accepted. The location is the dispute.

**What I do not concede:** agentskills-specialist's revised retention argument rests on the claim that converge and gate "compose" the run engine rather than "call" it, making two-hop reference loading unavoidable. This framing is empirically false at the interface level. `converge` delegates to the run engine by invoking it — the agent reads handler-converge.md, reaches the delegation point, and at that point loads handler-run.md. This is one additional file read, not a structural two-hop dependency chain. The agent does not have to load handler-run.md before knowing what converge does; it loads it when converge instructs it to. The delegation point is explicit and the loading is sequential, not nested discovery.

**The residual disagreement:** If the agent fails to follow the delegation trigger in handler-converge.md and attempts to execute a multi-phase deliberation with only the converge handler's summary, the failure mode is severe. agentskills-specialist correctly identifies this as a "high-fragility silent failure mode." I accept the failure mode exists. My position is that the failure mode is an argument for explicit, mandatory load triggers — not for keeping the engine in root. The trigger in handler-converge.md should be unambiguous: "The following execution delegates to the run engine. You must read `references/handler-run.md` before proceeding. Do not attempt to proceed without it." A mandatory-framed Class A trigger is qualitatively different from an optional or conditional one.

**What the three camps need to decide:** Is the risk of a missed mandatory load trigger in handler-converge.md acceptable in exchange for a root SKILL.md at ~300-350 lines, or does the severity of the failure mode justify keeping the engine in root at ~500-550 lines? This is an empirical question about agent reliability that none of us has data to answer definitively. I maintain the reference file is correct; I accept the other position is reasonable.

---

### Dispute 2: Dispute-Parsing Subsystem — Inline vs. Extracted

**The unresolved split:** functional-decomposition's revised position downgrades dispute-parsing extraction to P2 conditional on handler extraction succeeding first, and explicitly acknowledges functional-decomposition's own Dangerous Contradiction: the original review simultaneously argued for always-keeping breaking-change content in context (Recommendation 10) and for extracting dispute-parsing (Recommendation 3). My sustained position: extract to `references/subsystem-dispute-parsing.md`, loaded from handler-run.md. apm-specialist: extract to `references/dispute-parsing.md`. agentskills-specialist: maintain extraction.

The functional-decomposition revision introduces a sequencing condition that does not resolve the underlying architectural question — it defers it. I support the staging approach (functional-decomposition New Recommendation B, agentskills-specialist New Recommendation A), but the staged execution still requires a decision about the destination before Phase 1 begins. You cannot extract gate handler in Phase 1 without having decided what dispute-parsing will look like in Phase 3, because gate handler contains dispute-parsing consumers.

**What I do not concede:** functional-decomposition's internal inconsistency (acknowledged in their own revision) between "breaking-change content always in context" and "extract dispute-parsing" does not resolve in favor of either position — it reveals that the "always in context" principle needs to be scoped. I scope it as: breaking-change invariants with no defined call site must stay in the always-loaded core. Dispute-parsing has three defined call sites (run engine, converge, gate), each of which can carry an explicit load trigger. The trigger tells the agent when to load it; the agent does not have to carry it in context on every path that never reaches Phase 6.

**The residual disagreement:** functional-decomposition's valid concern is that the dispute-parsing subsystem, as an interface contract with breaking-change implications, loses some of its protective function when it is only conditionally loaded. An agent executing a `/conversus define` invocation (which never reaches Phase 6) will never load it — fine. But an agent executing `/conversus run` must load it before Phase 6 begins, and if the trigger is missed, the failure mode is silent incorrect output. This is the same failure mode argument as Dispute 1. I maintain the load trigger solution is sufficient; functional-decomposition's revised position maintains conditional deferral is prudent. We are 80% convergent on the end state, 20% apart on timing and conditionality.

---

### Dispute 3: Naming Convention — Two-Tier vs. Flat

**The unresolved split:** My sustained two-tier naming convention (`handler-{name}.md`, `subsystem-{name}.md`) conflicts with agentskills-specialist's flat naming (`dispute-parsing.md`, `preset-resolution.md`). functional-decomposition's New Recommendation C adopts my convention. apm-specialist's revision adopts my convention. agentskills-specialist's revision explicitly rejects it.

agentskills-specialist's argument: the agentskills specification does not define file-type prefixes for references, adding a taxonomy imposes classification overhead, and the load trigger in SKILL.md provides all the context the agent needs about the file's role. This argument would be correct if the reference directory had 3-4 files. It is less correct at 9-11 files, where directory navigation without prefixes requires reading each file's header to understand its role. A directory listing of `handler-define.md`, `handler-gate.md`, `subsystem-dispute-parsing.md` is immediately parseable. A listing of `define.md`, `gate.md`, `dispute-parsing.md` is parseable only if you already know the domain.

**What I do not concede:** The navigability argument at scale. This is a minor convention decision with low implementation cost and no architectural impact. The three-to-one position split (functional-decomposition, apm-specialist, integration-specialist vs. agentskills-specialist) does not guarantee correctness, but the convention costs nothing to adopt and provides measurable benefit at 9-11 files. agentskills-specialist's position that the specification does not mandate it is correct — the specification also does not prohibit it, and navigability conventions are exactly where local judgment should prevail.

**The residual disagreement:** Whether the classification overhead ("is dispute-parsing a subsystem or a handler?") introduces ambiguity that exceeds the navigability benefit. agentskills-specialist has a latent point here: if future files do not fit cleanly into `handler-` or `subsystem-`, contributors will create ad-hoc prefixes or misclassify. I accept this as a real risk but maintain it is manageable with a documented convention (two categories, clear definitions) rather than by abandoning categorization.

---

### Dispute 4: Run Engine Multi-Round Extraction — Dependency Analysis Required vs. Position Now

**The unresolved split:** functional-decomposition's revised Recommendation 4 requires an explicit dependency analysis before deciding whether multi-round orchestration can be extracted. My original Dangerous Contradiction 1 identified the shared state machine as the reason extraction is risky. agentskills-specialist's revision creates `references/multi-round-execution.md` and retains it. These three positions conflict: one defers to empirical analysis, one extracts, one (my original) opposed extraction.

In my revision I conceded the run engine placement but retained the "do not decompose" constraint specifically for the round/iteration state machine. If the engine moves to `references/handler-run.md`, then multi-round orchestration within handler-run.md is a question of internal decomposition within that file — and my "do not decompose" constraint applies. The round loop + iteration loop + output path computation + termination logic must remain a single unit within handler-run.md, regardless of the file's location. This is the position I maintain.

What I do not resolve here: if the engine stays in root SKILL.md (agentskills-specialist's revised position), then functional-decomposition's proposed extraction of multi-round to a conditional reference file creates a seam through the middle of root SKILL.md's most critical state machine. My original critique applies with full force in that scenario.

**What the group needs to decide:** The multi-round extraction decision depends on run engine placement (Dispute 1). These two disputes are coupled. Whatever file contains the run engine core contains the multi-round orchestration, and the "do not further decompose" constraint applies within that file. This is not a separate dispute; it is downstream of Dispute 1.

---

## Convergence

### Convergence 1: References as the Primary Decomposition Mechanism

All five positions — including apm-specialist's full reversal from sub-skills — converge on agentskills `references/` as the correct decomposition primitive for conversus. This is not a superficial agreement: apm-specialist explicitly retracts the APM sub-skills proposal and explains why the invocation-time conditional loading model addresses conversus's context window problem, while install-time packaging does not. The convergence is architecturally substantive.

**Shared implications:** No sub-skills needed (except gate as a future candidate after reference file decomposition proves stable). No APM context primitives for runtime execution content. Mode specifications belong in `references/mode-{name}.md` or within the run engine core, not in `.apm/context/`. Preset resolution belongs in `references/subsystem-preset-resolution.md` (or flat equivalent), not as a registered sub-skill.

**Implementation implication:** The agentskills `references/` directory is the primary structural work product of this spec. All other structural decisions (AGENTS.md files, APM manifest, linter expansion) are secondary to getting the reference file layout and load triggers correct.

### Convergence 2: The Two-Class Load Trigger Model

My New Recommendation N2 introduced the Class A (dispatch-table, pre-invocation) vs. Class B (config-conditional, mid-execution) distinction. functional-decomposition adopted it as New Recommendation B's "Modified Recommendation 8." agentskills-specialist's revised Recommendation 9 proposes the identical Tier 1/Tier 2 framing. apm-specialist's New Recommendation N2 states: "The key architectural insight from this review cycle is the distinction between install-time placement and invocation-time loading" — and endorses runtime-state-triggered loading with explicit fallback behavior.

**Shared implications:** Subcommand handlers are Class A / Tier 1 — loaded unconditionally at dispatch time for a given invocation, before execution begins. Shared subsystems (dispute-parsing, preset-resolution) are Class B / Tier 2 — loaded conditionally based on config field inspection. Class B triggers require explicit fallback behavior in the handler that calls them. No reviewer disputes this framing; only the naming differs slightly across documents.

**Implementation implication:** Every reference file load instruction must specify its class. Handler reference files carry Class A triggers in the dispatch table. Subsystem reference files carry Class B triggers in the handler that invokes them, with explicit "if this file cannot be loaded, halt and report" language.

### Convergence 3: AGENTS.md Files are Pointer-Based, Not Rule-Restating

agents-md-specialist's revision fully accepts the correction from all four cross-reviews: AGENTS.md files should not duplicate runtime-enforced contracts. The revised scope is 15-30 line pointer files with linter commands and "see also" references. All four other reviewers endorsed this scope restriction.

**Shared implications:** No AGENTS.md file should contain validation rules, naming conventions, or structural markers that are also enforced by the runtime. Where content overlaps, SKILL.md (or reference files) owns the authoritative version; AGENTS.md points to it. The pointer format is explicit and consistent: "Rule X is enforced at runtime. See `references/subsystem-Y.md` for the authoritative contract."

**Implementation implication:** AGENTS.md creation is not a SKILL.md size-reduction strategy and should not be presented as one. It is a cross-agent contribution discoverability improvement. Sequence it after reference file extraction.

### Convergence 4: The Run Engine's Internal State Machine Must Not Be Split

My original Dangerous Contradiction 1 critique of multi-round extraction produced universal acceptance that the round/iteration state machine is a non-decomposable unit. agentskills-specialist's revision explicitly states: "the round loop, iteration loop, output path computation, and termination logic must remain a single unit." functional-decomposition's revision accepts the dependency analysis requirement before any split. apm-specialist's revision does not challenge this constraint.

**Shared implication:** Whether the engine lives in root SKILL.md or `references/handler-run.md`, the "do not decompose" annotation applies within that file. The single-round path and multi-round path are not separately extractable because single-round semantics are defined as the negation of multi-round behavior (no `round-N/` directories, no stagnation detection, no cross-round synthesis). Splitting them requires one to restate what it is opting out of.

**Implementation implication:** Any implementation of this spec must validate that the multi-round orchestration block and single-round termination conditions remain in the same file as a single cohesive unit.

### Convergence 5: Staged Execution with Validation Gates

functional-decomposition's New Recommendation B, agentskills-specialist's New Recommendation A, and my own staging-compatible position all agree: implement gate handler extraction first, validate that reference loading works in practice, then proceed to remaining handlers, then subsystem references. No reviewer advocates all-at-once structural replacement.

**Shared implication:** The gate handler is the Phase 1 validation target regardless of any other architectural decision. It is universally agreed to be the lowest-risk extraction, the cleanest boundary, and the most self-contained subcommand. Its extraction proves the reference file mechanism before any ambiguous cases are attempted.

**Implementation implication:** The execution plan should be: (0) triage and move contribution-oriented content per agents-md-specialist's New Recommendation B, (1) extract gate handler and validate, (2) extract remaining guided handlers, (3) extract subsystem references if handler extractions succeed, (4) revisit multi-round and run engine placement based on empirical results from phases 1-3.

---

## Final Position Statement

### Non-Negotiables

**1. The run engine's internal state machine is never split across files.**
The round/iteration counters, output path formulas, retroactive directory moves, stagnation detection, and termination conditions are a single unit. They may not be separated into a "single-round core" and "multi-round extension" without one restating what it is opting out of. This constraint applies within whatever file contains the engine, whether that is root SKILL.md or `references/handler-run.md`. Violation produces a silent failure mode where the single-round path operates without knowing its own boundary conditions.

**2. Class B load triggers must include explicit fallback behavior.**
Any conditional subsystem reference — dispute-parsing, preset-resolution, or future equivalents — must specify what the agent does if the file cannot be loaded. "Halt and report the error" is the only safe default. Silent skipping of a failed subsystem load means the agent attempts dispute parsing without the parsing algorithm, producing incorrect round-termination decisions. The fallback instruction must be in the handler that calls the subsystem, not assumed.

**3. Reference files are the authoritative source for runtime contracts; AGENTS.md files are pointer documents.**
No runtime validation rule, structural marker, or interface contract may exist in a canonical form only in AGENTS.md. The authoritative version lives in SKILL.md or a reference file. AGENTS.md may summarize, point to, and cite — never own. If this boundary erodes, the decomposition gains a drift surface that is invisible to the linter and has no runtime signal.

**4. The two-tier naming convention (`handler-`, `subsystem-`) must be decided before Phase 1 extraction.**
Retroactive renames after 9-11 reference files exist are high-friction and create broken load triggers across SKILL.md. The naming convention is a P3 decision but must be made before any file is written.

### Flexibility

**On run engine placement:** I hold that `references/handler-run.md` is the correct destination for the engine, enabling a root SKILL.md at ~300-350 lines under 5,000 tokens. However, if empirical testing of the gate handler extraction (Phase 1) reveals that agents routinely fail to follow mandatory load triggers in handler reference files, I will accept keeping the engine in root. The principle is execution correctness over token budget — I just assess that a mandatory-framed Class A trigger is sufficient. This assessment should be revisited with evidence.

**On dispute-parsing timing:** I accept functional-decomposition's staging condition: validate handler extractions first, then assess whether to extract dispute-parsing. If Phase 1 and Phase 2 handler extractions succeed, the argument for extracting dispute-parsing becomes stronger (agents are proven to follow reference triggers). If they reveal load-trigger fragility, keeping dispute-parsing inline is the correct response. My position is that the end-state architecture includes extracted dispute-parsing; the timing is genuinely negotiable.

**On multi-round extraction:** If the engine moves to `references/handler-run.md` and a dependency analysis shows that fewer than 20 lines constitute the shared interface between single-round and multi-round paths, I am open to further decomposing multi-round orchestration within that reference file. The "do not decompose" constraint was calibrated for the state machine's coupling in the current codebase; if extraction can be done cleanly without restating the single-round boundary conditions, I do not oppose it on principle.

**On APM gate sub-skill promotion:** apm-specialist's New Recommendation N1 (promote gate to an APM sub-skill after reference file decomposition stabilizes) is architecturally sound and I support it in principle. Gate's CI/CD audience, self-contained config schema, and self-contained output format make it the only subcommand that passes both sub-skill tests. My non-negotiables do not constrain this decision; it is orthogonal to reference file decomposition and can proceed independently once the reference file structure has proven stable across two or more spec iterations.
