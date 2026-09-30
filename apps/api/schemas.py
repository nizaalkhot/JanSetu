"""FastAPI API schemas for JanSetu."""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class WhatIfRequest(BaseModel):
    admin_unit_id: str
    sector: str
    additional_budget_cr: float = Field(..., description="Additional budget allocated in Crores / Millions")
    intervention_type: str = Field(default="rapid_repair", description="rapid_repair, new_infrastructure, staff_expansion")


class WhatIfResponse(BaseModel):
    admin_unit_id: str
    district: str
    sector: str
    baseline_supply_index: float
    simulated_supply_index: float
    baseline_gap_score: float
    simulated_gap_score: float
    gap_reduction_pct: float
    projected_additional_beneficiaries: int
    recommendation_summary: str


class CopilotQueryRequest(BaseModel):
    query: str
    admin_unit_id: Optional[str] = None
    sector_filter: Optional[str] = None


class CopilotQueryResponse(BaseModel):
    query: str
    answer: str
    grounded_evidence: List[str]
    suggested_actions: List[str]


class RecommendationActionRequest(BaseModel):
    action: str = Field(..., description="'approve', 'reject', or 'revise'")
    reviewer_name: str
    notes: Optional[str] = None


class ImpactProjectMetric(BaseModel):
    project_id: str
    title: str
    district: str
    sector: str
    status: str
    pre_complaint_monthly_volume: int
    post_complaint_monthly_volume: int
    complaint_reduction_pct: float
    pre_citizen_sentiment: float
    post_citizen_sentiment: float
    infrastructure_index_gain: float
