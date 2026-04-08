# Cross-Review: spec-compliance reviewing security-reviewer

**Spec**: 029-code-review-domain

---

## Agreement

The security-reviewer's analysis is thorough and technically accurate. I agree with:

- Bandit severity mapping is reasonable
- secrets_exposed inversion logic is correct
- Hard block operator parsing works correctly
- The "MUST NOT execute code" constraint is upheld (confirmed in their cross-review)

## Disagreements

### FR-013 reclassification -- I accept the security-reviewer's argument

The security-reviewer argues FR-013 should be NOT IMPLEMENTED rather than PARTIAL. After reflection, I agree. The current implementation only has a binary "declining = alert" signal with a hardcoded threshold (slope < -0.01). The spec requires "configured threshold" which implies:
1. Per-dimension threshold configuration in scaffolds or config
2. An alerting mechanism that fires when thresholds are crossed

Neither exists. I will revise FR-013 from PARTIAL to NOT IMPLEMENTED in my revision.

### Concern #1 (LOW severity findings) -- agree with devex-advocate

The security-reviewer notes LOW severity findings are dropped. I agree with the devex-advocate that this is the right default -- LOW severity bandit findings are predominantly false positives. A scaffold-level configuration for minimum severity would be a clean enhancement.

## Additions

The security-reviewer's observation about XXE vulnerability in `_safe_read_xml()` is important to acknowledge. The `# noqa: S314` comment correctly marks this as a trusted local file operation. Since the spec constraint says extractors read local tool output only, the risk is mitigated. But if the tool evolves to accept remote inputs, switching to `defusedxml` would be necessary.

The security-reviewer did not assess whether the hard block rules in scaffolds are safe from injection. Since scaffold files are YAML (no code execution), and the hard block evaluator uses a simple string parser (not eval()), there's no injection risk. This is good security practice.
