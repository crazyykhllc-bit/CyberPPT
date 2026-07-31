#!/usr/bin/env python3
"""Validate or build a visual element registry for an approved blueprint."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


PRIORITY_TOLERANCE = {"P0": 3, "P1": 4, "P2": 6}
PPT_CANVAS_IN = {"w": 13.333, "h": 7.5}


def image_size(path: Path) -> tuple[int, int]:
    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit("Pillow is required for measure_blueprint.py") from exc
    with Image.open(path) as image:
        return image.size


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def convert_bbox(bbox: dict[str, Any], scale_x: float, scale_y: float) -> dict[str, float]:
    return {
        "x": round(float(bbox["x"]) * scale_x, 4),
        "y": round(float(bbox["y"]) * scale_y, 4),
        "w": round(float(bbox["w"]) * scale_x, 4),
        "h": round(float(bbox["h"]) * scale_y, 4),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create/validate a PengyuyanPPT_Skill visual_element_registry.")
    parser.add_argument("--blueprint", required=True, help="Approved blueprint PNG.")
    parser.add_argument("--annotations", help="Manual/AI element annotation JSON with elements array.")
    parser.add_argument("--out", required=True, help="Output visual element registry JSON.")
    args = parser.parse_args()

    blueprint = Path(args.blueprint)
    width, height = image_size(blueprint)
    scale_x = PPT_CANVAS_IN["w"] / width
    scale_y = PPT_CANVAS_IN["h"] / height
    elements: list[dict[str, Any]] = []
    failures: list[str] = []

    if args.annotations:
        payload = read_json(Path(args.annotations))
        raw_elements = payload.get("elements") if isinstance(payload, dict) else payload
        if not isinstance(raw_elements, list):
            failures.append("annotations must contain an elements array")
            raw_elements = []
        for index, item in enumerate(raw_elements, start=1):
            if not isinstance(item, dict):
                failures.append(f"elements[{index}] must be an object")
                continue
            bbox = item.get("blueprint_bbox_px")
            priority = item.get("priority")
            if priority not in PRIORITY_TOLERANCE:
                failures.append(f"elements[{index}] priority must be P0/P1/P2")
                continue
            if not isinstance(bbox, dict) or not all(k in bbox for k in ("x", "y", "w", "h")):
                failures.append(f"elements[{index}] requires blueprint_bbox_px")
                continue
            element = dict(item)
            element.setdefault("tolerance_px", PRIORITY_TOLERANCE[priority])
            element["ppt_target_bbox_in"] = convert_bbox(bbox, scale_x, scale_y)
            elements.append(element)
    else:
        failures.append("manual element annotations are required; automatic full-element detection is not reliable")

    registry = {
        "schema": "pengyuyanppt_skill.visual_element_registry.v1",
        "blueprint_path": str(blueprint),
        "blueprint_sha256": sha256_file(blueprint),
        "blueprint_canvas_px": {"w": width, "h": height},
        "ppt_canvas_in": PPT_CANVAS_IN,
        "scale_x": scale_x,
        "scale_y": scale_y,
        "elements": elements,
        "element_count": len(elements),
        "coverage_check": {
            "manual_annotations_required": True,
            "passed": bool(elements) and not failures,
            "failures": failures,
        },
    }

    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(output), "element_count": len(elements), "passed": not failures}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
