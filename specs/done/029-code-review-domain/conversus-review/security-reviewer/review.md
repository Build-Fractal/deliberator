# Security Reviewer — Phase 1 Review: Code Review Domain (Spec 029)

## Executive Summary

The code review domain plugin handles security fundamentals correctly: all 5 scaffolds block on `secrets_exposed`, the `_evaluate_hard_block` function processes comparison operators safely, and the SecurityExtractor parses bandit/gitleaks output without executing arbitrary code. However, the security model has structural weaknesses that undermine the safety guarantees the spec promises.

The most severe issue is that the `secrets_exposed` inversion logic in `_normalize_variable` is correct but fragile — it depends on a hard-coded set (`_INVERTED_BOOLEANS`) that must be manually maintained. The hard block evaluation for `secrets_exposed` uses a different code path (truthy check, line 195-202) than the inversion in normalization (line 85-89), creating two parallel mechanisms that must stay synchronized. The SecurityExtractor's bandit parser maps HIGH severity + HIGH confidence to "critical" — a synthetic severity level that bandit does not define — which could cause confusion when developers cross-reference tool output with domain scores.

The hard block system is sound in design but incomplete in coverage: the scaffolds block on `secrets_exposed` and `critical_vulns > 0`, but no scaffold blocks on `high_vulns > 0` despite HIGH severity vulnerabilities being genuinely dangerous. The scoring can be gamed by manipulating which tool reports are provided, and the API surface described in the spec (Section 3, API Layer) has potential injection vectors that the implementation does not yet address.

---

## SecurityExtractor Thoroughness

### Bandit Parser — ADEQUATE

The `_parse_bandit` method correctly handles both the `{"results": [...]}` dict format and a flat list format. The severity/confidence mapping is:

| bandit severity | bandit confidence | Domain variable |
|---|---|---|
| HIGH | HIGH | `critical_vulns` |
| HIGH | non-HIGH | `high_vulns` |
| MEDIUM | any | `medium_vulns` |
| LOW | any | not counted |

This mapping has two issues:

1. **LOW severity findings are silently discarded.** The bandit fixture (`bandit-output.json`) includes a B101 (assert_used) finding at LOW severity that is not counted. While LOW severity findings are often noise, discarding them entirely means the domain has no visibility into the LOW-severity count. A team that suppresses all LOW findings with `# nosec` would have the same security profile as one that does not — the domain cannot distinguish them.

2. **The "critical" severity is synthetic.** Bandit uses LOW/MEDIUM/HIGH, not CRITICAL. The domain creates a synthetic CRITICAL level by combining HIGH severity with HIGH confidence. This is a reasonable heuristic but it is undocumented in the spec. Developers inspecting bandit output will see 2 HIGH severity findings, but the domain reports 2 "critical" findings. This mismatch will cause confusion.

### Gitleaks Parser — CORRECT

The `_parse_gitleaks` method correctly interprets a non-empty finding list as `secrets_exposed = True` and an empty list as `False`. The fallback for dict-wrapped output (`data.get("findings", data.get("leaks", []))`) covers both the standard format and older versions.

### Missing Tool Support

The SecurityExtractor handles only bandit and gitleaks. The following widely-used security tools are not supported:

- **Semgrep** — the dominant SAST tool for polyglot codebases (SARIF or JSON output)
- **CodeQL** — GitHub's built-in SAST (SARIF output)
- **Snyk** — dependency vulnerability scanning (JSON output)
- **pip-audit / safety** — Python dependency audit (JSON output)
- **npm audit** — JavaScript dependency audit (JSON output)
- **trivy** — container and dependency scanning (JSON output)

The absence of dependency vulnerability scanning is particularly concerning. The SecurityExtractor focuses on code-level vulnerabilities (bandit) and secrets (gitleaks) but has no mechanism for detecting known-vulnerable dependencies, which are the most common attack vector in modern applications.

---

## secrets_exposed Inversion Correctness

### Normalization Path

In `_normalize_variable` (domain.py, line 85-89):

```python
_INVERTED_BOOLEANS = {"secrets_exposed"}
if isinstance(value, bool):
    if name in _INVERTED_BOOLEANS:
        return 0.0 if value else 1.0  # True = bad = 0.0
    return 1.0 if value else 0.0
```

This is **correct**: `secrets_exposed = True` normalizes to 0.0 (bad), `False` normalizes to 1.0 (good). The inversion is necessary because most booleans in the domain follow the convention "True = good" (e.g., `format_compliant = True` is good), but `secrets_exposed = True` is bad.

### Hard Block Path

In `_evaluate_hard_block` (domain.py, line 195-202), the simple truthy check:

```python
value = variables.get(rule)  # rule = "secrets_exposed"
if isinstance(value, bool):
    return value  # True → block triggered
```

This is **correct**: `secrets_exposed = True` triggers the block, `False` does not.

### Synchronization Risk

The two paths are correct today but use different mechanisms:
- Normalization uses an explicit `_INVERTED_BOOLEANS` set
- Hard block uses Python's truthiness

If a future developer adds a new inverted boolean (e.g., `has_known_exploits`) they must:
1. Add it to `_INVERTED_BOOLEANS` for normalization
2. Add it to the scaffold's `hard_blocks` list
3. Ensure the truthy check in `_evaluate_hard_block` works correctly

Step 1 is easy to forget because `_INVERTED_BOOLEANS` is defined inside the function body as a local constant, not as a module-level constant or configuration. This should be elevated to a module-level constant with a docstring explaining the inversion semantics.

### Edge Case: secrets_exposed = None

If no gitleaks report is provided, `secrets_exposed` is `None`. In the hard block path, `variables.get("secrets_exposed")` returns `None`, and the function returns `False` (line 197: `if value is None: return False`). This means **missing gitleaks data causes the secrets hard block to not trigger**. This is the correct behavior per FR-003 ("missing tool output MUST default to None, not zero") but creates a security gap: the easiest way to bypass the secrets block is to not provide a gitleaks report.

---

## Hard Block Assessment

### Current Hard Blocks by Scaffold

| Scaffold | secrets_exposed | critical_vulns > 0 | has_spec == false | has_changelog_entry == false |
|---|---|---|---|---|
| startup-mvp | Yes | Yes | No | No |
| enterprise | Yes | Yes | No | Yes |
| healthcare | Yes | Yes | Yes | Yes |
| api-service | Yes | Yes | No | No |
| open-source | Yes | Yes | No | No |

### Assessment

- **secrets_exposed — correct across all scaffolds.** A secret in code is always a hard block regardless of context. No scaffold should ever score a "pass" with exposed secrets.

- **critical_vulns > 0 — correct but based on synthetic severity.** As noted above, "critical" is a domain-defined combination (HIGH severity + HIGH confidence), not a standard bandit level. The threshold is appropriate given the synthetic definition.

- **Missing: high_vulns > 0.** No scaffold blocks on HIGH severity vulnerabilities. The enterprise and healthcare scaffolds have `minimum_security: 0.9` and `0.95` thresholds, which would catch high vuln counts through dimension scoring. But the startup-mvp and api-service scaffolds have `minimum_security: 0.8`, and a single HIGH vulnerability without HIGH confidence (which counts as `high_vulns`, not `critical_vulns`) would score `1 / (1 + 1) = 0.5` for that variable. Combined with clean values for `critical_vulns` (1.0), `medium_vulns` (1.0), and `secrets_exposed` (1.0), the security dimension would average 0.875 — above the 0.8 threshold. A HIGH severity vulnerability passes the startup-mvp scaffold. This seems wrong for a scaffold that claims "security basics."

- **has_spec == false and has_changelog_entry == false — appropriate for healthcare.** These are compliance requirements, not security blocks. Their presence on healthcare (a regulated environment scaffold) is correct.

### Operator Parsing Security

The `_evaluate_hard_block` function parses operator strings using string splitting. The parsing order (line 164-166) checks `==` before `>` and `<`, which prevents `>=` from being misinterpreted as `>` with `=` in the RHS. However, the operator check uses `if op_str in rule`, which means a rule like `has_spec == false` would match `==` (correct) but a malformed rule like `something===bad` would also match `==` and split incorrectly. The `parts = rule.split(op_str, 1)` with `maxsplit=1` provides some protection, but the parsing is not robust against adversarial input. Since scaffolds are YAML files loaded from disk (not user input at runtime), this is acceptable — but if the API layer ever allows user-defined scaffolds, this parser needs hardening.

---

## Gaming Vectors

### 1. Selective Report Omission

The most effective gaming strategy is to omit tool reports for dimensions where the project performs poorly. Because `_score_dimension` excludes None values and `score()` excludes None dimensions from the weighted composite:

- **Omit security reports** → security dimension is None → excluded from composite → score improves
- **Omit coverage reports** → test quality dimension is None → excluded → score improves
- **Omit complexity reports** → code quality dimension improves (fewer variables with low scores)

This is a fundamental design flaw. The scoring system rewards ignorance over transparency. A project that runs all analysis tools and surfaces issues will score lower than one that runs none.

**Mitigation**: Apply a penalty when a dimension has no data. For example, a dimension with all None variables could score 0.5 (uncertain) rather than being excluded.

### 2. Trivial Coverage Inflation

The `line_coverage` variable measures statement coverage, which can be inflated by testing trivial code paths. A developer can write tests that exercise getters, setters, and constant definitions to achieve high line coverage without testing meaningful logic. The `branch_coverage` variable partially mitigates this, but both can be inflated by testing easy branches and ignoring hard ones.

The `edge_case_coverage` variable from the spec (Section 2, parameters) is defined but not extracted by any extractor, so the spec's intended mitigation (measuring error path and boundary testing) is not operational.

### 3. Complexity Manipulation

Cyclomatic complexity can be reduced by extracting conditions into helper functions without reducing actual logical complexity. The domain would see lower `cyclomatic_complexity_avg` but the code is not actually simpler.

### 4. Hard Block Bypass

As noted in the `secrets_exposed = None` analysis, not providing a gitleaks report bypasses the secrets hard block. Similarly, not providing a bandit report means `critical_vulns` is None, bypassing the `critical_vulns > 0` hard block. **A project with active security vulnerabilities and exposed secrets can score "pass" on all scaffolds simply by not running security scanners.**

---

## API Safety (Spec Section 3)

The spec defines seven API endpoints. The implementation does not yet include the API layer, but the spec design has potential issues:

### POST /api/review — Submit a Review

The endpoint accepts `repo_root`, `changed_files`, and `spec_path` as input. If the extractor code ever evolves to read files at these paths (rather than reading tool output), this creates a **path traversal risk**: an attacker could submit `repo_root: /etc/` and `spec_path: /etc/passwd` to read arbitrary files. Currently, extractors read only tool output files specified via context attributes, so this is not an active vulnerability, but the API design should validate that all paths are within a configured workspace root.

### GET /api/developers/:author — Developer Profile

This endpoint aggregates scores by author. If developer names come from git history, they could contain special characters that cause issues in downstream systems (e.g., SQL injection if using raw string interpolation, XSS if rendered in a web UI). The spec mentions Supabase as a backend, which uses parameterized queries, but the JSONL backend could be vulnerable if the query function uses naive string matching.

### Hard Block Rule Injection

If user-defined scaffolds are ever supported via the API, the `_evaluate_hard_block` function would parse user-supplied rule strings. While the current parser is limited to simple comparisons, the `eval`-like nature of rule evaluation (comparing named variables to values) creates a potential for confusion attacks where a rule like `secrets_exposed == true` (without quotes) is parsed differently from `secrets_exposed` (truthy check).

---

## Recommendations

### Ordered by Security Impact

1. **[CRITICAL] Missing data must not improve scores** — Apply a configurable penalty when a dimension has no data rather than excluding it from the weighted composite. The current behavior creates a perverse incentive to not run security scanners. Default penalty: 0.5 (uncertain). Configurable per-scaffold so healthcare can set missing_data_penalty to 0.0 (block) while startup-mvp can set it to 0.5 (warn).

2. **[CRITICAL] Hard blocks must trigger on missing security data** — When `secrets_exposed` is None (no gitleaks report) and the scaffold has `secrets_exposed` in its `hard_blocks`, the system should either (a) block with a message indicating missing data, or (b) treat missing as "unknown, which is not clean" and trigger the block. Currently, None bypasses all hard blocks, which defeats the purpose of mandatory security gates.

3. **[HIGH] Add dependency vulnerability scanning** — At minimum, support pip-audit JSON and npm-audit JSON output. Dependency vulnerabilities (known CVEs in third-party packages) are the most common attack vector and are entirely invisible to the current extractor set.

4. **[HIGH] Elevate `_INVERTED_BOOLEANS` to module-level constant** — Move the set from inside `_normalize_variable` to module scope with documentation explaining the inversion semantics. This reduces the risk of a future developer adding an inverted boolean to the hard blocks but forgetting to add it to the inversion set.

5. **[MEDIUM] Add `high_vulns > 0` hard block to healthcare and enterprise scaffolds** — HIGH severity vulnerabilities in regulated or production environments should be hard blocks, not just score penalties. A single HIGH vuln currently passes startup-mvp through dimension scoring.

6. **[MEDIUM] Document the synthetic "critical" severity mapping** — The bandit parser creates a severity level that bandit does not define. Document this mapping in the SecurityExtractor docstring and in any user-facing scaffold documentation.

7. **[LOW] Add path validation for API inputs** — When the API layer is implemented, validate that all file paths in review submission requests are within a configured workspace root. Reject paths containing `..` or absolute paths outside the workspace.

---

## Referenced Files

- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/domains/code_review/domain.py` — `_normalize_variable` (lines 76-126), `_evaluate_hard_block` (lines 152-202), `_score_dimension` (lines 128-149)
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/domains/code_review/extractors.py` — `SecurityExtractor` (lines 311-392), `_parse_bandit` (lines 349-376), `_parse_gitleaks` (lines 378-392)
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/domains/code_review/scaffolds/*.yml` — hard block configurations
- `/Users/business-daddy/code/payer-index-mono/conversus/tests/test_code_review.py` — SC-002 test (lines 667-684), SecurityExtractor tests (lines 241-298)
- `/Users/business-daddy/code/payer-index-mono/conversus/tests/fixtures/code_review/bandit-output.json` — bandit fixture with severity/confidence mapping
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/029-code-review-domain/spec.md` — API layer (Section 3), parameters (Section 2), constraints (Section 6)
