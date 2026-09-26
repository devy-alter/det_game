from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(min_length=2, max_length=1000)


class StartGameRequest(BaseModel):
    case_id: str


class TurnResponse(BaseModel):
    question_number: int
    questions_remaining: int
    detective_question: str
    suspect_response: str
    confidence: int
    room_pressure: str = "low"
    confession_progress: int
    status: str
    discovered_facts: list[str]
