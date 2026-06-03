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
        self.assertGreaterEqual(field_completeness(result), 1.0)


if __name__ == "__main__":
    unittest.main()
