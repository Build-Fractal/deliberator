# Spec Compliance — Round 1 Disputes

---

### Remaining Disputes

- **Dispute: SC-005 Assessment Method**
  - **My claim**: SC-005 ("All existing tests pass unchanged") is NOT VERIFIABLE by code inspection alone. It requires running the test suite. The template engineer and game theorist argue that additive changes and enum tiebreakers guarantee backward compatibility BY DESIGN. While I accept the design argument for FR-011, SC-005 is a different requirement: it asks whether tests PASS, not whether the design is backward-compatible.
  - **Opposing position(s)**: Template engineer and game theorist argue that FR-011 (MET BY DESIGN) implies SC-005 would pass. The logic: if existing modes work identically (FR-011), then tests of existing modes pass (SC-005).
  - **Why I hold firm**: The implication is valid ONLY if the existing tests test ONLY mode behavior. If existing tests test anything that touches the expanded `VALID_MODES` (e.g., testing that `len(VALID_MODES) == 4`), they would fail. Hardcoded constants in existing tests are a real risk. SC-005 requires empirical verification, not logical deduction.
  - **Proposed resolution**: The synthesizer should note this as an unresolved item requiring test execution. The test file should include both new tests AND a regression suite that runs existing tests.

### Convergence

- **Converged: Test file population is critical**
  - **Shared position**: `tests/test_mode_expansion.py` must be populated.
  - **Agreeing agents**: template-engineer, game-theorist, spec-compliance
  - **Strength**: Unanimous
  - **Path to convergence**: Independent Phase 1 identification.

- **Converged: "ration" keyword defect**
  - **Shared position**: FR-007 has a defect: `ration` pattern matches "rational."
  - **Agreeing agents**: All three agents
  - **Strength**: Unanimous
  - **Path to convergence**: Game theorist Phase 1, universally adopted.

- **Converged: Spec Section 2.1 game form text update**
  - **Shared position**: Remove "Stackelberg" from negotiation game form claim, add note about procedural phase dynamics.
  - **Agreeing agents**: All three agents
  - **Strength**: Unanimous
  - **Path to convergence**: Game theorist identified, spec compliance classified, all agreed in revision.

- **Converged: FR-001 through FR-009 compliance**
  - **Shared position**: All core FRs are MET (with noted defect on FR-007 and deviation on FR-002).
  - **Agreeing agents**: All three agents
  - **Strength**: Unanimous
  - **Path to convergence**: Spec compliance audit confirmed, cross-reviews corroborated.

- **Converged: FR-011 backward compatibility by design**
  - **Shared position**: All changes are additive. Existing modes work identically. Enum ordering tiebreaker preserves classification behavior.
  - **Agreeing agents**: template-engineer, game-theorist (strong support), spec-compliance (accepts design argument)
  - **Strength**: Unanimous
  - **Path to convergence**: Spec compliance initially rated NOT VERIFIABLE, upgraded to MET BY DESIGN after cross-review evidence.

### Final Position Statement

**Non-Negotiables**:
1. SC-005 must be verified empirically. The design argument supports FR-011 but does not substitute for running the test suite. Until tests run, SC-005 remains NOT VERIFIABLE. [No other agent contests this directly — they agree tests should exist, they just argue the design is sound]
2. The "ration" regex fix is a P1 requirement for FR-007 correctness.

**Flexibility**:
1. FR-005 and FR-010 assumptions can remain as assumptions unless the team wants to examine the CLI and linter implementations. The assumptions are reasonable.
2. The spec Section 2.1 update can be combined with the "Modes Considered and Excluded" section the game theorist requests.
