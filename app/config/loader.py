from __future__ import annotations

from pathlib import Path
from typing import Any


DEFAULT_SETTINGS_PATH = Path(__file__).with_name("settings.yaml")


def _convert_scalar(raw: str) -> Any:
    value = raw.strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(0, root)]

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.strip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if not line.endswith(":") and ":" not in line:
            raise ValueError(f"Unsupported YAML line: {raw_line}")

        while stack and indent < stack[-1][0]:
            stack.pop()

        current = stack[-1][1]

        if line.endswith(":"):
            key = line[:-1].strip()
            new_dict: dict[str, Any] = {}
            current[key] = new_dict
            stack.append((indent + 2, new_dict))
        else:
            key, raw_val = line.split(":", 1)
            current[key.strip()] = _convert_scalar(raw_val)

    return root


def load_settings(path: str | Path | None = None) -> dict[str, Any]:
    target = Path(path) if path else DEFAULT_SETTINGS_PATH
    return _parse_simple_yaml(target.read_text(encoding="utf-8"))
