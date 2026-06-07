import json
from typing import Any

from src.core.types import InspectionRequest


def _join_items(value: Any) -> str:
    if isinstance(value, list):
        return "；".join(str(item) for item in value if item)
    if value:
        return str(value)
    return "未提供"


def _format_rule(index: int, rule: Any) -> str:
    if isinstance(rule, str):
        return f"{index}. 临时补充规则：{rule}"

    output = rule.get("output", {})
    output_text = ", ".join(
        f"{key}={value}" for key, value in output.items()
    ) or "未提供"

    return "\n".join(
        [
            f"{index}. 规则ID: {rule.get('id', 'UNKNOWN')} | 名称: {rule.get('title', '未命名规则')}",
            f"   类别: {rule.get('category', '未分类')} | 风险等级: {rule.get('severity', '未提供')} | 优先级: {rule.get('priority', 0)}",
            f"   适用地类: {_join_items(rule.get('applies_to', []))}",
            f"   触发条件: {_join_items(rule.get('trigger_conditions', []))}",
            f"   所需证据: {_join_items(rule.get('required_evidence', []))}",
            f"   判断逻辑: {rule.get('decision_logic') or rule.get('description', '未提供')}",
            f"   目标输出: {output_text}",
        ]
    )


def build_inspection_prompt(request: InspectionRequest, rules: list[Any]) -> str:
    rule_block = "\n\n".join(
        _format_rule(index, rule)
        for index, rule in enumerate(rules, start=1)
    ) or "未提供审查规则"
    metadata_block = json.dumps(request.metadata, ensure_ascii=False, indent=2)
    return f"""你是一个国土图斑审查预检助手。

任务目标：结合地块说明、图像线索、元数据和审查规则，对国土图斑进行机器预审。

判断原则：
1. 必须优先依据规则库判断，不要自由扩展无依据结论。
2. 若证据不足、图像遮挡、时间地点异常或规则冲突，应建议人工复核。
3. 若多条规则同时命中，优先采用 priority 更高、severity 更高的规则。
4. 输出必须能追溯到规则ID，命中规则写入 rule_hits。

地块编号: {request.parcel_id}
图像路径: {request.image_path}
地类信息: {request.land_type or "未提供"}
文字说明: {request.text_description}
元数据:
{metadata_block}

审查规则:
{rule_block}

请只返回合法 JSON，不要输出 Markdown，不要额外解释。字段必须包括:
{{
  "is_abnormal": true/false,
  "issue_type": "异常类型或未发现明显异常",
  "reason": "结合图像、文本和规则给出的判断理由",
  "confidence": 0.0到1.0之间的小数,
  "requires_manual_review": true/false,
  "evidence": ["证据1", "证据2"],
  "rule_hits": ["R001"]
}}
"""
