"""FastAPI router for policymaker natural language copilot."""

from fastapi import APIRouter
from apps.api.schemas import CopilotQueryRequest, CopilotQueryResponse
from apps.api.services import query_copilot

router = APIRouter(prefix="/api/copilot", tags=["Copilot"])


@router.post("/query", response_model=CopilotQueryResponse)
def ask_copilot(req: CopilotQueryRequest):
    """Natural-language AI copilot for policymakers to query citizen demand, supply distress, and cross-country comparisons."""
    return query_copilot(req)
