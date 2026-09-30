"""JanSetu Agents package."""

import sys
from pathlib import Path

_root = str(Path(__file__).resolve().parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

from apps.agents.agents import (
    root_agent,
    intake_agent,
    language_agent,
    classifier_agent,
    geo_agent,
    analyst_agent,
    policy_agent,
    critic_agent,
    citizen_feedback_agent,
)

__all__ = [
    "root_agent",
    "intake_agent",
    "language_agent",
    "classifier_agent",
    "geo_agent",
    "analyst_agent",
    "policy_agent",
    "critic_agent",
    "citizen_feedback_agent",
]
