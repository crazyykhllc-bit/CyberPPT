#!/usr/bin/env python3
"""Inspect PPTX object counts and full-slide image risks."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}


def bounds(element: ET.Element) -> tuple[int, int, int, int] | None:
    xfrm = element.find(".//a:xfrm", NS)
    if xfrm is None:
        return None
    off = xfrm.find("a:off", NS)
    ext = xfrm.find("a:ext", NS)
    if off is None or ext is None:
        return None
    return (int(off.get("x", "0")), int(off.get("y", "0")), int(ext.get("cx", "0")), int(ext.get("cy", "0")))


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect PengyuyanPPT_Skill PPTX object structure.")
    parser.add_argument("pptx")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    pptx = Path(args.pptx)
    report = {"pptx": str(pptx), "slides": [], "failures": []}
    with zipfile.ZipFile(pptx) as archive:
        presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
        sld_size = presentation.find("p:sldSz", NS)
        width = int(sld_size.get("cx", "0")) if sld_size is not None else 0
        height = int(sld_size.get("cy", "0")) if sld_size is not None else 0
        slide_area = max(width * height, 1)
        slide_names = sorted(name for name in archive.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml"))
        for number, name in enumerate(slide_names, start=1):
            root = ET.fromstring(archive.read(name))
            pictures = root.findall(".//p:pic", NS)
            shapes = root.findall(".//p:sp", NS)
            full_slide_pictures = 0
            for picture in pictures:
                box = bounds(picture)
                if box is None:
                    continue
                _, _, cx, cy = box
                if (cx * cy) / slide_area >= 0.9:
                    full_slide_pictures += 1
            report["slides"].append(
                {
                    "slide": number,
                    "shapes": len(shapes),
                    "pictures": len(pictures),
                    "full_slide_pictures": full_slide_pictures,
                }
            )
            if full_slide_pictures:
                report["failures"].append({"slide": number, "code": "FULL_SLIDE_BACKGROUND_RISK"})

    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(output), "failures": len(report["failures"])}, indent=2))
    return 1 if report["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
