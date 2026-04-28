# Remaining Production Gaps (2026-04-28)

These 3 test failures were surfaced by PR #42 and **deliberately not fixed**
because doing so would have weakened the test assertions in violation of
Principle XXVIII (proposed in spec 071). Each represents a real production
gap in error-path handling.

All three live in `linter/test_mcp_server.py` and exercise the public MCP
surface (`_run_config` / `_decide`). Each asserts that an *invalid input*
should surface a clear error to the caller; production currently lets the
pipeline run silently (mock provider, invalid mode validation skipped) and
returns a "successful" result instead.

## Failure 1 — `test_run_in_process_unsupported_provider`

**Location**: `linter/test_mcp_server.py:595` (mirrored at
`desktop-extension/server/lib/linter/test_mcp_server.py:594`).

**What it asserts**:
```python
result = _run_config(config_yaml=config_yaml, provider="gemini")
assert result.mode == "in_process"
assert any("Unknown provider" in e for e in result.errors)
assert result.output is None
```

**What production code is doing wrong**: `_run_config` accepts an
unrecognized provider name (`"gemini"`) and proceeds to execute the
pipeline anyway — producing an `output` and an empty `errors` list. The
provider resolver at the in-process entry point does not validate the
provider name against the registered set before launching the deliberation,
so callers requesting a provider that doesn't exist get a silently-degraded
mock run instead of a hard error.

## Failure 2 — `test_decide_invalid_provider`

**Location**: `linter/test_mcp_server.py:744` (mirrored at
`desktop-extension/server/lib/linter/test_mcp_server.py:743`).

**What it asserts**:
```python
result = _decide(SUFFICIENT_QUESTION, provider="gemini")
assert result.sufficient is True               # question classifier passes
assert len(result.errors) > 0                  # but provider resolution fails
assert any("provider" in e.lower() or "unknown" in e.lower() for e in result.errors)
assert result.output is None
```

**What production code is doing wrong**: Same root cause as Failure 1, on
the `_decide` code path. The question classifier correctly accepts the
question, but provider resolution then falls through to the mock provider
without raising. The caller's request for `provider="gemini"` is silently
remapped (or ignored) and the deliberation runs to completion with an
output, masking what should be an obvious configuration error.

## Failure 3 — `test_decide_mode_parameter`

**Location**: `linter/test_mcp_server.py:793` (mirrored at
`desktop-extension/server/lib/linter/test_mcp_server.py:792`).

**What it asserts**:
```python
result = _decide(SUFFICIENT_QUESTION, provider="mock", mode="red-blue")
assert result.sufficient is True               # question passes classification
assert len(result.errors) > 0
assert any("red" in e.lower() for e in result.errors)   # config validator
                                                        # should reject
                                                        # missing role:red/blue
assert result.output is None
```

**What production code is doing wrong**: `_decide` uses the
pragmatist + devils-advocate preset agents, which lack the
`role:red` / `role:blue` tags that `red-blue` mode requires. Production
should plumb the `mode` parameter through to config validation and raise
a clear "red-blue mode requires agents tagged role:red and role:blue"
error. Currently the validator either is not invoked, or the role
constraint is not checked, and the pipeline runs to a "successful" output
under a mode whose preconditions are violated.

## Recommended follow-up

**Shape: a single focused bug-fix PR**, not a spec or three issues. The
three failures share one root cause family — the in-process MCP entry
points (`_run_config`, `_decide`) accept caller parameters (`provider`,
`mode`) without revalidating them against the registered set / mode
preconditions before launching the pipeline. A single PR titled along the
lines of `fix(mcp): surface errors for invalid provider/mode instead of
silent run` can land all three fixes together with a small, coherent diff:

1. In the in-process resolver, lookup the provider name against the
   registered providers and raise / append an error string before the
   pipeline starts.
2. In `_decide`, plumb `mode` through to config validation and check
   role-tag preconditions for modes that require them (`red-blue`,
   `prisoners-dilemma` likely have similar invariants worth auditing).
3. Re-enable the three tests as the verification for the fix; do not
   weaken their assertions.

A spec is not warranted — the scope is narrow, the asserted behavior is
already documented by the tests, and the deliberation in spec 045 already
identified error-path coverage as a recurring weakness. Issues are not
warranted either — there is no need to triage; the work is small enough
to be one PR.
