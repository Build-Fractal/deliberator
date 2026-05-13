## Executive Summary

Spec v4.2.0 proposes migrating conversus deliberation outputs from markdown to structured JSON Schema with a constitutional deadline of 2026-12-01. The spec addresses documented production bugs (Bug A prompt overflow, Bug B cross-review persistence failures, Bug C missed dispute triggers) through a tiered rollout approach with PR-blocking CI enforcement.

From a risk perspective, this migration introduces several critical operational dependencies that compound under worst-case scenarios. The hard deadline creates a cascading failure risk where missing any intermediate milestone (template migration, adapter updates, fixture development) blocks the entire suite's compliance. The temporal-constraint exemption establishes a procedural precedent that, despite containment language, may encourage future creative interpretation.

Most critically, the spec assumes a clean implementation path while the transition period actually amplifies existing engine bugs, creating a worse-before-better trajectory that could destabilize production deliberations during the most time-constrained period. **My most important recommendation: the spec underestimates implementation-period risk accumulation and needs explicit degradation planning for missed milestones.**

## Alignment

- **Constitutional grounding** (spec § 5.4 E1, § 1.2): The spec properly cites both Tier 1 Principle II (Stable Interfaces) and Tier 2 Principle XXVIII (Persistence Contract Discipline) as constitutional authority for the PR-blocking CI gate, establishing clear doctrinal foundation for enforcement mechanisms.

- **Tiered rollout strategy** (spec § 11): The four-tier approach (T1 parallel-format → T2 advisory CI → T3 blocking CI → T4 markdown deprecation) provides structured risk mitigation with checkpoints at each stage rather than a single hard cut.

- **Bidirectional validation** (spec § 5.4 D12): The drift detection mechanism addresses schema evolution risk by validating existing artifacts against new schemas, preventing silent breakage from schema edits.

- **Fixture-based enforcement** (spec § 5.3): The four fixture types (conformant, missing-required, wrong-type, enum-violation) provide concrete test coverage for the mechanical enforcement surface required by XXVIII sub-clause 2.

## Missed Opportunities

- **Graceful degradation specification**: The spec assumes all milestones will be met by 2026-12-01 but provides no explicit degradation plan for missed intermediates. If template migration or adapter updates lag, what happens to consumer products? Impact: **high** — cascading compliance failures across the suite.

- **Implementation velocity calibration**: The spec mandates 24+ fixtures (4 types × 6 modes) plus dependency-ordered template migration across all modes by cliff date, but provides no engineering capacity analysis against historical velocity. Impact: **high** — resource planning blind spot.

- **Engine transition bug amplification**: During markdown→JSON transition, existing engine bugs (Bug C disputes_remain trigger miss) remain unfixed while new validation surface is added, creating compound failure modes. The spec acknowledges this in § 13 but provides no mitigation. Impact: **medium** — operational reliability during critical transition window.

- **Schema iteration lock-in analysis**: Starting at `1.0.0-rc.1` with SemVer enforcement means field renames become MAJOR bumps immediately, potentially blocking necessary ergonomic adjustments discovered during pilot deployment. Impact: **medium** — premature schema lock-in.

- **Consumer coordination failure modes**: The orchestrator adapter migration is critical path for suite compliance, but the spec doesn't address what happens if the adapter team has conflicting priorities or capacity constraints. Impact: **medium** — cross-team dependency risk.

- **Performance budget validation**: The <100ms validator budget assumes single-digit millisecond performance on ~20-50KB JSON, but some synthesis outputs exceed 100K chars. No analysis of performance scaling or fallback behavior when budget exceeded. Impact: **low** — operational assumptions may not hold at scale.

## Off-Base Assumptions

- **Assumption: Clean implementation timeline** (spec § 11): The spec assumes template migration proceeds smoothly in dependency order without addressing the documented engine bugs that will persist and potentially worsen during the transition period. The real operational environment during implementation includes ongoing Bug C manifestations that could destabilize the very deliberations needed to validate the migration.

- **Assumption: Uniform engineering capacity** (spec § 11 steps 1-7): The spec treats all implementation steps as equally feasible without acknowledging that some steps (like orchestrator adapter migration in § 6.2) depend on external teams with different priorities and capacity constraints.

- **Assumption: RC window flexibility** (spec § 4.8 C10): The spec frames the `1.0.0-rc.1` → `1.0.0` transition as allowing "ergonomic refinement" but SemVer rules lock field structure immediately, potentially preventing necessary adjustments discovered during pilot testing.

## Actionable Recommendations

1. **Add explicit degradation planning** (Priority: P1)
   - **Current state**: Spec assumes all milestones met by 2026-12-01 cliff date.
   - **Proposed change**: Add § 11.2 "Missed Milestone Protocols" specifying what happens if template migration lags, adapter updates fail, or fixture development falls behind. Include per-milestone fallback procedures and communication protocols.
   - **Rationale**: The universal deadline creates cascading failure risk where any single missed milestone can block entire suite compliance.
   - **Risk if ignored**: Suite-wide compliance crisis if any critical path component slips, with no documented authority or procedure for deadline extensions.

2. **Require engineering capacity validation** (Priority: P1)
   - **Current state**: Spec mandates 24+ fixtures plus full template migration without capacity analysis.
   - **Proposed change**: Add requirement in § 11 step 2 for engineering team to confirm capacity against historical velocity before proceeding to implementation.
   - **Rationale**: The cliff date is constitutionally binding; scope must be validated as achievable within available engineering resources.
   - **Risk if ignored**: Remediation-Blocked status for conversus-oss if implementation scope exceeds available capacity by deadline.

3. **Document engine transition risk** (Priority: P2)
   - **Current state**: § 13 acknowledges Bug C persistence during transition but provides no mitigation.
   - **Proposed change**: Add explicit transition-period operational guidance in § 5.1, including manual arbitration triggers when automated dispute detection fails.
   - **Rationale**: The transition period amplifies existing engine bugs rather than immediately fixing them, creating worse-before-better operational reliability.
   - **Risk if ignored**: Increased deliberation failures during the implementation window when system reliability is most critical.

4. **Tighten temporal-constraint containment** (Priority: P2)
   - **Current state**: E2 technical condition + D5 categorical prohibitions attempt to contain bootstrap-paradox precedent.
   - **Proposed change**: Add requirement that future invocations must cite both boundary precedents (v4.1.0 + v4.2.0) AND demonstrate the exact same logical impossibility structure.
   - **Rationale**: Even with containment language, creative future amendments may find ways to invoke "schema-substrate-standup-adjacent" reasoning.
   - **Risk if ignored**: Precedent erosion leading to routine temporal-constraint exemptions that undermine XXVIII enforcement.

5. **Specify adapter coordination mechanism** (Priority: P2)
   - **Current state**: § 6.2 assumes orchestrator adapter migration proceeds smoothly.
   - **Proposed change**: Add cross-team coordination protocol in § 6.2 with specific escalation path if adapter team capacity is insufficient.
   - **Rationale**: Orchestrator adapter migration is critical path for suite compliance but depends on external team with different priorities.
   - **Risk if ignored**: Suite-wide compliance failure if adapter migration blocks due to resource conflicts in orchestrator team.

6. **Add performance scaling analysis** (Priority: P3)
   - **Current state**: <100ms budget assumes performance holds at larger output sizes.
   - **Proposed change**: Add requirement in § 5.1 for validator performance testing against maximum observed synthesis output sizes (>100K chars).
   - **Rationale**: Performance assumptions may not hold at the upper end of actual deliberation output sizes.
   - **Risk if ignored**: Validator timeouts or degraded performance on large synthesis outputs.

7. **Clarify RC window schema flexibility** (Priority: P3)
   - **Current state**: C10 suggests ergonomic refinement is possible during RC window.
   - **Proposed change**: Clarify in § 4.8 which types of changes are feasible during RC period given SemVer constraints.
   - **Rationale**: Field-level changes require MAJOR bumps even in RC, potentially blocking necessary adjustments from pilot feedback.
   - **Risk if ignored**: Schema lock-in preventing ergonomic improvements discovered during pilot deployment.

## Referenced Documentation

- `specs/v4.2.0-structured-deliberation-outputs/spec.md` — sections/lines cited: L47-48 (D6 post-cliff handling), L867-876 (tiered rollout), L594-602 (universal deadline), L916-918 (Bug C acknowledgment)
- `build-fractal/CONSTITUTION.md` — sections/lines cited: L84-112 (Principle II Stable Interfaces)
- `build-fractal/conversus/CONSTITUTION.md` — sections/lines cited: L70-80 (Principle V Observable Deliberation), L490-614 (Principle XXVIII Persistence Contract Discipline universal deadline)
- `deliberations/v4.2.0-structured-deliberation-outputs-blind-2026-05-13/QUESTION.md` — sections/lines cited: L40-55 (Q2 risk examination criteria)

Q2 RULING: MODERATE-RISK-MANAGEABLE — critical operational dependencies and transition amplification risks identified but containable with proper degradation planning and capacity validation