import json

from src.core.types import InspectionResult


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
        }

    return InspectionResult(
        parcel_id=parcel_id,
        is_abnormal=bool(payload.get("is_abnormal", False)),
        issue_type=str(payload.get("issue_type", "未知")),
        reason=str(payload.get("reason", "")),
        confidence=float(payload.get("confidence", 0.0)),
        requires_manual_review=bool(payload.get("requires_manual_review", True)),
        evidence=list(payload.get("evidence", [])),
        raw_output=raw_output,
    )
