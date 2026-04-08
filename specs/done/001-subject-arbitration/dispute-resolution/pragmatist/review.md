# The Pragmatist Review: 001-Subject-Arbitration Blockers

**Agent**: The Pragmatist
**Date**: 2026-03-19
**Disposition**: Ship v1 with minimum viable contracts, iterate from real usage

---

## Blocker 1: "Dispute entry" definition

**Position**: Option B -- content-negative (any non-whitespace, non-HTML-comment content).

**Rationale**:

The structural markers exist precisely to decouple trigger evaluation from Markdown formatting. Option A (pattern-matching `**Dispute:**`) defeats that purpose -- it makes the primary mechanism functionally identical to the fallback, which means the markers add complexity without adding capability. You built a new trigger surface and then evaluated it with the old trigger's logic. That is wasted architecture.

The false-positive concern is real but recoverable. If the markers contain stray template artifacts that trip the trigger, Phase 6 runs unnecessarily. The arbiter reads the disputes, finds nothing actionable, and produces an endorsement-style output or flags "UNRESOLVED -- no actionable disputes found." The cost is one extra agent invocation. Compare that to the false-negative cost of Option A: a formatting deviation in the Phase 5 template (the synthesizer writes `**Remaining dispute:**` instead of `**Dispute:**`) silently suppresses Phase 6. Disputes go unresolved. Nobody notices until downstream.

The asymmetry is clear. False positives cost one agent call. False negatives cost silent dispute loss. FR-012 already encodes this philosophy: "default to true as a safety measure -- better to run the arbiter unnecessarily than to skip it when disputes exist." Option B is the consistent extension of FR-012's design intent.

The 2:1 split (gh-aw + spec-kit favoring content-negative) reflects this same reasoning from two independent perspectives.

**Evidence**:

- FR-012 already defaults to `true` on parse failure, establishing the "err toward running" principle.
- The v2 synthesis explicitly frames this as "strictness-vs-decoupling" and notes the markers were introduced to decouple from prose formatting (v1 convergence point 5).
- gh-aw's argument is decisive: "A false-positive trigger surfaces a Phase 5 template bug rather than silently swallowing it."

**Spec text**:

Add to FR-011 after "checks whether at least one dispute entry exists within that range":

> A "dispute entry" is any line between the structural markers that contains non-whitespace content and is not an HTML comment (`<!-- ... -->`). This definition intentionally decouples the primary trigger mechanism from Markdown formatting conventions. If the markers contain non-dispute content (template artifacts, preamble text), Phase 6 runs and the arbiter evaluates the content -- the cost of a false-positive trigger is one agent invocation, which is strictly preferable to a false-negative that silently suppresses dispute resolution.

---

## Blocker 2: Structured output -- normative weight for v1

**Position**: Option B -- headings + prose conventions as SHOULD-level template instructions.

**Rationale**:

This is where I break from the "defer everything" instinct. Options A and C both punt the structured output question entirely to v2. Option B (spec-kit's hybrid) puts lightweight prose conventions (`**Dispute:**`, `**Ruling:**`, `**Grounding:**`, `**Required Changes:**`) into the template as SHOULD-level guidance.

The key insight: prose conventions are not structured output. They are template instructions. The template is the enforcement surface for LLM agents -- this is the central thesis of Blocker 4, and both gh-aw and spec-kit agree on it there. Prose conventions in the template are the lowest-cost way to get consistent arbiter output without building extraction machinery.

The risk of Option A (headings only) is that v1 arbiter output will be freeform prose under each FR-018 heading. When v2 extraction arrives, the training data from v1 runs will be inconsistent. You will spend v2 retrofitting extraction logic to handle the formatting entropy that v1 allowed. Prose conventions in the template cost zero implementation effort (they are instructions to the LLM, not code), constrain output just enough to be useful, and give v2 extraction a head start by establishing consistent patterns in real output.

gh-aw's concern about downstream tooling relying on prose conventions is valid but manageable. The SHOULD-level framing explicitly permits deviation. If an arbiter writes `**Decision:**` instead of `**Ruling:**`, that is fine -- the convention is guidance, not contract. The FR-018 section headings remain the MUST-level contract.

APM and gh-aw align on "headings only for v1" but their reasoning differs. APM wants a clean v1 contract. gh-aw worries about soft requirements hardening. The Pragmatist position: SHOULD-level template instructions are the right enforcement surface for LLM output shaping, they cost nothing to add, they improve output consistency, and they do not create contractual obligations. This is the definition of "minimum viable improvement."

**Evidence**:

- spec-kit's hybrid proposal originated from real arbitration experience where freeform prose under section headings was harder to consume than labeled entries.
- The template is already the enforcement surface for FR-015's six behavioral constraints -- adding labeled sub-field conventions is stylistically consistent with how the template already works.
- SHOULD-level language in RFC 2119 explicitly permits deviation: "there may exist valid reasons in particular circumstances to ignore a particular item."

**Spec text**:

Add to FR-015 after the six behavioral constraints:

> The template SHOULD instruct the arbiter to use labeled sub-fields within each Binding Decisions entry: `**Dispute:**` (reference to the dispute with Phase 4 citations), `**Ruling:**` (the binding decision), `**Grounding:**` (citation to the grounding document), `**Rejected Positions:**` (positions not adopted, with reasons), `**Required Changes:**` (concrete changes, citing target-document identifiers per FR-025 and specifying affected files per FR-026). These conventions are SHOULD-level template guidance to improve output consistency; the MUST-level v1 contract remains the FR-018 section headings.

Add a "Deferred: Structured Output" section in Implementation Guidance:

> The following fields are defined as advisory for future structured extraction: `dispute_id`, `ruling_type` (accept | reject | modify | unresolved), `grounding_citation`, `required_changes` (list), `affected_target_files` (list), `confidence_level`. Future versions SHOULD target these fields for machine extraction. The production mechanism is deferred.

---

## Blocker 3: Success criteria priority

**Position**: Option A -- P1 (missing SCs block implementation planning).

**Rationale**:

This is the easiest blocker. gh-aw's P2 argument is that FRs with RFC 2119 language are "implementable without SCs." Technically true. You can implement code without tests too. The question is not whether you *can* implement without SCs but whether you *should*.

FR-022 (failure semantics) is the sharpest example. The three-tier failure model is unanimously agreed, but without SCs, two implementors could disagree on the boundary between "structurally unintelligible" (tier 2, no file written) and "incomplete but parseable" (tier 3, file written with warning). The FR says "zero FR-018 section headings" is the bright-line test, but an SC would make the expected behavior unambiguous: "Given an arbiter output containing no FR-018 section headings, When validation runs, Then no resolution.md is written and a diagnostic warning is emitted."

FR-024 (citation boundary) is similar. Without an SC, how do you test that `docs` citations are never the sole basis for a ruling? The SC forces you to define the observable behavior: "Given a resolution.md where a binding decision cites only a `docs` entry, When validation runs, Then a warning is emitted."

The SCs are not bureaucratic overhead. They are the bridge between spec language and test cases. Writing them takes less time than the dispute about whether to write them.

The 2:1 split (APM + spec-kit favor P1) reflects the practical reality: specs without acceptance criteria produce implementation ambiguity.

**Evidence**:

- APM conceded to spec-kit's framing: "A spec without acceptance criteria for its requirements is incomplete by any consumption model."
- The v2 synthesis lists this as P1 item 3 in actionable spec changes.
- FR-022's three-tier model is unanimously agreed but relies on a bright-line test that only an SC can make testable.

**Spec text**:

Add to the Success Criteria section:

> **SC-008**: Given a Phase 6 agent that fails (timeout, crash, or zero FR-018 section headings in output), the engine does NOT write `resolution.md`, emits a diagnostic warning, and Phase 5 output is the terminal state.
>
> **SC-009**: Given a Phase 6 output containing at least one FR-018 section heading but missing others, the engine writes `resolution.md` and emits a validation warning listing the missing headings.
>
> **SC-010**: Given a binding decision in `resolution.md` that cites only a `docs` entry (not the `grounding` document), a post-hoc review or validation check flags the citation as non-authoritative.
>
> **SC-011**: Given an existing `resolution.md` from a previous Phase 6 run, re-running Phase 6 overwrites the file completely. No merge or append behavior.

---

## Blocker 4: Citation boundary enforcement surface

**Position**: Option C -- both spec-level FR and template-level instruction, but weighted toward the template.

**Rationale**:

This is not a close call. The arbiter is an LLM agent. It sees its prompt. It does not see the spec. FR-024 in the spec is a normative statement for human readers and implementors. The template instruction is the enforcement surface for the agent that actually makes citation decisions at runtime.

APM's concern about maintenance drift is valid in principle but negligible in practice. The template instruction is one sentence: "Only cite the grounding document ({GROUNDING_PATH}) as authority in binding decisions. Other docs provide context but are not authoritative." The template authoring contract already exists. Adding this as a sixth invariant keeps it in sync. The drift risk is one sentence in one file, cross-referenced by an existing maintenance mechanism.

APM's alternative -- extending FR-023 validation to check citation sources post-hoc -- is the more expensive option with lower effectiveness. Citation-source validation requires parsing prose to determine which document a citation refers to, which is an NLP problem, not a string-matching problem. An arbiter might write "as established in the architecture principles" without naming the file. Is that a grounding citation or a docs citation? Post-hoc validation cannot reliably answer this. A template instruction that says "only cite {GROUNDING_PATH} as authority" prevents the problem at the source.

The defense-in-depth model (Option C) is correct: FR-024 in the spec defines the rule. The template instruction enforces it at runtime. FR-023 validates output structure (headings), not citation sourcing -- and extending it to citation validation is a v2 concern at best. For v1, the template is sufficient.

**Evidence**:

- gh-aw's argument is the strongest in the entire dispute set: "The arbiter is an LLM agent that sees its prompt, not the spec. FR-024 in the spec is invisible at runtime."
- spec-kit endorses and extends: "The enforcement surface for an LLM agent is the prompt. One sentence in the template closes the gap at low cost."
- The template authoring contract (Implementation Guidance) already has four invariants. A fifth for citation boundary is structurally consistent.
- FR-023's current scope is section-heading validation. Extending it to citation-source validation is a fundamentally different capability that should not be conflated with structural validation.

**Spec text**:

Add to the template authoring contract invariants:

> 5. The template must instruct the arbiter that only the grounding document (`{GROUNDING_PATH}`) may be cited as authority in binding decisions. Other documents provided via `docs` may be referenced for factual context but must not serve as the sole basis for any ruling (per FR-024).

Add one sentence to FR-015, item 1 (after "Read the grounding document first"):

> The template MUST instruct the arbiter that only the grounding document may be cited as binding authority.

---

## Why My Approach Wins

The four blockers share a common structure: they are calibration disputes within a settled architecture. Nobody is arguing about whether Phase 6 should exist, how triggers work, or where templates live. The arguments are about strictness, normative weight, priority, and enforcement surface. These are pragmatic tradeoffs, not architectural decisions.

My resolutions follow three principles:

**1. Favor the recoverable error.** Blocker 1: false positives (extra agent call) over false negatives (silent dispute loss). Blocker 4: template instruction (prevents bad citations) over post-hoc validation (detects them after the fact). In both cases, the cheaper-to-recover option wins.

**2. The template is the enforcement surface.** LLM agents see prompts, not specs. Blockers 2 and 4 both turn on this insight. Prose conventions in the template (Blocker 2) shape arbiter output at zero implementation cost. Citation instructions in the template (Blocker 4) enforce the grounding boundary where it matters. The spec is for humans and implementors. The template is for the agent. Both matter, but the template is the runtime enforcement surface.

**3. Ship the minimum viable contract, then iterate.** Blocker 2: SHOULD-level prose conventions cost nothing and improve v1 output consistency without creating contractual debt. Blocker 3: SCs are cheap to write and expensive to skip. In both cases, the work is small, the benefit is real, and deferral creates more work later than doing it now.

Every resolution I propose is implementable today with text changes only -- no new code, no new mechanisms, no new abstractions. That is the Pragmatist's test: if the resolution requires architecture, it is not a calibration fix. All four of these are calibration fixes. Write the words, ship the spec, observe the output, iterate.
