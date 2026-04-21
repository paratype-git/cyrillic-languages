# Cyrillic Reference — status and next steps

Working notes for the next session / next agent picking this up.

## Where we are (2026-04-20)

This subproject lives as a subdirectory of `paratype-git/cyrillic-languages` — a monorepo decision made after the "separate repo" plan was reconsidered. The whole repository is MIT-licensed (see `/LICENSE` at repo root); `cyrillic-reference/LICENSE` is kept for clarity of this subtree. Scope is **pan-Cyrillic single characters across 77 languages**, not per-language alphabets with digraphs — decision made mid-session after the first per-language pass was thrown away.

Files present:
- `LICENSE` — MIT, Paratype, 2026
- `README.md` — project framing, data pipeline, SVG layout + calibration, manual re-render instructions, known limitations, license matrix
- `generate.py` — Python 3 stdlib only; reads the sibling `cyrillic-languages` repo and writes the three Markdown tables
- `generate_svgs.py` — needs fontTools + FontDocTools; reads the same sources plus PT Serif Expert Regular and produces one SVG diagram per row
- `characters-uppercase.md` — **177** unique uppercase codepoints (54 PUA). 105 have composed descriptions: 67 decomposed into base + combining marks, 38 kept as structural composites
- `characters-lowercase.md` — **176** unique lowercase codepoints (54 PUA). 105 composed: 67 decomposed, 38 structural
- `glyph-variants.md` — **82** variant forms that share a codepoint with a base letter but render differently under `locl` or `.str`/`.ita` stylistic alternates. Locales: ba, bg, cv, sr (ru-default languages do not produce locl variants)
- `svg/uc/*.{svg,txt}` — 177 SVG diagrams + plotter sources for uppercase codepoints
- `svg/lc/*.{svg,txt}` — 176 for lowercase
- `svg/variants/*.{svg,txt}` — 26 for locl-named variants (15 GSUB-only rows stay unrendered)
- `svg/_calibration/accents.{svg,txt}` — reference sheet for the 10 combining marks + Cyrillic breves

Regeneration:
```bash
# Markdown tables (Python stdlib only)
cd cyrillic-reference/ && python3 generate.py

# SVG diagrams (needs Python 3.13+, fontTools, FontDocTools)
python3 generate_svgs.py \
    --font ../cyrillic-languages/fonts/web/PT-Serif-Expert_Regular/pt-serif-expert_regular.ttf
```

## Done in this pass

### 1. Decompose "… WITH …" composed descriptions into base + combining marks — **done**

`decompose()` in `generate.py` now parses the description into `base_name WITH <tokens>`, looks up the base via `unicodedata.lookup`, and maps ten standard tokens: MACRON (U+0304), DIAERESIS (U+0308), BREVE (Cyrillic-specific U+F6D1 uppercase / U+F6D4 lowercase — **not** the generic U+0306), ACUTE (U+0301), CIRCUMFLEX (U+0302), GRAVE (U+0300), CARON (U+030C), DOUBLE ACUTE (U+030B), CEDILLA (U+0327), DOT ABOVE (U+0307). Multi-accent phrases (`DIAERESIS AND BREVE`, etc.) are split on ` AND ` and emit all marks in order. For non-PUA rows the result is cross-checked against `unicodedata.normalize('NFD', …)` with the one allowed deviation that the generic breve is rewritten to F6D1/F6D4 — a mismatch raises at generation time.

Structural composites (DESCENDER, HOOK, TAIL, STROKE, BAR, TICK, UPTURN, MIDDLE HOOK, VERTICAL STROKE, and the STROKE AND HOOK pair on Ӻ/ӻ) have no standard combining mark and are left undecomposed — they stay as their codepoint plus the descriptive name.

Numbers: 134 decomposed (67 UC + 67 LC), 76 structural (38 UC + 38 LC), sum 210 — matches the original composed-entry count.

### 2. Legacy PUA mapping column — **done**

The main tables now have two new columns: `Decomposition` (`XXXX + XXXX + …` for decomposable rows, empty for structural and non-composite rows) and `Legacy PUA` (`FXXX` for PUA rows that have a decomposition; empty otherwise). The original `Codepoint` column is unchanged in all rows — "Variant 1" symmetric layout, chosen over the spec's suggestion of rewriting `Codepoint` to the sequence on PUA rows.

### 3. SVG illustrations via `glyphplotter` — **done**

`generate_svgs.py` emits one SVG per row in the master tables plus their matching `.txt` plotter sources. Layout: decomposable composites render as `base + mark(s) → composed` with each mark in its own dotted-circle box; structural composites and plain letters render as a single centred glyph; locl variants render as `default → variant` via the TTF's suffixed glyph names (`.BGR`, `.BSH`, `.CHU`, `.SRB`). Service elements (rectangles, `+`, `→`, labels) are drawn with glyphplotter primitives, not saved from a second font. Vertical placement lifts above-marks by `GAP=150` above `dc.yMax` and drops below-marks (cedilla) the same distance below `dc.yMin`; horizontal placement uses the glyph's bbox centre plus per-mark `X_NUDGE_EXTRA` / `Y_NUDGE_EXTRA` overrides calibrated on the `svg/_calibration/accents.svg` reference sheet. Full layout, calibration constants, and manual re-rendering instructions are in `README.md`.

**Remaining SVG-stage TODOs:**

- **Font gap — BGR missing in both families (designers):** `uni0416.BGR` (Ж) and `uni041A.BGR` (К) are absent from both PT Sans Expert Regular and PT Serif Expert Regular. Suppressed from `glyph-variants.md` via `_FONT_GAPS_SUPPRESSED` in `tools/generate.py`. To restore: add the glyphs to the relevant `.ufo` source(s), rebuild the TTF pair, and remove the entry from `_FONT_GAPS_SUPPRESSED`.
- **Font gap — BGR missing in Sans only (designers):** `uni043D.BGR` (н) and `uni0447.BGR` (ч) exist in PT Serif Expert Regular but not in PT Sans Expert Regular. The Sans column of `glyph-variants.md` currently shows a broken image for these two rows (the Serif column renders fine). Either add the missing `.BGR` glyphs to the Sans font, or add a per-family suppression branch.
- **`.str` style variants** are not rendered yet. They would need a parallel branch in `generate_svgs.py`'s `process_variants` pointing at the upright weight (similar to how `.ita` variants now load `PT-Serif-Expert_Italic.ttf`).

### 4. Publish

No separate repo needed — this tree is already part of `paratype-git/cyrillic-languages`. When stages 1–3 produce usable output, commit the generated tables alongside the generator. The deliverable URL becomes `https://github.com/paratype-git/cyrillic-languages/tree/master/cyrillic-reference`.

## Non-negotiables

- **MIT license on every outbound artifact.** The whole repository is MIT (`/LICENSE`); this subproject inherits it.
- **77-language scope** — the list is in `generate.py` as `LANGUAGES_IN_SCOPE`. Not 79: `Kaitag` and `Uzbek` are in our data but out of scope here.
- **PUA is a shared Unicode range** used by Paratype Expert fonts, not proprietary to any one foundry. Frame it accordingly in any descriptive text.

## Useful references in the source data repo

- `cyrillic-languages/PT_PUA_unicodes-descriptions.txt` — `FXXX  CYRILLIC …` mappings for every PUA codepoint used by PT Expert fonts. This is the canonical list for stage 1 (decomposition) and §4.10 descriptive forms.
- `cyrillic-languages/site/cyrillic/cyrillic_characters_lib.json` — aggregated pan-Cyrillic set that `generate.py` reads from.
- `cyrillic-languages/library/cyrillic/base/*.json` — 79 source language files; 77 are in scope.
- `cyrillic-languages/library/cyrillic/_legacy/Russian Old (XIX).json` — spec §4.11 mentions `RussianOld` for PUA but it is NOT in the 77-language scope.
