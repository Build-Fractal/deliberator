# Cooperative Cross-Review — Phase 2

**Reviewer**: integration-architect
**Reviewed**: devils-advocate

---

### Dangerous Contradictions

- **Gate scope: orchestration vs. operational platform**
  - **devils-advocate claims**: Gates need timeout, resource limits, bypass mechanisms, artifact content validation (Recommendations 1, 2, 4, 5). These are framed as P1/P2 requirements.
  - **integration-architect claims**: Gates are an integration layer — they generate configs and delegate to the run engine (Alignment section). Missing integration fields (stagnation, iterations, prior) are within scope. Operational platform features are not.
  - **Why this is dangerous**: If devils-advocate's operational features are adopted, the gate handler grows from a thin orchestration layer to a full CI/CD platform component. This contradicts the spec's explicit constraint at L100: "Must NOT modify the engine." While the features are technically in the handler (not the engine), they shift the complexity boundary significantly.
  - **Suggested resolution**: Separate operational concerns from specification concerns. Timeout and resource limits should be documented as CI/CD runner responsibilities with guidance, not embedded in the gate spec. Bypass is a legitimate gate feature because it affects the gate-result.md output (auditability). Accept bypass, defer timeout and resource limits.

- **Non-determinism acknowledgment**
  - **devils-advocate claims**: Gate verdicts are "advisory quality signals, not deterministic test results" (Recommendation 3). Wants a `## Confidence` section in gate-result.md.
  - **integration-architect claims**: Treated gate verdicts as deterministic outputs of the Dispute-Parsing Subsystem (Alignment, FR-007). The subsystem produces integer counts that feed into pass criteria comparison — this is deterministic.
  - **Why this is dangerous**: If devils-advocate is right, the entire exit code framework is misleading. If integration-architect is right, the confidence section adds noise. The truth is nuanced: the deliberation is non-deterministic, but the verdict derivation (dispute count vs. threshold) is deterministic.
  - **Suggested resolution**: Acknowledge non-determinism in spec guidance (as a note, not in the schema). The gate correctly applies deterministic rules to non-deterministic input — this is well-understood in quality tooling (e.g., flaky test detection). Do not add confidence to gate-result.md.

- **No additional contradictions identified.**

### Tensions

- **`always` vs. `advisory` naming**
  - **devils-advocate's position**: Rename `always` to `advisory` (Recommendation 6) for clearer semantics.
  - **integration-architect's position**: Did not challenge the naming. Used `always` without comment.
  - **Nature of tension**: `always` is accurate but potentially misleading. `advisory` better communicates intent but changes the spec's vocabulary. The naming affects how teams perceive and use the criteria.
  - **Coordination needed**: Decide at the spec level. Both names are valid; the choice affects documentation and user guidance more than implementation.

- **Gate bypass vs. pass criteria flexibility**
  - **devils-advocate's position**: Add `--force-pass` flag with mandatory reason (Recommendation 4).
  - **integration-architect's position**: Did not address bypass. The pass criteria system (`converged`, `max_disputes`, `always`) already provides flexibility.
  - **Nature of tension**: Bypass is a runtime override; pass criteria is a configuration choice. Both achieve the same outcome (gate passes) but through different mechanisms with different accountability models. Bypass leaves an audit trail per-invocation; `always` is a persistent configuration.
  - **Coordination needed**: If bypass is added, document how it differs from `pass: always`. Bypass is per-run with reason. `always` is persistent without per-run justification.

- **Agent count limits**
  - **devils-advocate's position**: Add `max_agents` to gate config (Recommendation 2). Hard limit with ERROR on exceeded.
  - **integration-architect's position**: The pre-execution estimate (SKILL.md L318-319) already computes agent counts. Did not propose a limit.
  - **Nature of tension**: The estimate exists but is informational. Adding a limit makes it enforceable. This is a policy question: should the gate prevent expensive configurations, or just report them?
  - **Coordination needed**: If `max_agents` is added, it must use the same formula as the pre-execution estimate. The gate handler enforces the limit before delegating to the run engine.

### Safe Agreements

- **Engine independence is genuine**
  - **Shared position**: Both reviews affirm FR-012 (integration-architect Alignment, devils-advocate Alignment: "strongest design decision in the spec").
  - **Combined evidence**: Both cite SKILL.md L2127-2135 and spec L56-57.
  - **Confidence level**: High.

- **Exit codes are correct**
  - **Shared position**: Both reviews confirm the 0/1/2 exit code mapping is sufficient (integration-architect Alignment, devils-advocate Alignment).
  - **Combined evidence**: Both cite SKILL.md L2039-2055.
  - **Confidence level**: High.

- **Re-run behavior needs enhancement**
  - **Shared position**: Both reviews approve the current re-run mechanism but identify limitations. integration-architect recommends `prior_on_rerun` (Recommendation 3). devils-advocate documents re-run limitations (Recommendation 7).
  - **Combined evidence**: Both identify the gap between "archive and restart" and "incremental improvement." The direction is the same — re-runs should benefit from previous attempt context.
  - **Confidence level**: Medium. Agreement on the gap but different solutions (automatic prior injection vs. documented limitation).
