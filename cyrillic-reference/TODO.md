# Cyrillic Reference — status and next steps

Working notes for the next session / next agent picking this up.

## Where we are (2026-04-20)

This subproject lives as a subdirectory of `paratype-git/cyrillic-languages` — a monorepo decision made after the "separate repo" plan was reconsidered. The whole repository is MIT-licensed (see `/LICENSE` at repo root); `cyrillic-reference/LICENSE` is kept for clarity of this subtree. Scope is **pan-Cyrillic single characters across 77 languages**, not per-language alphabets with digraphs — decision made mid-session after the first per-language pass was thrown away.

Files present:
- `LICENSE` — MIT, Paratype, 2026
- `README.md` — project framing, repo map, regeneration instructions, PUA explanation, license matrix
- `generate.py` — Python 3 stdlib only; reads the sibling `cyrillic-languages` repo and writes the tables below
- `characters-uppercase.md` — **177** unique uppercase codepoints (54 PUA). 105 have composed descriptions: 67 decomposed into base + combining marks, 38 kept as structural composites
- `characters-lowercase.md` — **176** unique lowercase codepoints (54 PUA). 105 composed: 67 decomposed, 38 structural
- `glyph-variants.md` — **82** variant forms that share a codepoint with a base letter but render differently under `locl` or `.str`/`.ita` stylistic alternates. Locales: ba, bg, cv, sr (ru-default languages do not produce locl variants)

Regeneration:
```bash
cd cyrillic-reference/
python3 generate.py
```

## Done in this pass

### 1. Decompose "… WITH …" composed descriptions into base + combining marks — **done**

`decompose()` in `generate.py` now parses the description into `base_name WITH <tokens>`, looks up the base via `unicodedata.lookup`, and maps ten standard tokens: MACRON (U+0304), DIAERESIS (U+0308), BREVE (Cyrillic-specific U+F6D1 uppercase / U+F6D4 lowercase — **not** the generic U+0306), ACUTE (U+0301), CIRCUMFLEX (U+0302), GRAVE (U+0300), CARON (U+030C), DOUBLE ACUTE (U+030B), CEDILLA (U+0327), DOT ABOVE (U+0307). Multi-accent phrases (`DIAERESIS AND BREVE`, etc.) are split on ` AND ` and emit all marks in order. For non-PUA rows the result is cross-checked against `unicodedata.normalize('NFD', …)` with the one allowed deviation that the generic breve is rewritten to F6D1/F6D4 — a mismatch raises at generation time.

Structural composites (DESCENDER, HOOK, TAIL, STROKE, BAR, TICK, UPTURN, MIDDLE HOOK, VERTICAL STROKE, and the STROKE AND HOOK pair on Ӻ/ӻ) have no standard combining mark and are left undecomposed — they stay as their codepoint plus the descriptive name.

Numbers: 134 decomposed (67 UC + 67 LC), 76 structural (38 UC + 38 LC), sum 210 — matches the original composed-entry count.

### 2. Legacy PUA mapping column — **done**

The main tables now have two new columns: `Decomposition` (`XXXX + XXXX + …` for decomposable rows, empty for structural and non-composite rows) and `Legacy PUA` (`FXXX` for PUA rows that have a decomposition; empty otherwise). The original `Codepoint` column is unchanged in all rows — "Variant 1" symmetric layout, chosen over the spec's suggestion of rewriting `Codepoint` to the sequence on PUA rows.

## Still to do

### 3. SVG illustrations via `glyphplotter` (§4.2)

Sample code is in §4.13 of the spec. Required asset on disk:
- `cyrillic-languages/fonts/web/PT-Serif-Expert_Regular/pt-serif-expert_regular.ttf` — already in the repo tree (gitignored). Covers every combining mark we emit, the Cyrillic-specific breve glyphs, and `U+25CC` DOTTED CIRCLE. Use it as the single SVG-rendering font.

`Noto Serif Balinese` is **no longer needed** — `U+25CC` is present in PT Serif Expert, so isolated combining-mark diagrams can use it as the carrier without a second font.

`generate.py` needs a function that takes a single character (or decomposed sequence) and emits a glyphplotter input file describing one diagram per letter. Diagram shape: `<char-box> { + <char-box> } --> <final-glyph>`. Then invoke the glyphplotter binary to rasterize to SVG.

The `glyphplotter` tool lives at <https://bitbucket.org/Lontar/FontDocTools/src/master/> — MIT. Install from source (no PyPI release yet): `pip install git+https://bitbucket.org/Lontar/FontDocTools.git`. Requires Python ≥ 3.13 (our `.venv` is already on 3.14). The macOS-only tools in the package (`glyphshaper`, `glyphdump`, `roentgen`) are not needed and are skipped automatically on Linux via platform markers; the two we use (`glyphplotter`, `dottedcircleshaper`) are pure Python + fontTools.

For the 82 variant forms in `glyph-variants.md`, SVGs need to activate the matching OpenType feature (`locl` with the right language tag, or the right stylistic set). That's a glyphplotter config question — worth a small experiment before committing to a design.

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
