# Editable PPT Production

## Lock geometry first

Set the slide size before placing content. Use one coordinate system consistently.

Common 16:9 dimensions:

- 13.333 × 7.5 inches
- 10 × 5.625 inches
- 12,192,000 × 6,858,000 EMU
- 9,144,000 × 5,143,500 EMU

Different sizes can share 16:9, but coordinates must match the chosen canvas.

## Native-element requirement

Build these as editable PowerPoint objects:

- titles and body text;
- conclusion and annotation boxes;
- tables;
- charts and data labels;
- arrows, process diagrams, matrices, and dividers;
- source notes and page numbers.

Use images for photography, illustration, textures, maps that cannot reasonably be rebuilt, and approved decorative assets. Do not flatten the entire slide into a screenshot.

## Blueprint-to-PPT production

Use confirmed ImageGen blueprints as visual references only. Before building each slide, write a brief production note:

- conclusion title;
- primary chart or analytical construct;
- supporting evidence blocks;
- interpretation text;
- business implication or SO WHAT;
- native editable element list;
- source note and footer requirements.

Build the PPT from that note and the evidence table, not from generated text in the blueprint.

## Chart standards

- Match chart type to the analytical question.
- Use the source evidence table for every value.
- Show units, periods, bases, and forecast markers.
- Direct-label important series when possible.
- Reduce gridlines and decoration that do not carry meaning.
- Use the accent color for the key comparison, not every series.
- Add a concise interpretation near the chart.
- Keep labels clear of lines, bars, and page edges.

## Table standards

- Use a clear reading direction and visible hierarchy.
- Minimize borders; emphasize headers, totals, exceptions, and decisions.
- Keep decimal precision consistent.
- Align numbers by decimal or right edge.
- State units in the header rather than repeating them in every cell.

## Text and hierarchy

- Use one conclusion title per content page.
- Keep body copy concise but sufficient to explain evidence.
- Avoid solving density by shrinking all text.
- Do not produce chart-only pages. Every content page needs enough explanatory text to show what the evidence proves and what decision it implies.
- For MBB-style or consulting report decks, default covers should be low-density and title-led. Do not add KPI blocks, dashboards, or data cards to the cover unless requested.
- Use consistent typography, indentation, bullet spacing, and source notes.
- Ensure contrast remains accessible on projectors and exported images.

## File handling

- Preserve the source files.
- Save versioned PPTX outputs.
- Keep generated references separate from final assets.
- Maintain editable chart data where the authoring library permits.
- Record external sources and assumptions.

## Production exit criteria

Before QA:

- all planned pages exist;
- titles match the confirmed storyline;
- figures match the evidence table;
- native elements remain editable;
- no generated placeholder wording remains;
- no content slide is only a chart skeleton without interpretation and implication;
- page geometry matches the selected visual system.
