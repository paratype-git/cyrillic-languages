# Cyrillic Reference

Open-source Unicode reference for 77 Cyrillic-based languages. A pan-Cyrillic table of every single character used across the covered languages — with each character's Unicode codepoint (or sequence of codepoints), a catalog of glyph variants that share a codepoint (localized and stylistic forms), and per-letter SVG diagrams illustrating how composed codepoints decompose into a base plus combining marks.

Part of the Paratype Cyrillic Languages project; released under the **MIT License** — see [`LICENSE`](LICENSE).

## Scope

77 Cyrillic-based languages. The full list lives in [`tools/_catalog.py`](tools/_catalog.py) as `LANGUAGES_IN_SCOPE`. `Kaitag` and `Uzbek` exist in the source data repository but are out of scope here.

## Outputs

| File | Description |
| --- | --- |
| [`characters-uppercase.md`](characters-uppercase.md) | Master table of every unique uppercase codepoint, deduplicated. Columns: `Sign`, `Codepoint`, `Description`, `PUA`, `Decomposition`, `Diagram`, `Locales`. Sorted by codepoint so PUA entries cluster at the end. |
| [`characters-lowercase.md`](characters-lowercase.md) | Same shape for lowercase codepoints. |
| [`glyph-variants.md`](glyph-variants.md) | Rows for glyphs that share a codepoint with a base letter but render differently under `locl` or stylistic-alternate features (Bulgarian `Д`, Serbian italic `г`, …). |
| [`svg/uc/XXXX.{svg,txt}`](svg/uc/) | One SVG decomposition diagram per uppercase codepoint, plus its glyphplotter source. |
| [`svg/lc/XXXX.{svg,txt}`](svg/lc/) | Same for lowercase. |
| [`svg/variants/XXXX.LANG.{svg,txt}`](svg/variants/) | `default → variant` diagrams for locl-named glyph variants. |
| [`svg/{Sans,Serif}/_calibration/accents.svg`](svg/Serif/_calibration/) (+ `glyphplotter/{Sans,Serif}/_calibration/accents.txt`) | Reference sheet per family — all 10 combining marks + Cyrillic breve UC/LC on a dotted circle, using the calibration constants. |
| [`data/pan-cyrillic.json`](data/pan-cyrillic.json) | Machine-readable pan-Cyrillic JSON. One entry per in-scope codepoint (sorted by Unicode value), with description, decomposition, SVG/plotter paths, nested locl variants, and a `used_by[]` list of languages. |
| [`data/languages/<Name>.json`](data/languages/) | One JSON per in-scope language (77 files — `Kaitag` and `Uzbek` skipped). Meta block (BCP 47 / ISO / OT tags, Paratype identifiers, confidence grade) plus `characters[]` filtered to this language's codepoints, with locl variants attached where the language declares them. |

## Data pipeline

Three independent generators, all reading `cyrillic-languages/` directly. None consumes another's output — `generate_json.py` and `generate.py` are siblings, not a chain.

```
../cyrillic-languages/                               (source repo)
├── library/cyrillic/base/*.json         hand-edited per-language alphabets
├── library/cyrillic/cyrillic_library.json     language registry
├── site/cyrillic/cyrillic_characters_lib.json  pan-Cyrillic aggregate (from compile_languages.py)
└── fonts/web/PT-{Sans,Serif}-Expert_{Regular,Italic}/*.ttf    rendering fonts
                                    │ read by all three
                                    ▼
                         ┌─────────────────────┐
                         │   tools/_catalog.py │   shared core
                         │  (decompose,        │   (stdlib)
                         │   classify_variant, │
                         │   extract_lang…,    │
                         │   collect_variants, │
                         │   load_pan_cyrillic)│
                         └──────────┬──────────┘
               ┌────────────────────┼────────────────────┐
               ▼                    ▼                    ▼
      tools/generate.py    tools/generate_svgs.py   tools/generate_json.py
         (stdlib)            (fontTools +              (stdlib)
                              FontDocTools)
               │                    │                    │
               ▼                    ▼                    ▼
       characters-*.md     svg/{Sans,Serif}/       data/pan-cyrillic.json
       glyph-variants.md   glyphplotter/           data/languages/*.json
```

Rendered SVGs and the glyphplotter `.txt` sources that produce them live in separate parallel trees: `svg/<family>/` for artefacts, `glyphplotter/<family>/` for sources. `.txt` files are per-family — pen positions are derived from each font's metrics, so Sans and Serif sources differ in coordinates even though they describe the same diagram.

Three generators, one shared core:

- **[`tools/_catalog.py`](tools/_catalog.py)** — single source of truth for the 77-language scope, the Paratype-aware NFD (`… WITH <mark>` parsing + BREVE → U+F6D1/U+F6D4 swap + structural-composite detection), variant-token classification, and per-language codepoint extraction. All three generators import from here; none duplicate the logic.
- **`generate.py`** reads the pan-Cyrillic summary plus the per-language base files and emits the three Markdown tables. Pure Python 3 stdlib.
- **`generate_svgs.py`** reads the same sources plus the PT Expert TTFs, and renders one SVG diagram per row via `glyphplotter` (a command-line tool from the [FontDocTools](https://bitbucket.org/Lontar/FontDocTools/src/master/) package). Requires Python ≥ 3.13, `fontTools`, and FontDocTools installed in the active venv.
- **`generate_json.py`** reads the same sources and emits `data/pan-cyrillic.json` and one `data/languages/<Name>.json` per in-scope language. Pure Python 3 stdlib.

### Decomposition logic

The `Description` field in the pan-Cyrillic summary follows Unicode naming: e.g. `"Cyrillic Capital Letter A With Breve"` for U+04D0. `generate.py`'s `decompose()`:

1. Splits on ` WITH ` → base name (`"Cyrillic Capital Letter A"`) and accent phrase (`"Breve"`).
2. Splits the accent phrase on ` AND ` → list of tokens (`["BREVE"]`).
3. If every token is one of the ten **decomposable** accents (`MACRON`, `DIAERESIS`, `BREVE`, `ACUTE`, `CIRCUMFLEX`, `GRAVE`, `CARON`, `DOUBLE ACUTE`, `CEDILLA`, `DOT ABOVE`), maps each to its combining-mark codepoint. Otherwise returns `None` — the row is "structural" and stays as its codepoint + descriptive name.
4. `BREVE` resolves differently by case: **U+F6D1** for uppercase rows, **U+F6D4** for lowercase — the Cyrillic-shaped breve glyphs in the Paratype Expert fonts, not the generic combining U+0306 (whose shape is Latin-centric and doesn't match Cyrillic typography).
5. Base letter is looked up via `unicodedata.lookup(base_name)` — works for all 210 composites in the current dataset including PUA composites built on transformed bases like "Reversed Ze".

### Structural composites (not decomposed)

76 out of 210 composed codepoints have accents with no standard combining-mark equivalent: **DESCENDER**, **HOOK**, **TAIL**, **STROKE**, **BAR**, **TICK**, **UPTURN**, **MIDDLE HOOK**, **VERTICAL STROKE**, and the **STROKE AND HOOK** pair on Ӻ/ӻ. These are structural outline modifications, not combining marks — no standard Unicode sequence expresses them. They render as a single glyph with the original codepoint preserved and are distinguished in the tables by an empty `Decomposition` cell.

### Soft_Dotted bases (lowercase `ї`)

Canonical NFD for lowercase `ї` (U+0457) yields `U+0456 + U+0308` — Cyrillic small letter Byelorussian-Ukrainian `і` plus combining diaeresis. `U+0456` carries the Unicode [`Soft_Dotted`](https://www.unicode.org/reports/tr44/#Soft_Dotted) property: a conforming shaper drops the letter's inherent dot when a combining mark above is attached, so the pair is supposed to render as a dotless `ı` with the diaeresis on top. PT Expert ships a dotless-i glyph at `U+0131` (glyph name `dotlessi`) for renderers that do not honour `Soft_Dotted` automatically — substitute `U+0131` for `U+0456` in that one case when rendering without a shaper.

The `Decomposition` column (and the `decomposition` field in the machine-readable JSON) carries the canonical Unicode pair — that is the interchange form. Any dotless-i substitution is a rendering concern, not a data concern.

Capital `Ї` (U+0407) decomposes to `U+0406 + U+0308` and has no such issue: `U+0406` (І) is visually dotless by design.

### Locl/style variants

39 rows in `glyph-variants.md` cover glyphs that share a codepoint with a base letter but render as a different shape under an OpenType feature:

- `&`-marked tokens in the per-language source files correspond to `locl` forms selected by the language's tag (`BGR`, `SRB`, `BSH`, `CHU` — Bulgarian, Serbian, Bashkir, Chuvash).
- `+`-marked tokens pair with the `&` tokens and provide the default shape.

PT Expert fonts expose locl variants by **suffixed glyph name** — `uni0492.BSH` (Bashkir Ghe-with-Stroke), `uni0433.BGR` (Bulgarian ge), etc. `generate_svgs.py` queries the font's `post` table for `<base_name>.<locale_tag>` and, if found, renders a `default → variant` diagram. Serif currently renders all 39 rows; Sans renders 37 (the BGR `Ж`/`К` glyphs are missing from PT Sans Expert — see [Known limitations](#known-limitations)).

## Machine-readable JSON (`data/`)

`tools/generate_json.py` reads `cyrillic-languages/` directly via the shared `_catalog.py` core — independent of `generate.py` and `generate_svgs.py` — and emits a machine-readable mirror under [`data/`](data/): a pan-Cyrillic codepoint catalog (`data/pan-cyrillic.json`) and one JSON per in-scope language under `data/languages/`.

See [`data/README.md`](data/README.md) for the full schema — field reference, path convention, the 77-language index with tag columns, and generator inputs.

## Regenerating

### Step 1 — Markdown tables

Python 3 stdlib only.

```bash
cd cyrillic-reference/
python3 tools/generate.py
```

Reads `../cyrillic-languages/` by default; override with `--data` / `--out`.

### Step 2 — SVG diagrams

Requires Python 3.13+ with `fontTools` and FontDocTools:

```bash
# One-time setup (into the active venv):
pip install git+https://bitbucket.org/Lontar/FontDocTools.git

# Regenerate both families (runs back-to-back, ~35s each):
cd cyrillic-reference/

python3 tools/generate_svgs.py --family Sans \
    --data ../cyrillic-languages \
    --font        ../cyrillic-languages/fonts/web/PT-Sans-Expert_Regular/pt-sans-expert_regular.ttf \
    --font-italic ../cyrillic-languages/fonts/web/PT-Sans-Expert_Italic/PT-Sans-Expert_Italic.ttf

python3 tools/generate_svgs.py --family Serif \
    --data ../cyrillic-languages \
    --font        ../cyrillic-languages/fonts/web/PT-Serif-Expert_Regular/pt-serif-expert_regular.ttf \
    --font-italic ../cyrillic-languages/fonts/web/PT-Serif-Expert_Italic/PT-Serif-Expert_Italic.ttf
```

`--family` names the output subtree. Each run writes SVGs to
`svg/<Family>/{uc,lc,variants}/` and matching `.txt` plotter sources
to `glyphplotter/<Family>/{uc,lc,variants}/`.

Each invocation renders one font family. The italic TTF is used only for locl variants whose source token carries a `.ita` suffix (Serbian italic). Invokes `glyphplotter` via subprocess per row. The macOS-only tools in the FontDocTools package (`glyphshaper`, `glyphdump`, `roentgen`) are not needed and are skipped automatically on Linux via platform markers.

### Step 3 — Machine-readable JSON

Python 3 stdlib only. Independent of Steps 1 and 2 — reads `cyrillic-languages/` directly via the shared `_catalog.py` core, same as `generate.py`. Run in any order.

```bash
cd cyrillic-reference/
python3 tools/generate_json.py
```

Writes `data/pan-cyrillic.json` and 77 `data/languages/<Name>.json`. No arguments; all paths are resolved relative to the script's location.

## Diagram layout

Each decomposable composite is rendered as a horizontal sequence of boxes:

```
[ base letter ]  +  [ mark₁ on ◌ ]  +  [ mark₂ on ◌ ]  →  [ composed ]
```

Single-accent rows have three boxes (base + mark + composed); double-accent rows have four. Structural composites and plain letters render as a single box. Locl/style variants render as `[ default ] → [ variant ]`.

**Service elements** (rectangles, `+`, `→`, labels) are drawn with glyphplotter primitives — `drawRectangle`, `drawCross`, `drawArrow`, `drawLabel` — **not** by saving glyphs from a second font. The rendering font is either PT Sans Expert or PT Serif Expert, both of which carry `U+25CC` natively, so no Noto Serif Balinese fallback is needed. The main tables show Sans and Serif side by side in two columns so the same letter can be compared across families.

### Calibration constants

Combining marks in OpenType fonts are designed with GPOS anchor attachments that a shaper applies at rendering time. Glyphplotter performs no layout — it is passive — so we position each mark ourselves, using the glyph's bounding box centre as the starting point and tuning visually with per-mark nudges. The calibration table lives at the top of `generate_svgs.py`:

| Constant | Value | Purpose |
| --- | --- | --- |
| `BOX_W` | 1400 | Box width in font units. Wide enough for the widest glyph in the dataset (U+04A6, advance 1010) plus visible padding. |
| `BOX_TOP` | 1440 | Top of the unicode box. Accommodates tall composites and double accents. |
| `BOX_BOTTOM` | -900 | Bottom of the unicode box. Leaves room for below-marks (cedilla). |
| `GAP` | 150 | Vertical clearance between a combining mark and the dotted circle. |
| `H_NUDGE_CYR_BREVE` | -40 | Horizontal nudge applied only to U+F6D1 / U+F6D4 (the Paratype-specific Cyrillic breves). Established visually on U+04D0. |
| `X_NUDGE_EXTRA[0x030B]` | +20 | Per-mark horizontal override for DOUBLE ACUTE. |
| `Y_NUDGE_EXTRA[0xF6D4]` | -30 | Per-mark vertical override for Cyrillic lowercase breve. |

Above-marks are lifted so their `yMin` sits at `dc_yMax + GAP`; below-marks (cedilla) are dropped so their `yMax` sits at `dc_yMin - GAP`. Classification is by the mark's bbox y-centre sign.

To add a new per-mark tweak, append to `X_NUDGE_EXTRA` or `Y_NUDGE_EXTRA` in `tools/generate_svgs.py`. The calibration sheet at `svg/Serif/_calibration/accents.svg` shows all 10 + 1 marks side-by-side on a dotted circle in PT Serif Expert; regenerating it after a constants change gives immediate feedback.

## Re-rendering one diagram manually

Every `.txt` file is self-contained — no absolute paths — and carries a header comment with the exact command:

```
# Generated by cyrillic-reference/generate_svgs.py
# To re-render manually:
#   glyphplotter --input 04D0.txt --output 04D0.svg \
#                --font <path>/pt-serif-expert_regular.ttf
```

Run the shown command (supplying your own path to the TTF) to get a fresh SVG. Hand-edit the `.txt` to experiment with positioning — a numeric tweak in the file regenerates visibly in seconds.

`glyphplotter`'s instruction language is documented at <https://bitbucket.org/Lontar/FontDocTools/raw/master/GlyphPlotter.md>. The key commands you will see in our files:

- `drawRectangle pen left top right bottom stroke` — the box around each glyph.
- `drawGlyph pen x y /glyphname` — draw a glyph from the font at pen-relative position.
- `drawCross pen cx cy radius` — the `+` separator between boxes.
- `drawArrow pen x1 y1 x2 y2 closed60` — the `→` separator before the composed glyph.
- `drawLabel pen x y center "U+XXXX"` — the hex label beneath each box.
- `move n` — advance the pen horizontally after each box or separator.

## Private Use Area

Paratype's PT Sans Expert / PT Serif Expert fonts historically used Unicode Private Use Area codepoints (`E000`–`F8FF`) for glyphs that had no official Unicode assignment at the time. Where a PUA codepoint can be expressed as a sequence of standard Unicode characters (e.g. `F510` → `0415 + 0304`), the master tables show the decomposition in the `Decomposition` column; the original PUA hex remains in the `Codepoint` column so older references stay resolvable.

Where no standard sequence exists, the row keeps its codepoint and descriptive name with an empty `Decomposition` cell — see [Structural composites](#structural-composites-not-decomposed) above.

The PUA is a shared range in the Unicode standard — no organisation owns specific codepoints within it. `!FXXX` notation in Paratype's source data means "this glyph at this codepoint *in the Paratype Expert fonts*".

## Known limitations

- **Two BGR variants missing from PT Sans Expert.** `uni0416.BGR` (Ж) and `uni041A.BGR` (К) are absent from PT Sans Expert Regular (they exist in PT Serif Expert). Suppressed from `glyph-variants.md` via `_FONT_GAPS_SUPPRESSED` in `tools/_catalog.py`. To restore: add the glyphs to the Sans `.ufo` source, rebuild the TTF, and remove the entry from the suppression set.
- **No GPOS anchor positioning.** Glyphplotter does not apply GPOS mark-attachment anchors. Combining marks are placed by bbox centering plus hand-tuned nudges, not by the designer-intended anchor points. For the standard combining set this is close enough; unfamiliar marks may need their own `X_NUDGE_EXTRA` / `Y_NUDGE_EXTRA` override.
- **Python 3.13+ required for SVG stage.** FontDocTools itself requires ≥ 3.13. The stdlib-only generators (`generate.py` and `generate_json.py`) run on any Python 3.

## License

[MIT](https://opensource.org/licenses/MIT). See [`LICENSE`](LICENSE).

## Contact

© Paratype. Questions, suggestions: **info@paratype.net**.
