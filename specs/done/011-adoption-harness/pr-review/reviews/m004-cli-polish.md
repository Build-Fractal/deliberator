# M004 CLI Polish + Auth Hardening Review

## Summary

M004 delivers 8 commits across 13 files with +1440/-65 lines. The milestone restructures the CLI from a single cli.py into a package (cli/__init__.py, cli/progress.py, cli/render.py), implements Anthropic's code-paste OAuth PKCE flow with JSON token persistence, adds conditional stealth header injection, introduces --format json on decide, adds a status command, and wires Rich-based progress rendering into both run and decide. Test coverage is thorough with 228 lines for progress, 184 for render, 216 for auth, 248 for CLI, and 57 for providers.

## Spec Compliance Scorecard

| FR | Status | Evidence | Notes |
|----|--------|----------|-------|
| FR-010 | PASS | RichProgressHandler renders all 4 event types to stderr | Events flow through CallbackEmitter |
| FR-022 | PARTIAL | Rich progressive output for CLI, JSON for programmatic | No truly "concise + expandable" yet -- dumps everything |
| FR-023 | PASS | render_result displays quality indicators table | Headline, summary, full analysis with markdown rendering |
| FR-027 | PASS | run_engine emitter defaults to None with fallback | Existing call sites unaffected |
| FR-028 | PASS | conversus run still accepts YAML config | No regression in power-user workflow |
| US-1 | PARTIAL | conversus decide works end-to-end | 30s target is runtime, not code |
| US-6 | PASS | RichProgressHandler wired into both run and decide | stderr for progress, stdout for results |

## UX Assessment

### Rich Output
- Panel for headline, Table for quality indicators, Markdown for analysis
- Progress events use Console(stderr=True) with timestamps
- Restrained emoji usage
- Missing: --verbose flag for full analysis vs concise default

### JSON Mode
- model_dump_json(indent=2) directly from Pydantic
- Tests verify valid JSON, all required keys, no ANSI escapes
- Directly consumable for scenario storage (spec 020)

### Status Command
- Rich table with Provider / Status / Details columns
- Three states: logged in, env var, not configured
- Distinguishes subscription tokens from regular OAuth
- Cross-layer import concern: imports is_oauth_token from provider implementation

### Auth Flow
- Opens browser -> prompts paste -> parses code#state -> exchanges -> stores
- Clear error messages for malformed input
- 5-minute expiry buffer on Anthropic tokens

## Security Assessment

### OAuth Code-Paste (P1)
- State parameter generated but NOT validated locally -- CSRF vector
- PKCE implementation correct (S256, 64-byte verifier)
- Code sends state_returned to server but never compares to locally-generated state

### Stealth Headers (P2)
- CLAUDE_CODE_VERSION = "2.1.62" hardcoded -- will drift
- Conditional injection only for sk-ant-oat tokens -- correct scoping
- ToS concern: impersonating Claude Code user-agent

### Token Storage
- ~/.conversus/auth.json with chmod 600
- Redaction in logs (first/last 4 chars)
- Corrupt JSON handled gracefully

## Code Quality Assessment

### Strengths
- Clean separation: progress.py, render.py, __init__.py
- Dependency injection for testability (_open_browser, _prompt_code, _exchange_token)
- Callable protocol: RichProgressHandler.__call__ satisfies CallbackEmitter directly
- TTY-aware output with tests for both paths
- Backward compatibility preserved (additive emitter parameter)

### Issues
- [P1] Missing state validation in OAuth flow -- CSRF vector
- [P2] CLAUDE_CODE_VERSION hardcoded -- should be configurable
- [P2] is_oauth_token imported from provider implementation (should be in auth)
- [P3] No --verbose flag for render output (FR-022 gap)
- [P3] OpenAI login duplicates URL construction
- [P3] _exchange_code defined after its caller

## Vision Alignment

### Supports Future Specs
- Spec 016: render_result accepts Console parameter; plugins could swap
- Spec 020: --format json output is ConversusOutput.model_dump_json() -- zero transformation for storage
- Telemetry: CallbackEmitter + RichProgressHandler extensible for TelemetryEmitter
- Credibility: render_result QualityIndicators table extensible for score display

### Blocks or Conflicts
- No blocking conflicts. Milestone is additive.

## Recommendations

| # | Priority | Recommendation | Rationale | Affects |
|---|----------|---------------|-----------|---------|
| 1 | P1 | Add local state validation in _login_anthropic | CSRF prevention per OAuth 2.0 spec | M004 |
| 2 | P2 | Make CLAUDE_CODE_VERSION configurable via env var | Prevents silent breakage on version drift | M004 |
| 3 | P2 | Move is_oauth_token() to engine/auth.py | Eliminates CLI -> provider implementation dependency | M004 |
| 4 | P3 | Add --verbose / --brief flag to decide | Better aligns with FR-022 "concise + expandable" | M004 |
| 5 | P3 | Refactor OpenAI login to deduplicate URL construction | Near-identical code blocks | M004 |
| 6 | P3 | Document ToS risk of stealth headers | Future maintainers need context | M004 |

## Cross-Milestone Observations
- Auth module at ~300+ lines is the most complex single module; consider splitting before M005
- Rich is now a runtime dependency but correctly not transitively imported by SDK
- The decide command is becoming primary UX surface; orchestration should be extracted to service function
- Test culture consistently strong across all milestones
