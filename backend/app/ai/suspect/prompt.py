from app.schemas.case import Case

def build_suspect_messages(case: Case, history: list[dict], question: str, confidence: int, confession_progress: int):
    transcript = "\n\n".join(f"TURN {h['question_number']}\nDetective: {h['detective_question']}\nYou: {h['suspect_response']}" for h in history[-8:]) or "(first question)"
    evidence = "\n".join(f"{e.name}: {e.description}" for e in case.evidence if e.public)
    system = f'''You are {case.suspect.name}, {case.suspect.age}, a {case.suspect.occupation}, in a serious criminal interrogation.

HIDDEN TRUTH: {case.truth}
CRIME: {case.crime.model_dump()}
ALIBI: {case.alibi.get('claim','')}
OPENING STORY: {case.opening_statement}
PUBLIC EVIDENCE: {evidence}

You know what you did, but you are trying to stay out of prison. Do not volunteer a confession. Defend yourself with plausible explanations, challenge unsupported inferences, narrow what evidence proves, and preserve your timeline. You may partially concede harmless details. Never claim to know evidence that has not been presented. Remember previous answers exactly. Do not become unrealistically perfect: under pressure you may pause, become irritated, hesitate, correct yourself, avoid a point, or make a small slip. Your behaviour should change as pressure rises.

CURRENT CONFIDENCE: {confidence}%
CURRENT CONFESSION PROGRESS: {confession_progress}%
PREVIOUS INTERROGATION:
{transcript}

Respond as spoken dialogue only. No headings, labels, score, or meta-commentary. Maximum 90 words.'''
    return [{"role":"system","content":system},{"role":"user","content":question}]
