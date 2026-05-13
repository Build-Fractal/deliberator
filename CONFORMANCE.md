# conversus-oss — Conformance Declaration

**Suite:** conversus
**Inherits from:**
- `https://github.com/Build-Fractal/build-fractal-mono/blob/main/build-fractal/CONSTITUTION.md` (Tier 1 — Universal, v1.0.0 ratified 2026-05-07 with v4.0.0)
- `https://github.com/Build-Fractal/build-fractal-mono/blob/main/build-fractal/conversus/CONSTITUTION.md` (Tier 2 — Suite, v1.0.0 ratified 2026-05-07 with v4.0.0)

**Component constitution:** `CONSTITUTION.md` (this repo) — currently v3.2.3, the canonical source for all three tiers until v4.0.0 ratifies the split.

**Admission deliberation:** `deliberations/v4.0.0-tier-extraction-originating-2026-05-06/` Q2 ADMIT-PROVISIONAL.

**Status:** Provisional — admitted via v4.0.0 tier-extraction (2026-05-07); all Batch-1 Provisional remediations closed 2026-05-11. XII closed 2026-05-09 by `linter/dead_infra.py` + CI wiring. V closed 2026-05-11 by cross-mode parametrization in `linter/test_output_contract.py`. XXII closed 2026-05-11 by per-channel vendoring gates in `.github/workflows/distribution-surface-integrity.yml`. XXVI closed 2026-05-11 by `engine/tests/test_mode_provider_matrix.py`. XXIV closed 2026-05-11 by `SAFETY.md` enumerating 10 named perimeters and their independent guards. Tier 2 Principle XXVIII (Persistence Contract Discipline) admitted Provisional 2026-05-12 via spec v4.1.0 (commit `e0f5a74`) — remediation deadline 2026-12-01. Implementation discipline ratified 2026-05-13 via spec v4.2.0 (Component Principle XXIX); remediation is now in-progress per the ratified spec's § 11 implementation order with cliff date **2026-12-01** retained.

**Last re-audit:** 2026-05-13 (spec v4.2.0 ratification — Component Principle XXIX added; XXVIII remediation status: in-progress per ratified spec).

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
| XXIV | Safety-Critical Defense-in-Depth | Satisfied | `SAFETY.md` enumerates 10 named perimeters (P1 user-config YAML, P2 MCP tool surface, P3 deliberation-sandbox file IO, P4 capability metadata → generated source, P5 synthesis text → downstream gates, P6 arbiter resolution.md → next-round, P7 subprocess execution, P8 provider rate-limit response, P9 settings cascade, P10 ad-hoc display name) with their independent guards cited at file:line. All 10 perimeters defense-in-depth-compliant; three single-guard follow-ons (JSONL streaming parsing, env-var typo tolerance, `literal()` repr fallback) logged in SAFETY.md tail section. **Closed 2026-05-11**. |
| XXV | Live Test Cost Discipline | Satisfied | Live tests opt-in only via env vars; mock provider is default. Cost tracking in conftest.py. |
| XXVII | Operator-Configurable Tool Surface | Satisfied | Per-surface tool inventory: CLI (`engine/cli/`), MCP (`mcp_server.py`), claude-code-plugin (`claude-code-plugin/skills/`), .mcpb bundle (separate repo plan). Each enumerated, no accidental surface. |
| XXVIII | Persistence Contract Discipline | In-progress | Implementation discipline ratified 2026-05-13 via spec v4.2.0 (Component Principle XXIX). Remediation is now in-progress per ratified spec § 11 implementation order. Tier 2 anchor: ratified into Tier 2 via spec v4.1.0 (commit `e0f5a74`) and `build-fractal/conversus/CONSTITUTION.md` (commit `551f647` in `clariti-care/payer-index-mono`). Remediation scope for conversus-oss: structured-output migration (V principle un-xfail — the marker-tier dispute parser gap pinned `strict xfail` in `linter/test_output_contract.py`) and schema declaration coverage for engine persisted artifacts (deliberation outputs, presets, dispatch payloads). Deadline **2026-12-01** per amendment C7. |

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
| XXVI | Meta-Testing | Satisfied | `engine/tests/test_mode_provider_matrix.py` (added 2026-05-11) closes the cross-product gap: 8 modes × {`mock`, `demo`} = 16 cell-runnable end-to-end pipeline runs, plus 13 dispatch-only provider instantiation checks covering every other registered provider (`anthropic`, `openai`, `claude-code`, `claude-desktop`, `aider`, `opencode`, `codex`, `copilot`, `gemini`, `pi`, `ollama`, `llama-cpp`, `vllm`). Live LLM calls are excluded per Principle XXV. Source-of-truth meta-assertions tie the parametrize breadth to `conversus.schemas.modes.VALID_MODES` and `engine.execution.providers.PROVIDER_REGISTRY`; adding a new mode or provider without updating the matrix trips the meta-test. **Closed 2026-05-11**. |

---

## Provisional remediation plan

| Principle | Gap | Remediation | Deadline | Tracking |
|---|---|---|---|---|
| ~~V (Observable Deliberation)~~ | ~~Output_contract cross-mode coverage not verified~~ | **CLOSED 2026-05-11**: `linter/test_output_contract.py` parametrizes over all 8 modes (`TestCrossModeMetadataCoverage`, `TestCrossModeDisputeCoverage`). Coverage surfaced a marker-tier dispute parser gap in 6 of 8 modes; gap pinned as `strict xfail` and tracked as a separate output-contract follow-on. | ~~2026-08-01~~ | Closed |
| ~~XII (No Dead Infrastructure)~~ | ~~No automated dead-code linter~~ | **CLOSED 2026-05-09**: `linter/dead_infra.py` shipped. Schema variables must reference at least one template OR carry a `consumer:` annotation. CI gate in `.github/workflows/linter-checks.yml`. | ~~2026-07-01~~ | Closed |
| ~~XXII (Distribution Surface Integrity)~~ | ~~Per-channel vendoring rules not in CI~~ | **CLOSED 2026-05-11**: `.github/workflows/distribution-surface-integrity.yml` shipped. Three SHIP-blocking jobs: `pypi-wheel` (build + clean-venv install + smoke import + force-include assertion + console-script resolution), `mcpb-bundle` (mirror `release-mcpb.yml` vendoring + manifest sync from pyproject + registry, archive structural integrity check), `plugin-marketplace` (JSON structural validation + version/name coherence between marketplace.json and plugin.json). Cross-repo .mcpb bundling with conversus-enhanced remains a follow-on spec gated on conversus-enhanced's own XXII closure. | ~~2026-08-01~~ | Closed |
| ~~XXIV (Safety-Critical Defense-in-Depth)~~ | ~~Named perimeters not enumerated~~ | **CLOSED 2026-05-11**: `SAFETY.md` enumerates 10 named perimeters with independent guards cited file:line. 10/10 defense-in-depth-compliant; three single-guard follow-ons (JSONL streaming parsing, env-var typo tolerance, `literal()` repr fallback) logged in SAFETY.md tail section for future investment. | ~~2026-09-01~~ | Closed |
| ~~XXVI (Meta-Testing)~~ | ~~(Mode × provider) cross-product coverage not confirmed~~ | **CLOSED 2026-05-11**: `engine/tests/test_mode_provider_matrix.py` exercises 8 modes × {mock, demo} end-to-end (16 cells) plus 13 dispatch-only provider instantiation checks. Source-of-truth assertions pin the matrix to `VALID_MODES` and `PROVIDER_REGISTRY` — any future mode or provider addition without a matrix update trips the meta-test. | ~~2026-08-01~~ | Closed |
| XXVIII (Persistence Contract Discipline) | Engine persisted artifacts (deliberation outputs, presets, dispatch payloads) not declared under a single structured-output schema; V principle parametrization closed 2026-05-11 surfaced a marker-tier dispute parser gap currently pinned `strict xfail`. | Structured-output migration: un-xfail the parser gap in `linter/test_output_contract.py` by emitting the marker-tier dispute payload from the engine in declared schema form, then extend schema declarations across engine persisted artifacts (deliberation outputs, presets, dispatch payloads) so each persisted surface has a single source of truth consumed by sibling products. Author `CONSUMER-CONTRACT.md` enumerating the stable surfaces. Spec v4.1.0 (commit `e0f5a74`) is the ratifying reference; Tier 2 CONSTITUTION.md commit `551f647` in `clariti-care/payer-index-mono`. Ratified 2026-05-13 via spec v4.2.0 (commit `24538e7`); Component Principle XXIX added. Implementation begins per spec § 11. | 2026-12-01 | In-progress (ratified spec) |

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

See `https://github.com/Build-Fractal/build-fractal-mono/blob/main/build-fractal/conversus/COMPLIANCE.md` for the contract definition this declaration conforms to.
