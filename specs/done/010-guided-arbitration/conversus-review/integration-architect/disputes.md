# Cooperative Disputes — Phase 4

**Agent**: integration-architect
**Round**: 1 of 2
**Mode**: cooperative

---

### Remaining Disputes

- **Dispute: Default influence level (binding vs. recommended)**
  - **My claim**: I did not take a strong position on the default value in my review. However, after cross-review, I align with the consistency argument: the default should match the spec (L44) and the Run engine (SKILL.md L222). If changed, it must change everywhere.
  - **Opposing position(s)**: Devils-advocate (revision, Recommendation 2, surviving) argues `recommended` should be the default for the guided flow. They claim the guided handler serves a different user population.
  - **Why I will not concede**: Architectural consistency requires the same default across all access paths. The arbiter schema defines `binding` as the default (SKILL.md L222). The spec defines `binding` as the default (spec L44). Introducing a handler-specific override creates a layered default system where the outcome depends on which entry point the user chose, not the user's intent. This is an integration anti-pattern.
  - **Counter-argument to their position**: Devils-advocate's argument that "the handler serves different users" is a UX observation, not an architectural requirement. The correct response is UX guidance (which they also recommend in modified Recommendation 5), not a default change. Different defaults for the same feature based on entry point is confusing and increases the surface area for bugs.
  - **Proposed resolution path**: Keep `binding` as the default. Adopt the first-time guidance note (devils-advocate modified Recommendation 5). If the project decides `recommended` is universally better, change the spec, engine, and handler simultaneously.

- **Dispute: Dispute preview in Step 1 (subsystem extension)**
  - **My claim**: Adding dispute preview requires extending the Dispute-Parsing Subsystem to extract content, not just count/boolean (revision, from cross-review of devils-advocate). This is a subsystem change with implications beyond the arbitrate handler.
  - **Opposing position(s)**: Devils-advocate (revision, modified Recommendation 1) argues the preview can use existing heading-based parsing — extracting labels from `**Dispute:` entries is "an extension of the existing count logic."
  - **Why I will not concede**: The Dispute-Parsing Subsystem has a documented stable interface (SKILL.md L751-777) with defined outputs: boolean and integer. Adding content extraction changes the interface contract. Even if the implementation uses existing parsing logic, the subsystem's return type changes. This must be acknowledged as a subsystem modification, not dismissed as a minor extension.
  - **Counter-argument to their position**: Devils-advocate frames label extraction as using "existing heading-based parsing." The parsing logic is indeed reusable, but the subsystem's output contract changes. A consumer that expects boolean/integer now gets boolean/integer/content. This is a breaking change to the stable interface contract described at SKILL.md L777.
  - **Proposed resolution path**: Adopt dispute preview BUT explicitly acknowledge it as a Dispute-Parsing Subsystem extension. Document the new output (list of dispute labels) alongside the existing boolean/integer outputs. Note this as a subsystem change in the spec, not hidden inside the handler. The handler's feature request is valid; the implementation path needs proper scoping.

### Convergence

- **Converged: YAML-aware serialization**
  - **Shared position**: All config modifications use YAML-aware serialization. Unanimous.
  - **Agreeing agents**: integration-architect (revision, Recommendation 3), functional-typing (revision, Recommendation 8), devils-advocate (implicit)
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1. Never challenged.

- **Converged: Template validation in Step 5**
  - **Shared position**: Validate template existence before Phase 6 execution. User-friendly error messages.
  - **Agreeing agents**: integration-architect (revision, Recommendation 2), functional-typing (revision, New Recommendation 1)
  - **Strength**: Bilateral
  - **Path to convergence**: Integration-architect identified in Phase 1. Functional-typing adopted in Phase 3 revision.

- **Converged: Multi-round output documentation**
  - **Shared position**: Explicitly document that `summary/final.md` serves both single-round and multi-round outputs.
  - **Agreeing agents**: integration-architect (revision, Recommendation 7), functional-typing (revision, Recommendation 5)
  - **Strength**: Bilateral
  - **Path to convergence**: Both independently proposed in Phase 1. Confirmed in cross-review.

- **Converged: Grounding document content validation**
  - **Shared position**: Validate emptiness and warn on thin content.
  - **Agreeing agents**: functional-typing (revision, modified Recommendation 1), devils-advocate (revision, modified Recommendation 3)
  - **Strength**: Bilateral
  - **Path to convergence**: Emerged through cross-review. Functional-typing proposed emptiness check; devils-advocate proposed qualitative warning. Combined in Phase 3.

- **Converged: Arbiter name collision check**
  - **Shared position**: Check arbiter name against agent names; adjust on collision.
  - **Agreeing agents**: integration-architect (revision, New Recommendation), devils-advocate (revision, Recommendation 6)
  - **Strength**: Bilateral
  - **Path to convergence**: Devils-advocate proposed in Phase 1. Integration-architect adopted in Phase 3 as part of scoped validation.

### Final Position Statement

**Non-Negotiables** (2 items):
- Template validation must be added to Step 5. The arbitrate handler delegates to Phase 6 but skips the Run engine's template loading step. Without template validation, a missing template produces an opaque error. [SKILL.md L1811, Run engine Step 3 L281-296]
- Dispute-Parsing Subsystem extension must be acknowledged as a subsystem change if dispute preview is adopted. The subsystem's stable interface contract (SKILL.md L751-777) defines boolean/integer outputs. Adding content extraction is a contract change that must be documented. [SKILL.md L751-777]

**Flexibility** (2 items):
- Step 5 validation scope: currently scoped to arbiter block + cross-references. I'm flexible on the exact scope — the core requirement is that validation does not reject configs on grounds unrelated to the arbiter block.
- Generated config completeness (timing field, docs support): both are recommended but not essential. If the guided flow needs to be simplified, these can be omitted without architectural impact.
