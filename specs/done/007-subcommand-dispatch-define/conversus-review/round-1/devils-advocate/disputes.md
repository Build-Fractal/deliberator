# Disputes — Devil's Advocate Final Position on 007-subcommand-dispatch-define

**Reviewer**: devils-advocate
**Phase**: Final disputes and convergence
**Date**: 2026-03-22

---

## Remaining Disputes

### Dispute 1: Producer-side validation is necessary but not sufficient — the shared validation function is non-negotiable

All three reviewers now agree on producer-side post-write schema validation for `problem.md`. The consensus position (integration-architect Rec #1, functional-typing New Rec A) is that the define handler validates all 7 headings after writing. I do not dispute this.

What I dispute is the implicit assumption — held most strongly by integration-architect — that producer-side validation is *structurally prior* and therefore the dominant checkpoint. Integration-architect's revision states: "producer-side validation is structurally prior" and "consumer trusts the schema." This framing is dangerously incomplete. The define handler writes `problem.md`. The user edits it to resolve `[CLARIFY:]` tags. The user accidentally deletes `## Constraints`. Producer-side validation has already run and catches nothing. The artifact is now malformed, and every downstream consumer that trusts the schema breaks silently.

Functional-typing's New Recommendation B attempts to scope `[CLARIFY:]` tags as advisory within spec 007, explicitly deferring enforcement to downstream specs. This is a reasonable boundary for spec 007's authority, but it creates a vacuum: if spec 007 says "tags are advisory" and spec 008 does not yet exist to say "tags are gates," then tags are functionally meaningless. The spec has created a signaling mechanism that no one is obligated to read.

**My position**: The spec must mandate a shared validation function — not just a prose contract, but a named operation ("validate problem.md schema") with defined behavior (check 7 headings, report missing ones). The define handler calls it at write time. Downstream consumers call the same function at read time. This is the only architecture that survives post-write mutation. Integration-architect's revision gestures toward this ("define a validation function that downstream consumers can reference") but treats it as optional additive. It is not optional — it is the load-bearing element. Without it, producer-side validation is a checkpoint that validates the artifact at the moment it is least likely to be wrong.

**Why consensus is insufficient**: The current consensus says "producer validates, consumers may also validate." This "may" must become "must call the shared function." The difference is whether post-write mutation is a recognized threat model or an edge case each future spec author can independently choose to ignore.

---

### Dispute 2: The `[CLARIFY:]` status field must exist — advisory semantics are a design failure

Functional-typing's revised Recommendation 5 and New Recommendation B together construct a position where `[CLARIFY:]` tags are "advisory markers" whose enforcement is "a spec 008 decision, not a spec 007 decision." This is architecturally clean boundary-drawing, but it produces a broken user experience.

The spec's promise to non-expert users (spec.md L87: "Must NOT require coding knowledge to use") relies on the guided workflow catching incomplete problem definitions before they propagate. If `[CLARIFY:]` tags are advisory, a user who runs `/conversus define "architecture"` gets a `problem.md` with five `[CLARIFY:]` tags, sees the warning at SKILL.md L872-875, ignores it, and runs `/conversus interests`. What happens? The spec is silent. If `interests` proceeds anyway, the entire guided workflow's quality promise is void. If `interests` independently re-discovers the tags and blocks, we have redundant enforcement that functional-typing claims to want to avoid.

Integration-architect proposed a `## Status` section (`draft` / `ready`) that centralizes the gate in the artifact itself. This is the correct mechanism. I adopt it over my original consumer-side gate proposal. But functional-typing's advisory framing undermines even this mechanism: if the status field is also advisory, it adds a section that no one is required to check.

**My position**: The `## Status` section must be normative, not advisory. The define handler sets `status: draft` when `[CLARIFY:]` tags exist. Spec 007 must state: "Downstream commands SHOULD check the Status section before proceeding. Commands that consume a draft artifact SHOULD warn the user." The word "SHOULD" (RFC 2119) makes the expectation explicit without creating a hard gate that spec 007 does not have authority to impose on unwritten specs. This is stronger than functional-typing's "advisory" but weaker than a MUST-block gate. It is the appropriate middle ground.

---

### Dispute 3: Per-handler validation is the wrong architecture, even as a "pragmatic fix"

All three reviewers converged on the same pragmatic fix for `--context` path validation: mirror the `run` handler's validation at SKILL.md L195-196 in the `define` handler. Functional-typing proposed the specific error messages. Integration-architect upgraded it to P1. I also rated it P1.

But all three of us then acknowledged the architecture is wrong. I raised it in my revision (New Recommendation 1): per-handler validation scales linearly with subcommand count and guarantees inconsistency. Integration-architect's revision mentions "a validation function that downstream consumers can reference" without connecting it to dispatch-layer architecture. Functional-typing dismisses the concern outright: "The dispatch layer is a routing table, not a validation framework. Pushing validation into the dispatch layer would conflate routing with input validation."

Functional-typing's counterargument confuses the dispatch *table* with the dispatch *layer*. The dispatch table is the routing lookup at SKILL.md L22-26. The dispatch layer is the entire section (L18-34) plus any shared infrastructure handlers use. Common path validation is not "routing" — it is pre-handler infrastructure that runs after routing and before handler-specific logic. Every web framework in production distinguishes between routing (URL resolution), middleware (shared pre-handler logic), and handlers (endpoint-specific logic). Functional-typing's position collapses middleware into handlers, forcing each handler to reimplement shared concerns.

**My position**: Spec 007 should add a "Common Handler Utilities" subsection after the dispatch table (after SKILL.md L33) specifying at minimum: (a) path existence validation, (b) artifact schema validation (the shared function from Dispute 1). This does not need to be fully implemented in spec 007 — it needs to be *named and scoped* so that spec 008's handlers call the shared function instead of reimplementing it. The pragmatic fix (mirror L195-196 in the define handler) is acceptable as a stopgap, but the spec must acknowledge it is a stopgap and point to the shared-layer architecture as the intended direction. Without this, spec 008 will copy-paste the same validation block, spec 009 will do it again, and by the time someone notices the pattern, three specs have three independent implementations.

---

### Dispute 4: Multiple `--context` paths should not be deferred

Functional-typing's revision explicitly withdraws multi-path `--context` support, stating: "`--context` accepts exactly one path. To include multiple context sources, point to a directory containing them." Integration-architect withdrew their Recommendation 3, agreeing with functional-typing's conservative scoping.

I maintain this is wrong. The workaround — "point to a directory" — forces users to copy documents from their actual locations into a staging directory, creating stale duplicates. Integration-architect's own cross-review made this exact argument ("creates stale copies that drift from their sources") and then withdrew the recommendation anyway, deferring to functional-typing's conservative scoping.

The implementation cost is trivial: `--context` becomes a repeated flag (`--context a --context b`), each path is validated independently using the same path validation logic, and the Context Ingestion section (SKILL.md L797-802) processes them sequentially. There is no architectural complexity. There is no FR that prohibits it. There is no spec interaction that complicates it. The deferral is motivated by scope conservatism, not by technical or design concerns.

**My position**: The spec should support `--context` as a repeated flag. The single-path limitation creates a worse user experience than any scope concern justifies, and the workaround actively degrades input quality by encouraging stale document copies. If the consensus position is to defer, the spec must at minimum document the limitation as a known gap rather than presenting single-path as the intended design.

---

### Dispute 5: Refine semantics need more than "agent judgment"

Integration-architect's revised Recommendation 2 reduces the refine contract to four rules: (a) all 7 headings present, (b) existing content not silently deleted, (c) Source Documents unioned, (d) Type re-evaluated. My own New Recommendation 2 argues refine is "inherently heuristic" and should be left to agent judgment within schema validation bounds.

On reflection, I dispute my own prior position. Four rules is not enough, and "agent judgment" is not a specification. The problem is that "refine" has no observable contract a user can reason about. If I run `/conversus define "caching architecture"` and then `/conversus define --context new-requirements.md` choosing "refine," what guarantees do I have about the output? Under integration-architect's contract: headings are present, nothing was silently deleted, Source Documents include the new path, Type was reconsidered. But "nothing was silently deleted" is unverifiable — how does a user know whether a constraint was deleted or rephrased? "Type was reconsidered" is unobservable — the Type might stay the same because the agent reconsidered and confirmed it, or because it did not actually reconsider.

**My position**: The refine operation needs one additional guarantee beyond integration-architect's four: a visible diff summary. After refining, the define handler should print what changed: "Added 2 constraints, updated Context, Type unchanged." This makes the heuristic operation auditable without prescribing deterministic merge rules. The user can inspect the summary, open `problem.md`, and verify. Without this, "refine" is a black box whose output the user must manually diff against the prior version.

---

## Convergence

The following positions have reached genuine consensus across all three reviewers and I do not dispute them.

### 1. Post-write schema validation is required (P1)

All three reviewers independently converged on this: the define handler must validate that `problem.md` contains all 7 required headings after writing. The mechanism (check headings, add `[CLARIFY:]` placeholders for missing ones) is agreed. The only remaining dispute is whether consumer-side validation is also required (see Dispute 1 above), not whether producer-side validation should exist.

### 2. `--context` path validation is required (P1)

Universal convergence. All three reviewers rate this P1. The define handler must fail with a clear error if `--context <path>` does not exist, mirroring the `run` handler's path validation at SKILL.md L195-196. The error message format ("Context path does not exist: {path}") is agreed. The directory-with-no-markdown-files warning is agreed.

### 3. Dispatch matching is exact and case-sensitive

Functional-typing's revised Recommendation 1 (exact, case-sensitive matching that fires L31-32 on mismatch) is accepted by all reviewers. The fallback-to-`run` proposal is fully withdrawn. Integration-architect's New Recommendation 3 adds an improved error message with a suggestion ("Did you mean: `/conversus run {cmd}`?"), which is a welcome addition that does not conflict.

### 4. The `define` command runs in the main conversation, no subagents

All three reviewers agree on the substance. Functional-typing's version-scoped wording ("In this version, the define command executes entirely in the main conversation") is the best formulation because it avoids permanently constraining future iterations. Upgrade to P2 is agreed.

### 5. Empty-section `[CLARIFY:]` coverage for Constraints and Success Criteria

Functional-typing's Recommendation 5 and integration-architect's New Recommendation 2 converge on the same fix: extend SKILL.md L854 to specify `[CLARIFY:]` behavior for empty Constraints and Success Criteria sections. The proposed text is substantively identical across both reviews. Agreed at P2.

### 6. Staleness tracking via content hash

My Recommendation 3 (staleness tracking between `problem.md` and `interests.md`) is agreed in principle, with integration-architect's refinement (content hash over modification timestamp) adopted. The mechanism is straightforward and the pattern has precedent in the engine. Agreed at P2, with implementation deferred to spec 008 since `interests.md` does not yet exist.

### 7. Taxonomy closure acknowledged as a design decision

My Recommendation 4 (acknowledge the four-type taxonomy is intentionally closed) is agreed by integration-architect and not contested by functional-typing. The revised language — committing to closure and naming the prerequisite for extension (companion spec 008 update) — eliminates the self-contradiction functional-typing identified. Agreed at P2.

### 8. Backward compatibility is preserved

All three reviewers confirm: FR-002 (run behavior unchanged) and FR-003 (no-argument defaults to run) are fully satisfied. The dispatch table is additive. The engine internals are untouched by the define handler. This is the spec's strongest property.

### 9. `--output` directory creation semantics

Functional-typing's Recommendation 4 (create output directory including intermediates, fail with clear error on creation failure) is uncontested. Agreed at P2.

### 10. Single `--context` path documented (even if I dispute deferring multi-path)

If multi-path support is not added in spec 007, the spec must at minimum clarify that `--context` accepts exactly one path. This documentation is agreed regardless of the multi-path dispute.

---

## Final Position Statement

The spec is well-constructed. The dispatch mechanism is clean, backward compatibility is preserved, FR coverage is complete, and the define handler is properly isolated from engine internals. These are not in dispute.

The disputes that remain are architectural, not functional. They concern how the spec positions itself relative to the commands that will consume its output — and whether "spec 007 does not have authority over spec 008" is a valid reason to leave critical integration contracts unspecified.

Three disputes are load-bearing:

**First**, the shared validation function. Producer-side validation alone does not survive post-write mutation. The spec either mandates a shared validation function that both producer and consumer call, or it accepts that `problem.md` schema compliance is unenforceable after the user edits the file. The current consensus ("producer validates, consumers may also validate") is an architecture that works only if every future spec author independently chooses to add validation — which is another way of saying it works by coincidence, not by design.

**Second**, the `[CLARIFY:]` enforcement semantics. Advisory tags in a guided workflow for non-expert users are a contradiction. The spec promises structured output with marked ambiguities. If nothing enforces those marks, the workflow degrades to "the agent writes some markdown and the user can ignore the warnings." Integration-architect's `## Status` field is the right mechanism. Functional-typing's advisory scoping is the wrong semantics. The middle ground is RFC 2119 SHOULD: explicit expectation without hard mandate.

**Third**, the dispatch-layer architecture. Per-handler validation is copy-paste engineering. The spec should at minimum name and scope a shared validation layer, even if the full implementation waits for a later spec. Functional-typing's position that "the dispatch layer is a routing table, not a validation framework" mistakes the dispatch table for the dispatch layer and will produce three independent validation implementations by spec 009.

The remaining disputes (multi-path `--context`, refine diff summary) are genuine improvements that would make the spec better, but the system works without them. The three disputes above concern whether the system works *reliably* as it scales to multiple consuming specs — and that is not optional for a foundational specification.
