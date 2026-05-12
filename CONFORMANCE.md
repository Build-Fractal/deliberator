# conversus-oss — Conformance Declaration

**Suite:** conversus
**Inherits from:**
- `https://github.com/clariti-care/payer-index-mono/blob/main/build-fractal/CONSTITUTION.md` (Tier 1 — Universal, v1.0.0 ratified 2026-05-07 with v4.0.0)
- `https://github.com/clariti-care/payer-index-mono/blob/main/build-fractal/conversus/CONSTITUTION.md` (Tier 2 — Suite, v1.0.0 ratified 2026-05-07 with v4.0.0)

**Component constitution:** `CONSTITUTION.md` (this repo) — currently v3.2.3, the canonical source for all three tiers until v4.0.0 ratifies the split.

**Admission deliberation:** `deliberations/v4.0.0-tier-extraction-originating-2026-05-06/` Q2 ADMIT-PROVISIONAL.

**Status:** Provisional — admitted via v4.0.0 tier-extraction (2026-05-07); 2 open remediations (XXIV, XXVI). XII closed 2026-05-09 by `linter/dead_infra.py` + CI wiring. V closed 2026-05-11 by cross-mode parametrization in `linter/test_output_contract.py`. XXII closed 2026-05-11 by per-channel vendoring gates in `.github/workflows/distribution-surface-integrity.yml`.

**Last re-audit:** 2026-05-07 (post v4.0.0 ratification + blind verification surfaced V/XXIV/XXVI Provisional updates).

---

## Tier 1 declarations

| # | Principle | Status | Evidence / Rationale |
|---|---|---|---|
| I | Spec-Driven Development | Satisfied | `specs/` directory with 21 active specs. Every behavioral change carries a spec; documented in CONSTITUTION.md and CONTRIBUTING.md. |
| II | Stable Interfaces | Satisfied | Stable interfaces enumerated in CONSTITUTION.md § Principle II (markers, template variables, dispatch table, principle numbers, file paths, schema variables). CHANGELOG.md tracks breaking changes. |
| III | Backward-Compatible Extension | Satisfied | All recent feature additions (preset, rounds, stagnation, arbiter, iterations) added as optional fields; CHANGELOG distinguishes Added/Changed/Deprecated/Removed. |
| IV | Documentation Is the Product | Satisfied | Per-skill `claude-code-plugin/skills/{name}/SKILL.md` files; CONSTITUTION.md, CONSTITUTIONAL_CONVERSATIONS.md, CONTRIBUTING.md, docs/ all carry normative content. STATUS.md maintained. |
| VII | Reproducibility | Satisfied | `uv.lock` committed; pinned Python 3.12; templates deterministic per Principle VII enforcement. |
| VIII | Templating Engines | Satisfied | Templates under `templates/{mode}/` use `{VARIABLE}` syntax driven by `schema/variables.yml`. Linter (`linter/validate.py`) enforces variable contract. |
| IX | Functional Programming | Satisfied | Engine code is function-based (`engine/handlers.py`, `engine/run.py`, `engine/settings.py`). Class-based code limited to data containers (Pydantic models, dataclasses). Type hints enforced. |
| XI | Single Source of Truth | Satisfied | `schema/variables.yml` is canonical for template variables; `STATUS.md` for spec status; CONSTITUTION.md for principles. Cross-references over duplication. |
| XIV | Spec-Implementation Parity | Satisfied | `linter/validate.py` enforces template ↔ schema parity. CI runs the linter. Specs link to implementation PRs and back. |
| XXVIII | Test-Fix Boundary Preservation | Satisfied | PR review enforces; ratified post-gate (Principle XXVIII passed Constitutional Inclusion Criteria). |

---

## Tier 2 declarations

| # | Principle | Status | Evidence / Rationale |
|---|---|---|---|
| V | Observable Deliberation | Satisfied | Phase progress reporting in engine; output validation via `linter/output_contract.py`. Cross-mode coverage verified: `linter/test_output_contract.py` parametrizes over all 8 modes (`TestCrossModeMetadataCoverage`, `TestCrossModeDisputeCoverage`). **Closed 2026-05-11**. |
| XII | No Dead Infrastructure | Satisfied | `linter/dead_infra.py` enforces schema → templates parity: every variable in `schema/variables.yml` with declared `phases:` must either appear in at least one matching template or carry an explicit `consumer:` annotation naming its orchestrator consumer. CI runs the linter on every PR (`.github/workflows/linter-checks.yml`). **Closed 2026-05-09**. |
| XIII | Enum Completeness | Satisfied | Mode enum (`cooperative`, `winner-take-all`, `prisoners-dilemma`, `red-blue`, plus 4 game-engine modes) exhaustively dispatched. Phase enum (1-6) fixed. |
| XV | Plugin Isolation | Satisfied | Plugin entry-points (`conversus.solvers`, `conversus.domains`) declared as the suite's monetization seam. OSS layer carries no proprietary modules. spec 016 codifies the boundary. |
| XVI | Mathematical Transparency | Satisfied | Scoring code in `engine/` documented and deterministic. v3.2.3 disambiguated "shape" vs "assembly form" terminology to remove cross-principle collision with IX. |
| XXII | Distribution Surface Integrity | Satisfied | Per-channel vendoring gates in `.github/workflows/distribution-surface-integrity.yml`: (1) PyPI wheel built with `uv build`, installed into a clean venv with `pip install 'conversus[mcp]'`, smoke imports `conversus`, `engine`, `linter`, `mcp_server`, `capabilities` and resolves both console scripts; (2) .mcpb bundle vendored via the same pipeline as `release-mcpb.yml` (pip --target into `desktop-extension/server/lib`, copy `presets/`/`schema/`/`templates/`, sync `manifest.json` version + tools[] from `pyproject.toml` + `capabilities.CAPABILITIES`), then archive opened and asserted to contain required paths plus version coherence with pyproject; (3) plugin marketplace JSON files structurally validated and version + name asserted coherent between `.claude-plugin/marketplace.json` and `claude-code-plugin/.claude-plugin/plugin.json`. **Closed 2026-05-11**. |
| XXIII | Provider Robustness Contract | Satisfied | All 12 providers (`anthropic`, `openai`, `claude-code`, `aider`, `opencode`, `codex`, `copilot`, `gemini`, `pi`, `ollama`, `mock`, `demo`) conform to `engine/providers/base.py` contract. Tested via `engine/tests/test_concrete_providers.py`. |
| XXIV | Safety-Critical Defense-in-Depth | Provisional | Multiple guards on prompt-injection (output sanitization in synthesis), deliberation drift (stagnation detection), antipattern catalog. **Gap surfaced by 2026-05-06 originating deliberation:** named perimeters and their independent guards not enumerated; "multiple guards" without enumeration is vague. **Remediation:** enumerate perimeters in CONSTITUTION.md or a sibling SAFETY.md (deadline: 2026-09-01). |
| XXV | Live Test Cost Discipline | Satisfied | Live tests opt-in only via env vars; mock provider is default. Cost tracking in conftest.py. |
| XXVII | Operator-Configurable Tool Surface | Satisfied | Per-surface tool inventory: CLI (`engine/cli/`), MCP (`mcp_server.py`), claude-code-plugin (`claude-code-plugin/skills/`), .mcpb bundle (separate repo plan). Each enumerated, no accidental surface. |

---

## Component-tier declarations

These component-tier principles will remain in `conversus-oss/CONSTITUTION.md` after v4.0.0 ratification.

| # | Principle | Status | Evidence |
|---|---|---|---|
| XVII | Content Classification | Satisfied | spec 033 monetization partition codifies free vs paid surface; conversus-oss is the canonical free side. |
| XVIII | Progressive Disclosure | Satisfied | Capability discovery surface tiered by operator authentication. spec 064 / 064.1 establish runtime registration. |
| XIX | Non-Extractable Core | Satisfied | OSS engine is the truth; paid layers extend via plugin entry-points, not by reimplementation. |
| XX | Decomposition Mechanism Precedence | Satisfied | Documented order: plugin entry-point → preset composition → spec-driven mode → constitutional amendment. |
| XXI | Extraction Ordering | Satisfied | Documented sequence: spec → tests → implementation → templates → docs → constitution. |
| XXVI | Meta-Testing | Provisional | Parametrized capabilities (modes, presets, providers) have meta-suites (`engine/tests/test_skill_engine.py` parametrizes across all modes; `test_concrete_providers.py` across all providers). **Gap surfaced by 2026-05-06 originating deliberation:** parametrization breadth claimed but not confirmed — does test_skill_engine.py hit every (mode × provider) cell or just cooperative × mock? **Remediation:** confirm cross-product coverage; add missing cells if any (deadline: 2026-08-01). |

---

## Provisional remediation plan

| Principle | Gap | Remediation | Deadline | Tracking |
|---|---|---|---|---|
| ~~V (Observable Deliberation)~~ | ~~Output_contract cross-mode coverage not verified~~ | **CLOSED 2026-05-11**: `linter/test_output_contract.py` parametrizes over all 8 modes (`TestCrossModeMetadataCoverage`, `TestCrossModeDisputeCoverage`). Coverage surfaced a marker-tier dispute parser gap in 6 of 8 modes; gap pinned as `strict xfail` and tracked as a separate output-contract follow-on. | ~~2026-08-01~~ | Closed |
| ~~XII (No Dead Infrastructure)~~ | ~~No automated dead-code linter~~ | **CLOSED 2026-05-09**: `linter/dead_infra.py` shipped. Schema variables must reference at least one template OR carry a `consumer:` annotation. CI gate in `.github/workflows/linter-checks.yml`. | ~~2026-07-01~~ | Closed |
| ~~XXII (Distribution Surface Integrity)~~ | ~~Per-channel vendoring rules not in CI~~ | **CLOSED 2026-05-11**: `.github/workflows/distribution-surface-integrity.yml` shipped. Three SHIP-blocking jobs: `pypi-wheel` (build + clean-venv install + smoke import + force-include assertion + console-script resolution), `mcpb-bundle` (mirror `release-mcpb.yml` vendoring + manifest sync from pyproject + registry, archive structural integrity check), `plugin-marketplace` (JSON structural validation + version/name coherence between marketplace.json and plugin.json). Cross-repo .mcpb bundling with conversus-enhanced remains a follow-on spec gated on conversus-enhanced's own XXII closure. | ~~2026-08-01~~ | Closed |
| XXIV (Safety-Critical Defense-in-Depth) | Named perimeters not enumerated | Enumerate perimeters + independent guards in CONSTITUTION.md or sibling SAFETY.md | 2026-09-01 | TBD issue |
| XXVI (Meta-Testing) | (Mode × provider) cross-product coverage not confirmed | Audit test_skill_engine.py parametrization; add missing cells if any | 2026-08-01 | TBD issue |

---

## Relief claims

*None.*

---

## Re-audit cadence

This declaration is re-audited:
- Annually (next: 2027-05-06).
- On any constitutional amendment that touches Tier 1 or Tier 2 (the v4.0.0 tier extraction will trigger the first formal re-audit).
- On any structural change to this repo (added surfaces, removed providers, etc.).

---

## Status & Provenance

This declaration was created 2026-05-06 as part of Phase A.5 of the build-fractal hierarchical constitution stand-up. It pre-dates the v4.0.0 ratification deliberation that will formally admit conversus-oss to the suite.

Until v4.0.0 ratifies, this file is **advisory** — it documents the intended compliance position but is not enforceable as a deliberation-grounded admission. Upon v4.0.0 ratification:
- The admission deliberation reference at the top will be filled in.
- Status will flip from `Implicit-Provisional` to `Compliant` (or `Provisional` if remediation deadlines extend past ratification).
- The first formal re-audit cycle begins.

See `https://github.com/clariti-care/payer-index-mono/blob/main/build-fractal/conversus/COMPLIANCE.md` for the contract definition this declaration conforms to.
