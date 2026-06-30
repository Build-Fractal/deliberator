"""Parameter and surface primitives for the capability registry.

These are the leaf types — no dependencies on other registry modules —
so both ``capability.py`` and the adapter classes can import from here
without risking circular imports.

Constitution alignment
----------------------
- Principle IX (Explicit Typing — non-negotiable): ``Surface`` is a
  ``StrEnum`` because it is a closed behavioral choice whose values
  each trigger distinct projector code paths. ``Param`` is a
  ``pydantic.BaseModel`` for validated, typed data structures — no
  ``Any`` on field annotations.
- Principle XI (Single Source of Truth): the ``Param`` model is the
  one definition of parameter metadata used by every adapter.
"""

from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    pass


class Surface(StrEnum):
    """The four distribution surfaces deliberator projects capabilities to.

    Using ``StrEnum`` (Python 3.11+) makes the enum values YAML-compatible
    and allows exhaustive pattern matching in the projector without
    string-literal comparisons.
    """

    CLI = "cli"
    MCP = "mcp"
    PLUGIN = "plugin"
    MCPB = "mcpb"


#: Acceptable runtime value types for ``Param.default`` and entries of
#: ``Param.choices``. This is the closed set of primitives the projector
#: can emit as Python source literals via ``literal()`` in
#: ``adapters/_helpers.py`` — extending it means extending the emitter.
ParamValue = str | int | bool | None


class Param(BaseModel):
    """A single parameter exposed by a capability.

    One ``Param`` instance describes the parameter once; each surface's
    adapter decides how to expose it (e.g. Click option, MCP tool arg,
    SKILL.md frontmatter, manifest.json input).

    ``surfaces`` is optional per-surface visibility: if ``None`` (the
    default), the param appears on every surface the capability opts
    into. If set to a list of ``Surface`` values, the param only appears
    on those surfaces — used when a capability has a CLI-only flag
    (e.g. ``--format rich|json``) that doesn't make sense for MCP, or
    an MCP-only safety cap (``max_launches``) that CLI users control via
    other means.
    """

    model_config = ConfigDict(
        # ``type`` is a Python builtin; Pydantic needs this flag to accept
        # it as a field type rather than trying to serialize it as JSON.
        arbitrary_types_allowed=True,
        frozen=True,
    )

    name: str
    type: type
    required: bool = False
    default: ParamValue = None
    choices: list[ParamValue] | None = None
    help: str = ""
    surfaces: list[Surface] | None = None

    def visible_on(self, surface: Surface) -> bool:
        """Return True if this param should be exposed on the given surface."""
        if self.surfaces is None:
            return True
        return surface in self.surfaces
