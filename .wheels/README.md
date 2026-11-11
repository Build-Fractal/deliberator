# .wheels

Wheels for dependencies that are not on PyPI. Only this README is committed; the wheels are
not published with this repo.

`scripts/lattice-wheel.sh --install` downloads lattice-graph from Lattice's releases (needs
access to Build-Fractal/lattice-releases), checks SHA256SUMS and installs it into `.venv`.
Deliberator does not declare lattice-graph as a dependency; without it the rest works.
