def turn_quality(detective_score: int, suspect_score: int) -> str:
    gap = detective_score - suspect_score
    if gap >= 5: return "decisive_detective"
    if gap >= 2: return "detective_advantage"
    if gap <= -5: return "decisive_suspect"
    if gap <= -2: return "suspect_advantage"
    return "even"
