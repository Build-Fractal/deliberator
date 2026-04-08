# The Mechanist Review: 001-Subject-Arbitration Dispute Resolution

**Agent**: The Mechanist (operational/engine perspective)
**Date**: 2026-03-19
**Scope**: 4 blockers from `dispute-resolution/problem.md`
**Philosophy**: If a machine can't check it, it doesn't belong in the spec. Engine validation is the only reliable enforcement surface. False negatives are worse than false positives. LLM output is probabilistic prose.

---

## Blocker 1 — Dispute Entry Definition

### Position: Option B (content-negative)

Any non-whitespace content between `<!-- CONVERSUS:DISPUTES_BEGIN -->` and `<!-- CONVERSUS:DISPUTES_END -->` that is not an HTML comment constitutes a dispute entry.

### Rationale

The entire point of introducing structural HTML markers was to decouple the trigger mechanism from Markdown formatting. The v1 synthesis established this as convergence point 5: "Structural HTML markers for trigger evaluation." If the engine then pattern-matches `**Dispute:**` inside those markers, the markers are ceremonial -- the actual trigger is still a Markdown convention, identical to the fallback mechanism. Two mechanisms that test the same thing provide zero defense-in-depth.

The mechanist cares about one question: can the engine evaluate this deterministically? Both options are deterministic. The difference is what failure mode each selects for:

- **Pattern-match (Option A)** fails closed on formatting drift. If a Phase 5 synthesizer writes `**Unresolved:**` instead of `**Dispute:**`, the trigger evaluates to false. Disputes exist but Phase 6 does not run. This is a **false negative** -- the worst outcome in the spec's own terms, because FR-012 explicitly states: "better to run the arbiter unnecessarily than to skip it when disputes exist."
- **Content-negative (Option B)** fails open on template artifacts. If a Phase 5 template leaves a stale placeholder between markers, the trigger evaluates to true. Phase 6 runs unnecessarily. This is a **false positive** -- the arbiter reads the synthesis, finds no disputes, and produces an endorsement-mode output or a trivial resolution. The cost is one extra agent invocation. The benefit is that no real dispute is ever silently dropped.

FR-012 already codifies the spec's preference: default to `true` when parsing fails. Option B extends this principle to the primary mechanism. Option A contradicts it.

### Evidence from the Deliberation Record

The v2 synthesis records a 2:1 split favoring content-negative (gh-aw + spec-kit vs. APM). The synthesis characterizes the dispute as "strictness-vs-decoupling" and notes that spec-kit's argument is decisive on mechanism independence: "The structural markers exist to decouple evaluation from prose formatting; APM's pattern requirement re-couples them, making the primary mechanism functionally identical to the fallback."

Convergence point 3 (content-presence guard) already handles the whitespace-only edge case: markers containing only whitespace evaluate to false for `trigger: disputes_remain`. This means the content-negative definition is not "anything at all" -- it is "non-whitespace, non-comment content." The guard makes Option B precise enough to avoid the most obvious false-positive vector.

### Proposed Spec Text

Add to FR-011 after "checks whether at least one dispute entry exists within that range":

> A **dispute entry** is any line between the structural markers that contains non-whitespace content and is not an HTML comment (i.e., not matching `<!-- ... -->`). The engine does not interpret the formatting or semantics of dispute entries; it evaluates content presence only. This definition ensures the primary trigger mechanism is independent of Markdown prose conventions. The heading-based fallback, which does interpret Markdown formatting, remains as a degraded-mode alternative when markers are absent.

---

## Blocker 2 — Structured Output: Normative Weight for v1

### Position: Option A (headings only)

FR-018 section headings are the sole v1 output contract. No prose conventions. The advisory schema belongs in a standalone "Deferred: Structured Output" section with SHOULD-level language for v2 planning.

### Rationale

LLM output is probabilistic prose. This is the foundational constraint the mechanist refuses to ignore.

Adding SHOULD-level prose conventions (`**Dispute:**`, `**Ruling:**`, etc.) to the v1 template creates a contract the engine cannot validate. FR-023 validates section headings -- those are structural, deterministic, machine-checkable. Labeled sub-fields within a section are semantic content that would require either (a) regex matching on LLM prose, which is brittle and produces false validation signals, or (b) no validation at all, which means the SHOULD is unenforceable and therefore not a contract but a suggestion wearing a contract's clothes.

The mechanist's rule: if a machine can't check it, it doesn't belong in the spec as a normative requirement. Move it to implementation guidance where it correctly lives as a recommendation for template authors.

The practical risk of prose conventions is downstream coupling. spec-kit's own argument reveals this: they want prose conventions as "an intermediate step" toward structured extraction. But intermediate steps that cannot be validated become load-bearing assumptions that downstream tooling relies on without the engine guaranteeing them. When the engine eventually extracts structured data (v2), it will need to handle the full range of actual LLM output, not just the subset that happened to follow the SHOULD convention. Better to defer cleanly than to create a false contract.

### Evidence from the Deliberation Record

The v2 synthesis records a 2:1 alignment between APM and gh-aw on "section headings only for v1, advisory schema for v2." gh-aw's argument is directly mechanist: "Adding labeled sub-field conventions to FR-015 is a softer version of requiring structured output from the LLM and creates a dependency downstream tooling will rely on."

The v2 assessment classifies this dispute as deferrable: "Structured output schema normative weight (Dispute 2) -- all agents accept SHOULD-level advisory for v1." and "Prose conventions for Binding Decisions entries -- spec-kit's hybrid proposal can be evaluated after observing real arbiter output."

This last sentence is key. The spec itself recommends gathering empirical data before committing to prose conventions. The mechanist agrees: observe real arbiter output, measure adherence variance, then decide whether to formalize conventions or go straight to engine-side extraction.

### Proposed Spec Text

Move schema fields from Implementation Guidance to a new section:

> ## Deferred: Structured Output (v2)
>
> The following schema fields are defined for future structured extraction from arbitration output. They are advisory -- they guide template design and v2 planning but impose no v1 contract on arbiter output beyond the FR-018 section headings.
>
> | Field | Type | Description |
> |-------|------|-------------|
> | `dispute_id` | string | Identifier for the dispute being resolved |
> | `ruling_type` | enum | One of `accept`, `reject`, `modify`, `unresolved` |
> | `grounding_citation` | string | Specific principle/requirement cited from the grounding document |
> | `required_changes` | list | Concrete changes required |
> | `affected_target_files` | list | Which target files the changes apply to (per FR-026) |
> | `confidence_level` | string | Arbiter's confidence in the ruling |
>
> The production mechanism (arbiter-produced structured output, engine extraction from prose, or sidecar file) is deferred to v2. The v1 implementation SHOULD collect real arbiter output samples to inform the extraction strategy.

Remove any reference to prose conventions (`**Dispute:**`, `**Ruling:**`, etc.) from FR-015 and the template authoring contract. Template authors MAY use labeled sub-fields in their templates as instructional hints, but this is a template-author decision, not a spec-level contract.

---

## Blocker 3 — Success Criteria Priority

### Position: Option A (P1)

Missing success criteria are a spec-completeness defect that blocks implementation planning.

### Rationale

The mechanist operates the engine. The engine needs to know what "correct" looks like for every requirement it enforces. A requirement without success criteria is a requirement without a test. A requirement without a test is a requirement the engine cannot verify. A requirement the engine cannot verify is dead letter.

The argument that "FRs with RFC 2119 language are implementable without SCs" (gh-aw's P2 position) confuses implementability with verifiability. An implementor can write code that satisfies their interpretation of a MUST. But without an SC, a second implementor can write different code that satisfies their different interpretation. Both believe they are correct. Neither can prove it because the acceptance boundary was never specified.

This is exactly the scenario the conversus process is designed to prevent. The v2 deliberation surfaced this gap explicitly: "FR-022 through FR-027 have no corresponding SC entries." The synthesis says "the requirements exist but have no acceptance tests." Two of three agents classify this as P1. The mechanist's position is even stronger: without SCs, the engine has no specification for its own validation behavior. FR-022 says "diagnostic warning MUST be emitted" -- what does the test check? Output to stderr? A structured log entry? A return code? The SC defines this. Without it, the FR is a wish.

### Evidence from the Deliberation Record

APM concedes directly: "A spec without acceptance criteria for its requirements is incomplete by any consumption model." spec-kit's argument is the strongest in the record: "Without explicit SCs, independent implementors will produce incompatible failure behaviors. SCs are the bridge between normative language and test plans."

The synthesis itself classifies this as P1 item 3 in "Actionable Spec Changes" and lists it under "What does not block but should land before v1 ships." This is internally inconsistent -- if it's P1 but doesn't block, it's not really P1. The mechanist resolves this: it IS P1 and it DOES block, specifically because the engine validation behavior (FR-023) and failure semantics (FR-022) are untestable without SCs.

### Proposed Spec Text

Add to the Success Criteria section:

> - **SC-008**: When Phase 6 agent-process fails (timeout, crash) or produces structurally unintelligible output (zero FR-018 section headings), no `resolution.md` is written, Phase 5 output is the terminal state, and a diagnostic warning is emitted to the engine's warning channel. *(Validates FR-022.)*
> - **SC-009**: When Phase 6 produces output with at least one FR-018 section heading but missing others, `resolution.md` IS written and a validation warning is emitted identifying the missing headings. *(Validates FR-023.)*
> - **SC-010**: No binding decision in `resolution.md` cites a `docs` entry as the sole authority for a ruling. At least one `grounding` citation appears in every ruling's rationale. *(Validates FR-024.)*
> - **SC-011**: When binding decisions reference numbered requirements in target documents, they use the specific identifiers (e.g., FR-xxx) rather than vague references. *(Validates FR-025.)*
> - **SC-012**: When multiple target files exist, each binding decision's Required Changes specifies which file is affected. *(Validates FR-026.)*
> - **SC-013**: Re-running Phase 6 on an existing `resolution.md` overwrites the previous file completely. No merge, no append, no conflict. *(Validates FR-027.)*

---

## Blocker 4 — Citation Enforcement Surface

### Position: Option C (both), weighted toward engine validation

FR-024 in the spec defines the normative rule. The template includes a one-sentence instruction making the constraint visible to the arbiter agent. FR-023 validation scope is extended to check citation sources post-hoc. All three surfaces. But the engine validation is the only one that matters for correctness.

### Rationale

This blocker presents a false trichotomy. The real question is: which enforcement surface is reliable?

- **Spec-level (FR-024)**: Defines the rule. Necessary but not sufficient -- the arbiter LLM does not read the spec at runtime.
- **Template-level instruction**: Makes the rule visible to the arbiter. Useful but unreliable -- LLM agents do not deterministically follow instructions. A template instruction is a probability modifier, not an enforcement mechanism.
- **Engine validation (FR-023 extension)**: Checks the output after the fact. This is the only surface that is deterministic, machine-verifiable, and cannot be bypassed by LLM non-compliance.

The mechanist's hierarchy: define the rule in the spec (normative source of truth), hint the rule in the template (probabilistic compliance aid), validate the rule in the engine (deterministic enforcement). All three, but only the third is load-bearing.

gh-aw and spec-kit argue that "the arbiter is an LLM agent that sees its prompt, not the spec" and therefore the template is the enforcement surface. This is half right. The arbiter sees its prompt, so the template instruction increases the probability of compliance. But probability is not enforcement. If the arbiter cites a `docs` entry as sole authority despite the template instruction, what catches it? Only engine validation.

APM argues that restating spec requirements in templates creates maintenance drift. This concern is valid but manageable -- the template authoring contract already exists as the synchronization mechanism. One sentence is low-drift-risk. The real APM contribution is the insight that FR-023 validation should be extended, which is the mechanist's primary position.

The cost of Option C is minimal: one sentence in the template, one additional validation check in the engine. The benefit is defense-in-depth across all three surfaces, with the engine as the authoritative backstop.

### Evidence from the Deliberation Record

The 2:1 split (gh-aw + spec-kit for template enforcement, APM for engine validation) obscures a latent agreement: all three agents want the constraint enforced; they disagree on where. Option C resolves this by doing all three, which is what the synthesis's P2 item 15 already gestures at: "Acknowledge the hybrid enforcement model in the template authoring contract."

gh-aw's strongest argument -- "FR-023 validates headings, not citation sourcing -- there is no post-hoc catch" -- is a diagnosis, not a terminal conclusion. The fix is to extend FR-023, which is exactly what APM proposes. The mechanist takes gh-aw's diagnosis and APM's remedy and combines them with gh-aw's template instruction.

### Proposed Spec Text

Amend FR-023:

> **FR-023**: After Phase 6 completes, the engine MUST validate that `resolution.md` contains (a) the required section headings defined in FR-018, and (b) at least one citation referencing the `grounding` document in the Binding Decisions section. If heading validation fails, the engine MUST emit a warning flagging the malformed output. If citation validation fails, the engine MUST emit a separate warning: "Binding decisions may cite only the grounding document as authority (FR-024). Detected rulings without grounding citations." Malformed output MUST NOT be silently accepted, but the file MUST still be written (warnings are informational, not blocking).

Add to the template authoring contract invariants:

> - The template MUST include an instruction to the arbiter that only the `grounding` document may be cited as authority in binding decisions (per FR-024). `docs` entries may be cited for factual context but must not serve as the sole basis for a ruling.

Add one sentence to the arbitration template content (FR-015):

> Under item 1 ("Read the grounding document first"), append: "This is your sole citation authority for binding decisions. Other documents (`docs`) provide context only and must not serve as the sole basis for any ruling."

---

## Why My Approach Wins

The conversus engine is a state machine. It executes phases, validates output, and manages transitions. Every decision it makes must be deterministic. The four blockers are all, at bottom, questions about what the engine can reliably check and what it should do when checks fail.

**The mechanist philosophy produces the best conversus implementation because it aligns every spec decision with the engine's actual capabilities:**

1. **Dispute entry definition (content-negative)**: The engine can check "is there non-whitespace, non-comment content between these markers?" in one pass with zero knowledge of Markdown conventions. It cannot reliably check "does this line match a bold-label pattern the LLM was supposed to use?" without coupling the primary mechanism to the fallback and introducing false-negative risk that the spec itself says is the worst outcome.

2. **Structured output (headings only for v1)**: The engine can validate section headings deterministically. It cannot validate prose sub-field conventions without either brittle regex or no validation at all. An unenforceable SHOULD is worse than no SHOULD -- it creates false confidence. Defer to v2 when engine-side extraction makes the contract machine-checkable.

3. **Success criteria (P1)**: The engine needs to know what correct behavior looks like for every FR it enforces. Without SCs, the engine's own validation logic has no specification. This is not a documentation gap -- it is a correctness gap. Every FR that describes engine behavior (FR-022, FR-023, FR-024, FR-027) requires an SC before implementation can begin.

4. **Citation enforcement (all three surfaces, engine-weighted)**: The template instruction is a probability modifier. The spec text is a normative declaration. The engine validation is the only deterministic enforcement. All three should exist, but only the engine validation is load-bearing. When the LLM ignores the template instruction -- and it will, eventually -- the engine catches it.

The common thread: **the engine is the only actor in the system that behaves deterministically.** LLM agents are probabilistic. Template instructions are suggestions. Spec text is invisible at runtime. The mechanist builds every decision around what the engine can verify, because that is the only thing that is reliable. Specs that defer to LLM compliance are specs that hope. Specs that defer to engine validation are specs that enforce.

The conversus framework's own design reflects this: FR-012 defaults to running Phase 6 when parsing fails (trust the engine's safe default, not the LLM's output quality). FR-022 says Phase 5 is terminal when Phase 6 fails (trust the engine's state management, not the arbiter's output). FR-023 validates headings (trust what the engine can check). Every FR that works well in this spec works well because it defers to deterministic engine behavior. The mechanist simply applies this principle consistently to the four remaining blockers.
