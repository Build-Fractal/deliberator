"""Abstract base classes for per-surface capability adapters.

One base class per surface. Each adapter's single responsibility is to
project a ``Capability`` onto the format its target surface expects:

- ``CLIAdapter``    → Python source for a Click command function
- ``MCPAdapter``    → Python source for an ``@mcp.tool()`` function
- ``PluginAdapter`` → SKILL.md file text (YAML frontmatter + Markdown body)
- ``MCPBAdapter``   → a ``tools[]`` entry for ``desktop-extension/manifest.json``

Day 1-2 of spec 055 only requires the ABC skeletons — the ``Default*``
concrete implementations land on Day 3-4. Override adapters (e.g.
``DecideMCPAdapter``) subclass these bases directly and override only the
fields/methods that need per-capability tuning.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from deliberator.registry.adapters.mcpb import MCPBToolEntry
    from deliberator.registry.capability import Capability


class CLIAdapter(ABC):
    """Projects a capability into a Click command source fragment."""

    @abstractmethod
    def render(self, capability: "Capability") -> str:
        """Return Python source code for one Click command."""


class MCPAdapter(ABC):
    """Projects a capability into an ``@mcp.tool()`` function source fragment."""

    #: Override this in a subclass to provide a verbose MCP tool description
    #: (used by Claude Desktop / Cowork when picking which tool to invoke).
    description: str | None = None

    @abstractmethod
    def render(self, capability: "Capability") -> str:
        """Return Python source code for one ``@mcp.tool()`` function."""


class PluginAdapter(ABC):
    """Projects a capability into a ``skills/<name>/SKILL.md`` file body."""

    @abstractmethod
    def render(self, capability: "Capability") -> str:
        """Return the full SKILL.md file text, including YAML frontmatter."""


class MCPBAdapter(ABC):
    """Projects a capability into a manifest.json ``tools[]`` entry."""

    @abstractmethod
    def render(self, capability: "Capability") -> "MCPBToolEntry":
        """Return a single element of the manifest ``tools`` array.

        The concrete return type is ``MCPBToolEntry`` — a TypedDict
        defined in ``adapters/mcpb.py``. The projector serializes the
        whole manifest back to JSON and the TypedDict fields appear
        verbatim in the output.
        """
