import json
import unittest
from pathlib import Path

from scripts.evaluate_samples import run_evaluation


class EvaluationSmokeTest(unittest.TestCase):
    def test_sample_set_can_generate_summary(self) -> None:
        project_root = Path(__file__).resolve().parents[2]
        output_dir = project_root / "tmp_test_dir" / "evaluation_smoke"

        summary = run_evaluation(
            sample_path=project_root / "data" / "samples" / "sample_set.json",
            rule_path=project_root / "data" / "rules" / "rule_template.json",
            output_dir=output_dir,
        )

        self.assertEqual(summary["sample_count"], 5)
        self.assertIn("metrics", summary)
        self.assertTrue((output_dir / "evaluation_summary.json").exists())
        payload = json.loads((output_dir / "evaluation_summary.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["sample_count"], 5)


if __name__ == "__main__":
    unittest.main()
