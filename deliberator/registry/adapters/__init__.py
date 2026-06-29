"""Per-surface adapter base classes and default implementations.

The ``*Adapter`` classes are the ABCs override authors subclass. The
``Default*Adapter`` classes are the concrete projections the build
script uses when a capability doesn't specify an override.
"""

from deliberator.registry.adapters.base import (
    CLIAdapter,
    MCPAdapter,
    MCPBAdapter,
    PluginAdapter,
)
from deliberator.registry.adapters.cli import DefaultCLIAdapter
from deliberator.registry.adapters.mcp import DefaultMCPAdapter
from deliberator.registry.adapters.mcpb import DefaultMCPBAdapter, MCPBToolEntry
from deliberator.registry.adapters.plugin import DefaultPluginAdapter

__all__ = [
    "CLIAdapter",
    "MCPAdapter",
    "MCPBAdapter",
    "PluginAdapter",
    "DefaultCLIAdapter",
    "DefaultMCPAdapter",
    "DefaultMCPBAdapter",
    "DefaultPluginAdapter",
    "MCPBToolEntry",
]
