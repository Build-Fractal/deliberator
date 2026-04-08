"""FastAPI router factory for domain plugins.

Creates REST endpoints for a domain plugin backed by a DomainStore.
Each domain gets its own router that can be mounted on a FastAPI app.

Endpoints:
  - POST /submit — extract + score + persist
  - GET /{record_id} — get a record
  - GET /health — aggregate recent scores
  - GET /trends/{field} — field trend analysis
  - GET /scaffolds — list available scaffolds

This module imports nothing from ``engine/``, ``linter/``, or ``mcp_server``.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from conversus.domains.base import (
    DomainContext,
    DomainPlugin,
    Scaffold,
    load_scaffold,
)
from conversus.domains.store import DomainStore

logger = logging.getLogger("conversus.domains.api")


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------


class SubmitRequest(BaseModel):
    """Request body for the /submit endpoint."""

    workspace: str
    changed_files: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    scaffold: str = "default"
    equilibrium_score: float | None = None
    convergence: str | None = None


class SubmitResponse(BaseModel):
    """Response body for the /submit endpoint."""

    record_id: str
    verdict: str
    overall: float
    hard_blocks: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    dimensions: dict[str, float] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    """Response body for the /health endpoint."""

    domain: str
    recent_count: int
    average_overall: float
    verdict_distribution: dict[str, float] = Field(default_factory=dict)


class TrendResponse(BaseModel):
    """Response body for the /trends/{field} endpoint."""

    field: str
    slope: float
    direction: str
    alert: bool
    values: list[float] = Field(default_factory=list)


class ScaffoldInfo(BaseModel):
    """Summary of a scaffold for the /scaffolds endpoint."""

    name: str
    description: str
    dimensions: list[str] = Field(default_factory=list)
    hard_block_count: int = 0


# ---------------------------------------------------------------------------
# Router factory
# ---------------------------------------------------------------------------


def create_domain_router(
    domain: DomainPlugin,
    store: DomainStore,
) -> APIRouter:
    """Create REST endpoints for a domain plugin.

    Args:
        domain: The domain plugin instance.
        store: The storage backend for records.

    Returns:
        A FastAPI APIRouter with all domain endpoints.
    """
    router = APIRouter(
        prefix=f"/{domain.name}",
        tags=[domain.name],
    )

    @router.post("/submit", response_model=SubmitResponse)
    def submit(request: SubmitRequest) -> SubmitResponse:
        """Extract variables, score, and persist a review record."""
        context = DomainContext(
            workspace=Path(request.workspace),
            changed_files=[Path(f) for f in request.changed_files],
            metadata=request.metadata,
        )

        # Extract
        variables = domain.extract(context)

        # Score
        score = domain.score(variables, request.scaffold)

        # Persist
        record = domain.create_record(
            score=score,
            context=context,
            equilibrium_score=request.equilibrium_score,
            convergence=request.convergence,
        )
        record_id = store.append(record)

        return SubmitResponse(
            record_id=record_id,
            verdict=score.verdict,
            overall=score.overall,
            hard_blocks=score.hard_blocks,
            recommendations=score.recommendations,
            dimensions=score.dimensions,
        )

    @router.get("/record/{record_id}")
    def get_record(record_id: str) -> dict[str, Any]:
        """Get a review record by ID."""
        record = store.get(record_id)
        if record is None:
            raise HTTPException(status_code=404, detail="Record not found")
        return record.model_dump(mode="json")

    @router.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        """Aggregate recent scores for health monitoring."""
        records = store.query(domain.name, limit=50)
        if not records:
            return HealthResponse(
                domain=domain.name,
                recent_count=0,
                average_overall=0.0,
            )

        total = sum(r.score.overall for r in records)
        avg = total / len(records)

        # Verdict distribution
        verdict_counts: dict[str, int] = {}
        for r in records:
            verdict_counts[r.score.verdict] = (
                verdict_counts.get(r.score.verdict, 0) + 1
            )
        total_count = len(records)
        distribution = {
            k: v / total_count for k, v in verdict_counts.items()
        }

        return HealthResponse(
            domain=domain.name,
            recent_count=len(records),
            average_overall=round(avg, 4),
            verdict_distribution=distribution,
        )

    @router.get("/trends/{field}", response_model=TrendResponse)
    def trends(field: str, window: int = 20) -> TrendResponse:
        """Compute a trend for a numeric field."""
        result = store.trend(domain.name, field, window)
        return TrendResponse(
            field=result.field,
            slope=round(result.slope, 6),
            direction=result.direction,
            alert=result.alert,
            values=result.values,
        )

    @router.get("/scaffolds", response_model=list[ScaffoldInfo])
    def list_scaffolds() -> list[ScaffoldInfo]:
        """List available scaffolds for this domain."""
        scaffolds: list[ScaffoldInfo] = []

        if not domain.scaffold_dir.exists():
            return scaffolds

        for path in sorted(
            p
            for ext in ("*.json", "*.yml", "*.yaml")
            for p in domain.scaffold_dir.glob(ext)
        ):
            try:
                scaffold = load_scaffold(path)
                scaffolds.append(ScaffoldInfo(
                    name=scaffold.name,
                    description=scaffold.description,
                    dimensions=list(scaffold.weights.keys()),
                    hard_block_count=len(scaffold.hard_blocks),
                ))
            except Exception:
                logger.warning(
                    "Failed to load scaffold %s, skipping.", path,
                    exc_info=True,
                )

        return scaffolds

    return router
