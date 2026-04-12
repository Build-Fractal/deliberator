"""The ``Capability`` Pydantic model — canonical metadata for one capability.

Usage in ``capabilities.py`` at the repo root::

    from conversus.registry import Capability, Param, Surface
    from conversus.registry.adapters import DefaultMCPAdapter

    class DecideMCPAdapter(DefaultMCPAdapter):
        description = "Run an ad-hoc deliberation. Use this when..."

    decide = Capability(
        name="decide",
        summary="Run an ad-hoc deliberation",
        surfaces=[Surface.CLI, Surface.MCP, Surface.PLUGIN, Surface.MCPB],
        params=[
            Param(name="question", type=str, required=True),
            Param(name="provider", type=str, default="mock"),
        ],
        handler="engine.handlers:run_decide_cli",
        handlers={Surface.MCP: "engine.handlers:run_decide_mcp"},
        mcp_adapter=DecideMCPAdapter(),
    )

    CAPABILITIES: list[Capability] = [decide]

The explicit ``CAPABILITIES`` list is how the projector discovers
capabilities — there is no module-level registry populated by import-time
side effects. This is a deliberate choice to satisfy constitution
principle IX (no mutable module-level state) and XI (single source of
truth — ``CAPABILITIES`` is the one list, and the projector reads it
directly rather than introspecting module globals).

Adapter slots
-------------
The four ``*_adapter`` fields are optional per-capability overrides. When
a slot is ``None`` (the default), the projector applies the corresponding
``Default*Adapter``. Set a slot to an instance of the appropriate
``*Adapter`` subclass to override the projection for that surface.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from conversus.registry.params import Param, Surface

if TYPE_CHECKING:
    from conversus.registry.adapters.base import (
        CLIAdapter,
        MCPAdapter,
        MCPBAdapter,
        PluginAdapter,
    )


class Capability(BaseModel):
    """Canonical description of a capability.

    Holds the metadata the projector needs to emit a surface-specific
    artifact. It does not hold the runtime logic — ``handler`` is an
    import string of the form ``"module.path:func_name"`` that adapters
    resolve lazily when generating or invoking code.

    ``handlers`` is an optional per-surface override dict. Most
    capabilities use a single ``handler`` across all surfaces, but some
    (notably ``decide``) have intrinsic surface-specific behavior: the
    CLI wrapper prints + exits, the MCP wrapper returns structured data.
    When ``handlers[Surface.MCP]`` is set, the projector uses that handler
    for MCP projection; otherwise it falls back to ``handler``.
    """

    model_config = ConfigDict(
        # Adapter slots hold instances of ABCs defined in a sibling module.
        # ``arbitrary_types_allowed`` lets Pydantic accept isinstance checks
        # against those ABCs as validation.
        arbitrary_types_allowed=True,
        # Allow ``cap.mcp_adapter = X()`` after construction and re-validate.
        # Adapter attachment is the one post-construction mutation pattern
        # the API supports, so we accept a single write path with validation
        # rather than forbidding mutation entirely.
        validate_assignment=True,
    )

    name: str
    summary: str
    surfaces: list[Surface]
    params: list[Param]
    handler: str
    long_description: str = ""
    handlers: dict[Surface, str] = Field(default_factory=dict)

    cli_adapter: "CLIAdapter | None" = None
    mcp_adapter: "MCPAdapter | None" = None
    plugin_adapter: "PluginAdapter | None" = None
    mcpb_adapter: "MCPBAdapter | None" = None

    def handler_for(self, surface: Surface) -> str:
        """Return the handler import string for the given surface.

        Falls back to the default ``handler`` when no per-surface override
        is registered. This keeps single-handler capabilities simple while
        allowing surgical per-surface overrides for capabilities that need
        them (without forcing every capability to declare a dict).
        """
        return self.handlers.get(surface, self.handler)

    def params_for(self, surface: Surface) -> list[Param]:
        """Return only the params visible on the given surface.

        Preserves the declared order, filtering out params whose
        ``surfaces`` allowlist excludes the target. Adapters should
        iterate ``cap.params_for(Surface.X)`` instead of ``cap.params``
        when projecting, so CLI-only and MCP-only flags land only where
        they belong.
        """
        return [p for p in self.params if p.visible_on(surface)]
