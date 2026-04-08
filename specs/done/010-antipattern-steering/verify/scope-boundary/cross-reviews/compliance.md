# Cross-Review of compliance's Review — from scope-boundary

**Cross-reviewer**: scope-boundary
**Reviewing**: compliance's review of Spec 010 — Agent Antipattern Steering
**Date**: 2026-03-20

---

## Dangerous Contradictions

### 1. Priority disagreement on constitution Principle IV resolution

**compliance** rates the Principle IV / STATUS.md contradiction as **P1** (recommendation 2) and proposes amending the constitution directly — specifically rewriting Principle IV to remove the STATUS.md mandate and replace it with a derivation-from-speckit-artifacts instruction (compliance review, Actionable Recommendations #2: "Amend Principle IV to remove or qualify the STATUS.md mandate").

**scope-boundary** rates this as **P2** (recommendation 2) and proposes a narrower intervention: either adding an acknowledgment note to the Known Antipatterns section or adding a "When This Does NOT Apply" exclusion to the antipattern entry itself.

**Why this matters**: Amending Principle IV is a constitutional change. Constitution.md L201-204 specifies that amendments "require documentation of the change, rationale, and impact on existing specs" and follow a versioning scheme (MAJOR/MINOR/PATCH). Principle I (L24-29) states every behavioral change must start with a specification. Rewriting Principle IV as part of spec 010's implementation — a spec whose scope is explicitly "one catalog file, one SKILL.md instruction block" — would be a scope violation by the standard I enforce. The compliance review is correct that the contradiction exists and is real, but its proposed fix exceeds the scope of spec 010. The safe path is to flag the tension for a follow-up spec (as scope-boundary recommends) rather than performing a constitutional amendment inline.

**Resolution needed**: Both reviewers agree the contradiction is real. The disagreement is about the remedy's scope. Compliance should downgrade this to P2 (acknowledge + queue follow-up spec) or explicitly note that the proposed constitutional amendment requires its own spec per Principle I.

---

### 2. T006 traceability: implicit acceptance vs. explicit scope violation

**compliance** treats T006 (constitution Known Antipatterns update) as fully aligned, listing it under Alignment: "The constitution's 'Known Antipatterns' section references `antipatterns/catalog.md` and describes the SKILL.md enforcement mechanism, satisfying T006" (compliance review, Alignment section, bullet 6).

**scope-boundary** flags T006 as a scope-boundary concern: "The plan added T006 (constitution update) which goes beyond the spec's stated scope. The spec mentions only SKILL.md and templates (L109) as integration points" and notes "T006 has no spec-level traceability" (scope-boundary review, Missed Opportunities, bullet 3).

**Why this matters**: Compliance's review validates T006 as passing without acknowledging that the task has no spec-level acceptance scenario. This is a compliance gap, not a scope-boundary gap — compliance should flag that a checked-off task traces to no spec requirement. The compliance review's own Off-Base Assumptions section (bullet 1) notes the wrong example path but does not raise the T006 traceability issue at all. If compliance accepts T006 without traceability, it undermines the compliance framework's ability to catch future tasks that drift from spec.

**Resolution needed**: Compliance should either (a) note that T006 is not traceable to any spec requirement and flag this as a gap, or (b) explicitly justify why the constitution cross-reference is compliant despite spec.md L109 scoping integration to "SKILL.md or templates."

---

## Tensions

### 1. Broken example path: agreement on finding, tension on propagation scope

Both reviews identify the `specs/001-antipattern-steering/` vs. `specs/010-antipattern-steering/` path error and rate it P1. However, compliance's review is more thorough on propagation, noting the error appears in tasks.md T003 (L38), T011 (L77), and the catalog (compliance review, Off-Base Assumptions #2: "The `001` prefix appears to be a typo from early development. The tasks reference this same incorrect path... suggesting the error was present in the task definitions and propagated into the implementation").

Scope-boundary's review also notes the propagation (scope-boundary review, Missed Opportunities #2: "This same wrong path appears in tasks.md T003 (L38), T011 (L77), the plan (L63), quickstart.md, and research.md") and adds plan.md, quickstart.md, and research.md to the affected file list.

**Tension**: Compliance scopes the fix to catalog.md and tasks.md (recommendation 1). Scope-boundary lists plan.md, quickstart.md, and research.md as also affected. For a complete fix, all references need updating — but updating design-phase documents (plan.md, research.md, quickstart.md) is a judgment call. From a scope-boundary perspective, those are historical design artifacts; from a compliance perspective, T011's validation checkpoint itself has the wrong path, making it the critical fix. The tension is minor — compliance's recommended fix is necessary but not sufficient; scope-boundary's is comprehensive but includes design documents that may be treated as frozen records.

**Suggested resolution**: Fix catalog.md (runtime artifact) and tasks.md (implementation record) at minimum. Note plan.md and research.md paths as known errata without requiring fixes to historical design documents.

### 2. SC-001 and SC-002 measurability: different emphasis

**compliance** flags both SC-001 (zero repeated antipatterns) and SC-002 (<30s overhead) as "Not measurable" in the Requirement Verification Matrix and provides specific recommendations for both (recommendations 5 and 6). Compliance proposes defining measurement methods: post-deliberation review for SC-001, context-window-consumption reframing for SC-003.

**scope-boundary** does not flag SC-001 or SC-002 measurability. My review focuses on whether the implementation stayed within scope, not on whether success criteria are testable — testability is a compliance concern, not a scope concern.

**Tension**: This is not a conflict but a gap in scope-boundary's coverage. Compliance is correct to flag these as compliance gaps. From my perspective, the success criteria as written are part of the spec's scope definition, so they define the boundary. Whether they are measurable affects compliance's assessment but not the scope-boundary verdict: the implementation neither exceeds nor falls short of SC-001/SC-002 because those criteria are aspirational by design. The tension is that compliance wants the criteria strengthened, which would change the scope boundary for future verification passes.

**Suggested resolution**: Accept compliance's framing. SC-001 and SC-002 are compliance concerns, not scope violations. Both reviews are internally consistent on this point.

### 3. Recommendation density and prioritization

**compliance** provides 7 recommendations (2 P1, 3 P2, 1 P3, plus recommendation 6 which is P2). **scope-boundary** provides 7 recommendations (1 P1, 4 P2, 2 P3). There is high overlap on P1 (both flag the broken path), but compliance elevates the constitution amendment to P1 while scope-boundary keeps it at P2.

**Tension**: The prioritization difference on the constitution issue (P1 vs. P2) reflects the reviewers' different mandates. Compliance sees a MUST-level contradiction and wants it resolved before the spec is declared complete. Scope-boundary sees a contradiction that exists but requires its own spec to fix properly. Neither is wrong — the tension is between "fix the contradiction" (compliance) and "fix it in the right spec" (scope-boundary).

**Suggested resolution**: Resolve via the Dangerous Contradiction #1 above. The finding is agreed; only the remedy's scope is disputed.

---

## Safe Agreements

### 1. FR-001 through FR-010 implementation quality

Both reviews agree that functional requirements FR-001 through FR-010 are implemented, with the sole exception of FR-002/FR-004 being partially violated by the broken example path. Compliance's Requirement Verification Matrix marks FR-002 as "Partially implemented" and FR-001, FR-003, FR-004, FR-005 through FR-010 as "Implemented." Scope-boundary's Alignment section confirms data model fidelity, append-only structure, SKILL.md integration, and keyword retrieval.

**Agreement is safe**: Both reviews ground their assessment in the same artifacts (catalog.md, SKILL.md, data-model.md, catalog-format.md) and reach the same conclusions.

### 2. SKILL.md change is additive and correctly positioned

Both reviews agree the Antipattern Check instruction is correctly positioned (after Step 1, before Step 2), is purely additive, and matches the contract wording. Compliance cites SKILL.md L199-207 and catalog-format.md L89-103. Scope-boundary cites SKILL.md L199-207 and plan.md L29.

**Agreement is safe**: The SKILL.md change is the primary runtime integration point. Both reviews verify it independently against different source documents and reach the same conclusion.

### 3. Catalog structure matches the contract and data model

Both reviews verify that the catalog file at `antipatterns/catalog.md` matches the structure defined in catalog-format.md and the entity model in data-model.md. Compliance's field-by-field validation table (Catalog Entry Field Validation) and scope-boundary's data model fidelity bullet both confirm all required fields are present and correctly formatted, with the sole exception of the broken Example path.

**Agreement is safe**: The structural compliance is verified through different lenses (field-level validation vs. data-model alignment) and both converge.

### 4. Append-only and deprecation mechanisms are correctly documented

Both reviews confirm FR-009 (deprecation) and FR-010 (append-only) are satisfied. Compliance cites catalog.md L59-71. Scope-boundary cites catalog.md L59-71 and confirms no template modifications occurred.

**Agreement is safe**: The Maintenance section is a straightforward documentation artifact. Both reviews read it and agree it matches the spec.

### 5. The broken example path is the highest-priority fix

Both reviews identify the `specs/001-antipattern-steering/` path as the single most important defect. Both rate it P1. Both cite SC-004 and FR-004 as the violated requirements. Both confirm the correct path is `specs/010-antipattern-steering/examples/redundant-cache/`.

**Agreement is safe**: This is a factual finding with no interpretive ambiguity.

### 6. Constitution Known Antipatterns section is present and adequate

Both reviews confirm the Known Antipatterns section in constitution.md (L179-192) references the catalog and describes the SKILL.md enforcement mechanism. The disagreement (see Dangerous Contradiction #2) is about whether T006 has proper spec traceability, not about whether the content itself is correct.

**Agreement is safe**: The content quality of the constitution update is not disputed by either review.

---

## Summary Assessment

Compliance's review is thorough, well-structured, and provides the most detailed field-level verification of any reviewer. The Requirement Verification Matrix and Task Completion Verification tables are particularly valuable as permanent audit artifacts. The two dangerous contradictions identified above — priority on the constitution fix and T006 traceability — are resolvable through discussion rather than indicating fundamental methodological disagreement. The reviews are complementary: compliance verifies requirement-by-requirement conformance while scope-boundary verifies that the implementation boundary matches the spec boundary. Both find the same primary defect (broken path) and the same secondary concern (constitution contradiction), differing only on the appropriate remedy scope.
