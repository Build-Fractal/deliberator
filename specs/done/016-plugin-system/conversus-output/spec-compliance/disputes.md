# Spec Compliance Disputes — 016 Plugin System Infrastructure

**Role**: spec-compliance
**Phase**: 4 — Disputes
**Date**: 2026-03-24

---

## Remaining Disputes

- **Dispute: FeatureSet field on DeliberationState — in spec 016 vs. in spec 017**
  - **My claim**: The features field should NOT be added in spec 016. Spec 016 declares "Depends On: None." Adding a features pathway, even as `dict[str, Any]`, introduces a conceptual dependency on spec 015's output. The field should be added by spec 017 (equilibrium scorer) which explicitly depends on spec 015. Cite: spec-compliance DC-1 in cross-review of plugin-architect.
  - **Opposing position(s)**: Plugin-architect disputes the features field, arguing that without it, every numerical plugin must independently discover and parse feature files. They propose `features: dict[str, Any] | None = None` as a dependency-free compromise.
  - **Why I will not concede**: The "Depends On: None" declaration is a deliberate architectural choice. Spec 016 is the framework foundation. If we add features here, the next request will be to add synthesis text, then agent recommendations, then dispute results. The framework should provide the hook mechanism and state interface; what data goes into the state is the responsibility of specs that produce and consume that data. The features field is a data concern, not a framework concern.
  - **Counter-argument to their position**: Plugin-architect argues plugins should "receive data from the orchestrator, not scavenge it from the filesystem." But `output_dir` is already on DeliberationState. Plugins can read feature files from `output_dir / "features.json"`. The filesystem is not scavenging when the output directory is part of the state.
  - **Proposed resolution path**: Defer the features field to spec 017 or a new bridging spec. Spec 016 provides `output_dir` on the state; plugins that need features can read them from there. If this proves insufficient, spec 017's review will surface it. The synthesizer should decide.

- **Dispute: FR-001 assessment — PARTIALLY MET vs. MET at parsing layer**
  - **My claim**: FR-001 is PARTIALLY MET because the engine's EngineConfig does not include a `plugins` field. The config format support exists in `config.py` but is not consumed. Cite: spec-compliance review FR-001.
  - **Opposing position(s)**: Schema-engineer DC-1 argues FR-001 is MET at the config-parsing layer, and engine integration is a separate requirement (FR-003/FR-006).
  - **Why I will not concede**: FR-001 says "A `plugins` field in `conversus.yml` MUST allow declaring plugins." The word "allow" implies the config is actionable, not just parseable. A field that is parsed but ignored does not "allow declaring plugins" -- it allows writing YAML that is silently discarded. The distinction matters for implementors: they should know that writing `plugins:` in their config currently does nothing.
  - **Counter-argument to their position**: Schema-engineer separates parsing from consumption. But the spec does not make this separation. FR-001, FR-003, and FR-006 together define the pipeline: config -> load -> execute. If any link is broken, the chain is broken. FR-001 without FR-003 is a broken chain.
  - **Proposed resolution path**: Mark FR-001 as PARTIALLY MET with a note that engine integration (R-1) is required to complete it. The synthesizer should reflect this in the final compliance table.

---

## Convergence

- **Converged: Engine integration is the critical deliverable**
  - **Shared position**: Wire execute_hooks() into the engine pipeline at all four hook points.
  - **Agreeing agents**: All three reviewers.
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1.

- **Converged: Amend FR-012 package naming**
  - **Shared position**: Use `conversus.plugins`, not `conversus-plugins`.
  - **Agreeing agents**: All three reviewers.
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1.

- **Converged: Remove config param from execute()**
  - **Shared position**: Simplified `execute(self, state)` signature.
  - **Agreeing agents**: All three reviewers.
  - **Strength**: Unanimous
  - **Path to convergence**: Emerged Phase 2-3.

- **Converged: Remove AgentState.positions**
  - **Shared position**: Dead field, remove it.
  - **Agreeing agents**: All three reviewers.
  - **Strength**: Unanimous
  - **Path to convergence**: Schema-engineer Phase 1, all agreed Phase 3.

---

## Final Position Statement

**Non-Negotiables**:
- Engine integration must be a spec 016 deliverable. FR-006 says "MUST call execute()." The orchestrator does not call it. This is a NOT MET MUST requirement that blocks "done" status.
- Spec amendments (FR-012 package naming) must be explicit. No implicit drift.

**Flexibility**:
- PluginFacingConfig vs. dict config. I lean toward dict (simpler, less coupling) but will accept the typed model if it uses `extra="allow"`.
- Features field timing. I prefer deferral to spec 017, but will accept the untyped `dict[str, Any]` field if the synthesizer determines it is framework infrastructure.
