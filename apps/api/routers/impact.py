"""FastAPI router for project impact tracking and before/after metrics."""

from fastapi import APIRouter
from typing import List
from apps.api.schemas import ImpactProjectMetric
from apps.api.services import get_impact_metrics

router = APIRouter(prefix="/api/impact", tags=["Impact"])


@router.get("/metrics", response_model=List[ImpactProjectMetric])
def list_impact_metrics():
    """Returns empirical before/after metrics measuring whether completed projects actually relieved citizen distress."""
    return get_impact_metrics()
