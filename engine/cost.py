"""Shared cost estimation for conversus deliberations.

Provides the canonical D007 formula for estimating LLM launches per phase.
Used by CLI, SDK, MCP server, and web API — extracted here to avoid
duplication (CQ-1).
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Per-model pricing (USD per 1M tokens) — updated 2025-Q1
# ---------------------------------------------------------------------------

MODEL_PRICING: dict[str, dict[str, float]] = {
    # Anthropic
    "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
    "claude-opus-4-20250514": {"input": 5.00, "output": 25.00},
    "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
    "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
    "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
    # OpenAI
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
}

# Default pricing when model is unknown — use claude-sonnet-4 as baseline
_DEFAULT_PRICING = {"input": 3.00, "output": 15.00}

# Provider → default model mapping
PROVIDER_DEFAULT_MODELS: dict[str, str] = {
    "anthropic": "claude-sonnet-4-20250514",
    "openai": "gpt-4o",
}

# Provider → available model options (default first, then premium)
PROVIDER_MODEL_OPTIONS: dict[str, list[dict[str, str | float]]] = {
    "anthropic": [
        {
            "id": "claude-sonnet-4-20250514",
            "name": "Claude Sonnet 4",
            "tier": "default",
            "description": "Fast, capable, and cost-effective. Best balance of quality and price.",
        },
        {
            "id": "claude-opus-4-20250514",
            "name": "Claude Opus 4",
            "tier": "premium",
            "description": "Anthropic's most capable model. Deeper reasoning and higher quality output.",
        },
    ],
    "openai": [
        {
            "id": "gpt-4o",
            "name": "GPT-4o",
            "tier": "default",
            "description": "Fast and capable multimodal model. Great balance of speed and quality.",
        },
        {
            "id": "gpt-4o-mini",
            "name": "GPT-4o Mini",
            "tier": "budget",
            "description": "Lightweight and very affordable. Good for simple questions.",
        },
    ],
}


def estimate_cost(
    agent_count: int,
    iterations: int,
    has_arbiter: bool,
) -> dict[str, int]:
    """Calculate expected LLM launches per phase.

    Formula (D007, corrected for iteration loop)::

        review:       agents
        cross_review: agents × (agents - 1) × iterations
        revision:     agents × iterations
        disputes:     agents
        synthesis:    1
        arbitration:  1 if arbiter else 0

    The iteration loop (per spec 005 universal rounds + spec 061 §3.1.9)
    runs Phase 2 cross-review AND Phase 3 revision once per iteration.
    Both must scale by ``iterations``. Prior to the spec 061 step 13
    cost-estimate gap fix (issue #109), ``cross_review`` was missing the
    ``× iterations`` factor and undercounted by a factor of ``iterations``.

    Args:
        agent_count: Number of agents in the deliberation.
        iterations: Number of revision iterations.
        has_arbiter: Whether an arbiter is configured.

    Returns:
        Dict mapping phase names to launch counts.
    """
    phases: dict[str, int] = {
        "review": agent_count,
        "cross_review": agent_count * (agent_count - 1) * iterations,
        "revision": agent_count * iterations,
        "disputes": agent_count,
        "synthesis": 1,
    }
    if has_arbiter:
        phases["arbitration"] = 1
    return phases


def estimate_cost_usd(
    agent_count: int,
    iterations: int = 1,
    has_arbiter: bool = False,
    provider: str = "anthropic",
    model: str | None = None,
    avg_input_tokens: int = 4000,
    avg_output_tokens: int = 2000,
) -> dict:
    """Estimate total API cost in USD for a deliberation.

    Uses the D007 launch formula combined with per-model token pricing
    to produce a cost range. The estimate is approximate — actual costs
    vary based on prompt length and response verbosity.

    Args:
        agent_count: Number of agents.
        iterations: Revision iterations (default 1).
        has_arbiter: Whether an arbiter is configured.
        provider: Provider name for model pricing lookup.
        model: Explicit model ID. When None, uses the provider default.
        avg_input_tokens: Estimated average input tokens per launch.
        avg_output_tokens: Estimated average output tokens per launch.

    Returns:
        Dict with phase breakdown, total launches, and estimated USD cost.
    """
    phases = estimate_cost(agent_count, iterations, has_arbiter)
    total_launches = sum(phases.values())

    effective_model = model or PROVIDER_DEFAULT_MODELS.get(provider, "claude-sonnet-4-20250514")
    pricing = MODEL_PRICING.get(effective_model, _DEFAULT_PRICING)

    cost_per_launch = (
        (avg_input_tokens / 1_000_000) * pricing["input"]
        + (avg_output_tokens / 1_000_000) * pricing["output"]
    )

    estimated_usd = total_launches * cost_per_launch

    # Provide a range (0.7x – 1.5x) since token counts vary significantly
    low_estimate = estimated_usd * 0.7
    high_estimate = estimated_usd * 1.5

    return {
        "phases": phases,
        "total_launches": total_launches,
        "model": effective_model,
        "estimated_usd": round(estimated_usd, 3),
        "low_estimate_usd": round(low_estimate, 3),
        "high_estimate_usd": round(high_estimate, 3),
        "pricing_per_1m_tokens": pricing,
    }
