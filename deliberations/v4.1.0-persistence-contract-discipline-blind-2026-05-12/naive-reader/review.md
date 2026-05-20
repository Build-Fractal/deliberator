### Executive Summary

Spec v4 establishes a "Persistence Contract Discipline" principle requiring conversus-family products to declare versioned schemas for persistent artifacts, mechanically enforce conformance in CI, and maintain stable cross-product consumer contracts. As a naive reader encountering this fresh, the principle addresses a real problem (implicit persistence contracts causing silent failures) with a structured approach that is largely implementable. However, several key terms lack definitions within the spec itself, and some mechanisms are referenced but not specified in sufficient detail for uniform implementation. The spec assumes readers understand concepts like "discoverable location," "explicit declaration," and "consumer surface" without defining these terms, requiring interpretive charity that constitutional principles should avoid.

Most concerning is that a junior engineer reading only this spec would need to make judgment calls on format choices, documentation adequacy, and procedural details where uniformity is essential for the principle's effectiveness. The principle is well-intentioned and addresses genuine technical debt, but requires clarification of approximately 8-10 ambiguous terms and mechanisms before it can function as self-contained constitutional doctrine.

**My most important recommendation: Define all technical terms within the spec itself rather than relying on implied understanding of "discoverable," "explicit declaration," and "adequate documentation."**

### Alignment

- **Clear CI gate requirements** (spec § 4 sub-clause 2, L159-175): The spec explicitly mandates "PR-required and merge-blocking" CI gates with "machine-executable" validation producing "binary pass/fail result with specific failure descriptions." This creates actionable implementation requirements.

- **Concrete test fixture specification** (spec § 4 sub-clause 2, L183-189): Requires exactly three test fixtures with specific failure modes (conformant pass, missing-required fail, wrong-type fail). This provides clear acceptance criteria.

- **Format flexibility with enforcement constraint** (spec § 4 sub-clause 2, L165-169): Allows product choice of schema format while mandating mechanical enforceability. Balances implementation freedom with operational discipline.

- **Bidirectional validation requirement** (spec § 4 sub-clause 2, L175-182): Explicitly requires both forward validation (artifacts conform to schema) and drift detection (schema changes trigger producer validation). Addresses the full lifecycle.

### Missed Opportunities

- **Missing schema format guidance**: The spec allows "XSD, JSON Schema, Pydantic model, AST validator, or any other format" but provides no guidance for choosing between them. A naive reader cannot determine which format suits different artifact types.

- **Undefined version bump procedure content**: Sub-clause 3 requires "documented bump procedure" but doesn't specify what the documentation should cover (breaking vs non-breaking changes, backward compatibility, migration steps).

- **Vague consumer contract scope**: Sub-clause 4 mentions "output surfaces" without defining what constitutes a surface versus an implementation detail, beyond the examples given.

- **Unclear debt closure mechanism**: Sub-clause 5 mentions products can "declare display text as the contract" but must "close" this debt without specifying how debt closure is verified or what constitutes adequate structural replacement.

- **Missing implementation timeline guidance**: While § 2 goals 3-5 specify 2026-12-01 deadline, no guidance exists for planning schema declaration and CI gate implementation across multiple products.

### Off-Base Assumptions

- **Assumption: "discoverable location" is self-evident** (spec § 4 sub-clause 1, L145): The spec assumes readers understand what makes a location "discoverable" versus not, but this is a judgment call that could vary between implementers.

- **Assumption: "explicit declaration" mechanism is obvious** (spec § 4 sub-clause 5, L205): The spec states display text must be "explicitly declared as such" to be stable, but never specifies how this declaration occurs or what format it takes.

- **Assumption: schema adequacy is deterministic** (spec § 4 sub-clause 3, L195): Requires "documented bump procedure" but assumes readers can distinguish adequate from inadequate documentation without criteria.

### Actionable Recommendations

1. **Define "discoverable location" criteria** (Priority: P1)
   - **Current state**: Spec L145 mentions "discoverable location (typically `STATE-FILES.md`, `CONSUMER-CONTRACT.md`, or an equivalent canonical doc at the repo root)"
   - **Proposed change**: Add specific criteria: "A location is discoverable if it appears in the repo root directory, has a filename matching `*CONTRACT*.md` or `*SCHEMA*.md`, and is linked from README.md or the main documentation entry point."
   - **Rationale**: Constitutional principles require mechanical verifiability; "discoverable" must have objective criteria.
   - **Risk if ignored**: Different teams will interpret "discoverable" differently, undermining uniform application.

2. **Specify schema_version field format** (Priority: P1)
   - **Current state**: Spec L150 requires "schema_version field" without format specification.
   - **Proposed change**: "The schema_version field MUST use semantic versioning format (MAJOR.MINOR.PATCH) as defined by semver.org."
   - **Rationale**: Version comparison requires standardized format for CI gates and cross-product compatibility checks.
   - **Risk if ignored**: Inconsistent version formats will break automated validation and cross-product integration.

3. **Define explicit declaration mechanism** (Priority: P1)
   - **Current state**: Spec L205 requires display text be "explicitly declared as such" without specifying how.
   - **Proposed change**: Add: "Explicit declaration occurs via a `STABLE-DISPLAY-SURFACES.md` file listing specific text patterns marked stable, with regex patterns and context boundaries."
   - **Rationale**: Sub-clause 5 is unimplementable without a concrete declaration mechanism.
   - **Risk if ignored**: Teams cannot implement the display text stability requirement, undermining the principle's applicability.

4. **Clarify consumer surface definition** (Priority: P2)
   - **Current state**: Spec L201 references "output surfaces" without definition beyond negative examples.
   - **Proposed change**: "An output surface is a file path, directory structure, data field, or API endpoint intended for cross-product consumption. Implementation details include internal file organization, temporary paths, and undocumented data fields."
   - **Rationale**: Clear boundaries prevent confusion about what requires consumer contracts.
   - **Risk if ignored**: Ambiguous surface boundaries will lead to over-documentation or missed integration points.

5. **Specify bump procedure documentation requirements** (Priority: P2)
   - **Current state**: Spec L195 requires "documented bump procedure" without content specification.
   - **Proposed change**: "The bump procedure MUST document: (a) criteria for MAJOR vs MINOR vs PATCH increments, (b) backward compatibility guarantees, (c) consumer migration steps for breaking changes."
   - **Rationale**: Uniform version bump documentation enables predictable cross-product integration.
   - **Risk if ignored**: Inconsistent bump procedures will create confusion during schema evolution.

6. **Define debt closure verification** (Priority: P2)
   - **Current state**: Spec L208 mentions closing debt for display text contracts without verification criteria.
   - **Proposed change**: "Debt is closed when a structural surface replaces the display text contract AND consumer products migrate to the structural surface AND the display text dependency is removed from consumer CI."
   - **Rationale**: Debt closure must be mechanically verifiable to maintain the principle's discipline.
   - **Risk if ignored**: Display text dependencies will persist indefinitely without clear closure criteria.

7. **Add implementation planning guidance** (Priority: P3)
   - **Current state**: Spec § 2 goals 3-5 specify deadline without implementation sequence guidance.
   - **Proposed change**: Add: "Recommended implementation sequence: (1) declare schemas for existing artifacts, (2) implement CI validation gates, (3) add consumer contracts, (4) deploy test fixtures."
   - **Rationale**: Complex multi-product changes benefit from coordination guidance.
   - **Risk if ignored**: Uncoordinated implementation may create temporary integration failures.

### Q1 Implementability Assessment

**Sub-clause 1 (Declared schema):** IMPLEMENTABLE-WITH-CLARIFICATIONS - Core requirement is clear but "discoverable location," "schema_version" format, and JSONL "line semantics" need definition.

**Sub-clause 2 (Mechanical enforcement):** IMPLEMENTABLE - CI gate requirements and test fixtures are sufficiently specified, though bidirectional validation adds complexity.

**Sub-clause 3 (Versioning):** IMPLEMENTABLE-WITH-CLARIFICATIONS - Requires clarification of what constitutes "documented bump procedure."

**Sub-clause 4 (Cross-product contracts):** IMPLEMENTABLE-WITH-CLARIFICATIONS - Consumer contract concept is clear but "output surfaces" and "equivalent" to CONSUMER-CONTRACT.md need definition.

**Sub-clause 5 (Declaration scope):** NOT-IMPLEMENTABLE-AS-WRITTEN - "Explicit declaration" mechanism for display text stability is referenced but not specified.

**Q1 RULING: IMPLEMENTABLE-WITH-CLARIFICATIONS — Core requirements are actionable but 5-6 key terms lack definitions needed for uniform implementation.**

### Referenced Documentation

- `specs/v4.1.0-persistence-contract-discipline/spec.md` — sections cited: § 4 (L145-212), § 2 goals 3-5, § 3 non-goals
- `deliberations/v4.1.0-persistence-contract-discipline-blind-2026-05-12/QUESTION.md` — Q1 methodology and assessment criteria