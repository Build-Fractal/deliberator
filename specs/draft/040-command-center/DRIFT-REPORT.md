# Drift Report — Spec 040: Command Center

**Report date**: 2026-04-05
**Analyzed against**: current codebase HEAD (main)
**Key post-040 spec**: 042-execution-providers (binding condition #5 — cost telemetry)

---

## Executive Summary

Spec 040 was written before spec 042 defined the `ExecutionProvider` cost telemetry system. The drift is structural: 040 assumes cost data flows from `AgentCompleted` events (which carry no cost), but 042 actually placed real-cost data on `ExecutionResult.cost` — a field that the engine currently drops before any downstream consumer (web layer, SDK, or a future Command Center) can see it.

The gap is not hypothetical. The `Cost` dataclass (`engine/execution/provider.py`) exists, providers populate it correctly, but the pipeline discards it before surfacing anything to the web layer. The web layer then reconstructs an approximation using a fixed-token heuristic. A Command Center built today against the spec 040 design would inherit that approximation and lose the real per-execution signal that spec 042 explicitly intended for it to consume.

---

## Drift Analysis

### 1. What spec 040 assumed about cost data

Spec 040 §2 (FR-016) requires:

> After gap-filling, the system MUST show a plain-language summary of the assembled objective and **a cost estimate** before starting deliberation.

Spec 040 §5.2 (WebGapFiller) and §3 (layer diagram) both treat cost as dashboard content, with `provider+token pricing → USD display` feeding the Command Center's activity and team views (US-3, US-6). The implicit assumption is that the engine surfaces cost data the dashboard can consume directly.

Spec 040's docstring on `Cost` (`engine/execution/provider.py`, line 103–105) confirms this design intent explicitly:

> "The distinction between 'unknown' and 'zero' is load-bearing for downstream aggregation in the command center (spec 040) and monetization tier tracking (spec 033)."

### 2. What spec 042 actually built

Spec 042 defined a proper cost telemetry chain:

| Layer | What it does | File |
|-------|-------------|------|
| `Cost` dataclass | Structured per-execution cost: `input_tokens`, `output_tokens`, `usd` (nullable), `currency` | `engine/execution/provider.py` |
| `AnthropicExecutionProvider` | Extracts real token counts from `response.usage`, sets `usd=None` (SDK does not report dollars) | `engine/execution/providers/anthropic.py` |
| `ClaudeCodeProvider` | Parses `total_cost_usd` + per-model usage from `--output-format json`; this is the only provider that CAN set a real `usd` value | `engine/execution/providers/claude_code.py` |
| `MockExecutionProvider` | Reports `Cost(input_tokens=0, output_tokens=0, usd=None)` — zero tokens, not zero dollars | `engine/execution/providers/mock.py` |
| `ModelProviderExecutionAdapter` | Always sets `cost=None` — legacy `ModelProvider.complete()` returns only text, no usage data | `engine/dispatch.py` line 164 |

### 3. Where cost data is dropped

`ExecutionResult.cost` is populated correctly by native providers. The problem is what happens after `execute()` returns:

**`dispatch_agent()` in `engine/dispatch.py`** (lines 298–312): After calling `exec_provider.execute(task)`, the function reads `result.content` and `result.error`, then emits `AgentCompleted`. It never reads `result.cost` and never attaches cost to the event.

**`AgentCompleted` in `engine/events.py`** has no `cost` field at all. The event carries: `phase`, `agent_name`, `success`, `error`, `duration_ms`, `timestamp`, `response_text`. Zero cost fields.

**`PipelineResult` in `engine/phases.py`** (lines 59–72) carries: `output_dir`, `written_files`, `active_agents`, `phases_completed`, `total_dispatches`, `rounds_completed`, `termination_reason`, `arbitration_ran`. Zero cost fields.

**`engine/sdk.py` `Result`** (lines 64–84): `headline`, `summary`, `full_analysis`, `quality_indicators`, `debate_transcript`, `rounds_completed`, `termination_reason`, `written_files`, `output_dir`. Zero cost fields.

Cost is fully dropped at the `dispatch_agent()` boundary. It never reaches the SDK, the web layer, or any future Command Center consumer.

### 4. What the web layer does instead

`web/app.py` `_calculate_actual_cost()` (lines 791–820) reconstructs an approximation:

```python
launch_count = sum(1 for ev in events if isinstance(ev, AgentCompleted) and ev.success)
# Estimate ~4000 input + ~2000 output tokens per launch on average
```

This is an event-count heuristic multiplied by static average token estimates from a pricing table. It is a pre-spec-042 workaround that 042's `Cost` telemetry was designed to replace. The web layer reports `actual_cost_usd` via this approximation while the real per-execution data sits unused in `ExecutionResult.cost` inside `dispatch_agent()`'s stack frame.

### 5. Downstream consequences for spec 040

The Command Center spec relies on cost data in two concrete ways:

**FR-016** (cost estimate before deliberation): The `GET /api/estimate` endpoint works correctly — it uses `engine/cost.py` `estimate_cost_usd()` which is pre-execution estimation, not affected by this gap.

**Post-execution cost display** (US-3, US-5, US-6 — result summary with cost, team activity feed with cost trends): These require real per-run actual cost. Today that is `actual_cost_usd` from the heuristic. With spec 042's real telemetry, it could be the sum of `result.cost.usd` values across all `ExecutionResult`s in a run. The Command Center cannot currently get the latter because the pipeline never aggregates or surfaces it.

**Monetization tier tracking** (spec 033, referenced in the `Cost` docstring at line 103): The Command Center's Enterprise tier visibility (US-6 trends) is specifically called out in the `Cost` dataclass comment as a consumer. That consumer does not exist yet — but it is designed to consume `Cost` objects, not the heuristic in `_calculate_actual_cost`.

---

## Specific Gaps to Resolve Before Building Command Center Cost Tracking

These are not spec 040 errors — 040 predates 042. They are implementation gaps between the two specs that must close before the Command Center dashboard can display real cost data.

### Gap A — `AgentCompleted` has no cost field

`engine/events.py` `AgentCompleted` needs an optional `cost: Cost | None = None` field so `dispatch_agent()` can attach per-execution cost to the event stream. This is the minimum change that makes real cost data flow to any consumer (SSE stream → web layer → dashboard).

### Gap B — `dispatch_agent()` does not read `result.cost`

`engine/dispatch.py` line 303 emits `AgentCompleted` without reading `result.cost`. After Gap A is resolved, this function needs one line: `cost=result.cost` in the `AgentCompleted` constructor.

### Gap C — `PipelineResult` has no aggregate cost field

Once per-agent cost flows through events, the pipeline (or the SDK's `Result`) should aggregate total `input_tokens`, `output_tokens`, and `usd` (summing non-None values, carrying None when any provider could not report). Without this, the Command Center must re-aggregate from the raw event log on every query.

### Gap D — The web `_calculate_actual_cost()` heuristic can be retired

`web/app.py` line 791 can be replaced with a sum over `AgentCompleted.cost` once Gap A/B land. The heuristic should not carry forward into the Command Center's design — it produces systematically wrong numbers for runs that mix models or have varying response lengths.

### Gap E — `ModelProviderExecutionAdapter` always produces `cost=None`

`engine/dispatch.py` line 164 (`# ModelProvider does not report cost data — leave None`). This is correct behavior — the adapter wraps legacy `ModelProvider` which returns only text. But it means any run using the adapter path (legacy `anthropic` or `openai` through `ModelProvider`) produces no cost data at all, even in the future Command Center. The Command Center spec should document that cost display requires a native `ExecutionProvider` (not the legacy adapter path).

---

## What is Already Aligned

The following parts of spec 040's design are not in drift:

- **Pre-execution cost estimation** (FR-016, `GET /api/estimate`): Works correctly via `engine/cost.py`. No gap.
- **SSE event streaming** for real-time dashboard updates: `AsyncQueueEmitter` is implemented and used in `web/app.py`. The event infrastructure spec 040 relies on exists. The gap is only that cost is not in the events.
- **Engine immutability constraint** (spec 040 §8): The `Cost` telemetry additions to spec 042 were additive and do not modify deliberation logic. The "must not modify the engine" constraint in 040 is compatible with adding `cost` to `AgentCompleted`.
- **`web/` as prototype**: Spec 040 §1 and §2 explicitly note the `web/` directory is a prototype tied to Supabase, not the Command Center starting point. The Supabase-coupled code in `web/app.py` and `web/db.py` is consistent with this — it is not intended as Command Center production code.

---

## Summary Table

| Spec 040 Assumption | Actual State | Gap Severity |
|---------------------|-------------|-------------|
| Cost data available per-run for dashboard | `ExecutionResult.cost` exists but is dropped at `dispatch_agent()` — never reaches SDK or web layer | **High** — core dashboard metric missing |
| Real token counts per agent available | `AnthropicExecutionProvider` and `ClaudeCodeProvider` populate them; never propagated past `execute()` | **High** — data exists but is unreachable |
| `AgentCompleted` event carries cost | No `cost` field on `AgentCompleted` | **High** — event schema gap |
| Heuristic cost estimate is the current state | `_calculate_actual_cost()` uses fixed token averages per launch | **Medium** — works as fallback, not production quality |
| Command Center can consume `Cost.usd` directly | `usd` is `None` for all providers except `claude-code` (which reports via JSON output); dollar amount requires pricing-table lookup elsewhere | **Low** — by design per spec 042; Command Center must apply pricing table |
| Pre-execution cost estimate works | `GET /api/estimate` + `engine/cost.py` `estimate_cost_usd()` | **No gap** |
| SSE streaming infrastructure exists | `AsyncQueueEmitter` implemented | **No gap** |
