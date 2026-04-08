# Spec-Kit Review: Subject Arbitration (Phase 6)

**Reviewer**: spec-kit (SDD framework)
**Spec**: `conversus/specs/001-subject-arbitration/spec.md`
**Date**: 2026-03-19
**Review Type**: Cooperative conversus — spec-kit perspective

---

## Executive Summary

The subject-arbitration spec proposes an optional Phase 6 for the conversus framework where the subject of a review acts as a binding arbiter for unresolved disputes. The spec is well-motivated by a real-world gap (9 unresolved disputes from a live run), and the game-theoretic framing (interested-party arbitration constrained by a grounding document) is sound. The design is conservative in the right ways: cooperative-only, fully optional, backward compatible.

From the spec-kit perspective, the spec is strong on requirements rigor and acceptance scenarios but underspecifies how arbitration interacts with downstream SDD workflow stages. The spec treats arbitration output as a terminal artifact, but in practice it feeds directly into `/speckit.specify --input` and `/speckit.plan`, which have their own requirements for input format, traceability, and entity extraction. The grounding document concept closely parallels spec-kit's constitution, creating a natural alignment point that the spec does not exploit. Several opportunities exist to make arbitration output machine-consumable for the SDD pipeline rather than a human-readable document that requires manual interpretation.

---

## Alignment

- **Grounding document requirement maps directly to spec-kit's constitution pattern.** Both enforce that decisions cite a declared framework. The arbiter's grounding document IS a constitution in SDD terms -- a set of governing principles that constrain design decisions and must be cited. This parallel is architecturally sound and validates the approach.

- **Template-driven extensibility follows spec-kit's own extension model.** The `templates/{mode}/arbitration.md` convention mirrors how spec-kit uses `templates/commands/*.md` and `templates/*-template.md` -- each new capability is a template, not a code change. The auto-discovery claim (US3-AS3) aligns with spec-kit's philosophy of convention over configuration.

- **Acceptance scenarios use proper Given/When/Then structure with testable outcomes.** The seven acceptance scenarios in US1 are independently verifiable, which meets spec-kit's spec quality checklist requirement that "all acceptance scenarios are defined" and "requirements are testable and unambiguous."

- **The spec correctly separates schema (FR-001 through FR-005) from execution (FR-006 through FR-012) from output (FR-016 through FR-021).** This layered requirement organization follows the same pattern spec-kit uses in plan-template.md where Technical Context, Constitution Check, and Phase outputs are structurally separated.

- **The "no new recommendations" constraint (FR-015.5) enforces scope discipline.** This is analogous to spec-kit's principle that specs define the WHAT and WHY, not the HOW. The arbiter resolves existing positions rather than introducing new ones, keeping the deliberation record closed and auditable.

- **Backward compatibility is a first-class design constraint, not an afterthought.** FR-005 and SC-004 explicitly require that omitting the arbiter field produces identical output. This matches spec-kit's approach where every extension (presets, custom commands) is additive and never changes the default behavior of the core workflow.

---

## Missed Opportunities

1. **No structured output format for downstream SDD consumption.** The spec requires `resolution.md` to contain specific sections (Process Note, Decision Framework, Binding Decisions, Summary of Changes Required) but does not define a machine-parseable structure within those sections. When a user runs `/speckit.specify --input {output}/summary/final.md` after a conversus run, the specify command must extract requirements, entities, and acceptance criteria. If binding decisions are buried in free-form prose, the specify command cannot reliably extract the arbiter's rulings. Consider requiring structured markers (e.g., `<!-- RULING: dispute-id -->` ... `<!-- /RULING -->`) or a YAML front matter block in the resolution that lists each dispute ID, ruling, and required change in a parseable format.

2. **No linkage between binding decisions and the spec-kit requirements they modify.** The spec requires "Required changes" in each ruling but does not require that those changes reference specific FR-numbers, SC-numbers, or user story IDs from the target spec. If the target of a conversus run is a spec-kit spec (which the example `conversus.yml` shows it often is), every binding decision should trace to the specific requirement it modifies. Without this, implementing binding decisions requires a human to map "change X in the data model" back to "FR-003 needs to be rewritten."

3. **The trigger evaluation mechanism (FR-011) is fragile against template evolution.** The spec requires parsing `### Remaining Disputes` and finding `**Dispute:` entries. But it also states in Assumptions that "Phase 5 synthesis templates maintain the `### Remaining Disputes` heading convention across all future template revisions." This is a cross-template coupling that spec-kit would flag as a constitution violation -- the Phase 6 trigger depends on a specific formatting convention in a Phase 5 template, but there is no mechanism to enforce that convention. A spec-kit constitution would declare this as a structural invariant; the spec should elevate it from an assumption to a constraint with a validation mechanism (e.g., a template linting rule or a structured output format for Phase 5 that Phase 6 can reliably parse).

4. **No integration with spec-kit's checklist workflow.** After arbitration resolves disputes, the natural next step is to verify that the resolutions are implemented. Spec-kit's `/speckit.checklist` command generates verification checklists from specs and plans. The arbitration output should be consumable by the checklist workflow -- each binding decision's "Required changes" should generate a checklist item. The spec does not mention this integration path.

5. **The `arbiter.docs` field duplicates spec-kit's documentation pattern without leveraging it.** The arbiter configuration includes `docs` (optional) and `grounding` (required). In spec-kit, a constitution IS the grounding document, and the spec's docs are the supporting context. The spec could formalize this relationship: if the target of the conversus is a spec-kit project, `arbiter.grounding` SHOULD be the constitution path, and `arbiter.docs` SHOULD include the spec and plan. This convention would make the arbiter's decision framework self-documenting for spec-kit projects.

6. **The Confidence Assessment section in the template is unconnected to any success criteria.** The cooperative arbitration template requires a confidence table per ruling, but no success criterion or functional requirement addresses what happens when confidence is "Low." A Low-confidence ruling is functionally different from a High-confidence one -- it may warrant a follow-up conversus cycle or a flag for human review. The spec does not define any behavior based on confidence levels, making the field informational rather than actionable.

7. **No support for partial arbitration across multiple target files.** The spec supports multiple target files (`target` as a list), but the arbiter produces a single `resolution.md`. When a conversus runs against 6 target files (as in the speckit-orchestrator example), disputes may cluster around specific files. The resolution does not require per-file attribution, making it hard to apply rulings surgically. If one file's disputes are resolved but another file's are not, the entire resolution must be read end-to-end.

8. **Non-cooperative mode templates exist but the spec bans their use.** The repo already contains `templates/winner-take-all/arbitration.md`, `templates/prisoners-dilemma/arbitration.md`, and `templates/red-blue/arbitration.md` -- fully fleshed out templates with mode-appropriate vocabulary (verdict review, boundary disputes, risk disputes). Yet FR-004 and the Constraints section explicitly limit arbitration to cooperative mode. The spec should acknowledge these templates exist, explain their status (draft/experimental/future), and define what validation error they trigger if someone tries to use them today.

---

## Off-Base Assumptions

1. **"Subject arbitration is only meaningful when the deliberation agents represent external perspectives and the subject has its own distinct operational perspective."** This assumption is too narrow. In spec-kit workflows, the subject is often a spec document, not a system with an operational perspective. A spec does not "know" things that reviewers do not -- it IS the artifact being reviewed. The meaningful distinction is not external-vs-internal perspective but rather authority-to-decide vs. authority-to-advise. A project owner running a conversus on their own spec would be the arbiter not because they have hidden operational knowledge, but because they have decision authority over scope and priority tradeoffs. The spec should reframe this assumption around decision authority rather than information asymmetry.

2. **"Phase 5 synthesis templates maintain the `### Remaining Disputes` heading convention across all future template revisions."** This is stated as an assumption but is actually a hard dependency. If the heading changes, Phase 6 trigger evaluation breaks silently (defaulting to "run" per FR-012, which masks the breakage). Treating a hard dependency as an assumption creates a latent failure mode. This should be a constraint with a validation mechanism, not an assumption about future template authors' behavior.

3. **"The grounding document exists on disk at the configured path before the conversus run starts."** This is correct for the validation case (FR-003 checks the path), but does not account for the case where the grounding document changes during a long-running conversus. If a multi-iteration conversus takes significant time, and the grounding document is modified mid-run (e.g., by another developer or by a concurrent spec-kit workflow), the arbiter could cite a version of the document that differs from what was validated at config parse time. This is an edge case, but the spec should state whether the grounding document is read once (at Phase 6 start) or whether it is expected to be stable for the duration of the run.

---

## Actionable Recommendations

### P1 -- Required for correctness

1. **Add a structured machine-readable block to the arbitration output format.** Require that `resolution.md` includes a YAML front matter or a fenced code block at the end with a structured summary: each dispute ID, its ruling (adopt-A, adopt-B, compromise, unresolved), the grounding citation key, and the required change as a one-line action. This allows `/speckit.specify --input` and automated tooling to extract rulings without parsing prose. Add this to FR-018. *(Addresses Missed Opportunity #1)*

2. **Require binding decisions to reference target-document identifiers when the target is a spec-kit spec.** When `Required changes` refers to a spec element, it must cite the FR-number, SC-number, or user story ID. Add a template instruction: "If the target documents contain numbered requirements (e.g., FR-001, SC-001), your Required changes MUST reference the specific requirement identifiers affected." Add to FR-015 or FR-019. *(Addresses Missed Opportunity #2)*

3. **Elevate the `### Remaining Disputes` heading convention from an assumption to a constraint with enforcement.** Move the heading convention out of the Assumptions section. Add a new constraint: "The Phase 5 synthesis template for any mode that supports arbitration MUST contain a `### Remaining Disputes` section with `**Dispute:` entries as the parseable marker. Template authors MUST NOT rename this section." Optionally, add a template validation step that checks for the heading's presence during template loading (Step 3 in SKILL.md). *(Addresses Missed Opportunity #3 and Off-Base Assumption #2)*

4. **Define behavior for Low-confidence rulings.** Add to FR-018 or create a new FR: "When a binding decision has confidence 'Low', the resolution MUST include a `Requires follow-up:` field specifying what additional information or process would raise confidence." This makes Low confidence actionable rather than merely informational. *(Addresses Missed Opportunity #6)*

### P2 -- Required for design integrity

5. **Acknowledge the non-cooperative arbitration templates and define their status.** Add a section to the spec or to the Constraints section: "Arbitration templates exist for winner-take-all, prisoners-dilemma, and red-blue modes. These are draft templates prepared for future extension. In this release, configuring `arbiter` on a non-cooperative mode triggers a validation error (FR-004). Enabling arbitration for other modes requires a separate spec that analyzes the game-theoretic implications." This prevents confusion about the templates' presence. *(Addresses Missed Opportunity #8)*

6. **Add a convention for spec-kit projects: arbiter.grounding SHOULD be the constitution.** Add a non-normative note or a new user story: "When the target of a conversus is a spec-kit project, the recommended configuration is `grounding: .specify/memory/constitution.md`. This aligns the arbiter's decision framework with the project's governing principles as established by `/speckit.constitution`." This does not change validation -- it provides guidance that makes the two systems composable. *(Addresses Missed Opportunity #5)*

7. **Reframe the information-asymmetry assumption around decision authority.** Replace the current assumption ("Subject arbitration is only meaningful when deliberation agents represent external perspectives...") with: "Subject arbitration is meaningful when the arbiter has both decision authority over the target artifact and a declared grounding document that constrains that authority. The grounding document -- not the arbiter's perspective -- is the mechanism that makes rulings legitimate." This broadens applicability to spec-kit workflows where the subject is a document, not a running system. *(Addresses Off-Base Assumption #1)*

### P3 -- Recommended improvement

8. **Add per-file attribution in binding decisions when multiple targets are used.** Add a template instruction to FR-015: "When the conversus has multiple target files, each binding decision's Required changes MUST specify which target file is affected." This enables surgical application of rulings to specific spec files, plans, or data models without reading the entire resolution. *(Addresses Missed Opportunity #7)*

9. **Define a checklist output format for binding decisions.** Add an optional output: alongside `resolution.md`, the arbiter MAY produce a `resolution-checklist.md` with one checkbox item per Required change. This integrates with spec-kit's `/speckit.checklist` workflow and gives implementers a trackable list. Alternatively, define the structured block from recommendation #1 such that `/speckit.checklist` can consume it directly. *(Addresses Missed Opportunity #4)*

10. **Add a note about grounding document stability during long runs.** Add to Assumptions or Constraints: "The grounding document is assumed to be stable for the duration of the conversus run. If the document may change during execution (e.g., in a shared repository), the user should ensure no concurrent modifications occur during the run." This acknowledges the edge case without adding implementation complexity. *(Addresses Off-Base Assumption #3)*

---

## Referenced Documentation

| Document | Path | Relevance |
|----------|------|-----------|
| Subject Arbitration Spec | `conversus/specs/001-subject-arbitration/spec.md` | Primary review target |
| Conversus SKILL.md | `conversus/SKILL.md` | Framework orchestration logic, Phase 6 integration |
| Cooperative Arbitration Template | `conversus/templates/cooperative/arbitration.md` | Phase 6 prompt template for cooperative mode |
| Winner-Take-All Arbitration Template | `conversus/templates/winner-take-all/arbitration.md` | Draft template for future mode extension |
| Prisoner's Dilemma Arbitration Template | `conversus/templates/prisoners-dilemma/arbitration.md` | Draft template for future mode extension |
| Red-Blue Arbitration Template | `conversus/templates/red-blue/arbitration.md` | Draft template for future mode extension |
| Example Config | `conversus/conversus.example.yml` | Arbiter configuration example |
| Spec-Kit README | `spec-kit/README.md` | SDD philosophy, workflow stages, CLI reference |
| Spec Template | `spec-kit/templates/spec-template.md` | Spec structure requirements, quality checklist criteria |
| Plan Template | `spec-kit/templates/plan-template.md` | Plan structure, constitution check pattern |
| Specify Command | `spec-kit/templates/commands/specify.md` | Downstream consumer of conversus output via `--input` |
| Plan Command | `spec-kit/templates/commands/plan.md` | Downstream consumer for technical planning |
