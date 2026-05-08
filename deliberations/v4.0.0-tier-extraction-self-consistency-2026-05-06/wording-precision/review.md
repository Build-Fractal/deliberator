I'll read through all the target files to conduct the wording-precision review as specified.

### Executive Summary

The v4.0.0 tier extraction spec attempts to mechanically relocate 20 principles from the flat conversus-oss constitution to a three-tier hierarchy without changing normative content. While the scope discipline and verbatim preservation intent are sound, the wording precision of the preservation contract and verification procedures contains several falsifiability gaps that could enable subtle violations during implementation. The spec's cross-reference rewrite documentation is incomplete, the SIR preview omits required audit trail preservation, and the conditions discharge claims contain minor inaccuracies that undermine verification credibility. These are not conceptual flaws but mechanical precision issues that must be addressed before blind verification can meaningfully assess the amendment.

Most critically: the verbatim preservation contract in §5 uses imprecise language that could permit paragraph reflows, formatting changes, or whitespace modifications while still claiming "verbatim" compliance—yet §7's "byte-equal content" requirement is much more stringent and represents the actual standard.

### Alignment

- **Verbatim preservation scope documentation** (spec L108-109): The spec explicitly enumerates what counts as normative text ("bullet lists, 'Origin:' attributions, 'Extension (vN.M.K)' sub-blocks, and cross-references"), providing concrete boundaries for preservation requirements rather than vague "content" language.

- **Cross-tier number stability preservation** (spec L111-112): The specification that principles keep their Roman numeral identifiers across tiers prevents renumbering confusion and maintains reference integrity, aligning with Principle II's stable interfaces requirement.

- **Concrete verification checks** (spec L179-186): The negative verification checks ("Search Tier 1 for any principle in {V, XII, XIII...}. There MUST be zero matches") provide mechanically falsifiable tests rather than subjective assessments.

- **Conditions discharge empirical evidence** (spec L224-231): Each condition status links to specific empirical verification (grep commands, directory listings) rather than unsupported claims, enabling third-party verification of discharge accuracy.

### Missed Opportunities

- **Verbatim contract falsifiability refinement**: The preservation contract uses "every word...is preserved" (L108) but §7 specifies "byte-equal content" (L181)—the former allows formatting changes that violate the latter. **Impact: medium**. The contract should reference the byte-equal standard consistently, or explicitly enumerate what non-content changes (whitespace, line breaks) are permitted.

- **Cross-reference syntax standardization**: The spec provides inconsistent cross-reference examples ("Principle IX (../CONSTITUTION.md)" vs "../../build-fractal/CONSTITUTION.md § Principle IX") without explaining why different syntax forms apply. **Impact: medium**. A complete cross-reference matrix (all tier combinations × syntax patterns) would prevent implementation ambiguity.

- **SIR audit trail preservation gaps**: The SIR preview references "prior SIR comment block below" (L306) but doesn't specify that multiple prior SIR blocks exist and must be preserved. Reading CONSTITUTION.md shows ~6 prior SIR blocks preserved as comments; the spec should explicitly enumerate this preservation requirement. **Impact: high**.

- **Missing component-to-Tier-2 cross-reference form**: The spec shows Tier 2→Tier 1 and component→Tier 1 patterns but omits component→Tier 2, creating an implementation gap. **Impact: low**. Component principles may reference Suite principles and need a documented path syntax.

- **Conditions accuracy verification**: The spec claims "V, XXIV, XXVI flipped Satisfied → Provisional" (L230) but reading conversus-oss/CONFORMANCE.md shows V was already Provisional, not flipped from Satisfied. **Impact: medium**. The discharge claims should match actual file state, not idealized state.

- **Tier-coherence linter mechanism specification**: The linter description (L166-171) uses "string-match heuristic plus name-collision check" without defining the heuristic algorithm, making mechanical verification non-reproducible. **Impact: medium**. The string-match algorithm should be specified (exact substring match, regex pattern, similarity threshold).

### Off-Base Assumptions

- **Assumption: "verbatim" and "byte-equal" are equivalent** (spec L108 vs L181): The spec uses these terms interchangeably but they have different technical meanings. "Verbatim" typically allows formatting changes; "byte-equal" forbids any changes. The more stringent standard should be consistently applied.

- **Assumption: all cross-reference rewrites follow the same pattern**: The spec provides examples but doesn't account for different reference styles within principles (some use "Principle IX", others use "IX", others use section references). The preservation contract should specify how each existing reference style gets translated.

### Actionable Recommendations

1. **Unify preservation contract language** (Priority: P1)
   - **Current state**: §5 says "every word...is preserved" while §7 requires "byte-equal content" (L108 vs L181).
   - **Proposed change**: Replace L108 "every word of the principle's normative text" with "byte-for-byte identical content of the principle's normative text".
   - **Rationale**: Eliminates ambiguity about formatting, whitespace, and encoding preservation.
   - **Risk if ignored**: Implementation could reflow paragraphs, change indentation, or alter line endings while claiming compliance.

2. **Complete cross-reference matrix documentation** (Priority: P2)
   - **Current state**: Incomplete examples showing only 2 of 6 possible tier reference patterns (L109-110).
   - **Proposed change**: Add complete table showing source tier × target tier × syntax pattern for all combinations.
   - **Rationale**: Implementation needs unambiguous syntax for every possible cross-reference scenario.
   - **Risk if ignored**: Inconsistent cross-reference syntax across relocated principles, breaking links.

3. **Specify SIR audit trail preservation** (Priority: P1)
   - **Current state**: SIR preview mentions "prior SIR comment block below" without enumerating existing blocks (L306).
   - **Proposed change**: Add explicit requirement: "Preserve all existing SIR comment blocks (v3.2.2→v3.2.3, v3.2.1→v3.2.2, v3.1.3→v3.2.0, etc.) as comment blocks below the v4.0.0 SIR."
   - **Rationale**: Audit trail preservation is documented pattern in current CONSTITUTION.md.
   - **Risk if ignored**: Loss of amendment history violates established governance documentation pattern.

4. **Correct conditions discharge accuracy** (Priority: P2)
   - **Current state**: Claims "V, XXIV, XXVI flipped Satisfied → Provisional" but V was already Provisional (L230).
   - **Proposed change**: Review actual CONFORMANCE.md state and correct status claims to match reality.
   - **Rationale**: Verification credibility depends on accurate empirical claims.
   - **Risk if ignored**: Undermines verification process when factual claims are demonstrably wrong.

5. **Define tier-coherence linter algorithm** (Priority: P2)
   - **Current state**: "string-match heuristic plus name-collision check" without algorithmic specification (L167).
   - **Proposed change**: Specify exact matching algorithm (e.g., "exact substring match of principle header + first paragraph").
   - **Rationale**: Mechanical verification requires reproducible algorithms.
   - **Risk if ignored**: Non-deterministic linter behavior makes Constitutional Inclusion Criterion 1 unverifiable.

6. **Document backward cross-reference handling** (Priority: P3)
   - **Current state**: Only shows lower-tier → higher-tier references; no higher-tier → lower-tier pattern.
   - **Proposed change**: Specify syntax for Tier 1 principle referencing Tier 2/component principles.
   - **Rationale**: Completeness principle for reference documentation.
   - **Risk if ignored**: Ambiguity if future Tier 1 amendments need to reference lower tiers.

7. **Enumerate normative text boundaries** (Priority: P2)
   - **Current state**: Lists some components ("bullet lists, Origin attributions") but not others (L108).
   - **Proposed change**: Complete enumeration including "all paragraph text, all bullet points, all sub-headings within principles, all bracketed annotations, all footnotes".
   - **Rationale**: Falsifiable preservation requires complete boundary definition.
   - **Risk if ignored**: Implementation could modify unlisted content while claiming preservation compliance.

### Referenced Documentation

- `conversus-oss/specs/v4.0.0-tier-extraction/spec.md` — sections cited: L108-112 (verbatim preservation), L166-171 (tier-coherence linter), L179-186 (verification checks), L224-231 (conditions table), L306 (SIR preview)
- `conversus-oss/CONSTITUTION.md` — sections cited: multiple SIR comment blocks, cross-reference patterns
- `conversus-oss/CONFORMANCE.md` — sections cited: L39 (V status), L46 (XXIV status), L63 (XXVI status)
- `conversus-oss/deliberations/v4.0.0-tier-extraction-originating-2026-05-06/VERDICT.md` — sections cited: L26-30 (templating audit), L84-88 (V/XXIV/XXVI translation)