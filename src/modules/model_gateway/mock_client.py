import json

from src.modules.model_gateway.base import ModelClient


class MockModelClient(ModelClient):
    def inspect(self, prompt: str, image_path: str | None = None) -> str:
        prompt_text = prompt.lower()
        input_text = _extract_current_input(prompt_text)
        land_type_line = _extract_line(input_text, "地类信息:")

        is_farmland = "耕地" in land_type_line or "申报为耕地" in input_text
        is_forest = "林地" in land_type_line or "申报为林地" in input_text
        is_construction_land = "建设用地" in land_type_line
        has_building = _contains_any(input_text, ["建筑", "院落", "硬化地表"])
        has_forest_occupation = is_forest and _contains_any(input_text, ["硬化道路", "道路硬化", "施工", "堆料", "建筑结构"])
        has_authenticity_risk = _contains_any(input_text, ["时间戳异常", "时间异常", "旧图新用", "异地拍照", "位置不匹配", "场景与地块信息不匹配"])
        has_usage_risk = is_construction_land and _contains_any(input_text, ["荒置", "用途不符", "用途异常", "使用情况不一致"])
        has_text_conflict = _contains_any(input_text, ["图文不一致", "不一致", "冲突", "不匹配"])
        incomplete_evidence = _contains_any(input_text, ["角度有限", "证据不足", "遮挡", "只能看到", "无法完整", "死角", "漏拍"])

        result = _normal_result()

        if has_authenticity_risk:
            result = {
                "is_abnormal": True,
                "issue_type": "举证真实性风险",
                "reason": "当前样本存在时间、位置或场景不匹配线索，疑似旧图新用或异地拍照。",
                "confidence": 0.9,
                "requires_manual_review": True,
                "evidence": ["时间或场景信息异常", "举证真实性存疑"],
                "rule_hits": ["R004"],
            }
        elif has_building and is_farmland:
            result = {
                "is_abnormal": True,
                "issue_type": "耕地疑似建筑占用",
                "reason": "文本描述显示为耕地，但样本中包含疑似建筑物或硬化地表线索。",
                "confidence": 0.82,
                "requires_manual_review": True,
                "evidence": ["地块说明包含耕地信息", "样本描述包含疑似建筑物或硬化地表"],
                "rule_hits": ["R002"],
            }
        elif has_forest_occupation:
            result = {
                "is_abnormal": True,
                "issue_type": "林地疑似占用",
                "reason": "地块申报为林地，但样本中出现硬化道路、施工或堆料等非林地利用线索。",
                "confidence": 0.84,
                "requires_manual_review": True,
                "evidence": ["文本说明为林地", "样本描述包含硬化或施工线索"],
                "rule_hits": ["R005"],
            }
        elif has_usage_risk:
            result = {
                "is_abnormal": True,
                "issue_type": "建设用地用途异常",
                "reason": "建设用地申报用途与现场使用状态存在不一致线索。",
                "confidence": 0.72,
                "requires_manual_review": True,
                "evidence": ["建设用地用途存在异常线索"],
                "rule_hits": ["R006"],
            }
        elif has_text_conflict:
            result = {
                "is_abnormal": True,
                "issue_type": "图文不一致",
                "reason": "样本描述中出现图像、文本或地块信息不一致线索。",
                "confidence": 0.7,
                "requires_manual_review": True,
                "evidence": ["图文或属性信息存在冲突"],
                "rule_hits": ["R001"],
            }

        if incomplete_evidence:
            if not result["is_abnormal"]:
                result = {
                    "is_abnormal": False,
                    "issue_type": "证据不足",
                    "reason": "样本存在遮挡、视角有限或无法完整判断的问题，应转人工复核。",
                    "confidence": 0.45,
                    "requires_manual_review": True,
                    "evidence": ["举证视角或证据链不完整"],
                    "rule_hits": ["R003"],
                }
            elif "R003" not in result["rule_hits"]:
                result["requires_manual_review"] = True
                result["evidence"].append("举证证据不完整")
                result["rule_hits"].append("R003")

        return json.dumps(result, ensure_ascii=False)


def _extract_current_input(prompt_text: str) -> str:
    if "地块编号:" in prompt_text and "审查规则:" in prompt_text:
        return prompt_text.split("地块编号:", 1)[1].split("审查规则:", 1)[0]
    if "审查规则:" in prompt_text:
        return prompt_text.split("审查规则:", 1)[0]
    return prompt_text


def _extract_line(text: str, label: str) -> str:
    for line in text.splitlines():
        if line.strip().startswith(label):
            return line.split(label, 1)[1].strip()
    return ""


def _contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def _normal_result() -> dict:
    return {
        "is_abnormal": False,
        "issue_type": "未发现明显异常",
        "reason": "当前样本未触发明显异常规则。",
        "confidence": 0.65,
        "requires_manual_review": False,
        "evidence": ["规则未触发强冲突"],
        "rule_hits": [],
    }
