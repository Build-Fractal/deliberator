# .wheels

Wheels for dependencies that are not on PyPI, found through `[tool.uv] find-links` in
`pyproject.toml`. Only this README is committed; the wheels are not published with this repo.

`scripts/lattice-wheel.sh` downloads lattice-graph from Lattice's releases (needs access to
Build-Fractal/lattice-releases). Without it, the `graph` extra won't install; the rest of
Deliberator works.
