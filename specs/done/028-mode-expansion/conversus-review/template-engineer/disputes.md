# Template Engineer — Round 1 Disputes

---

### Remaining Disputes

- **Dispute: Spec Section 2.1 Game Form Text**
  - **My claim**: The spec text "Game forms: Bayesian (hidden preferences) + Stackelberg (sequential offers)" should be updated to "Game forms: Bayesian (hidden preferences). Sequential offer dynamics are captured by the engine's phase structure." This is a documentation fix, not a code change. [revision.md, adopted from game theorist GT-R1-01]
  - **Opposing position(s)**: None — all three agents converge on this. However, the resolution PATH differs: game theorist recommends updating the spec, spec compliance rates FR-002 as "MET with deviation noted." The template engineer agrees with updating the spec.
  - **Why I hold firm**: The deviation between spec text and implementation creates confusion for future contributors. Spec text should be the source of truth, and when the implementation makes a deliberate design choice (Stackelberg via phase structure), the spec should document that choice.
  - **Proposed resolution**: The synthesizer should mark this as a convergence point, not a dispute. All agents agree the spec should be updated.

The revision process resolved the remaining template engineering conflicts. TE-R1-03 (negotiation review structure) was withdrawn after the game theorist's counter-argument. TE-R1-01 (variable injection) was downgraded to non-issue.

### Convergence

- **Converged: Empty test file is the critical gap**
  - **Shared position**: `tests/test_mode_expansion.py` must be populated with tests covering mode count, template existence, keyword classification, and backward compatibility.
  - **Agreeing agents**: template-engineer, game-theorist, spec-compliance
  - **Strength**: Unanimous
  - **Path to convergence**: All three agents independently identified this in Phase 1.

- **Converged: "ration" keyword regex is a bug**
  - **Shared position**: The regex pattern `ration` in `_DECISION_TYPE_PATTERNS[RESOURCE_ALLOCATION]` matches "rational" as a substring. Fix: `\bration(?:ing|ed)?\b` or `\bration\b`.
  - **Agreeing agents**: template-engineer (adopted in revision), game-theorist (original finder), spec-compliance (rates FR-007 as MET WITH DEFECT)
  - **Strength**: Unanimous
  - **Path to convergence**: Game theorist identified in Phase 1. Template engineer and spec compliance adopted in revision.

- **Converged: All 4 mode-to-form mappings are correct (with spec text fix for negotiation)**
  - **Shared position**: negotiation->bayesian, resource-allocation->coalitional, fair-division->coalitional, mechanism-design->mechanism-design are all correct mappings. The negotiation spec text should be updated to match.
  - **Agreeing agents**: game-theorist, template-engineer, spec-compliance
  - **Strength**: Unanimous
  - **Path to convergence**: Game theorist assessed in Phase 1. Cross-review refined the negotiation mapping from "partially correct" to "correct with spec update needed."

- **Converged: DISPUTES markers and dispute headings are correct**
  - **Shared position**: All 4 new synthesis templates have correctly placed DISPUTES_BEGIN/END markers with mode-specific dispute headings matching schema definitions.
  - **Agreeing agents**: template-engineer, spec-compliance
  - **Strength**: Bilateral (game theorist did not assess this directly)
  - **Path to convergence**: Template engineer verified in Phase 1. Spec compliance independently verified in cross-review.

- **Converged: FR-001 through FR-009 are MET**
  - **Shared position**: The core functional requirements (template sets, mode-mapping, VALID_MODES, decision type classifier, keywords, dispute headings, arbitration headings) are all satisfied.
  - **Agreeing agents**: spec-compliance (primary), template-engineer (supporting on FR-001, FR-008), game-theorist (supporting on FR-002, FR-004, FR-007)
  - **Strength**: Unanimous (different agents verified different FRs)
  - **Path to convergence**: Spec compliance audit in Phase 1, corroborated by cross-reviews.

### Final Position Statement

**Non-Negotiables**:
1. `test_mode_expansion.py` must be populated. Without tests, SC-005 is unverifiable and FR-011 is supported only by design argument. [Consensus across all agents]
2. The "ration" regex must be fixed. A false-positive that matches "rational" in analytical texts will cause misclassification. [Game theorist GT-R1-04, adopted unanimously]

**Flexibility**:
1. The spec Section 2.1 game form text update can be deferred if there is a reason to preserve the current wording (e.g., a future spec plans to add formal Stackelberg support). The template engineer supports updating now but acknowledges the deviation is non-blocking.
2. Cross-round-synthesis DISPUTES marker verification can be deferred to a multi-round testing phase.
