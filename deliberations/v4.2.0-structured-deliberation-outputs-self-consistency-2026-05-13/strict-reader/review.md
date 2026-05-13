I need to read all the target documents before providing my review. Let me start by reading the files systematically.

# Strict-Reader Review — v4.2.0 Structured Deliberation Outputs

---

### Executive Summary

Spec v2 attempts to implement Tier 2 Principle XXVIII (Persistence Contract Discipline) for conversus-oss deliberation outputs by mandating JSON Schema validation with CI enforcement. The spec addresses legitimate production bugs (prompt overflow, cross-review persistence failures, trigger misses) through structural schema enforcement replacing brittle markdown parsing.

However, my strict literal reading reveals critical constitutional violations: v2's blocking validation directly contradicts Tier 2 Principle V's explicit "does NOT block file writes" requirement, and v2 incompletely implements two of the five XXVIII sub-clauses. The spec extends stable interfaces correctly but creates constitutional conflicts in validation behavior.

**Most important recommendation:** Fix the Principle V contradiction by implementing non-blocking schema validation that warns but does not abort phases.

### Alignment

- **JSON Schema canonical format** (`spec.md L90`): Convergence on JSON Schema Draft 2020-12 with Python `jsonschema` library aligns with mechanical enforceability requirements. Supports literal interpretation of XXVIII sub-clause 2's "machine-executable conformance check." [`build-fractal/conversus/CONSTITUTION.md L527-531`]

- **SemVer versioning policy** (`spec.md L463-468`): Consumer-impact qualification for MAJOR/MINOR/PATCH bumps correctly implements XXVIII sub-clause 3's documented bump procedure requirement. Field renames classified as MAJOR despite technical additivity shows correct consumer-perspective reasoning. [`build-fractal/conversus/CONSTITUTION.md L547-553`]

- **Three worked-example fixtures** (`spec.md L541-547`): Conformant/non-conformant test fixtures with expected validator outputs satisfy XXVIII sub-clause 2's fixture requirements. Mechanical CI enforcement with binary pass/fail results. [`build-fractal/conversus/CONSTITUTION.md L538-545`]

- **Cross-product contract declarations** (`spec.md L571, L592-596`): CONSUMER-CONTRACT.md at producer repo root with orchestrator adapter consumer-side declarations correctly implements XXVIII sub-clause 4's cross-product consumer contract requirement. [`build-fractal/conversus/CONSTITUTION.md L555-568`]

### Missed Opportunities

- **Principle V harmonization**: XXVIII sub-clause 2 requires CI enforcement but doesn't mandate blocking behavior at write-time. v2 could implement non-blocking validation that satisfies both principles by warning on schema violations without aborting phases. Impact: high.

- **CONFORMANCE.md schema location documentation**: XXVIII sub-clause 1 requires suite-convention directories be documented in the repo's CONFORMANCE.md. v2 omits this documentation step for `engine/schema/v1/` location. Impact: medium.

- **Display text declaration scope coverage**: XXVIII sub-clause 5 requires explicit declaration of any display-text surfaces with stability guarantees. v2 migrates away from display text but doesn't declare the migration scope explicitly. Impact: medium.

- **Component-tier principle compatibility check**: v2 doesn't verify compatibility with component-tier principles that may constrain engine validation behavior. Missing systematic constitutional review. Impact: medium.

- **Recursion precedent boundary definition**: v2's RECURSION-EXEMPTED status needs clearer boundaries to prevent slippery precedent for future meta-schema amendments. Current wording is too permissive. Impact: low.

### Off-Base Assumptions

- **Validation blocking assumption** (`spec.md L527-528`): Spec assumes schema validation failures should "abort the phase (does not write the malformed file)" but Principle V explicitly states output validation "does NOT block file writes. Malformed output is better than no output." The assumption directly contradicts ratified constitutional text.

- **Location discoverability assumption** (`spec.md L525`): Spec assumes `engine/schema/v1/` is inherently discoverable but XXVIII sub-clause 1 requires suite-convention directories be documented in CONFORMANCE.md. Literal reading shows this assumption is constitutionally insufficient.

### Actionable Recommendations

1. **Fix Principle V contradiction** (Priority: P1)
   - **Current state**: L527-528 mandates validation failures "abort the phase (does not write the malformed file)"
   - **Proposed change**: Replace with non-blocking validation that emits warnings but allows file writes to proceed, per Principle V's "Malformed output is better than no output" requirement
   - **Rationale**: Direct constitutional conflict requires resolution [`build-fractal/conversus/CONSTITUTION.md L76-78`]
   - **Risk if ignored**: Constitutional violation; spec contradicts ratified Tier 2 principle

2. **Document schema location in CONFORMANCE.md** (Priority: P1)  
   - **Current state**: L525 places schemas at `engine/schema/v1/` without CONFORMANCE.md documentation
   - **Proposed change**: Add requirement to document the schema location in conversus-oss CONFORMANCE.md per XXVIII sub-clause 1 discoverability criteria
   - **Rationale**: XXVIII sub-clause 1 literal text requires suite-convention directories be documented [`build-fractal/conversus/CONSTITUTION.md L504-505`]
   - **Risk if ignored**: Incomplete XXVIII implementation; discoverable-location criterion unfulfilled

3. **Add display text declaration scope** (Priority: P2)
   - **Current state**: v2 migrates from display text but doesn't address XXVIII sub-clause 5 declaration requirements  
   - **Proposed change**: Explicitly declare in CONSUMER-CONTRACT.md which display-text surfaces (if any) remain stable during migration, or declare complete migration away from display text parsing
   - **Rationale**: XXVIII sub-clause 5 requires explicit declaration of display-text stability [`build-fractal/conversus/CONSTITUTION.md L570-585`]
   - **Risk if ignored**: Incomplete constitutional compliance; unclear consumer contract scope

4. **Clarify recursion precedent boundaries** (Priority: P2)
   - **Current state**: L623-626 documents RECURSION-EXEMPTED status without clear precedent boundaries
   - **Proposed change**: Add explicit language that exemption applies only to this specific bootstrap case, not as general precedent for meta-schema amendments
   - **Rationale**: Prevent slippery precedent similar to override-with-rationale debacle in v4.1.0 [`QUESTION.md L47-48`]
   - **Risk if ignored**: Precedent erosion; future amendments claiming inappropriate exemptions

5. **Add component-tier compatibility verification** (Priority: P3)
   - **Current state**: v2 doesn't verify compatibility with component-tier principles  
   - **Proposed change**: Add systematic review against component-tier conversus-oss CONSTITUTION.md principles for validation behavior constraints
   - **Rationale**: Q3 requirement to check component-tier principle compatibility [`QUESTION.md L64-65`]
   - **Risk if ignored**: Potential constitutional conflicts at component tier

### Referenced Documentation

- `build-fractal/conversus/CONSTITUTION.md` — sections/lines cited: L70-81 (Principle V), L490-644 (Principle XXVIII), L500-522 (sub-clause 1), L524-545 (sub-clause 2), L547-553 (sub-clause 3), L555-568 (sub-clause 4), L570-585 (sub-clause 5)
- `build-fractal/conversus/conversus-oss/specs/v4.2.0-structured-deliberation-outputs/spec.md` — sections/lines cited: L90, L463-468, L525, L527-528, L541-547, L571, L592-596, L623-626
- `QUESTION.md` — sections/lines cited: L47-48, L60, L64-65