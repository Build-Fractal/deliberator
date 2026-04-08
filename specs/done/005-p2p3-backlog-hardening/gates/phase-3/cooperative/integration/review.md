# Phase 3 Gate Review — Integration Checker

**Agent**: integration
**Date**: 2026-03-20
**Gate**: Phase 3 (STATUS.md Enrichment)
**Spec**: 005-p2p3-backlog-hardening
**Target**: `conversus/specs/STATUS.md`

---

### Executive Summary

Spec 005 Phase 3 transforms STATUS.md from a basic status tracker into a comprehensive cross-spec reference document. The phase adds six discrete enrichment tasks (T008-T012a) covering shared subsystems, cross-spec dependencies, risk-of-gap assessments, effort estimates, SKILL.md structure plans, and a self-referential spec 005 entry. My role as integration checker is to assess whether the resulting STATUS.md content is accurate, internally consistent, actionable for a new implementor, and correctly calibrated against the spec's own source material and Phase 2's taxonomy.

The current STATUS.md (L1-139) is well-structured and largely achieves its goal. The taxonomy section, shared subsystem entries, dependency graph, and structure plan are all present and substantively correct. The risk-of-gap and effort fields are populated for all five specs. The document uses Phase 2's taxonomy labels consistently. An implementor new to conversus could orient themselves from STATUS.md alone for most purposes, satisfying SC-003. However, several content accuracy issues and calibration gaps reduce the document's reliability as a single-source reference — the most significant being that the Dispute-Parsing Subsystem entry documents a known limitation (stagnation detection does not support structural-marker parsing) without connecting this to spec 002's "Spec-complete" label, creating a misleading confidence signal.

My most important recommendation: the Dispute-Parsing Subsystem shared subsystem entry must explicitly state that the heading-match semantics used by the fallback parser are not yet specified in the subsystem documentation, because this is the gap that Phase 4's T013 is designed to close, and an implementor reading STATUS.md needs to know this dependency exists before building on the subsystem.

### Alignment

- **Two-tier taxonomy application** (STATUS.md L7-24): The taxonomy section cleanly separates Implementation Tier and Acceptance Tier with three labels each, matching the Phase 2 deliberation outcome. The "Interpreting the Two Tiers" paragraph (L22-24) correctly states the tiers are orthogonal and provides the dependency example that prevents misinterpretation. This aligns with FR-012 (spec.md L225) and the Phase 2 final synthesis convergence point 3. `[tasks.md, L44-47]`

- **Shared Subsystem structure** (STATUS.md L86-104): The three shared subsystem entries (Dispute-Parsing, Structural Markers, Template Conventions) each specify Location, Stability, Consumers, Interface, and Notes — the exact fields T008 requires. The Interface descriptions for Dispute-Parsing (input/output/parsing rules) match FR-010's specification. `[tasks.md, L63]`

- **Dependency graph with rationale** (STATUS.md L106-129): The ASCII dependency graph and the recommended implementation order (001 -> 004 -> 002 -> 003) both match T009's specification. The rationale for ordering is clear: 001 is foundational, 004 is self-contained, 002 depends on 001, 003 depends on all three. The authoritative-source note at L129 correctly defers to per-spec "Depends On" fields. `[tasks.md, L64]`

- **Spec 005 self-entry** (STATUS.md L58-64): The spec 005 entry exists with implementation status, acceptance status, gaps, dependencies, notes, risk-of-gap, and effort. This satisfies SC-003's requirement that "any spec" is trackable from STATUS.md. The self-referential nature is handled cleanly without circular references. `[tasks.md, L68]`

- **Maintenance obligation** (STATUS.md L138): The maintenance note ("This document MUST be updated when any spec's implementation or acceptance status changes (FR-008a)") is present and cites the correct FR. This is a direct implementation of the FR-008a requirement from T008. `[tasks.md, L63]`

### Missed Opportunities

- **Dispute-Parsing heading-match gap not actionable**: STATUS.md L93 notes that "Heading-match semantics for the dispute-parsing fallback are not explicitly specified in the subsystem documentation." This is factually correct but not actionable — it does not tell the reader where the semantics will be specified, when, or what the current workaround is. The tasks.md (L88) specifies that T013 in Phase 4 will add these semantics. STATUS.md should cross-reference Phase 4's T013 so an implementor knows the gap has a scheduled fix rather than being an open-ended deficiency. Impact: **high** — an implementor building on the dispute-parsing subsystem has no way to know whether to wait for the fix or work around it. `[tasks.md, L86-88]`

- **Stagnation detection limitation not linked to spec 002 label**: STATUS.md L92 notes that "stagnation detection (spec 002) does not support structural-marker parsing — it uses only heading-based parsing." STATUS.md L38 labels spec 002 as "Implementation-complete" and "Spec-complete." These two facts are in tension: a "Spec-complete" spec has a documented limitation in a shared subsystem. STATUS.md does not connect these entries, so an implementor must cross-reference manually. The Phase 2 synthesis (final.md L82-84) explicitly recorded a post-condition to re-evaluate spec 002's label after Phase 4's T019. STATUS.md should carry this forward as a noted dependency. Impact: **medium** — the label is technically defensible (spec 002's own acceptance scenarios may not require marker-based parsing), but the silent tension erodes trust in the labels. `[tasks.md, L86]`

- **Effort estimates lack comparative anchor**: STATUS.md uses "Small," "None," "Large," "Small," "Small" for specs 001-005 respectively (L35, L42, L49, L56, L64). The spec (spec.md L151) requires estimates to cover "new files, logic complexity, testing surface, and relative effort." The current entries provide only the summary label and a brief justification, but no comparative anchor. For instance, spec 001 "Small" (2 FRs, template instructions) and spec 004 "Small" (3 FRs, CLI commands) are labeled identically despite different complexity profiles — one is template text, the other involves new subcommand routing. A single sentence establishing the scale (e.g., "Effort is relative to spec 003, the largest remaining deliverable") would make the labels more meaningful. Impact: **medium** — maintainers can still prioritize, but the identical "Small" labels for dissimilar work reduce the discriminating value of the field. `[tasks.md, L66]`

- **Risk-of-gap for spec 005 is self-referential without actionable consequence**: STATUS.md L63 states spec 005's risk-of-gap as "Documentation gaps persist in SKILL.md Phase 6 section (heading match semantics, missing document handling, overwrite behavior) and STATUS.md lacks complete cross-spec reference information." This describes what spec 005 delivers, not what happens if it is never delivered. Compare spec 003's risk (L48): "Users must manually configure conversus.yml for every deliberation" — this describes a concrete user-facing consequence. Spec 005's risk statement should follow the same pattern: "Implementors lack a single reference for cross-spec status, and SKILL.md Phase 6 edge cases remain undocumented, increasing the probability of inconsistent implementations." Impact: **medium** — the current statement is accurate but tautological; it describes the spec's deliverables rather than the cost of their absence. `[tasks.md, L65-66]`

- **SKILL.md Structure Plan lacks section-level specificity for spec 003**: STATUS.md L76-80 describes spec 003's structure plan as needing a "new Subcommand Dispatch section before Step 1," "entry point routing logic," and "Phase A/B/C orchestration." This is more specific than the other two entries but still does not identify which existing SKILL.md sections would be modified (as opposed to new sections added). The tasks.md (L67) requires the plan to identify "which existing sections change and what new sections are needed." For spec 003, the plan identifies only new sections. Does Step 1 (Parse Config) need modification for subcommand routing? Does Step 4 (Execute Phases) need modification for Phase A/B/C? These questions are left open. Impact: **low** — the plan is sufficient for advance planning but does not meet the full specificity required by FR-019. `[tasks.md, L67]`

- **No explicit statement that spec 004 discovery is a prerequisite for spec 003 Phase A**: STATUS.md L46 lists spec 004's dependency as "004 (soft dependency for `/conversus interests` preset suggestions)" under spec 003. STATUS.md L55-56 describes spec 004's discovery features as "Not started" and notes they become a "prerequisite when spec 003 Phase A enters development." These are in different sections and the connection is indirect. An implementor planning spec 003 Phase A would need to read both the spec 003 and spec 004 entries to discover this sequencing constraint. The dependency graph (L115) marks it as "soft" without noting the Phase A timing constraint. Impact: **low** — the information is present but distributed; consolidation would improve the document's function as a planning reference. `[tasks.md, L64]`

### Off-Base Assumptions

- **"STATUS.md lacks complete cross-spec reference information" (STATUS.md L63)**: This characterization in spec 005's own risk-of-gap statement is outdated. After Phase 3's completion (T008-T012a), STATUS.md does contain cross-spec reference information — shared subsystems, dependency graph, risk, effort, and structure plan are all present. The risk-of-gap field appears to have been written before Phase 3 work was done (or describes the pre-Phase-3 state), and was not updated after the Phase 3 enrichment tasks were completed. The correct characterization of the remaining gap is narrower: "STATUS.md lacks transition criteria for the acceptance tier and Phase 4 post-conditions are not tracked" — or the risk-of-gap should describe the cost of never implementing spec 005 at all (the pre-spec state), not the current partially-implemented state. `[STATUS.md, L63; tasks.md, L68]`

- **Spec 002 effort "None — complete" (STATUS.md L42) paired with T019 dependency**: STATUS.md marks spec 002's effort as "None" and its implementation as complete. However, Phase 4's T019 (tasks.md L86) modifies the Round Termination Check section of SKILL.md to replace inline dispute-counting with a cross-reference to the Dispute-Parsing Subsystem. This is a change that affects spec 002's implementation (stagnation detection uses the Round Termination Check). The effort field's "None" is accurate only if T019 is considered a spec 005 task, not a spec 002 task. This distinction should be made explicit — otherwise an implementor reading "None — complete. All 36 FRs implemented" will not anticipate that Phase 4 of a different spec (005) will modify a section their spec depends on. `[STATUS.md, L42; tasks.md, L86]`

### Actionable Recommendations

1. **Add Phase 4 cross-reference to Dispute-Parsing heading-match note** (Priority: P1)
   - **Current state**: STATUS.md L93 states "heading-match semantics for the dispute-parsing fallback are not explicitly specified in the subsystem documentation" with no remediation pointer.
   - **Proposed change**: Append to the sentence: "heading-match semantics for the dispute-parsing fallback are not explicitly specified in the subsystem documentation; Phase 4 task T013 (FR-007) will add explicit matching rules."
   - **Rationale**: An implementor building on the dispute-parsing subsystem needs to know whether the gap is scheduled for closure or is an open deficiency. The current note flags the problem without indicating a path to resolution. `[tasks.md, L88]`
   - **Risk if ignored**: Implementors may attempt to define their own heading-match semantics locally, creating exactly the divergent parsing implementations that FR-011 and SC-004 exist to prevent.

2. **Add spec 002 Phase 4 re-evaluation note** (Priority: P1)
   - **Current state**: STATUS.md L38 labels spec 002 as "Implementation-complete | Spec-complete" with no caveats. STATUS.md L92 notes a limitation in stagnation detection's parsing approach.
   - **Proposed change**: Add to spec 002's Notes field: "Phase 4 post-condition: after T019 replaces Round Termination Check's inline parsing with a Dispute-Parsing Subsystem cross-reference, re-evaluate the Spec-complete label against spec 002's acceptance scenarios."
   - **Rationale**: The Phase 2 final synthesis (final.md L82-84, P3 item 4) explicitly recorded this as a post-condition. STATUS.md should carry it forward so the obligation is not lost between phases. `[gates/phase-2/summary/final.md, L213-214]`
   - **Risk if ignored**: The spec 002 "Spec-complete" label may become inaccurate after Phase 4 changes without anyone noticing, because the re-evaluation trigger is buried in a Phase 2 synthesis document that implementors will not routinely read.

3. **Rewrite spec 005 risk-of-gap as cost-of-absence statement** (Priority: P2)
   - **Current state**: STATUS.md L63 states "Documentation gaps persist in SKILL.md Phase 6 section... and STATUS.md lacks complete cross-spec reference information."
   - **Proposed change**: Replace with: "Implementors lack a single reference for cross-spec status, shared subsystem stability, and dependency ordering, increasing the risk of building on incomplete or unstable foundations. SKILL.md Phase 6 edge cases (missing documents, overwrite behavior, heading match semantics) remain undocumented."
   - **Rationale**: Risk-of-gap should describe the consequence of the spec never being implemented, following the pattern established by specs 001-004. The current text describes deliverables, not consequences. `[tasks.md, L65; spec.md, L127-128]`
   - **Risk if ignored**: The risk-of-gap field loses its comparative value — maintainers cannot weigh spec 005's priority against other specs because its risk is stated differently from the others.

4. **Add comparative anchor to effort estimates** (Priority: P2)
   - **Current state**: STATUS.md L35, L42, L49, L56, L64 use "Small," "None," "Large," "Small," "Small" without an explicit scale definition.
   - **Proposed change**: Add a one-sentence preamble to the first effort field (spec 001, L35) or to the taxonomy section: "Effort is relative: Small = targeted edits to existing files; Medium = new sections or modest new functionality; Large = multiple new components with cross-cutting integration."
   - **Rationale**: FR-017 (spec.md L242) requires estimates to cover "relative effort (small/medium/large)." The labels are present but the scale is implicit. An explicit scale makes the labels meaningful to readers who were not part of the original estimation. `[tasks.md, L66; spec.md, L242]`
   - **Risk if ignored**: Effort labels become subjective judgments rather than calibrated estimates, reducing their utility for prioritization. Future spec entries may use "Small" or "Large" inconsistently.

5. **Specify which existing SKILL.md sections change for spec 003** (Priority: P2)
   - **Current state**: STATUS.md L76-80 lists only new sections needed for spec 003 (Subcommand Dispatch, entry point routing, Phase A/B/C orchestration, preset integration).
   - **Proposed change**: Add: "Existing sections modified: Step 1 (Parse Config) for subcommand-specific validation rules; Step 4 (Execute Phases) for `converge` subcommand's Phase A/B/C orchestration flow; Step 5 (Report) for subcommand-specific output formatting."
   - **Rationale**: FR-019 (spec.md L250) requires identifying "which existing sections change and what new sections are needed." The current plan covers only the latter. `[tasks.md, L67; spec.md, L250]`
   - **Risk if ignored**: Implementors starting spec 003 will discover modification requirements ad hoc, potentially causing structural conflicts with other in-progress changes to those SKILL.md sections.

6. **Add transition criteria as deferred Phase 3 obligation** (Priority: P2)
   - **Current state**: STATUS.md's taxonomy section (L7-24) defines labels but has no transition criteria for when a spec moves between acceptance tiers. The Phase 2 synthesis (final.md L200-202, P2 item 3) recorded a binding commitment that T008 would include dual-condition transition criteria.
   - **Proposed change**: Add after the "Interpreting the Two Tiers" paragraph (L24): "A spec transitions from feature-complete to spec-complete when (a) all documented gaps in its Gaps field are resolved and (b) all acceptance scenarios defined in its spec.md are verified as satisfied."
   - **Rationale**: The Phase 2 synthesis recorded this as a "binding commitment, not an optional suggestion" (final.md L171). T008's scope includes the taxonomy section's maintenance obligation (FR-008a), and transition criteria define when maintenance triggers a label change. `[gates/phase-2/summary/final.md, L152-156, L200-202]`
   - **Risk if ignored**: The boundary between "Feature-complete" and "Spec-complete" remains implicit. Different reviewers may apply different thresholds for relabeling, undermining the convention's purpose.

7. **Consolidate spec 004 discovery prerequisite timing** (Priority: P3)
   - **Current state**: The soft dependency between spec 004 discovery and spec 003 Phase A is split across two entries (STATUS.md L46, L55-56) and the dependency graph (L115).
   - **Proposed change**: In the spec 003 "Depends On" field, expand "004 (soft dependency for `/conversus interests` preset suggestions)" to: "004 (soft: `/conversus interests` preset suggestions — discovery features (FR-022-024) must be implemented before spec 003 Phase A)."
   - **Rationale**: A planning reference should make sequencing constraints visible in one place rather than requiring cross-referencing between entries. `[STATUS.md, L46, L55-56; tasks.md, L67]`
   - **Risk if ignored**: An implementor starting spec 003 Phase A without reading spec 004's entry may not realize the discovery prerequisite, leading to either blocked progress or a decision to skip preset integration.

8. **Update spec 002 effort field to note Phase 4 T019 dependency** (Priority: P3)
   - **Current state**: STATUS.md L42 states "Effort: None — complete. All 36 FRs implemented. No remaining work."
   - **Proposed change**: Append: "Note: spec 005 Phase 4 (T019) will modify the Round Termination Check section, which implements spec 002's stagnation detection. The change is a cross-reference replacement, not a behavioral change."
   - **Rationale**: The "No remaining work" statement is accurate for spec 002 in isolation but misleading when a downstream spec (005) plans to modify a section spec 002 depends on. Documenting the dependency preserves the accuracy claim while adding context. `[tasks.md, L86; STATUS.md, L42]`
   - **Risk if ignored**: An implementor may rely on the "No remaining work" statement and be surprised when Phase 4 modifies a section they considered stable, even though the modification is a documentation cross-reference rather than a behavioral change.

### Referenced Documentation

- `conversus/specs/STATUS.md` -- sections/lines cited: L7-24, L35, L38, L42, L46, L48, L49, L55-56, L58-64, L63, L76-80, L86-104, L92, L93, L106-129, L115, L138
- `conversus/specs/005-p2p3-backlog-hardening/spec.md` -- sections/lines cited: L127-128, L151, L225, L242, L250
- `conversus/specs/005-p2p3-backlog-hardening/tasks.md` -- sections/lines cited: L44-47, L63, L64, L65-66, L67, L68, L86, L86-88, L88
- `conversus/specs/005-p2p3-backlog-hardening/gates/phase-2/summary/final.md` -- sections/lines cited: L82-84, L152-156, L171, L200-202, L213-214
- `conversus/specs/005-p2p3-backlog-hardening/plan.md` -- sections/lines cited: L46-49 (structure), L72 (FR-011 gap analysis)
- `conversus/SKILL.md` -- sections/lines cited: L453-469 (Round Termination Check), L531-542 (Trigger Evaluation), L641-668 (Dispute-Parsing Subsystem)
