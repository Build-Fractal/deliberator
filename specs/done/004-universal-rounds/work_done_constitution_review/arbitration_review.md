# Constitution Compliance Review — Arbitration Templates (Spec 004)

**Reviewer**: Constitution compliance reviewer
**Date**: 2026-03-20
**Scope**: Three un-drafted arbitration templates (red-blue, winner-take-all, prisoners-dilemma) vs. constitution v1.2.0, with cooperative template as reference baseline.

---

## 1. Production Readiness Assessment

### Reference Baseline: Cooperative Template

The cooperative template (`templates/cooperative/arbitration.md`) is 124 lines and includes:
- Role framing with `{ARBITER_NAME}`, `{ARBITER_PROMPT}`
- Authority statement with grounding citation requirement
- Ordered reading list (grounding, synthesis, disputes, targets, docs)
- `{REMAINING_DISPUTES}` extraction section
- Required output sections: Process Note, Decision Framework, Binding Decisions, Summary of Changes Required, Confidence Assessment
- Detailed sub-structure for each binding decision (Positions, Synthesizer's assessment, Ruling, Grounding citation, Rationale, Rejected position, Required changes)
- Constraints section with 8 specific constraint bullets
- UNRESOLVED escape hatch

### Red-Blue Template (117 lines)

**Quality**: Production-ready. Adapts the cooperative structure to adversarial risk assessment with mode-appropriate terminology (risk disputes, RISK-ID, Red/Blue teams, severity/likelihood). Includes mode-specific ruling options (Accept Red, Accept Blue, Reclassify, Accept with monitoring) and an Updated Risk Register section. Slightly fewer constraints (6 vs 8) but all are mode-appropriate.

**Gap vs cooperative**: Missing the `{REMAINING_DISPUTES}` extraction section that the cooperative template has (the "Extracted Remaining Disputes" section at line 36-40 of cooperative). The red-blue template relies solely on the reading instructions telling the arbiter to look at "Disputed Risks". This is a functional gap — the cooperative template has both the reading instruction AND the pre-extracted disputes injected via `{REMAINING_DISPUTES}`, providing a belt-and-suspenders approach.

**Gap vs cooperative**: Missing the explicit "Cite specific identifiers" and "Attribute changes to specific files" constraint bullets that the cooperative template has. The red-blue template's "Required actions must be concrete" constraint is less specific.

### Winner-Take-All Template (108 lines)

**Quality**: Production-ready. Appropriately adapts to the competitive selection mode with Verdict Review, single Binding Decision (not per-dispute), and mode-specific ruling options (Affirm, Override, Affirm with conditions). The structure is leaner because winner-take-all arbitration resolves one question (which competitor wins) rather than N disputes.

**Gap vs cooperative**: Missing `{REMAINING_DISPUTES}` extraction section (same gap as red-blue).

**Structural difference**: Uses a single "Binding Decision" (singular) section instead of "Binding Decisions" (plural). This is appropriate because winner-take-all arbitration makes one verdict, not multiple dispute resolutions. The SKILL.md validation table correctly reflects this as "Binding Decision" (singular).

### Prisoners-Dilemma Template (114 lines)

**Quality**: Production-ready. Adapts to boundary dispute resolution with mode-appropriate concepts (claimants, trust scores, boundary specifications with owner/scope/handoff, Revised Responsibility Map). Includes the unique "Respect trust scores" constraint that maps to the mode's game-theory dynamics.

**Gap vs cooperative**: Missing `{REMAINING_DISPUTES}` extraction section (same gap as red-blue).

**Gap vs cooperative**: Missing the "Cite specific identifiers" constraint.

### Cross-Template Gap Summary

| Feature | Cooperative | Red-Blue | Winner-Take-All | Prisoners-Dilemma |
|---------|------------|----------|-----------------|-------------------|
| `{REMAINING_DISPUTES}` section | Yes | No | No | No |
| "Cite specific identifiers" constraint | Yes | No | N/A (single verdict) | No |
| "Attribute changes to specific files" constraint | Yes | No | N/A | No |

**Assessment**: The missing `{REMAINING_DISPUTES}` section is a P2 gap. The variable IS listed in SKILL.md's Phase 6 template variables (line 569) and IS populated by the orchestrator for all modes. The cooperative template uses it; the other three do not reference it. This means the orchestrator will compute and fill `{REMAINING_DISPUTES}` but the template will discard the value silently. The arbiter will still function (it reads the full synthesis), but loses the convenience of pre-extracted disputes.

---

## 2. Constitutional Principle Compliance

### Red-Blue Arbitration Template

| Principle | Verdict | Rationale |
|-----------|---------|-----------|
| I. Spec-Driven Development | PASS | Template was created per spec 004 FR-006. |
| II. Stable Interfaces | PASS | Uses all stable template variables (`{ARBITER_NAME}`, `{GROUNDING_PATH}`, etc.). Output headings match SKILL.md validation table. Dispute heading `### Disputed Risks` matches Dispute-Parsing Subsystem. |
| III. Backward-Compatible Extension | PASS | New template, no existing behavior changed. Cooperative template untouched. |
| IV. Documentation Is the Product | PASS | Template defines agent behavior with explicit instructions, required sections, and output format. No reliance on unstated conventions. |
| V. Observable Deliberation | PASS | Requires Process Note (progress reporting), Confidence Assessment (observability of decision quality). Includes UNRESOLVED escape hatch for insufficient-information cases. |
| VI. Scripts Over Markdown | PASS | Template is a parameterized prompt (executable artifact), not static prose. |
| VII. Reproducibility Over Inconsistency | PASS | Same config produces same prompt via mechanical variable substitution. Output structure is deterministic. |
| VIII. Templating Engines Over Inference | PASS | Structure is template-driven (required sections, ruling options). Agent reasoning is constrained to content within the prescribed structure. Ruling options are enumerated (Accept Red, Accept Blue, Reclassify, Accept with monitoring) rather than open-ended. |
| IX. Zen of Python Output | PASS | Output structure is clean: Process Note, Decision Framework, per-risk decisions, Updated Risk Register, Confidence Assessment. Each section has one purpose. |

### Winner-Take-All Arbitration Template

| Principle | Verdict | Rationale |
|-----------|---------|-----------|
| I. Spec-Driven Development | PASS | Created per spec 004 FR-007. |
| II. Stable Interfaces | PASS | Uses all stable template variables. Output headings match SKILL.md validation table (Process Note, Decision Framework, Verdict Review, Binding Decision). |
| III. Backward-Compatible Extension | PASS | New template, no existing behavior changed. |
| IV. Documentation Is the Product | PASS | Template is self-contained prompt engineering. No unstated conventions. |
| V. Observable Deliberation | PASS | Requires Process Note, Confidence Assessment. |
| VI. Scripts Over Markdown | PASS | Parameterized prompt template. |
| VII. Reproducibility Over Inconsistency | PASS | Deterministic variable substitution. |
| VIII. Templating Engines Over Inference | PASS | Structure is template-driven. Ruling options enumerated (Affirm, Override, Affirm with conditions). Rationale has a prescribed 5-paragraph structure. |
| IX. Zen of Python Output | PASS | Single-verdict structure is simpler than the multi-dispute modes — appropriate for the one-winner decision. Each section has one purpose. |

### Prisoners-Dilemma Arbitration Template

| Principle | Verdict | Rationale |
|-----------|---------|-----------|
| I. Spec-Driven Development | PASS | Created per spec 004 FR-008. |
| II. Stable Interfaces | PASS | Uses all stable template variables. Output headings match SKILL.md validation table (Process Note, Decision Framework, Binding Decisions, Revised Responsibility Map). Dispute heading `## Disputed Boundaries` matches Dispute-Parsing Subsystem. |
| III. Backward-Compatible Extension | PASS | New template, no existing behavior changed. |
| IV. Documentation Is the Product | PASS | Template is self-contained. Boundary specification sub-structure (Owner, Scope, Handoff) makes the output actionable. |
| V. Observable Deliberation | PASS | Process Note, Confidence Assessment, UNRESOLVED escape hatch. |
| VI. Scripts Over Markdown | PASS | Parameterized prompt template. |
| VII. Reproducibility Over Inconsistency | PASS | Deterministic variable substitution. |
| VIII. Templating Engines Over Inference | PASS | Boundary assignment structure prescribed. Trust score context provided for tiebreaking — a rule-based heuristic, not unconstrained inference. |
| IX. Zen of Python Output | PASS | Revised Responsibility Map table provides a clean, scannable summary. Each section has one purpose. |

---

## 3. Required Headings — SKILL.md Phase 6 Validation Match

The SKILL.md validation table (lines 586-593) specifies:

| Mode | SKILL.md Required Headings | Template Actual Headings | Match? |
|------|---------------------------|-------------------------|--------|
| cooperative | Process Note, Decision Framework, Binding Decisions, Summary of Changes Required | Process Note, Decision Framework, Binding Decisions, Summary of Changes Required, Confidence Assessment | PASS (superset) |
| red-blue | Process Note, Decision Framework, Binding Decisions, Updated Risk Register | Process Note, Decision Framework, Binding Decisions, Updated Risk Register, Confidence Assessment | PASS (superset) |
| winner-take-all | Process Note, Decision Framework, Verdict Review, Binding Decision | Process Note, Decision Framework, Verdict Review, Binding Decision, Confidence Assessment | PASS (superset) |
| prisoners-dilemma | Process Note, Decision Framework, Binding Decisions, Revised Responsibility Map | Process Note, Decision Framework, Binding Decisions, Revised Responsibility Map, Confidence Assessment | PASS (superset) |

Note: The original spec FR-009 proposed different heading names (Risk Framework, Binding Risk Decisions, Residual Risk Summary, etc.) but the implementation in both SKILL.md and the templates uses the headings shown above. The SKILL.md validation table and the templates are in sync. The spec FR-009 heading names are superseded by the implementation — this is a JUSTIFIED DEVIATION from the spec's letter, aligning with the implementation's decision to use "Decision Framework" consistently across all modes rather than mode-specific framework names.

All templates include "Confidence Assessment" as an additional section not in the required-headings table. This is fine — the validation checks for presence of required headings (a minimum), not an exact match. Templates may include additional sections.

**Verdict: PASS** — all templates produce headings that satisfy the SKILL.md validation requirements.

---

## 4. Template Variable Coverage

SKILL.md (lines 557-569) defines these Phase 6 template variables:

| Variable | Cooperative | Red-Blue | Winner-Take-All | Prisoners-Dilemma |
|----------|------------|----------|-----------------|-------------------|
| `{ARBITER_NAME}` | Yes | Yes | Yes | Yes |
| `{ARBITER_PROMPT}` | Yes | Yes | Yes | Yes |
| `{ARBITER_DOCS}` | Yes | Yes | Yes | Yes |
| `{GROUNDING_PATH}` | Yes | Yes | Yes | Yes |
| `{SYNTHESIS_PATH}` | Yes | Yes | Yes | Yes |
| `{ALL_DISPUTES}` | Yes | Yes | Yes | Yes |
| `{TARGET_FILES}` | Yes | Yes | Yes | Yes |
| `{TARGET_PATH}` | Not used | Not used | Not used | Not used |
| `{AGENT_NAMES}` | Yes | Yes | Yes | Yes |
| `{MODE}` | Yes | Yes | Yes | Yes |
| `{OUTPUT_PATH}` | Yes | Yes | Yes | Yes |
| `{TRIGGER}` | Yes | Yes | Yes | Yes |
| `{REMAINING_DISPUTES}` | Yes | **MISSING** | **MISSING** | **MISSING** |

**Finding**: `{REMAINING_DISPUTES}` is referenced in the cooperative template (line 38: `{REMAINING_DISPUTES}`) but absent from all three new templates. The orchestrator will still populate this variable and pass it to the template, but the template text never references it, so the populated value is silently discarded.

`{TARGET_PATH}` is not referenced in any of the four arbitration templates. This is acceptable — `{TARGET_FILES}` is the list-form variable that covers the same ground, and `{TARGET_PATH}` is documented as "primary target path" which is redundant when `{TARGET_FILES}` is present.

**Verdict**: PASS with one P2 recommendation — add `{REMAINING_DISPUTES}` extraction section to the three new templates for parity with cooperative.

---

## 5. Stable Interface Contract — Dispute Headings

The Dispute-Parsing Subsystem (SKILL.md lines 656-683) defines stable dispute headings per mode:

| Mode | Stable Dispute Heading | Template References | Match? |
|------|----------------------|---------------------|--------|
| cooperative | `### Remaining Disputes` | Cooperative template: "Remaining Disputes" section | PASS |
| red-blue | `### Disputed Risks` | Red-blue template: "Disputed Risks" section in reading instructions | PASS |
| winner-take-all | `## Runner-Up` | Winner-take-all template: "Runner-Up" section reference in reading instructions | PASS |
| prisoners-dilemma | `## Disputed Boundaries` | Prisoners-dilemma template: "Disputed Boundaries" reference in reading instructions | PASS |

All templates correctly reference the stable dispute headings that the Dispute-Parsing Subsystem uses for trigger evaluation. This means Phase 6 trigger evaluation will correctly detect disputes in synthesized outputs produced by the mode-specific Phase 5 templates.

**Verdict: PASS** — stable interface contract is maintained.

---

## 6. Antipattern Catalog Check

The antipattern catalog contains one active entry: `redundant-cache`.

**Does this change risk triggering `redundant-cache`?**

No. The arbitration templates are parameterized prompts consumed by the orchestrator — they are executable artifacts, not manually-maintained tracking documents. They do not duplicate computable state. They are structural templates that the SKILL.md engine fills with variables at runtime.

The templates do not create any new tracking documents, status files, or summary caches. The outputs they instruct the arbiter to produce (Updated Risk Register, Revised Responsibility Map, Confidence Assessment) are deliberation artifacts with original analysis, not caches of existing state.

**Verdict: PASS** — no antipattern risk.

---

## 7. Findings Summary

### PASS (no action required)

- All nine constitutional principles are satisfied by all three templates.
- Required headings in all templates match the SKILL.md Phase 6 validation table.
- Stable interface contract for dispute headings is maintained.
- Template variables (except `{REMAINING_DISPUTES}`) are properly referenced.
- No antipattern risks identified.
- Spec FR-009 heading names vs SKILL.md/template heading names: JUSTIFIED DEVIATION — the implementation chose consistent "Decision Framework" naming across all modes, which is cleaner than mode-specific framework names. Both SKILL.md and templates are in sync with each other.

### P2 Recommendations (not blocking, improve parity)

1. **Add `{REMAINING_DISPUTES}` section to all three templates.** The cooperative template includes an "Extracted Remaining Disputes" section (lines 36-40) that pre-injects the dispute content extracted by the orchestrator. The three new templates omit this. The arbiter will still function (it reads the full synthesis), but loses the belt-and-suspenders redundancy. Recommend adding the following section to each template, after the reading list and before "What to Produce":

   ```markdown
   ## Extracted Remaining Disputes

   The remaining disputes from the synthesis have been extracted for you:

   {REMAINING_DISPUTES}

   These are the disputes you must resolve. If this section is empty, read the full synthesis to identify any remaining disputes.
   ```

   Adapt the wording per mode:
   - Red-blue: "remaining disputed risks"
   - Winner-take-all: "the contested verdict elements" (or omit — single-verdict mode may not need it)
   - Prisoners-dilemma: "remaining boundary disputes"

2. **Add "Cite specific identifiers" constraint to red-blue and prisoners-dilemma templates.** The cooperative template has two constraint bullets about citing specific FR/SC identifiers and attributing changes to specific files. These are good prompt engineering practices that improve output actionability. The red-blue and prisoners-dilemma templates would benefit from equivalent constraints referencing RISK-IDs and boundary specifications respectively.

### Overall Assessment

The three templates are production-ready. They maintain structural consistency with the cooperative reference template while appropriately adapting terminology, ruling structures, and constraint language to each mode's game-theory dynamics. The SKILL.md validation table is in sync with the templates. The `draft` markers were correctly removed. Constitution compliance is complete across all nine principles.
