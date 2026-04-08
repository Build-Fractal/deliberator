# Cooperative Cross-Review — Phase 2

**Reviewer**: devils-advocate
**Reviewed**: functional-typing

---

### Dangerous Contradictions

- **max_disputes N range internal inconsistency**
  - **functional-typing claims**: Recommendation 2 says "N must be a positive integer (1 or greater)." Recommendation 7 says "max_disputes 0 is valid and equivalent to converged."
  - **devils-advocate claims**: Did not address max_disputes 0 specifically. My concern is with the broader non-determinism of gate verdicts (Recommendation 3), which makes the exact threshold value less important than the threshold concept.
  - **Why this is dangerous**: functional-typing's internal contradiction means implementing both recommendations produces a validation bug. However, this is a known issue within functional-typing's own review, not a cross-review contradiction.
  - **Suggested resolution**: functional-typing should fix the inconsistency. Non-negative integer (0+) is the correct constraint.

- **Structural correctness vs. operational readiness**
  - **functional-typing claims**: The implementation is "largely sound" with all 12 FRs having corresponding handler sections (Executive Summary). The focus is on validation rules and parsing edge cases.
  - **devils-advocate claims**: The spec "fails to address" critical operational concerns — timeout, resource limits, idempotency, bypass (Executive Summary, Missed Opportunities). These are not minor gaps but potential blockers for real-world adoption.
  - **Why this is dangerous**: If functional-typing's structural assessment carries the day, the spec ships with correct validation rules but no operational safety. If devils-advocate's operational concerns dominate, the spec grows significantly in scope, potentially delaying implementation.
  - **Suggested resolution**: Both perspectives are valid but operate at different levels. The spec should implement structural correctness first (functional-typing) and add operational guidance as a separate section or follow-up spec. Attempting to do both in one spec risks bloat.

- **No additional contradictions identified.**

### Tensions

- **Depth vs. breadth of review**
  - **functional-typing's position**: Detailed validation rules for existing fields — max_disputes parsing, attempt numbering, gates.yml format (Recommendations 2, 4, 6).
  - **devils-advocate's position**: Broad operational gaps — timeout, resource limits, non-determinism, bypass (Recommendations 1-4).
  - **Nature of tension**: functional-typing reviews what the spec says and finds it mostly correct but underspecified in edge cases. devils-advocate reviews what the spec does not say and finds critical omissions. Both are correct — the spec is structurally sound but operationally incomplete.
  - **Coordination needed**: Agree on which concerns belong in spec 011 vs. a follow-up spec. Operational concerns may need their own "011.1: Gate Operational Readiness" spec.

- **Preset gap remediation**
  - **functional-typing's position**: Either the spec or the preset system needs to change (Recommendation 1). Frames this as a P1 blocking issue.
  - **devils-advocate's position**: Single-agent presets "were never designed for multi-agent deliberation" (Off-Base Assumptions). The spec should acknowledge the gap rather than showing a failing example.
  - **Nature of tension**: functional-typing wants a fix (change the preset system or the spec example). devils-advocate wants acknowledgment (document the limitation). The fix is more work; the acknowledgment is faster but leaves the gap open.
  - **Coordination needed**: At minimum, fix the spec example. Whether to extend the preset system is a scope decision for this spec.

- **Error handling philosophy**
  - **functional-typing's position**: Detailed error messages for each validation failure (Recommendations 2, 6 — specific message formats).
  - **devils-advocate's position**: Broad error categories (ERROR verdict) with less focus on message formatting.
  - **Nature of tension**: functional-typing optimizes for developer experience at the validation layer. devils-advocate optimizes for pipeline reliability at the execution layer. Both are valid — validation errors need good messages for humans, execution errors need deterministic signals for pipelines.
  - **Coordination needed**: Both approaches can coexist. Validation errors (config/schema problems) use functional-typing's detailed messages. Execution errors (timeouts, parse failures) use the EXIT code system that devils-advocate emphasizes.

### Safe Agreements

- **Engine independence is genuine**
  - **Shared position**: Both reviews confirm FR-012 is correctly implemented (functional-typing Alignment, devils-advocate Alignment).
  - **Combined evidence**: Both cite SKILL.md L2127-2135.
  - **Confidence level**: High. Universal agreement.

- **Preset gap exists and needs addressing**
  - **Shared position**: The spec example showing `preset: review/thorough` for gates contradicts the single-agent preset system (functional-typing Off-Base Assumptions and Recommendation 1, devils-advocate Off-Base Assumptions third point).
  - **Combined evidence**: Both trace from spec L65-66 to the preset system.
  - **Confidence level**: High. All three reviewers found this independently.

- **Re-run audit trail design is correct**
  - **Shared position**: The attempt-based archival system is well-designed (functional-typing Alignment, devils-advocate Alignment).
  - **Combined evidence**: Both cite SKILL.md L2114-2125. functional-typing adds the numeric sorting detail (Recommendation 4) which devils-advocate does not challenge.
  - **Confidence level**: Medium-High.
