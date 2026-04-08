# Scope-Boundary Review — Phase 2 Gate (Spec 005)

**Reviewer**: scope-boundary
**Date**: 2026-03-20
**Spec**: 005-p2p3-backlog-hardening
**Gate**: Phase 2 (Two-Tier Status Convention)
**Tasks Under Review**: T006, T007

---

### Executive Summary

Phase 2's scope is narrow and well-defined: T006 adds the two-tier acceptance convention to the STATUS.md taxonomy section, and T007 applies acceptance labels to all four existing specs. Both tasks are marked complete. The deliverable — `specs/STATUS.md` — is the only file that Phase 2 modifies, and the current state of that file reflects exactly the taxonomy definitions (FR-012) and per-spec acceptance labels (FR-013, FR-009) that the spec requires.

The STATUS.md produced by Phase 2 is clean from a scope-boundary perspective. The taxonomy section (L5-24) defines both tiers without introducing terminology beyond what FR-012 specifies. The per-spec entries (L30-49) apply acceptance labels consistently. The "Interpreting the Two Tiers" section (L22-24) is one paragraph of necessary clarification — it explains orthogonality, which is the single non-obvious property of a two-dimensional status system, and does not bloat into a tutorial or guide. No Phase 3 content (subsystems, dependencies, risk, effort, structure plan) has leaked into the current STATUS.md. No SKILL.md modifications were made. Phase boundaries are intact.

My most important recommendation: the "Not started" acceptance label used for spec 003 (L41) is not defined in the taxonomy section and is not part of FR-012's two-tier convention — it must either be added to the taxonomy or replaced with a label that is defined there.

---

### Alignment

- **Two-tier taxonomy placement** (STATUS.md L5-21, tasks.md L44): T006 placed the acceptance tier definitions in the Taxonomy section of STATUS.md, directly below the existing implementation tier. This is the correct location — FR-012 (`spec.md` L225) requires the convention to be "established and documented," and the Taxonomy section is where status conventions live. The taxonomy is authoritative as required by the Phase 2 checkpoint (`tasks.md` L47).

- **Spec 001 acceptance label with gaps** (STATUS.md L31-33, spec.md L226): T007 labels spec 001 as "Feature-complete" with exactly the three gaps FR-013 mandates: FR-023 (with the "template-level heading instructions pending" qualifier), FR-025, and FR-026. The gaps text matches the spec nearly verbatim. [`spec.md` L226; `tasks.md` L45]

- **Spec 002 acceptance label** (STATUS.md L36): Spec 002 is labeled "Spec-complete," which is correct — all 36 FRs are represented in SKILL.md and the spec's acceptance criteria are met. This satisfies FR-009's requirement that all status labels use the two-tier convention. [`tasks.md` L45 — "Apply acceptance labels to specs 002, 003, 004 as well"]

- **No SKILL.md modifications** (STATUS.md only): Phase 2 touched only `specs/STATUS.md`. SKILL.md was not modified. This is correct — T006 and T007 are taxonomy-and-labeling tasks. SKILL.md modifications belong exclusively to Phase 4 (T013-T015, T019). [`tasks.md` L74-93]

- **No Phase 3 content leakage** (STATUS.md L28-49): The per-spec entries contain status labels, gaps, dependency notes, and implementation notes — but no risk-of-gap statements (FR-016, Phase 3 T010), no effort estimates (FR-017, Phase 3 T011), no shared subsystem section (FR-008, Phase 3 T008), and no structure plan (FR-019, Phase 3 T012). Phase 3 content is absent, as it should be.

- **"Interpreting the Two Tiers" section is appropriately minimal** (STATUS.md L22-24): The section is one paragraph. It states the tiers are orthogonal, gives two concrete examples of independent tier combinations, and notes that dependencies are also orthogonal. This is the minimum explanation needed for a two-dimensional system and does not duplicate material that belongs in a user guide or separate document.

---

### Missed Opportunities

- **Undefined "Not started" acceptance label**: STATUS.md L41 labels spec 003's acceptance as "Not started," and L41 also uses "Not started" for spec 003's implementation tier. The implementation tier defines "Not started" (L13), but the acceptance tier (L17-20) defines only "Feature-complete" and "Spec-complete." FR-012 (`spec.md` L225) defines only those two tiers. A spec with zero acceptance criteria satisfied needs a label, but that label is currently undocumented in the taxonomy. This creates exactly the labeling ambiguity FR-012 was designed to prevent. **Impact: high.** [`spec.md` L225; STATUS.md L17-20]

- **Spec 004 acceptance label ambiguity**: STATUS.md L46 labels spec 004's acceptance as "Feature-complete," but the entry describes a split: core (FR-001-021) is implementation-complete, discovery (FR-022-024) is not started. The acceptance label applies to the spec as a whole. If "Feature-complete" means "all major capabilities present but AC gaps remain," that is defensible — core is present, discovery is a gap. But the entry does not state which acceptance criteria are unmet. FR-013 explicitly requires "documented gaps" for spec 001; FR-009 requires the two-tier convention for all specs. Consistency would demand gap documentation for spec 004 as well. **Impact: medium.** [`spec.md` L216, L225-226]

- **No explicit mapping from FR-012 terms to taxonomy text**: FR-012 (`spec.md` L225) defines "feature-complete" with a parenthetical: "(all major capabilities present, acceptance criteria gaps remain)." The taxonomy (STATUS.md L19) uses nearly identical but not exact wording: "All major capabilities are present, but acceptance criteria gaps remain (e.g., missing template instructions, incomplete edge case documentation)." The "(e.g., ...)" addendum is not in FR-012. While helpful, it introduces examples that could be read as constraining the definition. A strict reading of the scope-boundary mandate ("convention must match the spec exactly — no embellishments") flags this. **Impact: low.** [`spec.md` L225; STATUS.md L19]

- **Spec 005 is absent from STATUS.md**: The Phase 1 final synthesis (`gates/phase-1/summary/final.md` L279) explicitly noted: "Spec 005 must track itself in STATUS.md to satisfy SC-003." The current STATUS.md has entries for specs 001-004 only. Task T012a in Phase 3 (`tasks.md` L68) is designated for this, so the omission is by-design for Phase 2. However, T007's description says "Apply acceptance labels to specs 002, 003, 004 as well" — it does not mention spec 005. If T007 is the task that applies acceptance labels, and spec 005 is a spec, T007's scope is arguably incomplete. This is a Phase 3 task (T012a), but the boundary could be cleaner if T007's description explicitly excluded spec 005 with rationale. **Impact: medium.** [`tasks.md` L45, L68; `spec.md` L279]

---

### Off-Base Assumptions

- **FR-012 defines exactly two acceptance labels**: The spec (`spec.md` L225) defines the two-tier convention as: "feature-complete" and "spec-complete." STATUS.md applies a third label — "Not started" — to spec 003's acceptance tier (L41). FR-012 does not define a "Not started" acceptance state. The implementation tier has "Not started" (STATUS.md L13), but the acceptance tier taxonomy (STATUS.md L17-20) only lists two labels. The current STATUS.md assumes "Not started" is an implicit acceptance-tier label because it is defined in the implementation tier, but the tiers are explicitly described as measuring "different dimensions" (STATUS.md L5). If they are truly orthogonal, labels from one tier do not automatically transfer to the other. This is not a catastrophic error, but it is a taxonomy gap that Phase 2 was specifically designed to prevent. [`spec.md` L225; STATUS.md L5, L13, L17-20, L41]

- **FR-009 scope matches FR-012/FR-013 scope**: FR-009 (`spec.md` L216) says "Status labels MUST use the two-tier convention defined in FR-012/FR-013." T007 (`tasks.md` L45) applies labels to specs 001-004. But FR-009 is under the "Cross-Spec Status Tracking (P2-3)" group, which belongs to US3, not US5. The task plan assigns FR-009 to T007 in Phase 2 (US5). This is pragmatically correct — you cannot apply labels before defining them — but it means Phase 2 partially satisfies a US3 requirement. The scope boundary is not violated because the work (labeling) naturally belongs here, but it is worth noting that FR-009 satisfaction is split: the labeling convention is applied in Phase 2, but FR-008's broader STATUS.md requirements (subsystems, dependencies, implementation order) that also use those labels are deferred to Phase 3. [`spec.md` L215-216; `tasks.md` L44-45, L59-68]

---

### Actionable Recommendations

1. **Add "Not started" to acceptance tier taxonomy** (Priority: P1)
   - **Current state**: STATUS.md L17-20 defines only "Feature-complete" and "Spec-complete" in the acceptance tier. Spec 003 (L41) uses "Not started" as an acceptance label.
   - **Proposed change**: Add `- **Not started**: No acceptance criteria have been evaluated. The spec's features are not yet implemented.` to the Acceptance Tier list (after "Spec-complete," L20).
   - **Rationale**: FR-012 (`spec.md` L225) requires a documented convention. Using an undocumented label in the same file that defines the convention contradicts the purpose of the convention. The Phase 1 synthesis convergence point 5 (`gates/phase-1/summary/final.md` L113) established that enumeration prevents ambiguity — the same principle applies to tier labels.
   - **Risk if ignored**: Spec 003's acceptance status uses a label that is not defined in the taxonomy it sits beneath. Any future reviewer applying the convention strictly will flag this as a gap, recreating the "labeling disagreement" FR-012 was designed to resolve.

2. **Document spec 004 acceptance gaps** (Priority: P2)
   - **Current state**: STATUS.md L46-48 labels spec 004 as "Feature-complete" but does not list which acceptance criteria are unmet, unlike spec 001 (L32) which lists specific FR gaps.
   - **Proposed change**: Add a `**Gaps**:` line to spec 004's entry identifying that discovery commands (FR-022-024) represent the acceptance criteria gap that prevents "Spec-complete" status.
   - **Rationale**: FR-009 (`spec.md` L216) requires labels to use the two-tier convention. FR-013 (`spec.md` L226) sets the precedent that "feature-complete" labels come with "documented gaps." Consistency across specs prevents the convention from being applied rigorously to some specs and loosely to others.
   - **Risk if ignored**: Spec 004's "Feature-complete" label lacks the same rigor applied to spec 001. An implementor reading STATUS.md would know spec 001's gaps precisely but would have to infer spec 004's gaps from the narrative text.

3. **Remove or justify "(e.g., ...)" examples in Feature-complete definition** (Priority: P3)
   - **Current state**: STATUS.md L19 includes "(e.g., missing template instructions, incomplete edge case documentation)" in the Feature-complete definition. FR-012 (`spec.md` L225) defines the label without examples.
   - **Proposed change**: Either remove the parenthetical to match FR-012 exactly, or add a brief justification that these are illustrative, not exhaustive (e.g., change to "...acceptance criteria gaps remain. Examples include missing template instructions or incomplete edge case documentation.").
   - **Rationale**: The scope-boundary mandate states "The convention must match the spec exactly — no embellishments." The examples are not in the spec. They are helpful but they are embellishments. If retained, they should be clearly marked as illustrative to prevent a reader from treating them as an exhaustive list of what constitutes "feature-complete."
   - **Risk if ignored**: Minor. A future reviewer could interpret the examples as constraining the definition. Low probability but inconsistent with the principle of matching the spec.

4. **Add explicit T007 exclusion note for spec 005** (Priority: P3)
   - **Current state**: T007 (`tasks.md` L45) says "Apply acceptance labels to specs 002, 003, 004 as well." Spec 005 is not mentioned. T012a (`tasks.md` L68) handles spec 005 in Phase 3.
   - **Proposed change**: Append to T007's description: "(Spec 005 entry deferred to T012a, Phase 3)."
   - **Rationale**: SC-003 (`spec.md` L265) requires "status of any spec" to be in STATUS.md. A reader of T007 might reasonably ask why spec 005 is missing. An explicit deferral note prevents that question and cleanly delineates the Phase 2/Phase 3 boundary for spec 005.
   - **Risk if ignored**: Minimal. T012a exists and will handle it. But without the note, the Phase 2 boundary for spec 005 is implicit rather than explicit.

5. **Verify Phase 2 checkpoint against FR-012 and FR-009 satisfaction** (Priority: P2)
   - **Current state**: The Phase 2 checkpoint (`tasks.md` L47) states: "Two-tier convention defined and applied to all 4 specs. STATUS.md taxonomy is authoritative." Both T006 and T007 are marked `[x]`.
   - **Proposed change**: Verify that (a) every acceptance label used in STATUS.md L28-49 is defined in the taxonomy section L15-20, and (b) every spec entry has both an implementation-tier and acceptance-tier label. If "Not started" is used for spec 003's acceptance, it must be in the taxonomy.
   - **Rationale**: The checkpoint claims the taxonomy is "authoritative." An authoritative taxonomy cannot have labels in use that it does not define. This is the same enumeration principle established in Phase 1 convergence (`gates/phase-1/summary/final.md` L113).
   - **Risk if ignored**: The checkpoint passes with a taxonomy gap (undocumented "Not started" acceptance label), undermining the authoritativeness claim.

6. **Confirm "Interpreting the Two Tiers" section does not exceed minimum-necessary scope** (Priority: P3)
   - **Current state**: STATUS.md L22-24 contains one paragraph explaining orthogonality with two examples and a note about dependency orthogonality.
   - **Proposed change**: No change needed. The section is minimal and necessary. Confirm it should remain as-is and flag if any future expansion is proposed — expansion belongs in a separate document, not in this section.
   - **Rationale**: The scope-boundary mandate states this section "must be minimal and necessary, not an over-explanation that belongs in a separate guide." The current content satisfies this constraint. The recommendation is to explicitly mark this as reviewed-and-approved so future phases do not inadvertently expand it.
   - **Risk if ignored**: None currently. Defensive recommendation to preserve scope cleanliness.

7. **Confirm no SKILL.md changes occurred in Phase 2** (Priority: P1)
   - **Current state**: Phase 2 tasks (T006, T007) target only `specs/STATUS.md`. SKILL.md modifications belong to Phase 4 (`tasks.md` L74-93).
   - **Proposed change**: Verify via git diff or file inspection that SKILL.md has not been modified since Phase 1 completed. If it has been modified, flag the modification as a phase boundary violation.
   - **Rationale**: The scope-boundary mandate explicitly states "Phase 4 writes edge cases, match semantics, overwrite semantics to SKILL.md." Any SKILL.md change during Phase 2 is a boundary violation regardless of intent.
   - **Risk if ignored**: If SKILL.md was inadvertently modified, Phase 4's assumptions about the file's baseline state could be wrong, leading to merge conflicts or incorrect edits.

---

### Referenced Documentation

- `conversus/specs/005-p2p3-backlog-hardening/spec.md` — sections/lines cited: L215-216 (FR-008, FR-009), L225-226 (FR-012, FR-013), L265 (SC-003), L278-279 (FR-011 assumption, spec 005 self-tracking)
- `conversus/specs/005-p2p3-backlog-hardening/tasks.md` — sections/lines cited: L34-47 (Phase 2 definition, T006, T007, checkpoint), L45 (T007 scope), L59-68 (Phase 3 tasks), L68 (T012a), L74-93 (Phase 4 tasks)
- `conversus/specs/STATUS.md` — sections/lines cited: L5-24 (taxonomy), L13 (implementation Not started), L17-20 (acceptance tier), L19 (Feature-complete definition), L22-24 (Interpreting section), L28-49 (per-spec entries), L31-33 (spec 001), L36 (spec 002), L41 (spec 003), L46-48 (spec 004)
- `conversus/specs/005-p2p3-backlog-hardening/gates/phase-1/summary/final.md` — sections/lines cited: L113 (enumeration convergence point), L279 (spec 005 self-tracking note)
