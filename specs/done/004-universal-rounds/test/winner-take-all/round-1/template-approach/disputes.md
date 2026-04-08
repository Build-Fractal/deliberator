# Template-Approach: Final Statement

## Remaining Disputes

**Dispute: The label "mode-agnostic" vs. "mode-parameterized" has architectural significance, not just documentation significance.**

The engine-approach insists that the engine's three mode-keyed data structures make the label "mode-agnostic" misleading, and that "mode-parameterized" is the only honest descriptor. I adopted "mode-parameterized" in my revision (CA-4) and consider this a terminology improvement. However, the engine-approach treats this relabeling as if it carries architectural weight -- as if acknowledging mode-parameterization somehow validates the thesis that mode behavior belongs in the engine. It does not. The relabeling is a documentation concern. The engine's algorithm remains mode-invariant. Adding rows to a lookup table is categorically different from adding conditional branches. The engine-approach's own revision (N3) concedes that "the distinction has architectural substance" and that lookup tables are "additive, non-branching, declarative." Once you concede that, the relabeling is a naming fix, not an architectural discovery.

**Dispute: Role enforcement as evidence for expanding engine-level mode awareness.**

The engine-approach's strongest surviving argument (Advantage 3) is that role enforcement -- e.g., red-blue requiring at least one red and one blue agent -- is a mode-specific invariant that templates cannot express. This is factually correct. Templates run after configuration validation; they cannot reject a misconfigured `conversus.yml`. But the engine-approach overreaches when it uses this to argue for a general principle that "mode behavior belongs in the engine." Role enforcement is a configuration validation concern, not a mode behavior concern. It runs at config parse time, before any template loads, before any phase executes. It is structurally identical to validating that `rounds` is a positive integer or that `agents` is a non-empty list. The fact that different modes have different valid agent configurations does not mean that the analytical frameworks, output structures, and prompt engineering that define each mode's character should also live in the engine. Configuration validation and runtime behavior are separate architectural layers. Role enforcement belongs in the former; mode-specific behavior belongs in templates via the latter.

**Dispute: Where automated heading validation should run.**

Both sides agree that heading drift (e.g., templates using `### Remaining Contested Positions` instead of `### Remaining Disputes`) should be caught by automated validation. The engine-approach originally proposed runtime engine-level validation. In their revision (Advantage 6), they withdrew the claim that this must be runtime/engine-level and acknowledged that "a development-time linter or pre-execution check is a better fit." However, they note that "a linter is not a template -- it is engine-adjacent infrastructure." I contest the characterization "engine-adjacent." A template linter validates templates against the stable interface contract defined in SKILL.md. It is a development tool, like a schema validator or a type checker. It does not execute during conversus runs. It does not modify engine behavior. It belongs in the development toolchain (CI, pre-commit hooks, review workflows), not in the engine's execution path. Calling it "engine-adjacent" implies it should be coupled to the engine, which would conflate development-time validation with runtime orchestration.

---

## Convergence

The following positions are now agreed by both sides:

1. **The template-first architecture is correct.** The engine-approach's revision states explicitly: "The template-first architecture is the correct framing" and "I argued for a paradigm shift but was actually proposing an incremental enhancement to the existing architecture." Both sides agree that mode-specific behavior -- analytical frameworks, output structures, prompt engineering -- belongs in templates.

2. **The engine is mode-parameterized, not mode-agnostic.** The template-approach adopted "mode-parameterized" in CA-4. The engine-approach proposed this terminology. Both sides agree the engine maintains bounded, data-level mode awareness via three lookup tables (Dispute-Parsing Subsystem headings, Phase 6 validation headings, role enforcement rules).

3. **The engine's mode awareness is data, not logic.** The engine-approach conceded this in N3: "The engine's mode awareness is genuinely the former [lookup tables: additive, non-branching, declarative]." The template-approach has consistently maintained this position. Both sides now agree that the mode-keyed structures in SKILL.md are parameterized data for a uniform algorithm, not conditional branching.

4. **Adding a new mode requires bounded, non-breaking data additions to the engine.** The template-approach withdrew "zero engine changes" and specified the actual cost: one Dispute-Parsing row, one Phase 6 validation row, one enum entry, potentially one role rule, plus template files. The engine-approach acknowledged in N2 that this is "a lightweight, scalable pattern" and withdrew the characterization of "just add templates" as "aspirational marketing."

5. **Principle VIII supports the template-first architecture.** The engine-approach withdrew their constitutional argument (Advantage 4): "The constitution favors templates for mode-specific behavior and the engine for mode-agnostic orchestration parameterized by mode data. This is the template-first position."

6. **Heading drift requires automated validation.** Both sides agree the heading inconsistencies found during review should be caught by automated tooling. The disagreement on where that tooling runs (development-time linter vs. runtime check) is narrow, and the engine-approach has largely conceded toward development-time validation.

7. **FR-001's direction of change supports the template-first thesis.** The engine-approach did not contest the argument (NA-3) that spec 004 removed engine mode-awareness (deleting validation restrictions) rather than adding it, and acknowledged in N2 that "FR-001 REMOVED engine mode-awareness -- this moved the engine toward mode-agnosticism, the opposite of my thesis."

8. **Role enforcement is a genuine engine-level concern.** The template-approach acknowledges that configuration validation invariants (e.g., red-blue requires red and blue agents) cannot be expressed in templates and correctly belong in the engine's config validation layer.

9. **The engine-approach's concrete deliverables are enhancements to the template-first architecture, not replacements.** The engine-approach conceded this in N1: "this characterization is largely accurate" and in their revised verdict: "My strongest surviving arguments (role enforcement, heading validation) are compatible with the template-first architecture and do not require an alternative paradigm."

---

## Final Position Statement

### Non-Negotiables

1. **Templates own mode-specific behavior.** The analytical frameworks, output structures, phase-specific instructions, and prompt engineering that make each mode distinct live in template files organized by mode. This is the architecture that shipped, that the spec mandated (spec.md Section 6: "Template-First Approach"), that the constitution endorses (Principle VIII), and that the engine-approach's own revision accepts. Any proposal that moves mode-specific behavioral logic from templates into the engine violates this principle.

2. **The engine's algorithm is mode-invariant.** The round loop, phase sequence, stagnation detection algorithm (count comparison), and Phase 6 trigger evaluation use identical logic across all four modes. They are parameterized by mode-keyed data (which headings to search, which patterns to count), but the algorithm applied to that data does not branch per mode. This invariance is what makes new modes cheap to add and existing modes safe from cross-contamination.

3. **Mode-keyed data in the engine is bounded and declarative.** The three lookup tables in SKILL.md (Dispute-Parsing headings, Phase 6 validation headings, role enforcement rules) are the complete set of engine-level mode awareness. They are additive (new rows do not affect existing rows), non-branching (no if/else paths), and declarative (state what to look for, not how to behave). Any future engine enhancement must preserve these properties.

4. **Each template is independently reviewable against constitutional principles.** This is the conceded advantage (CA-3) that neither side disputes. Template isolation enables per-mode, per-phase review without navigating interleaved conditional branches. Any architectural change that distributes mode behavior across engine logic would degrade this property.

### Flexibility

1. **Terminology.** I have adopted "mode-parameterized" over "mode-agnostic" and consider the terminology debate resolved. If the engine-approach or the judge prefers a different precise label that acknowledges bounded data-level mode awareness without implying logic-level branching, I am open to it.

2. **Automated heading validation.** I support adding automated heading validation as a development-time tool (linter, CI check, pre-commit hook). I am flexible on the exact mechanism. If the judge or the engine-approach can demonstrate that a lightweight pre-execution check (not full runtime validation, but a fast sanity check before phase execution begins) provides meaningfully better coverage than a development-time linter without adding runtime fragility, I would consider it.

3. **Mode registry consolidation.** The engine-approach proposed consolidating the three existing lookup tables into a single "Mode Registry" section in SKILL.md. This is a documentation reorganization with no behavioral impact. I am neutral on it -- if it improves readability for future maintainers, it is a reasonable change. It does not alter the template-first architecture.

4. **Role enforcement expansion.** I accept that future modes may require new engine-level configuration validation rules (e.g., "auction mode requires at least three agents"). These are config-parse-time invariants, not runtime mode behavior. I am flexible on how they are structured, provided they remain in the configuration validation layer and do not expand into runtime orchestration logic.
