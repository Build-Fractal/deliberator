# Phase 2 Cross-Review: plugin-engineer reviews spec-compliance

**Spec**: 017-equilibrium-scorer
**Reviewer**: plugin-engineer
**Reviewing**: spec-compliance's Phase 1 review
**Date**: 2026-03-24

---

## Agreement

1. **FR-005 NOT MET**: Agree completely. The code structure suggests nashopt integration was intended but deferred. The import check and solver-field logic are scaffolding for future integration.

2. **FR-007 PARTIALLY MET**: Agree on the `hook` field issue. The fix is straightforward -- either pass the hook point to `execute()` (requires an ABC change) or accept that `execute_hooks()` provides the correct hook in the JSON output and document this as the intended behavior.

3. **FR-012, FR-013 MET**: spec-compliance correctly identifies the robust error handling. I verified both paths in my review.

4. **SC-004 NOT VERIFIED**: Agree. This is a packaging/distribution concern, not a code review finding. The code is structured correctly for extraction into a separate package.

## Points to Add

1. **FR-003 MET assessment needs nuance**: spec-compliance marks FR-003 as MET because `_try_extract_features()` calls `extract_features()`. However, from an engineering perspective, the feature extraction fallback chain is: (a) try full extraction from files, (b) fall back to state-based features. The spec says "using the `conversus-features` API (`extract_features()` or pre-computed `features.json`)." The implementation does attempt (a) but has no code path to read a pre-computed `features.json` file directly. It only reads via `extract_features()`. If someone pre-computes `features.json` manually, the scorer won't pick it up unless `extract_features()` reads that file. This is a minor gap.

2. **Constraints compliance table is valuable**: spec-compliance's constraint check is the only review that explicitly verifies the Section 5 constraints. All four constraints are MET, which I confirm.

## Disagreement

**FR-008**: I agree with spec-compliance that this is PARTIALLY MET, contrary to game-theorist's likely position that it's fully MET. The spec uses "MUST" language with a specific filename pattern. While the base infrastructure's pattern is arguably better, the spec is normative and the implementation deviates from the stated format. If the spec intended the base pattern, it would not have specified a concrete filename.
