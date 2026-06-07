import json
import unittest
from pathlib import Path

from src.core.types import InspectionRequest
from src.main import build_default_pipeline
from src.modules.evaluation.metrics import field_completeness


class PipelineSmokeTest(unittest.TestCase):
    def test_demo_request_can_run(self) -> None:
        project_root = Path(__file__).resolve().parents[2]
        sample_path = project_root / "data" / "samples" / "request_example.json"
        payload = json.loads(sample_path.read_text(encoding="utf-8"))
        request = InspectionRequest(**payload)

        pipeline = build_default_pipeline()
        result = pipeline.run(request)

        self.assertEqual(result.parcel_id, "FJ-2026-001")
        self.assertTrue(result.is_abnormal)
        self.assertIn("R002", result.rule_hits)
        self.assertGreaterEqual(field_completeness(result), 1.0)

    def test_rule_library_text_does_not_trigger_mock_by_itself(self) -> None:
        request = InspectionRequest(
            parcel_id="FJ-2026-NORMAL",
            image_path="data/raw/normal.jpg",
            text_description="现场为正常厂房及配套道路，图文一致。",
            land_type="建设用地",
            metadata={"source": "smoke"},
        )

        pipeline = build_default_pipeline()
        result = pipeline.run(request)

        self.assertFalse(result.is_abnormal)
        self.assertFalse(result.requires_manual_review)
        self.assertEqual(result.rule_hits, [])


if __name__ == "__main__":
    unittest.main()
