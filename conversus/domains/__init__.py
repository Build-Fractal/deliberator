"""conversus.domains — Domain plugin framework.

COUPLING RULES (enforced, not aspirational):
- Domain implementations MUST import only from conversus.domains.base
- Domain implementations MUST NOT import from engine/, linter/, web/, mcp_server
- Domain implementations MUST NOT import from conversus.plugins (except via base hooks)
- Domain implementations MUST NOT import from conversus.schemas directly
- The domains/ package is independently installable with zero engine dependencies

These rules make extraction to separate packages (conversus-swe, etc.) mechanical.
"""

from conversus.domains.base import (
    DomainContext,
    DomainPlugin,
    DomainRecord,
    DomainScore,
    Scaffold,
    TrendResult,
    VariableExtractor,
    load_scaffold,
)
from conversus.domains.store import (
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
