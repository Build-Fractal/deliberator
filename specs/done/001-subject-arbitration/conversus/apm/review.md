# APM Review: Subject Arbitration (Phase 6)

**Reviewer**: APM (Agent Package Manager)
**Spec**: `conversus/specs/001-subject-arbitration/spec.md`
**Date**: 2026-03-19
**Perspective**: Packaging, distribution, context compilation, agent primitives, and the SKILL.md-based skill execution model

---

## Executive Summary

The subject-arbitration spec proposes a well-motivated Phase 6 for the conversus framework that resolves a genuine gap: cooperative mode's inability to produce binding decisions from survived disputes. The design is structurally sound -- the grounding-document constraint, conditional trigger system, and scope limitations (disputes only, no new recommendations, no overturning convergence) form a coherent integrity mechanism. The template-per-mode extensibility model aligns with APM's own pattern of convention-based file discovery. However, the spec underspecifies several dimensions that matter from a packaging and distribution perspective: the arbiter configuration has no reuse or composition story, the grounding document is treated as a monolithic path rather than a composable context graph, and the relationship between conversus's SKILL.md execution model and APM's skill/primitive system is left entirely implicit. The spec also unnecessarily restricts arbitration to cooperative mode when the templates for all four modes are already written and ready, creating a contradiction between the spec's stated constraints and the delivered artifacts.

---

## Alignment

- **Template-per-mode convention is correct.** The decision to place `arbitration.md` in `templates/{mode}/` rather than a global location mirrors APM's own convention-based file discovery (`.apm/agents/`, `.apm/instructions/`, etc.). New modes get their own templates with no code changes. This is the right architectural call.

- **Grounding-document-as-citation-source is a strong integrity mechanism.** Requiring every ruling to cite a specific grounding document maps directly to APM's constitution injection pattern (`memory/constitution.md` injected at top of `AGENTS.md` during `apm compile`). Both systems solve the same problem: making an agent's decision framework legible and auditable.

- **The `{VARIABLE}` substitution model is consistent.** Phase 6 reuses the exact same template variable system as Phases 1-5, with well-chosen additions (`{ARBITER_NAME}`, `{GROUNDING_PATH}`, `{SYNTHESIS_PATH}`). No special-case parsing required. This preserves the clean separation between orchestration logic and prompt engineering that makes the framework extensible.

- **Backward compatibility is properly preserved.** The `arbiter` field is fully optional, omitting it produces identical Phase 1-5 behavior. This is the correct approach -- additive features should never break existing configurations.

- **Scope constraints are well-defined.** "No new recommendations" and "no overturning convergence" are precise, enforceable rules that prevent the arbiter from becoming an unconstrained override mechanism. The UNRESOLVED escape hatch for insufficient information is also correct -- forcing a ruling when evidence is lacking would undermine the grounding requirement.

- **The trigger evaluation with safe defaults is sound.** Defaulting to "run Phase 6" when the synthesis file cannot be parsed is the right failure mode -- better to run the arbiter unnecessarily than to silently skip it when disputes exist.

---

## Missed Opportunities

1. **No arbiter reuse or composition story.** The `arbiter` block is defined inline in `conversus.yml` with no mechanism for referencing a shared arbiter configuration. In a monorepo with multiple specs running conversus, the same subject (e.g., the orchestrator) would need its arbiter config duplicated across every `conversus.yml`. APM's dependency model (`apm.yml` dependencies, `apm_modules/`) already solves artifact reuse. The arbiter should be extractable as a named configuration that can be referenced across runs, analogous to how APM packages reference shared context files.

2. **Grounding document treated as a single file path, not a composable context graph.** APM's context linking system allows primitives to reference other context files via markdown links, creating composable knowledge graphs. The spec's `grounding` field accepts exactly one path. In practice, a system's decision framework is rarely a single document -- it might span a constitution, architecture decision records, and operational requirements. The spec should support a `grounding` list (like `docs`) or leverage APM's link resolution to allow the grounding document to reference other context files that get resolved at runtime.

3. **No integration with APM's SKILL.md frontmatter model.** Conversus is itself packaged as a SKILL.md with frontmatter (`name`, `description`, `compatibility`, `allowed-tools`). The arbiter configuration introduces what is effectively a new agent primitive type -- a post-synthesis decision-maker with a grounding constraint. This concept has no representation in APM's primitive taxonomy (agents, instructions, skills, context, hooks). An `.arbiter.md` or `.arbiter.yml` primitive type, discoverable by APM and deployable across projects, would make subject arbitration a first-class packaging concept rather than an inline config block.

4. **The cooperative-only restriction contradicts the delivered templates.** The spec states "Cooperative mode only for initial release" (Constraints section) and FR-004 enforces this with a validation error. Yet all four mode templates (`cooperative/arbitration.md`, `winner-take-all/arbitration.md`, `prisoners-dilemma/arbitration.md`, `red-blue/arbitration.md`) are already written, reviewed, and ready. The templates demonstrate that arbitration semantics differ per mode (dispute resolution vs. verdict review vs. boundary assignment vs. risk assessment). Shipping the templates but blocking their use creates dead code and delays value delivery for non-cooperative modes.

5. **No versioning or migration path for the `conversus.yml` schema.** Adding `arbiter` as a top-level field is the first schema extension documented in the spec. There is no `version` or `schema` field in `conversus.yml` to distinguish configs that support arbitration from those that do not. APM's `apm.yml` has a `version` field for exactly this purpose. As conversus evolves, schema versioning will become necessary -- better to introduce it now with a low-cost `schema: 1` or `version: 2` field than to retrofit it later.

6. **The arbiter's `docs` field duplicates APM's context resolution.** The arbiter has `docs: [list of paths]` for supporting documentation, which is the same pattern as regular agents. But APM already has context linking (`*.context.md` files with automatic link resolution) that could provide richer, more maintainable documentation loading. The spec does not explore whether the arbiter's documentation could be managed through APM's existing context pipeline rather than raw path lists.

7. **No hook integration for Phase 6 lifecycle events.** APM supports lifecycle hooks (`PreToolUse`, `PostToolUse`, `Stop`, etc.) that run scripts at specific points during agent operations. Phase 6 introduces a new lifecycle moment (pre-arbitration, post-arbitration) with no hook points. A project might want to run validation scripts after arbitration (e.g., checking that every ruling has a grounding citation before accepting the output) or trigger downstream workflows (e.g., creating GitHub issues for each required change).

8. **`{ALL_DISPUTES}` variable naming is ambiguous in Phase 6 context.** In Phases 4-5, `{ALL_DISPUTES}` means "all dispute documents." In Phase 6, the same variable is reused but the arbiter is only supposed to address *remaining* disputes from the synthesis. The template handles this correctly through instructions, but a dedicated `{REMAINING_DISPUTES}` variable (parsed from the synthesis) would reduce prompt fragility and make the scope constraint machine-enforceable rather than instruction-dependent.

9. **No structured output format for machine consumption.** The arbitration output is a markdown file (`resolution.md`). The "Summary of Changes Required" section lists actionable changes, but there is no structured format (YAML frontmatter, JSON sidecar, or structured markdown convention) that downstream tools could parse programmatically. APM's `apm compile` and spec-kit's `/speckit.specify` would benefit from a machine-readable summary of rulings alongside the human-readable narrative.

---

## Off-Base Assumptions

1. **"Subject arbitration is only meaningful when the deliberation agents represent external perspectives and the subject has its own distinct operational perspective."** (Assumptions section) This is too narrow. Subject arbitration is also meaningful when the agents represent *internal* perspectives (e.g., backend, frontend, infra teams in a prisoners-dilemma mode) and the subject is the system that must integrate all of their work. The system-as-integrator has information none of the individual teams have: cross-cutting constraints, production behavior, and actual usage patterns. The assumption as written could be read as discouraging arbitration in scenarios where it would be highly valuable.

2. **"Phase 5 synthesis templates maintain the `### Remaining Disputes` heading convention across all future template revisions."** (Assumptions section) This is a fragile contract. The trigger evaluation (FR-011) depends on parsing a specific markdown heading and entry format (`**Dispute:`). If a future template revision changes this heading or entry format, the trigger silently breaks. This should be a formalized contract (documented in the template with a machine-readable marker, or enforced by a schema) rather than an implicit assumption about heading stability.

3. **The arbiter MUST NOT introduce new recommendations is presented as absolute.** While the constraint is sound for dispute resolution, there is a legitimate case for the arbiter to flag observations that no agent raised -- the spec acknowledges this in the template ("note it as an observation in the Confidence Assessment") but the spec's requirements section (FR-015.5, Constraints section) states "MUST NOT introduce new recommendations" without the observation escape valve. The template is more nuanced than the spec's formal requirements, creating a gap between the normative spec and the prescriptive template.

---

## Actionable Recommendations

### P1 -- Required for Correctness

1. **Reconcile the cooperative-only restriction with the delivered templates.** Either (a) remove FR-004 and enable all four modes from launch since the templates are already written and tested, or (b) remove the non-cooperative templates from the deliverable and note them as future work. Shipping templates that validation blocks is a consistency defect. *Recommendation*: Option (a) -- enable all modes. The templates are well-differentiated and the per-mode arbitration semantics are already designed.

2. **Formalize the `### Remaining Disputes` / `**Dispute:` contract.** Add a machine-readable marker to the synthesis template (e.g., `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->`) so that trigger evaluation does not depend on markdown heading text. Update FR-011 to reference the marker. This eliminates the fragile assumption about heading stability.

3. **Align the spec's "no new recommendations" constraint with the template's observation mechanism.** FR-015 item 5 says "NOT introduce new recommendations." The template says "note it as an observation in the Confidence Assessment, not as a ruling." The spec's formal requirements should explicitly carve out the observation exception to match the template. A recommendation that is labeled as an observation and explicitly excluded from the binding decisions section is not a new recommendation -- it is a signal for future deliberation.

### P2 -- Required for Design Integrity

4. **Support `grounding` as a list of paths, not just a single path.** Change FR-002 to accept `grounding` as either a string (single path) or a list of strings (multiple paths). The primary grounding document should be the first entry, with supplementary grounding documents following. The template's Decision Framework section already supports extracting "3-7 principles" -- these could naturally span multiple documents.

5. **Add a `schema` or `version` field to `conversus.yml`.** Introduce `schema: 1` (or `version: 1`) as an optional field with a default of `1`. This costs nothing now and prevents painful migration when the next schema-breaking change arrives. APM's `apm.yml` versioning is the precedent.

6. **Introduce `{REMAINING_DISPUTES}` as a Phase 6-specific template variable.** Parse the synthesis output to extract the remaining disputes section and expose it as a dedicated variable. This makes the arbiter's scope machine-defined rather than instruction-defined, reducing the chance that a poorly-behaved LLM ignores the "disputes only" constraint.

7. **Add hook points for Phase 6 lifecycle.** Define `pre-arbitration` and `post-arbitration` hook events in the conversus SKILL.md execution model, consistent with APM's hook system. At minimum, `post-arbitration` allows validation scripts to verify grounding citations before the output is accepted.

### P3 -- Recommended Improvement

8. **Design an arbiter extraction/reuse pattern.** Document a convention (not necessarily code) for extracting an `arbiter` block into a standalone file (e.g., `arbiter.yml` or `.apm/arbiters/my-system.arbiter.yml`) that can be referenced from `conversus.yml` via a path: `arbiter: ./arbiters/orchestrator.yml`. This is a documentation-level recommendation for now, with implementation deferred until multiple conversus runs per project become common.

9. **Add a machine-readable summary sidecar.** Alongside `resolution.md`, produce `resolution.summary.yml` containing the structured ruling data: dispute labels, rulings, grounding citations, confidence levels, and required changes. This enables downstream tooling (spec-kit's `/speckit.specify`, APM's compile pipeline, GitHub issue creation via gh-aw) to consume arbitration results programmatically.

10. **Expand the assumption about when subject arbitration is valuable.** Rewrite the fourth assumption to cover both external-perspective and internal-perspective scenarios. The current wording unnecessarily narrows the design's applicability and could discourage adoption in prisoners-dilemma and red-blue modes where it would be equally valuable.

---

## Referenced Documentation

| Document | Relevance |
|----------|-----------|
| `conversus/specs/001-subject-arbitration/spec.md` | Primary spec under review |
| `conversus/SKILL.md` | Conversus skill definition with Phase 6 execution model |
| `conversus/templates/cooperative/arbitration.md` | Cooperative mode arbitration template |
| `conversus/templates/winner-take-all/arbitration.md` | WTA mode arbitration template (exists but blocked by FR-004) |
| `conversus/templates/prisoners-dilemma/arbitration.md` | PD mode arbitration template (exists but blocked by FR-004) |
| `conversus/templates/red-blue/arbitration.md` | Red-Blue mode arbitration template (exists but blocked by FR-004) |
| `conversus/conversus.example.yml` | Example config showing arbiter block (commented out) |
| `apm/docs/src/content/docs/introduction/key-concepts.md` | APM primitive taxonomy, context linking, constitution injection |
| `apm/docs/src/content/docs/guides/skills.md` | APM skill packaging, distribution, and discovery model |
