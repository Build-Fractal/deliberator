# Feature Specification: Free/Paid Tier Partitioning

**Feature ID**: `033-monetization-partitioning`
**Created**: 2026-03-25
**Updated**: 2026-04-03
**Status**: Done — 2026-04-03
**Depends On**: `032-package-splitting` (build-time split must be in place)
**Trigger**: Execute immediately after 032. Unblocks command center (040), execution providers (042), and all downstream work.
**Origin**: Architecture decision — define what is free and what is paid. Heuristics are paid. Deliberation engine is free.

---

## 1. Core Principle

**Deliberation is free. Scoring is paid.**

The free tier gives you the full multi-agent deliberation engine — 8 modes, templates, presets, CLI, MCP, web UI. Agents argue, cross-review, revise, and synthesize. You get the full 5-phase pipeline with dispute detection and round management.

The paid tier adds **quantitative analysis** — equilibrium scoring, convergence prediction, config optimization, and payoff computation. These are the features that make agent output consistent, tunable, and reproducible across runs.

---

## 2. Feature Matrix: Free vs Paid

### Deliberation Engine (FREE — `pip install conversus`)

| Feature | Description | Spec |
|---------|-------------|------|
| 8 deliberation modes | cooperative, WTA, PD, red-blue, negotiation, resource-allocation, fair-division, mechanism-design | 028 |
| 5-phase pipeline | review → cross-review → revision → disputes → synthesis | Core |
| Phase 6 arbitration | Subject arbitration with grounding document | 001 |
| Multi-round deliberation | Up to 5 rounds with stagnation detection | 002, 004 |
| Iterations | Cross-review/revision depth control | Core |
| Template system | Per-mode markdown templates with variable substitution | 005 |
| Preset system | Agent persona presets with composition | 004 |
| Guided workflow | `/conversus define/interests/mode/converge/arbitrate/gate` | 007-011 |
| CLI | `conversus run`, `conversus decide`, `conversus lint` | Core |
| MCP server | 3 tools for IDE integration | Core |
| Web UI | BYOK FastAPI + frontend | Core |
| Schema validation | Game form schemas, objective templates, feature extraction definitions | 012-015 |
| Plugin framework | Plugin ABC, hooks, loading, produces/consumes | 016, 024 |
| Domain framework | Domain ABC, stores, API router, scaffolds | 029, 030 |
| Scenario storage | Basic save/load/replay | 020 |
| Linter | Template validation, schema checking | Core |
| Antipattern catalog | Steering agents away from known pitfalls | 010 |
| Dispute parsing | `DISPUTES_BEGIN/END` markers, mode-specific heading detection | Core |
| Prior context | `prior:` field for building on previous deliberations | Core |
| Documentation | Full public docs site | 031 |
| Blog | Engineering, Process, Release posts | 031 |

### Scoring & Optimization (PAID — `pip install conversus-solvers`)

| Feature | Description | Spec | Why Paid |
|---------|-------------|------|----------|
| **Heuristic payoff functions** | All 8 mode payoff calculations with `(payoff, best_response)` output | 017, 039 | Quantitative scoring that makes agent output comparable and consistent |
| **EquilibriumScorer plugin** | Equilibrium quality score [0.0-1.0] per round | 017, 021 | Measures whether agents reached Nash equilibrium |
| **Convergence predictor** | Kalman filter-based convergence prediction with confidence bounds | 018, 022 | Predicts when deliberation will converge — saves budget |
| **Config optimizer** | Budget-constrained config recommendation (rounds, agents, iterations) | 019, 023 | Optimal resource allocation for deliberation |
| **nashopt integration** | Exact Nash equilibrium computation via JAX | 021 | Solver-backed equilibrium verification |
| **AMPL integration** | MIP/LP optimization via AMPL/HiGHS | 023 | Exact optimization for config and game theory |
| **Cross-plugin interfaces** | produces/consumes data flow (eq_score → Kalman) | 024 | Enables 3D Kalman state with real equilibrium data |
| **Solver validation flow** | Post-solve verification of solution concepts | 027 | Proves agents are at equilibrium, not just estimates |
| **AMPL game solvers** (future) | Exact game-theoretic solutions per mode | 043 | Formal optimization models for consistency/tunability |
| **AMPL model templates** (future) | Template library for optimization problems | 044 | Agent skill for building optimization models |

### Domain Implementations (PAID — per vertical)

| Package | Domain | Spec | Why Paid |
|---------|--------|------|----------|
| `conversus-swe` | Code review | 029 | Vertical-specific feature extraction, scaffolds, verdict logic |
| `conversus-healthcare` (future) | Healthcare compliance | — | Domain expertise |
| `conversus-legal` (future) | Legal review | — | Domain expertise |

### Enterprise (future)

| Feature | Description |
|---------|-------------|
| Self-hosted deployment | ECS/K8s + managed database |
| Custom domains | White-label domain plugin development |
| SLA | Guaranteed response times |
| SSO | Org-level authentication |
| Audit log | Full deliberation history with compliance export |

---

## 3. Why Heuristics Are Paid

The heuristic payoff functions (spec 039) compute `(payoff, best_response_payoff)` for all 8 modes. They're "just math" — but they're the math that:

1. **Makes agent output comparable** — without scoring, you have 3 review documents and a synthesis. With scoring, you know Agent A's position is 0.85 and Agent B's is 0.62.
2. **Enables consistency** — the same features produce the same score deterministically. This is what makes conversus output stable across runs.
3. **Provides the tuning interface** — parameters like `gamma` (overreach penalty) control agent behavior quantitatively. Without the scoring tier, tuning is prompt engineering only.
4. **Gates the premium path** — heuristics are the foundation that nashopt, AMPL, and Kalman build on. If heuristics are free, the premium tier is just "better heuristics" (weak value prop). If heuristics are paid, the premium tier is the entire quantitative layer (strong value prop).

The free tier is a complete deliberation engine. The paid tier is the instrumentation that makes it enterprise-grade.

---

## 4. Install Experience

```bash
# Free: full deliberation engine
pip install conversus
conversus run config.yml
# Output: reviews, cross-reviews, revisions, disputes, synthesis
# No scoring, no convergence prediction, no optimization

# Paid: add scoring + optimization
pip install conversus-solvers
conversus run config.yml
# Output: same + plugins/equilibrium-scorer.json, plugins/convergence-predictor.json
# Scores per agent, equilibrium quality, convergence estimate

# Paid: add code review domain
pip install conversus-swe
# Enables: code review mode with extraction, scaffolds, verdict logic

# Everything
pip install conversus[all]
```

---

## 5. Feature Gating

### Detection (not enforcement)

```python
# In engine, when plugin loading occurs:
try:
    from conversus.plugins.nashopt import EquilibriumScorer
    SOLVERS_AVAILABLE = True
except ImportError:
    SOLVERS_AVAILABLE = False
    # Deliberation runs without scoring — no error, no nag
```

No license key validation in v1. The gating mechanism is simply: installed = available, not installed = silent skip. License enforcement is a future spec.

### No Nag Screens

When a user runs without `conversus-solvers`:
- Deliberation completes normally (all 5-6 phases)
- No "upgrade to unlock" messages
- No degraded output
- The synthesis and disputes are the full output

The paid tier is additive. The free tier is not a crippled version.

---

## 6. Documentation Tiers

| Site | Content | Auth | Tier |
|------|---------|------|------|
| `docs.conversus.dev` | Engine, modes, CLI, templates, presets, plugin/domain ABCs, blog | Public | Free |
| `portal.conversus.dev` | Scorer guides, Kalman docs, AMPL docs, payoff function reference, domain implementation guides | API key / SSO | Paid |
| Internal (monorepo) | ADRs, infra, deployment | Org-only | Internal |

### Cross-Tier Linking

Public docs reference premium features with callouts:

```markdown
!!! info "Premium Feature"
    Equilibrium scoring provides quantitative analysis of deliberation quality.
    Available with `pip install conversus-solvers`.
    [Learn more →](https://portal.conversus.dev/scoring/)
```

---

## 7. Functional Requirements

### Tier Boundary
- **FR-001**: `pip install conversus` MUST have zero imports from `conversus-solvers` or any paid package.
- **FR-002**: Free tier MUST run complete deliberations (all 8 modes, 5-6 phases) without paid packages.
- **FR-003**: Paid packages MUST import from free tier via documented public APIs only.
- **FR-004**: Removing paid packages MUST NOT degrade free tier behavior.

### Feature Gating
- **FR-005**: Plugin loading MUST silently skip unavailable paid plugins.
- **FR-006**: No "upgrade" messages in free tier output.
- **FR-007**: `PluginResult.data["solver"]` MUST report `"none"` (free) vs `"heuristic"` / `"nashopt"` / `"ampl-highs"` (paid).

### Licensing
- **FR-008**: Free packages: Apache-2.0 license (amended from MIT per spec 052 arbiter ruling 2026-04-07).
- **FR-009**: Paid packages: commercial license file with clear terms.
- **FR-010**: License key enforcement deferred to future spec.

### Documentation
- **FR-011**: Public docs MUST cover all free-tier features completely.
- **FR-012**: Premium portal MUST be auth-gated.
- **FR-013**: Blog MUST be public and ungated.
- **FR-014**: Cross-tier links MUST use callout pattern (never broken links).

---

## 8. Success Criteria

- **SC-001**: `pip install conversus` → `conversus run` produces synthesis with zero scoring output.
- **SC-002**: `pip install conversus-solvers` → same run adds scoring/convergence output.
- **SC-003**: `import conversus` never triggers nashopt/jax/amplpy/highspy import.
- **SC-004**: Free tier test suite passes with paid packages uninstalled.
- **SC-005**: README clearly shows free vs paid matrix.

---

## 9. Constraints

- No retroactive paywalling of existing free functionality.
- No time-limited trials or feature countdown.
- Heuristic payoff functions are part of the paid `conversus-solvers` package, not the free core.
- The paid tier is additive — it never replaces or degrades the free tier.
- License enforcement (key validation) is out of scope for this spec.
