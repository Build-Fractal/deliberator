# Spec-Kit Cross-Review of APM's Review

**Cross-Reviewer**: spec-kit
**Reviewing**: APM's review of Subject Arbitration (Phase 6)
**Date**: 2026-03-19

---

## Dangerous Contradictions

### DC-1: Removing the cooperative-only restriction versus game-theoretic rigor

APM's top-priority recommendation (P1-1) is to remove FR-004 and enable all four modes immediately, arguing that the templates are "already written and tested" and that blocking them creates dead code. Spec-kit's review (Missed Opportunity #8, Recommendation P2-5) takes the opposite position: the non-cooperative templates should be *acknowledged and documented* but kept blocked, because "enabling arbitration for other modes requires a separate spec that analyzes the game-theoretic implications."

This is not a stylistic disagreement. The game-theoretic implications of arbitration differ fundamentally across modes. In cooperative mode, the arbiter resolves disputes between agents who were *trying to converge* -- the arbitration is a tiebreaker within a consensus-seeking process. In winner-take-all, the arbiter reviews a *verdict* -- a zero-sum outcome -- and arbitration becomes an appeals court that can reverse the entire deliberation. In prisoners-dilemma, the arbiter adjudicates *boundary disputes* between agents who were incentivized to defect, meaning arbitration can retroactively punish or reward strategic behavior. These are structurally different authority relationships, and enabling them without formal analysis of how arbitration changes each mode's incentive structure risks undermining the game-theoretic integrity that makes conversus's multi-mode design meaningful. APM's framing ("the templates exist, therefore ship them") treats arbitration as a file-delivery problem when it is actually a mechanism-design problem. Shipping all four modes without the analysis spec-kit recommends would create a correctness risk, not merely dead code.

### DC-2: Arbiter as a reusable package artifact versus arbiter as a context-bound decision authority

APM recommends (Missed Opportunity #3, Recommendation P3-8) creating an `.arbiter.md` or `.arbiter.yml` primitive type in APM's taxonomy, making arbiters discoverable, distributable, and reusable across projects. This treats the arbiter as a portable artifact -- something you install from a registry and plug into any conversus run.

Spec-kit's position is that the arbiter's legitimacy comes from *decision authority over the specific target artifact* combined with *a declared grounding document that constrains that authority* (Recommendation P2-7). The arbiter is not a generic capability; it is a role that derives meaning from its relationship to a particular subject, a particular grounding document, and a particular set of disputes. A reusable, distributable arbiter package decouples the arbiter from the context that makes its rulings legitimate. You cannot install "decision authority" from a package manager. An arbiter extracted into `apm_modules/` and shared across projects would carry its configuration but not its grounding relationship -- the very thing that distinguishes arbitration from unconstrained override. APM's recommendation optimizes for distribution at the cost of the grounding constraint that makes the entire Phase 6 design trustworthy.

### DC-3: Grounding document as a composable context graph versus grounding as a singular authoritative source

APM argues (Missed Opportunity #2, Recommendation P2-4) that the single-path `grounding` field should accept a list of paths, noting that "a system's decision framework is rarely a single document." APM further suggests leveraging its link-resolution system to build a composable knowledge graph from the grounding field.

Spec-kit's review treats the grounding document as a direct parallel to a constitution -- a single, declared source of governing principles (Alignment point #1, Recommendation P2-6). In spec-kit's model, a constitution is deliberately singular: it forces the spec author to distill governing principles into one authoritative document rather than scattering them across a graph of linked files. The singularity is a feature, not a limitation -- it prevents citation laundering, where a ruling claims grounding in a chain of linked documents that no single reader can verify. If the arbiter can cite a document that links to another document that links to another, the grounding constraint becomes unfalsifiable. A single grounding path forces the arbiter to cite a specific, bounded document that a human can read end-to-end and verify. APM's composability recommendation, while sound for general context management, would weaken the grounding constraint's auditability -- the core integrity mechanism of Phase 6.

---

## Tensions

### T-1: Hook-based lifecycle extensibility versus spec-defined behavioral boundaries

APM recommends adding `pre-arbitration` and `post-arbitration` hook points (Missed Opportunity #7, Recommendation P2-7), consistent with APM's existing lifecycle hook system. Spec-kit does not propose hooks but instead recommends defining explicit *behavior* for specific conditions (e.g., Recommendation P1-4: "When a binding decision has confidence 'Low', the resolution MUST include a `Requires follow-up:` field"). These are philosophically different extension strategies. Hooks say "let the user define what happens at this point." Behavioral requirements say "the spec defines what happens at this point." Both are valid, but they pull the design in opposite directions -- hooks toward open extensibility, behavioral requirements toward closed predictability. The spec will need to decide which extension model Phase 6 follows, and the answer may differ from what APM uses for its own lifecycle.

### T-2: Machine-readable output -- where and what

Both reviews independently identify the lack of structured output as a gap (APM Missed Opportunity #9, spec-kit Missed Opportunity #1), and both recommend a machine-readable format alongside the human-readable `resolution.md`. But the proposed solutions differ. APM recommends a *sidecar file* (`resolution.summary.yml`) with dispute labels, rulings, grounding citations, confidence levels, and required changes. Spec-kit recommends *inline structured markers* (`<!-- RULING: dispute-id -->`) or *YAML front matter within `resolution.md` itself*. The sidecar approach keeps the human-readable document clean but introduces a second artifact that must stay in sync. The inline approach keeps everything in one file but makes the markdown harder to read and edit. More importantly, the *contents* differ: APM's sidecar is oriented toward dispute metadata (labels, citations, confidence), while spec-kit's structured block needs requirement identifiers (FR-numbers, SC-numbers) for downstream SDD consumption. Both are needed, but neither review accounts for the other's format requirements.

### T-3: `{ALL_DISPUTES}` variable semantics

APM recommends (Missed Opportunity #8) introducing a dedicated `{REMAINING_DISPUTES}` variable parsed from the synthesis output, arguing that reusing `{ALL_DISPUTES}` in Phase 6 is ambiguous and makes the scope constraint "instruction-dependent rather than machine-enforceable." Spec-kit's review does not flag this variable naming issue but instead focuses on the parsing mechanism (the `### Remaining Disputes` heading convention) and recommends elevating it from an assumption to a constraint with enforcement (Recommendation P1-3). APM wants a new variable that carries only the remaining disputes. Spec-kit wants a formalized contract for extracting disputes from the synthesis. These are complementary but create a tension: if `{REMAINING_DISPUTES}` is introduced as a separate variable, the parsing contract spec-kit recommends becomes the mechanism that populates it -- but the spec currently defines template variables as static substitutions, not as parsed extractions from prior phase outputs. This would be a new category of template variable (derived rather than configured), and neither review fully addresses the implementation implications of that shift.

### T-4: Scope of the "no new recommendations" constraint

Both reviews flag the gap between FR-015.5 ("MUST NOT introduce new recommendations") and the template's observation mechanism (APM Off-Base #3, and implicitly in spec-kit's alignment with the constraint in Alignment point #5). APM explicitly calls out the contradiction and recommends reconciling the spec's formal requirements with the template's observation escape valve. Spec-kit endorses the constraint as enforcing scope discipline analogous to "specs define the WHAT and WHY, not the HOW." The tension is that APM sees the observation mechanism as a necessary nuance that the spec's formal language fails to capture, while spec-kit's alignment section implicitly endorses the strict reading. Both positions have merit: the strict constraint is simpler to enforce and audit, but the observation mechanism prevents information loss when the arbiter notices something no agent raised. The resolution needs to be explicit about whether observations are a carve-out from the constraint or a separate category entirely.

### T-5: Schema versioning urgency

APM recommends (Recommendation P2-5) adding a `schema` or `version` field to `conversus.yml` now, citing APM's own `apm.yml` versioning as precedent and arguing that it is cheaper to add before the first breaking change than after. Spec-kit's review does not mention schema versioning at all -- its concerns are oriented toward output format and downstream consumption, not configuration schema evolution. This is not a contradiction but a tension of priorities: APM views the configuration file as a distribution artifact that needs versioning for package management, while spec-kit views it as a local configuration that matters less than the output artifacts it produces. If conversus is distributed through APM (which the monorepo structure suggests), APM's versioning concern is legitimate. If conversus is used as a standalone skill, the urgency is lower.

---

## Safe Agreements

### SA-1: The `### Remaining Disputes` heading convention is a fragile dependency that must be formalized

Both reviews independently identify this as a critical issue. APM calls it an "Off-Base Assumption" (#2) and recommends adding machine-readable markers (`<!-- CONVERSUS:DISPUTES_BEGIN -->`) to the synthesis template (P1-2). Spec-kit calls it both an Off-Base Assumption (#2) and a Missed Opportunity (#3), recommending elevation from assumption to constraint with a validation mechanism. The diagnosis is identical: treating a hard parsing dependency as an informal assumption about future template authors' behavior creates a latent failure mode. Both reviews agree this must be fixed before the spec is considered correct. The specific mechanism (HTML comments vs. template linting rules) can be debated, but the requirement to formalize the contract is unanimous.

### SA-2: The information-asymmetry assumption about when arbitration is meaningful is too narrow

APM (Off-Base #1) argues the assumption excludes internal-perspective scenarios (e.g., backend/frontend/infra teams in prisoners-dilemma mode). Spec-kit (Off-Base #1) argues it excludes document-as-subject scenarios where the arbiter's legitimacy comes from decision authority, not operational knowledge. Both agree the current framing unnecessarily restricts the design's applicability and should be rewritten. APM recommends broadening to cover internal perspectives. Spec-kit recommends reframing around decision authority rather than information asymmetry. These are compatible expansions -- the rewritten assumption should encompass both the authority framing and the internal-perspective case.

### SA-3: Non-cooperative mode templates need explicit acknowledgment in the spec

Both reviews identify the disconnect between the existence of four mode templates and the cooperative-only restriction. APM frames this as a contradiction (Missed Opportunity #4, Recommendation P1-1). Spec-kit frames it as an unacknowledged presence (Missed Opportunity #8, Recommendation P2-5). They disagree on the remedy (APM: enable all modes; spec-kit: document the templates as drafts and keep the restriction), but they agree on the problem: the spec says nothing about the non-cooperative templates, and that silence is a defect regardless of whether the restriction is kept or lifted.

---

## Summary

The two reviews converge strongly on diagnostics -- both identify the heading-convention fragility, the narrow information-asymmetry assumption, and the need for structured output. Where they diverge, the disagreements are substantive and load-bearing: whether to ship all modes now versus gate on game-theoretic analysis, whether the arbiter is a distributable artifact or a context-bound authority, and whether the grounding document should be composable or deliberately singular. These are not reconcilable through compromise -- they reflect genuinely different models of what makes arbitration trustworthy, and the spec must choose.
