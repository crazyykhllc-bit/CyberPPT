from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("select_icon.py")


def load_script():
    if not SCRIPT_PATH.exists():
        raise AssertionError(f"script is missing: {SCRIPT_PATH}")
    spec = importlib.util.spec_from_file_location("cyber_ppt_select_icon", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("unable to load select_icon module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SelectIconTests(unittest.TestCase):
    def test_build_index_searches_and_syncs_icon(self):
        module = load_script()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "icons"
            library = root / "tabler-outline"
            library.mkdir(parents=True)
            source_icon = library / "cash-flow.svg"
            source_icon.write_text(
                '<svg viewBox="0 0 24 24"><path d="M1 1h22v22H1z"/></svg>',
                encoding="utf-8",
            )
            (library / "risk-alert.svg").write_text(
                '<svg viewBox="0 0 24 24"><path d="M4 4h16v16H4z"/></svg>',
                encoding="utf-8",
            )

            index = module.build_index(root)
            self.assertEqual(2, len(index["icons"]))
            results = module.search_icons(index, "cash", library="tabler-outline", limit=5)
            self.assertEqual("tabler-outline/cash-flow", results[0]["icon_id"])

            output_root = Path(temp_dir) / "project-icons"
            synced = module.sync_icon(root, output_root, "tabler-outline/cash-flow")
            self.assertTrue(synced.exists())
            self.assertEqual(source_icon.read_text(encoding="utf-8"), synced.read_text(encoding="utf-8"))

            index_path = Path(temp_dir) / "index.json"
            module.write_json(index_path, index)
            loaded = json.loads(index_path.read_text(encoding="utf-8"))
            self.assertEqual("cyberppt.icon_index.v1", loaded["schema"])


if __name__ == "__main__":
    unittest.main()
