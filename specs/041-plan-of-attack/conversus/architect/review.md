I'll conduct a thorough technical risk analysis of this plan as the red team architect. Let me read through all the target documents and documentation first.

<antArtifact identifier="red-team-architect-review" type="text/markdown" title="Red Team Technical Risk Analysis" path="/Users/brettkellgren/Sites/conversus/specs/041-plan-of-attack/conversus/architect/review.md">
# Red Team Technical Risk Analysis - Phase 1

## Executive Summary

The Plan of Attack proposes a 7-phase bottom-up build strategy for conversus, transitioning from monolith to packageable components, culminating in a Command Center dashboard. While the strategic direction shows promise, this plan contains **critical technical risks** that could derail execution or produce an unmaintainable system.

The most dangerous architectural flaw is **assuming mechanical package extraction without validating runtime coupling**. The plan claims "zero cross-boundary imports" make splitting mechanical (plan-of-attack.md), but import-level coupling is insufficient to guarantee runtime independence. Hidden dependencies in plugin loading, schema validation, domain stores, and configuration resolution could create circular dependencies that only surface during actual extraction.

**Overall threat assessment: HIGH** - The plan underestimates infrastructure complexity, makes unvalidated coupling assumptions, and contains multiple single points of failure that could cascade into project delays or architectural collapse.

## Threat Catalog

### Package Splitting Vulnerabilities

**[THREAT-001: Runtime Coupling Discovery]** (severity: critical)
- **Description**: Package extraction fails due to hidden runtime dependencies not captured by import analysis. Plugin loading, schema validation, and domain API generation may have circular runtime dependencies between supposedly independent packages.
- **Attack vector**: During Phase 0 execution, pytest failures emerge showing conversus-domains requires conversus-plugins at runtime, while conversus-plugins requires conversus-schemas for validation, creating circular dependency hell.
- **Evidence**: spec-032 L52-57 claims "coupling rules enforced throughout development (zero cross-boundary imports) make this extraction mechanical" but provides no validation of runtime coupling beyond import analysis.
- **Blast radius**: Package split becomes impossible, forcing architectural redesign or abandoning the split strategy entirely. 3+ month delay minimum.
- **Likelihood**: Likely - Complex Python applications commonly have runtime coupling that static analysis misses.

**[THREAT-002: Configuration Resolution Fragmentation]** (severity: high)  
- **Description**: After splitting, configuration resolution becomes fragmented across packages with no clear authority. `conversus.yml` parsing, preset resolution, and template loading could break when dependencies are distributed.
- **Attack vector**: Template loading in SKILL.md L168-175 expects templates relative to conversus package root, but after splitting, template resolution fails when engine and schemas are separate packages.
- **Evidence**: SKILL.md L161-165 shows complex preset resolution logic that walks parent directories. This logic assumes monolith structure and will break with distributed packages.
- **Blast radius**: CLI commands fail with configuration errors, user workflows break, rollback to monolith required.
- **Likelihood**: Certain - Template and preset resolution explicitly depends on monolith directory structure.

### Data Layer Architecture Risks

**[THREAT-003: Memgraph Operational Complexity]** (severity: high)
- **Description**: Memgraph introduces significant operational overhead that the plan underestimates. In-memory graph databases require careful memory management, backup strategies, and failure recovery that AWS infrastructure may not support well.
- **Attack vector**: Production deployment fails because Memgraph memory requirements exceed ECS task limits, or data loss occurs during container restarts because WAL replay fails.
- **Evidence**: spec-040 L405-407 acknowledges "Memgraph operational complexity" as a concern but plan-of-attack Phase 3 proceeds without addressing this risk.
- **Blast radius**: Command Center becomes unusable, customer data loss, emergency migration to PostgreSQL required.
- **Likelihood**: Likely - In-memory databases have well-known operational challenges in containerized environments.

**[THREAT-004: Graph-Relational Impedance Mismatch]** (severity: medium)
- **Description**: The dual-store design (Memgraph for graph, RDS for vectors) creates consistency problems and operational complexity. Data synchronization between stores could diverge, leading to inconsistent query results.
- **Attack vector**: Vector embeddings in PostgreSQL become stale after graph updates in Memgraph, causing semantic search to return outdated results that don't match current graph state.
- **Evidence**: spec-040 L380-384 proposes "two stores, each doing what it's best at" but provides no consistency mechanism between them.
- **Blast radius**: User queries return inconsistent results, data integrity violations, debugging becomes extremely difficult.
- **Likelihood**: Possible - Multi-store consistency is a classic distributed systems problem.

### Schema Layer Standalone Risks

**[THREAT-005: Schema-Engine Circular Dependency]** (severity: critical)
- **Description**: The "free schemas without engine" strategy creates a circular dependency. Schemas need validation logic from the engine, but the engine depends on schemas for type definitions.
- **Attack vector**: `pip install conversus-schemas` fails because schema validation requires engine components, but engine import causes the full conversus dependency tree to be pulled in, defeating the "lightweight" purpose.
- **Evidence**: spec-033 L68-70 claims "schema layer is free, engine is paid" but spec-040 FR-005 requires schema validation, which currently lives in the engine's linter.
- **Blast radius**: Free tier strategy collapses, monetization model breaks, architectural rework required.
- **Likelihood**: Certain - Current schema validation is tightly coupled to engine linter components.

### Infrastructure Integration Failures

**[THREAT-006: AWS Service Integration Gaps]** (severity: medium)
- **Description**: The "all-AWS" constraint creates integration challenges where AWS services don't naturally fit the architecture. Forcing Memgraph onto ECS or Lambda may create performance bottlenecks or cost explosions.
- **Attack vector**: Memgraph on ECS requires persistent EBS volumes for durability, but ECS task restarts cause data loss because volume mounting fails during rapid scaling events.
- **Evidence**: spec-040 L418 mentions "Amazon Neptune is AWS's managed graph database" as an alternative but plan-of-attack Phase 3 proceeds with Memgraph without AWS fit analysis.
- **Blast radius**: Infrastructure costs 10x projections, performance degrades under load, customer deployments fail.
- **Likelihood**: Possible - AWS service constraints often emerge during actual deployment.

### Command Center Scaling Risks

**[THREAT-007: WebSocket Connection Flooding]** (severity: medium)
- **Description**: Real-time dashboard updates via WebSockets (SSE) could overwhelm the backend when multiple team members monitor the same project, especially during large deliberations.
- **Attack vector**: 20 team members open the Command Center during a major deliberation, each establishing WebSocket connections. Backend runs out of file descriptors, new connections fail, existing connections drop.
- **Evidence**: spec-040 FR-008 requires "live updates via Memgraph triggers → SSE" but provides no connection management or rate limiting.
- **Blast radius**: Dashboard becomes unusable during peak usage, users lose confidence in real-time features.
- **Likelihood**: Possible - WebSocket resource exhaustion is common in multi-user applications.

### Development Process Risks

**[THREAT-008: Phase Dependencies Violation]** (severity: high)
- **Description**: The "each layer validates the one below it" approach breaks when higher layers discover fundamental flaws in lower layers, requiring rework that cascades backward through completed phases.
- **Attack vector**: Phase 5 (co-pilot) discovers that Phase 3 (data layer) cannot support the required query patterns for impact analysis, forcing a complete data layer redesign.
- **Evidence**: plan-of-attack L29-31 claims each layer validates below, but L125-135 shows complex interdependencies where co-pilot needs data layer, dashboard needs co-pilot, creating validation cycles.
- **Blast radius**: Development timeline collapses as later phases invalidate earlier work, forcing iterative rework.
- **Likelihood**: Likely - Bottom-up development commonly discovers integration issues late in the process.

## Cascading Failures

**Scenario 1: Package Split Cascade**
- **Trigger**: Phase 0 package extraction reveals circular runtime dependencies between conversus-plugins and conversus-domains
- **Propagation**: Schema validation breaks → template loading fails → CLI commands error → user workflows stop working → emergency rollback required → confidence in architecture planning destroyed
- **Terminal state**: Team abandons package splitting, returns to monolith, 2+ months of work wasted, architecture credibility damaged

**Scenario 2: Data Layer Infrastructure Collapse**  
- **Trigger**: Memgraph memory usage exceeds AWS ECS task limits during production load testing
- **Propagation**: Graph queries fail → Command Center becomes unusable → customer demos fail → emergency migration to PostgreSQL required → data layer redesign needed → all higher layers (co-pilot, dashboard) need rework
- **Terminal state**: 6+ month delay while data layer is completely rebuilt on PostgreSQL, Command Center launch postponed indefinitely

**Scenario 3: Free Tier Strategy Breakdown**
- **Trigger**: Schema package cannot be extracted standalone due to engine dependencies
- **Propagation**: Free tier becomes unavailable → monetization strategy fails → product positioning as "free deliberation, paid optimization" collapses → go-to-market plan needs complete revision
- **Terminal state**: Forced into full-product pricing only, losing competitive advantage of freemium model

## Missing Safeguards

**Dependency Validation Framework**: The plan lacks automated tooling to validate that package boundaries are truly independent. Static analysis of imports is insufficient - runtime dependency validation, integration testing of split packages, and circular dependency detection are essential before attempting mechanical extraction.

**Rollback Strategy**: No plan exists for rolling back failed phases. Each phase builds on the previous, but if Phase 4 fails, how do you revert the data layer changes made in Phase 3? Database migrations, package publications, and infrastructure changes need explicit rollback procedures.

**Performance Benchmarking**: The plan includes no performance validation at each layer. Memgraph vs PostgreSQL performance, WebSocket connection limits, and Command Center responsiveness need baseline measurements and acceptance criteria before proceeding to dependent phases.

**Integration Testing Strategy**: The plan assumes each layer will integrate smoothly with the next. Missing comprehensive integration testing between layers - particularly the schema/engine boundary, data layer/co-pilot integration, and WebSocket/dashboard communication paths.

**Operational Readiness Gates**: Each phase needs operational validation - monitoring, logging, alerting, backup/recovery, and deployment automation. The plan focuses on feature development but ignores operational requirements that could block production deployment.

**Customer Impact Analysis**: No mechanism exists to validate that each layer meets actual user needs before proceeding. The bottom-up approach could build technically sound but user-irrelevant functionality. Early user feedback loops and usage validation are missing from the execution model.
</antArtifact>