"""Export OpenAPI 3.x JSON from the Conversus FastAPI application.

Instantiates the FastAPI app, mounts domain routers, and writes
the OpenAPI schema to ``docs/rest-api/openapi.json``.

Usage::

    uv run python scripts/export_openapi.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure the project root is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def main() -> None:
    """Generate OpenAPI JSON from the FastAPI app."""
    from web.app import app  # noqa: E402

    # Mount domain routers if available
    try:
        import tempfile

        from conversus.domains.api import create_domain_router
        from conversus.domains.implementations.code_review import CodeReviewDomain
        from conversus.domains.store import JSONLStore

        domain = CodeReviewDomain()
        store = JSONLStore(Path(tempfile.mkdtemp()) / "openapi_export.jsonl")
        router = create_domain_router(domain, store)
        app.include_router(router, prefix="/api/domains")
    except ImportError:
        print("Warning: could not mount domain routers (optional)", file=sys.stderr)

    schema = app.openapi()
    output_path = PROJECT_ROOT / "docs" / "rest-api" / "openapi.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(schema, indent=2) + "\n")
    print(f"OpenAPI schema written to {output_path}")


if __name__ == "__main__":
    main()
