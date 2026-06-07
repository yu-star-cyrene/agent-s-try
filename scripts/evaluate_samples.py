"""Batch evaluation script for parcel precheck samples.

Usage:
    python scripts/evaluate_samples.py
    python scripts/evaluate_samples.py --sample-path data/samples/sample_set.json
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.types import InspectionRequest  # noqa: E402
from src.main import InspectionPipeline, build_default_pipeline  # noqa: E402
from src.modules.evaluation.metrics import field_completeness  # noqa: E402


def load_samples(sample_path: Path) -> list[dict[str, Any]]:
    payload = json.loads(sample_path.read_text(encoding="utf-8"))
    samples = payload.get("samples", [])
    if not isinstance(samples, list):
        raise ValueError("sample_set.json 中的 samples 必须是数组。")
    return samples


def make_request(sample: dict[str, Any]) -> InspectionRequest:
    rules = sample.get("rules", [])
    if not isinstance(rules, list):
        rules = []

    metadata = sample.get("metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}

    return InspectionRequest(
        parcel_id=str(sample.get("parcel_id", "")),
        image_path=str(sample.get("image_path", "")),
        text_description=str(sample.get("text_description", "")),
        land_type=str(sample.get("land_type", "")),
        rules=rules,
        metadata=metadata,
    )


def safe_set(value: Any) -> set[str]:
    if isinstance(value, list):
        return {str(item) for item in value}
    if value:
        return {str(value)}
    return set()


def compare_one(sample: dict[str, Any], prediction: dict[str, Any]) -> dict[str, Any]:
    expected = sample.get("expected_result", {})
    expected_rules = safe_set(expected.get("rule_hits", sample.get("applied_rule_ids", [])))
    predicted_rules = safe_set(prediction.get("rule_hits", []))

    if expected_rules:
        rule_any = bool(predicted_rules & expected_rules)
        rule_recall = len(predicted_rules & expected_rules) / len(expected_rules)
    else:
        rule_any = not predicted_rules
        rule_recall = 1.0 if not predicted_rules else 0.0

    return {
        "sample_id": sample.get("sample_id"),
        "parcel_id": sample.get("parcel_id"),
        "expected": expected,
        "prediction": prediction,
        "checks": {
            "is_abnormal_match": prediction.get("is_abnormal") == expected.get("is_abnormal"),
            "issue_type_match": prediction.get("issue_type") == expected.get("issue_type"),
            "requires_manual_review_match": prediction.get("requires_manual_review")
            == expected.get("requires_manual_review"),
            "rule_hits_exact_match": predicted_rules == expected_rules,
            "rule_hits_any_match": rule_any,
            "rule_hits_recall": rule_recall,
            "field_completeness": prediction.get("field_completeness", 0.0),
        },
    }


def average(items: list[float]) -> float:
    return round(sum(items) / len(items), 4) if items else 0.0


def build_summary(details: list[dict[str, Any]]) -> dict[str, Any]:
    checks = [item["checks"] for item in details]
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "sample_count": len(details),
        "metrics": {
            "is_abnormal_accuracy": average([float(c["is_abnormal_match"]) for c in checks]),
            "issue_type_accuracy": average([float(c["issue_type_match"]) for c in checks]),
            "requires_manual_review_accuracy": average(
                [float(c["requires_manual_review_match"]) for c in checks]
            ),
            "rule_hits_exact_accuracy": average([float(c["rule_hits_exact_match"]) for c in checks]),
            "rule_hits_any_accuracy": average([float(c["rule_hits_any_match"]) for c in checks]),
            "rule_hits_avg_recall": average([float(c["rule_hits_recall"]) for c in checks]),
            "avg_field_completeness": average([float(c["field_completeness"]) for c in checks]),
        },
        "failed_samples": [
            {
                "sample_id": item["sample_id"],
                "parcel_id": item["parcel_id"],
                "failed_checks": [
                    key
                    for key, value in item["checks"].items()
                    if isinstance(value, bool) and not value
                ],
                "expected_issue_type": item["expected"].get("issue_type"),
                "predicted_issue_type": item["prediction"].get("issue_type"),
                "expected_rules": item["expected"].get("rule_hits", []),
                "predicted_rules": item["prediction"].get("rule_hits", []),
            }
            for item in details
            if not all(value for value in item["checks"].values() if isinstance(value, bool))
        ],
    }


def write_csv(details: list[dict[str, Any]], csv_path: Path) -> None:
    fieldnames = [
        "sample_id",
        "parcel_id",
        "expected_is_abnormal",
        "predicted_is_abnormal",
        "is_abnormal_match",
        "expected_issue_type",
        "predicted_issue_type",
        "issue_type_match",
        "expected_review",
        "predicted_review",
        "requires_manual_review_match",
        "expected_rule_hits",
        "predicted_rule_hits",
        "rule_hits_exact_match",
        "rule_hits_any_match",
        "field_completeness",
    ]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in details:
            expected = item["expected"]
            prediction = item["prediction"]
            checks = item["checks"]
            writer.writerow(
                {
                    "sample_id": item["sample_id"],
                    "parcel_id": item["parcel_id"],
                    "expected_is_abnormal": expected.get("is_abnormal"),
                    "predicted_is_abnormal": prediction.get("is_abnormal"),
                    "is_abnormal_match": checks["is_abnormal_match"],
                    "expected_issue_type": expected.get("issue_type"),
                    "predicted_issue_type": prediction.get("issue_type"),
                    "issue_type_match": checks["issue_type_match"],
                    "expected_review": expected.get("requires_manual_review"),
                    "predicted_review": prediction.get("requires_manual_review"),
                    "requires_manual_review_match": checks["requires_manual_review_match"],
                    "expected_rule_hits": "|".join(expected.get("rule_hits", [])),
                    "predicted_rule_hits": "|".join(prediction.get("rule_hits", [])),
                    "rule_hits_exact_match": checks["rule_hits_exact_match"],
                    "rule_hits_any_match": checks["rule_hits_any_match"],
                    "field_completeness": checks["field_completeness"],
                }
            )


def run_evaluation(
    sample_path: Path,
    output_dir: Path,
    rule_path: Path | None = None,
) -> dict[str, Any]:
    samples = load_samples(sample_path)
    pipeline = InspectionPipeline(rule_path=rule_path) if rule_path else build_default_pipeline()

    details: list[dict[str, Any]] = []
    for sample in samples:
        request = make_request(sample)
        result = pipeline.run(request)
        prediction = result.to_dict()
        prediction["field_completeness"] = field_completeness(result)
        details.append(compare_one(sample, prediction))

    summary = build_summary(details)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "evaluation_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "evaluation_details.json").write_text(
        json.dumps(details, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_csv(details, output_dir / "evaluation_details.csv")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="批量评测国土图斑预检样本。")
    parser.add_argument("--sample-path", default="data/samples/sample_set.json")
    parser.add_argument("--rule-path", default="data/rules/rule_template.json")
    parser.add_argument("--output-dir", default="outputs/reports")
    args = parser.parse_args()

    sample_path = (PROJECT_ROOT / args.sample_path).resolve()
    rule_path = (PROJECT_ROOT / args.rule_path).resolve()
    output_dir = (PROJECT_ROOT / args.output_dir).resolve()

    summary = run_evaluation(
        sample_path=sample_path,
        rule_path=rule_path,
        output_dir=output_dir,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\n评测结果已保存到: {output_dir}")


if __name__ == "__main__":
    main()
