# Feature Specification: Capability Discovery via Entry Points

**Feature ID**: `064-capability-discovery`
**Created**: 2026-04-18
**Status**: Draft v2 — post-deliberation revisions applied; ready for implementation
**Depends On**: `055-capability-registry.md`
**Governed by**: `CONSTITUTION.md` principle IX (no module-level mutable state), XI (single source of truth)
**Originating context**: `payer-index-mono/deliberations/conversus-divergence/entrypoint-verification.md` (W0.2 of the divergence consolidation SPEC.md found the entry-point discovery the SPEC presumed does not exist)
**Deliberation outputs**: `conversus-oss/specs/064-capability-discovery/output/` (3-agent cooperative run, 2026-04-18; synthesis preamble + 15 upstream artifacts)

> **Revision log (v1 → v2)**: Five unanimous deliberation findings applied:
> 1. Version bump target raised from PATCH (`0.1.1`) to MINOR (`0.2.0`) — adds a new public symbol, semver demands it.
> 2. Added `_load_single` helper for per-entry-point error attribution (one bad wheel must not break discovery for all).
> 3. Explicit prohibition on `@lru_cache` (and equivalents) — the decorator silently reintroduces module-level state via its internal dict, recreating exactly what spec 055's Day 1-4 rework eliminated.
> 4. Reconciled with parent `SPEC.md` §W3.1's 4 functional entry-point groups (`conversus.modes`, `.presets`, `.domains`, `.solvers`) per user directive: capabilities can REFER to these functional axes; `conversus.capabilities` is the umbrella discovery target that walks all four. The fifth group from §W3.1 (`conversus.mcp_tools`) is dropped — MCP is a projection of capabilities (per spec 055's adapter pattern), not a parallel registration channel.
> 5. Added `__all__` snapshot test acceptance criterion to lock the public API surface mechanically.

> **Scope discipline**: This spec adds ONE umbrella discovery function — `collect_capabilities()` — that walks four functional entry-point groups (modes, presets, domains, solvers) at invocation time and returns a fresh, composed `list[Capability]`. It does NOT add a `discover()` method on the registry, does NOT add module-level state, does NOT cache results across calls, does NOT change the existing `Capability`, `Surface`, `get`, or `for_surface` API. It is the smallest change that satisfies the SPEC.md W0.2 / W3.1 acceptance criteria without violating spec 055 or principle IX.

---

## 1. Summary

Conversus paid wheels (planned per `payer-index-mono/deliberations/conversus-divergence/SPEC.md` Wave 3) need to register capabilities with the OSS engine without import-time coupling — i.e., installing `conversus-strategies` should make its capabilities visible to OSS without OSS having to import `conversus_strategies`.

The standard Python solution is `importlib.metadata.entry_points()` discovery against published group names. Spec 055 chose to keep capabilities as an explicit list (no module-level state), so a discovery layer was deliberately omitted. This spec adds discovery as a **call-time pure function**, preserving spec 055's no-module-state invariant.

Per the parent `SPEC.md` §W3.1 (and confirmed by user directive after the v1 deliberation), capabilities are functionally categorized into four registration axes — modes, presets, domains, solvers — each as its own entry-point group. `collect_capabilities()` is the umbrella that walks all four and returns the composed list. Paid wheels register against whichever functional axis fits their content.

## 2. Goals

- G1. **Paid wheels can register capabilities** by declaring the appropriate `[project.entry-points."conversus.<axis>"]` group in their `pyproject.toml`, with no patches to OSS code. Axes: `conversus.modes`, `conversus.presets`, `conversus.domains`, `conversus.solvers`.
- G2. **OSS can collect capabilities across all axes** via `from conversus.registry import collect_capabilities; collect_capabilities()` — returns a fresh `list[Capability]` each call, no caching at module level.
- G3. **The existing registry API is unchanged.** `Capability`, `Surface`, `Param`, adapters, `get`, `for_surface` all keep their current signatures and semantics.
- G4. **Principle IX is preserved.** No module-level `REGISTRY` dict, no `@capability` decorator, no `@lru_cache` on `collect_capabilities()`, no import-time side effects. The function reads the entry-point cache at call time only.
- G5. **Spec 055's existing `CAPABILITIES` list at the repo root remains canonical for built-in capabilities.** Discovered capabilities are *additional*, not a replacement. Composition is the caller's responsibility.
- G6. **A single bad entry point does not break discovery for all others.** Errors are attributed to the offending entry-point + dist by name, and the failing entry is excluded with a logged warning while remaining discoveries proceed (per `_load_single` helper).

## 3. Non-Goals

- N1. NO replacement of `capabilities.py`'s explicit list. Built-in capabilities are still hand-listed.
- N2. NO `conversus.mcp_tools` entry-point group (despite parent SPEC.md §W3.1 listing it). MCP surface is a *projection* of capabilities via `MCPAdapter` (per spec 055), not a parallel registration channel. A capability that opts into the MCP surface registers under whichever functional axis fits (modes / presets / domains / solvers) and exposes itself to MCP via its adapter, not via a separate entry-point group.
- N3. NO automatic merging of discovered capabilities into the projector pipeline. Callers compose their own list (typically `CAPABILITIES + collect_capabilities()`).
- N4. NO caching of the discovered list — neither manual (module-level dict) nor decorator-based (`@lru_cache`, `@cache`, `@cached_property`). The function is pure — every call hits `importlib.metadata.entry_points()` afresh. Callers may memoize at their layer if they need to.
- N5. NO changes to spec 055. This is additive.

## 4. Proposal

### 4.1 New module: `conversus/registry/discovery.py`

```python
"""Call-time entry-point discovery for capabilities.

This module provides ONE umbrella function — ``collect_capabilities()`` —
that walks four functional entry-point groups
(``conversus.modes``, ``conversus.presets``, ``conversus.domains``,
``conversus.solvers``) on each invocation and returns a fresh,
composed ``list[Capability]``.

It is intentionally a pure function with no module-level state — each
call rereads the installed-package cache. Per Constitution Principle IX
(no module-level mutable state) this module MUST NOT decorate the
public function with ``functools.lru_cache``, ``functools.cache``, or
any equivalent that maintains a hidden module-level dict. Callers may
memoize at their own layer if they need to.

Composition is the caller's responsibility::

    from capabilities import CAPABILITIES  # built-ins, hand-curated
    from conversus.registry import collect_capabilities

    all_caps = CAPABILITIES + collect_capabilities()
    # ... pass all_caps to the projector or to get() / for_surface()

A single bad entry point does not break discovery for all others —
per-entry-point errors are attributed by name + distribution and
excluded with a logged warning, leaving other entries discoverable.
"""

from __future__ import annotations

import importlib.metadata
import logging

from conversus.registry.capability import Capability

logger = logging.getLogger(__name__)

#: The four functional entry-point groups walked by ``collect_capabilities``.
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

    Each entry point under any of ``CAPABILITY_GROUPS`` MUST resolve to
    a zero-argument callable returning a single ``Capability`` instance,
    or to a ``Capability`` instance directly. Multiple capabilities per
    wheel are registered as separate entry-point lines.

    A single bad entry point (raising on load, returning the wrong type)
    is logged and excluded; other discoveries proceed. This is essential
    for the multi-wheel paid ecosystem — one broken wheel must not
    invalidate discovery for the others.
    """
    capabilities: list[Capability] = []
    for group in CAPABILITY_GROUPS:
        for ep in importlib.metadata.entry_points(group=group):
            cap = _load_single(ep)
            if cap is not None:
                capabilities.append(cap)
    return capabilities


def _load_single(ep: importlib.metadata.EntryPoint) -> Capability | None:
    """Load one entry point into a Capability, or log+skip on failure.

    Returns the Capability on success. Returns None on any of:
      - the entry point fails to load (broken import, missing module),
      - the loaded value is neither a Capability nor a callable
        producing one,
      - the callable raises during instantiation.

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

    cap = loaded() if callable(loaded) else loaded
    if not isinstance(cap, Capability):
        logger.warning(
            "capability discovery: entry point %r (from %s) did not produce a "
            "Capability — got %s; skipping.",
            ep.name, dist_name, type(cap).__name__,
        )
        return None

    return cap
```

### 4.2 Four entry-point groups + the umbrella function

Paid wheels declare entry points under whichever functional axis fits their content:

```toml
# packages/conversus-strategies/pyproject.toml
[project.entry-points."conversus.solvers"]
nashopt = "conversus_strategies.nashopt:nashopt_capability"

[project.entry-points."conversus.modes"]
strategic_review = "conversus_strategies.review:strategic_review_capability"
```

```toml
# packages/conversus-swe/pyproject.toml
[project.entry-points."conversus.domains"]
software_eng = "conversus_swe.domain:swe_domain_capability"

[project.entry-points."conversus.presets"]
swe_critic = "conversus_swe.presets:swe_critic_preset"
```

`collect_capabilities()` walks all four groups in declaration order (modes → presets → domains → solvers) and returns the concatenated list. Within each group, entry-point order is implementation-defined.

**Why no `conversus.mcp_tools` group** (per N2): MCP exposure is a per-capability *opt-in* via `Capability.surfaces` containing `Surface.MCP`, projected through `MCPAdapter`. A capability becomes MCP-visible by declaring its surface, not by registering against a separate entry-point group. This keeps MCP's projection logic on the existing per-surface adapter axis spec 055 chose, rather than splitting registration semantics across two surfaces.

**Why an umbrella function rather than four** (e.g., `collect_modes()`, `collect_presets()`, ...): the projector and other consumers operate on `list[Capability]` regardless of axis — a capability's axis is a registration concern, not a runtime distinction. If a future spec needs axis-filtered discovery (e.g., "only the solver capabilities"), it can add a thin filter on top of the umbrella result, or extend `collect_capabilities` with an optional `groups: tuple[str, ...] = CAPABILITY_GROUPS` parameter.

### 4.3 Public API additions

Add to `conversus/registry/__init__.py`:

```python
from conversus.registry.discovery import (
    CAPABILITY_GROUPS,
    collect_capabilities,
)

__all__ = [
    # ... existing entries (Capability, Surface, Param, adapters, get, for_surface) ...
    "CAPABILITY_GROUPS",
    "collect_capabilities",
]
```

The two new public symbols (`CAPABILITY_GROUPS`, `collect_capabilities`) are the only API additions introduced by this spec. The `__all__` change is locked in by the snapshot test added in §5 / §6.

## 5. Acceptance Criteria

The spec is successfully implemented when ALL of the following hold:

1. **Function exists and is importable**: `from conversus.registry import collect_capabilities, CAPABILITY_GROUPS` resolves.
2. **Empty case**: with no installed packages declaring any of the four group's entry points, `collect_capabilities()` returns `[]`.
3. **Single-package case**: a test fixture wheel declaring one entry point under any of the four groups produces exactly one `Capability` in the returned list when installed.
4. **Multi-package, multi-group case**: two test fixture wheels each declaring one entry point against a *different* group produce two `Capability` instances composed in the umbrella list.
5. **Per-entry-point failure isolation**: a wheel declaring a non-`Capability` factory produces a logged warning naming the offending entry point and dist, AND is skipped (does not raise from `collect_capabilities()`); other valid entry points in the same group still appear in the result. Validated via three sub-cases: load-time exception, returned-wrong-type, and factory-raises.
6. **No module-level mutable state**: `inspect.getmembers(conversus.registry.discovery)` shows no module-level `dict`, `list`, or other mutable that holds capabilities. The only module-level attribute is `CAPABILITY_GROUPS` (tuple, immutable).
7. **Pure function**: calling `collect_capabilities()` twice in succession returns two distinct list objects (`is not` check). The list contents are equal but the objects themselves are fresh.
8. **No `@lru_cache`-class decorators**: a static AST scan of `discovery.py` confirms `collect_capabilities` is not decorated with `functools.lru_cache`, `functools.cache`, `functools.cached_property`, or any other caching decorator. (Encoded as a test that imports the source and asserts `collect_capabilities.__wrapped__ is collect_capabilities` — pure functions have no `__wrapped__`.)
9. **`__all__` snapshot lock**: a test compares `conversus.registry.__all__` to a frozen snapshot file (`conversus/registry/tests/snapshots/__all__.txt`). Any change requires updating the snapshot, making API drift a deliberate, reviewable diff.
10. **Constitution audit pass**: a manual reading confirms principle IX is preserved (no `REGISTRY = {}`, no `@capability` decorator, no caching).
11. **Group walk is in declared order**: `collect_capabilities()` walks `CAPABILITY_GROUPS` in tuple order; reordering the tuple is a deliberate API change requiring a snapshot update.

## 6. Test Plan

Add `conversus-oss/conversus/registry/tests/test_discovery.py` with:
- `test_empty_no_packages_installed` (case 2)
- `test_single_capability_via_modes_group` (case 3, modes axis)
- `test_single_capability_via_solvers_group` (case 3, solvers axis)
- `test_multi_group_composition` (case 4)
- `test_failure_load_time_exception_skips_entry` (case 5a)
- `test_failure_wrong_return_type_skips_entry` (case 5b)
- `test_failure_factory_raises_skips_entry` (case 5c)
- `test_failure_does_not_break_other_entries` (case 5 isolation)
- `test_returns_fresh_list_each_call` (case 7)
- `test_no_module_level_capability_state` (case 6 — `inspect`-based)
- `test_no_caching_decorator_on_collect_capabilities` (case 8 — `__wrapped__` and AST scan)
- `test_capability_groups_walk_order` (case 11)
- `test_all_snapshot` (case 9 — diff against snapshot file)

Test fixtures live under `conversus-oss/conversus/registry/tests/fixtures/` and use `uv pip install --target` into a tmpdir during test setup. The `__all__` snapshot lives at `conversus-oss/conversus/registry/tests/snapshots/__all__.txt` (plain text, sorted, one symbol per line).

## 7. Migration & Compatibility

- **No breaking changes to existing API.** The current registry public surface is preserved verbatim. Adding `collect_capabilities` and `CAPABILITY_GROUPS` is a pure addition.
- **Version bump**: `conversus==0.2.0` (**MINOR** bump, NOT PATCH). Reason: the spec adds two new public symbols (`collect_capabilities`, `CAPABILITY_GROUPS`) to `conversus.registry.__all__`. Per semver, adding a public symbol is a MINOR bump. PATCH (`0.1.2`) would mis-signal the change and let consumers' tools auto-upgrade past it without notice.
- **Documentation**: Update `conversus-oss/CLAUDE.md` and `conversus-oss/conversus/registry/__init__.py` docstring to document the new function. Update `payer-index-mono/deliberations/conversus-divergence/SPEC.md` §W0.2 and §W3.1 to point at this spec. The §W3.1 list of 5 entry-point groups updates to 4 (drop `conversus.mcp_tools`) with a cross-reference to N2 here.

## 8. Dependencies and Sequencing

- **Blocks**: Wave 3 of the divergence consolidation (per `SPEC.md` §W0.2). Wave 1 (fixtures) and Wave 2 (engine) do NOT block on this spec.
- **Blocked by**: nothing internal to conversus-oss. The implementation is ~80 lines (function + helper + groups constant + module docstring) plus ~150 lines of tests + fixtures.
- **Estimated effort**: 1-2 days (single contributor) including the 13 tests.

## 9. Open Questions

- **Q1 (closed)**: Should `collect_capabilities` take an optional `group` parameter? **Resolved**: walks all 4 groups by default per `CAPABILITY_GROUPS`. A future spec can add `groups: tuple[str, ...] = CAPABILITY_GROUPS` if axis-filtered discovery becomes a real consumer need; not speculated for now.
- **Q2**: Should the function deduplicate capabilities by `name` across groups? Two wheels could register entry points with the same local name in different groups. **Recommendation**: do not dedup; raise on first conflict at composition time (caller's `get()` or projector pass). Surfaces the conflict mechanically. If two wheels collide in the same group, both are returned and the conflict surfaces at the same point.
- **Q3**: Should the OSS `capabilities.py` automatically include `collect_capabilities()` results, or should every consumer compose explicitly? **Recommendation**: explicit composition; spec 055's "explicit list" stance applies. Auto-merge would silently widen the OSS surface.

## 10. Source Documents

- `payer-index-mono/deliberations/conversus-divergence/entrypoint-verification.md` — the W0.2 finding that motivated this spec
- `payer-index-mono/deliberations/conversus-divergence/SPEC.md` §W0.2, §W3.1 — the original assumption that needs reconciliation (this spec's v2 closes the reconciliation per user's "capabilities can refer modes/presets/domains/solvers; mcp built from functionality" directive, 2026-04-18)
- `conversus-oss/specs/055-capability-registry.md` — the binding spec for the existing registry shape
- `conversus-oss/CONSTITUTION.md` — principle IX (no module-level mutable state), principle XI (single source of truth)
- `conversus-oss/conversus/registry/__init__.py` — current public API surface
- `conversus-oss/specs/064-capability-discovery/output/` — v1 deliberation outputs (3 reviews + 6 cross-reviews + 3 revisions + 3 disputes; synthesis preamble) that surfaced the 5 revisions applied here. Notable synthesis statement: "no agent rejected the spec; function shape, composition model, and Principle IX framing are sound."
