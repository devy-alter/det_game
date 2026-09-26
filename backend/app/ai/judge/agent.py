from app.ai.ai_manager import ai_manager
from app.ai.judge.parser import parse_judge
from app.ai.judge.prompt import build_judge_messages
from app.ai.judge.rules import clamp_judge_result
from app.config.settings import settings
from app.schemas.case import Case
from app.schemas.judge import JudgeResult


class JudgeAgent:
    async def evaluate(
        self,
        case: Case,
        history: list[dict],
        question: str,
        suspect_response: str,
        confidence: int,
        progress: int,
    ) -> JudgeResult:
        messages = build_judge_messages(
            case, history, question, suspect_response, confidence, progress
        )
        raw = await ai_manager.chat(
            "judge",
            messages,
            json_mode=True,
            temperature=settings.judge_ai_temperature,
        )
        return clamp_judge_result(parse_judge(raw))


judge_agent = JudgeAgent()
