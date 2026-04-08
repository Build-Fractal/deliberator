# Cooperative Revision — Phase 3

**Agent**: devils-advocate
**Iteration**: 1

---

### Recommendation Dispositions

#### Recommendation 1: Add gate execution timeout
- **Original position**: Add `timeout: <seconds>` to gate config schema for CI/CD pipeline safety.
- **Disposition**: Modified
- **Explanation**: functional-typing's cross-review (Dangerous Contradictions, "Timeout as P1 requirement") raised a valid question: is timeout a gate concern or a pipeline concern? CI/CD runners already have step-level timeouts. Adding a gate-level timeout creates a second mechanism. integration-architect's cross-review (Dangerous Contradictions, "Gate scope") argued operational features shift the complexity boundary. Modified recommendation: Do not add `timeout` to the gate config schema. Instead, add to the spec's Constraints section or a CI/CD Integration Guidance subsection: "Gate execution time is proportional to agent count and round count. CI/CD pipelines should configure step-level timeouts appropriate to their gate configuration. A 3-agent, 1-round gate typically completes in 5-15 minutes. Multi-round gates may take proportionally longer." This provides guidance without duplicating runner functionality.

#### Recommendation 2: Add agent count limit for gates
- **Original position**: Add `max_agents: <N>` to gate config schema.
- **Disposition**: Modified
- **Explanation**: integration-architect's cross-review (Tensions, "Agent count limits") noted that the pre-execution estimate already computes agent counts. The estimate exists as an informational message (SKILL.md L316-322). Modified recommendation: Rather than adding a new `max_agents` field, enhance the pre-execution estimate to emit a WARNING when the count exceeds a threshold (e.g., 50). For gates specifically, if the estimated count exceeds 50, warn: "This gate will launch approximately {N} agents. Consider reducing rounds or agent count for CI/CD efficiency." No hard limit — the warning is sufficient for gate users to self-correct. This avoids adding gate-specific configuration that the run engine does not have.

#### Recommendation 3: Acknowledge non-determinism in gate-result.md
- **Original position**: Add a `## Confidence` section to gate-result.md.
- **Disposition**: Modified
- **Explanation**: Both functional-typing and integration-architect's cross-reviews pushed back on adding confidence to the schema (functional-typing cross-review, Dangerous Contradictions, "Non-determinism"; integration-architect cross-review, Dangerous Contradictions, "Non-determinism acknowledgment"). The consensus is that non-determinism should be acknowledged in guidance, not in the schema. Modified recommendation: Add a note to the spec's Constraints section: "Gate verdicts are derived from LLM-based deliberation, which is non-deterministic. The same artifact may produce different dispute counts across runs. Teams should calibrate pass criteria to account for variance — `max_disputes 1` provides more stability than `converged`." Do not add a Confidence section to gate-result.md.

#### Recommendation 4: Add gate bypass mechanism
- **Original position**: Add `--force-pass` flag with mandatory reason.
- **Disposition**: Surviving
- **Explanation**: integration-architect's cross-review (Tensions, "Gate bypass vs. pass criteria flexibility") distinguished bypass (per-run override) from pass criteria (persistent configuration). This distinction strengthens my recommendation: bypass and `pass: always` serve different purposes. Bypass is an emergency escape hatch with audit trail. `pass: always` is a persistent configuration choice. No reviewer argued that bypass is unnecessary — the tension was about how it relates to existing pass criteria, not whether it should exist. The recommendation stands with an addition: document how `--force-pass` differs from `pass: always`.

#### Recommendation 5: Add artifact content validation
- **Original position**: Validate artifact content — not empty, is text, under size limit.
- **Disposition**: Modified
- **Explanation**: No cross-review directly challenged this, but on reflection during revision, the size limit is arbitrary and the text-vs-binary check is fragile. Modified recommendation: Validate that the artifact is not empty. If the artifact is a single file with 0 bytes, fail with ERROR: "Artifact is empty: {path}." If the artifact is a directory with no .md files, the existing run engine target resolution handles this. Drop the size limit and binary check — the run engine reads files and will naturally fail on binary content. Keep the empty check as a fast-fail.

#### Recommendation 6: Reconsider the `always` pass criteria naming
- **Original position**: Rename `always` to `advisory`.
- **Disposition**: Withdrawn
- **Explanation**: integration-architect's cross-review (Tensions, "`always` vs. `advisory` naming") and functional-typing's cross-review (Dangerous Contradictions, "`always` pass criteria naming") both noted this is a naming preference, not a structural issue. I initially framed this as a usability concern, but on reflection, `always` is accurate and the spec is not yet shipped — renaming later is low-cost if needed. The substance of my concern (users ignoring advisory output) is better addressed by the post-execution report guidance than by renaming. I withdraw the naming recommendation.

#### Recommendation 7: Document re-run limitations
- **Original position**: Add a note documenting that re-runs are independent deliberations.
- **Disposition**: Surviving
- **Explanation**: integration-architect proposed `prior_on_rerun` as a feature enhancement (Recommendation 3, modified in their revision). This addresses part of the limitation but not all of it. My recommendation to document the limitation is still valuable as a user-facing explanation, even if `prior_on_rerun` is implemented. The documentation should note: "Re-runs are independent deliberations by default. If prior_on_rerun is enabled, the previous attempt's synthesis provides context but does not guarantee consistent findings."

#### Recommendation 8: Add gate execution summary to gate-result.md
- **Original position**: Add a `## Execution` section to gate-result.md with agent count, rounds, duration.
- **Disposition**: Surviving
- **Explanation**: No cross-review challenged this. The information is readily available after execution and adds diagnostic value for CI/CD operators. The recommendation stands as originally stated.

### New Recommendations

No new recommendations. The cross-review process did not surface issues outside the scope of my original review. The modifications to existing recommendations (especially Recs 1, 2, 3) represent the integration of feedback rather than new concerns.

### Position Summary

I withdrew 1 recommendation (Rec 6, `always`-to-`advisory` rename), modified 4 (Recs 1, 2, 3, 5), and maintained 3 (Recs 4, 7, 8). No new recommendations added.

The most significant change was demoting timeout and resource limits from gate-config features to guidance (Recs 1, 2). functional-typing and integration-architect correctly argued that these are CI/CD runner responsibilities, not gate responsibilities. The gate's job is orchestration and verdict — operational constraints belong to the environment. This sharpened my understanding of the gate's scope boundary.

My remaining highest-priority recommendation is Recommendation 4 (gate bypass mechanism). No reviewer argued against its necessity. The `--force-pass` flag with mandatory reason and audit trail is essential for real-world CI/CD adoption. Critical hotfixes cannot be blocked by advisory quality gates, and the bypass mechanism with accountability is the standard solution.
