#!/usr/bin/env python3
"""Index, search, and sync CyberPPT SVG icons without loading the whole library."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


SVG_NS_RE = re.compile(r"\{.*\}")
WORD_RE = re.compile(r"[a-z0-9]+")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_words(value: str) -> list[str]:
    return WORD_RE.findall(value.lower().replace("-", " ").replace("_", " "))


def read_svg_viewbox(path: Path) -> str | None:
    try:
        root = ET.fromstring(path.read_text(encoding="utf-8"))
    except (ET.ParseError, UnicodeDecodeError):
        return None
    tag = SVG_NS_RE.sub("", root.tag)
    if tag.lower() != "svg":
        return None
    return root.get("viewBox")


def build_index(icons_root: str | Path) -> dict[str, Any]:
    root = Path(icons_root)
    icons: list[dict[str, Any]] = []
    for svg_path in sorted(root.glob("*/*.svg")):
        library = svg_path.parent.name
        name = svg_path.stem
        icon_id = f"{library}/{name}"
        icons.append(
            {
                "icon_id": icon_id,
                "library": library,
                "name": name,
                "path": str(svg_path.relative_to(root)).replace("\\", "/"),
                "viewBox": read_svg_viewbox(svg_path),
                "search_terms": normalize_words(f"{library} {name}"),
                "bytes": svg_path.stat().st_size,
            }
        )
    return {
        "schema": "cyberppt.icon_index.v1",
        "icons_root": str(root),
        "icon_count": len(icons),
        "libraries": sorted({icon["library"] for icon in icons}),
        "icons": icons,
    }


def search_icons(
    index: dict[str, Any],
    query: str,
    *,
    library: str | None = None,
    limit: int = 20,
) -> list[dict[str, Any]]:
    query_words = normalize_words(query)
    if not query_words:
        return []
    results: list[tuple[int, dict[str, Any]]] = []
    for icon in index.get("icons", []):
        if not isinstance(icon, dict):
            continue
        if library and icon.get("library") != library:
            continue
        haystack = set(icon.get("search_terms", []))
        name = str(icon.get("name", "")).lower()
        score = 0
        for word in query_words:
            if word in haystack:
                score += 4
            elif word in name:
                score += 2
        if score:
            results.append((score, icon))
    results.sort(key=lambda item: (-item[0], item[1].get("icon_id", "")))
    return [icon for _, icon in results[:limit]]


def sync_icon(icons_root: str | Path, output_root: str | Path, icon_id: str) -> Path:
    if "/" not in icon_id:
        raise ValueError("icon_id must use '<library>/<name>' format")
    library, name = icon_id.split("/", 1)
    source = Path(icons_root) / library / f"{name}.svg"
    if not source.exists():
        raise FileNotFoundError(f"Icon not found: {icon_id}")
    destination = Path(output_root) / library / source.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return destination


def load_index(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CyberPPT icon library helper.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build-index", help="Build assets/icons/index.json.")
    build.add_argument("--icons-root", required=True)
    build.add_argument("--out", required=True)

    search = subparsers.add_parser("search", help="Search icon index by keyword.")
    search.add_argument("--index", required=True)
    search.add_argument("--query", required=True)
    search.add_argument("--library")
    search.add_argument("--limit", type=int, default=20)

    sync = subparsers.add_parser("sync", help="Copy one icon into a project icons folder.")
    sync.add_argument("--icons-root", required=True)
    sync.add_argument("--icon", required=True)
    sync.add_argument("--out-dir", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "build-index":
        index = build_index(args.icons_root)
        write_json(Path(args.out), index)
        print(json.dumps({"path": args.out, "icon_count": index["icon_count"]}, indent=2))
        return 0
    if args.command == "search":
        index = load_index(Path(args.index))
        results = search_icons(index, args.query, library=args.library, limit=args.limit)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0 if results else 1
    if args.command == "sync":
        destination = sync_icon(args.icons_root, args.out_dir, args.icon)
        print(json.dumps({"icon": args.icon, "path": str(destination)}, indent=2))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
