# Game Theorist — Round 1 Disputes

---

### Remaining Disputes

- **Dispute: Whether 8 modes is the right number or should be 9+**
  - **My claim**: The current 8 modes cover the vast majority of real-world multi-agent decision scenarios. The voting/social choice gap (GT-R1-06) was correctly withdrawn as out of scope. However, I want to register a formal observation: the mode expansion spec should include an explicit "modes NOT covered" section documenting what was deliberately excluded and why. This prevents future contributors from re-discovering the same gaps.
  - **Opposing position(s)**: Template engineer argues that winner-take-all approximates committee voting. This is true for simple plurality votes but not for ranked-choice or Condorcet methods. The approximation is "good enough" for spec 028 but the limitation should be documented.
  - **Why I hold firm**: This is not a dispute about adding modes — it is a dispute about documentation completeness. The spec should explicitly state: "The following decision types were considered and excluded: voting/social choice (approximated by winner-take-all), repeated games (handled by multi-round infrastructure), coalition attribution (handled by existing mode-mapping entry)."
  - **Proposed resolution**: Add a "Modes Considered and Excluded" section to spec 028. This is a documentation addition, not a code change.

The revision process resolved the game form mapping concerns (GT-R1-01 → spec update, GT-R1-06 → withdrawn). The keyword concerns (GT-R1-03 → downgraded, GT-R1-04 → adopted unanimously) are settled.

### Convergence

- **Converged: Empty test file must be populated**
  - **Shared position**: `tests/test_mode_expansion.py` is the critical gap. Must include mode count tests, keyword classification tests, and backward compatibility regression tests.
  - **Agreeing agents**: template-engineer, game-theorist, spec-compliance
  - **Strength**: Unanimous
  - **Path to convergence**: Independent identification in Phase 1 by all three agents.

- **Converged: "ration" keyword is a bug requiring fix**
  - **Shared position**: The `ration` pattern in RESOURCE_ALLOCATION keywords matches "rational." Fix required.
  - **Agreeing agents**: game-theorist (finder), template-engineer (adopted), spec-compliance (adopted)
  - **Strength**: Unanimous
  - **Path to convergence**: Identified by game theorist in Phase 1, universally adopted in revisions.

- **Converged: Negotiation spec text should be updated**
  - **Shared position**: Spec Section 2.1 should state "Game forms: Bayesian" and note that Stackelberg dynamics are procedural.
  - **Agreeing agents**: game-theorist, template-engineer, spec-compliance
  - **Strength**: Unanimous
  - **Path to convergence**: Game theorist identified the deviation. Spec compliance classified it. All agree on spec update as resolution.

- **Converged: All mappings are formally correct**
  - **Shared position**: The 4 new mode-to-form mappings (bayesian, coalitional, coalitional, mechanism-design) are the correct formal game theory mappings for their respective deliberation modes.
  - **Agreeing agents**: game-theorist, template-engineer (corroborated form-template consistency), spec-compliance (FR-002 MET)
  - **Strength**: Unanimous
  - **Path to convergence**: Game theorist assessed formally, template engineer verified template-form consistency, spec compliance verified existence.

- **Converged: No redundant modes exist**
  - **Shared position**: All 8 modes are distinct and serve different decision structures.
  - **Agreeing agents**: game-theorist (formal analysis), template-engineer (structural analysis)
  - **Strength**: Bilateral
  - **Path to convergence**: Game theorist's differentiation table in Phase 1. Template engineer corroborated via distinct output structures.

### Final Position Statement

**Non-Negotiables**:
1. The "ration" regex must be fixed before the mode expansion is considered complete. A keyword pattern that generates false positives undermines the heuristic classification that FR-007 depends on.
2. Test coverage must exist. Without tests, the formal correctness of the mappings cannot be verified at runtime.

**Flexibility**:
1. The "Modes Considered and Excluded" documentation addition can be deferred to a post-implementation documentation pass if the team prefers to ship the 8-mode implementation first.
2. The "settle" keyword hardening (GT-R1-03) is truly optional — the match-count mechanism provides adequate protection.
