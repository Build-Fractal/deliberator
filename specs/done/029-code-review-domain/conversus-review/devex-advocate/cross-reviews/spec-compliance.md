# Cross-Review: devex-advocate reviews spec-compliance

## Context

The devex-advocate evaluates the spec-compliance auditor's Phase 1 review. The spec-compliance auditor systematically checks each FR and SC. This cross-review examines whether the compliance verdicts align with practical developer experience.

---

### Dangerous Contradictions

- **FR-006 rated PARTIALLY MET — the devex-advocate rates it higher**
  - **spec-compliance claims**: FR-006 (recommendations ordered by impact) is PARTIALLY MET because the impact calculation operates at dimension granularity, not variable granularity. The spec says "the change that would most improve the overall score listed first."
  - **devex-advocate claims**: The dimension-level ordering IS the correct granularity for developer experience. A recommendation that says "[security] fix: 5 high vulns, secrets detected" tells the developer which dimension to focus on, and the dimension-specific advice within the recommendation provides actionable detail. Variable-level ordering would produce confusing recommendations like "improve branch_coverage before fixing high_vulns" — which may be mathematically optimal but misleads developers about what matters.
  - **Why this is dangerous**: If the implementation team reads PARTIALLY MET and builds variable-level impact sorting, the recommendations will become less intuitive, not more. The current dimension-level ordering followed by dimension-specific detail is the better UX pattern.
  - **Suggested resolution**: Rate FR-006 as MET. The spec's language ("the change that would most improve the overall score") is ambiguous about granularity. The current implementation satisfies the intent: recommendations are ordered by which improvement area has the most impact.

- **FR-015 rated PARTIALLY MET — DomainScore.variables not populated**
  - **spec-compliance claims**: `CodeReviewDomain.score()` does not populate `DomainScore.variables`, unlike the base class implementation.
  - **devex-advocate claims**: This is a genuine bug, not a partial implementation. The base class does `variables=variables` but the override in domain.py omits it. This means any code consuming the score (including the planned gate integration) cannot access the raw variables. The spec-compliance auditor correctly identified the gap but should rate it as a bug fix rather than a missing feature.
  - **Why this is dangerous**: If treated as a partial implementation, it might be deprioritized. It is a one-line fix that should be immediate.
  - **Suggested resolution**: Agree this is a bug, not a design gap. Add `variables=variables` to the DomainScore constructor in `CodeReviewDomain.score()`. Elevate to P1.

---

### Tensions

- **FR-010 through FR-013 (persistence) rated NOT MET — is this the right scope?**
  - **spec-compliance's position**: The persistence layer is not implemented: no ReviewStore, no JSONL/SQLite/Supabase backends, no trend analysis, no developer profiles, no debt alerts. Four FRs are NOT MET.
  - **devex-advocate's position**: The persistence FRs represent a different development phase than the core scoring pipeline. The spec correctly separates the plugin into extraction → scoring → persistence → API → gate layers. The current implementation covers extraction and scoring completely. Rating 4 FRs as NOT MET suggests the implementation is failing, when in reality it is progressing through a natural layer-by-layer build. The audit should distinguish between "not yet implemented" and "implemented incorrectly."
  - **Nature of tension**: The spec-compliance auditor measures against the full spec. The devex-advocate measures against what a developer can use today. Both are valid but produce different impressions of project health.
  - **Coordination needed**: Add a "phasing" note to the compliance audit that acknowledges the layer-by-layer implementation strategy. The NOT MET verdicts are factually correct but should include context about whether the missing functionality is part of a planned subsequent phase.

- **Missing spec variables (edge_case_coverage, test_to_code_ratio, duplication_rate, coupling_score)**
  - **spec-compliance's position**: These are defined in the spec's parameter list (Section 2) but have no extractors. They should be added.
  - **devex-advocate's position**: These variables require analysis tools that either do not exist (edge_case_coverage has no standard tool) or require expensive computation (coupling_score requires full import graph analysis). Adding extractors for uncomputable variables would produce permanent None values, which adds noise without value. The spec should be updated to mark these as "future" or "manual assessment" variables rather than expecting extractors for them.
  - **Nature of tension**: Spec fidelity vs. practical implementability.
  - **Coordination needed**: Propose a spec amendment that categorizes variables into "auto-extractable" (have standard tool output) and "manual/future" (require custom tooling or human judgment). Extract only the auto-extractable set.

---

### Safe Agreements

- **SC-001 and SC-002 are correctly rated MET**
  - **Shared position**: The test suite confirms both success criteria. SC-001 is tested with realistic variable values and the healthcare scaffold. SC-002 iterates all scaffolds to confirm universal blocking on secrets_exposed. The devex-advocate confirms the test approach is sound and the variable values in `_make_good_variables()` are realistic for a well-maintained project.
  - **Confidence level**: High.

- **SC-003 is correctly rated NOT MET**
  - **Shared position**: No persistence or trend analysis is operational. The linear regression function exists but is disconnected from any data source. Both perspectives agree this requires implementing the ReviewStore layer.
  - **Confidence level**: High.

- **The core extraction-scoring pipeline is solid**
  - **Shared position**: Both reviews converge on the assessment that FR-001 through FR-009 (extraction and scoring core) are substantially met. The 8 extractors parse real tool output correctly, scaffolds validate against Pydantic, and the weighted scoring produces intuitive results. The spec-compliance audit confirms formal compliance; the devex-advocate confirms practical usability.
  - **Confidence level**: High.

---
