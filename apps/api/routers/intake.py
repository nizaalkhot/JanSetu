"""FastAPI router for citizen grievance intake channels and pipeline execution."""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from apps.agents.schemas import CitizenRequestInput
from apps.agents.pipeline import pipeline_instance, PipelineExecutionResult
from apps.api.services import recommendation_store

router = APIRouter(prefix="/api/intake", tags=["Intake"])


@router.post("/submit", response_model=PipelineExecutionResult)
def submit_citizen_request(req: CitizenRequestInput):
    """Processes a citizen voice or text submission through the Google ADK multi-agent pipeline."""
    result = pipeline_instance.run(req)
    # Store in memory for analytics
    recommendation_store.processed_requests.append(result.model_dump())
    return result


@router.get("/history", response_model=List[Dict[str, Any]])
def get_intake_history():
    """Returns recently processed citizen requests."""
    return recommendation_store.processed_requests[-20:]
