def apply_confidence(current: int, delta: int) -> int:
    return max(0, min(100, current + delta))

def apply_progress(current: int, delta: int) -> int:
    return max(0, min(100, current + delta))
