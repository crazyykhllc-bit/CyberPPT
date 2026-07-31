#!/usr/bin/env python3
"""Index, search, sync, and cache PengyuyanPPT_Skill SVG icons.

The index may aggregate the bundled library plus optional open-source SVG roots.
"""

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
STYLE_FAMILIES = {
    "outline-business": {
        "tabler-outline",
        "lucide",
        "heroicons-outline",
        "fluent-regular",
        "carbon",
        "bootstrap",
        "remix-line",
    },
    "filled-business": {
        "tabler-filled",
        "heroicons-solid",
        "material-symbols",
        "bootstrap-filled",
        "remix-fill",
        "fluent-filled",
    },
    "duotone-premium": {"phosphor-duotone"},
    "technical-system": {
        "chunk-filled",
        "carbon",
        "fluent-regular",
        "fluent-filled",
    },
    "brand-logo": {"simple-icons"},
}

SEMANTIC_ALIASES = {
    "knowledge": {"book", "books", "library", "brain", "database", "file"},
    "search": {"find", "magnifier", "zoom"},
    "risk": {"warning", "alert", "shield", "exclamation"},
    "strategy": {"target", "compass", "map", "roadmap"},
    "workflow": {"process", "flow", "route", "nodes"},
    "customer": {"user", "users", "person", "people"},
    "sales": {"briefcase", "handshake", "chart", "money"},
    "ai": {"sparkles", "robot", "brain", "cpu"},
}


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


def build_index(
    icons_root: str | Path,
    *,
    extra_roots: list[str | Path] | None = None,
) -> dict[str, Any]:
    root = Path(icons_root)
    roots = [root, *(Path(item) for item in (extra_roots or []))]
    icons: list[dict[str, Any]] = []
    seen: set[str] = set()
    for source_root in roots:
        if not source_root.exists():
            continue
        for svg_path in sorted(source_root.glob("*/*.svg")):
            library = svg_path.parent.name
            name = svg_path.stem
            icon_id = f"{library}/{name}"
            if icon_id in seen:
                continue
            seen.add(icon_id)
            icons.append(
                {
                    "icon_id": icon_id,
                    "library": library,
                    "name": name,
                    "path": str(svg_path.resolve()),
                    "source_root": str(source_root.resolve()),
                    "viewBox": read_svg_viewbox(svg_path),
                    "search_terms": normalize_words(f"{library} {name}"),
                    "bytes": svg_path.stat().st_size,
                }
            )
    return {
        "schema": "pengyuyanppt_skill.icon_index.v1",
        "icons_root": str(root.resolve()),
        "source_roots": [str(item.resolve()) for item in roots if item.exists()],
        "icon_count": len(icons),
        "libraries": sorted({icon["library"] for icon in icons}),
        "icons": icons,
    }


def search_icons(
    index: dict[str, Any],
    query: str,
    *,
    library: str | None = None,
    style_family: str | None = None,
    limit: int = 20,
) -> list[dict[str, Any]]:
    query_words = normalize_words(query)
    if not query_words:
        return []
    expanded_words = set(query_words)
    for word in query_words:
        expanded_words.update(SEMANTIC_ALIASES.get(word, set()))
    allowed_libraries = STYLE_FAMILIES.get(style_family or "")
    results: list[tuple[int, dict[str, Any]]] = []
    for icon in index.get("icons", []):
        if not isinstance(icon, dict):
            continue
        if library and icon.get("library") != library:
            continue
        if allowed_libraries and icon.get("library") not in allowed_libraries:
            continue
        haystack = set(icon.get("search_terms", []))
        name = str(icon.get("name", "")).lower()
        score = 0
        for word in expanded_words:
            if word in haystack:
                score += 4
            elif word in name:
                score += 2
        if any(word in haystack for word in query_words):
            score += 3
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


def cache_icon(index: dict[str, Any], output_root: str | Path, icon_id: str) -> Path:
    match = next((item for item in index.get("icons", []) if item.get("icon_id") == icon_id), None)
    if not match:
        raise FileNotFoundError(f"Icon not found in index: {icon_id}")
    source = Path(str(match["path"]))
    if not source.is_absolute():
        source = Path(str(index.get("icons_root", ""))) / source
    if not source.exists():
        raise FileNotFoundError(f"Indexed SVG is missing: {source}")
    destination = Path(output_root) / str(match["library"]) / source.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return destination


def load_index(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PengyuyanPPT_Skill icon library helper.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build-index", help="Build assets/icons/index.json.")
    build.add_argument("--icons-root", required=True)
    build.add_argument(
        "--extra-root",
        action="append",
        default=[],
        help="Optional open-source SVG root containing <library>/*.svg; repeatable.",
    )
    build.add_argument("--out", required=True)

    search = subparsers.add_parser("search", help="Search icon index by keyword.")
    search.add_argument("--index", required=True)
    search.add_argument("--query", required=True)
    search.add_argument("--library")
    search.add_argument("--style-family", choices=sorted(STYLE_FAMILIES))
    search.add_argument("--limit", type=int, default=20)

    sync = subparsers.add_parser("sync", help="Copy one icon into a project icons folder.")
    sync.add_argument("--icons-root", required=True)
    sync.add_argument("--icon", required=True)
    sync.add_argument("--out-dir", required=True)

    cache = subparsers.add_parser("cache", help="Copy any indexed icon into a project cache.")
    cache.add_argument("--index", required=True)
    cache.add_argument("--icon", required=True)
    cache.add_argument("--out-dir", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "build-index":
        index = build_index(args.icons_root, extra_roots=args.extra_root)
        write_json(Path(args.out), index)
        print(json.dumps({"path": args.out, "icon_count": index["icon_count"]}, indent=2))
        return 0
    if args.command == "search":
        index = load_index(Path(args.index))
        results = search_icons(
            index,
            args.query,
            library=args.library,
            style_family=args.style_family,
            limit=args.limit,
        )
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0 if results else 1
    if args.command == "sync":
        destination = sync_icon(args.icons_root, args.out_dir, args.icon)
        print(json.dumps({"icon": args.icon, "path": str(destination)}, indent=2))
        return 0
    if args.command == "cache":
        index = load_index(Path(args.index))
        destination = cache_icon(index, args.out_dir, args.icon)
        print(json.dumps({"icon": args.icon, "path": str(destination)}, indent=2))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
