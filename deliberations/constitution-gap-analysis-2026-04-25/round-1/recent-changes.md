# Recent Changes Since Constitution v2.2.0

The last constitution bump (v2.2.0) added 5 principles for SKILL.md
decomposition. Since then, 10 PRs have merged. Each is summarized
below with the unwritten invariant it embodies — the question for
this deliberation is which of those invariants belong in CONSTITUTION.md.

---

## #4 — Spec 064.1: runtime registration of discovered capabilities

Adds `register_discovered_mcp_tools(mcp)` and
`register_discovered_cli_commands(cli)`. Walks
`collect_capabilities()`, filters by `Surface.MCP` / `Surface.CLI`,
and registers each via FastMCP `add_tool` or click `add_command`.
Paid wheels (`conversus-enhanced`) advertise capabilities via
setuptools entry points — the OSS engine discovers them at runtime.

**Unwritten invariant**: third-party packages can extend conversus
through the entry-point group `conversus.solvers` / `conversus.domains`
without modifying core. The registry is the contract.

## #5 — claude-code: tool-use response treated as success

When the claude-code CLI returns a tool-use-only response (no text),
the provider used to error. Now it succeeds with the tool-use
content as the deliberation message.

**Unwritten invariant**: provider parsers must not treat structurally-valid
but text-empty responses as failures. Tool calls are first-class output.

## #6 — anthropic: OAuth concurrency + 429 retry

Anthropic provider now respects subscription concurrency limits and
retries 429 responses with jitter (exponential backoff up to N
attempts).

**Unwritten invariant**: providers MUST handle rate limits gracefully
without losing deliberation state. Retry-with-jitter is the
expected pattern; concurrency must be respected per subscription tier.

## #8 — token tracking across all providers + live integration tests

Wires `_record_usage` into every provider's response path. Per-call
token consumption is now visible. Adds live integration tests that
exercise real subprocesses and may cost API credits (marked
`@pytest.mark.live`).

**Unwritten invariant**: every provider must report tokens consumed.
Live integration tests are a permitted test category, gated behind
a `live` marker so CI can opt out.

## #9 — claude-code: single-object JSON parser fix

The current claude CLI emits a single JSON object instead of
JSONL. Parser now handles both formats.

**Unwritten invariant**: parsers must be robust to upstream protocol
shifts. CLI versions are not pinned; conversus must adapt.

## #10 — red-blue: three-layer contract break (false-PASS on dangerous deliberations)

Red-blue mode synthesis was returning PASS on deliberations where
the red team raised unanswered safety concerns. Three-layer fix:
schema-level required fields, parser-level validation, contract
test that reproduces the false-PASS scenario.

**Unwritten invariant**: synthesis verdicts must be structurally
auditable. Schema → parser → contract test is the defense-in-depth
pattern. (NB: this is exactly the kind of bug a constitutional
"safety-critical default" principle would have caught in design.)

## #11 — packaging: force-include mcp_server.py + capabilities.py in wheel

Hatchling wheel was missing two repo-root files. Without them,
`pip install conversus[mcp]` shipped a broken `conversus mcp` CLI.

**Unwritten invariant**: every distribution path must be tested
end-to-end. Wheel contents are not implicit — explicit force-include
is required for non-package modules.

## #12 — test coverage for 7 @mcp.prompt() definitions

Prompts had zero unit coverage. New file
`linter/test_mcp_prompts.py` covers return shape, parameter
embedding, mode hints, role-split pattern (spec 060), tool
references, and determinism. Includes a meta-test that asserts
coverage of all 7 prompts (drift guard for new prompts).

**Unwritten invariant**: prompts and tools have equal testing
expectations. Adding a new `@mcp.prompt()` requires adding test
coverage; the meta-test enforces this.

## #13 — manifest.json version sync from pyproject.toml

Desktop bundle's manifest had drifted to 0.1.0 while pyproject was
at 0.3.0. Build-time projector now reads pyproject's `[project]
version` and writes it into manifest.json before zip. Mirrored in
local `build.sh` for parity with CI.

**Unwritten invariant**: version is single-sourced from
`pyproject.toml`. Surface artifacts that carry a version field
(manifest.json, plugin.json, etc.) are projected, not hand-edited.
Distribution drift is a build-time concern, not a runtime one.

## #14 — CONVERSUS_DISABLED_TOOLS env var to hide tools

`mcp_server.py` reads `CONVERSUS_DISABLED_TOOLS` at module load
and skips registering listed tools. Lets operators (Claude Desktop
user_config, MCP launcher env, CI bundles) restrict the tool
surface without forking the server. Filter currently applies only
to the 4 hand-coded tools; runtime-discovered tools are out of scope.

**Unwritten invariant**: deployment-time tool surface is
configurable without code changes. User_config in
`desktop-extension/manifest.json` is the canonical configuration
contract for Desktop installs.

---

## Cross-cutting themes that may warrant new principles

1. **Capability registry as the cross-surface contract** — #4, #14,
   and the in-flight Phase 1 (manifest tools[] from CAPABILITIES)
   all assume the registry is the canonical declaration. Should
   "registry-first declaration" be a principle?

2. **Distribution surface invariants** — #11, #13, and the .mcpb
   pipeline all touched the wheel + bundle path. The constitution
   has nothing on packaging. Should "distribution-surface integrity"
   be a principle (single-source versioning, force-include
   discipline, end-to-end install testing)?

3. **Provider robustness pattern** — #5, #6, #8, #9 all hardened
   provider edge cases (text-empty, 429s, JSON shape, token
   tracking). The constitution mentions provider-agnostic execution
   but not the robustness expectations. Should "provider robustness
   contract" (token reporting, retry semantics, format-shift
   tolerance, structurally-valid response handling) be a principle?

4. **Drift guard testing** — #12 introduced a meta-test asserting
   the file covers all 7 prompts. The DISABLED_TOOLS PR also has
   a parametrized test exercising the integration path. Should
   "drift guard tests for parametrized surfaces" be a principle?

5. **Operator-configurable tool surface** — #14 gives operators the
   ability to hide tools without forking. Should
   "operator-runtime tool surface configurability" be a principle?

6. **Schema → parser → contract defense-in-depth** — #10's red-blue
   fix was a textbook three-layer defense. The constitution
   mentions "stable interfaces" but not the layered-defense pattern.
   Should this be a principle?

7. **Prompts as first-class capabilities** — the registry models
   tools but not prompts; #12 added prompt tests but the registry
   has no prompt type. Future Phase 3 of MCP projection blocked on
   this. Should "prompts as first-class registry entities" be a
   principle, or stay deferred?

These themes are the deliberation seed. Agents should evaluate each
on its merits and surface ones I missed.
