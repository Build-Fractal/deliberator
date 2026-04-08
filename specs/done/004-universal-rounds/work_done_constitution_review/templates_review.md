# Constitution Compliance Review — Cross-Round Synthesis Templates

**Reviewer**: Constitution compliance reviewer
**Date**: 2026-03-20
**Constitution version**: 1.2.0
**Spec under review**: `specs/004-universal-rounds/spec.md`
**Templates reviewed**:
- `templates/red-blue/cross-round-synthesis.md`
- `templates/winner-take-all/cross-round-synthesis.md`
- `templates/prisoners-dilemma/cross-round-synthesis.md`
- Reference: `templates/cooperative/cross-round-synthesis.md`

---

## 1. Red-Blue Cross-Round Synthesis

### I. Spec-Driven Development — PASS

The template was created pursuant to FR-003 of spec `004-universal-rounds`. The spec was written before the template was implemented, and the template satisfies the spec's requirements: it tracks risk evolution, attack pattern shifts, defense effectiveness improvements, and produces a final risk register.

### II. Stable Interfaces — PASS

- **Template variables**: Uses the correct `{VARIABLE}` syntax. All nine variables specified in FR-003 are present: `{ROUND_SYNTHESES}`, `{ROUNDS_COMPLETED}`, `{MAX_ROUNDS}`, `{TERMINATION_REASON}`, `{MODE}`, `{TARGET_FILES}`, `{TARGET_PATH}`, `{AGENT_NAMES}`, `{OUTPUT_PATH}`.
- **Dispute heading**: The template uses `### Disputed Risks` (line 114), which matches the SKILL.md stable interface contract: `### Disputed Risks` heading with `**[RISK-ID]` entries beneath it. This is correct.
- **Structural markers**: The template does not include `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` markers around the Disputed Risks section. This matches the cooperative cross-round synthesis reference, which also omits them. The per-round synthesis templates include these markers, but the cross-round synthesis is a different artifact that feeds into Phase 6 trigger evaluation via its own output path. Since the Dispute-Parsing Subsystem states heading-based parsing is the fallback when markers are absent, this is functionally correct but suboptimal — including the markers would give the parser the primary (more reliable) parsing path. **Observation, not a violation**, since the cooperative reference template also omits them.

### III. Backward-Compatible Extension — PASS

This is a purely additive template. It creates a new file in a new template slot (`templates/red-blue/cross-round-synthesis.md`) that did not previously exist. No existing templates or behavior are modified.

### IV. Documentation Is the Product — PASS

The template contains mode-specific prompt engineering appropriate to red-blue adversarial dynamics. It correctly instructs the synthesizer on the red-blue-specific analytical framework: risk trajectory, defense effectiveness progression, attack pattern shifts, and a final risk register with Landed/Mitigated/Accepted/Disputed categories.

### V. Observable Deliberation — PASS

The template requires a Process Summary section with statistical counts, per-round risk counts, and termination reason. This ensures the cross-round synthesis is self-documenting about the deliberation process.

### VI. Scripts Over Markdown — PASS

The template is a parameterized prompt (structured data with `{VARIABLE}` substitution), not freeform prose. It drives agent behavior through explicit section requirements and rules.

### VII. Reproducibility Over Inconsistency — PASS

Same config produces same prompts. All variables are mechanically substituted. The template structure is deterministic — same sections in same order every time. The output path is explicit.

### VIII. Templating Engines Over Inference — PASS

The template heavily constrains agent behavior:
- Six mandatory sections in a prescribed order (Process Summary, Risk Trajectory, Defense Effectiveness Progression, Attack Pattern Shifts, Final Risk Register, Disputed Risks, Termination Assessment).
- Explicit table formats for risk tracking.
- Required classification categories for persisting risks (Escalating, Narrowing, Stagnant, Oscillating).
- Required categories for the final risk register (Landed, Mitigated, Accepted, Required Mitigations).
- Explicit rules section constraining synthesizer behavior (neutrality, tracing, no new risks, completeness).
- Defense effectiveness ratio formula provided, eliminating the need for inference about how to measure it.

### IX. Zen of Python Output — PASS

The output structure is clean and predictable. Each section has one clear purpose. The template follows the same structural pattern as the cooperative reference (Context, What to Read, What to Produce, Rules) while adapting content for red-blue semantics. Flat structure — no unnecessary nesting.

---

## 2. Winner-Take-All Cross-Round Synthesis

### I. Spec-Driven Development — PASS

Created pursuant to FR-004. The template satisfies all spec requirements: tracks proposal evolution, identifies incorporated vs. ignored feedback, assesses whether the winner improved or merely survived, and produces a final ranking.

### II. Stable Interfaces — VIOLATION

**Finding 1: Dispute heading mismatch.**

The SKILL.md Dispute-Parsing Subsystem stable interface contract defines the winner-take-all dispute heading as `## Runner-Up` (presence indicates a contested decision). The per-round synthesis template (`templates/winner-take-all/synthesis.md`) uses both `## Runner-Up` and `### Remaining Disputes` (the latter wrapped in `DISPUTES_BEGIN`/`DISPUTES_END` markers).

The cross-round synthesis template uses:
- `## Runner-Up` (line 84) — matches the stable interface.
- `### Remaining Contested Positions` (line 95) — this heading does NOT match the stable interface. The SKILL.md contract specifies `### Remaining Disputes` for winner-take-all fallback heading-based parsing (via `## Runner-Up`). The per-round synthesis uses `### Remaining Disputes`. The cross-round synthesis renames this to `### Remaining Contested Positions`.

This is a **heading rename** that could affect the Dispute-Parsing Subsystem if the cross-round synthesis is ever fed into Phase 6 trigger evaluation. The Dispute-Parsing Subsystem for winner-take-all mode looks for `## Runner-Up`, which IS present, so the parser would still detect disputes via the `## Runner-Up` heading. However, the heading inconsistency between the per-round synthesis (`### Remaining Disputes`) and the cross-round synthesis (`### Remaining Contested Positions`) breaks the naming convention and could confuse consumers that expect consistent heading names across synthesis artifacts.

**Severity**: Low — functionally the parser would still work because `## Runner-Up` is present and is the primary heading the parser checks. But the heading rename is an unnecessary deviation from the per-round synthesis naming convention and introduces a gratuitous inconsistency.

**Recommendation**: Rename `### Remaining Contested Positions` to `### Remaining Disputes` to match the per-round synthesis template and the stable interface naming convention. The content can remain winner-take-all-specific while using the standard heading.

**Finding 2: Template variables — PASS.** All required variables present with correct `{VARIABLE}` syntax.

### III. Backward-Compatible Extension — PASS

Purely additive. New file in a previously empty slot.

### IV. Documentation Is the Product — PASS

Mode-specific prompt engineering appropriate to competitive dynamics. The template correctly distinguishes between "earned victories" (improved under pressure) and "default victories" (won because competition was weak), which is the key analytical insight for winner-take-all.

### V. Observable Deliberation — PASS

Process Summary requires per-round winners, ranking stability assessment, and statistical overview.

### VI. Scripts Over Markdown — PASS

Parameterized prompt with structured sections and variable substitution.

### VII. Reproducibility Over Inconsistency — PASS

Deterministic template structure. Same config produces same prompts.

### VIII. Templating Engines Over Inference — PASS

The template constrains agent behavior effectively:
- Six mandatory sections in prescribed order.
- Ranking trajectory table with required columns.
- Per-competitor proposal evolution tracking with required sub-sections (thesis, adaptations, feedback incorporated, feedback ignored, net trajectory).
- Explicit winner analysis structure (winning criteria, how earned, conceded weaknesses, surviving advantages).
- Runner-up analysis with required "conditions for reconsideration."
- Rules section constraining synthesizer behavior.

### IX. Zen of Python Output — PASS

Clean, predictable structure. Each section has one clear purpose. Follows the cooperative reference's structural pattern.

---

## 3. Prisoners-Dilemma Cross-Round Synthesis

### I. Spec-Driven Development — PASS

Created pursuant to FR-005. The template satisfies all spec requirements: tracks cooperation/defection patterns, identifies tit-for-tat dynamics, assesses boundary stability, and produces a final boundary map.

### II. Stable Interfaces — VIOLATION

**Finding: Dispute heading mismatch.**

The SKILL.md Dispute-Parsing Subsystem stable interface contract defines the prisoners-dilemma dispute heading as `## Disputed Boundaries` with `### [` sub-headings beneath it. The per-round synthesis template (`templates/prisoners-dilemma/synthesis.md`) uses `## Disputed Boundaries` (line 98), matching the contract exactly.

The cross-round synthesis template uses `### Remaining Disputed Boundaries` (line 101). This deviates from the stable interface in two ways:

1. **Heading level**: `###` instead of `##`. SKILL.md says heading-level prefix is irrelevant for matching (case-insensitive, any heading level), so this alone would not break parsing.
2. **Heading name**: "Remaining Disputed Boundaries" instead of "Disputed Boundaries". The SKILL.md heading matching rule says "The heading text must match as a substring of the line after stripping `#` prefix and whitespace." The substring "Disputed Boundaries" IS contained within "Remaining Disputed Boundaries", so the parser WOULD match it.

However, this is still a deviation from the exact heading name used in the per-round synthesis and the stable interface contract. The stable contract explicitly lists `## Disputed Boundaries` — the cross-round template adds the word "Remaining" as a prefix. While substring matching saves this from being a functional failure, the inconsistency is a deviation from the naming convention.

**Severity**: Low — functionally the parser would match via substring matching. But the heading rename is unnecessary and introduces inconsistency between per-round and cross-round naming.

**Recommendation**: Rename to `## Disputed Boundaries` to exactly match the stable interface contract and the per-round synthesis template. The word "Remaining" is implied by context (these are boundaries that survived the full multi-round process, as the section description already explains).

**Finding 2: Template variables — PASS.** All required variables present.

### III. Backward-Compatible Extension — PASS

Purely additive. New file in a previously empty slot.

### IV. Documentation Is the Product — PASS

The template contains game-theory-informed prompt engineering specific to iterated prisoner's dilemma dynamics. The Cooperation Dynamics section correctly instructs analysis of tit-for-tat emergence, reputation effects, and cooperation equilibrium — all key analytical constructs for this mode.

### V. Observable Deliberation — PASS

Process Summary requires per-round trust scores, boundary counts, and termination reason. The Cooperation Dynamics section adds another layer of observability by tracking agent behavior profiles per round.

### VI. Scripts Over Markdown — PASS

Parameterized prompt with structured sections and variable substitution.

### VII. Reproducibility Over Inconsistency — PASS

Deterministic template structure. Same config produces same prompts.

### VIII. Templating Engines Over Inference — PASS

The template constrains agent behavior effectively:
- Seven mandatory sections in prescribed order.
- Per-agent behavior profile table with required columns (Cooperation Signals, Defection Signals, Net Behavior).
- Required analysis of tit-for-tat emergence, reputation effects, cooperation equilibrium, and trust score trajectory.
- Boundary trajectory table matching the cooperative reference format.
- Final boundary map with three categories (Uncontested Territory, Shared Territory, Resolved Disputes) using explicit table formats.
- Stagnation diagnosis required for persisting disputes.
- Game theory rule: "Game theory is descriptive, not prescriptive" — prevents the synthesizer from rewarding/punishing strategic choices.
- Rules section constraining synthesizer behavior.

### IX. Zen of Python Output — PASS

Clean, predictable structure. The Final Boundary Map uses tables for assignments, which is cleaner than prose. Each section has one clear purpose.

---

## Cross-Template Observations

### Structural Consistency Across All Three Templates — PASS

All three templates follow the same structural pattern established by the cooperative reference:
1. Title and role statement
2. Context block with `{VARIABLE}` substitutions
3. What to Read instructions
4. What to Produce with mandatory sections
5. Rules section

This consistency supports Principle IX (predictable output) and Principle VII (reproducibility).

### Variable Parity — PASS

All three templates use the same nine variables as the cooperative reference: `{MODE}`, `{AGENT_NAMES}`, `{TARGET_PATH}`, `{ROUNDS_COMPLETED}`, `{MAX_ROUNDS}`, `{TERMINATION_REASON}`, `{TARGET_FILES}`, `{ROUND_SYNTHESES}`, `{OUTPUT_PATH}`. No template introduces unexpected variables or omits required ones.

### Absence of DISPUTES_BEGIN/END Markers — JUSTIFIED DEVIATION

None of the three new cross-round synthesis templates include `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` structural markers around their dispute sections. This matches the cooperative cross-round synthesis reference template, which also omits them. The per-round synthesis templates all include these markers.

This is a justified deviation because:
1. The cooperative reference template set the precedent.
2. The cross-round synthesis is consumed by Phase 6 trigger evaluation, which uses the Dispute-Parsing Subsystem. The subsystem's heading-based fallback parsing will correctly identify disputes in all three templates.
3. Adding the markers to the cross-round templates without adding them to the cooperative reference would create an inconsistency.

**Recommendation for future work**: Consider adding `DISPUTES_BEGIN`/`DISPUTES_END` markers to ALL cross-round synthesis templates (including cooperative) for parser reliability. This would be a separate enhancement, not a fix for this spec.

### Spec FR-009 vs SKILL.md Heading Discrepancy — OBSERVATION

The spec's FR-009 defines Phase 6 required headings that differ from what SKILL.md was actually updated with:

| Mode | Spec FR-009 | SKILL.md (authoritative) |
|------|-------------|--------------------------|
| red-blue | Risk Framework, Binding Risk Decisions, Residual Risk Summary | Decision Framework, Binding Decisions, Updated Risk Register |
| winner-take-all | Selection Criteria, Winner Declaration, Runner-Up Assessment | Decision Framework, Verdict Review, Binding Decision |
| prisoners-dilemma | Boundary Framework, Binding Boundary Decisions, Cooperation Assessment | Decision Framework, Binding Decisions, Revised Responsibility Map |

Per Principle IV, SKILL.md is the single source of truth. The spec's FR-009 was a design intent document; the SKILL.md implementation is authoritative. This observation does not affect the cross-round synthesis templates (which are Phase 5 artifacts, not Phase 6), but it documents the divergence for spec hygiene.

---

## Summary

| Template | I | II | III | IV | V | VI | VII | VIII | IX |
|----------|---|-----|------|-----|---|------|------|-------|-----|
| red-blue/cross-round-synthesis.md | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| winner-take-all/cross-round-synthesis.md | PASS | VIOLATION | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| prisoners-dilemma/cross-round-synthesis.md | PASS | VIOLATION | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

### Violations Requiring Action

1. **winner-take-all**: `### Remaining Contested Positions` should be renamed to `### Remaining Disputes` to match the per-round synthesis heading and the stable interface naming convention. (Principle II)

2. **prisoners-dilemma**: `### Remaining Disputed Boundaries` should be renamed to `## Disputed Boundaries` to exactly match the stable interface contract heading. (Principle II)

### Severity Assessment

Both violations are **low severity** — the Dispute-Parsing Subsystem would still function correctly due to substring matching (prisoners-dilemma) and the presence of `## Runner-Up` as the primary heading (winner-take-all). Neither violation would cause a runtime failure. However, they introduce gratuitous naming inconsistencies that could compound as the template set grows, and the constitution is clear that stable interface naming consistency is a contract obligation.

### Recommendations (Non-Blocking)

1. Consider adding `DISPUTES_BEGIN`/`DISPUTES_END` markers to all cross-round synthesis templates in a future spec for parser reliability parity with per-round synthesis templates.
2. Update `specs/004-universal-rounds/spec.md` FR-009 headings to match the authoritative SKILL.md headings, or add a note documenting the intentional divergence during implementation.
