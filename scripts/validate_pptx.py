#!/usr/bin/env python3
"""Inspect a PPTX for structural, editability, and layout risks."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
}
PLACEHOLDER_RE = re.compile(
    r"\b(?:TODO|TBD)\b|Lorem ipsum|Click to add|单击此处添加",
    re.IGNORECASE,
)
SLIDE_RE = re.compile(r"ppt/slides/slide(\d+)\.xml$")


def issue(code: str, message: str, *, slide: int | None = None) -> dict[str, Any]:
    item: dict[str, Any] = {"code": code, "message": message}
    if slide is not None:
        item["slide"] = slide
    return item


def read_xml(archive: zipfile.ZipFile, name: str) -> ET.Element:
    return ET.fromstring(archive.read(name))


def find_slide_names(archive: zipfile.ZipFile) -> list[str]:
    matched: list[tuple[int, str]] = []
    for name in archive.namelist():
        result = SLIDE_RE.fullmatch(name)
        if result:
            matched.append((int(result.group(1)), name))
    return [name for _, name in sorted(matched)]


def shape_bounds(element: ET.Element) -> tuple[int, int, int, int] | None:
    xfrm = element.find(".//a:xfrm", NS)
    if xfrm is None:
        return None
    offset = xfrm.find("a:off", NS)
    extent = xfrm.find("a:ext", NS)
    if offset is None or extent is None:
        return None
    try:
        return (
            int(offset.get("x", "0")),
            int(offset.get("y", "0")),
            int(extent.get("cx", "0")),
            int(extent.get("cy", "0")),
        )
    except ValueError:
        return None


def text_content(element: ET.Element) -> str:
    return " ".join((node.text or "") for node in element.findall(".//a:t", NS)).strip()


def inspect_slide(
    root: ET.Element,
    slide_number: int,
    width: int,
    height: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    warnings: list[dict[str, Any]] = []
    shapes = root.findall(".//p:sp", NS)
    pictures = root.findall(".//p:pic", NS)
    graphic_frames = root.findall(".//p:graphicFrame", NS)
    charts = root.findall(".//c:chart", NS)
    tables = root.findall(".//a:tbl", NS)

    native_text_shapes = sum(1 for shape in shapes if text_content(shape))
    all_elements = [*shapes, *pictures, *graphic_frames]
    bounds: list[tuple[int, int, int, int]] = []

    for element in all_elements:
        box = shape_bounds(element)
        if box is None:
            continue
        bounds.append(box)
        x, y, cx, cy = box
        if x < 0 or y < 0 or x + cx > width or y + cy > height:
            warnings.append(
                issue(
                    "SHAPE_OUTSIDE_SLIDE",
                    f"Element extends beyond the {width}×{height} EMU slide canvas.",
                    slide=slide_number,
                )
            )

    combined_text = " ".join(filter(None, (text_content(shape) for shape in shapes)))
    if PLACEHOLDER_RE.search(combined_text):
        warnings.append(
            issue(
                "PLACEHOLDER_TEXT",
                "Possible authoring placeholder text remains on the slide.",
                slide=slide_number,
            )
        )

    slide_area = max(width * height, 1)
    for picture in pictures:
        box = shape_bounds(picture)
        if box is None:
            continue
        _, _, cx, cy = box
        if (cx * cy) / slide_area >= 0.90 and native_text_shapes == 0:
            warnings.append(
                issue(
                    "FULL_SLIDE_IMAGE_RISK",
                    "A single image covers at least 90% of the slide and no native text was found.",
                    slide=slide_number,
                )
            )

    if bounds:
        left = min(x for x, _, _, _ in bounds)
        top = min(y for _, y, _, _ in bounds)
        right = max(x + cx for x, _, cx, _ in bounds)
        bottom = max(y + cy for _, y, _, cy in bounds)
        coverage = max(0.0, min(1.0, ((right - left) * (bottom - top)) / slide_area))
        right_gap = max(0, width - right) / max(width, 1)
        bottom_gap = max(0, height - bottom) / max(height, 1)
        if right_gap > 0.28 and bottom_gap > 0.28 and len(all_elements) >= 2:
            warnings.append(
                issue(
                    "UNBALANCED_EMPTY_SPACE",
                    "Content leaves more than 28% unused space on both the right and bottom edges.",
                    slide=slide_number,
                )
            )
    else:
        coverage = 0.0
        warnings.append(
            issue(
                "EMPTY_OR_UNMEASURABLE_SLIDE",
                "No measurable native slide elements were found.",
                slide=slide_number,
            )
        )

    if len(all_elements) <= 1 and not pictures:
        warnings.append(
            issue(
                "LOW_CONTENT_DENSITY",
                "The slide contains one or fewer measurable elements; review information density.",
                slide=slide_number,
            )
        )

    metrics = {
        "slide": slide_number,
        "native_text_shapes": native_text_shapes,
        "native_graphic_shapes": len(shapes) + len(graphic_frames),
        "pictures": len(pictures),
        "charts": len(charts),
        "tables": len(tables),
        "element_count": len(all_elements),
        "coverage_ratio": round(coverage, 4),
        "text_characters": len(combined_text),
    }
    return metrics, warnings


def empty_report(path: Path) -> dict[str, Any]:
    return {
        "file": str(path),
        "summary": {
            "slide_count": 0,
            "width_emu": 0,
            "height_emu": 0,
            "aspect_ratio": 0.0,
            "native_text_shapes": 0,
            "native_graphic_shapes": 0,
            "pictures": 0,
            "charts": 0,
            "tables": 0,
        },
        "errors": [],
        "warnings": [],
        "slides": [],
    }


def validate_pptx(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    report = empty_report(source)
    if not source.exists():
        report["errors"].append(issue("FILE_NOT_FOUND", f"File does not exist: {source}"))
        return report

    try:
        with zipfile.ZipFile(source) as archive:
            names = set(archive.namelist())
            required = {"[Content_Types].xml", "ppt/presentation.xml"}
            missing = sorted(required - names)
            if missing:
                report["errors"].append(
                    issue("MISSING_PACKAGE_PART", f"Missing required parts: {', '.join(missing)}")
                )
                return report

            presentation = read_xml(archive, "ppt/presentation.xml")
            slide_size = presentation.find("p:sldSz", NS)
            if slide_size is None:
                report["errors"].append(
                    issue("MISSING_SLIDE_SIZE", "ppt/presentation.xml has no p:sldSz element.")
                )
                return report

            width = int(slide_size.get("cx", "0"))
            height = int(slide_size.get("cy", "0"))
            if width <= 0 or height <= 0:
                report["errors"].append(
                    issue("INVALID_SLIDE_SIZE", f"Invalid slide size: {width}×{height} EMU.")
                )
                return report

            ratio = width / height
            report["summary"].update(
                {
                    "width_emu": width,
                    "height_emu": height,
                    "aspect_ratio": round(ratio, 4),
                }
            )
            if not 1.75 <= ratio <= 1.79:
                report["warnings"].append(
                    issue(
                        "NON_WIDESCREEN_ASPECT",
                        f"Slide aspect ratio is {ratio:.4f}; expected approximately 16:9.",
                    )
                )

            slide_names = find_slide_names(archive)
            if not slide_names:
                report["errors"].append(issue("NO_SLIDES", "No ppt/slides/slideN.xml parts found."))
                return report

            for slide_number, slide_name in enumerate(slide_names, start=1):
                try:
                    slide_root = read_xml(archive, slide_name)
                except (KeyError, ET.ParseError) as exc:
                    report["errors"].append(
                        issue(
                            "INVALID_SLIDE_XML",
                            f"Cannot parse {slide_name}: {exc}",
                            slide=slide_number,
                        )
                    )
                    continue
                metrics, warnings = inspect_slide(slide_root, slide_number, width, height)
                report["slides"].append(metrics)
                report["warnings"].extend(warnings)

            report["summary"]["slide_count"] = len(slide_names)
            for field in (
                "native_text_shapes",
                "native_graphic_shapes",
                "pictures",
                "charts",
                "tables",
            ):
                report["summary"][field] = sum(slide[field] for slide in report["slides"])
    except zipfile.BadZipFile:
        report["errors"].append(issue("INVALID_PPTX_ZIP", "File is not a readable PPTX ZIP package."))
    except (ET.ParseError, KeyError, ValueError) as exc:
        report["errors"].append(issue("INVALID_PACKAGE_XML", str(exc)))

    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check PPTX structure, aspect ratio, editability, placeholders, and layout risks."
    )
    parser.add_argument("pptx", help="Path to the PPTX file")
    parser.add_argument("--json-out", help="Optional path for a UTF-8 JSON report")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = validate_pptx(args.pptx)
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_out:
        output = Path(args.json_out)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
