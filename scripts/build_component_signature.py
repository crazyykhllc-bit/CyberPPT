#!/usr/bin/env python3
"""Build a frozen blueprint component signature for a confirmed slide blueprint."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_components(components: Any) -> list[str]:
    if not isinstance(components, list) or not components:
        return ["components must be a non-empty array"]
    failures: list[str] = []
    for index, component in enumerate(components, start=1):
        if not isinstance(component, dict):
            failures.append(f"components[{index}] must be an object")
            continue
        for field in ("id", "type", "priority", "required_subcomponents"):
            value = component.get(field)
            if field == "required_subcomponents":
                if not isinstance(value, list) or not value:
                    failures.append(f"components[{index}].required_subcomponents is required")
            elif value in (None, "", [], {}):
                failures.append(f"components[{index}].{field} is required")
        if component.get("must_preserve_type") is not True:
            failures.append(f"components[{index}].must_preserve_type must be true")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a PengyuyanPPT_Skill blueprint_component_signature JSON.")
    parser.add_argument("--blueprint", required=True, help="Approved blueprint PNG.")
    parser.add_argument("--content-lock", required=True, help="Frozen slide_content_lock JSON.")
    parser.add_argument("--components", required=True, help="Component annotation JSON with a components array.")
    parser.add_argument("--slide", required=True, type=int, help="Slide number.")
    parser.add_argument("--out", required=True, help="Output component signature JSON.")
    args = parser.parse_args()

    blueprint = Path(args.blueprint)
    content_lock = Path(args.content_lock)
    components_path = Path(args.components)
    components_payload = read_json(components_path)
    components = components_payload.get("components") if isinstance(components_payload, dict) else components_payload
    failures = validate_components(components)

    signature = {
        "schema": "pengyuyanppt_skill.blueprint_component_signature.v1",
        "slide": args.slide,
        "locked": not failures,
        "blueprint_path": str(blueprint),
        "blueprint_sha256": sha256_file(blueprint),
        "content_lock_path": str(content_lock),
        "content_lock_sha256": sha256_file(content_lock),
        "component_annotation_path": str(components_path),
        "component_annotation_sha256": sha256_file(components_path),
        "components": components if isinstance(components, list) else [],
        "validation_failures": failures,
    }

    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(signature, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(output), "sha256": sha256_file(output), "locked": not failures}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
