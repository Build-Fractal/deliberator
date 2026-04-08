# Cross-Review of integration-architect (Round 2)

**Cross-reviewer**: functional-typing
**Reviewing**: integration-architect Round 2 review
**Date**: 2026-03-21

---

## Dangerous Contradictions

### DC-1: MO-1 (SKILL.md invocation pathway) presupposes a runtime model that conflicts with the programmatic API's purpose

integration-architect's MO-1 identifies that the SKILL.md `allowed-tools` frontmatter does not authorize `uv run python linter/validate.py`, and proposes updating `allowed-tools` to permit this CLI invocation. However, the entire point of the P1-2 programmatic API convergence -- which integration-architect explicitly endorses as "the mechanism spec 008 should use" -- is to decouple validation from CLI invocation. The recommendation simultaneously (a) affirms `validate_all(config: ValidationConfig)` as the canonical API and (b) proposes solving the invocation problem via CLI shell-out with `allowed-tools` whitelisting.

These are architecturally contradictory. If the programmatic API is the right abstraction, the SKILL.md step should describe calling it as a library function (option 2 in integration-architect's own analysis), not shelling out to the CLI entry point. If the CLI entry point is what gets whitelisted, then the programmatic API is not the invocation mechanism -- it is an internal implementation detail behind the CLI, and the "decoupled from CLI" property that P1-2 was designed to achieve is not exercised by the primary consumer.

integration-architect acknowledges this tension by listing both options but then recommends the CLI path (Rec 1: "SKILL.md Step 3's validation invocation should use `Bash` tool with `uv run python linter/validate.py --mode {mode}`"). This contradicts the Round 1 synthesis rationale for P1-2, which states the API exists so that spec 008 and CI pipelines can call the linter "without going through the Click CLI."

The resolution is not to pick one option -- it is to recognize that the SKILL.md invocation pathway is a spec 008 concern (executable conversus), not a spec 005 concern. Spec 005 delivers the library API. Spec 008 defines how the orchestrator calls it. Labeling this P2 in spec 005 is scope inflation of exactly the kind Round 1 identified and corrected in game-engine-advocate's original recommendations.

### DC-2: Rec 4 (filename-phase constraint) conflicts with MO-2 (reverse template check) on what constitutes a valid template

integration-architect's MO-2 proposes that the linter should report template files on disk that are not listed in the mode schema's `templates` field. Rec 4 then proposes documenting that "template filenames must match phase names exactly" and that variant templates must use conditional blocks, not separate files.

These two recommendations create a subtle contradiction when combined. MO-2 treats the mode schema `templates` list as the authoritative registry of valid templates -- if a file exists but is not in the list, it is orphaned and should be reported. Rec 4 treats the filename itself as the authoritative identifier of the phase -- if the filename does not match a known phase name, the template is invalid regardless of whether it appears in the mode schema.

The contradiction emerges when a template file exists, IS listed in the mode schema's `templates` field, but has a filename that does not match a known phase name. Under MO-2, this template is valid (it is declared in the schema). Under Rec 4, it is invalid (its filename is not a recognized phase). The linter cannot simultaneously trust the mode schema as the source of truth for template validity (MO-2) and trust the filename-phase mapping as the source of truth (Rec 4) without defining which takes precedence.

This is resolvable -- the mode schema `templates` list should be validated against known phase names, making both checks reinforce rather than conflict. But integration-architect does not propose this bridging validation, leaving the two recommendations in tension.

---

## Tensions

### T-1: MO-3 (ROUND_SYNTHESES comment fix) scope vs. systematic type audit

integration-architect correctly identifies that `ROUND_SYNTHESES` has a misleading comment ("newline-separated paths") that contradicts the schema's `type: extracted-content`. The recommendation to fix the comment and exclude this field from P1-3's PathList conversion is sound.

However, this raises a broader question that integration-architect does not address: how many other fields have comments that disagree with their schema types? If ROUND_SYNTHESES has a misleading comment, the same drift could exist on other fields. A point fix on one field is appropriate at P3, but the pattern suggests a systematic audit of all model field comments against their schema declarations should accompany P1-3 (PathList conversion), since that work already requires examining every path-like field.

My MO-1 (ValidationContext dataclass) and integration-architect's MO-3 are complementary but address different layers: mine refactors function signatures, integration-architect's fixes data-level comment drift. Neither proposes the systematic audit that would catch all instances of the ROUND_SYNTHESES pattern.

### T-2: OBA-2 (validate_templates granularity) direction vs. my OBA-2 (condition field structure)

integration-architect's OBA-2 proposes that `validate_templates` may evolve from boolean to a structured config (e.g., `{variables: true, headings: false}` or `{skip_modes: [auction]}`). My OBA-2 observes that the `condition` field in `variables.yml` has a similar gap between the spec's aspiration (parseable expressions like `"rounds > 1"`) and the implementation's reality (prose documentation strings).

Both observations point to the same systemic tension: the spec describes several fields that are simple scalars today but will need structured evolution. The risk is that each field evolves independently with its own ad-hoc structure, rather than adopting a consistent pattern for "scalar that becomes structured." P1-4's `ConfigCondition` model is the right pattern for this evolution (typed model replaces unstructured field), but neither review explicitly proposes applying this pattern to `validate_templates` when it eventually needs granularity.

This is a low-severity tension -- it is about future consistency, not current correctness -- but it is worth flagging so that P2-6 (Extension Points documentation) can name the pattern: "When a scalar field needs structured evolution, introduce a typed model; do not evolve to an untyped dict."

### T-3: Rec 5 (validate_templates evolution path) implies forward compatibility that contradicts the "freeze first" principle

The Round 1 synthesis established a systemic principle (S1): "freeze first, compose later." integration-architect's Rec 5 proposes documenting that `validate_templates` "may evolve to accept a structured config object" and that "the boolean form must remain valid for backward compatibility." This pre-commits the field to backward-compatible evolution, which constrains how the structured form can be designed. For example, if `validate_templates: true` must remain valid, the structured form cannot use the same field name with an incompatible type in strictly-typed YAML consumers -- it would need to be a union type (`bool | ValidateTemplatesConfig`), which is an antipattern in Pydantic models.

The "freeze first" principle would say: document the boolean as the current contract, note that it may be revisited, but do NOT commit to backward compatibility of the boolean form. Spec 007 or whatever spec introduces granular validation should be free to replace the boolean entirely if the structured form is cleaner.

This tension is minor and documentation-only, but the phrasing "the boolean form must remain valid" is a stronger commitment than the "freeze first" principle warrants at this stage.

### T-4: Dispute 2 refinement alignment

integration-architect accepts the synthesizer's Dispute 2 resolution (`str` with `KNOWN_ERROR_TYPES` frozenset and `@field_validator`) without refinement. My review accepts the same resolution but proposes that the `@field_validator` should issue a warning for unknown error types rather than reject the `LintError` instance. integration-architect's phrasing -- "validate at construction time against a known set" -- is ambiguous between warn-and-accept and reject-on-unknown.

The difference matters for plugin extensibility. If the validator rejects unknown types, plugin-contributed `check_*` functions cannot return custom error types without first registering them in the core module -- recreating the `Literal` closed-set problem in runtime form. If the validator warns but accepts, the set serves documentation and autocompletion without gatekeeping.

integration-architect does not address this distinction, which means the two reviews could produce conflicting implementations: one that rejects unknown types (integration-architect's reading) and one that warns (my proposal). This should be resolved in the synthesis.

---

## Safe Agreements

### SA-1: All four Round 1 dispute resolutions are accepted

Both reviews accept all four synthesizer resolutions without reversal. integration-architect explicitly endorses each resolution with reasoning; my review concurs with three and refines the fourth (Dispute 2) without reversing it. There is no dispute over dispute resolutions.

### SA-2: P1-1 (purify schema-loading functions) is the highest-leverage change

Both reviews independently identify P1-1 as the single most important change. integration-architect frames it as the prerequisite for all downstream integration (spec 006, spec 008, CI pipelines). I frame it as the prerequisite for functional correctness (testability, composability). The framing differs; the conclusion is identical.

### SA-3: P1-4 (ConfigCondition model) is critical for spec 006 interop

integration-architect emphasizes that ConfigCondition enables spec 006's `PRIOR_ARBITRATION_PATH` conditioned on `arbiter.timing: inter-round`. My review does not re-argue this point but endorses it through the Round 1 convergence. Both reviews treat P1-4 as correctly prioritized and well-designed.

### SA-4: All Round 1 concessions are maintained

integration-architect explicitly lists all 5 Round 1 concessions as standing. My review similarly does not reverse any prior concessions. Neither reviewer attempts to re-litigate settled items. The deliberation has no backsliding.

### SA-5: MODE_PRESENCE migration (P2-1) is high-value maintenance debt elimination

integration-architect calls the hardcoded 28-entry dict "the single largest maintenance burden in the linter." My review endorsed this item through Round 1 convergence. Both reviews treat P2-1 as the most impactful P2 item.

### SA-6: New recommendations are correctly prioritized at P2-P3

integration-architect introduces 5 new items: 2 at P2 (Rec 1, Rec 4/5 as P2-6 addenda), 2 at P3 (Rec 2, Rec 3), and one documentation-only (Rec 4). My review introduces 3 new items: 1 at P2 (MO-1), 1 at P3 (MO-2), and 1 editorial (OBA-2). Neither reviewer introduces new P1 items, which is appropriate for Round 2 -- the P1 set is settled.

### SA-7: The ROUND_SYNTHESES field must not be converted to PathList

integration-architect's MO-3 identifies that `ROUND_SYNTHESES` is `type: extracted-content` in the schema, not a path-list, and must be excluded from P1-3's PathList conversion. My review does not address this specific field but the conclusion is consistent with my P1-3 endorsement, which specifies applying PathList only to path-list fields. The explicit exclusion call-out is a useful guard against mechanical over-application.

### SA-8: No new P1 disputes are introduced

Both reviews focus Round 2 energy on refinements, missed opportunities, and forward-looking documentation rather than re-opening fundamental architectural questions. This signals that the Round 1 synthesis successfully resolved the design-level disagreements.
