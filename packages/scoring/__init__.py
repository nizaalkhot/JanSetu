"""JanSetu Demand-vs-Supply Gap and Explainable Priority Scoring Engine.

Formulas:
- Gap Score = (Demand Intensity * (Population Affected / 10,000)) / (Current Supply Index + 0.1)
  Normalized to 0 - 100 scale.
- Priority Score = Gap Score * Urgency Weight * Equity Weight * Feasibility * Budget Headroom Factor
  Produces a transparent score between 0 and 100 with full explainability breakdown.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field


class ScoreBreakdown(BaseModel):
    gap_score: float = Field(..., description="0-100 severity of unmet citizen demand")
    priority_score: float = Field(..., description="0-100 final actionable investment priority")
    demand_intensity: float
    population_affected: int
    current_supply_index: float
    urgency_weight: float
    equity_weight: float
    feasibility_weight: float
    budget_headroom_factor: float
    explanation: str


def compute_gap_score(
    demand_intensity: float,
    population_affected: int,
    current_supply_index: float,
) -> float:
    """
    Computes unmet infrastructure gap (0-100):
    - demand_intensity: aggregate citizen requests / complaints normalized (1.0 to 10.0)
    - population_affected: number of people in the catchment area
    - current_supply_index: 0.0 (no infrastructure) to 1.0 (fully saturated)
    """
    # Safeguard zero division and range [0.05, 0.98]
    effective_supply = max(0.05, min(0.98, current_supply_index))
    
    # Population scaling weight (dampened square-root factor normalized per 1M pop)
    pop_factor = max(0.6, min(1.4, (population_affected / 1000000.0) ** 0.3))
    
    # Unmet severity is proportional to demand intensity, unmet supply (1 - supply), and population weight
    unmet_supply = 1.0 - effective_supply
    raw_gap = demand_intensity * 10.0 * unmet_supply * pop_factor
    
    normalized_gap = max(5.0, min(100.0, raw_gap))
    return round(normalized_gap, 2)


def compute_priority_score(
    gap_score: float,
    urgency: int = 3,  # 1 (low) to 5 (critical emergency)
    equity_weight: float = 1.0,  # 1.0 to 1.5 for historically marginalized / aspirational districts
    feasibility: float = 0.85,  # 0.0 to 1.0 (technical, topographic & administrative feasibility)
    budget_allocated: float = 100.0,  # in Millions / Crores
    budget_spent: float = 30.0,
) -> ScoreBreakdown:
    """
    Computes actionable investment priority with full explainability.
    """
    # Urgency weight: scale 1-5 to multiplier 0.7 - 1.3
    urgency_weight = 0.7 + (urgency - 1) * 0.15

    # Budget headroom: if budget spent is low vs allocated, there is high unspent headroom to deploy
    if budget_allocated > 0:
        utilization = min(1.0, budget_spent / budget_allocated)
        # More unspent headroom = higher ease of deploying funds immediately
        budget_headroom_factor = 0.7 + (1.0 - utilization) * 0.4
    else:
        budget_headroom_factor = 0.8

    # Calculate raw priority
    raw_priority = (
        gap_score
        * (urgency_weight / 1.3)
        * (equity_weight / 1.5)
        * feasibility
        * budget_headroom_factor
    )
    final_priority = round(min(100.0, max(0.0, raw_priority)), 2)

    # Narrative explanation for policymakers
    narrative = (
        f"Priority Score {final_priority}/100 derived from Gap Score {gap_score}/100. "
        f"Urgency multiplier is {urgency_weight:.2f} (level {urgency}/5). "
        f"Equity weight of {equity_weight:.2f} ensures low-digital-voice regions are prioritized. "
        f"Budget headroom factor is {budget_headroom_factor:.2f} based on available fiscal envelope."
    )

    return ScoreBreakdown(
        gap_score=gap_score,
        priority_score=final_priority,
        demand_intensity=round(gap_score / 10.0, 2),
        population_affected=10000,
        current_supply_index=0.3,
        urgency_weight=round(urgency_weight, 2),
        equity_weight=round(equity_weight, 2),
        feasibility_weight=round(feasibility, 2),
        budget_headroom_factor=round(budget_headroom_factor, 2),
        explanation=narrative,
    )
