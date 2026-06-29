"""Concrete execution provider implementations (spec 042 Phase 2+).

This subpackage holds the provider classes that implement
:class:`~engine.execution.ExecutionProvider`.  Phase 2 ships ``mock`` and
``anthropic``.  Phase 3 adds ``claude-code`` and ``opencode``.  The
optional ``litellm`` companion package lives outside deliberator core.

Providers are exposed via the :data:`PROVIDER_REGISTRY` dict for name-based
resolution at runtime.  The registry is populated at import time by each
provider module's module-level registration call.
"""

from __future__ import annotations

from engine.execution.provider import ExecutionProvider

#: Name → provider class registry.  Populated at import time by each
#: provider module.  Callers resolve providers via :func:`get_provider`
#: rather than importing the provider class directly.
PROVIDER_REGISTRY: dict[str, type[ExecutionProvider]] = {}


def register_provider(name: str, provider_cls: type[ExecutionProvider]) -> None:
    """Register a provider class under a name.

    Called at module import time by each provider module.  Raises
    :class:`ValueError` on duplicate registration to prevent silent
    override of a provider by a later import.
    """
    if name in PROVIDER_REGISTRY:
        existing = PROVIDER_REGISTRY[name]
        if existing is provider_cls:
            # Re-import of the same module — idempotent.
            return
        raise ValueError(
            f"Provider name '{name}' is already registered to "
            f"{existing.__module__}.{existing.__qualname__}; "
            f"refusing to override with "
            f"{provider_cls.__module__}.{provider_cls.__qualname__}",
        )
    PROVIDER_REGISTRY[name] = provider_cls


def get_provider(name: str, **options: object) -> ExecutionProvider:
    """Resolve a provider by name and instantiate it.

    Args:
        name: The registered provider name (e.g., ``"mock"``, ``"anthropic"``).
        **options: Provider-specific constructor options passed through
            unchanged.  The engine does not validate these — providers
            validate their own options.

    Returns:
        A new instance of the provider class.

    Raises:
        ValueError: If ``name`` is not registered, with a list of
            available names in the error message.
    """
    if name not in PROVIDER_REGISTRY:
        available = sorted(PROVIDER_REGISTRY.keys())
        raise ValueError(
            f"Unknown execution provider '{name}'. "
            f"Available: {available}. "
            f"Install the provider package or check spelling.",
        )
    provider_cls = PROVIDER_REGISTRY[name]
    return provider_cls(**options)  # type: ignore[call-arg]


# ---------------------------------------------------------------------------
# Eager imports to populate the registry at package import time
# ---------------------------------------------------------------------------
#
# Each provider module calls :func:`register_provider` at module scope, so
# importing the module is sufficient to make the provider available under
# :func:`get_provider`.  We import them here so users do not have to
# remember which modules to import.

from engine.execution.providers import mock  # noqa: E402, F401
from engine.execution.providers import anthropic as _anthropic  # noqa: E402, F401
from engine.execution.providers import claude_code as _claude_code  # noqa: E402, F401
from engine.execution.providers import aider as _aider  # noqa: E402, F401
from engine.execution.providers import opencode as _opencode  # noqa: E402, F401
from engine.execution.providers import openai_compat as _openai_compat  # noqa: E402, F401
from engine.execution.providers import codex as _codex  # noqa: E402, F401
from engine.execution.providers import copilot as _copilot  # noqa: E402, F401
from engine.execution.providers import gemini as _gemini  # noqa: E402, F401
from engine.execution.providers import pi as _pi  # noqa: E402, F401
from engine.execution.providers import desktop_sampling as _desktop_sampling  # noqa: E402, F401

__all__ = [
    "PROVIDER_REGISTRY",
    "get_provider",
    "register_provider",
]
