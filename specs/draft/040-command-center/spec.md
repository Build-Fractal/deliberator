# Feature Specification: Command Center

**Feature ID**: `040-command-center`
**Created**: 2026-04-02
**Status**: Draft — initial vision for refinement
**Depends On**: `030-domain-plugin-architecture` (domain plugin lifecycle), `014-guided-objective-construction` (construction pipeline + GapFiller), `020-scenario-storage` (persistent game state), `032-package-splitting` (clean package boundaries), `016-plugin-system` (plugin output for quality indicators)
**Infrastructure**: All AWS. No Supabase. The `web/` and `frontend/` directories on some branches are adoption-harness prototypes, not the starting point for this spec.
**Origin**: Vision — conversus as a non-technical command center where any team member can browse, query, and change project decisions through voice or text, with Conversus acting as co-pilot.

---

## 1. Vision

The conversus engine is mature: 8 game-theoretic modes, 38 objective function templates, adversarial cross-review, domain plugins, a construction pipeline that turns natural language into parameterized objective functions with interactive gap-filling. But every interface today assumes a technical user — CLI, YAML configs, Python SDK, or a minimal web launcher.

The Command Center is the **product layer** on top of the engine layer. It turns conversus from a developer tool into a team collaboration platform where:

1. **Anyone can see everything** — all project decisions, goals, features, brand voice, specs, and test coverage, browsable and searchable in plain language
2. **Anyone can ask questions** — voice or text queries against the project knowledge graph, answered in context
3. **Anyone can submit changes** — report an issue, request a feature, propose a change via voice or text
4. **Conversus acts as co-pilot** — it understands what the change affects, builds a plan, and only involves the user where their input matters
5. **It works on mobile** — chat-first interface with push notifications when Conversus needs a decision

This is the product surface for the Hosted API and Enterprise tiers defined in spec 033.

---

## 2. What Already Exists (Foundation)

The following existing systems are **direct building blocks**, not things that need to be rebuilt:

### Construction Pipeline (spec 014) → Change Request Engine

The 3-stage pipeline already does:
- Stage 1: Classify natural language into decision type (SELECTION, INTEGRATION, SCOPING, STRESS_TEST, NEGOTIATION, RESOURCE_ALLOCATION, FAIR_DIVISION, MECHANISM_DESIGN)
- Stage 2: Interactive gap-filling via `GapFiller` protocol with plain-English `gap_question` fields on every parameter
- Stage 3: Deterministic assembly of parameterized objective function

**What this means for Command Center**: When a user says "I want to add dark mode," Stage 1 classifies it, Stage 2 asks them clarifying questions ("How important is visual consistency vs development speed?"), and Stage 3 produces a formal objective. The pipeline IS the change request engine. We build a `WebGapFiller` implementation that renders gap questions in the UI.

### Domain Plugin System (specs 029-030) → Project Knowledge Index

The domain lifecycle (extract → score → persist → gate → serve) is generic:
- `VariableExtractor` protocol pulls typed data from a workspace
- Scaffolds define weighted scoring dimensions with hard blocks and thresholds
- `DomainStore` (JSONL/SQLite) supports query, trend, aggregate
- `create_domain_router()` auto-generates REST endpoints for any domain

**What this means for Command Center**: Each category of project knowledge (brand, goals, features, specs, tests) becomes a domain. New extractors, new scaffolds, same infrastructure. Every domain auto-generates its own queryable API. The dashboard consumes these APIs.

### Guided Workflow (specs 007-011) → Change Request Flow

`/conversus define → interests → mode → converge → arbitrate → gate` already walks from "I have a problem" to "here's the deliberated outcome with quality gates."

**What this means for Command Center**: The same flow, wrapped in a visual UI with voice input instead of slash commands. The workflow handlers already exist — we surface them through a different interface.

### Scenario Storage (spec 020) → Persistent Project State

Stored scenarios capture game structure (mode, objective, parameters, agent roles), data bindings (swappable per run), and run history (outcomes, scores, rounds used).

**What this means for Command Center**: Cross-run analysis ("how consistent are outcomes?", "did preferences drift?", "which decisions stagnate?") becomes dashboard content. Project health trends come from scenario history.

### Plugin Output → Dashboard Quality Layer

Plugins produce structured data at lifecycle hooks — equilibrium scores, convergence predictions, config recommendations — as machine-readable JSON with display fields (headline, body, recommendation, severity).

**What this means for Command Center**: Quality indicators and trend charts render directly from plugin output.

### Starting from Scratch (No Existing Web UI)

The `web/` and `frontend/` code on the adoption-harness branch is a prototype tied to Supabase. The Command Center starts fresh on an all-AWS stack. This is an advantage — no legacy to work around, clean architecture from day one. The engine's Python interfaces (SDK, construction pipeline, domain plugin lifecycle) are the integration points, not any existing web layer.

---

## 3. Architecture

### Layer Diagram

```
┌──────────────────────────────────────────────────────────────┐
│  INTERACTION LAYER (new)                                     │
│  Voice I/O · Chat UI · Mobile PWA · Push Notifications       │
├──────────────────────────────────────────────────────────────┤
│  DASHBOARD LAYER (new)                                       │
│  Artifact Browser · Search/Filter · Status Views · Trends    │
│  Impact Visualization · Change Request Submission            │
├──────────────────────────────────────────────────────────────┤
│  CO-PILOT LAYER (new protocol adapter)                       │
│  WebGapFiller · Impact Analysis · Selective User Involvement │
│  Multiple-Choice Rendering · Progress Tracking               │
├──────────────────────────────────────────────────────────────┤
│  PROJECT GRAPH LAYER (new domain + Memgraph)                 │
│  ProjectDomain · Artifact Extractors · Cypher Queries        │
│  MemgraphStore · Triggers → SSE · Full-Text + Semantic Search│
├──────────────────────────────────────────────────────────────┤
│  DATA LAYER                                                  │
│  Memgraph (graph)  ·  RDS Postgres / pgvector (vector search) │
├──────────────────────────────────────────────────────────────┤
│  EXISTING ENGINE LAYER (unchanged)                           │
│  Construction Pipeline · Domain Plugins · Scenario Storage   │
│  Plugin System · Guided Workflow · Deliberation Engine       │
└──────────────────────────────────────────────────────────────┘
```

**Coupling rule**: The Command Center layers import from `conversus.domains`, `conversus.schemas`, and REST APIs. They MUST NOT import from `engine.*` directly. The engine remains unchanged.

**Data flow**: Extractors write to Memgraph (graph structure + relationships) and optionally to RDS Postgres/pgvector (embeddings for semantic search). The dashboard reads from both via the domain REST API. Memgraph triggers push real-time updates through the backend via SSE.

### Package Placement

Following spec 032's package map:

| New Package | Contents | Dependencies |
|-------------|----------|-------------|
| `conversus-graph` | ProjectDomain, artifact extractors, MemgraphStore, Cypher queries | conversus-domains, conversus-schemas, gqlalchemy (Memgraph driver) |
| `conversus-dashboard` | Next.js frontend, dashboard API routes, WebGapFiller | conversus-graph REST API, conversus engine REST API |

---

## 4. User Stories

### US-1 — Browse Project State (Priority: P1)

A product manager opens the Command Center and sees a high-level dashboard of the project: categories like Brand, Goals, Features, Specs, Tests, and Decisions. Each category shows a count, a health indicator (from domain scoring), and recent activity. They click into Features and see a filterable list of all features with status (proposed, in-progress, decided, shipped), relationships (which goals each feature serves, which specs define it, which tests cover it), and the latest deliberation outcome for each.

**Why this priority**: Without browsability, everything else is useless. This is the "see everything" foundation.

**Independent Test**: A project with 10+ indexed artifacts renders a navigable dashboard with working search and category filters.

**Acceptance Scenarios**:

1. **Given** a project with indexed artifacts across 3+ categories, **When** the user opens the Command Center, **Then** they see a dashboard with category cards showing counts, health scores, and recent activity.
2. **Given** the Features category contains 15 features, **When** the user clicks into Features and types "auth" in the search box, **Then** only features matching "auth" appear, with status badges and relationship links.
3. **Given** a feature has relationships to 2 goals, 1 spec, and 3 tests, **When** the user clicks that feature, **Then** the detail view shows all relationships with clickable navigation to each related artifact.

---

### US-2 — Submit a Change Request (Priority: P1)

A team member types or speaks: "We need to add support for dark mode across the app." The Command Center classifies this as a change request, runs it through the construction pipeline (Stage 1: classify decision type, select templates, extract parameters, identify gaps), and presents a summary: "I've classified this as an INTEGRATION decision. Before I can plan this, I need to understand a few things." It then renders the gap questions from the matched objective template as multiple-choice cards or text inputs. The user answers. The system assembles the objective function and kicks off a deliberation.

**Why this priority**: This is the core value — non-technical users can submit changes that trigger the full conversus pipeline.

**Independent Test**: A user submits a natural-language change request, answers 2-3 gap questions via the UI, and a deliberation starts.

**Acceptance Scenarios**:

1. **Given** the user types a change request in the input box, **When** they submit it, **Then** the system classifies the decision type and shows a summary with identified gaps.
2. **Given** the system has identified 3 parameter gaps, **When** it presents gap questions, **Then** each question renders with the `gap_question` text contextualized to the user's input, with appropriate input controls (slider for numeric ranges, radio for enums, text for open-ended).
3. **Given** the user has answered all gap questions, **When** the system assembles the objective, **Then** it shows a plain-language summary of what will be deliberated and a cost estimate before starting.

---

### US-3 — Co-Pilot Interaction (Priority: P2)

After submitting a change request, the user enters "co-pilot mode." Conversus runs the deliberation in the background. The user receives updates only when their input is needed — for example, when agents disagree on an approach and the user's preference would break the tie, or when the change has an impact the user didn't anticipate ("This would affect the auth flow — is that okay?"). Updates arrive as cards with multiple-choice options, or the user can tap to give a voice response. When the deliberation completes, the user gets a plain-language summary of the decision, what changed, and any remaining disputes.

**Why this priority**: This is what makes Conversus a co-pilot rather than a black box. But it requires US-1 and US-2 to function.

**Independent Test**: A deliberation runs with at least one user interaction point where the co-pilot surfaces a question, the user answers, and the deliberation incorporates the answer.

**Acceptance Scenarios**:

1. **Given** a deliberation is running on the user's change request, **When** agents reach a dispute that benefits from user input, **Then** the user receives a notification card with a plain-language description of the disagreement and 2-4 options.
2. **Given** the change request impacts artifacts the user didn't mention, **When** impact analysis detects this, **Then** the user receives an impact summary with the option to proceed or adjust scope.
3. **Given** the deliberation completes, **When** the user views the result, **Then** they see a plain-language summary with: decision headline, what changed, remaining disputes (if any), quality indicators (agent count, mode, convergence score), and suggested next steps.

---

### US-4 — Voice Interaction (Priority: P2)

The user taps a microphone icon and says: "What's the status of the payment feature?" The system transcribes, classifies this as a query (not a change request), searches the project graph, and speaks back: "The payment feature is in-progress. It was approved in a cooperative deliberation on March 15th with 3 agents converging. Two specs define it — spec 041 for the API and spec 042 for the UI. Test coverage is at 78%." The user can follow up conversationally: "What are the remaining gaps?" and the system maintains context.

**Why this priority**: Voice is the interaction mode that makes this feel like the future, but it's an interface layer on top of US-1's project graph. Can be built independently once the graph exists.

**Independent Test**: User asks a question by voice, gets a spoken answer that references real project data.

**Acceptance Scenarios**:

1. **Given** the user taps the microphone and speaks a question about a known artifact, **When** transcription completes, **Then** the system classifies it as a query, searches the project graph, and returns a spoken answer within 3 seconds of silence detection.
2. **Given** the user speaks a change request rather than a query, **When** intent classification detects mutation intent, **Then** the system routes to the change request flow (US-2) rather than answering as a query.
3. **Given** the user has asked one question and received an answer, **When** they ask a follow-up without restating context, **Then** the system maintains conversational context and answers in relation to the previous exchange.

---

### US-5 — Mobile Chat Interface (Priority: P3)

The user opens the Conversus app on their phone. They see a chat thread with their project. Recent activity appears as message bubbles — "Payment feature deliberation completed: Redis selected over Postgres (equilibrium score: 0.91)." They can reply with text or voice. Push notifications arrive when Conversus needs their input on a co-pilot decision. The mobile experience is chat-first: no dashboards, no tables, just conversation.

**Why this priority**: Mobile extends reach to the full team, but the core value is delivered through the web dashboard (US-1 through US-4).

**Independent Test**: User receives a push notification on mobile, opens the app, answers a co-pilot question via voice, and the deliberation proceeds.

**Acceptance Scenarios**:

1. **Given** a deliberation needs user input, **When** the user's mobile app is registered, **Then** they receive a push notification within 30 seconds.
2. **Given** the user opens the mobile app, **When** they view the chat thread, **Then** they see recent project activity as message bubbles with the most recent at the bottom.
3. **Given** the user taps reply and speaks a response to a co-pilot question, **When** transcription completes, **Then** the answer is routed to the active deliberation and the user sees confirmation.

---

### US-6 — Team Activity View (Priority: P3)

A team lead opens the Command Center and sees a feed of all team activity: who submitted what change requests, which deliberations are running, which completed, what decisions were made, who was involved in co-pilot interactions. They can filter by team member, by date range, by artifact category. They can see trends: "We're averaging 3 change requests per week, 85% converge in one round, the most-deliberated category is API design."

**Why this priority**: Team visibility is a product differentiator for the Enterprise tier, but individual use cases (US-1 through US-5) deliver value first.

**Independent Test**: A project with 5+ completed deliberations renders an activity feed with working filters and at least one trend metric.

**Acceptance Scenarios**:

1. **Given** a project with multiple completed deliberations, **When** the team lead opens the activity view, **Then** they see a reverse-chronological feed of all project activity with actor, action, and outcome.
2. **Given** the activity feed, **When** the team lead filters by "API" category and "last 7 days," **Then** only matching activity appears.

---

### Edge Cases

- What happens when the construction pipeline can't classify a change request? → Fall back to cooperative mode with a prompt asking the user to clarify, rather than failing silently.
- What happens when voice transcription is ambiguous? → Show the transcription and ask for confirmation before routing.
- What happens when there are no indexed artifacts yet? → Show an empty state with a guided setup wizard that helps index the first artifacts.
- How does the system handle concurrent change requests from multiple team members on overlapping artifacts? → Queue with conflict detection; if two change requests touch the same artifacts, surface the overlap to both users before proceeding.
- What happens when a co-pilot question goes unanswered? → Configurable timeout (default: 24h) after which Conversus proceeds with its recommendation and flags the decision as "auto-resolved."

---

## 5. New Components

### 5.1 Project Knowledge Graph (Memgraph + ProjectDomain)

A graph database backed by **Memgraph** that indexes all project artifacts as nodes with typed relationships as edges, exposed through the existing domain plugin lifecycle.

#### Why Memgraph over Neo4j

| Dimension | Memgraph | Neo4j |
|-----------|----------|-------|
| License | BSL 1.1 → Apache 2.0 after 4 years. Clean for distribution. | Community is **GPL** (viral). Conflicts with MIT-compatible distribution goals. |
| Scale fit | In-memory. At our volume (hundreds to low thousands of artifacts), entire graph is sub-100 MB in RAM. Sub-millisecond queries. | Disk-based, JVM-backed. 1-2 GB minimum RAM for JVM overhead. Engineered for billions of nodes we'll never have. |
| Real-time | Built-in **triggers** (on-create, on-update hooks) push to external systems. Direct fit for live dashboard updates. | No native streaming. CDC is enterprise-only. Would need polling. |
| Cypher | openCypher + MAGE (open-source algorithms). | openCypher + APOC (proprietary extensions). |
| Vectors | No native vector index. | Native HNSW vector index since 5.11. |
| Migration | Both use openCypher — queries are portable. Low lock-in risk. | Same. |

**Vector search strategy**: Embeddings live in **RDS Postgres + pgvector** (fits the all-AWS stack). Graph structure lives in Memgraph (runs on EC2 or ECS). Two stores, each doing what it's best at. When `conversus-embeddings` is installed, semantic search queries pgvector for candidate artifact IDs, then enriches results from the graph. Without it, keyword search via Memgraph's text indexing. Alternative: **Amazon Neptune** is AWS's managed graph database (supports openCypher) — higher cost but zero operational overhead.

**Fallback option**: If Memgraph operational complexity is a concern, **Apache AGE** (Postgres extension adding openCypher) could keep everything in a single RDS instance — zero new infrastructure. Less mature but worth a spike.

#### Graph Schema

**Nodes** (artifact types, extensible):

| Label | Source | Extractors | Properties |
|-------|--------|-----------|------------|
| `:Brand` | Markdown docs, constitution | Tone extractor, value extractor | name, description, status |
| `:Goal` | Specs, roadmap docs | Goal extractor (OKR-style or freeform) | name, description, status, priority |
| `:Feature` | Specs, code, config | Feature extractor, status extractor | name, description, status, category |
| `:Spec` | `specs/` directory | Spec metadata extractor | id, name, status, depends_on, fr_count |
| `:Decision` | Deliberation output, `decisions/` dirs | Decision extractor | question, outcome, mode, eq_score, agents |
| `:Test` | Test suites, coverage reports | Coverage extractor, test-to-feature mapper | name, type, coverage, passing |
| `:Domain` | Domain plugin output | Domain score extractor, trend extractor | name, verdict, overall_score |

**Edges** (relationship types):

```cypher
(:Goal)-[:SERVED_BY]->(:Feature)
(:Feature)-[:DEFINED_BY]->(:Spec)
(:Feature)-[:TESTED_BY]->(:Test)
(:Feature)-[:SCORED_BY]->(:Domain)
(:Spec)-[:DECIDED_BY]->(:Decision)
(:Spec)-[:DEPENDS_ON]->(:Spec)
(:Decision)-[:AFFECTED]->(:Feature)
(:Brand)-[:CONSTRAINS]->(:Feature)
```

All edges are stored directionally; the query layer provides bidirectional traversal via Cypher's undirected match syntax (`()-[:SERVED_BY]-()`) when needed.

**Example queries**:

```cypher
// Impact analysis: what does changing the auth feature affect?
MATCH (f:Feature {name: "auth"})-[*1..3]-(affected)
RETURN affected.name, labels(affected), length(path) AS distance
ORDER BY distance

// Dashboard: category counts with health scores
MATCH (n) WHERE n:Feature OR n:Spec OR n:Goal OR n:Decision
RETURN labels(n)[0] AS category, count(n) AS total,
       avg(n.health_score) AS avg_health

// Co-pilot: find disputes related to a change request
MATCH (d:Decision)-[:AFFECTED]->(f:Feature)
WHERE d.disputes_remaining > 0 AND f.category = "payments"
RETURN d.question, d.disputes_remaining, f.name

// Team activity: recent decisions with convergence
MATCH (d:Decision)
WHERE d.created > datetime() - duration('P7D')
RETURN d.question, d.outcome, d.eq_score, d.mode
ORDER BY d.created DESC
```

**Trigger-driven dashboard updates**:

```cypher
// Memgraph trigger: notify dashboard when a new decision is created
CREATE TRIGGER new_decision
ON CREATE AFTER COMMIT
EXECUTE CALL publish_event('decision_created', createdVertices)
```

This pushes events to the backend via WebSocket or HTTP callback, which relays to the frontend via SSE.

#### Integration with Domain Plugin System

The `ProjectDomain` still implements `DomainPlugin` ABC. The difference is the store backend:

```python
class MemgraphStore(DomainStore):
    """Graph-backed store implementing the DomainStore protocol."""

    def append(self, record: DomainRecord) -> str:
        # CREATE node + relationship edges in Memgraph
        ...

    def query(self, domain: str, filters: dict, limit: int) -> list[DomainRecord]:
        # Cypher query with filters
        ...

    def trend(self, domain: str, field: str, window: int) -> TrendResult:
        # Cypher aggregation over time window
        ...

    def traverse(self, artifact_id: str, depth: int = 2) -> GraphResult:
        # Graph-specific: walk relationships to find connected artifacts
        ...
```

`create_domain_router(ProjectDomain, MemgraphStore(...))` auto-generates REST endpoints as usual, plus additional graph-specific endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/project/graph/{id}` | GET | Traverse from artifact, return subgraph |
| `/project/impact/{id}` | GET | Impact analysis — all artifacts within N hops |
| `/project/search` | GET | Full-text + optional semantic search |
| `/project/categories` | GET | Aggregated category view for dashboard |

#### Deployment

**Development**: Memgraph runs as a single Docker container (`memgraph/memgraph:latest`). Add to existing `docker-compose.yml` alongside the FastAPI backend.

**Production**: Memgraph Cloud free tier (1 project) for hosted option. Self-hosted on the same infrastructure as the FastAPI backend for the Enterprise tier.

**Data durability**: Memgraph uses WAL (write-ahead log) + periodic snapshots. For our data volume, snapshot + WAL replay on restart is effectively instant.

### 5.2 WebGapFiller

A `GapFiller` protocol implementation that renders gap questions in a web UI instead of CLI.

```python
class WebGapFiller(GapFiller):
    """Renders gap questions as UI components and collects answers via WebSocket."""

    async def fill(self, gaps: list[ParameterGap], context: ProblemContext) -> dict[str, Any]:
        # Send gap questions to frontend via WebSocket
        # Wait for user responses
        # Map responses to parameter values using template constraints
        # Return filled parameter dict
```

**Input rendering** (automatic from parameter type):

| Parameter Type | UI Control |
|---------------|-----------|
| `float` with range | Slider with min/max labels |
| `integer` with range | Number stepper |
| `string` with enum | Radio buttons or dropdown |
| `string` open-ended | Text input |
| `boolean` | Toggle switch |
| `function` (derived) | Read-only display with explanation |

### 5.3 Impact Analysis

When a change request is submitted, use Memgraph's graph traversal to find all artifacts connected to the affected area.

**Input**: Change request text + classified decision type + matched objective template.

**Process**: Cypher variable-depth traversal from affected artifacts:

```cypher
// Find all artifacts within 3 hops of the target feature
MATCH path = (target:Feature {name: $feature_name})-[*1..3]-(affected)
RETURN affected, relationships(path) AS via,
       length(path) AS distance,
       affected.health_score AS risk
ORDER BY distance, risk ASC
```

Distance from the change target determines risk level: 1 hop = directly affected, 2 hops = transitively affected, 3 hops = peripherally affected. Domain health scores on each artifact provide a second risk signal — a low-health artifact hit by a transitive change is flagged higher.

**Output**: Impact summary showing: directly affected artifacts (distance 1), transitively affected artifacts (distance 2-3), risk level per artifact (distance × inverse health score), and the relationship path explaining why each artifact is affected.

### 5.4 Voice Interface

**Speech-to-text**: Web Speech API (browser-native, zero dependency) with optional Whisper/Deepgram upgrade path for accuracy.

**Intent classification**: Route transcribed text through `classify_decision_type()` from construction pipeline. Two top-level intents:
- **Query**: Decision type classification fails or matches no mutation pattern → search project graph → speak answer
- **Mutation**: Decision type classification succeeds → enter change request flow (US-2)

**Text-to-speech**: Web Speech API (browser-native) with optional ElevenLabs/OpenAI TTS upgrade path for natural voice.

**Conversation memory**: Maintain session context (last 10 turns) so follow-up questions work without restating context.

---

## 6. Functional Requirements

### Project Graph

- **FR-001**: A `ProjectDomain` MUST implement the `DomainPlugin` ABC with extractors for at least: specs, decisions, features, and goals.
- **FR-002**: Each artifact in the project graph MUST have: `id`, `type`, `name`, `description`, `status`, `relationships`, `created`, `updated`.
- **FR-003**: Relationships MUST be bidirectional — if Feature A is `defined-by` Spec B, then Spec B is `defines` Feature A.
- **FR-004**: The project graph MUST be stored in Memgraph and queryable via openCypher.
- **FR-005**: The project graph MUST support full-text search via Memgraph text indexing, with optional semantic search via RDS Postgres/pgvector when `conversus-embeddings` is installed.
- **FR-006**: The project graph MUST be re-indexable from source (specs directory, deliberation output, domain records) without manual curation.
- **FR-007**: `create_domain_router(ProjectDomain, MemgraphStore(...))` MUST produce REST endpoints for browsing, searching, traversal, and impact analysis.
- **FR-008**: Memgraph triggers MUST push artifact create/update events to the dashboard via SSE.

### Dashboard UI

- **FR-009**: The dashboard MUST render a top-level view with category cards (one per artifact type) showing count, health score, and recent activity.
- **FR-010**: Each category MUST support: list view with filters (status, date range, text search), detail view with relationships and history, and navigation between related artifacts.
- **FR-011**: The dashboard MUST display quality indicators from plugin output (equilibrium score, convergence status, dispute count) on relevant artifacts.
- **FR-012**: The dashboard MUST receive live updates via Memgraph triggers → SSE, not polling.

### Change Request Flow

- **FR-013**: Users MUST be able to submit a change request as free-form text or voice.
- **FR-014**: The system MUST classify the change request using `classify_decision_type()` and present the classification to the user for confirmation.
- **FR-015**: `WebGapFiller` MUST render gap questions with appropriate UI controls based on parameter type and range.
- **FR-016**: After gap-filling, the system MUST show a plain-language summary of the assembled objective and a cost estimate before starting deliberation.
- **FR-017**: The change request flow MUST produce the same `objective.yml` output that the CLI construction pipeline produces — no divergence between web and CLI paths.

### Co-Pilot

- **FR-018**: During deliberation, the system MUST surface questions to the user only when: (a) agents are deadlocked on a dispute where user preference would break the tie, or (b) impact analysis reveals affected artifacts the user didn't mention.
- **FR-019**: Co-pilot questions MUST render as cards with: plain-language description, 2-4 options (or free-text input), and a "let Conversus decide" default option.
- **FR-020**: The user MUST be able to ignore co-pilot questions. After a configurable timeout, Conversus proceeds with its recommendation.
- **FR-021**: Upon deliberation completion, the system MUST present a result summary with: headline, decision, affected artifacts, remaining disputes, quality indicators, and suggested next steps.

### Voice

- **FR-022**: Voice input MUST work via browser-native Web Speech API with no additional service dependencies for basic functionality.
- **FR-023**: Voice input MUST be classified as query or mutation before routing.
- **FR-024**: Query responses MUST be spoken aloud via text-to-speech.
- **FR-025**: Conversational context MUST persist for at least 10 turns within a session.

### Mobile

- **FR-026**: The mobile interface MUST be a PWA installable from the web dashboard URL.
- **FR-027**: Push notifications MUST fire when a co-pilot question is waiting for user input.
- **FR-028**: The mobile UI MUST be chat-first — conversation thread, not dashboard tables.

---

## 7. Success Criteria

- **SC-001**: A non-technical user (no CLI, no YAML, no code) can browse all project artifacts, submit a change request by typing a sentence, answer gap questions via the UI, and view the deliberation result — end to end.
- **SC-002**: The project graph indexes at least 4 artifact types from a real conversus project (this repo) with correct relationships.
- **SC-003**: `WebGapFiller` produces identical `objective.yml` output to `InteractiveGapFiller` given the same inputs.
- **SC-004**: A voice query against the project graph returns a relevant answer within 5 seconds of speech completion.
- **SC-005**: A co-pilot interaction (question surfaced → user answers → deliberation incorporates) completes without the user needing to understand modes, templates, or game theory.
- **SC-006**: The dashboard loads and renders artifacts from the domain REST API — no direct engine imports.

---

## 8. Constraints

### Must NOT

- **Must NOT modify the deliberation engine.** The Command Center consumes engine output via REST APIs, domain stores, and the construction pipeline's public API. Zero changes to `engine/`, `linter/`, or `SKILL.md`.
- **Must NOT require the Command Center for existing workflows.** CLI, SDK, MCP, and guided workflow continue to work unchanged. The Command Center is additive.
- **Must NOT expose raw deliberation artifacts to non-technical users.** Everything surfaced in the dashboard must be translated to plain language. Markdown synthesis output is for technical users; the dashboard shows headlines, summaries, and quality indicators.
- **Must NOT require paid plugins for core Command Center functionality.** Browsing, searching, submitting changes, and viewing results work with the free engine. Paid plugins add quality indicators (equilibrium scores, convergence predictions) as optional enrichment.

### Must

- **Must build on existing domain plugin infrastructure.** ProjectDomain uses `DomainPlugin` ABC, `VariableExtractor` protocol, `DomainStore`, and `create_domain_router()`. No parallel persistence or API system.
- **Must build on existing construction pipeline.** Change requests route through `classify_decision_type()`, `select_candidate_templates()`, `identify_gaps()`, and `assemble_objective()`. The `WebGapFiller` is a new implementation of the existing `GapFiller` protocol.
- **Must follow existing package coupling rules.** Dashboard layer imports from `conversus.domains` and `conversus.schemas`. Never from `engine.*` directly.

---

## 9. Execution Order

### Phase 1: Foundation (depends on specs 034-037, 039)
Fix engine bugs first. All 8 modes must work correctly before exposing them to non-technical users.

### Phase 2: Project Knowledge Graph
Build `ProjectDomain` with extractors for specs, decisions, features, goals. Index this repo as the first test case. REST API auto-generated via `create_domain_router()`.

### Phase 3: Dashboard UI
Build the web frontend (greenfield). Artifact browser, search, filter, category views, detail views with relationships. Consumes project graph REST API. [NEEDS CLARIFICATION: Next.js, or a different framework?]

### Phase 4: Change Request Flow + WebGapFiller
Web-based change submission. `WebGapFiller` renders gap questions. Impact analysis from project graph. Cost estimate before deliberation. SSE streaming for deliberation progress.

### Phase 5: Co-Pilot
Selective user involvement during deliberation. Question cards with multiple-choice. Timeout + auto-resolve. Result summary with plain-language translation.

### Phase 6: Voice
Speech-to-text input. Intent classification (query vs mutation). Text-to-speech responses. Conversational context.

### Phase 7: Mobile PWA
Chat-first interface. Push notifications. Installable PWA from dashboard URL.

---

## 10. Open Questions

- **OQ-1**: **Memgraph vs Neptune vs Apache AGE**: Memgraph is recommended (in-memory, triggers, BSL license, runs on EC2/ECS). Amazon Neptune is the managed AWS alternative (openCypher support, zero ops, higher cost). Apache AGE keeps everything in a single RDS Postgres instance (zero new infra, less mature). Which fits the AWS stack best?
- **OQ-2**: **Semantic search**: Embedding-based search lives in RDS Postgres/pgvector, graph structure in Memgraph. Should semantic search be free-tier (bundle a small embedding model) or paid-only (require `conversus-embeddings`)? Keyword search works without it.
- **OQ-3**: How does artifact indexing work for projects that aren't conversus itself? Is there a guided setup wizard? Do we provide starter extractors for common project structures (React app, API service, etc.)?
- **OQ-4**: Should the co-pilot timeout be per-user-configurable or project-level? What's the right default — 1 hour, 24 hours, or "wait forever"?
- **OQ-5**: Does the mobile app need offline support, or is it online-only?
- **OQ-6**: Should the Command Center support multiple projects per instance (multi-tenant graph), or is it one Memgraph instance per project?
- **OQ-7**: What authentication model — Cognito (AWS-native), SSO for Enterprise, or both?
- **OQ-8**: How do we handle the bootstrap problem — a new project has no indexed artifacts. What's the onboarding experience?
- **OQ-9**: **Graph visualization**: Should the dashboard include an interactive graph view (force-directed layout showing artifact relationships), or are list/card views sufficient? Graph viz is impressive but complex to build well.
