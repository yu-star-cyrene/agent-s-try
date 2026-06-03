import json

from src.modules.model_gateway.base import ModelClient


class MockModelClient(ModelClient):
    def inspect(self, prompt: str, image_path: str | None = None) -> str:
        prompt_text = prompt.lower()
        has_building = "建筑" in prompt_text or "硬化地表" in prompt_text
        is_farmland = "耕地" in prompt_text
        incomplete_evidence = "角度有限" in prompt_text or "证据不足" in prompt_text

        result = {
            "is_abnormal": has_building and is_farmland,
            "issue_type": "耕地疑似建筑占用" if has_building and is_farmland else "未发现明显异常",
            "reason": "文本描述显示为耕地，但样例中包含疑似建筑物线索。"
            if has_building and is_farmland
            else "当前样例未触发明显冲突规则。",
            "confidence": 0.82 if has_building and is_farmland else 0.55,
            "requires_manual_review": incomplete_evidence or (has_building and is_farmland),
            "evidence": [
                "地块说明包含耕地信息",
                "样例描述包含疑似建筑物",
                "拍摄角度有限"
            ]
            if has_building and is_farmland
            else ["规则未触发强冲突"],
        }
        return json.dumps(result, ensure_ascii=False)
