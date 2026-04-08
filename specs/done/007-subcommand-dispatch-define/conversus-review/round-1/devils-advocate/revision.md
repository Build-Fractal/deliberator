# Revised Review: Devil's Advocate — 007-subcommand-dispatch-define

**Reviewer**: devils-advocate
**Revision iteration**: 1
**Basis**: Original review + cross-reviews from functional-typing and integration-architect

---

## Recommendation Dispositions

### Recommendation 1: Add [CLARIFY:] gate to spec 008 — MODIFIED

**Original**: Add a gate to spec 008 (or spec 007 section 2) requiring `/conversus interests` to present and resolve unresolved `[CLARIFY:]` tags before proceeding.

**Cross-review feedback**: Integration-architect proposed centralizing the gate in the artifact itself via a `status: draft | ready` field in `problem.md` frontmatter. Functional-typing warned that combining this gate with their Recommendation 5 (add `[CLARIFY:]` tags to empty sections) would transform vague inputs into artifacts that block all downstream progression -- a significant UX change neither review evaluated holistically.

**Revised position**: I withdraw the proposal to place the gate in spec 008's consumer logic. Integration-architect's centralized-in-the-artifact approach is architecturally cleaner: a `status: draft | ready` field in `problem.md` means every downstream consumer checks one field rather than scanning for `[CLARIFY:]` tag patterns independently. The producer (`define`) sets `status: draft` when any `[CLARIFY:]` tag exists; downstream consumers check the single field. This avoids the N-consumer enforcement problem I created.

However, I defend the core concern against functional-typing's softening. Functional-typing treats `[CLARIFY:]` tags as a schema-completeness feature. They are not -- they are the spec's only mechanism for signaling that the problem definition is unreliable. If downstream consumers ignore them, the guided workflow's promise to non-expert users is hollow. The UX concern functional-typing raises (vague inputs produce blocking artifacts) is real, but it is the *correct* behavior: a vague problem definition *should not* produce agents and interests without user intervention. The alternative is silently generating low-quality output, which is worse than asking the user to do more work.

**Priority**: P1 (unchanged). **Mechanism**: modified from consumer-side gate to producer-side status field.

---

### Recommendation 2: Define problem.md validation contract — MODIFIED

**Original**: Add explicit validation rules ("Decision must be exactly one sentence," etc.) enforced by any consumer of `problem.md`.

**Cross-review feedback**: Integration-architect identified a dangerous contradiction -- consumer-side validation distributes enforcement logic across specs 008, 009, and 010, inviting divergence. Their counter-proposal: producer-side validation at write time, mirroring the engine's Phase 6 output validation pattern (SKILL.md L659-676). Functional-typing noted that the schema contract already exists implicitly and raised a dual-validation concern: the spec would simultaneously tell the producer "write this schema" and consumers "validate this schema" without designating a single source of truth.

**Revised position**: I withdraw consumer-side enforcement as the primary mechanism. Integration-architect is right that distributing validation across consuming specs is an integration nightmare. The producer should validate at write time.

But I defend the need for consumer-side validation as a secondary check, contra integration-architect's "consumer trusts the schema" position. My cross-review of integration-architect made this case explicitly: producer-side validation catches agent generation errors, but post-write mutations are the real threat. The user manually edits `problem.md` to resolve `[CLARIFY:]` tags and accidentally deletes the `## Type` heading. Producer-side validation catches nothing at that point because it already ran. The solution is both: producer validates at write time (integration-architect's recommendation), and a shared validation function (not per-consumer reimplementation) runs at read time. If the spec mandates factoring validation into a single reusable check, both the dual-validation and the distribution problems are solved.

**Priority**: P1 (unchanged). **Mechanism**: modified from consumer-only to producer-primary with shared-function consumer guard.

---

### Recommendation 3: Add staleness tracking between problem.md and interests.md — MAINTAINED with mechanism refinement

**Original**: Add a `## Generated From` section to `interests.md` containing the path and modification timestamp of the `problem.md` used to generate it.

**Cross-review feedback**: Integration-architect agreed on the gap but proposed content hash (SHA-256) over modification timestamp, noting that timestamps change on `touch`, copy, or backup restoration without content changes.

**Revised position**: Integration-architect's hash-based mechanism is strictly superior. Timestamps are fragile; content hashes are deterministic. I adopt the refinement. The core recommendation -- that the staleness-detection pattern established in spec 008 (between `interests.md` and `conversus.yml`) must also apply at the `problem.md`-to-`interests.md` boundary -- survives without modification. The gap is real, the fix is lightweight, and the pattern already has precedent.

**Priority**: P2 (unchanged). **Mechanism**: content hash replaces timestamp.

---

### Recommendation 4: Acknowledge taxonomy closure as a design decision — MAINTAINED, narrowed

**Original**: Add a "Design Note" acknowledging that the four-type taxonomy is intentionally closed and may be extended in a future spec.

**Cross-review feedback**: Functional-typing flagged that my proposed text contradicts itself ("intentionally closed" but "may be extended") -- a structural contradiction. Integration-architect agreed the taxonomy is load-bearing (type maps 1:1 to mode in spec 008) and that my recommended design note is proportionate.

**Revised position**: Functional-typing's critique of my proposed language is valid. The Design Note should commit to one position. The correct position is closure: the taxonomy is closed *because* spec 008 maps types 1:1 to modes, and extending the taxonomy without a companion 008 update would break that mapping. The escape hatch is not "extend the taxonomy" but "bypass `define` and write `conversus.yml` directly."

Revised text: "This taxonomy is intentionally closed. Each type maps to a specific mode in `/conversus interests`. Problems that do not fit these types should be reframed in terms of the closest type, or users should bypass the guided workflow and configure `conversus.yml` directly. Extending this taxonomy requires a companion update to the mode mapping in spec 008."

**Priority**: P2 (unchanged). **Language**: revised to eliminate self-contradiction.

---

### Recommendation 5: Support multiple --context paths — MAINTAINED, priority elevated

**Original**: Allow `--context` to be specified multiple times for files in different directories. Priority P2.

**Cross-review feedback**: Integration-architect provided a stronger framing than I did: users will work around the single-path limitation by copying documents into a single directory, creating stale duplicates that drift from their sources. Both reviews converged on the repeated-flag syntax (`--context a --context b`) as preferable to comma-separated.

**Revised position**: Maintained. Integration-architect's data-integrity framing is more rigorous than my consistency argument. A user who copies three specs into a temp directory to satisfy a single-path constraint has created three stale copies that will never be updated. The limitation does not just inconvenience users -- it actively encourages practices that degrade input quality.

**Priority**: P2 (unchanged, but with stronger justification).

---

### Recommendation 6: Add --force and --dry-run flags to define — MAINTAINED with scope note

**Original**: Add `--force` (overwrite without asking) and `--dry-run` (print without writing) for scripted/automated usage, citing spec 011's gate automation.

**Cross-review feedback**: Functional-typing noted that spec 007 targets non-expert human users (spec L87) and the SKILL.md compatibility note (L11-13) scopes the runtime to conversational agents, making automation flags a pre-investment for a future spec. Integration-architect agreed both flags should exist but warned that `--force` in an interactive context is dangerous -- habitual `--force` silently destroys refined `problem.md` files.

**Revised position**: Maintained, with the scope refinement integration-architect suggests. Both flags serve legitimate purposes, but they serve different audiences. `--dry-run` is useful for both interactive and automated contexts (preview before committing). `--force` is specifically for non-interactive contexts (CI, gates, scripted pipelines) and should be documented as such. The spec should note: "`--force` bypasses the existing-file safeguard (FR-011) and is intended for non-interactive contexts. Interactive users should prefer the refine/replace prompt."

Functional-typing's counter-argument (this is pre-investment for a future spec) is a prioritization disagreement, not a factual one. I concede it is not urgent for spec 007 alone, but maintaining it at P2 because spec 011 is already on the roadmap.

**Priority**: P2 (unchanged).

---

### Recommendation 7: Validate --context paths before ingestion — MAINTAINED, priority elevated

**Original**: Fail with a clear error if `--context <path>` does not exist or is unreadable. Priority P2.

**Cross-review feedback**: All three reviews independently identified this gap. Functional-typing rated it P1 (structural completeness gap -- `define` omits validation that `run` requires). Integration-architect rated it P2 (upgrading from their initial P3). Both cite SKILL.md L195-196 as the pattern to follow.

**Revised position**: Maintained. Functional-typing's P1 rating is arguably correct -- the asymmetry between `run` (which validates paths at L195-196) and `define` (which does not) is a structural consistency gap within SKILL.md. However, I also accept my own cross-review observation that per-handler validation is a copy-paste pattern that scales linearly with subcommand count. The ideal fix is shared validation in the dispatch layer, but that is an architectural change beyond spec 007's scope. For this spec, mirroring the `run` handler's validation in `define` is the pragmatic fix.

**Priority**: elevated to P1. The consensus across all three reviews, plus the silent-failure mode (user gets a valid-looking `problem.md` missing critical constraints), justifies the upgrade.

---

### Recommendation 8: Document the escape hatch from the guided workflow — MAINTAINED

**Original**: Add guidance that users with an existing `conversus.yml` should use `/conversus run` directly; the guided workflow is optional.

**Cross-review feedback**: Not directly contested. Integration-architect's pipeline overview recommendation (their P2 #4) serves a related purpose, though my cross-review noted the pipeline overview risks being a "dead-end map" describing commands that do not yet exist.

**Revised position**: Maintained as written. The escape hatch documentation is simpler and less risky than a full pipeline overview -- it states what exists now rather than promising what will exist later. The two are not mutually exclusive, but the escape hatch should be implemented regardless of whether a pipeline overview is added.

**Priority**: P3 (unchanged).

---

### Recommendation 9: Constrain problem.md artifact size — MAINTAINED

**Original**: Add soft guidance limiting Constraints to 5-10 items, suggesting sub-problem decomposition for complex inputs.

**Cross-review feedback**: Integration-architect agreed the recommendation is directionally correct and consistent with the engine's bounded complexity pattern (SKILL.md L213-214). Not contested by functional-typing.

**Revised position**: Maintained as written. The recommendation is low-priority and advisory, but it addresses a real concern: every downstream consumer reads `problem.md` in full, and unbounded artifacts become a context-window tax on the entire pipeline. Soft guidance is proportionate to the risk.

**Priority**: P3 (unchanged).

---

## New Recommendations

### New Recommendation 1: Push shared path validation into the dispatch layer (Priority: P2)

**Source**: My cross-review of functional-typing identified that both reviews recommended per-handler path validation (my Rec #7, functional-typing's Rec #2) but neither addressed the architectural implication: if every handler independently replicates the `run` handler's validation discipline, the dispatch architecture has no shared validation layer. This scales linearly with subcommand count and guarantees inconsistency as each spec author reinvents the same checks.

**Proposed change**: Add a "Common Handler Utilities" subsection to the Subcommand Dispatch section of SKILL.md specifying shared validation operations (path existence, path readability, artifact schema checks) that any handler can invoke. For spec 007, this means the `define` handler calls the shared path validator rather than reimplementing it. Future handlers (interests, mode) use the same function.

**Rationale**: The CLAUDE.md base-integrator architecture pattern explicitly states "push shared validation into the base class so every integrator benefits." The same principle applies to subcommand handlers. Per-handler validation is a short-term pragmatic fix (my revised Rec #7); shared dispatch-layer validation is the correct medium-term architecture.

**Risk if ignored**: By spec 009, three handlers will have three independent path validation implementations. When one is updated (e.g., to support glob patterns or remote URLs), the others lag behind. This is exactly the integration drift that the dispatch architecture was designed to prevent.

---

### New Recommendation 2: Specify refine semantics as heuristic, not deterministic (Priority: P2)

**Source**: My cross-review of integration-architect challenged their P1 #2 (detailed merge semantics for the refine operation). Integration-architect proposed specific operations: replace the Decision, merge Constraints (deduplicated), merge Open Questions (remove resolved), re-evaluate Type. I argued these present heuristic operations as if they were deterministic algorithms.

**Proposed change**: Add to SKILL.md's refine step (L791): "Refine merges the new input with the existing `problem.md`. The agent uses judgment to update the Decision, merge or replace Constraints, resolve Open Questions answered by the new input, and re-evaluate the Type classification. The refine operation is inherently heuristic -- the spec defines the intent (incorporate new information while preserving prior refinements) but does not prescribe deterministic merge rules. The resulting `problem.md` must pass the same schema validation as a fresh definition."

**Rationale**: Natural-language constraints cannot be deduplicated algorithmically ("Must support 10,000 concurrent users" and "The system needs to handle 10K simultaneous connections" are semantic duplicates that no markdown parser can detect). Specifying merge rules as if they were deterministic creates false precision. The spec should bound acceptable variance rather than pretending the operation is mechanistic. The schema validation gate (Rec #2, revised) provides the structural guarantee; the merge semantics should be left to agent judgment within that constraint.

---

## Position Summary

After reading both cross-reviews and reconsidering my original positions, I withdraw two specific mechanisms while defending the underlying concerns they addressed. The `[CLARIFY:]` gate should be centralized in the artifact (via a `status: draft | ready` field) rather than distributed across consuming specs -- integration-architect's architecture is cleaner and avoids the N-consumer enforcement problem I created. The validation contract should be primarily producer-side with a shared validation function available to consumers, rather than mandating independent consumer-side validation that would distribute enforcement logic across specs 008-010. In both cases, the cross-reviews identified better solutions to problems I correctly diagnosed.

The strongest challenge to my review came from functional-typing's observation that my taxonomy-closure Design Note contradicted itself by declaring the taxonomy "intentionally closed" while simultaneously saying it "may be extended." This is a genuine logical flaw. The revised language commits to closure and names the prerequisite for extension (a companion spec 008 update), eliminating the contradiction. More broadly, functional-typing's structural precision exposed imprecision in my own recommendations -- a useful reminder that challenging assumptions requires the same rigor one demands of the assumptions being challenged.

The concerns that survive scrutiny intact are: the `[CLARIFY:]` enforcement gap (the mechanism is theater if no one acts on the tags), staleness tracking across the `problem.md`-to-`interests.md` boundary (the pattern exists at one boundary but not the other), and the need for `--force`/`--dry-run` flags to support the automated invocations spec 011 envisions. The cross-reviews strengthened the path validation recommendation (all three reviewers converged independently, elevating it from P2 to P1) and the multi-context-path recommendation (integration-architect's data-integrity framing is more compelling than my consistency argument). The most important new insight from the cross-review process is the shared validation layer problem: all three reviews recommended per-handler validation fixes without questioning whether per-handler validation is the right architecture. It is not, and spec 007 should plant the seed for shared dispatch-layer utilities even if the full implementation waits for a later spec.
