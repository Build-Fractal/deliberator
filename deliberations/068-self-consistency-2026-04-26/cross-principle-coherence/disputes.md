# Phase 4 Disputes — cross-principle-coherence

**Reviewer**: cross-principle-coherence
**Target**: `CONSTITUTION-v2.3.2-candidate.md`, Principle XVI
**Inputs read**: my Phase 3 revision, wording-precision (WP) Phase 3 revision, pr-evidence-grounding (PEG) Phase 3 revision

---

### Remaining Disputes

#### Dispute 1: Where the Principle XXIV cross-reference lands and what it obligates

- **My claim**: The XVI clarification block must contain an explicit Principle XXIV cross-reference that names the *re-resolution failure pattern* as the safety-critical contract test obligation. Without this cross-reference, the falsification clause (L496-498) lives in the wrong principle for enforcement weight — XXIV is the constitutional source of contract-test power and XVI must route through it.
- **Opposing position(s)**: PEG (Rec 10) treats the XXIV cross-reference as adequate with a generic parenthetical "(Principle XXIV's contract-test obligation applies to the within-run pinning invariant)" and pairs it with an out-of-band follow-up spec for the CI lint. WP (Rec 8) phrases it as routing through XXIV but explicitly notes "no within-run pinning test currently exists in `engine/tests/`" via my own Tension #1, treating the cross-reference as paper.
- **Why I will not concede**: PEG's softer phrasing leaves XXIV's three-layer requirement (schema-required, parser-validated, contract-tested) un-actuated. A bare "applies to" sentence does not name which of the three layers v2.3.2's pinning discipline must satisfy first, and XXIV's whole point is that all three are required. WP's note that the test does not yet exist *strengthens* my claim — the principle text must explicitly require a contract test reproducing the re-resolution-mid-run failure scenario, otherwise v2.3.2 codifies a falsification clause with no enforcement layer behind it.
- **Counter-argument**: Both opposing positions could argue that constitutional text should not over-specify enforcement mechanisms — that's spec/test work, not principle work. The reply: XXIV itself is principle-level enforcement specification; the parallel construction in XVI's clarification is required for symmetry with how XXII enforces distribution-surface integrity and how XXVI enforces meta-test coverage.
- **Proposed resolution path**: Adopt my Rec #3 modified text verbatim ("Enforcement: Principle XXIV applies — a contract test reproducing the re-resolution failure pattern is required (follow-up to spec 013 / spec 014 acceptance criteria)"). The phrase "reproducing the re-resolution failure pattern" is non-negotiable; the spec follow-up clause is negotiable.

#### Dispute 2: Whether the v2.3.2 clarification block carries a Principle II stable-interface anchor for `objective.yml`

- **My claim**: The clarification block must contain an explicit Principle II cross-reference declaring `objective.yml`'s schema (parameter names, keying, structure) a stable interface. Without II coverage, future changes to `objective.yml`'s shape become silent breakage paths — and PEG's grounding evidence shows `objective.yml` is precisely the artifact that bridges within-run pinning, cross-run reproducibility, and the III backward-compatibility extension surface.
- **Opposing position(s)**: PEG's New Rec 2 collapses II/X/XI into a single anchor sentence covering only X (findability) and XI (single source of truth), omitting the II stable-interface dimension. WP's modified Rec #6 names `objective.yml` as the storage location but does not lift it to II contract status, treating it as deterministic placement only.
- **Why I will not concede**: II and XI do different work. XI says "no duplicate sources of the same fact"; II says "this contract surface cannot be silently broken." `objective.yml`'s schema satisfies both, but only II creates the obligation that schema changes coordinate updates across all consumers (parsers, validators, downstream stages, plugin authors). Folding II into XI loses the coordination obligation. PEG's three-anchor merge is efficient but elides this distinction. WP's storage-only treatment is even narrower.
- **Counter-argument**: PEG could argue adding II adds clutter to a clarification block that is already absorbing five cross-references (VII, X, XI, XXIV, V). Reply: the block can be a sub-bulleted list rather than running prose; II is a one-line addition that prevents a category of future drift WP's grounding work will not detect.
- **Proposed resolution path**: Add to the v2.3.2 clarification a sub-bullet: "The `objective.yml` schema (parameter names, keying, and structure) is a Principle II stable interface; changes require coordinated update of all consumers." Place adjacent to the XI anchor, not folded into it.

#### Dispute 3: Whether the "mechanical assembly" → "deterministic assembly" reconciliation lands in XVI or VIII

- **My claim**: The reconciliation belongs in **Principle VIII** as a one-line parenthetical (my Rec #8 Option A), not in XVI's stage-3 label. VIII is the principle that introduced the "mechanical" vocabulary at L178; relabeling stage 3 inside XVI without touching VIII leaves VIII with the older term and creates a new drift between VIII's "mechanical" treatment and XVI's "deterministic" stage label.
- **Opposing position(s)**: Both WP (New Rec B) and PEG (Rec 3) prefer renaming stage 3 inside XVI to "Deterministic assembly" to match `construction.py:8-14` and spec 014 FR-012. WP's rationale: pick one term, document equivalence. PEG's rationale: vocabulary harmonization, the wording shift is constitutional alignment.
- **Why I will not concede**: WP and PEG are optimizing for codebase-text alignment; I am optimizing for principle-to-principle alignment. If stage 3 in XVI becomes "deterministic assembly," then VIII line 178 still says "Prefer mechanical template-driven behavior over LLM inference and improvisation" — and a future reader cannot tell whether VIII's "mechanical" subsumes XVI's "deterministic" or contradicts it. The principle-level term is "mechanical" (per VIII); XVI is a downstream consumer of that vocabulary. The fix should educate VIII about XVI's specific use of the term, not rename XVI's term and leave VIII unrevised.
- **Counter-argument**: Opposing reviewers could argue the codebase already uses "deterministic" and a future grep against `construction.py` for "mechanical" returns nothing — the practical drift is between code and constitution, not between principles. Reply: code-vs-constitution drift is fixable by a single comment in `construction.py`; constitution-vs-constitution drift is fixable only by amendment.
- **Proposed resolution path**: Adopt Option A from my Rec #8: add to Principle VIII line 178 the parenthetical "(In v2.3.2, Principle XVI uses 'mechanical' specifically for the post-pinning assembly stage — the term subsumes the determinism XVI describes.)" Leave XVI stage 3 labeled "Mechanical assembly." If WP/PEG insist on renaming, fall back to my Option B (equivalence note inside XVI) as a compromise that at least acknowledges the drift exists.

---

### Convergence

#### Converged 1: VII ↔ XVI carve-out lives in XVI's clarification, not amended into VII

- **Shared position**: The carve-out scoping VII's "structurally identical output" claim against XVI's LLM-resolved parameter values is authored *once* inside XVI's v2.3.2 clarification block, with a single back-reference parenthetical added to VII line 163. Co-authoring the carve-out into both principles violates Principle XI.
- **Agreeing agents**: All three (WP Rec 3 modified, my Rec #1 modified, PEG Rec 9 refined).
- **Strength**: Highest-strength convergence in the deliberation. Three independent reviewers, three different framings, identical destination.
- **Path**: WP authors the canonical carve-out text in XVI's clarification; I supply the back-reference parenthetical for VII line 163; PEG's user-facing example ("two `/conversus mode` invocations on the same `problem.md` MAY produce different `objective.yml` files") lands inside the carve-out paragraph as concretization.

#### Converged 2: Pinning is artifact-mediated via `objective.yml`, not via a runtime cache

- **Shared position**: The candidate's L463-466 phrase "cached values from the first resolution are reused" describes a runtime cache that does not exist in `conversus/schemas/construction.py`. The actual mechanism is artifact-based persistence via `objective.yml` (spec 014 FR-012). The MUST conversion must anchor to the artifact name, not an abstract "cache."
- **Agreeing agents**: All three (PEG Rec 2 strengthened, WP Rec 1 modified, my Rec #2 surviving-with-reframing). PEG sourced the grounding evidence; WP and I retroactively repaired our framings.
- **Strength**: High. PEG's evidence is dispositive — both WP and I conceded the phantom-cache problem in our cross-reviews.
- **Path**: Land PEG's combined edit phrasing: "Resolved parameter values **MUST** be persisted to `objective.yml` (spec 014 FR-012) for the duration of the deliberation run; the LLM **MUST NOT** be re-invoked for parameter resolution within the same run; values **MUST** be re-loaded from `objective.yml` rather than re-resolved." Add WP's "evidence-pending" hedge if a code grep before merge fails to verify the discipline is implemented.

#### Converged 3: The v2.3.2 Sync Impact Report is a P1 metadata gap

- **Shared position**: The candidate constitution's top-of-file SIR describes only v2.3.1 while the version footer says 2.3.2. This is a precision/audit-trail failure independent of principle text and must be fixed in the same PR.
- **Agreeing agents**: WP New Rec A (sourced) and PEG New Rec 1 (concurring). I missed it in original review and concur in revision.
- **Strength**: High. One-edit fix, no substantive disagreement.
- **Path**: Prepend a v2.3.2 SIR block above the v2.3.1 SIR. Document: (a) version 2.3.1 → 2.3.2 PATCH, (b) modified principle XVI, (c) effect on Principle VII (narrowed), (d) origin = spec 068 self-consistency deliberation, (e) verification status of the pinning discipline (audit result or "evidence-pending" hedge).

#### Converged 4: `SourceProvenance.filled_by` is the auditable hook for stage-2 pinning

- **Shared position**: The pinning discipline must reference `SourceProvenance.filled_by` (`construction.py:262-279`) as the existing data-structure hook that records who pinned each value. This is the difference between sanctioned explicit persistence (XVI) and the "ambient state or hidden context" that VII line 167 prohibits.
- **Agreeing agents**: PEG (Rec 6 / Tension #4 sourced), WP (Rec 10 modified), my Rec #4 (withdrawn-and-replaced; Rec #6 V-observability link).
- **Strength**: High. PEG's grounding work named the hook; WP and I integrated it from different angles (WP: agent-naming, mine: V-observability + VII boundary).
- **Path**: Add to clarification block: "The run orchestrator MUST persist resolved parameter values to `objective.yml`; pinning is auditable via `SourceProvenance.filled_by` — a sanctioned form of explicit, keyed persistence distinguished from the ambient state Principle VII line 167 prohibits." This sentence single-handedly satisfies VII boundary, V observability, and II/XI auditability.

#### Converged 5: "Deliberation run" is artifact-scoped, defined by `objective.yml` lifetime

- **Shared position**: The term "deliberation run" must be defined in v2.3.2 as the lifetime of one `objective.yml` artifact, not by-fiat. Retries that reuse the same artifact are part of the same run; separate `/conversus run` invocations producing new artifacts are different runs. Cross-version cache reuse is out of scope.
- **Agreeing agents**: WP Rec 2 modified (proposed), PEG Rec 5 strengthened (concurred), my NR-1 (out-of-scope statement).
- **Strength**: Medium-high. The artifact anchor is dispositive; the cross-version-replay scope statement is the lighter-weight piece.
- **Path**: Add to clarification block: "*deliberation run*: the lifetime of one `objective.yml` artifact; retries that reuse the same artifact are part of the same run, separate `/conversus run` invocations producing new artifacts are different runs. Cross-version replay (re-running after a `conversus` upgrade) is out of scope of this principle."

---

### Final Position Statement

#### Non-Negotiables

1. **The XXIV cross-reference must name the failure pattern, not just route to XXIV generically.** A bare "Principle XXIV applies" parenthetical is constitutionally inert. The clarification block must specify "a contract test reproducing the re-resolution failure pattern is required" — otherwise v2.3.2 ships a falsification clause with no enforcement layer, replicating the exact paper-rule failure XXIV exists to prevent.

2. **VII receives a back-reference parenthetical, not the full carve-out text.** Authoring the carve-out into both VII and XVI violates Principle XI (same fact in two places). The canonical text lives in XVI's v2.3.2 clarification; VII line 163 receives only "(narrowed by Principle XVI for LLM-resolved parameters; see XVI Clarification v2.3.2)". This is the single coordination point on which all three reviewers agree, and it must not regress under late editing pressure.

3. **`objective.yml` is the single named artifact bridging X, XI, II, and V.** All four principle cross-references anchor to this one artifact. If late editing tries to introduce a parallel name ("the cache," "the parameter store," "resolved-values.json"), reject it — drift between the principle text and PEG's grounding evidence (`construction.py`, spec 014 FR-012) reintroduces the phantom-cache problem this deliberation surfaced.

#### Flexibility

1. **Stage-3 vocabulary placement (XVI vs VIII) is negotiable.** I prefer the VIII parenthetical (my Rec #8 Option A) for principle-to-principle coherence; WP and PEG prefer renaming inside XVI for code-vocabulary alignment. Either lands the reconciliation. If synthesis chooses the XVI rename, I accept it on the condition that VIII line 178 receives at minimum a footnote acknowledging the term shift.

2. **The Principle II stable-interface sub-bullet (Dispute 2) can be deferred to a follow-up amendment.** My preference is to add it now (one line, no blocker), but if the synthesis judges the clarification block is at bloat capacity, II coverage of `objective.yml`'s schema can land in a v2.3.3 PATCH triggered by the first schema change. The XI anchor PEG and I agree on covers single-source-of-truth; II's coordination obligation becomes load-bearing only when the schema changes.

3. **The "evidence-pending" hedge is conditional on the code grep result.** WP and PEG both recognize this — if a pre-merge grep confirms the within-run pinning discipline is implemented in `construction.py` (`GapFiller.fill()` produces `objective.yml`, no re-invocation paths exist), the MUST conversion lands without hedge. If the grep is inconclusive or the discipline is partially implemented, the hedge is non-negotiable. The synthesis must record the grep result in the v2.3.2 SIR.
