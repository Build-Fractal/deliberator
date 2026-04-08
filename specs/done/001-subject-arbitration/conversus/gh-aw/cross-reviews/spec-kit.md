# gh-aw Cross-Review of spec-kit's Review

**Cross-reviewer**: gh-aw (GitHub Agentic Workflows)
**Reviewing**: spec-kit's review of Subject Arbitration (Phase 6)
**Date**: 2026-03-19

---

## Dangerous Contradictions

### DC-1: Structured output requirements vs. arbiter as an AI agent

spec-kit's P1 recommendation #1 requires machine-readable YAML front matter or structured markers (`<!-- RULING: dispute-id -->`) in `resolution.md`. Our review's Missed Opportunity #2 flags the absence of output validation -- the arbiter is an AI agent whose output is a suggestion, not a schema-conforming response. These two positions compound into a dangerous contradiction: spec-kit wants to ADD structured formatting requirements to the arbiter's output while neither review addresses how to ENFORCE them. An AI agent instructed to produce YAML front matter may produce malformed YAML, omit fields, or hallucinate dispute IDs. Without the output validation step we flagged (our recommendation #3), spec-kit's structured output requirement creates a false sense of machine-readability -- downstream tooling (e.g., `/speckit.specify --input`) would parse the block trusting its correctness, but nothing guarantees it. The result is worse than no structure at all: tooling that silently consumes garbage. Both reviews must converge on a single position: either (a) add structured output AND post-arbitration validation together as a coupled requirement, or (b) treat the resolution as human-readable prose and keep machine consumption out of scope for the initial release.

### DC-2: Elevating the heading convention to a locked contract vs. replacing it with structured signals

spec-kit's recommendation #3 proposes elevating `### Remaining Disputes` from an assumption to a constraint and locking it in the synthesis template with enforcement rules ("Template authors MUST NOT rename this section"). Our recommendation #2 proposes replacing or supplementing heading-based parsing with structured signals (`<!-- disputes_remaining: N -->` or a sidecar metadata file). These are fundamentally opposed mitigation strategies for the same fragility. Locking a prose heading as a contract creates template ossification -- every future template author is bound by an invisible dependency they may not know about, and the enforcement mechanism (template linting) is itself a new system that must be built and maintained. Structured signals decouple the control-flow dependency from the prose structure entirely. Adopting both creates redundancy and confusion: is the heading the contract, or is the structured signal the contract? If they disagree, which wins? The spec must pick ONE strategy. We maintain that structured signals are the safer path because they separate the human-readable document from the machine-readable control flow, but if the conversus adopts spec-kit's locking approach, our structured-signal recommendation should be withdrawn entirely.

### DC-3: Broadening grounding citation scope vs. maintaining single-document accountability

Our recommendation #7 proposes expanding FR-019 to allow citations to any document in the arbiter's `docs` list, not just the single `grounding` path. spec-kit's alignment point on the grounding document ("the arbiter's grounding document IS a constitution in SDD terms") and their recommendation #6 ("arbiter.grounding SHOULD be the constitution") together argue for a TIGHTER coupling between the grounding document and decision authority. If we broaden citation scope to include supplementary docs, the single-document accountability model that both reviews praise breaks down. An arbiter could cite a tangential supporting document to justify a ruling that the grounding document would not support, defeating the transparency mechanism. The spec's current design -- single grounding document as the sole citable authority -- is more restrictive but more auditable. We should reconsider our recommendation #7: if citations are broadened, the grounding document loses its special status as THE constraint mechanism. The safer path is to keep FR-019 as-is (grounding-only citations) and let `docs` serve as context the arbiter can read but not cite as authority.

---

## Tensions

### T-1: SDD pipeline integration vs. initial release scope

spec-kit's review is oriented around making arbitration output consumable by the downstream SDD pipeline (`/speckit.specify --input`, `/speckit.plan`, `/speckit.checklist`). Our review is oriented around making arbitration operationally safe (failure modes, dry-run, idempotency). These are both valid but competing priorities for a v1 release. spec-kit wants richer output; we want safer execution. Attempting both in the initial release risks a feature that is neither production-safe nor pipeline-integrated. The tension is real but manageable: execution safety (our P1s) should gate the initial release, and pipeline integration (spec-kit's P1s) should be a fast follow once the arbitration phase is proven stable.

### T-2: Decision authority framing vs. information asymmetry framing

spec-kit's Off-Base Assumption #1 argues that the spec's information-asymmetry framing ("the subject has information that external reviewers lack") should be replaced with a decision-authority framing ("the arbiter has decision authority over the target artifact"). Our review does not challenge this framing -- we accepted the spec's game-theoretic rationale at face value. On reflection, spec-kit's reframing is partially right: decision authority is the more general case. But the spec's information-asymmetry argument is not wrong for the motivating use case (the speckit-orchestrator example, where the subject genuinely had operational knowledge the reviewers lacked). The tension: reframing around pure decision authority removes the justification for WHY the subject specifically should be the arbiter rather than any authorized party. The spec should retain both framings -- information asymmetry as the common case, decision authority as the general principle -- rather than replacing one with the other as spec-kit recommends.

### T-3: Template acknowledgment strategy for non-cooperative modes

Both reviews flag the template/constraint mismatch (templates exist for all four modes, but FR-004 restricts to cooperative). spec-kit recommends acknowledging the templates and documenting their status as draft/experimental. We recommend either removing them or relaxing FR-004. These are different risk postures: spec-kit tolerates documented dead code; we prefer eliminating ambiguity. Neither position is clearly superior -- removing templates loses preparatory work, while keeping them invites premature use. The resolution depends on the project's release philosophy, which the spec does not declare.

### T-4: Grounding document quality vs. grounding document validation

spec-kit's Missed Opportunity #5 proposes a convention that `arbiter.grounding` SHOULD be the constitution for spec-kit projects. Our recommendation #8 proposes documenting what makes an effective grounding document (minimum content expectations, anti-patterns). These address the same underlying concern -- grounding document quality -- but from opposite directions. spec-kit's approach is prescriptive (use THIS specific document type). Ours is descriptive (here is what GOOD looks like). A prescriptive convention for spec-kit projects does not help non-spec-kit users, and descriptive guidance without tooling enforcement is advice that can be ignored. The tension is unresolved but low-stakes: both recommendations can coexist without contradiction.

### T-5: Confidence levels as actionable vs. informational

spec-kit's Missed Opportunity #6 flags that the confidence assessment in the template is "unconnected to any success criteria" and recommends requiring Low-confidence rulings to include a `Requires follow-up:` field. Our review does not address confidence levels at all. spec-kit's recommendation adds process weight to a field that may be better left lightweight. If Low-confidence rulings trigger mandatory follow-up fields, arbiters will be incentivized to report Medium confidence to avoid the extra requirement -- a perverse incentive. Conversely, leaving confidence purely informational (the current design) means the field adds no value beyond author self-assessment. The tension is whether confidence should drive process or merely inform readers.

---

## Safe Agreements

### SA-1: Phase 5 heading-based trigger parsing is fragile and must be hardened

Both reviews independently identify FR-011's reliance on `### Remaining Disputes` heading parsing as the spec's most significant fragility. spec-kit calls it "cross-template coupling" that violates constitution principles. We call it "treating prose output as a reliable control-flow signal." The diagnosis is identical even though the remediation strategies differ (see DC-2). The spec must address this fragility in some form before the feature ships.

### SA-2: Non-cooperative mode templates need explicit status declaration

Both reviews flag the mismatch between FR-004 (cooperative-only) and the existence of templates for all four modes. spec-kit recommends acknowledging them with documented status. We recommend resolving the ambiguity by either removing or enabling them. Both agree the current state -- templates that exist but are rejected by validation -- is unacceptable for a shipped feature. The spec must take a position.

### SA-3: Backward compatibility is correctly designed and does not need changes

Both reviews independently validate that the opt-in model (FR-005, SC-004) is architecturally sound. spec-kit calls it consistent with spec-kit's additive extension philosophy. We call it consistent with gh-aw's additive frontmatter field pattern. Neither review proposes changes to the backward-compatibility design. This is a settled area of the spec.

### SA-4: The grounding document requirement is the right integrity mechanism

Both reviews endorse the grounding document as the core constraint on arbiter authority. spec-kit maps it to the SDD constitution pattern. We map it to gh-aw's protected-files permission boundary. The specific framing differs, but both reviews agree that requiring citation of a declared framework is what separates legitimate arbitration from unconstrained decision-making. No changes needed to FR-003 or FR-019's core design.

---

## Synthesis Note

The two reviews are largely complementary: spec-kit focuses on downstream pipeline consumability and SDD workflow integration; gh-aw focuses on operational safety, failure modes, and execution robustness. The dangerous contradictions arise not from disagreement about the spec's quality but from incompatible remediation strategies for shared concerns. DC-1 (structured output without validation) and DC-2 (heading locking vs. structured signals) require explicit resolution before recommendations from both reviews can be implemented together. DC-3 (citation scope) requires gh-aw to reconsider its own recommendation in light of spec-kit's tighter accountability model.
