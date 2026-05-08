### Executive Summary

The conversus CONFORMANCE.md declaration presents a concerning pattern of misrepresenting the actual repo state, particularly around N/A claims that appear to be "we don't think it applies" disguised as structural justifications. Four of the five N/A claims I investigated are contradicted by the actual codebase: the repo defines StrEnums (violating the XIII N/A claim), ships template directories (contradicting the VIII N/A claim), contains provider implementations and tests (undermining the XXIII N/A claim), and most critically, still ships framework duplicates despite claiming PR #30 achieved Plugin Isolation. The Provisional deadline clustering around 2026-08-01 suggests unrealistic coordination timelines, and the Plugin Isolation "Satisfied" claim is demonstrably false based on the pyproject.toml's own comments about retaining framework duplicates.

The declaration systematically overstates compliance while understating the scope of principles that actually apply to this repo. Most significantly, the Plugin Isolation violation means the paid layer is still entangled with OSS code, contradicting the fundamental monetization seam that the suite constitution assumes.

**My most important recommendation: DEFER admission until Plugin Isolation (XV) is actually achieved and the N/A claims are truthfully reassessed against the actual codebase.**

### Alignment

- **Conformance schema compliance** (`COMPLIANCE.md`, L75-136): The declaration follows the required tabular format and includes all mandatory sections (Tier 1, Tier 2, remediation plan, re-audit cadence). The structural compliance is correct.

- **Honest Provisional declarations** (`CONFORMANCE.md`, L248-254): The CHANGELOG.md gap (III) and missing CI checks (XIV, XVI, XXII) are honestly acknowledged as Provisional rather than inflated to Satisfied. These gaps are real and the remediation plans are concrete.

- **Plugin entry-points structure** (`CONFORMANCE.md`, L41-47): The entry-point declarations in pyproject.toml correctly follow the conversus.solvers/conversus.domains pattern per the compliance matrix expectations.

- **Versioning discipline** (`COMPLIANCE.md`, L40-41): The version bump 0.1.0 → 0.2.0 for the package rename is correctly classified as MAJOR under Principle III, and the need for CHANGELOG documentation is appropriately flagged.

### Missed Opportunities

- **Framework duplication detection**: The pyproject.toml explicitly documents that engine/, linter/, web/ are "framework duplicates of OSS, retained for now" (L102-105), yet the declaration claims PR #30 achieved Plugin Isolation. A contrarian audit should leverage this internal documentation as smoking-gun evidence of non-compliance.

- **Enum registry verification**: The linter/models.py file defines 4 StrEnums (InfluenceLevel, ArbiterTiming, Phase, ErrorType) that should be subject to exhaustive dispatch checks per Principle XIII. The N/A claim ignores this actual enum surface.

- **Template surface analysis**: The templates/ directory contains 8 mode-specific subdirectories (cooperative, red-blue, etc.) plus meta-review-instructions.md, indicating significant templating infrastructure that contradicts the VIII N/A claim about "no templating surface."

- **Provider testing evidence**: The test files test_engine_providers.py and test_engine_providers_anthropic.py import from engine.providers and test ModelProvider protocol compliance, contradicting the XXIII N/A claim about "no LLM providers."

- **Cross-repo coordination risks**: Three Provisional items (XIV, XVI, XXII) are deadlined 2026-08-01 with explicit coordination requirements with conversus-oss, but no evidence of joint planning or shared tracking issues to ensure atomicity.

- **CI verification gaps**: The declaration claims many principles are "Satisfied" but provides no CI evidence. For a contrarian audit, the absence of mechanical verification (per Constitutional Inclusion Criterion 1) should flag these as potentially inflated claims.

### Off-Base Assumptions

- **Plugin entry-points equal isolation** (`L42`): The declaration assumes that having plugin entry-points in pyproject.toml satisfies Plugin Isolation, when the actual requirement is "no shared modules with OSS." The pyproject.toml ships OSS-duplicate modules, violating isolation regardless of entry-point structure.

- **Upstream templating exempts local templating** (`L27`): The rationale "templating happens upstream in conversus-oss" misunderstands Principle VIII scope. The principle applies when a repo generates ANY content via templating, not just when it's the primary templating layer. The existence of templates/ makes VIII applicable.

- **String registries bypass enum principles** (`L41`): The claim that "capability dispatch is via plugin entry-points (string keys), not enums" misses that the repo defines actual StrEnums for its own domain logic, making XIII applicable regardless of entry-point dispatch mechanisms.

### Actionable Recommendations

1. **Reclassify Plugin Isolation to Provisional** (Priority: P1)
   - **Current state**: Claims XV as "Satisfied" despite shipping framework duplicates (`L42`)
   - **Proposed change**: Flip XV to Provisional with remediation plan to actually delete engine/, linter/, web/ directories and remove them from pyproject.toml wheel targets
   - **Rationale**: The pyproject.toml comment "framework duplicates of OSS, retained for now" directly contradicts the Satisfied claim
   - **Risk if ignored**: Suite admission based on false Plugin Isolation claim undermines the entire free/paid partition model

2. **Reclassify Enum Completeness to Satisfied or Provisional** (Priority: P1)
   - **Current state**: Claims XIII as N/A (`L41`)
   - **Proposed change**: Assess whether linter/models.py StrEnums are exhaustively dispatched; if yes, mark Satisfied; if no, mark Provisional with exhaustive dispatch remediation
   - **Rationale**: InfluenceLevel, ArbiterTiming, Phase, ErrorType StrEnums exist in the codebase, making XIII applicable
   - **Risk if ignored**: Repo escapes enum discipline via false N/A claim while having actual enum surface

3. **Reclassify Templating Engines to Satisfied or Provisional** (Priority: P1)
   - **Current state**: Claims VIII as N/A (`L27`)
   - **Proposed change**: Assess whether templates/ directory uses mechanical substitution per VIII requirements; mark accordingly
   - **Rationale**: templates/ directory with 8 mode subdirectories contradicts "no templating surface" claim
   - **Risk if ignored**: Repo escapes templating discipline while having actual template infrastructure

4. **Investigate Provider Robustness applicability** (Priority: P2)
   - **Current state**: Claims XXIII as N/A (`L45`)
   - **Proposed change**: Determine if test_engine_providers.py imports indicate actual provider implementations in engine/; reclassify if providers exist
   - **Rationale**: Provider test files suggest this repo may implement providers, not just consume them
   - **Risk if ignored**: Potential provider code escapes robustness requirements

5. **Defer admission pending isolation completion** (Priority: P1)
   - **Current state**: Implicit-Provisional status pending v4.0.0 ratification (`L12`)
   - **Proposed change**: DEFER admission until Plugin Isolation (XV) remediation is actually completed and verified
   - **Rationale**: Plugin Isolation is foundational to the suite's monetization model per `COMPLIANCE.md` Part IV.C requirements
   - **Risk if ignored**: Suite admits a repo that violates its core paid/free partition principle

6. **Coordinate Provisional deadlines** (Priority: P2)
   - **Current state**: XIV, XVI, XXII all deadline 2026-08-01 with "coordinate with conversus-oss" requirements (`L63-65`)
   - **Proposed change**: Establish joint tracking issues with conversus-oss before admission to ensure atomic delivery
   - **Rationale**: `COMPLIANCE.md` L67 requires "Coordinated remediations... should land in a single spec across both repos"
   - **Risk if ignored**: Remediation deadlines slip due to cross-repo coordination failures

7. **Strengthen mechanical verification claims** (Priority: P3)
   - **Current state**: Many "Satisfied" claims lack CI evidence (`L20-48`)
   - **Proposed change**: For each "Satisfied" claim, cite specific CI check, linter, or test that enforces compliance
   - **Rationale**: Constitutional Inclusion Criterion 1 requires mechanical verification capability for all principles
   - **Risk if ignored**: "Satisfied" claims become unverifiable assertions rather than auditable compliance

### Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus/CONFORMANCE.md` — L12, L20-48, L41-42, L27, L45, L63-65
- `/Users/business-daddy/code/payer-index-mono/build-fractal/conversus/COMPLIANCE.md` — L20-21, L40-41, L67, L75-136, L192-195, L248-254
- `/Users/business-daddy/code/payer-index-mono/conversus-oss/CONSTITUTION.md` — L1344-1354, L1391-1401, L1162-1172, L1745-1755
- `/Users/business-daddy/code/payer-index-mono/conversus/pyproject.toml` — L102-105, L108-111, L41-47