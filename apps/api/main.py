"""JanSetu Master FastAPI Gateway.

Exposes:
- Citizen intake channels (WhatsApp, IVR, Telegram, Web)
- Google ADK Multi-Agent Pipeline
- Analytics & Demand-vs-Supply Hotspots
- Recommendation Review & Audit Trail
- What-If Policy Simulation
- Conversational Policymaker Copilot
- Impact Loop Tracker
- Sovereign BRICS Federation Layer
- Web Command Centre Dashboard & PWA Portal
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from apps.api.routers import (
    intake,
    analytics,
    recommendations,
    simulation,
    copilot,
    impact,
    federation,
)

app = FastAPI(
    title="JanSetu API — Citizen-to-Policy Intelligence for BRICS",
    description="Sovereign Digital Public Good closing the loop from citizen voice to national budget line.",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(intake.router)
app.include_router(analytics.router)
app.include_router(recommendations.router)
app.include_router(simulation.router)
app.include_router(copilot.router)
app.include_router(impact.router)
app.include_router(federation.router)

# Mount static frontend
static_dir = Path(__file__).resolve().parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", include_in_schema=False)
def serve_dashboard():
    """Serves the JanSetu Web Command Centre & Citizen Intake Portal."""
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "JanSetu Sovereign API is live. Visit /docs for OpenAPI specs."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apps.api.main:app", host="0.0.0.0", port=8000, reload=True)
