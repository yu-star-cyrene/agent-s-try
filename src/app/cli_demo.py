import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from src.core.types import InspectionRequest
from src.main import build_default_pipeline


def load_demo_request(sample_path: Path) -> InspectionRequest:
    payload = json.loads(sample_path.read_text(encoding="utf-8"))
    return InspectionRequest(**payload)


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    sample_path = project_root / "data" / "samples" / "request_example.json"
    request = load_demo_request(sample_path)
    pipeline = build_default_pipeline()
    result = pipeline.run(request)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
