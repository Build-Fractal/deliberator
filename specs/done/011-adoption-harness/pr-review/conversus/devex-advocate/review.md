# Developer Experience Advocate — Initial Utilization Review

## Executive Summary

The global synthesis identifies 32 issues across 5 milestones and correctly elevates CLI, SDK, and auth problems that directly impact the developer's first hour. However, the synthesis underweights the cumulative friction of the developer journey — each individual issue is cataloged, but the *compound effect* of hitting G4 (broken --phase choices), G10 (empty client_id), G15 (inconsistent --provider validation), and G30 (async-only SDK) in sequence is what actually loses users. A developer who runs `conversus decide` and gets a ValueError from a value the CLI itself advertised will not trust the tool enough to investigate the second error. The P1/P2/P3 triage is mostly correct, but several issues rated P3 should be promoted because they gate the zero-to-working-deliberation path.

The strongest finding across all milestone reviews is the pure-function extraction pattern — every CLI command, MCP tool, and SDK method wraps a testable pure function. This is the right architecture for developer experience and should be preserved. The weakest finding is that the CLI `decide` command is accumulating orchestration responsibilities (quality gating, progress rendering, JSON output, provider resolution, auth flow) without a service-layer extraction, making it fragile and hard to extend.

## Alignment

The synthesis correctly identifies the issues that matter most to developers using conversus as a tool:

1. **G4 (--phase broken choices) as P1**: Correct. The M003 review (Section "API Design Assessment") documents that `run --phase` offers click.Choice values that raise ValueError at runtime. This is the single most damaging first-impression bug because the CLI *actively misleads* the developer.

2. **G15 (inconsistent --provider validation) as P2**: Correct priority. The M003 review notes `run` uses `click.Choice` while `decide` uses freeform string. This is confusing but not a crash — the developer can recover.

3. **G10 (empty Anthropic client_id) as P2**: Correct. The M003 review (Security Assessment) confirms the client_id is an empty string placeholder. This blocks the real OAuth flow but does not affect BYOK or env-var-based auth, so P2 is appropriate.

4. **CLI/MCP asymmetry documentation**: The M003 review (cross-milestone observations) flags that CLI warns on insufficient questions while MCP rejects. The synthesis captures this under the "Pure function extraction" strong pattern but does not explicitly call out the documentation gap. This is a miss.

5. **Auth module complexity**: Both M003 and M004 reviews flag auth.py at ~300+ lines. M004 recommends splitting before M005. The synthesis does not elevate this as a standalone issue, instead burying it under "Auth complexity" in Weak Patterns. For a developer trying to understand or debug auth failures, a 300-line module handling two OAuth flows, PKCE, storage, refresh, and resolution is a wall.

6. **Test culture as strong pattern**: The synthesis correctly highlights 1,318+ tests. From a DevEx perspective, this is critical — it means contributors can refactor with confidence and the test suite serves as living documentation.

## Missed Opportunities

1. **No "getting started" friction analysis.** The synthesis catalogs bugs but never asks: "Can a developer go from `pip install conversus` to a working deliberation in under 5 minutes?" The answer, based on the evidence, is *probably not* because: (a) `conversus decide` is the happy path but requires a provider, (b) provider setup requires either OAuth login (broken client_id per G10) or env var, (c) the `status` command (M004) shows auth state but is not discoverable from `--help` if the developer starts with `decide`, and (d) no `conversus init` or `conversus quickstart` command exists. The synthesis should have flagged this as a cross-cutting concern.

2. **`decide` command becoming a monolith.** Both M003 and M004 reviews independently note that "the decide command is becoming the primary UX surface" and "orchestration should be extracted into a service function." The synthesis lists this nowhere. For DevEx, this matters because a fat command is hard to test in isolation, hard to extend (e.g., adding `--dry-run`, `--budget`), and hard to compose in scripts.

3. **`validate()` never raises — good or bad?** The M003 review notes this as "good defensive design." The synthesis does not examine the tradeoff. For SDK users, a validate() that returns errors but never raises means they must always check the return value. If they forget, they get a silent pass followed by a cryptic engine error. A `validate(strict=True)` mode that raises on errors would be the standard SDK pattern. This is a P3 but deserves mention.

4. **No per_agent_outputs in SDK Result (G31 at P3).** The M003 review flags this. For any developer building on conversus output — training data extraction, feature engineering, custom rendering — requiring file reads to access per-agent outputs is a major ergonomic failure. This should be P2, not P3, because it gates the SDK's usefulness as a building block.

5. **ProviderError.category lost on string conversion (G23 at P3).** The M003 review documents this in dispatch_agent. For a developer handling errors programmatically (e.g., retrying on rate_limit but aborting on auth_error), losing the category taxonomy at the string conversion boundary destroys the error's value. This should be P2.

6. **No timeout on httpx.post calls (G24 at P3).** The M003 review flags this. A hanging token exchange with no timeout is a first-hour showstopper — the developer's terminal freezes with no feedback. This should be P2.

7. **EngineConfig.provider defaults to "anthropic" but runtime defaults to "mock".** The M003 review (final bullet) flags this contradiction. A developer reading the config schema will expect Anthropic; the runtime will silently use mock. This is exactly the kind of mismatch that burns 30 minutes of debugging.

## Off-Base Assumptions

1. **G30 (async-only SDK) rated P3.** The synthesis places this at the bottom of the priority list. For SDK adoption, this is a significant barrier. Most Python scripts, CI/CD pipelines, Jupyter notebooks, and synchronous web frameworks (Django, Flask) cannot call `await` without wrapping in `asyncio.run()`. The M003 review correctly recommends a `run_sync()` wrapper. This should be P2 — it is not polish, it is an API design decision that determines whether the SDK is usable in the most common Python contexts.

2. **"Test culture" as purely positive.** The synthesis praises 1,318+ tests and 3x spec requirements. From a DevEx perspective, this is mostly good but the M001 review notes a `try/except ImportError` pattern in all test files and a missing `conftest.py`. This means contributing tests requires understanding a non-standard import dance. The test *count* is strong; the test *ergonomics* for contributors need work.

3. **G9 (stealth header version hardcoded) rated P2.** This is correct for security/maintenance but underestimates the DevEx impact. When `CLAUDE_CODE_VERSION = "2.1.62"` drifts and requests silently fail, the developer gets no actionable error — just a mysterious auth rejection. The M004 review recommends making it configurable via env var, which is the right fix, but the synthesis should note that this will be one of the hardest bugs to diagnose because the failure mode is completely opaque.

4. **The synthesis treats CLI and SDK as separate surfaces.** In practice, many developers will use the SDK *because* they started with the CLI and want programmatic access. The gap between `conversus decide "question"` (works, shows Rich output) and `Deliberation(question="question").run()` (requires async, no progress output by default, no per_agent_outputs) is a cliff, not a ramp. The synthesis should identify this CLI-to-SDK graduation path as a design concern.

## Actionable Recommendations (7-10 numbered items, P1 first)

1. **[P1] Remove unsupported --phase choices immediately.** The CLI advertises `cross-review`, `revision`, `disputes`, `synthesis` as valid --phase values but they raise ValueError at runtime (G4, M003 review "API Design Assessment"). Either restrict click.Choice to `["all", "review"]` or implement the missing phases. A CLI that crashes on its own advertised options is a trust-destroyer. Fix: 1-line change to the Choice list.

2. **[P1] Add local OAuth state validation in _login_anthropic.** The M004 review (Security Assessment) documents that state is generated but never compared to the returned value — a textbook CSRF vector (G2). Beyond the security concern, a developer who gets CSRF-attacked during login will see an inscrutable auth error with no diagnostic path. Fix: add `assert state_returned == state_local` before token exchange.

3. **[P2] Add run_sync() wrapper to Deliberation.** The M003 review recommends this (recommendation #8). Without it, every synchronous Python context requires `asyncio.run(d.run())` boilerplate. This is the single biggest SDK adoption barrier because it makes the simplest example 3 lines instead of 1. Pattern: `def run_sync(self, **kwargs) -> Result: return asyncio.run(self.run(**kwargs))`.

4. **[P2] Promote per_agent_outputs into SDK Result.** Currently rated P3 (G31) but the M003 review identifies this as required for "training data extraction" without falling back to file reads. Any developer using conversus as a building block — which is the SDK's entire purpose — needs structured access to individual agent outputs. This is not polish; it is API completeness.

5. **[P2] Add 30-second timeout to all httpx.post calls.** The M003 review flags no timeout on token exchange (G24). A developer doing `conversus login` on a flaky network will see their terminal hang indefinitely with no feedback. Add `timeout=30` to all httpx calls and surface a clear `ProviderError("Token exchange timed out after 30s")`.

6. **[P2] Preserve ProviderError.category through dispatch_agent.** The M003 review documents that string conversion in dispatch loses the category (G23). For SDK consumers handling errors programmatically, the category (auth, rate_limit, content_filter, provider_error) is the entire value of the error taxonomy. Without it, all errors are opaque strings. Fix: propagate the ProviderError object, not `str(e)`.

7. **[P2] Resolve EngineConfig.provider vs runtime provider default mismatch.** The M003 review (final bullet) notes EngineConfig defaults to "anthropic" while runtime defaults to "mock." This means `conversus.validate()` will say the config is valid, but `conversus.run()` will silently use mock. Either make the defaults consistent or require explicit provider specification.

8. **[P2] Extract decide orchestration into a service function.** Both M003 and M004 reviews independently flag that `decide` is accumulating responsibilities. The decide CLI command should be a thin wrapper around a `decide()` service function that the SDK, MCP tool, and CLI all call. This unblocks `--dry-run`, `--budget`, and composability.

9. **[P3] Document CLI/MCP behavioral asymmetry.** The M003 review notes that CLI warns on insufficient questions while MCP rejects. This is a deliberate design choice (FR-014) but is not documented anywhere a developer would find it. Add a "Behavioral Differences" section to `docs/mcp-setup.md` and a note in CLI `--help`.

10. **[P3] Add conftest.py to eliminate dual-import pattern in tests.** The M001 review identifies `try/except ImportError` boilerplate across all 7 test files. For contributors, this is an unnecessary barrier. A single conftest.py with proper path setup removes the boilerplate and makes the test suite approachable.

## Referenced Documentation

| Document | Key Findings Used |
|----------|-------------------|
| `global-synthesis.md` | G4 (--phase broken), G10 (empty client_id), G15 (--provider inconsistency), G23 (ProviderError.category lost), G24 (no httpx timeout), G30 (async-only SDK), G31 (no per_agent_outputs), G2 (OAuth state), G9 (stealth header version) |
| `reviews/m003-provider-cli-sdk.md` | CLI API design inconsistencies, SDK validate() behavior, async-only run(), per_agent_outputs gap, ProviderError dispatch, EngineConfig.provider mismatch, httpx timeout, decide command growth |
| `reviews/m004-cli-polish.md` | OAuth state validation gap, stealth header hardcoding, auth module complexity (~300+ lines), is_oauth_token module placement, Rich output architecture, decide command growth |
| `reviews/m002-engine.md` | Linter/engine dependency inversion, EventEmitter protocol, ModelProvider text-only limitation, missing plugin hooks, OutputManager mutation, test coverage (281+ methods, 3x spec requirement) |
| `reviews/m001-foundation.md` | Test dual-import pattern, conftest.py absence, pure function extraction pattern, MCP server tool architecture |
| `reviews/m005-web-interface.md` | BYOK os.environ race condition, RLS/user_id mismatch, no rate limiting, AsyncQueueEmitter architecture |
