<!--
Sync Impact Report
Version change: 3.2.3 → 4.0.0 (MAJOR — tier extraction. 20 principles
relocated to higher tiers; 6 retained at component scope; 2 retired
markers preserved.)

Modified sections:
  - "Core Principles" reduced to 6 principles (XVII-XXI, XXVI) plus
    retired markers for VI and X. Cross-reference block added at top
    pointing readers to https://github.com/Build-Fractal/build-fractal-mono/blob/main/CONSTITUTION.md (Tier 1) and
    https://github.com/Build-Fractal/build-fractal-mono/blob/main/deliberator/CONSTITUTION.md (Tier 2) for relocated
    principles.
  - "Governance" preserved verbatim. Pathway Taxonomy, Constitutional
    Inclusion Criteria, Compliance, Amendment Process all retained
    here as the canonical procedural reference for amendments at any
    tier.

Relocated to Tier 1 (https://github.com/Build-Fractal/build-fractal-mono/blob/main/CONSTITUTION.md, v1.0.0):
  I. Spec-Driven Development
  II. Stable Interfaces
  III. Backward-Compatible Extension
  IV. Documentation Is the Product
  VII. Reproducibility Over Inconsistency
  VIII. Templating Engines Over Inference
  IX. Functional Programming and Clean Code
  XI. Single Source of Truth
  XIV. Spec-Implementation Parity
  XXVIII. Test-Fix Boundary Preservation

Relocated to Tier 2 (https://github.com/Build-Fractal/build-fractal-mono/blob/main/deliberator/CONSTITUTION.md, v1.0.0):
  V. Observable Deliberation
  XII. No Dead Infrastructure
  XIII. Enum Completeness
  XV. Plugin Isolation
  XVI. Mathematical Transparency  [Suite-tier rationale in Tier 2 doc per Fix B5]
  XXII. Distribution Surface Integrity
  XXIII. Provider Robustness Contract
  XXIV. Safety-Critical Defense-in-Depth
  XXV. Live Test Cost Discipline
  XXVII. Operator-Configurable Tool Surface

Retained at component tier:
  XVII. Content Classification
  XVIII. Progressive Disclosure Contract
  XIX. Non-Extractable Core
  XX. Decomposition Mechanism Precedence
  XXI. Extraction Ordering
  XXVI. Meta-Testing for Parametrized Capabilities

Retired (number stability — never reuse):
  VI (Scripts Over Markdown) — retired v3.0.0
  X (Zen of Python Output) — retired v3.0.0

Why MAJOR: structural reorganization of the canonical constitution.
Existing readers' paths to relocated principles change. Per Principle II
the principle numerals stay stable across tiers; per the verbatim
preservation contract (spec §5) the principle bodies are byte-equal at
their new locations.

Suite admissions ratified at v4.0.0:
  - deliberator admitted Provisional (5 open remediations: V, XII,
    XXII, XXIV, XXVI) per CONFORMANCE.md.
  - deliberator admitted Provisional (4 open remediations: III, XIV,
    XVI, XXII) per CONFORMANCE.md.

Constitutional debt acknowledgment (per Fix B2):
  Tier 1 (Universal) carries grandfathered principles ratified
  pre-Inclusion-Criteria-gate (v2.4.0): I, II, III, IV, VII, VIII,
  IX, XI, XIV. XXVIII passed the post-gate criteria. Their
  constitutional validity is preserved per Principle II + the
  grandfathering provision; their post-gate compliance with current
  Inclusion Criteria is NOT re-evaluated by v4.0.0. Future targeted
  amendments may address individual principles' post-gate
  conformance as separate cycles.

Cross-tier weakening prohibition (per Fix B3):
  A lower-tier amendment weakens an upper-tier principle if any of:
  (i) implicit relief outside COMPLIANCE.md Part VI Relief pathway;
  (ii) interpretation language flipping existing-Satisfied to
  not-Satisfied; (iii) suite-specific adaptation bypassing a MUST.
  Enforcement: meta-arbiter review + tier-coherence linter
  flagged-words check + existing-implementation impact check on
  every cross-tier amendment. https://github.com/Build-Fractal/build-fractal-mono/blob/main/deliberator/CONSTITUTION.md
  § Cross-tier weakening prohibition documents the full operational
  definition.

Originating deliberation:
  deliberations/v4.0.0-tier-extraction-originating-2026-05-06/
  Verdict: Q1 APPROVE-AS-DRAFTED, Q2 ADMIT-PROVISIONAL, Q3 ADMIT-
  PROVISIONAL. All four P1 conditions discharged or translated to
  Provisional remediations.

Verification deliberations (both required per spec 067):
  - deliberations/v4.0.0-tier-extraction-self-consistency-2026-05-06/
    Verdict: PASS WITH FIXES — 7 fixes applied in spec v2.
  - deliberations/v4.0.0-tier-extraction-blind-2026-05-07/
    Verdict: PASS WITH FIXES — 5 fixes B1-B5 applied in spec v3.

Spec: specs/v4.0.0-tier-extraction/spec.md (v3 — both verifications passed).
Governance log: https://github.com/Build-Fractal/build-fractal-mono/blob/main/deliberator/CONSTITUTIONAL_CONVERSATIONS.md
                CONSTITUTIONAL_CONVERSATIONS.md (this repo)

Engine note: arbitration phase auto-arbitrator crashed on both
verification deliberations at dispatch (1ms / 2ms; bug logged in
project_deliberator_arbitration_crash_2026_05_06 memory). Manual
arbitrations performed grounded in synthesis + disputes per spec 067
balanced-arbiter standard. Both manual arbitrations recorded in their
respective resolution.md files. Engine fix tracked separately.

Discharges: build-fractal Phase A → Phase B in
            ~/.claude/plans/peaceful-stargazing-moler.md.

Prior amendment SIRs preserved below for audit trail (per Fix #3 + Fix B2).
-->



# Deliberator OSS Constitution (Component Tier)

**Status:** RATIFIED — v4.2.0 (2026-05-13).
**Version:** 4.2.0
**Inherits from:**
- `https://github.com/Build-Fractal/build-fractal-mono/blob/main/CONSTITUTION.md` (Tier 1 — Universal, v1.0.0)
- `https://github.com/Build-Fractal/build-fractal-mono/blob/main/deliberator/CONSTITUTION.md` (Tier 2 — Suite, v1.0.0)

For Universal and Suite principles, see those documents. This document holds the **7 component-tier principles** specific to the deliberator repo, plus the canonical Governance section (which governs amendments at all tiers), plus retired-principle markers, plus the full audit trail of prior Sync Impact Reports.

---

## Retired

The following principles were retired in prior amendments. Their numerals are permanently retired per Principle II number-stability and MUST NOT be reused.

### VI. ~~Scripts Over Markdown~~ — RETIRED v3.0.0

**Retired** 2026-05-01 in v3.0.0 per spec 070 cycle 2. The original
content has been migrated to `CONTRIBUTING.md` § Authoring Conventions.
Principle number VI is **permanently retired** and MUST NOT be reused
for any future principle, regardless of gate criteria — see Governance
§ Principle Number Stability.

### X. ~~Zen of Python Output~~ — RETIRED v3.0.0

**Retired** 2026-05-01 in v3.0.0 per spec 070 cycle 2. The original
content has been migrated to `docs/output-conventions.md`. Principle
number X is **permanently retired** and MUST NOT be reused for any
future principle, regardless of gate criteria — see Governance
§ Principle Number Stability.


## Component Principles

The 7 principles below describe constraints on the OSS engine specifically, not on the suite as a whole. Principles XVII-XXI and XXVI are byte-for-byte identical to their text in `CONSTITUTION.md` v3.2.3. Principle XXIX was added 2026-05-13 via spec v4.2.0.

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
  `deliberator.yml`, e.g., "if `arbiter:` is present, read
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
  reach 8-12k tokens for complex paths (e.g., `/deliberator run` with
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

#### Architectural invariants

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

#### Operational constants

- **Re-run overwrite behavior**
- **Agent count formulas**
- **Template-vs-skill responsibility boundary**
- **Baseline features list**

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

### XXIX. Structured Deliberation Outputs

Deliberator-oss deliberation outputs (review, cross-review, revision, disputes, synthesis, arbitration) MUST be emitted as declared, schema-validated JSON envelopes per the canonical schemas in `engine/schema/v1/*.schema.json`. The Component-tier implementation of Tier 2 Principle XXVIII (Persistence Contract Discipline) for deliberator is specified by spec `v4.2.0-structured-deliberation-outputs` (RATIFIED 2026-05-13).

- **Schema location MUST be discoverable** via `CONFORMANCE.md` (one canonical path) with cross-references from `README.md` AND `CLAUDE.md`. This implements XXVIII sub-clause 1.
- **A non-blocking validator MUST emit conformance warnings** to an event stream and a sidecar `.validation-warnings.json` adjacent to each persisted output. The validator MUST NOT raise or abort — per Tier 2 Principle V, malformed output is better than no output. The persistence layer writes the output file UNCONDITIONALLY before any validator invocation. This implements XXVIII sub-clause 2 while preserving Principle V.
- **A PR-required CI gate** (`validate-conformance` + `drift-detection-bidirectional` + `schema-version-bump-detection` + `fixture-and-renderer-tests` jobs) MUST block merge of non-conformant changes on `main`. Constitutional authority: Tier 1 Principle II (Stable Interfaces) + Tier 2 Principle XXVIII sub-clause 2.
- **Four fixture types per output type** MUST be carried: conformant, missing-required, wrong-type, baseline. This implements XXVIII C6 with one additional type beyond the three-type minimum.
- **Schema versioning** follows SemVer with the consumer-impact rule: a field rename or removal that breaks any declared consumer is MAJOR; a backward-compatible addition is MINOR; pure validator-error-format adjustment is PATCH. Initial schema version is `1.0.0-rc.1`; promotion to `1.0.0` requires 30 days of clean operation per the qualification criteria in spec § 4.8.
- **A `CONSUMER-CONTRACT.md` at the repo root** MUST declare each consumed surface using the six-section template (Consumed Surface Declaration / Schema Version Pinning / Stability Guarantee / Consumer-Side Obligations / Producer-Side Enforcement / Change Coordination) per spec § 7.1. The deliberator CONSUMER-CONTRACT.md MUST declare deliberation-output schemas as a stable consumed surface for downstream consumers (orchestrator spec-kit adapter, deliberator-enhanced).

**Cliff date:** Markdown deliberation outputs are deprecated effective **2026-12-01** (Tier 2 Principle XXVIII universal deadline). All six mode templates MUST emit JSON envelopes by the cliff date; the orchestrator spec-kit adapter MUST migrate from grep-parsing to JSON parsing during the rollout window (T1-T4 per spec § 11).

**Authority:** Spec `v4.2.0-structured-deliberation-outputs` v5 (commit `24538e7`) — see `CONSTITUTIONAL_CONVERSATIONS.md` 2026-05-13 entry for the SIR with full four-stage verification record.

*Origin: spec v4.2.0 motivated by three concrete bugs from the v4.1.0 cycle (Phase 5 synthesis-prompt overflow crash; Phase 2 cross-review persistence failures; Phase 6 `disputes_remain` trigger grep-mismatch). All three are addressed by structured-output schema enforcement. Methodology meta-signal: the trigger-miss bug occurred in 4 of 5 v4.1.0+v4.2.0 deliberation stages — exactly the failure mode this principle ratifies the fix for.*

## Governance

This constitution supersedes conflicting guidance in individual specs
or agent prompts. When a spec contradicts a constitutional principle,
the constitution governs unless the spec explicitly documents and
justifies the deviation.

- **Amendments**: Require documentation of the change, rationale, and
  impact on existing specs. Use `/speckit.constitution` to update.
- **Versioning**: MAJOR for principle removals or redefinitions, MINOR
  for new principles or material expansions, PATCH for clarifications.
- **Constitutional Inclusion Criteria** (added v2.4.0): a principle
  qualifies for constitutional inclusion only if it satisfies all
  three:

  1. **Mechanical verification capability**: at least one form of
     automated check (CI lint, parity test, structural assertion,
     schema validation, or equivalent) MUST be feasible such that a
     future PR violating the principle would fail the check. The
     check does NOT have to exist at amendment time, but the path
     to building it MUST be concrete enough that an engineer reading
     the principle can sketch the check in one paragraph.

  2. **Falsifiable scope**: the principle's wording MUST be specific
     enough to flag a hypothetical future PR as violating, without
     requiring "interpretation." If a reviewer must reason "well, X
     might be okay if Y," the principle is too vague for the
     constitution and belongs in operational guidance.

  3. **Distinct from existing principles**: the principle MUST cover
     concerns not already addressable by composing existing principles.
     Restating an existing principle in different words is rejected
     by this gate. Refining or extending an existing principle goes
     in that principle's body, not as a new principle.

  **Worked examples.** A principle proposing "code should be readable"
  fails Criterion 1: no automated check is feasible. A principle
  proposing "all template variables MUST be lowercase" fails Criterion
  3: it composes from Principle IX (typing/style discipline) and
  Principle XI (single source of truth in `schema/variables.yml`); the
  refinement belongs in IX's body or as a schema constraint, not as a
  new principle.

  **Passing borderline worked example** (added v3.2.2 per spec 070
  cycle 3D, issue #122): a principle requiring "every newly added
  `pytest.skip()` directive MUST cite a bug number and remediation
  timeline" passes Criterion 1 (lint matching `(issue|PR|#\d+)` plus
  a timeline cue is feasible), passes Criterion 2 (specific enough to
  flag an uncited skip without interpretation), and passes Criterion 3
  (not addressable by composing Principles IX, XXIV, or XXV).
  **Principle XXVIII is the ratified example** of this borderline-pass
  pattern — see its v2.5.0 SIR for the override-with-rationale
  precedent. An acknowledged residual that is honestly labeled in
  clause text and accompanied by an override-with-rationale entry in
  the governance log does not require migration to operational guidance.

  This third worked example complements the two failure examples
  above. Calibration instruments with only failure anchors are
  structurally biased toward over-migration: amendment authors lack
  a positive reference for borderline cases. The XXVIII precedent
  closes that calibration gap.

  Principles that fail any criterion belong in **operational guidance**:
  `AGENTS.md`, the relevant spec, `SKILL.md` instructions, or
  domain-specific reference documents. Operational guidance is the
  explicit home for "judgment calls" and "rules of thumb"; the
  constitution is the home for invariants.

  This gate applies **prospectively** — to amendments landing after
  v2.4.0. The grandfathered set, as of v3.0.0, is enumerated
  explicitly: Principles I, II, III, IV, V, ~~VI~~, VII, VIII, IX,
  ~~X~~, XI, XII, XIII, XIV, XV, XVI, XVII, XVIII, XIX, XX, XXI, XXII,
  XXIII, XXIV, XXV, XXVI, XXVII (with XXVIII added post-gate per
  v2.5.0). **Principles VI (Scripts Over Markdown) and X (Zen of
  Python Output) are RETIRED v3.0.0** per spec 070 cycle 2 and are
  shown struck through above. Numbers VI and X are permanently retired
  and **MUST NOT be reused by any future amendment, regardless of
  whether proposed content would satisfy the three-criterion gate or
  any other qualification criteria** — see the Principle Number
  Stability subsection below for the underlying rationale. The
  current count is **26 active principles** (28 grandfathered minus 2
  retired). Migrating any other grandfathered principle to operational
  guidance is a separate, intentional act governed by the same
  amendment process (with the receiving document identified
  explicitly in the migration spec).

  When drafting new principles, prefer the structural pattern of
  principles whose verification artifact is named explicitly (e.g.,
  Principles XI, XII, XIII, XXII, XXIV, XXVI). This is calibration
  guidance only and does not affect the ratified status of any
  pre-gate principle.

  **Extension blocks.** Extension or Clarification blocks added to a
  grandfathered principle after the gate's ratification MUST include
  the structured `Verification:` block (Criterion 1) when they
  introduce new normative requirements. The block MAY cite the parent
  principle's verification artifact if the extension reuses it. The
  Distinctness criterion (Criterion 3) does not apply to Extension
  blocks — by construction, they are extensions of an existing
  principle — but the Extension MUST declare in one sentence why the
  new content belongs in the parent principle's body rather than as a
  new principle. Wording-level clarifications (typo fixes,
  reformattings, cross-references) are exempt from this rule.

  **Grandfathered-principle headline rewrites (path (c)).** A headline
  rewrite of a grandfathered principle that restructures existing body
  content into a new headline without introducing new normative
  requirements constitutes a path (c) amendment. Path (c) amendments
  are PATCH-class for the restructuring component; the MINOR
  designation applies only if genuinely new normative requirements
  are introduced alongside the restructuring, in which case those
  requirements are subject to the full three-criterion gate (Criteria
  1, 2, and 3) regardless of how the surrounding restructuring is
  framed. A path (c) SIR MUST include an explicit attestation that no
  new normative requirements are introduced by the headline
  restructuring itself. Body content that existed in a grandfathered
  principle before v2.4.0 is not re-audited under the three-criterion
  gate when elevated to headline status under path (c); the gate
  applies only to genuinely new content. This 2026-05-01 amendment
  establishing the path (c) definition (v2.6.0, spec 070 cycle 1) is
  the canonical path (c) precedent for future in-place headline
  rewrites of grandfathered principles. The 2026-05-01 v3.0.0
  amendment (spec 070 cycle 2) is the canonical migrate-out precedent
  for removal of grandfathered principles to operational guidance.
  Both precedents may be cited by future amendments without
  re-litigating the analytical foundation, provided the citing
  amendment demonstrates analytical fit.

  **Coordination with Principle XVII (Content Classification).** The
  gate inherits XVII's vocabulary; routing decisions to operational
  guidance follow XVII's execution-logic vs. contribution-guidelines
  distinction. The cross-reference flows gate → XVII (newer references
  older), per the constitution's reference topology.
- **Principle Number Stability**: principle numbers (Roman numerals)
  are stable interfaces (Principle II). Once retired, a principle's
  number MUST NOT be reused — regardless of whether a future
  candidate principle would pass the Constitutional Inclusion
  Criteria gate. The retirement creates a permanent identifier
  attached to the now-removed principle's content, enabling external
  citations (other specs, deliberation logs, agent skills, third-
  party documentation) to remain unambiguous after retirement.

  Cf. RFC and CVE numbering: retired identifiers stay attached to
  their original assignments forever. The constitutional analogue
  is identical — the cost of preserving citation integrity is
  cheap (ledger entry); the cost of losing it is unbounded
  (every prior reference becomes ambiguous).

  Future principle additions MUST use unused numbers (XXIX, XXX, …)
  rather than filling gaps left by retirements. Tombstone entries
  in the principle list document each retirement; gaps in the
  enumeration are intentional.
- **Removal checklist**: a principle removal MUST satisfy each of
  the following before ratification:

  (a) **Verification deliberations**: both self-consistency and
      blind verification per spec 067 must complete with PASS or
      PASS WITH FIXES verdicts; all P1 fixes from both verdicts
      must be applied in the ratification commit.
  (b) **Migration target identified**: the receiving document for
      the removed principle's substantive content must be named
      and the content must exist at the named location at
      ratification time, not as a deferred follow-up.
  (c) **Tombstone entry created**: the removed principle's slot in
      the principle list must contain a strikethrough headline,
      retirement date, retirement version, migration target, and
      the no-reuse declaration cross-referencing Principle Number
      Stability.
  (d) **Principle Number Stability cited**: the SIR and the
      tombstone must both cite the no-reuse rule explicitly, so
      future readers cannot construct a "gate-eligible reuse"
      reading of the retirement.
  (e) **Arbiter-ruling Origin note amendments coordinated**: any
      principles whose normative bodies contain embedded arbiter-
      ruling language describing prior amendments (cf. cycle 2B
      for XXIV, XXV, XXVII) must have their Origin notes updated
      with retroactive Amendment record subsections in the same
      PR as the prospective Governance change that requires
      arbiter-ruling documentation, when both are coordinated.
      When the prospective and retroactive items are sequenced
      across separate PRs (as in this v3.0.0 ratification, which
      defers cycle 2B), the deferral and the rationale must be
      documented in the SIR.
  (f) **Cross-reference audit**: every body-text reference to the
      removed principle must be updated in the same commit.
      The audit MUST cover **singular form, plural form, and
      adjacent-phrase forms** of the removed principle's name and
      number (e.g., "Principle VI", "Principles VI and X",
      "VI/X migration"). The cycle 1 amendment's audit missed the
      L1589 plural form; the v3.0.0 amendment establishes the
      extended methodology for future audits.
- **Constitutional Amendment Pathways** (added v3.2.0, migrated from
  CONSTITUTIONAL_CONVERSATIONS.md per the pathway-taxonomy
  deliberation 2026-05-01): the deliberation pathway used for an
  amendment is determined by both the version-bump impact (MAJOR /
  MINOR / PATCH) and the verification cost (full dual-deliberation /
  single PR with verbatim contract / single PR with pre-ratified
  deferred wording). The taxonomy below names the four ratified
  pathways and the authorization basis that justifies each:

  | # | Pathway | Cost | Trigger | Authorization basis | Example |
  |---|---------|------|---------|---------------------|---------|
  | 1 | MAJOR with full dual-deliberation | spec 067 self + blind | Principle removal/redefinition | Full dual-deliberation (spec 067) | v3.0.0 |
  | 2 | MINOR with verbatim contract | single PR | First instance of new structural feature | Absence of new normative content | v3.1.0 |
  | 3 | PATCH with verbatim contract | single PR | Sub-headings within existing structure | Absence of new normative content | v3.1.1 |
  | 4 | PATCH with pre-ratified deferred wording (Provisional — single canonical example; canonical status requires two independent uses from distinct sessions without governance anomalies) | single PR | Same-version follow-up named in prior SIR | Prior deliberation scope coverage of deferred wording | v3.1.2 |

  **Routing function vs. gate-enforcement function**: For routing,
  all single-PR rows answer "no deliberation required when verbatim
  preservation holds." Authorization basis governs what conditions
  must be satisfied to invoke each single-PR pathway — see gate
  conditions for row 4 below.

  **Gate conditions for row 4** (PATCH with pre-ratified deferred
  wording): an amendment qualifies for this pathway only when ALL
  three conditions are affirmatively satisfied:
  (a) **Wording pre-specified**: the appended sentence text matches a
      prior SIR's TODO specification character-for-character.
  (b) **Prior deliberation scope coverage**: the prior SIR's
      verification cycle MUST have covered the substantive claim of
      the deferred wording (not merely its existence as a TODO). The
      cycle's deliberation phase or finding that evaluated the
      claim's correctness MUST be cited by version and section in
      the implementing PR.
  (c) **No new normative requirements**: the appended wording adds
      linkage between two already-ratified texts, not a new normative
      requirement.

  **Self-consistency note**: condition (b) raises a self-consistency
  question for row 4's canonical example (v3.1.2). The v3.0.0
  deliberation validated the Principle II stable-interfaces
  enumeration extension as an architectural change. Whether the
  deliberation's scope explicitly covered the correctness of the
  specific elaboration sentence ("Reusing a retired principle number
  is a breaking change — any historical document that cited the
  retired number by identity would thereafter refer to a different
  principle.") is not determinable from the governance log as
  written. If scope did not extend to that sentence's substantive
  claim, v3.1.2 satisfies conditions (a) and (c) but not (b). Future
  applications of this pathway MUST resolve condition (b)
  affirmatively — by citing the specific deliberation phase and
  finding that evaluated the claim's correctness — before invoking
  the low-cost pathway. This gap does not void the pathway's
  analytical framework; it identifies a documentation deficiency in
  the canonical example.

  **Note on the RFC/CVE analogy**: the RFC/CVE reference in the
  Principle Number Stability subsection above supports identifier
  stability — the no-reuse rule for principle numbers. RFC and CVE
  processes use single amendment pathways; the deliberator
  multi-pathway taxonomy is a departure from that model, not an
  extension of it. The analogy cannot be cited as authority for
  adding new pathway rows to this taxonomy. Adding a fifth, sixth,
  Nth pathway requires the same dual-deliberation that constitutional
  changes require, with explicit grounding in the pathway taxonomy's
  authorization-basis structure.
- **Operational guidance documents** (added v3.2.1 per the
  closure-verification deliberation 2026-05-01 P2 #4, discharging
  the v3.0.0 SIR's deferred Governance-list commitment): the
  canonical destinations for migrated grandfathered-principle
  substantive content are:
  - `CONTRIBUTING.md` § Authoring Conventions — the migrated home
    for Principle VI's substantive guidance (orchestration in
    SKILL.md/templates, configuration in YAML, markdown for human
    orientation). Receiving document declared in the v3.0.0 SIR.
  - `docs/output-conventions.md` — the migrated home for Principle
    X's substantive guidance (predictable output tree, flat
    hierarchies, warnings for malformed output, sparse content).
    Receiving document declared in the v3.0.0 SIR.

  Future migrations that retire a grandfathered principle to
  operational guidance MUST name the receiving document in the
  migration spec's SIR (per the Removal checklist subsection (b)
  precedent). Adding a new operational-guidance destination
  requires citing this list and is itself a MINOR amendment when
  the destination is a new file or directory; PATCH when an
  existing file gains a new section.
- **Compliance**: The plan template includes a Constitution Check gate.
  Plans MUST pass this gate before proceeding to implementation.

**Version**: 3.2.3 | **Ratified**: 2026-03-20 | **Last Amended**: 2026-05-04
