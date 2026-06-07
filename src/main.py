from pathlib import Path

from src.core.types import InspectionRequest, InspectionResult
from src.modules.model_gateway.base import ModelClient
from src.modules.model_gateway.mock_client import MockModelClient
from src.modules.postprocess.parser import parse_model_output
from src.modules.prompt_engine.prompt_builder import build_inspection_prompt
from src.modules.rule_engine.rule_loader import list_enabled_rules, load_rule_bundle


class InspectionPipeline:
    def __init__(self, rule_path: str | Path, model_client: ModelClient | None = None) -> None:
        self.rule_bundle = load_rule_bundle(rule_path)
        self.model_client = model_client or MockModelClient()

    def run(self, request: InspectionRequest) -> InspectionResult:
        rules = list_enabled_rules(self.rule_bundle)
        rules.extend(request.rules)
        prompt = build_inspection_prompt(request=request, rules=rules)
        raw_output = self.model_client.inspect(prompt=prompt, image_path=request.image_path)
        return parse_model_output(parcel_id=request.parcel_id, raw_output=raw_output)


def build_default_pipeline() -> InspectionPipeline:
    project_root = Path(__file__).resolve().parents[1]
    rule_path = project_root / "data" / "rules" / "rule_template.json"
    return InspectionPipeline(rule_path=rule_path)
