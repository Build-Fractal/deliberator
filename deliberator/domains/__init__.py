"""deliberator.domains — Domain plugin framework.

COUPLING RULES (enforced, not aspirational):
- Domain implementations MUST import only from deliberator.domains.base
- Domain implementations MUST NOT import from engine/, linter/, web/, mcp_server
- Domain implementations MUST NOT import from deliberator.plugins (except via base hooks)
- Domain implementations MUST NOT import from deliberator.schemas directly
- The domains/ package is independently installable with zero engine dependencies

These rules make extraction to separate packages (deliberator-swe, etc.) mechanical.
"""

from deliberator.domains.base import (
    DomainContext,
    DomainPlugin,
    DomainRecord,
    DomainScore,
    Scaffold,
    TrendResult,
    VariableExtractor,
    load_scaffold,
)
from deliberator.domains.store import (
    DomainStore,
    JSONLStore,
    SQLiteStore,
)

__all__ = [
    # Core models
    "DomainContext",
    "DomainPlugin",
    "DomainRecord",
    "DomainScore",
    "Scaffold",
    "TrendResult",
    "VariableExtractor",
    # Scaffold loading
    "load_scaffold",
    # Store protocol + implementations
    "DomainStore",
    "JSONLStore",
    "SQLiteStore",
]
