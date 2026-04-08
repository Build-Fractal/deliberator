# Feature Specification: Domain Plugin Architecture

**Feature ID**: `030-domain-plugin-architecture`
**Created**: 2026-03-31
**Status**: Draft
**Depends On**: `016-plugin-system` (plugin framework), `029-code-review-domain` (first implementation, proves the pattern)
**Origin**: Vision — conversus as a general-purpose engine that turns real-world problems into optimization problems with deterministic harnesses around indeterminate AI processes

---

## 1. Vision

Conversus is an engine that:

1. **Takes a real-world problem** (code review, negotiation, hiring, resource allocation)
2. **Formulates it as an optimization problem** (objective function + constraints + game form)
3. **Wraps indeterminate AI processes in a deterministic harness** (multi-agent deliberation with convergence guarantees)
4. **Forces convergence to an understandable, predictable goal** (equilibrium scoring + convergence prediction)
5. **Exposes the results as an API** for frontends and backend services to consume

A **domain plugin** is a vertical application that implements steps 1-5 for a specific problem domain. The domain plugin architecture standardizes how these verticals are built, so every domain gets: variable extraction, objective scoring, persistence, API endpoints, and conversus integration — without rebuilding the infrastructure each time.

---

## 2. Domain Plugin Contract

Every domain plugin implements the same interface:

```python
from conversus.domains import DomainPlugin, DomainContext, DomainScore, DomainRecord

class CodeReviewDomain(DomainPlugin):
    name = "code-review"
    version = "1.0.0"

    # --- Schema ---
    objective_template = "code-review-quality"  # from template library
    scaffold_dir = "scaffolds/code-review/"     # pre-built weight configs

    # --- Extraction ---
    extractors = [
        CoverageExtractor(),
        LintExtractor(),
        SecurityExtractor(),
        SpecComplianceExtractor(),
    ]

    # --- Persistence ---
    record_type = ReviewRecord                  # frozen Pydantic model
    store_type = "jsonl"                        # jsonl | sqlite | supabase

    # --- API ---
    router = code_review_router                 # FastAPI APIRouter

    # --- Conversus ---
    gate_config = "gate-configs/code-review.yml"  # conversus gate definition
    validation_agents = [                       # auto-generated for solver validation
        "correctness-auditor",
        "security-reviewer",
        "maintainability-advocate",
    ]
```

### The DomainPlugin ABC

```python
class DomainPlugin(ABC):
    """Base class for domain plugins.

    A domain plugin turns a real-world problem domain into a quantifiable
    optimization problem on top of the conversus engine.

    The lifecycle:
    1. extract()  — pull variables from domain-specific sources
    2. score()    — compute weighted composite via scaffold
    3. persist()  — append to domain-specific store
    4. gate()     — optionally run conversus deliberation
    5. serve()    — expose API endpoints
    """

    name: str
    version: str

    @abstractmethod
    def extract(self, context: DomainContext) -> dict[str, Any]:
        """Extract domain variables from context."""

    @abstractmethod
    def score(self, variables: dict[str, Any], scaffold: str) -> DomainScore:
        """Score the extracted variables using a named scaffold."""

    def persist(self, record: DomainRecord, store: DomainStore) -> None:
        """Append a record to the domain store. Default: delegate to store."""
        store.append(record)

    def gate(self, score: DomainScore, context: DomainContext) -> GateResult | None:
        """Optionally run a conversus gate. Default: skip."""
        return None

    def get_router(self) -> APIRouter | None:
        """Return a FastAPI router for domain-specific endpoints. Default: None."""
        return None
```

---

## 3. The Deterministic Harness

This is the core architectural insight. AI processes (LLM calls) are indeterminate — same input can produce different output. Conversus wraps them in a deterministic harness:

```
INDETERMINATE (AI)              DETERMINISTIC (harness)
─────────────────               ───────────────────────
Agent writes review      →      Template constrains structure
Agent cross-reviews      →      Phase barrier enforces ordering
Agent revises position   →      Disposition labels (Withdrawn/Modified/Surviving)
Synthesis weighs positions →    Structural markers (DISPUTES_BEGIN/END)
                                Equilibrium scorer quantifies stability
                                Convergence predictor estimates remaining rounds
                                Stagnation detector forces termination
```

**What makes it deterministic:**
- Same config → same number of agents, same phase sequence, same template structure
- Disposition labels are a closed set — withdrawn, modified, surviving — no ambiguity
- Dispute count is integer — parseable, comparable, trend-analysable
- Equilibrium score is float [0,1] — comparable across runs
- Convergence prediction is enum — CONVERGE, STAGNATE, UNCERTAIN
- Quality gates are boolean — PASS or BLOCK

**What remains indeterminate:**
- Agent opinions (different LLM calls produce different reviews)
- The specific recommendations each agent makes
- Whether agents concede or defend positions

**The harness guarantees:**
- Convergence (stagnation detection terminates non-converging runs)
- Stability measurement (equilibrium score quantifies how stable the outcome is)
- Reproducible structure (same template → same output sections → same parse paths)
- Audit trail (every agent's position is written to disk, every phase is traceable)

For domain plugins, this means:
- **Variable extraction is deterministic** — same code → same coverage number
- **Scoring is deterministic** — same variables + same scaffold → same score
- **The conversus gate is the indeterminate part** — but it's harnessed by the engine
- **The equilibrium score tells you how much to trust the indeterminate part**

---

## 4. Data Layer & API Architecture

### Domain Store Protocol

```python
class DomainStore(Protocol):
    """Storage backend for domain records."""

    def append(self, record: DomainRecord) -> str:
        """Append a record, return its ID."""

    def get(self, record_id: str) -> DomainRecord | None:
        """Retrieve by ID."""

    def query(self, filters: dict, limit: int = 100) -> list[DomainRecord]:
        """Query with filters."""

    def trend(self, field: str, window: int = 10) -> TrendResult:
        """Compute trend over recent records."""

    def aggregate(self, group_by: str, field: str) -> dict[str, float]:
        """Aggregate a field grouped by another field."""
```

Backends:
- `JSONLStore` — file-based, zero deps, good for CLI
- `SQLiteStore` — local database, good for single-machine deployments
- `SupabaseStore` — PostgreSQL, good for web/team deployments
- `APIStore` — delegates to a remote conversus API server

### API Server

A FastAPI application that serves multiple domain plugins:

```python
app = FastAPI(title="Conversus Domain API")

# Each domain plugin mounts its router
for domain in load_domain_plugins():
    if router := domain.get_router():
        app.include_router(router, prefix=f"/api/{domain.name}")

# Shared endpoints
app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth")
```

Each domain gets:
```
/api/{domain}/submit         — submit a new item for scoring
/api/{domain}/{id}           — get scoring results
/api/{domain}/health         — domain health metrics
/api/{domain}/trends/{field} — field trend over time
/api/{domain}/gate/{id}      — run conversus gate
/api/{domain}/scaffolds      — list available scaffolds
```

### Frontend Contract

The API is designed for frontends to consume:

```typescript
// Frontend interface (framework-agnostic)
interface DomainAPI {
  submit(context: DomainContext): Promise<DomainScore>;
  getScore(id: string): Promise<DomainScore>;
  getHealth(): Promise<HealthMetrics>;
  getTrend(field: string, window?: number): Promise<TrendData>;
  runGate(id: string): Promise<GateResult>;
  listScaffolds(): Promise<Scaffold[]>;
}
```

---

## 5. Domain Plugin Registry

Domains are discovered and loaded like conversus plugins:

```yaml
# conversus.yml or domains.yml
domains:
  - name: code-review
    package: conversus-code-review
    store: jsonl
    store_path: .conversus/reviews/
    scaffold: healthcare
    config:
      coverage_tool: pytest-cov
      lint_tool: ruff

  - name: negotiation
    package: conversus-negotiation
    store: supabase
    scaffold: default
    config:
      parties: 2
```

### Planned Domain Plugins

| Domain | Package | Objective | Modes |
|--------|---------|-----------|-------|
| Code review | `conversus-code-review` | Maximize code quality within velocity constraints | cooperative, red-blue |
| Negotiation | `conversus-negotiation` | Maximize ZOPA coverage with stability | negotiation, prisoners-dilemma |
| Hiring | `conversus-hiring` | Maximize candidate-role fit across multiple criteria | winner-take-all, cooperative |
| Resource allocation | `conversus-allocation` | Maximize utilization with fairness constraints | resource-allocation, fair-division |
| Architecture review | `conversus-architecture` | Minimize coupling, maximize cohesion, security | cooperative, red-blue |
| Compliance audit | `conversus-compliance` | Maximize regulatory requirement coverage | cooperative |
| Vendor selection | `conversus-vendor` | Maximize value within budget + risk constraints | winner-take-all |
| Sprint planning | `conversus-planning` | Maximize delivered value within capacity | scheduling, resource-allocation |

---

## 6. Functional Requirements

### Domain Plugin Infrastructure
- **FR-001**: `DomainPlugin` ABC MUST define the extract → score → persist → gate → serve lifecycle.
- **FR-002**: Domain plugins MUST be loadable via `importlib` (same pattern as conversus plugins, spec 016).
- **FR-003**: Missing domain packages MUST warn and skip, not crash.
- **FR-004**: Each domain MUST define its own `DomainRecord` model (frozen Pydantic).

### Data Layer
- **FR-005**: `DomainStore` MUST be a protocol with append, get, query, trend, aggregate methods.
- **FR-006**: At least 3 backends MUST be implemented: JSONL, SQLite, Supabase.
- **FR-007**: Backend selection MUST be via configuration, not code changes.
- **FR-008**: All backends MUST enforce append-only semantics for audit trail.

### API
- **FR-009**: The API server MUST mount domain routers dynamically based on installed plugins.
- **FR-010**: Each domain MUST get a standard set of endpoints (submit, get, health, trends, gate, scaffolds).
- **FR-011**: The API MUST support authentication (API key or OAuth) for team deployments.
- **FR-012**: The API MUST support CORS configuration for frontend access.

### Deterministic Harness Integration
- **FR-013**: Variable extraction MUST be deterministic — same inputs produce same variables.
- **FR-014**: Scoring MUST be deterministic — same variables + scaffold produce same score.
- **FR-015**: The conversus gate is the only indeterminate component, and its output MUST include an equilibrium score.
- **FR-016**: The equilibrium score MUST be persisted alongside the domain score for trust calibration.

### Scaffold System
- **FR-017**: Each domain MUST ship with at least 3 pre-built scaffolds.
- **FR-018**: Scaffolds MUST be YAML files (no code execution).
- **FR-019**: Users MUST be able to create, share, and version custom scaffolds.

---

## 7. Success Criteria

- **SC-001**: The code-review domain plugin (spec 029) is implementable as a `DomainPlugin` subclass with zero infrastructure code.
- **SC-002**: Two domain plugins can run simultaneously on the same API server with isolated stores.
- **SC-003**: Switching from JSONL to Supabase backend requires only a config change, no code.
- **SC-004**: A frontend consuming the API can render a project health dashboard from the `/trends` and `/health` endpoints.
- **SC-005**: The full pipeline (extract → score → persist → gate → equilibrium → API response) completes in under 90 seconds.

---

## 8. Constraints

- Domain plugins MUST NOT depend on each other. Each is independently installable.
- The core `conversus` package MUST NOT depend on any domain plugin.
- The API server is optional — domains work as libraries without it.
- Scaffolds are data, not code — no arbitrary code execution from scaffold files.
- The deterministic harness is the value proposition — don't compromise it for convenience.

---

## 9. The Pitch

> **Conversus turns real-world problems into optimization problems.**
>
> You describe a decision. We formulate it as a mathematical game. We run multiple AI agents through a deterministic deliberation process — cross-reviewing, revising, disputing. A Nash equilibrium scorer tells you if the outcome is stable. A convergence predictor tells you if more deliberation would help.
>
> The AI is indeterminate. The harness is not. You get reproducible structure, measurable quality, and an audit trail — wrapped around the creativity and perspective-taking that AI provides.
>
> Build a domain plugin for your problem space. Get an API, a persistence layer, trend analysis, and conversus integration — for free. Ship a vertical product in days, not months.
