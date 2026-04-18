"""Tests for :mod:`conversus.registry.discovery`.

Implements the 13 acceptance-criterion tests from spec 064 §6.
Mock-based — patches ``importlib.metadata.entry_points`` to return
synthetic ``EntryPoint``-like objects. A real-fixture integration
test is a planned follow-up; mock coverage is sufficient for
correctness and is deterministic in CI.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import logging
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from conversus.registry import (
    CAPABILITY_GROUPS,
    Capability,
    Param,
    Surface,
    collect_capabilities,
)
from conversus.registry import discovery as discovery_module
from conversus.registry import __all__ as registry_all


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_capability(name: str) -> Capability:
    """Construct a minimal Capability for tests."""
    return Capability(
        name=name,
        summary=f"Test capability {name!r}",
        surfaces=[Surface.CLI],
        params=[Param(name="x", type=str, required=True)],
        handler="tests.fixtures:noop",
    )


def make_ep(name: str, group: str, load_returns: Any, dist_name: str = "test-fixture") -> MagicMock:
    """Create a mock EntryPoint whose ``.load()`` returns ``load_returns``.

    ``load_returns`` may be a Capability, a zero-arg callable producing
    one, an unrelated value (to test the wrong-type path), or ``Exception``
    instances substituted via ``side_effect``.
    """
    ep = MagicMock()
    ep.name = name
    ep.group = group
    ep.dist = MagicMock()
    ep.dist.name = dist_name
    ep.load = MagicMock(return_value=load_returns)
    return ep


def patch_entry_points(group_to_eps: dict[str, list[MagicMock]]):
    """Patch ``importlib.metadata.entry_points`` to return the given map.

    Returns a context manager. Empty groups not present in the map
    return ``[]``.
    """
    def fake_entry_points(*args, **kwargs):
        group = kwargs.get("group")
        return group_to_eps.get(group, [])

    return patch("importlib.metadata.entry_points", side_effect=fake_entry_points)


# ---------------------------------------------------------------------------
# Acceptance criterion 2: empty case
# ---------------------------------------------------------------------------


def test_empty_no_packages_installed() -> None:
    """No installed packages declare any of the four groups → empty list."""
    with patch_entry_points({}):
        assert collect_capabilities() == []


# ---------------------------------------------------------------------------
# Acceptance criterion 3: single-package case (one per axis)
# ---------------------------------------------------------------------------


def test_single_capability_via_modes_group() -> None:
    """One entry point under conversus.modes → one Capability."""
    cap = make_capability("test_mode")
    ep = make_ep("test_mode", "conversus.modes", lambda: cap)
    with patch_entry_points({"conversus.modes": [ep]}):
        result = collect_capabilities()
    assert len(result) == 1
    assert result[0].name == "test_mode"


def test_single_capability_via_solvers_group() -> None:
    """Same coverage on a different axis — confirms walk visits all groups."""
    cap = make_capability("test_solver")
    ep = make_ep("test_solver", "conversus.solvers", lambda: cap)
    with patch_entry_points({"conversus.solvers": [ep]}):
        result = collect_capabilities()
    assert len(result) == 1
    assert result[0].name == "test_solver"


def test_capability_returned_directly_is_accepted() -> None:
    """Entry point may resolve to a Capability instance directly (not factory)."""
    cap = make_capability("direct")
    ep = make_ep("direct", "conversus.presets", cap)
    with patch_entry_points({"conversus.presets": [ep]}):
        result = collect_capabilities()
    assert len(result) == 1
    assert result[0].name == "direct"


# ---------------------------------------------------------------------------
# Acceptance criterion 4: multi-group composition
# ---------------------------------------------------------------------------


def test_multi_group_composition() -> None:
    """Two entry points across two different groups → two Capabilities composed."""
    cap_mode = make_capability("alpha_mode")
    cap_solver = make_capability("beta_solver")
    ep_mode = make_ep("alpha", "conversus.modes", lambda: cap_mode)
    ep_solver = make_ep("beta", "conversus.solvers", lambda: cap_solver)

    with patch_entry_points({
        "conversus.modes": [ep_mode],
        "conversus.solvers": [ep_solver],
    }):
        result = collect_capabilities()

    assert len(result) == 2
    names = {c.name for c in result}
    assert names == {"alpha_mode", "beta_solver"}


# ---------------------------------------------------------------------------
# Acceptance criterion 5: per-entry-point failure isolation
# ---------------------------------------------------------------------------


def test_failure_load_time_exception_skips_entry(caplog: pytest.LogCaptureFixture) -> None:
    """An entry point whose ``.load()`` raises is skipped, not propagated."""
    bad_ep = MagicMock()
    bad_ep.name = "broken_import"
    bad_ep.dist = MagicMock(name="MockDist")
    bad_ep.dist.name = "broken-wheel"
    bad_ep.load = MagicMock(side_effect=ImportError("no module named foo"))

    with caplog.at_level(logging.WARNING, logger="conversus.registry.discovery"):
        with patch_entry_points({"conversus.modes": [bad_ep]}):
            result = collect_capabilities()

    assert result == []
    # Warning attributes the failing entry-point + dist by name
    assert any(
        "broken_import" in r.message and "broken-wheel" in r.message
        for r in caplog.records
    ), f"warning missing entry-point/dist attribution: {[r.message for r in caplog.records]}"


def test_failure_wrong_return_type_skips_entry(caplog: pytest.LogCaptureFixture) -> None:
    """An entry point producing a non-Capability is skipped with a typed warning."""
    ep = make_ep("wrong_type", "conversus.modes", lambda: "not-a-capability")
    with caplog.at_level(logging.WARNING, logger="conversus.registry.discovery"):
        with patch_entry_points({"conversus.modes": [ep]}):
            result = collect_capabilities()
    assert result == []
    assert any("did not produce a Capability" in r.message for r in caplog.records)
    assert any("str" in r.message for r in caplog.records)


def test_failure_factory_raises_skips_entry(caplog: pytest.LogCaptureFixture) -> None:
    """An entry point whose factory raises during invocation is skipped."""
    def boom():
        raise RuntimeError("factory blew up")
    ep = make_ep("explosive", "conversus.solvers", boom)
    with caplog.at_level(logging.WARNING, logger="conversus.registry.discovery"):
        with patch_entry_points({"conversus.solvers": [ep]}):
            result = collect_capabilities()
    assert result == []
    assert any("factory raised" in r.message for r in caplog.records)


def test_failure_does_not_break_other_entries() -> None:
    """One bad entry point in a group does not stop the others from being returned."""
    good_cap = make_capability("survivor")
    good_ep = make_ep("survivor", "conversus.modes", lambda: good_cap)
    bad_ep = make_ep("bad", "conversus.modes", lambda: 42)  # int, not Capability

    with patch_entry_points({"conversus.modes": [bad_ep, good_ep]}):
        result = collect_capabilities()

    assert len(result) == 1
    assert result[0].name == "survivor"


# ---------------------------------------------------------------------------
# Acceptance criterion 6: no module-level mutable state
# ---------------------------------------------------------------------------


def test_no_module_level_capability_state() -> None:
    """The discovery module exposes no mutable container holding capabilities.

    Only legitimate module-level attributes:
    - the function, the helper, the imported logger
    - CAPABILITY_GROUPS (tuple — immutable, not a registry)
    - imports (module objects, the Capability class, logging, etc.)
    """
    members = inspect.getmembers(discovery_module)
    forbidden_types = (dict, list, set)
    for name, obj in members:
        if name.startswith("_"):
            continue  # dunders + private
        if isinstance(obj, forbidden_types):
            pytest.fail(
                f"discovery module exposes mutable {type(obj).__name__} "
                f"at module level: {name!r} = {obj!r}. "
                "Principle IX forbids module-level mutable state."
            )


# ---------------------------------------------------------------------------
# Acceptance criterion 7: pure function — fresh list per call
# ---------------------------------------------------------------------------


def test_returns_fresh_list_each_call() -> None:
    """Two consecutive calls return distinct list objects."""
    with patch_entry_points({}):
        result_a = collect_capabilities()
        result_b = collect_capabilities()
    assert result_a is not result_b
    assert result_a == result_b == []


# ---------------------------------------------------------------------------
# Acceptance criterion 8: no caching decorator
# ---------------------------------------------------------------------------


def test_no_caching_decorator_on_collect_capabilities() -> None:
    """Function must not be wrapped by lru_cache, cache, or similar.

    All caching decorators in functools set ``__wrapped__`` on the
    returned wrapper. A pure undecorated function does not have it.
    """
    assert not hasattr(collect_capabilities, "__wrapped__"), (
        "collect_capabilities is wrapped — likely @lru_cache or @cache. "
        "Principle IX (no module-level mutable state) forbids this; "
        "cache state lives in the decorator's hidden dict."
    )


def test_no_caching_decorator_in_source_ast() -> None:
    """AST scan: no decorator named lru_cache, cache, or cached_property
    on collect_capabilities (catches future regressions earlier than
    runtime introspection).
    """
    source_path = Path(discovery_module.__file__)
    tree = ast.parse(source_path.read_text())
    forbidden_decorator_names = {"lru_cache", "cache", "cached_property"}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "collect_capabilities":
            for dec in node.decorator_list:
                # @lru_cache or @lru_cache()
                dec_target = dec.func if isinstance(dec, ast.Call) else dec
                # @functools.lru_cache → Attribute
                if isinstance(dec_target, ast.Attribute):
                    if dec_target.attr in forbidden_decorator_names:
                        pytest.fail(f"collect_capabilities decorated with @{dec_target.attr}")
                # @lru_cache → Name
                elif isinstance(dec_target, ast.Name):
                    if dec_target.id in forbidden_decorator_names:
                        pytest.fail(f"collect_capabilities decorated with @{dec_target.id}")
            return

    pytest.fail("collect_capabilities not found in discovery.py AST scan")


# ---------------------------------------------------------------------------
# Acceptance criterion 9: __all__ snapshot
# ---------------------------------------------------------------------------


def test_all_snapshot() -> None:
    """``conversus.registry.__all__`` matches the snapshot file exactly.

    To intentionally change the public API: edit ``__all__`` and update
    ``snapshots/__all__.txt`` in the same PR. The snapshot is sorted
    so re-orderings of the source list don't appear as diffs.
    """
    snapshot_path = Path(__file__).parent / "snapshots" / "__all__.txt"
    expected = sorted(snapshot_path.read_text().strip().splitlines())
    actual = sorted(registry_all)
    assert actual == expected, (
        f"public API drift detected.\n"
        f"In code but not snapshot: {sorted(set(actual) - set(expected))}\n"
        f"In snapshot but not code: {sorted(set(expected) - set(actual))}\n"
        f"To accept: update {snapshot_path}"
    )


# ---------------------------------------------------------------------------
# Acceptance criterion 11: walk order
# ---------------------------------------------------------------------------


def test_capability_groups_walk_order() -> None:
    """``CAPABILITY_GROUPS`` is the declared tuple in the documented order."""
    assert CAPABILITY_GROUPS == (
        "conversus.modes",
        "conversus.presets",
        "conversus.domains",
        "conversus.solvers",
    )


def test_walk_order_reflected_in_results() -> None:
    """Capabilities from earlier groups appear before later groups in the result."""
    cap_mode = make_capability("z_mode")     # 'z' to make ordering test independent of name sort
    cap_solver = make_capability("a_solver")
    ep_mode = make_ep("z_mode", "conversus.modes", lambda: cap_mode)
    ep_solver = make_ep("a_solver", "conversus.solvers", lambda: cap_solver)

    with patch_entry_points({
        "conversus.modes": [ep_mode],
        "conversus.solvers": [ep_solver],
    }):
        result = collect_capabilities()

    # modes group is walked before solvers group → mode comes first
    assert [c.name for c in result] == ["z_mode", "a_solver"]


# ---------------------------------------------------------------------------
# Constants & importability sanity checks (acceptance criterion 1)
# ---------------------------------------------------------------------------


def test_capability_groups_is_tuple() -> None:
    """CAPABILITY_GROUPS must be a tuple (immutable), not a list (mutable)."""
    assert isinstance(CAPABILITY_GROUPS, tuple)
    assert len(CAPABILITY_GROUPS) == 4


def test_collect_capabilities_is_callable() -> None:
    """Public symbol resolves and is callable."""
    assert callable(collect_capabilities)
