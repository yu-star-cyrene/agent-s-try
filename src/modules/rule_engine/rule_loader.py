import json
from pathlib import Path


def load_rule_bundle(rule_path: str | Path) -> dict:
    path = Path(rule_path)
    return json.loads(path.read_text(encoding="utf-8"))


def list_rule_statements(rule_bundle: dict) -> list[str]:
    rules = rule_bundle.get("rules", [])
    return [item.get("description", "").strip() for item in rules if item.get("description")]
