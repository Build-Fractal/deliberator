# Final Disputes — functional-typing

**Reviewer**: functional-typing (structural correctness & specification compliance)
**Phase**: 4 — Final Disputes and Convergence
**Date**: 2026-03-22

---

## Remaining Disputes

### Dispute 1: `[CLARIFY:]` tags MUST remain advisory within spec 007 — contra integration-architect's `## Status` section

Integration-architect's New Recommendation 1 (revision.md, "Add `[CLARIFY:]` gate status to problem.md," P1) proposes adding a `## Status` section to `problem.md` with values `draft` or `ready` that downstream consumers check as a gate. Devils-advocate's revised Recommendation 1 (revision.md L17) endorses this mechanism, stating the producer sets `status: draft` when any `[CLARIFY:]` tag exists.

I dispute both the priority and the mechanism. The `problem.md` schema at SKILL.md L822-850 defines seven required sections. Adding an eighth (`## Status`) is a schema expansion that spec 007 does not motivate. FR-010 (spec.md L39) says ambiguities "MUST be marked with `[CLARIFY: ...]` tags for the user to resolve before proceeding." The tags themselves are the signaling mechanism; a redundant `## Status` field that mechanically derives its value from tag presence adds no information. Any consumer that can read `## Status` can equally scan for `[CLARIFY:]` tags -- the tags are grep-able by design.

More critically, gate enforcement is a consumer-side decision. Whether `/conversus interests` treats `[CLARIFY:]` tags as blocking is a spec 008 question, not a spec 007 question. Embedding a gate status in the producer's output prescribes consumer behavior from the wrong spec. My Recommendation B (revision.md L131-141) already addresses this: "`[CLARIFY:]` tags are advisory markers indicating fields that benefit from user review. The `define` command writes the file regardless of how many `[CLARIFY:]` tags are present. Whether downstream commands enforce these tags as gates is defined by those commands' own specifications." This is the structurally correct boundary.

If a gate mechanism is needed, it belongs in spec 008 where the consumer is defined. Spec 007 should not grow the schema to solve a problem that does not yet exist.

### Dispute 2: Multiple `--context` paths belong in a follow-up spec, not spec 007

Devils-advocate's Recommendation 5 (revision.md L65-73) maintains that `--context` should accept multiple paths, now at P2, with integration-architect's data-integrity framing (stale copies from workaround copying). Integration-architect withdrew this recommendation in their revision (Recommendation 3, revision.md L26-31), explicitly agreeing with my conservative position: "functional-typing's conservative reading is appropriate for spec 007's scope."

I maintain my position from my revision (Recommendation 8, revision.md L105-112). SKILL.md L778 specifies `--context path/to/spec.md` -- singular path, singular usage example. The spec (spec.md L35, FR-006) says "`/conversus define --context <path>` MUST read context documents" -- `<path>` is singular. Extending the interface to accept repeated flags is a feature addition that no FR motivates. The workaround (point `--context` at a directory) is explicitly supported at SKILL.md L797-798: "path may be a file or directory." A directory containing multiple documents is the intended multi-source mechanism.

Devils-advocate's data-integrity argument (users copy files into a temp directory, creating stale duplicates) is a usage-pattern concern, not a specification gap. The correct response is a follow-up spec that adds multi-path support with proper semantics (ordering, deduplication, conflict resolution), not a P2 bolt-on to spec 007 that expands the interface without evaluating these interactions.

### Dispute 3: `--force` and `--dry-run` flags are pre-investment that spec 007 should not carry

Devils-advocate's Recommendation 6 (revision.md L77-87) maintains `--force` and `--dry-run` at P2, citing spec 011's gate automation. Integration-architect's cross-review acknowledged the danger of `--force` in interactive contexts (habitual use silently destroys refined `problem.md` files). Devils-advocate concedes the urgency concern but maintains the recommendation because "spec 011 is already on the roadmap."

I dispute inclusion in spec 007. The spec's Constraint 1 (spec.md L87) states: "Must NOT require coding knowledge to use. Plain-language descriptions are the input." Both `--force` and `--dry-run` are automation-facing flags that add cognitive surface area for the non-expert user this spec targets. FR-011 (spec.md L40) already defines the interactive safeguard: "the agent MUST present it and ask whether to refine or replace." Adding `--force` to bypass this safeguard and `--dry-run` to preview it adds two flags, two documentation requirements, and two interaction paths -- all for a use case (scripted/automated invocation) that does not exist yet.

The "spec 011 is on the roadmap" argument is speculative coupling. Spec 011 can add these flags when it defines the automation context that motivates them. Spec 007 should define the minimal viable interface for its stated audience: non-expert human users doing interactive problem definition.

---

## Convergence

### Convergence 1: Post-write schema validation for `problem.md` is a P1 gap

All three reviewers converge on this finding. Integration-architect's Recommendation 1 (revision.md L5-13) identified the gap. My New Recommendation A (revision.md L117-128) adopted it. Devils-advocate's revised Recommendation 2 (revision.md L27-35) concurs that producer-side validation is the primary mechanism. The specific validation target is also agreed: all seven required headings (`# Problem Definition`, `## Decision`, `## Type`, `## Context`, `## Constraints`, `## Success Criteria`, `## Open Questions`, `## Source Documents`) must be verified after the agent writes `problem.md`. This mirrors the engine's Phase 6 output validation pattern at SKILL.md L659-676 and is the single most important structural addition to spec 007.

### Convergence 2: `--context` path validation is P1

All three reviewers independently identified this gap and converged on P1. My Recommendation 2 (revision.md L27-36), integration-architect's Recommendation 8 (revision.md L65-71), and devils-advocate's Recommendation 7 (revision.md L92-99) all cite the same structural asymmetry: the `run` handler validates all paths at SKILL.md L195-196, but the `define` handler performs no path validation for `--context`. The proposed fix is identical across all three reviews: fail with "Context path does not exist: {path}" if the path does not exist, mirroring L195-196. This is a settled point.

### Convergence 3: Dispatch matching is exact and case-sensitive; the error path at L31-32 is correct

All three reviewers agree that the error-on-unknown behavior at SKILL.md L31-32 is the correct default. My revised Recommendation 1 (revision.md L11-22) withdrew the fallback-to-`run` proposal after both integration-architect and devils-advocate demonstrated the typo masking and forward-compatibility risks. Integration-architect's New Recommendation 3 (revision.md L96-100) and my revised position agree on the resolution: the spec should explicitly state that subcommand matching is exact and case-sensitive, and that the dispatch table is exhaustive. The only minor difference is in suggested error message enhancement (integration-architect proposes a "Did you mean" suggestion), which is an implementation detail, not a structural disagreement.

### Convergence 4: `define` executes in the main conversation with no subagents (version-scoped)

Integration-architect's Recommendation 7 (revision.md L57-63, upgraded to P2) and my Recommendation 6 (revision.md L81-93) converge on both the substance and the wording. Devils-advocate did not contest this point. The agreed formulation is: "In this version, the define command executes in the main conversation. No subagents are launched." The phrase "In this version" scopes the constraint without prohibiting future evolution, addressing devils-advocate's forward-compatibility concern.

### Convergence 5: Empty-section `[CLARIFY:]` coverage for Constraints and Success Criteria

Integration-architect's New Recommendation 2 (revision.md L90-94) and my Recommendation 5 (revision.md L63-77) agree that SKILL.md L854 must be extended to cover Constraints and Success Criteria, not just Source Documents and Open Questions. FR-010 at SKILL.md L852 establishes the universal rule; L854 only enumerates two sections. The gap is a simple omission. Devils-advocate's concern about interaction with downstream gates (revision.md L15-19) is addressed by my Recommendation B (advisory scoping) and does not block this addition.

---

## Final Position Statement

### Non-Negotiables

1. **Post-write schema validation for `problem.md`** (my New Recommendation A, P1). The `define` handler uses LLM generation, not template filling. Structural conformance of the output to the seven-heading schema at SKILL.md L822-850 is not guaranteed without explicit validation. The engine validates its outputs at L659-676. The `define` handler must do the same. This is the single highest-priority addition to spec 007.

2. **`--context` path validation before ingestion** (my Recommendation 2, P1). The `run` handler validates paths at SKILL.md L195-196. The `define` handler must validate `--context` paths with the same discipline. A missing context path silently degrades `problem.md` quality with no visible signal. This is a structural consistency requirement within SKILL.md.

3. **Dispatch matching semantics must be explicit** (my revised Recommendation 1, P1). SKILL.md L31-32 defines the error behavior but not the matching behavior. The spec must state that matching is exact and case-sensitive. Without this, the dispatch table is ambiguous on whether prefix matching, case-insensitive matching, or fuzzy matching is permitted. This is a one-sentence addition that closes a routing correctness gap.

4. **`[CLARIFY:]` tags are advisory within spec 007's scope** (my Recommendation B, P2). The `define` command writes `problem.md` regardless of tag count. Gate enforcement is a consumer-side decision belonging to spec 008. Adding a `## Status` section to the schema is unnecessary schema expansion that prescribes consumer behavior from the wrong spec. I will not accept a `## Status` field in the `problem.md` schema defined by spec 007.

### Flexibility

1. **Refine semantics**: I accept integration-architect's revised minimal contract (revision.md L16-23) -- all headings preserved, no silent deletion, Source Documents unioned, Type re-evaluated. This is appropriately scoped: bounded but not falsely deterministic. I have no competing recommendation on this topic and defer to integration-architect's formulation.

2. **Staleness tracking**: Devils-advocate's Recommendation 3 (revision.md L39-47) on content-hash-based staleness tracking between `problem.md` and `interests.md` is a reasonable P2 addition. I neither endorse nor contest it -- it is an integration concern that falls squarely in integration-architect's domain and can be resolved between them.

3. **Taxonomy closure design note**: Devils-advocate's revised Recommendation 4 (revision.md L51-61) correctly resolves the self-contradiction in the original formulation. The revised text ("This taxonomy is intentionally closed. Each type maps to a specific mode in `/conversus interests`. Extending this taxonomy requires a companion update to the mode mapping in spec 008.") is structurally sound. I accept this as a P2 documentation addition.

4. **Shared validation layer**: Devils-advocate's New Recommendation 1 (revision.md L129-138) proposing shared path validation in the dispatch layer is architecturally correct as a medium-term goal. For spec 007, per-handler validation (mirroring L195-196 in the `define` handler) is the pragmatic fix. Whether to plant the seed for shared utilities now or defer to a later spec is a scoping decision I am flexible on. The validation must exist in some form; the location is negotiable.

5. **`--output` directory creation**: My Recommendation 4 (revision.md L53-59) on creating the output directory if it does not exist is uncontested and straightforward. I am flexible on the exact error message wording.

6. **Single `--context` path documentation**: My Recommendation 8 (revision.md L105-112) is a documentation clarification, not a structural change. I am flexible on exact wording as long as the spec does not silently imply multi-path support that does not exist.
