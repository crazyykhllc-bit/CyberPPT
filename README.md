# CyberPPT

CyberPPT is a Codex Skill for turning source documents, research notes, and business data into high-density, editable consulting presentations.

It is designed for work such as industry reports, consumer research, brand strategy, e-commerce analysis, management briefings, and client-ready consulting decks.

## What it enforces

- Evidence-based source analysis before slide writing.
- SCR storyline structure: Situation, Complication, Resolution.
- Explicit user approval gates for outline, visual direction, and final deck.
- Five separate 16:9 visual style explorations by default.
- Editable PowerPoint output built from native text, shapes, tables, and charts.
- Structural PPTX validation to catch common risks such as non-16:9 sizing, off-slide elements, placeholder text, and full-slide screenshot shortcuts.

## Repository layout

```text
cyber-ppt/
  SKILL.md
  agents/
    openai.yaml
  references/
    source-analysis.md
    storyline.md
    visual-system.md
    ppt-production.md
    quality-assurance.md
  scripts/
    validate_pptx.py
    test_validate_pptx.py
  prompts/
    CyberPPT-prompts.txt
```

## Installation

Clone or copy this repository into your Codex skills directory as `cyber-ppt`.

Windows PowerShell:

```powershell
git clone https://github.com/crazyykhllc-bit/CyberPPT.git "$env:USERPROFILE\.codex\skills\cyber-ppt"
```

macOS/Linux:

```bash
git clone https://github.com/crazyykhllc-bit/CyberPPT.git ~/.codex/skills/cyber-ppt
```

If you are not using Git, copy the full folder into the same location. The folder must contain `SKILL.md` at its root.

## Usage

Example request:

```text
Use CyberPPT to turn this DOCX/PDF/research material into a 7-page high-density consulting PPT. First generate the outline, then ask me to confirm the style before producing the deck. Use SCR logic and include detailed charts.
```

The reusable prompt library is available at:

```text
prompts/CyberPPT-prompts.txt
```

## PPTX validation

Run the validator against a generated deck:

```bash
python scripts/validate_pptx.py path/to/deck.pptx --json-out path/to/report.json
```

Run the validator tests:

```bash
python -m unittest scripts/test_validate_pptx.py -v
```

The validator is intentionally structural. It flags layout/editability risks, but it does not replace full-slide visual review.

## Privacy and source material

Do not commit client documents, generated decks, slide renders, validation reports from private decks, or project-specific process notes. The `.gitignore` is configured to exclude common source and output files by default.

## License

MIT. See [LICENSE](LICENSE).

