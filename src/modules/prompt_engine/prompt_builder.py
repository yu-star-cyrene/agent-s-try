from src.core.types import InspectionRequest


def build_inspection_prompt(request: InspectionRequest, rules: list[str]) -> str:
    rule_block = "\n".join(f"- {rule}" for rule in rules)
    return f"""你是一个国土图斑审查预检助手。

请结合地块说明、图像线索和审查规则，输出结构化判断。

地块编号: {request.parcel_id}
图像路径: {request.image_path}
地类信息: {request.land_type or "未提供"}
文字说明: {request.text_description}

审查规则:
{rule_block}

请返回 JSON，字段包括:
- is_abnormal
- issue_type
- reason
- confidence
- requires_manual_review
- evidence
"""
