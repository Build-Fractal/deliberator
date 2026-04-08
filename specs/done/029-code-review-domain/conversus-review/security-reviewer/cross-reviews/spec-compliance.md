# Cross-Review: security-reviewer reviews spec-compliance

## Context

The security-reviewer evaluates the spec-compliance auditor's Phase 1 review, focusing on whether the compliance verdicts correctly assess security-relevant requirements and whether the gap analysis addresses security-critical omissions.

---

### Dangerous Contradictions

- **FR-015 rated PARTIALLY MET — but the security implication is understated**
  - **spec-compliance claims**: FR-015 (gate agents receive extracted variables and scaffold as input) is PARTIALLY MET because `CodeReviewDomain.score()` does not populate `DomainScore.variables`. This is described as a missing constructor argument.
  - **security-reviewer claims**: The unpopulated `variables` field is not just a data completeness issue — it has security implications. If the gate system receives a `DomainScore` without `variables`, gate agents cannot verify that the score corresponds to the claimed variable values. An attacker (or buggy code) could construct a `DomainScore` with `overall=0.95, verdict="pass"` without any backing variable data, and the gate would accept it because it has no way to independently verify the score. The `variables` field serves as an audit trail — its absence breaks the verifiability chain.
  - **Why this is dangerous**: If this is treated as a low-priority "add missing parameter" fix, the security gap remains until the gate integration is implemented. The fix should be made immediately because it affects the integrity of any code consuming `DomainScore`.
  - **Suggested resolution**: Agree with the spec-compliance auditor's identification of the bug. Elevate to P1 as the security-reviewer recommends: the `variables` field is the audit trail that makes scores verifiable.

- **FR-010 (append-only persistence) rated NOT MET without security framing**
  - **spec-compliance claims**: FR-010 is NOT MET because no ReviewStore implementation exists. The auditor treats this as a feature gap.
  - **security-reviewer claims**: Append-only semantics are a security property, not just a persistence feature. In a code review domain, append-only ensures that historical scores cannot be retroactively modified to hide regressions. When the store is eventually implemented, the append-only constraint must be enforced at the storage layer (e.g., JSONL files opened in append mode, database INSERT without UPDATE permissions), not just as a protocol convention. The spec-compliance auditor's NOT MET verdict is correct but should note that this is a security-critical FR, not just a missing feature.
  - **Why this is dangerous**: If the persistence layer is implemented without append-only enforcement at the storage level, it could be implemented as a regular CRUD store, violating the spec's intent of immutable audit records.
  - **Suggested resolution**: When implementing FR-010, the ReviewStore must enforce append-only at the I/O layer. JSONLReviewStore should open files with `mode="a"` only. SupabaseReviewStore should use INSERT-only permissions. Add this implementation guidance to the compliance audit's recommendations.

---

### Tensions

- **SC-005 rated PARTIALLY MET — timing criterion vs. completeness**
  - **spec-compliance's position**: SC-005 (full pipeline in under 60s) is PARTIALLY MET because only extract + score run. The timing target is met for the implemented portion but the criterion requires the full pipeline.
  - **security-reviewer's position**: The 60-second timing constraint has security implications for the gate stage. If the conversus gate involves 3 LLM agent calls (as specified in SC-004), the 60-second budget must accommodate LLM latency. At typical Claude/GPT latencies of 5-15 seconds per call with 3 agents doing review + cross-review + synthesis, the gate alone could consume 45-90 seconds. The timing constraint may be unrealistic for the full pipeline, which means either (a) the gate stage must use a cheaper/faster model, or (b) the timing constraint needs revision. The spec-compliance auditor should flag this as a constraint that may not be satisfiable.
  - **Nature of tension**: The spec-compliance auditor evaluates against the stated criterion. The security-reviewer evaluates whether the criterion is achievable given the architecture.
  - **Coordination needed**: Flag SC-005 as potentially unsatisfiable given the gate's LLM latency requirements. The pipeline extract → score → persist runs in milliseconds. The gate → equilibrium adds LLM calls that may exceed the 60-second budget. Either revise the criterion or specify that the gate uses a fast model.

- **Missing variables (edge_case_coverage, duplication_rate, coupling_score)**
  - **spec-compliance's position**: These are in the spec but have no extractors. Recommends adding them.
  - **security-reviewer's position**: `edge_case_coverage` is the most security-relevant missing variable. Edge case coverage directly correlates with resilience against unexpected inputs — a primary attack vector. The fact that no standard tool produces this metric is a real limitation, but it could be approximated by analyzing test names/docstrings for keywords like "edge", "boundary", "error", "invalid", "empty", "null", "overflow". This heuristic approach would be better than permanent None.
  - **Nature of tension**: The spec-compliance auditor lists all missing variables equally. The security-reviewer wants to prioritize `edge_case_coverage` because of its security relevance.
  - **Coordination needed**: Implement a heuristic `edge_case_coverage` extractor that analyzes test names and docstrings. Even a rough approximation provides more security signal than None.

---

### Safe Agreements

- **FR-001, FR-002, FR-003 correctly rated MET**
  - **Shared position**: The extraction core is solid. FR-001 (standard tool output parsing) is confirmed by tests with real-format fixtures. FR-002 (pluggable extractors) is confirmed by the Protocol-based design. FR-003 (None defaults with warnings) is confirmed by comprehensive missing-report tests. The security-reviewer confirms that the None-default behavior does not introduce false positives (it introduces false negatives, which is the lesser evil for a tool-optional system).
  - **Confidence level**: High.

- **FR-005 correctly rated MET**
  - **Shared position**: Hard blocks override composite scores. The `if triggered_blocks: verdict = "block"` check at domain.py line 408 is the first verdict check, ensuring no subsequent logic can downgrade a BLOCK to PASS. Tests confirm universal blocking on secrets_exposed across all scaffolds. The security-reviewer verifies this is the correct priority ordering.
  - **Confidence level**: High.

- **SC-002 correctly rated MET**
  - **Shared position**: All scaffolds block on `secrets_exposed`. The test iterates all scaffolds programmatically (not hard-coded names), so adding a new scaffold that omits `secrets_exposed` would fail the test. The security-reviewer confirms the test methodology is sound — it tests the invariant rather than individual scaffolds.
  - **Confidence level**: High.

---
