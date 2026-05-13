Looking at the spec files and my role as adapter-consumer, I need to read the target documents first before proceeding with my review.

Now I need to look for any consumer-side documentation that would help me understand the adapter's perspective. Let me check if there are any relevant files in the orchestrator directory.

Based on my reading of the target files and my role as adapter-consumer representing downstream consumers of conversus-oss output, here is my review:

---

### Executive Summary

The spec proposes migrating conversus deliberation outputs from grep-parsed markdown to XML schema validation, addressing three production bugs caused by format-contract drift. As the primary downstream consumer, the orchestrator's spec-kit adapter (`scripts/dispatch/adapters/tool/conversus.sh`) currently relies on hardcoded grep patterns to extract verdict lines from arbitration outputs (e.g., `Q1 RULING: APPROVE-WITH-FIXES — rationale`). This migration represents a fundamental breaking change to consumer interfaces but addresses real fragility in the current display-text contract that has caused silent failures. The proposed XML structure with `<ruling_lines>` provides better parse reliability, but the migration path needs more consumer-protective guarantees. My most important recommendation is to mandate parallel format support with explicit consumer CI validation during the entire transition window, not just as an optional courtesy.

### Alignment

- **Schema-driven stability** (L306-309): The spec's `CONSUMER-CONTRACT.md` approach aligns with established consumer-side pinning patterns. Principle XXVIII sub-clause 4 provides the contract surface consumers need to declare their dependencies and pin version ranges.

- **Denormalized ruling lines** (L225-226): The `<ruling_lines>` block specifically addresses current adapter usage patterns. The spec correctly identifies that spec-kit-orc "grep-extracts one-line ruling summaries and benefits from a flat list" - this shows understanding of actual consumer needs.

- **Backward-compatibility mandate** (L364): The transition window explicitly requires "spec-kit-orc adapter supports both formats during the window" which protects consumers from forced lockstep upgrades.

- **Consumer CI fixtures** (L308): Both producer and consumer CI verification creates mutual enforcement of the contract surface, preventing silent drift that has caused production bugs.

### Missed Opportunities

- **Validator format specification**: The spec defers XSD vs JSON Schema choice (§5.1) but doesn't address consumer parsing complexity. XML parsing requires heavier tooling (xmllint/lxml) vs JSON which has ubiquitous shell parsing support. Impact: high - affects operational complexity of adapter migration.

- **Schema evolution API**: No mechanism specified for consumers to query supported schema versions from a deployed conversus-oss instance. Consumers need runtime version discovery, not just static `CONSUMER-CONTRACT.md` declarations. Impact: medium - affects adapter's ability to gracefully handle version mismatches.

- **Parallel format signal**: When both `.xml` and `.md` exist during transition, spec says "XML is preferred when both are present" but doesn't specify the discovery mechanism. Should adapters check for both files? Is there a metadata signal? Impact: medium - affects transition reliability.

- **Cross-repo CI coordination**: Consumer CI fixtures are mentioned but not specified. Orchestrator needs vendored fixture sets from conversus-oss, but the update mechanism when conversus-oss schema evolves isn't detailed. Impact: medium - affects consumer test maintenance.

- **Error handling semantics**: When XML validation fails at write-time (L243), what artifact does the consumer receive? Is partial output preserved? Current adapter expects some output artifact; silent failure breaks downstream expectations. Impact: medium - affects consumer resilience.

- **Version constraint failure modes**: When consumer declares `>=1.0.0,<2.0.0` but conversus-oss moves to 2.0.0, how does the adapter detect incompatibility? Runtime discovery vs build-time checks. Impact: medium - affects operational monitoring.

- **Schema namespace stability**: The namespace `https://build-fractal.org/conversus/schema/v1` is declared stable across PATCH/MINOR (L284) but the enforcement mechanism isn't specified. Consumer parsers may cache namespace resolution. Impact: low - namespace changes are rare but brittle.

- **Migration testing strategy**: No specification for validating that XML → MD → grep extraction produces identical results to current markdown during transition. Consumer needs proof of semantic equivalence. Impact: medium - affects migration confidence.

- **Rollback procedure**: If XML migration introduces consumer-breaking changes, what's the rollback path? Consumers may need emergency fallback to markdown mode. Impact: low - unlikely but critical if needed.

### Off-Base Assumptions

- **Consumer parsing effort assumption** (L291): The spec assumes "New parser invokes `xmllint --xpath` (or equivalent Python `lxml`)" understates migration complexity. The adapter currently uses simple grep/sed patterns integrated with shell pipelines. XML parsing requires fundamentally different tooling, error handling, and namespace management. The migration is not a drop-in replacement.

- **"Convenience" framing of ruling_lines** (L225): The spec treats `<ruling_lines>` as adapter convenience, but it's actually a consumer requirement. Without the denormalized format, consumers would need complex XPath traversal to extract verdict summaries. This is a consumer contract necessity, not optimization.

### Actionable Recommendations

1. **Mandate parallel CI validation** (Priority: P1)
   - **Current state**: Spec § 6.2 mentions "Markdown-format outputs are still consumed for backward compatibility during the migration window" (L291).
   - **Proposed change**: Add to § 6.2: "Consumer CI MUST validate identical semantic extraction from both XML and markdown formats during transition. Consumer CI failure on format divergence blocks conversus-oss merges."
   - **Rationale**: Consumer protection requires active validation, not passive compatibility. Cross-repo CI enforcement prevents consumer-side silent breaks.
   - **Risk if ignored**: Consumer adapters may silently break during transition with no detection mechanism.

2. **Specify version discovery mechanism** (Priority: P1)
   - **Current state**: Schema version appears only in output attributes (L75); no runtime discovery specified.
   - **Proposed change**: Add to CONSUMER-CONTRACT.md declaration: "Consumers query supported schema versions via [mechanism] before parsing. Conversus-oss MUST provide version compatibility API at [endpoint/file]."
   - **Rationale**: Consumer adapters need runtime version negotiation to handle schema evolution gracefully.
   - **Risk if ignored**: Adapter failures when schema versions diverge; no graceful degradation path.

3. **Strengthen format discovery mechanism** (Priority: P1)
   - **Current state**: Spec § 5.2 says "XML is canonical; companion `.md` is rendered-for-humans" but discovery logic unspecified.
   - **Proposed change**: Define precedence rules: "Consumers MUST check for .xml first; if absent, fallback to .md. During transition, both formats MUST be semantically identical per consumer CI validation."
   - **Rationale**: Explicit precedence prevents format selection ambiguity that could cause consumer parsing errors.
   - **Risk if ignored**: Race conditions or inconsistent format selection during transition.

4. **Define consumer fixture update procedure** (Priority: P2)
   - **Current state**: Spec § 5.3 mentions "vendored copy of conversus-oss's fixture set" (L293) but update mechanism unspecified.
   - **Proposed change**: Add to § 7: "Consumer repositories vendor conversus-oss fixtures via [mechanism]. Conversus-oss schema changes trigger automated PRs to consumer repositories updating vendored fixtures."
   - **Rationale**: Consumer CI fixtures must stay synchronized with producer schema evolution or they become stale/misleading.
   - **Risk if ignored**: Consumer CI fixtures drift from reality; false confidence in contract compliance.

5. **Specify validation failure artifact behavior** (Priority: P2)
   - **Current state**: Spec L243 says validation failure "does not write the malformed file" but consumer expectations unaddressed.
   - **Proposed change**: Add to § 5.1: "On validation failure, engine writes .xml.error file with diagnostic info; consumers detect absence of expected .xml and handle gracefully."
   - **Rationale**: Consumer adapters need predictable failure modes; silent absence is harder to handle than explicit error artifacts.
   - **Risk if ignored**: Consumer adapters may hang waiting for output files that never arrive; poor operational visibility.

6. **Mandate semantic equivalence testing** (Priority: P2)  
   - **Current state**: Migration strategy § 11 lacks validation that XML→markdown→grep produces identical results.
   - **Proposed change**: Add to § 11.1: "Migration MUST include compatibility tests proving XML parsed verdicts match grep-extracted verdicts on all historical arbitration outputs."
   - **Rationale**: Consumer confidence requires proof of semantic preservation across format migration.
   - **Risk if ignored**: Subtle semantic changes during migration break consumer assumptions without detection.

7. **Document schema evolution consumer impact** (Priority: P3)
   - **Current state**: Schema versioning § 4.8 focuses on producer-side bump procedure; consumer impact unspecified.
   - **Proposed change**: Add consumer impact table: "MAJOR bumps require consumer adapter update; MINOR bumps are backward-compatible; PATCH bumps transparent to consumers."
   - **Rationale**: Consumer planning requires predictability of schema evolution impact.
   - **Risk if ignored**: Consumer upgrade planning becomes ad-hoc; unexpected breaking changes.

8. **Add rollback procedure specification** (Priority: P3)
   - **Current state**: Migration is described as forward-only; no rollback path for consumer failures.
   - **Proposed change**: Add to § 11: "Emergency rollback procedure: conversus-oss --legacy-markdown-mode flag forces markdown output for consumer compatibility during rollback scenarios."
   - **Rationale**: Mission-critical consumers need rollback guarantees for operational safety.
   - **Risk if ignored**: No escape path if XML migration breaks critical consumer systems.

### Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/build-fractal/conversus/conversus-oss/specs/v4.2.0-structured-deliberation-outputs/spec.md` — sections cited: L225-226, L284, L291, L306-309, L364, L75, L243, L291, L293, L364
- `/Users/business-daddy/code/payer-index-mono/build-fractal/conversus/conversus-oss/CONFORMANCE.md` — sections cited: L49 (XXVIII Provisional status)
- `/Users/business-daddy/code/payer-index-mono/build-fractal/conversus/conversus-oss/deliberations/v4.1.0-persistence-contract-discipline-originating-2026-05-11/arbitration/resolution.md` — sections cited: L175-177 (current ruling line format)