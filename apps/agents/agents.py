"""JanSetu multi-agent system built on the Google Agent Development Kit (ADK).

Architecture aligns with Section 4 of PLAN.md:
- Intake Agent (LlmAgent + tools)
- Language Agent (LlmAgent)
- Classifier Agent (LlmAgent with Pydantic schema)
- Geo Agent (Tool-using agent)
- Analyst Agent (LlmAgent + scoring tools)
- Policy Drafting Agent (LlmAgent)
- Critic/Bias Auditor Agent (LoopAgent component)
- Citizen Feedback Agent (LlmAgent)
- Orchestrator Agent (Root Agent)
"""

from typing import List, Optional
from google.adk.agents import Agent, SequentialAgent, LoopAgent

from apps.agents.tools import (
    transcribe_audio_tool,
    geo_resolve_tool,
    taxonomy_classify_tool,
    compute_gap_and_priority_tool,
    audit_bias_and_equity_tool,
)
from apps.agents.schemas import (
    ClassificationResult,
    RecommendationBrief,
    CritiqueReport,
    CitizenFeedbackResponse,
)

# 1. Intake Agent: Normalises raw input and transcribes audio/voice notes
intake_agent = Agent(
    name="intake_agent",
    description="Normalises citizen messages across channels (WhatsApp, Telegram, IVR, PWA) and handles voice transcription.",
    instruction=(
        "You are the JanSetu Citizen Intake Agent. Your job is to ingest citizen input, whether text "
        "or audio voice note, and produce clean normalized text while preserving local dialect nuances."
    ),
    tools=[transcribe_audio_tool],
)

# 2. Language Agent: Multilingual dialect detection and translation into canonical English pivot
language_agent = Agent(
    name="language_agent",
    description="Identifies language/dialect (e.g. Bundeli, Hinglish, Portuguese, Russian) and translates into canonical English pivot.",
    instruction=(
        "You are the JanSetu Multilingual Agent. Identify the source language, dialect, and whether code-mixing "
        "(e.g., Hinglish) is present. Provide an accurate English pivot translation that retains the full severity "
        "and emotional context of the citizen's complaint."
    ),
)

# 3. Classifier Agent: Maps to UN SDG unified taxonomy with structured Pydantic output
classifier_agent = Agent(
    name="classifier_agent",
    description="Classifies problem description into UN SDG taxonomy, urgency (1-5), and sentiment.",
    instruction=(
        "You are the JanSetu Classification Agent. Analyze the citizen's grievance. Classify it into one of the "
        "development taxonomy categories (water_sanitation, healthcare, transport_roads, education, electricity_energy, "
        "digital_connectivity), rate urgency from 1 to 5, and compute sentiment."
    ),
    tools=[taxonomy_classify_tool],
    output_schema=ClassificationResult,
)

# 4. Geo Agent: Resolves landmarks and villages to sovereign administrative units
geo_agent = Agent(
    name="geo_agent",
    description="Resolves village, landmark and ward mentions to administrative unit boundaries and coordinates.",
    instruction=(
        "You are the JanSetu Geo-Enrichment Agent. Resolve the location mentioned in the citizen's request "
        "to the exact administrative unit, state, country, and geo-coordinates."
    ),
    tools=[geo_resolve_tool],
)

# 5. Analyst Agent: Computes Demand-vs-Supply Gap and Priority Scores
analyst_agent = Agent(
    name="analyst_agent",
    description="Computes mathematical Gap Score and Priority Score using infrastructure supply and budget data.",
    instruction=(
        "You are the JanSetu Data Analyst Agent. Use the compute_gap_and_priority_tool to compare the citizen's "
        "demand signal against existing infrastructure supply indices and unspent public budget allocations. "
        "Provide a clear, defensible scoring breakdown."
    ),
    tools=[compute_gap_and_priority_tool],
)

# 6. Policy Drafting Agent: Synthesizes evidence-backed project recommendations
policy_agent = Agent(
    name="policy_drafting_agent",
    description="Drafts actionable project investment recommendations for policymakers.",
    instruction=(
        "You are the JanSetu Policy Drafting Agent. Turn the citizen demand signal and gap analysis into an "
        "actionable, cost-estimated project recommendation card with clear deliverables and risk mitigations."
    ),
    output_schema=RecommendationBrief,
)

# 7. Critic / Bias Auditor Agent: Checks for digital-divide bias and feasibility
critic_agent = Agent(
    name="critic_agent",
    description="Audits recommendations for equity, digital-divide bias, and administrative feasibility.",
    instruction=(
        "You are the JanSetu Critic and Bias Auditor Agent. Verify that digitally active groups are not unfairly "
        "favored over silent rural populations. Ensure equity weights are applied and approve or suggest revisions."
    ),
    tools=[audit_bias_and_equity_tool],
    output_schema=CritiqueReport,
)

# 8. Citizen Feedback Agent: Closes the loop by notifying citizens in their mother tongue
citizen_feedback_agent = Agent(
    name="citizen_feedback_agent",
    description="Generates warm, empathetic status updates in the citizen's native language.",
    instruction=(
        "You are the JanSetu Citizen Feedback Agent. Compose a clear, respectful notification to the citizen "
        "in their original language explaining how their voice has been recorded and linked to a project priority."
    ),
    output_schema=CitizenFeedbackResponse,
)

# Root Orchestrator Agent uniting all agents
root_agent = Agent(
    name="jansetu_orchestrator",
    model="gemini-3.5-flash",
    description="JanSetu Master Orchestrator: Citizen-to-Policy Intelligence for BRICS.",
    instruction=(
        "You are the root orchestrator of JanSetu. You route citizen grievances through the understanding pipeline, "
        "fuse them with infrastructure data, compute gap and priority scores, generate audited policy recommendations, "
        "and close the loop back with the citizen."
    ),
    sub_agents=[
        intake_agent,
        language_agent,
        classifier_agent,
        geo_agent,
        analyst_agent,
        policy_agent,
        critic_agent,
        citizen_feedback_agent,
    ],
)
