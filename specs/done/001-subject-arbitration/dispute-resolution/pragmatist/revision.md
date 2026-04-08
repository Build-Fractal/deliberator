# The Pragmatist: Revised Positions

**Agent**: The Pragmatist
**Date**: 2026-03-19
**Inputs**: Mechanist cross-review, Purist cross-review, own cross-reviews of both
**Method**: For each blocker, assess whether the cross-reviews exposed a genuine defect in my reasoning, a valid refinement, or a mischaracterization. Revise accordingly.

---

## Blocker 1: "Dispute entry" definition

**Original position**: Option B (content-negative)
**Revised position**: **Held**

### Assessment of cross-reviews

The Purist's DC-2 is the only serious challenge. The argument: a false-positive trigger does not cost "one agent call" -- it costs a vacuous `resolution.md` that passes validation, looks legitimate, and resolves nothing. The Purist calls this "camouflage" and argues it is worse than the false-negative case (no `resolution.md` at all), because absence is a signal while vacuity is silent.

This is the strongest argument against my position in the entire dispute set, and I need to engage with it honestly.

The Purist is correct that FR-022's three-tier failure model does not cover semantically vacuous output. A resolution that contains all FR-018 section headings but resolves zero disputes is tier 3 (incomplete but parseable) -- the engine writes the file and emits a warning for missing headings, but the headings are not missing. They are present and empty. This is a gap.

However, the Purist's argument proves too much. The vacuous-output problem exists regardless of the trigger definition. Even under Option A, a correctly formatted `**Dispute:** The parties could not agree on X` entry could trigger Phase 6, and the arbiter could produce a vacuous resolution for other reasons (confused by the grounding document, hallucinating consensus, or simply failing to engage). The vacuous-output problem is a Phase 6 output quality problem, not a trigger precision problem. Option A narrows the trigger input but does not address the output gap. The correct fix is an SC or FR-022 amendment that covers vacuous output -- not tightening the trigger definition to prevent one source of vacuous input while leaving every other source unaddressed.

The Mechanist's cross-review marks Blocker 1 as a safe agreement. Both the Mechanist and I selected Option B for the same reasons. The Purist stands alone on Option A.

The Purist's subsidiary argument -- that Option A makes the trigger "testable with a single regex" -- is true but irrelevant. Option B is also testable with a single predicate: `any(line.strip() and not line.strip().startswith('<!--') for line in marker_content)`. The predicate form differs; the testability does not.

**What I incorporate**: The Purist's vacuous-output concern is real and should be addressed, but as a new SC (vacuous resolution detection), not as a trigger definition change. I add this to my Blocker 3 position.

---

## Blocker 2: Structured output -- normative weight for v1

**Original position**: Option B (SHOULD-level prose conventions in the template)
**Revised position**: **Modified** -- retreat to Option A (headings only) with a narrower template-author recommendation

### Assessment of cross-reviews

Both the Mechanist and the Purist identified the same contradiction in my position, and they are right.

The Mechanist's DC-1 is precise: "Once the template tells the arbiter to use `**Ruling:**`, downstream consumers will expect `**Ruling:**` to appear. The developer who sees `**Ruling:**` in 95% of real output will write code that depends on it. When the LLM writes `**Decision:**` or `**Judgment:**` in the other 5%, that code breaks. The SHOULD did not protect them -- it lured them." This is correct. I dismissed gh-aw's downstream coupling concern too quickly. SHOULD-level language is read by spec authors, not by the developers who encounter the patterns in real output. The patterns harden into de facto contracts regardless of the spec's normative framing.

The Purist's DC-3 sharpens the knife further: "Either the SHOULD-level conventions produce consistent patterns (in which case they are functioning as de facto constraints and should be acknowledged as such), or they permit deviation freely (in which case they do not produce consistent patterns and the v2 benefit is illusory)." This is a clean dilemma and I was on the wrong side of it. I wanted the benefit of consistency without the cost of commitment. That is not a principled specification choice.

The Purist's T-1 is also fair: I claimed to ship the "minimum viable contract" while pre-specifying six labeled sub-fields and six deferred schema fields -- more specification than either Option A or the Purist's own Option C. I was doing purist work under a pragmatist banner. Acknowledged.

**What I concede**: Elevating prose conventions to spec-level SHOULD language creates an unenforceable pseudo-contract. The Mechanist is right that if the engine cannot validate it, it does not belong in the spec as a normative provision.

**What I retain**: The deferred structured output section with the schema fields. The Purist's activation condition ("when any downstream system declares a dependency on structured arbitration data") is a genuine contribution that no other agent proposed, and it transforms the deferral from aspirational to actionable. I adopt it.

**What I add**: Template authors MAY use labeled sub-fields as instructional hints in their templates. This is a template-author decision documented in Implementation Guidance, not a spec-level contract. This preserves the ability to shape LLM output without creating a normative obligation.

**Revised spec text**:

FR-018 section headings are the sole v1 output contract. Add a standalone deferred section:

> ### Deferred: Structured Output
>
> The following schema fields are defined as targets for future structured extraction from arbitration output. For v1, the output contract is FR-018 section headings only.
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
> **Activation condition**: Structured extraction becomes a P1 requirement when any downstream system (CI integration, automated change application, cross-conversus chaining) declares a dependency on machine-readable arbitration data. Until that trigger, the schema remains advisory.

Add to Implementation Guidance:

> Template authors MAY use labeled sub-fields (e.g., `**Dispute:**`, `**Ruling:**`, `**Grounding:**`, `**Required Changes:**`) as instructional hints to improve output regularity. This is a template-author design decision, not a spec-level contract. The engine does not validate sub-field presence or format.

---

## Blocker 3: Success criteria priority

**Original position**: Option A (P1, with SC-008 through SC-011)
**Revised position**: **Modified** -- expand SC coverage to six, adopt Given/When/Then format, add vacuous-output SC

### Assessment of cross-reviews

The Mechanist's tension note is constructive: my Given/When/Then format is stronger for test derivation, but my four SCs leave gaps that the Mechanist's six SCs cover (FR-025 requirement identifiers, FR-026 per-file attribution). The Mechanist is right: "If SCs are the bridge between spec language and test cases, the bridge should cross the entire river." My own principle -- that SCs are cheap to write and expensive to skip -- applies to the SCs I omitted.

The Purist's T-2 raises a real specificity question: my SCs say "diagnostic warning" without specifying the output channel, while the Purist's SCs specify stderr and exact report format strings. The Purist is correct that without a channel, the SC is not testable by CI. However, specifying stderr and exact format strings over-constrains implementation when the consumption model is not yet declared. I split the difference: specify the output channel (stderr or structured log, implementor's choice documented in engine configuration) but do not mandate exact format strings.

From Blocker 1's revision, I identified a gap: vacuous resolution output (valid structure, zero substantive content). This needs an SC.

**Revised spec text**:

> - **SC-008**: Given a Phase 6 agent that fails (timeout, crash, or output containing zero FR-018 section headings), When the engine processes the result, Then no `resolution.md` is written, Phase 5 output is the terminal state, and a diagnostic warning is emitted to the engine's warning channel identifying the failure reason.
>
> - **SC-009**: Given Phase 6 output containing at least one FR-018 section heading but missing others, When the engine validates the output, Then `resolution.md` is written and a validation warning is emitted listing the missing headings.
>
> - **SC-010**: Given a `resolution.md` where a binding decision cites only a `docs` entry (not the grounding document) as the basis for a ruling, When post-hoc validation or review is performed, Then the citation is flagged as non-authoritative. (Note: v1 validation MAY implement this as a string-presence heuristic for the grounding document path; full citation-source validation is a v2 concern.)
>
> - **SC-011**: Given binding decisions that reference requirements in target documents, When the decisions use vague references (e.g., "the validation requirement") instead of specific identifiers (e.g., "FR-003"), Then a validation warning is emitted.
>
> - **SC-012**: Given multiple target files in the conversus, When a binding decision's Required Changes section does not specify which file is affected, Then a validation warning is emitted for the unattributed entry.
>
> - **SC-013**: Given an existing `resolution.md` from a previous Phase 6 run, When Phase 6 runs again, Then the engine overwrites the file completely. No merge, no append, no conflict resolution, no confirmation prompt.
>
> - **SC-014**: Given a Phase 6 run triggered by a false-positive dispute predicate (markers contain non-dispute content), When the arbiter produces output with all FR-018 section headings but zero binding decisions in the Binding Decisions section, Then the engine writes `resolution.md` and emits a validation warning: "Arbitration produced zero binding decisions -- verify dispute trigger content."

SC-014 addresses the vacuous-output gap the Purist identified in Blocker 1. It does not prevent the vacuous output (the arbiter has already run) but it makes the condition detectable rather than silent. This closes the Purist's "camouflage" concern without changing the trigger definition.

---

## Blocker 4: Citation boundary enforcement surface

**Original position**: Option C (all three surfaces), weighted toward the template
**Revised position**: **Modified** -- Option C, rebalanced weighting

### Assessment of cross-reviews

The Mechanist's DC-2 is the sharpest challenge: "The Pragmatist diagnoses the failure mode correctly and then proposes the remedy that is vulnerable to exactly that failure mode." I said the arbiter might write "as established in the architecture principles" without naming the file, and used this to argue that engine validation is hard. The Mechanist correctly points out that under my template-weighted position, the template instruction is equally vulnerable to this exact failure -- the arbiter ignores the template instruction and cites a docs entry obliquely. The template instruction did not "prevent the problem at the source." It shifted the probability distribution. The Mechanist is right that "prevents" was the wrong word.

The Purist's DC-1 drives the same point: "A system that relies on a single probabilistic enforcement point for a constraint that the entire spec identifies as critical is a system designed to fail silently. That is the opposite of the Pragmatist's own Principle 1 ('favor the recoverable error')." This is a legitimate internal contradiction in my original position. I built my entire review around "favor the recoverable error" and then proposed a template-only enforcement for v1 citation boundaries that makes citation violations unrecoverable (undetectable without human review).

However, I do not fully concede to the Mechanist's engine-weighted position either. The Mechanist's proposed FR-023 extension checks for "at least one citation referencing the grounding document in the Binding Decisions section." This is a string-presence check -- does the grounding document path appear in the section? The Mechanist is right that this is cheap and feasible. But it is a necessary-condition check, not a sufficient-condition check. It catches the case where the grounding document is never mentioned (clear violation) but does not catch the case where the grounding document is mentioned once and a docs entry is cited as sole authority for a different ruling. The Mechanist's own DC-2 point -- that engine citation validation is also probabilistic for the hard cases -- remains true.

What I got wrong: dismissing FR-023 extension as "a v2 concern." The Mechanist and Purist are both right that a basic string-presence check for the grounding document path in Binding Decisions is cheap, deterministic, and catches the most egregious violation class. Deferring this to v2 when the cost is one string check was not pragmatic -- it was negligent. The Mechanist's word.

What I got right: the template instruction is still the primary shaping mechanism. The engine check is a backstop, not a replacement. Both matter.

**Revised weighting**: The template instruction is the primary prevention surface (it shapes the probability distribution at generation time). The engine check is the primary detection surface (it catches violations deterministically, at least for the grounding-path-presence class). Neither is sufficient alone. Implementation effort should flow to both: one sentence in the template (cheap), one string-presence check in the engine (cheap). The weighting question dissolves when both are cheap.

**Revised spec text**:

Add to the template authoring contract invariants:

> 5. The template MUST instruct the arbiter that only the grounding document (`{GROUNDING_PATH}`) may be cited as authority in binding decisions. Other documents provided via `docs` may be referenced for factual context but must not serve as the sole basis for any ruling (per FR-024).

Add one sentence to FR-015, item 1:

> The template MUST instruct the arbiter that only the grounding document may be cited as binding authority.

Amend FR-023:

> After Phase 6 completes, the engine MUST validate that `resolution.md` contains (a) the required section headings defined in FR-018, and (b) at least one reference to the grounding document path in the Binding Decisions section. If heading validation fails, the engine MUST emit a warning. If the grounding document path is absent from Binding Decisions, the engine MUST emit a separate warning: "No grounding document citation detected in Binding Decisions (FR-024)." Both warnings are informational -- the file is still written.

Note: This is a necessary-condition check (grounding path must appear), not a sufficient-condition check (it does not verify that every ruling cites the grounding document or that no ruling cites only a docs entry). Full citation-source validation is a v2 concern requiring semantic parsing. The v1 check catches the most egregious class of violation -- complete omission of the grounding document -- at minimal implementation cost.

---

## Final Position

| Blocker | Original | Revised | Disposition |
|---------|----------|---------|-------------|
| 1. Dispute entry definition | Option B (content-negative) | Option B (content-negative) | **Held**. Vacuous-output concern addressed via SC-014 in Blocker 3, not trigger redefinition. |
| 2. Structured output | Option B (SHOULD-level prose conventions) | Option A (headings only) + deferred schema with activation condition | **Modified**. Conceded to Mechanist and Purist: SHOULD-level prose conventions are unenforceable pseudo-contracts. Retreated to headings-only v1 contract with MAY-level template-author guidance. Adopted Purist's activation condition. |
| 3. Success criteria | P1, four SCs (SC-008--011) | P1, seven SCs (SC-008--014) | **Modified**. Expanded coverage to match Mechanist's scope (FR-025, FR-026). Added SC-014 for vacuous-output detection from Blocker 1 analysis. Retained Given/When/Then format. |
| 4. Citation enforcement | Option C, template-weighted | Option C, balanced weighting | **Modified**. Conceded that deferring FR-023 grounding-path check to v2 was negligent when the cost is one string comparison. Template remains the primary shaping surface; engine check is the primary detection surface. Both are cheap. The weighting debate dissolves. |

### What changed and why

The cross-reviews exposed one genuine internal contradiction (Blocker 4: I advocated "favor the recoverable error" while proposing a template-only enforcement that makes citation violations unrecoverable) and one genuine analytical failure (Blocker 2: I conflated "minimum viable" with "pre-specified conventions" and dismissed the de facto hardening of SHOULD-level patterns). Both modifications make my positions more internally consistent, not less pragmatic. The retreats are toward cheaper, more honest contracts -- which is what pragmatism demands.

What I did not concede: the trigger definition (Blocker 1) remains content-negative. The Purist's vacuous-output concern is real but is an output quality problem, not a trigger precision problem, and I address it with SC-014 rather than trigger redefinition. The Mechanist agreed with me on this blocker from the start.
