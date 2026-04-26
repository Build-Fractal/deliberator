I'll analyze the conversus codebase from a testing and quality assurance perspective to review the CONSTITUTION.md and identify gaps related to testing discipline.

---

### Executive Summary

The CONSTITUTION.md v2.2.0 establishes solid principles for deterministic orchestration and functional programming but has significant gaps in testing discipline that recent PRs (#8, #10, #12) have exposed. While Principle V (Observable Deliberation) addresses output validation and Principle IX mentions testable functions, the constitution lacks explicit guidance on critical testing patterns that are emerging in the codebase. PR #12's drift guard meta-tests, PR #10's three-layer defense pattern, and PR #8's live integration test discipline represent established testing practices that deserve constitutional protection. The constitution currently treats testing as an implementation detail rather than a first-class architectural concern, leaving teams without clear guidance on when expensive tests are justified, how to prevent coverage drift, or what constitutes adequate defense-in-depth for safety-critical features. **Most important recommendation: Codify the three-layer defense pattern (schema → parser → contract test) as a constitutional principle for safety-critical features.**

### Alignment

- **Observable output validation** (L108-110): The constitution correctly mandates that "Output validation MUST catch malformed results" and "emits warnings for malformed output but does NOT block file writes." This aligns with testing philosophy of validation without blocking progress.

- **Testable functional design** (L172-180): Principle IX correctly emphasizes "easier to test, compose, and reason about" functions and "can be tested in isolation." This matches core testing principles of composability and isolation.

- **Enum completeness verification** (L302-303): The constitution correctly states "The test suite SHOULD verify enum completeness: grep for string literals matching enum values" - this acknowledges automated verification as a testing responsibility.

- **Deterministic reproducibility** (L131-142): Principle VII correctly mandates "Given the same inputs, conversus MUST produce structurally identical output" - this enables reliable testing and validation.

### Missed Opportunities

- **Live test cost discipline**: The constitution lacks guidance on when expensive tests (`@pytest.mark.live`) are appropriate. PR #8 introduced live integration tests that "may cost API credits" but provides no framework for cost justification vs. value. Impact: high.

- **Drift guard meta-test pattern**: PR #12 introduced a meta-test that "asserts coverage of all 7 prompts (drift guard for new prompts)" but this critical pattern isn't codified. When parametrized surfaces expand, coverage can silently degrade without meta-tests. Impact: high.

- **Defense-in-depth testing layers**: PR #10's "schema-level required fields, parser-level validation, contract test" represents a systematic approach to safety-critical testing, but the constitution only mentions validation generically. Impact: high.

- **Behavior-over-shape assertion quality**: The testing constitution in CLAUDE.md emphasizes "behavioral over shape" assertions but this critical principle isn't reflected in CONSTITUTION.md. Shape-only tests create false confidence. Impact: medium.

- **Integration test vs unit test boundaries**: The constitution doesn't distinguish when real integration (PR #14's parametrized FastMCP registration) is necessary vs when mocking suffices. Teams lack guidance on test architecture. Impact: medium.

- **Mutation testing sanity checks**: The CLAUDE.md testing constitution mentions mutation sanity but CONSTITUTION.md has no equivalent. Tests that pass when the real bug is introduced are worthless. Impact: medium.

- **Test categorization discipline**: PR #8's `@pytest.mark.live` pattern suggests a need for systematic test categorization (unit, integration, live, contract) but the constitution provides no framework. Impact: low.

### Off-Base Assumptions

- **Testing as implementation detail** (L164-180): The constitution treats testing as a byproduct of good functional design rather than a first-class architectural concern. PR #10's safety-critical bug demonstrates that testing patterns deserve constitutional protection, not just functional programming patterns.

- **Validation scope too narrow** (L108-110): The constitution focuses validation on "malformed output" but PR #10 showed that structural validation (required fields, parser contracts) is equally critical for correctness. Safety-critical features need more than output format checks.

### Actionable Recommendations

1. **Establish Defense-in-Depth Testing Principle** (Priority: P1)
   - **Current state**: Constitution mentions validation generically (L108-110).
   - **Proposed change**: Add new principle: "Safety-critical features MUST use three-layer defense: schema-level required fields, parser-level validation, contract tests that reproduce failure scenarios. Each layer catches different failure modes and provides independent verification."
   - **Rationale**: PR #10's false-PASS red-blue synthesis bug demonstrates that single-layer validation is insufficient for safety-critical features.
   - **Risk if ignored**: Silent failures in safety-critical paths, as evidenced by the red-blue synthesis returning PASS on dangerous deliberations.

2. **Codify Drift Guard Meta-Test Pattern** (Priority: P1)  
   - **Current state**: Constitution mentions enum completeness checks (L302-303) but not parametrized surface coverage.
   - **Proposed change**: Add requirement: "When adding parametrized capabilities (prompts, tools, modes), MUST include meta-tests that assert complete coverage. Meta-tests fail when new items are added without corresponding test coverage."
   - **Rationale**: PR #12's meta-test prevents coverage drift when new `@mcp.prompt()` definitions are added.
   - **Risk if ignored**: Coverage silently degrades as parametrized surfaces expand, creating untested code paths.

3. **Define Live Test Cost Discipline** (Priority: P1)
   - **Current state**: Constitution has no guidance on expensive test categories.
   - **Proposed change**: Add principle: "Live integration tests that cost API credits or exercise external services MUST be marked with `@pytest.mark.live` and justify their necessity. Live tests are appropriate for: end-to-end distribution verification, provider protocol validation, real subprocess integration. CI MUST be able to opt out."
   - **Rationale**: PR #8 introduced live tests but without framework for when they're justified vs excessive.
   - **Risk if ignored**: Test suites become expensive to run, teams skip testing, or unnecessary API costs accumulate.

4. **Establish Behavior-Over-Shape Testing Principle** (Priority: P2)
   - **Current state**: Constitution emphasizes functional design (L172-180) but not assertion quality.
   - **Proposed change**: Add requirement: "Tests MUST verify behavior, not just shape. Assert what the function accomplishes, not just what it returns. Count side-effects, verify state changes, ensure mutations are sane."
   - **Rationale**: Matches CLAUDE.md testing constitution principles that prevent false confidence from shape-only assertions.
   - **Risk if ignored**: Tests pass when real bugs are introduced, providing false security.

5. **Define Integration Test Architecture Boundaries** (Priority: P2)
   - **Current state**: Constitution doesn't distinguish integration vs unit test appropriateness.
   - **Proposed change**: Add guidance: "Use real integration tests for: capability registration paths, provider protocol handling, cross-process communication. Use mocked unit tests for: pure function logic, data transformations, isolated business rules."
   - **Rationale**: PR #14's parametrized FastMCP integration tests exercise real registration but constitution provides no framework for this choice.
   - **Risk if ignored**: Over-mocking misses integration bugs; over-integration makes tests slow and brittle.

6. **Mandate Contract Test Coverage for Critical Paths** (Priority: P2)
   - **Current state**: Constitution mentions output validation (L108) but not contract verification.
   - **Proposed change**: Add requirement: "Critical state machines and synthesis logic MUST include contract tests that reproduce known failure scenarios. Contract tests verify the fix and prevent regression."
   - **Rationale**: PR #10's contract test that reproduces false-PASS scenario ensures the fix is durable.
   - **Risk if ignored**: Fixed bugs regress because the failure scenario isn't encoded in tests.

7. **Establish Test Category Taxonomy** (Priority: P3)
   - **Current state**: Constitution doesn't categorize test types.
   - **Proposed change**: Add framework: "Test categories are: unit (isolated functions), integration (real registration/subprocess), live (external APIs/costs), contract (reproduce specific failure scenarios). Each serves different validation purposes."
   - **Rationale**: PR #8's `@pytest.mark.live` suggests systematic categorization is emerging organically.
   - **Risk if ignored**: Teams lack shared vocabulary for test architecture decisions.

8. **Require Mutation Sanity Verification** (Priority: P3)
   - **Current state**: Constitution mentions testability but not test effectiveness.
   - **Proposed change**: Add guidance: "Tests SHOULD verify mutation sanity - they fail when the real bug is introduced. Line coverage is a floor, not a quality claim."
   - **Rationale**: CLAUDE.md testing constitution principle that prevents worthless high-coverage tests.
   - **Risk if ignored**: Teams achieve high coverage with ineffective tests that miss real bugs.

### Referenced Documentation

- `CONSTITUTION.md` — sections/lines cited: L108-110, L164-180, L302-303, L131-142, L172-180
- `recent-changes.md` — sections/lines cited: L43-51, L83-92, L61-71, L141-144, L150-153