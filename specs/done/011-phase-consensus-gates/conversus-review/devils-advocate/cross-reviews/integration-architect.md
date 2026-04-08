# Cooperative Cross-Review — Phase 2

**Reviewer**: devils-advocate
**Reviewed**: integration-architect

---

### Dangerous Contradictions

- **Dispute-Parsing failure: ERROR vs. nuanced handling**
  - **integration-architect claims**: Parsing failures should always produce ERROR verdict (exit code 2) (Recommendation 1). The argument: "A parse failure is a system error, not a quality finding."
  - **devils-advocate claims**: Parsing failures are part of the broader non-determinism problem (Recommendation 3). The specific exit code matters less than acknowledging that gate verdicts are advisory, not deterministic.
  - **Why this is dangerous**: integration-architect's ERROR verdict for parse failures is clean but hides information. If the synthesis exists but lacks dispute markers, the deliberation did run — calling it ERROR misrepresents what happened. If the synthesis does not exist, ERROR is correct. The distinction matters for CI/CD retries (retry errors, escalate blocks).
  - **Suggested resolution**: Two-tier approach: (1) No synthesis file = ERROR (exit code 2), (2) Synthesis exists but markers/headings missing = BLOCK (exit code 1) with a note in gate-result.md: "Dispute count determined via fallback parsing." This preserves the useful distinction.

- **Prior context injection for re-runs**
  - **integration-architect claims**: Automatic `prior_on_rerun: true` injects previous attempt's synthesis as prior context (Recommendation 3).
  - **devils-advocate claims**: Re-runs are fundamentally unreliable due to non-determinism (Off-Base Assumptions, Recommendation 7). Adding prior context may make re-runs more consistent but does not address the core issue.
  - **Why this is dangerous**: If `prior_on_rerun` is adopted, re-runs are no longer independent — they are influenced by previous (potentially wrong) findings. If a previous gate run found a false positive, the re-run inherits that bias through prior context. This could make re-runs worse, not better.
  - **Suggested resolution**: If `prior_on_rerun` is adopted, it must be opt-in (integration-architect already proposes this) AND the prior context should be clearly marked as previous-attempt context, distinct from intentional prior context. The gate handler should warn: "Prior context from attempt {N-1} injected. Previous findings may influence this run."

### Tensions

- **Integration completeness vs. operational safety**
  - **integration-architect's position**: Comprehensive integration: stagnation, iterations, prior context, SC mapping, validate_templates pass-through (Recommendations 2, 3, 4, 6). The gate should expose all run engine capabilities.
  - **devils-advocate's position**: Operational safety: timeout, resource limits, bypass, artifact validation (Recommendations 1, 2, 4, 5). The gate should protect against misuse.
  - **Nature of tension**: integration-architect wants to maximize what gates can do. devils-advocate wants to limit what gates can do wrong. Fully capable gates that can be misconfigured are worse than limited gates that always behave predictably.
  - **Coordination needed**: Prioritize safety constraints (devils-advocate) alongside capability exposure (integration-architect). Every new capability should ship with corresponding guardrails.

- **SC verification formalism**
  - **integration-architect's position**: Wants an explicit FR-to-implementation mapping table (Recommendation 4).
  - **devils-advocate's position**: Did not address SC verification — focused on what the spec misses, not how to verify what it has.
  - **Nature of tension**: Verification mapping is valuable for correctness but adds overhead to the spec. devils-advocate would argue that verifying the existing spec is less important than fixing its gaps.
  - **Coordination needed**: The mapping table is useful as a review artifact (produced during review, not embedded in the spec). This satisfies integration-architect's traceability need without adding spec overhead.

- **Naming: `always` vs. `advisory`**
  - **integration-architect's position**: Did not challenge the naming (used `always` without comment).
  - **devils-advocate's position**: Rename to `advisory` (Recommendation 6) for clearer semantics and user guidance.
  - **Nature of tension**: Naming affects perception. `always` is technically accurate. `advisory` communicates intent. Integration-architect may prefer stability (no naming changes). devils-advocate prefers clarity (rename before shipping).
  - **Coordination needed**: Decide before implementation. Post-implementation rename is a breaking change.

### Safe Agreements

- **Engine independence is the right design**
  - **Shared position**: Both reviews affirm FR-012 is the strongest aspect of the spec (integration-architect Alignment, devils-advocate Alignment: "strongest design decision").
  - **Combined evidence**: Both cite SKILL.md L2127-2135 and spec L56-57.
  - **Confidence level**: High. Universal agreement.

- **Exit codes are correct**
  - **Shared position**: Both reviews confirm the 0/1/2 mapping is appropriate (integration-architect Alignment, devils-advocate Alignment).
  - **Combined evidence**: Both cite SKILL.md L2039-2055.
  - **Confidence level**: High.

- **Re-run limitations exist**
  - **Shared position**: Both reviews identify that re-runs start from scratch as a limitation. integration-architect proposes `prior_on_rerun` (Recommendation 3). devils-advocate documents the limitation (Recommendation 7).
  - **Combined evidence**: Both cite SKILL.md L2114-2125. Both agree re-runs could be better — they disagree on how.
  - **Confidence level**: Medium. Agreement on the problem, different solutions.

- **Flag override semantics need specification**
  - **Shared position**: integration-architect recommends explicit "flags override config" (Recommendation 5). devils-advocate did not address this directly but the implied CI/CD model requires override capability.
  - **Combined evidence**: integration-architect cites SKILL.md L1877-1880. The agreement is indirect but directionally aligned.
  - **Confidence level**: Medium. One explicit, one implied.
