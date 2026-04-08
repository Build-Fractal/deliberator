# Cross-Review of functional-decomposition's Review

**Reviewer:** integration-specialist
**Reviewing:** functional-decomposition's Phase 1 review of spec 011a (SKILL.md Breakdown)

---

## Dangerous Contradictions

### 1. Run engine extraction depth — "~265 lines remaining" vs "tightly coupled state machine"

functional-decomposition proposes extracting multi-round orchestration (~360 lines), preset resolution (~75 lines), and the Dispute-Parsing Subsystem (~30 lines) from the run engine, leaving a ~265-line core in SKILL.md (Recommendation 7). My review explicitly identifies the round loop + iteration loop + output path computation + termination check (lines 346-580) as a "tightly coupled state machine" that must remain as a cohesive unit and names it a "do not decompose" boundary (Recommendation 7).

The contradiction: functional-decomposition counts multi-round orchestration as a clean extraction (~360 lines that "only apply when rounds > 1"), but this block contains the output path formulas, iteration file naming logic, retroactive Round 1 directory moves, and termination condition checks that the single-round path also depends on for its negative-case definitions (e.g., "When rounds: 1, no round directories, no cross-round synthesis"). Extracting multi-round to a conditional reference means the single-round execution path in SKILL.md must restate what "no round directories" means without referencing the round directory logic it is opting out of. The agent executing a single-round run would have no loaded context for what round directories are, making error messages about accidental round-directory creation incomprehensible.

**Resolution required:** The run engine's round/iteration state machine must either stay fully intact in SKILL.md (my position) or be extracted as a complete unit including the single-round path (neither review proposes this). A partial extraction that removes multi-round but keeps single-round creates an interface boundary through the middle of a state machine.

### 2. Token budget targets are incompatible with run engine retention

functional-decomposition's Recommendation 9 proposes documenting a per-invocation token budget, citing the agentskills recommendation that "the activated body" stay under 5,000 tokens. Recommendation 7 proposes retaining the run engine core at ~265 lines (~3k tokens) in SKILL.md plus dispatch table, shared notes, and frontmatter for a total of ~345 lines. My review proposes retaining the dispatch table, multi-agent isolation rules, and run engine core at ~400-500 lines.

The contradiction is not between us but between both reviews and the 5,000-token ceiling. My estimate of 400-500 lines for the root SKILL.md translates to roughly 6-7k tokens. functional-decomposition's ~345-line estimate assumes successful multi-round extraction, which I challenge in Contradiction 1 above. If multi-round logic stays in SKILL.md (as I recommend), the root file lands at ~700 lines / ~9k tokens. If it is extracted (as functional-decomposition recommends), the root file meets the target but the multi-round conditional reference adds ~5k tokens for multi-round invocations, bringing the per-invocation total to ~8k tokens anyway.

**Resolution required:** Both reviews should acknowledge that conversus, as an orchestration engine with a complex state machine, may legitimately exceed the 500-line / 5k-token guideline. The token budget should be framed as a target with a documented exception for the run engine, not as a hard constraint that drives unsafe extraction.

### 3. Reference file load triggers — "unambiguous" dispatch vs conditional subsystem loading

functional-decomposition describes subcommand-routed loading as having "unambiguous" triggers (Recommendation 2: "it matches exactly one dispatch table entry") and conditional subsystem loading as equally clean ("if rounds > 1, read multi-round reference" in Recommendation 4; "if any agent entry has a preset field, read preset-resolution reference" in Recommendation 5). My review's Recommendation 1 keeps the run engine intact specifically to avoid conditional mid-execution loading, and my Missed Opportunities section flags the lack of consideration for error message contracts across reference boundaries.

The contradiction: dispatch-table triggers are indeed unambiguous because they fire at invocation time before execution begins. But conditional subsystem triggers fire mid-execution based on config inspection. An agent that has already begun config parsing and encounters a preset field must then load a reference file, integrate its content into its active context, and resume parsing. This is a fundamentally different operation from pre-loading a handler file before starting work. functional-decomposition treats both patterns as equivalent ("conditional load trigger is clean and unambiguous"), but mid-execution reference loading creates a context-switching cost and a failure mode (what if the file is missing?) that pre-invocation loading does not.

**Resolution required:** Distinguish between two classes of reference loading: (a) pre-invocation dispatch routing (safe, analogous to function call dispatch), and (b) mid-execution conditional loading (risky, analogous to dynamic module import). Class (b) needs explicit fallback behavior and should be minimized.

---

## Tensions

### 1. Extraction granularity — maximum extraction vs minimum interface surface

functional-decomposition proposes nine extraction targets (gate handler, five guided handlers, dispute parsing, multi-round orchestration, preset resolution, validation contract) totaling approximately 1,500-1,800 lines removed from SKILL.md. My review proposes seven extraction targets (five guided handlers, gate handler, dispute parsing, preset resolution, template variables) but explicitly keeps multi-round orchestration and validation inline. functional-decomposition optimizes for minimal always-loaded context; I optimize for minimal interface boundary count.

Both positions are defensible. functional-decomposition's aggressive extraction achieves a ~345-line root SKILL.md that is close to the agentskills guideline. My conservative extraction results in a ~500-line root SKILL.md that requires fewer cross-file references. The tension is real: each extracted reference file creates a new interface boundary that must be maintained, versioned, and kept consistent. But each retained inline section inflates the always-loaded context.

The deciding factor should be empirical: how often do single-round, preset-free runs occur? If they are the 80% case (as functional-decomposition asserts), multi-round extraction pays off. If multi-round runs are common, the extraction creates load overhead on the majority path.

### 2. Validation centralization — shared contract file vs handler-specific schemas

functional-decomposition's Recommendation 6 proposes a `references/validation-contract.md` that defines shared heading checks, name pattern regex, path existence verification, and the post-write validation pattern. My review does not propose validation extraction and instead focuses on expanding the linter (Recommendation 8) to serve as the executable integration test.

The tension: a shared validation reference file makes the contract human-readable and agent-accessible. An expanded linter makes the contract machine-executable and automatically verified. These are not mutually exclusive, but maintaining both creates a synchronization burden. If the validation reference file says "headings are case-insensitive" but the linter implements case-sensitive matching, the reference file becomes a source of bugs rather than a source of truth. functional-decomposition's approach trusts the agent to follow the reference file; my approach trusts the linter to enforce the contract. The pragmatic resolution is to choose one as authoritative and derive the other.

### 3. Naming convention scope — type-prefixed names vs flat names

My review proposes a naming convention (`handler-{name}.md`, `subsystem-{name}.md`, `contract-{name}.md`) that encodes the reference file's architectural role in its filename (Recommendation 9). functional-decomposition proposes the same `handler-{name}.md` pattern for guided handlers (Recommendation 2) but does not extend this to subsystems or contracts, using ad-hoc names like `dispute-parsing.md`, `preset-resolution.md`, `validation-contract.md`, `multi-round-orchestration.md`.

The tension is between discoverability and simplicity. Type-prefixed names make the dependency graph readable from `ls references/` alone, and they prevent name collisions between handler files and subsystem files. But they add a convention that must be learned and enforced. Flat names are more natural and do not require understanding the type taxonomy. For a skill with 8-10 reference files this is a minor concern; for a skill that grows to 20+ reference files it becomes material.

### 4. Antipattern catalog integration — orchestrator concern vs handler concern

My review flags the antipattern check (lines 237-244) as a missed consideration: if each handler becomes a reference file, does each handler need its own antipattern check, or is this an orchestrator-level concern? functional-decomposition does not mention `antipatterns/catalog.md` at all.

The tension: the antipattern check currently runs as a pre-execution step in the run engine. After decomposition, `converge` and `gate` both delegate to the run engine, so the antipattern check is inherited. But the guided handlers (define, interests, mode) do not invoke the run engine and therefore would not trigger the antipattern check. If a future antipattern is added that applies to problem definition or interest discovery, the decomposed structure has no hook for it. This is a latent integration gap that neither review addresses directly.

### 5. The `converge` handler's dual nature — thin wrapper vs unique post-execution logic

functional-decomposition includes `converge` in the set of guided handlers to extract (Recommendation 2), estimating ~210 lines. My review's Alignment section notes that `converge` and `gate` both "delegate to the run engine without adding execution logic" (thin wrappers). But my Missed Opportunities section also flags that the converge handler's post-execution report (lines 1458-1533) duplicates the run engine's Step 5 report with mode-specific interpretation, creating drift risk if both are extracted to separate reference files without a shared report vocabulary.

The tension: extracting `converge` is straightforward if it is treated as a thin wrapper. But the post-execution report section is not thin — it contains ~75 lines of mode-specific interpretation logic that overlaps with run engine output. Extracting both to separate files without a shared contract for report structure risks the two reports diverging. functional-decomposition does not address this overlap; my review identifies it but does not propose a specific resolution.

---

## Safe Agreements

### 1. Subcommand handlers are the primary extraction candidates

Both reviews independently identify the six non-core subcommand handlers (define, interests, mode, converge, arbitrate, gate) as the highest-value extraction targets. functional-decomposition's Recommendations 1-2 propose exactly this, estimating ~1,400 lines removed. My Recommendations 2-3 propose the same extraction with the same rationale: these handlers are mutually exclusive at invocation time, have no shared in-memory state, and communicate through file artifacts on disk.

The reasoning converges from different angles: functional-decomposition arrives at this conclusion through context-efficiency analysis (why load gate handler logic during a define invocation?), while I arrive at it through interface analysis (file-mediated coupling between handlers is the safest form of dependency). Both analyses produce the same decomposition boundary, which is strong evidence that this boundary is correct.

### 2. The Dispute-Parsing Subsystem is a natural extraction target with a proven stable interface

Both reviews identify the Dispute-Parsing Subsystem (lines 750-777) as a well-bounded extraction candidate. functional-decomposition's Recommendation 3 proposes extraction to `references/dispute-parsing.md`. My Recommendation 4 proposes extraction to `references/subsystem-dispute-parsing.md`. The interface contract is agreed: input is a synthesis file path, output is boolean + integer, the structural markers and mode-specific headings are stable interfaces, and changes to them are breaking changes.

The only divergence is naming convention (flat name vs type-prefixed name), which falls under the Tensions section above. The decomposition boundary itself is safe because the SKILL.md already documents this subsystem's interface contract explicitly, including breaking-change semantics — it was designed for extraction even if it was not yet extracted.

### 3. Multi-agent isolation rules and gotchas must remain in the root SKILL.md

functional-decomposition's Alignment section identifies the non-negotiable multi-agent rules (lines 324-336) as "cross-cutting invariants" and Recommendation 10 explicitly retains the Important Notes and Baseline Features sections in SKILL.md as "gotchas — the highest-value content type." My Alignment section independently reaches the same conclusion: "These rules should remain in the root SKILL.md rather than being buried in a reference file, because they are the most important constraint an implementing agent must internalize."

Both reviews cite the agentskills best practices on gotchas as the justification. This is a safe agreement because it establishes a clear principle for what stays in the root file: invariants and gotchas that apply to all invocation paths. Any decomposition proposal that moves these to reference files should be rejected.

### 4. The spec (011a) is underspecified and both reviews are generating the decomposition proposal from scratch

functional-decomposition's Executive Summary notes that the spec "provides only a one-line prompt without proposing concrete decomposition boundaries." My Missed Opportunities section states the spec "is only 11 lines and provides no concrete decomposition proposal." Both reviews independently generated detailed extraction plans, naming conventions, and interface contracts that the spec itself does not contain.

This is a safe agreement about the state of the input, and it has a practical implication: the deliberation output will need to function as the actual decomposition specification, not merely as commentary on an existing proposal. The synthesis should consolidate the two reviews' extraction plans into a single actionable specification with explicit file boundaries, interface contracts, and load triggers.

---

## Referenced Documentation

- `conversus/specs/011a-skill-breakdown/conversus-output/functional-decomposition/review.md` — functional-decomposition's Phase 1 review (full file)
- `conversus/specs/011a-skill-breakdown/conversus-output/integration-specialist/review.md` — integration-specialist's Phase 1 review (full file)
- `conversus/SKILL.md` — lines 22-44 (dispatch table), 324-336 (multi-agent rules), 346-580 (round/iteration state machine), 750-777 (dispute-parsing subsystem)
- `conversus/specs/011a-skill-breakdown/spec.md` — the decomposition problem statement (full file)
- `conversus/README.md` — architectural context (full file)
