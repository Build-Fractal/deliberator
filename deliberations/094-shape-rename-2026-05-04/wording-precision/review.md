### Executive Summary

This deliberation reviews a proposed terminology rename in Principle XVI's v2.3.2 Clarification block, changing "shape" to "assembly form" to resolve a cross-principle vocabulary collision with Principle IX's behavior-over-shape testing framework. The rename addresses a legitimate terminological inconsistency where "shape" serves different semantic purposes in different principles, while Principle XVI already uses "assembly-form-identical" elsewhere in the same section. From a wording-precision perspective, the proposed change preserves normative force while improving internal consistency and eliminating ambiguity. The rename should proceed as proposed.

### Alignment

- **Existing terminology consistency** (L1485, L1489): The principle already uses "assembly-form" terminology in the Enforcement section ("Stage-3 assembly-form determinism" and "asserts assembly-form-identical"), providing precedent for the proposed rename.

- **Enumerated component preservation** (L1460-1461): The clarification explicitly enumerates what constitutes the shape/assembly form (parameter names, template selection, gap-identifier set), ensuring definitional stability regardless of the term used.

- **Cross-principle collision avoidance** (L1460 vs L1204-1218): The rename resolves the vocabulary conflict with Principle IX's "shape test" concept, which refers to structural testing patterns rather than objective function components.

### Missed Opportunities

- **Terminology alignment audit**: While this specific collision is addressed, no broader audit of terminology consistency across principles is evident. The constitution would benefit from systematic terminology harmonization.

- **Definitional anchoring**: The rename could be strengthened by adding a brief parenthetical definition of "assembly form" at first use, making the concept self-contained.

- **Cross-reference updating**: The v2.3.2 block refers to determinism scope but doesn't cross-reference the specific line where "assembly-form-identical" is already established.

### Off-Base Assumptions

No incorrect assumptions about wording precision are evident in the proposed change. The terminology substitution is mechanically sound and preserves semantic intent.

### Actionable Recommendations

1. **Approve the terminology substitution** (Priority: P1)
   - **Current state**: Line 1460 uses "shape" which collides with Principle IX terminology.
   - **Proposed change**: Replace "*shape*" with "*assembly form*" as specified.
   - **Rationale**: Resolves cross-principle vocabulary collision while aligning with existing usage in the same principle section.
   - **Risk if ignored**: Continued ambiguity between IX's "shape test" (testing methodology) and XVI's "shape" (objective function structure).

2. **Add definitional clarity** (Priority: P2)
   - **Current state**: "Assembly form" would be used without explicit definition.
   - **Proposed change**: Insert "(the structural composition)" after "assembly form" on first use.
   - **Rationale**: Makes the concept immediately interpretable without requiring cross-reference to the enumerated components.
   - **Risk if ignored**: Minor - the enumerated components provide implicit definition, but explicit definition improves precision.

3. **Consider systematic terminology audit** (Priority: P3)
   - **Current state**: No evidence of broader terminology consistency review.
   - **Proposed change**: Flag for future governance review whether other cross-principle vocabulary conflicts exist.
   - **Rationale**: This collision suggests potential for similar issues elsewhere in the constitution.
   - **Risk if ignored**: Other undetected terminology collisions may persist.

### Referenced Documentation

No documentation files were provided for the "wording-precision" perspective, though the evaluation references:
- CONSTITUTION.md — lines 1379-1517 (Principle XVI full text), L1460-1461 (specific collision site), L1485, L1489 (existing assembly-form usage), L1204-1218 (Principle IX shape test definition)