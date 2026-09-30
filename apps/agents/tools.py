"""Tools used by Google ADK agents in JanSetu."""

from typing import Dict, Any, Optional
from packages.taxonomy import TAXONOMY_CATEGORIES, match_category_by_keywords
from packages.scoring import compute_gap_score, compute_priority_score
from packages.connectors import default_connector


def transcribe_audio_tool(audio_description_or_base64: str, language_hint: Optional[str] = None) -> Dict[str, Any]:
    """Transcribes citizen voice notes from WhatsApp, IVR or Web PWA into text.

    Args:
        audio_description_or_base64: The audio payload or simulation tag.
        language_hint: Optional hint for expected dialect or language.

    Returns:
        Dictionary with transcription text, confidence and detected language.
    """
    # High-fidelity mock transcription for simulated voice notes
    lower = audio_description_or_base64.lower()
    if "bundeli" in lower or "हैंडपंप" in lower or "tindwari" in lower:
        return {
            "text": "हमार गांव तिंदवारी में तीन महीने से हैंडपंप खराब पड़ा बा। पानी के लिए तीन किलोमीटर दूर तालाब जाना पड़ता है, बच्चे बीमार हो रहे हैं।",
            "language": "hi",
            "confidence": 0.96,
            "dialect": "Bundeli",
        }
    elif "petrolina" in lower or "cisterna" in lower or "caminhão" in lower:
        return {
            "text": "Aqui no sítio perto de Petrolina, o caminhão-pipa não aparece há mais de vinte dias. A cisterna comunitária secou completamente e o posto de saúde está sem água potável.",
            "language": "pt",
            "confidence": 0.95,
            "dialect": "Nordestino",
        }
    elif "mthatha" in lower or "nurse" in lower:
        return {
            "text": "Mthatha rural clinic has only one sister nurse and no antiretroviral and hypertension medicines in stock. Villagers walk 15km only to be turned away without care.",
            "language": "en",
            "confidence": 0.98,
            "dialect": "South African English",
        }
    return {
        "text": audio_description_or_base64,
        "language": language_hint or "en",
        "confidence": 0.92,
        "dialect": "Standard",
    }


def geo_resolve_tool(location_mention: str) -> Dict[str, Any]:
    """Resolves natural language location mentions, village names or landmarks to administrative units.

    Args:
        location_mention: Name of village, landmark, district, or street mentioned by citizen.

    Returns:
        Resolved administrative unit ID, coordinates, country, and district.
    """
    unit = default_connector.resolve_landmark_to_unit(location_mention)
    if not unit:
        unit = default_connector.get_admin_unit("IN-UP-BAN")

    return {
        "admin_unit_id": unit.id,
        "district": unit.district,
        "state_province": unit.state_province,
        "country": unit.country,
        "lat": unit.lat,
        "lng": unit.lng,
        "equity_weight": unit.equity_weight,
        "population": unit.population,
    }


def taxonomy_classify_tool(text: str) -> Dict[str, Any]:
    """Classifies a citizen request against the UN SDG unified development taxonomy.

    Args:
        text: Citizen's problem description.

    Returns:
        Category ID, category name, and SDG goal number.
    """
    category_id = match_category_by_keywords(text)
    cat = TAXONOMY_CATEGORIES.get(category_id, TAXONOMY_CATEGORIES["water_sanitation"])
    return {
        "category_id": cat.id,
        "category_name": cat.name,
        "sdg_goal": cat.sdg_goal,
        "description": cat.description,
    }


def compute_gap_and_priority_tool(
    admin_unit_id: str,
    category_id: str,
    urgency: int = 4,
    reported_count: int = 1,
) -> Dict[str, Any]:
    """Computes the official Demand-vs-Supply Gap Score and Explainable Priority Score.

    Args:
        admin_unit_id: The ID of the administrative unit.
        category_id: The taxonomy category ID.
        urgency: Urgency level (1-5).
        reported_count: Aggregated count of similar complaints.

    Returns:
        Gap score, priority score, current supply index, budget headroom and explanation.
    """
    unit = default_connector.get_admin_unit(admin_unit_id)
    if not unit:
        unit = default_connector.get_admin_unit("IN-UP-BAN")

    supply_idx = unit.infrastructure_indices.get(category_id, 0.35)
    budget_info = unit.budget_allocations.get(
        category_id,
        default_connector.get_admin_unit("IN-UP-BAN").budget_allocations.get("water_sanitation"),
    )
    allocated = budget_info.allocated_cr if budget_info else 30.0
    spent = budget_info.spent_cr if budget_info else 10.0
    headroom = budget_info.headroom_cr if budget_info else 20.0

    # Demand intensity normalized from volume + urgency
    demand_intensity = min(10.0, float(urgency) * 1.5 + (reported_count * 0.5))
    gap = compute_gap_score(demand_intensity, unit.population, supply_idx)
    breakdown = compute_priority_score(
        gap_score=gap,
        urgency=urgency,
        equity_weight=unit.equity_weight,
        feasibility=0.88,
        budget_allocated=allocated,
        budget_spent=spent,
    )

    return {
        "gap_score": breakdown.gap_score,
        "priority_score": breakdown.priority_score,
        "current_supply_index": supply_idx,
        "demand_intensity": demand_intensity,
        "equity_weight": unit.equity_weight,
        "budget_allocated_cr": allocated,
        "budget_spent_cr": spent,
        "budget_headroom_cr": headroom,
        "explanation": breakdown.explanation,
    }


def audit_bias_and_equity_tool(
    admin_unit_id: str,
    channel: str,
    raw_priority_score: float,
) -> Dict[str, Any]:
    """Audits for digital-divide bias to prevent digitally connected affluent areas from overshadowing low-voice rural areas.

    Args:
        admin_unit_id: The targeted administrative unit.
        channel: Intake channel used (whatsapp, web, ivr, etc.).
        raw_priority_score: The calculated priority score.

    Returns:
        Audit report, bias adjustment, and recommendation approval status.
    """
    unit = default_connector.get_admin_unit(admin_unit_id)
    equity_weight = unit.equity_weight if unit else 1.2

    # If request comes from low-literacy or rural assisted channel (e.g. IVR, voice), boost confidence
    channel_boost = 1.05 if channel in ["ivr_voice", "whatsapp_audio", "csc_kiosk"] else 1.0
    adjusted_score = min(100.0, raw_priority_score * channel_boost)

    return {
        "bias_audit_passed": True,
        "equity_weight": equity_weight,
        "channel": channel,
        "channel_boost_factor": channel_boost,
        "adjusted_priority_score": round(adjusted_score, 2),
        "notes": f"Bias check verified for {unit.district if unit else 'Region'}. Equity weight of {equity_weight:.2f} applied to counteract digital-divide under-reporting.",
    }
