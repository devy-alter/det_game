def enforce_word_limit(text: str, limit: int = 100) -> str:
    words = text.strip().split()
    if len(words) <= limit:
        return text.strip()
    return " ".join(words[:limit]).rstrip(".,;:") + "…"
