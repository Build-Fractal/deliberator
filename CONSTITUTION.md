<!--
Sync Impact Report
Version change: 2.3.0 → 2.3.1 (PATCH — Principle XV clarification:
registry as extension interface, completes blind-verification finding
#1 whose XXVII half landed in 2.3.0)
Added principles: none
Modified principles:
  - XV. Plugin Isolation — added "Clarification (v2.3.1): registry as
    the extension interface" sub-section coordinating with XXVII
Removed sections: none
Templates requiring updates: none
Rationale: 2026-04-25 blind verification deliberation (3 agents, no
v2.3.0 markers visible to agents) recommended both XV and XXVII be
clarified as defining the registry as the architectural extension
boundary. XXVII received its half in 2.3.0 (PR #19); this PATCH adds
the parallel XV clarification. Governance log entry: 2026-04-25 in
CONSTITUTIONAL_CONVERSATIONS.md (blind verification entry, fix #1
remainder).
Prior amendment (v2.2.0 → 2.3.0): see git history for the 6 new
principles + 2 extensions added on 2026-04-25.
-->

<!--
Sync Impact Report (prior — preserved for audit trail)
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
  - none in this repo (.specify/templates/* referenced in prior reports
    do not exist here; the line is dropped per spec 066 §8 Q3)
Follow-up TODOs:
  - Spec 065 (path to open source) v2 references the new principles in
    gates G2/G5/G6/G9 — ✅ already amended in PR #15
  - Run a verification deliberation against this amended text to catch
    inter-principle conflicts (per spec 066 §7); 0 disputes is the
    acceptance bar before this PR merges
  - Phase 1 (manifest tools[] from CAPABILITIES) operationalizes
    Principle XXII — PR #18, awaiting CI
Rationale: 2026-04-25 4-agent cooperative deliberation, 2 rounds, ~52
launches. Arbiter (subject arbitration, binding) ruled on 6 disputes.
Unanimous convergence on 4 P1 principles + Principle IX extension;
majority convergence on 3 additional P2 principles + Principle XI
extension. Full deliberation record:
deliberations/constitution-gap-analysis-2026-04-25/. Spec 066 proposed
the wording; this PR applies it. Governance log entry: 2026-04-25 in
CONSTITUTIONAL_CONVERSATIONS.md.
Prior amendment (v2.1.0 → 2.2.0): see git history for the SKILL.md
decomposition principles (XVII-XXI) added on 2026-03-22.
-->

# Conversus Constitution

## Core Principles

### I. Spec-Driven Development

Every behavioral change MUST start with a specification. SKILL.md is
the executable truth — the agent runtime consumes it directly as
orchestration instructions. Changes to SKILL.md ARE behavioral changes.

- New features require a spec in `specs/{NNN}-{name}/spec.md` before
  any SKILL.md edits.
- Specs define WHAT and WHY. Implementation plans define HOW.
- The speckit pipeline (`specify → clarify → plan → tasks → implement`)
  is the standard workflow. Skipping phases is permitted only for
  trivial changes (single-line documentation fixes).

### II. Stable Interfaces

Structural markers, template variables, the dispute-parsing subsystem,
the preset schema, reference file paths, and the dispatch table are
stable contracts. Breaking changes MUST be coordinated across all
consumers.

- `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->`
  markers, mode-specific dispute headings, and `{VARIABLE}` template
  syntax are stable interfaces documented in SKILL.md.
- The dispatch table subcommand names (`run`, `define`, `interests`,
  `mode`, `converge`, `arbitrate`, `gate`) are stable interfaces.
  Adding a new subcommand is not breaking. Renaming or removing one IS.
- Reference file paths referenced by SKILL.md load triggers are stable
  interfaces. Adding a new reference file is not breaking. Renaming or
  moving a reference file IS breaking for any SKILL.md load trigger
  that references it.
- Template variable names in `schema/variables.yml` and the
  `conversus.yml` config schema are stable interfaces.
- Changing a stable interface requires updating every consumer (specs,
  templates, SKILL.md sections, reference files) in a single atomic
  change.
- New interfaces SHOULD be marked stable only after at least one spec
  has consumed them successfully.

### III. Backward-Compatible Extension

New features MUST extend existing behavior rather than restructuring it.
Omitting optional fields MUST preserve existing behavior exactly.

- The `preset:`, `rounds:`, `stagnation:`, `arbiter:`, and `iterations:`
  fields are all optional. Omitting any of them produces identical
  behavior to the pre-feature baseline.
- New SKILL.md sections are additive. Existing sections are modified
  only to add cross-references or refine documentation.
- Phase numbering (1-6) is fixed. New orchestration capabilities are
  added as conditional behavior within existing phases or as new
  named phases after Phase 6.

### IV. Documentation Is the Product

In a prompt-orchestrated system, specification text IS the
implementation. SKILL.md edits carry the same weight as code changes
in a traditional codebase.

- SKILL.md MUST be the single source of truth for agent behavior.
  Agents MUST NOT rely on conventions not written in SKILL.md.
- Templates contain mode-specific prompt engineering. The skill
  fills variables and orchestrates — templates define agent behavior.
- STATUS.md MUST be updated when any spec's implementation or
  acceptance status changes. It is the authoritative cross-spec
  reference. (See Known Antipatterns — `redundant-cache`: this
  applies to STATUS.md itself, not to creating new tracking
  documents that duplicate computable state.)

### V. Observable Deliberation

Every phase MUST report progress. Output validation MUST catch
malformed results. Agents MUST NOT silently swallow errors.

- Each phase emits a report line: "Phase {N} complete: {summary}."
- Output validation (e.g., Phase 6 heading checks) emits warnings
  for malformed output but does NOT block file writes. Malformed
  output is better than no output.
- Failure handling preserves prior phase results. A Phase 6 failure
  does NOT invalidate Phases 1-5.

### VI. Scripts Over Markdown

Prefer executable scripts over static markdown when the artifact
drives behavior. If a document is consumed by automation or agents
to make decisions, it SHOULD be a script, config, or structured
data — not prose that must be parsed ambiguously.

- Orchestration logic belongs in SKILL.md (executable spec) and
  templates (parameterized prompts), not in freeform documentation.
- Configuration belongs in YAML (`conversus.yml`, preset files),
  not in markdown tables or inline instructions.
- When a markdown artifact exists purely for human orientation
  (quickstart, README), markdown is appropriate. When it drives
  agent behavior, prefer structured and executable formats.

### VII. Reproducibility Over Inconsistency

Given the same inputs, conversus MUST produce structurally
identical output. Deterministic orchestration is non-negotiable.

- Template variable substitution is mechanical — same config
  produces same prompts. No ambient state or hidden context.
- File paths, phase ordering, and output directory structure are
  deterministic from the config. An implementor can predict the
  output tree from `conversus.yml` alone.
- Re-running a conversus with the same config overwrites cleanly.
  No accumulated state, no merge conflicts with prior runs.
- Preset resolution is deterministic: same name resolves to same
  file, same composition order produces same prompt.

### VIII. Templating Engines Over Inference

Prefer mechanical template-driven behavior over LLM inference
and improvisation. When an outcome can be achieved by variable
substitution, structured config, or deterministic rules, do NOT
delegate it to agent reasoning.

- Template variable substitution (`{VARIABLE}`) is mechanical and
  predictable. Agents fill variables; they do not invent structure.
- Mode-specific behavior is encoded in templates, not inferred by
  agents at runtime. The template dictates the output shape — the
  agent provides the content within that shape.
- Orchestration decisions (phase ordering, trigger evaluation,
  termination checks) are rule-based, not inferred. SKILL.md
  specifies deterministic logic; agents execute it.
- When agents MUST reason (reviews, cross-reviews, synthesis),
  templates constrain the reasoning with explicit instructions,
  required sections, and output formats. Unconstrained inference
  is a last resort.

### IX. Functional Programming and Clean Code

Code artifacts MUST follow functional programming practices and clean
code principles per the Python Functional Programming HOWTO
(reference: `.firecrawl/python-functional-howto.md`). Functions are
stateless, composable, and testable. Classes are used only when
framework or domain modeling requires them.

- Prefer pure functions over classes. A function that takes explicit
  inputs and returns a result is easier to test, compose, and reason
  about than a stateful object with methods.
- No mutable global state. Configuration is loaded once and passed
  explicitly. Validation functions receive their schema as parameters,
  not from module-level singletons.
- Compose small, focused functions rather than building monolithic
  procedures. Each function does one thing well and can be tested
  in isolation.
- Use iterators, generators, and `itertools`/`functools` when they
  improve clarity. Prefer `map()`, `filter()`, list comprehensions,
  and generator expressions over imperative loops when the intent
  is transformation or filtering.
- When classes ARE used (Pydantic models, framework-required base
  classes), prefer immutable data structures and minimize internal
  state.
- Code should be self-documenting through clear naming and structure.
  Comments explain WHY, not WHAT.
- Follow the principle of least surprise: APIs behave as their names
  suggest, edge cases are handled explicitly, and errors are
  descriptive.

**Explicit Typing (non-negotiable):**

- ALL function signatures MUST have explicit type annotations for
  every parameter and return value. No exceptions.
- ALL data structures MUST use Pydantic models for validation and
  type safety. Raw dicts from YAML/JSON parsing MUST be loaded
  into typed Pydantic models before use.
- Duck typing is permitted ONLY when the benefit is so significant
  it justifies breaking the convention. Every such case MUST include
  a comment explaining: (a) why duck typing is used, (b) what the
  benefit is, (c) why explicit typing would be worse.
- Use `typing` module constructs (`Optional`, `Union`, `Literal`)
  for precise type narrowing. Avoid `Any` unless wrapping an
  untyped third-party API.
- **Closed behavioral choices** (where each value triggers distinct
  code paths) MUST use `StrEnum` (Python 3.11+) for type-safe,
  YAML-compatible value enforcement with exhaustive pattern matching.
  Examples: `InfluenceLevel`, `ArbiterTiming`, error types.
- **Open registries** (where new values are data-driven and require
  no code changes) MUST use `str` with `frozenset` validation.
  Examples: mode names, phase names, variable types.
- Plugins extend closed enums via factory functions that produce new
  `StrEnum` subclasses with additional members. The factory pattern
  preserves runtime extensibility without sacrificing type safety.

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

### X. Zen of Python Output

Output MUST be clean, readable, and unsurprising. Follow the
spirit of the Zen of Python: explicit is better than implicit,
simple is better than complex, readability counts.

- There SHOULD be one obvious way to find the result. The output
  tree follows a predictable structure: `summary/final.md` is
  always the starting point.
- Flat is better than nested — avoid deep directory hierarchies
  when shallow ones suffice. Agent output is one level deep
  (`{agent}/review.md`), not arbitrarily nested.
- Errors should never pass silently — warnings are emitted for
  malformed output, missing documents, and edge cases.
- Sparse is better than dense — output files contain focused
  content, not kitchen-sink aggregations. Each file has one
  clear purpose.
- If the implementation is hard to explain, it's a bad idea.
  If SKILL.md instructions require paragraphs of caveats,
  the design needs simplification.

### XI. Single Source of Truth

Every piece of information MUST have exactly one authoritative source.
All other representations MUST be derived from that source, not
maintained independently. When two sources disagree, it is always a
bug — and the fix is always to eliminate the duplicate, not reconcile it.

- `schema/variables.yml` is the authoritative source for template
  variable definitions. Pydantic models, SKILL.md prose, and linter
  logic MUST derive from it, not duplicate it.
- Mode schemas (`schema/modes/*.yml`) are the authoritative source for
  mode-specific behavior (dispute headings, required headings,
  structural markers, mode_in_phases). SKILL.md references them;
  it does not restate them.
- When a hardcoded lookup table duplicates information that exists in
  structured data (e.g., `MODE_PRESENCE` dict vs `mode_in_phases` in
  YAML), the hardcoded version MUST be replaced with a derivation
  from the authoritative source.
- If you find yourself writing the same fact in two places, stop.
  One of them is wrong, or will be soon.

*Origin: spec 005 — MODE_PRESENCE dict duplicated mode_in_phases data,
INFLUENCE_LEVEL typed differently in model vs schema, FR-018 text
contradicted schema phases. All three were the same class of bug:
information in two places that disagreed.*

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

*Origin (v2.3.0): PR #4 (spec 064.1 runtime registration) and PR #18
(manifest tools[] projection) both assume the registry is authoritative.
This extension codifies that assumption.*

### XII. No Dead Infrastructure

Every provisioned capability MUST have at least one consumer. Variables
defined in the schema MUST be referenced in templates. Fields added to
Pydantic models MUST be populated by the orchestrator. Config options
documented in SKILL.md MUST be consumed by the execution logic.

- When adding a variable to `schema/variables.yml`, verify that at
  least one template in the corresponding phase contains `{VARIABLE}`.
  A variable that exists in the schema but appears in zero templates
  is dead infrastructure.
- When adding a field to a Pydantic context model, verify that the
  SKILL.md orchestration logic populates it. A field that exists in
  the model but is never set is a false promise.
- When provisioning infrastructure for a future spec (e.g., spec 005
  pre-provisioning spec 006 variables), document the intended consumer
  explicitly. Unattributed future-proofing becomes dead code.
- The linter SHOULD eventually check for dead variables (defined in
  schema but referenced in zero templates for their declared phases).

*Origin: spec 006 — ARBITRATION_PATHS and ARBITRATION_RULINGS were
provisioned in schema and Pydantic models but never referenced in
cross-round-synthesis templates. Fully defined, fully typed, fully dead.*

### XIII. Enum Completeness

When a `StrEnum` exists for a domain, ALL comparisons, assignments,
and references in that domain MUST use enum members — never string
literals. Partial adoption is worse than no adoption because it creates
a false sense of type safety while leaving unprotected string comparisons
that the enum was created to eliminate.

- When a `StrEnum` is introduced (e.g., `Phase`, `ErrorType`,
  `InfluenceLevel`), every file that compares against values in that
  domain MUST be updated in the same change. Do not leave string
  literals "to be converted later."
- The test suite SHOULD verify enum completeness: grep for string
  literals matching enum values and flag any that don't use the enum.
- When adding a new member to a `StrEnum`, update all `match`/`if-elif`
  chains that branch on that enum. Exhaustive handling is the point
  of using an enum.

*Origin: spec 006 — Phase StrEnum was created in models.py but
validate.py continued using `phase == "arbitration"` string literals
in 5 locations. The enum existed but wasn't adopted where it mattered.*

### XIV. Spec-Implementation Parity

When implementation intentionally narrows or broadens the scope of a
functional requirement, the spec text MUST be updated to match. Specs
and implementations MUST agree on what was built. A spec that says
"Phase 1-5" when the implementation does "Phase 1 only" is a bug in
the spec, even if the implementation is correct.

- After implementing an FR, re-read the FR text. If the implementation
  deviates (intentionally or not), update the spec to match reality.
- Spec amendments are cheap. Drift between spec and implementation
  is expensive — it misleads future implementors and produces wrong
  conversus review findings.
- The conversus review process SHOULD catch spec-implementation drift.
  If multiple agents independently flag the same discrepancy, treat
  it as a spec bug and fix it immediately.
- When a spec is moved to `specs/done/`, its text MUST reflect what
  was actually built, not what was originally proposed.

*Origin: spec 006 — FR-018 stated "All Phase 1-5 templates MUST
support PRIOR_ARBITRATION_SECTION" but the implementation correctly
restricted it to Phase 1 only (Phases 2-5 operate within a single
round and don't need prior-round arbitration context). The spec was
the bug, not the implementation.*

### XV. Plugin Isolation

Plugins consume core artifacts; they MUST NOT modify them. Core
deliberation MUST produce identical output with or without plugins
installed. Plugin output goes to a separate namespace (`plugins/`).
Plugin failure MUST NOT block core execution — warnings only.

- Data flows one direction: core produces deliberation artifacts →
  plugins consume them. Plugins never write to core output directories
  (`summary/`, `{agent}/`, `arbitration/`).
- Plugin configuration in `conversus.yml` is optional. Omitting the
  `plugins:` field produces identical behavior to pre-plugin conversus.
- A plugin that crashes, times out, or returns invalid data emits a
  warning. The core deliberation completes normally. Partial plugin
  output is preserved (unlike Phase 6, where partial output is deleted).
- Third-party plugins follow the same isolation rules. The plugin
  interface enforces this — `PluginResult` has no mechanism to modify
  core state.

**Clarification (v2.3.1): registry as the extension interface.** The
capability registry (`capabilities.py` + `conversus/registry/`)
constitutes an explicit extension interface separate from core
deliberation logic. Plugins extend conversus by registering new
`Capability` objects via this interface; they do not patch, override,
or otherwise modify the deliberation engine. The registry is the
**only** sanctioned extension point. Operators (via Principle XXVII)
filter the registered set — the two principles bracket the registry's
read/write contract.

*Origin: game engine vision (specs 016-020) — the paid optimization
layer must not compromise the free deliberation core. A user who
uninstalls a plugin must get the exact same deliberation they had before.*

### XVI. Mathematical Transparency

When optimization drives decisions, the user MUST understand what is
being optimized, even without understanding the math. Objective
functions are parameterized by user-provided values (weights,
constraints, criteria), not by opaque model internals.

- The 3-stage pipeline (symbolic parsing → LLM gap-filling →
  deterministic assembly) ensures the math reflects user intent.
  The LLM asks questions; the user's answers become parameters;
  the math is pre-defined. The LLM does not generate the objective
  function — it translates gap identifiers into natural-language
  questions and answers into parameter values.
- Every objective function template (spec 013) documents its
  mathematical form, its parameters, and what each parameter means
  in plain language. A user who reads the template understands what
  they are optimizing.
- Plugin recommendations (equilibrium scores, convergence predictions,
  config suggestions) MUST include plain-language explanations
  alongside numerical outputs. "Equilibrium quality: 0.87" is
  insufficient; "87% of agents are at their best possible position
  given others' positions" is required.
- Solver choice (nashopt, AMPL, future alternatives) is an
  implementation detail. The objective function is the contract
  between user intent and mathematical optimization. Changing
  solvers MUST NOT change what is being optimized.

*Origin: game engine vision (specs 012-019) — the transition from
template-driven prompts to mathematical optimization must not make
the system opaque. Users parameterize the math; they do not need
to understand it.*

### XVII. Content Classification

Execution logic and contribution guidelines MUST live in separate
formats. Runtime-enforced rules MUST NOT be split across both — drift
between execution and contribution surfaces creates silent failures.

- **Execution logic** (phase orchestration, template variable expansion,
  dispatch routing, validation with error messages, trigger evaluation,
  dispute parsing) MUST live in SKILL.md or its `references/` files.
  These are consumed by the agent runtime during deliberation.
- **Contribution guidelines** (naming conventions, PR instructions,
  coding standards, linter invocation, template authoring rules) MUST
  live in AGENTS.md files. These are consumed by coding agents during
  development.
- A rule that is enforced at runtime (e.g., preset validation, template
  `TEMPLATE_STATUS: draft` gate, antipattern check) is execution logic
  even if it also serves as a contribution guideline. The authoritative
  source MUST be in SKILL.md/references; AGENTS.md MAY reference it
  but MUST NOT redefine it.
- When extracting content from SKILL.md, classify each item before
  choosing its destination. The wrong classification creates either
  invisible execution rules (in AGENTS.md, not read by the runtime)
  or invisible contribution rules (in references, not read by
  non-Claude-Code agents).

*Origin: spec 011a deliberation — 4 of 5 agents independently
discovered that preset validation rules, template naming conventions,
and antipattern checks were being proposed for AGENTS.md extraction
despite being runtime-enforced contracts.*

### XVIII. Progressive Disclosure Contract

Every subcommand handler extracted to a reference file MUST have a
specific, unambiguous load trigger in the root SKILL.md. Agents load
only what the current invocation requires.

- Load triggers are either **dispatch-routed** (subcommand match from
  the dispatch table) or **config-conditional** (field presence in
  `conversus.yml`, e.g., "if `arbiter:` is present, read
  `references/subsystem-arbitration.md`").
- Generic triggers like "see references/" are prohibited — they defeat
  the context-reduction purpose of extraction by making the agent guess
  which files are relevant.
- Each reference file MUST be loadable independently. Circular
  dependencies between reference files are prohibited. A reference
  file MAY reference another reference file for shared subsystems,
  but the load trigger chain MUST be acyclic and documented.
- The root SKILL.md SHOULD stay under 500 lines / ~5,000 tokens.
  Per-invocation total (root + loaded references) is permitted to
  reach 8-12k tokens for complex paths (e.g., `/conversus run` with
  multi-round + arbiter). This is a documented exception to the
  agentskills.io 5,000-token recommendation, not a compliance failure.

*Origin: spec 011a deliberation — the agentskills.io 5,000-token
ceiling and run engine retention were identified as mutually exclusive
constraints. The progressive disclosure contract resolves this by
distinguishing always-loaded root from conditionally-loaded references.*

### XIX. Non-Extractable Core

The following MUST remain in the always-loaded root SKILL.md regardless
of any decomposition. These items are needed by every invocation path
or define invariants that must be impossible to accidentally violate.

- **Subcommand dispatch table**: the routing contract that maps
  invocations to handlers. Every subcommand's load trigger lives here.
- **Non-negotiable multi-agent rules**: one agent per output file,
  all agents within a phase launch in a single message, each agent is
  context-isolated, no meta-agents, phase boundaries are hard barriers.
  These are the architectural invariants that make deliberation
  adversarial — they must be in context for every run, converge, and
  gate invocation.
- **Phase-level execution flow summary**: a compact description of the
  6-phase pipeline sufficient for the agent to orchestrate without
  loading handler-specific reference files.
- **Important Notes / operational gotchas**: re-run overwrite behavior,
  agent count formulas, template-vs-skill responsibility boundary,
  baseline features list.

Removing any item from this list requires a constitutional amendment
with a rationale explaining how the invariant is preserved by other
means.

*Origin: spec 011a deliberation — all 5 agents unanimously converged
on these four categories as non-extractable. The multi-agent rules
received the strongest consensus: "any decomposition must make
invariant violations impossible to introduce, not just documented."*

### XX. Decomposition Mechanism Precedence

For single-consumer skills (used by one project), prefer agentskills.io
`references/` conditional loading over APM sub-skill promotion.
Sub-skills are warranted only when multiple independent consumers need
different subsets of the skill, or when the skill has independent
versioning requirements.

- `references/` files provide conditional on-demand loading at
  invocation time — the agent reads only what the current subcommand
  requires. This directly reduces per-invocation context cost.
- APM sub-skills provide install-time compilation and distribution —
  useful for packaging and version management across consumers, but
  they replace one monolith with several smaller monoliths that each
  still load fully on activation.
- Packaging overhead (manifest files, version management, dependency
  resolution) MUST be justified by distribution benefit. A skill used
  by one project does not need to be an APM package.
- When a second independent consumer appears, reassess whether
  `references/` is sufficient or whether APM sub-skill promotion
  provides meaningful distribution value.

*Origin: spec 011a deliberation — cross-reviews between apm-specialist
and agentskills-specialist identified `references/` and `.apm/skills/`
as mutually exclusive mechanisms. The agentskills approach won for
single-consumer projects because it solves the actual context window
problem (conditional loading) rather than the distribution problem
(packaging).*

### XXI. Extraction Ordering

When decomposing a monolithic skill, extract in order of independence.
Earlier extractions have lower risk and validate the decomposition
pattern before tackling tighter coupling.

1. **Handlers with no shared state** (e.g., gate handler — different
   audience, minimal coupling to run engine, independent config schema).
2. **Handlers with file-mediated coupling only** (e.g., guided workflow
   handlers — prerequisite chain is enforced through file existence
   checks, not shared memory).
3. **Shared subsystems with stable interfaces** (e.g., dispute parsing,
   preset resolution — already have documented interface contracts and
   multiple consumers).
4. **Core engine periphery** (e.g., multi-round orchestration,
   inter-round arbitration — tightly coupled to the run engine state
   machine; extract only if the boundary is clean).
5. **Never extract last**: if the core engine cannot be cleanly
   separated from its periphery, document why and leave it. A
   partially-extracted state machine is worse than a monolith.

Each extraction step MUST be independently verifiable: the skill
MUST produce identical output before and after the extraction for
all existing test configurations.

*Origin: spec 011a deliberation — the integration-specialist flagged
that extracting multi-round orchestration splits a state machine at
its midpoint. The ordering principle ensures high-risk extractions
happen last, after the pattern is proven on safer targets.*

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

*Origin: PR #11 (mcp_server.py missing from wheel), PR #13
(manifest.json drifted to 0.1.0 while pyproject was 0.3.0),
PR #18 (manifest tools[] from CAPABILITIES). Distribution drift is
build-time concern, not runtime.*

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

*Origin: PR #5 (claude-code tool-use response), PR #6 (anthropic
429 retry + concurrency), PR #8 (token tracking), PR #9 (claude-code
single-object JSON parser).*

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

The 2026-04-25 deliberation arbiter explicitly extended this scope to
provider protocols (not just synthesis logic) on the evidence that
PRs #5, #6, #8, #9 produced the same class of silent failure as
PR #10's false-PASS bug.

*Origin: PR #10 (red-blue contract break → false-PASS); generalized
over PRs #5, #6, #8, #9.*

### XXV. Live Test Cost Discipline

Tests that consume API credits, spawn subprocesses, or otherwise
incur real-world cost MUST follow four discipline rules:

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
XXII's end-to-end install testing requirement runs in CI. Install
tests that incur measurable cost (downloading wheels, spawning
isolated environments) MUST be marked `@pytest.mark.live` and run
under the gated job. Install tests that run in-process (e.g.,
`importlib.reload` against a built wheel) are not live and run on
every PR.

This principle is **foundational** for Principle XXIII (Provider
Robustness Contract) — provider contract tests are inherently live.
Without cost discipline, provider testing becomes prohibitively
expensive and the robustness contract goes untested.

*Origin: PR #8 introduced `@pytest.mark.live` without codifying the
discipline. The 2026-04-25 deliberation arbiter ruled this principle
must precede provider contract testing requirements.*

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
message ("Expected 8 prompts, parametrize covers 7: …new prompt
'estimate_complexity' missing").

*Origin: PR #12 introduced the meta-test pattern for `@mcp.prompt()`
definitions. The deliberation ruled this pattern should generalize
to all parametrized capability sets.*

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
how operators **subtract** capabilities. The two are complementary —
plugins extend the registry; operators filter the registered set.
Neither modifies core deliberation behavior.

**Registry as configuration boundary**: registry modifications via
this principle (operator subtraction) and Principle XV (plugin
extension) are **configuration changes affecting tool availability**,
not behavioral modifications to the deliberation process. The
capability registry constitutes an explicit extension interface
separate from core deliberation logic — changes inside the registry
do not change how deliberation works, only which deliberation
capabilities are exposed.

*Origin: PR #14 (CONVERSUS_DISABLED_TOOLS). The 2026-04-25 deliberation
arbiter ruled this should be a standalone principle (not a Principle
XV extension) because operator configuration scope extends beyond
plugin isolation to the core tool surface.*

## Development Workflow

The standard workflow for conversus feature development:

1. **Specify** (`/speckit.specify`): Define the feature as user stories
   with acceptance scenarios and functional requirements.
2. **Clarify** (`/speckit.clarify`): Identify and resolve underspecified
   areas in the spec.
3. **Plan** (`/speckit.plan`): Generate implementation plan with
   technical context, project structure, and risk assessment.
4. **Tasks** (`/speckit.tasks`): Break the plan into dependency-ordered,
   parallelizable implementation tasks.
5. **Implement** (`/speckit.implement`): Execute tasks, marking each
   complete as work progresses.
6. **Verify**: Confirm all FRs are satisfied against the spec.

Completed specs move to `specs/done/`. Active specs use sequential
numbering in `specs/{NNN}-{name}/`.

## Known Antipatterns

Agents MUST check the antipattern catalog at `antipatterns/catalog.md`
before proposing new artifacts, tracking documents, or process changes.
The SKILL.md Antipattern Check instruction (after Step 1) enforces this
workflow: read the Summary Index, match against current work, follow
corrections for any matches.

- **Redundant Cache**: Do not create manually-maintained tracking
  documents that duplicate existing infrastructure (e.g., task
  checkboxes, git history, speckit artifacts). Use existing tools.
- New antipatterns are recorded as they are observed, following the
  catalog format defined in `antipatterns/catalog.md` and the contract
  in `specs/010-antipattern-steering/contracts/catalog-format.md`.

## Governance

This constitution supersedes conflicting guidance in individual specs
or agent prompts. When a spec contradicts a constitutional principle,
the constitution governs unless the spec explicitly documents and
justifies the deviation.

- **Amendments**: Require documentation of the change, rationale, and
  impact on existing specs. Use `/speckit.constitution` to update.
- **Versioning**: MAJOR for principle removals or redefinitions, MINOR
  for new principles or material expansions, PATCH for clarifications.
- **Compliance**: The plan template includes a Constitution Check gate.
  Plans MUST pass this gate before proceeding to implementation.

**Version**: 2.3.1 | **Ratified**: 2026-03-20 | **Last Amended**: 2026-04-26
