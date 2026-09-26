from app.ai.ai_manager import ai_manager
from app.ai.suspect.parser import parse_suspect_response
from app.ai.suspect.prompt import build_suspect_messages
from app.ai.suspect.rules import enforce_word_limit
from app.config.settings import settings

class SuspectAgent:
    async def respond(self, case, history, question, confidence, confession_progress):
        messages = build_suspect_messages(case, history, question, confidence, confession_progress)
        chunks = []
        async for chunk in ai_manager.stream("suspect", messages, temperature=settings.suspect_ai_temperature):
            chunks.append(chunk)
        return enforce_word_limit(parse_suspect_response("".join(chunks)))

    async def respond_stream(self, case, history, question, confidence, confession_progress):
        messages = build_suspect_messages(case, history, question, confidence, confession_progress)
        full = []
        async for chunk in ai_manager.stream("suspect", messages, temperature=settings.suspect_ai_temperature):
            full.append(chunk)
            yield chunk
        final = enforce_word_limit(parse_suspect_response("".join(full)))
        if final != "".join(full):
            yield ""  # finalization is enforced before persistence

suspect_agent = SuspectAgent()
