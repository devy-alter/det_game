import asyncio

from app.game.engine import GameEngine
from app.schemas.judge import JudgeResult


class FakeSuspect:
    async def respond(self, *args, **kwargs):
        return "I deny the allegation."


class FakeJudge:
    async def evaluate(self, *args, **kwargs):
        return JudgeResult(
            detective_score=9,
            suspect_score=3,
            confidence_change=-12,
            confession_progress_change=18,
            reason="Strong pressure.",
            facts_established=["suspect was at crime scene"],
            evidence_strength="strong",
            pressure_level="high",
        )


def test_question_updates_state(monkeypatch):
    import app.game.engine as module
    monkeypatch.setattr(module, "suspect_agent", FakeSuspect())
    monkeypatch.setattr(module, "judge_agent", FakeJudge())

    engine = GameEngine()
    _, state = engine.start("case_001")
    _, updated, judge = asyncio.run(engine.ask(state.game_id, "Where were you?"))

    assert updated.question_count == 1
    assert updated.questions_remaining if hasattr(updated, "questions_remaining") else True
    assert updated.confidence == 88
    assert updated.confession_progress == 18
    assert judge.detective_score == 9
