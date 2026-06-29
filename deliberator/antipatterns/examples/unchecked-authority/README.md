# Antipattern: Unchecked Authority Assertion

## Summary

An agent leverages its domain expertise to assert positions as fact without grounding them in the actual code or documentation under review. When the assertion is wrong, other agents defer to the "expert" rather than verifying independently — propagating the error through cross-reviews, revisions, and into the synthesis.

## Classification

- **Severity**: High
- **Detection difficulty**: Medium (requires cross-referencing agent claims against source material)
- **Blast radius**: High (ungrounded claims survive multiple phases if unchallenged)

## Symptoms

1. An agent's Alignment section praises something that contradicts their own Recommendations section
2. An agent labels code as "well-structured" or "correct" without citing specific lines
3. Expert-role agents make domain claims that other agents accept without independent verification
4. The synthesis records a "convergence" on a position that no agent actually verified against the source

## Real Example: Spec 005 Deliberation

### The Incident

**integration-architect** (Round 1, review.md) made two unchecked authority assertions:

#### Assertion 1: "Pure functions" label on impure code

In the Alignment section, integration-architect praised the schema-loading functions as "pure functions returning typed models" and part of a "well-structured pipeline." This was factually wrong — `load_variables_schema` and `load_mode_schema` both called `sys.exit(2)` and `click.echo()` on failure paths, making them impure and untestable.

**Source**: [integration-architect/review.md, Alignment section](../../../specs/done/005-generalized-templates/deliberator-review/round-1/integration-architect/review.md)

The same agent then recommended a programmatic `validate_all()` API (Recommendation #2) that *depended on those functions being composable* — but never connected that the impurity was a blocker.

#### Assertion 2: Self-contradictory MODE_PRESENCE position

In the same review, integration-architect stated in Alignment: "The hardcoded table is the correct implementation" and "This is the right approach." Then in Recommendation #7: called the same table "brittle coupling" and proposed moving it to mode schema YAML.

**Source**: [integration-architect/review.md, Alignment bullet 6 vs Recommendation 7](../../../specs/done/005-generalized-templates/deliberator-review/round-1/integration-architect/review.md)

### How It Propagated

- **Phase 1**: integration-architect publishes the self-contradictory review
- **Phase 2**: functional-typing catches BOTH contradictions in cross-review ([functional-typing/cross-reviews/integration-architect.md](../../../specs/done/005-generalized-templates/deliberator-review/round-1/functional-typing/cross-reviews/integration-architect.md), Dangerous Contradictions #1 and #2)
- **Phase 3**: integration-architect concedes and retracts ([integration-architect/revision.md](../../../specs/done/005-generalized-templates/deliberator-review/round-1/integration-architect/revision.md), Rec 7 disposition: "I retract the Alignment endorsement")
- **Phase 5 Synthesis**: Records the self-contradictions as resolved, notes "integration-architect retracted 2 self-contradictions identified by cross-reviewers" ([summary/final.md](../../../specs/done/005-generalized-templates/deliberator-review/round-1/summary/final.md), line 30)

### What Went Right

The cross-review phase caught the errors. functional-typing independently verified the claims against the actual code and identified both contradictions with line-number citations. The adversarial structure worked.

### What Could Have Gone Wrong

If functional-typing had deferred to integration-architect's "expert assessment" of the pipeline as well-structured, the impure loaders would have remained unaddressed. The programmatic API (Rec #2) would have been implemented on top of functions that call `sys.exit()`, producing a `validate_all()` that terminates the process instead of returning errors. This would have been caught at runtime, wasting implementation effort.

The MODE_PRESENCE contradiction, if undetected, would have produced a synthesis that both endorsed the hardcoded table AND recommended replacing it — confusing the implementer.

## Correction

Templates and agent instructions should:
1. Require agents to cite specific line numbers for every factual claim about code
2. Instruct cross-reviewers to independently verify cited lines, not accept claims on authority
3. Flag uncited praise (Alignment claims without line references) as lower-confidence than cited criticism

## Related

- Constitution Principle IX: explicit typing and clean code
- Template rule: "Evidence over opinion"
- Spec 005 cross-round synthesis: [summary/final.md](../../../specs/done/005-generalized-templates/deliberator-review/summary/final.md)
