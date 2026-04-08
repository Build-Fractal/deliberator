# Phase 3 Revision: plugin-engineer

**Spec**: 017-equilibrium-scorer
**Reviewer**: plugin-engineer
**Date**: 2026-03-24
**Phase**: 3 (Revised Review After Cross-Review)

---

## Revisions Based on Cross-Review Feedback

### From game-theorist

1. **Thread safety qualification**: game-theorist points out that `_try_extract_features()` performs file I/O, so my "safe for concurrent use" claim needs qualification. I accept this. **Updated assessment**: Thread-safe for the scorer logic itself, but the feature extraction fallback performs file reads. Since `execute_hooks()` runs sequentially, this is not a practical concern, but I revise my claim to "safe for sequential hook execution."

2. **FR-008 is MET (game-theorist's position)**: game-theorist argues the filename requirement's intent (include round number) is met. I originally sided with spec-compliance (PARTIALLY MET). After reconsideration, I maintain my position: the spec's MUST language with a specific format is normative. However, I acknowledge this is a disagreement about spec interpretation, not a code defect.

### From spec-compliance

1. **FR-003 nuance -- pre-computed features.json**: spec-compliance via its cross-review noted that `_try_extract_features()` calls `extract_features()` but does not directly read a pre-computed `features.json`. This is a valid observation. The spec says "using the `conversus-features` API (`extract_features()` or pre-computed `features.json`)." If `extract_features()` internally reads `features.json`, this is satisfied transitively. If not, direct `features.json` reading is missing. **Updated assessment**: Depends on `extract_features()` implementation. Mark as needs-verification.

2. **Undocumented `gamma` config**: spec-compliance notes that `gamma` is not in FR-010's config list but exists in the code. This is a config surface area issue. The plugin accepts parameters the spec does not define. Not harmful, but not spec-sanctioned either. **Updated assessment**: Note as an extension beyond spec requirements.

---

## Updated Key Issues

1. **`hook` field in PluginResult.data (medium)**: Still the top engineering issue. The in-memory result has a wrong hook value. Fix options: (a) pass hook to execute(), (b) accept JSON output as source of truth and document this.

2. **Filename format deviation (low)**: Base infrastructure pattern vs. spec-specified pattern. This is a cross-cutting concern affecting all plugins, not scorer-specific.

3. **Thread safety (low)**: Revised to "safe for sequential execution; file I/O in fallback path is not thread-safe."

4. **Undocumented gamma config (low, new)**: Config parameter exists without spec coverage.

---

## Unchanged Assessments

- Full ABC conformance.
- Hook execution works correctly for both POST_PHASE_5 and POST_DELIBERATION.
- Error handling is thorough (FR-012, FR-013).
- advisory=True is correctly set in all paths.
- Output namespace isolation is clean.
