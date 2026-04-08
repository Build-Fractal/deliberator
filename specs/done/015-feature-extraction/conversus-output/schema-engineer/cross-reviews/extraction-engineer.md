# Schema Engineer Cross-Review of Extraction Engineer
# Spec: 015-feature-extraction

**Cross-reviewer**: schema-engineer
**Reviewing**: extraction-engineer's review at `conversus-output/extraction-engineer/review.md`
**My review**: `conversus-output/schema-engineer/review.md`
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1: Position vector normalization — extraction-level fix vs. schema-level contract

Extraction-engineer R-1 recommends normalizing position vector lengths to the max across agents, post-extraction. My review does not address vector length normalization because I treat the model's `list[int]` type as intentionally variable-length. The contradiction is in who owns the invariant: should the schema enforce equal-length vectors (via a model_validator on RoundFeatures that checks all agents' vectors have the same length), or should the extraction code pad after the fact?

**My position**: The schema should document but not enforce equal-length vectors. Enforcement at the schema layer creates a coupling between the schema and a cooperative-mode-specific invariant that does not apply to other modes (red-blue severity vectors have no fixed length). The extraction code should normalize, and the schema should note the convention in its docstring. Extraction-engineer R-1 is the correct fix location.

### DC-2: Model_copy vs. dump-reconstruct — agreed on the problem, different urgency

Extraction-engineer M-5 correctly identifies the `model_dump()` + re-construct pattern as fragile and recommends `model_copy(update=...)`. My review does not flag this because I reviewed `features.py` models, not `extraction.py` logic. No contradiction exists -- this is a gap in my review scope. I agree with the fix.

---

## Tensions

### T-1: `_DISPOSITION_PATTERN` closing boundary — correctness vs. resilience

Extraction-engineer M-2 recommends tightening the regex closing boundary from `\*?\*?` to `\*\*`. This is technically correct for well-formed output. However, the closing `\*?\*?` is intentionally permissive: LLM output occasionally produces `**Disposition*:` (one closing star instead of two) when the response is truncated or reformatted. The current pattern gracefully handles this. Tightening the boundary would cause silent extraction failures on slightly-malformed output that the current code handles.

**My position**: The current permissive pattern is the better default for a pipeline that processes LLM-generated markdown. If tightening is desired, it should be accompanied by a logging statement when the permissive path fires, so that malformed output is tracked without causing extraction failures.

### T-2: Red/blue role detection — content vs. config

Extraction-engineer M-4 recommends passing red/blue roles explicitly from config rather than inferring from content. This is architecturally correct but creates a coupling between the extraction pipeline and the config schema that does not currently exist. The extraction pipeline's API is `extract_features(output_dir, mode)` -- it does not accept a config object. Adding role information requires either extending the API signature or reading the config file from the output directory.

**My position**: The role should be stored in a `{agent}/meta.json` file by the engine at Phase 1, not inferred from content or passed through the extraction API. This keeps the extraction pipeline's input as filesystem artifacts only, consistent with its current design.

---

## Safe Agreements

- **SA-1: DISPUTES_BEGIN/END parsing is correct** — Extraction-engineer A-1 confirms the markers match the synthesis template. My review does not cover extraction logic but accepts this assessment.

- **SA-2: Convergence counting targets correct template output** — Extraction-engineer A-4 confirms the pattern matches the disputes template. Agreed.

- **SA-3: Agent discovery exclusion list needs extension** — Extraction-engineer O-2 identifies that PD/RB extraction iterates parent directories and may encounter `plugins/` directories. My review O-1 (territory_claim_vector) and O-2 (confirmed_count) surface a different set of gaps. Both reviews agree that the agent/non-agent directory boundary needs explicit enforcement beyond the current exclusion list.

- **SA-4: Position vector fallback defaults need spec documentation** — Extraction-engineer M-1 identifies that priority-absent defaults (Surviving=2, Modified=1) are not in the spec. My review does not address this but agrees it should be documented for determinism transparency.
