# Attack Brief: anti-framework-skeptic vs pro-adapter-pattern

## False Claims

### "Unanimous Convergence" Misrepresentation

**Claim**: "The synthesis documented unanimous convergence on 'eliminate duplication via shared metadata' and 'CLI canonical authority,' proving the team already agrees the problem exists and needs solving."

**Factual Correction**: The synthesis actually documented significant disagreement on implementation approaches. The pragmatist-maintainer explicitly warned about "build system complexity" and recommended "CLI-first authority with shared metadata" rather than registry-driven generation. The developer-power-user supported "bounded auto-generation" but preferred CLI centricity over registry approaches. Agreement on principles ≠ agreement on mechanisms.

**Impact**: This undermines their core "existing consensus" argument. They're claiming a mandate that doesn't exist.

### Mathematical Projection Inflation

**Claim**: "At 12 capabilities × 4 surfaces = 48 maintained projections, conversus is already beyond the point where hand-written maintenance is sustainable."

**Factual Correction**: This is misleading multiplication. It's not 48 independent implementations - surfaces provide structural reuse. CLI commands follow Click patterns, MCP tools follow server patterns, plugin skills follow markdown templates. The actual maintenance burden is closer to 12 capability implementations + 4 surface patterns, not 48 discrete entities.

**Impact**: Their economic justification is built on inflated cost estimates.

### Missing Economic Math

**Claim**: "The math shows 3-4 days registry investment pays back in under 3 months."

**Factual Correction**: No math is provided. They assert payback without showing the calculation. Framework maintenance costs, debugging time, and format evolution updates are completely unaccounted for. 

**Impact**: Core economic argument lacks supporting evidence.

## Overstated Strengths

### "Best of Both Worlds" Framework Fantasy

**Claim**: "The adapter pattern directly solves the 'consistency vs. per-surface UX' tension that paralyzed the previous deliberation—80% default consistency with 20% opt-in customization."

**Technically True**: Adapter patterns can provide default behavior with override capability.

**Misleading Context**: This assumes the framework complexity is worth it for 12 capabilities. The "80%/20%" numbers are invented - they provide no evidence that most capabilities actually benefit from defaults rather than purpose-built implementations. Classic engineering trap: trying to optimize everything often optimizes nothing well.

**Full Picture**: Hand-written surfaces already provide 100% optimal UX per surface with zero framework overhead. Trading proven simplicity for theoretical flexibility at tiny scale.

### "Byte-Identical Validation" as Risk Mitigation

**Claim**: "Concrete week-by-week implementation plan starting with the `decide` capability and byte-identical validation requirements."

**Technically True**: Byte-identical validation can catch migration errors.

**Misleading Context**: Byte-identical validation is actually evidence of migration fragility, not safety. You need such strict validation precisely because generated output is unpredictable and risky. Hand-written code doesn't need byte-identical validation because humans understand what they're changing.

**Full Picture**: The need for byte-identical validation proves the migration introduces significant complexity and failure risk.

## Understated Risks

### Framework Maintenance Death Spiral

**Risk**: Framework code becomes a maintenance liability that compounds over time.

**Their Treatment**: Listed under "Honest Weaknesses" as "framework maintenance burden" but immediately dismissed as "acceptable given the current context."

**Real Severity**: Framework maintenance scales superlinearly with target format evolution. Every MCPB version update, every Claude Code skill format change, every CLI option syntax evolution requires updating the projector. With hand-written surfaces, format changes affect only the one surface that changed. They've created a single point of failure that touches all surfaces.

### Format Evolution Fragility

**Risk**: Target surface formats evolve unpredictably, breaking the projector.

**Their Treatment**: Completely omitted from their analysis.

**Real Severity**: MCPB is pre-1.0, Claude Code skills are evolving, MCP tools are adding new features. Each format change requires framework updates. Hand-written surfaces adapt to format changes locally - registry approaches require global framework updates that can break all surfaces simultaneously.

### Resource Allocation Opportunity Cost

**Risk**: 3-4 days of framework work means 3-4 days not shipping user-visible features.

**Their Treatment**: Dismissed with "the math shows payback in under 3 months" (no math provided).

**Real Severity**: At pre-1.0, pre-public, zero-paid-users scale, the highest priority is feature velocity, not infrastructure optimization. 3-4 days represents 15-20% of monthly development capacity for a 1-2 person team. That time could ship entire new capabilities users actually want.

## Head-to-Head

| Criterion | pro-adapter-pattern | anti-framework-skeptic | Verdict |
|---|---|---|
| **Implementation Speed** | 3-4 days upfront investment, then "one registry entry" per capability | Zero upfront cost, 30 minutes per capability across 4 surfaces | **anti-framework-skeptic wins**. 12 capabilities × 30 min = 6 hours total vs 3-4 days upfront + ongoing maintenance |
| **Format Evolution Resilience** | Framework must be updated when any target format changes | Each surface adapts independently to its format changes | **anti-framework-skeptic wins**. Local changes vs global framework updates |
| **Maintenance Burden** | Registry + adapters + projector + build scripts (~1000+ LOC of infrastructure) | Hand-written surfaces with shared metadata imports | **anti-framework-skeptic wins**. Infrastructure code scales maintenance burden |
| **Feature Velocity** | Framework work delays feature shipping by 3-4 days | Immediate feature development with discipline checklist | **anti-framework-skeptic wins**. No opportunity cost for infrastructure |
| **Risk at Current Scale** | Framework complexity for 12 capabilities | Manual maintenance for 12 capabilities | **anti-framework-skeptic wins**. Known simple cost vs unknown complex costs |

**Verdict Summary**: The competitor wins on theoretical future consistency but loses on every practical criterion that matters at conversus's current scale. They're solving tomorrow's problems while ignoring today's constraints.