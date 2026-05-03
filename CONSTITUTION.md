<!--
Sync Impact Report
Version change: 3.1.2 → 3.1.3 (PATCH — cycle 2C follow-on: split
the comma-listed Operational constants bullet into 4 separate bullets
matching issue #97's literal listing. Surfaced as a self-flagged
uncertainty during PR #104 ratification: the issue listed 4 distinct
items under Operational constants; PR #104 conservatively kept them
as the existing single bullet under the new sub-heading. The user
clarified intent: split them.)

Modified principles:
  - XIX. Non-Extractable Core — single bullet "Important Notes /
    operational gotchas: re-run overwrite behavior, agent count
    formulas, template-vs-skill responsibility boundary, baseline
    features list." replaced by 4 separate bullets matching the issue
    #97 specification:
      - Re-run overwrite behavior
      - Agent count formulas
      - Template-vs-skill responsibility boundary
      - Baseline features list
    The labeling "Important Notes / operational gotchas" parent header
    is dropped because the items are now individually addressable
    under the Operational constants sub-heading. No item is added or
    removed; the comma-list is decomposed into bullets.

Why PATCH: completes a structural-grouping change initiated by PR #104
(cycle 2C v3.1.1). The combined PR #104 + this PR realizes issue #97's
specification end-to-end. No normative content is added or removed;
the four item names are unchanged.

Verbatim-preservation contract: each new bullet's name matches the
corresponding word group in the original comma list. "Re-run overwrite
behavior" matches "re-run overwrite behavior". "Agent count formulas"
matches "agent count formulas". "Template-vs-skill responsibility
boundary" matches "template-vs-skill responsibility boundary".
"Baseline features list" matches "baseline features list". No
rewording, no scope expansion.

Governance log entry: 2026-05-01 in CONSTITUTIONAL_CONVERSATIONS.md
(spec 070 cycle 2C bullet-split follow-on).

Prior amendment (v3.1.1 → v3.1.2): see prior SIR comment block below.
-->

<!--
Sync Impact Report (prior — preserved for audit trail)
Version change: 3.1.1 → 3.1.2 (PATCH — same-version Principle II
elaboration deferred from v3.0.0 cycle 2A. Per the v3.0.0 SIR's
"Follow-up TODOs" section: "Same-version Principle II elaboration:
add to Principle II's breaking-change coordination text the sentence
'Reusing a retired principle number is a breaking change — any
historical document that cited the retired number by identity would
thereafter refer to a different principle.' Marked with
`# TODO(spec-070-cycle2-followup)` in body. Deferral to a same-
version follow-up is a downstream elaboration, not a Principle II
atomicity violation, per blind verdict ruling on Atomic bundle scope.")

Modified principles:
  - II. Stable Interfaces — the deferred no-reuse elaboration sentence
    is appended to the existing "Changing a stable interface requires
    updating every consumer..." bullet. The TODO comment block at
    that bullet (introduced in v3.0.0) is removed since the deferral
    is now resolved.

Why PATCH: same-version elaboration of an existing principle bullet,
adding a single declarative sentence that operationalizes the
already-ratified Principle Number Stability rule (v3.0.0 Governance
section) within Principle II's atomic-update language. No new
governance feature is introduced; the no-reuse rule itself is
unchanged. The elaboration adds linkage between two already-ratified
texts (Principle II's "single atomic change" requirement and
Principle Number Stability's "permanent retirement, never reuse").

Why no deliberation cycle: the wording was pre-ratified in v3.0.0
(see "Modified principles: II. Stable Interfaces — stable-interfaces
enumeration extended to include..." in the v3.0.0 SIR). The blind
verdict ruling on Atomic bundle scope explicitly authorized this
deferral as a downstream elaboration. The PATCH-class single-PR
pathway with verbatim-preservation contract applies: the appended
sentence text is preserved verbatim from the v3.0.0 SIR's TODO
specification.

Verbatim-preservation contract:
  - Sentence appended ("Reusing a retired principle number is a
    breaking change — any historical document that cited the retired
    number by identity would thereafter refer to a different
    principle.") matches the v3.0.0 SIR's TODO specification
    character-for-character.
  - Pre-existing bullet text ("Changing a stable interface requires
    updating every consumer...single atomic change.") is unchanged.
  - All other Principle II bullets are unchanged.
  - TODO comment block is removed (this is the resolution mechanism;
    leaving it in place would mis-document the principle as still
    deferring).

Governance log entry: 2026-05-01 in CONSTITUTIONAL_CONVERSATIONS.md
(spec 070 cycle 2 same-version follow-up).

Prior amendment (v3.1.0 → v3.1.1): see prior SIR comment block below.
-->

<!--
Sync Impact Report (prior — preserved for audit trail)
Version change: 3.1.0 → 3.1.1 (PATCH — labels-only structural
reorganization; no normative content change. Scope: spec 070 cycle 2C
adds two clearly-labeled sub-headings ("Architectural invariants" /
"Operational constants") to Principle XIX's bullet list. Per blind
verification's two-stage ruling on XIX, this is the immediate stage —
the migration eligibility note for Operational constants is reserved
for a future deliberation cycle because adding it would change the
operative meaning of XIX's "regardless of any decomposition" language.)

Modified principles (purely structural — no normative content change):
  - XIX. Non-Extractable Core — two sub-headings inserted between the
    introductory paragraph and the existing bullet list. Bullets 1-3
    (Subcommand dispatch table, Non-negotiable multi-agent rules,
    Phase-level execution flow summary) grouped under "Architectural
    invariants". Bullet 4 (Important Notes / operational gotchas)
    grouped under "Operational constants". All bullet text preserved
    verbatim; the trailing "Removing any item from this list requires
    a constitutional amendment" paragraph is unchanged.

Why PATCH (not MINOR): per the v3.0.0 Removal-checklist subsection (e)
precedent that introducing the FIRST instance of a new structural
feature qualifies as MINOR, sub-headings within an existing bullet
list are not a new structural feature — markdown sub-headings are a
generic typographic primitive, not a governance feature. The
classification matches the issue #97 P2 PATCH-class designation.

Why no deliberation cycle: per issue #97, "Because cycle 2C modifies
no normative language, a lightweight verification suffices: cross-
reference audit (does any other body text refer to XIX's bullets by
ordinal position, which would shift under sub-heading reorganization?),
and a single review pass to confirm verbatim preservation. Spec 067
dual-deliberation is not required for a PATCH-class structural-
grouping-only change." Cross-reference audit completed: XIX is only
cited at its own definition (no body text outside §1264 references
"XIX." or "Principle XIX" or "Non-Extractable").

Verbatim-preservation contract: all four bullet texts are unchanged
character-for-character. The introductory paragraph ("The following
MUST remain in the always-loaded root SKILL.md regardless of any
decomposition...") is unchanged. The closing paragraph ("Removing any
item from this list requires a constitutional amendment...") is
unchanged. The Origin note is unchanged.

Deferred to a future deliberation cycle (P3, NOT filed as an issue
here): the migration eligibility note for Operational constants. Per
issue #97 sequencing, this is "reserved for a second stage because
adding it would change the operative meaning of XIX's 'regardless of
any decomposition' language." When it lands, it will require dual-
deliberation per spec 067 because it modifies normative meaning.

Governance log entry: 2026-05-01 in CONSTITUTIONAL_CONVERSATIONS.md
(spec 070 cycle 2C implementation).

Prior amendment (v3.0.0 → v3.1.0): see prior SIR comment block below.
-->

<!--
Sync Impact Report (prior — preserved for audit trail)
Version change: 3.0.0 → 3.1.0 (MINOR — governance-record correction;
no normative content change, no body-text rewriting. Scope: spec 070
cycle 2B retroactive Origin-note Amendment record subsections for
Principles XXIV, XXV, XXVII. Closes the latent Principle XI documentation
gap surfaced by blind verification's arbiter ruling on retroactive
Origin notes during the v3.0.0 ratification.)

Modified principles (purely structural — no normative content change):
  - XXIV. Safety-Critical Defense-in-Depth — the arbiter-ruling sentence
    that previously sat in the normative body ("The 2026-04-25
    deliberation arbiter explicitly extended this scope to provider
    protocols ...") is moved verbatim into a labeled Amendment record
    subsection appended to the Origin note. Body content is reduced to
    the four numbered discipline rules; no new requirement is added,
    none is removed.
  - XXV. Live Test Cost Discipline — the existing Origin note's
    embedded arbiter-ruling sentence ("The 2026-04-25 deliberation
    arbiter ruled this principle must precede provider contract testing
    requirements.") is split out into a labeled Amendment record
    subsection. Origin note retains only the originating PR reference.
  - XXVII. Operator-Configurable Tool Surface — same treatment as XXV:
    arbiter-ruling sentence split out of Origin note into a labeled
    Amendment record subsection.

Why MINOR (not PATCH): each principle gains a new Amendment record
subsection — that is new structural infrastructure within the principle
container, even though no normative wording changes. Per the v3.0.0
Removal-checklist subsection (e), Amendment record placement is itself
a governance feature; introducing the first instances of it qualifies
as a MINOR governance enhancement. Future Amendment record additions
to other principles, when prompted by the same documentation-gap
mechanism, will follow the precedent established here.

Verification approach: per issue #96, "if the change is purely
structural (verbatim move from body to Amendment record), a single
coordinated PR with cross-reference verification suffices" — no
deliberation cycle required. The verbatim-preservation contract is
upheld:
  - XXIV body sentence (originally lines 1373-1376) → XXIV Origin
    Amendment record (verbatim wording with closing rationale appended:
    "No contemporaneous /speckit.constitution invocation was recorded;
    this retroactive record closes that historical process gap").
  - XXV Origin note tail sentence → XXV Amendment record (verbatim).
  - XXVII Origin note tail sentence → XXVII Amendment record (verbatim).

The closing rationale appended to each Amendment record names the
historical process gap explicitly and cites Removal checklist
subsection (e) so the v3.0.0 prospective infrastructure receives its
first three retroactive applications in lockstep.

No CONTRIBUTING.md, docs/output-conventions.md, mkdocs.yml, or schema
changes are required (governance bookkeeping does not affect operational
guidance or runtime behavior). The v3.0.0 deferred-items list (cycle 2B
entry at lines 138-146 of the prior SIR) is satisfied by this amendment.

Governance log entry: 2026-05-01 in CONSTITUTIONAL_CONVERSATIONS.md
(spec 070 cycle 2B implementation).

Prior amendment (v2.6.0 → v3.0.0): see prior SIR comment block below.
-->

<!--
Sync Impact Report (prior — preserved for audit trail)
Version change: 2.6.0 → 3.0.0 (MAJOR — principle removals: VI (Scripts
Over Markdown) and X (Zen of Python Output) are migrated out of the
constitution to operational guidance per spec 070 cycle 2. Per the
Governance Versioning bullet, MAJOR is triggered for principle
removals or redefinitions; both removals are bundled in this single
amendment cycle to amortize the verification overhead and to ratify
the migrate-out pattern as a coherent precedent rather than as two
sequential single-principle amendments.)

Removed principles:
  - VI. Scripts Over Markdown — RETIRED. The headline qualifier "when
    the artifact drives behavior" fails Constitutional Inclusion
    **Criterion 2 (Falsifiable scope)**: a reviewer must reason
    "well, X might be okay if Y" to apply it, which is precisely the
    failure mode Criterion 2 was designed to flag. (The v2.4.0
    grandfathering disclosure labeled this as a Criterion 1 failure;
    that label is corrected here. Criterion 1 tests *mechanical
    verification capability*; Criterion 2 tests *falsifiable scope*.
    The two have distinct remediation paths: Criterion 2 failures
    trigger wording-refinement evaluation as a first step before
    migrate-out is selected.) Reasoning chain followed for VI:
    (a) Criterion 2 identified as the applicable failure; (b) wording
    refinement evaluated; (c) no viable refinement exists — "drives
    behavior" has no structural default class (no file extension,
    directory pattern, or schema property identifies a behavior-
    driving artifact without human classification in every case),
    so no rewrite can operationalize it into a mechanically-applicable
    rule; (d) migrate-out concluded. The migrate-out conclusion is
    independent of the criterion label: under either Criterion 1 or
    Criterion 2 identification, the migrate-out outcome for VI holds
    because no viable refinement exists. The substantive guidance is
    preserved as authoring guidance in `CONTRIBUTING.md` § Authoring
    Conventions. The Governance section's existing Criterion 1 worked
    example ("code should be readable") exhibits the same Criterion
    1/2 conflation pattern; that worked example is flagged here for
    future correction.
  - X. Zen of Python Output — RETIRED. The headline claim "readability
    counts" is irreducibly subjective; the body's "errors should
    never pass silently" overlaps Principle V (Observable Deliberation)
    and the safety-critical defense-in-depth posture in Principle XXIV.
    Substrate analysis of the "one clear purpose per output file"
    sub-bullet (Criterion 3, Distinctness): this sub-bullet is
    subsumed by Principles V (Observable Deliberation) and VII
    (Reproducibility) applied to output schema design — the
    requirement that each output file has a focused, predictable
    purpose is a derived property of "every phase MUST report
    progress" composed with "deterministic orchestration is
    non-negotiable; an implementor can predict the output tree from
    `conversus.yml` alone." It is not an independent Criterion 3
    claim. The migrate-out for X holds. The substantive guidance is
    preserved at `docs/output-conventions.md`.

Migration targets:
  - VI guidance: `CONTRIBUTING.md` § Authoring Conventions
  - X guidance: `docs/output-conventions.md`

Modified principles:
  - II. Stable Interfaces — stable-interfaces enumeration extended to
    include "principle numbers (Roman numeral identifiers; permanent
    retirement is the only state change permitted, never reuse)."
    The Principle II elaboration making principle-number reuse an
    explicit breaking-change is deferred to a same-version follow-up
    (see TODO below); deferral is a downstream elaboration, not a
    Principle II atomicity violation per the blind verdict ruling on
    Atomic bundle scope.
Modified Governance section:
  - New "Principle Number Stability" subsection inserted after
    Constitutional Inclusion Criteria, before Compliance.
  - New Removal checklist subsection appended.
  - Grandfathering paragraph corrected: active set enumerated
    (I–V, VII–IX, XI–XXVII, plus XXVIII added post-gate); VI and X
    permanently retired and MUST NOT be reused regardless of gate
    criteria; current count = 26 active principles.
  - Path (c) precedent text (L1493–1495) corrected to a cycle/version-
    only formulation that no longer names VI and X by principle in
    the migrate-out clause; the v3.0.0 amendment is named as the
    canonical migrate-out precedent.

Ratification commit atomicity (per blind verdict ruling on Sequencing,
adopting co-equal P1 framing): this commit atomically includes
`CONSTITUTION.md`, `CONTRIBUTING.md`, `docs/output-conventions.md`,
`mkdocs.yml`, and `CONSTITUTIONAL_CONVERSATIONS.md`. No element lands
in isolation.

Cross-reference audit methodology: the cycle 1 implementation's
"zero body-text cross-references" claim missed the L1589 plural-form
"Principles VI and X" reference. This v3.0.0 amendment establishes
the audit methodology going forward: **singular form, plural form,
and adjacent-phrase forms** of removed principle identifiers must be
searched. Future principle-removal amendments MUST apply this
extended methodology and document the result in the SIR.

Comparative-principles asymmetry (CI-detectable structural default
class): Future migrate-out deliberations citing v3.0.0 as precedent
must demonstrate the absence of a structural default class for the
principle being remediated. **Judgment calls that have a CI-detectable
structural default class survive the Constitutional Inclusion Criteria
gate; judgment calls that have no structural default class do not.**
A structural default class is the set of structural properties (file
extension, directory location, schema field, code property) that
identify the dominant case mechanically, leaving only edge cases
requiring human classification. Principles XV ("core artifacts" =
files consumed by the deliberation runtime), XXIV ("safety-critical
paths" = synthesis verdict generation and provider protocol
implementation, explicitly enumerated), and IX ("prefer pure
functions" = stateless functions with no side effects and no
external state dependencies, statically analyzable) each have a
structural default class. Principle VI ("when the artifact drives
behavior") does not — there is no file extension, directory pattern,
or schema property that identifies a behavior-driving artifact
without human classification in every case. This distinction is the
constitutional load-bearing reason why VI was removed while XV, XXIV,
and IX were retained.

MUST→SHOULD rationale (for migrated text in CONTRIBUTING.md and
docs/output-conventions.md): the v2.4.0 gate governs *location*, not
*normative weight*. SHOULD is appropriate in operational guidance
because the same judgment-call qualifier that caused migrate-out also
makes MUST unenforceable without a mechanical check.

Verification trail:
  - Self-consistency: deliberations/070-cycle2-vi-x-self-2026-05-01/
    — PASS WITH FIXES. All P1 changes applied (L1589 wording fix,
    Criterion 2 SIR label correction with full reasoning chain,
    mkdocs.yml nav entry, X substrate analysis paragraph,
    cross-reference audit methodology documentation).
  - Blind verification: deliberations/070-cycle2-vi-x-blind-2026-05-01/
    — PASS WITH FIXES. All P1 atomic-bundle elements applied
    (Recs 1+2+3+4+6: tombstones for VI and X, Principle II stable-
    interfaces list addition, Governance Principle Number Stability
    subsection, Governance Removal checklist, grandfathering clause
    correction with explicit MUST NOT and 26-active count).

Deferred items (filed as GitHub issues, sequenced after v3.0.0
ratification):
  - Cycle 2B (P1, MINOR-class): retroactive Origin note Amendment-record
    subsections for Principles XXIV, XXV, XXVII to close the latent
    Principle XI documentation gap surfaced by blind verification's
    arbiter ruling on retroactive Origin notes. Each principle has
    arbiter-ruling language in its normative body describing a
    2026-04-25 deliberation extension; Governance has no amendment
    record. Cycle 2B closes these historical process gaps with
    retroactive Amendment record subsections in each principle's
    Origin note.
  - Cycle 2C (P2, PATCH-class): XIX labels-only sub-headings
    ("Architectural invariants" / "Operational constants"). Reorganize
    XIX's bullet list under two clear sub-headings without modifying
    any normative language and without adding any "may be migrated"
    note. Sequenced after cycle 2B.

Follow-up TODOs:
  - Same-version Principle II elaboration: add to Principle II's
    breaking-change coordination text the sentence "Reusing a retired
    principle number is a breaking change — any historical document
    that cited the retired number by identity would thereafter refer
    to a different principle." Marked with `# TODO(spec-070-cycle2-followup)`
    in body. Deferral to a same-version follow-up is a downstream
    elaboration, not a Principle II atomicity violation, per blind
    verdict ruling on Atomic bundle scope.
  - Cross-reference: CONTRIBUTING.md and docs/output-conventions.md
    are the canonical operational-guidance destinations for migrated
    VI and X content. The Governance section's operational-guidance
    list will be updated in a subsequent PATCH (P2 in the self verdict).

Governance log entry: 2026-05-01 in CONSTITUTIONAL_CONVERSATIONS.md
(spec 070 cycle 2 implementation).
Prior amendment (v2.5.0 → v2.6.0): see prior SIR comment block below.
-->

<!--
Sync Impact Report (prior — preserved for audit trail)
Version change: 2.5.0 → 2.6.0 (MINOR — combined: PATCH-class XVI
headline rewrite under path (c) restructuring + MINOR Governance
section addition defining the path (c) amendment category. Per
spec 070 cycle 1, the amendment closes the v2.4.0 grandfathering gap
for Principle XVI by elevating its existing structural substrate —
parameter pinning — as the load-bearing headline claim, while
deferring the original mechanically-unverifiable "user MUST
understand the math" framing to the Origin note as design intent.
The Governance section gains a new path (c) definition that names
this amendment as the canonical precedent for future remediation of
grandfathered Principles VI and X. The XVI headline rewrite
component is PATCH-class under path (c); the Governance section
addition is independently MINOR; the combined package is MINOR.)
Added principles: none
Modified principles:
  - XVI. Mathematical Transparency — headline reduced to ONE
    structural invariant (parameter pinning). Stage-3 of the 3-stage
    pipeline body relocated to attribute its guarantee to Principles
    VII and VIII (no additional normative requirement introduced at
    that stage; "assembly-form-identical" replaces prior "identical
    bit-for-bit" wording for IX-collision avoidance). The
    plain-language pairing requirement is restructured as an atomic
    package: structural definition (string-typed field; not merely
    restating the value; domain terms over math notation;
    interpretable without source code) + XV enforce-mode clause
    (malformed plugin output under XV warn-and-continue, registry-
    emission enforcement, plugin-failure isolation). Design-intent
    paragraph relocated to the Origin note (preceded by "Design
    intent:" label) with targeted wording fixes: L790 deletion,
    "(auditable)" → "(persisted to `objective.yml` via
    `SourceProvenance.filled_by`)", "template shapes are stable (no
    surprise math)" → "assembly structure is deterministic given
    the same template and pinned parameters", "(no bare numbers)"
    retained. Stage-3 verification artifact added to the
    Clarification (v2.3.2) Enforcement sub-bullet, explicitly
    labeled as a VII+VIII composition completeness test (not a
    Criterion 3 demonstration of independence) with a future-
    amendment reconsideration clause if the test reveals a
    stage-3-specific failure mode.
Modified Governance section: new "Grandfathered-principle headline
  rewrites (path (c))" paragraph inserted after the Extension blocks
  paragraph defining the amendment category, its PATCH-class
  classification, the SIR attestation requirement, and the
  no-re-audit rule for pre-v2.4.0 grandfathered body content.
Removed sections: none
Templates requiring updates: none

Path (c) attestation: No new normative requirements are introduced
by the XVI headline restructuring itself. The headline now elevates
parameter pinning as the load-bearing invariant; the "assembly-form
identity" language in the relocated stage-3 body is explicitly an
attribution to Principles VII and VIII, not a new requirement. The
plain-language pairing structural definition and XV enforce-mode
clause ARE new content added to the body, but they sharpen
verification scaffolding for an already-existing v2.3.2 requirement
rather than introducing a new normative obligation; they do not
change WHAT is required, only HOW the existing requirement is
verified and what XV-protocol applies on violation. Restructured
body content (3-stage pipeline, Clarification v2.3.2 block,
Observability/Enforcement/Falsification sub-bullets) existed
pre-v2.4.0 and is not re-audited under the three-criterion gate per
the path (c) no-re-audit rule.

Constitutional Inclusion Criteria — Criterion 3 formal record for
stage-3 deterministic assembly (deliberation 070 cycle 1,
2026-05-01):
  (a) Question: does stage-3's assembly-form-identity claim produce
      a verifiable assertion not already implied by composing
      Principle VII ("same config produces same prompts; no ambient
      state") with Principle VIII ("mechanical template-driven
      behavior")?
  (b) Evidence: bilateral negative finding from two adversarially-
      positioned reviewing agents (skeptic-mathematical, skeptic-
      cross-principle), each arriving at the composition conclusion
      through different analytical paths; neither agent identified
      a stage-3-specific verifiable claim that VII+VIII do not
      subsume.
  (c) Conclusion: stage-3 is a VII+VIII composition applied to the
      optimization domain; no independent normative requirement
      beyond those principles is introduced.
  (d) Headline consequence: one named invariant (parameter pinning).
  (e) Artifact disposition: stage-3 verification artifact added to
      the Clarification v2.3.2 Enforcement block as a VII+VIII
      composition completeness test. A future amendment may reopen
      this assessment if a stage-3-specific claim is identified
      that the completeness test demonstrates to be independent of
      VII+VIII.

Criterion 3 interpretation disclosure: Criterion 3 was designed to
prevent duplicate principles; its behavior when applied to a
within-principle reorganization is not explicitly defined by the
gate text. This SIR interprets Criterion 3 as asking whether the
elevated body content covers distinct ground from peer principles —
which has been true of XVI's parameter-pinning substrate since the
v2.3.2 amendment. This interpretation is disclosed for future
governance reference.

Design intent positioning: The original "user MUST understand what
is being optimized, even without understanding the math" framing —
which fails Criterion 1 because "user understanding" is not
mechanically checkable — is preserved as the principle's animating
purpose in a relocated Origin-note paragraph labeled "Design intent."
The constitutional claim is now the structural substrate (parameter
pinning) that achieves the design intent, not the design intent
itself. This positioning is the constitutionally established home
for design-intent prose (compare existing Origin notes in
Principles XIX, XXII, etc.).

Verification trail:
  - Self-consistency: deliberations/070-cycle1-xvi-self-2026-05-01/
    — PASS WITH FIXES (5 disputes ruled). All 5 P1 required changes
    applied to live CONSTITUTION.md in this PR.
  - Blind verification: deliberations/070-cycle1-xvi-blind-2026-05-01/
    — PASS WITH FIXES (2 disputes ruled). Both P1 required changes
    applied (headline reduction to ONE invariant; stage-3 body
    relocation with VII+VIII attribution; stage-3 verification
    artifact in enforcement block; Criterion 3 SIR formal record).
    Per spec 067, the more rigorous architectural standard (blind's
    headline-reduction-to-ONE-invariant) is adopted; self's
    orthogonal fixes (atomic plain-language package, design-intent
    relocation to Origin note, path (c) Governance addition) layer
    on top.
  - Arbitral precedent: the self arbiter elevated WP Rec 7
    (design-intent paragraph relocation to Origin note) from P3
    optional to MANDATORY co-blocking — the first use of arbitral
    authority to upgrade a convergence point's priority
    classification rather than resolve a disputed position. Logged
    in CONSTITUTIONAL_CONVERSATIONS.md 2026-05-01 entry as a
    precedent distinct from path (c).

Disclosure: The v2.3.2 Clarification block's use of "shape" for
assembled objective function structure (parameter names, template
selection, gap-identifier set) creates a terminological collision
with Principle IX's behavior-over-shape extension ("shape test" for
test-assertion quality). This collision is deferred to a named
follow-up PATCH per the self verdict's Dispute 4 ruling (Option B).
Both collision sites — the v2.3.2 block's "assembled objective
function's *shape*" and any preceding usages — must be resolved in
the same pass under that PATCH, which must receive dual-perspective
wording-precision and cross-principle-coherence review of the full
v2.3.2 block text before ratification. Tracking issue:
GitHub issue #94 (https://github.com/Build-Fractal/conversus-oss/issues/94),
also cited in the follow-up TODO list below.

Follow-up TODOs:
  - GitHub issue #94 (https://github.com/Build-Fractal/conversus-oss/issues/94):
    "fix(constitution): v2.3.2 Clarification block 'shape'
    terminology rename to 'assembly-form' (spec 070 cycle 1
    follow-up)" — covers both v2.3.2 block collision sites under
    dual-perspective wording-precision + cross-principle-coherence
    review of the full v2.3.2 block text before PATCH ratification.
  - Stage-3 assembly-form determinism completeness test (CI check
    invoking the assembly path twice within the same run artifact
    and asserting assembly-form-identical output) — pending
    implementation under the spec 014 contracts.
  - Plain-language schema lint (structural inspection of plugin
    recommendation output schemas for adjacent string-typed
    explanation fields) — pending implementation; ticket to be
    filed.

Rationale: Per spec 070 cycle 1's PASS WITH FIXES verdicts on the
v2.5.0 grandfathered-principle audit, Principle XVI's pre-v2.6.0
headline ("the user MUST understand what is being optimized, even
without understanding the math") fails Constitutional Inclusion
Criterion 1 ("user understanding" is not mechanically checkable),
and the v2.4.0 grandfathering disclosure flagged XVI as one of three
pre-gate principles failing under the new criteria. Both
deliberations (self-consistency 5 disputes; blind 2 disputes) ruled
PASS WITH FIXES; per spec 067, the more rigorous architectural
standard (blind's headline-reduction-to-ONE-invariant for stage-3
attributed to VII+VIII) is taken as the architectural shape; self's
orthogonal fixes (atomic plain-language package, design-intent
prose relocation to Origin note, path (c) Governance definition) are
layered on top. The combined amendment closes the XVI grandfathering
gap, establishes path (c) as a precedent for future grandfathered-
principle remediation, and preserves XVI's animating design intent
as a derived property of the structural invariant rather than as
the constitutional claim itself.

Governance log entry: 2026-05-01 in CONSTITUTIONAL_CONVERSATIONS.md
(spec 070 cycle 1 implementation).
Prior amendment (v2.4.0 → v2.5.0): see prior SIR comment block
below.
-->

<!--
Sync Impact Report (prior — preserved for audit trail)
Version change: 2.4.0 → 2.5.0 (MINOR — new principle: XXVIII Test-Fix
Boundary Preservation. Codifies the discipline that when fixing a
failing test, the fix MUST preserve the test's verification of real
behavior. Per spec 071 Q4 and CONSTITUTION.md Versioning, adding a
new principle is a MINOR bump.)
Added principles:
  - XXVIII. Test-Fix Boundary Preservation
Modified principles: none (cross-reference to Principle IX in
  XXVIII headline; IX text unchanged)
Removed sections: none
Templates requiring updates: none

Constitutional Inclusion Criteria self-assessment (per the v2.4.0
gate in Governance): Principle XXVIII passes all three criteria as
documented in spec 071 §5.
  - Criterion 1 (Mechanical verification): PASS. Skip-discipline
    regex check + diff-shape consistency check are both feasible
    and concretely sketchable.
  - Criterion 2 (Falsifiable scope): PASS. The four categories
    partition the legitimate fix space; mismatched diff shapes are
    structurally detectable; uncited skips are unambiguous.
  - Criterion 3 (Distinctness): PASS. v1's "assertion fidelity"
    clause was withdrawn after blind verification flagged it as a
    duplicate of Principle IX's behavior-over-shape extension; v2
    explicitly cross-references IX for assertion-fidelity
    discipline. Skip discipline + diff-shape categorization cover
    ground IX, XXIV, and XXVI do not.

Verification (per spec 067 §4):
  - Self-consistency: deliberations/071-self-consistency-2026-04-28/
    — PASS WITH FIXES (4 disputes ruled; all addressed in v2 or
    out-of-scope).
  - Blind v1: deliberations/071-blind-2026-04-28/ — "move to
    operational guidance." Drove v1 → v2: dropped duplicate clause,
    strengthened clause 3 with diff-shape consistency, fixed RFC
    2119 "MAY NOT".
  - Blind v2: deliberations/071-blind-v2-2026-04-29/ — PASS WITH
    FIXES (3 rulings). Rulings 1 and 2 OVERRIDDEN with rationale
    logged in CONSTITUTIONAL_CONVERSATIONS.md 2026-04-29 entry.
    Ruling 3 (no emergency bypass) N/A — XXVIII never proposed any.

Override-with-rationale: the blind v2 reviewing standard
("acknowledged residual = operational guidance"), if applied
uniformly, would relegate analogous extensions in Principle IX
(behavior-over-shape) to operational guidance. Diff-shape
consistency IS substantively verifying for the dominant failure
mode this principle was designed to catch (PR #42 case study); the
residual is honestly acknowledged in clause 2's text. The override
precedent is established here for future reference.

Follow-up TODOs:
  - .github/pull_request_template.md addition (per spec 071 §7).
  - scripts/lint-test-fixes.py implementation (per spec 071 §6).
  - specs/067-verification-methodology/spec.md §4.6 amendment
    (per spec 071 §8).

Rationale: 2026-04-28 spec 045 verification surfaced 95 failing
tests; 4-subagent investigation found 1 production bug
(engine/handlers.py import-shadowing — PR #42, merged 2026-04-28)
hiding behind ~70 mechanical failures. A naive sweep would have
labeled the shadowing fix as "fixture drift" and shipped it. This
principle codifies the discipline that surfaced it. Two refinement
iterations driven by adversarial blind verification: v1 → v2
dropped a duplicate clause (genuine distinctness fix); v2 → v2-
final overrode further narrowing with rationale logged per
established override precedent.

Governance log entry: 2026-04-29 in CONSTITUTIONAL_CONVERSATIONS.md
(spec 071 implementation).
Prior amendment (v2.3.2 → v2.4.0): see prior SIR comment block
below.
-->

<!--
Sync Impact Report (prior — preserved for audit trail)
Version change: 2.3.2 → 2.4.0 (MINOR — new Governance gate:
Constitutional Inclusion Criteria. A material expansion of the
Governance section that adds a three-criterion test (mechanical
verification capability, falsifiable scope, distinctness) that future
amendments MUST satisfy. Existing principles I-XXVII are grandfathered.)
Added principles: none (governance gate, not a new principle)
Modified sections:
  - Governance — inserted new "Constitutional Inclusion Criteria"
    bullet between the existing **Versioning** and **Compliance**
    bullets. Codifies the three-criterion gate from spec 069 §4.1
    with the 3 ACCEPT findings from the 2026-04-26 blind verification
    arbitration folded in: (a) Dispute 1 partial-ACCEPT — calibration
    sentence (positive-examples-only footnote naming Principles XI,
    XII, XIII, XXII, XXIV, XXVI as well-modeled patterns) appended
    after the prospective-only paragraph; (b) Dispute 2 ACCEPT —
    Practitioner middle ground: two worked examples in gate text
    (mechanical-falsifiability rejection + distinctness/composition
    rejection); (c) Dispute 3 ACCEPT — synthesizer middle position:
    Extension blocks landing post-ratification MUST include
    Verification artifact (Criterion 1) when introducing new normative
    requirements; Criterion 3 does not apply to Extension blocks by
    construction; wording-level clarifications exempt.
Removed sections: none
Templates requiring updates: none
Grandfathering disclosure (per spec 069 §5): three pre-gate
principles fail under the new criteria as drafted — VI (Scripts Over
Markdown — judgment-laden "when the artifact drives behavior"),
X (Zen of Python Output — irreducibly subjective "readability counts"),
XVI (Mathematical Transparency — plain-language explanation
requirement is unverifiable). All three retain ratified status. The
gate applies prospectively; migration of any grandfathered principle
to operational guidance is a separate, intentional act governed by
the same amendment process with the receiving document identified
explicitly in the migration spec.
Follow-up TODOs:
  - Verification-deliberation codification deferred to v2.5.0;
    acceptance bar (substantive zero-disputes vs. documented-disputes)
    to be resolved at that amendment with the panel-composition
    disclosure and unanimous-out-of-scope escape hatch as candidate
    inputs.
  - Grandfathering disposition (whether to migrate VI, X, XVI to
    operational guidance; tiering; deadlines) deferred to a follow-up
    amendment per the gate's prospective-only scope clause.
  - Form-only CI lint and PR template enforcement (synthesis P1
    convergent fixes from both verification deliberations) ship as
    paired follow-ups; the gate text in this amendment establishes
    the substantive requirement, with mechanical enforcement to land
    in a subsequent PR.
  - Precedent log build step lands as part of the form-check lint CI
    in the same PR sequence; if the lint ships before the rebuild
    step, the rebuild MUST be added as a follow-up CI change before
    the next MINOR amendment opens.
Rationale: 2026-04-26 spec 069 self-consistency deliberation (3
agents + subject arbitration, binding) on candidate v2.4.0 text
produced 0 ACCEPT-level findings on the amendment as drafted (Dispute
1 REJECT — AND-coupling unchanged; Dispute 2 DEFER — verification-
deliberation acceptance bar deferred to v2.5.0; Dispute 3 ACCEPT —
cooperative composition on precedent-log build moment, not a
defect-correction edit). A parallel 2026-04-26 spec 069 BLIND
verification deliberation (3 agents + subject arbitration) ruled 3
ACCEPT findings on the gate text, all folded into this amendment per
the listing above. Per the conservative-wording rule, the more
rigorous gate text is adopted where the two deliberations diverged.
Governance log entry: 2026-04-26 in CONSTITUTIONAL_CONVERSATIONS.md
(spec 069 implementation).
Prior amendment (v2.3.1 → 2.3.2): see git history for the XVI
determinism-scope clarification (3-stage pipeline determinism
properties, `objective.yml`-anchored pinning discipline).
Prior amendment (v2.3.0 → 2.3.1): see git history for the XV
"Clarification (v2.3.1)" registry-as-extension-interface sub-section.
Prior amendment (v2.2.0 → 2.3.0): see git history for the 6 new
principles + 2 extensions added on 2026-04-25.
-->

<!--
Sync Impact Report (prior — preserved for audit trail)
Version change: 2.3.1 → 2.3.2 (PATCH — Principle XVI determinism-scope
clarification: 3-stage pipeline determinism properties, `objective.yml`-
anchored pinning discipline, VII↔XVI bilateral carve-out, vocabulary
alignment with spec 014 / `construction.py`)
Added principles: none
Modified principles:
  - XVI. Mathematical Transparency — first bullet replaced with explicit
    3-stage determinism breakdown (symbolic parsing → LLM gap-filling →
    deterministic assembly); appended "Clarification (v2.3.2):
    determinism scope" block including `objective.yml`-anchored MUSTs
    (spec 014 FR-012), `GapFiller.fill()` protocol-boundary text,
    deliberation-run definition, `SourceProvenance.filled_by` audit
    hook, V observability obligation subordinate to VII reproducibility
    pre-conditions, XXIV enforcement cross-reference, falsification
    clause; stage 3 renamed "Mechanical assembly" → "Deterministic
    assembly" for vocabulary alignment with spec 014 / `construction.py`
  - VII. Reproducibility Over Inconsistency — line 163 receives a
    parenthetical "(narrowed by Principle XVI for LLM gap-filling
    output)" implementing the VII side of the bilateral carve-out
  - VIII. Templating Engines Over Inference — line 178 receives a
    one-line co-extensive parenthetical reconciling VIII's "mechanical"
    vocabulary with XVI's renamed "deterministic" stage 3
Removed sections: none
Templates requiring updates: none
Verification status of the pinning discipline: evidence-pending —
pinning discipline assumes spec 014 FR-012/SC-004 enforcement; contract
test per Principle XXIV filed as a follow-up to spec 014 (and CI lint
detecting re-entrant `GapFiller.fill()` per spec 068 follow-up).
Rationale: 2026-04-26 spec 068 self-consistency deliberation (3 agents
+ subject arbitration, binding) ruled on 4 disputes — 3 ACCEPT (P1-A
SIR audit-status hedge, P1-B `GapFiller.fill()` boundary text, P1-C
mechanical→deterministic rename + VIII parenthetical) plus 1 DEFER
(II stable-interface sub-bullet for `objective.yml` schema, deferred
to v2.3.3 unblock condition: second consumer of the schema lands).
A parallel 2026-04-26 spec 068 BLIND verification deliberation (3
agents + subject arbitration) ruled 4 ACCEPT findings, of which 2
converge with self-consistency (B2 spec-013-routed test contract
absorbed into the XXIV enforcement bullet, B3 V-emission subject to
VII reproducibility pre-conditions absorbed into the V observability
sub-bullet). The remaining 2 blind findings (B1 tightened-standalone
rewrite, B4 drop XXIV citation) conflicted with self-consistency's
stronger MUST/SHOULD discipline; per the conservative-wording rule the
self-consistency wording is adopted. Governance log entry: 2026-04-26
in CONSTITUTIONAL_CONVERSATIONS.md (spec 068 implementation).
Prior amendment (v2.3.0 → 2.3.1): see git history for the XV
"Clarification (v2.3.1)" registry-as-extension-interface sub-section.
Prior amendment (v2.2.0 → 2.3.0): see git history for the 6 new
principles + 2 extensions added on 2026-04-25.
-->

<!--
Sync Impact Report (prior — preserved for audit trail)
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
- Principle numbers (Roman numeral identifiers) are stable interfaces;
  permanent retirement is the only state change permitted, never
  reuse. See Governance § Principle Number Stability for the no-reuse
  rule and the RFC/CVE rationale.
- Changing a stable interface requires updating every consumer (specs,
  templates, SKILL.md sections, reference files) in a single atomic
  change. Reusing a retired principle number is a breaking change —
  any historical document that cited the retired number by identity
  would thereafter refer to a different principle.
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

### VI. ~~Scripts Over Markdown~~ — RETIRED v3.0.0

**Retired** 2026-05-01 in v3.0.0 per spec 070 cycle 2. The original
content has been migrated to `CONTRIBUTING.md` § Authoring Conventions.
Principle number VI is **permanently retired** and MUST NOT be reused
for any future principle, regardless of gate criteria — see Governance
§ Principle Number Stability.

### VII. Reproducibility Over Inconsistency

Given the same inputs, conversus MUST produce structurally
identical output (narrowed by Principle XVI for LLM gap-filling
output). Deterministic orchestration is non-negotiable.

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
and improvisation. (In v2.3.2, Principle XVI uses "deterministic"
for the post-pinning assembly stage; the term is co-extensive
with VIII's "mechanical" — both denote rule-based, non-inference-
driven execution.) When an outcome can be achieved by variable
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

### X. ~~Zen of Python Output~~ — RETIRED v3.0.0

**Retired** 2026-05-01 in v3.0.0 per spec 070 cycle 2. The original
content has been migrated to `docs/output-conventions.md`. Principle
number X is **permanently retired** and MUST NOT be reused for any
future principle, regardless of gate criteria — see Governance
§ Principle Number Stability.

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

When optimization drives decisions, conversus MUST satisfy one
structural invariant: **parameter pinning** — resolved values are
persisted once and re-loaded, never re-resolved within a deliberation
run.

- The 3-stage pipeline (symbolic parsing → LLM gap-filling →
  deterministic assembly) ensures the math reflects user intent.
  The three stages have different determinism properties, and
  conflating them is the source of past wording confusion:

    1. **Symbolic parsing**: deterministic — given a template ID,
       the parser yields the same gap identifiers every time.
    2. **LLM gap-filling**: stochastic at the `GapFiller.fill()`
       boundary. The protocol entrypoint is one call; whether the
       implementation makes one model invocation or several is an
       implementation detail. All resulting parameter values **MUST**
       be pinned together once `fill()` returns. Resolved parameter
       values **MUST** be persisted to `objective.yml` (spec 014
       FR-012) for the duration of the deliberation run; the LLM
       **MUST NOT** be re-invoked for parameter resolution within
       the same run; values **MUST** be re-loaded from `objective.yml`
       rather than re-resolved.
    3. **Deterministic assembly**: applies Principles VII and VIII
       to the optimization domain — given a template and a
       fully-pinned parameter set (every gap identifier from stage 1
       has a pinned value from stage 2), the assembled objective
       function is assembly-form-identical on every assembly within
       a deliberation run. No additional normative requirement
       beyond Principles VII and VIII is introduced at this stage.

  The math template is pre-defined at design time (spec 013). The
  LLM does not generate the objective function — it translates gap
  identifiers into natural-language questions and the user's
  answers into parameter values. Once parameters are pinned, the
  optimization is reproducible (Principle VII applies).
- Every objective function template (spec 013) documents its
  mathematical form, its parameters, and what each parameter means
  in plain language. A user who reads the template understands what
  they are optimizing.
- Plugin recommendations (equilibrium scores, convergence predictions,
  config suggestions) MUST include plain-language explanations
  alongside numerical outputs (no bare numbers). A conforming
  plain-language explanation is a string-typed field in the plugin
  recommendation output schema whose content (a) does not merely
  restate the numerical value as its sole information, (b) expresses
  the value's meaning in terms of the optimization domain rather than
  mathematical notation alone, and (c) is interpretable without
  reference to source code or schema definitions. A plugin
  recommendation that omits or incorrectly structures plain-language
  pairing is treated as malformed plugin output under Principle XV's
  warn-and-continue protocol (enforced at registry-emission time per
  Principle XV's registry-as-extension-interface clarification); it
  does NOT block core deliberation execution, and the core run
  completes normally per Principle XV's plugin-failure isolation
  guarantee. "Equilibrium quality: 0.87" is insufficient; "87% of
  agents are at their best possible position given others' positions"
  is required.
- The objective function — *what is being optimized* — is the
  contract between user intent and mathematical optimization.
  Changing solvers (nashopt, AMPL, future alternatives) MUST NOT
  change the objective function (Principle VII applies to the
  objective-function contract). Numerical optimization output may
  vary across solvers within documented stability bounds; that
  variance is solver behavior, not a violation of this principle.

**Clarification (v2.3.2): determinism scope.** Principle XVI
**requires** within-run determinism for the assembled objective
function and cross-run reproducibility once parameters are pinned.
This carves an explicit exception to Principle VII's unconditional
"structurally identical output": the assembled objective function
is the determinism boundary, not the LLM-resolved parameter values
that feed into it. Principle XVI does NOT claim the LLM gap-filling
step itself is deterministic; that step is allowed to be stochastic,
and the discipline is in pinning its output rather than re-running
it. Specifically: (a) the LLM MUST NOT be re-invoked for parameter
resolution within a single deliberation run; (b) cross-run variance
in resolved parameter *values* is acceptable (e.g., two
`/conversus mode` invocations on the same `problem.md` MAY produce
different `objective.yml` files); (c) cross-run variance in the
assembled objective function's *shape* (parameter names, template
selection, gap-identifier set) is prohibited.

- *deliberation run*: the lifetime of one `objective.yml` artifact;
  retries that reuse the same artifact are part of the same run,
  separate `/conversus run` invocations producing new artifacts are
  different runs. Cross-version replay (re-running after a
  `conversus` upgrade) is out of scope of this principle.
- The run orchestrator **MUST** persist resolved parameter values to
  `objective.yml`; pinning is auditable via `SourceProvenance.filled_by`
  (`conversus/schemas/construction.py:262-279`) — a sanctioned form of
  explicit, keyed persistence distinguished from the ambient state
  Principle VII prohibits.
- **Observability (Principle V):** Stage 2 emits a Principle V phase
  report line: ``{N} gap identifiers resolved ({K} from
  `objective.yml`, {N-K} newly resolved via `GapFiller.fill()` and
  recorded under `SourceProvenance.filled_by`)``. The phase-report
  emission is meaningful only when VII's reproducibility pre-conditions
  hold (config, template registry, capability registry byte-identical
  between runs); a registry change between runs makes the emission
  misleading rather than auditable.
- **Enforcement:** Principle XXIV applies — a contract test
  reproducing the re-resolution failure pattern is required, filed as
  a follow-up to spec 014 FR-012/SC-004 acceptance criteria and to
  spec 013's parameter-pinning contract test, plus a CI lint detecting
  re-entrant `GapFiller.fill()` calls. Stage-3 assembly-form
  determinism MUST have a corresponding completeness test: a CI
  check that invokes the assembly path twice within the same run
  artifact, using the same fully-pinned parameter set and the same
  template registry state, and asserts assembly-form-identical
  output. This test verifies the VII+VIII composition applied to
  the optimization domain. It is a pipeline completeness test —
  not a Criterion 3 demonstration of stage-3 independence from
  those principles. If a future implementation of this test reveals
  a failure mode that Principles VII and VIII individually would
  not catch, that finding constitutes grounds for a new amendment
  reconsidering stage-3's constitutional status.
- **Falsification:** A future PR that re-resolves parameters
  mid-deliberation, or that lets parameter values drift during a
  single optimization run, violates this principle.

*Origin: game engine vision (specs 012-019) — pinning behavior is
specified in **spec 014 FR-012/SC-004** (assembly determinism) and
FR-020/FR-021 (artifact contract). Spec 013 supplies the template
definitions stage 1 parses. Some referenced runtime layers (specs
016-019, optimizer/nashopt/ampl) are spec'd but partly under
construction; this principle codifies the discipline they will
satisfy when implemented. Enforcement is verified by a contract test
per Principle XXIV at the path declared in spec 014's contracts.*

*Design intent: that users understand what is being optimized
without understanding the math. This is achieved through the
structural requirements above: user-provided parameters stay pinned
(persisted to `objective.yml` via `SourceProvenance.filled_by`),
assembly structure is deterministic given the same template and
pinned parameters, and outputs are paired with explanations (no
bare numbers).*

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

*Origin: PR #10 (red-blue contract break → false-PASS); generalized
over PRs #5, #6, #8, #9.*

*Amendment record (2026-04-25, arbiter ruling): The 2026-04-25
deliberation arbiter extended this principle's scope from synthesis
verdict generation to provider protocol implementation, on the
evidence that PRs #5, #6, #8, #9 produced the same class of silent
failure as PR #10's false-PASS bug. No contemporaneous /speckit.constitution
invocation was recorded; this retroactive record closes that historical
process gap (added in v3.0.x cycle 2B per Removal checklist subsection (e)).*

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
discipline.*

*Amendment record (2026-04-25, arbiter ruling): The 2026-04-25
deliberation arbiter ruled this principle must precede provider
contract testing requirements. No contemporaneous /speckit.constitution
invocation was recorded; this retroactive record closes that historical
process gap (added in v3.0.x cycle 2B per Removal checklist subsection (e)).*

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

*Origin: PR #14 (CONVERSUS_DISABLED_TOOLS).*

*Amendment record (2026-04-25, arbiter ruling): The 2026-04-25
deliberation arbiter ruled this should be a standalone principle
(not a Principle XV extension) because operator configuration scope
extends beyond plugin isolation to the core tool surface. No
contemporaneous /speckit.constitution invocation was recorded; this
retroactive record closes that historical process gap (added in
v3.0.x cycle 2B per Removal checklist subsection (e)).*

### XXVIII. Test-Fix Boundary Preservation

When fixing a failing test, the fix MUST preserve the test's
verification of real behavior. Assertion-fidelity discipline is
governed by Principle IX (behavior-over-shape extension); this
principle adds two mechanically verifiable disciplines that
operate at fix-time.

1. **Skip discipline**: any `pytest.skip()`, `@pytest.skip`, or
   `@pytest.mark.skip` newly introduced in a PR MUST cite the bug
   being skipped (issue or PR number) and a remediation timeline.
   "Flaky", "slow", "broken", or similar without a citation is
   prohibited.
   *Mechanical check*: any newly added skip directive whose
   adjacent comment or docstring does not match
   `(issue|PR|#\d+|TODO\(.+\))` plus a timeline cue is a violation.

2. **Test-or-bug categorization with diff-shape consistency**:
   every PR that modifies a test file in a fix-time context MUST
   declare each fix as exactly one of four categories, and the
   PR's diff shape MUST match the declared category:

   | Category | Required diff signature |
   |---|---|
   | fixture/path drift | only test files modified |
   | production bug | ≥1 production-source file modified |
   | legitimate test bug | only test files modified; PR body cites the test-side bug |
   | defunct test | test deletion (not modification); PR body cites why the behavior is no longer relevant |

   *Mechanical check*: the lint reads the declared category from
   a structured PR-template field, computes the actual diff shape,
   and flags any mismatch. A mismatch is the violation, not the
   misjudgment that produced it — mismatch is structurally
   detectable; misjudgment is not, and that limit is acknowledged
   rather than papered over.

*Origin: 2026-04-28 spec-045 verification surfaced 95 failing
tests; the 4-subagent investigation found 1 production bug
(engine/handlers.py import shadowing — PR #42) hiding behind ~70
mechanical failures. A naive sweep would have labeled the
shadowing fix as "fixture drift" and shipped it; the diff-shape
check (production-source edit incompatible with that label) is
the discipline that catches that exact failure mode.*

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
- **Compliance**: The plan template includes a Constitution Check gate.
  Plans MUST pass this gate before proceeding to implementation.

**Version**: 3.1.3 | **Ratified**: 2026-03-20 | **Last Amended**: 2026-05-01
