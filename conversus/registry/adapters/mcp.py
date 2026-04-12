"""DefaultMCPAdapter — projects a Capability to ``@mcp.tool()`` source.

Generated tool shape::

    @mcp.tool()
    def conversus_hello(who: str, loud: bool = False) -> str:
        \"\"\"Say hello\"\"\"
        from conversus.demo import say_hello
        return say_hello(who=who, loud=loud)

**Override convention**: if a capability needs a verbose tool description
(which Claude Desktop and Cowork use for tool selection), subclass
``DefaultMCPAdapter`` — *not* the bare ``MCPAdapter`` ABC — and set
``description`` on the subclass. You inherit all the rendering and only
change the docstring::

    @DecideCapability.mcp_adapter
    class DecideMCPAdapter(DefaultMCPAdapter):
        description = \"\"\"
        Run an ad-hoc deliberation. Use this when the user describes a
        decision they're facing (e.g. "Postgres or MongoDB?")...
        \"\"\"

If you need to replace the full function body (rare), subclass
``MCPAdapter`` directly and implement ``render()`` from scratch.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from conversus.registry.adapters._helpers import literal, split_handler
from conversus.registry.adapters.base import MCPAdapter
from conversus.registry.params import Surface

if TYPE_CHECKING:
    from conversus.registry.capability import Capability
    from conversus.registry.params import Param


#: Prefix applied to every generated MCP tool name. ``decide`` → ``conversus_decide``.
#: Keeps the conversus namespace separate from other MCP servers Claude may have.
TOOL_PREFIX = "conversus_"


class DefaultMCPAdapter(MCPAdapter):
    """Projects a capability to an ``@mcp.tool()`` function source block."""

    def render(self, capability: "Capability") -> str:
        params = capability.params_for(Surface.MCP)
        tool_name = TOOL_PREFIX + capability.name.replace("-", "_")
        sig = self._signature(params, tool_name)
        docstring = self._docstring(capability)
        body = self._body(capability, params)
        return (
            "@mcp.tool()\n"
            f"{sig}\n"
            f"{docstring}\n"
            f"{body}"
        )

    # ------------------------------------------------------------------
    # Signature
    # ------------------------------------------------------------------

    def _signature(self, params: list["Param"], tool_name: str) -> str:
        """Emit ``def conversus_<name>(...) -> str:``.

        Multi-line when there are 2+ params so the generated source stays
        within a sensible line length — matches the style of the existing
        hand-written ``conversus_decide`` in ``mcp_server.py``.
        """
        if not params:
            return f"def {tool_name}() -> str:"

        if len(params) == 1:
            return f"def {tool_name}({_sig_param(params[0])}) -> str:"

        lines = [f"def {tool_name}("]
        for param in params:
            lines.append(f"    {_sig_param(param)},")
        lines.append(") -> str:")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Docstring
    # ------------------------------------------------------------------

    def _docstring(self, cap: "Capability") -> str:
        """Use ``self.description`` if an override subclass sets it, else
        the capability's ``long_description``, else its ``summary``.

        This three-level fallback is what makes ``DefaultMCPAdapter``
        convenient to subclass for the "only the docstring changes" case.
        """
        text = self.description or cap.long_description.strip() or cap.summary
        if "\n" not in text:
            return f'    """{text}"""'

        lines = ['    """']
        for line in text.strip().split("\n"):
            lines.append(f"    {line.strip()}")
        lines.append('    """')
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Body — lazy handler import + keyword-forwarded call
    # ------------------------------------------------------------------

    def _body(self, cap: "Capability", params: list["Param"]) -> str:
        module, func = split_handler(cap.handler_for(Surface.MCP))
        kwargs = ", ".join(f"{p.name}={p.name}" for p in params)
        return (
            f"    from {module} import {func}\n"
            f"    return {func}({kwargs})"
        )


# ---------------------------------------------------------------------------
# Helpers private to this module
# ---------------------------------------------------------------------------


def _sig_param(param: "Param") -> str:
    """Render one parameter for the ``def`` signature with type annotation."""
    type_name = param.type.__name__
    if param.required:
        return f"{param.name}: {type_name}"
    return f"{param.name}: {type_name} = {literal(param.default)}"
