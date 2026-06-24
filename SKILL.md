---
name: cyber-ppt
description: Use when turning DOCX, PDF, TXT, XLSX, research reports, business materials, or raw data into a high-density editable consulting presentation, or when a PPT needs SCR structure, visual style exploration, detailed charts, and rendered quality assurance.
---

# CyberPPT

## Overview

Turn source material into an evidence-based, conclusion-led, editable consulting deck. Preserve traceability, enforce three user approvals, and judge completion from rendered slides rather than file generation alone.

## Mandatory workflow

| Phase | Required output | Stop condition | Read |
|---|---|---|---|
| 1. Analyze | Evidence table, conflicts, SCR, page outline, chart plan | **First confirmation:** approve storyline and outline | `references/source-analysis.md`, `references/storyline.md` |
| 2. Explore | Five distinct, separate, full-slide 16:9 visual samples | **Second confirmation:** choose visual direction | `references/visual-system.md` |
| 3. Produce | Editable PPTX, full-deck renders, QA report | **Third confirmation:** approve final deck | `references/ppt-production.md`, `references/quality-assurance.md` |

Do not continue past a gate without explicit approval. If the user requests changes, revise that phase and request confirmation again.

## Non-negotiable controls

- Derive facts and numbers from source material. Never fabricate missing evidence.
- Record inconsistent source values or calculations; do not silently normalize them.
- Use SCR across the deck and a defensible conclusion as each content-slide title.
- Generate five style directions by default. Create each as its own complete 16:9 image; never use a collage, contact sheet, or compressed multi-slide canvas.
- Skip ImageGen only when the user explicitly requests it. Record the decision and use the supplied template, reference, or visual specification.
- Treat ImageGen text and numbers as unreliable. Use generated images only for visual composition and art direction.
- Build final titles, text, shapes, tables, and charts as native editable PowerPoint elements. Do not use full-slide screenshots as a shortcut.
- Lock the slide dimensions before layout. Keep the coordinate system, visual references, renders, and output at the same aspect ratio.
- Render every slide and inspect the full deck. File creation, compilation, or XML validity alone does not prove visual quality.

## Production and validation

Use the most suitable presentation tooling available. Preserve the original sources and output versioned files.

Run the structural validator:

```powershell
python scripts/validate_pptx.py path/to/deck.pptx --json-out path/to/report.json
```

Treat validator warnings as review prompts, not absolute visual judgments. Inspect rendered pages for whitespace imbalance, small type, clipping, overlaps, chart-label collisions, weak hierarchy, and style drift.

## Common failures

- Combining style samples to save time destroys 16:9 judgment.
- Shrinking type is not a valid substitute for restructuring content.
- Matching only colors does not reproduce a visual system; match grid, density, hierarchy, chart language, and spacing.
- Copying generated labels corrupts evidence.
- Using a 10×5.625 coordinate plan on a 13.333×7.5 canvas creates right/bottom whitespace.
- Checking only the first slide misses repeated layout and label failures.
