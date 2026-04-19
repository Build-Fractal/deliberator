"""Call-time entry-point discovery for capabilities.

This module provides ONE umbrella function — :func:`collect_capabilities`
— that walks four functional entry-point groups
(``conversus.modes``, ``conversus.presets``, ``conversus.domains``,
``conversus.solvers``) on each invocation and returns a fresh,
composed ``list[Capability]``.

It is intentionally a pure function with no module-level state — each
call rereads the installed-package cache. Per Constitution Principle IX
(no module-level mutable state) this module MUST NOT decorate the
public function with :func:`functools.lru_cache`, :func:`functools.cache`,
or any equivalent that maintains a hidden module-level dict. Callers
may memoize at their own layer if they need to.

Composition is the caller's responsibility::

    from capabilities import CAPABILITIES  # built-ins, hand-curated
    from conversus.registry import collect_capabilities

    all_caps = CAPABILITIES + collect_capabilities()
    # ... pass all_caps to the projector or to get() / for_surface()

A single bad entry point does not break discovery for all others —
per-entry-point errors are attributed by name + distribution and
excluded with a logged warning, leaving other entries discoverable.

Binding spec: ``specs/064-capability-discovery/spec.md``.
"""

from __future__ import annotations

import importlib.metadata
import logging

from conversus.registry.capability import Capability

logger = logging.getLogger(__name__)

#: The four functional entry-point groups walked by :func:`collect_capabilities`.
#: Paid wheels register against whichever axis fits their content.
#: This is a module-level constant (immutable tuple), NOT a mutable
#: registry — Principle IX permits constants, forbids mutables.
CAPABILITY_GROUPS: tuple[str, ...] = (
    "conversus.modes",
    "conversus.presets",
    "conversus.domains",
    "conversus.solvers",
)


def collect_capabilities() -> list[Capability]:
    """Return capabilities registered via entry-points across all four
    functional groups, at call time.

    Each entry point under any of :data:`CAPABILITY_GROUPS` MUST resolve
    to either a zero-argument callable returning a single
    :class:`~conversus.registry.capability.Capability` instance, or to
    a :class:`~conversus.registry.capability.Capability` instance
    directly. Multiple capabilities per wheel are registered as separate
    entry-point lines.

    A single bad entry point (raising on load, returning the wrong type,
    or factory raising during invocation) is logged and excluded; other
    discoveries proceed. This is essential for the multi-wheel paid
    ecosystem — one broken wheel must not invalidate discovery for the
    others.

    Returns a fresh ``list[Capability]`` on every call. The list is
    composed in :data:`CAPABILITY_GROUPS` walk order; within each group
    entry-point order is implementation-defined (typically install
    order, but importlib.metadata makes no guarantee).
    """
    capabilities: list[Capability] = []
    for group in CAPABILITY_GROUPS:
        for ep in importlib.metadata.entry_points(group=group):
            cap = _load_single(ep)
            if cap is not None:
                capabilities.append(cap)
    return capabilities


def _load_single(ep: importlib.metadata.EntryPoint) -> Capability | None:
    """Load one entry point into a :class:`Capability`, or log+skip on failure.

    Returns the Capability on success. Returns ``None`` on any of:

    * the entry point fails to load (broken import, missing module),
    * the loaded value is neither a Capability nor a callable producing one,
    * the callable raises during instantiation.

    In every failure case the offending entry point name and
    distribution are included in the log line so the operator can
    trace which paid wheel is misbehaving without having to grep
    the whole entry-point graph.
    """
    dist_name = ep.dist.name if ep.dist else "<unknown-dist>"
    try:
        loaded = ep.load()
    except Exception as exc:
        logger.warning(
            "capability discovery: entry point %r (from %s) failed to load: %s",
            ep.name, dist_name, exc,
        )
        return None

    try:
        cap = loaded() if callable(loaded) else loaded
    except Exception as exc:
        logger.warning(
            "capability discovery: entry point %r (from %s) factory raised: %s",
            ep.name, dist_name, exc,
        )
        return None

    if not isinstance(cap, Capability):
        logger.warning(
            "capability discovery: entry point %r (from %s) did not produce a "
            "Capability — got %s; skipping.",
            ep.name, dist_name, type(cap).__name__,
        )
        return None

    return cap
