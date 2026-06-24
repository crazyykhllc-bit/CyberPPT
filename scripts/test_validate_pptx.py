from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("validate_pptx.py")


def load_validator():
    if not SCRIPT_PATH.exists():
        raise AssertionError(f"validator is missing: {SCRIPT_PATH}")
    spec = importlib.util.spec_from_file_location("cyber_ppt_validate_pptx", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("unable to load validator module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_pptx(
    path: Path,
    *,
    width: int = 12_192_000,
    height: int = 6_858_000,
    x: int = 500_000,
    y: int = 500_000,
    cx: int = 3_000_000,
    cy: int = 1_000_000,
    text: str = "Evidence-based conclusion",
    full_slide_picture: bool = False,
) -> None:
    presentation_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst>
  <p:sldSz cx="{width}" cy="{height}"/>
</p:presentation>"""

    if full_slide_picture:
        shape_xml = f"""
<p:pic>
  <p:nvPicPr><p:cNvPr id="2" name="Full slide image"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr>
  <p:blipFill><a:blip r:embed="rId2"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
  <p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{width}" cy="{height}"/></a:xfrm></p:spPr>
</p:pic>"""
    else:
        shape_xml = f"""
<p:sp>
  <p:nvSpPr><p:cNvPr id="2" name="TextBox 1"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm></p:spPr>
  <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:t>{text}</a:t></a:r></a:p></p:txBody>
</p:sp>"""

    slide_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree>
    <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
    <p:grpSpPr/>
    {shape_xml}
  </p:spTree></p:cSld>
</p:sld>"""

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="xml" ContentType="application/xml"/>
</Types>"""

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("ppt/presentation.xml", presentation_xml)
        archive.writestr("ppt/slides/slide1.xml", slide_xml)


class ValidatePptxTests(unittest.TestCase):
    def test_healthy_presentation_has_no_errors(self):
        module = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "healthy.pptx"
            make_pptx(path)
            report = module.validate_pptx(path)
        self.assertEqual([], report["errors"])
        self.assertEqual(1, report["summary"]["slide_count"])
        self.assertAlmostEqual(16 / 9, report["summary"]["aspect_ratio"], places=2)
        self.assertEqual(1, report["summary"]["native_text_shapes"])

    def test_non_widescreen_size_is_reported(self):
        module = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "standard.pptx"
            make_pptx(path, width=9_144_000, height=6_858_000)
            report = module.validate_pptx(path)
        self.assertTrue(
            any(item["code"] == "NON_WIDESCREEN_ASPECT" for item in report["warnings"])
        )

    def test_shape_outside_slide_is_reported(self):
        module = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "overflow.pptx"
            make_pptx(path, x=11_500_000, cx=1_500_000)
            report = module.validate_pptx(path)
        self.assertTrue(
            any(item["code"] == "SHAPE_OUTSIDE_SLIDE" for item in report["warnings"])
        )

    def test_placeholder_text_is_reported(self):
        module = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "placeholder.pptx"
            make_pptx(path, text="TODO: add market data")
            report = module.validate_pptx(path)
        self.assertTrue(
            any(item["code"] == "PLACEHOLDER_TEXT" for item in report["warnings"])
        )

    def test_full_slide_image_risk_is_reported(self):
        module = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "raster-only.pptx"
            make_pptx(path, full_slide_picture=True)
            report = module.validate_pptx(path)
        self.assertTrue(
            any(item["code"] == "FULL_SLIDE_IMAGE_RISK" for item in report["warnings"])
        )
        self.assertEqual(1, report["summary"]["pictures"])
        self.assertEqual(0, report["summary"]["native_text_shapes"])

    def test_cli_writes_json_report(self):
        load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source.pptx"
            output = Path(temp_dir) / "report.json"
            make_pptx(source)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    str(source),
                    "--json-out",
                    str(output),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue(output.exists())
            report = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(1, report["summary"]["slide_count"])


if __name__ == "__main__":
    unittest.main()
