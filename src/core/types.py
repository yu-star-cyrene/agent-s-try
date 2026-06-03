from dataclasses import dataclass, field
from typing import Any


@dataclass
class InspectionRequest:
    parcel_id: str
    image_path: str
    text_description: str
    land_type: str = ""
    rules: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class InspectionResult:
    parcel_id: str
    is_abnormal: bool
    issue_type: str
    reason: str
    confidence: float
    requires_manual_review: bool
    evidence: list[str] = field(default_factory=list)
    raw_output: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "parcel_id": self.parcel_id,
            "is_abnormal": self.is_abnormal,
            "issue_type": self.issue_type,
            "reason": self.reason,
            "confidence": self.confidence,
            "requires_manual_review": self.requires_manual_review,
            "evidence": self.evidence,
            "raw_output": self.raw_output,
        }
