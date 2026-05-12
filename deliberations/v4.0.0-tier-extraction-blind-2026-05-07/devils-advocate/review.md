I'll read all the target files and then provide a devils-advocate review challenging the spec's strongest assumptions.

### Executive Summary

The tier extraction amendment proposes to split conversus-oss/CONSTITUTION.md into a 3-tier hierarchy, relocating 20 of 26 active principles to two higher-tier documents while claiming "byte-for-byte identical" preservation and mechanical verification via a linter. While the motivation for hierarchical organization is sound, the spec contains critical vulnerabilities in its core technical claims. The tier classification appears to have misclassified at least one principle, the verbatim preservation contract overlooks complex cross-reference dependencies, the proposed linter has fundamental detection gaps, and the monolithic implementation strategy creates unrecoverable failure modes. The spec treats mechanical relocation as trivial when it is fundamentally architectural surgery requiring much more sophisticated tooling and safeguards.

**Most important recommendation:** **ACCEPT-level finding** - The tier-coherence linter algorithm is insufficient for Constitutional Inclusion Criterion 1 because it can be trivially defeated by principle duplication patterns that preserve header/first-paragraph identity while duplicating substantial normative content.

### Alignment

- **Hierarchical organization motivation** (spec L15-25): The core problem is real — flat structure forces duplication/forking as the suite grows. This aligns with basic software architecture principles. [QUESTION.md, L9-15].

- **Grandfathering preservation** (spec L37): Smart to avoid re-applying Constitutional Inclusion Criteria to relocated principles — preserves validity while enabling structural refactoring. [CONSTITUTION.md, L2075-2091].

- **Monolithic implementation** (spec L291): Correctly identifies that partial application creates inconsistent state. Atomicity requirement is architecturally sound. [spec L291-292].

- **Cross-reference rewrite enumeration** (spec L110-124): Spec explicitly tackles the most obvious preservation challenge with documented patterns for path-prefix changes. Shows awareness of reference maintenance complexity. [spec L112-119].

### Missed Opportunities

- **MAJOR GAP: Complex cross-references** (spec L110-124): The spec only handles simple `Principle {Roman}` patterns but misses inline numbered references, governance section references, and Amendment record citations that appear throughout the current constitution. **Impact: high** — relocation will break undocumented reference types that the linter won't catch.

- **No rollback procedure** (spec L318): Claims "PR is reverted (not fixed forward)" but provides no verification that reversion actually restores consistency across all 3+ edited files. **Impact: medium** — implementation failure could leave permanently inconsistent state.

- **Linter false positive handling** (spec L188-191): Algorithm uses "normalized signature" matching but provides no escape hatch for legitimate shared content (Origin attributions, Amendment records) that could trigger false duplication alerts. **Impact: medium** — could block future legitimate amendments.

- **Cross-tier reference validation gaps** (spec L204-209): Check (c) validates that Tier matches principle-set but doesn't verify that cross-references maintain semantic meaning after relocation. **Impact: high** — could create valid paths to wrong content.

- **Version consistency timing** (spec L213-216): Check (d) validates version fields but doesn't specify timing relative to the monolithic PR merge, creating a race condition window. **Impact: low** — mostly cosmetic but violates stated atomicity.

- **Component-tier rationale gaps** (spec L80-92): Lists which principles stay but provides minimal justification for why XVII-XXI, XXVI are component-only vs XVI's mathematical content being suite-wide. **Impact: medium** — classification appears arbitrary without stronger rationale.

- **SIR preservation mechanics** (spec L150-151): Claims "All existing SIR comment blocks preserved" but doesn't specify how relative cross-references within preserved SIRs are updated when target principles relocate. **Impact: high** — breaks audit trail integrity.

### Off-Base Assumptions

- **"Header + first-paragraph" sufficiency** (spec L186-188): Assumes this signature uniquely identifies principles, but Principles XV and XXVII both start with registry-related content and could have overlapping opening paragraphs. The algorithm would miss substantial body duplication if headers diverge slightly.

- **"Cross-reference rewrites — patterns that actually appear"** (spec L110): Claims to handle all current patterns, but misses Amendment record subsections that cross-reference specific deliberation dates and findings that would become ambiguous post-relocation.

- **Atomic bundle assumption** (spec L291-318): Assumes all edits can be successfully applied in a single PR, but doesn't account for potential merge conflicts if the constitution is amended during the implementation window.

### Actionable Recommendations

1. **Construct defeating duplication pattern for linter** (Priority: P1)
   - **Current state**: Spec L185-191 claims header + first-paragraph matching detects cross-tier duplication.
   - **Proposed change**: Test the algorithm against a principle whose body content is substantially duplicated but whose header uses "XVI. Mathematical Transparency" vs "Mathematical Transparency Principle XVI" — same semantic content, different normalization.
   - **Rationale**: The normalization described (L188-189) would treat these as different signatures, missing genuine duplication. [spec L188-191]
   - **Risk if ignored**: Future amendments could accidentally duplicate principles across tiers without detection.

2. **Challenge XVI tier classification** (Priority: P1)  
   - **Current state**: Spec L73 classifies XVI as "Suite" but L27 claims it's "Specific to scoring + solver code."
   - **Proposed change**: Reclassify XVI as component-tier because parameter pinning and mathematical transparency are conversus-oss engine implementation details, not suite-wide architectural requirements.
   - **Rationale**: The "paid layer" (conversus-enhanced) could implement entirely different optimization approaches that don't use the 3-stage pipeline or objective.yml pinning. [CONSTITUTION.md, L1425-1561]
   - **Risk if ignored**: Forces inappropriate mathematical constraints on future suite siblings that don't use optimization.

3. **Specify comprehensive cross-reference audit** (Priority: P1)
   - **Current state**: Spec L110-124 lists 4 rewrite patterns but misses Amendment records and inline citations.
   - **Proposed change**: Add explicit patterns for "Amendment record (2026-04-25, arbiter ruling)" style references that appear in XXIV, XXV, XXVII and cross-reference deliberation findings.
   - **Rationale**: Current audit methodology (L512-518 in CONSTITUTION.md) requires "singular form, plural form, and adjacent-phrase forms" but spec doesn't apply this standard. [CONSTITUTION.md, L512-518]
   - **Risk if ignored**: Relocated principles will contain dangling references to principles in other tiers.

4. **Define rollback verification procedure** (Priority: P1)
   - **Current state**: Spec L318 claims "PR is reverted" but doesn't specify how to verify reversion succeeded across all edited files.
   - **Proposed change**: Add mandatory rollback verification that runs the tier-coherence linter on the reverted tree and confirms all 3 constitution files return to pre-PR state.
   - **Rationale**: Monolithic operations that span multiple files can leave inconsistent state even after attempted reversion. [spec L291-318]
   - **Risk if ignored**: Implementation failure could permanently break the constitutional system with no recovery procedure.

5. **Add false positive escape mechanism** (Priority: P2)
   - **Current state**: Spec L188-191 provides no way to mark legitimate shared content as exempt from duplication detection.
   - **Proposed change**: Add `<!-- TIER-COHERENCE:IGNORE -->` comment syntax that disables duplication checking for specific principle sections.
   - **Rationale**: Origin attributions and shared boilerplate legitimately appear across tiers but could trigger false positives that block amendments. [spec L188-191]
   - **Risk if ignored**: Future amendments could be blocked by spurious duplication alerts.

6. **Strengthen component-tier classification rationale** (Priority: P2)
   - **Current state**: Spec L40-47 provides minimal justification for XVII-XXI, XXVI staying component-tier.
   - **Proposed change**: Add explicit analysis showing why each component-tier principle is conversus-oss-specific rather than suite-wide.
   - **Rationale**: Tier classification should be mechanically verifiable, not judgment calls that require re-litigation in future amendments. [spec L42-44]
   - **Risk if ignored**: Arbitrary-appearing classifications undermine the entire tier extraction rationale.

7. **Verify SIR cross-reference preservation** (Priority: P2)
   - **Current state**: Spec L150-151 preserves SIR blocks but doesn't address internal cross-references within preserved SIRs.
   - **Proposed change**: Add check that relative cross-references within preserved SIR comment blocks are updated to point to relocated principles.
   - **Rationale**: SIR blocks contain audit trail references that become invalid when principles relocate but spec doesn't account for this. [CONSTITUTION.md, L1-595]
   - **Risk if ignored**: Breaks governance audit trail integrity by leaving invalid historical references.

8. **Add implementation window conflict detection** (Priority: P3)
   - **Current state**: Spec L291-318 assumes clean monolithic implementation but doesn't account for concurrent constitution amendments.
   - **Proposed change**: Add requirement that implementation PR blocks any other constitutional amendments from merging during implementation window.
   - **Rationale**: Concurrent amendments could create merge conflicts that make monolithic atomicity impossible to achieve. [spec L291]
   - **Risk if ignored**: Implementation could fail due to conflicts with concurrent amendments.

### Referenced Documentation

- `blind-inputs/spec-stripped.md` — sections cited: L15-25 (motivation), L37 (grandfathering), L80-92 (classification), L110-124 (cross-references), L150-151 (SIR preservation), L185-191 (linter algorithm), L291-318 (implementation)
- `<HOME>/code/payer-index-mono/conversus-oss/CONSTITUTION.md` — sections cited: L512-518 (audit methodology), L1425-1561 (XVI content), L2075-2091 (grandfathering), L1-595 (SIR blocks)
- `QUESTION.md` — sections cited: L9-15 (verification scope), L20-32 (review requirements)