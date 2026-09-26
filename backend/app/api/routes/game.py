from fastapi import APIRouter, HTTPException
from app.game.engine import engine
from app.schemas.game import GameStateResponse
from app.schemas.interrogation import StartGameRequest

router = APIRouter(prefix="/game", tags=["game"])

def public_history(state):
    result = []
    for item in state.history:
        result.append({
            "question_number": item.get("question_number"),
            "detective_question": item.get("detective_question", ""),
            "suspect_response": item.get("suspect_response", ""),
            "confidence_after": item.get("confidence_after"),
            "progress_after": item.get("progress_after"),
            "room_pressure": item.get("room_pressure", "low"),
        })
    return result

def to_response(state):
    return GameStateResponse(
        game_id=state.game_id,
        case_id=state.case_id,
        question_count=state.question_count,
        questions_remaining=max(0, 10-state.question_count),
        confidence=state.confidence,
        confession_progress=state.confession_progress,
        status=state.status,
        discovered_facts=state.discovered_facts,
        history=public_history(state),
    )

@router.post("/start", response_model=GameStateResponse)
def start_game(req: StartGameRequest):
    try:
        case, state = engine.start(req.case_id)
    except FileNotFoundError:
        raise HTTPException(404, "Case not found")
    return to_response(state)

@router.get("/{game_id}", response_model=GameStateResponse)
def get_game(game_id: str):
    try:
        state = engine.get(game_id)
    except KeyError:
        raise HTTPException(404, "Game not found")
    return to_response(state)

@router.post("/{game_id}/restart", response_model=GameStateResponse)
def restart(game_id: str):
    try:
        old = engine.get(game_id)
        case, state = engine.start(old.case_id)
    except KeyError:
        raise HTTPException(404, "Game not found")
    return to_response(state)
