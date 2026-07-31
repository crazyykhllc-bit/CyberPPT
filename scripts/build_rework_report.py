#!/usr/bin/env python3
"""Create a human-readable rework report from PengyuyanPPT_Skill QA reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a PengyuyanPPT_Skill rework report.")
    parser.add_argument("--compare-report", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    report = read_json(Path(args.compare_report))
    failures = report.get("failures", []) if isinstance(report, dict) else []
    lines = ["# PengyuyanPPT_Skill Rework Report", ""]
    if not failures:
        lines.append("No rework items reported by compare_render.py.")
    else:
        lines.append("The slide cannot be delivered until these items are fixed:")
        lines.append("")
        for failure in failures:
            if not isinstance(failure, dict):
                continue
            lines.append(f"- `{failure.get('element_id', 'unknown')}`: {failure.get('code', 'failed')}")
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(output), "failures": len(failures)}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
