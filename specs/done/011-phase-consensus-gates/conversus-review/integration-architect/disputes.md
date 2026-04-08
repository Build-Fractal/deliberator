# Cooperative Disputes — Phase 4

**Agent**: integration-architect

---

### Remaining Disputes

- **Dispute: Gate config schema should include stagnation and iterations**
  - **My claim**: Gate config should include `stagnation` and `iterations` fields to expose core engine capabilities (Rec 2, surviving in revision).
  - **Opposing position(s)**: functional-typing argues the gate should ship with minimum viable schema and let the run engine defaults handle stagnation and iterations. Users who need these features can use `/conversus run` directly (functional-typing's implicit position — they did not address these fields and their revision did not adopt them).
  - **Why I will not concede**: Stagnation detection is not just a nice-to-have — it is a correctness feature for multi-round gates. A gate with `rounds: 3` and `stagnation: ignore` will waste resources running 3 full rounds even if disputes stabilize after round 1. The run engine defaults to `stagnation: detect`, but this is not documented in the gate context. Users configuring `rounds: 2` in a gate will not know whether stagnation detection applies. Omitting these fields from the gate config creates an invisible default dependency.
  - **Counter-argument to their position**: functional-typing argues the generated config inherits run engine defaults. This is true, but it violates a key principle: gate configurations should be self-documenting. A gate config that says `rounds: 2` but silently depends on the run engine's `stagnation: detect` default is not self-documenting. If the run engine changes its default, existing gates change behavior silently.
  - **Proposed resolution path**: At minimum, add `stagnation` to the gate config schema with the same default as the run engine (`detect`). `iterations` can be deferred if the synthesizer agrees it is less critical. The key principle: any run engine feature that affects gate behavior should be explicitly configurable in the gate schema.

- **Dispute: Gate bypass mechanism belongs in spec 011**
  - **My claim**: I did not originally propose bypass, but after reading devils-advocate's revised Rec 4, I believe bypass is a legitimate gate feature — not an operational concern. It affects gate-result.md output and provides an audit trail.
  - **Opposing position(s)**: functional-typing proposes deferring bypass to a follow-up spec (disputes section). Their argument: `pass: always` already provides a mechanism to make gates non-blocking, and bypass is a refinement, not a fundamental capability.
  - **Why I will not concede**: `pass: always` is a persistent configuration change. It requires modifying the gate definition (or adding a flag to the pipeline config). Bypass is a per-invocation override with accountability. These serve different needs. A deployment engineer who needs to push a hotfix cannot modify the gate definition — they need a runtime override. This is standard in CI/CD tooling (e.g., `git push --no-verify`, pipeline skip flags). Additionally, bypass affects gate-result.md (adding `## Bypass: true`), which is firmly within the gate's domain.
  - **Counter-argument to their position**: functional-typing argues bypass undermines the verdict's meaning. But the audit trail (mandatory reason, recorded in gate-result.md) preserves accountability. A bypassed gate is more auditable than a deleted gate stage.
  - **Proposed resolution path**: Include bypass in spec 011 with minimal scope: `--force-pass --force-pass-reason "reason"` flag, recorded in gate-result.md as `## Bypass: true` and `## Bypass Reason: <reason>`. Exit code is 0 on bypass. No other operational concerns are pulled in.

### Convergence

- **Converged: Preset-to-multi-agent gap**
  - **Shared position**: The spec example showing `preset: review/thorough` for gates is unimplementable. Fix the spec example and/or define multi-agent presets.
  - **Agreeing agents**: functional-typing (Rec 1), integration-architect (Off-Base Assumptions), devils-advocate (Off-Base Assumptions)
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1. Never contested.

- **Converged: max_disputes N non-negative integer**
  - **Shared position**: N must be a non-negative integer. 0 is valid and equivalent to `converged`.
  - **Agreeing agents**: functional-typing (Rec 2 modified), integration-architect (Rec 8 surviving)
  - **Strength**: Bilateral
  - **Path to convergence**: Converged in Phase 3 after cross-review exposed functional-typing's internal inconsistency.

- **Converged: CLI flag override precedence**
  - **Shared position**: CLI flags override gate config values. Standard convention.
  - **Agreeing agents**: functional-typing (Rec 3), integration-architect (Rec 5)
  - **Strength**: Bilateral
  - **Path to convergence**: Agreed from Phase 1.

- **Converged: Engine independence (FR-012)**
  - **Shared position**: Correctly implemented. Gates do not modify the engine.
  - **Agreeing agents**: All three.
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1.

- **Converged: Two-tier error handling**
  - **Shared position**: No synthesis = ERROR. Synthesis exists but unparseable = BLOCK with note.
  - **Agreeing agents**: functional-typing (Rec 5 modified), integration-architect (Rec 1 modified), devils-advocate (cross-review proposal)
  - **Strength**: Unanimous
  - **Path to convergence**: Converged in Phase 3 through cross-review.

- **Converged: Non-determinism guidance**
  - **Shared position**: Acknowledge in spec guidance, not in gate-result.md schema.
  - **Agreeing agents**: All three.
  - **Strength**: Unanimous
  - **Path to convergence**: Converged in Phase 3. devils-advocate modified original schema proposal.

### Final Position Statement

**Non-Negotiables**:

1. Stagnation must be explicitly configurable in the gate config schema. Invisible default dependencies in CI/CD configurations cause silent behavior changes when defaults change. (SKILL.md L229 — the current default is `detect`, but this could change.)

2. The two-tier error handling for Dispute-Parsing failures must be implemented. CI/CD pipelines need to distinguish ERROR (retry-worthy) from BLOCK (review-worthy). (Unanimous convergence.)

**Flexibility**:

1. `iterations` in gate config — I am willing to defer this if stagnation is included. Iterations is lower priority than stagnation for gate use cases.

2. Bypass mechanism — I believe it belongs in spec 011, but I am willing to accept deferral if the spec explicitly acknowledges the need and provides a deferral note. An undocumented gap is worse than a documented deferral.

3. `prior_on_rerun` — Opt-in with warnings is my preferred approach, but I am flexible on whether this is in spec 011 or a follow-up.
