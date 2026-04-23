# Cyrillic Reference — status and next steps

Working notes for the next session / next agent picking this up.

## Where we are (2026-04-23)

This subproject lives as a subdirectory of `paratype-git/cyrillic-languages` — a monorepo decision made after the "separate repo" plan was reconsidered. The whole repository is MIT-licensed (see `/LICENSE` at repo root); `cyrillic-reference/LICENSE` is kept for clarity of this subtree. Scope is **pan-Cyrillic single characters across 77 languages**, not per-language alphabets with digraphs — decision made mid-session after the first per-language pass was thrown away.

Files present:
- `LICENSE` — MIT, Paratype, 2026
- `README.md` — project framing, data pipeline, SVG layout + calibration, manual re-render instructions, known limitations, license
- `tools/_catalog.py` — Python 3 stdlib; shared core (decompose, variants, language catalog) imported by all three generators
- `tools/generate.py` — Python 3 stdlib only; reads the sibling `cyrillic-languages` repo and writes the three Markdown tables
- `tools/generate_svgs.py` — needs fontTools + FontDocTools; reads the same sources plus PT Expert TTFs and produces one SVG diagram per row
- `tools/generate_json.py` — Python 3 stdlib only; emits `data/pan-cyrillic.json` and `data/languages/*.json` — machine-readable mirror of the Markdown tables (see `data/README.md`)
- `characters-uppercase.md` — **177** unique uppercase codepoints (54 PUA). 105 have composed descriptions; 73 decompose into base + combining marks (67 via the `… WITH …` description + 6 via Unicode NFD fallback), 38 remain as structural composites
- `characters-lowercase.md` — **176** unique lowercase codepoints (54 PUA). Same 105 / 73 / 38 breakdown as uppercase
- `glyph-variants.md` — **39** variant rows that share a codepoint with a base letter but render differently under `locl`. Styles: any=22, straight=12, italic=5. Locales: ba, bg, cv, sr (ru-default languages do not produce locl variants)
- `svg/{Sans,Serif}/uc/*.svg` + `glyphplotter/{Sans,Serif}/uc/*.txt` — 177 diagrams + plotter sources per family for uppercase codepoints
- `svg/{Sans,Serif}/lc/*.svg` + `glyphplotter/{Sans,Serif}/lc/*.txt` — 176 per family for lowercase
- `svg/{Sans,Serif}/variants/*.svg` + `glyphplotter/{Sans,Serif}/variants/*.txt` — 39 per family for Serif; 37 for Sans (missing 2 BGR glyphs — see below)
- `svg/{Sans,Serif}/_calibration/accents.svg` + `glyphplotter/{Sans,Serif}/_calibration/accents.txt` — reference sheet per family for the 10 combining marks + Cyrillic breves
- `data/pan-cyrillic.json` + `data/languages/*.json` — machine-readable JSON (77 per-language files; Kaitag and Uzbek skipped). See `data/README.md`

Regeneration (from `cyrillic-reference/`):
```bash
# Markdown tables (Python stdlib only)
python3 tools/generate.py

# Machine-readable JSON (Python stdlib only, independent of the MDs)
python3 tools/generate_json.py

# SVG diagrams (needs Python 3.13+, fontTools, FontDocTools)
python3 tools/generate_svgs.py --family Sans \
    --font        ../cyrillic-languages/fonts/web/PT-Sans-Expert_Regular/pt-sans-expert_regular.ttf \
    --font-italic ../cyrillic-languages/fonts/web/PT-Sans-Expert_Italic/PT-Sans-Expert_Italic.ttf

python3 tools/generate_svgs.py --family Serif \
    --font        ../cyrillic-languages/fonts/web/PT-Serif-Expert_Regular/pt-serif-expert_regular.ttf \
    --font-italic ../cyrillic-languages/fonts/web/PT-Serif-Expert_Italic/PT-Serif-Expert_Italic.ttf
```

## Done in this pass

### 1. Decompose "… WITH …" composed descriptions into base + combining marks — **done**

`decompose()` in `generate.py` now parses the description into `base_name WITH <tokens>`, looks up the base via `unicodedata.lookup`, and maps ten standard tokens: MACRON (U+0304), DIAERESIS (U+0308), BREVE (Cyrillic-specific U+F6D1 uppercase / U+F6D4 lowercase — **not** the generic U+0306), ACUTE (U+0301), CIRCUMFLEX (U+0302), GRAVE (U+0300), CARON (U+030C), DOUBLE ACUTE (U+030B), CEDILLA (U+0327), DOT ABOVE (U+0307). Multi-accent phrases (`DIAERESIS AND BREVE`, etc.) are split on ` AND ` and emit all marks in order. For non-PUA rows the result is cross-checked against `unicodedata.normalize('NFD', …)` with the one allowed deviation that the generic breve is rewritten to F6D1/F6D4 — a mismatch raises at generation time.

Structural composites (DESCENDER, HOOK, TAIL, STROKE, BAR, TICK, UPTURN, MIDDLE HOOK, VERTICAL STROKE, and the STROKE AND HOOK pair on Ӻ/ӻ) have no standard combining mark and are left undecomposed — they stay as their codepoint plus the descriptive name.

Numbers: 146 decomposed (73 UC + 73 LC), 76 structural (38 UC + 38 LC). 210 rows carry a `WITH` in their description (105 per side) — of those, 134 decompose via the `WITH` parse path; the other 12 rows decompose via the NFD fallback on precomposed codepoints (Ё, Й, Ў, Ѓ, Ї, Ќ and their lowercase forms) whose Unicode names carry only a language label.

### 2. PUA decomposition — **done**

PUA codepoints whose shape can be expressed as a sequence of standard Unicode characters (e.g. `F510` → `0415 + 0304`) render the sequence in the `Decomposition` column and keep the PUA hex in the `Codepoint` column. Structural PUA rows (accents with no combining-mark equivalent) keep an empty `Decomposition` cell.

### 3. SVG illustrations via `glyphplotter` — **done**

`generate_svgs.py` emits one SVG per row in the master tables plus their matching `.txt` plotter sources. Layout: decomposable composites render as `base + mark(s) → composed` with each mark in its own dotted-circle box; structural composites and plain letters render as a single centred glyph; locl variants render as `default → variant` via the TTF's suffixed glyph names (`.BGR`, `.BSH`, `.CHU`, `.SRB`). Service elements (rectangles, `+`, `→`, labels) are drawn with glyphplotter primitives, not saved from a second font. Vertical placement lifts above-marks by `GAP=150` above `dc.yMax` and drops below-marks (cedilla) the same distance below `dc.yMin`; horizontal placement uses the glyph's bbox centre plus per-mark `X_NUDGE_EXTRA` / `Y_NUDGE_EXTRA` overrides calibrated on the per-family `accents.svg` reference sheet at `svg/{Sans,Serif}/_calibration/`. Full layout, calibration constants, and manual re-rendering instructions are in `README.md`. Both styles of locl variant — `any` / `straight` (upright TTF) and `italic` (italic TTF) — are rendered; the italic TTF is used only for the five `.ita`-suffixed rows.

**Remaining SVG-stage TODOs:**

- **Font gap — BGR `Ж` and `К` missing from PT Sans Expert.** `uni0416.BGR` and `uni041A.BGR` are absent from Sans (Serif has them). Suppressed from `glyph-variants.md` via `_FONT_GAPS_SUPPRESSED` in `tools/_catalog.py`. To restore: add the glyphs to the Sans `.ufo` source, rebuild the TTF, and remove the entry from the suppression set.

### 4. Publish — **done**

The subproject lives at `paratype-git/cyrillic-languages/cyrillic-reference/`; all generated tables, SVG/plotter sources, and machine-readable JSON are committed alongside the generators. The deliverable URL is `https://github.com/paratype-git/cyrillic-languages/tree/master/cyrillic-reference`.

## Non-negotiables

- **MIT license on every outbound artifact.** The whole repository is MIT (`/LICENSE`); this subproject inherits it.
- **77-language scope** — the list is in `tools/_catalog.py` as `LANGUAGES_IN_SCOPE`. Not 79: `Kaitag` and `Uzbek` are in our data (`SKIP_LANGUAGES`) but out of scope for deliverables.
- **PUA is a shared Unicode range** used by Paratype Expert fonts, not proprietary to any one foundry. Frame it accordingly in any descriptive text.

## Useful references in the source data repo

- `cyrillic-languages/PT_PUA_unicodes-descriptions.txt` — `FXXX  CYRILLIC …` mappings for every PUA codepoint used by PT Expert fonts. Canonical descriptions for PUA rows.
- `cyrillic-languages/site/cyrillic/cyrillic_characters_lib.json` — aggregated pan-Cyrillic set that `tools/_catalog.load_pan_cyrillic` reads from.
- `cyrillic-languages/library/cyrillic/base/*.json` — 79 source language files; 77 are in scope.
- `cyrillic-languages/library/cyrillic/_legacy/Russian Old (XIX).json` — archived historical alphabet, not registered in `cyrillic_library.json` and not in the 77-language scope.
