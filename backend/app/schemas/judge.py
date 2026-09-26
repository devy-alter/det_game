from pydantic import BaseModel, Field
from typing import Literal


class JudgeResult(BaseModel):
    detective_score: int = Field(ge=0, le=10)
    suspect_score: int = Field(ge=0, le=10)
    confidence_change: int = Field(ge=-25, le=10)
    confession_progress_change: int = Field(ge=-5, le=25)
    contradiction_found: bool = False
    evidence_strength: Literal["none", "weak", "medium", "strong"] = "none"
    pressure_level: Literal["low", "medium", "high", "critical"] = "low"
    facts_established: list[str] = Field(default_factory=list)
    reason: str = Field(default="No detailed judge explanation was returned by the model.")
    likely_confession: bool = False
