"""Runtime registration of entry-point-discovered capabilities (spec 064.1).

Spec 064 added :func:`~conversus.registry.discovery.collect_capabilities`
— a pure discovery primitive that walks entry points across four
functional groups. This module provides the per-surface RUNTIME hooks
that take those discovered capabilities and register them against a
live MCP server (FastMCP) or CLI group (click) at process startup.

Why a separate hook (instead of extending the existing adapters): the
``Default*Adapter`` classes are build-time CODEGEN — their
:meth:`~conversus.registry.adapters.base.MCPAdapter.render` returns
Python source written to disk by ``scripts/build-surfaces.py``.
Entry-point-discovered capabilities are unknown at codegen time
(they live in wheels installed AFTER the host was built), so they
need a runtime path. These functions are that path.

The two registration tracks coexist by design:

- **Static**: ``CAPABILITIES`` (in ``capabilities.py``) → codegen →
  ``@mcp.tool()`` / ``@cli.command()`` decorators in the generated
  surface modules. Build-time, deterministic, snapshot-friendly.

- **Dynamic**: :func:`collect_capabilities` → these helpers →
  ``mcp.add_tool(...)`` / ``cli.add_command(...)`` calls at startup.
  Runtime, picks up paid wheels installed alongside the host.

A single bad capability (handler resolution fails, ``add_tool`` raises,
name collides) is logged and skipped — never breaks registration of
the others. Per-capability isolation is essential for the multi-wheel
paid ecosystem.

Constitution alignment:

- Principle IX (no module-level mutable state): these functions own
  no state. They mutate the caller's ``mcp``/``cli`` instance, which
  is the documented runtime state holder for those frameworks.
- Principle XI (single source of truth): :class:`Capability` remains
  the one metadata definition; this module routes it to a different
  sink, not a different definition.
"""

from __future__ import annotations

import importlib
import json
import logging
from typing import TYPE_CHECKING, Any, Callable

from conversus.registry.discovery import collect_capabilities
from conversus.registry.params import Surface

if TYPE_CHECKING:
    import click
    from mcp.server.fastmcp import FastMCP

    from conversus.registry.capability import Capability

logger = logging.getLogger(__name__)


#: Prefix applied to MCP tool names. Must match ``TOOL_PREFIX`` in
#: :mod:`conversus.registry.adapters.mcp` so dynamically-registered
#: tools share the namespace with build-time-codegened ones.
_MCP_TOOL_PREFIX = "conversus_"


def _resolve_handler(handler_string: str) -> Callable[..., Any]:
    """Resolve a ``"module:function"`` string to the actual callable.

    Mirrors PEP 621 entry-point resolution semantics. Raises
    :class:`ValueError` if the string is malformed; raises
    :class:`ImportError` if the module isn't importable; raises
    :class:`AttributeError` if the named function isn't on the module.
    """
    if ":" not in handler_string:
        raise ValueError(
            f"handler string must use 'module:function' form, got {handler_string!r}"
        )
    module_path, _, attr = handler_string.partition(":")
    module = importlib.import_module(module_path)
    return getattr(module, attr)


def register_discovered_mcp_tools(mcp: "FastMCP") -> int:
    """Register entry-point-discovered capabilities against ``mcp``.

    Walks :func:`collect_capabilities`, filters to those opting into
    :data:`Surface.MCP`, resolves each handler, and calls
    ``mcp.add_tool(handler, name=..., description=...)`` for each.

    Returns the count of successfully registered tools.
    """
    registered = 0
    for cap in collect_capabilities():
        if Surface.MCP not in cap.surfaces:
            continue
        tool_name = f"{_MCP_TOOL_PREFIX}{cap.name}"
        try:
            handler = _resolve_handler(cap.handler_for(Surface.MCP))
        except Exception as exc:
            logger.warning(
                "spec 064.1: skipping MCP registration for %r — handler "
                "resolution failed: %s",
                cap.name, exc,
            )
            continue

        description = cap.summary
        if cap.mcp_adapter is not None and cap.mcp_adapter.description:
            description = cap.mcp_adapter.description

        try:
            mcp.add_tool(handler, name=tool_name, description=description)
        except Exception as exc:
            logger.warning(
                "spec 064.1: skipping MCP registration for %r — add_tool "
                "raised: %s",
                cap.name, exc,
            )
            continue

        registered += 1
    return registered


def register_discovered_cli_commands(cli: "click.Group") -> int:
    """Register entry-point-discovered capabilities against ``cli``.

    Walks :func:`collect_capabilities`, filters to those opting into
    :data:`Surface.CLI`, builds a click command for each, and calls
    ``cli.add_command(command, name=...)``. Hand-coded
    ``@cli.command()`` registrations on the host module are unaffected.

    Returns the count of successfully registered commands.
    """
    registered = 0
    for cap in collect_capabilities():
        if Surface.CLI not in cap.surfaces:
            continue
        try:
            handler = _resolve_handler(cap.handler_for(Surface.CLI))
        except Exception as exc:
            logger.warning(
                "spec 064.1: skipping CLI registration for %r — handler "
                "resolution failed: %s",
                cap.name, exc,
            )
            continue
        try:
            command = _build_click_command(cap, handler)
            cli.add_command(command, name=cap.name)
        except Exception as exc:
            logger.warning(
                "spec 064.1: skipping CLI registration for %r — "
                "add_command failed: %s",
                cap.name, exc,
            )
            continue
        registered += 1
    return registered


def _build_click_command(
    capability: "Capability",
    handler: Callable[..., Any],
) -> "click.Command":
    """Build a click command from a Capability + resolved handler.

    Maps each ``capability.params_for(Surface.CLI)`` entry to a
    ``click.Option`` keyed on ``--{name}``. The handler is invoked with
    the parsed options as keyword arguments. The result is rendered:
    ``dict``/``list`` → pretty-printed JSON; non-None scalar → ``str``.
    ``None`` returns are silent (no spurious blank line).
    """
    import click

    params: list[click.Parameter] = []
    for p in capability.params_for(Surface.CLI):
        params.append(
            click.Option(
                [f"--{p.name.replace('_', '-')}"],
                type=p.type,
                required=p.required,
                default=p.default,
                help=p.help,
            )
        )

    def _callback(**kwargs: Any) -> None:
        result = handler(**kwargs)
        if isinstance(result, (dict, list)):
            click.echo(json.dumps(result, indent=2))
        elif result is not None:
            click.echo(str(result))

    return click.Command(
        name=capability.name,
        params=params,
        callback=_callback,
        help=capability.summary,
    )
