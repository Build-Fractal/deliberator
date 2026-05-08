### Executive Summary

The v4.0.0 tier extraction proposal attempts to split 26 active constitutional principles across three hierarchical tiers, moving from a flat structure to Universal/Suite/Component classification. From an inclusion criteria perspective, the proposed reclassification creates a tension between grandfathered status and tier-specific verification requirements. Most principles pass the Constitutional Inclusion Criteria at their proposed tiers, but the amendment introduces a critical ambiguity about whether tier reclassification re-opens the gate for grandfathered principles. The mechanical verification requirements become tier-specific (Universal principles need verification across all Build Fractal products, Suite principles only across conversus-family repos), which generally aligns with the proposed classification but raises questions about the grandfathering contract. **The most important issue is clarifying whether grandfathered principles retain immunity from gate re-evaluation during tier reclassification, or whether the MAJOR amendment re-opens constitutional inclusion review.**

### Alignment

- **Gate criteria enumeration** (conversus-oss/CONSTITUTION.md L2198-2262): The amendment preserves the three-criterion gate (mechanical verification, falsifiable scope, distinctness) established in v2.4.0, maintaining consistent constitutional quality standards across all tiers.

- **Grandfathering preservation** (conversus-oss/CONSTITUTION.md L2420-2430): The amendment explicitly enumerates the 26 active grandfathered principles, maintaining the v2.4.0 grandfather clause while noting the 2 retired principles (VI, X).

- **Tier-appropriate verification scope** (build-fractal/conversus/GOVERNANCE.md L45-65): Universal principles require verification "across every Build Fractal product" while Suite principles only need "conversus-family" verification, matching the proposed tier boundaries.

- **Distinctness preservation across tiers** (multiple principles): The proposed classification maintains distinctness - no principle becomes a corollary of another through tier separation (e.g., XV Plugin Isolation vs XI Single Source of Truth remain distinct).

### Missed Opportunities

- **Explicit grandfathering-reclassification interaction** (missing): The amendment lacks a clear statement of whether tier reclassification re-triggers Constitutional Inclusion Criteria evaluation for grandfathered principles, creating constitutional interpretation ambiguity. Impact: high.

- **Tier-specific verification artifact enumeration** (build-fractal/CONSTITUTION.md, build-fractal/conversus/CONSTITUTION.md): The tier constitutions don't specify which verification mechanisms work at each tier scope, leaving implementation guidance incomplete. Impact: medium.

- **Cross-tier distinctness validation** (missing): No systematic verification that principles split across tiers don't create new compositional overlaps that violate Criterion 3. Impact: medium.

- **Mechanical verification scalability analysis** (missing): Universal-tier principles need verification mechanisms that scale beyond conversus to "every Build Fractal product," but no analysis confirms existing mechanisms meet this requirement. Impact: medium.

- **Gate re-evaluation trigger documentation** (missing): The amendment doesn't specify what future tier changes would re-trigger Constitutional Inclusion Criteria evaluation, creating precedent gaps. Impact: medium.

- **Component-tier weakening detection** (missing): No systematic check that component principles don't grant relief from higher-tier requirements, violating the "strengthen but not weaken" hierarchy rule. Impact: low.

### Off-Base Assumptions

- **Grandfathering carries through reclassification** (implied throughout): The amendment assumes grandfathered principles automatically pass at their new tiers without gate re-evaluation. The Constitutional Inclusion Criteria text is ambiguous on whether tier reclassification constitutes a new "amendment landing after v2.4.0" that triggers the gate.

- **Existing verification mechanisms are tier-portable** (implied): The amendment assumes current conversus-specific verification mechanisms work at Universal tier across all Build Fractal products, but many are conversus-domain-specific (e.g., deliberation phases, template variables).

### Actionable Recommendations

1. **Clarify grandfathering-reclassification interaction** (Priority: P1)
   - **Current state**: The amendment leaves ambiguous whether tier reclassification re-triggers Constitutional Inclusion Criteria evaluation for grandfathered principles.
   - **Proposed change**: Add explicit language to the Sync Impact Report stating either "grandfathered principles retain immunity from gate re-evaluation during tier reclassification" OR "tier reclassification subjects all principles to gate review at their new tier."
   - **Rationale**: Constitutional interpretation ambiguity creates enforcement uncertainty and precedent confusion for future tier changes.
   - **Risk if ignored**: Future amendments may inconsistently apply grandfathering, undermining constitutional stability.

2. **Document tier-specific verification constraints** (Priority: P1)  
   - **Current state**: Universal principles require verification "across every Build Fractal product" but existing mechanisms are conversus-specific.
   - **Proposed change**: Enumerate which Universal principles need verification mechanism updates before ratification, with implementation deadlines.
   - **Rationale**: Universal-tier mechanical verification must work beyond conversus domain [conversus-oss/CONSTITUTION.md L2198-2204].
   - **Risk if ignored**: Universal principles become unenforceable outside conversus, violating Criterion 1.

3. **Validate cross-tier distinctness preservation** (Priority: P2)
   - **Current state**: No systematic check that tier separation doesn't create new Criterion 3 violations through compositional overlaps.
   - **Proposed change**: Add to verification protocol a cross-tier distinctness audit checking all tier-crossing principle pairs.
   - **Rationale**: Distinctness must hold across tier boundaries, not just within tiers [conversus-oss/CONSTITUTION.md L2250-2257].
   - **Risk if ignored**: Tier separation may inadvertently create principle composition overlaps that violate distinctness.

4. **Specify component-tier weakening detection** (Priority: P2)
   - **Current state**: Component principles XVII-XXI, XXVI lack systematic validation that they don't weaken higher-tier requirements.
   - **Proposed change**: Add component-tier admission requirement that no principle grants relief from Tier 1 or Tier 2 without explicit relief deliberation.
   - **Rationale**: "Lower tiers may strengthen but not weaken upper-tier rules" hierarchy constraint [build-fractal/conversus/GOVERNANCE.md L15-20].
   - **Risk if ignored**: Component principles may silently undermine higher-tier requirements.

5. **Document gate re-evaluation triggers** (Priority: P2)
   - **Current state**: No specification of what tier changes trigger Constitutional Inclusion Criteria re-evaluation in the future.
   - **Proposed change**: Add to Governance section explicit triggers: tier promotion, tier demotion, tier creation, tier merger.
   - **Rationale**: Future tier changes need consistent gate application precedent [build-fractal/conversus/GOVERNANCE.md L45-85].
   - **Risk if ignored**: Future tier amendments may inconsistently apply constitutional quality gates.

6. **Validate Universal-tier verification feasibility** (Priority: P3)
   - **Current state**: Principles I, VII, IX claim Universal applicability but verification mechanisms may be conversus-specific.
   - **Proposed change**: Audit each Universal principle's verification mechanism for Build Fractal product generality.
   - **Rationale**: Universal principles need domain-agnostic enforcement [build-fractal/CONSTITUTION.md principles].
   - **Risk if ignored**: Universal principles become conversus-specific in practice, undermining tier hierarchy.

### Referenced Documentation

- `conversus-oss/CONSTITUTION.md` — sections/lines cited: L2198-2262 (Constitutional Inclusion Criteria), L2420-2430 (grandfathering enumeration), L2250-2257 (distinctness criterion)
- `build-fractal/conversus/GOVERNANCE.md` — sections/lines cited: L15-20 (tier hierarchy rules), L45-65 (verification protocol), L45-85 (pathway taxonomy)
- `build-fractal/CONSTITUTION.md` — sections/lines cited: Universal principles enumeration
- `build-fractal/conversus/CONSTITUTION.md` — sections/lines cited: Suite principles enumeration