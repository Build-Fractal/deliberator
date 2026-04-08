# Security Review — 011-adoption-harness Global Synthesis

**Reviewer**: security-reviewer
**Date**: 2026-03-24
**Scope**: M003, M004, M005 security findings as reflected in global-synthesis.md

---

### Executive Summary

The 011-adoption-harness PR introduces a multi-surface application (CLI, SDK, MCP server, web API) with OAuth authentication, BYOK key handling, Supabase persistence, and public sharing. From a security perspective, the implementation demonstrates solid fundamentals: PKCE with S256 is correctly implemented, token storage uses chmod 600, credential redaction in logs is present, and error categorization prevents information leakage in provider errors. The overall security posture is appropriate for a developer-facing pre-GA tool.

However, the PR has three genuine security defects that the synthesis correctly identifies as P1: the OAuth state validation gap, the BYOK os.environ race condition, and the RLS/user_id mismatch. My assessment differs from the synthesis on severity classification for several of these. The OAuth state issue is real but its exploitability is drastically reduced by the code-paste flow (no redirect URI to hijack). The BYOK race is a real concurrency bug with actual key leakage consequences under uvicorn. The RLS mismatch is the most severe finding because it creates a hard deployment blocker — migration 002 policies will reject every INSERT from the backend since user_id is never populated, meaning either the application breaks entirely or the operator skips migration 002 and runs with the permissive 001 policies, leaving all deliberation data world-readable to anyone with the anon key.

The single most important recommendation: fix the RLS/user_id mismatch in migration 002 by switching to the Supabase service role key for backend operations, because this is the only finding that blocks production deployment entirely.

### Alignment

- **PKCE implementation is correct.** 64-byte verifier exceeds RFC 7636 minimum of 43 characters. S256 challenge is properly computed. This is verified in the M003 review (`m003-provider-cli-sdk.md`, Security Assessment section) and confirmed by source inspection of `engine/auth.py` lines 112-121.
- **Token storage permissions are appropriate for the threat model.** `~/.conversus/auth.json` with chmod 600 (lines 80-82 of `engine/auth.py` on the PR branch) matches the pattern used by `~/.docker/config.json`, `~/.aws/credentials`, and `~/.config/gh/hosts.yml`. The M003 review correctly notes this as equivalent to industry standard (`m003-provider-cli-sdk.md`, line 29).
- **Credential redaction in logs.** The `_redact()` function (auth.py lines 199-203) shows first/last 4 characters, preventing full token exposure in log output while preserving debuggability.
- **Error categorization prevents information leakage.** ProviderError wraps all SDK exceptions with category tags (`auth`, `rate_limit`, `server`, `unknown`), preventing raw Anthropic/OpenAI error details from reaching end users through the web API's `map_engine_error()` function.
- **Share link access control is correct.** Migration 003 adds an RLS policy that restricts public reads to `is_public = true` rows only. The `set_deliberation_public()` function in `web/db.py` enforces `status = 'completed'` before allowing sharing.
- **Dependency injection pattern enables security testing.** Every auth function accepts injectable parameters (`_open_browser`, `_prompt_code`, `_exchange_token`, `_post`), making it possible to test OAuth flows without real network calls.

### Missed Opportunities

- **No httpx timeout on token exchange requests.** Both `_exchange_code()` (auth.py line 338) and `_exchange_code_json()` (auth.py line 227 on PR branch) call `httpx.post()` without a `timeout` parameter. A malicious or malfunctioning OAuth server can hang the CLI process indefinitely. The M003 review flags this at P3 (`m003-provider-cli-sdk.md`, recommendation 6) but it should be P2 — a hung CLI during login is a denial-of-service against the user's terminal.
- **No input length validation on the web question field.** The `DeliberateRequest` model has `min_length=1` but no `max_length` (`web/app.py` line 72 on PR branch). The M005 review correctly identifies this (`m005-web-interface.md`, recommendation 4) but understates the risk — a 1MB question string will be embedded in every agent prompt, multiplied by agent count and round count, creating a token-exhaustion amplification vector.
- **No rate limiting on POST /api/deliberate.** Each request spawns a full engine pipeline with multiple LLM calls. Without rate limiting, a single attacker can exhaust API quotas or rack up significant costs. Identified in M005 review (`m005-web-interface.md`, recommendation 5) as P2 — I agree with this classification.
- **Anthropic client_id is base64-encoded but not secret.** The client_id in `OAUTH_CONFIGS["anthropic"]` is base64-encoded (`OWQxYzI1MGEt...`), which provides zero security value — base64 is not encryption. This creates a false sense of obscurity. It should be stored as a plain string or, if it is actually sensitive, loaded from environment variables.
- **No token refresh race protection.** The `refresh_token()` function in auth.py reads credentials, checks expiry, makes an HTTP call, and writes back — with no file locking. If two processes (e.g., CLI and MCP server) refresh simultaneously, one token write may overwrite the other's updated refresh_token, invalidating it.
- **No CSRF protection on web POST endpoints.** The `/api/deliberate` and `/api/deliberations/{id}/share` POST endpoints have no CSRF token validation. While the API is consumed by a separate frontend (making CORS the primary defense), the CORS configuration uses `allow_methods=["*"]` and `allow_headers=["*"]`, which weakens that defense layer.
- **share_id entropy is low and predictable.** `uuid.uuid4().hex[:8]` yields 32 bits of entropy (4 billion possibilities). For an MVP this is acceptable, but the synthesis flags no-unshare as P3 (`global-synthesis.md`, G29). Combined with low entropy, this means a motivated attacker could brute-force share links. At 100 requests/second, the full space is exhaustible in ~497 days — but with known timing (share created after a deliberation), the search space narrows.
- **The _CallbackHandler.authorization_code class variable is a concurrency hazard.** If two login flows overlap in the same process, the class variable will be overwritten. The M003 review flags this at P3 (`m003-provider-cli-sdk.md`, recommendation 10). For CLI use this is unlikely, but the pattern is architecturally unsound.

### Off-Base Assumptions

- **G2 (OAuth state validation) is classified as P1/MUST FIX — this overstates the real CSRF risk for the code-paste flow.** The synthesis (`global-synthesis.md`, line 27) and M004 review (`m004-cli-polish.md`, line 48) classify the missing state validation as a CSRF vector per OAuth 2.0 spec. This is technically correct per the specification, but the threat model is different here. In Anthropic's code-paste flow, there is no redirect URI that an attacker can intercept — the user manually copies `code#state` from a browser page and pastes it into their own terminal. For CSRF to succeed, an attacker would need to: (1) convince the victim to initiate a login, (2) have the victim paste an attacker-controlled `code#state` value into their own terminal. The state validation should still be added (it is a 1-line fix), but this is SHOULD FIX severity, not MUST FIX. The state value is already sent to the server in the token exchange body — the only missing piece is the local comparison.

- **G3 (BYOK os.environ race) severity is understated as "Medium" fix complexity.** The synthesis (`global-synthesis.md`, line 28) correctly identifies this as P1 but labels the fix as "Medium." In practice, the fix is trivial — the `AnthropicProvider` already accepts `auth_token` as a constructor parameter, and `OpenAIProvider` accepts `api_key`. The web app should construct the provider directly with the key instead of mutating process environment. The current code (`web/app.py` lines 253-269 on PR branch) does `os.environ[env_var] = request.api_key`, uses a try/finally to restore the old value, but this is not atomic — under uvicorn with multiple async tasks, a concurrent request between the `os.environ` set and the `os.environ.pop` will see the other user's API key. This is a real credential exposure bug, not a theoretical race.

- **Token storage "no at-rest encryption" is flagged but not actionable.** The M003 review (`m003-provider-cli-sdk.md`, line 29) notes "No at-rest encryption" for the credential store. This is standard practice for developer CLI tools. Docker, AWS CLI, GitHub CLI, and kubectl all store credentials as plaintext JSON or YAML with file permissions as the access control mechanism. Adding encryption would require a master password or system keyring integration, which is a significant UX burden for a developer tool. This is a FALSE POSITIVE for the current threat model.

### Actionable Recommendations

1. **Fix RLS/user_id mismatch** (Priority: P1)
   - **Current state**: Migration 002 (`supabase/migrations/002_rls_user_scoped.sql`) creates INSERT policy `WITH CHECK (auth.uid() = user_id)`, but `store_deliberation()` in `web/db.py` (lines 99-116) never sets `user_id` in the inserted row. The Supabase client uses `SUPABASE_ANON_KEY` (`web/db.py` line 47).
   - **Proposed change**: Use `SUPABASE_SERVICE_ROLE_KEY` for backend operations (bypasses RLS), or populate `user_id` from the anonymous session's `auth.uid()` on every insert. The service role approach is simpler and matches the backend-as-trusted-service pattern.
   - **Rationale**: With migration 002 applied and the anon key, every INSERT and SELECT will fail because `auth.uid()` will not equal the NULL `user_id`. The application is non-functional in production with this migration applied. [`m005-web-interface.md`, recommendation 2; `global-synthesis.md`, G5]
   - **Risk if ignored**: Complete deployment failure — the web interface cannot store or retrieve any deliberation data.

2. **Eliminate BYOK os.environ mutation** (Priority: P1)
   - **Current state**: `web/app.py` lines 253-269 (PR branch) temporarily sets `os.environ[env_var] = request.api_key`, calls `resolve_provider()`, then restores the original value in a finally block.
   - **Proposed change**: Add an `api_key` parameter to `resolve_provider()` that takes precedence over env var and stored credentials. Construct the provider directly: `AnthropicProvider(auth_token=api_key)` or `OpenAIProvider(api_key=api_key)`. Remove all `os.environ` mutation from the web request path.
   - **Rationale**: Under uvicorn's async concurrency model, multiple requests are interleaved on the same event loop. Between `os.environ[env_var] = key_A` and the finally-block restoration, a concurrent request reading `os.environ.get(env_var)` will see user A's API key. This is a cross-user credential exposure. [`m005-web-interface.md`, recommendation 1; `global-synthesis.md`, G3]
   - **Risk if ignored**: User A's API key is briefly visible to user B's concurrent request. Under load, this is reliably exploitable.

3. **Add local state validation in Anthropic code-paste flow** (Priority: P2)
   - **Current state**: `_login_anthropic()` in `engine/auth.py` (PR branch, around line 290) generates `state = secrets.token_urlsafe(32)`, sends it in the auth URL, parses `code#state_returned` from user paste, but never compares `state_returned` to the original `state`. The `state_returned` is passed to the token exchange endpoint but not validated locally.
   - **Proposed change**: Add `if state_returned != state: raise ProviderError("OAuth state mismatch — possible CSRF attack.", category="auth")` immediately after parsing `code#state_returned`.
   - **Rationale**: While the code-paste flow substantially mitigates the redirect-based CSRF attack, validating state locally is a defense-in-depth measure that costs one line and prevents any future flow changes from introducing a regression. [`m004-cli-polish.md`, recommendation 1; `global-synthesis.md`, G2]
   - **Risk if ignored**: Minimal practical risk in the current code-paste flow. However, if the flow ever changes to use a redirect URI, this becomes a real CSRF vulnerability.

4. **Add max_length to web question field** (Priority: P2)
   - **Current state**: `DeliberateRequest.question` in `web/app.py` line 72 has `min_length=1` but no `max_length`.
   - **Proposed change**: Add `max_length=10_000` (or a contextually appropriate limit) to the `question` field: `question: str = Field(..., min_length=1, max_length=10_000)`.
   - **Rationale**: The question is embedded in every agent prompt, multiplied by agent count (typically 3-5) and round count. A 1MB question creates a token amplification attack that exhausts the API key quota or triggers rate limits across all agents simultaneously. [`m005-web-interface.md`, recommendation 4]
   - **Risk if ignored**: Deliberate or accidental oversized payloads cause cost explosion or service degradation.

5. **Add rate limiting to POST /api/deliberate** (Priority: P2)
   - **Current state**: No rate limiting exists on the deliberation endpoint (`web/app.py`, PR branch). Each request spawns a full engine pipeline with multiple LLM API calls.
   - **Proposed change**: Add a per-IP rate limiter using `slowapi` or a simple in-memory token bucket. Suggested limit: 5 requests per minute per IP for the deliberation endpoint.
   - **Rationale**: Without rate limiting, a single client can trigger hundreds of concurrent LLM API calls, exhausting quotas and incurring unbounded costs. This is especially dangerous with BYOK keys where the cost is borne by the user, but also applies to any shared API keys. [`m005-web-interface.md`, recommendation 5; `global-synthesis.md`, G11]
   - **Risk if ignored**: Unbounded cost exposure and denial of service for legitimate users.

6. **Restrict CORS allow_methods and allow_headers** (Priority: P2)
   - **Current state**: `web/app.py` lines 57-62 (PR branch) set `allow_methods=["*"]` and `allow_headers=["*"]`.
   - **Proposed change**: Restrict to `allow_methods=["GET", "POST", "OPTIONS"]` and `allow_headers=["Content-Type", "Authorization"]`.
   - **Rationale**: Wildcard CORS methods and headers weaken the browser's same-origin policy protection unnecessarily. The API only uses GET and POST. Restricting headers to Content-Type and Authorization covers all current use cases. The wildcard pattern is a common default that should be tightened before production. [`m005-web-interface.md`, recommendation 6; `global-synthesis.md`, G28]
   - **Risk if ignored**: An attacker who finds an XSS vulnerability in the frontend or a colocated domain can use arbitrary HTTP methods and headers in cross-origin requests, expanding the attack surface.

7. **Add httpx timeout to all token exchange calls** (Priority: P2)
   - **Current state**: `_exchange_code()` (auth.py line 338) and `_exchange_code_json()` (auth.py line 227 on PR branch) call `httpx.post()` with no timeout parameter. `refresh_token()` similarly passes no timeout.
   - **Proposed change**: Add `timeout=30` to all `httpx.post()` calls in auth.py.
   - **Rationale**: A malicious or malfunctioning OAuth server can hang the CLI indefinitely. For the web path (if refresh_token is ever called server-side), this hangs an async worker. [`m003-provider-cli-sdk.md`, recommendation 6]
   - **Risk if ignored**: CLI hangs indefinitely during login/refresh. If ever invoked in the web server path, it blocks an async worker permanently.

8. **Add unshare endpoint** (Priority: P3)
   - **Current state**: `set_deliberation_public()` in `web/db.py` makes a deliberation public but there is no reverse operation. Once shared, a deliberation cannot be un-shared. (`global-synthesis.md`, G29; `m005-web-interface.md`, recommendation 7).
   - **Proposed change**: Add a `DELETE /api/deliberations/{id}/share` endpoint that sets `is_public = false` and nullifies `share_id`.
   - **Rationale**: Users may share deliberations containing sensitive information and later want to revoke access. Without unshare, the only recourse is database-level intervention. The 32-bit share_id entropy makes this more pressing — if a share link is guessed or leaked, there is no way to revoke it.
   - **Risk if ignored**: Sensitive deliberation content remains permanently publicly accessible once shared.

9. **Document stealth header ToS implications** (Priority: P3)
   - **Current state**: The `AnthropicProvider` on the PR branch (commit `4f64a5c`) injects `user-agent: claude-cli/2.1.62`, `x-app: cli`, and `anthropic-beta: claude-code-20250219,oauth-2025-04-20` headers for subscription OAuth tokens. The version is hardcoded. (`m004-cli-polish.md`, recommendation 2 and 6; `global-synthesis.md`, G9).
   - **Proposed change**: (a) Make `CLAUDE_CODE_VERSION` configurable via environment variable with the current value as default. (b) Add a code comment and README note documenting why these headers exist, that they impersonate Claude Code's user-agent, and the ToS risk this entails.
   - **Rationale**: Impersonating another client's user-agent may violate Anthropic's Terms of Service. A hardcoded version string will silently break when Anthropic updates their client fingerprinting. Future maintainers need to understand the trade-off being made. This is not a security vulnerability per se — it is a compliance and sustainability risk.
   - **Risk if ignored**: Token rejection when Anthropic updates version checks. Potential account termination for ToS violation.

### Security Finding Classifications

| Finding | Synthesis Rating | My Classification | Rationale |
|---------|-----------------|-------------------|-----------|
| G2 — OAuth state not validated | P1 / MUST FIX | **SHOULD FIX** | Code-paste flow has no redirect URI to hijack; CSRF requires victim to paste attacker's code. 1-line fix, so do it, but not a merge blocker. |
| G3 — BYOK os.environ race | P1 / MUST FIX | **MUST FIX** | Real cross-user credential exposure under uvicorn concurrency. Reliably exploitable under load. |
| G5 — RLS/user_id mismatch | P1 / MUST FIX | **MUST FIX** | Hard deployment blocker. Application non-functional with migration 002 applied. |
| G9 — Stealth header version | P2 / SHOULD FIX | **SHOULD FIX** | Functional risk (version drift) plus ToS risk. Not a security vulnerability. |
| G10 — Empty Anthropic client_id | P2 / SHOULD FIX | **FALSE POSITIVE** | Client_id on the PR branch is populated via base64 decode. The M003 review's finding appears to predate the M004 commit that added the real client_id. |
| G11 — No rate limiting | P2 / SHOULD FIX | **SHOULD FIX** | Cost amplification and DoS vector. Agree with P2. |
| G16 — No max_length on question | P2 / SHOULD FIX | **SHOULD FIX** | Token amplification vector. Agree with P2. |
| G25 — _CallbackHandler class var | P3 / NICE TO HAVE | **ACCEPTED RISK** | CLI login is single-threaded in practice. Document the limitation. |
| G28 — CORS overly permissive | P3 / NICE TO HAVE | **SHOULD FIX** (upgrade) | Wildcard CORS methods/headers is a defense-in-depth failure. Simple fix, should be P2. |
| G29 — No unshare endpoint | P3 / NICE TO HAVE | **SHOULD FIX** | Combined with 32-bit share_id entropy, inability to revoke is a data exposure risk. |
| Token storage plaintext | Noted in M003 | **FALSE POSITIVE** | Industry standard for developer CLI tools. chmod 600 is the accepted control. |

### Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus/specs/011-adoption-harness/pr-review/global-synthesis.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/011-adoption-harness/pr-review/reviews/m004-cli-polish.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/011-adoption-harness/pr-review/reviews/m005-web-interface.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/011-adoption-harness/pr-review/reviews/m003-provider-cli-sdk.md`
- `engine/auth.py` (PR branch: `remotes/origin/011-adoption-harness`)
- `engine/providers/anthropic.py` (PR branch: `remotes/origin/011-adoption-harness`)
- `web/app.py` (PR branch: `remotes/origin/011-adoption-harness`)
- `web/db.py` (PR branch: `remotes/origin/011-adoption-harness`)
- `supabase/migrations/001_initial_schema.sql` (PR branch)
- `supabase/migrations/002_rls_user_scoped.sql` (PR branch)
- `supabase/migrations/003_sharing.sql` (PR branch)
