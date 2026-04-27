# Feature Specification: Constitution v2.3.0 Amendment Package

**Feature ID**: `066-constitution-v2.3.0`
**Created**: 2026-04-25
**Status**: Done — implemented as CONSTITUTION.md v2.3.0 (PR #19) and v2.3.1 PATCH (PR #20). Closed 2026-04-27.
**Depends On**: `CONSTITUTION.md` (current v2.2.0), `CONSTITUTIONAL_CONVERSATIONS.md` (governance log)
**Governed by**: `CONSTITUTION.md` Governance section — "MINOR for new principles or material expansions, PATCH for clarifications"
**Originating context**: [`deliberations/constitution-gap-analysis-2026-04-25/`](../../deliberations/constitution-gap-analysis-2026-04-25/) — 4-agent cooperative deliberation, 2 rounds, ~52 launches, arbiter binding rulings on 6 disputes. Governance log entry: 2026-04-25 in `CONSTITUTIONAL_CONVERSATIONS.md`.

> **Scope discipline**: This spec **proposes** the wording of new principles and the version bump. It does NOT commit the edits to `CONSTITUTION.md`. The actual edit lands in a follow-up implementation PR after this spec is reviewed and approved. Two-step keeps the review surface clean — wording disagreements get litigated in this spec; the implementation PR is mechanical.

> **Two-stage discipline**: Stage 1 (4 new principles + 1 extension) addresses unanimous convergence from the deliberation. Stage 2 (3 new principles + extensions) addresses majority convergence. Stages may ship as one v2.3.0 amendment or as v2.3.0 + v2.4.0 — the arbiter ruled comprehensive amendment with staging is acceptable.

---

## 1. Summary

The 2026-04-25 constitutional gap analysis surfaced systematic constitutional debt across 10 PRs merged since v2.2.0 (PRs #4-#14). The arbiter (subject arbitration grounded in `CONSTITUTION.md`, binding influence) ruled on 6 disputes with high confidence on 3 and medium confidence on 3.

This spec operationalizes the arbiter's rulings as concrete principle wording for `CONSTITUTION.md` v2.3.0.

## 2. Goals

1. Codify 4 new constitutional principles addressing distribution, provider robustness, defense-in-depth, and live test cost discipline (Stage 1).
2. Extend Principle IX (Functional Programming and Clean Code) to include behavior-over-shape testing as a general framework that domain-specific tests reference.
3. Codify 3 additional principles for meta-testing, registry-first declaration, and operator configuration (Stage 2).
4. Specify the Sync Impact Report block to drop into `CONSTITUTION.md`'s leading HTML comment.
5. Produce wording specific enough to operationally **catch a future bug**, not just describe the team's preferences.

## 3. Non-goals

- **Editing `CONSTITUTION.md` itself.** That happens in a follow-up implementation PR.
- **Re-litigating arbiter rulings.** This spec accepts the rulings; disagreements with the rulings need a fresh deliberation, not edits here.
- **Templates / specs that depend on the new principles.** Spec 065 (path to open source) v2 amendment is a separate spec edit.

## 4. Stage 1 — Unanimous P1 (must implement)

### 4.1 New Principle XXII — Distribution Surface Integrity

**Proposed text**:
```markdown
### XXII. Distribution Surface Integrity

Every distribution surface (PyPI wheel, .mcpb bundle, Claude Code
plugin, generated SKILL.md) MUST satisfy three invariants:

1. **Single-source versioning**: the version field appears in exactly
   one source — `pyproject.toml` `[project] version`. All other
   surfaces (`desktop-extension/manifest.json`, plugin manifests,
   release artifacts) derive their version from this source at build
   time. Hand-editing a derived version field is prohibited.

2. **Force-include discipline**: any module that is shipped as part
   of a distribution but does not live inside a packaged Python
   directory (e.g., repo-root `mcp_server.py`, `capabilities.py`)
   MUST be explicitly declared in `[tool.hatch.build.targets.wheel.force-include]`
   or the equivalent for the targeted distribution. Implicit inclusion
   via filesystem proximity is prohibited.

3. **End-to-end install testing**: every distribution path MUST be
   tested from a fresh environment in CI (or a documented manual
   test) before tagging a release. "It works in my dev checkout"
   is not sufficient evidence that `pip install` or `.mcpb`
   installation will succeed.

**Rationale (PR evidence)**: PR #11 (mcp_server.py missing from wheel),
PR #13 (manifest.json drifted to 0.1.0 while pyproject was 0.3.0),
plus the in-flight Phase 1 work (manifest tools[] from CAPABILITIES)
all embody this principle. Distribution drift is build-time concern,
not runtime.
```

### 4.2 New Principle XXIII — Provider Robustness Contract

**Proposed text**:
```markdown
### XXIII. Provider Robustness Contract

Every execution provider implementation MUST satisfy four robustness
guarantees:

1. **Token consumption reporting**: every successful provider call
   reports the tokens consumed via `_record_usage` (or the project's
   equivalent telemetry hook). Cost visibility is a contract, not a
   debugging convenience.

2. **Retry-with-jitter for rate limits**: HTTP 429 / equivalent
   rate-limit signals MUST trigger exponential backoff with jitter
   up to a configured maximum attempt count. Bare retry loops without
   jitter are prohibited (synchronized retry storms compound rate
   pressure).

3. **Protocol format tolerance**: parsers MUST tolerate documented
   format variations from upstream APIs (single-object JSON vs JSONL,
   tool-use-only responses without text content, etc.) and treat
   them as success when the underlying response is structurally valid.
   "Empty text content" is not a parse failure if the response carries
   a tool call.

4. **Concurrency respect**: providers MUST respect subscription-level
   concurrency limits. Issuing N concurrent requests to a provider
   that allows N-1 is a contract violation, not a performance choice.

**Rationale (PR evidence)**: PR #5 (claude-code tool-use response),
PR #6 (anthropic 429 retry + concurrency), PR #8 (token tracking),
PR #9 (claude-code single-object JSON parser).
```

### 4.3 New Principle XXIV — Safety-Critical Defense-in-Depth

**Proposed text**:
```markdown
### XXIV. Safety-Critical Defense-in-Depth

Safety-critical paths — defined as **synthesis verdict generation**
(red-blue mode, arbitration rulings, false-PASS / false-FAIL
boundary cases) AND **provider protocol implementation** (rate
limiting, response handling, token reporting) — MUST implement
three-layer defense:

1. **Schema-level required fields**: the data structure declares
   the field as required (Pydantic `Field(...)`, JSON Schema
   `required: [...]`). Missing fields fail at deserialization, not
   at use site.

2. **Parser-level validation**: the parser that converts raw output
   into the typed structure validates field presence and shape
   independently of the schema. Schemas can be bypassed; parsers
   cannot.

3. **Contract test reproducing the failure scenario**: every
   safety-critical path has at least one test that **reproduces
   the original bug or failure pattern** the principle was created
   to prevent. The test asserts the bug does not recur.

The arbiter's binding ruling explicitly extended this scope to
provider protocols (not just synthesis logic) on the evidence that
PRs #5, #6, #8, #9 produced the same class of silent failure as
PR #10's false-PASS bug.

**Rationale (PR evidence)**: PR #10 (red-blue contract break →
false-PASS); generalized over PRs #5, #6, #8, #9.
```

### 4.4 New Principle XXV — Live Test Cost Discipline

**Proposed text**:
```markdown
### XXV. Live Test Cost Discipline

Tests that consume API credits, spawn subprocesses, or otherwise
incur real-world cost MUST follow three discipline rules:

1. **Explicit marker**: `@pytest.mark.live` (or the project's
   equivalent) on every test that incurs cost. Unmarked tests are
   assumed free; introducing cost into an unmarked test is a
   contract violation.

2. **Cost justification in docstring**: every `@pytest.mark.live`
   test has a docstring stating *what the test exercises that
   cannot be tested cheaply*. "Tests that the provider actually
   works" is not sufficient — the cost must buy something specific
   the mock provider can't.

3. **CI opt-out by default**: CI runs `pytest -m "not live"` by
   default. Live tests run in a separate, manually-triggered job
   gated behind a maintainer-supplied secret. PRs do not pay live
   test costs; only releases do (or scheduled smoke runs).

4. **Test category taxonomy**: the permitted markers for
   cost-bearing tests are `live` (consumes API credits or
   subprocess spawning), `integration` (multi-component but
   in-process), and `security` (path traversal, injection, input
   validation surfaces). Adding a new top-level marker requires a
   constitutional amendment — the taxonomy is the contract.

**Interaction with Principle XXII (Distribution Surface Integrity)**:
XXII's end-to-end install testing requirement (G9 in spec 065)
runs in CI. Install tests that incur measurable cost (downloading
wheels, spawning isolated environments) MUST be marked
`@pytest.mark.live` and run under the gated job. Install tests that
run in-process (e.g., `importlib.reload` against a built wheel)
are not live and run on every PR.

This principle is **foundational** for Principle XXIII (Provider
Robustness Contract) — provider contract tests are inherently live.
Without cost discipline, provider testing becomes prohibitively
expensive and the robustness contract goes untested.

**Rationale (PR evidence)**: PR #8 introduced `@pytest.mark.live`
without codifying the discipline. The deliberation arbiter ruled
this principle must precede provider contract testing requirements.
```

### 4.5 Extension to Principle IX — Behavior-Over-Shape Testing

**Proposed addition** (appended to existing Principle IX):
```markdown
**Extension (v2.3.0): Behavior-over-shape testing.**

Tests MUST assert behavioral properties (what the code *does*) rather
than structural properties (what fields are populated, what classes
exist). Domain-specific testing requirements — distribution
validation, provider robustness, synthesis correctness — reference
this general framework rather than introducing parallel "behavioral
validation" requirements per domain.

A test that verifies `result.foo == 9` without verifying that the 9
actually represents the right behavior is a shape test, not a
behavior test. Shape tests pass when the bug is structurally invisible
(field is set to a wrong-but-valid value); behavior tests catch
the bug.

**Operational test**: an assertion that checks only field presence,
type, or non-null status WITHOUT also constraining the value's
*meaning* is a shape test. Examples of shape tests (prohibited
on their own): `assert "headline" in result`, `assert
isinstance(rounds_completed, int)`, `assert len(errors) >= 0`.
Examples of behavior tests (required): `assert result["headline"]
== expected_headline`, `assert rounds_completed == 2 because the
config requested 2 rounds`, `assert errors == []` (when zero is
the expected behavioral state). Shape tests are permitted only as
preconditions inside a test that ALSO asserts behavior.
```

## 5. Stage 2 — Majority P2 (should implement)

### 5.1 New Principle XXVI — Meta-Testing for Parametrized Capabilities

**Proposed text**:
```markdown
### XXVI. Meta-Testing for Parametrized Capabilities

Any test file that exercises a parametrized set of capabilities
(MCP prompts, MCP tools, registered providers, plugin skills, etc.)
MUST include a **meta-test** that asserts the parametrize lists
cover the full set. Adding a new capability without updating the
parametrize list trips the meta-test.

This is foundational testing infrastructure: it prevents silent
coverage gaps as the system grows. The trigger is mechanical, not
discretionary — any test module that uses `@pytest.mark.parametrize`
to enumerate a *capability set* (MCP tools, MCP prompts, providers,
plugin skills, registered modes, registry entry points) MUST also
include a meta-test asserting the parametrize list has the same
length as the authoritative capability source. Modules that
parametrize over arbitrary values (e.g., `[None, 0, 1, "x"]` for
input validation) are out of scope — meta-testing applies only to
parametrized capability *sets*.

A coverage-drift guard converts an easy mistake ("forgot to add
the new tool to the test list") into a CI failure with a specific
message ("Expected 8 prompts, parametrize covers 7: deliberate,
challenge, force_decision, design_deliberation, analyze_documents,
review_config, check_cost — new prompt 'estimate_complexity'
missing").

**Rationale (PR evidence)**: PR #12 introduced the meta-test pattern
for `@mcp.prompt()` definitions. The deliberation ruled this pattern
should generalize to all parametrized capability sets.
```

### 5.2 Extension to Principle XI — Registry-First Declaration

**Proposed addition** (appended to existing Principle XI):
```markdown
**Extension (v2.3.0): Registry-First Declaration.**

The capability registry (`capabilities.py` + `conversus/registry/`)
is the **single authoritative source** for tool, prompt, and
plugin-skill availability across all distribution surfaces. Hand-
written tool decorations, manifest entries, or plugin SKILL.md
files that conflict with the registry are violations of single-
source-of-truth, not parallel declarations.

Surface artifacts that today carry hand-written tool/prompt entries
(`mcp_server.py` `@mcp.tool()` decorators, `manifest.json` `tools[]`
array, `claude-code-plugin/skills/*/SKILL.md`) are **migration
targets**. Until projection is complete, hand-written and projected
declarations MUST agree — drift is detected by parity tests, not
silently accepted.

**Rationale (PR evidence)**: PR #4 (spec 064.1 runtime registration)
and the in-flight Phase 1 manifest tools[] projection both assume
the registry is authoritative. This extension codifies that
assumption.
```

### 5.3 New Principle XXVII — Operator-Configurable Tool Surface

**Proposed text**:
```markdown
### XXVII. Operator-Configurable Tool Surface

The tool surface exposed by a deployed conversus instance MUST be
configurable by the **operator** (the person installing or running
the server) without source code changes. Configuration channels are:

- **Environment variables** (e.g., `CONVERSUS_DISABLED_TOOLS`)
- **Manifest `user_config` entries** for Desktop Extension installs
- **CLI flags** for ad-hoc invocations

Operators MAY restrict the available tool surface (hide tools they
don't want exposed). They MAY NOT extend it (operators do not add
tools — that's the registry's job). This asymmetry preserves
deterministic capability discovery while allowing deployment-time
hardening.

**Coordination with Principle XV (Plugin Isolation)**: Principle XV
governs how plugins **add** capabilities; Principle XXVII governs
how operators **subtract** capabilities. The two are complementary:
plugins extend the registry; operators filter the registered set.
Neither modifies core deliberation behavior.

**Rationale (PR evidence)**: PR #14 (CONVERSUS_DISABLED_TOOLS).
The arbiter ruled this should be a **standalone principle** (not
a Principle XV extension) because operator configuration scope
extends beyond plugin isolation to the core tool surface.
```

### 5.4 Stage 2 batch — supporting clarifications

Bundled together as PATCH-level clarifications inside existing
principles, since each is a refinement rather than a new principle:

- **Principle XXIII clarification**: "Retry-with-jitter" specified
  with a default formula (exponential backoff, jitter ±25%, max 5
  attempts) as a normative reference. Implementations may diverge
  with documented justification.

- **Principle XXIII clarification**: "Token consumption transparency"
  specified to require both prompt and completion tokens reported
  separately, not aggregate.

- **Principle XXIII clarification**: "Protocol tolerance" specified
  to require a documented allow-list of tolerated format variations
  in each provider's source — silent tolerance is prohibited.

- **Principle XXIV clarification**: "Contract test" specified to
  require a comment in the test body referencing the original PR
  or issue that documented the failure pattern. This forms the
  test-to-bug-history audit trail.

- (Test category taxonomy moved to Principle XXV.4 — it belongs
  with cost discipline, not meta-testing for parametrized
  capabilities.)

## 6. Sync Impact Report (proposed)

To be inserted at the top of `CONSTITUTION.md` replacing the v2.2.0
report:

```markdown
<!--
Sync Impact Report
Version change: 2.2.0 → 2.3.0 (MINOR — 6 new principles + 2 extensions for
constitutional gaps surfaced by 2026-04-25 deliberation)
Added principles:
  - XXII. Distribution Surface Integrity
  - XXIII. Provider Robustness Contract
  - XXIV. Safety-Critical Defense-in-Depth
  - XXV. Live Test Cost Discipline
  - XXVI. Meta-Testing for Parametrized Capabilities
  - XXVII. Operator-Configurable Tool Surface
Modified principles:
  - IX. Functional Programming and Clean Code — extended to include
    behavior-over-shape testing as general framework
  - XI. Single Source of Truth — extended for Registry-First Declaration
Removed sections: none
Templates requiring updates:
  - .specify/templates/plan-template.md — verify new principles do not
    break existing template assumptions
  - .specify/templates/spec-template.md — same
  - .specify/templates/tasks-template.md — same
Follow-up TODOs:
  - Spec 065 (path to open source) v2 amendment to reference Distribution
    Surface Integrity in gates G2/G9 and Provider Robustness in G5/G6
  - Phase 1 (manifest tools[] from CAPABILITIES) ships under Distribution
    Surface Integrity umbrella
Rationale: 2026-04-25 4-agent cooperative deliberation, 2 rounds, ~52
launches. Arbiter (subject arbitration, binding) ruled on 6 disputes.
Unanimous convergence on 4 P1 principles + Principle IX extension;
majority convergence on 3 additional P2 principles + Principle XI
extension. Full deliberation record:
deliberations/constitution-gap-analysis-2026-04-25/.
Governance log entry: 2026-04-25 in CONSTITUTIONAL_CONVERSATIONS.md.
-->
```

## 7. Verification — re-run constitution arbitration

> **SUPERSEDED 2026-04-26**: this section's single-deliberation protocol is replaced by spec 067 (`Constitutional Verification Methodology — Both Self-Consistency AND Blind`). See spec 067 §4 for the canonical protocol — both methodologies are now required for every constitutional amendment. The original §7 text below is preserved for audit context.

### 7-original (historical)

Before merging the implementation PR (the actual `CONSTITUTION.md`
edit), run a follow-up deliberation against the **proposed amended
text** with the same arbiter pattern (`grounding: CONSTITUTION.md`,
binding influence, but pointing at the candidate v2.3.0 file).

The arbiter today grounded its rulings in v2.2.0. The amendment
package should pass arbitration against itself — i.e., the new
principles should not contradict each other or violate the existing
ones.

This is not a formality. It catches:
- Wording drift (the spec writes "must" but principle wording uses
  "should")
- Scope creep (the spec proposes Principle XXII but the implementation
  PR slipped in a fifth bullet not in the spec)
- Inter-principle conflicts (e.g., a new principle that contradicts
  an existing one)

**Acceptance criterion for verification**: 0 disputes raised by
arbitration against the v2.3.0 candidate text.

## 8. Open questions

- **Q1**: Single-stage v2.3.0 or two-stage v2.3.0 + v2.4.0?
  Arbiter accepted comprehensive amendment with staging. Recommend
  single-stage v2.3.0 unless review surfaces wording disagreements
  that would split the amendment.

- **Q2**: Should the verification deliberation (§7) run before this
  spec merges, or before the implementation PR? Recommend before
  the implementation PR — the spec is the proposal, the implementation
  is the change requiring re-arbitration.

- **Q3**: Templates referenced in §6 (Sync Impact Report) — do
  `.specify/templates/*` exist in this repo? If not, the line
  should be removed or amended.

## 9. References

- `CONSTITUTION.md` (current v2.2.0)
- `CONSTITUTIONAL_CONVERSATIONS.md` — entry: 2026-04-25
- `deliberations/constitution-gap-analysis-2026-04-25/`
  - `summary/final.md` — cross-round synthesis
  - `round-2/arbiter/resolution.md` — final binding rulings
- PRs informing this amendment: #4, #5, #6, #8, #9, #10, #11, #12, #13, #14
- Spec 052 (open source extraction)
- Spec 064 (capability discovery)
- Spec 065 (path to open source) — to be amended in v2

## 10. Acceptance criteria for this spec

The spec itself is "done" when:

1. Each proposed principle has wording that survives review without
   substantive rewording.
2. The Sync Impact Report block (§6) is reviewed and approved.
3. Open questions Q1-Q3 in §8 are resolved.
4. The verification deliberation (§7) is queued or completed.
5. A follow-up implementation PR is filed editing `CONSTITUTION.md`
   to v2.3.0.

## Closure note (2026-04-27)

**Implementation**:
- PR #19 — `feat(constitution): v2.2.0 → v2.3.0 — amendment package`
- PR #20 — `fix(constitution): v2.3.0 → v2.3.1 PATCH` (clarification follow-up)

**Verification**:
- Self-consistency: `deliberations/v2.3.0-verification-2026-04-25/`
- Blind: `deliberations/v2.3.0-blind-verification-2026-04-25/`

**Governance log**: 2026-04-25 self-consistency entry + 2026-04-25 blind entry in `CONSTITUTIONAL_CONVERSATIONS.md`.

The v2.3.0 amendment package shipped after both verifications. The blind verification surfaced two follow-on findings — finding #2 (Principle XVI logical contradiction, addressed by spec 068 / PR #29 as v2.3.2 PATCH) and finding #3 (mechanical verification gate, addressed by spec 069 / PR #32 as v2.4.0 MINOR). PR #20 (v2.3.1 PATCH) folded in additional clarifications surfaced post-merge. The 2026-04-27 post-v2.4.0 gap analysis flagged that re-verification was not run after fixes were folded in — this implementation is grandfathered; spec 067 v2 amendment (PR #35) addresses re-verification for future amendments.
