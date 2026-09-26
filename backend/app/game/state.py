from dataclasses import dataclass, field

@dataclass
class GameState:
    game_id: str
    case_id: str
    question_count: int = 0
    confidence: int = 100
    confession_progress: int = 0
    status: str = "active"
    discovered_facts: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
