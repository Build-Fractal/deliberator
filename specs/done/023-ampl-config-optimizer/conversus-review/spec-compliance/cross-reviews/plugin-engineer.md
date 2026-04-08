# Cross-Review of plugin-engineer's Review

**Cross-reviewer**: spec-compliance
**Reviewing**: plugin-engineer's review of spec 023
**Date**: 2026-04-01

---

### Dangerous Contradictions

- **Unimplemented `solver` config key: dead documentation vs. spec scope**
  - **plugin-engineer claims**: The `solver` config key documented in `optimizer.py` L38-39 is never read, making it "dead documentation" (Rec 2, P2). Users who configure `solver: grid-search` will be silently ignored.
  - **spec-compliance claims**: The spec does not define a `solver` plugin config key. FR-001 says "the optimizer MUST use the AMPL/HiGHS formulation" when available; FR-002 says "MUST fall back to grid search" when unavailable. There is no FR for user-selectable solver override. The docstring in `optimizer.py` documents a feature that goes beyond the spec.
  - **Why this is dangerous**: If plugin-engineer's Rec 2 is implemented, it introduces a feature not covered by the spec. This creates a compliance ambiguity: is the implementation now ahead of the spec, or is the spec incomplete? From a spec-compliance perspective, implementing undocumented features without a spec amendment risks drift between the contract (spec) and the system (code).
  - **Suggested resolution**: Either (a) remove the `solver` config key from the docstring to align with the spec, or (b) amend the spec to add an FR for solver pinning. Option (b) is preferred if solver pinning is genuinely needed for reproducibility, but it requires a spec update, not just a code change. Until the spec is amended, the docstring should not promise features the spec does not define.

### Tensions

- **Error handling unification priority**
  - plugin-engineer rates asymmetric error handling as P1. spec-compliance did not flag this because the external interfaces (FR-011, FR-012) are satisfied regardless of internal error handling conventions. The `solve_with_ampl` / `solve_ampl` asymmetry is an internal API concern that does not affect spec compliance.
  - However, plugin-engineer's point about API usability is valid: a public function (`solve_ampl`, exported in `__init__.py`) with inconsistent error semantics relative to its sibling function is a real usability problem. I accept the finding but consider P2 more appropriate than P1, because it does not affect any FR or SC.

- **`.dat` file support**
  - plugin-engineer recommends `.dat` file support (Missed Opportunities). FR-009 says "Model files MUST be loadable from disk (.mod files) or from string." The spec does not mention `.dat` files. From a compliance perspective, the absence of `.dat` support is not a gap. plugin-engineer correctly notes this "would exceed the spec" -- I confirm that it is not a compliance issue.

- **File detection heuristic**
  - plugin-engineer identifies the `.mod` suffix check as fragile. From a compliance perspective, FR-009 only requires `.mod` file support. The heuristic correctly handles `.mod` files. Support for `.ampl` or `.run` files is not required by the spec. However, the false-positive risk (model strings ending in ".mod") is a real correctness concern that affects FR-009 compliance in edge cases.

### Safe Agreements

- **Plugin interface backward compatibility**: plugin-engineer's Alignment section and spec-compliance's FR-011 analysis both confirm that `PluginResult.data` is non-breaking. The new fields are additive. Both reviews verify this through test references.

- **General-purpose API compliance**: Both reviews confirm FR-007 (API exposed), FR-009 (file and string support), and FR-010 (no licence). plugin-engineer provides deeper API design analysis; spec-compliance provides per-requirement verification. The assessments are complementary and consistent.

- **AMPL resource cleanup**: plugin-engineer explicitly notes the `try/finally` pattern. spec-compliance implicitly validates it through the FR analysis. Both agree cleanup is properly implemented.

- **Naming inconsistencies are low priority**: plugin-engineer flags `cost_per_agent_launch` vs `cost_per_launch` and `solver_timeout` vs `timeout` at P3. These naming differences do not affect any FR or SC. From a compliance perspective, they are irrelevant. From a usability perspective, plugin-engineer's P3 rating is appropriate.

- **NLP/MINLP documentation gap**: plugin-engineer identifies that FR-008's NLP/MINLP claim depends on non-default solvers. spec-compliance rated FR-008 as PASS with a documentation gap note. Both reviews reach the same conclusion through different reasoning.

- **AMPL Community Edition limits**: plugin-engineer recommends documenting the limits (Rec 5, P3). spec-compliance notes this under FR-010. Neither considers it a compliance failure -- FR-010 requires no licence, not unlimited problem size. The documentation gap is real but minor.
