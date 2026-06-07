import json
from pathlib import Path


def load_rule_bundle(rule_path: str | Path) -> dict:
    path = Path(rule_path)
    return json.loads(path.read_text(encoding="utf-8"))


def list_enabled_rules(rule_bundle: dict) -> list[dict]:
    rules = [
        item
        for item in rule_bundle.get("rules", [])
        if item.get("enabled", True)
    ]
    return sorted(rules, key=lambda item: item.get("priority", 0), reverse=True)


def list_rule_statements(rule_bundle: dict) -> list[str]:
    rules = list_enabled_rules(rule_bundle)
    return [item.get("description", "").strip() for item in rules if item.get("description")]
