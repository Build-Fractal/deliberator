# Building Domain Plugins

Domain plugins turn review into a quantifiable optimization problem. They follow a 5-stage lifecycle: extract, score, persist, gate, serve.

## Setup

```bash
git clone https://github.com/anthropic/deliberator.git
cd deliberator
uv sync
```

## End-to-end tutorial: building a domain from scratch

This walkthrough builds a "commit quality" domain through all 5 lifecycle stages.

### Stage 1: Extract -- collect variables from the workspace

Extractors implement the `VariableExtractor` protocol and pull raw data from a `DomainContext`. The context provides `workspace` (a `Path`), `changed_files` (typed as `list[Path]`), and `metadata` (an arbitrary dict).

```python
from pathlib import Path
from typing import Any
from deliberator.domains.base import DomainContext

class CommitMessageExtractor:
    name = "commit-message"
    variables = ["has_type_prefix", "body_length", "references_issue"]

    def extract(self, context: DomainContext) -> dict[str, Any]:
        msg = context.metadata.get("commit_message", "")
        lines = msg.strip().splitlines()
        first_line = lines[0] if lines else ""
        return {
            "has_type_prefix": bool(
                any(first_line.startswith(p) for p in ["feat:", "fix:", "chore:", "docs:"])
            ),
            "body_length": len("\n".join(lines[1:])),
            "references_issue": "#" in msg,
        }
```

### Stage 2: Score -- evaluate variables against a scaffold

Wire the extractor into a `DomainPlugin` subclass and point `scaffold_dir` at your YAML configs:

```python
from deliberator.domains.base import DomainPlugin, VariableExtractor

class CommitQualityDomain(DomainPlugin):
    name = "commit-quality"
    version = "1.0.0"
    scaffold_dir = Path(__file__).parent / "scaffolds"

    def get_extractors(self) -> list[VariableExtractor]:
        return [CommitMessageExtractor()]
```

Create `scaffolds/default.yml`:

```yaml
name: default
description: Standard commit quality checks.
weights:
  has_type_prefix: 3.0
  body_length: 1.0
  references_issue: 2.0
thresholds:
  minimum_overall: 0.5
hard_blocks: []
```

Run extraction and scoring:

```python
context = DomainContext(
    workspace=Path("."),
    changed_files=[Path("main.py")],
    metadata={"commit_message": "feat: add login endpoint\n\nCloses #42"},
)
domain = CommitQualityDomain()
variables = domain.extract(context)
score = domain.score(variables, "default")
# score.verdict -> "pass", "block", or "revise"
```

### Stage 3: Persist -- store the review record

Use `create_record()` to build a `DomainRecord`, then persist it via a store backend:

```python
from deliberator.domains.store import JSONLStore

store = JSONLStore(Path("./reviews"))
record = domain.create_record(score, context)
record_id = store.append(record)
```

### Stage 4: Gate -- use the verdict to gate CI

The `score.verdict` value drives decisions. In a CI pipeline:

```python
if score.verdict == "block":
    sys.exit(1)  # Hard-fail the pipeline
elif score.verdict == "revise":
    print("Revisions recommended:", score.recommendations)
```

`score.hard_blocks` lists which blocking conditions triggered. `score.recommendations` lists improvement advice ordered by impact.

### Stage 5: Serve -- expose via REST API

Mount REST endpoints using the router factory:

```python
from fastapi import FastAPI
from deliberator.domains.api import create_domain_router

app = FastAPI()
router = create_domain_router(domain, store)
app.include_router(router, prefix="/api")
# Creates: POST /api/commit-quality/submit, GET /api/commit-quality/health, etc.
```

---

## DomainPlugin ABC

Every domain extends `deliberator.domains.base.DomainPlugin`:

```python
from pathlib import Path
from deliberator.domains.base import (
    DomainPlugin,
    VariableExtractor,
    DomainContext,
    DomainScore,
    Scaffold,
)

class MyDomain(DomainPlugin):
    name = "my-domain"
    version = "1.0.0"
    scaffold_dir = Path(__file__).parent / "scaffolds"

    def get_extractors(self) -> list[VariableExtractor]:
        return [MyExtractor()]
```

**Required attributes:**
- `name`: Domain identifier (used in storage keys, API routes).
- `version`: Semver string.
- `scaffold_dir`: Path to directory containing scaffold YAML/JSON files.

**Required method:**
- `get_extractors()`: Return the list of variable extractors.

## VariableExtractor protocol

Extractors are the data collection layer. Each produces a subset of variables:

```python
from deliberator.domains.base import DomainContext, VariableExtractor

class CoverageExtractor:
    name = "coverage"
    variables = ["line_coverage", "branch_coverage"]

    def extract(self, context: DomainContext) -> dict[str, Any]:
        # Read coverage data from context.workspace
        coverage_file = context.workspace / "coverage.json"
        if not coverage_file.exists():
            return {}

        data = json.loads(coverage_file.read_text())
        return {
            "line_coverage": data.get("totals", {}).get("percent_covered", 0) / 100,
            "branch_coverage": data.get("totals", {}).get("branch_rate", 0),
        }
```

**Protocol requirements:**
- `name`: String identifier.
- `variables`: List of variable names this extractor produces.
- `extract(context) -> dict[str, Any]`: Return variable name to value mapping.

`DomainContext` provides:
- `workspace`: Path to the project root.
- `changed_files`: List of changed file paths.
- `metadata`: Arbitrary dict for domain-specific context.

## Scaffolds: YAML weight configs

Scaffolds define how variables are scored. Put them in your `scaffold_dir`:

```yaml
# scaffolds/startup-mvp.yml
name: startup-mvp
description: Ship fast with security basics.
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
```

**Fields:**
- `weights`: Dimension name to relative importance. Higher = more impact on overall score.
- `thresholds`: Dimension name to minimum acceptable score. Below triggers "revise" verdict.
- `hard_blocks`: Rules that force a "block" verdict. Supports: bare truthy checks (`secrets_exposed`), comparisons (`critical_vulns > 0`), boolean equality (`has_spec == false`).

Multiple scaffolds per domain are encouraged -- different projects have different quality bars.

## Scoring pipeline

The base class `DomainPlugin.score()` handles the generic pipeline. Override hooks to customize:

```python
class MyDomain(DomainPlugin):
    # ...

    def get_dimension_variables(self) -> dict[str, list[str]]:
        """Map weight keys to their constituent variables."""
        return {
            "security": ["critical_vulns", "high_vulns", "secrets_exposed"],
            "quality": ["lint_count", "complexity_avg"],
        }

    def normalize_variable(self, name: str, value: Any) -> float | None:
        """Convert raw values to [0, 1]. None if not normalizable."""
        if name in ("critical_vulns", "lint_count"):
            return 1.0 / (1.0 + int(value))  # Fewer is better
        return max(0.0, min(1.0, float(value)))

    def score_dimension(self, dimension: str, variables: dict) -> float | None:
        """Score one dimension. Default: average of normalized variables."""
        # Custom logic here, or call super()
        return super().score_dimension(dimension, variables)

    def build_recommendations(self, dimension_scores, weights, thresholds, variables):
        """Generate ordered improvement advice. Default: by impact (weight * gap)."""
        return super().build_recommendations(dimension_scores, weights, thresholds, variables)
```

If `get_dimension_variables()` returns empty (default), scoring maps weight keys directly to variable values (1:1 mode).

### Verdict determination

#### Default behavior

The base class `determine_verdict()` applies a simple three-tier rule:

1. If any hard block is triggered: return `"block"`.
2. If any dimension score is below its scaffold threshold: return `"revise"`.
3. Otherwise: return `"pass"`.

The method signature is:

```python
def determine_verdict(
    self,
    overall: float,
    hard_blocks: list[str],
    thresholds: dict[str, float],
    dimensions: dict[str, float],
    variables: dict[str, Any],
) -> Literal["pass", "block", "revise"]:
```

Note that the default implementation does not use `overall` or `variables` -- it only checks `hard_blocks` and per-dimension `thresholds`. This means the base behavior ignores composite score entirely.

#### Custom verdict logic

Override `determine_verdict()` to add domain-specific rules. A common pattern is checking `minimum_overall` from the scaffold thresholds:

```python
def determine_verdict(self, overall, hard_blocks, thresholds, dimensions, variables):
    if hard_blocks:
        return "block"
    # Check composite score against an overall minimum
    min_overall = thresholds.get("minimum_overall", 0.7)
    if overall < min_overall:
        return "revise"
    # Check individual dimension thresholds
    for dim, threshold in thresholds.items():
        if dim.startswith("minimum_"):
            continue  # Skip meta-thresholds
        if dimensions.get(dim, 0.0) < threshold:
            return "revise"
    return "pass"
```

You can also use `variables` for domain-specific logic (e.g., always block if a certain variable is present regardless of score):

```python
def determine_verdict(self, overall, hard_blocks, thresholds, dimensions, variables):
    if hard_blocks:
        return "block"
    if variables.get("license_violation"):
        return "block"
    if overall < thresholds.get("minimum_overall", 0.6):
        return "revise"
    return "pass"
```

### Hard block evaluation

The framework provides two levels of hard block evaluation with different capabilities.

#### `_check_hard_blocks` (module-level function)

Evaluates conditions of the form `"variable_name <op> threshold"` where the condition string must have exactly three whitespace-separated tokens. Supported operators: `<`, `>`, `<=`, `>=`, `==`. This function only handles numeric comparisons -- it skips conditions it cannot parse.

```python
from deliberator.domains.base import _check_hard_blocks

triggered = _check_hard_blocks(
    variables={"critical_vulns": 3, "coverage": 0.4},
    hard_block_conditions=["critical_vulns > 0", "coverage < 0.5"],
)
# triggered -> ["critical_vulns > 0", "coverage < 0.5"]
```

#### `evaluate_hard_blocks` (DomainPlugin method)

The instance method on `DomainPlugin` delegates to `_evaluate_hard_block_rules`, which supports a richer rule syntax:

- **Bare variable name** (truthy check): `"secrets_exposed"` -- triggers if the variable is truthy (bool True, number > 0, or truthy value).
- **Numeric comparison**: `"critical_vulns > 0"` -- standard numeric operators (`<`, `>`, `<=`, `>=`, `==`, `!=`).
- **Boolean equality**: `"has_spec == false"` -- compares against `true`/`false` literals.

This is the method called by `DomainPlugin.score()` during the scoring pipeline. Override it to add custom block evaluation logic:

```python
def evaluate_hard_blocks(self, rules, variables):
    # Add domain-specific checks before the standard evaluation
    triggered = super().evaluate_hard_blocks(rules, variables)
    if variables.get("unsigned_commits"):
        triggered.append("unsigned_commits (policy violation)")
    return triggered
```

## DomainStore: JSONL vs SQLite

Two storage backends implement the `DomainStore` protocol:

```python
from deliberator.domains.store import JSONLStore, SQLiteStore

# JSONL: one file per domain, append-only. Good for < 10K records.
store = JSONLStore(Path("./reviews"))

# SQLite: single DB file, SQL queries. Good for larger datasets.
store = SQLiteStore(Path("./reviews.db"))
```

**DomainStore protocol:**

| Method | Purpose |
|--------|---------|
| `append(record)` | Persist a record, return its ID |
| `get(record_id)` | Retrieve by UUID |
| `query(domain, filters, limit)` | Query with optional verdict/score filters |
| `trend(domain, field, window)` | Linear regression over recent records |
| `aggregate(domain, group_by, field)` | Group-by averages |

## API router factory

Mount REST endpoints for any domain:

```python
from fastapi import FastAPI
from deliberator.domains.api import create_domain_router
from deliberator.domains.store import JSONLStore

app = FastAPI()
domain = MyDomain()
store = JSONLStore(Path("./reviews"))

router = create_domain_router(domain, store)
app.include_router(router, prefix="/api")
```

This creates:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/{domain.name}/submit` | POST | Extract + score + persist |
| `/{domain.name}/record/{id}` | GET | Get a record |
| `/{domain.name}/health` | GET | Aggregate recent scores |
| `/{domain.name}/trends/{field}` | GET | Trend analysis |
| `/{domain.name}/scaffolds` | GET | List available scaffolds |

## Example: Build a "commit quality" domain

```python
from pathlib import Path
from typing import Any
from deliberator.domains.base import DomainPlugin, DomainContext, VariableExtractor

class CommitMessageExtractor:
    name = "commit-message"
    variables = ["has_type_prefix", "body_length", "references_issue"]

    def extract(self, context: DomainContext) -> dict[str, Any]:
        msg = context.metadata.get("commit_message", "")
        lines = msg.strip().splitlines()
        first_line = lines[0] if lines else ""
        return {
            "has_type_prefix": bool(
                any(first_line.startswith(p) for p in ["feat:", "fix:", "chore:", "docs:"])
            ),
            "body_length": len("\n".join(lines[1:])),
            "references_issue": "#" in msg,
        }


class CommitQualityDomain(DomainPlugin):
    name = "commit-quality"
    version = "1.0.0"
    scaffold_dir = Path(__file__).parent / "scaffolds"

    def get_extractors(self) -> list[VariableExtractor]:
        return [CommitMessageExtractor()]
```

Scaffold (`scaffolds/default.yml`):
```yaml
name: default
description: Standard commit quality checks.
weights:
  has_type_prefix: 3.0
  body_length: 1.0
  references_issue: 2.0
thresholds:
  minimum_overall: 0.5
hard_blocks: []
```
