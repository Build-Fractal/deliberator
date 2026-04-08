# Cross-Review of integration-architect's Round 2 Review

**Cross-reviewer**: game-engine-advocate
**Reviewing**: integration-architect Round 2 review
**Round**: 2 of 2
**Date**: 2026-03-21

---

## Dangerous Contradictions

### DC-1: Rec 1 (SKILL.md `allowed-tools`) solves a problem that may not exist after P2-8

integration-architect's MO-1 identifies a real gap: SKILL.md Step 3 has no authorized invocation pathway for the linter. The recommendation is to update `allowed-tools` in SKILL.md frontmatter to permit `uv run python linter/validate.py`. However, integration-architect also acknowledges that P2-8 creates a `[project.scripts]` entry point (`conversus-lint`), which would make the invocation `conversus-lint --mode {mode}` -- a different command entirely.

The contradiction: Rec 1 proposes a spec note specifying the `uv run python linter/validate.py` invocation, while simultaneously acknowledging that P2-8 will change the invocation surface. If both ship, the spec note is immediately stale. The recommendation should pick one invocation pathway and commit to it, or explicitly frame the `uv run` form as the interim mechanism that P2-8 supersedes. As written, it risks encoding the pre-packaging invocation as the canonical form in documentation that outlives the packaging work.

This is not a deep architectural conflict, but it is the kind of documentation-implementation drift that integration-architect's own MO-2 (orphaned templates) warns against. The principle -- things that exist but aren't accounted for cause silent failures -- applies to spec notes that describe superseded invocation patterns just as well.

### DC-2: OBA-1 (filename-phase mapping) contradicts the "freeze first, compose later" principle

integration-architect identifies that the `phase = tmpl_path.stem` pattern is a load-bearing assumption and recommends documenting it as a constraint in P2-6. The recommendation is that variant templates for the same phase "must use conditional blocks within a single template, not separate files."

This is architecturally prescriptive in a way that conflicts with the Round 1 synthesis's governing principle (S1: "spec 005 optimizes for correctness of the current system; spec 007 designs extension mechanisms with full knowledge of the frozen foundation"). The filename-phase mapping is a current implementation detail. Whether future specs must use conditional blocks vs. separate files is a design decision that belongs to those future specs, informed by the constraints they discover. Documenting the current constraint ("filenames currently map 1:1 to phases") is correct. Prescribing the solution for future specs ("must use conditional blocks") oversteps spec 005's authority.

The Round 1 deliberation caught exactly this pattern when I front-loaded spec 007 design decisions into spec 005 recommendations (7 of 10 withdrawn as scope inflation). integration-architect's Rec 4 makes the same category of error in reverse: instead of front-loading an extension mechanism, it front-loads a constraint on how extensions must be designed. The P2-6 documentation should state the constraint (filename = phase name, 1:1), not the mandated workaround.

---

## Tensions

### T-1: MO-2 (reverse template existence check) is correct but the priority may be wrong

integration-architect identifies that templates existing on disk but not listed in mode schema YAML are silently ignored, and recommends a reverse existence check. This is a "pit of success" improvement I endorse. However, the P3 priority may be too low given that P2-1 is moving MODE_PRESENCE to mode schema YAML. When P2-1 ships, the mode schema `templates` list becomes the authoritative declaration of which templates exist for a mode. At that point, orphaned templates are not just a cosmetic concern -- they represent templates that the orchestrator will never load. A reverse existence check becomes the natural companion to P2-1, not an independent P3 item.

I would argue this should be part of P2-1's implementation scope (when you make the `templates` list authoritative, validate it in both directions), but integration-architect's P3 placement is defensible if P2-1's scope is already large enough. The tension is between scope containment (keep P2-1 focused) and logical completeness (bidirectional validation is a single concept).

### T-2: MO-3 (ROUND_SYNTHESES comment fix) intersects with my own P1-3 scope concern

integration-architect correctly identifies that `ROUND_SYNTHESES` is typed `extracted-content` in the schema but commented as "newline-separated paths" in models.py. The recommendation to fix the comment and explicitly exclude this field from P1-3 PathList conversion is sound. This aligns with my own concern about PathList application -- I did not raise this specific case, but the principle (not all `str` fields are path lists) is one I would have flagged during P1-3 implementation review. The tension is minor: whether this is a standalone P3 fix or a guardrail that should be encoded as a linter rule (e.g., "fields with `type: extracted-content` must not use `PathList`"). For v1, the comment fix is sufficient.

### T-3: OBA-2 (`validate_templates` granularity) vs. YAGNI

integration-architect recommends documenting that `validate_templates` may evolve from boolean to structured config. This is reasonable forward-looking documentation, but it sits in tension with the Round 1 synthesis's scope discipline (S2). The synthesis explicitly identified that front-loading extension mechanisms into spec 005 is the primary scope inflation risk. Documenting a speculative evolution path for a config field that currently has exactly one consumer (SKILL.md Step 3) and exactly one behavior (on/off) is low-risk but also low-value. If the need for granular validation arises, the implementer will design it based on the actual requirements, not based on a spec 005 note speculating about possible shapes.

I do not object to including it in P2-6, but I would frame it as an observation ("the boolean toggle is v1; granularity is a future concern") rather than a design suggestion ("may evolve to accept a structured config object"), to avoid biasing future implementers toward a specific shape that may not match their actual needs.

### T-4: My Dispute 1 refinement and integration-architect's acceptance diverge on specificity

I narrowed Dispute 1 to a docstring request: the `ValidationConfig` docstring should specifically mention `known_plugin_variables: frozenset[str]` as the anticipated extension, not just vaguely state "spec 007 may extend this model." integration-architect accepts the synthesizer's resolution without this refinement, stating the `ValidationConfig` model "provides a stable extension surface" and leaving the docstring content at the synthesizer's generic formulation.

This is not a contradiction -- we both accept `ValidationConfig` without the parameter. But there is a practical tension: a generic docstring ("spec 007 may extend") gives spec 007 implementers no guidance on what the extension should look like, which could lead to an incompatible design (e.g., adding plugin variables as a separate validation pass rather than as a parameter to the existing validation). A specific docstring ("anticipated extension: `known_plugin_variables: frozenset[str]`") costs nothing and provides a concrete contract. integration-architect's silence on this refinement neither endorses nor opposes it, which means it may fall through the cracks in synthesis.

---

## Safe Agreements

### SA-1: All 4 Round 1 dispute resolutions are accepted

Both integration-architect and I accept all 4 of the synthesizer's dispute resolutions. Neither of us reverses any Round 1 concession. This is the strongest possible signal that the Round 1 synthesis was well-calibrated. The deliberation has achieved genuine convergence on the foundational questions (API design, error typing, schema versioning, import sequencing).

### SA-2: P1-1 (purify schema-loading functions) is the highest-leverage change

integration-architect explicitly calls this "the single highest-leverage change" and connects it to spec 006, spec 008, and CI pipeline integration. I agree with this assessment and the reasoning. Every downstream consumer of the linter depends on being able to call schema-loading functions without triggering process termination. This is the correct P1 priority.

### SA-3: P1-4 (ConfigCondition model) correctly enables spec 006 conditional variables

integration-architect's analysis of how `ConfigCondition` enables `PRIOR_ARBITRATION_PATH` conditioning on `arbiter.timing: inter-round` is precise and matches my own assessment (A6 in my review). We both see this as establishing the typed-model precedent that spec 007 will compose with. No divergence.

### SA-4: P2-1 (MODE_PRESENCE as YAML) eliminates the largest maintenance burden

integration-architect identifies the 28-entry hardcoded dict as "the single largest maintenance burden in the linter" with "no derivation trail." This matches my own assessment from Round 1 (GE-6). We agree on both the problem characterization and the solution (mode schema YAML declarations with pure-function derivation).

### SA-5: Extension contract documentation (P2-6) is the most valuable non-code deliverable

integration-architect's Rec 4 and Rec 5 both propose addenda to P2-6, which implicitly endorses the P2-6 deliverable's importance. I explicitly called P2-6 "the single most valuable non-code deliverable in spec 005 for spec 007's benefit" (A7 in my review). We agree on the deliverable's centrality, even where we differ on specific content (see DC-2 on prescriptive vs. descriptive constraint documentation).

### SA-6: MO-3 (ROUND_SYNTHESES type mismatch) is a real bug risk

integration-architect's identification of the `ROUND_SYNTHESES` comment/schema mismatch is precise and actionable. The field is `extracted-content` in the schema, not a path list. If P1-3 (PathList) is applied mechanically to all string fields with path-related comments, this field would be incorrectly converted. I did not independently identify this specific case, but the fix is clearly correct and the P3 priority is appropriate.

### SA-7: No off-base assumptions in the Round 1 synthesis

integration-architect's review does not identify any off-base assumptions in the Round 1 synthesis itself (OBA-1 and OBA-2 are about the spec and linter, not the synthesis). My review similarly found no off-base assumptions in the synthesis (OB-1: "None identified"). This mutual validation confirms the synthesis accurately represented the deliberation.

### SA-8: Round 2 positions are refinements, not reversals

Both reviews explicitly maintain all Round 1 concessions and introduce only documentation-level refinements or new observations. integration-architect: "No Round 1 concessions are reversed. My 5 concessions from Round 1 all stand." My review: "All 7 concessions from Round 1 are maintained without reversal." The deliberation has stabilized. New Round 2 material is additive (missed opportunities, documentation addenda), not corrective.
