"""FastAPI router for policy recommendations and human-in-the-loop review."""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from apps.api.services import recommendation_store
from apps.api.schemas import RecommendationActionRequest

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


@router.get("", response_model=List[Dict[str, Any]])
def list_recommendations():
    """Lists all AI-generated policy recommendations with explainable priority scores."""
    return recommendation_store.get_all()


@router.get("/{rec_id}")
def get_recommendation(rec_id: str):
    """Retrieves specific recommendation detail with audit trail."""
    rec = recommendation_store.get_by_id(rec_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return rec


@router.post("/{rec_id}/review")
def review_recommendation(rec_id: str, action_req: RecommendationActionRequest):
    """Human-in-the-loop review endpoint for policymakers to approve, reject or request revisions."""
    updated = recommendation_store.update_status(
        rec_id=rec_id,
        action=action_req.action,
        reviewer=action_req.reviewer_name,
        notes=action_req.notes,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return updated
