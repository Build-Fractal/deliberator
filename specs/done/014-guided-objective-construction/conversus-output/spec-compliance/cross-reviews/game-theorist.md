# Cross-Review: spec-compliance reviewing game-theorist

## Dangerous Contradictions

### DC-1. FR-003 priority: P2 (game-theorist) vs P1 (spec-compliance)

Game-theorist classifies FR-003 multi-template presentation as P2 (Recommendation 6). I classify it as P1 because FR-003 uses "MUST present." The contradiction: game-theorist argues the pipeline functions correctly for single-candidate cases and that alphabetical ordering rarely produces ambiguous multi-candidate scenarios. But the spec's MUST is unconditional -- it applies whenever `len(candidates) > 1`, which happens for every SELECTION problem (the mode-specific templates `budget-constrained`, `competitive-selection`, `competitive-ranking` plus general templates all qualify). Game-theorist's framing as "rarely produces ambiguous results" is incorrect: *every* multi-template case triggers the violation.

My position: MUST-level requirements are P1 by definition. The spec author used MUST deliberately. If the implementation team disagrees, they should amend the spec, not silently downgrade the priority.

### DC-2. Missing SC-002, FR-009, FR-014, FR-022 assessments

Game-theorist's review does not assess SC-002 (natural-language weight mapping), FR-009 (gap_fill_model config), FR-014 (conversus.yml integration), or FR-022's LLMGapFiller requirement. I flag all four as NOT MET or PARTIALLY MET. The contradiction: game-theorist's scope ("Does the construction pipeline correctly bridge natural-language problem descriptions to parameterized objective functions?") inherently includes SC-002 (the headline success criterion for natural-language bridging) and FR-009/FR-022 (the mechanism for that bridging). Omitting these creates a gap in the game-theorist's coverage.

### DC-3. Disambiguation via ValueError is unsafe for non-interactive mode

Game-theorist's Recommendation 3 proposes raising `ValueError` when classification is ambiguous (top two types within 1 match). This conflicts with FR-023 (non-interactive mode): if the pipeline is running non-interactively and the classification is ambiguous, raising `ValueError` halts the pipeline with no recovery path. Non-interactive mode is designed to use defaults and fail only on true gaps. Ambiguous classification is not a gap -- it's a classification, just a low-confidence one. The pipeline should log a warning and proceed with the deterministic tiebreaker, not raise an exception.

## Tensions

### T-1. Constraint gap-filling: P3 (game-theorist) vs P1 (spec-compliance, implicit)

Game-theorist raises constraint parameter gap-filling as P3 (Recommendation 8). I don't explicitly raise it as a separate item, but FR-011 ("output includes... constraints with parameters") implies it's needed for compliance. The tension: game-theorist treats constraint parameters as a future completeness item, while the spec requires them in the output. If constraints are listed by name but their parameters are unresolved, the output is structurally valid but practically incomplete. I'd classify this as P2 -- the model validates, but the output is not fully actionable.

### T-2. `problem.md` parser: P3 (game-theorist) vs not raised (spec-compliance)

Game-theorist's Recommendation 9 proposes a `parse_problem_md` function (P3). I mark FR-019 as MET because `classify_decision_type` accepts `explicit_type`. The tension: the *function* accepts explicit type, but there's no *code* to read it from a file. Game-theorist is right that the end-to-end story is incomplete, but the function-level contract is correct. The parser belongs in a CLI or integration layer, not in the construction pipeline. P3 seems right.

### T-3. Template ranking as a correctness concern

Game-theorist devotes significant space to template ranking (Recommendation 10, off-base assumption #1). I note the alphabetical ordering in my FR-002 assessment but mark it as MET because the spec says "select top 1-3 candidate templates" without specifying ranking criteria beyond mode compatibility. The tension: game-theorist reads "candidate templates" as implying relevance ranking, I read it as allowing any deterministic selection. The spec is silent on ranking criteria within the mode-compatible set, so both readings are valid.

### T-4. String parameter enum validation

Game-theorist's Recommendation 5 proposes adding an `options` field to `ParameterDefinition` for string parameters with closed valid sets. I don't raise this. The tension: it's a good UX improvement but requires a schema change to `ParameterDefinition`, which affects the YAML template format. This should be a spec amendment, not a P2 fix applied to the current spec.

## Safe Agreements

### SA-1. Source map discarded by `fill_parameter_gaps`

Both reviews identify the same root cause and propose the same structural fix. Game-theorist's description of the value-comparison bug (user confirms default, recorded as "default" instead of "gap_filled") is precise and matches my understanding.

### SA-2. Boolean coercion is a latent bug

Both reviews identify `_coerce_value` returning `None` for boolean type. Game-theorist proposes P1; I don't explicitly raise it but it falls under the type-safety umbrella.

### SA-3. NonInteractiveGapFiller exception pattern is fragile

Both reviews identify RuntimeError as too broad. Game-theorist offers three alternatives; I don't explicitly raise it but the diagnosis aligns.
