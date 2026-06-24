# Quality Assurance

## Two-layer QA

### Static checks

Run `scripts/validate_pptx.py` and review:

- package and XML integrity;
- slide count and dimensions;
- 16:9 aspect ratio;
- elements beyond the slide canvas;
- placeholder text;
- full-slide image risk;
- native text, shape, chart, table, and image counts;
- coverage and low-density warnings.

Static checks are heuristic. A clean report does not prove the deck looks correct.

### Rendered visual checks

Render every slide to high-resolution PNG with PowerPoint, LibreOffice, or another faithful renderer. Inspect at full-page and normal reading size.

Check:

- unexpected right or bottom whitespace;
- clipping, overflow, and text wrapping;
- minimum readable type size;
- overlapping labels, legends, arrows, and shapes;
- chart labels obscuring data;
- inconsistent margins, title positions, and footers;
- weak contrast and excessive accent use;
- density differences between pages;
- style drift from the approved direction;
- missing sources, units, periods, or forecast labels;
- conclusions unsupported by visible evidence.

## Severity

| Severity | Meaning | Action |
|---|---|---|
| Critical | Wrong data, missing page, corrupted file, unreadable output | Stop delivery |
| High | Overflow, major overlap, wrong ratio, raster-only page | Fix before review |
| Medium | Weak hierarchy, excess whitespace, small labels, inconsistency | Fix in normal iteration |
| Low | Minor spacing or cosmetic refinement | Fix when it improves clarity |

## Iteration order

1. Correct data and missing content.
2. Correct canvas, overflow, and clipping.
3. Correct hierarchy and readability.
4. Correct chart labels and annotation.
5. Correct consistency and polish.

Re-render affected pages after every layout change. Re-run the structural validator after regenerating the PPTX.

## Third confirmation package

Provide:

- editable PPTX;
- full-deck rendered previews;
- structural QA summary;
- disclosed warnings or unresolved source conflicts;
- version and output paths.

Stop and request the third confirmation. Continue iterating until the user approves the final deck.
