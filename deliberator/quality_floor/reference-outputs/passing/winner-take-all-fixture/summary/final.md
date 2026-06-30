# Synthesis: Best API Framework Selection

**Deliberation mode:** Winner-Take-All
**Target:** api-framework-selection.md — Which API framework should the platform team adopt for the new service mesh?
**Synthesizer:** Neutral (no agent affiliation)

---

### Process Summary

| Metric | Value |
|--------|-------|
| Agents | 3 (advocate-fastapi, advocate-express, advocate-go) |
| Total artifacts produced | 16 |
| Candidates evaluated | 3 (FastAPI, Express.js, Go net/http) |
| Rounds of cross-review | 2 |
| Disputes remaining after Phase 4 | 2 |

---

### Recommendation Scorecard

| # | Recommendation | Advocate-Fastapi | Advocate-Express | Advocate-Go | Status |
|---|---------------|-----------------|-----------------|-------------|--------|
| 1 | Primary framework selection | FastAPI (P99 latency) | Express.js (ecosystem) | Go net/http (throughput) | **DECIDED: FastAPI** |
| 2 | Migration timeline | 6 months (incremental) | 3 months (drop-in) | 9 months (rewrite) | **DECIDED: 6 months** |
| 3 | Fallback strategy | Express adapter layer | N/A (current stack) | Go sidecar for hot paths | **ADOPTED: Express adapter** |

**Advocate-Express conceded:** Express.js ecosystem advantage does not offset the P99 latency gap measured in benchmarks. (Pragmatist cross-review §2)
**Advocate-Go conceded:** Go rewrite timeline exceeds the Q3 deadline constraint. (revision R3 → adopted conditional sidecar)

---

## Winner

**FastAPI** selected as the primary API framework based on:
- Lowest measured P99 latency (12ms vs 34ms Express, 8ms Go — but Go excluded on timeline)
- Native async support aligns with event-driven architecture (cross-review Phase 2)
- Type safety via Pydantic reduces runtime errors (revision Phase 3 concession from Express advocate)

---

## Runner-Up

**Express.js** retained as fallback adapter layer. The selection was contested on ecosystem maturity grounds — Express has 4× the middleware library count and the team has 3 years of production experience. However, benchmark data (Phase 1) and the P99 latency requirement (Phase 3 revision) favored FastAPI.

---

<!-- DELIBERATOR:DISPUTES_BEGIN -->

### Remaining Disputes

**Dispute: Benchmark Representativeness**

**Positions:**

*Advocate-Express:* The synthetic benchmarks do not reflect real-world middleware chains with auth, logging, and rate limiting — Express overhead is lower in production scenarios.

*Advocate-Fastapi:* Benchmark methodology was agreed upon in Phase 1; post-hoc methodology challenges should not override converged acceptance.

**Arguments:** Express advocate argues production workloads differ materially from synthetic benchmarks. FastAPI advocate notes the benchmark protocol was accepted by all agents before Phase 2.

**Synthesizer assessment:** Benchmark methodology was ratified by consensus. Express advocate's concern is valid but should be tested in the 6-month migration, not used to override the selection. Recommend a production validation checkpoint at month 3.

---

**Dispute: Go Sidecar Scope Creep**

**Positions:**

*Advocate-Go:* The Go sidecar for hot paths should cover the top 5 latency-critical endpoints, not just the 2 identified in Phase 1.

*Advocate-Fastapi:* Expanding sidecar scope undermines the single-framework decision and creates maintenance burden.

**Arguments:** Go advocate's position would effectively create a dual-framework architecture. FastAPI advocate argues this contradicts the winner-take-all selection principle.

**Synthesizer assessment:** Sidecar scope should remain at the 2 endpoints identified in Phase 1. Expansion requires a separate deliberation with fresh benchmarks. *(Phase 4 disputes, cross-review §3)*

<!-- DELIBERATOR:DISPUTES_END -->

---

### Concessions & Convergence

| Agent | Concession | Phase |
|-------|-----------|-------|
| Advocate-Express | Withdrew ecosystem-maturity argument after P99 benchmark data | Phase 2 cross-review |
| Advocate-Go | Accepted timeline constraint eliminates full rewrite option | Phase 3 revision |
| Advocate-Fastapi | Adopted Express adapter layer as migration safety net | Phase 3 revision |

---

### Dangerous Contradictions Found

**Resolved:**

1. **Framework lock-in vs. sidecar flexibility.** Selecting FastAPI as the sole framework while allowing Go sidecars creates a de facto dual-framework architecture. **Resolution:** Go sidecar scoped to exactly 2 hot-path endpoints with quarterly review. *(Phase 3 revision, Phase 4 dispute)*

---

### Phase References

- Benchmark protocol ratified (Phase 1 review, all agents)
- P99 latency measurements introduced (Phase 2 cross-review §1)
- Timeline constraint formalized (Phase 3 revision R3)
- Sidecar scope limited (Phase 4 dispute resolution)
