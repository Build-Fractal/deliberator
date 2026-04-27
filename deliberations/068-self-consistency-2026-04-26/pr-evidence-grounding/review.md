### Executive Summary

The amended Principle XVI makes three concrete, code-checkable claims about the 3-stage pipeline: (1) symbolic parsing is deterministic given a template ID; (2) LLM gap-filling output is **pinned per deliberation run** with a cached-reuse rule ("repeating a deliberation with the same input does NOT re-call the LLM for parameters; cached values from the first resolution are reused"); (3) mechanical assembly is bit-for-bit identical given a fully-pinned parameter set. Claims (1) and (3) are testably present in `conversus/schemas/construction.py` and the `objective.yml` artifact contract from spec 014. Claim (2) — the **pinning + cached-reuse** discipline — is the one the candidate text most strongly asserts as code behavior, and it is the one I cannot ground in the current codebase.

A spot-check of `conversus/schemas/construction.py`, `conversus/schemas/objectives.py`, and spec 014 (`done/014-guided-objective-construction/spec.md`) shows the pipeline is structured around three stages whose names match the candidate (FR-012 is exactly the bit-for-bit assembly claim; the docstring at construction.py:1-15 names "deterministic / interactive / deterministic" stages). However, **no module persists or caches LLM gap-filled values across deliberation runs.** The `GapFiller` protocol (construction.py:139-171) is invoked synchronously; `InteractiveGapFiller` calls `input()`, `NonInteractiveGapFiller` raises. There is no cache layer between gap_filler invocations and no "first resolution wins; subsequent calls reuse" mechanism in either the schema or any optimizer/nashopt module (in fact, no `optimizer/` or `nashopt/` package exists in conversus-oss yet — game-engine specs 016-019 are speced but the runtime layer they describe is partly aspirational).

Spec 068 itself anticipates this gap: §7 Q1 says **"Required check before deliberations: grep `conversus/` for parameter-resolution call sites,"** and §6 lists "the 'pinned per deliberation run' claim conflicts with how parameters actually flow" as a Medium risk. Constitution v2.3.2's wording does not reflect that the check has been performed — it asserts the discipline as if already implemented. The principle is therefore best characterized as **a target state the codebase has not yet reached**, written in the indicative mood. This is not necessarily wrong (constitutions can codify forward intent), but the candidate's lack of any "aspirational" / "this is the discipline future PRs must satisfy" hedge makes the claim falsifiable today.

### Alignment

- **Three-stage naming matches code.** Candidate lines 462-470 align with `conversus/schemas/construction.py:1-15` ("Stage 1 (deterministic) … Stage 2 (interactive) … Stage 3 (deterministic)"). Terminology and ordering grounded.
- **Stage 3 mechanical determinism is verifiable.** Candidate lines 471-473 matches spec 014 FR-012 ("Assembly is deterministic: same template + same parameters = same `objective.yml`"). SC-004 already constitutes a regression test.
- **Stage 1 symbolic parsing determinism is verifiable.** `_DECISION_TYPE_PATTERNS` and `select_candidate_templates()` (construction.py) are pure functions over loaded templates.
- **Spec 013 reference is correct.** `ObjectiveTemplate` Pydantic model loads design-time YAML — the math IS template-shaped, not LLM-generated.
- **Provenance tracking provides the within-run discipline hook.** `SourceProvenance.filled_by` (construction.py:262-279) tags parameters as `"explicit" | "default" | "gap_filled" | "deferred"`. A future CI check could enforce "no parameter changes its `gap_filled` value within a single run."
- **The clarification's testable invariant is well-formed.** "A future PR that re-resolves parameters mid-deliberation … violates this principle" (lines 497-498) is enforceable by a hypothetical lint or CI test.

### Missed Opportunities

- **No mention of `objective.yml` as the pinning artifact.** The candidate frames pinning as a runtime cache when spec 014's actual mechanism is **artifact-mediated**: `objective.yml` is written once, and subsequent runs load it instead of re-calling the LLM. Lines 469-471 should reference `objective.yml` directly.
- **No cross-reference to spec 014 FR-012/SC-004.** Candidate cites spec 013 but not spec 014, where the deterministic-assembly contract is actually written.
- **"Per deliberation run" is undefined.** Without an artifact anchor (session ID, output directory, `conversus.yml` invocation), the within-run-vs-cross-run boundary is ambiguous.
- **Spec 016 plugin-system reference is missing.** Origin note (line 500) cites "specs 012-019" but body doesn't say which spec governs *when* the LLM is called.
- **No mention of provenance auditability.** `SourceProvenance.filled_by` is the natural hook for verifying the pinning discipline.
- **The "stochastic at the LLM call" caveat could name the failure mode.** "Two `/conversus mode` invocations on the same problem.md MAY produce different `objective.yml` files; the constitution permits this" would make the cross-run permission unambiguous.
- **No explicit "evidence-pending" hedge.** Spec 068 §7 Q1 explicitly flags that the parameter-pinning behavior must be verified in code before merging the wording.
- **Stage-2 GapFiller protocol could be referenced.** `GapFiller` (construction.py:139-149) is the literal extension point for the LLM call.
- **"Cross-run variance is acceptable" deserves a note about VII reconciliation.** Principle VII demands "Given the same inputs, conversus MUST produce structurally identical output." The candidate's "cross-run variance is acceptable" creates an apparent conflict.

### Off-Base Assumptions

- **"Cached values from the first resolution are reused" is not implemented as described.** No cache layer exists in `conversus/schemas/construction.py`, `conversus/registry/`, or any optimizer module. The pinning is achieved by **writing `objective.yml` to disk and re-reading it** — artifact-based persistence, not a runtime cache.
- **"Mechanical assembly" rename may be premature.** `conversus/schemas/construction.py:8-14` still calls stage 3 "deterministic," and spec 014 FR-012 says "Assembly is deterministic." The constitution and code now use different vocabulary for the same stage.
- **The optimizer/plugin layer XVI describes is partly aspirational.** No `conversus/optimizer/`, `conversus/nashopt/`, or `conversus/ampl/` directory in conversus-oss. Specs 016-019 are spec'd but the runtime is partly in development.
- **"Pinned per deliberation run" boundary is not enforced anywhere.** No test in `engine/tests/` asserts within-run pinning; no Pydantic validator flags re-resolution; no CI gate.

### Actionable Recommendations

1. **(P1)** Add an "evidence-pending" hedge to XVI lines 469-471 OR perform spec 068 §7 Q1's required grep audit and cite the result inline before merging.
2. **(P1)** Replace "cached values from the first resolution are reused" with the actual mechanism: "values are persisted to `objective.yml` (spec 014 FR-012) and re-loaded rather than re-resolved."
3. **(P1)** Reconcile the "mechanical assembly" vs "deterministic assembly" terminology drift.
4. **(P2)** Add cross-references in XVI to spec 014 FR-012/SC-004 and spec 016 (plugin system).
5. **(P2)** Define "deliberation run" explicitly — tie it to a concrete artifact.
6. **(P2)** Add a constitutional reference to `SourceProvenance.filled_by` as the auditable hook.
7. **(P2)** Acknowledge that the optimization-layer specs (016-019) are partly under construction.
8. **(P3)** Add a regression test covering SC-004.
9. **(P3)** Clarify the relationship between Principle XVI and Principle VII.
10. **(P3)** File a separate spec or follow-up issue to add a CI lint detecting re-entrant `GapFiller.fill()` calls.

### Referenced Documentation

- `CONSTITUTION-v2.3.2-candidate.md` — lines 448-503 (XVI body), 462-490 (replaced first bullet), 491-498 (v2.3.2 clarification)
- `specs/068-principle-xvi-fix/spec.md` — §6 Risks, §7 Q1
- `conversus/schemas/construction.py` — lines 1-15 (stage docstring), 139-171 (`GapFiller`, no caching), 262-316 (`SourceProvenance`, `AssembledObjective` validators)
- `conversus/schemas/objectives.py` — lines 49-91 (`ParameterDefinition`)
- `specs/done/014-guided-objective-construction/spec.md` — FR-012, FR-020, FR-021, SC-004
- Spot-check confirmation: no `optimizer/`, `nashopt/`, `ampl/` directories in `conversus/` outside `.venv`.
