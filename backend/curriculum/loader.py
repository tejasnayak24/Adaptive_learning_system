import json
from pathlib import Path
from typing import Any

CONTENT_DIR = Path(__file__).resolve().parent / "content"


def load_file(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    data["_file"] = path.name
    return data


def load_all(content_dir: Path = CONTENT_DIR) -> list[dict[str, Any]]:
    """All grade-subject files, sorted by grade then subject."""
    files = [load_file(p) for p in sorted(content_dir.glob("g*_*.json"))]
    return sorted(files, key=lambda d: (d.get("grade", 0), d.get("subject", "")))


def iter_lessons(data: dict[str, Any]):
    """Yield (unit, topic, lesson) in curriculum order for one file."""
    for unit in data.get("units", []):
        for topic in unit.get("topics", []):
            for lesson in topic.get("lessons", []):
                yield unit, topic, lesson
