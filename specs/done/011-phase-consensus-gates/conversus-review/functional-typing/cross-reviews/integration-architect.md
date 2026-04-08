# Cooperative Cross-Review — Phase 2

**Reviewer**: functional-typing
**Reviewed**: integration-architect

---

### Dangerous Contradictions

- **Dispute-Parsing failure semantics**
  - **integration-architect claims**: Parsing failures should produce an ERROR verdict (exit code 2) rather than BLOCK (Recommendation 1, Actionable Recommendations). Their argument: "A BLOCK verdict implies the deliberation ran correctly but found issues. A parse failure is a system error."
  - **functional-typing claims**: The current default behavior (SKILL.md L773, treat as having disputes) feeds into the gate verdict as BLOCK (my Missed Opportunities, "Error verdict in gate-result.md"). I framed this as needing specification but did not explicitly advocate for ERROR over BLOCK.
  - **Why this is dangerous**: If functional-typing's framing stands (BLOCK on parse failure), CI/CD pipelines will treat infrastructure failures as quality findings. If integration-architect's framing stands (ERROR), pipelines can retry infrastructure failures but not quality blocks. Both cannot be correct — the exit code is a single value.
  - **Suggested resolution**: integration-architect's position is stronger. ERROR (exit code 2) for parse failures is correct because it distinguishes infrastructure failures from quality findings. functional-typing should concede this point.

- **max_disputes N validation — zero handling**
  - **integration-architect claims**: "N must be a non-negative integer. 0 is allowed and is equivalent to converged" (Recommendation 8).
  - **functional-typing claims**: "max_disputes 0 is valid and equivalent to converged. Emit info message" (Recommendation 7). Additionally, Recommendation 2 says "N must be a positive integer (1 or greater)."
  - **Why this is dangerous**: functional-typing's Recommendation 2 (positive integer, 1 or greater) contradicts Recommendation 7 (0 is valid). integration-architect's position (non-negative) is internally consistent. If both recommendations are implemented, 0 is simultaneously invalid (Rec 2) and valid (Rec 7).
  - **Suggested resolution**: functional-typing should fix the internal inconsistency. Non-negative integer (0 or greater) is the correct constraint — 0 is logically valid as equivalent to `converged`.

- **No additional contradictions identified.**

### Tensions

- **Prior context for re-runs**
  - **integration-architect's position**: Recommends automatic `prior` context injection for re-runs (Recommendation 3), with opt-in flag `prior_on_rerun: true`.
  - **functional-typing's position**: Did not address re-run context at all. Focused on attempt numbering mechanics (Recommendation 4).
  - **Nature of tension**: integration-architect adds a feature that functional-typing did not consider. If adopted, it changes the re-run semantics that functional-typing's attempt numbering relies on — attempt-N output becomes both an archive and a potential input.
  - **Coordination needed**: If `prior_on_rerun` is adopted, the attempt archival process (functional-typing's Recommendation 4) must preserve the synthesis file in a predictable location for `prior` resolution.

- **Stagnation and iterations in gate config**
  - **integration-architect's position**: Gate config should include `stagnation` and `iterations` fields (Recommendation 2).
  - **functional-typing's position**: Did not address these fields — focused on validation and parsing within the existing schema.
  - **Nature of tension**: Adding fields expands the gate schema without functional-typing's review for structural completeness. Each new field needs validation rules, error messages, and default values.
  - **Coordination needed**: If these fields are added, functional-typing should define their validation rules and error messages, consistent with the run engine's validation (SKILL.md L224-232).

- **SC verification mapping**
  - **integration-architect's position**: Wants an explicit FR-to-implementation mapping table (Recommendation 4).
  - **functional-typing's position**: Verified FR mapping implicitly through the Alignment section but did not produce a formal table.
  - **Nature of tension**: integration-architect wants a structural artifact; functional-typing already performed the verification informally. The question is whether the mapping should be a persistent document or an analysis-time activity.
  - **Coordination needed**: Both should agree on whether the mapping lives in the spec, SKILL.md, or only in review artifacts.

### Safe Agreements

- **Engine independence is correctly implemented**
  - **Shared position**: Both reviews confirm FR-012 is properly implemented — gates generate standard configs, the engine has zero gate awareness (functional-typing Alignment section, integration-architect Alignment section).
  - **Combined evidence**: functional-typing cites SKILL.md L2127-2135; integration-architect cites the same section plus L1955 (generated config). Both independently verified the boundary.
  - **Confidence level**: High. This is the strongest consensus point.

- **Exit codes are correct and sufficient**
  - **Shared position**: Both reviews confirm FR-008's three exit codes (0/1/2) are correctly mapped and CI-friendly (functional-typing Alignment, integration-architect Alignment).
  - **Combined evidence**: Both cite SKILL.md L2039-2055 and spec L47.
  - **Confidence level**: High.

- **Flag-override precedence needs specification**
  - **Shared position**: Both reviews independently identified that CLI flag override behavior is unspecified (functional-typing Recommendation 3, integration-architect Recommendation 5).
  - **Combined evidence**: Both cite SKILL.md L1877-1880. Both recommend explicit "flags override config" semantics.
  - **Confidence level**: High. Identical recommendation from independent review.

- **Preset-to-multi-agent gap exists**
  - **Shared position**: Both reviews identify that the spec example showing `preset: review/thorough` for gates contradicts the single-agent preset system (functional-typing Off-Base Assumptions, integration-architect Off-Base Assumptions).
  - **Combined evidence**: Both trace from spec L65-66 through SKILL.md L126-200 to L1924.
  - **Confidence level**: High. Both independently found the same structural gap.
