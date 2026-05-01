# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.4.0] - 2026-05-01

The "Principle XXVIII era" — constitutional discipline established and applied across 30+ PRs.

### Added

- **Constitution v2.5.0 — Principle XXVIII (Test-Fix Boundary Preservation)** ratified with override-with-rationale precedent (#46).
- **Operational scaffolding for XXVIII**: `.github/pull_request_template.md` with structured `test-fix-category` marker (#48), `scripts/lint-test-fixes.py` advisory CI lint with skip-discipline + diff-shape consistency checks (#49), spec 067 §4.6 binding the 4-subagent investigation pattern as canonical first response (#47).
- **Spec 047 (Duration Parser) Phases 1-4**: new `conversus/schemas/duration.py` with `Duration`, `TemporalMatch`, 5-tier parser (ISO 8601 / numeric+unit / colloquial / fiscal / category inference) covering 7 temporal categories. Replaces `_CONSTRAINT_PATTERN` regex in `linter/question_classifier.py`. Adds `extract_temporal_constraints()` API (#82).
- **Spec 061 step 7 — deepeval quality layer**: `engine/tests/test_evals.py` with 5 GEval metrics (Review Independence, Cross-Review Adversarial, Revision Responsiveness, Dispute Specificity, Synthesis Grounding) per spec §3.2.1. All `@pytest.mark.eval`, excluded from default CI (#83).
- **Anthropic-backed deepeval judge**: `_build_judge()` factory using `AnthropicModel` instead of OpenAI default (#85).
- **Claude-code-subprocess judge** (`engine.eval_judge.ClaudeCodeJudge`): closes the OAuth-user gap so the deepeval suite runs without `ANTHROPIC_API_KEY` when both `CONVERSUS_EVAL_PROVIDER` and `CONVERSUS_EVAL_JUDGE_PROVIDER` are set to `claude-code` (#89).
- **Spec 057 SC-003 — settings cascade display**: `engine/handlers.py::status_cli` now shows per-key resolution (env / project / global / default) with new `inspect_settings_cascade` API (#71).
- **Spec 057 SC-004 — per-provider credentials**: storage moves from monolithic `~/.conversus/auth.json` to per-provider `~/.conversus/credentials/{provider}.json` with lazy migration, atomic writes (`os.replace` via `.tmp`), 0o700/0o600 permissions, and per-provider file lock with 200ms timeout (#74).
- **Spec 072 — credential source display**: per-provider source attribution in `conversus status` (per-provider-file / legacy-fallback / env-var / none) via `inspect_credential_source` (#76).
- **Spec 006 Phase 2 — inter-round arbitration completion**: 7 FRs across 5 PRs (#65, #66, #67, #69, #70). Strict validation (FR-003), `arbiter/`→`arbitration/` path rename (FR-006), round-loop parity test (FR-P2-3), template variable wiring (FR-P2-5), influence-aware dispute counting (FR-P2-4), cross-round Resolution Attribution (FR-P2-6), SC-002/003/007/008 end-to-end tests (FR-P2-7), `linter/arbitration_parser.py` (issue #68).

### Changed

- **`engine.dispatch._gated_dispatch` documented**: clarifies actual concurrency semantics (asyncio.gather across agents; fail-fast via `return_exceptions=True` + sequential post-processing). Corrects the prior session's deliberation miscall (#80).
- **`conversus init` writes `.conversus/settings.yml`** (was `settings.json`). Legacy `settings.json` files are preserved on disk and content is migrated on first init (#72).
- **`OutputManager.get_arbitration_path` returns `{base}/arbitration/resolution.md`** (was `{base}/arbiter/`). All path-aware tests updated (#65).
- **`decide --model X` flag** added; threads through to `run_engine` (#52). Regression tests in #56.
- **OAuth marker regex**: drops `subscription` token from preflight to eliminate the false-positive surface (#81).

### Fixed

- **Silent-stub deliberation** when claude-code subprocess returned an error string as agent content (Bug 3a). New `FatalProviderResponseError` aborts the pipeline rather than synthesizing the error string as if it were valid output (#52).
- **claude-code provider model leak** (Bug 3b): the legacy `claude-sonnet-4-20250514` literal substituted with the provider's own default to prevent OAuth sessions hitting unreachable models (#52).
- **`find_project_root` import shadowing** in `engine/handlers.py` (PR #42, pre-0.4.0 — referenced for context).
- **Stale `prior_arbitration_path`** after `retroactive_move_to_round_1` — Round 2's context builders received a path that no longer existed. Surfaced by FR-P2-3's parity test (#66).
- **Cross-round Resolution Attribution wiring void** — template had the section + placeholders shipped, but the runtime never populated `arbitration_paths`/`arbitration_rulings`. Surfaced by FR-P2-6 (#69).
- **Test isolation gap in SC-004**: pre-existing tests patched `DEFAULT_AUTH_PATH` only; with per-provider files now active, those tests would have started reading the user's real OAuth tokens. Fixed by pinning `DEFAULT_CREDENTIALS_DIR` everywhere `DEFAULT_AUTH_PATH` was already pinned (#74).
- **Principle XI single-source-of-truth violation in CLI status**: the `status` command duplicated auth logic instead of delegating to `status_cli` handler. Refactored to delegate (#71).

### Deprecated

- **`specs/EXECUTION-ORDER.md`**: deprecated 2026-05-01. Source of truth is now `specs/STATUS.md` + `git log specs/done/` + `CONSTITUTIONAL_CONVERSATIONS.md`. File preserved as historical artifact (#90).

### Specs closed in 0.4.0

`006`, `057`, `064`, `071`, `072`. Plus 4 reopened/promoted specs added to the active list (`047`, `048`, `056`, `059`) and 7 specs still in active development as of release.

### Verification trail

- **2 conversus deliberations** run during the session: session-review meta-review (verdict: ACCEPTED WITH RECOMMENDATIONS); SC-004 strategy review (verdict: SHIP WITH MODIFICATIONS, all applied).
- **6 production bugs caught by Principle XXVIII discipline** across the 30+ PRs: stale path (#66), wiring void (#69), test isolation gap (#74), Principle XI violation (#71), GEval lazy-init (#83), intrinsic keyword detection (#82), regex-greedy-newline edge case (#70).

### Cross-refs

- `CONSTITUTION.md` v2.5.0 (with override-with-rationale paragraph in SIR)
- `CONSTITUTIONAL_CONVERSATIONS.md` 2026-04-29 entry (governance log of the override)
- `deliberations/071-self-consistency-2026-04-28/`, `deliberations/071-blind-2026-04-28/`, `deliberations/071-blind-v2-2026-04-29/` (XXVIII verification trail)
- `deliberations/session-review-2026-04-29/`, `deliberations/057-sc4-migration-strategy-2026-04-30/`, `deliberations/070-spec-review-2026-04-28/` (other deliberations referenced)

## [0.3.0] and earlier

Pre-0.4.0 history is in git log. Notable closures: spec 042 (12 execution providers), spec 052 (open-source extraction), spec 054 (public documentation), spec 055 (capability registry), spec 064 (capability discovery), spec 066 (constitution v2.3.0), spec 069 (mechanical verification gate / Constitutional Inclusion Criteria gate, v2.4.0).
