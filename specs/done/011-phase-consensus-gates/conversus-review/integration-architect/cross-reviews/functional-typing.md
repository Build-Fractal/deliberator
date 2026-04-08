# Cooperative Cross-Review — Phase 2

**Reviewer**: integration-architect
**Reviewed**: functional-typing

---

### Dangerous Contradictions

- **max_disputes N range: positive vs. non-negative**
  - **functional-typing claims**: Recommendation 2 says "N must be a positive integer (1 or greater)." Recommendation 7 says "max_disputes 0 is valid and equivalent to converged."
  - **integration-architect claims**: Recommendation 8 says "N must be a non-negative integer. 0 is allowed and is equivalent to converged."
  - **Why this is dangerous**: functional-typing has an internal contradiction (Rec 2 vs. Rec 7). If Rec 2 is implemented, `max_disputes 0` would fail validation. If Rec 7 is implemented, `max_disputes 0` would succeed. Integration-architect's position is consistent: non-negative (0+) with 0 being equivalent to converged.
  - **Suggested resolution**: functional-typing should reconcile their two recommendations. The correct constraint is non-negative integer (0 or greater). Recommendation 2 should be modified to say "non-negative integer" rather than "positive integer."

- **Partial execution verdict**
  - **functional-typing claims**: Recommendation 5 distinguishes between "no synthesis" (ERROR) and "incomplete synthesis" (use Dispute-Parsing defaults). This is framed as a specification gap.
  - **integration-architect claims**: Recommendation 1 says Dispute-Parsing failures should produce ERROR verdict. My position is stronger: any failure in the parsing pipeline should be ERROR, not BLOCK.
  - **Why this is dangerous**: functional-typing allows BLOCK for incomplete synthesis (Dispute-Parsing defaults to "has disputes"). integration-architect requires ERROR. These produce different exit codes (1 vs. 2) for the same failure scenario.
  - **Suggested resolution**: Distinguish two cases: (1) synthesis exists but has no dispute markers — use Dispute-Parsing defaults (BLOCK, because the deliberation ran and likely found issues), (2) synthesis does not exist — ERROR. This preserves functional-typing's nuance while adopting integration-architect's ERROR for true failures.

- **No additional contradictions identified.**

### Tensions

- **Scope of structural validation**
  - **functional-typing's position**: Focused on validation rules, parsing constraints, and error messages for existing schema fields (Recommendations 2, 4, 6, 7, 8).
  - **integration-architect's position**: Focused on missing schema fields (stagnation, iterations, prior) and integration gaps (Recommendations 2, 3, 6).
  - **Nature of tension**: functional-typing validates depth within the existing schema. integration-architect validates breadth by identifying missing fields. Both are needed but pull in different directions: depth tightens the existing design, breadth expands it.
  - **Coordination needed**: Adopt both — tighten validation on existing fields (functional-typing) AND add missing fields (integration-architect). Ensure new fields get the same validation rigor.

- **gates.yml validation**
  - **functional-typing's position**: Recommendation 6 proposes strict validation: gates.yml must contain exactly one top-level key `gates:`. Any other key fails.
  - **integration-architect's position**: Off-Base Assumptions notes the validation gap but does not prescribe strict validation.
  - **Nature of tension**: Strict validation prevents future extension of gates.yml without a schema change. Lenient validation (ignore unknown keys) allows forward compatibility but risks silent misconfiguration.
  - **Coordination needed**: Agree on a validation strategy. Recommendation: warn on unknown keys (not fail). This allows forward compatibility while alerting users to potential errors.

- **Generated config documentation**
  - **functional-typing's position**: Recommendation 8 proposes YAML comment headers in the generated config for debugging.
  - **integration-architect's position**: Recommendation 7 proposes clarifying that the config is passed by reference (not re-read by the engine).
  - **Nature of tension**: Both address the generated config but from different angles. functional-typing wants the file to be self-documenting. integration-architect wants the usage semantics to be clear. Both can be implemented independently.
  - **Coordination needed**: None — these are complementary, not conflicting.

### Safe Agreements

- **Engine independence is correctly implemented**
  - **Shared position**: Both reviews confirm FR-012 implementation (functional-typing Alignment, integration-architect Alignment).
  - **Combined evidence**: Both cite SKILL.md L2127-2135. Both independently verified the engine boundary.
  - **Confidence level**: High.

- **Flag-override precedence must be specified**
  - **Shared position**: Both reviews recommend explicit "flags override config" semantics (functional-typing Recommendation 3, integration-architect Recommendation 5).
  - **Combined evidence**: Both cite SKILL.md L1877-1880. Both arrive at the same recommendation independently.
  - **Confidence level**: High.

- **Preset gap is real**
  - **Shared position**: Both reviews identify the `preset: review/thorough` example as problematic (functional-typing Off-Base Assumptions, integration-architect Off-Base Assumptions).
  - **Combined evidence**: Both trace from spec L65-66 through the preset system. functional-typing calls it "spec-level confusion." integration-architect calls it a "gap."
  - **Confidence level**: High.
