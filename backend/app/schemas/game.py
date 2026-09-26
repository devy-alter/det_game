from pydantic import BaseModel

class GameStateResponse(BaseModel):
    game_id: str
    case_id: str
    question_count: int
    questions_remaining: int
    confidence: int
    confession_progress: int
    status: str
    discovered_facts: list[str]
    history: list[dict]
