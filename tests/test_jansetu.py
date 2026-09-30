"""Comprehensive unit and integration test suite for JanSetu."""

import pytest
from fastapi.testclient import TestClient
from packages.taxonomy import TAXONOMY_CATEGORIES, match_category_by_keywords
from packages.scoring import compute_gap_score, compute_priority_score
from packages.connectors import default_connector
from apps.agents.pipeline import pipeline_instance
from apps.agents.schemas import CitizenRequestInput
from apps.api.main import app

client = TestClient(app)


def test_taxonomy_and_scoring():
    """Validates UN SDG taxonomy and explainable scoring formulas."""
    assert len(TAXONOMY_CATEGORIES) == 6
    matched = match_category_by_keywords("pani ki samasya handpump")
    assert matched == "water_sanitation"

    gap = compute_gap_score(demand_intensity=8.0, population_affected=20000, current_supply_index=0.25)
    assert 0 <= gap <= 100

    priority = compute_priority_score(gap_score=gap, urgency=4, equity_weight=1.3)
    assert 0 <= priority.priority_score <= 100
    assert "Priority Score" in priority.explanation


def test_country_connectors():
    """Validates sovereign data connectors for BRICS pilot units."""
    units = default_connector.get_all_admin_units()
    assert len(units) >= 4

    banda = default_connector.get_admin_unit("IN-UP-BAN")
    assert banda is not None
    assert banda.district == "Banda (Bundelkhand)"
    assert "water_sanitation" in banda.infrastructure_indices

    resolved = default_connector.resolve_landmark_to_unit("tindwari")
    assert resolved.id == "IN-UP-BAN"


def test_multi_agent_pipeline_execution():
    """Tests the full Google ADK multi-agent execution pipeline on Bundeli voice note."""
    req = CitizenRequestInput(
        channel="whatsapp_audio",
        audio_base64="bundeli_tindwari_handpump",
        reported_location="Tindwari, Banda"
    )
    result = pipeline_instance.run(req)

    assert result.status == "completed"
    assert result.intake.is_audio is True
    assert result.language.detected_language == "hi"
    assert "Bundeli" in result.language.dialect_notes
    assert result.classification.category_id == "water_sanitation"
    assert result.geo.admin_unit_id == "IN-UP-BAN"
    assert result.analysis.gap_score > 50
    assert result.analysis.priority_score > 50
    assert result.critique.approved is True
    assert "नमस्ते" in result.citizen_feedback.message


def test_api_endpoints():
    """Tests FastAPI REST endpoints."""
    # 1. Hotspots
    res = client.get("/api/analytics/gap-hotspots")
    assert res.status_code == 200
    hotspots = res.json()
    assert len(hotspots) > 0

    # 2. Recommendations
    res = client.get("/api/recommendations")
    assert res.status_code == 200
    recs = res.json()
    assert len(recs) >= 3

    # 3. What-If Simulation
    res = client.post("/api/simulation/what-if", json={
        "admin_unit_id": "IN-UP-BAN",
        "sector": "water_sanitation",
        "additional_budget_cr": 15.0
    })
    assert res.status_code == 200
    sim = res.json()
    assert sim["gap_reduction_pct"] > 0
    assert sim["simulated_supply_index"] > sim["baseline_supply_index"]

    # 4. Copilot
    res = client.post("/api/copilot/query", json={
        "query": "Which districts have the highest water distress?"
    })
    assert res.status_code == 200
    copilot_res = res.json()
    assert len(copilot_res["grounded_evidence"]) > 0

    # 5. Impact Metrics
    res = client.get("/api/impact/metrics")
    assert res.status_code == 200
    metrics = res.json()
    assert len(metrics) >= 3

    # 6. BRICS Federation Nodes
    res = client.get("/api/federation/nodes")
    assert res.status_code == 200
    nodes = res.json()
    assert any(n["country"] == "India" for n in nodes)
    assert any(n["country"] == "Brazil" for n in nodes)
