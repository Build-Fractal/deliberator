# Extraction Engineer Revision: 015 Feature Extraction Pipeline

**Reviewer**: extraction-engineer
**Revision iteration**: 1
**Date**: 2026-03-24

---

## Recommendation Dispositions

#### Recommendation 1: Normalize position vector lengths to max recommendations across agents

- **Original position**: Compute `max_recs` across agents and re-pad all vectors.
- **Disposition**: Surviving
- **Explanation**: Spec-compliance DC-1 explicitly endorses this as a correctness issue, noting that unnormalized vectors are not comparable and defeat the purpose of feature vectors. Schema-engineer DC-1 agrees this is the correct fix location (extraction code, not schema). No cross-review challenges this recommendation.

#### Recommendation 2: Fix the `_DISPOSITION_PATTERN` closing boundary

- **Original position**: Change `\*?\*?` to `\*\*` to require balanced bold markers.
- **Disposition**: Modified
- **Explanation**: Schema-engineer T-1 correctly argues that the permissive boundary handles truncated LLM output gracefully. Spec-compliance DC-2 proposes a middle ground: tighten the primary regex but keep the permissive pattern as a separate fallback with logging. Modified recommendation: make `\*\*` the primary pattern and add a second-pass permissive fallback with `logger.warning()` when it fires. This satisfies FR-002's strict format requirement while preserving FR-003's resilience guarantee.

#### Recommendation 3: Tighten `_SAFE_AGREEMENT` to match top-level agreement items only

- **Original position**: Require items at zero or two spaces of indentation.
- **Disposition**: Surviving
- **Explanation**: Schema-engineer T-2 agrees this is complementary to their AgreementMatrix typing recommendation. No cross-review challenges the parsing fix itself. The regex should match only top-level list items (indentation <= 2 spaces) within the Safe Agreements section.

#### Recommendation 4: Pass red/blue role explicitly from config

- **Original position**: Add a `roles: dict[str, str]` parameter to `_extract_rb_features()`.
- **Disposition**: Modified
- **Explanation**: Schema-engineer T-2 proposes an alternative: store the role in a `{agent}/meta.json` file written by the engine at Phase 1. This is architecturally cleaner because it keeps the extraction pipeline's input as filesystem artifacts only, consistent with its design (no config dependency). Modified recommendation: the engine should write `{agent}/meta.json` with at minimum `{"role": "red"|"blue"}` for red-blue mode, and the extraction pipeline should read this file when available, falling back to content detection when it is absent. This preserves backward compatibility with existing output directories.

#### Recommendation 5: Use model_copy instead of dump-reconstruct for round number override

- **Original position**: Replace the model_dump() pattern with model_copy(update=...).
- **Disposition**: Surviving
- **Explanation**: Schema-engineer DC-2 explicitly agrees. No cross-review challenges this.

#### Recommendation 6: Exclude `plugins/` from non-agent directory iteration

- **Original position**: Add "plugins" to the exclusion list in PD/RB extraction.
- **Disposition**: Surviving
- **Explanation**: Spec-compliance T-1 endorses this as forward-compatible with spec 016. No cross-review challenges the fix.

#### Recommendation 7: Add explicit write-time validation to `write_features()`

- **Original position**: Call model_validate before serialization.
- **Disposition**: Surviving
- **Explanation**: Spec-compliance T-2 agrees on the gap, noting it matters for manual construction paths. Schema-engineer does not address this but the fix is non-controversial.

#### Recommendation 8: Document priority-absent position vector defaults in the spec

- **Original position**: Add explicit extraction rules for when Priority labels are missing.
- **Disposition**: Surviving
- **Explanation**: Schema-engineer SA-4 agrees. Spec-compliance SA-5 notes this gap makes extension harder. The spec should document: "When a recommendation section does not include a Priority label, Surviving defaults to position value 2, Modified defaults to 1."

---

## New Recommendations

- **Add meta.json writing to engine for red-blue roles** (Priority: P2)
  - Triggered by: Schema-engineer T-2 proposing `{agent}/meta.json` as the role storage mechanism.
  - Proposed change: The engine should write a `meta.json` file in each agent's output directory containing at minimum `{"role": "red"|"blue"}` for red-blue mode. This is a cross-spec change (engine, not extraction), so it should be coordinated with the engine team.
  - Rationale: Keeps extraction pipeline input as filesystem artifacts; no config dependency.

---

## Position Summary

Withdrew 0, modified 2, maintained 6. Added 1 new recommendation.

The most significant change is R-4 (role detection), which shifted from a config-parameter approach to a meta.json filesystem approach based on schema-engineer's feedback. This preserves the extraction pipeline's design principle of reading only filesystem artifacts. The second modification (R-2, disposition regex) is a tightening-with-fallback compromise that satisfies both strict FR-002 compliance and FR-003 resilience.

My highest-priority surviving recommendation is R-1 (position vector normalization). Without it, cooperative feature vectors are not comparable across agents, which undermines the fundamental purpose of the extraction pipeline as a bridge to game theory analysis.
