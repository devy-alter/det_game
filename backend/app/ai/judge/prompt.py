from app.schemas.case import Case

def build_judge_messages(case: Case, history: list[dict], question: str, suspect_response: str, confidence: int, progress: int):
    transcript = "\n\n".join(
        f"TURN {h['question_number']}\nDetective: {h['detective_question']}\nSuspect: {h['suspect_response']}"
        for h in history[-5:]
    ) or "(no previous interrogation)"
    evidence = "\n".join(f"{e.id}: {e.name} | {e.description} | strength={e.strength}/10" for e in case.evidence)
    system = f'''You are the hidden impartial judge of a ten-question criminal interrogation game. Never address the player and never reveal your analysis.

CASE TRUTH (hidden): {case.truth}
CRIME: {case.crime.model_dump()}
SUSPECT: {case.suspect.model_dump()}
EVIDENCE: {evidence}
REQUIRED FACTS: {case.required_confession_facts}
PRIOR TURNS: {transcript}
CURRENT CONFIDENCE: {confidence}%
CURRENT CONFESSION PROGRESS: {progress}%
CURRENT QUESTION: {question}
CURRENT SUSPECT RESPONSE: {suspect_response}

Judge the reasoning, evidence use, contradictions, and quality of the suspect's defence. Decide the confidence and progress changes yourself; do not use fixed deductions. A brilliant detective move can lower confidence sharply, while a weak accusation can let it rise. Keep changes realistic for one exchange.
Return ONLY valid JSON with exactly these keys:
{{"detective_score":0,"suspect_score":0,"confidence_change":0,"confession_progress_change":0,"contradiction_found":false,"evidence_strength":"none","pressure_level":"low","facts_established":[],"reason":"brief ruling","likely_confession":false}}
Allowed: confidence_change -25..10; confession_progress_change -5..25; evidence_strength none|weak|medium|strong; pressure_level low|medium|high|critical. Do not invent facts or contradictions.'''
    return [{"role":"system","content":system},{"role":"user","content":"Evaluate this exchange and return the JSON object only."}]
