from fastapi import APIRouter, HTTPException

from app.cases.loader import loader
from app.schemas.case import Case, PublicCase

router = APIRouter(prefix="/cases", tags=["cases"])


def to_public(case: Case) -> PublicCase:
    return PublicCase(
        id=case.id,
        title=case.title,
        description=case.description,
        difficulty=case.difficulty,
        crime=case.crime,
        suspect=case.suspect,
        alibi_claim=case.alibi.get("claim", ""),
        evidence=[e for e in case.evidence if e.public],
        opening_statement=case.opening_statement,
    )


@router.get("", response_model=list[PublicCase])
def list_cases():
    return [to_public(case) for case in loader.list_cases()]


@router.get("/{case_id}", response_model=PublicCase)
def get_case(case_id: str):
    try:
        return to_public(loader.load(case_id))
    except FileNotFoundError:
        raise HTTPException(404, "Case not found")
