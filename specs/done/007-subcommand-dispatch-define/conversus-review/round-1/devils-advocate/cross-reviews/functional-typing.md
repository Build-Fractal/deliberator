# Cross-Review of functional-typing's Review — by devils-advocate

**Cross-reviewer**: devils-advocate
**Reviewing**: functional-typing's Phase 1 review of 007-subcommand-dispatch-define
**Perspective**: Challenge convergent positions; surface unstated tensions

---

## Dangerous Contradictions

### 1. We agree on path validation but disagree on where the validation contract lives

functional-typing recommends adding `--context` path validation to the `define` handler (Recommendation 2, P1) and `--output` directory creation semantics (Recommendation 4, P2). I flagged the same gap (Missed Opportunity: "No explicit error path for unreadable context documents"; Recommendation 7, P2). On the surface this is agreement. It is not.

functional-typing frames the fix as local to spec 007 -- add validation rules to the `define` handler in SKILL.md, mirroring the `run` handler's validation block (SKILL.md L195-196). I framed the fix the same way. But here is the contradiction neither of us addressed: **if every handler must independently replicate the `run` handler's validation discipline, the dispatch architecture has no shared validation layer**. The `run` handler validates paths at L195-196. The `define` handler would validate paths in Context Ingestion. Future handlers (`interests`, `mode`) will each need their own path validation. We are both recommending a pattern that scales linearly with the number of subcommands and guarantees inconsistency as each spec author reinvents the same checks.

The dangerous part: functional-typing's framing ("maintain the same validation discipline") sounds like a principle, but it is actually a copy-paste instruction. My framing ("mirror the `run` engine's validation pattern") is the same copy-paste instruction in different words. Neither of us recommended what the base-integrator architecture pattern in CLAUDE.md demands: **push shared validation into the dispatch layer itself**, not into each handler. If we both ship our recommendations as-is, we entrench per-handler validation silos that will drift apart by spec 009.

### 2. functional-typing's dispatch precedence rule undermines its own backward-compatibility claim

functional-typing's highest-priority recommendation (Recommendation 1, P1) proposes: "If [the first argument] does not exactly match any known subcommand, it is treated as a config file path and routed to `run`." This means `/conversus my-config.yml` silently becomes `/conversus run my-config.yml`.

functional-typing justifies this as "more useful and backward-compatible." I disagree that this is backward-compatible -- it is a behavioral expansion. Pre-dispatch, `/conversus my-config.yml` was the only invocation form; there was no subcommand to match against. Post-dispatch, the same invocation now passes through a matching step that happens to fall through to `run`. The behavior is the same, but the mechanism is different, and the mechanism has failure modes the old path did not:

- If a future subcommand is added whose name collides with a config filename (e.g., a subcommand named `test` and a file `test.yml` where the user runs `/conversus test`), the dispatch precedence rule silently changes the routing. The user gets the `test` subcommand, not their config file.
- functional-typing's rule says "exact and case-sensitive match." But SKILL.md's dispatch table (L22-27) does not specify case sensitivity. If one implementation is case-insensitive, `/conversus Run` might match the subcommand; under functional-typing's exact-match rule, it would fall through to config path routing.

My review did not flag dispatch precedence at all -- I focused on what happens after routing, not during it. But functional-typing's proposed rule, while addressing a real ambiguity, introduces a new class of silent misrouting that neither review accounts for. The safer rule is the one already in SKILL.md L31-32: unknown subcommands produce an error. Falling through to `run` is convenient but masks mistakes.

### 3. We both understate the severity of the [CLARIFY:] enforcement gap -- but in opposite directions

I flagged the `[CLARIFY:]` gate as my P1 recommendation: "Add [CLARIFY:] gate to spec 008." functional-typing flagged empty-section handling (Recommendation 5, P2) and the `[CLARIFY:]` tag syntax (Alignment section), but did not recommend enforcing `[CLARIFY:]` tags at consumption boundaries. functional-typing treats the tags as a schema feature to be more thorough; I treat them as a contract enforcement problem.

The contradiction: functional-typing's Recommendation 5 says that when Constraints or Success Criteria are empty, the system should insert `[CLARIFY:]` tags. This is the right instinct -- it increases the surface area of structured ambiguity marking. But functional-typing simultaneously praises the `[CLARIFY:]` system as "character-for-character identical to the spec's schema" (Alignment, point 4) without questioning whether anyone downstream will act on those tags. More `[CLARIFY:]` tags is only better if someone reads them. If spec 008 ignores them (which it currently does -- my Off-Base Assumption 1), then functional-typing's recommendation to add more tags to more sections increases the amount of ignored structured data, not the quality of the output.

We need to reconcile: either `[CLARIFY:]` tags are advisory decorations (functional-typing's implicit model) or they are machine-parseable contracts that downstream consumers must enforce (my explicit model). Both positions are defensible. The dangerous contradiction is holding both simultaneously.

---

## Tensions

### 1. Completeness vs. simplicity in the dispatch table

functional-typing recommends adding dispatch precedence rules, error message improvements with Levenshtein suggestions, frontmatter change acknowledgment, and a Baseline Features inventory entry (Recommendations 1, 3, 7). These are all structurally sound additions. But collectively they transform the dispatch table from a 6-line routing mechanism into a subsystem with matching semantics, error heuristics, metadata contracts, and a feature registry.

My review did not flag the dispatch mechanism at all because I found it adequate for its purpose -- minimal routing infrastructure that gets out of the way. The tension is genuine: functional-typing's completionism makes the dispatch table more robust but also more complex than the `define` handler it routes to. The dispatch section would grow from 17 lines (L18-34) to approximately 30-35 lines, rivaling the define handler's Input section (L774-784) in length. A routing table should not be more complex than what it routes to.

This tension does not have a clean resolution. functional-typing is right that ambiguities exist; I am right that addressing every ambiguity in a routing table over-engineers the simplest part of the system.

### 2. Schema rigidity vs. taxonomy openness

functional-typing's Off-Base Assumption 2 questions whether `problem.md` sections are always populatable. My Off-Base Assumption 2 questions whether the four problem types are exhaustive. These are the same concern expressed at different levels of the schema: functional-typing worries about empty fields within the existing structure; I worry about missing categories in the type system.

functional-typing's fix (Recommendation 5) is additive: more `[CLARIFY:]` tags for more sections. My fix (Recommendation 4) is meta: acknowledge the taxonomy's closure as a design decision. The tension is that functional-typing's approach keeps the schema rigid and handles edge cases with tags, while my approach suggests the schema might need to flex. These pull in opposite directions. If we follow functional-typing and add `[CLARIFY:]` tags everywhere, we are saying "the schema is correct; the data is incomplete." If we follow my recommendation, we are saying "the schema might be wrong; the structure is incomplete." The spec cannot hold both positions simultaneously for the same artifact.

My recommendation: adopt functional-typing's approach for field-level gaps (empty Constraints, empty Success Criteria) and my approach for structural-level gaps (the type taxonomy). These are different kinds of incompleteness and deserve different mechanisms.

### 3. Single-agent declaration vs. implicit architecture

functional-typing recommends explicitly stating that `define` is a single-agent command (Recommendation 6, P2). My review did not flag this -- I implicitly accepted it by noting that the interactive fallback (FR-012) requires "synchronous user-input" in the orchestrator, which only makes sense for a single-agent model.

The tension: functional-typing wants to prevent over-engineering by making the execution model explicit. But adding "No subagents are launched" to the `define` handler creates a constraint that may be premature. What if a future iteration of `define` wants to launch a research agent to scan a large context directory? What if `--context` points to a 50-file directory and the orchestrator cannot process them all within its context window? The single-agent declaration solves today's problem (preventing implementers from adding unnecessary complexity) but may constrain tomorrow's solution. functional-typing's own review notes the lack of complexity bounds on `problem.md` -- one natural response to unbounded complexity is delegation, which the single-agent declaration would prohibit.

This is a genuine design tension, not a clear error. I lean toward functional-typing's recommendation because the current spec is simple and should be kept simple, but the declaration should be worded as a current constraint, not an architectural principle: "In this spec, the define command executes in the main conversation" rather than "No subagents are launched" as a permanent rule.

### 4. functional-typing's anchor-breakage concern vs. the self-contained system claim

functional-typing's Off-Base Assumption 1 notes that the heading renames (`Input` to `Run: Input`, `Execution` to `Run: Execution`) break existing anchor links (`#input`, `#execution`), then immediately softens this by saying "the SKILL.md is self-contained." My review did not flag this at all.

The tension is with functional-typing's own Recommendation 3 (acknowledge frontmatter changes). If SKILL.md is self-contained and external links do not matter, then the frontmatter change is also cosmetic -- agent runtimes that discover the skill via frontmatter are external consumers, the same kind functional-typing dismissed for anchor links. Either external consumers matter (in which case both the anchor and frontmatter changes are significant) or they do not (in which case neither needs acknowledgment). functional-typing cannot simultaneously argue that anchor breakage is irrelevant because the file is self-contained and that frontmatter changes must be documented because external runtimes consume them.

---

## Safe Agreements

### 1. The dispatch mechanism is structurally sound

functional-typing: "The dispatch table (L22-27) routes all four cases specified by FR-001 through FR-004" (Alignment). My review: "The dispatch mechanism is clean and minimal -- a routing table in SKILL.md, backward-compatible defaulting to `run`, and a clear error for unknown subcommands" (Executive Summary). Both reviews find the dispatch table correct and complete for its stated requirements. No disagreement here.

### 2. The run path is behaviorally unchanged

functional-typing: "All content beneath these headings is untouched -- Step 1 through Step 5, template variables, phase execution, arbitration, dispute parsing, and the report format are identical to their pre-dispatch state" (Alignment, point 3). My review: "FR-003 defaults no-argument invocation to `run`, and constraint C2 (L88) explicitly gates the dispatch as additive-only" (Alignment, point 1). Both reviews confirm that the run path is preserved. This is the spec's most important constraint and it holds.

### 3. Schema fidelity between spec and SKILL.md

functional-typing: "The `problem.md` schema in SKILL.md (L824-850) is character-for-character identical to the spec's schema (spec L45-71)" (Alignment, point 4). My review did not independently verify character-for-character fidelity but accepted the schema as matching (Alignment, point 4 references the same taxonomy). No contradictions in the schema itself.

### 4. Context path validation is missing and needed

functional-typing: Recommendation 2 (P1), "Add `--context` path validation to define handler." My review: Recommendation 7 (P2), "Validate `--context` paths before ingestion." Same finding, same fix, same rationale (mirror the `run` engine's validation at SKILL.md L195-196). I rated it P2; functional-typing rated it P1. The priority difference is minor -- both agree the gap exists and must be closed.

### 5. The existing-file safeguard (FR-011) is correctly specified

functional-typing implicitly endorses FR-011 by not flagging it. My review explicitly praises it: "This matches the pattern established by spec 008's FR-005 and FR-012 for `interests.md` and `conversus.yml` respectively" (Alignment, point 5). Both reviews find the overwrite protection adequate as specified.

---

## Summary for Reconciliation

The most consequential disagreement is on `[CLARIFY:]` tag enforcement. functional-typing treats tags as a schema-level concern (add more tags to more sections); I treat them as a contract-level concern (downstream consumers must enforce them). Both positions need reconciliation before spec 008 is finalized, because that spec is the first consumer of `problem.md`.

The dispatch precedence rule (functional-typing Recommendation 1) needs further scrutiny. The proposed fall-through-to-`run` behavior is convenient but introduces silent misrouting risks that the current error-on-unknown behavior avoids. This is not a safe default to adopt without analyzing future subcommand name collisions.

The shared validation layer question (neither review flagged this directly) is an architectural concern that will compound across specs 008-011. If we are going to recommend path validation for `define`, we should recommend it once in the dispatch layer, not per-handler.

Everything else is reconcilable through editorial refinement. The reviews are more aligned than not -- the disagreements are about severity and mechanism, not about what the problems are.

### Referenced Documentation

- functional-typing review: `<HOME>/code/payer-index-mono/conversus/specs/007-subcommand-dispatch-define/conversus-review/functional-typing/review.md`
- devils-advocate review: `<HOME>/code/payer-index-mono/conversus/specs/007-subcommand-dispatch-define/conversus-review/devils-advocate/review.md`
- Spec: `<HOME>/code/payer-index-mono/conversus/specs/007-subcommand-dispatch-define/spec.md`
- SKILL.md: `<HOME>/code/payer-index-mono/conversus/SKILL.md`
