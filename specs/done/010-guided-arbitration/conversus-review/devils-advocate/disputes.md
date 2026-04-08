# Cooperative Disputes — Phase 4

**Agent**: devils-advocate
**Round**: 1 of 2
**Mode**: cooperative

---

### Remaining Disputes

- **Dispute: Default influence level (binding vs. recommended)**
  - **My claim**: The default influence level for the guided flow should be `recommended`, not `binding` (revision, Recommendation 2, surviving). Users without a preference are uncertain, and defaulting to the most authoritative level is inappropriate for uncertain users.
  - **Opposing position(s)**: Functional-typing (revision, Position Summary) argues the spec explicitly states "Default to `binding`" (L44) and changing the handler default without changing the spec is a spec-implementation mismatch. Integration-architect (revision, general position) argues architectural consistency requires the same default across all access paths.
  - **Why I will not concede**: The consistency argument treats the guided handler as a transparent proxy for the spec — whatever the spec says, the handler does. But the guided handler is explicitly designed for users who don't understand Phase 6 (spec L14-16). These users are different from those who hand-write `conversus.yml`. UX best practice is to default to the safest option for users who don't understand the implications. `recommended` is safer because it preserves the user's ability to override with evidence. `binding` removes that ability. The spec should be updated to reflect this UX principle.
  - **Counter-argument to their position**: The consistency argument assumes the same default is always correct regardless of context. But defaults serve users, not architectures. A command-line tool's `--force` flag defaults to `false` even though the underlying operation supports both. The arbitrate handler's default should serve the guided-flow user, not mirror the engine's default for power users.
  - **Proposed resolution path**: Change the spec (L44) to: "Default to `recommended` if the user doesn't have a preference. Users who want binding authority should explicitly select 'final authority.'" Update the Run engine default (SKILL.md L222) simultaneously. This eliminates the consistency concern while serving the user population correctly.

- **Dispute: Dispute preview scope (subsystem extension)**
  - **My claim**: Dispute preview can use existing heading-based parsing — extracting labels from `**Dispute:` entries is an extension of the existing count logic, not a new subsystem capability (revision, modified Recommendation 1).
  - **Opposing position(s)**: Integration-architect (disputes, Remaining Disputes) argues this changes the Dispute-Parsing Subsystem's stable interface contract. The subsystem returns boolean/integer; adding content extraction is a breaking change.
  - **Why I will not concede**: The subsystem's interface is described in SKILL.md L756-758 as having two outputs (boolean, integer). Adding a third output (list of labels) does not break the existing two. Existing consumers continue to get boolean/integer. New consumers (the arbitrate handler) additionally get labels. This is an additive change, not a breaking change. The stable interface contract (SKILL.md L777) protects the markers and headings used for parsing, not the set of outputs.
  - **Counter-argument to their position**: Integration-architect conflates interface expansion with interface breakage. A breaking change removes or modifies existing outputs. An additive change adds new outputs while preserving existing ones. The dispute preview adds a new output type (label list) without modifying boolean or integer. The parsing logic is unchanged — labels are extracted during the same scan that produces counts. This is standard interface evolution, not a contract violation.
  - **Proposed resolution path**: Adopt dispute preview with explicit documentation of the new output type alongside existing outputs. Acknowledge this as a subsystem evolution (not a breaking change). Update the subsystem documentation to list three output types: boolean, integer, and label list. This satisfies integration-architect's concern about documentation while preserving the feature.

### Convergence

- **Converged: Grounding document quality validation**
  - **Shared position**: Combined emptiness check (block if empty) + qualitative warning (warn if fewer than 3 criteria).
  - **Agreeing agents**: devils-advocate (revision, modified Recommendation 3), functional-typing (revision, modified Recommendation 1)
  - **Strength**: Bilateral
  - **Path to convergence**: Emerged through Phase 2 cross-review. Both agents proposed complementary approaches that were merged in Phase 3.

- **Converged: YAML-aware serialization**
  - **Shared position**: All config modifications must use YAML-aware serialization.
  - **Agreeing agents**: All three agents
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1. Never challenged.

- **Converged: Config backup**
  - **Shared position**: Back up `conversus.yml` before modification.
  - **Agreeing agents**: functional-typing (revision, modified Recommendation 2), devils-advocate (revision, Recommendation 8)
  - **Strength**: Bilateral
  - **Path to convergence**: Functional-typing proposed in Phase 1. Devils-advocate's undo documentation complements it.

- **Converged: Arbiter name collision check**
  - **Shared position**: Check arbiter name against agent names and adjust on collision.
  - **Agreeing agents**: devils-advocate (revision, Recommendation 6), integration-architect (revision, New Recommendation)
  - **Strength**: Bilateral
  - **Path to convergence**: Devils-advocate proposed in Phase 1. Integration-architect adopted in Phase 3.

- **Converged: Template validation in Step 5**
  - **Shared position**: Validate template existence before Phase 6. User-friendly errors.
  - **Agreeing agents**: integration-architect (revision, Recommendation 2), functional-typing (revision, New Recommendation 1)
  - **Strength**: Bilateral
  - **Path to convergence**: Integration-architect identified. Functional-typing adopted. Devils-advocate suggested plain-language wrapping.

### Final Position Statement

**Non-Negotiables** (1 item):
- The default influence level must be changed to `recommended`. This is the single most impactful user-safety issue in the spec. Binding authority should be an intentional choice, not a passive default for users who don't understand the implications. [spec L44, SKILL.md L1752]

**Flexibility** (3 items):
- Dispute preview implementation path: I'm flexible on whether this is framed as a subsystem "extension" or "evolution" — the core requirement is that users see what they're arbitrating before configuring an arbiter. The documentation formality is negotiable.
- "Generate config only" mode (Recommendation 4): valuable but not essential. If the guided flow is simplified by omitting this, the core value (config generation + execution) is preserved.
- Grounding document template strengthening (Recommendation 7): the specific template wording is flexible as long as the generated document pushes users toward domain-specific criteria rather than generic principles.
