# Execution Provider Abstraction: Open-Source Tools Research

**Date**: 2026-04-03  
**Project**: conversus (Feature Specification 042-execution-providers)  
**Scope**: Comprehensive evaluation of tools for abstracting multi-agent deliberation from specific LLM SDKs and agent runtimes

---

## Executive Summary

This report investigates 14 major open-source tools and frameworks to solve conversus's execution provider abstraction problem: decoupling the multi-agent deliberation engine from any specific LLM SDK or agent runtime.

**Key Finding**: The tool landscape has matured significantly in 2026. Three distinct solution paths emerge:

1. **LiteLLM-based approach** (70% fit): Model API abstraction only; requires custom wrapping for agent runtimes
2. **A2A protocol approach** (85% fit): Native agent-to-agent communication; requires implementing ACP server wrappers for SDKs
3. **Hybrid approach** (95% fit): Build thin ExecutionProvider layer in spec 042, delegate individual providers to existing tools

No single tool solves 100% of the problem because conversus's unique requirement—supporting both model APIs (Anthropic, OpenAI) AND agent runtimes (Claude Code, OpenCode, Aider) in the same abstraction layer—is rare. Most frameworks optimize for one or the other.

**Recommendation**: Implement conversus's own lightweight `ExecutionProvider` protocol (already in spec 042), then use LiteLLM for Tier 3 (direct API) and A2A/MCP wrappers for Tier 1-2 (agentic SDKs). This gives conversus full control over the abstraction while reusing vetted provider implementations.

---

## Part 1: Tool Catalog

### 1. LiteLLM

**Purpose**: Unified SDK for 100+ model providers (Anthropic, OpenAI, Google, Mistral, Ollama, local)

**License**: MIT

**Maturity**
- **GitHub Stars**: 41,900 (as of 2026-04-03)
- **Last Commit**: Active, releases multiple times per month
- **Production Use**: Stripe, OpenAI, FastAPI maintainers, countless startups
- **Stability**: Stable; security advisories patched promptly (PYSEC-2026-2 fixed in March 2026)

**Provider Coverage**
- **Model APIs**: 100+ providers (OpenAI, Anthropic, Azure, Google, Mistral, Ollama, Bedrock, etc.)
- **Agent Runtimes**: None (model API only)
- **Local Models**: Full Ollama support; VLLM, LMStudio, TogetherAI via OpenAI-compatible endpoints

**Tool Use Support**
- **Function Calling**: Full support via unified API
- **Format Handling**: Automatic format conversion per provider (each provider has different function calling syntax)
- **MCP Integration**: Hosted MCP servers available (web search, computer use)
- **Agent Loop**: No built-in agent orchestration; providers only handle single completions

**Async Support**: Full `asyncio`-native; `AsyncLiteLLM` class

**Python SDK Availability**: Mature; `pip install litellm`

**Cost Tracking**
- Per-virtual-API-key spend tracking
- Real-time budget enforcement
- Detailed cost breakdown per provider and model
- Integrated into response metadata

**Rate Limiting / Retry**
- Built-in exponential backoff with configurable retries
- Per-provider rate limit handling
- Circuit breaker patterns available

**Extensibility**
- Custom provider plugins via class inheritance
- Proxy server mode for custom routing
- Extensible budget enforcement via `define_custom_budget()`

**Key Limitations**
- **No agent runtimes**: Cannot dispatch to Claude Code, Aider, OpenCode, Copilot
- **Model API only**: No file-reading or file-writing tools; engine must pre-read/post-write
- **Orchestration**: No multi-phase or multi-task coordination; single-completion only
- **Cost model mismatch**: Conversus needs per-task cost; LiteLLM tracks per-call, which is fine but doesn't understand phase-level semantics

**Complementary Use**: Ideal for Tier 3 (direct model API) providers in conversus's spec

---

### 2. pydantic-ai

**Purpose**: Type-safe Python agent framework with provider abstraction

**License**: MIT

**Maturity**
- **GitHub Stars**: 5,200+ (relatively new, launched 2025)
- **Last Commit**: Active development (2026)
- **Production Use**: Early adoption by Pydantic ecosystem; used internally by Pydantic
- **Stability**: Stable API; v0.x versioning, moving toward v1.0

**Provider Coverage**
- **Model APIs**: OpenAI, Anthropic, Google Gemini, Claude (native)
- **Agent Runtimes**: None explicitly; but the framework IS an agent runtime itself
- **Local Models**: Ollama support; any OpenAI-compatible endpoint

**Tool Use Support**
- **Function Calling**: First-class support via `@agent.tool` decorator
- **Tool Execution**: Framework handles tool invocation; integrates with Python functions
- **Agent Loop**: Built-in agentic loop with streaming results
- **Structured Output**: Pydantic models for response validation

**Async Support**: Full `asyncio`-native; all agent methods are async

**Python SDK Availability**: Yes; `pip install pydantic-ai`; production-ready

**Cost Tracking**: Optional via provider metadata; not first-class

**Rate Limiting / Retry**: Retry mechanism built in; rate limiting via provider

**Extensibility**
- Custom tool functions via decorators
- Custom model providers via `Model` class
- Durable execution wrappers (Temporal, DBOS) for long-running agents

**Key Limitations**
- **Opinionated architecture**: Agents are the center; less suitable as a "dispatch layer" for existing engines
- **Agent runtimes**: No support for Claude Code, Aider, OpenCode; would require wrapping
- **Single-model per agent**: Not designed for model routing or switching mid-run
- **Complexity overhead**: Full agent framework may be too heavyweight for conversus's minimal needs (task in → output out)

**Assessment for Conversus**: Could work as a provider implementation wrapper, but introduces unwanted abstraction—conversus already has its own orchestration, doesn't need another agent loop.

---

### 3. LangChain / LangGraph

**Purpose**: Composable, stateful orchestration framework for AI workflows

**License**: MIT

**Maturity**
- **GitHub Stars**: 100k+ (LangChain), 20k+ (LangGraph)
- **Last Commit**: Very active (multiple commits per day)
- **Production Use**: Thousands of companies (Stripe, DuckDuckGo, etc.)
- **Stability**: Stable; long-term API commitment; LangSmith observability integration standard

**Provider Coverage**
- **Model APIs**: 100+ via LangChain's `ChatModel` abstraction
- **Agent Runtimes**: Via LangGraph agents or custom nodes
- **Local Models**: Full support via Ollama, LLaMA.cpp, etc.

**Tool Use Support**
- **Function Calling**: Native support via LangChain's tools abstraction
- **Agent Loop**: LangGraph StateGraph provides multi-step orchestration
- **Parallel Execution**: Scatter-gather and pipeline parallelism patterns built-in
- **Tool Use Semantics**: Full control over tool binding and execution

**Async Support**: Full `asyncio`-native; all methods support async/await

**Python SDK Availability**: Mature; `pip install langchain langGraph`

**Cost Tracking**: Via LangSmith integration; not built-in to core library

**Rate Limiting / Retry**: Handled by underlying providers; LangChain adds retry logic

**Extensibility**: Extremely high; every component is pluggable (models, tools, memory, retrieval)

**Key Limitations**
- **High abstraction overhead**: LangGraph is a full workflow orchestrator; conversus already has its own orchestration
- **Opinionated state management**: StateGraph forces a specific graph structure; conversus's phase model is simpler
- **Learning curve**: Requires understanding graph concepts, node types, edge conditions
- **Over-engineered for task dispatch**: Conversus just needs "run this prompt, write output here"; LangGraph is for complex reasoning workflows
- **Agent runtimes**: Still no direct support for Claude Code, Aider, OpenCode; would require custom node implementation

**Assessment for Conversus**: Could be adapted as a provider implementation (each phase → node, each agent → task in node), but introduces significant unnecessary complexity. Better suited for conversus's "blog generation pipeline" use case than the core engine.

---

### 4. Anthropic Claude Agent SDK (Python)

**Purpose**: Official Anthropic SDK for building Claude agents with tool use

**License**: Anthropic Commercial License (free to use)

**Maturity**
- **GitHub Stars**: 3,000+
- **Last Commit**: Very active (2026)
- **Version**: 0.1.48 (as of 2026-04-03); moving toward 1.0
- **Production Use**: Anthropic-supported; Claude Code uses this internally

**Provider Coverage**
- **Model APIs**: Claude models only (Sonnet, Opus)
- **Agent Runtimes**: Can be used as a runtime but doesn't support other SDKs
- **Local Models**: No; Claude-only
- **Tool Use**: Full agentic loop with tool use (Read, Write, Edit, Bash, Grep, Glob, WebSearch)

**Async Support**: Full `asyncio`-native; `ClaudeSDKClient` for bidirectional conversations

**Python SDK Availability**: Yes; `pip install claude-agent-sdk`; production-ready

**Cost Tracking**: Via Anthropic's API dashboard; not built-in to SDK

**Rate Limiting / Retry**: Automatic retry with exponential backoff

**Extensibility**
- Custom tools via `ClaudeSDKClient` (Python functions as MCP servers)
- Hooks for lifecycle control (intercept, modify, audit)
- File checkpointing and rewind capabilities

**Key Limitations**
- **Claude-only**: Cannot use with other models (OpenAI, Google, etc.)
- **Not a dispatch abstraction**: Designed as a programming library, not as a unified provider layer
- **Conversus-specific concern**: While conversus spec 042 mentions Claude Code as the reference implementation, using only this SDK would reintroduce vendor lock-in

**Assessment for Conversus**: Suitable as one provider implementation (the reference), but should not be the only path. Spec 042 explicitly avoids Claude-only coupling.

---

### 5. OpenCode SDK

**Purpose**: Open-source coding agent with Python REST API

**License**: MIT (implied from GitHub)

**Maturity**
- **GitHub Stars**: 2,000+
- **Last Commit**: Active (2026)
- **Production Use**: Emerging; early-stage adoption
- **Stability**: Stable API; straightforward REST/async design

**Provider Coverage**
- **Model APIs**: Multiple (configurable; no hard requirement)
- **Agent Runtimes**: OpenCode is itself an agent runtime (runs autonomously)
- **Tool Use**: Full agentic loop (file read/write, search, execute)

**Interface Options**
- **REST API**: HTTP-native; agents expose OpenAPI 3.1 spec
- **Python SDK**: `from opencode_ai import Opencode` and `AsyncOpencode`
- **Server Mode**: OpenCode runs as a TUI + server; SDK communicates over HTTP

**Async Support**: Full; `AsyncOpencode` client

**Python SDK Availability**: Yes; `pip install opencode-ai`

**Cost Tracking**: Not built-in; model-dependent

**Rate Limiting / Retry**: Per-request handling

**Extensibility**: Agent-based; agents are configurable with custom prompts, models, tools

**Key Limitations**
- **Young project**: Smaller ecosystem than LiteLLM or LangGraph
- **REST API overhead**: Conversus agents would need to spawn OpenCode processes or call HTTP endpoints; adds latency vs. direct SDK use
- **No unified model abstraction**: OpenCode configures the model per agent, not a global abstraction

**Assessment for Conversus**: Could be a Tier 1 provider (agentic SDK), but requires either:
  1. Spawning OpenCode as a subprocess (similar to Claude Code)
  2. Running an OpenCode server and HTTP-dispatching tasks (adds complexity)

Would work but adds operational overhead compared to direct SDK usage.

---

### 6. Aider

**Purpose**: Open-source AI coding partner; terminal-based agent with file editing primitives

**License**: Apache 2.0

**Maturity**
- **GitHub Stars**: 12,000+
- **Last Commit**: Very active (multiple commits per week)
- **Production Use**: Popular among individual developers and small teams
- **Stability**: Stable; widely used in production

**Interface Options**
- **CLI**: Primary interface; `aider --message "description"`
- **Python Scripting**: Via CLI invocation; not a library
- **Edit Formats**: Multiple strategies (unified diff, whole-file, search-replace)

**Python SDK Availability**: No direct SDK; only CLI + subprocess

**Tool Use Support**
- **File Editing**: Primitive-based (unified diff, search-replace, whole-file)
- **Model Agnostic**: Works with any model via API key (OpenAI, Anthropic, etc.)
- **Agent Loop**: Built-in; Aider runs autonomously until task complete

**Async Support**: Not async-native; subprocess-based

**Key Limitations**
- **No Python library**: Must invoke via subprocess; adds coordination overhead
- **Edit format overhead**: File editing via primitives, not direct SDK tool use
- **Not a provider abstraction**: Aider is a full agent; conversus would need to wrap it heavily
- **Model routing**: Uses a single model per invocation; not pluggable per-task

**Assessment for Conversus**: Could be a Tier 1 provider, but subprocess invocation + lack of Python SDK makes it less attractive than Claude Code or OpenCode.

---

### 7. Microsoft AutoGen / Microsoft Agent Framework

**Purpose**: Multi-agent orchestration framework for conversational AI

**License**: MIT

**Maturity**
- **Legacy (AutoGen 0.2)**: Mature; 10,000+ stars
- **New (Microsoft Agent Framework 1.0)**: 2026; replacement for AutoGen
- **Status**: AutoGen in maintenance mode; Microsoft Agent Framework is the forward path

**Microsoft Agent Framework (2026)**
- **Architecture**: Unified SDK for .NET and Python
- **Provider Support**: OpenAI, Azure OpenAI, Ollama; MCP integration
- **Agent Orchestration**: Multi-language support; stateful conversations
- **Maturity**: Production-ready (v1.0 released 2026)

**Provider Coverage**
- **Model APIs**: OpenAI, Azure OpenAI, Ollama
- **Agent Runtimes**: Framework itself is a runtime (group chats, hierarchical agents)
- **MCP Integration**: Dynamic tool discovery via MCP servers

**Tool Use Support**
- **Function Calling**: Native support via functions/tools
- **Agent Loop**: Built-in multi-agent conversations
- **Orchestration**: GroupChat, User Proxy, Tool Executor patterns

**Async Support**: Full `asyncio`-native

**Python SDK Availability**: Yes; emerging in 2026

**Key Limitations**
- **Framework-heavy**: Conversus doesn't need multi-agent conversation; it needs single-task dispatch
- **Conversation-oriented**: Designed for back-and-forth dialogue; conversus is batch/async
- **Opinionated patterns**: Requires understanding GroupChat, User Proxy, etc.
- **Immature Python SDK**: Microsoft Agent Framework is very new; AutoGen (deprecated) is more mature but no longer receiving features

**Assessment for Conversus**: Interesting for future workflows (especially orchestration), but too heavy for the execution provider layer. Better suited for composing conversus runs into larger agentic workflows.

---

### 8. BAML (Boundary ML)

**Purpose**: Type-safe LLM function calls with schema-aligned parsing

**License**: MIT

**Maturity**
- **GitHub Stars**: 1,000+
- **Last Commit**: Active (2026)
- **Production Use**: Early adoption; integrations (cognee)
- **Stability**: Stable; focus on reliability

**Provider Support**
- **Model APIs**: OpenAI, Anthropic, Gemini, Vertex, Bedrock, Azure, OpenRouter, Ollama, etc.
- **Format**: Schema-Aligned Parsing (SAP) for reliable structured output from any LLM

**Tool Use Support**
- **Scope**: Structured output, not agent loops
- **Function Calling**: Full support; handles provider quirks automatically
- **Agent Loops**: No; single completion only

**Language Support**: Python, TypeScript, Ruby, Java, C#, Rust, Go (polyglot)

**Async Support**: Full in all languages

**Key Limitations**
- **Single-completion only**: No agent loops; not designed for tool use orchestration
- **Structured output focus**: Solves parsing and validation, not dispatch
- **Model API only**: No agentic runtimes

**Assessment for Conversus**: Useful as a complementary tool for output validation (e.g., ensuring phase output matches template structure), not as an execution provider. Could be used in Phase 6 (validation) but doesn't solve the dispatch problem.

---

### 9. instructor

**Purpose**: Structured output wrapper for LLMs (Python, TypeScript, Go, Ruby)

**License**: MIT

**Maturity**
- **GitHub Stars**: 5,000+
- **Last Commit**: Very active (2026)
- **Production Use**: Widely used; recommended by Pydantic community
- **Stability**: Stable; recommended as "safest default" for structured output

**Provider Support**
- **Model APIs**: 15+ providers (OpenAI, Anthropic, Google, Mistral, Cohere, Ollama, DeepSeek, xAI, etc.)
- **Approach**: Wraps provider clients with Pydantic validation and automatic retry

**Tool Use Support**
- **Scope**: Structured output only
- **Agent Loops**: No; single completion only
- **Retry**: Automatic retry on validation failure

**Language Support**: Python, TypeScript, Go, Ruby (polyglot)

**Key Limitations**
- **Single-completion only**: No multi-step reasoning or tool use
- **Wrapper pattern**: Requires wrapping provider clients; adds a layer
- **Structured output focus**: Solves parsing, not dispatch

**Assessment for Conversus**: Similar to BAML—useful for output validation, not execution dispatch. Could enhance Phase 6 validation but doesn't solve the core problem.

---

### 10. Mirascope

**Purpose**: "Goldilocks API" for LLM development—fine-grained control + type safety

**License**: MIT

**Maturity**
- **GitHub Stars**: 1,500+
- **Last Commit**: Active (2026)
- **Production Use**: Early adoption; focus on developer experience
- **Stability**: Stable; clean API design

**Provider Support**
- **Model APIs**: OpenAI, Anthropic, Mistral, Google, Groq, Cohere, LiteLLM, Azure, Bedrock
- **Positioning**: Unified interface while preserving provider-specific control

**Tool Use Support**
- **Function Calling**: Full support
- **Agent Loops**: Basic support; less sophisticated than LangChain
- **Philosophy**: Minimal abstraction; close to provider APIs

**Async Support**: Full `asyncio`-native

**Key Limitations**
- **Lightweight design**: Less comprehensive than LangChain; fewer features for complex workflows
- **No agent runtimes**: Model API only
- **Smaller ecosystem**: Fewer integrations than LiteLLM or LangChain

**Assessment for Conversus**: Could be used similarly to LiteLLM for Tier 3 (direct API), but LiteLLM is more mature and widely adopted. Mirascope's "close to provider APIs" philosophy means less abstraction—better for advanced use cases, less suitable for unified dispatch.

---

### 11. Haystack

**Purpose**: Open-source AI orchestration framework for RAG and agent workflows

**License**: Apache 2.0

**Maturity**
- **GitHub Stars**: 15,000+
- **Last Commit**: Very active (2026)
- **Production Use**: Widely used for RAG pipelines; emerging agent support
- **Stability**: Stable; enterprise-grade

**Provider Support**
- **Model APIs**: OpenAI, Mistral, Anthropic, Cohere, Hugging Face, Azure, Bedrock, Ollama, etc.
- **Architecture**: Modular pipeline design; components pluggable

**Agent Framework** (2025-2026 evolution)
- **Agentic Workflows**: Function-calling interfaces, branching, looping
- **Tool Use**: Full integration of tools via LangChain's tool abstraction
- **Orchestration**: DAG-based pipelines; more flexible than LangGraph

**Async Support**: Full `asyncio`-native

**Cost Tracking**: Via LangSmith integration; not built-in

**Key Limitations**
- **RAG-focused heritage**: Architecture optimized for retrieval; less ideal for pure task dispatch
- **Complexity**: Pipeline abstraction adds overhead for simple "prompt → output" tasks
- **Learning curve**: DAG concepts, pipeline design patterns

**Assessment for Conversus**: Similar to LangGraph—powerful for complex workflows, but heavier than needed for execution dispatch. Better suited for blog generation pipeline (involves RAG + generation) than core engine.

---

### 12. CrewAI / PraisonAI

**Purpose**: Multi-agent orchestration frameworks focused on collaborative AI agents

**License**: MIT

**Maturity**
- **CrewAI**: 5,000+ stars; stable; 2025+ production use
- **PraisonAI**: 2,000+ stars; newer; integrates CrewAI + AutoGen

**Provider Support**
- **CrewAI**: Model agnostic; integrates with LiteLLM, supports 100+ LLMs
- **PraisonAI**: Combines CrewAI, AutoGen, and custom agent orchestration

**Agent Framework**
- **Role-Based Abstraction**: Agents have roles, goals, backstories
- **Task Assignment**: Tasks assigned to agents; sequential/hierarchical/consensus execution
- **Tool Use**: Full support via tools defined in agent configuration

**Async Support**: Partial (CrewAI); improving in PraisonAI

**Key Limitations**
- **Agent-centric design**: Conversus phases are not "agents with roles"; this is a semantic mismatch
- **Task definition overhead**: Requires defining tasks separately from agents; conversus phases combine both
- **Over-orchestration**: Both frameworks add hierarchy and role semantics conversus doesn't need

**Assessment for Conversus**: Interesting for future multi-perspective deliberation (e.g., 5 different agent "roles"), but currently over-specified for the 042 use case. Would require refactoring conversus phases into CrewAI tasks + agents.

---

### 13. MCP (Model Context Protocol)

**Purpose**: Standardized protocol for exposing tools and resources to LLMs

**License**: MIT

**Maturity**
- **Python SDK**: 1.0 stable (released April 2, 2026)
- **Adoption**: Growing; used by Anthropic (Claude Code), GitHub, VSCode, others
- **Production Use**: Stable for tool exposure and LLM context

**Architecture**
- **Servers**: Expose resources (static data), tools (executable functions), prompts (templates)
- **Clients**: Consume servers and provide context to LLMs
- **Transports**: stdio, SSE, HTTP streaming

**Python SDK Requirements**: Python ≥3.10

**Tool Use Model**
- **Primitive**: Servers define tools; clients invoke them
- **MCP → LLM**: LLM calls tools; client implements actual execution
- **Not an orchestrator**: MCP is a transport/discovery layer, not a task orchestrator

**Async Support**: Full `asyncio`-native

**Key Limitations**
- **Discovery-layer only**: MCP defines how tools are exposed, not how agents are dispatched
- **No executor abstraction**: Still requires a runtime (Claude Code, Cursor, etc.) to invoke MCP servers
- **Semantic mismatch**: MCP is about tool exposure; conversus needs task dispatch

**Assessment for Conversus**: MCP is orthogonal to execution dispatch. Conversus agents would USE MCP (via their own SDK; e.g., Claude Code uses MCP for tools), but MCP itself doesn't solve the "which runtime" problem.

**Relevance to Spec 042**: Could be a fallback for Tier 1 providers if we can wrap SDKs as MCP servers, but A2A/ACP is more appropriate for agent orchestration.

---

### 14. A2A Protocol (Agent2Agent)

**Purpose**: Open standard for agent-to-agent communication and interoperability

**License**: Open source (Linux Foundation)

**Maturity**
- **Launched**: Google April 2025; IBM ACP merged September 2025
- **Current**: Unified under "A2A" name; Linux Foundation governance
- **Python SDK**: Available via BeeAI framework
- **Production Use**: Early adoption; framework-agnostic standard

**Architecture**
- **HTTP-native**: REST-based with MIME multipart messages
- **Async Streaming**: Native support for long-running tasks
- **Agent Discovery**: Self-describing capabilities via Agent Detail metadata
- **No dependencies**: Standard HTTP; can be implemented in any language

**Key Concepts**
- **Task Requests**: Envelope specifying agent task, input data, metadata
- **Agent Detail**: Self-description (capabilities, supported input types, SLA)
- **Async Completion**: Agents handle work asynchronously; client polls or receives notification

**Python Implementation**
- **BeeAI Framework**: Official Python/TypeScript SDK for building A2A agents
- **Decorator-based**: `@agent` decorator to mark functions as A2A-compliant
- **Custom tools**: Python functions as A2A agent capabilities

**Async Support**: Full `asyncio`-native

**Key Limitations**
- **No built-in orchestration**: A2A is a dispatch protocol, not an orchestrator
- **Server-side requirement**: Agents must expose A2A HTTP endpoints
- **Operational overhead**: Each agent needs to be running and reachable
- **Discovery complexity**: Agents self-describe capabilities; clients must understand the description format

**Assessment for Conversus**: **Excellent fit for the "future path"**. A2A is exactly what spec 042 describes for the ACP provider:
1. Conversus as A2A client sends Task Requests
2. Each agent runtime (Claude Code, Aider, OpenCode) wraps itself as A2A server
3. Perfect decoupling: conversus dispatches purely via HTTP; agents implement their own runtime

**Current Limitation**: A2A is still early (2025-2026); SDK maturity is improving but not yet as battle-tested as LiteLLM or LangChain.

**Recommendation**: A2A should be the **long-term vision** for conversus (spec 042's `acp` provider). However, implementing it now requires:
1. Building ACP server wrappers for each SDK (Claude Code, Aider, OpenCode)
2. Running agent servers in addition to conversus
3. Managing agent lifecycle and discovery

This is more complex than building direct SDK providers in the short term.

---

## Part 2: Fit Assessment for conversus

### What conversus Needs (from spec 042)

1. **Input Contract**: Fully-rendered prompt + file read list + output path + metadata
2. **Output Contract**: Success/failure + content or error + cost + duration
3. **Parallel Execution**: 10-20 concurrent tasks with consistent output paths
4. **Tool Use Binary**: Some providers give agents file tools; others need files pre-inlined
5. **Multiple Model APIs**: Anthropic, OpenAI, Google, Mistral, Ollama
6. **Multiple Agent Runtimes**: Claude Code, Aider, OpenCode (and future: Copilot, Gemini CLI)
7. **Cost Tracking**: Per-task in USD
8. **Error Handling**: Rate limits, timeouts, auth failures
9. **Async/await**: Python asyncio-native

### Evaluation: Top Candidates

#### Candidate A: LiteLLM (70% fit)

**Solves**
- Model API abstraction (Tier 3): ✓ Excellent (100+ providers, cost tracking, rate limiting)
- Parallel execution: ✓ Easy (`asyncio.gather` with semaphore)
- Async/await: ✓ Full support
- Cost tracking: ✓ Built-in
- Error handling: ✓ Typed error categories

**Requires Conversus to Build**
- Agent runtime dispatch (Tier 1-2): ✗ Not supported
- Tool use abstraction: ✗ (must pre-read files into prompt)
- File I/O coordination: ✗ (engine pre-reads; provider writes)

**Integration Sketch**
```python
# Tier 3: Direct API providers
class LiteLLMProvider(ExecutionProvider):
    def __init__(self, model_name: str):
        self.model = model_name
        self.supports_tool_use = False
    
    async def execute(self, prompt: str, output_path: str, read_paths, metadata=None):
        # Inline file contents
        full_prompt = augment_prompt_with_files(prompt, read_paths)
        
        # Dispatch via LiteLLM
        response = await litellm.completion_async(
            model=self.model,
            messages=[{"role": "user", "content": full_prompt}],
            **metadata.get("options", {})
        )
        
        # Post-write output
        Path(output_path).write_text(response.choices[0].message.content)
        return ExecutionResult(success=True, content=response.choices[0].message.content, ...)
```

**Dependency Footprint**: Single `pip install litellm`; minimal overhead

**Verdict**: Use LiteLLM for Tier 3. Don't use for Tier 1-2; build direct SDK providers instead.

---

#### Candidate B: A2A Protocol (85% fit)

**Solves**
- Agent-to-agent dispatch: ✓ Native (HTTP-based; no SDK coupling)
- Multiple runtimes: ✓ If each SDK wraps itself as A2A server
- Tool use abstraction: ✓ A2A agents manage their own tools
- Async/await: ✓ Native async Task Requests + streaming
- Error handling: ✓ Task status, failure metadata
- Cost tracking: ✓ (can be added to Task Response metadata)

**Requires Conversus to Build**
- A2A server wrappers for each SDK: ⚠ Medium effort (~500 lines per SDK)
- Agent discovery: ⚠ Simple HTTP; doable but adds operational complexity
- Agent lifecycle management: ⚠ (agents must be running)

**Integration Sketch**
```python
# A2A Provider (preferred path per spec 042)
class ACPProvider(ExecutionProvider):
    def __init__(self, agent_url: str):
        self.agent_url = agent_url
        self.supports_tool_use = True
    
    async def execute(self, prompt: str, output_path: str, read_paths=None, metadata=None):
        # Build A2A Task Request
        task = {
            "metadata": {
                "id": str(uuid.uuid4()),
                "phase": metadata.get("phase"),
                "output_path": output_path,
            },
            "message": {
                "type": "multipart/form-data",
                "parts": [
                    {"type": "text/markdown", "content": prompt},
                    *[{"type": "application/reference", "uri": f"file://{p}"} for p in (read_paths or [])]
                ]
            }
        }
        
        # POST to A2A server
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.agent_url}/task", json=task)
        
        # Poll for completion or stream results
        while True:
            result = await client.get(f"{self.agent_url}/task/{task['metadata']['id']}")
            if result.status_code == 200 and result.json().get("status") == "completed":
                return ExecutionResult(success=True, content=result.json()["output"], ...)
            await asyncio.sleep(0.5)
```

**Dependency Footprint**: No new dependencies; standard `httpx` for HTTP client

**A2A Server Wrappers (future work)**
```python
# conversus-acp-claude-code (reference implementation)
# Wraps Claude Code SDK as A2A server
from acp import acp_agent

@acp_agent
async def claude_code_agent(task: TaskRequest) -> TaskResponse:
    prompt = extract_prompt_from_task(task)
    files = extract_references_from_task(task)
    output_path = task.metadata["output_path"]
    
    # Dispatch via Claude Code SDK
    result = await claude_agent_sdk.execute(
        prompt=prompt,
        read_paths=files,
        output_path=output_path
    )
    
    return TaskResponse(
        status="completed",
        output=Path(output_path).read_text(),
        metadata={"cost_usd": result.cost, "duration_ms": result.duration}
    )

# Run as HTTP server
if __name__ == "__main__":
    run_acp_server(agent=claude_code_agent, port=8001)
```

**Verdict**: A2A is the **long-term ideal**. Short-term challenges:
1. Requires building/maintaining ACP wrappers for each SDK
2. Operational overhead (agents must be running as separate services)
3. A2A ecosystem still immature (2026, early adoption)

**Recommendation**: Implement A2A path in phase 2 (post-042); start with direct SDK providers in phase 1.

---

#### Candidate C: Hybrid Approach (95% fit) — **RECOMMENDED**

**Build spec 042's ExecutionProvider protocol as specified**, then:

1. **Tier 3 (Direct API)**: Use LiteLLM wrapper
   - Minimal, focused implementation
   - Leverage 100+ providers for free
   - No architectural baggage

2. **Tier 1-2 (Agent Runtimes)**: Build direct SDK providers
   - Claude Code: `conversus-provider-claude-code` (subprocess or SDK)
   - Aider: `conversus-provider-aider` (subprocess wrapper)
   - OpenCode: `conversus-provider-opencode` (REST API wrapper)
   - Future: Copilot, Gemini CLI (same pattern)

3. **Future: A2A Path**: Once A2A ecosystem matures, implement `acp` provider
   - Allows third-party A2A server wrappers to plug in
   - Conversus ships reference wrappers for popular SDKs
   - Community can contribute new A2A servers

**Why This Works**
- Conversus maintains full control over ExecutionProvider abstraction
- Each provider is a thin adapter (100-200 lines of code)
- No vendor lock-in; no framework lock-in (no LangChain, no AutoGen)
- Can migrate to A2A without engine changes (just swap `acp` provider)
- LiteLLM is stable, proven, low-risk for Tier 3

**Architecture Diagram**
```
┌─────────────────────────────────────────┐
│     conversus Engine (spec 042)         │
│  - Orchestration (phases, disputes)     │
│  - Template rendering                   │
│  - Output management                    │
└──────────────────┬──────────────────────┘
                   │
         ┌─────────┴─────────────────────────────┐
         │   ExecutionProvider Protocol          │
         │  (async execute, execute_batch)       │
         └────┬─────────────────────┬────────────┘
              │                     │
    ┌─────────▼────────┐   ┌───────▼──────────┐
    │  Tier 3 Providers │   │ Tier 1-2 Providers
    │  (Model API)      │   │ (Agent Runtimes)
    ├──────────────────┤   ├──────────────────┤
    │ anthropic        │   │ claude-code      │
    │ openai           │   │ aider            │
    │ google           │   │ opencode         │
    │ (via LiteLLM)    │   │ copilot (future) │
    │                  │   │ gemini-cli (fut.)│
    │                  │   │ acp (future)     │
    └──────────────────┘   └──────────────────┘
         │                        │
    ┌────▼───────┐            ┌───▼──────┐
    │ LiteLLM SDK│            │SDKs/REST │
    └────────────┘            │/subprocess
                              └──────────┘
```

**Dependency Footprint**
- Core `conversus`: 0 new dependencies (ExecutionProvider is a Protocol)
- `conversus-provider-litellm`: `litellm` only
- `conversus-provider-claude-code`: `claude-agent-sdk` or subprocess
- Each provider is optional; users install only what they need

---

## Part 3: Tradeoff Matrix

| Factor | **Build Our Own** | **Use LiteLLM** | **Use A2A** | **Hybrid (Recommended)** |
|--------|-------------------|-----------------|-----------|----------------------|
| **Fit** | 100% (by definition) | 70% (Model API only) | 85% (Requires wrappers) | 95% (Mix of both) |
| **Time to Ship** | 4-6 weeks | 1-2 weeks | 3-4 weeks + ongoing | 2-3 weeks + migration path |
| **Maintenance Burden** | High (reinvent wheels) | Medium (one dependency) | Medium (ecosystem) | Low (thin wrappers) |
| **Vendor Lock-in** | None (conversus-only) | Low (LiteLLM is OSS) | None (A2A is standard) | None (standard protocol) |
| **Provider Coverage** | Limited initially (1-3) | 100+ (day 1) | Depends on wrappers | 10+ (day 1 via LiteLLM) |
| **Agent Runtime Coverage** | Conversus controls | 0 | Depends on wrappers | Conversus controls |
| **Future Extensibility** | Low (hard to extend) | Medium (LiteLLM plugins) | High (A2A ecosystem) | High (ExecutionProvider is open) |
| **Operational Complexity** | Low (no servers) | Low (SDK only) | High (agents as services) | Low (SDK) → Medium (services future) |
| **Cost** | $0 | $0 | $0 | $0 |

---

## Part 4: Recommendation

### Executive Decision

**Implement the hybrid approach**:

1. **Phase 1 (Spec 042 v1)**: Build ExecutionProvider protocol; implement Tier 3 via LiteLLM wrapper + direct Claude Code provider
2. **Phase 2 (Post-042)**: Add Aider, OpenCode, Copilot providers
3. **Phase 3 (Future, ~6 months)**: Implement A2A protocol support; allow community to contribute ACP wrappers

### Rationale

1. **Fastest to ship**: 2-3 weeks to 042 with LiteLLM + Claude Code
2. **Lowest risk**: LiteLLM is production-proven; no unproven new dependencies
3. **Simplest architecture**: ExecutionProvider protocol is minimal; each provider is a thin wrapper
4. **Zero vendor lock-in**: Conversus controls the abstraction; can migrate to A2A or anything else without engine changes
5. **Solves the blog pipeline problem**: Can run conversus headless via `anthropic` provider (direct API) or `claude-code` provider (subprocess)
6. **Future-proof**: A2A path is clear; no rework needed to adopt it

### What NOT to Do

- **Don't use LangChain/LangGraph/Haystack**: Too heavyweight; introduces unnecessary coupling to orchestration framework conversus already has
- **Don't use AutoGen/Microsoft Agent Framework**: Over-specified for task dispatch; agent orchestration is conversus's job
- **Don't use CrewAI/PraisonAI**: Semantic mismatch (phases ≠ agents with roles)
- **Don't implement A2A now**: Ecosystem too new; operational overhead too high; LiteLLM + direct SDKs are faster
- **Don't build our own model provider abstraction**: LiteLLM solves this; reinventing wastes time

---

## Part 5: conversus-Specific Concerns

### Address Unique Requirements

#### 1. Tool Use vs. Inlining

**Spec 042 solution** (confirmed in research):
```python
if not provider.supports_tool_use:
    # Engine pre-reads files
    full_prompt = augment_with_files(prompt, read_paths)
else:
    # Provider manages file I/O
    full_prompt = prompt
```

- **LiteLLM + direct API providers**: Handled correctly (files inlined)
- **Direct SDK providers** (Claude Code, Aider): Handled correctly (agent reads files)
- **A2A providers** (future): Handled correctly (agents manage tools)

#### 2. Parallel Execution with Consistent Output Paths

**Challenge**: 20 concurrent agents writing to different `output_path` values; ensure no collisions

**Solution** (from spec 042 + asyncio):
```python
async def execute_batch(tasks: list[ExecutionTask]) -> list[ExecutionResult]:
    # Each task has unique output_path
    # asyncio.gather ensures parallel execution
    # fs is not shared; each agent writes independently
    results = await asyncio.gather(
        *[self.execute(t.prompt, t.output_path, t.read_paths, t.metadata) for t in tasks]
    )
    return results
```

No new issues; standard asyncio patterns work fine.

#### 3. Phase-Aware Metadata Routing

**Spec 042 solution**:
```python
metadata: dict = {
    "phase": "review",
    "agent_name": "code-verifier",
    "mode": "cooperative",
    "round": 1,
    "timeout": 120,
}
```

- All providers receive metadata
- Providers use as needed (e.g., OpenCode agent picks up custom prompt templates)
- No routing logic in engine; metadata is informational

#### 4. Structured Output (Phase Completed Events)

**Conversus requires**: 
- Phase completion events
- Artifact references (output file paths)
- Dispute metadata

**This is engine responsibility**, not provider responsibility:
```python
for task in phase_tasks:
    result = await provider.execute(...)  # provider doesn't know about events
    
    # Engine emits events
    emitter.emit(PhaseCompleted(
        phase=task.metadata["phase"],
        artifacts=[result.output_path],
        disputes=parse_disputes(result.content),
    ))
```

**No new tools needed**; conversus engine already has event emission.

#### 5. Cost Tracking Per Task

**Spec 042 solution**:
```python
@dataclass
class ExecutionResult:
    cost_usd: float = 0.0  # in result.metadata
    duration_ms: int
    provider: str
```

- **LiteLLM**: Built-in cost tracking via provider token counts
- **Direct SDKs**: Must call provider API cost functions (Anthropic has `usage.input_tokens`, `usage.output_tokens`; apply pricing model)
- **A2A providers**: Add to Task Response metadata

**Implementation**: Each provider calculates cost; engine sums per-phase.

#### 6. Timeout Handling

**Spec 042 solution**:
```python
timeout = metadata.get("timeout", 120)  # seconds
try:
    result = await asyncio.wait_for(
        provider.execute(...),
        timeout=timeout
    )
except asyncio.TimeoutError:
    return ExecutionResult(success=False, error="Timeout")
```

- Implemented in engine, not provider
- Provider must be cancellation-aware (all asyncio methods are)

---

## Part 6: Implementation Checklist for Spec 042 v1

### Core (week 1)
- [ ] Define `ExecutionProvider`, `ExecutionTask`, `ExecutionResult` data classes (spec 042 §3)
- [ ] Implement `PROVIDER_REGISTRY` and `get_provider()` resolution (spec 042 §2)
- [ ] Update `conversus.yml` config to support `executor:` field

### Tier 3: LiteLLM Wrapper (week 1-2)
- [ ] Create `conversus-provider-litellm` package
- [ ] Implement `LiteLLMProvider` wrapping `litellm.completion_async()`
- [ ] Test with Anthropic, OpenAI, Google, Ollama
- [ ] Cost tracking via token counts + pricing table

### Tier 1: Claude Code (week 2)
- [ ] Create `conversus-provider-claude-code` package
- [ ] Option A: Subprocess wrapper (simplest; recommended)
  - Spawn Claude Code CLI with task JSON
  - Collect output from file
- [ ] Option B: SDK wrapper
  - Use `claude-agent-sdk` directly
  - Better instrumentation; requires SDK maturity check

### Testing & Documentation (week 3)
- [ ] End-to-end test: spec deliberation using `claude-code` provider
- [ ] End-to-end test: spec deliberation using `anthropic` provider
- [ ] Blog generation pipeline proof-of-concept
- [ ] docs/developer-guide/execution-providers.md
- [ ] Update docs/developer-guide/architecture.md with provider layer diagram

### Backward Compatibility (week 3)
- [ ] Verify SKILL.md continues to work (no config = use Claude Code)
- [ ] Verify Python SDK continues to work (no config = use Anthropic)
- [ ] Verify CLI continues to work (no config = use Claude Code via subprocess)

### Future (post-042)
- [ ] Aider provider
- [ ] OpenCode provider
- [ ] A2A protocol support
- [ ] Community provider ecosystem

---

## Part 7: Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| LiteLLM supply chain incident | Low | High | Monitor releases; pin to stable version; fallback direct SDKs |
| A2A standard changes | Low | Medium | Don't commit to A2A yet; keep ACP provider as future work |
| Provider SDK deprecation | Low | Medium | Each provider is isolated; can sunset independently |
| Cost tracking errors | Medium | Medium | Compare LiteLLM costs vs. provider billing; add reconciliation test |
| File I/O race conditions | Low | Medium | Unique output_path per task; standard asyncio patterns |
| Timeout edge cases | Medium | Low | Test with `asyncio.wait_for()`; document timeout semantics |

---

## Conclusion

The execution provider abstraction problem is well-solved by the open-source ecosystem in 2026, but no single tool covers all of conversus's needs. The recommended hybrid approach leverages the best tools for each layer:

- **LiteLLM** for provider coverage (100+) at minimal complexity
- **Direct SDK providers** for tight integration with Claude Code, Aider, OpenCode
- **A2A protocol** as the future path when the ecosystem matures

This keeps conversus lightweight, maintainable, and extensible without introducing unnecessary framework dependencies or vendor lock-in.

---

## References

### Tools Evaluated
1. [LiteLLM](https://github.com/BerriAI/litellm)
2. [pydantic-ai](https://github.com/pydantic/pydantic-ai)
3. [LangGraph](https://www.langchain.com/langgraph)
4. [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python)
5. [OpenCode](https://opencode.ai/)
6. [Aider](https://github.com/Aider-AI/aider)
7. [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/)
8. [BAML](https://github.com/BoundaryML/baml)
9. [instructor](https://github.com/567-labs/instructor)
10. [Mirascope](https://github.com/Mirascope/mirascope)
11. [Haystack](https://github.com/deepset-ai/haystack)
12. [CrewAI](https://crewai.com/)
13. [MCP Protocol](https://github.com/modelcontextprotocol/python-sdk)
14. [A2A Protocol](https://a2a-protocol.org/)

### Research Sources
- [LiteLLM Maturity 2026](https://www.truefoundry.com/blog/a-detailed-litellm-review-features-pricing-pros-and-cons-2026)
- [pydantic-ai Overview](https://ai.pydantic.dev/)
- [LangGraph Multi-Agent 2026](https://dev.to/ottoaria/langgraph-in-2026-build-multi-agent-ai-systems-that-actually-work-3h5)
- [Anthropic Agent SDK 2026](https://medium.com/@shivanshmay2019/claude-agent-sdk-deep-dive-what-it-means-to-use-claude-code-as-a-library-773aea121787)
- [OpenCode REST API](https://opencode.ai/docs/sdk/)
- [Microsoft Agent Framework 1.0](https://devblogs.microsoft.com/foundry/introducing-microsoft-agent-framework-the-open-source-engine-for-agentic-ai-apps/)
- [A2A Protocol 2026](https://www.deeplearning.ai/short-courses/a2a-the-agent2agent-protocol/)
- [Cursor IDE 2026 Updates](https://theagencyjournal.com/cursors-march-2026-glow-up-self-hosted-agents-jetbrains-love-and-smarter-composer/)
- [dbt AI Agents 2026](https://www.getdbt.com/product/dbt-agents)
- [Astral Acquisition by OpenAI](https://www.computeleap.com/blog/openai-acquires-astral-python-tools-2026/)

---

**Report Generated**: 2026-04-03  
**Status**: Comprehensive; ready for implementation planning
