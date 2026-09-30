"""JanSetu Country Data Connectors and Adapters."""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class BudgetAllocation(BaseModel):
    allocated_cr: float
    spent_cr: float
    headroom_cr: float


class AdminUnit(BaseModel):
    id: str
    country: str
    country_code: str
    state_province: str
    district: str
    lat: float
    lng: float
    population: int
    equity_weight: float
    demographic_profile: str
    infrastructure_indices: Dict[str, float]
    budget_allocations: Dict[str, BudgetAllocation]


class DataConnector:
    """Provides sovereign-deployable unified access to country data."""

    def __init__(self, data_path: Optional[str] = None):
        if not data_path:
            base_dir = Path(__file__).resolve().parent.parent.parent
            data_path = base_dir / "data" / "seeds" / "brics_data.json"

        self.data_path = Path(data_path)
        self._units: Dict[str, AdminUnit] = {}
        self._sample_voices: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if self.data_path.exists():
            with open(self.data_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
                for item in raw.get("admin_units", []):
                    unit = AdminUnit(**item)
                    self._units[unit.id] = unit
                self._sample_voices = raw.get("sample_citizen_voices", [])

    def get_all_admin_units(self) -> List[AdminUnit]:
        return list(self._units.values())

    def get_admin_unit(self, unit_id: str) -> Optional[AdminUnit]:
        return self._units.get(unit_id)

    def get_sample_citizen_voices(self) -> List[Dict[str, Any]]:
        return self._sample_voices

    def resolve_landmark_to_unit(self, landmark_or_text: str) -> Optional[AdminUnit]:
        """Resolves text mentions of districts, villages or landmarks to the correct Admin Unit."""
        query = landmark_or_text.lower()
        for unit in self._units.values():
            if (
                unit.district.lower() in query
                or unit.state_province.lower() in query
                or unit.country.lower() in query
            ):
                return unit
            # specific sub-region checks
            if "tindwari" in query or "banda" in query or "naraini" in query:
                if unit.id == "IN-UP-BAN":
                    return unit
            if "beed" in query or "marathwada" in query:
                if unit.id == "IN-MH-BEE":
                    return unit
            if "petrolina" in query or "sertão" in query or "pernambuco" in query:
                if unit.id == "BR-PE-PET":
                    return unit
            if "ortambo" in query or "mthatha" in query or "eastern cape" in query:
                if unit.id == "ZA-EC-ORT":
                    return unit

        # Default fallback to Banda if in India or unknown
        return self._units.get("IN-UP-BAN")


# Global connector singleton
default_connector = DataConnector()
