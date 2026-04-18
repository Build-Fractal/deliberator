"""Antipattern catalog and worked examples shipped as wheel package data.

Access catalog and example files via ``importlib.resources.files``::

    import importlib.resources
    catalog = (
        importlib.resources.files("conversus.antipatterns")
        / "catalog.md"
    ).read_text()

The Summary Index in ``catalog.md`` is consumed by spec 055's typed
``AntipatternRef`` validator (see
``specs/055-challenge-loop-deliberation/spec.md`` §11.3) — format
changes require coordinated updates to consumers.
"""
