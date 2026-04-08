# Cross-Review: Guided Workflow Auditor reviewing Spec Compliance Auditor

**Reviewer perspective**: guided-workflow-auditor
**Reviewed**: spec-compliance-auditor
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1. `arbiter/` vs `arbitration/` directory name -- runtime failure claim

The spec-compliance-auditor flags the `arbiter/` vs `arbitration/` directory naming as P1 (R03), claiming it "would cause any SKILL.md-based workflow (including `/conversus arbitrate`) to look in the wrong directory." The guided-workflow-auditor does not flag this as an issue. The contradiction: the guided-workflow-auditor documents that the SKILL.md `arbitrate` handler runs Phase 6 inline -- it does not consume engine output at all. The handler writes its own output to whatever path SKILL.md specifies. The path mismatch only matters if the guided handlers read engine-produced output, which they do not (they produce their own via Agent tool calls). The spec-compliance-auditor's P1 rating assumes the engine and guided workflow share output paths, which the guided-workflow-auditor explicitly says they do not.

### DC-2. `PRIOR_ROUND_SECTION` gap -- flagged vs not flagged

The spec-compliance-auditor identifies `PRIOR_ROUND_SECTION` always being empty string as a P1 issue (R05). The guided-workflow-auditor does not mention `PRIOR_ROUND_SECTION` at all. This is a genuine oversight in the guided-workflow review if the SKILL.md handlers rely on engine-produced context for round 2+ reviews. However, given the dual-execution-path finding (SKILL.md handlers orchestrate their own phases), the guided-workflow perspective is that SKILL.md handlers compose this block themselves per the SKILL.md instructions, making the engine's empty `PRIOR_ROUND_SECTION` irrelevant to guided-workflow execution.

### DC-3. "Runtime failure" severity classification

The spec-compliance-auditor classifies 5 items as P1 ("Runtime Failure or Silent Incorrectness"). The guided-workflow-auditor classifies only 3 items as P1 ("Critical -- blocks correct guided workflow execution"). The guided-workflow-auditor's R1-R3 overlap with the spec-compliance-auditor's R01, R02, R06, but the spec-compliance-auditor adds R03 (directory name), R04 (PRIOR_ARBITRATION_SECTION), and R05 (PRIOR_ROUND_SECTION) as additional P1s. The guided-workflow perspective is that items only used by the engine's internal pipeline are P2/P3, not P1, because the guided handlers bypass the engine.

---

## Tensions

### T-1. Engine as sole execution path vs parallel implementation

The spec-compliance-auditor reviews the engine as if it is the authoritative execution path: "the engine is a faithful extraction of SKILL.md." The guided-workflow-auditor explicitly identifies the dual-execution-path architecture: the engine and SKILL.md handlers are parallel implementations. This framing difference affects every priority assessment. The spec-compliance-auditor rates engine gaps as runtime failures; the guided-workflow-auditor rates them as delegation-seam gaps.

### T-2. Influence-aware dispute counting priority

The spec-compliance-auditor rates influence-aware dispute counting as P2 (R07). The guided-workflow-auditor also rates inter-round arbitration as P1 (R2) but does not separately call out influence-aware dispute counting. The tension: the spec-compliance-auditor separates the inter-round insertion point from the influence-aware termination adjustment, while the guided-workflow-auditor bundles them as a single concern.

### T-3. Warning on unknown config fields

The spec-compliance-auditor recommends adding a warning when `timing`/`influence` appear in config but are not implemented (R08, P2). The guided-workflow-auditor does not recommend this interim measure -- they go straight to "add the fields" (R1). The tension is about the implementation sequence: warn-then-implement vs implement-directly. The guided-workflow perspective favors directness since the fields have clear defaults and the implementation is additive.

### T-4. Documentation of guided workflow architecture

The spec-compliance-auditor recommends documenting that guided workflow subcommands are SKILL.md-native (R09, P3). The guided-workflow-auditor recommends documenting the dual-execution-path architecture (R9, P3). These are complementary but different: one documents what the engine does NOT do, the other documents that there are TWO execution paths for the same pipeline.

---

## Safe Agreements

### SA-1. `timing`/`influence` fields are the top-priority gap

Both auditors agree these fields must be added to `ArbiterConfig`. Both cite the same code location and the same SKILL.md references.

### SA-2. `INFLUENCE_LEVEL` must be explicitly passed in `build_arbitration_context`

Both auditors agree the Pydantic default of `binding` is insufficient -- the engine must read from config. Both cite `templates.py:build_arbitration_context()` as the fix location.

### SA-3. Inter-round arbitration is missing from `run_pipeline()`

Both auditors agree the engine's round loop only runs Phase 6 after the final round, and that `timing: inter-round` requires Phase 6 inside the loop. The implementation details differ (see T-2) but the finding is shared.

### SA-4. Engine correctly handles config parsing for current fields

Both auditors agree the engine's `parse_config()` is a high-fidelity extraction for the fields it knows about (mode, target, agents, presets, trigger). The gaps are in the fields it does not know about.
