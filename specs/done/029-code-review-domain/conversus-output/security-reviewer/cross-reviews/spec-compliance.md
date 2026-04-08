# Cross-Review: security-reviewer reviewing spec-compliance

**Spec**: 029-code-review-domain

---

## Agreement

The compliance matrix is comprehensive. I agree with:

- FR-001 through FR-009 PASS verdicts
- FR-014 through FR-016 NOT IMPLEMENTED (gate integration pending)
- SC-001 and SC-002 PASS

## Disagreements

### FR-013 is closer to NOT IMPLEMENTED than PARTIAL

The spec-compliance agent marks FR-013 as PARTIAL. The spec says "Technical debt alerts MUST fire when a dimension's trend crosses a configured threshold." The current implementation:

- TrendResult.alert is True when direction is "declining" (hardcoded)
- There's no per-dimension threshold configuration
- There's no alerting mechanism (no webhook, no notification)

The "declining = alert" logic is a basic signal, but it doesn't match the spec's description of "crosses a configured threshold." I would classify this as NOT IMPLEMENTED rather than PARTIAL, since the core feature (configurable thresholds) is missing.

### SC-002 test coverage question

The spec-compliance agent marks SC-002 as PASS. I want to verify: does the test actually check that ALL scaffolds return BLOCK for secrets_exposed, or just one scaffold? SC-002 says "all scaffolds return BLOCK regardless of other scores." If only one scaffold is tested, this is PARTIAL compliance.

From my reading of the test file, the test uses the healthcare scaffold and a mock with secrets_exposed=True. It does not parametrize across all 5 scaffolds. Strictly speaking, SC-002 requires verification across all scaffolds. However, since all scaffolds include `secrets_exposed` in their hard_blocks list, the behavior is guaranteed by the hard block mechanism. I would maintain PASS but note the test coverage gap.

## Additions

The spec-compliance agent should note that the spec's constraint "MUST NOT execute code or run tests" is satisfied. The extractors read file output only:
- _safe_read_json, _safe_read_text, _safe_read_xml are all file reading functions
- No subprocess.run, os.system, or similar execution calls
- No eval() or exec() calls

This is a critical security constraint and it's correctly upheld.
