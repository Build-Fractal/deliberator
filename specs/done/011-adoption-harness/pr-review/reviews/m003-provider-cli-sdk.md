# M003 Multi-Provider + CLI + SDK Review

## Summary

M003 delivers a cohesive set of capabilities: an OpenAI provider alongside the existing Anthropic provider, a CredentialStore with OAuth PKCE login/logout/refresh, a Click CLI with 5 subcommands (run, validate, decide, login, logout), a _decide() pure function with quality gating, and a typed Python SDK (Deliberation, Result, ValidateResult, classify). All 262 tests pass. The architecture is clean -- pure functions extracted for testability, shared utilities deduplicated (cost estimation in engine/cost.py, root discovery in engine/_root.py), and the provider protocol uses structural typing.

## Spec Compliance Scorecard

| FR | Status | Evidence | Notes |
|----|--------|----------|-------|
| FR-013 | PASS | MCP server existed pre-M003; CLI added in M003 | Build order correct |
| FR-014 | PASS | conversus_run from M002; conversus_decide added with quality gate | Quality gate enforced in MCP; CLI warns but proceeds |
| FR-015 | PASS | All 3 tools have Pydantic response models with typed fields | Schema auto-generated from Pydantic via FastMCP |
| FR-019 | PARTIAL | Provider layer present; capability validation absent | No model catalog or capability negotiation |
| FR-020 | NOT IMPL | Single model string applied to all phases | No per-phase or per-agent model override |
| FR-021 | PASS | asyncio.gather(return_exceptions=True), continue-with-N-1 | ProviderError.category provides failure taxonomy |
| US-5 | PASS | SDK Result has all required fields, frozen Pydantic | headline, summary, full_analysis, quality_indicators, debate_transcript |
| US-6 | PASS | CLI has run, validate, decide, login, logout | 30 integration tests via CliRunner |

## Security Assessment

### Authentication
- OAuth PKCE: Correct S256 challenge, 64-byte verifier (above RFC 7636 minimum)
- Token expiry: 300s buffer on login, 60s buffer on refresh
- Anthropic client_id is empty string -- placeholder; breaks real OAuth

### Credential Storage
- File: ~/.conversus/auth.json with chmod 600
- Tokens stored as plaintext JSON (same pattern as ~/.docker/config.json)
- No at-rest encryption

### Input Validation
- CLI decide: validates non-empty, strips whitespace
- MCP _decide(): rejects insufficient questions (stricter than CLI)
- Config parsing: comprehensive mode, agent name, round, stagnation validation
- CLI login accepts arbitrary strings (no click.Choice constraint)

## API Design Assessment

### CLI
- Clean Click group with 5 subcommands
- Inconsistency: run uses click.Choice for --provider, decide uses freeform string
- run --phase offers choices that raise ValueError at runtime (only "all" and "review" work)

### SDK
- Two construction modes: config_path and question
- Event subscription via d.on(event_type, callback)
- validate() returns errors list (never raises) -- good defensive design
- No synchronous run() wrapper; CI/CD needs asyncio.run()

### MCP Tools
- Three tools with Pydantic response models
- conversus_decide has quality gate + max_launches safeguard
- Complete parameter documentation in docs/mcp-setup.md

## Code Quality Assessment

### Strengths
- Pure function extraction throughout
- Protocol-based typing (runtime_checkable Protocol)
- Consistent error wrapping with ProviderError categories
- 262 tests in 2.58s
- CQ remediation correctly extracted shared utilities

### Issues
- [P1] CLI --phase offers unsupported values (cross-review, revision, etc. raise ValueError)
- [P2] Inconsistent --provider validation between run and decide
- [P2] Anthropic client_id is empty string -- breaks real OAuth
- [P2] OpenAI login duplicates server startup logic
- [P3] dispatch_agent converts ProviderError to string, losing category
- [P3] _CallbackHandler.authorization_code is shared class variable (concurrency hazard)
- [P3] No timeout on httpx.post calls
- [P3] linter/test_mcp_server.py sys.path manipulation

## Vision Alignment

### Supports Future Specs
- Spec 016: SDK event subscription is natural plugin hook point
- Spec 019: EngineConfig + validate() + estimate_cost() enable optimizer dry-runs
- Spec 020: Result contains written_files + metadata for scenario serialization

### Blocks or Conflicts
- FR-020: Per-phase routing requires non-trivial plumbing changes
- FR-019 layer 2: No capability validation or model catalog

### Missing Extension Points
- No plugin hook interface or register_plugin()
- No middleware pattern on providers (logging, caching, retry)
- No SDK result transformer for plugin enrichment
- No per_agent_outputs in SDK Result (requires file reads for training data)

## Recommendations

| # | Priority | Recommendation | Rationale | Affects |
|---|----------|---------------|-----------|---------|
| 1 | P1 | Remove unsupported phase choices from run --phase or implement them | Users get ValueError at runtime | M003 |
| 2 | P2 | Add click.Choice to decide --provider | Inconsistent with run command | M003 |
| 3 | P2 | Populate Anthropic client_id or add guard | Empty client_id breaks real OAuth | M003 |
| 4 | P2 | Refactor OpenAI login to reuse _run_callback_server | Duplicated server startup code | M003 |
| 5 | P2 | Add 4-category model catalog per commit message claim | FR-019 capability validation | global |
| 6 | P3 | Add timeout=30 to httpx.post() calls | Token exchange can hang indefinitely | M003 |
| 7 | P3 | Preserve error categories through dispatch | ProviderError.category lost on string conversion | global |
| 8 | P3 | Add run_sync() to Deliberation | CI/CD shouldn't need asyncio.run() boilerplate | M003 |
| 9 | P3 | Add per_agent_outputs to SDK Result | Training data extraction requires file reads otherwise | global |
| 10 | P3 | Replace class-variable callback with thread-safe queue | Concurrency hazard | M003 |

## Cross-Milestone Observations
- Shared utility extraction pattern (ee01cfb) is good -- maintain as codebase grows
- CLI decide is becoming the primary UX surface; orchestration should be extracted into a service function
- Asymmetry between CLI (warns) and MCP (rejects) on insufficient questions is deliberate per FR-014 but should be documented
- EngineConfig.provider field defaults to "anthropic" but runtime defaults to "mock" -- confusing
