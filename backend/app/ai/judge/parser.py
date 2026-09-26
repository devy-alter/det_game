import json
import re

from app.schemas.judge import JudgeResult


def _extract_json_object(text: str) -> str:
    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned).strip()

    # Some models prepend a sentence despite being asked for JSON only.
    # Extract the outermost JSON object without trying to repair arbitrary prose.
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start >= 0 and end > start:
        return cleaned[start:end + 1]

    return cleaned


def parse_judge(text: str) -> JudgeResult:
    cleaned = _extract_json_object(text)
    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Judge AI did not return valid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("Judge AI JSON must be an object")

    # Be tolerant of models occasionally omitting optional-looking fields.
    payload.setdefault(
        "reason",
        "The judge model returned no detailed explanation for this exchange.",
    )
    payload.setdefault("facts_established", [])
    payload.setdefault("contradiction_found", False)
    payload.setdefault("evidence_strength", "none")
    payload.setdefault("pressure_level", "low")
    payload.setdefault("likely_confession", False)

    return JudgeResult.model_validate(payload)
