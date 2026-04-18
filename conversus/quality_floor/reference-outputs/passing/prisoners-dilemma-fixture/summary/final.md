# Synthesis: Platform vs. Product Team Responsibility Boundaries

**Deliberation mode:** Prisoner's Dilemma
**Target:** platform-product-boundaries.md — Where does platform team responsibility end and product team responsibility begin for observability infrastructure?
**Synthesizer:** Neutral (no agent affiliation)

---

### Process Summary

| Metric | Value |
|--------|-------|
| Agents | 2 (platform-advocate, product-advocate) |
| Total artifacts produced | 10 |
| Responsibility boundaries proposed | 6 |
| Boundaries converged | 3 |
| Boundaries disputed | 2 |
| Boundaries withdrawn | 1 |
| Rounds of cross-review | 2 |

---

### Responsibility Map

| # | Boundary | Platform-Advocate | Product-Advocate | Status |
|---|----------|------------------|-----------------|--------|
| B1 | Metrics collection pipeline | Platform owns Prometheus + Grafana infra | Product configures dashboards + alerts | **CONVERGED** |
| B2 | Log aggregation | Platform owns ELK stack + retention policy | Product owns log schema + structured logging | **CONVERGED** |
| B3 | Distributed tracing | Platform owns Jaeger deployment | Product owns span instrumentation | **CONVERGED** |
| B4 | Alert routing & on-call | Platform provides PagerDuty integration | Product defines escalation policies | **DISPUTED** |
| B5 | Custom metric creation | Platform provides SDK + rate limits | Product owns business metric definitions | **DISPUTED** |
| B6 | Cost allocation for observability | Platform absorbs all costs | Product pays per-team usage | **WITHDRAWN** |

**Platform-Advocate conceded:** Log schema ownership belongs to product teams; enforcing a platform-mandated schema creates adoption friction that undermines observability goals. (cross-review Phase 2, B2 §1)

**Product-Advocate conceded:** Prometheus infrastructure including HA, retention, and federation is beyond product team operational capacity. Platform ownership is appropriate. (revision Phase 3, B1)

---

<!-- CONVERSUS:DISPUTES_BEGIN -->

### Remaining Disputes

**Dispute: [B4] Alert Routing Ownership**

**Positions:**

*Platform-Advocate:* Platform team should own the PagerDuty integration AND default escalation policies. Product teams customize within platform-defined guardrails. This prevents alert fatigue from misconfigured escalations.

*Product-Advocate:* Product teams must own their escalation policies entirely. They understand their service criticality and team availability better than platform. Platform guardrails would slow incident response.

**Arguments:** Platform advocate cites 3 incidents in Q4 where misconfigured product team escalations caused 2+ hour response delays. Product advocate counters that those incidents were from a single team and do not justify platform-wide policy control.

**Synthesizer assessment:** Recommend a shared model: platform provides templates and validates escalation configs against SLA requirements, but product teams own the final policy. *(Phase 4 dispute, cross-review §2)*

---

**Dispute: [B5] Custom Metric Rate Limits**

**Positions:**

*Platform-Advocate:* Custom metrics must have platform-enforced rate limits (1000 series per service) to prevent Prometheus cardinality explosion. Product teams exceeding limits must request capacity through platform review.

*Product-Advocate:* Fixed rate limits are too restrictive for ML and analytics services that inherently produce high-cardinality metrics. Per-service limits should be negotiated, not mandated.

**Arguments:** Platform advocate presents data showing 3 cardinality incidents in 6 months caused by unrestricted metric creation. Product advocate argues the proposed 1000-series limit would require their ML pipeline to drop 40% of its monitoring signals.

**Synthesizer assessment:** Recommend tiered limits: 1000 series default, 5000 for approved high-cardinality services, with automatic alerting at 80% of limit. *(Phase 3 revision, Phase 4 dispute)*

<!-- CONVERSUS:DISPUTES_END -->

---

## Disputed Boundaries

### [B4: Alert Routing Ownership]

Platform-advocate wants platform to own PagerDuty integration and default escalation policies. Product-advocate wants full product-team ownership. Shared model recommended.

### [B5: Custom Metric Rate Limits]

Platform-advocate proposes 1000-series cap per service. Product-advocate argues ML services need higher limits. Tiered approach recommended.

---

### Concessions & Convergence

| Agent | Concession | Phase |
|-------|-----------|-------|
| Platform-Advocate | Accepted product team ownership of log schema | Phase 2 cross-review |
| Product-Advocate | Accepted platform ownership of Prometheus infrastructure | Phase 3 revision |
| Platform-Advocate | Withdrew cost allocation boundary (B6) as out of scope | Phase 3 revision |
| Product-Advocate | Acknowledged cardinality risk requires some rate limiting | Phase 4 disputes |

---

### Dangerous Contradictions Found

**Resolved:**

1. **Platform-mandated log schema vs. product adoption.** Platform advocate originally proposed enforcing a strict log schema across all services. Product advocate's cross-review showed this would require rewriting 12 services' logging. **Resolution:** Platform provides recommended schema + validation library; product teams adopt voluntarily with incentive (priority support for structured log users). *(cross-review Phase 2, revision Phase 3)*

---

### Phase References

- Initial boundary proposals (Phase 1 review, both advocates)
- Log schema ownership resolved (Phase 2 cross-review §1)
- Prometheus HA ownership converged (Phase 3 revision B1)
- Cost allocation withdrawn (Phase 3 revision B6)
- Alert routing and rate limits disputed (Phase 4 disputes, 2 boundaries)
