# Spec Compliance Cross-Review of Extraction Engineer
# Spec: 015-feature-extraction

**Cross-reviewer**: spec-compliance
**Reviewing**: extraction-engineer's review at `conversus-output/extraction-engineer/review.md`
**My review**: `conversus-output/spec-compliance/review.md`
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1: Position vector length normalization — implementation bug vs. spec gap

Extraction-engineer R-1 identifies that position vectors are not normalized to max recommendations across agents, citing the spec's "Vector length = max recommendations across agents" rule. My review does not flag this specific issue because I evaluated the extraction pipeline against FR requirements rather than Section 2's extraction rule details. The contradiction is in scope: extraction-engineer reads Section 2's extraction rules as normative requirements equal in weight to FRs; my review treats them as informational context.

**My position**: Extraction-engineer is correct. Section 2's extraction rules are the operational definition of what "correct extraction" means. If position vectors are not normalized to the same length across agents, the vectors are not comparable, which defeats the purpose of a feature vector. This is an FR-001 determinism issue: two pipelines that normalize differently produce different vectors.

### DC-2: Disposition regex permissiveness — correctness vs. resilience trade-off

Extraction-engineer M-2 recommends tightening the `_DISPOSITION_PATTERN` closing boundary from `\*?\*?` to `\*\*`. My review does not address regex correctness. The tension is between strict spec compliance (the template prescribes `**Disposition**:` with balanced stars) and operational resilience (LLM output is imperfect). FR-002 says extraction "MUST use structured parsing of conversus output format" -- the format is the template, which prescribes balanced stars. A strict reading of FR-002 supports tightening.

**My position**: FR-002 compliance argues for matching the prescribed format. However, FR-003 (graceful handling) argues for resilience. The correct middle ground is extraction-engineer's M-2 fix (tighten the regex) combined with schema-engineer's later suggestion of logging when the permissive path fires. But the permissive fallback should be a separate second-pass regex, not embedded in the primary pattern.

---

## Tensions

### T-1: `plugins/` directory exclusion urgency

Extraction-engineer R-6 recommends adding "plugins" to the exclusion list in PD/RB extraction. My review does not flag this because I evaluated against the current spec, which does not reference plugin output directories. However, spec 016 (Plugin System) will create `{output}/plugins/` directories. The extraction pipeline should be forward-compatible with spec 016's output structure.

**My position**: This is a valid P2 fix that should be included in the spec 015 implementation to avoid a cross-spec compatibility issue at deployment time.

### T-2: Write-time validation redundancy

Extraction-engineer R-7 recommends adding explicit write-time validation in `write_features()`. My review marks FR-013 as PARTIALLY MET for the same reason. We agree on the gap. The tension is whether this matters in practice: the normal pipeline path (`extract_features()` returns a constructed FeatureSet that has already been validated) does not benefit from re-validation. The edge case is manual construction for testing or debugging.

---

## Safe Agreements

- **SA-1: DISPUTES_BEGIN/END parsing is correct** — Extraction-engineer A-1 provides detailed evidence of pattern-to-template alignment. My review's FR-002 MET assessment is consistent.

- **SA-2: Severity vector encoding is correct** — Extraction-engineer A-5 confirms 4/3/2/1 encoding. My SC-003 MET assessment is consistent.

- **SA-3: Agent discovery exclusion list needs extension** — Both reviews agree the exclusion list should include `plugins/`.

- **SA-4: Red/blue role detection is fragile** — Extraction-engineer M-4 identifies content-based role detection as fragile. My review does not flag this but agrees the role should be an explicit input.

- **SA-5: Priority-absent defaults need spec documentation** — Extraction-engineer M-1 identifies undocumented defaults. My review's assessment that FR-007 (extensibility) is PARTIALLY MET is complementary: undocumented extraction rules make extension harder because new contributors do not know the implicit conventions.
