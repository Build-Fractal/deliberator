# Cooperative Cross-Review — Phase 2

**Reviewer**: functional-typing
**Reviewed**: devils-advocate

---

### Dangerous Contradictions

- **Timeout as P1 requirement**
  - **devils-advocate claims**: Gate execution timeout is P1 — CI/CD pipelines cannot tolerate unbounded execution (Recommendation 1). They argue this should be in the gate config schema.
  - **functional-typing claims**: Did not address timeout at all. My review focused on structural correctness of the existing spec, not operational concerns.
  - **Why this is dangerous**: If timeout is truly P1, then the spec has a blocking gap that functional-typing missed entirely. If timeout is not the gate's responsibility (but rather the CI/CD runner's), then adding it to the gate config schema adds unnecessary complexity. The question is scope: is timeout a gate concern or a pipeline concern?
  - **Suggested resolution**: This requires genuine deliberation. CI/CD runners (GitHub Actions, Jenkins) already have step-level timeouts. Adding a gate-level timeout creates a second timeout mechanism that may conflict with the runner's timeout. However, the gate-level timeout can provide earlier, more informative failure (ERROR verdict vs. runner kill). devils-advocate should defend why the gate needs its own timeout rather than relying on the runner.

- **Non-determinism as a fundamental design flaw**
  - **devils-advocate claims**: "Gate verdicts are advisory quality signals, not deterministic test results" (Recommendation 3). They argue gate-result.md should include a `## Confidence` section.
  - **functional-typing claims**: Treated gate verdicts as deterministic outputs of a well-defined process (Alignment section treats exit codes as unambiguous).
  - **Why this is dangerous**: If devils-advocate is right that non-determinism is a fundamental concern, then the entire exit code framework is misleading — a PASS verdict has an unknown confidence level. If functional-typing is right that the process is well-defined, then adding confidence levels adds noise without value.
  - **Suggested resolution**: Both positions have merit. Non-determinism exists but is bounded by the deliberation structure. The gate does not need a confidence section, but the spec should acknowledge non-determinism in its CI/CD integration guidance. A note in the spec is more appropriate than a schema change.

- **`always` pass criteria naming**
  - **devils-advocate claims**: Rename `always` to `advisory` for clearer semantics (Recommendation 6).
  - **functional-typing claims**: Did not challenge the naming. Documented the three criteria values without comment.
  - **Why this is dangerous**: Not deeply dangerous, but the naming affects user behavior. `always` communicates "this gate always passes" which is accurate. `advisory` communicates "this gate provides advice" which is also accurate but implies the output should be reviewed. The names produce different pipeline behaviors.
  - **Suggested resolution**: This is a naming preference, not a structural issue. Either name works if documented clearly. The spec owner should decide.

### Tensions

- **Scope of gate responsibility**
  - **devils-advocate's position**: Gates should handle timeout, resource limits, bypass mechanisms, artifact content validation — operational concerns beyond orchestration (Recommendations 1, 2, 4, 5).
  - **functional-typing's position**: Gates are structural correctness checks. The review focused on schema validation, parsing rules, and error messages — the spec's own domain (Recommendations 1-8).
  - **Nature of tension**: devils-advocate expands the gate's responsibility boundary to include operational concerns. functional-typing stays within the spec's stated scope. If both positions are adopted, the gate becomes both an orchestration layer AND an operational platform.
  - **Coordination needed**: Agree on scope. Either the gate handles operational concerns (timeout, resources) or it explicitly defers them to the CI/CD runner with documented guidance on how runners should configure those controls.

- **Agent count limit**
  - **devils-advocate's position**: Add `max_agents` to gate config (Recommendation 2). Prevent misconfigured gates from launching excessive agents.
  - **functional-typing's position**: Did not address resource limits. Focused on the existing config schema.
  - **Nature of tension**: Adding `max_agents` is a new validation rule that interacts with the run engine's agent count formula (SKILL.md L318-319). It adds a gate-specific constraint that the run engine does not have.
  - **Coordination needed**: If `max_agents` is added, it must be validated before the run engine starts, using the pre-execution estimate formula. The gate handler, not the run engine, enforces this limit.

- **Gate bypass mechanism**
  - **devils-advocate's position**: Add `--force-pass` flag with mandatory reason (Recommendation 4).
  - **functional-typing's position**: Did not address bypass — the spec does not mention it and the review stayed within spec scope.
  - **Nature of tension**: Bypass fundamentally changes the trust model. A gate that can be bypassed is not a gate — it is an advisory step. This interacts with the `always` pass criteria: if bypass exists, `always` is redundant.
  - **Coordination needed**: If bypass is added, clarify the relationship between `--force-pass` and `pass: always`. Are they different? (One is per-run, the other is persistent.) Document the accountability trail.

### Safe Agreements

- **Engine independence is genuine**
  - **Shared position**: Both reviews affirm that FR-012 is correctly implemented — gates do not modify the engine (functional-typing Alignment, devils-advocate Alignment).
  - **Combined evidence**: devils-advocate explicitly calls this "the strongest design decision in the spec." functional-typing cites the same SKILL.md sections.
  - **Confidence level**: High. Universal agreement across all three reviewers.

- **Re-run audit trail is well-designed**
  - **Shared position**: Both reviews approve the attempt-based archival system (functional-typing Alignment, devils-advocate Alignment).
  - **Combined evidence**: Both cite SKILL.md L2114-2125. Neither challenges the archive-and-increment approach.
  - **Confidence level**: Medium. Both approve the design but functional-typing notes the numeric vs. lexicographic sort issue, which is a detail within the approved design.

- **Preset gap must be addressed**
  - **Shared position**: The spec example showing `preset: review/thorough` for gates is problematic given single-agent presets (functional-typing Off-Base Assumptions, devils-advocate Off-Base Assumptions third point).
  - **Combined evidence**: Both trace from spec L65-66 to the preset system's single-agent resolution.
  - **Confidence level**: High.
