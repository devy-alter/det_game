def ensure_nonempty(value: str):
    if not value.strip():
        raise ValueError("Value cannot be empty")
