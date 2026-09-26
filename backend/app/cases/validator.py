from app.schemas.case import Case

def validate_case(case: Case):
    if not case.required_confession_facts:
        raise ValueError("Case must have at least one confession fact")
    if len(case.evidence) == 0:
        raise ValueError("Case must contain evidence")
    return True
