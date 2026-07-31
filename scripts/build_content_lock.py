#!/usr/bin/env python3
"""Build a frozen per-slide content lock from a confirmed outline JSON."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_slide(data: Any, slide_number: int) -> dict[str, Any]:
    slides = data.get("slides") if isinstance(data, dict) else None
    if not isinstance(slides, list):
        raise SystemExit("Input JSON must contain a slides array.")
    for slide in slides:
        if isinstance(slide, dict) and slide.get("slide") == slide_number:
            return slide
    raise SystemExit(f"Slide {slide_number} not found in input.")


def build_content_lock(slide: dict[str, Any], source_path: Path) -> dict[str, Any]:
    required = [
        "title",
        "subtitle",
        "charts",
        "tables",
        "kpis",
        "annotations",
        "so_what",
        "evidence_ids",
        "required_components",
    ]
    missing = [field for field in required if field not in slide]
    return {
        "schema": "pengyuyanppt_skill.slide_content_lock.v1",
        "slide": slide.get("slide"),
        "source_outline": str(source_path),
        "source_outline_sha256": sha256_file(source_path),
        "locked": True,
        "missing_fields": missing,
        "title": slide.get("title"),
        "subtitle": slide.get("subtitle"),
        "charts": slide.get("charts", []),
        "tables": slide.get("tables", []),
        "kpis": slide.get("kpis", []),
        "annotations": slide.get("annotations", []),
        "caveats": slide.get("caveats", []),
        "so_what": slide.get("so_what", []),
        "evidence_ids": slide.get("evidence_ids", []),
        "required_components": slide.get("required_components", []),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a PengyuyanPPT_Skill slide_content_lock JSON.")
    parser.add_argument("--outline", required=True, help="Confirmed stage-1 outline/evidence JSON.")
    parser.add_argument("--slide", required=True, type=int, help="Slide number to lock.")
    parser.add_argument("--out", required=True, help="Output content lock JSON.")
    args = parser.parse_args()

    source = Path(args.outline)
    output = Path(args.out)
    slide = find_slide(load_json(source), args.slide)
    lock = build_content_lock(slide, source)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(output), "sha256": sha256_file(output), "locked": True}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
