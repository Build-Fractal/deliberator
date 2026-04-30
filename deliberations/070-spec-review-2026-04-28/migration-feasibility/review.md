### Executive Summary

Spec 070 proposes a three-phase implementation plan to migrate constitutional principles VI, X, and XVI to operational guidance following audit failures against the v2.4.0 Constitutional Inclusion Criteria gate. From an implementation feasibility perspective, the spec significantly underestimates the complexity and cost of executing these migrations. The proposed "easiest first" ordering is incorrect, the migration targets are inconsistently available (CONTRIBUTING.md doesn't exist), and the verification requirements impose a substantial engineering burden not reflected in the planning. The spec treats these as simple file moves when they are actually multi-document edits with cross-reference maintenance and dual-verification overhead.

Most critically, the spec fails to account for the verification methodology requirements established in spec 067, creating an implementation plan that promises "clean migration" while requiring both self-consistency AND blind verification deliberations for each constitutional edit.

### Alignment

- **Clear scope boundaries** (L10, L36-42): The spec correctly limits itself to audit/planning without performing migrations, respecting the separation between governance-meta specs and amendment implementation. This aligns with engineering best practices of separating design from implementation phases.

- **Risk identification in §5.2** (L125-133): The risk register correctly identifies cross-reference breakage for XVI and enforcement weight loss for migration targets. These are genuine implementation hazards that would cause production issues if not mitigated during execution.

- **Success criteria documentation** (L134-143): §5.3 provides concrete completion criteria including cross-reference updates and CONSTITUTIONAL_CONVERSATIONS.md logging, establishing clear engineering acceptance criteria for each migration.

- **Verification protocol acknowledgment** (L140, L160-163): The spec correctly recognizes that implementation PRs require spec 067 §4 verification artifacts, showing awareness that constitutional amendments cannot merge without deliberation approval.

### Missed Opportunities

- **Migration target validation**: The spec proposes CONTRIBUTING.md as the VI migration target (L66, L121) without confirming the file exists. Repository analysis shows CONTRIBUTING.md is missing, making this a non-viable target that would require file creation before migration. **Impact: medium** - the "easiest first" ordering becomes invalid when the target doesn't exist.

- **Verification cost estimation**: The spec mentions "spec 067 §4 verification artifacts" (L140) but doesn't acknowledge that spec 067 requires BOTH self-consistency AND blind verification for every constitutional amendment. Each verification costs ~17 launches, meaning XVI Option A (refactor in place) requires ~34 launches plus re-verification if ACCEPT-level findings emerge. **Impact: high** - cost estimates are 3-4x higher than implied.

- **Cross-reference impact analysis**: While §5.2 mentions VII cross-references to XVI (L132), the spec doesn't catalog the full cross-reference web. Implementation requires scanning CONSTITUTION.md, all specs, and related documentation for references to migrated principles. **Impact: medium** - implementation PRs will discover additional cross-references not anticipated in the plan.

- **CI lint feasibility assessment**: The spec proposes CI hooks for mechanically-checkable subsets (L129, L173) but doesn't confirm which subsets are actually automatable. The `skills/`, `presets/`, `templates/` directory check mentioned for VI only works if those directories exist - repository analysis shows no `skills/` directory. **Impact: medium** - proposed mitigations may not be implementable.

- **Document creation requirements**: For X migration to `docs/output-conventions.md` (L86, L122), the spec assumes document creation is trivial but doesn't account for cross-linking, navigation updates, or integration with existing docs structure. **Impact: low** - additional integration work required.

- **Re-verification trigger awareness**: Spec 067 §4.4 requires re-verification after any ACCEPT-level fixes are applied. The spec doesn't budget for this possibility, which could double verification costs if fixes are needed. **Impact: high** - actual implementation cost could be 50-100% higher than planned.

### Off-Base Assumptions

- **"Easiest first" ordering assumption** (L119-124): The spec assumes VI migration to CONTRIBUTING.md is the simplest path, but CONTRIBUTING.md doesn't exist. Creating the file, establishing its structure, and integrating it with repository navigation is more complex than XVI Option A (refactor in place), which only requires headline editing. The ordering should be reversed.

- **"Clean migration" characterization** (L121): The spec describes VI as having "minimal side effects" when it actually requires creating a new authoring conventions framework, establishing cross-references from CONSTITUTION.md Governance, and potentially creating CI enforcement - this is infrastructure work, not a file move.

- **XVI Option A as "careful editing"** (L123): The spec treats Option A (headline refactor) as high-stakes because of cross-references, but editing existing principle text while preserving enforcement clauses is actually lower risk than creating new operational guidance documents and maintaining cross-references between constitution and external files.

### Actionable Recommendations

1. **Reverse migration ordering** (Priority: P1)
   - **Current state**: §5.1 L121-123 orders VI first as "lowest contention" with XVI last as "highest contention."
   - **Proposed change**: Order XVI Option A first (headline refactor only), X second (new doc creation), VI last (requires CONTRIBUTING.md creation + authoring conventions framework).
   - **Rationale**: XVI Option A is a single-file edit preserving existing enforcement clauses; VI requires creating infrastructure that doesn't exist.
   - **Risk if ignored**: Implementation PRs will fail on VI due to missing target file, invalidating the "prove methodology with easy cases first" approach.

2. **Acknowledge CONTRIBUTING.md creation requirement** (Priority: P1)
   - **Current state**: L66 proposes "CONTRIBUTING.md (or a new top-level docs/authoring-conventions.md if CONTRIBUTING.md does not yet have an 'authoring conventions' section)."
   - **Proposed change**: "CONTRIBUTING.md does not exist in this repository. VI migration requires creating CONTRIBUTING.md with authoring conventions structure, or alternatively creating docs/authoring-conventions.md."
   - **Rationale**: Repository analysis shows no CONTRIBUTING.md file. Implementation planning must account for file creation overhead.
   - **Risk if ignored**: VI implementation PR will fail immediately due to missing target file.

3. **Document verification methodology costs** (Priority: P1)
   - **Current state**: L140 mentions "spec 067 §4 verification artifacts" without elaboration.
   - **Proposed change**: "Each constitutional edit requires both self-consistency and blind verification per spec 067 §4, costing ~34 launches per principle migration. Re-verification after ACCEPT-level fixes adds additional cost."
   - **Rationale**: Spec 067 §4.1 mandates both methodologies; §4.4 requires re-verification after fixes. Engineering estimates must reflect actual requirements.
   - **Risk if ignored**: Implementation effort will be 3-4x higher than expected, potentially blocking migration execution.

4. **Clarify XVI Option A viability** (Priority: P2)
   - **Current state**: L109-112 presents Option A as "preferred" but L123 treats it as "highest contention" requiring "careful editing."
   - **Proposed change**: "XVI Option A (headline refactor) requires single-principle edit while preserving enforcement clauses, making it lower risk than VI/X which require new document creation and cross-reference establishment."
   - **Rationale**: In-place edits that preserve enforcement substrate are lower risk than multi-document coordination.
   - **Risk if ignored**: Implementation ordering will be suboptimal, making easier tasks appear harder than they are.

5. **Add cross-reference discovery task** (Priority: P2)
   - **Current state**: §5.3 L141 mentions "cross-references from other principles, specs, and skills point at the new location" as a success criterion.
   - **Proposed change**: Add preliminary task: "Before implementation, scan CONSTITUTION.md, specs/, deliberations/, and docs/ for all references to VI/X/XVI to establish complete cross-reference maintenance checklist."
   - **Rationale**: Cross-reference updates are implementation-critical and must be discovered before migration begins, not during.
   - **Risk if ignored**: Implementation PRs will have incomplete cross-reference updates causing broken internal links.

6. **Specify CI lint feasibility constraints** (Priority: P2)
   - **Current state**: L129 proposes "CI hook that flags new .md files in skills/, presets/, templates/ directories."
   - **Proposed change**: "CI hook feasible for presets/ and templates/ directories (verified present). No skills/ directory exists, so VI mechanically-checkable enforcement requires different approach."
   - **Rationale**: Repository analysis shows skills/ doesn't exist. Proposed mitigations must be grounded in actual repository structure.
   - **Risk if ignored**: Proposed enforcement mitigations will fail to implement, leaving operational guidance without automation backing.

7. **Add document integration checklist for new files** (Priority: P3)
   - **Current state**: L86 proposes creating "docs/output-conventions.md" without integration requirements.
   - **Proposed change**: Add requirement: "New docs require navigation integration (mkdocs.yml updates), cross-linking from relevant existing docs, and index updates."
   - **Rationale**: Creating isolated documents without navigation integration reduces discoverability and violates documentation best practices.
   - **Risk if ignored**: Migrated operational guidance will be poorly discoverable, undermining enforcement effectiveness.

8. **Consolidate migration targets** (Priority: P3)
   - **Current state**: VI → CONTRIBUTING.md, X → docs/output-conventions.md, XVI design intent → docs/optimization-design-intent.md or CONTRIBUTING.md section.
   - **Proposed change**: Standardize on CONTRIBUTING.md sections for all operational guidance to reduce fragmentation: "Authoring Conventions," "Output Conventions," "Design Intent."
   - **Rationale**: §7 L174 identifies fragmentation as a risk; consolidation into single file reduces maintenance overhead.
   - **Risk if ignored**: Operational guidance will scatter across multiple files, making maintenance harder and discovery less predictable.

### Referenced Documentation

- `specs/070-grandfathered-audit/spec.md` — sections/lines cited: L10, L36-42, L66, L86, L109-112, L119-124, L129, L140, L141, L174
- `specs/067-verification-methodology/spec.md` — sections/lines cited: L45-51, L93-105
- Repository structure analysis — CONTRIBUTING.md (missing), docs/ (exists), skills/ (missing), presets/ (exists), templates/ (exists)