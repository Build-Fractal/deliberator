"""Domain record storage: protocol and implementations.

Provides the DomainStore protocol and two concrete implementations:

  - **JSONLStore**: Append-only JSONL files, one file per domain.
    Thread-safe via ``fcntl`` file locking.  Query via line-by-line scan.
    Suitable for < 10K records per domain.

  - **SQLiteStore**: Local SQLite database with one table per domain.
    Query via SQL.  Trend via window functions.

Both implementations support the full DomainStore protocol: append, get,
query, trend, and aggregate.

This module imports nothing from ``engine/``, ``linter/``, ``web/``,
or ``mcp_server``.
"""

from __future__ import annotations

import fcntl
import json
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from conversus.domains.base import (
    DomainRecord,
    DomainScore,
    TrendResult,
    _linear_slope,
)

logger = logging.getLogger("conversus.domains.store")


# ---------------------------------------------------------------------------
# DomainStore protocol
# ---------------------------------------------------------------------------


@runtime_checkable
class DomainStore(Protocol):
    """Protocol for domain record storage backends.

    All methods accept domain names and record objects, so a single store
    instance can serve multiple domains.
    """

    def append(self, record: DomainRecord) -> str:
        """Persist a record and return its ID.

        Args:
            record: The domain record to persist.

        Returns:
            The record's UUID string.
        """
        ...

    def get(self, record_id: str) -> DomainRecord | None:
        """Retrieve a record by ID.

        Args:
            record_id: The UUID of the record.

        Returns:
            The record, or None if not found.
        """
        ...

    def query(
        self,
        domain: str,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
    ) -> list[DomainRecord]:
        """Query records for a domain with optional filters.

        Filters are key-value pairs matched against record fields.
        Currently supported filter keys:
          - ``verdict``: match score.verdict
          - ``min_overall``: score.overall >= value
          - ``max_overall``: score.overall <= value

        Args:
            domain: The domain name to query.
            filters: Optional filter dict.
            limit: Maximum number of records to return.

        Returns:
            List of matching records, newest first.
        """
        ...

    def trend(
        self,
        domain: str,
        field: str,
        window: int = 20,
    ) -> TrendResult:
        """Compute a trend for a numeric field over recent records.

        Args:
            domain: The domain name.
            field: The field to trend (e.g., "overall", or a dimension name).
            window: Number of recent records to include.

        Returns:
            A TrendResult with slope, direction, and alert flag.
        """
        ...

    def aggregate(
        self,
        domain: str,
        group_by: str,
        field: str,
    ) -> dict[str, float]:
        """Aggregate a field grouped by another field.

        Args:
            domain: The domain name.
            group_by: The field to group by (e.g., "verdict").
            field: The field to average (e.g., "overall").

        Returns:
            Dict mapping group values to averaged field values.
        """
        ...


# ---------------------------------------------------------------------------
# JSON serialization helpers
# ---------------------------------------------------------------------------


def _record_to_dict(record: DomainRecord) -> dict[str, Any]:
    """Serialize a DomainRecord to a JSON-compatible dict."""
    return {
        "id": record.id,
        "timestamp": record.timestamp.isoformat(),
        "domain": record.domain,
        "score": record.score.model_dump(),
        "context_summary": record.context_summary,
        "equilibrium_score": record.equilibrium_score,
        "convergence": record.convergence,
    }


def _dict_to_record(data: dict[str, Any]) -> DomainRecord:
    """Deserialize a dict to a DomainRecord."""
    score_data = data["score"]
    score = DomainScore(**score_data)

    ts = data["timestamp"]
    if isinstance(ts, str):
        # Handle both offset-aware and naive timestamps
        ts = datetime.fromisoformat(ts)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)

    return DomainRecord(
        id=data["id"],
        timestamp=ts,
        domain=data["domain"],
        score=score,
        context_summary=data.get("context_summary", {}),
        equilibrium_score=data.get("equilibrium_score"),
        convergence=data.get("convergence"),
    )


def _extract_field_value(record: DomainRecord, field: str) -> float | None:
    """Extract a numeric field value from a record.

    Supports:
      - "overall" -> record.score.overall
      - "equilibrium_score" -> record.equilibrium_score
      - Any dimension name -> record.score.dimensions[name]
    """
    if field == "overall":
        return record.score.overall
    elif field == "equilibrium_score":
        return record.equilibrium_score
    elif field in record.score.dimensions:
        return record.score.dimensions[field]
    return None


def _matches_filters(
    record: DomainRecord,
    filters: dict[str, Any] | None,
) -> bool:
    """Check if a record matches the given filters."""
    if not filters:
        return True

    for key, value in filters.items():
        if key == "verdict":
            if record.score.verdict != value:
                return False
        elif key == "min_overall":
            if record.score.overall < float(value):
                return False
        elif key == "max_overall":
            if record.score.overall > float(value):
                return False

    return True


def _compute_trend(
    values: list[float],
    field: str,
    improving_direction: str = "up",
) -> TrendResult:
    """Compute a TrendResult from a list of values.

    Args:
        values: Numeric values in chronological order.
        field: The field name for the result.
        improving_direction: "up" if higher is better, "down" otherwise.

    Returns:
        A TrendResult with slope, direction, and alert.
    """
    if not values:
        return TrendResult(field=field)

    slope = _linear_slope(values)

    # Classify direction
    threshold = 0.01  # Minimum slope magnitude for non-stable
    if abs(slope) < threshold:
        direction = "stable"
    elif slope > 0:
        direction = "improving" if improving_direction == "up" else "declining"
    else:
        direction = "declining" if improving_direction == "up" else "improving"

    # Alert if declining
    alert = direction == "declining"

    return TrendResult(
        field=field,
        values=values,
        slope=slope,
        direction=direction,
        alert=alert,
    )


# ---------------------------------------------------------------------------
# JSONLStore — append-only JSONL file, one per domain
# ---------------------------------------------------------------------------


class JSONLStore:
    """Append-only JSONL file store, one file per domain.

    Files are stored at ``{store_path}/{domain}.jsonl``.
    Thread-safe writes via ``fcntl`` file locking.
    Query via line-by-line scan (suitable for < 10K records per domain).
    """

    def __init__(self, store_path: Path) -> None:
        self.store_path = store_path
        self.store_path.mkdir(parents=True, exist_ok=True)

    def _domain_path(self, domain: str) -> Path:
        """Get the JSONL file path for a domain."""
        return self.store_path / f"{domain}.jsonl"

    def _read_all(self, domain: str) -> list[DomainRecord]:
        """Read all records for a domain."""
        path = self._domain_path(domain)
        if not path.exists():
            return []

        records: list[DomainRecord] = []
        text = path.read_text(encoding="utf-8")
        for line in text.strip().splitlines():
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                records.append(_dict_to_record(data))
            except (json.JSONDecodeError, Exception) as exc:
                logger.warning("Skipping malformed JSONL line: %s", exc)
        return records

    def append(self, record: DomainRecord) -> str:
        """Append a record to the domain's JSONL file."""
        path = self._domain_path(record.domain)
        data = _record_to_dict(record)
        line = json.dumps(data, default=str) + "\n"

        with open(path, "a", encoding="utf-8") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                f.write(line)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

        return record.id

    def get(self, record_id: str) -> DomainRecord | None:
        """Search all domain files for a record by ID."""
        for path in self.store_path.glob("*.jsonl"):
            domain = path.stem
            for record in self._read_all(domain):
                if record.id == record_id:
                    return record
        return None

    def query(
        self,
        domain: str,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
    ) -> list[DomainRecord]:
        """Query records for a domain, newest first."""
        records = self._read_all(domain)
        # Filter
        matched = [r for r in records if _matches_filters(r, filters)]
        # Sort newest first
        matched.sort(key=lambda r: r.timestamp, reverse=True)
        return matched[:limit]

    def trend(
        self,
        domain: str,
        field: str,
        window: int = 20,
    ) -> TrendResult:
        """Compute a trend for a field over recent records."""
        records = self._read_all(domain)
        # Sort oldest first for chronological order
        records.sort(key=lambda r: r.timestamp)
        # Take the last `window` records
        recent = records[-window:] if len(records) > window else records

        values: list[float] = []
        for r in recent:
            val = _extract_field_value(r, field)
            if val is not None:
                values.append(val)

        return _compute_trend(values, field)

    def aggregate(
        self,
        domain: str,
        group_by: str,
        field: str,
    ) -> dict[str, float]:
        """Aggregate a field grouped by another field."""
        records = self._read_all(domain)

        groups: dict[str, list[float]] = {}
        for r in records:
            # Get group key
            if group_by == "verdict":
                group_key = r.score.verdict
            elif group_by == "convergence":
                group_key = r.convergence or "none"
            elif group_by == "scaffold_name":
                group_key = r.score.scaffold_name
            else:
                continue

            # Get field value
            val = _extract_field_value(r, field)
            if val is not None:
                groups.setdefault(group_key, []).append(val)

        result: dict[str, float] = {}
        for key, vals in groups.items():
            result[key] = sum(vals) / len(vals) if vals else 0.0

        return result


# ---------------------------------------------------------------------------
# SQLiteStore — local database, one table per domain
# ---------------------------------------------------------------------------


class SQLiteStore:
    """SQLite-backed domain record store.

    Single ``reviews.db`` file with one table per domain.
    Thread-safe via SQLite's built-in locking.
    """

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(
            str(db_path),
            check_same_thread=False,
        )
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")

    def _ensure_table(self, domain: str) -> None:
        """Create the domain's table if it does not exist."""
        # Sanitize table name: replace non-alphanumeric with underscore
        table = self._table_name(domain)
        self._conn.execute(f"""
            CREATE TABLE IF NOT EXISTS [{table}] (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                domain TEXT NOT NULL,
                overall REAL NOT NULL,
                verdict TEXT NOT NULL,
                scaffold_name TEXT NOT NULL DEFAULT '',
                equilibrium_score REAL,
                convergence TEXT,
                data TEXT NOT NULL
            )
        """)
        self._conn.commit()

    @staticmethod
    def _table_name(domain: str) -> str:
        """Derive a safe table name from a domain name."""
        return "domain_" + "".join(
            c if c.isalnum() else "_" for c in domain
        )

    def append(self, record: DomainRecord) -> str:
        """Insert a record into the domain's table."""
        self._ensure_table(record.domain)
        table = self._table_name(record.domain)
        data = json.dumps(_record_to_dict(record), default=str)

        self._conn.execute(
            f"""INSERT INTO [{table}]
                (id, timestamp, domain, overall, verdict, scaffold_name,
                 equilibrium_score, convergence, data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                record.id,
                record.timestamp.isoformat(),
                record.domain,
                record.score.overall,
                record.score.verdict,
                record.score.scaffold_name,
                record.equilibrium_score,
                record.convergence,
                data,
            ),
        )
        self._conn.commit()
        return record.id

    def get(self, record_id: str) -> DomainRecord | None:
        """Search all domain tables for a record by ID."""
        # Get all domain tables
        cursor = self._conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name LIKE 'domain_%'"
        )
        for row in cursor.fetchall():
            table = row[0]
            result = self._conn.execute(
                f"SELECT data FROM [{table}] WHERE id = ?",
                (record_id,),
            ).fetchone()
            if result:
                data = json.loads(result[0])
                return _dict_to_record(data)
        return None

    def query(
        self,
        domain: str,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
    ) -> list[DomainRecord]:
        """Query records for a domain, newest first."""
        self._ensure_table(domain)
        table = self._table_name(domain)

        where_clauses = ["1=1"]
        params: list[Any] = []

        if filters:
            if "verdict" in filters:
                where_clauses.append("verdict = ?")
                params.append(filters["verdict"])
            if "min_overall" in filters:
                where_clauses.append("overall >= ?")
                params.append(float(filters["min_overall"]))
            if "max_overall" in filters:
                where_clauses.append("overall <= ?")
                params.append(float(filters["max_overall"]))

        where = " AND ".join(where_clauses)
        params.append(limit)

        cursor = self._conn.execute(
            f"SELECT data FROM [{table}] WHERE {where} "
            f"ORDER BY timestamp DESC LIMIT ?",
            params,
        )

        records: list[DomainRecord] = []
        for row in cursor.fetchall():
            data = json.loads(row[0])
            records.append(_dict_to_record(data))
        return records

    def trend(
        self,
        domain: str,
        field: str,
        window: int = 20,
    ) -> TrendResult:
        """Compute a trend for a field over recent records."""
        self._ensure_table(domain)
        table = self._table_name(domain)

        cursor = self._conn.execute(
            f"SELECT data FROM [{table}] ORDER BY timestamp ASC",
        )

        all_records: list[DomainRecord] = []
        for row in cursor.fetchall():
            data = json.loads(row[0])
            all_records.append(_dict_to_record(data))

        recent = all_records[-window:] if len(all_records) > window else all_records

        values: list[float] = []
        for r in recent:
            val = _extract_field_value(r, field)
            if val is not None:
                values.append(val)

        return _compute_trend(values, field)

    def aggregate(
        self,
        domain: str,
        group_by: str,
        field: str,
    ) -> dict[str, float]:
        """Aggregate a field grouped by another field."""
        self._ensure_table(domain)
        table = self._table_name(domain)

        # For simple cases, use SQL directly
        if group_by == "verdict" and field == "overall":
            cursor = self._conn.execute(
                f"SELECT verdict, AVG(overall) FROM [{table}] GROUP BY verdict"
            )
            return {row[0]: row[1] for row in cursor.fetchall()}

        # General case: load records and compute in Python
        cursor = self._conn.execute(f"SELECT data FROM [{table}]")
        records = [
            _dict_to_record(json.loads(row[0]))
            for row in cursor.fetchall()
        ]

        groups: dict[str, list[float]] = {}
        for r in records:
            if group_by == "verdict":
                group_key = r.score.verdict
            elif group_by == "convergence":
                group_key = r.convergence or "none"
            elif group_by == "scaffold_name":
                group_key = r.score.scaffold_name
            else:
                continue

            val = _extract_field_value(r, field)
            if val is not None:
                groups.setdefault(group_key, []).append(val)

        result: dict[str, float] = {}
        for key, vals in groups.items():
            result[key] = sum(vals) / len(vals) if vals else 0.0

        return result

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()
