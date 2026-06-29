"""Lookup helpers over an explicit capability list.

This module is a thin collection of pure functions. It deliberately does
*not* own any mutable module-level state — constitution principle IX
forbids module-level singletons. The caller owns the list (typically
``CAPABILITIES`` in ``capabilities.py`` at the repo root) and passes it
in explicitly.

If you're looking for where capabilities are registered: they aren't.
``capabilities.py`` builds its own list of ``Capability`` instances, and
every consumer (the projector, the build script, tests) either imports
that list directly or constructs its own.
"""

from __future__ import annotations

from typing import Iterable, Iterator

from deliberator.registry.capability import Capability
from deliberator.registry.params import Surface


def get(name: str, capabilities: Iterable[Capability]) -> Capability:
    """Return the capability named ``name`` from ``capabilities``.

    Raises ``KeyError`` if no capability with that name exists in the
    given iterable. This is a boundary check (capability lookup failure
    is programmer error, not a data error), so ``KeyError`` is
    appropriate rather than a result object.
    """
    for cap in capabilities:
        if cap.name == name:
            return cap
    raise KeyError(f"no capability named {name!r}")


def for_surface(
    surface: Surface,
    capabilities: Iterable[Capability],
) -> Iterator[Capability]:
    """Yield capabilities from ``capabilities`` that opt in to ``surface``.

    The projector's own filtering logic uses this shape — it's a pure,
    stateless transformation on an iterable, which composes cleanly with
    list comprehensions and generator pipelines elsewhere.
    """
    for cap in capabilities:
        if surface in cap.surfaces:
            yield cap
