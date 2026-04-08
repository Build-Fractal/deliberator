# Spec Execution Order

**Goal**: Get to spec 032 (package splitting) ASAP so users can `pip install conversus`.
**Updated**: 2026-04-02

---

## Done (moved to specs/done/)

| Spec | Title | Completed |
|------|-------|-----------|
| 001-030 | Core engine, schemas, plugins, domains, modes, solvers | Pre-031 |
| 031 | Documentation system + 55-agent review + blog | 2026-04-02 |
| 034 | Kalman convergence fixes (9 items) | 2026-04-01 |
| 035 | Plugin framework fixes (5 items) | 2026-04-01 |
| 036 | Mode template fixes (6 items) | 2026-04-01 |
| 037 | Validation flow fixes (7 items) | 2026-04-01 |
| 038 | Solver equilibrium fixes (3 spec amendments + docs) | 2026-04-02 |
| 039 | New mode payoffs (4 functions + tests + docs) | 2026-04-02 |
| 032 | Package splitting (build-time, 4 wheels) | 2026-04-03 |
| 033 | Free/paid tier gating (deliberation free, scoring paid) | 2026-04-03 |

---

## Wave 2: MIT-1 — Runtime Coupling Validation (DONE 2026-04-02)

**Completed**: 5 parallel agents, 8 production BREAKS fixed, 1 import violation fixed, 31 split tests added.

**What shipped**:
- `conversus/paths.py` — central path resolution via `importlib.resources` + fallback
- Fixed 7 files with `Path(__file__).parent` traversal (engine, linter, schemas, domains)
- `pyproject.toml` — `force-include` for schema/, templates/, presets/ in wheel
- Duplicated `estimate_cost` into optimizer to remove engine.cost cross-package dependency
- `tests/test_package_split.py` — 31 tests verifying package independence (all pass)

---

## Wave 3: 032 — Package Splitting (the goal)

Execute after MIT-1 passes. This is the spec that makes `pip install conversus` work.

**Effort**: ~6 hours (mechanical extraction + pyproject.toml per package).
**Tasks**:

### Phase A: Extract free-tier packages
1. Create `conversus-schemas/` with its own pyproject.toml from `conversus/schemas/`
2. Create `conversus-plugins/` (framework only) from `conversus/plugins/base.py`, `config.py`
3. Create `conversus-domains/` (framework only) from `conversus/domains/base.py`, `store.py`, `api.py`
4. Core `conversus` keeps `engine/`, `linter/`, `web/`, `SKILL.md`, `templates/`, `presets/`
5. Verify: `pip install conversus` in clean venv works, runs all 8 modes

### Phase B: Extract premium packages
6. Create `conversus-nashopt/` from `conversus/plugins/nashopt/`
7. Create `conversus-ampl/` from `conversus/plugins/optimizer/`
8. Create `conversus-scenarios/` from `conversus/plugins/scenarios/`
9. Create `conversus-swe/` from `conversus/domains/implementations/code_review/`
10. Verify: premium packages install on top of free tier, uninstalling reverts to heuristic

### Phase C: Documentation split
11. Update all import paths across docs/
12. Rewrite docs/index.md Quick Install for `pip install conversus`
13. Add per-package README.md files
14. Verify: `mkdocs build` passes with updated paths

### Phase D: CI + publish
15. Add CI workflow per package (test in isolation)
16. Publish to PyPI (or TestPyPI for validation)
17. Verify: `pip install conversus` from PyPI works end-to-end

**Docs**: Complete docs tier split per spec 032 Section 2b

---

## Wave 3b: 033 — Monetization Partitioning (~2h)

Execute immediately after 032. Defines free vs paid boundary. Unblocks everything downstream.

**Principle**: Deliberation is free. Scoring is paid.

Free tier (`pip install conversus`): 8 modes, 5-6 phases, templates, presets, CLI, MCP, web UI.
Paid tier (`pip install conversus-solvers`): Heuristic payoffs, equilibrium scoring, convergence prediction, config optimization, nashopt, AMPL.

---

## Wave 4: Platform & Enhancement (parallel, after 032+033)

### 042 — Execution Provider Abstraction
Decouple engine from Claude Code. `ExecutionProvider` protocol + ACP alignment. Enables CI/CD, headless execution, multi-SDK support.

### 040 — Command Center
Non-technical dashboard + co-pilot. Requires execution providers (042) for headless backend.

### 043 — AMPL Game-Theoretic Solvers
Formal optimization models for 6 modes. NL game theory enforced with optimization modeling. Adds consistency and tunability to the paid scoring tier. Heuristics remain as the implementation — AMPL adds the formal parameter interface.

### 044 — AMPL Model Templates & Self-Modeling
Template library of AMPL models indexed by game form. Feature binding, agent skills, self-modeling. Likely needs sub-spec breakdown.

### 046 — Commentator Agents (Verbose Mode)
Two optional commentator agents (play-by-play + color commentary) that run after synthesis to produce narrative output. Spans composed runs, populates graph/vector DBs, enables cross-run pattern detection. Opt-in via `verbose: true`. Post-hoc mode lets users generate commentary on already-completed runs.

### 047 — Structured Duration Parser & Temporal Classifier
Replaces regex-based `_CONSTRAINT_PATTERN` in `linter/question_classifier.py` with a structured duration parser. Returns `TemporalMatch` objects with `Duration` + category (deadline/performance/schedule/ttl/window/latency_bound). Unblocks: negotiation mode time-ranged ZOPA, scenario queries on durations, governance SLA enforcement, commentator timing.

### 048 — Autonomous Governance Mode ("CLI that runs outside your CLI")
Conversus as a background quality gate. Project declares governance docs (CONSTITUTION.md, AGENTS.md, CLAUDE.md) in `.conversus/.conversusrc`. Arbiter auto-grounds from those docs on every `conversus governance` invocation. CI invokes via `conversus governance --gate pr` with exit codes (0=PASS, 1=BLOCK, 2=ERROR, 3=META_DISPUTE). Turns conversus from a tool into infrastructure. HARD DEPENDENCY on 042 (**Accepted 2026-04-05** — unblocked). Depends on 046 (commentary in PR comments), 047 (SLA duration enforcement). 10 open questions from the user.

### 049 — Conversus as Universal Skill & MCP Server
Ships conversus to every IDE/agent host. Three artifacts: (a) `conversus-mcp-server` exposes 8 free + 4 paid MCP tools for any MCP-speaking host (Copilot, Cline, Continue, Roo Code, Augment, Cursor), (b) VSCode extension provides the rich UX (sidebar, command palette, diagnostics, arbitration renderer) — VSCode-first because it's the largest IDE audience and Microsoft-owned (same as GitHub which runs spec 048's CI gate), (c) APM cross-compiles single `.apm/` source tree to host-specific artifacts. Free-tier tools succeed with base install; paid-tier tools return structured `PAID_TIER_REQUIRED` error without paid package. HARD DEPENDENCY on 042. Runs in parallel with 042 implementation so both ship in the same sprint window. Spec 050 (JetBrains plugin + Agent Client Protocol) tracked as separate future work.

### 041 — Plan of Attack
Strategy document. Phases 0-1 map to waves 2-3 above. Phases 2+ are post-user-validation.

---

## Critical Path

```
Wave 1 (parallel):  038 (1h) + 039 (3h)     ← DONE 2026-04-02
Wave 2 (serial):    MIT-1 (4h)               ← DONE 2026-04-02
Wave 3 (serial):    032 build-time split (2h) ← DONE 2026-04-03
Wave 3b (serial):   033 free/paid tiers (2h)  ← DONE 2026-04-03
Wave 4 (parallel):  042 + 040 + 043 + 044 + 046 + 047 + 048 ← platform ← YOU ARE HERE
                                              ─────────────────────
                                              pip install conversus READY
```
