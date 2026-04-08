# Spec-Kit Revised Position: Subject Arbitration (Phase 6)

**Reviewer**: spec-kit (SDD framework)
**Revision Date**: 2026-03-19
**Inputs**: APM cross-review, gh-aw cross-review, spec-kit cross-reviews of APM and gh-aw

---

## Disposition of Original Recommendations

### P1-1: Add structured machine-readable block to arbitration output (FR-018)

**Modified.**

The original recommendation stands in principle but must be coupled with gh-aw's output validation concern. gh-aw's cross-review (DC-1) correctly identifies that requiring structured YAML or markers from an AI agent without a validation step creates a false sense of machine-readability -- downstream tooling that trusts the structure gets garbage if the agent produces malformed output. APM's cross-review (T-1) notes the architectural tension between inline markers (spec-kit's proposal) and a sidecar file (APM's proposal).

Revised position: Require a **fenced YAML code block at the end of `resolution.md`** (not front matter, not a sidecar) containing each dispute ID, ruling type, grounding citation key, and required-change summary. Add a **post-arbitration validation step** that parses the YAML block and logs warnings for malformed or missing entries. If validation fails, the resolution is still written (human-readable prose remains authoritative), but the structured block is flagged as unreliable in the final report. This keeps a single output artifact (no sidecar sync drift), makes machine consumption possible when the agent cooperates, and degrades gracefully when it does not.

The sidecar approach (APM) is withdrawn from consideration because it creates two artifacts that can drift. The inline HTML comment approach from the original recommendation is also withdrawn in favor of the fenced YAML block, which is more natural for AI agents to produce correctly.

### P1-2: Require binding decisions to reference target-document identifiers (FR-015/FR-019)

**Surviving.**

Neither cross-review challenged this recommendation. APM's review does not address requirement traceability at the ruling level. gh-aw's review does not address it either. The recommendation remains: when the target documents contain numbered requirements (FR-xxx, SC-xxx, US-xxx), the template MUST instruct the arbiter to reference specific identifiers in its Required changes. This is a template instruction change, not a schema change, and carries no implementation risk.

### P1-3: Elevate the `### Remaining Disputes` heading convention from assumption to constraint

**Modified.**

Both cross-reviews identify this as a critical fragility (APM SA-4, gh-aw SA-1). The disagreement is over remediation: spec-kit proposed locking the heading with a linting rule, APM proposed machine-readable HTML comment markers, gh-aw proposed structured signals (HTML comments or a sidecar metadata file).

gh-aw's cross-review (DC-2) makes the strongest argument against spec-kit's original position: locking a prose heading as a contract creates template ossification, and if both a structured signal and a locked heading are implemented, they can drift. APM's cross-review (T-3) frames the same tradeoff: spec-kit preserves backward compatibility while APM introduces a breaking change to Phase 5 templates.

Revised position: **Adopt a hybrid approach with a clear hierarchy.** The `### Remaining Disputes` heading remains the human-readable section (no ossification -- template authors can style it as needed). Add a machine-readable HTML comment `<!-- CONVERSUS:DISPUTES_REMAIN: {true|false} -->` at the end of the Phase 5 synthesis output, emitted by the synthesis template itself. FR-011 is updated to check the HTML comment first; if absent, fall back to heading parsing. This preserves backward compatibility (existing templates without the comment still work via fallback), gives new templates a robust signal path, and avoids the dual-source-of-truth problem because the heading is demoted from control-flow signal to human-readable display. The comment is the contract; the heading is the presentation.

This is a concession to both APM and gh-aw. Spec-kit's original "lock the heading" approach is withdrawn.

### P1-4: Define behavior for Low-confidence rulings

**Modified.**

gh-aw's cross-review (T-5) raises a valid perverse incentive: if Low-confidence rulings trigger mandatory follow-up fields, arbiters will be incentivized to report Medium confidence to avoid the extra requirement. APM's cross-review (DC-3) flags a related concern about the "no new recommendations" constraint -- observations noted in the Confidence Assessment may violate FR-015.5's literal reading.

Revised position: Do NOT make Low-confidence rulings trigger mandatory process requirements (withdrawn). Instead, add a simpler requirement: **the confidence field in the template MUST be accompanied by a one-sentence justification** (e.g., "High -- grounding document directly addresses this tradeoff" or "Low -- grounding document is silent on performance vs. correctness tradeoffs"). This makes confidence self-documenting without creating perverse incentives. The justification gives downstream consumers (human or machine) the information they need to decide whether to trust or revisit the ruling, without the spec prescribing what they must do with it.

### P2-5: Acknowledge non-cooperative arbitration templates and define their status

**Surviving.**

APM's cross-review (DC-1) identifies this as a dangerous contradiction with APM's own P1-1 (remove FR-004, ship all modes). APM's cross-reviewer itself recommends resolving this contradiction by adopting spec-kit's position: "resolve DC-1 by adopting spec-kit's position (keep cooperative-only, formally status the other templates as drafts)." gh-aw's cross-review (T-3) frames this as a tension between dead-code elimination (gh-aw) and preparatory design (spec-kit), and does not claim either is clearly superior.

The recommendation survives unchanged. The non-cooperative templates should be acknowledged in the spec as draft/experimental, the cooperative-only restriction (FR-004) should be retained, and the spec should state that enabling arbitration for other modes requires a separate spec analyzing game-theoretic implications. The templates are preparatory design artifacts, not dead code -- they document intent and reduce future implementation cost. Removing them (gh-aw's lean) discards work that will be needed; shipping them without analysis (APM's P1-1) creates correctness risk.

### P2-6: Add a convention for spec-kit projects: arbiter.grounding SHOULD be the constitution

**Modified.**

APM's cross-review (T-2) and gh-aw's cross-review (DC-3) both challenge the grounding model, but in opposite directions. APM wants to expand `grounding` to a list of paths. gh-aw initially recommended broadening citation scope to include `docs`, then reconsidered in their own cross-review (DC-3): "The safer path is to keep FR-019 as-is (grounding-only citations) and let `docs` serve as context the arbiter can read but not cite as authority."

Spec-kit's cross-review of APM (DC-3) argued that a multi-path grounding field enables citation laundering -- the arbiter cites a chain of linked documents that no single reader can verify. The singularity of the grounding document is a feature that forces distillation of governing principles into one auditable artifact.

Revised position: The original recommendation stands (convention that `arbiter.grounding` SHOULD be the constitution for spec-kit projects), but is strengthened by gh-aw's concession. Add an explicit clarification to the spec: **`docs` provides read-only context that informs the arbiter's reasoning; only the `grounding` document may be cited as authority in binding decisions.** This formalizes the distinction gh-aw converged toward and blocks the citation-scope expansion that would weaken the integrity mechanism. The `grounding` field remains a single path, not a list. APM's multi-path proposal is rejected.

### P2-7: Reframe the information-asymmetry assumption around decision authority

**Modified.**

APM's cross-review (DC-2) identifies a dangerous contradiction: spec-kit frames legitimacy as decision authority constrained by a grounding document, while APM frames it as integration scope (the subject knows cross-cutting constraints no individual agent knows). APM's cross-reviewer recommends synthesizing both: "decision authority constrained by a grounding document, informed by the arbiter's unique integration perspective."

gh-aw's cross-review (T-2) argues the spec should retain both framings rather than replacing one with the other: "information asymmetry as the common case, decision authority as the general principle."

Both cross-reviews are right that a pure decision-authority framing drops the information-asymmetry justification, which is valid for the motivating use case. Spec-kit's original recommendation was too aggressive in replacing rather than generalizing.

Revised position: Replace the current assumption with a two-part framing: **(1) The general principle: subject arbitration is meaningful when the arbiter has decision authority over the target artifact, constrained by a declared grounding document. (2) The common case: the subject typically has integration knowledge (cross-cutting constraints, production behavior, actual usage patterns) that individual reviewers lack, which makes it a natural arbiter.** Decision authority is the necessary condition. Information asymmetry is the common but not required justification. This synthesizes all three positions.

### P3-8: Add per-file attribution in binding decisions for multi-target runs

**Surviving.**

Neither cross-review challenged this recommendation. gh-aw's cross-review (T-5) notes it competes for implementation priority with run-level metadata, but acknowledges these are complementary granularities. The recommendation remains: when the conversus has multiple target files, each binding decision's Required changes MUST specify which target file is affected.

### P3-9: Define a checklist output format for binding decisions

**Withdrawn.**

On reflection, this recommendation overspecifies the integration surface for a v1 release. gh-aw's cross-review (T-1) correctly identifies the tension between pipeline integration (spec-kit's priority) and execution safety (gh-aw's priority), arguing that execution safety should gate the initial release and pipeline integration should be a fast follow. A separate checklist artifact adds scope without addressing the core Phase 6 design. If the structured YAML block from revised P1-1 is implemented, `/speckit.checklist` can consume it directly without a dedicated checklist output format. Withdrawn in favor of keeping the structured block as the single machine-readable integration point.

### P3-10: Add a note about grounding document stability during long runs

**Surviving.**

Neither cross-review challenged this recommendation. It is low-cost (a documentation note) and addresses a real edge case. The recommendation remains: add to Assumptions or Constraints that the grounding document is assumed stable for the duration of the run, and concurrent modifications should be avoided.

---

## New Recommendations

### N-1: Add explicit observation carve-out for FR-015.5 (from APM DC-3)

APM's cross-review (DC-3) identifies a correctness-level gap: the template's Confidence Assessment section instructs the arbiter to "note it as an observation... not as a ruling," but FR-015.5 ("MUST NOT introduce new recommendations") could suppress these observations under a literal reading. Spec-kit's original review endorsed FR-015.5 as enforcing scope discipline but did not examine the template's observation mechanism.

APM is right. The "no new recommendations" constraint and the observation mechanism serve different purposes. The constraint prevents the arbiter from expanding scope (new features, new requirements). The observation mechanism allows the arbiter to flag signals it noticed during review that may warrant future attention -- explicitly not binding, not actionable in this run.

**Recommendation (P1):** Add a clarification to FR-015 or create FR-015.6: "The arbiter MAY note observations in the Confidence Assessment section that are explicitly excluded from binding decisions. Observations are informational signals for future consideration, not recommendations. They do not expand the scope of the deliberation record." This reconciles the spec's formal requirements with the template's actual instructions.

### N-2: Define failure semantics for Phase 6 (from gh-aw, endorsed by gh-aw cross-review T-1)

Spec-kit's original review did not address failure modes. gh-aw's review correctly identifies this as a gap: what happens when the arbiter agent crashes, times out, or produces output that does not conform to the template structure? gh-aw's cross-review (T-1) frames this as complementary to spec-kit's structured-output concern: failure semantics protect the pipeline, structured output makes success valuable.

**Recommendation (P1):** Add a new FR: "If Phase 6 fails (agent error, timeout, or empty output), the conversus MUST complete using Phase 5 output as the terminal state. The final report MUST indicate 'Arbitration: failed ({reason})' and include the Phase 5 synthesis path as the authoritative output. Phase 6 failure MUST NOT invalidate the Phase 1-5 deliberation record." This ensures the conversus always produces a valid terminal state.

### N-3: Formalize docs vs. grounding distinction (from gh-aw DC-3 concession)

gh-aw's cross-review of spec-kit (DC-3) reconsidered its own recommendation to broaden citation scope and concluded: "The safer path is to keep FR-019 as-is (grounding-only citations) and let `docs` serve as context the arbiter can read but not cite as authority." This concession creates an opportunity to formalize a distinction the spec currently leaves implicit.

**Recommendation (P2):** Add to FR-019 or create a new FR: "The arbiter's `docs` field provides supplementary context that the arbiter may read to inform its reasoning. Only the `grounding` document may be cited as authority in binding decisions. Citations to documents in `docs` are not valid grounding citations." This is now a three-reviewer consensus (spec-kit original position, gh-aw revised position, APM's cross-review recommending synthesis).

---

## Position Summary

Spec-kit's revised position retains 5 of 10 original recommendations (2 unchanged, 3 modified) and withdraws 2. The most significant shifts:

1. **Structured output** (P1-1): Conceded to gh-aw that validation must accompany structure. Conceded to APM that a sidecar creates sync drift. Adopted a middle path: fenced YAML block with post-validation and graceful degradation.

2. **Heading convention** (P1-3): Conceded to both cross-reviewers that locking a prose heading is the wrong approach. Adopted structured HTML comments as the primary trigger signal with heading parsing as a backward-compatible fallback.

3. **Information-asymmetry framing** (P2-7): Conceded to both cross-reviewers that the pure decision-authority reframe was too aggressive. Synthesized a two-part framing that preserves information asymmetry as the common case under decision authority as the general principle.

4. **Grounding singularity** (P2-6): Held firm against APM's multi-path proposal, strengthened by gh-aw's concession on citation scope. The single grounding document remains the core integrity mechanism.

5. **Cooperative-only restriction** (P2-5): Held firm. APM's own cross-reviewer recommended adopting spec-kit's position on this point.

Three new recommendations were added: an observation carve-out for FR-015.5 (adopted from APM), failure semantics for Phase 6 (adopted from gh-aw), and formalization of the docs-vs-grounding distinction (consensus across all three reviewers).

The core thesis is unchanged: arbitration output must be traceable, grounding must be singular and auditable, and non-cooperative modes require formal analysis before shipping. The revisions make the output more robust (validation, failure handling) and the contracts more precise (structured triggers, observation carve-outs, citation scope) without expanding scope.
