# Feature Specification: MCP Sampling Provider (`claude-desktop`)

**Feature ID**: `060-mcp-sampling-provider`
**Created**: 2026-04-14
**Status**: Draft
**Depends On**: `055-capability-registry`, existing MCP server, Desktop Extension
**Motivated by**: Desktop Extension users shouldn't need API keys — they already have a Claude subscription

---

## 1. Problem

Desktop Extension users must configure an Anthropic API key in extension settings to run real deliberations. This is a fundamental UX failure: the user is ALREADY inside Claude Desktop, ALREADY authenticated with their Claude subscription, but conversus can't use that session. Instead it asks them to go to console.anthropic.com, create an API key, and paste it into extension settings.

The MCP protocol solves this via **sampling** — [`sampling/createMessage`](https://modelcontextprotocol.io/specification/draft/client/sampling) lets the MCP server ask the HOST to make LLM calls on its behalf. The host (Claude Desktop) forwards the request through its own Claude session and returns the response. No separate API key. No configuration. The user's existing subscription covers everything.

---

## 2. Proposed solution

A new execution provider: `claude-desktop`

```python
# engine/execution/providers/desktop_sampling.py

class DesktopSamplingProvider(ExecutionProvider):
    """Execution provider that routes agent calls through MCP sampling.

    Instead of calling the Anthropic API directly, sends each agent's
    prompt via sampling/createMessage to the MCP client (Claude Desktop).
    The client forwards it through its own Claude session and returns
    the response. Zero configuration — uses the host's subscription.
    """

    name = "claude-desktop"

    async def complete(self, prompt: str, *, model: str = "", max_tokens: int = 4096) -> ExecutionResult:
        # Send sampling/createMessage to the MCP client
        response = await self.mcp_context.sample(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return ExecutionResult(
            success=True,
            content=response.text,
            cost=Cost(input_tokens=0, output_tokens=0),  # host absorbs cost
            provider="claude-desktop",
        )
```

### How it works

```
User: "Deliberate on whether to use Postgres or MongoDB"
  ↓
Claude Desktop calls conversus_decide tool
  ↓
conversus MCP server starts 5-phase pipeline
  ↓
Phase 1: dispatch pragmatist agent
  ↓
DesktopSamplingProvider.complete(prompt="You are the pragmatist...")
  ↓
MCP server sends: sampling/createMessage {
  messages: [{"role": "user", "content": "You are the pragmatist..."}],
  maxTokens: 4096
}
  ↓
Claude Desktop forwards to its Claude session
  ↓
Claude generates the pragmatist's review
  ↓
Response flows back through MCP to the pipeline
  ↓
Phase 1 complete → Phase 2 (cross-review) → same flow for each agent
```

### Key constraint

From the MCP spec: "Servers MUST send sampling/createMessage requests only in association with an originating client request (e.g., during tools/call)." This is satisfied — every sampling call happens during a `tools/call` invocation (`conversus_decide`). The entire pipeline runs within the scope of a single tool call.

---

## 3. What changes

| Component | Change |
|---|---|
| `engine/execution/providers/desktop_sampling.py` | **New** — the provider implementation |
| `engine/execution/providers/__init__.py` | Register `"claude-desktop"` provider |
| `mcp_server.py` | Pass the MCP server context to the provider so it can call `sampling/createMessage` |
| `desktop-extension/manifest.json` | Default provider changes from `"demo"` to `"claude-desktop"` |
| `capabilities.py` | Add `"claude-desktop"` to the provider choices list |

### What does NOT change

- The pipeline (`engine/phases.py`) — it calls `provider.complete(prompt)` and doesn't care how the provider routes the call
- The result types — `ExecutionResult` shape is the same
- Templates — agent prompts are the same regardless of provider
- All other providers (anthropic, openai, ollama, etc.) — they continue to work via direct API calls

---

## 4. The zero-config experience

**Before (current)**:
1. Install .mcpb extension
2. Go to extension settings
3. Get API key from console.anthropic.com
4. Paste into Anthropic API Key field
5. NOW you can run real deliberations

**After (with claude-desktop provider)**:
1. Install .mcpb extension
2. Run a deliberation

That's it. The extension uses the Claude session the user is already in. No API key, no settings, no console.anthropic.com.

---

## 5. Implementation plan

### Phase 1: Provider skeleton

1. Create `engine/execution/providers/desktop_sampling.py`
2. The provider needs access to the MCP server's context to send sampling requests — FastMCP provides this via the `Context` object in tool handlers
3. Register as `"claude-desktop"`
4. Test: call `provider.complete("Say hello")` and verify the sampling request is sent

### Phase 2: Wire into the pipeline

1. The challenge: the provider needs the MCP context, but the pipeline runs deep inside `engine/phases.py` → `engine/dispatch.py`. The MCP context needs to be threaded from the `@mcp.tool()` handler all the way down to the provider.
2. Options:
   - (a) Pass the MCP context through the call chain (cleanest but touches many function signatures)
   - (b) Store it in a thread-local / contextvars (simpler wiring, less explicit)
   - (c) Create the provider instance inside the tool handler with the context bound (factory pattern)
3. Recommendation: option (c) — `DesktopSamplingProvider(mcp_context=ctx)` created in the tool handler, passed to `run_pipeline` as the provider

### Phase 3: Make it the default

1. Change `manifest.json` default provider from `"demo"` to `"claude-desktop"`
2. The settings cascade still works — users can override to `"anthropic"` or `"openai"` if they want direct API calls
3. `"demo"` remains available for offline/testing use

### Phase 4: Cost transparency

1. MCP sampling doesn't report token usage to the extension — the host absorbs the cost
2. Add a note in the `DecideResult` that cost information is unavailable when using the claude-desktop provider
3. The `max_launches` safety cap still works — it counts launches (API calls), not tokens

---

## 6. Technical considerations

### Human-in-the-loop

The MCP spec says: "For trust & safety and security, there SHOULD always be a human in the loop with the ability to deny sampling requests." Claude Desktop may show a confirmation dialog for each sampling request — that would make a 9-launch deliberation require 9 user confirmations. Need to verify whether Claude Desktop batches or auto-approves sampling from installed extensions.

### Concurrency

MCP sampling requests are sequential (the spec says "only in association with an originating client request"). The current pipeline dispatches agents in parallel within each phase. With the sampling provider, Phase 1 (2 agents) would need to either:
- Run sequentially (slower but simpler)
- Use multiple sampling requests in parallel (if the protocol allows)

### Model selection

The `sampling/createMessage` request can include `modelPreferences` to suggest a model. The provider should forward the user's `default_model` setting (or the `--model` flag) as a preference, not a hard requirement — the host decides which model to actually use.

---

## 7. Success criteria

- SC-001: `conversus_decide` with `provider="claude-desktop"` completes a full 5-phase deliberation using only the host's Claude session
- SC-002: No API key configuration required — the extension works immediately after install
- SC-003: The `max_launches` safety cap still limits the number of sampling requests
- SC-004: If Claude Desktop denies a sampling request, the error propagates cleanly to the user
- SC-005: The `demo` and `anthropic` providers still work as fallbacks

---

## 8. Out of scope

- **Token cost tracking** — the host absorbs sampling costs; the extension can't see them
- **Model selection** — the host decides which model to use; the extension can suggest via modelPreferences but can't mandate
- **Non-Claude hosts** — this provider is specific to MCP hosts that support sampling (Claude Desktop, potentially Cursor/Windsurf in the future)
- **Streaming** — MCP sampling doesn't support streaming responses in the current spec; the full response arrives when complete

---

## 9. Sources

| Source | Use |
|---|---|
| [MCP Sampling spec](https://modelcontextprotocol.io/specification/draft/client/sampling) | The protocol capability this provider uses |
| [MCP Sampling guide](https://mingzilla.github.io/specification/mcp-sampling-guide.html) | Implementation patterns and constraints |
| `engine/execution/providers/mock.py` | Pattern for implementing a new provider |
| `engine/execution/providers/anthropic.py` | How the direct-API provider works (for comparison) |
| FastMCP `Context` object | How to access sampling from inside a tool handler |
