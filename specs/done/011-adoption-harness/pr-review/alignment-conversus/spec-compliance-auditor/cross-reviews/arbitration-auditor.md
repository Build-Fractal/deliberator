# Cross-Review: Spec Compliance Auditor reviewing Arbitration Auditor

**Reviewer perspective**: spec-compliance-auditor
**Reviewed**: arbitration-auditor
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1. Output directory naming: "matches spec 006" vs SKILL.md divergence

The arbitration-auditor states "Output directory layout matches spec 006 US-4" and considers output paths correct. The spec-compliance-auditor found that the engine uses `arbiter/` while SKILL.md consistently uses `arbitration/`. The arbitration-auditor checked against spec 006 user stories; the spec-compliance-auditor checked against SKILL.md text. If SKILL.md is the authoritative source (as the spec-compliance-auditor's methodology assumes), the arbitration-auditor's "matches" claim is incorrect. This is not a minor naming preference -- any code that constructs paths from SKILL.md conventions will fail to find engine-produced files.

### DC-2. Inter-round arbitration priority level

The arbitration-auditor rates implementing inter-round arbitration in `run_pipeline()` as P1 (R2, "must-fix: blocks spec 006 correctness"). The spec-compliance-auditor rates it as P2 (R06, "Functional Gaps -- Not Crashes, But Missing Behavior"). The spec-compliance-auditor's rationale: inter-round arbitration is a feature addition, not a fix for existing broken behavior. No user currently configures `timing: inter-round` because the field does not exist in `ArbiterConfig`. The arbitration-auditor's rationale: spec 006 defines inter-round arbitration as a core requirement, and the engine claims to support the deliberation pipeline. The disagreement is about whether "not yet implemented" is P1 or P2.

### DC-3. Scope of template variable gaps identified

The arbitration-auditor identifies 8 specific things the engine gets wrong (section "What the engine gets wrong", items 1-8). The spec-compliance-auditor identifies 5 P1 items. Several of the arbitration-auditor's findings (cross-round synthesis missing arbitration context, stagnation detection not influence-aware) do not appear in the spec-compliance-auditor's P1 list at all. The spec-compliance-auditor groups these under P2 (R06, R07), while the arbitration-auditor's framing suggests they are all part of the same P1 urgency. The question: does grouping influence-aware dispute counting under P2 understate its importance?

---

## Tensions

### T-1. Depth vs breadth on spec 006

The arbitration-auditor's review is an exhaustive spec-006 compliance audit: every FR is checked, every template variable traced, every influence level analyzed. The spec-compliance-auditor's review covers spec 006 as one of several concerns (alongside specs 007-013). The arbitration-auditor finds issues the spec-compliance-auditor does not (e.g., `PipelineResult.arbitration_ran` type, cross-round synthesis missing arbitration context). The spec-compliance-auditor finds issues the arbitration-auditor does not (e.g., `arbiter/` vs `arbitration/` directory, `PRIOR_ROUND_SECTION`). Depth vs breadth tradeoff is expected, but the findings are complementary.

### T-2. `PipelineResult.arbitration_ran` type adequacy

The arbitration-auditor recommends changing this from `bool` to a richer type (R7, P2). The spec-compliance-auditor does not mention `PipelineResult` fields. The arbitration-auditor's reasoning is sound for inter-round arbitration tracking, but the spec-compliance-auditor's silence may reflect that this is an internal API concern that does not affect SKILL.md-specified behavior.

### T-3. `_resolve_arbiter` validation completeness

The arbitration-auditor specifically calls out that `_resolve_arbiter` does not parse `timing` or `influence` (What the engine gets wrong, item 2) and that no FR-003 validation exists (item 3). The spec-compliance-auditor bundles all of this under R01: "Add `timing` and `influence` fields to `ArbiterConfig`." The arbitration-auditor's granularity is more actionable -- it identifies the exact function (`_resolve_arbiter`) and the exact validation rule (FR-003: inter-round requires rounds > 1) that need changes.

### T-4. Warning on unknown fields as interim measure

The spec-compliance-auditor recommends a P2 warning when `timing`/`influence` appear but are not implemented (R08). The arbitration-auditor recommends a P3 warning (R10). Both agree a warning is needed as an interim measure, but disagree on priority. The spec-compliance-auditor sees it as should-have (P2); the arbitration-auditor sees it as nice-to-have (P3) since R1 (implementing the fields) is the real fix.

---

## Safe Agreements

### SA-1. `timing` and `influence` must be added to `ArbiterConfig`

Both auditors agree this is the single most important fix, rated P1 by both. Identical recommendation, identical code location.

### SA-2. `INFLUENCE_LEVEL` must be explicitly passed from config

Both auditors agree the engine's reliance on Pydantic default is insufficient. Both cite `build_arbitration_context()` as the fix point.

### SA-3. `PRIOR_ARBITRATION_SECTION` must be populated

Both auditors flag this gap (arbitration-auditor R4 at P1, spec-compliance-auditor R04 at P1). Both agree the engine threads `PRIOR_ARBITRATION_PATH` but never constructs the influence-aware block that `PRIOR_ARBITRATION_SECTION` should contain.

### SA-4. Engine's core Phase 6 trigger logic is correct

Both auditors confirm the trigger evaluation (`disputes_remain` vs `always`), the two-tier dispute extraction, and failure isolation are correctly implemented. The gaps are in the *new* spec-006 additions, not the existing Phase 6 infrastructure.
