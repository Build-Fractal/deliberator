"""Quality-floor reference fixtures shipped as wheel package data.

Access fixture files via ``importlib.resources.files``::

    import importlib.resources
    structural_defs = (
        importlib.resources.files("conversus.quality_floor")
        / "structural-definitions.md"
    ).read_text()

The fixture corpus pairs `configs/*.yml` (deliberation configs) with
`reference-outputs/{passing|failing}/<scenario>/` snapshots and
`questions/*.md` problem statements. Used to enforce baseline output
quality in conversus regression tests; not intended for application
consumption.
"""
