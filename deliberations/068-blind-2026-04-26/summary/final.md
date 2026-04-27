# Spec 068 BLIND Verification — Synthesis

**Target**: Constitution v2.3.2-blind, Principle XVI (Mathematical Transparency)
**Methodology**: BLIND (agents reviewed without knowing which principles are recent)
**Mode**: Cooperative
**Agents**: skeptic-mathematical, skeptic-cross-principle, practitioner
**Date**: 2026-04-26

---

## Process Summary

| Metric | Count |
|---|---|
| Agents | 3 |
| Phases run | 4 (Phase 1 review → Phase 2 cross-review → Phase 3 revision → Phase 4 disputes) |
| Total artifacts | 15 (3 reviews + 6 cross-reviews + 3 revisions + 3 disputes) |
| Phase 1 reviews | 3 |
| Phase 2 cross-reviews | 6 (each agent cross-reviewed the other two) |
| Phase 3 revisions | 3 |
| Phase 4 disputes | 3 |
| Recommendations proposed (Phase 1) | 30 (10 each from skeptic-mathematical, skeptic-cross-principle, practitioner) |
| Recommendations withdrawn (Phase 3) | 7 (skeptic-math: 4, 5, 7, 10; practitioner: 5, 7) — also skeptic-cross-principle Rec 10 folded |
| Recommendations modified (Phase 3) | 9 (skeptic-math: 1, 2, 3, 6; skeptic-cross-principle: 1, 5, 6, 7, 9; practitioner: 1, 3, 4, 6) |
| Recommendations surviving unchanged (Phase 3) | 5 (skeptic-math: 8, 9; skeptic-cross-principle: 2, 4, 8; practitioner: 2, 8, 9) |
| New recommendations added (Phase 3) | 8 (skeptic-math: A, B; skeptic-cross-principle: 1, 2, 3; practitioner: 11, 12, 13) |
| Final disputes remaining (Phase 4) | 4 unique disputes (structural fork; test-contract sequencing; cross-reference graph asymmetry; XXIV scope residual) |
| Convergence points | 5 unanimous + 2 bilateral-with-non-objection |

**Blind methodology note**: All findings concentrated on Principle XVI as instructed by the focus prompt. No incidental findings on other principles surfaced as standalone recommendations, though XVI's findings necessarily implicated **Principles VII, V, II, XI, IV, XV, XXIV** as cross-reference targets. These cross-principle implications are XVI-driven (in scope) rather than independent findings on those principles (out of scope).

---

## Recommendation Scorecard

| # | Agent | Recommendation | P1 Priority | P3 Disposition | Challenged By | Convergence | Final Status |
|---|---|---|---|---|---|---|---|
| 1 | skeptic-mathematical | Split XVI into XVI-A (transparency) and XVI-B (pinning discipline) | P1 | Modified | skeptic-cross-principle Tension #1; practitioner Tension #1 | Sequenced as analytic decomposition, no new principle numbers | **Accepted-Modified** |
| 2 | skeptic-mathematical | Move determinism claims to Principle VII; defer to it | P1 | Modified | skeptic-cross-principle Dangerous Contradiction #1; practitioner Dangerous Contradiction #2 | Bilateral cross-reference, inline (no `references/` redirect) | **Accepted-Modified** (rolled into Convergence 1) |
| 3 | skeptic-mathematical | Replace MUST/MUST NOT with test contract reference | P1 | Modified | skeptic-cross-principle Dangerous Contradiction #3 (XXIV scope); practitioner Tension #4 (test doesn't exist) | Generic test clause, no XXIV citation, aspirational caveat OR same-PR OR spec-013-routed | **Disputed** (sequencing) |
| 4 | skeptic-mathematical | Specify cache key tuple `(template_id, template_version, gap_identifier, user_answer_hash)` | P2 | Withdrawn | skeptic-cross-principle Tension #2 (constitutional overreach) | — | **Rejected** |
| 5 | skeptic-mathematical | Address LLM temperature/seed in constitutional prose | P2 | Withdrawn | skeptic-cross-principle Tension #3 (VIII inversion) | — | **Rejected** |
| 6 | skeptic-mathematical | Define audience for "transparency" as spec author | P2 | Modified | skeptic-cross-principle Dangerous Contradiction #4 (contradicts IV); practitioner Dangerous Contradiction #3 (revokes user promise) | Two audiences retained (template legibility = spec-author; runtime output = end-user) | **Accepted-Modified** |
| 7 | skeptic-mathematical | Acknowledge pinning trade-off (freshness vs reproducibility) | P2 | Withdrawn | practitioner Tension #3 (scope creep, feature-spec content) | — | **Rejected** |
| 8 | skeptic-mathematical | Add template-versioning to cross-run reproducibility claim | P2 | Surviving (scope expanded) | None contested; practitioner Phase 3 New Rec 13 reinforced | Lands in VII as broader (config, template registry, capability registry) precondition | **Accepted-Modified** (rolled into Convergence 4) |
| 9 | skeptic-mathematical | Reconcile plugin-explanation clause with Principle XV | P3 | Surviving | None | One-line cross-reference distinguishing XVI's content rule from XV's isolation rule | **Accepted** |
| 10 | skeptic-mathematical | Consider removing XVI entirely | P3 | Withdrawn | practitioner Dangerous Contradiction #1 (loses gate); skeptic-cross-principle Dangerous Contradiction #2 (XII violation, strands specs 012-019) | — | **Rejected** (Convergence 3) |
| A | skeptic-mathematical (NEW) | Define "pinning" as term-of-art in II's stable-interface vocabulary | P2 | Surviving | None | Glossary entry in II + V-emission cross-reference | **Accepted** (rolled into Convergence 7) |
| B | skeptic-mathematical (NEW) | Soften solver-substitution claim to semantic | P2 | Surviving | None | Unanimous adoption | **Accepted** (Convergence 2) |
| 1 | skeptic-cross-principle | Merge XVI into VII as extension | P1 | Softened to "merge OR demote, after decomposition" | skeptic-mathematical Dangerous Contradiction #1; practitioner Dangerous Contradiction #1 | Sequenced (split → relocate → cross-reference → absorb) | **Disputed** (structural fork) |
| 2 | skeptic-cross-principle | Narrow XVI to transparency-only as alternative | P1 | Kept (demoted to fallback) | None | Becomes natural disposition for transparency fragment if absorbed | **Accepted-Modified** |
| 3 | skeptic-cross-principle | Add VII↔XVI back-reference | P1 | Kept, strengthened | None — all three reviewers reinforced | Mandatory regardless of structural choice | **Accepted** (Convergence 1) |
| 4 | skeptic-cross-principle | Pick one term ("mechanical" vs "deterministic") aligned with VIII | P1 | Kept, sharpened | None | Stages 1, 3 use "deterministic"; "mechanical" reserved for VIII's antonym-of-inference sense | **Accepted** |
| 5 | skeptic-cross-principle | Define "pinning" as constitutional term in II | P2 | Kept, extended with test-contract spine | skeptic-mathematical Dangerous Contradiction #3 (terminology hardens, behavior remains soft) | Glossary in II + test contract reference in spec 013 | **Accepted-Modified** (Convergence 7) |
| 6 | skeptic-cross-principle | XVI ↔ V interaction clause (pinned values must be emitted) | P2 | Kept, strengthened | None — practitioner Phase 3 New Rec 11 adopted explicitly | Pinned values MUST be emitted under V's progress contract | **Accepted** (Convergence 5) |
| 7 | skeptic-cross-principle | XVI ↔ XXIV interaction clause | P2 | Kept, narrowed | skeptic-mathematical (their Phase 2 cross-review noted XXIV doesn't auto-generalize) | Restricted to optimization-driven outputs consumed by synthesis-verdict generation | **Disputed** (residual coverage gap) |
| 8 | skeptic-cross-principle | Soften solver-substitution claim | P2 | Kept, no change | None | Unanimous adoption | **Accepted** (Convergence 2) |
| 9 | skeptic-cross-principle | Generalize away from 3-stage pipeline; relocate to spec 013 | P2 | Kept with practitioner's relocation refinement (no property-form residue) | practitioner Dangerous Contradiction #2 (relocate vs property-form) | Pipeline description leaves XVI entirely; spec 013 owns it | **Accepted-Modified** (Convergence 6) |
| 10 | skeptic-cross-principle | Consider removing XVI entirely | P3 | Withdrawn (folded into Rec 1's decomposition path) | skeptic-cross-principle's own cross-review of skeptic-mathematical (XII violation) | — | **Rejected** (Convergence 3) |
| 1 | skeptic-cross-principle (NEW) | Sequence the disposition: split → relocate → cross-reference → absorb | — | Surviving | practitioner Tension (operational diffuseness) | Synthesizer must pick the structural endpoint, not just sequence | **Disputed** (structural fork) |
| 2 | skeptic-cross-principle (NEW) | Add audience disambiguation clause | — | Surviving | None | Plain-language explanations target end user; spec-author concerns governed by IV | **Accepted** |
| 3 | skeptic-cross-principle (NEW) | Treat "Mathematical Transparency" name as load-bearing remediation target | — | Surviving | practitioner (weakly held; would not block) | Rename if pinning fragment lives elsewhere; "Mathematical Transparency" acceptable if only transparency residual survives | **Accepted-Modified** (deferred per disputes) |
| 1 | practitioner | Rewrite XVI as 4-6 operational lines focused on parameter-pinning | P1 | Kept, slightly revised | skeptic-cross-principle (sequenced fork); skeptic-mathematical (no new numbers but absorb where possible) | Tight-standalone XVI is one option; deferred to synthesizer | **Disputed** (structural fork) |
| 2 | practitioner | Replace within-run/cross-run terminology with operational language | P1 | Kept | skeptic-cross-principle (academic vocabulary IS XVI's contribution) | Operational reframe holds; "called at most once per parameter per run; cached for the rest" | **Disputed** (vocabulary form, low-stakes) |
| 3 | practitioner | Resolve VII↔XVI cross-run reproducibility tension | P1 | Kept, sharpened | skeptic-mathematical (template versioning gap) | VII gains pre-condition tuple; XVI cross-references VII | **Accepted-Modified** (rolled into Convergence 4) |
| 4 | practitioner | Add verification mechanism (contract test) | P1 | Kept, sequenced | skeptic-mathematical (test doesn't exist; aspirational framing better) | Same-PR mandate vs aspirational vs spec-013-routed | **Disputed** (sequencing) |
| 5 | practitioner | Move plain-language rule into Principle X | P2 | Withdrawn | skeptic-cross-principle (X = output formatting, IV = spec product, would scatter rule) | — | **Rejected** |
| 6 | practitioner | Move template-documentation rule into spec 013 | P2 | Kept, narrowed | None | Form lives in spec 013; invariant stays in XVI | **Accepted** |
| 7 | practitioner | Consider removing XVI entirely | P2 | Withdrawn | skeptic-cross-principle (loses VII-exception); skeptic-mathematical (loses operational gate) | — | **Rejected** (Convergence 3) |
| 8 | practitioner | Rename XVI ("Pinned Parameter Discipline" / "Optimization Reproducibility Contract") | P3 | Kept, weakly | None | Conditional on structural outcome; rename if transparency leaves | **Accepted-Modified** |
| 9 | practitioner | CI hook for template description fields | P3 | Kept | None | Linter complements plain-language rule | **Accepted** |
| 10 | practitioner | Cross-reference VII↔XVI | P3 | Kept, expanded | None | Adopted skeptic-cross-principle's "sole sanctioned exception" wording | **Accepted** (Convergence 1) |
| 11 | practitioner (NEW) | Add V-emission clause to XVI | — | Surviving | None — adopted from skeptic-cross-principle's Phase 1 review | XVI cross-references V; pinned values emitted as `optimization/pinned_parameters.yml` or equivalent | **Accepted** (Convergence 5) |
| 12 | practitioner (NEW) | Soften solver-substitution per skeptic-cross-principle | — | Surviving | None | Unanimous adoption | **Accepted** (Convergence 2) |
| 13 | practitioner (NEW) | Anchor template-version dependency in VII | — | Surviving | None | Broader form: (config, template registry, capability registry) | **Accepted** (Convergence 4) |

---

## Dangerous Contradictions Found

### Resolved Contradictions

1. **"Move determinism to VII via `references/` doc" vs. "Inline in VII"**
   - **What**: skeptic-mathematical's Phase 1 Rec 2 proposed redirecting XVI's determinism block to a `references/parameter-resolution.md` file that does not exist.
   - **Who conceded**: skeptic-mathematical (Phase 3 modified Rec 2). Resolution: bilateral inline cross-reference in VII and XVI, no `references/` redirect.
   - **Resolution**: Both critics (skeptic-cross-principle Phase 2, practitioner Phase 2) flagged that pointing at a non-existent doc degrades constitutional weight; skeptic-mathematical accepted "the move must be bilateral and inline."

2. **"Remove XVI entirely" (proposed by all three)**
   - **What**: All three reviewers proposed removal as a Phase 1 backstop (skeptic-mathematical Rec 10, skeptic-cross-principle Rec 10, practitioner Rec 7).
   - **Who conceded**: All three withdrew in Phase 3.
   - **Resolution**: Two converging dangerous contradictions killed the option — (a) practitioner: removing XVI loses the *one* operationally crisp gate against re-resolving parameters mid-run; (b) skeptic-cross-principle: specs 012-019 reference Principle XVI by number, removing it strands them as a textbook XII (No Dead Infrastructure) violation.

3. **"Narrow audience to spec author" vs. "user-facing transparency promise"**
   - **What**: skeptic-mathematical's Phase 1 Rec 6 proposed narrowing XVI's audience to spec authors and outsourcing end-user transparency to Principle IV.
   - **Who conceded**: skeptic-mathematical (Phase 3 modified Rec 6).
   - **Resolution**: skeptic-cross-principle's Phase 2 Dangerous Contradiction #4 (IV is about prose-as-product, not runtime output legibility) and practitioner's Phase 2 Dangerous Contradiction #3 (silently revokes user-facing promise that the plain-language clause depends on) converged. New disposition retains both audiences with distinct surfaces.

4. **"Cache key tuple in constitution" vs. "constitution legislates vocabulary, not schemas"**
   - **What**: skeptic-mathematical's Phase 1 Rec 4 specified a four-field cache key tuple in constitutional prose.
   - **Who conceded**: skeptic-mathematical (Phase 3 withdrew Rec 4).
   - **Resolution**: skeptic-cross-principle's Phase 2 Tension #2 named this an III/VI violation (constitutions describe contracts, implementations evolve). Cache contract relocated to spec 013; II glossary holds the term-of-art.

5. **"LLM temperature/seed as constitutional prose" vs. "VIII treats LLM as last resort"**
   - **What**: skeptic-mathematical's Phase 1 Rec 5 proposed encoding temperature/seed choices in XVI.
   - **Who conceded**: skeptic-mathematical (Phase 3 withdrew Rec 5 explicitly as "an unforced error").
   - **Resolution**: skeptic-cross-principle's Phase 2 Tension #3 noted this elevates LLM API artifacts to first-class constitutional vocabulary, the inversion VIII resists.

6. **"XXIV pattern wholesale-imported into XVI" vs. "XXIV scoped to synthesis verdicts"**
   - **What**: skeptic-mathematical's Phase 1 Rec 3 cited XXIV's "schema + parser + reproducing test" pattern as the model XVI should follow.
   - **Who conceded**: skeptic-mathematical (Phase 3 modified Rec 3) — kept the *intent* but dropped the XXIV citation.
   - **Resolution**: skeptic-cross-principle's Phase 2 Dangerous Contradiction #3 noted this either silently expands XXIV's scope or creates a parallel doctrine (XI violation). New disposition: generic test-contract clause without XXIV citation.

7. **"Solver substitution promises numerical equivalence" vs. "two solvers cannot deliver bit-identical output"**
   - **What**: skeptic-cross-principle Phase 1 Rec 8 (also flagged in their Phase 2 cross-review of practitioner) noted current wording promises what no solvers can deliver.
   - **Who conceded**: All three reviewers adopted skeptic-cross-principle's softening.
   - **Resolution**: New unanimous wording: "Changing solvers MUST NOT change the objective function expression or its parameter semantics. Numerical results may differ within solver-tolerance bounds; the objective function is the contract, not the solver's output."

### Unresolved Contradictions

1. **Structural fork (collapse vs. decompose-and-redistribute vs. tightened-standalone)** — see Remaining Disputes below.
2. **Test-contract sequencing (same-PR mandate vs. aspirational vs. spec-013-routed)** — see Remaining Disputes below.
3. **Cross-reference graph asymmetry (which node owns which edge)** — see Remaining Disputes below.
4. **XXIV scope narrowing residual coverage gap** — see Remaining Disputes below.

---

## Systemic Contradictions

### Pattern 1: Constitutional density vs. cross-reference debt
- **Manifests in**: Structural fork dispute; "fold into IV/X/VII vs. keep XVI as numbered" tension across all three reviewers; rename question.
- **Root cause**: The constitution has accumulated 27 principles, and XVI bundles three independent claims under one heading. Reducing XVI's surface (practitioner direction) reduces principle count but increases coupling between the surviving sentence and existing principles. Decomposing XVI (skeptic-cross-principle direction) preserves clean fail-attribution but multiplies cross-reference edges. There is no Pareto-optimal fix.
- **Implication**: The synthesizer MUST pick a structural endpoint rather than letting all three Phase 3 revisions land independently. Three different terminal states (tight-standalone XVI, decompose-and-redistribute, freestanding-pinning-plus-IV-absorption) interact differently with V/XV/XXIV.

### Pattern 2: Constitution-vs-implementation abstraction boundary
- **Manifests in**: Cache key tuple withdrawal (Rec 4); LLM temperature/seed withdrawal (Rec 5); 3-stage pipeline relocation (Rec 9); test-contract sequencing dispute.
- **Root cause**: Multiple Phase 1 recommendations imported implementation contracts into constitutional prose. Both critics consistently caught this and pushed the content downstream (spec 013, references, tests). The corrective move is uniform: constitution legislates vocabulary and contracts; implementation schemas live in specs.
- **Implication**: Future amendments to XVI should default to spec-013-routing for any concrete artifact (cache keys, test names, LLM API configurations, pipeline stage descriptions).

### Pattern 3: Aspirational principle vs. enforceable contract
- **Manifests in**: Test-contract sequencing dispute; "MUST/MUST NOT without enforcement mechanism" critique (practitioner Phase 1 Missed Opportunity #5); pinning glossary debate.
- **Root cause**: XVI uses MUST language for behavior the constitution itself cannot enforce. XXII, XXIII, XXIV, XXVI, XXVII all anchor MUST-language to verifiable artifacts (CI tests, schema validation, parametrized meta-tests). XVI does not.
- **Implication**: Convergent fix is unanimous (test-contract reference required); divergent fix is sequencing (same-PR vs. aspirational caveat vs. spec-013-routed). The synthesizer must pick a sequencing model that respects both XII (no dead infrastructure) and the practical separation between governance PRs and implementation PRs.

### Pattern 4: Single-source-of-truth applied to constitutional prose itself
- **Manifests in**: VII↔XVI determinism overlap (Convergence 1); X↔XVI plain-language overlap; IX↔XVI explicit-typing overlap; II as glossary host for "pinning."
- **Root cause**: Principle XI (Single Source of Truth) governs information that has multiple representations. The reviewers consistently applied XI to constitutional text itself: when two principles claim overlapping territory, the constitution has the same drift problem the principles warn against in code.
- **Implication**: Bilateral cross-references (VII↔XVI; II↔XVI; V↔XVI; XXIV↔XVI) are the systemic remedy. The convergent direction across all three reviewers is "name the dependency explicitly, place each fact in one home, cross-reference from the others."

### Pattern 5: Defensive amendment as evidence of incomplete derivation
- **Manifests in**: All three reviewers identified XVI's "Clarification: determinism scope" block (lines 469–476) as a "tell" that the principle did not land cleanly the first time.
- **Root cause**: Post-hoc clarification blocks paper over principle conflicts rather than resolving them structurally. The Sync Impact Report shows XVI is *not* in the v2.3.0 amendment list (lines 1–38), supporting the hypothesis that the clarification was added separately.
- **Implication**: Future principles should not require titled clarification footnotes; if the principle's prose needs a footnote to explain what it claims, the principle has not yet landed. Rewrite to make the clarification unnecessary.

---

## Convergence Achieved

### Convergence 1 (Unanimous, Pre-existing Phase 1 → Earned Phase 4): VII↔XVI bilateral cross-reference is the highest-leverage edit
- **Agreed recommendation**: VII MUST append: "Principle XVI defines the sole sanctioned exception, scoped to LLM-mediated parameter resolution under within-run pinning discipline." XVI MUST open with "Subject to Principle VII, …".
- **Supporting agents**: skeptic-mathematical (revised Rec 2), skeptic-cross-principle (revised Rec 3, strengthened), practitioner (revised Rec 10, expanded).
- **Evidence basis**: All three Phase 1 reviews independently identified VII↔XVI as the load-bearing tension; all three Phase 4 disputes confirm "non-negotiable" or "the highest-leverage edit." Wording is settled.
- **Earned**: Yes — Phase 1 had three different framings ("move to VII" / "merge into VII" / "cross-reference VII"); Phase 3 settled on bilateral inline cross-reference.

### Convergence 2 (Unanimous, Earned Phase 3): Solver-substitution wording softens to semantic
- **Agreed recommendation**: Replace "Changing solvers MUST NOT change what is being optimized" with "Changing solvers MUST NOT change the objective function expression or its parameter semantics. Numerical results may differ within solver-tolerance bounds; the contract is on the function, not the solver's output."
- **Supporting agents**: skeptic-cross-principle (Original Rec 8, no change), skeptic-mathematical (New Recommendation B, surfaced after Phase 2 cross-review concession), practitioner (New Rec 12, adopted from skeptic-cross-principle).
- **Evidence basis**: skeptic-mathematical's Phase 1 alignment celebrated solver/objective separation; their Phase 2 cross-review of skeptic-cross-principle conceded "the conservative reading should win"; practitioner's Phase 3 revision explicitly adopted skeptic-cross-principle's wording.
- **Earned**: Yes — Phase 1 had two readings (numerical vs semantic); Phase 3 unified on semantic.

### Convergence 3 (Unanimous, Pre-existing Phase 1 → Earned Phase 3): Removing XVI is off the table
- **Agreed recommendation**: XVI stays as a numbered principle in some form. Removal would (a) discard the one operationally crisp gate against re-resolving parameters mid-run that VII/IV/X do not catch, and (b) strand specs 012-019 with dangling Principle-XVI pointers (XII violation).
- **Supporting agents**: skeptic-mathematical (withdrew Rec 10), practitioner (withdrew Rec 7), skeptic-cross-principle (withdrew Rec 10 / folded into decomposition path).
- **Evidence basis**: practitioner's Phase 2 Dangerous Contradiction #1 (loses gate); skeptic-cross-principle's Phase 2 Dangerous Contradiction #2 (XII violation).
- **Earned**: Yes — all three Phase 1 reviews proposed removal as a backstop; all three Phase 3 revisions withdrew.

### Convergence 4 (Bilateral with non-objection, Earned Phase 3): Template/registry versioning belongs in VII
- **Agreed recommendation**: VII MUST add "Reproducibility is conditional on (config, template registry, capability registry) being byte-identical between runs. Changes to any of these constitute a different input set." XVI cross-references VII's expanded clause rather than carrying its own version provision.
- **Supporting agents**: skeptic-mathematical (surviving Rec 8, scope expanded), practitioner (New Rec 13, broader form). skeptic-cross-principle did not contest in Phase 3 disputes.
- **Evidence basis**: skeptic-mathematical caught the gap in Phase 1; practitioner's Phase 3 revision explicitly conceded "skeptic identifies that cross-run reproducibility silently breaks when templates are edited. This is real and my review missed it"; broader form (capability registry per practitioner New Rec 13) supersedes narrower (template_version only per skeptic-mathematical) without contradiction.
- **Earned**: Yes — only skeptic-mathematical surfaced this in Phase 1; consensus reached in Phase 3.

### Convergence 5 (Unanimous, Earned Phase 3): V-emission of pinned parameter values is required
- **Agreed recommendation**: Pinned parameter values MUST be emitted as deliberation output (e.g., `optimization/pinned_parameters.yml`) under V's "every phase MUST report progress" contract.
- **Supporting agents**: skeptic-cross-principle (Phase 1 Missed Opportunity #5, strengthened in Phase 3 Rec 6), practitioner (Phase 3 New Rec 11 adopted explicitly), skeptic-mathematical (Phase 2 cross-review explicitly conceded "I did not connect XVI to V at all — their cross-principle audit caught something my logical-coherence audit missed").
- **Evidence basis**: skeptic-mathematical originally missed V; skeptic-cross-principle surfaced it; practitioner originally missed V (called out in skeptic-cross-principle's Phase 2 cross-review of practitioner) and adopted in Phase 3.
- **Earned**: Yes — only skeptic-cross-principle had it in Phase 1; unanimous by Phase 3.

### Convergence 6 (Unanimous, Earned Phase 3): 3-stage pipeline description leaves the constitution
- **Agreed recommendation**: The 3-stage pipeline description MUST be relocated from XVI to spec 013. XVI does not narrate the pipeline at any altitude (no property-form residue).
- **Supporting agents**: skeptic-cross-principle (Phase 1 Rec 9, refined Phase 3 with practitioner's relocation point), practitioner (Phase 1 Missed Opportunity #1, narrowed in Phase 3 Rec 6), skeptic-mathematical (Phase 3 modified Rec 1 endpoint).
- **Evidence basis**: All three reviewers identified the pipeline description as implementation documentation, not constitutional content. skeptic-cross-principle's Phase 3 explicitly converged on practitioner's relocation framing over their own property-form preservation.
- **Earned**: Yes — Phase 1 had two framings (skeptic-cross-principle: property-form residue; practitioner: physical relocation); Phase 3 unified on physical relocation.

### Convergence 7 (Bilateral with non-objection, Earned Phase 3): "Pinning" gets a constitutional definition in II + spec-013-routed contract test
- **Agreed recommendation**: Define "pinning" in II's stable-interface vocabulary as "a parameter value committed to a run-scoped store, immutable for the duration of the run, with invalidation policy specified in spec 013." XVI references the term-of-art; cache contract lives in spec 013; XVI also references a contract test in spec 013 that asserts no within-run drift.
- **Supporting agents**: skeptic-cross-principle (Rec 5 extended), skeptic-mathematical (New Recommendation A added in Phase 3 after conceding cache-tuple overreach). practitioner did not contest.
- **Evidence basis**: skeptic-cross-principle surfaced terminology gap; skeptic-mathematical pushed back on cache-contract overreach but conceded the underlying terminology gap; Phase 3 compromise puts vocabulary in II and contract in spec 013, preserving the abstraction boundary.
- **Earned**: Yes — Phase 1 had glossary-only (skeptic-cross-principle) vs. cache-tuple-in-constitution (skeptic-mathematical); Phase 3 split: vocabulary in II, contract in spec 013.

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes

#### Dispute: Structural fork (collapse vs. decompose-and-redistribute vs. tightened-standalone)

- **Positions**:
  - **practitioner** — keep XVI as a tight standalone principle (4–6 operational lines), with parameter-pinning rule and plain-language rule co-located; one numbered principle, one location, one PR-review checklist item. Will accept skeptic-mathematical's "no new principle numbers, transparency stays inline" as the convergence point.
  - **skeptic-cross-principle** — execute four-step sequence (split → relocate → cross-reference → absorb): transparency fragment lands in IV; pinning fragment folded into VII as named extension OR kept freestanding under tighter name. Treats this as the canonical path.
  - **skeptic-mathematical** — analytic decomposition along transparency/determinism/pinning axis, but no new principle numbers. Most likely outcome: transparency stays inline as XVI's surviving kernel; determinism cross-references VII; pinning collapses to one operational sentence with test contract. Tightened-standalone effectively, framed analytically.
- **Arguments**:
  - practitioner: constitutional density has real ergonomic cost; a reviewer reading a PR diff that touches optimization parameters needs to land on *one* checklist, not chase clauses across IV, VII, spec 013. The transparency rule and the pinning rule protect the same user-facing promise; co-locating them aids review.
  - skeptic-cross-principle: "Mathematical Transparency" name is too broad; its breadth *enabled* the bundling defect. The sequenced path (split → relocate → cross-reference → absorb) is constitutionally cleaner; each fragment finds its natural home; cross-references make dependencies explicit.
  - skeptic-mathematical: tightened-standalone preserves the "one operationally crisp gate" practitioner valued; absorbing pinning into VII as a "named extension" puts the gate inside a principle whose lead sentence is "Deterministic orchestration is non-negotiable" — dilutes visibility for the most likely reader. But agrees the name is a remediation target.
- **Synthesizer assessment** (editorial judgment):
  - The dispute is genuinely live. All three reviewers privately predict the structural disposition; none commits unconditionally. The lowest-risk path is the practitioner's "tight standalone XVI" outcome, because it (a) preserves the operationally crisp gate inline, (b) avoids the spec-redirect cleanup that absorption requires for specs 012-019, and (c) respects the convergence-floor edits (VII↔XVI cross-reference, V-emission, II glossary) which all three reviewers agreed land regardless of structural form.
  - skeptic-mathematical's "no new principle numbers, transparency stays inline" outcome is functionally equivalent to practitioner's tight-standalone but framed as the result of analytic decomposition rather than as a starting position. Practitioner explicitly accepts this as the convergence point. This is the strongest available consensus.
  - skeptic-cross-principle's full four-step decomposition lacks practitioner buy-in and adds cross-reference debt that the tighter outcome avoids. Their Phase 4 disputes acknowledge: "I now treat this as a synthesizer decision rather than a Devil's-Advocate hill — the cross-references in Non-Negotiables 1 and 2 land regardless of which structural form survives."
- **Recommended resolution**: Adopt the **tightened-standalone XVI** endpoint that emerges from skeptic-mathematical's analytic decomposition. XVI shrinks to ~4-8 lines containing: (a) opening "Subject to Principle VII, …" cross-reference, (b) parameter-pinning operational sentence (called at most once per parameter per run), (c) plain-language requirement for plugin/optimization output, (d) solver-substitution semantic invariant (softened wording), (e) cross-reference to V for pinned-value emission, (f) reference to II's "pinning" glossary entry, (g) reference to spec 013 for pipeline description and contract test. The 3-stage pipeline narration leaves XVI entirely. Rename to "Pinned Parameter Discipline" or similar IF the transparency clause also leaves; otherwise "Mathematical Transparency" remains acceptable.

#### Dispute: Test-contract sequencing (same-PR mandate vs. aspirational caveat vs. spec-013-routed)

- **Positions**:
  - **practitioner** (revised Rec 4) — same-PR mandate: "The PR amending XVI MUST also add `tests/test_parameter_pinning.py::test_no_within_run_drift` (or equivalent name) and the principle text MUST reference the test by path." Constitutional pointer to a missing artifact violates XII (No Dead Infrastructure).
  - **skeptic-mathematical** (modified Rec 3) — aspirational framing: "Until that test exists, this principle is aspirational; first PR adding the test removes the aspirational caveat." Decouples constitutional amendment (governance-weighted) from test design (engineering-weighted).
  - **skeptic-cross-principle** (revised Rec 5) — spec-013-routed: "XVI MUST reference a contract test in spec 013 that asserts no within-run drift. The cache key schema itself stays in spec 013, not constitutional prose." Routes through spec 013 indirection.
- **Arguments**:
  - practitioner: aspirational caveat itself is a tell that the pointer is a false promise; XII prohibits dead infrastructure. Same-PR mandate makes the gate real.
  - skeptic-mathematical: bundling constitutional amendment with test-implementation creates a PR needing both quorum sign-off on governance change AND code review on test design; failure mode is disagreement on test design blocking constitutional clarification.
  - skeptic-cross-principle: most internally consistent with constitution's existing spec-vs-implementation abstraction layer; constitution already routes through spec 013 for cache-contract content.
- **Synthesizer assessment**: skeptic-cross-principle's spec-013-routed shape is the strongest. It (a) avoids the same-PR governance/engineering coupling that skeptic-mathematical correctly identified as risky, (b) avoids the dead-infrastructure pattern practitioner correctly identified as forbidden, (c) leverages the spec-013 indirection the constitution already uses for cache-contract content. The constitutional text says "see spec 013's parameter-pinning contract test"; spec 013's existence (not a specific test file path) is the artifact dependency. The synthesizer should also note skeptic-mathematical's Phase 4 closing observation that this converges practitioner's same-PR mandate with their decoupling concern by making the dependency *spec 013 ships first*, not *test ships in same PR as constitution*.
- **Recommended resolution**: Adopt **shape C (spec-013-routed)**. XVI's text references spec 013's parameter-pinning contract test. Spec 013 must exist with the contract test before the constitutional amendment merges. Test name and path live in spec 013; constitutional pointer is generic but enforceable through spec 013's existence requirement.

#### Dispute: Cross-reference graph asymmetry (which node owns which edge)

- **Positions**:
  - **skeptic-cross-principle** (Phase 4 Dispute 2) — flagged that the convergent edits create a star graph centered on VII for some edges (template versioning, capability registry) and centered on XVI for others (V-emission, XXIV-synthesis). The three revisions never reconcile the centring choice. If template versioning lands in VII and V-emission lands in XVI, then XVI's V-emission depends on VII's reproducibility pre-conditions being satisfied — but neither revision states the dependency.
  - **skeptic-mathematical** and **practitioner** — did not surface this as a separate dispute; both treated each cross-reference edit as independent.
- **Arguments**:
  - skeptic-cross-principle: a future spec author editing a template breaks VII's reproducibility, which silently invalidates XVI's V-emission as an audit artifact (the emitted pinned values no longer correspond to the run that produced them). The cross-reference edges need to compose correctly.
- **Synthesizer assessment**: This is a real residual gap surfaced only by skeptic-cross-principle's Phase 4 audit. The other two reviewers did not contest it (silent, not opposed). The fix is straightforward: the V-emission clause (wherever it lands) MUST cross-reference VII's reproducibility pre-conditions, so a reader understands that observable pinned values depend on (config, template registry, capability registry) being byte-identical for the audit to be meaningful.
- **Recommended resolution**: Add to XVI's V-emission clause: "Pinned parameter values MUST be emitted as deliberation output under V's progress-reporting contract, subject to VII's reproducibility pre-conditions (config, template registry, capability registry byte-identical between runs)." This wires the V/XVI/VII edges into one composed rule.

#### Dispute: XXIV scope narrowing (residual coverage of optimization → synthesis-verdict path)

- **Positions**:
  - **skeptic-cross-principle** (Phase 4 Dispute 4, narrowed Rec 7) — restricted XVI/XXIV interaction to "optimization-driven outputs consumed by synthesis-verdict generation." Acknowledged residual gap: optimization that does NOT feed synthesis verdicts is now under XVI/VII alone, with no defense-in-depth requirement. Optimization output authored before it becomes synthesis-bearing is not retroactively covered by XXIV.
  - **skeptic-mathematical** (modified Rec 3) — dropped XXIV citation entirely in favor of generic test-contract clause.
  - **practitioner** — did not address XXIV in disputes; deliberately stayed at V/VII surface.
- **Arguments**:
  - skeptic-cross-principle: narrowing is constitutionally clean but operationally fragile — relies on spec authors knowing in advance whether optimization output will eventually feed a synthesis verdict.
  - skeptic-mathematical: XXIV's "schema + parser + reproducing test" pattern is *scoped* to synthesis verdicts and provider protocols; re-purposing it for optimization parameter pinning silently expands XXIV's safety-critical scope or creates parallel doctrine (XI violation).
- **Synthesizer assessment**: The disagreement is small in operational impact. skeptic-cross-principle's narrowed Rec 7 and skeptic-mathematical's drop-XXIV-in-favor-of-generic-test-contract reach functionally similar endpoints. The residual coverage gap is real but is a downstream evolution concern, not a v2.3.3 blocker. skeptic-cross-principle's own Phase 4 explicitly marks this as flexible: "Either disposition is constitutionally defensible; I prefer the narrowing because it preserves XXIV's scoped authority, but I will not block a synthesizer decision to drop the XXIV citation entirely if the test-contract clause stands on its own."
- **Recommended resolution**: Drop the explicit XXIV cross-reference from XVI per skeptic-mathematical's modified Rec 3. The generic test-contract clause (spec-013-routed per the test-sequencing dispute) covers the verification surface without expanding XXIV's authorized scope. Note in deliberation log: when an optimization output later becomes a synthesis-verdict input via a downstream spec, that downstream spec MUST add the XXIV three-layer defense at that point.
<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

**Blind-methodology distinction**: All recommendations below are **on Principle XVI** (in scope for spec 068). No incidental findings on other principles surfaced as standalone deferrable items in this run; cross-principle implications listed below (touching VII, V, II, XV) are XVI-driven cross-references, not independent findings.

### P1 (Mandatory, Convergence-floor)

1. **VII↔XVI bilateral inline cross-reference** [Convergence 1; skeptic-mathematical revised Rec 2; skeptic-cross-principle revised Rec 3; practitioner revised Rec 10].
   - VII appends: "Principle XVI defines the sole sanctioned exception, scoped to LLM-mediated parameter resolution under within-run pinning discipline."
   - XVI opens with: "Subject to Principle VII, …"
   - Inline prose, no `references/` redirect.

2. **VII pre-condition tuple expansion** [Convergence 4; skeptic-mathematical surviving Rec 8; practitioner New Rec 13].
   - VII adds: "Reproducibility is conditional on (config, template registry, capability registry) being byte-identical between runs. Changes to any of these constitute a different input set."
   - This stacks with P1 #1 in the same VII edit.

3. **V-emission for pinned parameter values** [Convergence 5; skeptic-cross-principle revised Rec 6; practitioner New Rec 11].
   - XVI adds: "Pinned parameter values MUST be emitted as deliberation output (e.g., `optimization/pinned_parameters.yml`) under V's progress-reporting contract, subject to VII's reproducibility pre-conditions."

4. **Solver-substitution wording softening** [Convergence 2; skeptic-mathematical New Rec B; skeptic-cross-principle Rec 8; practitioner New Rec 12].
   - Replace XVI's "Changing solvers MUST NOT change what is being optimized" with: "Changing solvers MUST NOT change the objective function expression or its parameter semantics. Numerical results may differ within solver-tolerance bounds; the objective function is the contract, not the solver's output."

5. **Relocate 3-stage pipeline description from XVI to spec 013** [Convergence 6; skeptic-cross-principle revised Rec 9; practitioner Rec 1+6 narrowed; skeptic-mathematical modified Rec 1].
   - Pipeline description leaves XVI entirely. No property-form residue. Spec 013 owns the architectural narration. XVI references spec 013 only for the contract test (P2 #1 below).

6. **Tightened-standalone XVI structural endpoint** [Disputed but synthesizer-recommended; skeptic-mathematical modified Rec 1; practitioner revised Rec 1].
   - XVI shrinks to ~4-8 lines: VII cross-reference, pinning operational sentence, plain-language requirement, softened solver-substitution invariant, V-emission cross-reference, II glossary reference, spec 013 reference. No new principle numbers.

### P2 (Recommended, structural follow-on)

1. **Spec-013-routed test contract reference** [Disputed; synthesizer recommends shape C; skeptic-cross-principle revised Rec 5; skeptic-mathematical modified Rec 3 (intent); practitioner revised Rec 4 (intent)].
   - XVI references spec 013's parameter-pinning contract test (no specific test file path in constitutional prose).
   - Spec 013 must contain the contract test before XVI amendment merges.

2. **"Pinning" term-of-art definition in II** [Convergence 7; skeptic-cross-principle revised Rec 5; skeptic-mathematical New Recommendation A].
   - II's stable-interface vocabulary adds: "Pinning — a parameter value committed to a run-scoped store, immutable for the duration of the run, with invalidation policy specified in spec 013."
   - XVI references this term-of-art.

3. **Vocabulary cleanup: "deterministic" vs. "mechanical"** [skeptic-cross-principle Rec 4 sharpened; skeptic-mathematical Safe Agreement #3; practitioner Tension #2 endorsing skeptic-cross-principle's direction].
   - In XVI, stages 1 and 3 (where surviving) use "deterministic" consistent with VII vocabulary.
   - "Mechanical" reserved for VIII's antonym-of-LLM-inference sense.

4. **Audience disambiguation clause** [skeptic-cross-principle New Rec 2; skeptic-mathematical modified Rec 6 (two-audience version)].
   - XVI's transparency claim retains both audiences: template legibility (spec-author concern, addressed by template-documentation clause) and runtime output legibility (end-user concern, addressed by plain-language clause). Neither silently dropped.

5. **Plugin-explanation cross-reference with XV** [skeptic-mathematical surviving Rec 9].
   - XVI adds one-line cross-reference: "This clause constrains plugin *output content*; Principle XV constrains plugin *isolation from core state*. The two are independent."
   - Mirrors XXVII's existing coordination language with XV.

### P3 (Optional, documentation/CI hygiene)

1. **CI hook for template description fields** [practitioner Rec 9].
   - Linter check scanning `templates/optimization/*.yml` (or wherever spec 013 templates live) for missing `description:` and `plain_language:` fields. Operationalizes the plain-language rule.

2. **Move template-documentation form spec to spec 013** [practitioner revised Rec 6 (narrowed)].
   - Detailed template documentation form lives in spec 013. Constitutional invariant ("every objective function template documents its parameters in plain language") stays in XVI.

3. **Rename XVI conditional on structural outcome** [skeptic-cross-principle New Rec 3; practitioner Rec 8 (weakly held)].
   - If only the transparency residual survives in XVI: "Mathematical Transparency" is acceptable.
   - If pinning is the surviving content: rename to "Pinned Parameter Discipline" or "Optimization Reproducibility Contract."
   - Under synthesizer-recommended tightened-standalone outcome (P1 #6), the rename question can be deferred to a follow-up PR after the residual content is settled.

4. **Drop the "Clarification: determinism scope" footnote** [skeptic-mathematical Safe Agreement #2; skeptic-cross-principle Phase 1 Executive Summary; practitioner Phase 1 Missed Opportunity #3].
   - The clarification block (lines 469–476) is a tell that the original wording did not land cleanly. Once the bilateral VII↔XVI cross-reference (P1 #1) and within-run/cross-run reframing land, the footnote becomes unnecessary and should be removed.

---

## Key Concessions

### skeptic-mathematical (Phase 3 revision)
- **Rec 1 (split into XVI-A/XVI-B)**: Modified — accepted skeptic-cross-principle's "splitting doubles the cross-reference debt" and practitioner's "more principles = more cost" critiques. Retreated from issuing new principle numbers; "decompose analytically, transparency stays inline as the surviving kernel" (revision §Recommendation 1).
- **Rec 2 (move determinism to references/parameter-resolution.md)**: Modified — both critics correctly flagged that pointing at a non-existent doc degrades constitutional weight. Accepted bilateral inline cross-reference with VII gaining LLM-mediated-pinning acknowledgment (revision §Recommendation 2).
- **Rec 3 (XXIV pattern citation)**: Modified — skeptic-cross-principle's Dangerous Contradiction #3 caught that XXIV is scoped to synthesis verdicts and provider protocols; re-purposing wholesale violates XI. Dropped XXIV citation, retained generic test-contract clause (revision §Recommendation 3).
- **Rec 4 (cache key tuple)**: Withdrawn — accepted skeptic-cross-principle's Tension #2 ("constitutional overreach"). "I withdraw the four-tuple specification entirely" (revision §Recommendation 4).
- **Rec 5 (LLM temperature/seed)**: Withdrawn — explicitly labeled "an unforced error" after skeptic-cross-principle's Tension #3 caught the VIII inversion (revision §Recommendation 5).
- **Rec 6 (narrow audience to spec author)**: Modified — both critics' Dangerous Contradictions converged: outsourcing end-user transparency to IV contradicts IV; revokes user-facing promise. Retreated to "two audiences, two surfaces, both retained" (revision §Recommendation 6).
- **Rec 7 (pinning trade-off)**: Withdrawn — accepted practitioner's "trade-off discussion is feature-spec content, not constitutional content" (revision §Recommendation 7).
- **Rec 10 (remove XVI entirely)**: Withdrawn — accepted both critics' Dangerous Contradictions (loses gate; XII violation strands specs 012-019). "XVI stays as a numbered principle" (revision §Recommendation 10).
- **Phase 2 cross-review concession**: V-emission requirement — "Their cross-principle audit caught something my logical-coherence audit missed" (Phase 2 cross-review of skeptic-cross-principle, Tension #3).
- **Phase 2 cross-review concession**: Solver-substitution wording — "I now think they are right; the conservative reading should win" (Phase 2 cross-review of skeptic-cross-principle, Tension #2).

### skeptic-cross-principle (Phase 3 revision)
- **Rec 1 (merge XVI into VII)**: Softened to "merge OR demote, after decomposition" — accepted skeptic-mathematical's "split first, then absorb" sequencing (revision §Recommendation 1). Conceded these are not opposites but sequential phases of one refactor.
- **Rec 7 (XVI ↔ XXIV interaction)**: Narrowed — skeptic-mathematical's cross-review flagged XXIV's pattern doesn't auto-generalize. Restricted to optimization outputs consumed by synthesis-verdict generation (revision §Recommendation 7).
- **Rec 9 (generalize away from 3-stage pipeline)**: Refined to practitioner's relocation-not-property-form framing — "I now think the practitioner's version is the right disposition — the 3-stage description should leave XVI entirely" (revision §Recommendation 9).
- **Rec 10 (remove XVI entirely)**: Withdrawn as standalone, folded into decomposition Rec 1 — own cross-review of skeptic-mathematical caught XII anti-pattern (specs 012-019 stranded) (revision §Recommendation 10).
- **Phase 2 cross-review concession**: practitioner's "remove XVI" was acceptable as a backstop only; skeptic-cross-principle held VII back-reference as load-bearing regardless of removal (Phase 2 cross-review of practitioner, Dangerous Contradiction #1).

### practitioner (Phase 3 revision)
- **Rec 4 (verification mechanism)**: Sequenced — accepted skeptic-mathematical's "test doesn't exist yet" critique. Restated as same-PR mandate to avoid pointing at fictional test files (revision §Original Rec 4).
- **Rec 5 (move plain-language to X)**: Withdrawn — skeptic-cross-principle's Phase 2 critique landed: X is output formatting, IV is spec product surface; splitting plain-language across both would scatter a coherent rule (revision §Original Rec 5).
- **Rec 7 (remove XVI entirely)**: Withdrawn — accepted skeptic-cross-principle's "removing XVI without fixing VII leaves VII's absolutism unchallenged" and own cross-review of skeptic-mathematical noting removal discards the only operationally crisp gate (revision §Original Rec 7).
- **Rec 10 (cross-reference VII↔XVI)**: Expanded — adopted skeptic-cross-principle's "sole sanctioned exception" wording over original "stochastic-input handling" framing as more constitutionally honest (revision §Original Rec 10).
- **New Rec 11 (V-emission)**: Added in revision after skeptic-cross-principle's Phase 2 critique caught practitioner's silence on V (Phase 2 cross-review of practitioner; revision §New Recommendations).
- **New Rec 12 (solver-substitution softening)**: Added in revision adopting skeptic-cross-principle's Phase 1 wording (revision §New Recommendations).
- **New Rec 13 (template-version dependency in VII)**: Added in revision explicitly conceding "skeptic identifies that cross-run reproducibility silently breaks when templates are edited. This is real and my review missed it" (Phase 2 cross-review of skeptic-mathematical, Tension #5; revision §New Recommendations).

---

**End of Synthesis**
