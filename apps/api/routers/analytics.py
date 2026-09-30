"""FastAPI router for administrative units, infrastructure indices, and gap score analytics."""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from packages.connectors import default_connector
from packages.taxonomy import get_all_categories
from packages.scoring import compute_gap_score

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/regions")
def get_all_regions():
    """Lists all monitored BRICS sovereign administrative units."""
    return default_connector.get_all_admin_units()


@router.get("/regions/{region_id}")
def get_region_detail(region_id: str):
    """Retrieves full details for a specific administrative unit."""
    unit = default_connector.get_admin_unit(region_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Administrative unit not found")
    return unit


@router.get("/categories")
def get_categories():
    """Returns UN SDG-aligned development taxonomy."""
    return get_all_categories()


@router.get("/gap-hotspots")
def get_gap_hotspots():
    """Returns calculated gap scores across all regions and sectors."""
    regions = default_connector.get_all_admin_units()
    hotspots = []

    for r in regions:
        for sector, supply_idx in r.infrastructure_indices.items():
            gap = compute_gap_score(demand_intensity=8.2, population_affected=r.population, current_supply_index=supply_idx)
            hotspots.append({
                "admin_unit_id": r.id,
                "district": r.district,
                "country": r.country,
                "lat": r.lat,
                "lng": r.lng,
                "sector": sector,
                "supply_index": supply_idx,
                "gap_score": gap,
                "equity_weight": r.equity_weight,
            })

    # Sort descending by gap score
    hotspots.sort(key=lambda x: x["gap_score"], reverse=True)
    return hotspots
