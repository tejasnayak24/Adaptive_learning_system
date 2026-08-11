"""FastAPI router exposing the RL recommendation endpoint.

This router is a thin HTTP boundary in front of ``RLService``. It
validates nothing itself beyond what ``RecommendationRequest`` already
enforces, builds no RL engine types, and contains no RL logic -- it only
forwards a validated request to ``RLService`` and shapes the resulting
``Recommendation`` into the JSON response.
"""

from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

from app.schemas.rl import RecommendationRequest
from app.services.rl_service import RLService

# Path to the trained Q-table, computed relative to this file's own
# location rather than the process's current working directory, so it
# resolves correctly no matter where uvicorn is started from.
# backend/app/routers/rl.py -> parents[3] is the project root.
_Q_TABLE_PATH = Path(__file__).resolve().parents[3] / "rl_engine" / "q_table.json"

# Instantiated once, when this module is imported, so the trained agent
# is loaded a single time and reused for every request rather than being
# reloaded or retrained per call.
_rl_service = RLService(_Q_TABLE_PATH)

router = APIRouter(
    prefix="/rl",
    tags=["Reinforcement Learning"],
)


@router.post("/recommend")
def recommend(request: RecommendationRequest) -> dict[str, Any]:
    """Return the RL agent's recommendation for a student's current state.

    Args:
        request: The validated student state data, already checked by
            ``RecommendationRequest``.

    Returns:
        A JSON-serializable mapping with exactly three keys:
            action: The recommended action's name (e.g. "NEXT_LESSON").
            confidence: The policy's confidence in the recommendation.
            explanation: A human-readable justification for it.

    Raises:
        HTTPException: With status 422 if ``RLService`` rejects the
            request data as invalid, or with status 500 if obtaining a
            recommendation fails for any other reason.
    """
    try:
        recommendation = _rl_service.get_recommendation(request.model_dump())
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="Failed to generate a recommendation."
        ) from exc

    return {
        "action": recommendation.action.name,
        "confidence": recommendation.confidence,
        "explanation": recommendation.explanation,
    }