import json

from src.core.types import InspectionResult


def _as_string_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if value:
        return [str(value)]
    return []


def _as_confidence(value) -> float:
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, min(1.0, confidence))


def parse_model_output(parcel_id: str, raw_output: str) -> InspectionResult:
    try:
        payload = json.loads(raw_output)
    except json.JSONDecodeError:
        payload = {
            "is_abnormal": False,
            "issue_type": "解析失败",
            "reason": "模型输出不是合法 JSON，建议人工复核。",
            "confidence": 0.0,
            "requires_manual_review": True,
            "evidence": [],
            "rule_hits": [],
        }

    return InspectionResult(
        parcel_id=parcel_id,
        is_abnormal=bool(payload.get("is_abnormal", False)),
        issue_type=str(payload.get("issue_type", "未知")),
        reason=str(payload.get("reason", "")),
        confidence=_as_confidence(payload.get("confidence", 0.0)),
        requires_manual_review=bool(payload.get("requires_manual_review", True)),
        evidence=_as_string_list(payload.get("evidence", [])),
        rule_hits=_as_string_list(payload.get("rule_hits", [])),
        raw_output=raw_output,
    )
