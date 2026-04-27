# Phase 3 Revision — wording-precision

**Reviewer**: wording-precision
**Iteration**: 1
**Target**: CONSTITUTION-v2.3.2-candidate.md, Principle XVI

### Recommendation Dispositions

#### Recommendation 1: Promote pinning from description to obligation
- **Original position**: Convert L463-466 descriptive prose ("are pinned per deliberation run", "cached values from the first resolution are reused") into MUST-language obligations.
- **Disposition**: Modified
- **Explanation**: Both cross-reviewers agreed this is the load-bearing P1 fix (CPC Safe Agreement #2; PEG Safe Agreement #1). PEG's Off-Base #1 and Dangerous Contradiction #1 surface a sequencing problem I missed: the candidate's "cached values are reused" describes a runtime cache that does not exist in the code — the actual mechanism is artifact-mediated (`objective.yml` written once, re-read on subsequent runs). My MUST conversion, applied verbatim, would mandate a non-existent cache. Modified text incorporates PEG's anchor: "Resolved parameter values **MUST be persisted to `objective.yml`** (spec 014 FR-012) for the duration of the deliberation run; the LLM **MUST NOT** be re-invoked for parameter resolution within the same run; values **MUST** be re-loaded from `objective.yml` rather than re-resolved." This preserves the normative upgrade and fixes the description-vs-reality gap in one edit. Sequencing per PEG: if a code grep proves the discipline is not yet implemented, an "evidence-pending" hedge precedes the MUST conversion.

#### Recommendation 2: Define "deliberation run"
- **Original position**: Add inline definition: "a single invocation of the run engine producing one output directory; retries within an invocation are part of the same run, separate `/conversus run` invocations are different runs."
- **Disposition**: Modified
- **Explanation**: Both cross-reviewers endorsed the gap (CPC Safe Agreement #2 implicit; PEG Safe Agreement #2). CPC Dangerous Contradiction #3 surfaced a foreclosure risk I missed: my definition implicitly prohibits cross-version cache reuse by tying "run" to a single invocation. PEG Dangerous Contradiction #2 added the artifact-anchor concern: "retries within an invocation are part of the same run" is a substantive claim about retry semantics that may be false on adoption if the code uses a different boundary. Modified text: anchor to the artifact (per PEG) and add a forward-pointing hedge (per CPC): "*deliberation run*: the lifetime of one `objective.yml` artifact; retries that reuse the same artifact are part of the same run, separate `/conversus run` invocations producing new artifacts are different runs. Cross-version cache reuse is out of scope of this principle." This preserves precision while leaving the III interaction explicit instead of silently foreclosed.

#### Recommendation 3: Resolve the VII ↔ XVI cross-run determinism tension explicitly
- **Original position**: Add carve-out sentence in the v2.3.2 clarification stating the assembled objective function is the determinism boundary, not the LLM-resolved parameter values.
- **Disposition**: Modified
- **Explanation**: Both cross-reviewers independently identified this as the largest defect and endorsed the carve-out (CPC Safe Agreement #1; PEG Safe Agreement, "VII ↔ XVI tension is real, not artifactual"). My self-review of CPC's review (cross-review file) flagged a real co-authoring risk: CPC's Recommendation #1 puts the fix into Principle VII, mine puts it into XVI's clarification — adopting both verbatim violates Principle XI by writing the same fact in two places. Modified text resolves where: full carve-out lives in XVI's clarification (the amendment in flight), with a single back-reference parenthetical inserted into VII line 163 ("Given the same inputs, conversus MUST produce structurally identical output (narrowed by Principle XVI for LLM gap-filling output)"). Never the full text in both. PEG's lighter framing ("acknowledge the apparent conflict") is rejected — the contradiction is real and a soft acknowledgment will not survive a future PR review.

#### Recommendation 4: Convert "claims" to normative verbs
- **Original position**: Replace "Principle XVI claims" (L491) with "Principle XVI requires."
- **Disposition**: Surviving
- **Explanation**: Both cross-reviewers endorsed (CPC Safe Agreement #3; PEG Safe Agreement, implicit in #1). CPC Tension #2 noted that this fix is complementary, not alternative, to my carve-out recommendation — both are needed. No modification required: the fix is a one-line verb swap. Surviving as P2.

#### Recommendation 5: Bound "cross-run variance is acceptable"
- **Original position**: Replace "Cross-run variance is acceptable" with bounded text scoping variance to parameter values, prohibiting variance in shape/parameter names/template selection.
- **Disposition**: Modified
- **Explanation**: CPC Dangerous Contradiction #2 surfaced a nesting issue: my bound addresses *what may differ across runs of the assembled function*, but the cache-hit-on-rerun policy is a separate bound at a different scope. PEG Tension #4 added that I bound *what variance is acceptable* while a concrete user-visible failure mode should also be named. Modified text composes all three: "(a) the LLM **MUST NOT** be re-invoked for parameter resolution within a single deliberation run; (b) cross-run variance in resolved parameter *values* is acceptable (e.g., two `/conversus mode` invocations on the same `problem.md` MAY produce different `objective.yml` files); (c) cross-run variance in the assembled objective function's *shape* (parameter names, template selection, gap-identifier set) is prohibited." The three clauses operate at different scopes and do not collide.

#### Recommendation 6: Specify pinning storage and lifetime
- **Original position**: Replace "cached values from the first resolution are reused" with "persisted to the run's output directory and reused for the lifetime of that directory."
- **Disposition**: Modified
- **Explanation**: Both cross-reviewers endorsed (CPC Safe Agreement #1; PEG Tension #5 + Dangerous Contradiction #1). CPC Dangerous Contradiction #1 and PEG Dangerous Contradiction #1 converge: my mechanism-agnostic phrasing is weaker than CPC's deterministic-tree placement (per Principle X) and weaker than PEG's `objective.yml` anchor. CPC also flagged that "the run's output directory" is itself undefined per X. Modified text adopts PEG's specific artifact anchor with CPC's forward-compatible hedge and X-aware deterministic placement: "Pinned parameter values **MUST** be persisted to `objective.yml` (spec 014 FR-012) at a deterministic path inside the run's output directory (per Principle X), or to its successor parameter artifact, and **MUST** be reused for the lifetime of that directory." Promoted P2 → P1 in priority because this fix is now coupled to Recommendation 1's MUST.

#### Recommendation 7: Disambiguate the two LLM activities in stage 2
- **Original position**: Split stage 2 prose into 2a (question generation) and 2b (answer→value extraction), each stochastic and pinned together.
- **Disposition**: Modified
- **Explanation**: PEG Tension #3 challenged the framing: `GapFiller.fill()` (construction.py:139-149) is the literal extension point and the constitution should name protocol-level boundaries, not activity-level boundaries — otherwise either decomposition risks describing a phantom split. CPC Tension #5 confirmed my split is the more defensible textual reading but is local; CPC did not raise it. Modified per PEG: name the `GapFiller.fill()` boundary (one call) and let stochasticity be a property of that call, regardless of how many model invocations the implementation chooses internally. New text: "**LLM gap-filling**: stochastic at the `GapFiller.fill()` boundary. The protocol entrypoint is one call; whether the implementation makes one model invocation or several (e.g., separate question-generation and answer-extraction calls in `InteractiveGapFiller`) is an implementation detail. All resulting parameter values **MUST** be pinned together once `fill()` returns." This matches both the code and my "pinned together" intent. Downgraded P2 → P3 per PEG's grounding.

#### Recommendation 8: Cite a spec FR for the pinning behavior
- **Original position**: Add specific FR or contract test reference to the Origin block, e.g., "spec 013 FR-{N} and verified by test {path}."
- **Disposition**: Modified
- **Explanation**: PEG Dangerous Contradiction #3 caught a specific error: I named spec 013, but spec 013 defines the *templates*; spec 014 defines the *assembly determinism contract*. Anchoring to the wrong spec FR makes the citation un-auditable. CPC Tension #5 added that the test obligation should also be routed through Principle XXIV (Safety-Critical Defense-in-Depth) for constitutional weight. Modified text adopts both: "Pinning behavior is specified in **spec 014 FR-012/SC-004** (assembly determinism) and FR-020/FR-021 (artifact contract). Spec 013 supplies the template definitions stage 1 parses. Enforcement is verified by a contract test per **Principle XXIV** at the path declared in spec 014's contracts." Surviving as P2 with corrected anchor.

#### Recommendation 9: Define "fully-pinned parameter set"
- **Original position**: Add inline parenthetical at L469: "every gap identifier produced by stage 1 has an associated pinned value from stage 2."
- **Disposition**: Surviving
- **Explanation**: Neither cross-reviewer challenged this directly. CPC Tension #1 flagged general bloat risk (mine adds inline definitions, CPC adds cross-references; together they could double the principle's length), but the fix here is a single parenthetical and does not contribute meaningfully to bloat. PEG did not raise it. Surviving as P3.

#### Recommendation 10: Name the agent that pins parameters
- **Original position**: Replace passive voice "are pinned" with named responsible component: "The run orchestrator MUST pin resolved parameter values…"
- **Disposition**: Modified
- **Explanation**: PEG Tension #4 surfaced an auditable hook I missed: `SourceProvenance.filled_by` (construction.py:262-279) is the existing enum that already records who pinned each value. Naming the orchestrator as the responsible component is a precision win, but PEG's hook anchors it to verifiable code. CPC Tension #4 added that naming the agent is also load-bearing for distinguishing the cache from VII line 167's prohibited "ambient state." Modified text composes both: "The run orchestrator **MUST** pin resolved parameter values; pinning is auditable via `SourceProvenance.filled_by` (a sanctioned form of explicit, keyed persistence as distinguished from the ambient state Principle VII prohibits)." Surviving as P3.

### New Recommendations

#### New Recommendation A: Add a v2.3.2 Sync Impact Report
- **Priority**: P1
- **Triggered by**: My own Scope Creep Check (review.md L113) flagged the missing v2.3.2 SIR but did not promote it to a recommendation. CPC's review did not catch it; PEG's Tension #2 confirmed this is a real metadata gap and noted it is the natural place to record either the spec 068 §7 Q1 grep result or the explicit "aspirational" framing for Recommendation 1's sequencing question.
- **Proposed change**: Add a v2.3.2 Sync Impact Report block at the top of the constitution (above the v2.3.1 SIR), documenting: (a) version change 2.3.1 → 2.3.2 (PATCH — XVI determinism scope clarification); (b) modified principle XVI (3-stage pipeline + clarification block); (c) the v2.3.2 carve-out's effect on Principle VII (narrowed to acknowledge XVI); (d) origin = spec 068 self-consistency deliberation.
- **Rationale**: Without a v2.3.2 SIR, the constitution's metadata describes only v2.3.1 while the version footer says 2.3.2. This is a precision failure independent of the principle text and creates audit-trail drift. Promoting to P1 because metadata consistency is a one-edit fix that should not block deferred to a follow-up.

#### New Recommendation B: Reconcile "mechanical" vs "deterministic" vocabulary across XVI and VIII
- **Priority**: P2
- **Triggered by**: PEG Tension #5 and Dangerous Contradiction (PEG Off-Base #2): the constitution says "mechanical assembly" while spec 014 FR-012 and `construction.py:8-14` say "deterministic." CPC Tension #4 independently flagged the same drift between XVI's "mechanical assembly" stage label and Principle VIII's umbrella "Templating Engines Over Inference" treatment of "mechanical." My original review missed this entirely — I praised "bit-for-bit" as unambiguous without noticing the stage label drifted from the codebase's vocabulary.
- **Proposed change**: Either (a) rename stage 3 in XVI from "Mechanical assembly" to "Deterministic assembly" to match spec 014 FR-012 and construction.py, or (b) add a single sentence to XVI's clarification: "Note: 'mechanical assembly' as used in stage 3 is co-extensive with the 'deterministic' vocabulary in spec 014 FR-012 and `construction.py`; the terms describe the same property."
- **Rationale**: Two terms for the same property invite future drift. Pick one and document the equivalence. P2 because this is precision-affecting but not safety-critical.

### Position Summary

Of my 10 original recommendations, **0 are withdrawn**, **8 are modified**, and **2 survive unchanged** (Recommendations 4 and 9). The high modification rate reflects a real shift: my Phase 1 review was wording-only and the cross-reviews supplied two anchors I lacked — codebase grounding (PEG's `construction.py`, `objective.yml`, `SourceProvenance.filled_by`) and inter-principle topology (CPC's mapping of where each fix should textually live). Most modifications are compositions, not retreats: adding PEG's artifact anchor to my MUST framing, adding CPC's deterministic-placement constraint to my storage-location fix, adding `SourceProvenance.filled_by` to my agent-naming fix.

The most significant change in my thinking is on **Recommendation 1** (the load-bearing P1). I framed it as a wording problem ("descriptive prose where MUST belongs"); PEG reframed it as a sequenced grounding problem ("the cache being described doesn't exist; the artifact is the mechanism"). Adopting only my framing would have locked in a constitutional obligation against a non-existent runtime cache, converting a documentation drift into a constitutional-violation backlog. The merged fix — name the artifact (`objective.yml`), use MUSTs, and sequence behind a code grep if the discipline is unverified — is materially stronger than either framing alone. I also updated my self-assessment of the "bit-for-bit" praise (review.md Alignment item): CPC and PEG both flagged that my praise was scope-ambiguous between stage 3 mechanical assembly (where "bit-for-bit" is the right level) and solver substitution (where "bit-for-bit" overclaims). The praise survives but is now scoped explicitly to stage 3.

The remaining highest-priority recommendation is the **VII ↔ XVI carve-out (Recommendation 3)**, jointly with the **MUST + artifact anchor (Recommendation 1, modified)** and the **new v2.3.2 Sync Impact Report (New Recommendation A)**. These three together turn v2.3.2 from a half-resolution of the VII contradiction into a clean, auditable, metadata-consistent amendment. The principle's existing strengths — the falsification clause (L496-498) and the explicit non-claim about LLM determinism (L493-495) — should not be touched by the surrounding tightening; both cross-reviewers and I agree these are the candidate's load-bearing precision wins.
