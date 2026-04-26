## Executive Summary

The CONSTITUTION.md v2.2.0 establishes governance guardrails for conversus, a multi-agent deliberation system, through 21 principles covering spec-driven development, stable interfaces, backward compatibility, and documentation standards. However, analysis of the 10 recent merged PRs reveals significant gaps in constitutional coverage around distribution integrity, provider robustness contracts, capability registry governance, and testing discipline for parametrized surfaces. The constitution excels at governing SKILL.md orchestration and template management but fails to address the operational invariants that ensure production reliability and packaging integrity. My most important recommendation: add Principle XXII (Distribution Surface Integrity) requiring single-sourced versioning and end-to-end distribution testing to prevent broken installations like PR #11.

### Alignment

- **Spec-driven development adherence** (`L34-45`): PR #4 correctly followed the spec-driven process as spec 064.1, demonstrating proper constitutional compliance for new feature development.
- **Single source of truth enforcement** (`L241-260`): PR #13's version drift detection (pyproject.toml 0.3.0 vs manifest.json 0.1.0) and build-time projection fix exemplifies Principle XI's demand for authoritative single sources.
- **Observable deliberation requirements** (`L102-112`): PR #10's false-PASS detection in red-blue synthesis aligns with Principle V's mandate that "agents MUST NOT silently swallow errors" and output validation must catch malformed results.
- **Explicit typing discipline** (`L194-217`): PR #10's schema→parser→contract three-layer defense demonstrates Principle IX's Pydantic model requirements and type-safe validation patterns.

### Missed Opportunities

- **Distribution surface integrity governance**: PRs #11 (broken wheel missing mcp_server.py) and #13 (version drift) reveal critical packaging gaps. The constitution covers SKILL.md and templates but ignores distribution integrity, wheel contents validation, and build-time projection discipline. **Impact: high** - broken installations directly impact user experience.

- **Provider robustness contract definition**: PRs #5 (tool-use response parsing), #6 (429 retry semantics), #8 (token tracking), and #9 (JSON format shifts) all address provider edge cases without constitutional guidance. Missing standards for rate limit handling, response format tolerance, and usage reporting. **Impact: high** - provider failures break deliberations.

- **Capability registry governance**: PRs #4 (runtime registration) and #14 (tool surface configuration) establish the registry as the cross-surface contract without constitutional recognition. No guidance on registry-first declaration, entry-point group contracts, or operator configurability patterns. **Impact: medium** - unclear extension contracts.

- **Testing discipline for parametrized surfaces**: PR #12's meta-test pattern (asserting coverage of all 7 prompts, drift guard for new prompts) represents a critical testing invariant missing from constitutional testing guidance. **Impact: medium** - silent test coverage drift.

- **Defense-in-depth validation patterns**: PR #10's schema→parser→contract three-layer fix for safety-critical synthesis represents a defensive pattern the constitution doesn't mandate for safety-critical domains. **Impact: high** - safety failures in adversarial deliberation.

- **Operator runtime configurability**: PR #14's CONVERSUS_DISABLED_TOOLS environment variable establishes deployment-time tool surface control without constitutional framework for operator customization contracts. **Impact: low** - operational flexibility gaps.

- **Versioning semantic coverage for distribution artifacts**: The constitution covers spec versioning (L582-583) but ignores distribution artifact versioning (wheel, bundle, manifest), as evidenced by PR #13's drift detection gap. **Impact: medium** - distribution integrity failures.

### Off-Base Assumptions

- **Scope limitation assumption** (`L86-100`): The constitution assumes "SKILL.md is the single source of truth for agent behavior" but ignores that distribution artifacts (wheel contents, manifests) also define agent behavior through capability availability, as demonstrated by PR #11's broken CLI.

- **Testing scope assumption** (`L302-306`): Principle XIII states enum completeness testing should verify usage, but doesn't address parametrized surface testing like PR #12's prompt coverage meta-test, missing a critical testing pattern.

### Actionable Recommendations

1. **Add Distribution Surface Integrity Principle** (Priority: P1)
   - **Current state**: Constitution has no packaging governance (no references to wheel, bundle, or manifest integrity).
   - **Proposed change**: Add Principle XXII requiring single-sourced versioning from pyproject.toml, explicit force-include for non-package modules, end-to-end distribution testing, and build-time artifact projection discipline.
   - **Rationale**: PR #11 broke `pip install conversus[mcp]` due to missing wheel contents; PR #13 showed version drift between distribution surfaces.
   - **Risk if ignored**: Continued broken installations, version inconsistencies across distribution channels.

2. **Add Provider Robustness Contract Principle** (Priority: P1)
   - **Current state**: Constitution mentions "provider-agnostic execution" but defines no robustness standards.
   - **Proposed change**: Add Principle XXIII mandating token usage reporting, retry-with-jitter for rate limits, graceful handling of format shifts, and treating structurally-valid responses as success regardless of text content.
   - **Rationale**: PRs #5, #6, #8, #9 all addressed provider edge cases without guidance, showing constitutional gap.
   - **Risk if ignored**: Provider failures will continue breaking deliberations; inconsistent error handling across providers.

3. **Expand Principle XI to cover Registry-First Declaration** (Priority: P2)
   - **Current state**: Single Source of Truth (`L241-260`) covers schema and templates but not capability registration.
   - **Proposed change**: Add bullet requiring capability registry as authoritative source for tool/prompt availability; entry-point groups as canonical extension contract.
   - **Rationale**: PRs #4 and #14 establish registry patterns without constitutional backing.
   - **Risk if ignored**: Inconsistent capability extension patterns; unclear third-party integration contracts.

4. **Add Testing Meta-Coverage Requirement** (Priority: P2)
   - **Current state**: Constitution has no guidance on testing parametrized surfaces or drift guards.
   - **Proposed change**: Add requirement to Principle IX that parametrized capabilities (prompts, tools) must include meta-tests asserting coverage completeness.
   - **Rationale**: PR #12's meta-test pattern prevents coverage drift for prompt additions.
   - **Risk if ignored**: Silent test coverage gaps when new capabilities are added.

5. **Add Safety-Critical Defense-in-Depth Principle** (Priority: P1)
   - **Current state**: Constitution mentions stable interfaces but no defensive validation patterns.
   - **Proposed change**: Add Principle XXIV requiring schema→parser→contract three-layer defense for safety-critical synthesis (red-blue, arbitration verdicts).
   - **Rationale**: PR #10's false-PASS bug demonstrates why constitutional guidance is needed for safety-critical domains.
   - **Risk if ignored**: Safety failures in adversarial deliberation contexts; synthesis verdict integrity compromised.

6. **Expand Principle XV to cover Operator Configuration** (Priority: P3)
   - **Current state**: Plugin Isolation (`L337-358`) doesn't address core tool surface configurability.
   - **Proposed change**: Add bullet requiring deployment-time tool surface configurability without code modification.
   - **Rationale**: PR #14's CONVERSUS_DISABLED_TOOLS establishes operator configuration pattern.
   - **Risk if ignored**: Limited operational flexibility; operators forced to fork for customization.

7. **Expand Principle XIV to cover Distribution Parity** (Priority: P2)
   - **Current state**: Spec-Implementation Parity (`L312-335`) only covers functional requirements vs implementation.
   - **Proposed change**: Add requirement that distribution artifacts must match documented capabilities; broken installs are spec-implementation bugs.
   - **Rationale**: PR #11's broken wheel represents spec-implementation drift in distribution surface.
   - **Risk if ignored**: Continued gap between documented and actually-available capabilities.

8. **Add Cross-Surface Versioning Requirement** (Priority: P2)
   - **Current state**: Versioning guidance (`L582-583`) only covers constitutional amendments.
   - **Proposed change**: Add requirement that all distribution surfaces (wheel, bundle, manifest) must derive version from single authoritative source.
   - **Rationale**: PR #13's version drift shows need for constitutional versioning discipline.
   - **Risk if ignored**: Version inconsistencies create user confusion and support burdens.

9. **Expand Antipattern Coverage for Distribution** (Priority: P3)
   - **Current state**: Antipattern section (`L558-571`) only references catalog.md.
   - **Proposed change**: Add explicit prohibition against hand-editing versioned artifacts; require build-time projection.
   - **Rationale**: PR #13's manual version maintenance created drift.
   - **Risk if ignored**: Continued manual maintenance of derived artifacts.

### Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus-oss/CONSTITUTION.md` — sections cited: L34-45, L86-100, L102-112, L194-217, L241-260, L302-306, L312-335, L337-358, L558-571, L582-583
- `/Users/business-daddy/code/payer-index-mono/conversus-oss/deliberations/constitution-gap-analysis-2026-04-25/recent-changes.md` — sections cited: L10-22, L23-31, L32-41, L42-52, L53-60, L61-72, L73-81, L82-93, L94-105, L106-118, L123-160