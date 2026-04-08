# Phase 1 Review: security-reviewer

**Spec**: 029-code-review-domain
**Agent**: security-reviewer
**Focus**: Security extractor thoroughness, hard block correctness, secrets_exposed inversion

---

## Overall Assessment

The security extractor is thorough for its scope. It correctly maps bandit severity/confidence to vulnerability categories, detects secrets via gitleaks, and the scoring layer properly inverts boolean security variables. Hard block evaluation is robust with support for comparison operators and truthy checks. The healthcare scaffold correctly prioritizes security with 5x weight and 0.95 minimum threshold.

**Verdict**: PASS with observations on defense depth.

---

## Detailed Findings

### 1. SecurityExtractor Thoroughness

**Bandit parsing** (lines 349-376): The severity mapping is:
- HIGH severity + HIGH confidence = critical_vulns
- HIGH severity + other confidence = high_vulns
- MEDIUM severity = medium_vulns

This is a reasonable triage. However:
- LOW severity findings are silently dropped. While LOW findings are often noise, some projects may want to track them.
- The `issue_confidence` field in bandit output has three levels (HIGH, MEDIUM, LOW). Only HIGH confidence promotes a HIGH severity to critical. A HIGH severity + MEDIUM confidence finding would be classified as high_vulns, which is sensible but could miss some genuine critical issues.

**Gitleaks parsing** (lines 379-391): Simple and correct -- non-empty findings list = secrets exposed. Handles both list format (standard) and dict format (some versions).

### 2. secrets_exposed Inversion Logic -- CORRECT

In `domain.py` (line 86-88), the `_normalize_variable` function treats `secrets_exposed` as an inverted boolean:
```python
_INVERTED_BOOLEANS = {"secrets_exposed"}
if isinstance(value, bool):
    if name in _INVERTED_BOOLEANS:
        return 0.0 if value else 1.0  # True = bad (0.0), False = good (1.0)
```

This inversion is correct. In the scoring system, higher values = better. Having secrets exposed is bad, so `True -> 0.0`. The `_INVERTED_BOOLEANS` set is extensible for future inverted variables.

### 3. Hard Block Evaluation -- ROBUST

The `_evaluate_hard_block` function in `domain.py` (lines 152-202) supports:
- Simple truthy check: `"secrets_exposed"` -- triggers if variable is truthy
- Comparison operators: `"critical_vulns > 0"`, `"has_spec == false"`
- Type coercion: boolean parsing for "true"/"false" strings, numeric parsing

**Concern**: The operator matching (line 163) iterates through operators in order: `==`, `!=`, `>=`, `<=`, `>`, `<`. Since `==` is checked before `>=`, a rule like `"x >= 5"` would first try to split on `==` (finding no match at `>=`), then correctly split on `>=`. Wait -- actually `==` is contained within `>=`, so `rule.split("==", 1)` on `"x >= 5"` would split at the `=` in `>=`, producing `["x >", " 5"]`. This would fail to parse `"x >"` as a variable name and fall through.

Actually, re-reading the code: the `for op_str ... in rule` check on line 163 uses `if op_str in rule`, so `"=="` would match `"x >= 5"` because `==` is not literally in `>=`. Wait -- `"=="` is not a substring of `">="`. So the check correctly moves to `>="` match. Let me trace again:

- `">=" in "x >= 5"` -> True. Split on `">=": ["x ", " 5"]`. var_name = "x", rhs = "5". Correct.

The ordering `==, !=, >=, <=, >, <` ensures multi-character operators are checked before single-character ones, which is the correct approach.

### 4. Hard Block Configuration in Scaffolds

The healthcare scaffold defines:
```yaml
hard_blocks:
  - secrets_exposed
  - critical_vulns > 0
  - has_spec == false
  - has_changelog_entry == false
```

These are appropriate for a regulated environment:
- `secrets_exposed`: Any exposed secret is a hard block
- `critical_vulns > 0`: Any critical vulnerability is a hard block
- `has_spec == false`: No spec = no deployment in healthcare
- `has_changelog_entry == false`: Audit trail requirement

The startup-mvp scaffold has a reduced set: only `secrets_exposed` and `critical_vulns > 0`. This is appropriate for fast-moving teams.

### 5. Security Scoring Normalization

In `_normalize_variable` (lines 92-98), vulnerability counts are normalized using a soft cap: `score = 1.0 / (1.0 + count)`. This means:
- 0 vulns -> score 1.0
- 1 vuln -> score 0.5
- 4 vulns -> score 0.2
- 9 vulns -> score 0.1

This is a reasonable diminishing-return curve. The first vulnerability has the largest impact, which correctly models the risk step function (going from 0 to 1 vulnerability is the biggest deal).

### 6. Missing: No SAST Tool Integration Beyond Bandit

The extractor supports bandit (Python SAST) and gitleaks (secrets). It does not support:
- Semgrep (multi-language SAST, increasingly popular)
- Snyk or Dependabot (dependency vulnerability scanning)
- Trivy (container scanning)

These are out of scope for the initial implementation (pluggable extractors allow future addition), but should be noted for the roadmap.

---

## Concerns

| # | Severity | Item |
|---|----------|------|
| 1 | Low | LOW severity bandit findings silently dropped |
| 2 | Low | No dependency vulnerability scanning (Snyk/Dependabot) |
| 3 | Info | Soft cap normalization curve for vulns may be too aggressive (1 vuln = 0.5 score) |

---

## Recommendation

Accept. The security extractor is thorough for its stated scope, the secrets_exposed inversion logic is correct, and hard blocks work correctly. The pluggable extractor architecture allows future security tool additions.
