# Cooperative Disputes — Phase 4

**Agent**: functional-typing

---

### Remaining Disputes

- **Dispute: Gate bypass mechanism**
  - **My claim**: Did not propose bypass. My review focused on structural correctness of the existing spec. Bypass was not raised in my original review or revision (no position taken).
  - **Opposing position(s)**: devils-advocate's revised Recommendation 4 proposes `--force-pass` with mandatory reason. integration-architect's revision did not address bypass.
  - **Why I will not concede**: I do not dispute bypass per se — I dispute its inclusion in spec 011. The spec explicitly states (L100): "Must NOT modify the engine." Bypass does not modify the engine, but it adds a feature that is outside the spec's stated scope. The spec defines gates as quality checks with deterministic verdict derivation. Bypass undermines the verdict's meaning by overriding it. If bypass is needed, it belongs in a follow-up spec that addresses CI/CD operational concerns holistically (timeout guidance, bypass, aggregate reporting).
  - **Counter-argument to their position**: devils-advocate's argument is that "critical hotfixes cannot be blocked by advisory quality gates." This is true, but the solution is `pass: always`, which already exists. `--force-pass` is `pass: always` with per-run scoping and audit trail — a refinement, not a fundamental capability. The refinement is valuable but not blocking for spec 011.
  - **Proposed resolution path**: Defer bypass to a follow-up spec (e.g., 011.1: Gate Operational Readiness). Note the deferral in spec 011's Constraints section: "Gate bypass is a recognized CI/CD need and will be addressed in a follow-up spec."

- **Dispute: Scope of gate config schema expansion**
  - **My claim**: Gate config should use the existing schema fields — expansion should be minimal and focused on validation (Recommendations 2, 4, 6 in my revision).
  - **Opposing position(s)**: integration-architect's Recommendation 2 (stagnation, iterations in gate config) expands the schema. devils-advocate's modified Recommendation 2 (warning threshold for agent count) adds behavior. Both expand the gate beyond its current schema.
  - **Why I will not concede**: Each new field in the gate config schema requires validation rules, error messages, defaults, and documentation. The spec should ship with the minimum viable schema and expand based on user feedback. Stagnation defaults to `detect` in the run engine (SKILL.md L229), so omitting it from the gate config is safe — the generated config inherits the run engine default. Iterations defaults to 1. These defaults are sensible for gates.
  - **Counter-argument to their position**: integration-architect argues that gates should "expose all run engine capabilities." But gates are a convenience layer, not a full-featured interface. Users who need stagnation control or multi-iteration depth can run `/conversus run` directly with a hand-crafted config. The gate handler is for common cases.
  - **Proposed resolution path**: Ship without stagnation and iterations in the gate config. Document that the generated config uses run engine defaults. If users request these fields, add them in a subsequent version. integration-architect's recommendation is valid but premature for the initial release.

### Convergence

- **Converged: Preset-to-multi-agent expansion gap**
  - **Shared position**: The spec example showing `preset: review/thorough` for gates is unimplementable with the current single-agent preset system. At minimum, fix the spec example. Optionally, define multi-agent presets as a new category.
  - **Agreeing agents**: functional-typing (Rec 1, surviving), integration-architect (Off-Base Assumptions), devils-advocate (Off-Base Assumptions)
  - **Strength**: Unanimous
  - **Path to convergence**: All three agents identified this independently in Phase 1. No disagreement at any stage.

- **Converged: max_disputes N validation as non-negative integer**
  - **Shared position**: N must be a non-negative integer (0 or greater). 0 is valid and equivalent to `converged`. Non-integer or negative values fail with a descriptive error.
  - **Agreeing agents**: functional-typing (Rec 2 modified), integration-architect (Rec 8 surviving)
  - **Strength**: Bilateral (functional-typing, integration-architect)
  - **Path to convergence**: functional-typing's original Rec 2 said "positive integer (1+)." integration-architect's Rec 8 and cross-review exposed the inconsistency. functional-typing conceded and modified to non-negative. Converged in Phase 3.

- **Converged: CLI flag override precedence**
  - **Shared position**: CLI flags override gate configuration values. This is standard CLI convention and required for CI/CD flexibility.
  - **Agreeing agents**: functional-typing (Rec 3 surviving), integration-architect (Rec 5 surviving)
  - **Strength**: Bilateral (functional-typing, integration-architect)
  - **Path to convergence**: Both identified this independently in Phase 1. No disagreement at any stage.

- **Converged: Engine independence correctly implemented**
  - **Shared position**: FR-012 is correctly implemented. Gates generate standard configs; the engine has zero gate awareness.
  - **Agreeing agents**: functional-typing, integration-architect, devils-advocate (all Alignment sections)
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1. Never contested.

- **Converged: Two-tier error handling for Dispute-Parsing failures**
  - **Shared position**: No synthesis = ERROR (exit 2). Synthesis exists but unparseable = BLOCK (exit 1) with a note. This distinguishes infrastructure failure from quality findings.
  - **Agreeing agents**: functional-typing (Rec 5 modified), integration-architect (Rec 1 modified), devils-advocate (cross-review proposal adopted by both)
  - **Strength**: Unanimous
  - **Path to convergence**: integration-architect originally proposed all failures = ERROR. devils-advocate proposed the two-tier approach in cross-review. Both functional-typing and integration-architect adopted it in Phase 3. Converged through deliberation.

- **Converged: Non-determinism guidance (not schema)**
  - **Shared position**: Add a note to the spec acknowledging non-determinism of LLM-based deliberation. Do not add a Confidence section to gate-result.md.
  - **Agreeing agents**: functional-typing (new Rec in revision), integration-architect (cross-review), devils-advocate (Rec 3 modified)
  - **Strength**: Unanimous
  - **Path to convergence**: devils-advocate originally proposed schema-level confidence. functional-typing and integration-architect pushed back in cross-review. devils-advocate modified to guidance-only in Phase 3. Converged through deliberation.

### Final Position Statement

**Non-Negotiables**:

1. Fix the spec example showing `preset: review/thorough` for gates, since it is unimplementable with the current preset system. This is blocking because the spec's own example fails. (Unanimous convergence.)

2. Specify max_disputes N as non-negative integer with explicit validation and error messages. Without this, implementations handle edge cases inconsistently. (Bilateral convergence with integration-architect.)

**Flexibility**:

1. Gate config schema scope (stagnation, iterations) — I am willing to accept inclusion if validation rules and error messages are fully specified. My concern is premature complexity, not the feature itself.

2. Bypass mechanism — I am willing to accept inclusion in spec 011 if it is clearly scoped (flag syntax, audit trail format, gate-result.md schema addition) and does not expand the spec's scope into other operational concerns.
