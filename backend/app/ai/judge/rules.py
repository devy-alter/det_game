def clamp_judge_result(result):
    result.confidence_change = max(-25, min(10, int(result.confidence_change)))
    result.confession_progress_change = max(
        -5, min(25, int(result.confession_progress_change))
    )
    result.detective_score = max(0, min(10, int(result.detective_score)))
    result.suspect_score = max(0, min(10, int(result.suspect_score)))
    return result
