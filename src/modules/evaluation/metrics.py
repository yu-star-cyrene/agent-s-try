from src.core.types import InspectionResult


def field_completeness(result: InspectionResult) -> float:
    required_fields = [
        result.issue_type,
        result.reason,
        result.evidence,
    ]
    filled = sum(1 for item in required_fields if item)
    return filled / len(required_fields)


def flag_accuracy(expected: list[bool], predicted: list[bool]) -> float:
    if not expected or len(expected) != len(predicted):
        return 0.0
    correct = sum(1 for e, p in zip(expected, predicted) if e == p)
    return correct / len(expected)
