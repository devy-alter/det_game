from uuid import uuid4
from app.game.state import GameState
from app.game.confidence import apply_confidence, apply_progress
from app.game.victory import finalize_after_turn
from app.cases.loader import loader
from app.ai.suspect.agent import suspect_agent
from app.ai.suspect.rules import enforce_word_limit
from app.ai.judge.agent import judge_agent
from app.config.settings import settings
from app.schemas.judge import JudgeResult

GAMES: dict[str, GameState] = {}

class GameEngine:
    def start(self, case_id: str):
        case = loader.load(case_id)
        game_id = uuid4().hex
        state = GameState(game_id=game_id, case_id=case_id, confidence=settings.starting_confidence, confession_progress=settings.starting_confession_progress)
        GAMES[game_id] = state
        return case, state

    def get(self, game_id: str):
        if game_id not in GAMES:
            raise KeyError(game_id)
        return GAMES[game_id]

    async def ask_stream(self, game_id: str, question: str):
        state = self.get(game_id)
        if state.status != "active": raise ValueError("Game is already finished")
        if state.question_count >= settings.max_questions:
            state.status = "lost"; raise ValueError("No questions remaining")

        case = loader.load(state.case_id)
        number = state.question_count + 1
        yield {"type":"suspect_start","question_number":number,"detective_question":question}

        collected=[]
        if hasattr(suspect_agent, "respond_stream"):
            async for chunk in suspect_agent.respond_stream(case,state.history,question,state.confidence,state.confession_progress):
                collected.append(chunk)
                yield {"type":"suspect_chunk","question_number":number,"text":chunk}
        else:
            text = await suspect_agent.respond(case,state.history,question,state.confidence,state.confession_progress)
            collected.append(text)
            yield {"type":"suspect_chunk","question_number":number,"text":text}

        suspect = enforce_word_limit("".join(collected).strip())
        yield {"type":"suspect_done","question_number":number,"suspect_response":suspect}

        judge = await judge_agent.evaluate(case,state.history,question,suspect,state.confidence,state.confession_progress)
        state.question_count += 1
        state.confidence = apply_confidence(state.confidence, judge.confidence_change)
        state.confession_progress = apply_progress(state.confession_progress, judge.confession_progress_change)
        for fact in judge.facts_established:
            if fact in case.required_confession_facts and fact not in state.discovered_facts: state.discovered_facts.append(fact)

        state.history.append({
            "question_number":number,
            "detective_question":question,
            "suspect_response":suspect,
            "judge":judge.model_dump(),
            "judge_reason":judge.reason,
            "room_pressure":judge.pressure_level,
            "confidence_after":state.confidence,
            "progress_after":state.confession_progress,
        })
        finalize_after_turn(case,state,judge)

        yield {"type":"state","question_number":number,"questions_remaining":max(0,settings.max_questions-state.question_count),"confidence":state.confidence,"confession_progress":state.confession_progress,"room_pressure":judge.pressure_level,"status":state.status,"discovered_facts":state.discovered_facts}

    async def ask(self, game_id: str, question: str):
        async for _ in self.ask_stream(game_id,question): pass
        state=self.get(game_id); case=loader.load(state.case_id)
        return case,state,JudgeResult.model_validate(state.history[-1]["judge"])

engine=GameEngine()
