# Feature Specification: Code Review Domain Plugin

**Feature ID**: `029-code-review-domain`
**Created**: 2026-03-31
**Status**: Draft
**Depends On**: `016-plugin-system` (plugin framework), `013-objective-function-templates` (template library), `014-guided-objective-construction` (construction pipeline), `020-scenario-storage` (persistence), `027-solver-validation-flow` (validation loop)
**Origin**: First domain plugin. Proves the domain plugin architecture (spec 030).

---

## 1. Feature Summary

A domain plugin that turns code review into a quantifiable optimization problem. The plugin:

1. Defines an objective function for code quality with configurable weights
2. Extracts variables from code analysis tools (coverage, lint, complexity, spec compliance)
3. Persists review scores over time for trend analysis
4. Exposes an API for frontends and CI/CD integration
5. Uses conversus gate (spec 011) for multi-agent review with equilibrium scoring

This is the first **domain plugin** — a vertical application built on the conversus engine. It proves the pattern that spec 030 generalizes.

---

## 2. Objective Function

### Variables

```yaml
# code-review-objective.yml
name: code-review-quality
description: Multi-dimensional code quality scoring for pull request review
form: "J = -Σ wᵢ · scoreᵢ + Σ penaltyⱼ · violationⱼ"
game_form: gnep
mode_compatibility: [cooperative, red-blue]

parameters:
  # --- Spec Compliance ---
  - name: fr_satisfaction_rate
    type: float
    description: Fraction of functional requirements satisfied
    range: { min: 0.0, max: 1.0 }
    gap_question: "How many FRs does the spec define?"
    derived_from: "spec traceability analysis"

  - name: sc_pass_rate
    type: float
    description: Fraction of success criteria passing
    range: { min: 0.0, max: 1.0 }
    derived_from: "test results mapped to SCs"

  # --- Test Quality ---
  - name: line_coverage
    type: float
    description: Statement coverage from test suite
    range: { min: 0.0, max: 1.0 }
    derived_from: "coverage tool output (pytest-cov, istanbul)"

  - name: branch_coverage
    type: float
    description: Branch/decision coverage
    range: { min: 0.0, max: 1.0 }
    derived_from: "coverage tool output"

  - name: edge_case_coverage
    type: float
    description: Error paths and boundary conditions tested
    range: { min: 0.0, max: 1.0 }
    gap_question: "Are error paths and boundary conditions tested?"

  - name: test_to_code_ratio
    type: float
    description: Test lines divided by code lines
    range: { min: 0.0, max: 5.0 }
    derived_from: "line count analysis"

  # --- Security ---
  - name: critical_vulns
    type: integer
    description: Critical severity vulnerabilities
    range: { min: 0 }
    derived_from: "SAST/dependency scan"

  - name: high_vulns
    type: integer
    range: { min: 0 }
    derived_from: "SAST/dependency scan"

  - name: secrets_exposed
    type: boolean
    description: API keys, credentials, or tokens in code
    derived_from: "secret scanner (gitleaks, trufflehog)"

  # --- Code Quality ---
  - name: cyclomatic_complexity_avg
    type: float
    description: Average cyclomatic complexity per function
    range: { min: 1.0, max: 100.0 }
    derived_from: "radon, eslint complexity rule"

  - name: duplication_rate
    type: float
    description: Fraction of duplicated code blocks
    range: { min: 0.0, max: 1.0 }
    derived_from: "jscpd, pylint duplicate-code"

  - name: coupling_score
    type: float
    description: Cross-module dependency ratio
    range: { min: 0.0, max: 1.0 }
    derived_from: "import graph analysis"

  # --- Documentation ---
  - name: docstring_coverage
    type: float
    description: Fraction of public functions with docstrings
    range: { min: 0.0, max: 1.0 }
    derived_from: "interrogate, pydocstyle"

  - name: type_hint_coverage
    type: float
    description: Fraction of functions with type annotations
    range: { min: 0.0, max: 1.0 }
    derived_from: "mypy --stats, pyright"

  - name: has_changelog_entry
    type: boolean
    description: CHANGELOG updated for this change
    derived_from: "git diff on CHANGELOG"

  # --- Conventions ---
  - name: lint_violation_count
    type: integer
    description: Linter violations in changed files
    range: { min: 0 }
    derived_from: "flake8, eslint, ruff"

  - name: format_compliant
    type: boolean
    description: Code passes formatter check
    derived_from: "black --check, prettier --check"

  - name: naming_consistency
    type: float
    description: Fraction of identifiers matching project conventions
    range: { min: 0.0, max: 1.0 }
    derived_from: "AST analysis against naming rules"

constraints:
  - non-negativity
  - bounds
```

### Scaffolds (Pre-Built Weight Configurations)

```yaml
# scaffolds/startup-mvp.yml
name: startup-mvp
description: Ship fast with security basics. Low ceremony.
weights:
  spec_compliance: 1.0
  test_quality: 1.5
  security: 5.0
  code_quality: 0.5
  documentation: 0.2
  conventions: 0.2
thresholds:
  minimum_overall: 0.5
  minimum_security: 0.8
hard_blocks:
  - secrets_exposed
  - critical_vulns > 0

# scaffolds/healthcare.yml
name: healthcare
description: Regulated environment. Audit trail. Spec-driven.
weights:
  spec_compliance: 5.0
  test_quality: 3.0
  security: 5.0
  code_quality: 2.0
  documentation: 3.0
  conventions: 1.0
thresholds:
  minimum_overall: 0.8
  minimum_security: 0.95
  minimum_coverage: 0.85
  minimum_spec_compliance: 0.9
hard_blocks:
  - secrets_exposed
  - critical_vulns > 0
  - has_spec == false
  - has_changelog_entry == false
```

---

## 3. Architecture

### Variable Extractors

Pluggable extractors that populate variables from code analysis tools:

```python
class VariableExtractor(Protocol):
    name: str
    variables: list[str]  # which variables this extractor populates

    def extract(self, context: ReviewContext) -> dict[str, Any]:
        """Extract variable values from code analysis."""

class ReviewContext:
    repo_root: Path
    changed_files: list[Path]
    base_branch: str
    head_branch: str
    spec_path: Path | None
    coverage_report: Path | None
    lint_report: Path | None
```

Built-in extractors:
- `CoverageExtractor` — reads pytest-cov/istanbul output
- `LintExtractor` — runs ruff/eslint, counts violations
- `ComplexityExtractor` — runs radon/eslint complexity
- `SecurityExtractor` — runs gitleaks/bandit
- `SpecComplianceExtractor` — parses spec FRs against test names
- `DocumentationExtractor` — runs interrogate/pydocstyle
- `ConventionExtractor` — checks formatting, naming, imports
- `GitDiffExtractor` — changelog entry, lines added/removed

### Scorer

```python
def score_review(
    variables: dict[str, Any],
    scaffold: ReviewScaffold,
) -> ReviewScore:
    """Compute weighted composite score from extracted variables."""

@dataclass(frozen=True)
class ReviewScore:
    overall: float                      # weighted composite [0, 1]
    dimensions: dict[str, float]        # per-dimension scores
    hard_blocks: list[str]              # triggered hard blocks
    verdict: Literal["pass", "block", "revise"]
    recommendations: list[str]          # ordered improvement suggestions
```

### Persistence

```python
@dataclass(frozen=True)
class ReviewRecord:
    # Identity
    pr_id: str
    commit_sha: str
    branch: str
    timestamp: datetime
    author: str

    # Scores
    scaffold: str
    overall: float
    dimensions: dict[str, float]
    verdict: str
    hard_blocks: list[str]

    # Code metrics
    files_changed: int
    lines_added: int
    lines_removed: int

    # Conversus integration
    agent_count: int | None
    equilibrium_score: float | None
    convergence: str | None
    deliberation_output: str | None  # path to conversus output

class ReviewStore(Protocol):
    def append(self, record: ReviewRecord) -> None: ...
    def query(self, filters: dict) -> list[ReviewRecord]: ...
    def trend(self, dimension: str, window: int) -> float: ...
    def developer_profile(self, author: str) -> dict[str, float]: ...
    def health_score(self, window: int) -> float: ...
```

Storage backends:
- `JSONLReviewStore` — append-only JSONL file (local, zero deps)
- `SupabaseReviewStore` — PostgreSQL via Supabase (web interface)
- `SQLiteReviewStore` — local database (middle ground)

### API Layer

```
POST /api/review              — submit a review (extract + score)
GET  /api/review/:pr_id       — get review results
GET  /api/health              — project health score + trends
GET  /api/trends/:dimension   — dimension trend over time
GET  /api/developers/:author  — developer profile
GET  /api/debt                — technical debt alerts
POST /api/review/:pr_id/gate  — run conversus gate on the review
```

---

## 4. Functional Requirements

### Extraction
- **FR-001**: The plugin MUST extract variables from standard tool output (pytest-cov XML, eslint JSON, ruff JSON, radon JSON).
- **FR-002**: Extractors MUST be pluggable — users can add custom extractors.
- **FR-003**: Missing tool output MUST default variables to `None` (not zero), with a warning.

### Scoring
- **FR-004**: The scorer MUST compute a weighted composite from a scaffold YAML file.
- **FR-005**: Hard blocks MUST override the composite score — any hard block = BLOCK verdict.
- **FR-006**: Recommendations MUST be ordered by impact: the change that would most improve the overall score listed first.

### Scaffolds
- **FR-007**: At least 5 pre-built scaffolds MUST be provided (startup, enterprise, open-source, healthcare, api-service).
- **FR-008**: Users MUST be able to create custom scaffolds by copying and modifying a pre-built one.
- **FR-009**: Scaffolds MUST validate against a Pydantic model.

### Persistence
- **FR-010**: Review records MUST be append-only (no deletion or mutation).
- **FR-011**: Trend analysis MUST use linear regression over a configurable window.
- **FR-012**: Developer profiles MUST aggregate scores by dimension across all reviews by that author.
- **FR-013**: Technical debt alerts MUST fire when a dimension's trend crosses a configured threshold.

### Conversus Integration
- **FR-014**: The plugin MUST support running a conversus gate (spec 011) using the review scores as context.
- **FR-015**: Gate agents MUST receive the extracted variables and scaffold as input.
- **FR-016**: The equilibrium scorer MUST run POST_DELIBERATION on gate output.

### API
- **FR-017**: The API MUST be a FastAPI application (reuse web infrastructure from M005).
- **FR-018**: API endpoints MUST be optional — the plugin works standalone without the API server.
- **FR-019**: The API MUST support both JSONL and Supabase backends via configuration.

---

## 5. Success Criteria

- **SC-001**: Given a PR with 90% test coverage, no vulnerabilities, and all FRs met, the healthcare scaffold scores > 0.85.
- **SC-002**: Given a PR with an exposed API key, all scaffolds return BLOCK regardless of other scores.
- **SC-003**: After 10 reviews, the trend API correctly identifies that `duplication_rate` is increasing.
- **SC-004**: A conversus gate with 3 review agents produces a synthesis that references specific extracted variable values.
- **SC-005**: The full pipeline (extract → score → persist → gate → equilibrium) runs in under 60 seconds.

---

## 6. Constraints

- The plugin MUST work without any code analysis tools installed (all variables default to None).
- The plugin MUST NOT execute code or run tests — it reads tool output files.
- The API server is optional — core scoring works as a library.
- Scaffolds are YAML — no code execution in scaffold files.
