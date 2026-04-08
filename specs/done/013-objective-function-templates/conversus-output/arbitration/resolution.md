# Arbitration Resolution: 013 Objective Function Templates

**Arbiter**: conversus-architect
**Authority**: Binding (trigger: disputes_remain)
**Date**: 2026-03-23
**Grounding document**: `conversus/README.md` (Conversus: Competitive Multi-Agent Deliberation)

---

## Process Note

This arbitration resolves four disputes that survived the full five-phase cooperative deliberation on spec 013 (Objective Function Templates). Four agents -- game-theorist, schema-engineer, functional-architect, and spec-compliance -- produced 4 initial reviews, 12 cross-reviews, 4 revisions, and 4 dispute filings. The Phase 5 synthesis identified 8 convergence points and 4 remaining disputes.

The arbiter is the conversus system itself. My interest is transparent: these objective function templates must serve as reliable building blocks for spec 014 (guided construction) and the plugin system (specs 016-019). A template that is mathematically wrong produces wrong optimizations. A schema that is incomplete forces spec 014 to work around gaps that should have been closed here. A process that adds fields without spec amendments creates the same class of deviation the deliberation identified and condemned in FR-011.

I have read the grounding document, the Phase 5 synthesis, all four Phase 4 dispute documents, the spec itself, the current `objectives.py` schema, and all six constraint YAML files. The rulings below cite the grounding document and are constrained by the principles it establishes.

---

## Decision Framework

The following principles from the grounding document govern these rulings:

**Principle 1: Competition surfaces the strongest arguments; the subject has operational knowledge.** The grounding document states: "External reviewers surface the strongest arguments through adversarial pressure. But the subject has operational knowledge and design intent that external agents lack." I apply this by weighing the agents' adversarial findings on their merits while exercising the operational judgment of knowing what spec 014 will actually need to consume.

**Principle 2: Convergence strength determines confidence.** The grounding document's cooperative mode scoring states: "Recommendations scored by convergence strength (unanimous > majority > single-tool)." Where agents have converged, I do not disturb the convergence. Where they disagree, I weigh the strength of surviving arguments after the full adversarial process.

**Principle 3: Synthesis output is converged positions + remaining disputes + prioritized spec changes.** The grounding document defines the cooperative synthesis output format. My role is to resolve the remaining disputes so the output becomes actionable. I do not revisit converged positions.

**Principle 4: The arbiter must cite the grounding document; decisions without citations are invalid.** The grounding document states: "For each remaining dispute, it issues a binding decision with a citation to the grounding document. Decisions without grounding citations are invalid."

**Principle 5: The process exists to produce battle-tested decisions.** The grounding document opens with: "Conversus is a game theory-informed framework for vetting ideas before they reach production." The purpose is not process purity -- it is producing decisions that survive contact with production. Where process arguments and production-readiness arguments conflict, production-readiness governs.

---

## Binding Decisions

### Dispute A: `optimization_direction` Field

**Positions:**

- **FOR addition as optional with default "minimize"** (game-theorist R6, functional-architect NR-1): The sign convention inconsistency is real. Adding `optimization_direction: Optional[Literal["minimize", "maximize"]] = "minimize"` provides a machine-readable convention declaration for spec 014. The optional-with-default design preserves FR-002 compliance for existing templates. Pair with a heuristic consistency check in `validate_library_integrity()`.

- **AGAINST addition at the model level** (schema-engineer): Creates a second source of truth alongside the `form` string. A template author can write `optimization_direction: maximize` without adjusting the form's signs, creating a silent inconsistency that is formally present in the schema and worse than the current implicit state.

- **AGAINST addition without spec amendment** (spec-compliance): FR-002 through FR-011 do not define this field. Adding it -- even as optional with a default -- instantiates a spec-vs-implementation divergence. Requires a spec amendment to FR-002 before implementation.

**Synthesizer's assessment:** The synthesizer recommended proposing a spec amendment to FR-002 first, then implementing as optional with default. This combines both procedural requirements.

**Ruling: DEFER. Propose spec amendment to FR-002 first; implement after ratification.**

**Grounding citation:** Principle 5 (battle-tested decisions) and Principle 2 (convergence strength). The deliberation unanimously adopted a spec amendment protocol (Convergence Point 4) that states: "any correction to a template's form field that changes the mathematical expression requires a spec Section 2 amendment before the YAML is updated." Adding a new field to the model is a more significant change than correcting a YAML value. Applying a weaker standard to a larger change is inconsistent with the protocol the agents themselves established. Spec-compliance's procedural objection is not mere formalism -- it is the same principle the deliberation already ratified for form-field corrections, applied consistently.

**Rationale:** The underlying problem -- no machine-readable optimization direction -- is real and acknowledged by all four agents. But the correct remedy is process-consistent: propose the spec amendment, ratify it, then implement. This does not block any v1 work. The sign convention corrections (P1-5) require spec amendments anyway; `optimization_direction` can be included in the same amendment batch. Schema-engineer's two-sources-of-truth concern is real but is mitigated (not eliminated) by placing consistency checks in `validate_library_integrity()` rather than in model validators. The field should be `Optional[Literal["minimize", "maximize"]] = "minimize"` when implemented, not required -- game-theorist's transition-risk argument is sound.

**Rejected position:** Adding the field to the model before a spec amendment (game-theorist's non-negotiable #4: "optimization_direction must accompany, not follow, the sign convention correction"). The sign convention correction itself requires a spec amendment per the adopted protocol. The `optimization_direction` field can be included in that same amendment. The sequencing game-theorist demands is achievable without bypassing the amendment process.

**Required changes:**
1. Add `optimization_direction` to the FR-002 spec amendment proposal (alongside the sign convention corrections in P1-5).
2. After ratification, implement as `optimization_direction: Optional[Literal["minimize", "maximize"]] = "minimize"` on `ObjectiveTemplate`.
3. Pair with a best-effort heuristic in `validate_library_integrity()` that flags potential sign/direction inconsistencies as advisory diagnostics, not hard failures.

---

### Dispute B: `computed_objective` Disposition

**Positions:**

- **REMOVE entirely** (spec-compliance): FR-002's "minimal valid parameterization" means parameter names and values only. `computed_objective` is documentation, not parameterization. Adding `example_note` creates a model field that FR-002 does not define.

- **MIGRATE to `example_note: Optional[str] = None`** (schema-engineer, functional-architect): The content is semantically distinct from the template `description`. `example_note` preserves documentation value in a typed field that spec 014 can consume.

- **REMOVE only after `optimization_direction` exists** (game-theorist): `computed_objective` implicitly encodes optimization direction. Removing it before `optimization_direction` exists destroys machine-readable metadata without replacement.

**Synthesizer's assessment:** Remove `computed_objective` immediately. Do not add `example_note`. Absorb documentation value into the `description` field. If spec 014 reveals the need for a separate field, propose it as a spec amendment then.

**Ruling: REMOVE `computed_objective` from all example blocks. Do NOT add `example_note` as a model field.**

**Grounding citation:** Principle 2 (convergence strength) and Principle 5 (battle-tested decisions). The deliberation unanimously adopted the principle that new model fields require spec amendments (this was the basis of the FR-011 convergence and spec-compliance's non-negotiable). `example_note` is a new model field. Adding it without a spec amendment violates the same principle the deliberation used to resolve FR-011. Consistency requires applying the rule uniformly.

**Rationale:** The dispute reduces to whether the documentation value of `computed_objective` justifies a new model field. It does not -- at this stage. The `description` field already exists on `ObjectiveTemplate` (FR-002 defines it). Any concrete illustration of what an objective evaluates to can be incorporated into the description. This is not ideal for every use case, but it is spec-compliant, and it unblocks the example standardization track (P1-7) immediately without introducing a new field that no spec defines.

Game-theorist's sequencing gate (remove only after `optimization_direction` exists) creates a dependency chain that blocks example standardization behind a spec amendment for an unrelated field. The machine-readable optimization direction concern is valid but is resolved by Dispute A's ruling: both `optimization_direction` and the sign convention corrections go through the spec amendment process together. Blocking example cleanup on a spec amendment for a different field is an unacceptable coupling.

If spec 014's design genuinely requires a distinct `example_note` field -- separate from `description` -- the correct path is a spec amendment at that time. This is not a permanent rejection of the idea; it is a refusal to add unamended fields to the model.

**Rejected position:** Adding `example_note: Optional[str] = None` without a spec amendment (schema-engineer NR-3, functional-architect D3). Also rejected: blocking removal on `optimization_direction` (game-theorist D1).

**Required changes:**
1. Remove `computed_objective` from all example blocks in objective template YAML files.
2. Where the `computed_objective` content adds genuine illustrative value, incorporate it into the template's `description` field.
3. Do not add `example_note` or any other new field to `ObjectiveTemplate` for this purpose.
4. This change is a prerequisite for P1-7 (example standardization) and must be completed first.

---

### Dispute C: `description` on ConstraintTemplate -- Required vs. Optional

**Positions:**

- **REQUIRED with atomic YAML migration** (schema-engineer NR-2): All six constraint YAMLs already contain description text in header comments. The migration is bounded. Starting optional creates a window where spec 014 must special-case absent descriptions, and that defensive code persists permanently.

- **OPTIONAL first, required later** (functional-architect R6 revised, spec-compliance R8): FR-007 does not mandate a description field. Making it required couples schema change with content population in a single deployment. Optional-first decouples them.

**Synthesizer's assessment:** Add as required with atomic YAML migration. The migration surface is small (six files), the content source is known. If any header comment requires substantial rewording, fall back to optional.

**Ruling: REQUIRED, with atomic YAML migration.**

**Grounding citation:** Principle 5 (battle-tested decisions). The grounding document states the framework exists to produce decisions that survive contact with production. An optional field that serves a mandatory downstream purpose (spec 014 needs constraint descriptions for guided construction prompts) is a decision that does not survive contact with production -- it pushes the problem downstream rather than solving it.

**Rationale:** I inspected all six constraint YAML files. Each one contains a header comment block with a clear, adequate plain-language description:

- `budget.yml`: "Total weighted cost must not exceed a budget limit."
- `capacity.yml`: "Total allocation must not exceed a capacity limit."
- `bounds.yml`: "Per-variable lower and upper bounds."
- `minimum-coverage.yml`: "At least K options must be included."
- `mutual-exclusivity.yml`: "Exactly one option must be selected."
- `non-negativity.yml`: "All decision variables must be non-negative."

Every one of these is adequate as a verbatim description. The migration is six mechanical edits: extract the first sentence from each header comment and add it as a `description:` field. No authoring review is needed. No rewording is needed. Functional-architect's own resolution condition stated: "if the six constraint YAML header comments are adequate verbatim, schema-engineer wins." They are. Schema-engineer wins.

The process risk of atomic migration is negligible for six files with known content in a single commit. The downstream risk of optional-first is concrete: spec 014's guided construction pipeline will need to display constraint descriptions to users. If `description` is optional, the pipeline must handle `None` gracefully -- that defensive code ships, and once shipped, it stays. Making the field required now eliminates that entire category of downstream defensive logic.

**Rejected position:** Optional first, required later (functional-architect, spec-compliance). The resolution condition that functional-architect set has been met: the header comments are adequate verbatim.

**Required changes:**
1. Add `description: str` as a required field to `ConstraintTemplate` in `objectives.py`.
2. In the same commit, update all six constraint YAML files to include a `description:` field extracted from each file's header comment.
3. The six descriptions (use the first summary sentence from each header comment, lightly edited for consistency):
   - `budget`: "Total weighted cost must not exceed a budget limit."
   - `capacity`: "Total allocation must not exceed a capacity limit."
   - `bounds`: "Per-variable lower and upper bounds on each decision variable."
   - `minimum-coverage`: "At least K options must be included in the solution."
   - `mutual-exclusivity`: "Exactly one option must be selected from the alternatives."
   - `non-negativity`: "All decision variables must be non-negative."

---

### Dispute D: Form-Completeness Validator -- Placement and Scope

**Positions:**

- **In the Pydantic model as a warning** (game-theorist R9 revised): A scoped validator checking scalar/integer parameter names appear as substrings in the `form` field. Implemented as a warning, not an error. The only mechanism that catches simultaneous form-and-example omissions.

- **In `validate_library_integrity()` as a diagnostic** (schema-engineer, functional-architect D2): Pydantic validators raise or pass -- they cannot emit warnings natively. Form-completeness checks belong in the integrity function as structured diagnostics.

**Synthesizer's assessment:** Place in `validate_library_integrity()`. The check returns structured diagnostics (advisory, not hard failures). Model validators remain strict and raise only for definite structural invalidity.

**Ruling: Place the form-completeness check in `validate_library_integrity()`, NOT in a Pydantic model_validator.**

**Grounding citation:** Principle 2 (convergence strength). Three of the four agents (schema-engineer, functional-architect, spec-compliance) converge on placement in `validate_library_integrity()`. Game-theorist's own "warning" framing implicitly requires placement outside the Pydantic model, because Pydantic validators cannot emit warnings -- they must raise or be silent. The functional-architect's D2 resolution text explicitly identified this convergence: "both live in `validate_library_integrity()` as diagnostic checks that return structured findings rather than raising exceptions."

**Rationale:** The positions are closer than the dispute framing suggests. Everyone agrees the check should exist. Everyone agrees it should be scoped to scalar/integer parameters only. Everyone agrees it should not produce hard validation failures. The only real question is where it lives.

Pydantic model validators have a binary contract: they raise `ValueError` or they pass. There is no native warning mechanism. Game-theorist's proposal to append to a `warnings: list[str]` field would require adding a new field to the model -- which, per the principle established in Disputes A and B, requires a spec amendment. More fundamentally, a model validator that modifies a `warnings` field as a side effect rather than raising on invalidity is an architectural misuse of the Pydantic validation contract. Validators validate; they do not accumulate advisory metadata.

`validate_library_integrity()` is the correct home. It already exists as the consensus location for cross-artifact integrity checks (Convergence Point 3), form-consistency heuristics, and cardinality verification. Adding the form-completeness check there is consistent with the architecture all four agents agreed on. The check returns structured diagnostics -- a list of findings with severity levels -- that the caller can handle as warnings, errors, or ignore entirely.

Game-theorist's substantive concern -- that the `false_positive_penalty` class of defect must be catchable by automated tooling -- is fully satisfied by this placement. The check exists, it runs, it catches the defect. Where it runs is an implementation detail; that it runs is the requirement.

**Rejected position:** Placement in a Pydantic model_validator with a `warnings` field side effect (game-theorist R9, D3). The architectural objection is decisive: model validators validate, they do not accumulate advisory metadata.

**Required changes:**
1. Implement a form-completeness diagnostic in `validate_library_integrity()` that checks whether scalar/integer parameter names appear as substrings in the template's `form` string.
2. Scope: scalar and integer parameter types only. Function-type and string-type parameters are excluded.
3. Output: structured diagnostic findings with advisory severity. Not exceptions. Not hard failures.
4. The check is explicitly labeled as a heuristic -- false positives are possible (e.g., a parameter named `x` will match many things). The naming convention for template parameters should be documented as a library authoring standard to improve heuristic reliability.
5. This is categorized as P3-7 in the synthesis priority list -- implement after the core infrastructure (loaders, integrity function skeleton) is in place.

---

## Summary of Changes Required

Ordered by priority and dependency:

1. **[Immediate] Dispute C implementation**: Add `description: str` as required to `ConstraintTemplate`; update all six constraint YAML files in a single atomic commit. No dependency on any other change.

2. **[Immediate] Dispute B implementation**: Remove `computed_objective` from all example blocks. Incorporate illustrative content into template `description` fields where it adds value. This unblocks P1-7 (example standardization).

3. **[Spec amendment batch] Dispute A**: Include `optimization_direction` in the FR-002 spec amendment alongside the sign convention corrections (P1-5). After ratification, implement as `Optional[Literal["minimize", "maximize"]] = "minimize"` on `ObjectiveTemplate`, paired with a best-effort heuristic in `validate_library_integrity()`.

4. **[Infrastructure] Dispute D implementation**: After `validate_library_integrity()` skeleton exists (P1-10), add the form-completeness diagnostic as a scoped heuristic for scalar/integer parameters. Advisory severity only.

---

## Confidence Assessment

| Dispute | Ruling | Confidence | Risk if Wrong |
|---|---|---|---|
| A: `optimization_direction` | Defer to spec amendment | **High** | Low -- the field is valuable but deferral costs only time, not correctness. The spec amendment batch already exists for sign convention fixes. |
| B: `computed_objective` | Remove, no `example_note` | **High** | Medium -- if spec 014 genuinely needs a separate example annotation field, a spec amendment will be required later. But the `description` field covers the most common case. |
| C: `description` on ConstraintTemplate | Required, atomic migration | **Very High** | Very Low -- the migration surface is six files with known, adequate content. The downside of being wrong (one extra commit to fix a description) is trivial. |
| D: Form-completeness validator | In `validate_library_integrity()` | **Very High** | Negligible -- all four agents functionally agree on this placement. The dispute was about framing, not substance. |

The strongest ruling is Dispute D, where the agents' positions had already converged in substance and the dispute was primarily about the architectural semantics of "warning in a validator" versus "diagnostic in an integrity function." The positions were compatible; the ruling simply makes the compatibility explicit.

The ruling I hold with highest practical importance is Dispute C. Schema-engineer's atomic-migration argument was correct, and the inspection of the six constraint YAML files confirms the migration surface is clean. This ruling prevents spec 014 from shipping with defensive `None`-handling code for constraint descriptions that will never actually be absent in practice.

Dispute A is the ruling most likely to generate friction, because game-theorist's non-negotiable #4 explicitly states `optimization_direction` must accompany the sign convention correction. My ruling permits this -- both go through the spec amendment process together -- but it requires the spec amendment to happen first, which game-theorist may perceive as delay. The operational reality is that the sign convention corrections already require spec amendments (Convergence Point 4), so adding `optimization_direction` to the same amendment batch adds zero calendar delay. The field arrives at the same time as the corrections it is meant to accompany.

Dispute B carries the most downstream risk. If spec 014's prompt construction genuinely needs to distinguish "what this template is for" (description) from "what this example parameterization produces" (the former computed_objective), then collapsing both into `description` will prove inadequate and a spec amendment for a dedicated field will be needed. I accept this risk because the alternative -- adding an unamended field now -- violates the principle the deliberation itself established and creates a precedent that undermines spec-compliance enforcement for all future field additions.
