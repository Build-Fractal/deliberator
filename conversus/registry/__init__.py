"""Capability registry — single source of truth for the 4 distribution surfaces.

Binding spec: ``specs/055-capability-registry.md``.
Governing document: ``CONSTITUTION.md`` at repo root (principles IX, XI, XII).

Public API (what ``capabilities.py`` at the repo root imports)::

    from conversus.registry import (
        Capability,        # the pydantic model
        Param,             # parameter descriptor (pydantic)
        Surface,           # StrEnum of the 4 surfaces
        CLIAdapter,        # adapter ABCs (for custom overrides)
        MCPAdapter,
        PluginAdapter,
        MCPBAdapter,
        DefaultCLIAdapter, # default per-surface adapters
        DefaultMCPAdapter,
        DefaultPluginAdapter,
        DefaultMCPBAdapter,
        MCPBToolEntry,     # TypedDict for manifest.json entries
        get,               # lookup by name (pure function taking a list)
        for_surface,       # filter by surface opt-in
    )

There is intentionally no module-level ``REGISTRY`` and no ``@capability``
decorator. ``capabilities.py`` builds an explicit ``CAPABILITIES`` list
and the projector reads that list directly. This is the constitution's
principle IX (no mutable module-level state) applied literally.
"""

from conversus.registry.adapters import (
    CLIAdapter,
    DefaultCLIAdapter,
    DefaultMCPAdapter,
    DefaultMCPBAdapter,
    DefaultPluginAdapter,
    MCPAdapter,
    MCPBAdapter,
    MCPBToolEntry,
    PluginAdapter,
)
from conversus.registry.capability import Capability
from conversus.registry.discovery import CAPABILITY_GROUPS, collect_capabilities
from conversus.registry.params import Param, Surface
from conversus.registry.registry import for_surface, get
from conversus.registry.runtime import (
    register_discovered_cli_commands,
    register_discovered_mcp_tools,
)

# Pydantic v2 forward-reference resolution: ``Capability`` declares its
# adapter slots with string annotations (``"CLIAdapter | None"``) to avoid
# circular imports. Now that both ``Capability`` and the adapter ABCs have
# been imported, rebuild the model so Pydantic can resolve the annotations
# to real classes. Without this call, instantiating ``Capability(...)``
# raises ``PydanticUserError: not fully defined``.
Capability.model_rebuild(
    _types_namespace={
        "CLIAdapter": CLIAdapter,
        "MCPAdapter": MCPAdapter,
        "PluginAdapter": PluginAdapter,
        "MCPBAdapter": MCPBAdapter,
    }
)

__all__ = [
    # Core models
    "Capability",
    "Param",
    "Surface",
    # Adapter ABCs (for user-defined overrides)
    "CLIAdapter",
    "MCPAdapter",
    "PluginAdapter",
    "MCPBAdapter",
    # Default adapter implementations
    "DefaultCLIAdapter",
    "DefaultMCPAdapter",
    "DefaultPluginAdapter",
    "DefaultMCPBAdapter",
    # TypedDict for MCPB manifest tools[] entries
    "MCPBToolEntry",
    # Lookup helpers (pure functions over an explicit list)
    "get",
    "for_surface",
    # Entry-point discovery (spec 064)
    "CAPABILITY_GROUPS",
    "collect_capabilities",
    # Runtime registration of discovered capabilities (spec 064.1)
    "register_discovered_mcp_tools",
    "register_discovered_cli_commands",
]
