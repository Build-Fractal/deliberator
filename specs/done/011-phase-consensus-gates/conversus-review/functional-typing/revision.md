# Cooperative Revision — Phase 3

**Agent**: functional-typing
**Iteration**: 1

---

### Recommendation Dispositions

#### Recommendation 1: Clarify preset-to-multi-agent expansion
- **Original position**: The spec example showing `preset: review/thorough` is unimplementable with the current single-agent preset system. Either the spec or the preset system needs to change.
- **Disposition**: Surviving
- **Explanation**: All three reviewers independently identified this gap. devils-advocate's cross-review (Tensions, "Preset gap remediation") suggests at minimum fixing the spec example. integration-architect's cross-review (Safe Agreements, "Preset gap is real") confirms the structural issue. No one challenged the substance — the preset system produces single-agent definitions and gates need at least 2. This recommendation has unanimous support.

#### Recommendation 2: Specify max_disputes N parsing rules
- **Original position**: N must be a positive integer (1 or greater).
- **Disposition**: Modified
- **Explanation**: integration-architect's cross-review (Dangerous Contradictions, "max_disputes N range") correctly identified my internal inconsistency — Recommendation 2 said "positive integer (1 or greater)" while Recommendation 7 said "max_disputes 0 is valid." devils-advocate's cross-review (Dangerous Contradictions) echoed this. The modified recommendation: "N must be a non-negative integer (0 or greater). Non-integer, negative, or non-numeric values fail with: 'max_disputes requires a non-negative integer. Got: {value}.' max_disputes 0 is valid and equivalent to converged — emit info: 'max_disputes 0 is equivalent to converged.'" This subsumes Recommendation 7.

#### Recommendation 3: Define flag-override precedence for config-based gates
- **Original position**: CLI flags should take precedence over gate config values.
- **Disposition**: Surviving
- **Explanation**: integration-architect independently made the same recommendation (Recommendation 5). Cross-reviews between the two (Safe Agreements, "Flag-override precedence") confirm this is a shared position. No reviewer challenged it.

#### Recommendation 4: Specify attempt-number scanning as numeric
- **Original position**: Scan `attempt-*` directories with numeric suffix parsing, not lexicographic sort.
- **Disposition**: Surviving
- **Explanation**: No cross-review challenged this recommendation. devils-advocate's cross-review (Safe Agreements, "Re-run audit trail") noted the design is correct and did not dispute the numeric sort detail. The recommendation stands as originally stated.

#### Recommendation 5: Define partial execution handling
- **Original position**: If the run engine fails before producing a synthesis, the gate verdict is ERROR. If synthesis exists but is incomplete, use Dispute-Parsing defaults.
- **Disposition**: Modified
- **Explanation**: integration-architect's Recommendation 1 and cross-review (Dangerous Contradictions, "Partial execution verdict") argued that all parsing failures should be ERROR. devils-advocate's cross-review of integration-architect (Dangerous Contradictions, "Dispute-Parsing failure") proposed a two-tier approach: no synthesis = ERROR, synthesis exists but unparseable = BLOCK with a note. I find the two-tier approach most correct. Modified recommendation: "(1) If no synthesis file exists after engine execution, the gate verdict is ERROR (exit code 2) with: 'Run engine failed to produce synthesis.' (2) If synthesis exists but the Dispute-Parsing Subsystem cannot find markers or headings, the gate verdict is BLOCK (exit code 1) with a note in gate-result.md Disputes section: 'Dispute count determined via fallback parsing — synthesis may be incomplete.' The deliberation ran; calling it ERROR misrepresents what happened."

#### Recommendation 6: Add gates.yml standalone validation
- **Original position**: gates.yml must contain exactly one top-level key: `gates:`. Extra keys fail validation.
- **Disposition**: Modified
- **Explanation**: integration-architect's cross-review (Tensions, "gates.yml validation") raised the forward-compatibility concern — strict validation prevents future extension. The modified recommendation: "A standalone gates.yml must contain a `gates:` top-level key. Unknown top-level keys emit a warning: 'Unknown key in gates.yml: {key}. Only the gates: section is used.' This allows forward compatibility while alerting users to potential errors."

#### Recommendation 7: Validate max_disputes 0 equivalence
- **Original position**: max_disputes 0 is valid and equivalent to converged. Emit info message.
- **Disposition**: Withdrawn
- **Explanation**: This recommendation is subsumed by the modified Recommendation 2. integration-architect's cross-review correctly identified the internal inconsistency between Rec 2 and Rec 7. The reconciled position (non-negative integer, 0 is valid) is captured in the modified Rec 2.

#### Recommendation 8: Document the generated conversus.yml audit trail
- **Original position**: Add YAML comment headers to the generated config for debugging.
- **Disposition**: Surviving
- **Explanation**: No cross-review challenged this. integration-architect's Recommendation 7 (clarify the config is passed by reference) is complementary. Both can be implemented independently.

### New Recommendations

- **Add non-determinism acknowledgment to spec guidance** (Priority: P3)
  - **Triggered by**: devils-advocate's Recommendation 3 (Confidence section in gate-result.md) and functional-typing/devils-advocate cross-review (Dangerous Contradictions, "Non-determinism"). The cross-review discussion clarified that non-determinism should be acknowledged in guidance, not in the schema.
  - **Proposed change**: Add a note to the spec's Constraints section (or a new subsection): "Gate verdicts derive from LLM-based deliberation, which is non-deterministic. The same artifact may produce different dispute counts across runs. Teams should treat gate verdicts as quality signals with inherent variance, not as deterministic test results. Calibrate pass criteria accordingly (e.g., `max_disputes 1` provides more stability than `converged`)."
  - **Rationale**: Acknowledges a real property of the system without adding schema complexity. Helps teams calibrate their CI/CD integration.

### Position Summary

I withdrew 1 recommendation (Rec 7, subsumed by modified Rec 2), modified 3 (Recs 2, 5, 6), and maintained 4 (Recs 1, 3, 4, 8). I added 1 new recommendation (non-determinism guidance).

The most significant change was reconciling the max_disputes 0 inconsistency (Recs 2 and 7). integration-architect's cross-review exposed a genuine internal contradiction that I should have caught in Phase 1. The non-negative integer constraint is clearly correct, and collapsing two recommendations into one strengthens the position.

My remaining highest-priority recommendation is Recommendation 1 (preset-to-multi-agent expansion), which has unanimous support and represents a blocking gap — the spec's own example cannot be implemented with the current system.
