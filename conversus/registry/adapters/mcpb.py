"""DefaultMCPBAdapter — projects a Capability to a manifest.json tools[] entry.

Unlike the CLI / MCP / Plugin adapters which emit strings, MCPB entries
are structured data: the projector inserts the returned dict into the
``tools`` array of ``desktop-extension/manifest.json``. The return type
is a ``TypedDict`` (not ``dict[str, Any]``) to satisfy constitution
principle IX — the shape of an MCPB tool entry is known at design time
and does not warrant ``Any``.

Generated entry shape::

    {
      "name": "conversus_hello",
      "description": "Say hello to someone"
    }

The ``name`` field uses the ``conversus_`` prefix — identical to the MCP
adapter — because the ``.mcpb`` bundle ships the same underlying MCP
server, and tool names must match across the two surfaces or Claude
Desktop's install dialog will show stale entries.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from conversus.registry.adapters.base import MCPBAdapter
from conversus.registry.adapters.mcp import TOOL_PREFIX

if TYPE_CHECKING:
    from conversus.registry.capability import Capability


class MCPBToolEntry(TypedDict):
    """One element of the ``tools`` array in an MCPB ``manifest.json``.

    MCPB v0.3 manifests allow additional fields on tool entries, but
    conversus only ever emits ``name`` + ``description``. If a future
    MCPB schema version adds required fields, extend this TypedDict and
    update every emit-site in one change.
    """

    name: str
    description: str


class DefaultMCPBAdapter(MCPBAdapter):
    """Projects a capability to a manifest.json ``tools[]`` entry."""

    def render(self, capability: "Capability") -> MCPBToolEntry:
        tool_name = TOOL_PREFIX + capability.name.replace("-", "_")
        description = (
            capability.long_description.strip()
            or capability.summary
        )
        # Manifest descriptions should be a single line — Claude Desktop's
        # install dialog shows them truncated at ~200 chars, and multi-line
        # text renders as a wall of whitespace.
        one_liner = " ".join(description.split())
        return MCPBToolEntry(
            name=tool_name,
            description=one_liner,
        )
