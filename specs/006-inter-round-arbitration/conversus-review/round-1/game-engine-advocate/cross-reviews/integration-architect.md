# Cross-Review: game-engine-advocate reviewing integration-architect

## Dangerous Contradictions

None identified. The integration-architect's recommendations focus on wiring completeness and template-level correctness, which are orthogonal to game engine extensibility concerns. No recommendation would block plugin integration.

## Tensions

### T1: Dead Infrastructure Priority vs. Game Engine Readiness

**integration-architect** identifies `{ARBITRATION_PATHS}` and `{ARBITRATION_RULINGS}` as dead infrastructure -- variables defined end-to-end in schema, model, and SKILL.md but never referenced in the cross-round synthesis template. Both are ranked P1.

**game-engine-advocate** did not identify this gap. This is a significant miss on the game-engine-advocate's part. Dead infrastructure is particularly problematic for the game engine vision because: (1) plugin developers reading the schema would expect these variables to work, and (2) the Resolution Attribution section in the cross-round synthesis template is exactly where the game engine's equilibrium scorer would inject its analysis. If the template does not even reference the arbitration data, the game engine's output would also lack an integration point.

No tension in terms of disagreement -- game-engine-advocate fully endorses the integration-architect's P1 ranking. The tension is that game-engine-advocate should have caught this and did not, suggesting the game engine review was too focused on structural compatibility and insufficiently focused on template-level completeness.

### T2: Structural Markers for Provisionally Resolved Disputes

**integration-architect** identifies the lack of structural markers for "Provisionally Resolved" disputes as a medium-impact gap. The dispute-parsing subsystem uses `DISPUTES_BEGIN`/`DISPUTES_END` markers but has no mechanism to distinguish provisionally-resolved disputes from remaining disputes.

**game-engine-advocate** notes this is relevant to the game engine because: the convergence predictor needs accurate dispute counts to predict convergence. If provisionally-resolved disputes are counted as remaining, the convergence prediction will be pessimistic (predicting more rounds needed). If they are excluded, the prediction is accurate. The structural marker gap means the convergence predictor would need to parse agent prose to determine dispute status, violating the "templating over inference" principle.

This is an alignment, not a tension -- both perspectives agree the gap matters, but for different reasons (integration-architect: orchestrator correctness; game-engine-advocate: plugin data quality).

### T3: influence_headings Schema Location

**integration-architect** proposes (Rec 1) adding `influence_headings` directly to the mode schema (`cooperative.yml`). This is a per-mode configuration.

**game-engine-advocate** proposed (R5) a dedicated `schema/influence-levels.yml` that maps each influence level to its behavioral parameters across all modes. The per-mode approach (integration-architect) is simpler and sufficient for cooperative mode. The cross-mode approach (game-engine-advocate) anticipates that influence levels have mode-independent semantics (e.g., `binding` always means "settled") with mode-specific manifestations (headings differ by mode).

For spec 006, the per-mode approach is correct since only cooperative mode has arbitration. The cross-mode approach is YAGNI until another mode adds arbitration. The tension resolves in favor of integration-architect's simpler proposal for now.

## Safe Agreements

### SA1: Influence-Aware Heading Validation Is the Top P1
Both agents rank this as the highest-priority gap. integration-architect's structured YAML proposal (Rec 1) and game-engine-advocate's R2 Option A are functionally equivalent.

### SA2: SKILL.md Runtime Validation Is the Correct Architecture
integration-architect's Off-Base Assumption correctly identifies that influence-adjusted heading validation belongs at the orchestrator level (runtime), not the schema level (static). game-engine-advocate's R2 Option B (skip linter validation for dynamic headings) reaches the same conclusion from a different direction. Both agree the linter cannot statically validate influence-dependent headings.

### SA3: Schema Variables Are Well-Provisioned
Both agents validate the schema variable definitions. integration-architect confirms all 23 FRs have implementation artifacts; game-engine-advocate confirms the `config_conditions` model supports future plugin conditions.

### SA4: Cross-Round Synthesis Is the Integration-Critical Template
Both agents focus significant attention on `cross-round-synthesis.md` as the template most affected by spec 006. integration-architect identifies dead variable references; game-engine-advocate identifies it as the natural predecessor to game engine post-deliberation hooks.

### SA5: Path Computation Should Be Explicit
integration-architect's Rec 6 (explicit PRIOR_ARBITRATION_PATH formula) aligns with game-engine-advocate's emphasis on deterministic execution. Plugin developers would need the same path computation clarity to know where to read arbitration artifacts.
