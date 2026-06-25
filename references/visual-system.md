# Visual System and ImageGen Exploration

## Default palette exploration

When no brand palette is supplied, show the eight fixed CyberPPT palette options first. Recommend one based on the source material, but do not force the choice.

| Option | Name | Colors | Best fit |
|---|---|---|---|
| 1 | Classic deep-red consulting | background `#F3F4EF`; title/body `#111111`; secondary `#555555`; line `#D6D6D2`; accent `#8B1E1E` | strategy, competitor analysis, industry research, business plans |
| 2 | Cool gray + burgundy | background `#F5F5F2`; title `#000000`; body `#151515`; secondary `#6B6B6B`; line `#D9D9D6`; accent `#7A1F2B` | finance, investment research, consulting, risk analysis |
| 3 | Warm ivory + dark wine | background `#F4F1EA`; title `#121212`; body `#2B2B2B`; secondary `#77736C`; line `#D8D3CA`; accent `#8A1538` | brand strategy, consumer goods, e-commerce, user research |
| 4 | Ivory + navy accent | background `#F7F6F0`; title `#101820`; body `#303030`; secondary `#6F7275`; line `#C9CDD1`; accent `#12355B` | technology, SaaS, B2B, enterprise digitalization, AI Agent reports |
| 5 | Light gray-white + dark green | background `#F2F3EF`; title `#111111`; body `#333333`; secondary `#666666`; line `#D7D9D3`; accent `#1F5B4D` | sustainability, overseas markets, growth strategy, long-term trends |
| 6 | Paper beige + copper brown | background `#F4F0E8`; title `#161616`; body `#2F2F2F`; secondary `#76716A`; line `#B8B6B1` / `#D8D5CE`; accent `#9A5A2E` | consumer, retail, luxury, business model analysis |
| 7 | Clean light gray + black-gold | background `#F6F6F4`; title `#000000`; body `#252525`; secondary `#707070`; line `#DADADA`; accent `#A87932` | executive briefings, financing decks, annual strategy, board materials |
| 8 | Cool white-gray + deep purple | background `#F4F5F6`; title `#111111`; body `#303030`; secondary `#6D7175`; line `#C8CCD0`; accent `#4B2E83` | AI, technology trends, product strategy, innovation research |

Each palette sample should use comparable content density and page structure so the user can judge tone, hierarchy, chart language, and readability. Once selected, the palette is locked for the full deck.

## Default style exploration

Generate five materially different directions:

1. MBB high-density consulting
2. Premium brand strategy
3. Executive editorial magazine
4. Swiss international grid
5. Modern data storytelling

Replace a direction when it conflicts with the subject or audience, but keep five clearly distinguishable options.

If the user asks specifically for palette comparison, generate all eight palette samples instead of the five style directions.

## Image generation rules

- Generate each direction as a separate complete 16:9 slide.
- Use the same representative content type across options so style can be compared fairly.
- Never create a collage, contact sheet, thumbnail grid, or multiple slides inside one image.
- Show enough content to judge title hierarchy, grid, chart style, annotation, spacing, and density.
- Avoid tiny pseudo-text. Use realistic text blocks, but treat all generated wording and values as disposable.
- Label each output outside the image or in the filename, not by relying on generated text.

The user may explicitly skip ImageGen. When skipped, confirm the supplied template, screenshot, brand guide, or written system is specific enough to build from.

## Convert the selected direction into a system

Document:

- slide dimensions and safe margins;
- column and row grid;
- title, subtitle, body, annotation, and footnote sizes;
- font families and fallbacks;
- background, text, line, neutral, and accent colors;
- chart palette and emphasis rules;
- table borders, fills, and hierarchy;
- corner radius, shadows, dividers, icons, and imagery;
- header, footer, source, and page-number treatment;
- spacing rhythm and content-density target.

Do not approve a style based on color alone. Grid, density, hierarchy, chart language, and whitespace behavior define the system.

## Page-level ImageGen blueprints

After the user confirms the palette and visual direction, generate a page-level blueprint for each planned slide before PPTX production.

Blueprint rules:

- Use one complete 16:9 image per slide.
- Keep the selected palette, grid, density, chart language, headers, footers, and spacing consistent.
- Use the confirmed outline as the content structure, but treat generated wording, numbers, citations, chart values, logos, and labels as unreliable placeholders.
- The blueprint defines composition only. Final PPT text, data, tables, charts, and source notes must be rebuilt from the evidence table.
- The cover blueprint should remain low-density for consulting reports unless the user explicitly asks for a data-heavy cover.

## Readability guardrails

- Prefer restructuring, grouping, or page splitting before reducing type.
- Make key numbers and conclusions scannable at normal presentation zoom.
- Reserve the accent color for meaning: priority, exception, conclusion, or action.
- Maintain deliberate whitespace, but reject large unused right/bottom regions caused by layout mismatch.
- Keep chart labels horizontal where practical and avoid legend-dependent decoding.

## Confirmation output

Present the independent images with a short comparison of tone, density, advantages, and risks. Include the recommended palette when applicable. Stop and request the second confirmation.
