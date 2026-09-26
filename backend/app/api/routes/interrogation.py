import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.ai.providers.base import ProviderError
from app.config.settings import settings
from app.game.engine import engine
from app.schemas.interrogation import QuestionRequest, TurnResponse
from app.utils.security import sanitize_question

router = APIRouter(prefix="/game", tags=["interrogation"])


def sse(payload: dict) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


@router.post("/{game_id}/question", response_model=None)
async def question(game_id: str, req: QuestionRequest):
    question_text = sanitize_question(req.question)
    try:
        state = engine.get(game_id)
    except KeyError:
        raise HTTPException(404, "Game not found")
    if state.status != "active":
        raise HTTPException(409, "Game is already finished")
    if state.question_count >= settings.max_questions:
        raise HTTPException(409, "No questions remaining")

    async def stream():
        try:
            async for event in engine.ask_stream(game_id, question_text):
                yield sse(event)
        except ProviderError as exc:
            yield sse({"type": "error", "message": str(exc)})
        except ValueError as exc:
            yield sse({"type": "error", "message": str(exc)})
        except Exception as exc:
            if settings.debug:
                yield sse({"type": "error", "message": f"Interrogation failed: {exc}"})
            else:
                yield sse({"type": "error", "message": "Interrogation failed"})

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
