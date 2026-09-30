"""Pydantic schemas for JanSetu Google ADK agents."""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class CitizenRequestInput(BaseModel):
    id: Optional[str] = None
    channel: str = Field(default="whatsapp", description="whatsapp, telegram, ivr_voice, pwa_web")
    raw_text: Optional[str] = None
    audio_base64: Optional[str] = None
    audio_duration_sec: Optional[float] = None
    reported_location: Optional[str] = None
    phone_number: Optional[str] = None


class IntakeResult(BaseModel):
    request_id: str
    channel: str
    normalized_text: str
    is_audio: bool = False
    transcription_confidence: float = 1.0


class LanguageResult(BaseModel):
    detected_language: str = Field(..., description="ISO language code, e.g., 'hi', 'pt', 'en', 'ru'")
    language_name: str
    dialect_notes: str = ""
    is_code_mixed: bool = False  # e.g., Hinglish
    pivot_english_text: str = Field(..., description="Canonical English translation")


class ClassificationResult(BaseModel):
    category_id: str = Field(..., description="ID from UN SDG taxonomy")
    category_name: str
    sdg_goal: int
    urgency: int = Field(..., ge=1, le=5, description="Urgency level from 1 (low) to 5 (critical/emergency)")
    sentiment: float = Field(..., ge=-1.0, le=1.0, description="Sentiment score from -1.0 to 1.0")
    key_issues: List[str] = Field(default_factory=list)
    entities: List[str] = Field(default_factory=list)


class GeoEnrichmentResult(BaseModel):
    admin_unit_id: str
    country: str
    state_province: str
    district: str
    resolved_lat: float
    resolved_lng: float
    confidence: float
    resolution_method: str  # landmark_ner, user_metadata, or cluster_inferred


class AnalysisResult(BaseModel):
    gap_score: float = Field(..., description="0-100 unmet infrastructure gap score")
    priority_score: float = Field(..., description="0-100 overall priority score")
    current_supply_index: float
    demand_intensity: float
    equity_weight: float
    budget_headroom_cr: float
    explanation: str


class RecommendationBrief(BaseModel):
    project_title: str
    sector: str
    target_admin_unit: str
    problem_statement: str
    evidence_summary: str
    estimated_beneficiaries: int
    estimated_cost_cr: float
    suggested_budget_head: str
    key_deliverables: List[str]
    implementation_risks: List[str]


class CritiqueReport(BaseModel):
    approved: bool
    bias_audit_passed: bool
    digital_divide_penalty_applied: bool
    notes: str
    suggested_refinements: List[str] = Field(default_factory=list)


class CitizenFeedbackResponse(BaseModel):
    request_id: str
    target_language: str
    message: str
    action_item: str
    estimated_resolution_time: str
