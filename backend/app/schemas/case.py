from typing import Literal

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    id: str
    name: str
    description: str
    strength: int = Field(ge=1, le=10)
    public: bool = True


class Crime(BaseModel):
    type: str
    victim: str
    location: str
    time: str


class SuspectProfile(BaseModel):
    name: str
    age: int
    occupation: str
    personality: str = "composed"


class Case(BaseModel):
    id: str
    title: str
    description: str
    difficulty: Literal["easy", "medium", "hard"]
    crime: Crime
    truth: dict
    suspect: SuspectProfile
    alibi: dict
    evidence: list[Evidence]
    required_confession_facts: list[str]
    opening_statement: str


class PublicCase(BaseModel):
    id: str
    title: str
    description: str
    difficulty: Literal["easy", "medium", "hard"]
    crime: Crime
    suspect: SuspectProfile
    alibi_claim: str
    evidence: list[Evidence]
    opening_statement: str
