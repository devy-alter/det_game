import json

from app.ai.judge.parser import parse_judge


def test_judge_parser_requires_no_reason_from_model():
    result = parse_judge(json.dumps({
        "detective_score": 2,
        "suspect_score": 6,
        "confidence_change": 0,
        "confession_progress_change": 0,
        "contradiction_found": False,
        "evidence_strength": "none",
        "pressure_level": "low",
        "facts_established": [],
        "likely_confession": False,
    }))
    assert result.reason


def test_judge_parser_extracts_fenced_json():
    result = parse_judge("```json\n{\"detective_score\": 5, \"suspect_score\": 5, \"confidence_change\": -2, \"confession_progress_change\": 1}\n```")
    assert result.confidence_change == -2
    assert result.reason
