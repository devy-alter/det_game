def sanitize_question(value: str) -> str:
    return " ".join(value.strip().split())[:1000]
