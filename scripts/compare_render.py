#!/usr/bin/env python3
"""Compare an approved blueprint PNG with a PowerPoint render PNG."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_image(path: Path):
    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit("Pillow is required for compare_render.py") from exc
    return Image.open(path).convert("RGB")


def crop_mean_abs_diff(a, b) -> float:
    try:
        import numpy as np
    except ImportError as exc:
        raise SystemExit("numpy is required for compare_render.py") from exc
    arr_a = np.asarray(a, dtype="int16")
    arr_b = np.asarray(b.resize(a.size), dtype="int16")
    return float(np.mean(np.abs(arr_a - arr_b)))


def bbox_tuple(bbox: dict[str, Any]) -> tuple[int, int, int, int]:
    x = int(round(float(bbox["x"])))
    y = int(round(float(bbox["y"])))
    w = int(round(float(bbox["w"])))
    h = int(round(float(bbox["h"])))
    return (x, y, x + w, y + h)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare blueprint/render crops using a visual element registry.")
    parser.add_argument("--blueprint", required=True)
    parser.add_argument("--render", required=True)
    parser.add_argument("--registry", required=True)
    parser.add_argument("--out", required=True, help="Output bbox/pixel diff report JSON.")
    parser.add_argument("--overlay-out", help="Optional overlay PNG.")
    args = parser.parse_args()

    blueprint_path = Path(args.blueprint)
    render_path = Path(args.render)
    registry_path = Path(args.registry)
    blueprint = load_image(blueprint_path)
    render = load_image(render_path).resize(blueprint.size)
    registry = read_json(registry_path)
    elements = registry.get("elements", registry.get("visual_element_registry", []))
    if not isinstance(elements, list):
        elements = []

    failures: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    for element in elements:
        if not isinstance(element, dict):
            continue
        bbox = element.get("blueprint_bbox_px")
        if not isinstance(bbox, dict):
            failures.append({"element_id": element.get("element_id"), "code": "BLUEPRINT_BBOX_MISSING"})
            continue
        crop_box = bbox_tuple(bbox)
        diff = crop_mean_abs_diff(blueprint.crop(crop_box), render.crop(crop_box))
        tolerance = float(element.get("pixel_mean_abs_tolerance", 18))
        status = "passed" if diff <= tolerance else "failed"
        result = {
            "element_id": element.get("element_id"),
            "priority": element.get("priority"),
            "blueprint_bbox_px": bbox,
            "render_bbox_px": element.get("render_bbox_px", bbox),
            "delta_px": element.get("delta_px", {"x": 0, "y": 0, "w": 0, "h": 0}),
            "tolerance_px": element.get("tolerance_px"),
            "pixel_mean_abs_diff": round(diff, 3),
            "pixel_mean_abs_tolerance": tolerance,
            "status": status,
        }
        results.append(result)
        if status != "passed":
            failures.append({"element_id": element.get("element_id"), "code": "PIXEL_DIFF_EXCEEDED", "severity": "High"})

    if args.overlay_out:
        from PIL import ImageChops

        overlay = ImageChops.blend(blueprint, render, 0.5)
        overlay_path = Path(args.overlay_out)
        overlay_path.parent.mkdir(parents=True, exist_ok=True)
        overlay.save(overlay_path)

    report = {
        "schema": "pengyuyanppt_skill.render_compare.v1",
        "blueprint_path": str(blueprint_path),
        "render_path": str(render_path),
        "registry_path": str(registry_path),
        "elements_checked": len(results),
        "passed": not failures and bool(results),
        "results": results,
        "failures": failures,
    }
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(output), "passed": report["passed"], "failures": len(failures)}, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
