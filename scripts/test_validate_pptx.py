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
    spec = importlib.util.spec_from_file_location("pengyuyan_ppt_skill_validate_pptx", SCRIPT_PATH)
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
        issues = [*report["warnings"], *report["errors"]]
        self.assertTrue(
            any(item["code"] == "FULL_SLIDE_BACKGROUND_RISK" for item in issues)
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

    def test_visual_qa_requires_container_text_and_table_gates(self):
        module = load_validator()
        manifest = {
            "slides": [
                {
                    "slide": 1,
                    "qa_expectations": {"visual_qa_required": True},
                }
            ]
        }
        visual_qa = {
            "slides": [
                {
                    "slide": 1,
                    "surface_system_match": True,
                    "main_chart_semantics_match": True,
                    "visual_semantics_preserved": True,
                    "editable_information_layer_pass": True,
                    "spatial_registration_pass": True,
                    "curve_fidelity_pass": True,
                    "label_collision_pass": True,
                    "text_overflow_pass": True,
                    "blueprint_background_not_used": True,
                    "deliverable_allowed": True,
                }
            ]
        }
        issues = module.validate_visual_qa(visual_qa, manifest)
        missing_fields = {
            item["message"].split("'")[1]
            for item in issues
            if item["code"] == "VISUAL_QA_FIELD_MISSING"
        }
        self.assertEqual(
            {
                "container_overflow_pass",
                "continuous_text_flow_pass",
                "table_semantic_typography_pass",
                "table_density_pass",
            },
            missing_fields,
        )

    def test_visual_qa_delivery_requires_render_comparison_artifacts(self):
        module = load_validator()
        manifest = {
            "slides": [
                {
                    "slide": 1,
                    "qa_expectations": {"visual_qa_required": True},
                }
            ]
        }
        visual_qa = {
            "slides": [
                {
                    "slide": 1,
                    "surface_system_match": True,
                    "main_chart_semantics_match": True,
                    "visual_semantics_preserved": True,
                    "editable_information_layer_pass": True,
                    "spatial_registration_pass": True,
                    "curve_fidelity_pass": True,
                    "label_collision_pass": True,
                    "text_overflow_pass": True,
                    "container_overflow_pass": True,
                    "continuous_text_flow_pass": True,
                    "table_semantic_typography_pass": True,
                    "table_density_pass": True,
                    "blueprint_background_not_used": True,
                    "deliverable_allowed": True,
                    "visual_differences": [],
                }
            ]
        }
        issues = module.validate_visual_qa(visual_qa, manifest)
        codes = {item["code"] for item in issues}
        self.assertIn("BLUEPRINT_RENDER_MISSING", codes)
        self.assertIn("PPT_RENDER_MISSING", codes)
        self.assertIn("SIDE_BY_SIDE_COMPARISON_MISSING", codes)

    def test_visual_qa_true_fields_require_evidence(self):
        module = load_validator()
        manifest = {
            "slides": [
                {
                    "slide": 1,
                    "qa_expectations": {"visual_qa_required": True},
                }
            ]
        }
        visual_qa = {
            "slides": [
                {
                    "slide": 1,
                    "surface_system_match": True,
                    "main_chart_semantics_match": True,
                    "visual_semantics_preserved": True,
                    "editable_information_layer_pass": True,
                    "spatial_registration_pass": True,
                    "curve_fidelity_pass": True,
                    "label_collision_pass": True,
                    "text_overflow_pass": True,
                    "container_overflow_pass": True,
                    "continuous_text_flow_pass": True,
                    "table_semantic_typography_pass": True,
                    "table_density_pass": True,
                    "blueprint_background_not_used": True,
                    "deliverable_allowed": False,
                }
            ]
        }
        issues = module.validate_visual_qa(visual_qa, manifest)
        self.assertTrue(
            any(item["code"] == "VISUAL_PASS_WITHOUT_EVIDENCE" for item in issues)
        )

    def test_table_prose_cannot_be_registered_as_micro_label(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "qa_expectations": {
                "table_semantic_typography_required": True,
            },
            "table_text_objects": [
                {
                    "id": "table_risk_01",
                    "semantic_role": "table_body",
                    "role": "T11",
                    "font_size_pt": 8,
                }
            ],
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        self.assertTrue(
            any(item["code"] == "MANIFEST_TABLE_SEMANTIC_TYPOGRAPHY_FAILED" for item in issues)
        )

    def test_required_container_flow_and_table_density_checks_must_pass(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "qa_expectations": {
                "container_overflow_check_required": True,
                "continuous_text_flow_check_required": True,
                "table_density_check_required": True,
            },
            "container_overflow_check": {"passed": True, "checked_regions": []},
            "continuous_text_flow_check": {"passed": False, "checked_text_runs": ["so_what"]},
            "table_density_check": {"passed": True, "checked_cells": []},
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        codes = {item["code"] for item in issues}
        self.assertIn("MANIFEST_CONTAINER_OVERFLOW_INCOMPLETE", codes)
        self.assertIn("MANIFEST_CONTINUOUS_TEXT_FLOW_FAILED", codes)
        self.assertIn("MANIFEST_TABLE_DENSITY_INCOMPLETE", codes)

    def test_visual_semantics_requires_blueprint_reconstruction_plan(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "qa_expectations": {
                "visual_semantics_required": True,
            },
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        self.assertTrue(
            any(
                item["code"] == "MANIFEST_BLUEPRINT_RECONSTRUCTION_PLAN_MISSING"
                for item in issues
            )
        )

    def test_visual_semantics_requires_complexity_scan(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "blueprint_reconstruction_plan": {
                "blueprint_path": "blueprints/slide-01.png",
                "canvas_size": "16:9",
                "background_color_sample": "#F3F4EF",
                "surface_system": "continuous paper system",
                "layout_regions": ["title", "main_chart", "so_what"],
                "header_footer_system": "source footer",
                "so_what_region": "bottom band",
                "main_chart_semantics": "flow diagram",
                "density_targets": "dense consulting page",
                "anchor_targets": ["title baseline", "flow endpoints"],
                "native_rebuild_targets": ["title", "labels", "so_what"],
                "allowed_visual_assets": [],
            },
            "qa_expectations": {
                "visual_semantics_required": True,
            },
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        self.assertTrue(
            any(
                item["code"] == "MANIFEST_VISUAL_COMPLEXITY_SCAN_MISSING"
                for item in issues
            )
        )

    def test_pictures_zero_cannot_be_declared_as_goal(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "blueprint_reconstruction_plan": {
                "blueprint_path": "blueprints/slide-01.png",
                "canvas_size": "16:9",
                "background_color_sample": "#F3F4EF",
                "surface_system": "continuous paper system",
                "layout_regions": ["title", "main_chart", "so_what"],
                "header_footer_system": "source footer",
                "so_what_region": "bottom band",
                "main_chart_semantics": "flow diagram",
                "density_targets": "dense consulting page",
                "anchor_targets": ["title baseline", "flow endpoints"],
                "native_rebuild_targets": ["title", "labels", "so_what"],
                "allowed_visual_assets": [],
                "complex_visual_scan": {
                    "completed": True,
                    "complex_visual_candidates": ["flow bands"],
                    "triggered_gates": ["curve_trace"],
                    "pictures_zero_is_not_goal": False,
                },
            },
            "qa_expectations": {
                "visual_semantics_required": True,
                "pictures_zero_goal": True,
            },
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        self.assertTrue(
            any(item["code"] == "MANIFEST_PICTURES_ZERO_USED_AS_GOAL" for item in issues)
        )

    def test_python_pptx_is_forbidden_as_generation_engine(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "generation_engine": {
                "tool": "python-pptx",
                "fallback_reason": "",
                "visual_fidelity_not_reduced": False,
            },
            "blueprint_reconstruction_plan": {
                "blueprint_path": "blueprints/slide-01.png",
                "canvas_size": "16:9",
                "background_color_sample": "#F3F4EF",
                "surface_system": "continuous paper system",
                "layout_regions": ["title", "main_chart", "so_what"],
                "header_footer_system": "source footer",
                "so_what_region": "bottom band",
                "main_chart_semantics": "flow diagram",
                "density_targets": "dense consulting page",
                "anchor_targets": ["title baseline", "flow endpoints"],
                "native_rebuild_targets": ["title", "labels", "so_what"],
                "allowed_visual_assets": [],
                "complex_visual_scan": {
                    "completed": True,
                    "complex_visual_candidates": [],
                    "triggered_gates": [],
                    "native_only_rationale": "no complex visual assets in blueprint",
                    "pictures_zero_is_not_goal": True,
                },
            },
            "qa_expectations": {
                "visual_semantics_required": True,
            },
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        codes = {item["code"] for item in issues}
        self.assertIn("MANIFEST_PYTHON_PPTX_FORBIDDEN", codes)
        self.assertIn("MANIFEST_GENERATION_ENGINE_INCOMPLETE", codes)

    def test_non_positive_shape_dimensions_are_strict_failures(self):
        module = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "invalid-bounds.pptx"
            make_pptx(path, cx=-1_000_000)
            report = module.validate_pptx(path, strict=True)
        self.assertTrue(
            any(item["code"] == "INVALID_SHAPE_BOUNDS" for item in report["errors"])
        )

    def test_native_only_complexity_scan_allows_empty_candidates_with_rationale(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "generation_engine": {
                "tool": "pptxgenjs",
                "fallback_reason": None,
                "visual_fidelity_not_reduced": True,
            },
            "blueprint_reconstruction_plan": {
                "blueprint_path": "blueprints/slide-01.png",
                "canvas_size": "16:9",
                "background_color_sample": "#F3F4EF",
                "surface_system": "flat editorial page",
                "layout_regions": ["title", "body", "so_what"],
                "header_footer_system": "source footer",
                "so_what_region": "bottom band",
                "main_chart_semantics": "none",
                "density_targets": "text-led page",
                "anchor_targets": ["title baseline", "body column"],
                "native_rebuild_targets": ["title", "body", "so_what"],
                "allowed_visual_assets": [],
                "complex_visual_scan": {
                    "completed": True,
                    "complex_visual_candidates": [],
                    "triggered_gates": [],
                    "native_only_rationale": "blueprint contains only text, flat color bands, and simple separators",
                    "pictures_zero_is_not_goal": True,
                },
            },
            "qa_expectations": {
                "visual_semantics_required": True,
            },
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        codes = {item["code"] for item in issues}
        self.assertNotIn("MANIFEST_VISUAL_COMPLEXITY_SCAN_INCOMPLETE", codes)

    def test_visual_semantics_requires_single_page_execution_record(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "generation_engine": {
                "tool": "pptxgenjs",
                "fallback_reason": None,
                "visual_fidelity_not_reduced": True,
            },
            "blueprint_reconstruction_plan": {
                "blueprint_path": "blueprints/slide-01.png",
                "canvas_size": "16:9",
                "background_color_sample": "#F3F4EF",
                "surface_system": "flat editorial page",
                "layout_regions": ["title", "body", "so_what"],
                "header_footer_system": "source footer",
                "so_what_region": "bottom band",
                "main_chart_semantics": "none",
                "density_targets": "text-led page",
                "anchor_targets": ["title baseline", "body column"],
                "native_rebuild_targets": ["title", "body", "so_what"],
                "allowed_visual_assets": [],
                "complex_visual_scan": {
                    "completed": True,
                    "complex_visual_candidates": [],
                    "triggered_gates": [],
                    "native_only_rationale": "blueprint contains only text and separators",
                    "pictures_zero_is_not_goal": True,
                },
            },
            "qa_expectations": {
                "visual_semantics_required": True,
            },
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        self.assertTrue(
            any(item["code"] == "MANIFEST_PAGE_EXECUTION_MISSING" for item in issues)
        )

    def test_page_execution_must_be_single_page_and_confirmed(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "generation_engine": {
                "tool": "pptxgenjs",
                "fallback_reason": None,
                "visual_fidelity_not_reduced": True,
            },
            "blueprint_reconstruction_plan": {
                "blueprint_path": "blueprints/slide-01.png",
                "canvas_size": "16:9",
                "background_color_sample": "#F3F4EF",
                "surface_system": "flat editorial page",
                "layout_regions": ["title", "body", "so_what"],
                "header_footer_system": "source footer",
                "so_what_region": "bottom band",
                "main_chart_semantics": "none",
                "density_targets": "text-led page",
                "anchor_targets": ["title baseline", "body column"],
                "native_rebuild_targets": ["title", "body", "so_what"],
                "allowed_visual_assets": [],
                "complex_visual_scan": {
                    "completed": True,
                    "complex_visual_candidates": [],
                    "triggered_gates": [],
                    "native_only_rationale": "blueprint contains only text and separators",
                    "pictures_zero_is_not_goal": True,
                },
            },
            "page_execution": {
                "mode": "batch_deck",
                "single_page_pptx_path": "",
                "blueprint_render_path": "blueprints/slide-01.png",
                "ppt_render_path": "renders/slide-01.png",
                "side_by_side_path": "qa/slide-01-side-by-side.png",
                "local_comparison_artifacts": [],
                "page_status": "draft",
                "user_confirmed": False,
                "made_before_next_slide": False,
            },
            "qa_expectations": {
                "visual_semantics_required": True,
            },
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        codes = {item["code"] for item in issues}
        self.assertIn("MANIFEST_PAGE_EXECUTION_NOT_SINGLE_PAGE", codes)
        self.assertIn("MANIFEST_PAGE_APPROVAL_MISSING", codes)

    def test_batch_final_delivery_is_forbidden_for_high_fidelity_deck(self):
        module = load_validator()
        manifest = {
            "delivery_mode": "batch_final_deck",
            "fidelity_requirement": "high_fidelity",
            "slides": [
                {
                    "slide": 1,
                    "qa_expectations": {"visual_semantics_required": True},
                },
                {
                    "slide": 2,
                    "qa_expectations": {"visual_semantics_required": True},
                },
            ],
        }
        issues = module.validate_manifest(manifest)
        self.assertTrue(
            any(item["code"] == "MANIFEST_BATCH_FINAL_DELIVERY_FORBIDDEN" for item in issues)
        )

    def test_final_merge_cannot_regenerate_pages_and_requires_regression(self):
        module = load_validator()
        manifest = {
            "delivery_mode": "approved_single_page_merge",
            "slides": [
                {"slide": 1, "qa_expectations": {"visual_semantics_required": True}},
                {"slide": 2, "qa_expectations": {"visual_semantics_required": True}},
            ],
            "final_merge": {
                "method": "regenerate_full_deck",
                "regenerated_pages": True,
                "source_single_page_pptx": ["pages/slide-01.pptx"],
                "merge_regression_rendered": False,
                "merge_regression_pass": False,
            },
        }
        issues = module.validate_manifest(manifest)
        codes = {item["code"] for item in issues}
        self.assertIn("MANIFEST_FINAL_MERGE_REGENERATED_PAGES", codes)
        self.assertIn("MANIFEST_MERGE_REGRESSION_MISSING", codes)
        self.assertIn("MANIFEST_MERGE_REGRESSION_FAILED", codes)

    def test_visual_semantics_requires_visual_element_inventory(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "blueprint_reconstruction_plan": {
                "blueprint_path": "blueprints/slide-01.png",
                "canvas_size": "16:9",
                "background_color_sample": "#F3F4EF",
                "surface_system": "flat editorial page",
                "layout_regions": ["title", "main_chart", "so_what"],
                "header_footer_system": "source footer",
                "so_what_region": "bottom band",
                "main_chart_semantics": "line chart",
                "density_targets": "dense consulting page",
                "anchor_targets": ["title baseline", "chart origin"],
                "native_rebuild_targets": ["title", "chart", "so_what"],
                "allowed_visual_assets": [],
                "complex_visual_scan": {
                    "completed": True,
                    "complex_visual_candidates": ["line chart labels"],
                    "triggered_gates": ["spatial_registration"],
                    "pictures_zero_is_not_goal": True,
                },
            },
            "qa_expectations": {
                "visual_semantics_required": True,
            },
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        self.assertTrue(
            any(item["code"] == "MANIFEST_VISUAL_ELEMENT_INVENTORY_MISSING" for item in issues)
        )

    def test_visual_element_requires_priority(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "visual_element_inventory": [
                {
                    "id": "title_block",
                    "role": "title",
                    "measurement_mode": "individual_bbox",
                    "must_reproduce": True,
                    "blueprint_bbox_px": {"x": 90, "y": 64, "w": 800, "h": 72},
                    "ppt_target_bbox_in": {"x": 0.63, "y": 0.44, "w": 5.56, "h": 0.5},
                    "tolerance_px": 3,
                }
            ],
            "blueprint_reconstruction_plan": {
                "blueprint_path": "blueprints/slide-01.png",
                "canvas_size": "16:9",
                "background_color_sample": "#F3F4EF",
                "surface_system": "flat editorial page",
                "layout_regions": ["title", "main_chart", "so_what"],
                "header_footer_system": "source footer",
                "so_what_region": "bottom band",
                "main_chart_semantics": "line chart",
                "density_targets": "dense consulting page",
                "anchor_targets": ["title baseline", "chart origin"],
                "native_rebuild_targets": ["title", "chart", "so_what"],
                "allowed_visual_assets": [],
                "complex_visual_scan": {
                    "completed": True,
                    "complex_visual_candidates": ["line chart labels"],
                    "triggered_gates": ["spatial_registration"],
                    "pictures_zero_is_not_goal": True,
                },
                "blueprint_measurement_table": {
                    "blueprint_canvas_px": {"w": 1920, "h": 1080},
                    "ppt_canvas_in": {"w": 13.333, "h": 7.5},
                    "scale_x": 0.006944,
                    "scale_y": 0.006944,
                    "regions": [],
                },
            },
            "qa_expectations": {
                "visual_semantics_required": True,
            },
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        self.assertTrue(
            any(item["code"] == "MANIFEST_VISUAL_ELEMENT_PRIORITY_INVALID" for item in issues)
        )

    def test_p0_requires_individual_measurement(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "visual_element_inventory": [
                {
                    "id": "main_chart",
                    "priority": "P0",
                    "role": "main_chart",
                    "measurement_mode": "decoration_group",
                    "must_reproduce": True,
                }
            ],
            "blueprint_reconstruction_plan": {
                "blueprint_path": "blueprints/slide-01.png",
                "canvas_size": "16:9",
                "background_color_sample": "#F3F4EF",
                "surface_system": "flat editorial page",
                "layout_regions": ["title", "main_chart", "so_what"],
                "header_footer_system": "source footer",
                "so_what_region": "bottom band",
                "main_chart_semantics": "line chart",
                "density_targets": "dense consulting page",
                "anchor_targets": ["title baseline", "chart origin"],
                "native_rebuild_targets": ["title", "chart", "so_what"],
                "allowed_visual_assets": [],
                "complex_visual_scan": {
                    "completed": True,
                    "complex_visual_candidates": ["line chart labels"],
                    "triggered_gates": ["spatial_registration"],
                    "pictures_zero_is_not_goal": True,
                },
                "blueprint_measurement_table": {
                    "blueprint_canvas_px": {"w": 1920, "h": 1080},
                    "ppt_canvas_in": {"w": 13.333, "h": 7.5},
                    "scale_x": 0.006944,
                    "scale_y": 0.006944,
                    "regions": [],
                },
            },
            "qa_expectations": {
                "visual_semantics_required": True,
            },
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        codes = {item["code"] for item in issues}
        self.assertIn("MANIFEST_KEY_REGION_MEASUREMENT_MISSING", codes)
        self.assertIn("MANIFEST_VISUAL_ELEMENT_PRIORITY_DOWNGRADED", codes)

    def test_p2_requires_decoration_group_measurement(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "visual_element_inventory": [
                {
                    "id": "background_dot_pattern",
                    "priority": "P2",
                    "role": "micro_decoration",
                    "measurement_mode": "decoration_group",
                    "must_reproduce": True,
                    "group_bbox_px": {"x": 80, "y": 140, "w": 1760, "h": 820},
                    "color": "#D8DAD2",
                    "spacing_px": 12,
                }
            ],
            "blueprint_reconstruction_plan": {
                "blueprint_path": "blueprints/slide-01.png",
                "canvas_size": "16:9",
                "background_color_sample": "#F3F4EF",
                "surface_system": "flat editorial page",
                "layout_regions": ["title", "main_chart", "so_what"],
                "header_footer_system": "source footer",
                "so_what_region": "bottom band",
                "main_chart_semantics": "line chart",
                "density_targets": "dense consulting page",
                "anchor_targets": ["title baseline", "chart origin"],
                "native_rebuild_targets": ["title", "chart", "so_what"],
                "allowed_visual_assets": [],
                "complex_visual_scan": {
                    "completed": True,
                    "complex_visual_candidates": ["line chart labels"],
                    "triggered_gates": ["spatial_registration"],
                    "pictures_zero_is_not_goal": True,
                },
                "blueprint_measurement_table": {
                    "blueprint_canvas_px": {"w": 1920, "h": 1080},
                    "ppt_canvas_in": {"w": 13.333, "h": 7.5},
                    "scale_x": 0.006944,
                    "scale_y": 0.006944,
                    "regions": [],
                },
            },
            "qa_expectations": {
                "visual_semantics_required": True,
            },
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        self.assertTrue(
            any(item["code"] == "MANIFEST_DECORATION_GROUP_MEASUREMENT_MISSING" for item in issues)
        )

    def test_blueprint_measurement_requires_coordinate_mapping(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "visual_element_inventory": [
                {
                    "id": "title_block",
                    "priority": "P0",
                    "role": "title",
                    "measurement_mode": "individual_bbox",
                    "must_reproduce": True,
                    "blueprint_bbox_px": {"x": 90, "y": 64, "w": 800, "h": 72},
                    "ppt_target_bbox_in": {"x": 0.63, "y": 0.44, "w": 5.56, "h": 0.5},
                    "tolerance_px": 3,
                }
            ],
            "blueprint_reconstruction_plan": {
                "blueprint_path": "blueprints/slide-01.png",
                "canvas_size": "16:9",
                "background_color_sample": "#F3F4EF",
                "surface_system": "flat editorial page",
                "layout_regions": ["title", "main_chart", "so_what"],
                "header_footer_system": "source footer",
                "so_what_region": "bottom band",
                "main_chart_semantics": "line chart",
                "density_targets": "dense consulting page",
                "anchor_targets": ["title baseline", "chart origin"],
                "native_rebuild_targets": ["title", "chart", "so_what"],
                "allowed_visual_assets": [],
                "complex_visual_scan": {
                    "completed": True,
                    "complex_visual_candidates": ["line chart labels"],
                    "triggered_gates": ["spatial_registration"],
                    "pictures_zero_is_not_goal": True,
                },
                "blueprint_measurement_table": {
                    "regions": [],
                },
            },
            "qa_expectations": {
                "visual_semantics_required": True,
            },
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        self.assertTrue(
            any(item["code"] == "MANIFEST_COORDINATE_MAPPING_MISSING" for item in issues)
        )

    def test_spatial_registration_requires_numeric_bbox_delta_tolerance(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "qa_expectations": {
                "spatial_registration_required": True,
            },
            "spatial_registration_check": {
                "passed": True,
                "checked_groups": [
                    {
                        "id": "flow_node",
                        "status": "passed",
                        "anchor_points": [
                            {"item": "node_label", "anchor": "text_baseline_center"}
                        ],
                    }
                ],
            },
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        self.assertTrue(
            any(item["code"] == "MANIFEST_SPATIAL_NUMERIC_ANCHOR_MISSING" for item in issues)
        )

    def test_spatial_anchor_delta_over_tolerance_is_strict_failure(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "qa_expectations": {
                "spatial_registration_required": True,
            },
            "spatial_registration_check": {
                "passed": True,
                "checked_groups": [
                    {
                        "id": "flow_node",
                        "status": "passed",
                        "anchor_points": [
                            {
                                "item": "node_label",
                                "anchor": "text_baseline_center",
                                "blueprint_bbox_px": {"x": 100, "y": 100, "w": 120, "h": 28},
                                "render_bbox_px": {"x": 118, "y": 100, "w": 120, "h": 28},
                                "delta_px": {"x": 18, "y": 0, "w": 0, "h": 0},
                                "tolerance_px": 6,
                                "status": "passed",
                            }
                        ],
                    }
                ],
            },
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        self.assertTrue(
            any(item["code"] == "MANIFEST_SPATIAL_ANCHOR_DELTA_FAILED" for item in issues)
        )

    def test_visual_qa_requires_local_overlay_for_deliverable(self):
        module = load_validator()
        manifest = {
            "slides": [
                {
                    "slide": 1,
                    "qa_expectations": {"visual_qa_required": True},
                }
            ]
        }
        visual_qa = {
            "slides": [
                {
                    "slide": 1,
                    "surface_system_match": True,
                    "main_chart_semantics_match": True,
                    "visual_semantics_preserved": True,
                    "editable_information_layer_pass": True,
                    "spatial_registration_pass": True,
                    "curve_fidelity_pass": True,
                    "label_collision_pass": True,
                    "text_overflow_pass": True,
                    "container_overflow_pass": True,
                    "continuous_text_flow_pass": True,
                    "table_semantic_typography_pass": True,
                    "table_density_pass": True,
                    "blueprint_background_not_used": True,
                    "deliverable_allowed": True,
                    "blueprint_render_path": "blueprints/slide-01.png",
                    "ppt_render_path": "renders/slide-01.png",
                    "side_by_side_comparison_path": "qa/slide-01-side-by-side.png",
                    "visual_differences": [],
                    "evidence": {
                        "surface_system_match": {"checked": True},
                        "main_chart_semantics_match": {"checked": True},
                        "visual_semantics_preserved": {"checked": True},
                        "editable_information_layer_pass": {"checked": True},
                        "spatial_registration_pass": {"checked": True},
                        "curve_fidelity_pass": {"checked": True},
                        "label_collision_pass": {"checked": True},
                        "text_overflow_pass": {"checked": True},
                        "container_overflow_pass": {"checked": True},
                        "continuous_text_flow_pass": {"checked": True},
                        "table_semantic_typography_pass": {"checked": True},
                        "table_density_pass": {"checked": True},
                        "blueprint_background_not_used": {"checked": True},
                    },
                }
            ]
        }
        issues = module.validate_visual_qa(visual_qa, manifest)
        self.assertTrue(
            any(item["code"] == "VISUAL_QA_LOCAL_OVERLAY_MISSING" for item in issues)
        )

    def test_high_or_critical_visual_difference_blocks_delivery(self):
        module = load_validator()
        manifest = {
            "slides": [
                {
                    "slide": 1,
                    "qa_expectations": {"visual_qa_required": True},
                }
            ]
        }
        visual_qa = {
            "slides": [
                {
                    "slide": 1,
                    "surface_system_match": True,
                    "main_chart_semantics_match": True,
                    "visual_semantics_preserved": True,
                    "editable_information_layer_pass": True,
                    "spatial_registration_pass": True,
                    "curve_fidelity_pass": True,
                    "label_collision_pass": True,
                    "text_overflow_pass": True,
                    "container_overflow_pass": True,
                    "continuous_text_flow_pass": True,
                    "table_semantic_typography_pass": True,
                    "table_density_pass": True,
                    "blueprint_background_not_used": True,
                    "deliverable_allowed": True,
                    "blueprint_render_path": "blueprints/slide-01.png",
                    "ppt_render_path": "renders/slide-01.png",
                    "side_by_side_comparison_path": "qa/slide-01-side-by-side.png",
                    "local_overlay_artifacts": ["qa/slide-01-title-overlay.png"],
                    "measurement_evidence_path": "qa/slide-01-blueprint-measurement.json",
                    "spatial_numeric_check_path": "qa/slide-01-spatial-numeric-check.json",
                    "visual_differences": [
                        {
                            "region": "main_chart_area",
                            "severity": "High",
                            "description": "main chart shifted by 22px",
                            "accepted_by_user": False,
                            "requires_rework": True,
                        }
                    ],
                    "evidence": {
                        "surface_system_match": {"checked": True},
                        "main_chart_semantics_match": {"checked": True},
                        "visual_semantics_preserved": {"checked": True},
                        "editable_information_layer_pass": {"checked": True},
                        "spatial_registration_pass": {"checked": True},
                        "curve_fidelity_pass": {"checked": True},
                        "label_collision_pass": {"checked": True},
                        "text_overflow_pass": {"checked": True},
                        "container_overflow_pass": {"checked": True},
                        "continuous_text_flow_pass": {"checked": True},
                        "table_semantic_typography_pass": {"checked": True},
                        "table_density_pass": {"checked": True},
                        "blueprint_background_not_used": {"checked": True},
                    },
                }
            ]
        }
        issues = module.validate_visual_qa(visual_qa, manifest)
        self.assertTrue(
            any(item["code"] == "VISUAL_QA_UNACCEPTED_HIGH_DIFFERENCE" for item in issues)
        )

    def test_visual_semantics_requires_frozen_content_lock_and_component_signature(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "visual_element_registry": [
                {
                    "element_id": "title",
                    "priority": "P0",
                    "element_type": "text",
                    "source_component_id": "title_block",
                    "blueprint_bbox_px": {"x": 100, "y": 60, "w": 600, "h": 48},
                    "ppt_target_bbox_in": {"x": 0.69, "y": 0.42, "w": 4.17, "h": 0.33},
                    "render_bbox_px": {"x": 102, "y": 60, "w": 600, "h": 48},
                    "delta_px": {"x": 2, "y": 0, "w": 0, "h": 0},
                    "tolerance_px": 3,
                    "registration_status": "passed",
                }
            ],
            "blueprint_reconstruction_plan": {
                "blueprint_path": "blueprints/slide-01.png",
                "canvas_size": "16:9",
                "background_color_sample": "#F3F4EF",
                "surface_system": "flat editorial page",
                "layout_regions": ["title", "main_chart", "so_what"],
                "header_footer_system": "source footer",
                "so_what_region": "bottom band",
                "main_chart_semantics": "line chart",
                "density_targets": "dense consulting page",
                "anchor_targets": ["title baseline", "chart origin"],
                "native_rebuild_targets": ["title", "chart", "so_what"],
                "allowed_visual_assets": [],
                "complex_visual_scan": {
                    "completed": True,
                    "complex_visual_candidates": [],
                    "triggered_gates": [],
                    "native_only_rationale": "simple page",
                    "pictures_zero_is_not_goal": True,
                },
                "blueprint_measurement_table": {
                    "blueprint_canvas_px": {"w": 1920, "h": 1080},
                    "ppt_canvas_in": {"w": 13.333, "h": 7.5},
                    "scale_x": 0.006944,
                    "scale_y": 0.006944,
                    "regions": [],
                },
            },
            "qa_expectations": {
                "visual_semantics_required": True,
                "all_key_text_editable": True,
                "dual_gate_required": True,
                "visual_qa_required": True,
            },
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        codes = {item["code"] for item in issues}
        self.assertIn("CONTENT_LOCK_MISSING", codes)
        self.assertIn("COMPONENT_SIGNATURE_MISSING", codes)

    def test_visual_element_registry_requires_render_measurement_for_all_priorities(self):
        module = load_validator()
        metrics = {
            "pictures": 0,
            "max_picture_area_ratio": 0,
            "native_text_shapes": 1,
        }
        manifest_entry = {
            "slide": 1,
            "expected_pictures": 0,
            "image_assets": [],
            "slide_content_lock": {
                "path": "qa/slide-01-content-lock.json",
                "sha256": "a" * 64,
                "locked": True,
            },
            "blueprint_component_signature": {
                "path": "qa/slide-01-component-signature.json",
                "sha256": "b" * 64,
                "locked": True,
                "components": [
                    {
                        "id": "so_what_band",
                        "type": "four_item_icon_band",
                        "priority": "P0",
                        "required_subcomponents": ["icon_01", "title_01"],
                        "must_preserve_type": True,
                    }
                ],
            },
            "visual_element_registry": [
                {
                    "element_id": "decorative_rule",
                    "priority": "P2",
                    "element_type": "line",
                    "source_component_id": "so_what_band",
                    "blueprint_bbox_px": {"x": 100, "y": 900, "w": 900, "h": 2},
                    "ppt_target_bbox_in": {"x": 0.69, "y": 6.25, "w": 6.25, "h": 0.01},
                    "delta_px": {"x": 0, "y": 0, "w": 0, "h": 0},
                    "tolerance_px": 6,
                    "registration_status": "passed",
                }
            ],
            "blueprint_reconstruction_plan": {
                "blueprint_path": "blueprints/slide-01.png",
                "canvas_size": "16:9",
                "background_color_sample": "#F3F4EF",
                "surface_system": "flat editorial page",
                "layout_regions": ["title", "main_chart", "so_what"],
                "header_footer_system": "source footer",
                "so_what_region": "bottom band",
                "main_chart_semantics": "line chart",
                "density_targets": "dense consulting page",
                "anchor_targets": ["title baseline", "chart origin"],
                "native_rebuild_targets": ["title", "chart", "so_what"],
                "allowed_visual_assets": [],
                "complex_visual_scan": {
                    "completed": True,
                    "complex_visual_candidates": [],
                    "triggered_gates": [],
                    "native_only_rationale": "simple page",
                    "pictures_zero_is_not_goal": True,
                },
                "blueprint_measurement_table": {
                    "blueprint_canvas_px": {"w": 1920, "h": 1080},
                    "ppt_canvas_in": {"w": 13.333, "h": 7.5},
                    "scale_x": 0.006944,
                    "scale_y": 0.006944,
                    "regions": [],
                },
            },
            "qa_expectations": {
                "visual_semantics_required": True,
                "all_key_text_editable": True,
                "dual_gate_required": True,
                "visual_qa_required": True,
            },
        }
        issues = module.validate_manifest_slide(manifest_entry, metrics, 1)
        self.assertTrue(any(item["code"] == "RENDER_BBOX_MISSING" for item in issues))

    def test_visual_qa_empty_differences_requires_external_diff_evidence(self):
        module = load_validator()
        manifest = {
            "slides": [
                {
                    "slide": 1,
                    "qa_expectations": {"visual_qa_required": True},
                }
            ]
        }
        visual_qa = {
            "slides": [
                {
                    "slide": 1,
                    "surface_system_match": True,
                    "main_chart_semantics_match": True,
                    "visual_semantics_preserved": True,
                    "editable_information_layer_pass": True,
                    "spatial_registration_pass": True,
                    "curve_fidelity_pass": True,
                    "label_collision_pass": True,
                    "text_overflow_pass": True,
                    "container_overflow_pass": True,
                    "continuous_text_flow_pass": True,
                    "table_semantic_typography_pass": True,
                    "table_density_pass": True,
                    "blueprint_background_not_used": True,
                    "deliverable_allowed": True,
                    "blueprint_render_path": "blueprints/slide-01.png",
                    "ppt_render_path": "renders/slide-01.png",
                    "side_by_side_comparison_path": "qa/slide-01-side-by-side.png",
                    "local_overlay_artifacts": ["qa/slide-01-title-overlay.png"],
                    "measurement_evidence_path": "qa/slide-01-blueprint-measurement.json",
                    "spatial_numeric_check_path": "qa/slide-01-spatial-numeric-check.json",
                    "visual_differences": [],
                    "evidence": {
                        "surface_system_match": {"checked": True},
                        "main_chart_semantics_match": {"checked": True},
                        "visual_semantics_preserved": {"checked": True},
                        "editable_information_layer_pass": {"checked": True},
                        "spatial_registration_pass": {"checked": True},
                        "curve_fidelity_pass": {"checked": True},
                        "label_collision_pass": {"checked": True},
                        "text_overflow_pass": {"checked": True},
                        "container_overflow_pass": {"checked": True},
                        "continuous_text_flow_pass": {"checked": True},
                        "table_semantic_typography_pass": {"checked": True},
                        "table_density_pass": {"checked": True},
                        "blueprint_background_not_used": {"checked": True},
                    },
                }
            ]
        }
        issues = module.validate_visual_qa(visual_qa, manifest)
        self.assertTrue(
            any(
                item["code"] == "VISUAL_DIFFERENCES_EMPTY_WITHOUT_EXTERNAL_EVIDENCE"
                for item in issues
            )
        )


if __name__ == "__main__":
    unittest.main()
