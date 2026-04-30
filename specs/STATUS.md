# Conversus Spec Status Index

**Generated 2026-04-29 from current repo state.**  
Source of truth: each spec's Status field. This index summarizes current implementation and acceptance state.

---

## Active Specs (Top-Level, Numbered)

### 047 — Duration Parser
**Status**: Active 2026-04-29 (promoted from draft) — bug fix (#4) + architecture gap identified; structured output needed by 3 downstream consumers. Implementation-ready.

### 048 — Autonomous Governance Mode
**Status**: Active 2026-04-29 (promoted from draft) — drift-analyzed + 3-agent deliberation resolved dependencies; specs 042/050/057 closed; governance config settled; implementation blockers documented.

### 056 — Deliberation Persistence
**Status**: Active 2026-04-29 (promoted from draft) — deliberation-revised, dependencies (055/057) closed, framing inverted to developer-first, workspace-scoped storage settled. Implementation-ready.

### 059 — Prompt and Skill Interface
**Status**: Active 2026-04-29 (promoted from draft) — deliberation-amended 2026-04-13, depends on 055 (closed), 5-prompt decision final, hybrid registry integration accepted. Implementation-ready.

### 061 — Engine Eval Suite
**Status**: Active (steps 1-6 of 14 complete per 2026-04-29 investigation; status line in spec self-claims "1-4 complete" but code shows 5-6 + parts of 9, 10, 12 also implemented — refresh needed; next: step 7 deepeval quality layer).

### 065 — Path to Open Source
**Status**: Draft v2 — amended to reference constitution v2.3.0 principles proposed by spec 066. Defines launch-readiness gate sequence and readiness checklist for repository publication.

### 067 — Verification Methodology
**Status**: Active — re-verification trigger + cost reporting added 2026-04-27; §4.6 added 2026-04-29 (PR #47) binding 4-subagent investigation pattern as canonical first response when verification surfaces failing tests.

### 070 — Grandfathered Audit
**Status**: Draft v1 with PASS WITH FIXES verdict applied 2026-04-29 (per `deliberations/070-spec-review-2026-04-28/`): SPLIT verdict on Principle XVI flipped to FAIL+Option A; Goal #6 added (operational impact assessment); §4 methodology statement added; §5.2 dual-purpose cost note added.

### 071 — Test-Fix Boundary Preservation (Principle XXVIII)
**Status**: Ratified-with-override 2026-04-29. `CONSTITUTION.md` v2.5.0 added Principle XXVIII (v2 wording). Self-consistency PASS WITH FIXES. Blind v2 PASS WITH FIXES — rulings 1 and 2 overridden with rationale in `CONSTITUTIONAL_CONVERSATIONS.md`. Three follow-up PRs (#47, #48, #49) merged.

---

## Closed Specs (in `specs/done/`, 59 total)

**Specs 001–069 (representative list):**  
001-subject-arbitration, 004-preset-agents, 004-universal-rounds, 005-generalized-templates, 005-p2p3-backlog-hardening, 006-inter-round-arbitration (closed 2026-04-30 after Phase 2 — PRs #65/#66/#67/#69 + closing PR), 007-game-engine, 007-subcommand-dispatch-define, 008-executable-conversus, 008-interests-mode, 009-guided-execution, 010-antipattern-steering, 010-guided-arbitration, 011-adoption-harness, 011-phase-consensus-gates, 011a-skill-breakdown, 012-game-form-schemas, 012-spec-hygiene, 013-objective-function-templates, 014-guided-objective-construction, 015-feature-extraction, 016-plugin-system, 017-equilibrium-scorer, 018-convergence-predictor, 019-config-optimizer, 020-scenario-storage, 021-nashopt-integration, 022-kalman-convergence, 023-ampl-config-optimizer, 024-cross-plugin-interfaces, 025-game-form-expansion, 026-optimization-template-library, 027-solver-validation-flow, 028-mode-expansion, 029-code-review-domain, 030-domain-plugin-architecture, 031-docs-and-vercel-compliance, 032-package-splitting, 033-monetization-partitioning, 034-kalman-convergence-fixes, 035-plugin-framework-fixes, 036-mode-template-fixes, 037-validation-flow-fixes, 038-solver-equilibrium-fixes, 039-new-mode-payoffs, 042-execution-providers, 045-test-coverage-review, 050-cascading-settings, 052-open-source-extraction, 054-public-documentation, 055-capability-registry, 057-settings-architecture (re-closed 2026-04-30 after Phase 2 SCs — PRs #71/#72/#74), 064-capability-discovery, 066-constitution-v2.3.0, 068-principle-xvi-fix, 069-mechanical-verification-gate, 072-credential-source-display (shipped 2026-04-30 — PR #76), 998-phase-consensus-gates, 999-decision-framework.

(057 was previously here; reopened 2026-04-29 — see Active Specs above.)

---

## Draft Specs (in `specs/draft/`, 8 total)

### 043 — AMPL Game Solvers
**Status**: Draft

### 044 — AMPL Model Templates
**Status**: Draft — likely needs breakdown into sub-specs (template infra, binding system, agent skill, self-modeling)

### 046 — Commentator Agents
**Status**: Draft

### 049 — Universal Skill MCP Server
**Status**: Draft — partial-close: FastMCP core + 3/5 v1 tools shipped; VSCode extension + APM targets unstarted; 6 drift vectors documented in DRIFT-REPORT.md (issues #62, #63 capture HIGH-severity remaining work).

### 051 — Sandbox Test Harness
**Status**: Draft

### 053 — Public CI Pipeline
**Status**: Draft — partial: 2 workflows exist but not under prescribed names; gaps: lint job, codecov, pytest markers, PyPI release.

### 058 — Typed Pipeline Output
**Status**: Draft (placeholder — implement after 057)

### 060 — MCP Sampling Provider
**Status**: Draft — Desktop Extension UX blocker; sampling/createMessage protocol defined; depends on 055 (closed) + MCP server.

---

## Archived Specs (in `specs/archive/`)

### 001 — Speckit Orchestrator
Empty stub; original orchestrator concept decomposed into specs 007-010 (now in done/).

### 040 — Command Center
Archived 2026-04-29 — vision-phase only with no DRIFT activity; 5 prior-spec dependencies all active/done; no code references found. Preserved in archive/ as historical product vision.

### game-engine-vision
Long-term north star, intentionally archived.

---

## Meta Files

- **README.md**: Spec lifecycle rules and promotion guidance. Authoritative source for directory-to-status mapping.
- **EXECUTION-ORDER.md**: Recommended sequencing for implementation work (last updated 2026-04-02; stale through Wave 4+).
- **AUDIT-2026-04-27.md**: Hygiene audit (stale by 2 days; PR #39 closed multiple specs that the audit listed as active — now reflected in this STATUS.md rebuild).
- **CONSTITUTION.md**: Governance framework (v2.5.0 as of 2026-04-29).
- **CONSTITUTIONAL_CONVERSATIONS.md**: Deliberation logs for all constitutional amendments. Inaugural override-with-rationale entry 2026-04-29.
- **plan-of-attack.md** / **plan-of-attack.conversus**: Operational roadmap (non-spec workspace).

---

## Landscape Summary

**Active work**: 11 specs.
- Constitutional/governance: 065, 067, 070, 071
- Engine completion: 006 (Phase 2), 057 (reopened SCs), 061 (next: deepeval)
- Promoted from draft 2026-04-29: 047, 048, 056, 059

**Closed**: 56 specs across core engine, plugins, UX, platform compliance, and governance.

**Drafts**: 8 specs in idea phase, mostly infrastructure (sandbox, CI, MCP sampling) and AMPL/optimization (043, 044, 060).

**Archived**: 3 historical artifacts (001 stub, 040 vision-only, game-engine-vision).

**Total**: 78 spec artifacts across the lifecycle.

**Trajectory**: post-v2.5.0 landscape is split between **completion work** (006 Phase 2, 057 SCs, 061 deepeval) and **promoted-from-draft new feature work** (047, 048, 056, 059). Constitutional governance has stabilized at the v2.5.0 anchor; next amendment cycle will carry the deferred Q3 must-quote anchor (per `deliberations/session-review-2026-04-29/arbiter/resolution.md`).
