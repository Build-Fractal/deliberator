# Template Engineer — Round 1 Review

## Assessment Scope

Reviewing the 4 new mode templates (negotiation, resource-allocation, fair-division, mechanism-design) against the original 4 modes for structural validity, dispute heading correctness, DISPUTES marker presence, and quality parity.

## Target Files Examined

- `specs/028-mode-expansion/spec.md`
- `engine/config.py`
- `conversus/schemas/construction.py`
- `templates/negotiation/review.md`
- `templates/negotiation/synthesis.md`
- `templates/resource-allocation/synthesis.md`
- `templates/fair-division/synthesis.md`
- `templates/mechanism-design/synthesis.md`
- `tests/test_mode_expansion.py`

---

### 1. Structural Validity — Do Templates Produce Parseable Output?

**PASS with observations.**

All 4 new mode synthesis templates use the same structural pattern as cooperative: variable placeholders (`{MODE}`, `{AGENT_NAMES}`, `{TARGET_PATH}`, `{ALL_REVIEWS}`, `{ALL_CROSS_REVIEWS}`, `{ALL_REVISIONS}`, `{ALL_DISPUTES}`, `{OUTPUT_PATH}`) are consistent with the engine's template variable injection system defined in `schema/variables.yml`.

The negotiation `review.md` template introduces mode-specific placeholders: `{TARGET_FILES}`, `{AGENT_DOCS}`, `{PRIOR_FILES_SECTION}`, `{PRIOR_ROUND_SECTION}`, `{PRIOR_ARBITRATION_SECTION}`. These match the cooperative `review.md` variable set exactly.

**Observation TE-R1-01**: The negotiation synthesis uses `{TARGET_PATH}` (singular) while the review template uses `{TARGET_FILES}` (plural). This is consistent with how the cooperative mode works (review gets the full list, synthesis gets a single reference), but it requires verification that the engine correctly resolves both for the negotiation mode specifically.

### 2. Dispute Headings — Correct for Dispute-Parsing Subsystem?

**PASS.** Each new mode's synthesis template uses a distinct dispute heading that matches its `schema/modes/*.yml` definition:

| Mode | Synthesis Dispute Heading | Schema `synthesis_heading` | Match? |
|------|--------------------------|---------------------------|--------|
| negotiation | `### Unresolved Terms` | `### Unresolved Terms` | YES |
| resource-allocation | `### Contested Allocations` | `### Contested Allocations` | YES |
| fair-division | `### Disputed Valuations` | `### Disputed Valuations` | YES |
| mechanism-design | `### Mechanism Vulnerabilities` | `### Mechanism Vulnerabilities` | YES |

Each dispute heading is semantically appropriate to its mode's domain language:
- Negotiation uses "Terms" (contract/deal terminology)
- Resource allocation uses "Allocations" (distribution terminology)
- Fair division uses "Valuations" (subjective value terminology)
- Mechanism design uses "Vulnerabilities" (system design terminology)

The `entry_pattern` values also correctly correspond to the template content:
- `**Term:` matches `- **Term: [Label]**` in negotiation synthesis
- `**Contested:` matches `- **Contested: [Resource label]**` in resource-allocation synthesis
- `**Disputed:` matches `- **Disputed: [Item label]**` in fair-division synthesis
- `**Vulnerability:` matches `- **Vulnerability: [Label]**` in mechanism-design synthesis

### 3. DISPUTES Markers — Present in All Synthesis Templates?

**PASS.** All 4 new synthesis templates contain both structural markers:

| Template | `DISPUTES_BEGIN` | `DISPUTES_END` | Correct Position? |
|----------|-----------------|----------------|-------------------|
| `templates/negotiation/synthesis.md` | Line ~101 | Line ~111 | YES — wraps Unresolved Terms |
| `templates/resource-allocation/synthesis.md` | Line ~91 | Line ~101 | YES — wraps Contested Allocations |
| `templates/fair-division/synthesis.md` | Line ~88 | Line ~98 | YES — wraps Disputed Valuations |
| `templates/mechanism-design/synthesis.md` | Line ~103 | Line ~113 | YES — wraps Mechanism Vulnerabilities |

The markers use the `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` HTML comment format, matching the cooperative synthesis template exactly.

**Observation TE-R1-02**: The `schema/modes/*.yml` files for all 4 new modes specify `structural_markers: true` and also `cross_round_synthesis.structural_markers: true`. This means the `cross-round-synthesis.md` templates for each new mode also need `DISPUTES_BEGIN/END` markers. I have not reviewed those templates, but the schema requirement is properly declared.

### 4. Template Quality — Comparable to Original 4 Modes?

**PASS with one concern.**

**Strengths:**
- All new templates follow the same structure: context section, what-to-read section, what-to-produce section, rules section. This mirrors cooperative, winner-take-all, prisoners-dilemma, and red-blue.
- Mode-specific terminology is well-chosen: "mediator" for negotiation, "allocator" for resource-allocation, "divider" for fair-division, "mechanism designer" for mechanism-design. The cooperative mode uses "synthesizer" — each new mode has its own role name.
- The negotiation synthesis includes a ZOPA Analysis and Deal Terms Scorecard that are genuinely mode-specific — not just renamed cooperative sections. The resource-allocation template has a Shapley Value Assessment and Allocation Table. Fair-division has Envy-Free Analysis and Fairness Guarantees. Mechanism-design has a Property Assessment Matrix and Vulnerability Report.
- All templates include the Arbiter-Resolved Disputes section with the "omit if not applicable" instruction, matching the cooperative pattern.
- The Key Concessions section is present in all templates, maintaining the deliberation record.

**Concern TE-R1-03**: The negotiation `review.md` template (Phase 1) is significantly more structured than the cooperative `review.md`. It prescribes 4 specific sections (Interests Declaration, Opening Offer, ZOPA Assessment, Risk Factors) with detailed subsection structure. The cooperative review template is more open-ended. This is not necessarily wrong — negotiation requires more structured opening positions — but it means the negotiation mode produces more constrained Phase 1 output, which could limit the richness of cross-review. Whether this is a strength or weakness depends on whether the structured output helps or hinders the mediator's synthesis.

### 5. Test File Status

**FAIL.** `tests/test_mode_expansion.py` is empty (0 bytes). FR-011 (backward compatibility) and SC-005 (all existing tests pass) require test coverage. Without tests, there is no way to verify that the mode expansion does not break existing functionality.

---

## Summary

| Check | Result |
|-------|--------|
| Structural validity | PASS |
| Dispute headings | PASS |
| DISPUTES markers | PASS |
| Quality parity | PASS (with minor concern) |
| Test coverage | FAIL — empty test file |

### Recommendations

1. **P1 — Must**: `tests/test_mode_expansion.py` must contain tests that verify: (a) all 8 modes are in `VALID_MODES`, (b) each new mode has a complete template set (7 templates), (c) the decision type classifier routes new keywords correctly, (d) existing tests still pass.

2. **P2 — Should**: Verify that the `cross-round-synthesis.md` templates for all 4 new modes contain `DISPUTES_BEGIN/END` markers (schema requires it but templates were not reviewed).

3. **P3 — Consider**: Evaluate whether the negotiation review template's highly structured Phase 1 output format is optimal or overly constraining.
