# The Purist: Revised Positions

**Agent**: The Purist (specification completeness, formal correctness, explicit contracts)
**Input**: Cross-reviews from The Mechanist and The Pragmatist; own cross-reviews of both
**Date**: 2026-03-19

---

## Blocker 1: "Dispute entry" definition

**Original position**: Option A -- pattern-match (`**Dispute:**`).
**Revised position**: **Modified** -- content-negative primary (Option B) with pattern-match fallback (Option A), reconciled under a unified fail-open rationale.

### What changed my mind

The Mechanist and the Pragmatist both identified the same contradiction in my original position, and they are right. I argued for defense-in-depth in Blocker 4 (err toward over-detection) while selecting the under-detecting mechanism in Blocker 1 (err toward precision). I cannot hold both positions simultaneously without a principled distinction between them, and I do not have one.

The Mechanist's argument is the one that actually moved me: "If primary and fallback use the same pattern, they are not independent mechanisms. They are the same mechanism executed twice." This is correct. My original FR-011 amendment collapses two trigger paths into one predicate wearing two syntactic costumes. The structural markers become ceremony. Defense-in-depth requires that the two mechanisms test different things -- content-negative for the primary (broad, catches anything) and pattern-match for the fallback (narrow, confirms specificity). This is the architecture that makes both mechanisms independently useful.

FR-012's fail-open directive settles the directional question. The spec authors explicitly chose "better to run the arbiter unnecessarily than to skip it when disputes exist." My original position optimized for the wrong failure mode. A false positive costs one wasted invocation and produces a vacuous resolution that, while not ideal, is detectable (zero disputes resolved in the report). A false negative silently drops real disputes with no artifact to signal the omission.

I concede to both reviewers that my false-positive cost analysis was incomplete. A vacuous `resolution.md` is a real problem -- I identified it myself -- but the Pragmatist's point about recoverability holds: a file that exists and says nothing is diagnosable. A file that does not exist when it should is invisible. I still believe the content-presence gap I identified (non-dispute preamble text triggering Phase 6) is a real risk. But the correct response is not to narrow the primary trigger; it is to ensure the arbiter's output under vacuous-input conditions is well-defined.

### What I still insist on

The content-negative definition alone is insufficient without the content-presence guard from Convergence 3. The definition must explicitly exclude whitespace-only lines AND HTML comments, which both reviewers already accept. Additionally, FR-022's three-tier failure model should be extended with a fourth category: "arbiter completes but resolves zero disputes." The final report should distinguish "Arbitration: 0 disputes resolved (no actionable disputes found)" from "Arbitration: 3 disputes resolved" so that vacuous resolutions are surfaced, not buried.

### Revised spec text

> **FR-011** (amended): [...] the engine looks for content between `<!-- CONVERSUS:DISPUTES_BEGIN -->` and `<!-- CONVERSUS:DISPUTES_END -->` markers and checks whether at least one line contains non-whitespace content that is not an HTML comment. A "dispute entry" is any line within the marker range whose text content, after stripping leading whitespace and HTML comments, is non-empty. If the primary mechanism cannot locate markers, the fallback mechanism checks whether the `### Remaining Disputes` heading contains at least one line matching the pattern `**Dispute` (bold-label prefix). The primary and fallback mechanisms are intentionally different predicates to provide independent detection paths.

---

## Blocker 2: Structured output -- normative weight for v1

**Original position**: Option C -- FR-018 headings as v1 contract, advisory schema in deferred section with explicit activation condition.
**Revised position**: **Modified** -- retain Option C structure, concede that the activation condition must be process-level rather than spec-level, and accept SHOULD-level prose conventions in the template as non-normative guidance.

### What changed my mind

The Mechanist identified a genuine contradiction: my activation condition ("when any downstream system declares a dependency on structured arbitration data") is not machine-checkable, which violates my own standard from Blocker 3 ("if it cannot be verified, it is not a requirement"). I applied my own principle inconsistently. An activation condition that requires a human to notice an external event is a process obligation, not a specification constraint. The Mechanist is right that honest deferral is better than pseudo-rigorous activation conditions that no system monitors.

The Pragmatist identified a second contradiction I must address: I dismissed SHOULD-level template conventions in Blocker 2 while endorsing SHOULD-equivalent template instructions in Blocker 4. Both are template-level guidance aimed at shaping LLM output. I drew a distinction between "constraint instructions" (Blocker 4: do not cite docs as authority) and "formatting instructions" (Blocker 2: use `**Ruling:**` labels) that does not survive scrutiny. Both are prompt instructions to a stochastic agent. I cannot endorse one category while rejecting the other on the grounds that LLMs do not distinguish SHOULD from MUST.

### What I still insist on

The v1 contract remains FR-018 section headings only. SHOULD-level prose conventions are guidance to template authors, not obligations on the arbiter. The distinction matters: when output deviates from a SHOULD convention, no validation warning fires and no failure is recorded. Calling them "conventions" rather than "contract" is not a cosmetic choice -- it determines whether the engine acts on their absence.

The deferred schema section must still exist as a standalone section. Without it, the six fields have no home in the spec and exist only in Implementation Guidance asides. A standalone section with SHOULD-level language communicates intent without creating false obligations.

I withdraw the machine-checkable activation condition and replace it with a process-level note that is honest about what it is.

### Revised spec text

> ### Deferred: Structured Output
>
> The following schema fields are defined as the target for future structured extraction from arbitration output. For v1, the output contract is FR-018 section headings only. Template authors SHOULD design prose to be consistent with these fields and SHOULD use labeled sub-fields (`**Dispute:**`, `**Ruling:**`, `**Changes Required:**`) to improve output regularity, but arbiter output that omits or renames these labels is compliant if it contains the required FR-018 section headings.
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
> **Process note**: This schema is advisory for v1. Promotion to a normative requirement is a future spec decision triggered by downstream consumption needs (CI integration, automated change application, cross-conversus chaining). This note exists to communicate intent, not to create an automated trigger.

---

## Blocker 3: Success criteria priority

**Original position**: Option A -- P1. Missing SCs block implementation.
**Revised position**: **Held** -- P1, with scope reduced from six SCs to five. SC-010 is rewritten to remove the dependency on sub-field parsing.

### Why I hold this position

All three agents agree that SCs are P1. The Mechanist and the Pragmatist both independently arrived at the same conclusion from different axioms. There is nothing to concede here because there is no remaining disagreement on the core question.

### What I concede on scope

The Mechanist correctly identified that my original SC-010 depends on `**Ruling:**` entries existing in a parseable form -- the same prose-convention parsing I rejected as a v1 contract in Blocker 2. This is an internal inconsistency I must fix. I cannot write an SC whose verification mechanism depends on capabilities the spec does not mandate.

The Pragmatist raised the same point as DC-3: SC-010's "post-hoc audit" is either a human audit (not an automated SC) or an NLP extraction problem (deferred to v2). Both reviewers are correct that SC-010 as originally written is unimplementable under my own Blocker 2 position.

I rewrite SC-010 to test at the section level, not the sub-field level. The check becomes: the Binding Decisions section must contain at least one reference to the grounding document path. This is a string-presence check -- does the grounding document filename or path appear in the section? -- not a semantic-parsing problem. It does not verify that every individual ruling cites the grounding document (that requires sub-field parsing). It verifies that the section as a whole is grounded. This is weaker than my original SC-010 but actually testable in v1.

I also accept the Pragmatist's point that SC-012 (numbered requirement references) may over-constrain implementations where the grounding document does not use numbered identifiers. I retain SC-012 but condition it: "When the grounding document contains numbered requirements or identifiers..."

### Revised spec text

> - **SC-008**: When the arbiter agent fails (timeout, crash, or output with zero FR-018 section headings), the engine MUST NOT write `resolution.md`, MUST emit a diagnostic warning to stderr, and MUST complete the conversus with Phase 5 as the terminal output. The final report MUST include an arbitration failure indicator with reason.
> - **SC-009**: When `resolution.md` is written but is missing one or more FR-018 section headings, the engine MUST emit a validation warning identifying the missing sections. The file MUST still be written. The final report MUST include a warning count.
> - **SC-010**: The Binding Decisions section of `resolution.md` MUST contain at least one textual reference to the grounding document (by filename, path, or explicit title). A `resolution.md` whose Binding Decisions section contains zero references to the grounding document MUST trigger a validation warning.
> - **SC-011**: When multiple target files exist, every entry in the "Summary of Changes Required" section MUST specify the affected file path. Entries without file attribution are validation warnings.
> - **SC-012**: When the grounding document contains numbered requirements or identifiers (e.g., "FR-003", "SC-002"), binding decisions SHOULD reference specific identifiers rather than vague references. This is a SHOULD-level quality check, not a blocking validation.
> - **SC-013**: Re-running Phase 6 on the same conversus output MUST overwrite any existing `resolution.md`. The engine MUST NOT prompt for confirmation, append, or rename the previous file.

---

## Blocker 4: Citation boundary enforcement surface

**Original position**: Option C -- all three surfaces (spec, template, validation).
**Revised position**: **Held** -- Option C, with FR-023 citation validation scoped to a string-presence check rather than semantic parsing.

### Why I hold this position

Both the Mechanist and the Pragmatist agree on Option C. The Mechanist selects it explicitly. The Pragmatist selects "Option C weighted toward the template" but still endorses all three surfaces. There is no remaining disagreement on the architectural choice.

The only dispute is about what FR-023 citation validation looks like in v1. The Pragmatist argues it is "a v2 concern at best" because citation-source validation "requires parsing prose to determine which document a citation refers to, which is an NLP problem." The Mechanist agrees on all three surfaces but frames engine validation as "the only load-bearing surface" with the others as "probability modifiers."

### What I concede on validation scope

The Pragmatist and the Mechanist both correctly identified that my original FR-023 amendment conflated two different capabilities: (1) checking that the grounding document is referenced at all, and (2) checking that no decision cites only docs entries. Capability (1) is a string-presence check. Capability (2) requires understanding citation intent, which is genuinely an NLP problem in unstructured prose.

I retain capability (1) as a MUST-level v1 check and defer capability (2) to v2 when structured output makes it tractable. This aligns with my revised Blocker 2 position: v1 validates structure and string-presence; v2 validates semantics.

The Mechanist's concern about hierarchy -- "whose verdict wins when surfaces conflict?" -- is well-taken but does not change my position. The engine is the authoritative validator. The spec is the authoritative definition. The template is the runtime enforcement surface. These are not co-equal in authority; they are co-necessary in coverage. When the template diverges from the spec, it is a template authoring defect, not a specification ambiguity. The template authoring contract invariants exist precisely to prevent this divergence.

### Revised spec text

Three changes, as originally proposed, with FR-023 scoped to string-presence:

1. Add to FR-015 instruction list:

> 7. Cite ONLY the `grounding` document as authority in binding decisions. Documents provided via `docs` may be referenced for factual context but MUST NOT serve as the sole basis for any ruling.

2. Add to the Template Authoring Contract invariants:

> - The template must restate the citation boundary constraint from FR-024: only the grounding document may be cited as authority in binding decisions.

3. Amend FR-023:

> **FR-023** (amended): After Phase 6 completes, the engine MUST validate that `resolution.md` contains the required section headings defined in FR-018. The engine MUST additionally validate that the Binding Decisions section contains at least one textual reference to the grounding document (by filename, path, or explicit title). If heading validation fails, the engine MUST emit a warning flagging the malformed output. If grounding-reference validation fails, the engine MUST emit a separate warning. In both cases, the file MUST still be written (warnings are informational, not blocking). Semantic citation-source analysis (verifying that individual rulings cite grounding rather than docs) is deferred to v2 when structured output makes per-ruling extraction tractable.

---

## Final Position

| Blocker | Original | Revised | Disposition |
|---------|----------|---------|-------------|
| 1: Dispute entry definition | Option A (pattern-match) | Option B primary + Option A fallback | **Modified** |
| 2: Structured output weight | Option C (headings + activation condition) | Option C (headings + process note + SHOULD conventions) | **Modified** |
| 3: Success criteria priority | P1, six SCs | P1, six SCs (SC-010 rewritten, SC-012 conditioned) | **Held** (scope adjusted) |
| 4: Citation enforcement surface | Option C (all three surfaces) | Option C (validation scoped to string-presence) | **Held** (scope adjusted) |

### Concessions made

1. **Blocker 1**: I concede that pattern-matching as the primary trigger optimizes for the wrong failure mode given FR-012's fail-open directive. The Mechanist's argument that primary and fallback must test different things to constitute independent mechanisms is correct. I was applying defense-in-depth selectively.

2. **Blocker 2**: I concede that my activation condition was unenforceable by my own standards. I also concede that SHOULD-level prose conventions in the template are architecturally consistent with the template instructions I endorsed in Blocker 4. I was drawing an unprincipled distinction between constraint instructions and formatting instructions.

3. **Blocker 3**: I concede that SC-010 as originally written depends on sub-field parsing that my Blocker 2 position does not mandate. The SC is rewritten to a string-presence check.

### Positions maintained

1. **Blocker 3 priority**: P1, without qualification. All three agents converged here.

2. **Blocker 4 all-three-surfaces**: Option C, without qualification. All three agents converged here.

3. **The deferred schema section must exist as a standalone section** in the spec, not scattered across Implementation Guidance asides. Advisory does not mean invisible.

4. **FR-023 must include grounding-reference validation in v1**, scoped to string-presence. Deferring all citation validation to v2 leaves the citation boundary enforced only by a probabilistic template instruction -- one enforcement surface for the constraint that makes arbitration authoritative rather than advisory. That is insufficient.

### The thread

My original review ended with: "a specification is a contract, and contracts must be enforceable at every boundary where violations can occur." I still believe this. What the cross-reviews taught me is that I was inconsistent in applying it. I demanded enforcement-at-every-boundary for citation constraints (Blocker 4) while selecting the narrower trigger for dispute detection (Blocker 1). I demanded machine-checkable activation conditions (Blocker 2) while writing success criteria that depend on capabilities the spec does not mandate (Blocker 3). The revised positions resolve these inconsistencies by applying the same principle uniformly: enforce broadly, validate at the level the v1 engine can actually check, defer semantic analysis to v2 honestly rather than pretending process notes are automated triggers.
