# Cross-Review: Devil's Advocate Review of 007-subcommand-dispatch-define

**Reviewer**: integration-architect
**Reviewing**: devils-advocate Phase 1 review
**Grounded in**: spec.md, SKILL.md, integration-architect review

---

## Dangerous Contradictions

### 1. Schema validation: we agree on the problem but prescribe incompatible enforcement points

Devil's advocate (Rec #2) proposes consumer-side validation: "Any consumer of `problem.md` MUST validate these constraints before proceeding." My review (Rec #1) proposes producer-side validation: a post-write output validation step in the define handler itself, mirroring the engine's Phase 6 output validation pattern (SKILL.md L659-676).

These are not additive -- they conflict on where the contract is enforced. If the producer validates, a consumer receiving a `problem.md` can trust the schema by construction. If every consumer validates independently, each implements its own version of the rules, inviting divergence (e.g., `/conversus interests` might tolerate a missing `## Open Questions` while `/conversus mode` does not). The engine itself chose producer-side validation: template validation runs before any agent launches (SKILL.md L286-295), and Phase 6 output validation runs after the arbiter writes (SKILL.md L659). The engine never asks a downstream phase to re-validate a prior phase's output.

**Resolution**: Producer validates at write time. Consumer trusts the schema. If we also want consumer-side guards (belt-and-suspenders), those should be identical checks factored into a shared validation function, not independently specified in each consuming spec. Devil's advocate's formulation ("any consumer MUST validate") would distribute validation logic across specs 008, 009, and 010 -- that is an integration nightmare.

### 2. `[CLARIFY:]` tags: gate vs. advisory -- both reviews see the problem, but the fix locations conflict

Devil's advocate (Rec #1) proposes adding the `[CLARIFY:]` gate to spec 008: "If `problem.md` contains unresolved `[CLARIFY:]` tags, `/conversus interests` MUST present them and ask the user to resolve them before proceeding." My review did not flag this, but it has integration implications.

The devil's advocate correctly identifies that spec 007 produces `[CLARIFY:]` tags (SKILL.md L852) and spec 008 consumes `problem.md` unconditionally. The question is architectural: should the gate live in the consumer (spec 008) or the producer (spec 007)?

If `[CLARIFY:]` is a blocking gate, it belongs in the producer -- `define` should refuse to write `problem.md` with a "complete" status if clarifications remain, or it should write the file but set an explicit status marker (e.g., `status: draft` in frontmatter) that downstream consumers can check with a single field read. Placing the gate in every consumer (spec 008, spec 009, spec 010) means N separate implementations of the same check.

However, devil's advocate's "Off-Base Assumptions" section (first bullet) correctly notes that nothing in the current SKILL.md prevents a user from running `/conversus interests` immediately after `define`, ignoring the warning at SKILL.md L872-875. The warning is advisory, not blocking. This is genuinely dangerous.

**Resolution**: Both reviews converge on the risk. The implementation should add a `status: draft | ready` field to `problem.md` frontmatter. `define` sets `status: draft` when `[CLARIFY:]` tags exist. Downstream consumers check this single field. The gate logic is centralized in the artifact, not distributed across consumers.

---

## Tensions

### 1. Taxonomy closure: devil's advocate calls it a risk, my review is silent -- but the structural concern is valid

Devil's advocate (Rec #4, Off-Base Assumption #2) argues the four-type taxonomy is presented as exhaustive without justification, and that missing types (prioritization, migration, compliance) could mean missing mode pathways in spec 008. My review did not flag this because the define handler is self-contained and does not reference the mode matrix -- from a pure integration standpoint, the type field is a string that flows downstream.

But devil's advocate's point is load-bearing: spec 008's FR-007 maps types 1:1 to modes (devil's advocate cites 008 spec.md L44-52). If a user's problem is misclassified because the taxonomy is too narrow, the wrong mode is selected, and the entire deliberation runs with the wrong game-theory dynamics. The integration surface between `problem.md` and `conversus.yml` passes through the type field -- it is not cosmetic.

My review should have flagged this as an integration risk. Devil's advocate is right to surface it. The recommended fix (add a design note acknowledging the closure) is proportionate -- it does not require implementation changes, only documentation of intent.

**Tension**: My review focused on structural isolation and handler independence (noting that the define handler "references zero engine internals" at integration-architect review, Alignment bullet 3). This isolation is genuine, but it obscured the fact that the type field is a semantic coupling point even though there is no code-level coupling. Structural isolation is not semantic isolation.

### 2. `--force` and `--dry-run`: both reviews want them, but for different reasons

Devil's advocate (Rec #6) argues for `--force` and `--dry-run` to enable scripted/CI usage, citing spec 011's gate automation (011 spec.md L104-106). My review (Rec #2 in Missed Opportunities) argues for `--dry-run` to support iterative preview during manual usage, without mentioning `--force`.

The tension: devil's advocate frames these flags as necessary for automation composability, while I framed `--dry-run` as a user-experience convenience. The automation argument is stronger because it identifies a hard failure mode (interactive prompts blocking CI pipelines). The UX argument is a soft improvement. However, `--force` in an interactive context is dangerous -- a user who habitually passes `--force` will silently destroy a refined `problem.md` without the protection that FR-011's overwrite check provides (SKILL.md L786-793).

**Tension**: Both flags should exist, but `--force` should be documented as intended for non-interactive contexts only. The spec should note that `--force` bypasses the existing-file safeguard, and that interactive users should prefer the refine/replace prompt.

### 3. Staleness tracking: devil's advocate identifies a gap my review missed entirely

Devil's advocate (Rec #3) notes that spec 008's FR-013 tracks staleness between `interests.md` and `conversus.yml` (008 spec.md L59) but no equivalent exists between `problem.md` and `interests.md`. My review does not mention staleness at all.

This is a real integration gap. If a user edits `problem.md` after running `/conversus interests`, the interests are derived from a stale problem definition. The devil's advocate's proposed fix (a `## Generated From` section with path and timestamp) is lightweight and follows the pattern already established in spec 008.

However, the proposed mechanism (modification timestamp comparison) is fragile. File modification timestamps change on `touch`, copy, or backup restoration without content changes. A content hash (e.g., SHA-256 of `problem.md`) would be more robust. This is the same philosophy behind the engine's deterministic hash patterns elsewhere in the platform.

**Tension**: We agree on the gap. I would strengthen the mechanism from timestamp to content hash.

### 4. Multiple `--context` paths: agreed, but the syntax matters

Both reviews independently identify the single-path limitation of `--context` (devil's advocate Rec #5; my review Rec #3 in Missed Opportunities). Both cite the engine's list-based `target:` support (SKILL.md L57-68) as precedent.

The tension is minor and syntactic: devil's advocate proposes repeated flags (`--context a --context b`), while I proposed either repeated flags or comma-separated (`--context a,b`). The repeated-flag pattern is more consistent with CLI conventions and avoids ambiguity with paths containing commas. This is a non-controversial alignment.

### 5. Context path validation: agreed, but my review deprioritized it

Devil's advocate (Rec #7) and my review (Rec #8) both call for validating `--context` paths before ingestion, both citing the engine's path validation at SKILL.md L195-196. Devil's advocate rates it P2; I rated it P3. Given that the engine applies this validation as part of its mandatory Step 1 (SKILL.md L192-222), and that a silent path resolution failure produces a `problem.md` missing critical domain constraints, P2 is the more appropriate priority. I underweighted this.

---

## Safe Agreements

### 1. Backward compatibility is correctly preserved

Both reviews confirm that the dispatch mechanism preserves existing `/conversus run` behavior. Devil's advocate (Alignment bullet 1) cites FR-003 and constraint C2 (spec.md L29, L88). My review (Alignment bullet 2) verified through git diff that only heading renames occurred and the engine body content is unchanged. SKILL.md L26 explicitly defaults no-argument invocation to `run`. No disagreement.

### 2. Handler isolation is clean and correct

My review (Alignment bullet 3) verified that the define handler (SKILL.md L769-877) references zero engine internals -- no template variables, no phase numbers, no mode logic, no Agent tool dispatch. Devil's advocate does not contest this. Both reviews treat the handler as self-contained. The define handler's tool usage (Read and Write only, no Agent) is consistent with its role as a single-agent command.

### 3. `[CLARIFY:]` tag mechanism is structurally sound but operationally unguarded

Devil's advocate (Alignment bullet 2) notes that `[CLARIFY:]` tags follow the same grep-friendly structural-marker pattern as `DISPUTES_BEGIN`/`DISPUTES_END` (SKILL.md L750-751). My review did not discuss the tag mechanism's design, but I agree with the pattern comparison. Both reviews agree the mechanism is well-designed but lacks operational enforcement downstream -- see Dangerous Contradiction #2 above.

### 4. Existing-file safeguard follows established patterns

Devil's advocate (Alignment bullet 5) notes that FR-011's overwrite protection matches the pattern in spec 008's FR-005 and FR-012. My review (FR-to-Implementation Mapping, FR-011) confirms the SKILL.md implementation at L786-793 faithfully implements the four-step check. Both reviews affirm this is correctly specified and implemented.

### 5. The spec is faithful to the implementation and vice versa

My review includes a complete FR-to-implementation mapping covering all 12 FRs and 5 success criteria, confirming each is satisfied. Devil's advocate's executive summary states "The SKILL.md implementation appears to match the spec's 12 FRs and 5 success criteria faithfully." No disagreement on completeness.

### 6. `problem.md` size should be bounded

Devil's advocate (Rec #9) proposes soft guidance limiting constraints to 5-10 items. My review does not address this directly, but it is consistent with my observation that the engine bounds complexity elsewhere (SKILL.md L213-214 limits rounds to 1-5, L197 requires at least 2 agents). Unbounded input artifacts are a context-window tax on every downstream consumer. The recommendation is low-priority but directionally correct.

### 7. Pipeline visibility is needed

My review (Rec #4) proposes adding a pipeline overview to the report section explaining the define-interests-mode progression. Devil's advocate does not explicitly propose this but notes in "Missed Opportunities" that spec 008 FR-001 reads `problem.md` unconditionally -- implicitly acknowledging that the pipeline relationship is underspecified. Both reviews agree the user needs to understand why they are running `define` and what comes next.

---

## Summary of Priority Alignment

| Topic | Devil's Advocate | Integration Architect | Agreed Priority |
|-------|-----------------|----------------------|-----------------|
| Schema validation | P1 (consumer-side) | P1 (producer-side) | P1, producer-side preferred |
| `[CLARIFY:]` gate enforcement | P1 (in spec 008) | Not flagged | P1, centralized in artifact |
| Refine semantics | Not flagged | P1 | P1, no disagreement |
| Staleness tracking | P2 | Not flagged | P2, with content hash |
| Multiple `--context` | P2 | P2 | P2 |
| `--force`/`--dry-run` | P2 | P2 (dry-run only) | P2 |
| Context path validation | P2 | P3 | P2 |
| Taxonomy closure note | P2 | Not flagged | P2 |
| Pipeline overview | Not explicit | P2 | P2 |
| Artifact size bounds | P3 | Not flagged | P3 |
