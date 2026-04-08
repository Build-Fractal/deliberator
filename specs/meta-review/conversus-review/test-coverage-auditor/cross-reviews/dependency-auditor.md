# Cross-Review: test-coverage-auditor reviewing dependency-auditor

**Date**: 2026-04-01
**Phase**: 2 — Cross-Reviews

---

## Dangerous Contradictions

### DC-1: "No cross-boundary violations found" is an import-level statement that my test coverage data complicates

The dependency-auditor's central conclusion is that all dependency boundaries are clean. My audit reveals that 59% of P1 findings lack test coverage. The tension: clean dependency boundaries create a false sense of safety if the code within those boundaries is untested. Specifically:
- `plugins/nashopt/` has clean imports but its solver post-processing (the code that maps results back to agents) has no test exercising the real code path.
- `domains/code_review/` has clean imports from `domains/base` but the behavioral contract (populating `DomainScore.variables`) is broken and untested.
- `plugins/optimizer/` has clean imports but the `HAS_AMPL` guard does not check for `highspy`, and no test verifies this.

The dependency-auditor's "verified" applies to the wiring. My "untested" applies to the behavior. Both are true, and together they reveal that the architecture is correctly wired but incompletely validated.

### DC-2: The VariableExtractor protocol conformance recommendation has no test to anchor it

The dependency-auditor recommends adding `isinstance(extractor, VariableExtractor)` assertions to tests (P2 recommendation #3). I confirm there is no test that verifies extractors satisfy the protocol at runtime. The recommendation is sound but the dependency-auditor does not specify which test file should contain these assertions. Given that the protocol is defined in `domains/base.py` (spec 030) but implemented in `code_review/extractors.py` (spec 029), the test could live in either `test_domains.py` or `test_code_review.py`. The cross-boundary nature of this test mirrors the cross-spec integration test gap I identified.

### DC-3: The engine isolation finding implies an untestable orchestration layer

The dependency-auditor correctly identifies that the engine has zero imports from plugins, domains, or schemas. This means plugin execution must happen at a higher layer. From a test perspective, this means there is no test (and possibly no code) for the orchestration that connects these components. My finding of zero cross-spec integration tests is the test-side manifestation of the dependency-auditor's engine isolation finding.

---

## Tensions

### T-1: How to prioritize dependency documentation vs. dependency testing

The dependency-auditor's P3 recommendation is to "map the full dependency DAG" with an import-linting tool. My priority is to add tests for the P1 code bugs that the dependency DAG cannot catch. Both are valuable: the dependency DAG prevents future boundary violations, and tests prevent future behavioral regressions. But with limited resources, I would prioritize tests over documentation because a failing test catches a regression automatically, while a dependency diagram requires manual review.

### T-2: The `domains/__init__.py` docstring fix

The dependency-auditor rates this P1. My audit does not directly address docstring accuracy, but I note that docstring inaccuracy does not cause test failures. If the docstring claims a dependency on `plugins.base` that does not exist, no test will fail because the dependency does not exist to test. The P1 rating reflects the dependency-auditor's concern about mental models; I would rate it P2 because it has no runtime or test impact.

### T-3: Protocol conformance testing approach

The dependency-auditor recommends `isinstance` checks in tests. An alternative approach would be to add `@runtime_checkable` to the Protocol definition and test with `assert isinstance(extractor, VariableExtractor)`. This would also serve as documentation of the protocol contract. My preference is the latter because it tests the actual Python runtime behavior, not just the test author's understanding of the protocol.

---

## Safe Agreements

### SA-1: Plugin-to-plugin isolation is verified at both dependency and test levels

The dependency-auditor verified zero cross-plugin imports. My audit confirms test files are organized per-spec and do not import test utilities across spec boundaries. The isolation holds at every level.

### SA-2: schemas/ independence is well-verified and well-tested

The dependency-auditor confirms schemas/ is a leaf package. My audit confirms specs 025 and 026 (which live in schemas/) have the best test coverage alignment.

### SA-3: The orchestration layer gap is shared across both reviews

The dependency-auditor's Missed Opportunity #2 and my Missed Opportunity #1 identify the same fundamental gap: there is no verified mechanism for connecting the components, and no test for it. This convergence strengthens the case for addressing the gap.
