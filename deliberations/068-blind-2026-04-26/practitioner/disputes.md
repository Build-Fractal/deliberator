# Practitioner Disputes — Phase 4

**Reviewer**: practitioner (developer ergonomics lens)
**Phase**: 4 (disputes / final position)
**Target**: Constitution v2.3.2-blind, Principle XVI

---

### Remaining Disputes

#### Dispute 1: Structural fork — tight standalone XVI vs. decompose-and-redistribute

- **Practitioner position**: Keep XVI as a *tight standalone* principle (4–6 operational lines), with the parameter-pinning rule and the plain-language rule co-located because they protect the same user-facing promise ("the user understands what they are optimizing"). One numbered principle, one location, one PR-review checklist item.
- **Skeptic-cross-principle position**: Execute the four-step sequence (split → relocate → cross-reference → absorb), with the transparency fragment landing in IV and the pinning fragment either folded into VII or kept freestanding under a tighter name. Their New Recommendation 1 spells this out as the canonical path.
- **Skeptic-mathematical position**: Decompose analytically along the transparency / determinism / pinning axis, but the output is *not* necessarily two new numbered principles — most likely transparency stays inline, determinism cross-references VII, pinning collapses to one operational sentence backed by a test contract. No new principle numbers.
- **Where the disagreement is real**: Whether the transparency rule and the pinning rule are tightly coupled (my view — they protect the same promise and a developer reads them together during code review) or whether they have different audiences and different enforcement surfaces (skeptic-cross-principle's view — transparency targets end users via X/IV, pinning targets developers via test contract). Skeptic-mathematical lands closer to my position structurally (no new numbers, decompose analytically) but closer to skeptic-cross-principle on the transparency-fragment-fits-elsewhere question.
- **Why I do not concede**: Constitutional density has a real ergonomic cost. A reviewer reading a PR diff that touches optimization parameters needs to land on *one* checklist, not chase a transparency clause to IV, a pinning clause to VII, a pipeline description to spec 013, and a cache test contract to spec 013's test directory. Skeptic-cross-principle's sequence is constitutionally elegant and operationally diffuse. Skeptic-mathematical's "no new numbers" outcome is closer to my position than the four-step framing reads.
- **Acceptable resolution**: I will accept skeptic-mathematical's modified Recommendation 1 outcome (decompose analytically, transparency stays inline, no new principle numbers, pinning collapses to one operational sentence) as the convergence point. This delivers most of skeptic-cross-principle's structural intent without paying the cross-reference debt of physically relocating the transparency fragment to IV.

#### Dispute 2: V-emission as constitutional requirement vs. spec-level requirement

- **Practitioner position** (from my New Rec 11): Pinned parameter values MUST be emitted in deliberation output (e.g., `optimization/pinned_parameters.yml`) so the user can audit which parameter values their objective function was assembled from. Without this, XVI's transparency claim is enforceable in CI but invisible at runtime.
- **Skeptic-cross-principle position**: Same outcome, stronger framing — they hold V-emission as "non-negotiable" in their final position and explicitly call out that both cross-reviewers (including me, in earlier phases) under-weighted it.
- **Skeptic-mathematical position**: Did not address V-emission as a separate item; their surviving recommendations are scoped to VII↔XVI cross-reference and template versioning. Their Phase 3 revision does not contest V-emission but also does not endorse it explicitly.
- **Where the disagreement is real**: Less than it appears. Skeptic-cross-principle and I converge on "V-emission required." Skeptic-mathematical is silent rather than opposed. The latent question is *where the requirement lives* — V's existing "every phase MUST report progress" clause already implies it, so the question is whether XVI needs an explicit V-cross-reference or whether V's general clause is sufficient.
- **Why I do not concede**: V's general progress-reporting clause does not name pinned parameters specifically; without an XVI↔V cross-reference, a future PR could ship pinning-without-emission and point at V's progress-line requirement (one line per phase) as already satisfied. The cross-reference is the load-bearing edit, not the V principle itself.
- **Acceptable resolution**: Add a single sentence to XVI: "Pinned parameter values MUST be emitted as deliberation output under V's progress-reporting contract (e.g., `optimization/pinned_parameters.yml`)." No new V amendment required; XVI cross-references V the same way it will cross-reference VII per Dispute 3.

#### Dispute 3: Where the template-version dependency lives — VII, XVI, or both

- **Practitioner position** (from my New Rec 13): Anchor the template-version dependency in VII, not XVI. VII's "same config produces same output" promise silently depends on template files and the capability registry being byte-identical between runs; the amendment should add a "Reproducibility is conditional on (config, template registry, capability registry) being byte-identical" clause to VII. Cross-run reproducibility is broader than just optimization; it affects every config-driven behavior.
- **Skeptic-mathematical position** (their surviving Rec 8): Template versioning belongs in VII as a clarification of what "same inputs" means (templates are inputs to the deterministic substitution), with XVI cross-referencing VII's expanded clause. Stacks with their modified Rec 2 (bilateral cross-reference between VII and XVI) — VII gains both the LLM-mediated-pinning exception *and* the template-version clarification in the same edit. Same destination as my position.
- **Skeptic-cross-principle position**: Did not contest template-versioning content; their final position holds VII↔XVI bidirectional cross-reference as "the single highest-leverage edit on which all three reviews converge" but is silent on whether template-version specifically lives in VII or XVI.
- **Where the disagreement is real**: Effectively none on placement (VII), but there is a residual question about *form*. Skeptic-mathematical writes "(config, template_version)" as the reproducibility-scope tuple; I write "(config, template registry, capability registry)" which is broader. The capability-registry inclusion matters because XI's v2.3.0 extension makes the registry authoritative — if a registry change between runs alters which capabilities are available, reproducibility breaks even if templates are identical.
- **Why I do not concede the broader form**: The capability-registry dependency is a real silent-failure surface. Spec 064.1 (runtime registration) and spec PR #18 (manifest projection) both assume registry stability between runs; without naming it in VII's pre-conditions, a future plugin install between runs would break "same config produces same output" with no constitutional warning.
- **Acceptable resolution**: VII gains "Reproducibility is conditional on (config, template registry, capability registry) being byte-identical between runs. Changes to any of these constitute a different input set." XVI cross-references this. Skeptic-mathematical's narrower (config, template_version) is preserved as a subset of my broader tuple; nothing they wrote is contradicted.

---

### Convergence

#### Convergence 1: VII↔XVI bidirectional cross-reference is the highest-leverage edit

All three reviewers converged on this independently. Skeptic-cross-principle frames it as "the single highest-leverage edit on which all three reviews converge"; skeptic-mathematical's modified Rec 2 makes it bilateral and inline (no `references/` redirect); my Rec 10 expands it to adopt skeptic-cross-principle's "sole sanctioned exception" wording. Final convergent text:

- VII appends: "Principle XVI defines the sole sanctioned exception, scoped to LLM-mediated parameter resolution under within-run pinning discipline."
- XVI opens with: "Subject to Principle VII, …"

This is mandatory regardless of which structural disposition (tight standalone, decompose-and-redistribute, or VII extension) the synthesizer chooses.

#### Convergence 2: Solver-substitution claim must soften from numerical to semantic

Skeptic-cross-principle's Rec 8 (no change in their disposition table); skeptic-mathematical's New Rec B (added in revision); my New Rec 12 (added in revision). All three converge on the same wording approximately: "Changing solvers MUST NOT change the objective function expression or its parameter semantics. Numerical results MAY differ within solver-tolerance bounds; the contract is on the function, not the solver's output." This closes a real ambiguity — current XVI wording promises numerical equivalence two solvers cannot deliver — at zero semantic cost.

#### Convergence 3: Removing XVI entirely is off the table

My original Rec 7, skeptic-mathematical's original Rec 10, skeptic-cross-principle's original Rec 10 all proposed removal as an option; all three withdrew it after cross-review. The two converging Dangerous Contradictions that killed removal: (a) XVI catches "developer adds a second LLM call to the gap-fill code path" — the one operationally crisp gate VII/IV/X do not catch; (b) specs 012-019 reference Principle XVI by name, removing it strands them as a textbook XII (No Dead Infrastructure) violation. XVI stays, in some form.

#### Convergence 4: The 3-stage pipeline description leaves the constitution

Skeptic-cross-principle's Rec 9 (relocated to spec 013); my Rec 6 narrowed (form lives in spec 013, invariant stays); skeptic-mathematical's modified Rec 1 (decompose analytically, pipeline description does not survive in property form). All three converge: the constitution does not narrate the pipeline at any altitude. Spec 013 owns it. The constitutional-residue question — whether XVI keeps a property-form summary or nothing at all — is less load-bearing than whether the description leaves XVI; on the latter, all three agree.

#### Convergence 5: "Pinning" as term-of-art with test-contract anchor

Skeptic-cross-principle's Rec 5 (define "pinning" in II's stable-interface vocabulary); skeptic-mathematical's New Rec A (add to II: "Pinning — a parameter value committed to a run-scoped store, immutable for the duration of the run, with invalidation policy defined in spec 013"); my Rec 4 sequenced (constitutional pointer + test landed in same PR). All three converge: "pinning" gets a constitutional definition in II, the cache contract stays in spec 013, and the principle MUST point at a contract test that demonstrably fails on within-run drift. The test name and path live in spec 013; the constitutional pointer is generic but enforceable.

---

### Final Position Statement

**Non-Negotiables**:

1. **VII↔XVI bidirectional cross-reference, inline, in the same PR.** VII's "deterministic orchestration is non-negotiable" framing and XVI's stochastic LLM admission cannot both stand without explicit mutual acknowledgement. The edit must be bilateral (VII names XVI as the sole sanctioned exception; XVI opens "Subject to Principle VII") and the prose stays inline rather than redirected to a non-existent `references/` doc. This is the load-bearing structural fix that makes everything else coherent.

2. **V-emission for pinned parameter values.** Pinned parameter values MUST be emitted as deliberation output (e.g., `optimization/pinned_parameters.yml`) under V's progress-reporting contract. Without observable pinned values, XVI's transparency claim is enforceable only in CI and invisible at runtime — which violates XVI's own "user understands what they are optimizing" promise. The XVI↔V cross-reference is mandatory.

3. **Template registry and capability registry as VII pre-conditions.** VII's "same config produces same output" silently breaks the moment any spec author edits a template or any plugin extends the registry. VII must add "Reproducibility is conditional on (config, template registry, capability registry) being byte-identical between runs" to make its pre-conditions enumerable. This formalizes what users assume but the constitution does not currently say, and resolves the silent-failure mode that affects every config-driven behavior, not just optimization.

**Flexibility**:

1. **Structural disposition (tight standalone vs. decompose-and-redistribute).** I prefer tight-standalone XVI (4–6 operational lines, transparency and pinning co-located) for developer ergonomics. Skeptic-cross-principle prefers the four-step decomposition; skeptic-mathematical lands at "decompose analytically, no new principle numbers, transparency stays inline." I will accept skeptic-mathematical's outcome as the convergence point — it delivers most of skeptic-cross-principle's structural intent (analytic decomposition, pipeline-description leaves, no XVI overcrowding) without the cross-reference debt of physically relocating the transparency fragment. If the synthesizer prefers full decompose-and-redistribute, I will not block it provided the V-emission and VII pre-conditions edits land regardless.

2. **Operational-language reframe vs. academic vocabulary.** I prefer "called at most once per parameter per run; cached for the rest of the run" over "within-run determinism / cross-run reproducibility." Skeptic-cross-principle argued the academic vocabulary is XVI's technical contribution. I hold the operational-language preference but will accept either if the test contract reference is concrete (a specific test name and assertion that fails on within-run drift). Vocabulary is incidental if the test enforces the behavior.

3. **Renaming XVI.** I prefer "Pinned Parameter Discipline" or "Optimization Reproducibility Contract" over "Mathematical Transparency" — the current name is too broad and enabled the bundling defect skeptic-cross-principle diagnosed. Skeptic-cross-principle's New Rec 3 treats the name as a remediation target. Skeptic-mathematical did not weigh in directly. I hold the rename preference weakly; I will not block convergence over it. If XVI stays tight-standalone with transparency and pinning co-located, "Mathematical Transparency" remains acceptable; if the transparency fragment leaves, rename is required.
