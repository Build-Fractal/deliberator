# Feature Specification: Engine & Linter Test Coverage Review

**Feature ID**: `045-test-coverage-review`
**Created**: 2026-04-04
**Status**: Draft
**Depends On**: Test coverage baseline established via 3-agent parallel test writing (engine core, engine phases/config/templates, linter modules)
**Docs Update**: None — internal quality work
**Origin**: Coverage audit revealed engine/ and linter/ at ~30% average. The conversus package is 80-90% covered but the runtime layer that actually executes deliberations is nearly untested.

---

## 1. Problem

After the Wave 1-3 work, total project coverage sits at **56.37%** — but the distribution is inverted from where it should be:

- **Well tested** (80-95%): `conversus/schemas/*`, `conversus/plugins/nashopt/*`, `conversus/domains/*`, `conversus/paths.py`
- **Nearly untested** (0-25%): `engine/phases.py` (10%), `engine/config.py` (18%), `engine/auth.py` (20%), `engine/templates.py` (20%), `engine/cli/__init__.py` (24%), `linter/quality.py` (24%)
- **Zero coverage**: `engine/errors.py`, `engine/models.py`, `engine/_root.py`, `engine/run.py`, `engine/adhoc.py`, `engine/providers/*`, `linter/validate.py`, `linter/usage.py`, `web/*`

The testable *pure logic* has tests. The *orchestration layer* — phases, config parsing, template resolution, validation — does not. This is backwards: the code that actually runs conversus is the code most at risk of regression.

## 2. Goal

**90% line coverage on `engine/` and `linter/` modules**, with tests that assert **behavior**, not just exercise code paths.

### Behavioral assertion requirement

Every test MUST verify that the function under test produces a specific observable outcome for a specific input. Coverage-bumping "smoke tests" that call a function with mock data and assert nothing meaningful are forbidden. Examples:

**Bad (smoke test):**
```python
def test_parse_config():
    config = parse_config(tmp_path / "conversus.yml")
    assert config is not None  # meaningless
```

**Good (behavioral):**
```python
def test_parse_config_rejects_invalid_mode():
    yml = tmp_path / "conversus.yml"
    yml.write_text("mode: invalid-mode\nagents: [...]")
    with pytest.raises(ConfigError, match="invalid mode"):
        parse_config(yml)

def test_parse_config_resolves_preset_docs():
    yml = tmp_path / "conversus.yml"
    yml.write_text("mode: cooperative\nagents: [{preset: mechanist, name: a1}, ...]")
    config = parse_config(yml)
    assert config.agents[0].docs == ["presets/philosophy/mechanist/docs/..."]
```

## 3. Review Agents

This review runs as a cooperative conversus deliberation with **3 agents and a chief architect arbiter**. The agents each evaluate the test suite from a different expertise angle; the arbiter issues binding decisions when they disagree.

### Agent 1: functional-programming-guru

**Identity:** A functional programming and typing expert. Evaluates tests against the principles of pure function design, type safety, referential transparency, and composability.

**Evaluates:**
- Are tests testing **pure functions** where possible? Impure tests (filesystem, network) should be isolated to explicit integration-style tests.
- Do tests leverage **type information**? Pydantic model tests should verify field constraints AND type coercion behavior.
- Are tests **composable**? Can fixtures be reused across test files without implicit coupling?
- Do tests avoid **hidden state**? Each test should be runnable in any order, with no shared mutable state.
- Are **types used correctly** in the code under test? Flags places where `Any`, untyped dicts, or string-typed enums weaken the type system.
- Does the code under test **return meaningful types**? Functions that return `None` when they should return `Result[T, Error]` are flagged.

**Docs to read:**
- `conversus/schemas/` — reference for well-typed pure-function code
- `tests/test_payoffs.py` — reference for well-structured unit tests

### Agent 2: sdet-agent

**Identity:** A Software Development Engineer in Test. Evaluates tests from a QA and testing discipline perspective.

**Evaluates:**
- **Behavioral assertions:** Does every test assert a specific observable outcome? Or are some tests just calling functions without meaningful assertions?
- **Edge cases:** Are boundary conditions tested (empty input, max input, invalid types, unicode, very long strings)?
- **Error paths:** Are error cases tested with `pytest.raises(SpecificException, match="...")`? Are exception messages asserted?
- **Parametrization:** Are tests that iterate over similar cases using `@pytest.mark.parametrize` instead of loops?
- **Coverage quality:** Does 90% line coverage translate to 90% branch coverage? Are conditional branches all exercised?
- **Test isolation:** Do any tests depend on execution order, shared state, environment variables, or filesystem state that persists between runs?
- **Mocking discipline:** Are mocks used appropriately? Is `unittest.mock` used where it should be, and not where real objects work?
- **Test naming:** Do test names describe the behavior being verified, not just the function being called?

**Docs to read:**
- `tests/test_package_split.py` — well-structured integration tests using `sys.modules` snapshots
- `tests/test_nashopt.py` — reference for behavioral assertions on scoring

### Arbiter: chief-architect

**Identity:** The chief architect of conversus. Has final authority on whether the test suite meets the project's quality bar. Grounded in the project's existing principles (Principle XV: Plugin Isolation, the three-tier fallback architecture, the free/paid boundary).

**Role:** When the functional-programming-guru and sdet-agent disagree on a test design, the architect decides. The architect also enforces:
- **Architectural consistency:** Tests must reflect the layered architecture (engine → linter → conversus package). Tests at the wrong layer are rejected.
- **Monotonic quality:** The test suite must never get worse. If a test is removed, it must be replaced with something stronger.
- **Free vs paid:** Tests for paid-tier code (nashopt, optimizer) stay in place. Tests for free-tier code (engine, linter) get the 90% push.
- **No shortcuts:** Fake tests that exist only to bump coverage are rejected. If a code path cannot be meaningfully tested, the architect requires either refactoring the code or explicitly documenting why.

**Grounding:** `conversus.example.yml` and the existing `conversus/` codebase as the source of truth for architecture decisions.

**Trigger:** `disputes_remain` — arbiter only fires if the two reviewers can't reach consensus on test quality issues.

**Influence:** `binding` — the architect's rulings are final.

## 4. Review Process

The review runs AFTER the 3 test-writing agents complete their work and push coverage to ~90% on engine/ and linter/.

### Inputs (targets)

- `tests/test_engine_core.py` (from Agent 1 — errors, models, _root, cost, events)
- `tests/test_engine_phases.py` (from Agent 2 — phase orchestration)
- `tests/test_engine_config.py` (from Agent 2 — config parsing)
- `tests/test_engine_templates.py` (from Agent 2 — template resolution)
- `tests/test_linter_validate.py` (from Agent 3 — schema validator)
- `tests/test_linter_usage.py` (from Agent 3 — usage tracker)
- `tests/test_linter_quality.py` (from Agent 3 — quality linter)
- `tests/test_linter_classifier.py` (from Agent 3 — question classifier)
- `tests/test_linter_output_contract.py` (from Agent 3 — output contract)

### Source code agents reference

- `engine/phases.py`, `engine/config.py`, `engine/templates.py`, `engine/errors.py`, `engine/models.py`, `engine/_root.py`, `engine/cost.py`, `engine/events.py`
- `linter/validate.py`, `linter/usage.py`, `linter/quality.py`, `linter/question_classifier.py`, `linter/output_contract.py`

### Output

- `specs/045-test-coverage-review/conversus-output/summary/final.md` — cross-agent synthesis
- `specs/045-test-coverage-review/conversus-output/arbitration/resolution.md` — arbiter rulings (if disputes remain)
- `specs/045-test-coverage-review/conversus-output/{agent}/` — per-agent reviews, cross-reviews, revisions, disputes

## 5. Success Criteria

- **SC-001:** Both reviewer agents independently verify that every test in the new test files asserts behavior, not just executes code
- **SC-002:** The functional-programming-guru identifies any code under test that has weak typing, and documents specific refactoring recommendations
- **SC-003:** The sdet-agent identifies any gaps in edge case or error path coverage
- **SC-004:** Line coverage on engine/ and linter/ reaches 90% measured by `pytest --cov`
- **SC-005:** Branch coverage reaches at least 80% (discoverable via `--cov-branch`)
- **SC-006:** All new tests pass in isolation (order-independent, no shared state)
- **SC-007:** The arbiter (chief architect) confirms the test suite meets the project's quality bar

## 6. Constraints

- No modifications to source files during the review phase — reviewers comment, don't patch
- Any source code changes recommended by the review become follow-up work, tracked separately
- The review must complete in a single 3-agent deliberation (not dragged across multiple runs)
- Bugs discovered in existing source code are documented in the synthesis but not fixed within this spec
