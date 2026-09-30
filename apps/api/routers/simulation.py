"""FastAPI router for What-If budget allocation simulations."""

from fastapi import APIRouter
from apps.api.schemas import WhatIfRequest, WhatIfResponse
from apps.api.services import run_what_if_simulation

router = APIRouter(prefix="/api/simulation", tags=["Simulation"])


@router.post("/what-if", response_model=WhatIfResponse)
def simulate_budget_allocation(req: WhatIfRequest):
    """Simulates how allocating funds to a sector in a district impacts infrastructure index and reduces the gap."""
    return run_what_if_simulation(req)
