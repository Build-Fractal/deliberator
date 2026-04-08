# Spec-Kit Final Disputes: Subject Arbitration (Phase 6) -- v2

**Agent**: spec-kit (SDD framework)
**Phase**: Disputes (Phase 4, Round 2)
**Date**: 2026-03-19
**Inputs**: All three v2 revised positions (spec-kit, APM, gh-aw)

---

## Remaining Disputes

### Dispute 1: Structured output — normative schema status and prose convention interaction

The three-way disagreement on structured output narrowed significantly in v2 revisions but did not fully resolve. The mechanism question (arbiter-produced YAML vs. engine extraction) is effectively settled -- spec-kit conceded in the revised P2-4 that the normative FR proposal for arbiter-produced structured output is withdrawn. APM and gh-aw's shared position that engine extraction is the correct mechanism is accepted. The remaining dispute is about the normative weight of the schema fields and their relationship to the prose conventions.

- **APM (N-1, revised P2-4 table row 5)**: Endorse spec-kit's proposed FR-028 schema fields with `affected_target_files` pluralization. The schema is normatively important for future versions. Separately, APM's original P1-3 prose conventions (`**Dispute:**`, `**Ruling:**`, `**Grounding:**`) were withdrawn, but spec-kit's revised N-4 resurrects them as a SHOULD-level template instruction.
- **gh-aw (modified P3-8)**: Extract the schema to a standalone "Deferred: Structured Output" section with SHOULD-level language. The fields are advisory, not normative. SHOULD is the ceiling -- MUST is premature before implementation experience.
- **Spec-kit (revised P2-4)**: Withdrew the normative FR. Adopted a hybrid: prose conventions as the v1 contract (SHOULD in FR-015), schema fields as advisory in a dedicated section. The fields "will be evaluated for normative elevation after implementation experience."

The convergence is real but the gap remains on one axis: APM says the schema fields are "normatively important" and endorses them as a P2 FR. gh-aw says they are advisory and SHOULD is the ceiling. Spec-kit's revised position aligns with gh-aw's SHOULD-level placement but accepts APM's pluralization fix. The dispute reduces to: does the dedicated section carry SHOULD weight (gh-aw, spec-kit) or FR-level normative weight (APM)?

**Spec-kit's position**: SHOULD-level in a dedicated section is correct for v1. APM's desire for normative weight is understandable from a packaging perspective -- APM needs stable field names to build extraction tooling against -- but normative commitment before any implementation has validated the field model creates rigidity that serves no current consumer. The schema section should state that field names are stable targets for early adopters (stronger than MAY, weaker than MUST), and that normative elevation is planned for v2 contingent on implementation findings. APM's `affected_target_files` pluralization is adopted regardless of normative level -- the cardinality fix is correct on its merits.

---

### Dispute 2: "Dispute entry" definition for the primary trigger mechanism

All three agents agree that (a) the "dispute entry" concept must be defined before SKILL.md is synced, and (b) the definition applies only to `trigger: disputes_remain`. The disagreement is over the definition itself.

- **APM (modified P1-1)**: A dispute entry is any line matching the `**Dispute:**` pattern, or at minimum any line beginning with a Markdown bold marker (`**`). This keeps the primary and fallback mechanisms structurally aligned.
- **gh-aw (modified P1-2)**: A dispute entry is any line containing non-whitespace content that is not an HTML comment. This excludes stray comments but does not couple the trigger to a specific Markdown formatting convention.
- **Spec-kit (modified P1-3)**: Adopted gh-aw's positive framing ("what a dispute entry IS") over spec-kit's original negative formulation. The content-presence check applies only to `trigger: disputes_remain`.

APM's definition couples the primary trigger mechanism to the `**Dispute:**` prose pattern. gh-aw's definition decouples the trigger from any specific Markdown convention, excluding only HTML comments. The practical difference: under APM's definition, a Phase 5 output that contains dispute text not formatted with `**Dispute:**` bold markers would fail to trigger Phase 6 even though disputes are present. Under gh-aw's definition, any non-comment, non-whitespace text between the markers triggers Phase 6.

**Spec-kit's position**: gh-aw's definition is correct. The structural markers exist precisely to decouple trigger evaluation from prose formatting conventions. APM's concern about false positives from template artifacts is valid but overfit -- the solution to template artifacts producing stray content between markers is to fix the Phase 5 template, not to make the trigger mechanism format-aware. A trigger that silently fails because disputes were written with `- Dispute:` instead of `**Dispute:**` is more dangerous than a trigger that fires on a stray template artifact, because the former is a silent omission of arbitration while the latter produces a diagnostic-rich Phase 6 run that surfaces the template bug. Spec-kit endorses gh-aw's "non-whitespace, non-HTML-comment" definition with one addition: the engine SHOULD log the extracted content count as a diagnostic, so that a single-line artifact trigger is distinguishable from a legitimate multi-dispute trigger in the Phase 6 audit trail.

---

### Dispute 3: Success criteria priority classification

All three agents now agree that success criteria for FR-022 through FR-027 are missing and must be added. The dispute is over whether this is a P1 (blocks spec completeness) or P2 (improves spec quality) gap.

- **Spec-kit (surviving P1-2)**: Missing SCs are P1. A spec without acceptance criteria for its requirements is incomplete. SCs are the bridge between normative language and test plans; without them, every implementor independently interprets what "testing FR-022" means.
- **APM (N-2)**: Concedes the gap is real. Classifies as P1. "A spec without acceptance criteria for its requirements is incomplete by any consumption model."
- **gh-aw (N-1)**: Accepts spec-kit's finding. Classifies as P2. "The FRs themselves are implementable without SCs -- the SCs formalize the acceptance boundary, they do not create it."

APM aligns with spec-kit on P1. gh-aw maintains P2. The substantive question is whether FRs with RFC 2119 language are self-sufficient for implementation or whether explicit SCs are a prerequisite for spec completeness.

**Spec-kit's position**: P1 is correct, and APM's concurrence strengthens the case. gh-aw's argument -- that FRs are implementable without SCs -- is true but misframes the concern. The issue is not whether a single implementor can build something that satisfies FR-022. The issue is whether two independent implementors, reading the same FR-022, will build things that are mutually compatible in their failure behavior. "Phase 6 failure MUST fall back to Phase 5 with a warning" leaves open: what constitutes "failure" (addressed by the three-tier model), what constitutes a "warning" (log line? sidecar file? exit code?), and what "fall back" means operationally (delete resolution.md if partially written? never create it? create it with a failure marker?). SCs close these interpretation gaps. P1 is the correct classification because the gaps affect interoperability, not just quality.

---

### Dispute 4: Citation boundary enforcement -- spec-level FR vs. template-level instruction

gh-aw's surviving P2-4 recommends adding an explicit instruction to the Phase 6 template restating FR-024's constraint that `docs` citations must not serve as the sole basis for binding rulings. APM's position is that FR-024 alone is sufficient and the template inherits the constraint through the spec's normative weight. This was not directly addressed in spec-kit's v2 revision but intersects with spec-kit's positions on template authoring contract completeness.

- **gh-aw (surviving P2-4)**: The arbiter is an LLM agent. It sees its prompt (the template), not the spec. FR-024 in the spec text is invisible to the arbiter at runtime. The template must contain the instruction or the constraint is unenforceable.
- **APM (cross-review Tension 4)**: FR-024 is normative. The engine validates output. The template inherits the constraint. Restating spec requirements in templates creates a maintenance burden where template and spec can drift.

**Spec-kit's position**: gh-aw is right. This is not a question of whether FR-024 is normative -- it is. The question is whether the arbiter agent can comply with a requirement it cannot see. For human-operated systems, the spec is the authority and the operator reads it. For LLM-agent-operated systems, the prompt is the only input the agent receives. FR-023 validates section-heading presence, not citation sourcing. There is no post-hoc validation that catches a `docs`-only citation masquerading as a grounding-derived ruling. The enforcement surface is the template itself. Adding one sentence to the template instruction -- "Binding rulings must cite the grounding document; supplementary docs may inform but not solely justify a ruling" -- is low-cost, eliminates the enforcement gap, and can be mechanically kept in sync with FR-024 via a template authoring contract invariant. The maintenance-drift risk APM cites is real but manageable; the enforcement gap gh-aw cites is not manageable without the instruction.

---

## Convergence

### Convergence 1: Three-tier failure model for FR-022/FR-023

All three agents now agree on the three-tier disambiguation that APM originated and gh-aw adopted in full:

1. Agent-process failure (FR-022): timeout, crash, no output. No resolution.md. Phase 5 terminal.
2. Structural unintelligibility (FR-022 sub-case): agent completed but output has zero recognizable FR-018 section headings. No resolution.md. Diagnostic emitted.
3. Incomplete but parseable prose (FR-023): agent completed, output has at least one FR-018 heading but is missing others. File written with warning.

The bright-line test between tiers 2 and 3 -- "does the output contain at least one FR-018 section heading?" -- is implementable without semantic parsing. This is the strongest new convergence point in v2, resolving a gap that spec-kit originally claimed was already addressed (v1 Alignment 5) but that cross-review evidence proved ambiguous.

### Convergence 2: Content-presence guard scoped to `trigger: disputes_remain` only

All three agents agree that the whitespace-only guard must not apply to `trigger: always`, preserving the subject-endorsement path (US1-AS3). For `trigger: disputes_remain`: if the structural markers are present but contain only whitespace (or no content matching the dispute-entry definition), the trigger evaluates to `false`. For `trigger: always`: the trigger fires regardless, with a diagnostic warning if `{REMAINING_DISPUTES}` extraction produces empty content. APM originated the scoping constraint; spec-kit adopted it in the revised P1-3; gh-aw's surviving P3-6 aligns through its diagnostic-warning approach.

### Convergence 3: Endorsement-mode behavior under `trigger: always` with empty disputes

All three agents agree that the `trigger: always` + empty `{REMAINING_DISPUTES}` interaction must be explicitly specified, not merely documented. The agreed resolution: when Phase 6 runs under `trigger: always` and `{REMAINING_DISPUTES}` is empty, the arbiter operates in endorsement mode. FR-018 required sections still apply; Binding Decisions contains a confirmation statement rather than dispute rulings; Confidence Assessment evaluates the synthesis positions. gh-aw originated the design-gap framing; spec-kit adopted it in modified P3-8; APM's silence on the substance implies acceptance of the mechanism (APM's cross-review challenged template branching, not the endorsement specification itself).

### Convergence 4: Draft template filtering requires a testable FR

All three agents agree that the Constraints-section MUST for draft template filtering needs a corresponding testable FR. gh-aw originated the proposal (P2-3). APM endorsed it explicitly (N-4). Spec-kit endorsed it in N-2 of the revision. The proposed FR requires the engine to not dispatch templates containing the `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` marker and to emit a diagnostic. The relationship between FR-004 (config-time gate) and the new FR (dispatch-time gate) is layered defense. No agent contests this.

### Convergence 5: Template authoring contract must be scoped to cooperative mode

All three agents agree that the current template authoring contract implicitly assumes cooperative-mode Phase 5 output and should make that assumption explicit. Spec-kit originated the scoping recommendation (P2-6). APM accepted it and proposed simultaneous application of scoping and invariant additions (revised P1-2). gh-aw did not contest. The contract header should declare its applicability to cooperative mode, and APM's additional invariants (per-file attribution, Phase 5 cross-reference) are adopted within that scope.

---

## Final Position Statement

Spec-kit enters the synthesis phase with its core thesis intact but refined by two rounds of cross-review. The largest concession -- withdrawing the normative FR for structured output schema -- reflects genuine persuasion, not tactical retreat. gh-aw's argument that normative commitment before implementation experience creates dead-letter requirements, combined with APM's argument that dual-binding (prose conventions + schema fields) creates maintenance drift, produced a better design than spec-kit's original proposal.

**Firm positions:**

1. **Success criteria for FR-022 through FR-027 are a P1 gap.** Two agents (spec-kit, APM) classify this as P1. One (gh-aw) classifies as P2. The interoperability argument is dispositive: without explicit SCs, two independent implementors reading the same FR will produce incompatible failure behaviors. This is a spec-completeness defect, not a quality-improvement opportunity.

2. **The citation boundary must be enforced in the template, not just the spec.** The arbiter is an LLM agent that sees its prompt, not the spec document. FR-024's constraint on `docs`-only citations has no post-hoc validation mechanism (FR-023 checks headings, not citation sourcing). The template is the only enforcement surface available. One sentence in the template instruction closes the gap.

3. **The "dispute entry" definition must not couple the trigger to prose formatting.** APM's `**Dispute:**` pattern requirement would make the primary trigger mechanism no more capable than the heading-based fallback, defeating the purpose of structural markers. gh-aw's "non-whitespace, non-HTML-comment" definition is the correct decoupling point. Template artifacts that produce false-positive triggers are Phase 5 template bugs that should surface, not be silently filtered.

**Positions held with flexibility:**

1. **Structured output schema at SHOULD level.** Spec-kit aligns with gh-aw that SHOULD is the correct normative ceiling for v1. APM's desire for FR-level commitment is understandable but premature. The schema section should signal stability for early adopters without creating binding obligations that foreclose implementation discovery. If the synthesis elevates to MUST, spec-kit will accept it provided an implementation-experience gate is attached to the commitment.

2. **Success criteria content.** Spec-kit proposed four specific SCs. The exact wording is negotiable; the existence of SCs covering failure fallback (FR-022), output validation (FR-023), draft template filtering, and idempotency (FR-027) is not.

The v2 deliberation resolved the deepest architectural disagreements from v1 -- structured output mechanism, failure-state disambiguation, trigger scoping, endorsement-mode specification. The four remaining disputes are narrower: normative weight of advisory schema fields, the precise definition of a dispute entry, the priority classification of missing success criteria, and whether a spec-level FR needs template-level restatement for LLM-agent enforcement. These are calibration disagreements within a shared design, not competing architectures. The synthesis should be able to resolve each by selecting a position and recording the rationale.
