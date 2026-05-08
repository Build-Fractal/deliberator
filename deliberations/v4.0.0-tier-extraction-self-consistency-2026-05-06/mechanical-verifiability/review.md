### Executive Summary

The v4.0.0 tier extraction spec aims to split the flat conversus-oss constitution into a three-tier hierarchy while preserving all principle text verbatim and formally admitting both suite repos. From a mechanical verification perspective, this amendment introduces new structural constraints that require automated enforcement but provides incomplete specifications for the proposed verification mechanisms. The spec correctly recognizes the need for mechanical verification (Constitutional Inclusion Criterion 1) and proposes a tier-coherence linter, but the linter's implementation details are underspecified in critical areas. The verification protocol invocation appears consistent with spec 067 requirements, though the relationship between automated checks and manual review processes needs clarification. My most important recommendation is to precisely define the "string-match heuristic" for cross-tier duplication detection before implementation begins.

### Alignment

- **Tier-coherence linter concept** (L2318-2329): The spec correctly identifies that structural amendments require mechanical verification and proposes an automated linter as the Constitutional Inclusion Criterion 1 compliance mechanism. This aligns with the requirement that violations must be detectable by automated means rather than human judgment.

- **Orphan detection check** (L2322-2323): The proposal to detect when "a relocated Tier 1 / Tier 2 principle's body still appears in conversus-oss/CONSTITUTION.md" is mechanically straightforward and directly verifiable through text search operations.

- **Version consistency enforcement** (L2325-2326): The check that "Version: field in any of the three constitution documents disagrees with the latest SIR" addresses a concrete failure mode and is mechanically implementable through frontmatter parsing.

- **Negative search specification** (L2332-2348): Section 7's concrete negative search requirements provide falsifiable test conditions that can be implemented as automated checks, complementing the heuristic approaches in the linter.

### Missed Opportunities

- **Fuzzy duplication detection**: The spec mentions "string-match heuristic" but provides no threshold or algorithm specification. Advanced text similarity measures (cosine similarity, edit distance, semantic embedding comparison) could provide more robust duplication detection than exact string matching. Impact: high.

- **Automated cross-reference validation**: The spec requires cross-reference rewriting (L1113-1120) but provides no mechanical check that the rewritten references actually resolve correctly. Link validation could prevent broken internal references. Impact: medium.

- **Principle enumeration validation**: The spec lists specific principle sets for each tier (L397-428) but doesn't propose automated verification that these enumerations are complete and non-overlapping. Set-theoretic validation could catch enumeration errors. Impact: medium.

- **Verbatim preservation verification**: Section 5's "byte-equal content" requirement (L1113) lacks automated verification. Cryptographic hashing or byte-level diff tools could mechanically verify the preservation contract. Impact: high.

- **Schema-based validation**: The spec describes specific file structure requirements (frontmatter, SIR blocks, principle headers) but relies on manual review. Schema validation could automate structural correctness checks. Impact: medium.

- **Dependency ordering verification**: The spec describes implementation order (L2468-2478) but provides no check that the "atomic" nature is preserved. Transaction-like verification could ensure consistency during implementation. Impact: low.

### Off-Base Assumptions

- **String matching sufficiency assumption**: The spec assumes "string-match heuristic plus name-collision check" (L2320) is adequate for duplication detection, but this approach will miss semantic duplication where identical concepts are expressed in different words. Semantic similarity detection would be more robust.

- **Manual review reliability assumption**: The spec treats the manual "negative checks" in Section 7 (L2342-2348) as authoritative but positions the automated linter as supplementary, when automated checks are typically more reliable for mechanical verification tasks.

### Actionable Recommendations

1. **Specify duplication detection algorithm** (Priority: P1)
   - **Current state**: "string-match heuristic plus name-collision check" (L2320) with no implementation details.
   - **Proposed change**: Define the heuristic as "exact substring match of principle body text after normalizing whitespace, plus header collision detection using regex `^### ([IVXLCDM]+)\. (.+)$`".
   - **Rationale**: Mechanical verification requires deterministic algorithms that multiple implementors can reproduce identically.
   - **Risk if ignored**: The linter becomes unimplementable or produces inconsistent results across implementations.

2. **Add verbatim preservation automation** (Priority: P1)
   - **Current state**: Section 5 verbatim preservation contract (L1113-1120) relies on manual verification.
   - **Proposed change**: Extend tier-coherence linter to compute SHA-256 hashes of principle bodies before and after relocation, verifying byte-equality modulo documented cross-reference changes.
   - **Rationale**: "Byte-equal content" claims require byte-level verification, not human review.
   - **Risk if ignored**: Verbatim preservation violations could go undetected, violating the core contract of the amendment.

3. **Clarify linter vs manual check relationship** (Priority: P1)  
   - **Current state**: Section 6.8 describes automated linter, Section 7 describes manual "negative checks" with overlapping scope.
   - **Proposed change**: Specify that the linter implements a subset of Section 7's checks automatically, with the manual checks serving as the authoritative verification for complex edge cases.
   - **Rationale**: Unclear relationships between automated and manual verification create gaps where violations might fall through.
   - **Risk if ignored**: Implementation teams won't know which verification method takes precedence when they disagree.

4. **Define "latest SIR" for version checking** (Priority: P2)
   - **Current state**: Version consistency check references "latest SIR" (L2325) without specifying how to identify it.
   - **Proposed change**: Define "latest SIR" as "the first Sync Impact Report comment block in each file, identified by the pattern `<!-- Sync Impact Report` followed by `Version change:`".
   - **Rationale**: Automated parsing requires unambiguous identification rules.
   - **Risk if ignored**: Version consistency check becomes unimplementable due to ambiguous SIR identification.

5. **Add cross-reference resolution validation** (Priority: P2)
   - **Current state**: Cross-reference rewriting is specified (L1113-1120) but not verified mechanically.
   - **Proposed change**: Extend linter to parse Markdown links and verify that all internal cross-references resolve to existing sections in the target files.
   - **Rationale**: Broken cross-references violate the structural integrity the amendment aims to preserve.
   - **Risk if ignored**: Post-relocation documents may contain unresolvable internal links.

6. **Implement principle enumeration validation** (Priority: P2)
   - **Current state**: Tier classifications (L397-428) are specified as lists but not cross-verified.
   - **Proposed change**: Add linter check that the union of all tier principle sets equals the complete active principle set, with no overlaps.
   - **Rationale**: Enumeration errors could result in principles being lost or duplicated across tiers.
   - **Risk if ignored**: The tier extraction might silently drop or duplicate principles.

7. **Specify whitespace normalization rules** (Priority: P3)
   - **Current state**: "String-match heuristic" (L2320) doesn't specify treatment of whitespace differences.
   - **Proposed change**: Define normalization as "collapse multiple whitespace characters to single spaces, strip leading/trailing whitespace per line".
   - **Rationale**: Exact string matching without normalization will fail on formatting differences that don't affect semantic content.
   - **Risk if ignored**: False positives from irrelevant whitespace differences could trigger spurious duplication warnings.

### Referenced Documentation

- `conversus-oss/specs/v4.0.0-tier-extraction/spec.md` — sections cited: L397-428 (tier classifications), L1113-1120 (verbatim preservation), L2318-2329 (tier-coherence linter), L2320 (string-match heuristic), L2322-2323 (orphan detection), L2325-2326 (version consistency), L2332-2348 (negative checks), L2468-2478 (implementation order)