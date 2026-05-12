I need to read all the target files to conduct my tier coherence audit. Let me start with the QUESTION.md to understand my specific role.

Now let me read the actual spec v3 to understand what I'm auditing:

Now let me read the Tier 1 Constitution to understand the universal requirements:

Now let me read the Tier 2 Constitution to understand the suite-level requirements:

Now I'll read the Constitutional Conversations file to understand the governance history:

Based on my analysis of the tier hierarchy and v3's placement, I'll provide my tier coherence audit focused on Q2:

---

### Executive Summary

Spec v3's Tier 2 placement of Persistence Contract Discipline as principle XXVIII represents a defensible suite-level constitutional amendment that correctly matches the evidence scope to the tier authority. The amendment applies uniformly to all conversus-family products (conversus-oss, conversus-enhanced, spec-kit-orc, and future siblings) without creating tier-specific exceptions or weakening upper-tier principles. However, the universal 2026-12-01 deadline creates a potential retroactive compliance burden for future siblings joining post-deadline, and the principle's relationship to Tier 1 Principle II requires clarification to ensure strengthening rather than duplication. The tier placement is constitutionally sound but needs minor clarifications on forward sibling obligations.

### Alignment

Where v3's Tier 2 placement correctly leverages tier hierarchy:

- **Suite-wide applicability** (spec v3 L46-50): Amendment explicitly states "every conversus-family product MUST" and "every conversus-family repo is subject" which matches Tier 2's "apply to **every conversus-family repo**" authority from Tier 2 CONSTITUTION.md L42-44.

- **Evidence base containment** (spec v3 L8, L15): Evidence drawn from "conversus-oss output parse contract, conversus-enhanced consumer surfaces, spec-kit-orc adapter" — all conversus suite products — correctly constrains placement to Tier 2 rather than overreaching to Tier 1's multi-product-family requirement.

- **Cross-tier strengthening** (spec v3 § 4): New Principle XXVIII strengthens Tier 1 Principle II's stable interface discipline by adding specific mechanical enforcement requirements for persistent state, without weakening existing stable interface coverage.

- **Forward sibling automatic application** (spec v3 § 7 L237): Table correctly shows future conversus-family siblings inherit the principle automatically with "Admission requires CONSUMER-CONTRACT.md + CI gate at admission time."

### Missed Opportunities

Where v3 fails to address tier coherence concerns that could strengthen its placement:

- **Retroactive deadline burden analysis**: v3's universal 2026-12-01 deadline applies to "all suite products" but doesn't address what happens when a new conversus sibling joins post-2026-12-01. Does the sibling get a retroactive deadline (already passed) or does admission-time obligation override the universal date? Impact: high.

- **Tier 1 Principle II relationship clarification**: While v3 § 4 appears to strengthen rather than duplicate Tier 1 II, the relationship isn't explicitly documented. Both principles govern "stable interfaces" but at different abstraction levels (II: structural markers/dispatch tables; XXVIII: persistent artifacts). Impact: medium.

- **Suite membership boundary definition**: spec v3 notes "spec-kit-orc is part of the conversus suite by virtue of its adapter consuming conversus deliberation outputs" but doesn't define the membership test generally. Future siblings need clear criteria for when Tier 2 principles apply. Impact: medium.

- **Cross-tier weakening prohibition compliance documentation**: v3 doesn't explicitly cite the three-criteria test from Tier 2 CONSTITUTION.md L475-488 to demonstrate it doesn't violate implicit relief, implementation-impact shift, or suite-specific bypass. Impact: low.

- **Universal applicability vs. admission-time exceptions**: v3 states principle applies "to all conversus-family products" but § 7 table suggests admission-gate enforcement. These could be reconciled by clarifying that universality applies post-admission. Impact: medium.

- **Tier 2 authority scope validation**: v3 doesn't reference Tier 2's presumed substrate ("multi-agent deliberation," "plugin entry-points," "free/paid partition") to show persistence contracts fit the suite's technical architecture assumptions. Impact: low.

### Off-Base Assumptions

Where v3 makes incorrect assumptions about tier hierarchy:

- **Assumption stated**: spec v3 L32 assumes "It does NOT amend Tier 1" is sufficient to avoid cross-tier impact analysis. Why it is wrong: Per Tier 1 CONSTITUTION.md L63-65, "Lower tiers may strengthen rules from higher tiers but may not weaken them." The relationship requires positive analysis, not just non-amendment. Correct understanding: Tier 2 principles that touch similar domains to Tier 1 principles must demonstrate strengthening, not just non-interference.

### Actionable Recommendations

My concrete proposals for spec v3 changes:

1. **Clarify retroactive deadline handling** (Priority: P1)
   - **Current state**: spec v3 L61 "single universal 2026-12-01 deadline" without future sibling provisions.
   - **Proposed change**: Add § 2 goal 7: "Future conversus-family products joining post-2026-12-01 receive admission-time deadlines per suite COMPLIANCE.md rather than retroactive 2026-12-01 obligation."
   - **Rationale**: Universal deadline cannot logically apply to products that didn't exist when set. Admission-gate enforcement (§ 7 table) resolves the apparent contradiction.
   - **Risk if ignored**: Constitutional inconsistency when first post-deadline sibling joins; unclear compliance obligation.

2. **Document Tier 1 Principle II relationship** (Priority: P1)
   - **Current state**: spec v3 § 4 L80 "Persistent on-disk state is itself a stable interface" without explicit cross-tier analysis.
   - **Proposed change**: Add § 5 clarification: "This amendment strengthens Tier 1 Principle II's stable interface discipline by adding mechanical enforcement for the persistent subset. Tier 1 II governs structural markers and runtime surfaces; Tier 2 XXVIII governs persistent artifacts."
   - **Rationale**: Tier 2 CONSTITUTION.md L475-488 cross-tier weakening prohibition requires positive demonstration of strengthening relationship.
   - **Risk if ignored**: Self-consistency or blind verification agents may flag apparent duplication; constitutional debt from unclear tier boundaries.

3. **Define suite membership test** (Priority: P2)
   - **Current state**: spec v3 L217 ad-hoc explanation for spec-kit-orc membership.
   - **Proposed change**: Add § 3 non-goal: "Suite membership determination follows conversus/COMPLIANCE.md admission criteria. Products that consume conversus deliberation outputs or register conversus-family plugins qualify for admission review."
   - **Rationale**: Clear membership test prevents future disputes over which products inherit Tier 2 obligations.
   - **Risk if ignored**: Scope creep arguments when non-conversus products adopt conversus outputs; unclear tier authority boundaries.

4. **Add cross-tier compliance attestation** (Priority: P2)
   - **Current state**: spec v3 doesn't cite Tier 2 CONSTITUTION.md L475-488 weakening prohibition.
   - **Proposed change**: Add § 8 paragraph: "Cross-tier weakening analysis: this amendment satisfies criteria (i-iii) per Tier 2 CONSTITUTION.md L475-488. No implicit relief, implementation-impact shift, or bypass language present. Amendment strengthens Tier 1 stable interface discipline."
   - **Rationale**: Demonstrates compliance with ratified cross-tier constraints; provides verification agents clear assessment trail.
   - **Risk if ignored**: Verification agents must perform weakening analysis from scratch; constitutional compliance not pre-validated.

5. **Reconcile universality with admission-gate language** (Priority: P2)
   - **Current state**: spec v3 L46 "every conversus-family product" vs § 7 "Admission requires."
   - **Proposed change**: Clarify in § 2: "The principle applies to all admitted conversus-family products; admission gate ensures compliance before suite membership."
   - **Rationale**: Resolves apparent tension between universal scope and conditional enforcement; aligns with Tier 2's "every conversus-family repo" authority.
   - **Risk if ignored**: Ambiguity about whether principle applies to non-compliant conversus products or only compliant ones.

6. **Reference Tier 2 technical substrate** (Priority: P3)
   - **Current state**: spec v3 doesn't validate alignment with Tier 2's presumed architecture.
   - **Proposed change**: Add § 1 note: "Persistence contracts fit conversus suite architecture: multi-agent deliberation produces persistent outputs; plugin entry-points consume those outputs; free/paid partition requires cross-product stability guarantees."
   - **Rationale**: Demonstrates amendment fits Tier 2's technical assumptions per Tier 2 CONSTITUTION.md L42-44.
   - **Risk if ignored**: Minor; tier placement already well-justified by evidence scope.

7. **Strengthen Constitutional Inclusion Criteria analysis** (Priority: P3)
   - **Current state**: spec v3 § 8 L249-252 brief gate analysis.
   - **Proposed change**: Expand mechanical verifiability analysis: "CI gate requirements make principle compliance deterministically checkable; bidirectional drift detection prevents silent schema degradation; three test fixtures provide objective pass/fail criteria."
   - **Rationale**: More thorough demonstration of Criterion 2 satisfaction strengthens constitutional foundation.
   - **Risk if ignored**: Verification agents may re-examine gate compliance; weaker constitutional justification than necessary.

### Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/build-fractal/conversus/conversus-oss/specs/v4.1.0-persistence-contract-discipline/spec.md` — sections/lines cited: L8, L15, L32, L46-50, L61, L217, L237, L249-252, L80, § 4, § 7 table
- `/Users/business-daddy/code/payer-index-mono/build-fractal/conversus/CONSTITUTION.md` — sections/lines cited: L42-44, L475-488
- `/Users/business-daddy/code/payer-index-mono/build-fractal/CONSTITUTION.md` — sections/lines cited: L63-65, L84-114
- `/Users/business-daddy/code/payer-index-mono/build-fractal/conversus/conversus-oss/deliberations/v4.1.0-persistence-contract-discipline-self-consistency-rerun-2026-05-12/QUESTION.md` — sections/lines cited: L37-48