# Extraction Engineer Cross-Review of Spec Compliance
# Spec: 015-feature-extraction

**Cross-reviewer**: extraction-engineer
**Reviewing**: spec-compliance's review at `conversus-output/spec-compliance/review.md`
**My review**: `conversus-output/extraction-engineer/review.md`
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1: FR-005 per-mode YAML schema files — strict spec reading vs. implementation adequacy

Spec-compliance marks FR-005 as NOT MET because no `schema/features/{mode}.yml` files exist. This is a correct reading of the literal spec text. However, the Pydantic models in `features.py` serve the same validation purpose: they define feature names, types, and defaults. The spec says YAML schemas should include "extraction source (phase, file pattern), and extraction rule (parsing logic reference)" -- this metadata is not in the Pydantic models but is documented in the extraction code's comments and the spec's Section 2 table. Creating YAML files that duplicate the Pydantic model definitions would create a maintenance burden with no clear consumer.

**My position**: FR-005 should be amended to accept Pydantic models as the normative schema definition, with the extraction source/rule metadata documented in the spec's Section 2 table (which already exists). Creating parallel YAML schemas is make-work that creates drift risk.

### DC-2: FR-014/FR-016 package naming — standalone vs. embedded

Spec-compliance marks FR-014 as NOT MET and FR-016 as PARTIALLY MET because the extraction pipeline ships within `conversus.schemas` rather than as a standalone `conversus-features` package. This is correct against the spec text. My review does not address packaging at all.

**My position**: Spec-compliance's recommendation 3 (option a: amend the spec to match the actual namespace) is the correct resolution. The extraction pipeline shares types with `game_forms.py` and `objectives.py` through `features.py`. Splitting it into a separate package would require either duplicating shared types or creating a third `conversus-schemas` base package. The current embedded structure is architecturally cleaner.

---

## Tensions

### T-1: CLI entry point priority

Spec-compliance marks FR-012 as NOT MET and gives the CLI implementation P1 priority. The extraction pipeline is currently consumed only through its Python API (`extract_features()`), and the upcoming plugins (specs 017-019) will also use the Python API. A CLI is useful for manual debugging but is not on the critical path for the plugin pipeline.

**My position**: The CLI should be P2, not P1. The Python API (FR-011) is the primary interface. The CLI is a convenience that can be added without changing any existing code.

### T-2: Pre-write validation strictness

Spec-compliance marks FR-013 as PARTIALLY MET because `write_features()` does not re-validate. My review R-7 also recommends adding write-time validation. We agree on the gap. The tension is in what validation means: Pydantic validates on construction, so a FeatureSet that reaches `write_features()` through the normal `extract_features()` pipeline has already been validated. The gap only matters for manually-constructed FeatureSets, which is a testing/debugging path, not the production path.

---

## Safe Agreements

- **SA-1: FR-001 (determinism) is fully MET** — Both reviews independently confirm deterministic extraction with the same evidence (no randomness, sorted iteration, sort_keys=True output).

- **SA-2: FR-002 (structural parsing) is fully MET** — Both reviews confirm regex-based structural parsing with no LLM calls.

- **SA-3: FR-003 (graceful degradation) is fully MET** — Both reviews confirm zero-default behavior for missing files.

- **SA-4: FR-015 (minimal dependencies) is MET** — Both reviews confirm stdlib + pydantic only imports.

- **SA-5: SC-001 through SC-004 are all MET** — Both reviews agree on test evidence for all four.

- **SA-6: territory_claim_vector and confirmed_count are unpopulated** — Spec-compliance R-4 and R-5 flag these gaps. My review M-6 overlaps on the vector-length normalization issue. The extraction logic for these fields needs to be implemented.
