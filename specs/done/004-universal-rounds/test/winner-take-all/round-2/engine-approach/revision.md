# Engine-Approach: Round 2 Revision

**Status**: All 3 disputes resolved. Convergence confirmed.

---

## Final Position

The template-first architecture is correct. My three proposals are documentation and specification enhancements within that architecture. The template-approach has accepted all three. No architectural changes, no engine expansion, no conditional branches added.

---

## Dispute 1: Mode-Keyed Tables as Interface Contract

**Resolved.** Both sides agree: add a "Mode Interface Contract" subsection to SKILL.md documenting the three mode-keyed data tables (Dispute-Parsing Subsystem headings, Phase 6 validation headings, role enforcement rules) with a new-mode checklist. The template-approach accepted the dedicated-section format over extending the existing paragraph at line 683.

The terminological question -- whether this constitutes "architectural significance" or "documentation significance" -- is moot. Both labels produce the identical concrete action. I drop the "architectural significance" framing without reservation.

## Dispute 2: Role Enforcement as Engine-Owned Config Validation

**Resolved.** Both sides agree: mode-specific configuration validation rules (currently: red-blue role coverage) are engine-owned, scoped to parse-time preconditions, and belong as a fourth item in the Mode Interface Contract section. The generalization to runtime mode behavior is withdrawn. The factual disagreement about whether role enforcement is "structurally identical" or "categorically different" from generic validation has no practical consequence -- both framings yield the same documentation.

I accept the template-approach's proposed wording: "Some configuration validation rules are mode-specific (e.g., role coverage requirements). These are parse-time preconditions, not runtime mode behavior, and belong in the engine's config validation layer."

## Dispute 3: Linter Classification

**Resolved.** Both sides agree on the linter's specification: it validates template output headings against SKILL.md's mode-keyed dispatch tables, runs at development time, and requires updates when either side of the interface changes. The bidirectional dependency is documented in the linter's specification and referenced from the Mode Interface Contract section.

On labeling: the template-approach offered "interface-contract enforcement tool" as an acceptable alternative to "template validation tool." I accept either label. If a single term is needed, "interface-contract validation tool" captures both sides' emphasis. The classification has no practical impact on where the linter runs or how it is implemented.

---

## Convergence Summary

| Dispute | Agreed Action | Type |
|---------|---------------|------|
| 1. Mode-keyed tables | Add "Mode Interface Contract" subsection to SKILL.md with three-table checklist | Documentation |
| 2. Role enforcement | Add mode-specific config validation as fourth item, scoped to parse-time preconditions | Documentation |
| 3. Linter | Define by specification (inputs, outputs, timing, dependencies); label as "interface-contract validation tool" if needed | Specification |

No remaining disagreements require adjudication. The deliberation has converged.
