# Cooperative Disputes — Phase 4

**Agent**: devils-advocate

---

### Remaining Disputes

- **Dispute: Gate bypass must be in spec 011**
  - **My claim**: `--force-pass --force-pass-reason "reason"` is essential for real-world CI/CD adoption (Rec 4, surviving in revision). It is a gate feature, not an operational concern, because it affects gate-result.md output.
  - **Opposing position(s)**: functional-typing proposes deferring bypass to a follow-up spec (disputes section). Their argument: `pass: always` already exists, bypass is a refinement.
  - **Why I will not concede**: `pass: always` requires changing the gate configuration file. In a real CI/CD pipeline, the engineer pushing a hotfix does not have time to (a) edit gates.yml, (b) commit the change, (c) run the pipeline. They need a command-line override that works immediately. This is the same reason `git push --no-verify` exists — not because it is ideal, but because the alternative (editing .git/hooks) is impractical in emergencies. `--force-pass` is the `--no-verify` of conversus gates.
  - **Counter-argument to their position**: functional-typing argues bypass "undermines the verdict's meaning." But the verdict is still recorded (BLOCK → bypassed PASS). The audit trail (mandatory reason) makes the override visible to reviewers. A bypassed gate in the audit trail is more accountable than a gate stage that was silently removed from the pipeline. Additionally, integration-architect now supports bypass inclusion in spec 011 (their disputes section).
  - **Proposed resolution path**: Include in spec 011 with minimal scope: flag syntax, gate-result.md additions (Bypass: true, Bypass Reason), exit code 0. No other operational concerns. The synthesizer should note that this has bilateral support (devils-advocate + integration-architect) vs. one agent proposing deferral (functional-typing).

- **Dispute: Execution metadata in gate-result.md**
  - **My claim**: gate-result.md should include a `## Execution` section with agent count, rounds executed, and termination reason (Rec 8, surviving in revision).
  - **Opposing position(s)**: No agent explicitly opposed this, but functional-typing and integration-architect did not adopt it either. The lack of adoption may indicate it is seen as out of scope.
  - **Why I will not concede**: Execution metadata is diagnostic information that CI/CD operators use to tune gate configurations. Without it, operators must inspect the full conversus output to understand gate performance. The information is available after execution (agent count is tracked, rounds are tracked, termination reason is computed). Adding a section to gate-result.md is low-cost and high-value.
  - **Counter-argument to their position**: No explicit opposition exists. The concern may be schema expansion, but gate-result.md is a new schema defined by this spec — now is the time to get it right, not after shipping.
  - **Proposed resolution path**: Include in the gate-result.md schema. If the synthesizer finds this is uncontested, it should be accepted as a straightforward improvement.

### Convergence

- **Converged: Preset-to-multi-agent gap**
  - **Shared position**: Fix the spec example. Current presets are single-agent and gates need at least 2.
  - **Agreeing agents**: All three.
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1.

- **Converged: Engine independence**
  - **Shared position**: FR-012 correctly implemented.
  - **Agreeing agents**: All three.
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1.

- **Converged: Two-tier error handling**
  - **Shared position**: No synthesis = ERROR. Synthesis exists but unparseable = BLOCK with note.
  - **Agreeing agents**: All three.
  - **Strength**: Unanimous
  - **Path to convergence**: I proposed this in cross-review. Both other agents adopted in Phase 3.

- **Converged: Non-determinism guidance**
  - **Shared position**: Guidance note in spec, not schema addition.
  - **Agreeing agents**: All three.
  - **Strength**: Unanimous
  - **Path to convergence**: My original Rec 3 proposed schema-level confidence. Cross-reviews pushed back. I modified to guidance-only in Phase 3.

- **Converged: CLI flag override precedence**
  - **Shared position**: Flags override config values.
  - **Agreeing agents**: functional-typing, integration-architect.
  - **Strength**: Bilateral
  - **Path to convergence**: I did not directly address this but do not dispute it. Directionally aligned.

- **Converged: max_disputes N validation**
  - **Shared position**: Non-negative integer, 0 valid.
  - **Agreeing agents**: functional-typing, integration-architect.
  - **Strength**: Bilateral
  - **Path to convergence**: Converged in Phase 3.

### Final Position Statement

**Non-Negotiables**:

1. Gate bypass (`--force-pass` with mandatory reason) must be included in spec 011. Without it, teams will bypass gates by removing them from pipelines entirely, which provides zero accountability. The flag is low-scope (syntax + gate-result.md additions) and has bilateral support (devils-advocate + integration-architect).

2. Non-determinism must be acknowledged in spec guidance. Gate verdicts are quality signals, not deterministic tests. Without this acknowledgment, teams will calibrate pipelines incorrectly. (Unanimous convergence — already resolved.)

**Flexibility**:

1. Execution metadata in gate-result.md — I am willing to accept this as P3 if the synthesizer determines it is uncontested but low-priority. The information is useful but not blocking.

2. Timeout and resource limits — I conceded these as guidance rather than gate features (Recs 1, 2 modified in revision). I am satisfied with the guidance approach.

3. Artifact content validation (empty check) — I am willing to accept this as P3. The empty check is fast-fail and useful but not critical.
