# Cooperative Review — Phase 1: Initial Utilization Review

**Agent**: devils-advocate

---

### Executive Summary

Spec 011 and its SKILL.md implementation present phase consensus gates as a thin orchestration layer that generates standard conversus configs, runs them through the existing engine, and interprets results for CI/CD consumption. The pitch is appealing: reuse the engine, keep gates dumb, let the deliberation do the work. But this simplicity may be a trap. Several design decisions that seem clean on paper create failure modes that only surface in real CI/CD usage, where false positives block deployments and false negatives let bad code through.

The biggest risk in this spec is not what it does wrong, but what it fails to address. The gap between "gate as conceptual quality check" and "gate as CI/CD pipeline stage" is wider than the spec acknowledges. Real pipelines need timeout handling, resource budgets, deterministic behavior across runs, and fast feedback loops. The spec gives us structured output and exit codes but leaves the operational concerns to "the calling automation" — a hand-wave that will frustrate every team that tries to adopt gates in production.

My most important recommendation: the spec must define a timeout mechanism for gate execution. A gate that hangs indefinitely blocks a CI/CD pipeline with no recourse.

### Alignment

- **Engine independence is genuine** (spec L56-57, SKILL.md L2127-2135): The gate truly does not modify the engine. The generated `conversus.yml` is a standard config. This is the strongest design decision in the spec.

- **Exit codes are correct and sufficient** (spec L47, SKILL.md L2039-2055): 0/1/2 covers the three meaningful outcomes. The mapping is unambiguous and CI-friendly.

- **Re-run audit trail is well-designed** (spec L53, SKILL.md L2114-2125): Moving previous output to `attempt-N/` preserves history without cluttering the current output. The attempt number in `gate-result.md` provides traceability.

- **gate-result.md is machine-parseable** (spec L48-49, SKILL.md L1972-2015): The structured markdown format with fixed headings and predictable values enables automated parsing. The Verdict field's three possible values (PASS/BLOCK/ERROR) are exhaustive.

### Missed Opportunities

- **No timeout mechanism**: Neither the spec nor SKILL.md defines a timeout for gate execution. A conversus run with 3 agents, 2 rounds, and arbitration could take 30+ minutes. In a CI/CD pipeline, this is unacceptable without a timeout. The run engine has no timeout concept either, so this is a gap at both levels. Impact: high.

- **No resource budget / agent count limit**: Gate configuration inherits all run engine features, including multi-round execution. A gate with `rounds: 5` and 5 agents would launch 130+ agents. There is no mechanism to limit gate resource consumption. CI/CD pipelines need predictable resource usage. Impact: high.

- **No idempotency guarantee**: Re-running a gate against the same artifact may produce different verdicts because LLM outputs are non-deterministic. The spec does not acknowledge this or provide mitigation (e.g., requiring multiple passing runs, or a quorum mechanism). Impact: high.

- **No gate bypass mechanism**: When a gate blocks a critical hotfix, there is no documented bypass procedure. CI/CD pipelines need an escape hatch. A `--force-pass` flag or a `CONVERSUS_GATE_BYPASS=true` environment variable would be expected. Impact: medium.

- **No artifact validation depth**: The gate validates that the artifact path exists (SKILL.md L1942) but does not validate artifact content. An empty file or a binary file would pass artifact validation and produce a meaningless deliberation. Impact: medium.

- **No gate result aggregation across phases**: If a project defines gates for spec, plan, and implementation phases, there is no mechanism to get an aggregate view of all gate results. Each gate runs independently. Impact: low.

- **`always` pass criteria undermines the concept**: The `always` pass criteria (spec L36, SKILL.md L1932) means the gate always passes regardless of deliberation quality. This creates a false sense of security — the gate ran, so the pipeline shows green, but the output may contain critical findings that no one reads. Impact: medium.

### Off-Base Assumptions

- **CI/CD integration is just exit codes**: The spec assumes that exit codes and structured output are sufficient for CI/CD integration (spec L47, L102). Real CI/CD integration requires: timeout handling, resource limits, parallel execution support (multiple gates on different artifacts), caching (skip gate if artifact unchanged), and notification on failure. Exit codes are the minimum, not the solution.

- **Deliberation quality is consistent across runs**: The spec assumes that a gate's verdict is meaningful as a binary signal. But LLM-based deliberation is inherently non-deterministic. The same artifact can produce 0 disputes in one run and 3 in another. The spec treats the verdict as if it is as reliable as a test suite, which it is not.

- **Single-agent presets are useful for gates**: The spec example (L65-66) shows `preset: review/thorough` as a gate agent config. The SKILL.md catches the minimum-2-agents violation, but the real issue is that single-agent presets were never designed for multi-agent deliberation. The spec should acknowledge this gap rather than showing an example that will fail.

- **Re-runs start from scratch**: The spec assumes re-runs are independent (SKILL.md L2114-2125). But if a gate blocked because of 2 disputes, and the user fixed one issue and re-ran, the new deliberation has no knowledge of the previous findings. It may find the same 2 original disputes (not noticing the fix) or find entirely different disputes. This makes re-runs unreliable as a "fix and retry" workflow.

### Actionable Recommendations

1. **Add gate execution timeout** (Priority: P1)
   - **Current state**: No timeout mechanism exists in the spec, SKILL.md, or run engine.
   - **Proposed change**: Add to gate config schema: `timeout: <seconds>` (optional, no default). When set, the gate terminates execution after the specified duration and produces an ERROR verdict with: "Gate execution timed out after {timeout}s." In the generated conversus.yml, add a comment: `# timeout: {timeout}s (enforced by gate handler)`.
   - **Rationale**: CI/CD pipelines cannot tolerate unbounded execution times. Every pipeline stage needs a timeout.
   - **Risk if ignored**: Gates hang indefinitely in CI/CD pipelines with no automated recovery.

2. **Add agent count limit for gates** (Priority: P1)
   - **Current state**: Gates inherit all run engine features without resource limits.
   - **Proposed change**: Add to gate config schema: `max_agents: <N>` (optional, default: 50). Before executing, compute the estimated agent count (using the formula at SKILL.md L318-319). If estimated count exceeds `max_agents`, fail with ERROR: "Gate would launch {estimated} agents, exceeding max_agents limit of {max_agents}. Reduce rounds, agents, or iterations."
   - **Rationale**: Prevents runaway resource consumption in CI/CD environments.
   - **Risk if ignored**: A misconfigured gate could launch hundreds of agents, consuming excessive resources.

3. **Acknowledge non-determinism in gate-result.md** (Priority: P1)
   - **Current state**: gate-result.md presents a binary verdict without confidence information.
   - **Proposed change**: Add a `## Confidence` section to gate-result.md: `<deterministic | advisory>`. Set to `advisory` always (since LLM deliberation is non-deterministic). Add a note in the spec: "Gate verdicts are advisory quality signals, not deterministic test results. Teams should calibrate their pipeline response accordingly."
   - **Rationale**: Prevents teams from treating gate verdicts as equivalents to test suite results.
   - **Risk if ignored**: False confidence in gate verdicts leads to either pipeline gridlock (too strict) or ignored gates (too lenient).

4. **Add gate bypass mechanism** (Priority: P2)
   - **Current state**: No bypass mechanism exists.
   - **Proposed change**: Add `--force-pass` flag to `/conversus gate`. When set: run the deliberation normally, write full output, but set the verdict to PASS regardless of dispute count. Include in gate-result.md: `## Bypass: true` and `## Bypass Reason: <user-supplied reason>`. Require `--force-pass-reason "reason"` to ensure accountability.
   - **Rationale**: Critical hotfixes cannot be blocked by advisory quality gates. Bypass with audit trail is standard practice.
   - **Risk if ignored**: Teams will bypass gates by removing them from the pipeline entirely, losing all quality signal.

5. **Add artifact content validation** (Priority: P2)
   - **Current state**: SKILL.md L1942 validates artifact path existence only.
   - **Proposed change**: After path validation, check: (a) file is not empty, (b) file is a text file (not binary), (c) file size is under a reasonable limit (e.g., 1MB for single files). If validation fails, produce ERROR verdict: "Artifact validation failed: {reason}."
   - **Rationale**: Empty or binary artifacts produce meaningless deliberations that waste resources and produce misleading verdicts.
   - **Risk if ignored**: Garbage-in-garbage-out gate runs that appear legitimate.

6. **Reconsider the `always` pass criteria** (Priority: P2)
   - **Current state**: `always` pass criteria (SKILL.md L1932) means the gate always passes.
   - **Proposed change**: Rename to `advisory` (clearer semantics). Add to the post-execution report for advisory gates: "This gate ran in advisory mode. Review the synthesis for quality findings even though the gate passed." Set exit code to 0 but add a warning indicator.
   - **Rationale**: "always pass" sends the wrong signal. "Advisory" communicates the intent accurately.
   - **Risk if ignored**: Teams deploy `pass: always` to stop pipeline blocking without understanding they are silencing quality signals.

7. **Document re-run limitations** (Priority: P3)
   - **Current state**: Re-runs are independent deliberations (SKILL.md L2114-2125).
   - **Proposed change**: Add to the re-run section: "Note: re-runs are independent deliberations. The new run does not have access to the previous attempt's findings. For improved re-run quality, consider using the prior context mechanism (future enhancement)."
   - **Rationale**: Sets correct expectations about re-run behavior.
   - **Risk if ignored**: Users assume re-runs are incremental and are confused when they get different results.

8. **Add gate execution summary to gate-result.md** (Priority: P3)
   - **Current state**: gate-result.md contains the verdict and disputes but not execution metadata.
   - **Proposed change**: Add `## Execution` section: agent count, rounds executed, total duration (if measurable), termination reason (for multi-round gates).
   - **Rationale**: Execution metadata helps diagnose gate performance issues in CI/CD.
   - **Risk if ignored**: No visibility into gate execution characteristics.

### Referenced Documentation

- `specs/011-phase-consensus-gates/spec.md` — sections/lines cited: L31, L36, L41, L42, L47-49, L53, L56-57, L65-66, L89-94, L102
- `SKILL.md` — sections/lines cited: L318-319, L773, L1859-1867, L1877-1880, L1908-1913, L1920-1924, L1932, L1942, L1946-1954, L1959, L1972-2015, L2005-2007, L2039-2055, L2061-2112, L2114-2125, L2127-2135
