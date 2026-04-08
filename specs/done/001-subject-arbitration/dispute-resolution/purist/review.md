# The Purist: Dispute Resolution Review

**Agent**: The Purist (specification completeness, formal correctness, explicit contracts)
**Spec**: `conversus/specs/001-subject-arbitration/spec.md`
**Input**: `dispute-resolution/problem.md` (4 blockers), v2 synthesis `final.md`
**Date**: 2026-03-19

---

## Blocker 1: "Dispute entry" definition

**Position**: Option A — pattern-match (`**Dispute:**` or equivalent bold-label pattern).

### Rationale

The trigger mechanism is a machine-readable predicate. Its job is to answer a binary question: does the synthesis contain at least one unresolved dispute? A predicate must have a precise positive definition — "what counts" — not a negative definition — "what does not count." Option B (content-negative) defines a dispute entry as "anything that is not whitespace and not an HTML comment." That is not a definition of a dispute. It is a definition of "non-empty content." It conflates the presence of content with the presence of disputes.

Consider the concrete failure mode: a Phase 5 synthesizer includes a one-line preamble between the markers — "All disputes were resolved during deliberation." Under Option B, this is a dispute entry. Phase 6 fires. The arbiter reads zero disputes, produces a vacuous resolution, and the engine writes a `resolution.md` that resolves nothing. The spec has no mechanism to recover from this false positive because FR-022 only covers agent-process failure and structurally unintelligible output — not semantically vacuous output triggered by a false-positive predicate.

The argument that Option A "re-couples the primary trigger to Markdown formatting" misunderstands the coupling hierarchy. The trigger mechanism is already coupled to content conventions — the markers themselves are a content convention (HTML comments). The question is not whether there is coupling but whether the coupling is to a *defined* convention or an *undefined* one. Option A couples to a defined label pattern that the spec controls. Option B couples to whatever text the LLM happens to emit, which the spec does not control.

### Evidence

The v2 synthesis itself documents this risk: "Content-presence gap between trigger evaluation and variable extraction — markers could contain only whitespace, causing Phase 6 to fire with empty dispute content" (new issue #5). The convergence on a content-presence guard (Convergence 3) treats whitespace-only content as a non-trigger — but it does not address non-whitespace non-dispute content. Option B has an unguarded gap that Option A closes.

The fallback mechanism in FR-011 already uses `**Dispute:` pattern matching: "checking whether the `### Remaining Disputes` heading contains at least one `**Dispute:` entry." If the primary mechanism uses a different definition than the fallback, the two mechanisms can disagree on the same document. A synthesis file where the markers contain preamble text but no `**Dispute:` entries would trigger under Option B's primary mechanism but not trigger under the fallback. Two mechanisms that answer the same question differently on the same input is a specification defect.

### Concrete spec text

Replace the undefined "at least one dispute entry" in FR-011 with:

> **FR-011** (amended): [...] the engine looks for content between `<!-- CONVERSUS:DISPUTES_BEGIN -->` and `<!-- CONVERSUS:DISPUTES_END -->` markers and checks whether at least one line matches the pattern `**Dispute` (bold-label prefix with formatting tolerance). A "dispute entry" is any line within the marker range whose text content, after stripping leading whitespace, begins with the Markdown bold marker `**Dispute`. This definition aligns the primary and fallback mechanisms on a single pattern. HTML comments and whitespace-only lines within the marker range are not dispute entries.

---

## Blocker 2: Structured output — normative weight for v1

**Position**: Option C — FR-018 section headings as the v1 contract, plus a SHOULD-level schema definition in a standalone "Deferred: Structured Output" section.

But I go further than any of the three agents: the schema fields MUST have explicit conditions for when they transition from SHOULD to MUST.

### Rationale

Option A (headings only) leaves the v1 output as unstructured prose inside defined sections. This is implementable but produces output that is not machine-parseable below the section level. If the goal of structured output is eventual machine extraction, the v1 output becomes a liability — every real arbiter output produced under v1 headings-only will have a different internal structure, and the v2 extraction engine will need heuristic parsing to handle the variance.

Option B (headings + prose conventions) adds SHOULD-level labeled sub-fields to the v1 template. spec-kit's argument is pragmatic: prose conventions guide LLM output toward regularity without requiring formal parsing. But spec-kit is wrong to classify this as a v1 contract obligation. A SHOULD-level instruction in a template is not a contract — it is a suggestion to an LLM. LLMs do not distinguish between SHOULD and MUST in their prompt. The instruction either constrains output or it does not.

Option C separates the concerns correctly: v1 has a contract (FR-018 headings), and v2 has a design target (schema fields). The SHOULD-level language in the deferred section communicates intent to template authors and future implementors without creating a pseudo-contract that is unenforceable in v1.

However, every agent missed the critical deficiency: the deferred section has no activation condition. "Future structured extraction SHOULD target these fields" is aspirational, not actionable. A deferred item without an explicit trigger for when it becomes required is indistinguishable from a wish. The spec must state when the deferral expires.

### Evidence

The v1 synthesis noted: "Structured output schema -- fields are listed in Implementation Guidance but as advisory, not normative. The v1 synthesis recommended normative definition of fields with deferred mechanism." The v2 synthesis narrowed the dispute to normative weight but did not address activation conditions. Two full deliberation rounds have failed to define when "deferred" becomes "required."

### Concrete spec text

Add a standalone section after Implementation Guidance:

> ### Deferred: Structured Output
>
> The following schema fields are defined as the target for future structured extraction from arbitration output. For v1, the output contract is FR-018 section headings only. Template authors SHOULD design prose to be consistent with these fields but are not required to produce them in any machine-parseable format.
>
> | Field | Type | Description |
> |-------|------|-------------|
> | `dispute_id` | string | Identifier for the dispute being resolved |
> | `ruling_type` | enum | One of `accept`, `reject`, `modify`, `unresolved` |
> | `grounding_citation` | string | Specific principle/requirement cited from the grounding document |
> | `required_changes` | list\<string\> | Concrete changes required |
> | `affected_target_files` | list\<string\> | Which target files the changes apply to (per FR-026) |
> | `confidence_level` | string | Arbiter's confidence in the ruling |
>
> **Activation condition**: Structured extraction becomes a P1 requirement when any downstream system (CI integration, automated change application, cross-conversus chaining) depends on machine-readable arbitration output. The trigger is the first spec that declares a dependency on structured arbitration data. Until that trigger, the schema remains advisory.

---

## Blocker 3: Success criteria priority

**Position**: Option A — P1. Missing success criteria are a spec-completeness defect that blocks implementation planning.

### Rationale

This is not a judgment call. It is a definitional question. What is the purpose of a success criterion? It is the bridge between a normative requirement and a test. Without it, the requirement is a statement of intent that cannot be verified.

FR-022 says: "If the arbiter agent fails (timeout, crash, or malformed output), Phase 5 output MUST be the terminal state." What does "terminal state" mean operationally? Does it mean the engine exits with code 0? Code 1? Does it mean the report still prints? Does it mean the `arbitration/` directory is not created, or created but empty, or not created at all? Every implementor will answer these questions differently. The SC is what forces a single answer.

gh-aw's argument — "FRs with RFC 2119 language are implementable without SCs" — is technically true and practically dangerous. Yes, you can write code that satisfies "Phase 5 output MUST be the terminal state." But two implementors will write different code, and without an SC, there is no test to determine which implementation is correct. The RFC 2119 language defines the obligation. The SC defines the observable behavior. They are complementary, not redundant.

The v2 synthesis records that APM conceded to spec-kit: "A spec without acceptance criteria for its requirements is incomplete by any consumption model." I agree with this statement without qualification. A spec that ships requirements without acceptance criteria has shipped untestable requirements. Untestable requirements are indistinguishable from aspirations.

### Evidence

The spec already has SCs for FR-001 through FR-021 (covered by SC-001 through SC-007 and the acceptance scenarios). FR-022 through FR-027 are the only requirements without SCs. These are not obscure edge cases — they include failure semantics (FR-022), output validation (FR-023), citation boundaries (FR-024), requirement traceability (FR-025), per-file attribution (FR-026), and idempotency (FR-027). These are the requirements most likely to produce implementation divergence because they govern non-happy-path behavior where "reasonable defaults" differ between implementors.

The cost of writing SCs is measured in minutes. The cost of discovering incompatible implementations is measured in debugging sessions. This is not a tradeoff.

### Concrete spec text

Add to the Success Criteria section:

> - **SC-008**: When the arbiter agent fails (timeout, crash, or output with zero FR-018 section headings), the engine MUST NOT write `resolution.md`, MUST emit a diagnostic warning to stderr, and MUST complete the conversus with Phase 5 as the terminal output. The final report MUST include "Arbitration: failed ({reason})" instead of dispute-resolved count.
> - **SC-009**: When `resolution.md` is written but is missing one or more FR-018 section headings, the engine MUST emit a validation warning identifying the missing sections. The file MUST still be written. The final report MUST include "Arbitration: {N} disputes resolved (validation warnings: {M} missing sections)."
> - **SC-010**: No binding decision in `resolution.md` MAY cite a `docs` entry as the sole basis for a ruling. Every binding decision MUST cite at least one principle, requirement, or constraint from the `grounding` document. A post-hoc audit of all `**Ruling:**` or equivalent decision entries must confirm grounding citations.
> - **SC-011**: When multiple target files exist, every entry in the "Summary of Changes Required" section MUST specify the affected file path. Entries without file attribution are validation warnings.
> - **SC-012**: When target documents contain numbered requirements, binding decisions MUST reference specific identifiers (e.g., "FR-003", "SC-002") rather than vague references (e.g., "the validation requirement"). At least one identifier per binding decision.
> - **SC-013**: Re-running Phase 6 on the same conversus output MUST overwrite any existing `resolution.md`. The engine MUST NOT prompt for confirmation, append, or rename the previous file.

---

## Blocker 4: Citation boundary enforcement surface

**Position**: Option C — FR-024 in the spec, instruction in the template, AND FR-023 validation covers all three surfaces.

### Rationale

This blocker asks: where is the citation constraint enforced? The correct answer is: everywhere it can be enforced. Defense in depth is not a luxury in specification design — it is the only strategy that accounts for the different failure modes at each layer.

**The spec layer** (FR-024) defines the normative requirement. Without it, the constraint has no formal standing. APM is correct that the spec is the authoritative source. But APM is wrong that "normatively sufficient" means "operationally enforced." A requirement that exists only in a spec is enforced by human reviewers reading the spec and checking the output. For an LLM agent, there is no human reviewer in the loop — the agent is autonomous.

**The template layer** adds a one-sentence instruction to the arbitration template: "Only the grounding document may be cited as authority in binding decisions. Documents listed in `docs` provide factual context only and must not serve as the sole basis for any ruling." This instruction costs one sentence and closes the gap between "what the spec says" and "what the agent sees." gh-aw and spec-kit are right: the enforcement surface for an LLM agent is its prompt. The agent does not read the spec. It reads its template. An unenforced constraint is not a constraint.

**The validation layer** (extending FR-023) provides post-hoc detection. Even with the template instruction, the LLM may violate the constraint. FR-023 currently validates section headings only. Extending it to check citation sources — verifying that every binding decision cites the grounding document and that no decision cites only `docs` entries — catches violations after the fact. This is the last line of defense.

APM's concern about "maintenance drift where template and spec can diverge" is real but already addressed by the template authoring contract in Implementation Guidance: "Template authors MUST preserve these invariants." Adding one more invariant — "The template must restate the citation boundary from FR-024" — is the mechanism for keeping them in sync. The drift risk from redundancy is lower than the enforcement gap from omission.

### Evidence

The spec already uses a multi-surface enforcement model for other constraints. FR-015 defines behavioral constraints in the spec AND requires the template to instruct the arbiter to follow them: "The template MUST instruct the arbiter to: [...] NOT introduce new recommendations [...] NOT overturn unanimous convergence points." These are spec-level constraints restated as template instructions. FR-024 (citation boundary) is architecturally identical to FR-015.5 (no new recommendations) — both constrain arbiter behavior. If one gets template enforcement, both should.

The asymmetry is the tell. FR-015's six behavioral constraints are spec-level requirements AND template instructions. FR-024's citation boundary is spec-level only. There is no principled reason for the inconsistency. Either template-level enforcement is unnecessary (in which case FR-015 template instructions are also unnecessary) or it is necessary (in which case FR-024 needs it too).

### Concrete spec text

Three changes:

1. Add to FR-015 instruction list:

> 7. Cite ONLY the `grounding` document as authority in binding decisions. Documents provided via `docs` may be referenced for factual context but MUST NOT serve as the sole basis for any ruling.

2. Add to the Template Authoring Contract invariants:

> - The template must restate the citation boundary constraint from FR-024: only the grounding document may be cited as authority in binding decisions.

3. Amend FR-023:

> **FR-023** (amended): After Phase 6 completes, the engine MUST validate that `resolution.md` contains the required section headings defined in FR-018. The engine SHOULD additionally validate that each binding decision entry contains at least one reference to the grounding document path or its content. If heading validation fails, the engine MUST emit a warning flagging the malformed output. If citation validation fails, the engine MUST emit a separate warning identifying decisions without grounding citations. Malformed output MUST NOT be silently accepted, but the file MUST still be written (warnings are informational, not blocking).

---

## Why My Approach Wins

The four blockers share a common root cause: the spec defines what should happen but does not fully specify how to verify that it happened. My resolutions address this systematically:

1. **Blocker 1**: I choose the definition that makes the trigger predicate testable with a single regex, aligns primary and fallback mechanisms, and eliminates false positives from non-dispute content. A trigger that can fire on preamble text is a trigger that cannot be tested deterministically.

2. **Blocker 2**: I choose the separation that keeps v1 contracts enforceable and v2 planning actionable, but I add what no agent proposed — an explicit activation condition for the deferred schema. A deferral without a trigger is a deferral forever.

3. **Blocker 3**: I classify missing SCs as P1 because the alternative — shipping requirements without acceptance criteria — violates the fundamental contract between a spec and its implementors. If a requirement cannot be tested, it cannot be verified. If it cannot be verified, it is not a requirement.

4. **Blocker 4**: I choose defense in depth across all three enforcement surfaces because each surface catches a different failure mode. The spec catches design errors. The template catches runtime omissions. The validation catches output violations. Choosing one surface means accepting that the other two failure modes are undetected.

The thread connecting all four positions: **a specification is a contract, and contracts must be enforceable at every boundary where violations can occur.** A contract that relies on a single enforcement point is a contract that fails when that point fails. My approach ensures that every requirement in this spec is defined precisely enough to test (Blocker 1), deferred with explicit activation conditions (Blocker 2), accompanied by acceptance criteria (Blocker 3), and enforced at every surface where violations are possible (Blocker 4).

Ambiguity is not flexibility. It is a defect.
