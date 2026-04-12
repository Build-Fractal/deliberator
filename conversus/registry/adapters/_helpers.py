"""Shared source-emission helpers used by the default adapters.

These are private to the ``adapters`` package (leading underscore) and
exist to centralize the handful of primitives that every default adapter
needs — literal rendering, handler parsing — so no adapter has to import
from another adapter module.
"""

from __future__ import annotations

import json
from typing import Any


def literal(value: Any) -> str:
    """Render a Python source literal for emission into generated code.

    Tricky bit: ``json.dumps(False)`` returns ``"false"`` and
    ``json.dumps(None)`` returns ``"null"`` — both valid JSON but NOT
    valid Python literals (Python requires ``False`` / ``None`` with
    capitals). For emission into source code we want Python forms.

    For strings we *do* want ``json.dumps``'s double-quoted output,
    because ``repr("x")`` in Python 3 yields single quotes which would
    clash diff-noisily with the existing hand-written surface files that
    consistently use double quotes.

    NOTE: ``bool`` is a subclass of ``int`` in Python, so the bool check
    has to come BEFORE the numeric check or ``True``/``False`` would hit
    the ``repr`` branch and emit ``"True"`` (fine for bool but the check
    order matters if we later add other ``int`` subclasses).
    """
    if value is None:
        return "None"
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, str):
        return json.dumps(value)
    return repr(value)


def split_handler(handler: str) -> tuple[str, str]:
    """Split a ``"module.path:func_name"`` handler string into parts.

    Capability handler strings are user-facing configuration — they live
    in the capabilities module and may be mistyped. This boundary check
    produces an actionable error rather than letting a malformed string
    leak into generated source code where it would surface as a confusing
    NameError at import time.
    """
    if handler.count(":") != 1:
        raise ValueError(
            f"handler must be of the form 'module.path:func_name', got {handler!r}"
        )
    module, func = handler.split(":")
    return module, func
