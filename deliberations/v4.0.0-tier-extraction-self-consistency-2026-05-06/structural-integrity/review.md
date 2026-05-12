### Executive Summary

The v4.0.0 tier extraction specification proposes to restructure the conversus constitutional hierarchy from a flat 26-principle document into three tiers: Universal (10), Suite (10), and Component (6), while formally admitting two suite repositories. From a structural integrity perspective, the spec demonstrates solid architectural planning with explicit enumeration of principles per tier, comprehensive file-edit procedures, and robust verbatim-preservation contracts. However, my analysis reveals critical arithmetic errors in the tier classification, missing file edits for cross-repo governance logging, and inconsistencies between the verbatim preservation claims and the actual structural changes described. The most important recommendation is to fix the fundamental counting error where the spec claims 26 active principles but only accounts for 25 in the tier assignments.

### Alignment

- **Tier enumeration methodology** (`spec.md L102-130`): The spec provides explicit tabular breakdowns of which principles move to each tier, enabling mechanical verification of the classification logic. This structured approach aligns with systematic integrity checking.

- **Verbatim preservation contract** (`spec.md L148-169`): Section 5 establishes concrete testable contracts for relocated content, including byte-level preservation requirements and specific exceptions for cross-reference rewriting. This provides clear falsification criteria.

- **Negative verification checks** (`spec.md L190-201`): Section 7 specifies mechanical grep-based checks to verify no principle appears in wrong tiers, enabling automated structural validation post-implementation.

- **File-edit enumeration** (`spec.md L203-254`): Sections 6.1-6.9 provide systematic coverage of all constitution files requiring updates, with specific change descriptions for each target file.

- **Number stability preservation** (`spec.md L148-169`): The verbatim preservation contract explicitly states that principle numerals are preserved across tiers (Principle II compliance), maintaining stable interface contracts.

### Missed Opportunities

- **Cross-validation matrix**: The spec lacks a comprehensive cross-reference table showing which files reference which principles, missing the opportunity to systematically verify all cross-references get updated during relocation. Impact: medium.

- **Tier-coherence linter specification**: While §6.8 mentions a new linter, it provides minimal detail about the actual implementation requirements, missing the opportunity to define concrete structural validation rules. Impact: high.

- **Dependency ordering for file edits**: Section 6 lists edits without specifying interdependencies, missing the opportunity to prevent intermediate invalid states during the atomic implementation. Impact: medium.

- **Version synchronization verification**: The spec doesn't specify how to verify that all three tier documents maintain synchronized version references, missing automated consistency checking. Impact: medium.

- **Tombstone verification procedures**: While retired principles VI and X are mentioned, there's no specification for verifying tombstone entries maintain proper historical references. Impact: low.

- **Cross-tier cross-reference audit**: Beyond the basic grep checks, there's no systematic verification that cross-references between tiers use correct relative paths and remain valid post-restructuring. Impact: medium.

### Off-Base Assumptions

- **Complete tier accounting assumption** (`spec.md L102-130`): The spec assumes all 26 active principles are properly distributed across tiers, but the actual enumeration only accounts for 25 principles (I-IV, VII-IX, XI, XIV, XXVIII = 10; V, XII-XIII, XV-XVI, XXII-XXV, XXVII = 10; XVII-XXI, XXVI = 6; total = 26 claimed but 25 actual). This is a fundamental structural error.

- **Atomic implementation assumption** (`spec.md L283-289`): The spec assumes all file edits can be applied atomically in a single PR without intermediate validation, but doesn't account for potential conflicts between the governance log updates and the constitution changes.

### Actionable Recommendations

1. **Fix tier classification arithmetic** (Priority: P1)
   - **Current state**: Spec §4 claims 26 active principles but tier assignments only total 25 (`spec.md L102-130`).
   - **Proposed change**: Recount all principle assignments and identify the missing principle, or correct the claimed total.
   - **Rationale**: Fundamental structural integrity requires accurate accounting of all constitutional elements.
   - **Risk if ignored**: Implementation will fail when attempting to relocate a miscounted set of principles.

2. **Add conversus governance log edit** (Priority: P1)
   - **Current state**: Section 6 omits updating `conversus/CONSTITUTIONAL_CONVERSATIONS.md` with admission entry (`spec.md L203-254`).
   - **Proposed change**: Add §6.10 specifying the admission log entry for conversus repo parallel to conversus-oss entry.
   - **Rationale**: Both repos require governance log entries for suite admission per the originating deliberation Q3 ruling.
   - **Risk if ignored**: Incomplete governance audit trail for conversus admission.

3. **Specify tier-coherence linter implementation details** (Priority: P1)
   - **Current state**: §6.8 mentions the linter with minimal specification (`spec.md L252-254`).
   - **Proposed change**: Expand §6.8 to specify exact file paths to check, string patterns to detect, and validation rules to enforce.
   - **Rationale**: Constitutional Inclusion Criterion 1 requires mechanical verification capability with concrete implementation paths.
   - **Risk if ignored**: Amendment ships without the promised mechanical verification mechanism.

4. **Verify retired principle tombstone accuracy** (Priority: P2)
   - **Current state**: Spec mentions VI and X stay in component tier but doesn't verify tombstone content (`spec.md L108-118`).
   - **Proposed change**: Add explicit check that retired markers reference correct retirement versions and migration targets.
   - **Rationale**: Principle II number stability requires accurate historical preservation.
   - **Risk if ignored**: Broken historical references in tombstone entries.

5. **Add file-edit dependency ordering** (Priority: P2)
   - **Current state**: Section 6 lists edits without interdependency specification (`spec.md L203-254`).
   - **Proposed change**: Specify that constitution file updates (§6.1-6.3) must precede governance log updates (§6.4-6.7) to maintain reference validity.
   - **Rationale**: Prevents invalid intermediate states where governance logs reference non-existent constitution sections.
   - **Risk if ignored**: Potential merge conflicts or broken references during implementation.

6. **Specify cross-tier cross-reference validation** (Priority: P2)
   - **Current state**: Section 5 mentions cross-reference rewriting but lacks validation procedures (`spec.md L148-169`).
   - **Proposed change**: Add concrete examples of cross-reference patterns and specify mechanical checks for relative path accuracy.
   - **Rationale**: Ensures relocated principles maintain valid internal linkage after tier restructuring.
   - **Risk if ignored**: Broken cross-references between constitution tiers.

7. **Clarify verbatim preservation vs structural changes** (Priority: P2)
   - **Current state**: Spec claims "verbatim preservation" while also describing "clearly bracketed new content" (`spec.md L148-169`).
   - **Proposed change**: Explicitly distinguish between principle body preservation (verbatim) and tier document structure (new content allowed).
   - **Rationale**: Removes apparent contradiction between preservation contract and tier introduction sections.
   - **Risk if ignored**: Ambiguity about what content can be modified during relocation.

### Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus-oss/specs/v4.0.0-tier-extraction/spec.md` — sections cited: L102-130, L148-169, L190-201, L203-254, L252-254, L283-289
- `<HOME>/code/payer-index-mono/conversus-oss/deliberations/v4.0.0-tier-extraction-self-consistency-2026-05-06/QUESTION.md` — sections cited: structural integrity task definition, tier classification checks