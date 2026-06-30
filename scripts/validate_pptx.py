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
TYPOGRAPHY_MIN_PT = {
    "C0": 32.0,
    "T1": 14.0,
    "T2": 22.0,
    "T3": 10.0,
    "T4": 11.0,
    "T5": 7.5,
    "T6": 11.0,
    "T7": 9.5,
    "T8": 10.0,
    "T9": 10.0,
    "T10": 9.5,
    "T11": 7.5,
    "T12": 8.5,
    "T13": 18.0,
    "T14": 6.5,
}
GLOBAL_MIN_FONT_PT = 6.5
LARGE_IMAGE_AREA_RATIO = 0.40
FULL_SLIDE_IMAGE_RATIO = 0.90
TRACE_METHODS = {
    "pixel-boundary-sampling",
    "manual-control-point-overlay",
    "svg-path-tracing",
    "ppt-custom-geometry-tracing",
    "approved-local-crop",
}
TRACE_REQUIRED_FIELDS = ("trace_method", "trace_reference_crop", "trace_debug_artifact", "rendered_crop_comparison")
TRACE_ASSET_FIELDS = ("svg_asset", "asset_path", "custom_geometry_asset", "picture_asset")
GEOMETRY_ANALYSIS_REQUIRED_FIELDS = (
    "shape_type",
    "stroke_or_fill",
    "endpoint_summary",
    "width_behavior",
    "local_features",
    "reconstruction_decision",
)
CORE_CURVE_MIN_POINTS = 16
BLUEPRINT_RECONSTRUCTION_REQUIRED_FIELDS = (
    "blueprint_path",
    "canvas_size",
    "background_color_sample",
    "surface_system",
    "layout_regions",
    "header_footer_system",
    "so_what_region",
    "main_chart_semantics",
    "density_targets",
    "anchor_targets",
    "native_rebuild_targets",
    "allowed_visual_assets",
    "complex_visual_scan",
)
COMPLEX_VISUAL_SCAN_REQUIRED_FIELDS = (
    "completed",
    "complex_visual_candidates",
    "triggered_gates",
    "pictures_zero_is_not_goal",
)
PYTHON_PPTX_TOOL_NAMES = {"python-pptx", "python_pptx", "pythonpptx"}
VISUAL_QA_REQUIRED_FIELDS = (
    "surface_system_match",
    "main_chart_semantics_match",
    "visual_semantics_preserved",
    "editable_information_layer_pass",
    "spatial_registration_pass",
    "curve_fidelity_pass",
    "label_collision_pass",
    "text_overflow_pass",
    "container_overflow_pass",
    "continuous_text_flow_pass",
    "table_semantic_typography_pass",
    "table_density_pass",
    "blueprint_background_not_used",
    "deliverable_allowed",
)
TABLE_PROSE_SEMANTIC_ROLES = {
    "table_body",
    "table_action",
    "table_risk",
    "table_explanation",
    "table_recommendation",
    "table_paragraph",
    "table_sentence",
    "table_bullet",
}
TABLE_PROSE_ALLOWED_ROLES = {"T7", "T10"}
STRICT_FAILURE_CODES = {
    "FULL_SLIDE_BACKGROUND_RISK",
    "PICTURES_NOT_ALLOWED",
    "PICTURE_COUNT_MISMATCH",
    "UNJUSTIFIED_LARGE_IMAGE",
    "NO_NATIVE_TEXT_WITH_EDITABLE_TEXT_REQUIRED",
    "MANIFEST_SLIDE_MISSING",
    "MANIFEST_TYPOGRAPHY_INCOMPLETE",
    "MANIFEST_TEXT_OBJECT_INVALID",
    "MANIFEST_FONT_BELOW_SCALE",
    "MANIFEST_DUAL_GATE_INCOMPLETE",
    "FONT_SIZE_BELOW_FOOTER_MIN",
    "MANIFEST_TRACE_INCOMPLETE",
    "MANIFEST_TRACE_METHOD_INVALID",
    "MANIFEST_TRACE_GEOMETRY_ANALYSIS_MISSING",
    "MANIFEST_TRACE_GEOMETRY_ANALYSIS_INCOMPLETE",
    "MANIFEST_TRACE_ASSET_MISSING",
    "MANIFEST_TRACE_FILE_NOT_FOUND",
    "MANIFEST_TRACE_CURVES_MISSING",
    "MANIFEST_TRACE_CURVE_POINT_COUNT_MISSING",
    "MANIFEST_TRACE_CURVE_POINT_COUNT_TOO_LOW",
    "MANIFEST_LABEL_COLLISION_CHECK_MISSING",
    "MANIFEST_LABEL_COLLISION_FAILED",
    "MANIFEST_SPATIAL_REGISTRATION_CHECK_MISSING",
    "MANIFEST_SPATIAL_REGISTRATION_FAILED",
    "MANIFEST_SPATIAL_REGISTRATION_INCOMPLETE",
    "MANIFEST_CONTAINER_OVERFLOW_CHECK_MISSING",
    "MANIFEST_CONTAINER_OVERFLOW_FAILED",
    "MANIFEST_CONTAINER_OVERFLOW_INCOMPLETE",
    "MANIFEST_CONTINUOUS_TEXT_FLOW_CHECK_MISSING",
    "MANIFEST_CONTINUOUS_TEXT_FLOW_FAILED",
    "MANIFEST_CONTINUOUS_TEXT_FLOW_INCOMPLETE",
    "MANIFEST_TABLE_SEMANTIC_TYPOGRAPHY_MISSING",
    "MANIFEST_TABLE_SEMANTIC_TYPOGRAPHY_INVALID",
    "MANIFEST_TABLE_SEMANTIC_TYPOGRAPHY_FAILED",
    "MANIFEST_TABLE_DENSITY_CHECK_MISSING",
    "MANIFEST_TABLE_DENSITY_FAILED",
    "MANIFEST_TABLE_DENSITY_INCOMPLETE",
    "MANIFEST_BLUEPRINT_RECONSTRUCTION_PLAN_MISSING",
    "MANIFEST_BLUEPRINT_RECONSTRUCTION_PLAN_INCOMPLETE",
    "MANIFEST_VISUAL_COMPLEXITY_SCAN_MISSING",
    "MANIFEST_VISUAL_COMPLEXITY_SCAN_INCOMPLETE",
    "MANIFEST_PICTURES_ZERO_USED_AS_GOAL",
    "MANIFEST_GENERATION_ENGINE_MISSING",
    "MANIFEST_GENERATION_ENGINE_INCOMPLETE",
    "MANIFEST_PYTHON_PPTX_FALLBACK_UNJUSTIFIED",
    "VISUAL_QA_NOT_PROVIDED",
    "VISUAL_QA_INVALID",
    "VISUAL_QA_SLIDE_MISSING",
    "VISUAL_QA_FIELD_MISSING",
    "VISUAL_QA_CHECK_FAILED",
    "VISUAL_QA_DELIVERY_BLOCKED",
    "VISUAL_QA_EVIDENCE_MISSING",
    "VISUAL_QA_EVIDENCE_FILE_NOT_FOUND",
    "BLUEPRINT_RENDER_MISSING",
    "PPT_RENDER_MISSING",
    "SIDE_BY_SIDE_COMPARISON_MISSING",
    "VISUAL_PASS_WITHOUT_EVIDENCE",
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


def font_sizes_pt(element: ET.Element) -> list[float]:
    sizes: list[float] = []
    for node in element.findall(".//a:rPr", NS) + element.findall(".//a:defRPr", NS):
        raw_size = node.get("sz")
        if raw_size is None:
            continue
        try:
            size = int(raw_size) / 100
        except ValueError:
            continue
        if size > 0:
            sizes.append(size)
    return sizes


def load_manifest(path: str | Path) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    manifest_path = Path(path)
    if not manifest_path.exists():
        return None, [issue("MANIFEST_NOT_FOUND", f"Manifest file does not exist: {manifest_path}")]
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [issue("MANIFEST_INVALID_JSON", f"Cannot parse manifest JSON: {exc}")]
    if not isinstance(data, dict):
        return None, [issue("MANIFEST_INVALID_ROOT", "Manifest root must be a JSON object.")]
    if not isinstance(data.get("slides"), list):
        return None, [issue("MANIFEST_MISSING_SLIDES", "Manifest must contain a slides array.")]
    return data, []


def load_visual_qa(path: str | Path) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    visual_qa_path = Path(path)
    if not visual_qa_path.exists():
        return None, [issue("VISUAL_QA_NOT_FOUND", f"Visual QA file does not exist: {visual_qa_path}")]
    try:
        data = json.loads(visual_qa_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [issue("VISUAL_QA_INVALID", f"Cannot parse visual QA JSON: {exc}")]
    if not isinstance(data, dict):
        return None, [issue("VISUAL_QA_INVALID", "Visual QA root must be a JSON object.")]
    if not isinstance(data.get("slides"), list):
        return None, [issue("VISUAL_QA_INVALID", "Visual QA must contain a slides array.")]
    return data, []


def find_manifest_slide(manifest: dict[str, Any], slide_number: int) -> dict[str, Any] | None:
    for entry in manifest.get("slides", []):
        if isinstance(entry, dict) and entry.get("slide") == slide_number:
            return entry
    return None


def find_visual_qa_slide(visual_qa: dict[str, Any], slide_number: int) -> dict[str, Any] | None:
    for entry in visual_qa.get("slides", []):
        if isinstance(entry, dict) and entry.get("slide") == slide_number:
            return entry
    return None


def manifest_requires_visual_qa(manifest: dict[str, Any] | None) -> bool:
    if manifest is None:
        return False
    for entry in manifest.get("slides", []):
        if not isinstance(entry, dict):
            continue
        qa = entry.get("qa_expectations") if isinstance(entry.get("qa_expectations"), dict) else {}
        if qa.get("visual_qa_required") is True:
            return True
    return False


def manifest_ref_exists(value: Any, manifest_dir: Path | None = None) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    candidate = Path(value)
    if candidate.exists():
        return True
    if not candidate.is_absolute() and manifest_dir is not None:
        return (manifest_dir / candidate).exists()
    return False


def validate_manifest_slide(
    entry: dict[str, Any] | None,
    metrics: dict[str, Any],
    slide_number: int,
    manifest_dir: Path | None = None,
) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    if entry is None:
        return [
            issue(
                "MANIFEST_SLIDE_MISSING",
                "No slide_manifest.json entry exists for this slide.",
                slide=slide_number,
            )
        ]

    qa = entry.get("qa_expectations") if isinstance(entry.get("qa_expectations"), dict) else {}
    if qa.get("dual_gate_required") is not True:
        warnings.append(
            issue(
                "MANIFEST_DUAL_GATE_INCOMPLETE",
                "qa_expectations.dual_gate_required must be true so editability and visual semantics are enforced as co-equal gates.",
                slide=slide_number,
            )
        )
    if qa.get("visual_semantics_required") is not True:
        warnings.append(
            issue(
                "MANIFEST_DUAL_GATE_INCOMPLETE",
                "qa_expectations.visual_semantics_required must be true; editable structure cannot substitute for visual-semantic fidelity.",
                slide=slide_number,
            )
        )
    else:
        reconstruction_plan = entry.get("blueprint_reconstruction_plan")
        if not isinstance(reconstruction_plan, dict):
            warnings.append(
                issue(
                    "MANIFEST_BLUEPRINT_RECONSTRUCTION_PLAN_MISSING",
                    "visual_semantics_required=true requires a blueprint_reconstruction_plan before PPTX generation.",
                    slide=slide_number,
                )
            )
        else:
            missing_plan_fields = []
            for field in BLUEPRINT_RECONSTRUCTION_REQUIRED_FIELDS:
                field_value = reconstruction_plan.get(field)
                if field == "allowed_visual_assets":
                    if not isinstance(field_value, list):
                        missing_plan_fields.append(field)
                elif field == "complex_visual_scan":
                    if not isinstance(field_value, dict):
                        missing_plan_fields.append(field)
                elif field in {"layout_regions", "anchor_targets", "native_rebuild_targets"}:
                    if not isinstance(field_value, list) or not field_value:
                        missing_plan_fields.append(field)
                elif field_value in (None, "", [], {}):
                    missing_plan_fields.append(field)
            if missing_plan_fields:
                warnings.append(
                    issue(
                        "MANIFEST_BLUEPRINT_RECONSTRUCTION_PLAN_INCOMPLETE",
                        f"blueprint_reconstruction_plan is missing: {', '.join(missing_plan_fields)}.",
                        slide=slide_number,
                    )
                )
            complex_visual_scan = reconstruction_plan.get("complex_visual_scan")
            if not isinstance(complex_visual_scan, dict):
                warnings.append(
                    issue(
                        "MANIFEST_VISUAL_COMPLEXITY_SCAN_MISSING",
                        "blueprint_reconstruction_plan requires complex_visual_scan before choosing native-only reconstruction.",
                        slide=slide_number,
                    )
                )
            else:
                scan_missing_fields = []
                if complex_visual_scan.get("completed") is not True:
                    scan_missing_fields.append("completed")
                if not isinstance(complex_visual_scan.get("complex_visual_candidates"), list):
                    scan_missing_fields.append("complex_visual_candidates")
                if not isinstance(complex_visual_scan.get("triggered_gates"), list):
                    scan_missing_fields.append("triggered_gates")
                if "pictures_zero_is_not_goal" not in complex_visual_scan:
                    scan_missing_fields.append("pictures_zero_is_not_goal")
                if scan_missing_fields:
                    warnings.append(
                        issue(
                            "MANIFEST_VISUAL_COMPLEXITY_SCAN_INCOMPLETE",
                            "complex_visual_scan must record completion, complex candidates, triggered gates, and the pictures=0 non-goal assertion.",
                            slide=slide_number,
                        )
                    )
                if (
                    complex_visual_scan.get("pictures_zero_is_not_goal") is not True
                    or qa.get("pictures_zero_goal") is True
                    or entry.get("pictures_zero_goal") is True
                    or qa.get("target_pictures") == 0
                    or entry.get("target_pictures") == 0
                ):
                    warnings.append(
                        issue(
                            "MANIFEST_PICTURES_ZERO_USED_AS_GOAL",
                            "pictures=0 is not a third-stage goal and cannot justify avoiding asset, curve, or complex-visual gates.",
                            slide=slide_number,
                        )
                    )
                candidates = complex_visual_scan.get("complex_visual_candidates")
                triggered_gates = complex_visual_scan.get("triggered_gates")
                if (
                    isinstance(candidates, list)
                    and isinstance(triggered_gates, list)
                    and not candidates
                    and not triggered_gates
                    and not complex_visual_scan.get("native_only_rationale")
                ):
                    warnings.append(
                        issue(
                            "MANIFEST_VISUAL_COMPLEXITY_SCAN_INCOMPLETE",
                            "native-only reconstruction requires a rationale when no complex visual candidates or gates are found.",
                            slide=slide_number,
                        )
                    )
        generation_engine = entry.get("generation_engine")
        if not isinstance(generation_engine, dict):
            warnings.append(
                issue(
                    "MANIFEST_GENERATION_ENGINE_MISSING",
                    "visual_semantics_required=true requires generation_engine metadata.",
                    slide=slide_number,
                )
            )
        else:
            tool_name = str(generation_engine.get("tool", "")).strip().lower()
            if not tool_name or generation_engine.get("visual_fidelity_not_reduced") is not True:
                warnings.append(
                    issue(
                        "MANIFEST_GENERATION_ENGINE_INCOMPLETE",
                        "generation_engine must record the PPTX tool and assert that visual fidelity was not reduced.",
                        slide=slide_number,
                    )
                )
            if tool_name in PYTHON_PPTX_TOOL_NAMES and not generation_engine.get("fallback_reason"):
                warnings.append(
                    issue(
                        "MANIFEST_PYTHON_PPTX_FALLBACK_UNJUSTIFIED",
                        "python-pptx fallback requires a concrete reason; it cannot be chosen to simplify blueprint reconstruction.",
                        slide=slide_number,
                    )
                )
    if qa.get("all_key_text_editable") is not True:
        warnings.append(
            issue(
                "MANIFEST_DUAL_GATE_INCOMPLETE",
                "qa_expectations.all_key_text_editable must be true; visual fidelity cannot substitute for editable key information.",
                slide=slide_number,
            )
        )
    if qa.get("dual_gate_required") is True and qa.get("visual_qa_required") is not True:
        warnings.append(
            issue(
                "MANIFEST_DUAL_GATE_INCOMPLETE",
                "qa_expectations.visual_qa_required must be true when dual_gate_required is true.",
                slide=slide_number,
            )
        )
    expected_pictures = entry.get("expected_pictures")
    pictures_must_be_zero = qa.get("pictures_must_be_zero") is True or expected_pictures == 0
    if pictures_must_be_zero and metrics["pictures"] > 0:
        warnings.append(
            issue(
                "PICTURES_NOT_ALLOWED",
                "Manifest requires pictures=0, but the slide contains image assets.",
                slide=slide_number,
            )
        )
    elif isinstance(expected_pictures, int) and metrics["pictures"] != expected_pictures:
        warnings.append(
            issue(
                "PICTURE_COUNT_MISMATCH",
                f"Manifest expects {expected_pictures} picture(s), but the slide contains {metrics['pictures']}.",
                slide=slide_number,
            )
        )

    image_assets = entry.get("image_assets")
    has_declared_images = isinstance(image_assets, list) and len(image_assets) > 0
    if metrics["max_picture_area_ratio"] >= LARGE_IMAGE_AREA_RATIO and not has_declared_images:
        warnings.append(
            issue(
                "UNJUSTIFIED_LARGE_IMAGE",
                "A picture covers at least 40% of the slide, but manifest image_assets is empty.",
                slide=slide_number,
            )
        )

    if qa.get("all_key_text_editable") is True and metrics["native_text_shapes"] == 0:
        warnings.append(
            issue(
                "NO_NATIVE_TEXT_WITH_EDITABLE_TEXT_REQUIRED",
                "Manifest requires key text to be editable, but no native text shapes were found.",
                slide=slide_number,
            )
        )

    if qa.get("typography_scale_required") is True:
        text_objects = entry.get("text_objects")
        if not isinstance(text_objects, list) or not text_objects:
            warnings.append(
                issue(
                    "MANIFEST_TYPOGRAPHY_INCOMPLETE",
                    "Typography scale is required, but manifest text_objects is missing or empty.",
                    slide=slide_number,
                )
            )
        else:
            for index, text_object in enumerate(text_objects, start=1):
                if not isinstance(text_object, dict):
                    warnings.append(
                        issue(
                            "MANIFEST_TEXT_OBJECT_INVALID",
                            f"text_objects[{index}] must be an object.",
                            slide=slide_number,
                        )
                    )
                    continue
                role = text_object.get("role")
                size = text_object.get("font_size_pt")
                if role not in TYPOGRAPHY_MIN_PT or not isinstance(size, (int, float)):
                    warnings.append(
                        issue(
                            "MANIFEST_TYPOGRAPHY_INCOMPLETE",
                            f"text_objects[{index}] must include a valid role and font_size_pt.",
                            slide=slide_number,
                        )
                    )
                    continue
                min_size = TYPOGRAPHY_MIN_PT[role]
                if float(size) < min_size:
                    warnings.append(
                        issue(
                            "MANIFEST_FONT_BELOW_SCALE",
                            f"text_objects[{index}] role {role} is {size}pt; minimum is {min_size}pt.",
                            slide=slide_number,
                        )
                    )

    for collection_name in ("image_assets", "native_components"):
        collection = entry.get(collection_name)
        if not isinstance(collection, list):
            continue
        for index, component in enumerate(collection, start=1):
            if not isinstance(component, dict) or component.get("trace_required") is not True:
                continue

            missing = [field for field in TRACE_REQUIRED_FIELDS if not component.get(field)]
            if missing:
                warnings.append(
                    issue(
                        "MANIFEST_TRACE_INCOMPLETE",
                        f"{collection_name}[{index}] has trace_required=true but is missing: {', '.join(missing)}.",
                        slide=slide_number,
                    )
                )

            method = component.get("trace_method")
            if method and method not in TRACE_METHODS:
                warnings.append(
                    issue(
                        "MANIFEST_TRACE_METHOD_INVALID",
                        f"{collection_name}[{index}] uses trace_method '{method}', expected one of: {', '.join(sorted(TRACE_METHODS))}.",
                        slide=slide_number,
                    )
                )

            geometry_analysis = component.get("geometry_analysis")
            if not isinstance(geometry_analysis, dict):
                warnings.append(
                    issue(
                        "MANIFEST_TRACE_GEOMETRY_ANALYSIS_MISSING",
                        f"{collection_name}[{index}] has trace_required=true but geometry_analysis is missing.",
                        slide=slide_number,
                    )
                )
            else:
                missing_geometry = [
                    field
                    for field in GEOMETRY_ANALYSIS_REQUIRED_FIELDS
                    if not geometry_analysis.get(field)
                ]
                if missing_geometry:
                    warnings.append(
                        issue(
                            "MANIFEST_TRACE_GEOMETRY_ANALYSIS_INCOMPLETE",
                            f"{collection_name}[{index}].geometry_analysis is missing: {', '.join(missing_geometry)}.",
                            slide=slide_number,
                        )
                    )

            if not any(component.get(field) for field in TRACE_ASSET_FIELDS):
                warnings.append(
                    issue(
                        "MANIFEST_TRACE_ASSET_MISSING",
                        f"{collection_name}[{index}] has trace_required=true but no traced asset path is declared.",
                        slide=slide_number,
                    )
                )

            for field in (*TRACE_REQUIRED_FIELDS[1:], *TRACE_ASSET_FIELDS):
                value = component.get(field)
                if value and not manifest_ref_exists(value, manifest_dir):
                    warnings.append(
                        issue(
                            "MANIFEST_TRACE_FILE_NOT_FOUND",
                            f"{collection_name}[{index}] declares {field}='{value}', but the file was not found.",
                            slide=slide_number,
                        )
                    )

            if component.get("curve_fidelity_required") is True:
                curves = component.get("trace_curves")
                if not isinstance(curves, list) or not curves:
                    warnings.append(
                        issue(
                            "MANIFEST_TRACE_CURVES_MISSING",
                            f"{collection_name}[{index}] has curve_fidelity_required=true but trace_curves is missing or empty.",
                            slide=slide_number,
                        )
                    )
                else:
                    for curve_index, curve in enumerate(curves, start=1):
                        if not isinstance(curve, dict):
                            warnings.append(
                                issue(
                                    "MANIFEST_TRACE_CURVE_POINT_COUNT_MISSING",
                                    f"{collection_name}[{index}].trace_curves[{curve_index}] must be an object.",
                                    slide=slide_number,
                                )
                            )
                            continue
                        point_count = curve.get("point_count")
                        min_required = curve.get(
                            "min_required_point_count",
                            component.get("min_required_point_count", CORE_CURVE_MIN_POINTS),
                        )
                        if not isinstance(point_count, int) or not isinstance(min_required, int):
                            warnings.append(
                                issue(
                                    "MANIFEST_TRACE_CURVE_POINT_COUNT_MISSING",
                                    f"{collection_name}[{index}].trace_curves[{curve_index}] must include integer point_count and min_required_point_count.",
                                    slide=slide_number,
                                )
                            )
                            continue
                        if point_count < min_required:
                            warnings.append(
                                issue(
                                    "MANIFEST_TRACE_CURVE_POINT_COUNT_TOO_LOW",
                                    f"{collection_name}[{index}].trace_curves[{curve_index}] has {point_count} point(s); minimum is {min_required}.",
                                    slide=slide_number,
                                )
                            )

    if qa.get("label_collision_check_required") is True:
        label_check = entry.get("label_collision_check")
        if not isinstance(label_check, dict):
            warnings.append(
                issue(
                    "MANIFEST_LABEL_COLLISION_CHECK_MISSING",
                    "Manifest requires label collision check, but label_collision_check is missing.",
                    slide=slide_number,
                )
            )
        elif label_check.get("passed") is not True:
            warnings.append(
                issue(
                    "MANIFEST_LABEL_COLLISION_FAILED",
                    "Manifest label_collision_check did not pass.",
                    slide=slide_number,
                )
            )

    if qa.get("spatial_registration_required") is True:
        spatial_check = entry.get("spatial_registration_check")
        if not isinstance(spatial_check, dict):
            warnings.append(
                issue(
                    "MANIFEST_SPATIAL_REGISTRATION_CHECK_MISSING",
                    "Manifest requires spatial registration check, but spatial_registration_check is missing.",
                    slide=slide_number,
                )
            )
        elif spatial_check.get("passed") is not True:
            warnings.append(
                issue(
                    "MANIFEST_SPATIAL_REGISTRATION_FAILED",
                    "Manifest spatial_registration_check did not pass.",
                    slide=slide_number,
                )
            )
        else:
            checked_groups = spatial_check.get("checked_groups")
            if not isinstance(checked_groups, list) or not checked_groups:
                warnings.append(
                    issue(
                        "MANIFEST_SPATIAL_REGISTRATION_INCOMPLETE",
                        "spatial_registration_check must include non-empty checked_groups.",
                        slide=slide_number,
                    )
                )
            else:
                for group_index, group in enumerate(checked_groups, start=1):
                    if not isinstance(group, dict):
                        warnings.append(
                            issue(
                                "MANIFEST_SPATIAL_REGISTRATION_INCOMPLETE",
                                f"spatial_registration_check.checked_groups[{group_index}] must be an object.",
                                slide=slide_number,
                            )
                        )
                        continue
                    if group.get("status") != "passed":
                        warnings.append(
                            issue(
                                "MANIFEST_SPATIAL_REGISTRATION_FAILED",
                                f"spatial_registration_check.checked_groups[{group_index}] status must be exactly 'passed'.",
                                slide=slide_number,
                            )
                        )
                    anchor_points = group.get("anchor_points")
                    if not isinstance(anchor_points, list) or not anchor_points:
                        warnings.append(
                            issue(
                                "MANIFEST_SPATIAL_REGISTRATION_INCOMPLETE",
                                f"spatial_registration_check.checked_groups[{group_index}] must include anchor_points for individual nodes/icons/labels/arrows.",
                                slide=slide_number,
                            )
                        )
                        continue
                    has_text_anchor = any(
                        isinstance(anchor, dict)
                        and isinstance(anchor.get("anchor"), str)
                        and ("label" in str(anchor.get("item", "")).lower()
                             or "text" in str(anchor.get("item", "")).lower()
                             or "baseline" in anchor.get("anchor", ""))
                        for anchor in anchor_points
                    )
                    if not has_text_anchor:
                        warnings.append(
                            issue(
                                "MANIFEST_SPATIAL_REGISTRATION_INCOMPLETE",
                                f"spatial_registration_check.checked_groups[{group_index}] must include at least one text/label baseline anchor.",
                                slide=slide_number,
                            )
                        )

    if qa.get("container_overflow_check_required") is True:
        overflow_check = entry.get("container_overflow_check")
        if not isinstance(overflow_check, dict):
            warnings.append(
                issue(
                    "MANIFEST_CONTAINER_OVERFLOW_CHECK_MISSING",
                    "Manifest requires container overflow check, but container_overflow_check is missing.",
                    slide=slide_number,
                )
            )
        elif overflow_check.get("passed") is not True:
            warnings.append(
                issue(
                    "MANIFEST_CONTAINER_OVERFLOW_FAILED",
                    "Manifest container_overflow_check did not pass.",
                    slide=slide_number,
                )
            )
        elif not isinstance(overflow_check.get("checked_regions"), list) or not overflow_check.get("checked_regions"):
            warnings.append(
                issue(
                    "MANIFEST_CONTAINER_OVERFLOW_INCOMPLETE",
                    "container_overflow_check must include non-empty checked_regions.",
                    slide=slide_number,
                )
            )

    if qa.get("continuous_text_flow_check_required") is True:
        flow_check = entry.get("continuous_text_flow_check")
        if not isinstance(flow_check, dict):
            warnings.append(
                issue(
                    "MANIFEST_CONTINUOUS_TEXT_FLOW_CHECK_MISSING",
                    "Manifest requires continuous text flow check, but continuous_text_flow_check is missing.",
                    slide=slide_number,
                )
            )
        elif flow_check.get("passed") is not True:
            warnings.append(
                issue(
                    "MANIFEST_CONTINUOUS_TEXT_FLOW_FAILED",
                    "Manifest continuous_text_flow_check did not pass.",
                    slide=slide_number,
                )
            )
        elif not isinstance(flow_check.get("checked_text_runs"), list) or not flow_check.get("checked_text_runs"):
            warnings.append(
                issue(
                    "MANIFEST_CONTINUOUS_TEXT_FLOW_INCOMPLETE",
                    "continuous_text_flow_check must include non-empty checked_text_runs.",
                    slide=slide_number,
                )
            )

    if qa.get("table_semantic_typography_required") is True:
        table_text_objects = entry.get("table_text_objects")
        if not isinstance(table_text_objects, list) or not table_text_objects:
            warnings.append(
                issue(
                    "MANIFEST_TABLE_SEMANTIC_TYPOGRAPHY_MISSING",
                    "Manifest requires table semantic typography, but table_text_objects is missing or empty.",
                    slide=slide_number,
                )
            )
        else:
            for index, table_text in enumerate(table_text_objects, start=1):
                if not isinstance(table_text, dict):
                    warnings.append(
                        issue(
                            "MANIFEST_TABLE_SEMANTIC_TYPOGRAPHY_INVALID",
                            f"table_text_objects[{index}] must be an object.",
                            slide=slide_number,
                        )
                    )
                    continue
                semantic_role = table_text.get("semantic_role")
                role = table_text.get("role")
                size = table_text.get("font_size_pt")
                if not isinstance(semantic_role, str) or role not in TYPOGRAPHY_MIN_PT or not isinstance(size, (int, float)):
                    warnings.append(
                        issue(
                            "MANIFEST_TABLE_SEMANTIC_TYPOGRAPHY_INVALID",
                            f"table_text_objects[{index}] must include semantic_role, valid role, and font_size_pt.",
                            slide=slide_number,
                        )
                    )
                    continue
                if semantic_role in TABLE_PROSE_SEMANTIC_ROLES and role not in TABLE_PROSE_ALLOWED_ROLES:
                    warnings.append(
                        issue(
                            "MANIFEST_TABLE_SEMANTIC_TYPOGRAPHY_FAILED",
                            f"table_text_objects[{index}] semantic_role '{semantic_role}' must use T7 or T10, not {role}.",
                            slide=slide_number,
                        )
                    )
                min_size = TYPOGRAPHY_MIN_PT[role]
                if float(size) < min_size:
                    warnings.append(
                        issue(
                            "MANIFEST_TABLE_SEMANTIC_TYPOGRAPHY_FAILED",
                            f"table_text_objects[{index}] role {role} is {size}pt; minimum is {min_size}pt.",
                            slide=slide_number,
                        )
                    )

    if qa.get("table_density_check_required") is True:
        density_check = entry.get("table_density_check")
        if not isinstance(density_check, dict):
            warnings.append(
                issue(
                    "MANIFEST_TABLE_DENSITY_CHECK_MISSING",
                    "Manifest requires table density check, but table_density_check is missing.",
                    slide=slide_number,
                )
            )
        elif density_check.get("passed") is not True:
            warnings.append(
                issue(
                    "MANIFEST_TABLE_DENSITY_FAILED",
                    "Manifest table_density_check did not pass.",
                    slide=slide_number,
                )
            )
        elif not isinstance(density_check.get("checked_cells"), list) or not density_check.get("checked_cells"):
            warnings.append(
                issue(
                    "MANIFEST_TABLE_DENSITY_INCOMPLETE",
                    "table_density_check must include non-empty checked_cells.",
                    slide=slide_number,
                )
            )

    return warnings


def validate_visual_qa(
    visual_qa: dict[str, Any] | None,
    manifest: dict[str, Any] | None,
    visual_qa_dir: Path | None = None,
) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    if manifest is None or not manifest_requires_visual_qa(manifest):
        return warnings
    if visual_qa is None:
        return [issue("VISUAL_QA_NOT_PROVIDED", "visual_qa_gate.json is required but was not provided.")]

    for manifest_entry in manifest.get("slides", []):
        if not isinstance(manifest_entry, dict):
            continue
        qa = manifest_entry.get("qa_expectations") if isinstance(manifest_entry.get("qa_expectations"), dict) else {}
        if qa.get("visual_qa_required") is not True:
            continue
        slide_number = manifest_entry.get("slide")
        if not isinstance(slide_number, int):
            continue
        entry = find_visual_qa_slide(visual_qa, slide_number)
        if entry is None:
            warnings.append(
                issue(
                    "VISUAL_QA_SLIDE_MISSING",
                    "visual_qa_gate.json has no entry for a slide that requires visual QA.",
                    slide=slide_number,
                )
            )
            continue
        for field in VISUAL_QA_REQUIRED_FIELDS:
            if field not in entry:
                warnings.append(
                    issue(
                        "VISUAL_QA_FIELD_MISSING",
                        f"visual_qa_gate.json slide entry is missing '{field}'.",
                        slide=slide_number,
                    )
                )
                continue
            if not isinstance(entry.get(field), bool):
                warnings.append(
                    issue(
                        "VISUAL_QA_INVALID",
                        f"visual_qa_gate.json field '{field}' must be boolean.",
                        slide=slide_number,
                    )
                )

        failed_fields = [
            field
            for field in VISUAL_QA_REQUIRED_FIELDS
            if field != "deliverable_allowed" and entry.get(field) is False
        ]
        if failed_fields:
            warnings.append(
                issue(
                    "VISUAL_QA_CHECK_FAILED",
                    f"Visual QA failed fields: {', '.join(failed_fields)}.",
                    slide=slide_number,
                )
            )
        if entry.get("deliverable_allowed") is not True:
            warnings.append(
                issue(
                    "VISUAL_QA_DELIVERY_BLOCKED",
                    "visual_qa_gate.json does not allow delivery for this slide.",
                    slide=slide_number,
                )
            )
        if failed_fields and entry.get("deliverable_allowed") is True:
            warnings.append(
                issue(
                    "VISUAL_QA_INVALID",
                    "deliverable_allowed cannot be true when any visual QA field failed.",
                    slide=slide_number,
                )
            )

        if entry.get("deliverable_allowed") is True:
            delivery_artifacts = (
                ("blueprint_render_path", "BLUEPRINT_RENDER_MISSING"),
                ("ppt_render_path", "PPT_RENDER_MISSING"),
                ("side_by_side_comparison_path", "SIDE_BY_SIDE_COMPARISON_MISSING"),
            )
            for artifact_field, code in delivery_artifacts:
                artifact_value = entry.get(artifact_field)
                if not manifest_ref_exists(artifact_value, visual_qa_dir):
                    warnings.append(
                        issue(
                            code,
                            f"deliverable_allowed=true requires an existing {artifact_field}.",
                            slide=slide_number,
                        )
                    )

            visual_differences = entry.get("visual_differences")
            if not isinstance(visual_differences, list):
                warnings.append(
                    issue(
                        "VISUAL_QA_EVIDENCE_MISSING",
                        "deliverable_allowed=true requires visual_differences to be recorded as a list, even when empty.",
                        slide=slide_number,
                    )
                )

        evidence = entry.get("evidence")
        if not isinstance(evidence, dict):
            evidence = {}
        for field in VISUAL_QA_REQUIRED_FIELDS:
            if field == "deliverable_allowed" or entry.get(field) is not True:
                continue
            field_evidence = evidence.get(field)
            if field_evidence in (None, "", [], {}):
                warnings.append(
                    issue(
                        "VISUAL_PASS_WITHOUT_EVIDENCE",
                        f"visual_qa_gate.json field '{field}' is true but has no evidence entry.",
                        slide=slide_number,
                    )
                )
                continue
            if isinstance(field_evidence, str) and not manifest_ref_exists(field_evidence, visual_qa_dir):
                warnings.append(
                    issue(
                        "VISUAL_QA_EVIDENCE_FILE_NOT_FOUND",
                        f"visual_qa_gate.json evidence for '{field}' was not found: {field_evidence}.",
                        slide=slide_number,
                    )
                )

    return warnings


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
    slide_area = max(width * height, 1)
    font_sizes = [size for shape in shapes for size in font_sizes_pt(shape)]
    picture_area_ratios: list[float] = []

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

    for picture in pictures:
        box = shape_bounds(picture)
        if box is None:
            continue
        _, _, cx, cy = box
        ratio = max(0.0, (cx * cy) / slide_area)
        picture_area_ratios.append(ratio)
        if ratio >= FULL_SLIDE_IMAGE_RATIO:
            warnings.append(
                issue(
                    "FULL_SLIDE_BACKGROUND_RISK",
                    "A single image covers at least 90% of the slide; this is treated as a full-slide background risk even if native text exists.",
                    slide=slide_number,
                )
            )
        elif ratio >= LARGE_IMAGE_AREA_RATIO:
            warnings.append(
                issue(
                    "LARGE_IMAGE_ASSET",
                    "A single image covers at least 40% of the slide and must be justified in slide_manifest.json.",
                    slide=slide_number,
                )
            )

    total_picture_area_ratio = round(min(sum(picture_area_ratios), 1.0), 4)
    max_picture_area_ratio = round(max(picture_area_ratios, default=0.0), 4)
    if total_picture_area_ratio >= LARGE_IMAGE_AREA_RATIO:
        warnings.append(
            issue(
                "HIGH_TOTAL_IMAGE_AREA",
                "Images cover at least 40% of the slide in total and must be justified in slide_manifest.json.",
                slide=slide_number,
            )
        )

    if font_sizes:
        min_font_size = min(font_sizes)
        max_font_size = max(font_sizes)
        if min_font_size < GLOBAL_MIN_FONT_PT:
            warnings.append(
                issue(
                    "FONT_SIZE_BELOW_FOOTER_MIN",
                    f"A native text run is {min_font_size:.1f}pt; global minimum is {GLOBAL_MIN_FONT_PT:.1f}pt.",
                    slide=slide_number,
                )
            )
    else:
        min_font_size = None
        max_font_size = None

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
        "picture_area_ratio": total_picture_area_ratio,
        "max_picture_area_ratio": max_picture_area_ratio,
        "min_font_size_pt": round(min_font_size, 2) if min_font_size is not None else None,
        "max_font_size_pt": round(max_font_size, 2) if max_font_size is not None else None,
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


def promote_strict_failures(report: dict[str, Any]) -> None:
    existing = {(item.get("code"), item.get("slide"), item.get("message")) for item in report["errors"]}
    for warning in report["warnings"]:
        if warning.get("code") not in STRICT_FAILURE_CODES:
            continue
        key = (warning.get("code"), warning.get("slide"), warning.get("message"))
        if key in existing:
            continue
        failure = dict(warning)
        failure["strict_failure"] = True
        report["errors"].append(failure)
        existing.add(key)


def validate_pptx(
    path: str | Path,
    manifest_path: str | Path | None = None,
    visual_qa_path: str | Path | None = None,
    *,
    strict: bool = False,
) -> dict[str, Any]:
    source = Path(path)
    report = empty_report(source)
    manifest: dict[str, Any] | None = None
    visual_qa: dict[str, Any] | None = None
    if manifest_path is not None:
        manifest, manifest_errors = load_manifest(manifest_path)
        report["manifest"] = {
            "file": str(Path(manifest_path)),
            "loaded": manifest is not None,
            "slide_entries": len(manifest.get("slides", [])) if manifest else 0,
        }
        report["errors"].extend(manifest_errors)
        if manifest is None:
            return report

    if visual_qa_path is not None:
        visual_qa, visual_qa_errors = load_visual_qa(visual_qa_path)
        report["visual_qa"] = {
            "file": str(Path(visual_qa_path)),
            "loaded": visual_qa is not None,
            "slide_entries": len(visual_qa.get("slides", [])) if visual_qa else 0,
        }
        report["errors"].extend(visual_qa_errors)
    elif manifest_requires_visual_qa(manifest):
        report["warnings"].append(
            issue("VISUAL_QA_NOT_PROVIDED", "visual_qa_gate.json is required by manifest but --visual-qa was not provided.")
        )

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
                if manifest is not None:
                    manifest_entry = find_manifest_slide(manifest, slide_number)
                    manifest_dir = Path(manifest_path).parent if manifest_path is not None else None
                    report["warnings"].extend(
                        validate_manifest_slide(manifest_entry, metrics, slide_number, manifest_dir)
                    )

            report["summary"]["slide_count"] = len(slide_names)
            for field in (
                "native_text_shapes",
                "native_graphic_shapes",
                "pictures",
                "charts",
                "tables",
            ):
                report["summary"][field] = sum(slide[field] for slide in report["slides"])

            visual_qa_dir = Path(visual_qa_path).parent if visual_qa_path is not None else None
            report["warnings"].extend(validate_visual_qa(visual_qa, manifest, visual_qa_dir))
    except zipfile.BadZipFile:
        report["errors"].append(issue("INVALID_PPTX_ZIP", "File is not a readable PPTX ZIP package."))
    except (ET.ParseError, KeyError, ValueError) as exc:
        report["errors"].append(issue("INVALID_PACKAGE_XML", str(exc)))

    if strict:
        promote_strict_failures(report)

    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check PPTX structure, aspect ratio, editability, placeholders, and layout risks."
    )
    parser.add_argument("pptx", help="Path to the PPTX file")
    parser.add_argument("--manifest", help="CyberPPT stage 3 slide_manifest.json")
    parser.add_argument("--visual-qa", help="CyberPPT stage 3 visual_qa_gate.json")
    parser.add_argument("--strict", action="store_true", help="Promote CyberPPT hard-rule violations to errors")
    parser.add_argument("--json-out", help="Optional path for a UTF-8 JSON report")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = validate_pptx(
        args.pptx,
        manifest_path=args.manifest,
        visual_qa_path=args.visual_qa,
        strict=args.strict,
    )
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_out:
        output = Path(args.json_out)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
