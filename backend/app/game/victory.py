from app.config.settings import settings
from app.schemas.case import Case


def confession_ready(case: Case, state, judge):
    required = len(case.required_confession_facts)
    covered = len(set(state.discovered_facts))
    return judge.likely_confession or (
        state.confession_progress >= 88
        and state.confidence <= 24
        and covered >= max(1, required - 1)
    )


def finalize_after_turn(case: Case, state, judge):
    if confession_ready(case, state, judge):
        state.status = "won"
    elif state.question_count >= settings.max_questions:
        state.status = "lost"
    return state
