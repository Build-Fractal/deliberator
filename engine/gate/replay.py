"""Replay recorded tool calls through the current gate, offline.

    replay(items, config, judge) -> list[Decision]

Each item is ``{"tool", "tool_input", "cwd", "session"}`` (the full input, as the hook got it).
Every call is decided in its own temporary store: no live log is read or written and nothing
is pushed to a graph, so earlier rulings can be compared with what the gate decides now.
"""

from __future__ import annotations

import asyncio
import shutil
import tempfile
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

from engine.gate.config import GateConfig
from engine.gate.core import decide
from engine.gate.judge import Judge
from engine.gate.ledger import Decision


async def replay_async(items: Iterable[Mapping[str, Any]], config: GateConfig,
                       judge: Judge | None = None, *, shared: bool = False) -> list[Decision]:
    """Decide each item in an isolated temp store (one per item, or one for all if `shared`,
    so earlier items become precedent for later ones)."""
    cfg = config.model_copy(update={"graph_uri": None, "log_dir": None})
    out: list[Decision] = []
    common = Path(tempfile.mkdtemp(prefix="gate-replay-")) if shared else None
    try:
        for item in items:
            store = common or Path(tempfile.mkdtemp(prefix="gate-replay-"))
            try:
                out.append(await decide(
                    store, cfg, tool=str(item.get("tool", "")),
                    tool_input=dict(item.get("tool_input") or {}),
                    cwd=str(item.get("cwd") or ""), session=item.get("session"),
                    judge=judge, push_graph=False,
                ))
            finally:
                if common is None:
                    shutil.rmtree(store, ignore_errors=True)
    finally:
        if common is not None:
            shutil.rmtree(common, ignore_errors=True)
    return out


def replay(items: Iterable[Mapping[str, Any]], config: GateConfig,
           judge: Judge | None = None, *, shared: bool = False) -> list[Decision]:
    """Synchronous `replay_async` (for scripts and notebooks without a running loop)."""
    return asyncio.run(replay_async(items, config, judge, shared=shared))
