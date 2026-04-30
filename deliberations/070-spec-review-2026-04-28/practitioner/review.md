### Executive Summary

Spec 070 proposes to audit three grandfathered constitutional principles (VI, X, XVI) against the new v2.4.0 gate criteria and potentially migrate them to operational guidance if they fail. From a practitioner perspective, this spec feels like constitutional tidying for its own sake rather than solving real operational problems. The constitution today has 27 principles that developers must navigate; dropping to 25 while adding scattered operational guidance across multiple documents (CONTRIBUTING.md, docs/output-conventions.md) may actually make the system harder to use, not easier. The spec acknowledges substantial risks (loss of enforcement weight, fragmentation, future authors not consulting moved guidance) but underestimates their operational impact. My most important recommendation: defer this entire effort until there's evidence that the grandfathered principles are actually causing problems in practice.

### Alignment

- **Risk identification** (L127-133, L168-177): The spec correctly identifies operational risks like "Future authors don't consult CONTRIBUTING.md" and "Loss of enforcement weight." This shows awareness that moving principles has real costs.
- **Easiest-first ordering** (L119-123): The migration plan sequences VI → X → XVI by complexity, which is operationally sound for testing the methodology before high-stakes changes.
- **Option A preference for XVI** (L109-113): Keeping Principle XVI in the constitution via refactoring rather than migration preserves its enforcement weight while fixing the gate compliance issue.
- **Concrete migration targets** (L66, L86, L113): The spec identifies specific documents for each migration rather than vague "operational guidance somewhere," making implementation tractable.

### Missed Opportunities

- **User impact analysis**: The spec audits principles against gate criteria but never asks "do developers actually struggle with these principles in practice?" Low impact if the principles work fine operationally.
- **Enforcement measurement**: No baseline for how often these principles are cited in PR reviews or enforcement actions. Migration may eliminate invisible but valuable enforcement. High impact.
- **Documentation discoverability study**: The assumption that developers will find guidance in CONTRIBUTING.md or docs/ is untested. Most developers read README and constitution, not scattered docs. High impact.
- **Constitutional bloat analysis**: Claims the constitution needs trimming but provides no evidence that 27 principles is too many or that developers struggle to navigate them. Medium impact.
- **Implementation cost accounting**: The spec requires this deliberation plus 1-3 implementation PRs each with dual verification. That's 4-8 total deliberations for constitutional cleanup with no demonstrated user benefit. High impact.
- **Rollback planning**: No consideration of how to restore a principle if migration fails operationally. Once enforcement weight is lost, it's hard to recover. Medium impact.
- **Alternative solutions**: Could add "gate compliance" metadata to existing principles rather than migrating them, preserving enforcement while marking gate status. Low impact.

### Off-Base Assumptions

- **CONTRIBUTING.md consultation rate**: The spec assumes (L129, L173) that developers regularly consult CONTRIBUTING.md and that cross-references from the constitution will maintain discoverability. Most developers ignore CONTRIBUTING.md unless explicitly directed to it during PR review.
- **Operational guidance enforcement**: The spec assumes (L173) that "operational guidance is reinforced by automation, not just by document presence," but provides no plan for automated enforcement of the migrated principles.
- **Constitutional two-tier concern**: The spec argues (L24) that grandfathering creates problematic "two-tier structure," but doesn't establish why this matters operationally if the principles work fine.

### Actionable Recommendations

1. **Add user research requirement** (Priority: P1)
   - **Current state**: The spec audits principles against gate criteria without evidence they cause operational problems (L18-26).
   - **Proposed change**: Require evidence that VI, X, XVI actually cause confusion, conflict, or enforcement problems before migration.
   - **Rationale**: Constitutional changes should solve real problems, not theoretical purity issues.
   - **Risk if ignored**: Substantial process overhead for cleanup that helps no one.

2. **Establish enforcement baseline** (Priority: P1)
   - **Current state**: No measurement of current principle citation or enforcement (missing from §7 risk analysis).
   - **Proposed change**: Audit last 6 months of PR reviews for principle VI/X/XVI citations before migration.
   - **Rationale**: Can't assess migration impact without knowing current usage.
   - **Risk if ignored**: May eliminate valuable enforcement unknowingly.

3. **Add operational success criteria** (Priority: P2)
   - **Current state**: Success criteria focus on process completion (L136-142) not operational outcomes.
   - **Proposed change**: Add "migrated guidance is discoverable and cited at same rate as original principle within 6 months."
   - **Rationale**: Migration success should be measured by continued effectiveness, not just completed paperwork.
   - **Risk if ignored**: Migration may succeed procedurally but fail operationally.

4. **Include rollback mechanism** (Priority: P2)
   - **Current state**: No consideration of reversing migration if it fails operationally.
   - **Proposed change**: Define criteria and process for restoring principle to constitution if migration loses enforcement effectiveness.
   - **Rationale**: Constitutional changes should be reversible if they don't work.
   - **Risk if ignored**: Stuck with ineffective fragmented guidance.

5. **Defer pending evidence** (Priority: P1)
   - **Current state**: Proceeds with migration based on gate-compliance audit alone.
   - **Proposed change**: Require demonstrated operational problems with grandfathered principles before migration.
   - **Rationale**: Gate compliance is means, not end. Operational effectiveness matters more than theoretical consistency.
   - **Risk if ignored**: Substantial overhead for theoretical benefit.

6. **Consolidate migration targets** (Priority: P2)
   - **Current state**: Scatters guidance across CONTRIBUTING.md, docs/output-conventions.md, docs/optimization-design-intent.md (L66, L86, L113).
   - **Proposed change**: Consolidate all migrated guidance into single "Constitutional Guidance" section of CONTRIBUTING.md.
   - **Rationale**: Single location preserves discoverability better than fragmentation.
   - **Risk if ignored**: Guidance becomes scattered and hard to find.

7. **Add automated enforcement plan** (Priority: P3)
   - **Current state**: Mentions CI hooks for some principles (L129, L173) but no concrete implementation.
   - **Proposed change**: Define specific linting rules for mechanically-checkable parts before migration.
   - **Rationale**: Automation can preserve enforcement when constitutional weight is lost.
   - **Risk if ignored**: Migrated guidance becomes suggestion, not requirement.

8. **Quantify activation energy** (Priority: P2)
   - **Current state**: Acknowledges "activation energy" (L8 Q5) but doesn't weigh it against benefits.
   - **Proposed change**: Estimate total deliberation and PR review hours for this effort vs. demonstrated operational benefit.
   - **Rationale**: Process overhead should be proportional to problem solved.
   - **Risk if ignored**: Expensive process for minimal gain.

9. **Define positive case explicitly** (Priority: P3)
   - **Current state**: Implies principles stay if they pass audit but doesn't state this clearly.
   - **Proposed change**: Add explicit section "If all principles pass audit, no constitutional changes result and this spec closes."
   - **Rationale**: Clarifies that audit doesn't force migration.
   - **Risk if ignored**: Confusion about audit vs. migration requirement.

### Referenced Documentation

No documentation files were provided for the practitioner perspective. Review is based solely on the target specification and audit context files.