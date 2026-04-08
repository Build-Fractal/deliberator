# Disputes — integration-architect (Phase 4)

**Reviewer**: integration-architect
**Phase**: Final Disputes & Convergence
**Date**: 2026-03-22
**Basis**: Revised positions from functional-typing, integration-architect, devils-advocate

---

## Remaining Disputes

### Dispute 1: Multi-path `--context` — scope boundary disagreement

**Parties**: devils-advocate (Rec #5, P2 maintain) vs. functional-typing (Rec #8, single-path survive) and integration-architect (Rec #3, withdrawn)

Devils-advocate maintains that `--context` should accept multiple paths via repeated flags (`--context a --context b`), elevating the justification from consistency to data-integrity: users who copy files into a single directory to work around the single-path constraint create stale duplicates that drift from source (devils-advocate revision, Rec #5). Functional-typing explicitly constrains `--context` to a single path with the workaround being a directory pointer (functional-typing revision, Rec #8). I withdrew my original multi-path recommendation in my revision (Rec #3) and conceded functional-typing's conservative scoping.

**My position**: This dispute is a scoping question, not a correctness question. Devils-advocate's data-integrity concern is real but speculative for spec 007's user population. The spec targets "non-expert" users (spec.md L87: "Must NOT require coding knowledge to use"). A non-expert user running `/conversus define` for the first time is unlikely to have context documents scattered across multiple directories. The multi-path use case arises in mature workflows where users have accumulated specs, proposals, and architecture docs in different repos or directories -- that is a power-user scenario better addressed in a follow-up spec once `/conversus define` has been used in practice and actual multi-path needs are observed. Functional-typing's single-path constraint with directory workaround is sufficient for spec 007. I side with functional-typing. This dispute should not block the spec.

---

### Dispute 2: `[CLARIFY:]` gate mechanism — status field vs. advisory semantics

**Parties**: devils-advocate (Rec #1, `status: draft | ready` field) and integration-architect (New Rec #1, `## Status` section) vs. functional-typing (New Rec B, advisory-only within spec 007)

All three reviewers agree that `[CLARIFY:]` tags need clearer enforcement semantics. The disagreement is about where and how strongly to enforce them:

- **Devils-advocate** originally proposed a consumer-side gate in spec 008, then revised to a producer-side `status: draft | ready` field in `problem.md` (devils-advocate revision, Rec #1). They explicitly defend that vague inputs *should* block downstream progression: "a vague problem definition should not produce agents and interests without user intervention."
- **I** proposed a `## Status` section in `problem.md` with `draft` / `ready` values and a count of items needing clarification (my revision, New Rec #1). This is architecturally aligned with devils-advocate's revised mechanism.
- **Functional-typing** proposed scoping `[CLARIFY:]` tags as advisory within spec 007, explicitly stating: "Whether downstream commands enforce these tags as gates is defined by those commands' own specifications" (functional-typing revision, New Rec B).

**My position**: I align with devils-advocate on the need for a concrete status indicator in the artifact, and I disagree with functional-typing's deferral. Here is why:

Functional-typing's position treats spec 007 as hermetically sealed from its downstream consumers. But spec 007 is explicitly the first step in a pipeline (spec.md L15-16: "This artifact feeds subsequent commands (interests, mode) that ultimately produce a `conversus.yml`"). The define handler's report already references the next step: "Next step: /conversus interests" (SKILL.md L869). A spec that declares "my tags are advisory; downstream consumers decide" without providing a machine-readable signal forces every consumer to independently scan for `[CLARIFY:]` patterns -- exactly the N-consumer enforcement problem devils-advocate identified.

However, I concede that the *enforcement behavior* (blocking vs. warning) is genuinely a spec 008 decision. The compromise is: spec 007 MUST produce a status indicator (a `## Status` section with `draft` or `ready` and a clarification count). Spec 008 decides whether `draft` status blocks or warns. This gives downstream consumers a structured signal without prescribing their response. The status section is a statement of fact ("this artifact has N unresolved items"), not a gate directive.

---

### Dispute 3: `--force` and `--dry-run` flags — pre-investment vs. scope discipline

**Parties**: devils-advocate (Rec #6, maintain P2) vs. functional-typing (implicit opposition) and integration-architect (not addressed)

Devils-advocate maintains `--force` and `--dry-run` at P2, citing spec 011's gate automation as the motivating use case (devils-advocate revision, Rec #6). Functional-typing noted in the cross-review phase that spec 007 targets non-expert human users and that automation flags are pre-investment for a future spec. I did not address these flags in my original or revised review.

**My position**: I side with functional-typing's implicit position. The flags are legitimate future features but belong in a spec that defines the automation surface (spec 011 or its successor). Adding `--force` and `--dry-run` to spec 007 expands the handler's interface surface by 50% (from two flags -- `--context` and `--output` -- to four) without an immediate user need. The existing FR-011 safeguard (SKILL.md L786-793: present existing file and ask refine/replace) is the correct interactive behavior. `--force` exists to bypass that safeguard, which is valuable in CI but premature in a spec whose constraint is "Must NOT require coding knowledge to use." I recommend deferring both flags to a follow-up spec with P3 priority as a documentation note.

---

### Dispute 4: Shared validation layer vs. per-handler validation

**Parties**: devils-advocate (New Rec #1, shared dispatch-layer validation) vs. functional-typing (Rec #2, handler-local validation) and integration-architect (Rec #8 revised, handler-local with shared function note)

Devils-advocate proposes a "Common Handler Utilities" subsection in the dispatch section of SKILL.md, specifying shared validation operations that any handler can invoke (devils-advocate revision, New Rec #1). Functional-typing explicitly defends handler-local validation: "The dispatch layer (SKILL.md L18-34) is a routing table, not a validation framework. Pushing validation into the dispatch layer would conflate routing with input validation -- two distinct concerns" (functional-typing revision, Rec #2).

**My position**: Both are partly right, but for spec 007, functional-typing's per-handler approach is correct. Here is the architectural reasoning:

The dispatch table at SKILL.md L18-34 is six lines of routing logic. It should stay minimal. Devils-advocate's "Common Handler Utilities" subsection would add validation infrastructure to a routing table, violating separation of concerns. However, devils-advocate's underlying concern -- that three handlers with three independent validation implementations will drift -- is a real integration risk.

The resolution is my revised Rec #1's approach: define a validation function as a prose contract in the `problem.md` schema section, not in the dispatch section. This keeps routing and validation separate while centralizing the schema validation logic. Future handlers that consume `problem.md` reference the same validation contract. For spec 007, the define handler implements path validation locally (mirroring SKILL.md L195-196), and the schema validation contract is defined alongside the `problem.md` schema (SKILL.md L822-850). This is not a dispatch-layer concern; it is a schema-layer concern.

---

### Dispute 5: Refine semantics — minimal contract vs. heuristic declaration

**Parties**: integration-architect (Rec #2 revised, minimal contract with four rules) vs. devils-advocate (New Rec #2, heuristic declaration)

Both my revised Rec #2 and devils-advocate's New Rec #2 agree that prescriptive merge rules are wrong. The dispute is about how much structure to impose on the refine operation:

- **I** define four minimum constraints: (a) all 7 headings preserved, (b) no silent deletion of existing content, (c) Source Documents unioned, (d) Type re-evaluated. These are verifiable post-conditions.
- **Devils-advocate** proposes a prose declaration that the operation "is inherently heuristic" and that the spec "defines the intent but does not prescribe deterministic merge rules," with only schema validation as the structural guarantee.

**My position**: My four-rule minimal contract is the correct resolution. Devils-advocate's "inherently heuristic" framing is accurate as a description but insufficient as a specification. A spec that says "the agent uses judgment" without bounding acceptable variance is not a spec -- it is a wish. My four rules are not algorithmic merge operations; they are post-conditions that can be verified after the refine completes. "All 7 headings preserved" is a heading-existence check. "No silent deletion" means the diff between old and new should not show sections vanishing without replacement. "Source Documents unioned" means old paths appear in the new file. "Type re-evaluated" means the Type field reflects the combined input. These are structural invariants, not algorithmic prescriptions, and they are exactly what a downstream consumer needs to trust the refined artifact.

---

## Convergence

The following positions have reached consensus across all three reviewers and require no further debate.

### 1. Context path validation is P1

All three reviewers independently converged on this: the `--context` path must be validated before ingestion, mirroring the `run` handler's validation at SKILL.md L195-196. Functional-typing (Rec #2), integration-architect (Rec #8 revised to P1), and devils-advocate (Rec #7 elevated to P1) are fully aligned. The implementation is a direct parallel: "If the path does not exist, fail with: 'Context path does not exist: {path}'." This is the single strongest consensus across the entire review process.

### 2. Post-write schema validation for `problem.md` is P1

Functional-typing (New Rec A) and integration-architect (Rec #1) converge on producer-side heading validation after writing `problem.md`. Devils-advocate (Rec #2 revised) agrees on producer-primary validation with a shared function for consumer use. The mechanism is: verify all 7 required headings exist after the agent writes the file; if any heading is missing, add it with a `[CLARIFY:]` placeholder and re-write. The engine precedent at SKILL.md L659-676 (Phase 6 output validation) and L286-295 (template validation) supports this pattern.

### 3. Dispatch matching is exact and case-sensitive

Functional-typing (Rec #1 revised) and integration-architect (New Rec #3) converge: subcommand matching is exact and case-sensitive, and the dispatch table is exhaustive. The error at SKILL.md L31-32 fires for any non-matching first argument. Functional-typing withdrew the fallback-to-`run` proposal after both other reviewers demonstrated the typo-masking failure mode. The remaining action is a clarifying sentence in SKILL.md, not a behavioral change.

### 4. `define` runs in main conversation (version-scoped)

All three reviewers agree this should be stated explicitly. Functional-typing (Rec #6 revised) proposed "In this version" scoping. Integration-architect (Rec #7 revised to P2) and devils-advocate did not contest. The wording is settled: "In this version, the define command executes entirely in the main conversation. No subagents are launched."

### 5. Empty-section `[CLARIFY:]` coverage for Constraints and Success Criteria

Functional-typing (Rec #5) and integration-architect (New Rec #2) converge: SKILL.md L854 should be extended to cover Constraints and Success Criteria sections with explicit `[CLARIFY:]` placeholder text when the agent cannot determine content. This is the logical consequence of FR-010's universal rule (SKILL.md L852) applied uniformly. Devils-advocate did not contest the substance.

### 6. Single `--context` path for spec 007

Functional-typing (Rec #8) and integration-architect (Rec #3 withdrawn) converge on documenting the single-path constraint now. Devils-advocate dissents (see Dispute 1) but acknowledges this is a prioritization disagreement. The majority position: "`--context` accepts exactly one path. To include multiple context sources, point to a directory containing them."

### 7. Staleness tracking uses content hash

Devils-advocate (Rec #3 revised) and integration-architect agree: if staleness tracking is added between `problem.md` and `interests.md`, it should use a SHA-256 content hash, not a modification timestamp. This is deferred to spec 008's scope but the mechanism is settled.

### 8. Taxonomy closure as a design decision

Devils-advocate (Rec #4 revised) and integration-architect agree: the four-type taxonomy (`selection`, `integration`, `scoping`, `stress-test`) is intentionally closed. Extending it requires a companion update to spec 008's mode mapping. Functional-typing did not contest.

### 9. Pipeline overview scaled down to single sentence

Functional-typing and devils-advocate both challenged my original multi-line pipeline overview (Rec #4) as speculative documentation of unimplemented commands. I conceded in my revision. The action is a single appended sentence at SKILL.md L869: "Next step: /conversus interests (not yet implemented -- this is the first of a series of guided setup commands)."

### 10. `--type` override flag withdrawn

Integration-architect withdrew (Rec #5). Functional-typing correctly noted no FR motivates it. Expert users who disagree with type classification edit the `## Type` line directly. No dissent.

---

## Final Position Statement

The spec 007 review process has produced a clear stratification of findings. Three items are P1 consensus with no remaining dispute: context path validation, post-write schema validation, and dispatch matching clarification. These should be incorporated into SKILL.md without further debate. Two items are P2 consensus: the version-scoped single-agent declaration and empty-section `[CLARIFY:]` coverage. These are low-risk additions with universal agreement.

The five remaining disputes are real but none threatens the spec's structural integrity. They divide into two categories:

**Scope disputes** (Disputes 1, 3, 4): Whether multi-path `--context`, `--force`/`--dry-run` flags, and shared validation infrastructure belong in spec 007 or a follow-up. These are prioritization disagreements where the majority position (defer) is correct for a foundational spec. The features are legitimate but premature. Spec 007's job is to establish the dispatch infrastructure and deliver a working `define` handler. Scope creep here delays delivery without improving the core user flow.

**Structural disputes** (Disputes 2, 5): How much structure to impose on `[CLARIFY:]` enforcement and refine semantics. These are genuine design questions. On `[CLARIFY:]` gates, I advocate a status indicator in the artifact (a factual signal) with enforcement behavior deferred to consuming specs. On refine semantics, I advocate a four-rule minimal contract (verifiable post-conditions) over a pure "agent judgment" framing. Both positions balance specification rigor against agent flexibility: enough structure to enable downstream consumers to trust the artifact, not so much that the spec becomes brittle.

The spec's strongest property -- complete isolation between the define handler (SKILL.md L769-876) and the engine internals (SKILL.md L36-766) -- is unchallenged by any reviewer. No recommendation from any reviewer requires modifying the run handler, the template system, or the engine execution flow. This confirms that spec 007's additive architecture is sound: it extends SKILL.md's capabilities without regressing its existing behavior. The synthesis phase should adopt the P1 consensus items, adopt the P2 consensus items, and resolve the five disputes by applying the majority positions documented above.
