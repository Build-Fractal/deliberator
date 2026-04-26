I'll begin by reading the target files to understand what I'm reviewing.

### Executive Summary

The Constitution establishes a comprehensive governance framework for conversus with 21 principles covering spec-driven development, stable interfaces, and decomposition mechanisms. However, analysis of the 10 recent merged PRs reveals significant governance gaps where unwritten invariants are guiding development decisions without constitutional backing. The recent work embodies seven cross-cutting themes that represent established patterns but lack principled foundation. Most critically, distribution surface integrity (#11, #13), provider robustness patterns (#5, #6, #8, #9), and capability registry contracts (#4, #14) are functioning as de facto governance rules without constitutional status. My most important recommendation: establish Principle XXII covering Distribution Surface Integrity to prevent the packaging drift and broken installs that have already occurred.

### Alignment

- **Spec-driven development enforcement** (L34-45): The constitution mandates that behavioral changes start with specifications, and recent PR #10's three-layer red-blue fix followed this pattern with proper schema → parser → contract test progression. This aligns with constitutional requirements for structured change management.

- **Stable interface protection** (L47-71): The constitution defines breaking change protocols, and the recent work has respected this with PRs #4 and #14 extending capability surfaces without breaking existing contracts. The registry-based extension pattern preserves backward compatibility as required.

- **Backward-compatible extension discipline** (L72-84): Recent PRs consistently added optional capabilities (CONVERSUS_DISABLED_TOOLS env var, OAuth retry logic, token tracking) without changing existing behavior, demonstrating adherence to Principle III's non-destructive extension mandate.

- **Single source of truth enforcement** (L240-265): PR #13's manifest.json sync from pyproject.toml directly implements Principle XI by eliminating version duplication and establishing build-time projection as the canonical pattern.

### Missed Opportunities

- **Distribution surface governance** (missing): The constitution lacks principles for packaging integrity, yet PRs #11 and #13 dealt with broken wheels and version drift. A distribution surface integrity principle would have prevented these issues. Impact: high.

- **Provider contract standardization** (missing): Four PRs (#5, #6, #8, #9) hardened provider edge cases without constitutional guidance on robustness expectations. A provider contract principle would ensure consistent implementation patterns. Impact: high.

- **Capability registry as governance mechanism** (missing): PRs #4 and #14 used the registry for third-party extension and operator configuration without constitutional recognition of this pattern. Registry-first governance principle missing. Impact: medium.

- **Testing expectations for parametrized surfaces** (missing): PR #12's drift guard meta-tests represent an important pattern for ensuring coverage completeness, but no constitutional principle mandates this approach for new parametrized capabilities. Impact: medium.

- **Safety-critical default patterns** (missing): PR #10's red-blue false-PASS bug would have been caught by constitutional safety requirements. No principle establishes defense-in-depth as mandatory for safety-critical synthesis. Impact: high.

- **Live integration test governance** (missing): PR #8 introduced `@pytest.mark.live` tests without constitutional guidance on when live testing is appropriate or how to manage API cost implications. Impact: low.

### Off-Base Assumptions

- **Distribution concerns as implementation details** (L495): The constitution treats packaging as implementation detail in Principle XX, but PRs #11 and #13 show distribution failures have user-facing impact equivalent to breaking changes. Constitutional framing underweights packaging governance.

- **Provider resilience as emergent behavior** (implied throughout): The constitution assumes provider-agnostic execution without explicitly requiring provider robustness contracts. Recent PRs show this assumption fails when providers have different retry semantics, response formats, and rate limiting.

### Actionable Recommendations

1. **Establish Distribution Surface Integrity principle** (Priority: P1)
   - **Current state**: Constitution treats packaging as implementation detail (L495).
   - **Proposed change**: Add Principle XXII requiring single-source versioning, force-include discipline for non-package modules, end-to-end install testing for every distribution path.
   - **Rationale**: PRs #11 and #13 show packaging failures create broken user installs equivalent to breaking changes.
   - **Risk if ignored**: More broken `pip install` experiences and version drift across distribution surfaces.

2. **Codify Provider Robustness Contract** (Priority: P1)
   - **Current state**: No constitutional guidance on provider implementation standards.
   - **Proposed change**: Add Principle XXIII mandating token reporting, 429 retry with jitter, format-shift tolerance, structurally-valid response handling for all providers.
   - **Rationale**: PRs #5, #6, #8, #9 establish this as de facto standard but lack principled foundation.
   - **Risk if ignored**: Inconsistent provider behavior and unhandled edge cases in future provider implementations.

3. **Registry-First Declaration principle** (Priority: P2)
   - **Current state**: Capability registry mentioned in passing (L19-21) but not as governance mechanism.
   - **Proposed change**: Add registry as canonical declaration mechanism for third-party extension and operator configuration.
   - **Rationale**: PRs #4 and #14 demonstrate registry as stable contract for capability management.
   - **Risk if ignored**: Ad hoc capability extension patterns that bypass the registry contract.

4. **Safety-Critical Default Defense-in-Depth** (Priority: P1)
   - **Current state**: No constitutional mandate for layered safety validation.
   - **Proposed change**: Add principle requiring schema → parser → contract test pattern for synthesis verdicts and safety-critical outputs.
   - **Rationale**: PR #10's false-PASS bug demonstrates the failure mode this would prevent.
   - **Risk if ignored**: More false-positive safety decisions with unauditable synthesis logic.

5. **Drift Guard Testing Mandate** (Priority: P2)
   - **Current state**: Testing principles focus on general coverage, not parametric completeness.
   - **Proposed change**: Add requirement for meta-tests asserting coverage of all parametrized surfaces (prompts, tools, modes).
   - **Rationale**: PR #12's approach prevents coverage gaps when new prompt definitions are added.
   - **Risk if ignored**: Silent coverage degradation as parametrized surfaces expand.

6. **Live Integration Test Governance** (Priority: P3)
   - **Current state**: No guidance on when live tests are appropriate or how to manage costs.
   - **Proposed change**: Add principle defining live test criteria and cost management patterns.
   - **Rationale**: PR #8's `@pytest.mark.live` needs constitutional guidance for consistent application.
   - **Risk if ignored**: Inconsistent live testing practices and unexpected API costs.

7. **Breaking Change Registry Expansion** (Priority: P2)
   - **Current state**: Stable interfaces include template variables and dispatch table (L54-70) but not capability registry contracts.
   - **Proposed change**: Expand breaking change registry to include capability entry points and configuration contracts.
   - **Rationale**: PRs #4 and #14 establish these as stable interfaces requiring coordination.
   - **Risk if ignored**: Uncoordinated changes to capability contracts breaking third-party extensions.

8. **Operator Configuration Pattern Recognition** (Priority: P2)
   - **Current state**: No constitutional recognition of operator-configurable surfaces.
   - **Proposed change**: Add principle establishing configuration-without-fork as standard pattern for deployment-time customization.
   - **Rationale**: PR #14's CONVERSUS_DISABLED_TOOLS represents important operational pattern.
   - **Risk if ignored**: Proliferation of deployment forks instead of configuration-based customization.

### Referenced Documentation

- `CONSTITUTION.md` — sections/lines cited: L34-45, L47-71, L72-84, L240-265, L495, L54-70, L19-21
- `recent-changes.md` — sections/lines cited: L10-21, L24-41, L64-81, L87-104, L106-118