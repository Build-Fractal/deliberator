### Dangerous Contradictions

- **Templating Engines tier placement vs. conversus N/A claim**
  - **admission-auditor-enhanced claims**: "The templates/ directory contains 8 mode-specific subdirectories (cooperative, red-blue, etc.) plus meta-review-instructions.md, indicating significant templating infrastructure that contradicts the VIII N/A claim about 'no templating surface.'" (Missed Opportunities section)
  - **tier-classifier claims**: If VIII (Templating Engines) is classified Universal (Tier 1), it should apply to every Build Fractal product. However, the conversus repo's N/A claim suggests templating is actually conversus-oss specific, which would make VIII Suite-tier, not Universal.
  - **Why this is dangerous**: If VIII stays Universal but conversus legitimately has no templating surface (as it claims), then Universal tier includes principles that don't apply universally. Conversely, if conversus does have templating (as evidence suggests), then the N/A claim is false and admission should be deferred.
  - **Suggested resolution**: admission-auditor-enhanced should investigate whether conversus's templating is genuinely upstream-delegated vs. actual local templating. If local templating exists, support VIII as Universal. If truly upstream-only, reclassify VIII to Suite tier.

- **Plugin Isolation enforcement level mismatch**
  - **admission-auditor-enhanced claims**: "DEFER admission until Plugin Isolation (XV) is actually achieved" because "pyproject.toml ships OSS-duplicate modules, violating isolation regardless of entry-point structure" (Executive Summary, Actionable Recommendations #5)
  - **tier-classifier claims**: If XV (Plugin Isolation) violations are systemic across conversus repos, this suggests the principle either needs Universal-tier enforcement (stronger discipline) or the monetization seam concept is Suite-specific but requires better compliance mechanisms.
  - **Why this is dangerous**: Deferring admission for XV violations while keeping XV at Suite tier creates a catch-22: repos can't join the suite until they comply with suite rules, but suite rules only apply to suite members. This could prevent any paid layer from ever achieving compliant admission.
  - **Suggested resolution**: Either promote XV to Universal tier (making plugin isolation a universal Build Fractal discipline) or create a provisional admission path with mandatory XV remediation timeline.

- **Evidence standard for tier classification vs. compliance**
  - **admission-auditor-enhanced claims**: Uses direct codebase inspection ("linter/models.py file defines 4 StrEnums", "templates/ directory with 8 mode subdirectories") to contradict conformance claims (Off-Base Assumptions section)
  - **tier-classifier claims**: Tier classification should be based on principle scope analysis from CONSTITUTION.md text, not on whether specific repos currently comply. A principle can be correctly tiered even if repos misstate their compliance.
  - **Why this is dangerous**: If admission decisions use codebase evidence to override conformance declarations, but tier classification uses principle text analysis, the same evidence leads to different conclusions about whether principles apply. This creates unstable classification boundaries.
  - **Suggested resolution**: Establish whether tier classification should be based on principle text scope or empirical repo compliance patterns. admission-auditor-enhanced's evidence-based approach should inform tier boundaries, not just admission decisions.

### Tensions

- **Compliance-first vs. classification-first sequencing**
  - **admission-auditor-enhanced's position**: Focuses on whether conversus correctly declares compliance against current tier assignments, recommending deferral until actual compliance is achieved (Actionable Recommendations section)
  - **tier-classifier's position**: Focuses on whether the 26 principles are assigned to appropriate tiers based on their inherent scope, which could change what compliance means
  - **Nature of tension**: admission-auditor-enhanced evaluates repos against fixed tier assignments while tier-classifier evaluates whether those assignments are correct. If tier assignments change, compliance evaluations become obsolete.
  - **Coordination needed**: tier-classification should complete before final admission decisions. If principles move between tiers, conformance declarations must be re-evaluated against the new assignments.

- **Granular codebase analysis vs. architectural scope analysis**
  - **admission-auditor-enhanced's position**: Uses specific file-level evidence ("test_engine_providers.py and test_engine_providers_anthropic.py import from engine.providers") to challenge N/A claims (Missed Opportunities section)
  - **tier-classifier's position**: Analyzes principle scope by reading constitutional text and asking which Build Fractal products would need each constraint
  - **Nature of tension**: File-level evidence proves what repos actually do, but tier classification needs to determine what repos should be required to do. Current practice vs. appropriate scope may differ.
  - **Coordination needed**: admission-auditor-enhanced's evidence should inform whether tier boundaries are drawn correctly. If many Suite-tier principles have Universal-tier evidence patterns, boundaries need adjustment.

- **Remediation timeline vs. classification stability**
  - **admission-auditor-enhanced's position**: Accepts Provisional status with specific deadlines (2026-08-01 for multiple principles) as adequate for admission
  - **tier-classifier's position**: Tier boundaries should be stable enough that classification doesn't depend on whether repos happen to be compliant this quarter
  - **Nature of tension**: Provisional admissions create time pressure to maintain current tier assignments even if they're wrong, because changing tiers would invalidate remediation plans.
  - **Coordination needed**: If tier reclassifications are needed, Provisional deadlines should be extended to allow repos to re-assess against new tier assignments.

- **Suite monetization boundary vs. Universal engineering discipline**
  - **admission-auditor-enhanced's position**: Treats Plugin Isolation (XV) as foundational to "suite's monetization model" and "free/paid partition principle" (Actionable Recommendations #5)
  - **tier-classifier's position**: Questions whether plugin isolation patterns could apply to any Build Fractal product with extension boundaries, not just conversus monetization
  - **Nature of tension**: admission-auditor-enhanced emphasizes conversus-specific monetization context while tier-classifier evaluates broader applicability. XV could be either Suite-specific (monetization) or Universal (extension discipline).
  - **Coordination needed**: Clarify whether XV's core constraint is "no shared modules between free/paid" (Suite-specific) or "no shared modules between core/extensions" (potentially Universal).

### Safe Agreements

- **Evidence-based analysis over wishful thinking**
  - **Shared position**: admission-auditor-enhanced provides concrete codebase evidence ("pyproject.toml explicitly documents that engine/, linter/, web/ are 'framework duplicates of OSS, retained for now'") while tier-classifier approach demands specific mechanical verification for each tier assignment. Both reject unsupported claims.
  - **Combined evidence**: admission-auditor-enhanced's file-level investigation validates that principles have actual implementation surfaces, supporting tier-classifier's requirement that tier assignments be based on real applicability rather than theoretical scope.
  - **Confidence level**: High - both approaches converge on requiring verifiable substance over aspirational declarations.

- **Constitutional consistency across hierarchy levels**
  - **Shared position**: admission-auditor-enhanced emphasizes that "Plugin Isolation violation means the paid layer is still entangled with OSS code, contradicting the fundamental monetization seam" while tier-classifier evaluates whether principles maintain consistent meaning across tier boundaries.
  - **Combined evidence**: admission-auditor-enhanced's findings about framework duplicates demonstrate that tier assignments must reflect actual architectural boundaries, not planned boundaries. tier-classifier's scope analysis ensures principles apply coherently at their assigned tier.
  - **Confidence level**: High - architectural integrity matters at both compliance and classification levels.

- **Mechanical verification as constitutional requirement**
  - **Shared position**: admission-auditor-enhanced cites "Constitutional Inclusion Criterion 1 requires mechanical verification capability for all principles" while tier-classifier's framework evaluates "mechanical-verification mechanism" for each principle's tier placement.
  - **Combined evidence**: Both approaches rely on Criterion 1's requirement that principles be objectively verifiable. admission-auditor-enhanced tests this by examining CI evidence; tier-classifier tests this by analyzing verification feasibility at each tier level.
  - **Confidence level**: Medium - agreement exists on the requirement, but coordination needed on whether verification happens at repo level (admission focus) or principle level (classification focus).