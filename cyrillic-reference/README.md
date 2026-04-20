# Cyrillic Reference

Open-source Unicode reference for 77 Cyrillic-based languages. A pan-Cyrillic table of every single character used across the covered languages — with each character's Unicode codepoint (or sequence of codepoints), a catalog of glyph variants that share a codepoint (localized and stylistic forms), and per-letter SVG diagrams illustrating how composed codepoints decompose into a base plus combining marks.

Part of the Paratype Cyrillic Languages project; released under the **MIT License** — see [`LICENSE`](LICENSE).

## Scope

77 Cyrillic-based languages. The full list lives in [`generate.py`](generate.py) as `LANGUAGES_IN_SCOPE`. `Kaitag` and `Uzbek` exist in the source data repository but are out of scope here.

## Outputs

| File | Description |
| --- | --- |
| [`characters-uppercase.md`](characters-uppercase.md) | Master table of every unique uppercase codepoint, deduplicated. Columns: `Sign`, `Codepoint`, `Description`, `PUA`, `Decomposition`, `Legacy PUA`, `Diagram`, `Locales`. Sorted by codepoint so PUA entries cluster at the end. |
| [`characters-lowercase.md`](characters-lowercase.md) | Same shape for lowercase codepoints. |
| [`glyph-variants.md`](glyph-variants.md) | Rows for glyphs that share a codepoint with a base letter but render differently under `locl` or stylistic-alternate features (Bulgarian `Д`, Serbian italic `г`, …). |
| [`svg/uc/XXXX.{svg,txt}`](svg/uc/) | One SVG decomposition diagram per uppercase codepoint, plus its glyphplotter source. |
| [`svg/lc/XXXX.{svg,txt}`](svg/lc/) | Same for lowercase. |
| [`svg/variants/XXXX.LANG.{svg,txt}`](svg/variants/) | `default → variant` diagrams for locl-named glyph variants. |
| [`svg/_calibration/accents.{svg,txt}`](svg/_calibration/) | Reference sheet of all 10 combining marks + Cyrillic breve UC/LC on a dotted circle, using the calibration constants. |

## Data pipeline

```
../cyrillic-languages/                               (source repo)
├── library/cyrillic/base/*.json         hand-edited per-language alphabets
├── site/cyrillic/cyrillic_characters_lib.json   pan-Cyrillic aggregated set
└── fonts/web/PT-Serif-Expert_Regular/
    └── pt-serif-expert_regular.ttf             rendering font (gitignored)
                         │
                         ▼
                    generate.py               (Python 3 stdlib only)
                         │
       ┌─────────────────┼─────────────────┐
       ▼                 ▼                 ▼
  characters-         characters-     glyph-variants.md
  uppercase.md        lowercase.md
                         │
                         ▼
                generate_svgs.py         (needs fontTools + FontDocTools)
                         │
       ┌─────────────────┼─────────────────┐
       ▼                 ▼                 ▼
   svg/uc/*.svg     svg/lc/*.svg     svg/variants/*.svg
   svg/uc/*.txt     svg/lc/*.txt     svg/variants/*.txt
```

Two stages, two scripts:

1. **`generate.py`** reads the pan-Cyrillic JSON and the per-language source JSONs, dedupes by codepoint, decomposes `… WITH <mark>` descriptions into base + combining marks, and emits the three Markdown tables. Pure Python 3 stdlib — no third-party dependencies.
2. **`generate_svgs.py`** reads the same sources plus the PT Serif Expert Regular TTF, and renders one SVG diagram per row via `glyphplotter` (a command-line tool from the [FontDocTools](https://bitbucket.org/Lontar/FontDocTools/src/master/) package). Requires Python ≥ 3.13, `fontTools`, and FontDocTools installed in the active venv.

### Decomposition logic

The `Description` field in the pan-Cyrillic summary follows Unicode naming: e.g. `"Cyrillic Capital Letter A With Breve"` for U+04D0. `generate.py`'s `decompose()`:

1. Splits on ` WITH ` → base name (`"Cyrillic Capital Letter A"`) and accent phrase (`"Breve"`).
2. Splits the accent phrase on ` AND ` → list of tokens (`["BREVE"]`).
3. If every token is one of the ten **decomposable** accents (`MACRON`, `DIAERESIS`, `BREVE`, `ACUTE`, `CIRCUMFLEX`, `GRAVE`, `CARON`, `DOUBLE ACUTE`, `CEDILLA`, `DOT ABOVE`), maps each to its combining-mark codepoint. Otherwise returns `None` — the row is "structural" and stays as its codepoint + descriptive name.
4. `BREVE` resolves differently by case: **U+F6D1** for uppercase rows, **U+F6D4** for lowercase — the Cyrillic-shaped breve glyphs in the Paratype Expert fonts, not the generic combining U+0306 (whose shape is Latin-centric and doesn't match Cyrillic typography).
5. Base letter is looked up via `unicodedata.lookup(base_name)` — works for all 210 composites in the current dataset including PUA composites built on transformed bases like "Reversed Ze".

### Structural composites (not decomposed)

76 out of 210 composed codepoints have accents with no standard combining-mark equivalent: **DESCENDER**, **HOOK**, **TAIL**, **STROKE**, **BAR**, **TICK**, **UPTURN**, **MIDDLE HOOK**, **VERTICAL STROKE**, and the **STROKE AND HOOK** pair on Ӻ/ӻ. These are structural outline modifications, not combining marks — no standard Unicode sequence expresses them. They render as a single glyph with the original codepoint preserved and are distinguished in the tables by an empty `Decomposition` cell.

### Locl/style variants

82 rows in `glyph-variants.md` cover glyphs that share a codepoint with a base letter but render as a different shape under an OpenType feature:

- `&`-marked tokens in the per-language source files correspond to `locl` forms selected by the language's tag (`BGR`, `SRB`, `BSH`, `CHU` — Bulgarian, Serbian, Bashkir, Chuvash).
- `+`-marked tokens pair with the `&` tokens and provide the default shape.

PT Serif Expert Regular exposes locl variants by **suffixed glyph name** — `uni0492.BSH` (Bashkir Ghe-with-Stroke), `uni0433.BGR` (Bulgarian ge), etc. `generate_svgs.py` queries the font's `post` table for `<base_name>.<locale_tag>` and, if found, renders a `default → variant` diagram. 26 of the 41 `&` rows currently have a matching named variant in the font; the remaining 15 are driven purely by GSUB lookups (no standalone name) and would require a shaper (`uharfbuzz` or CoreText) to render — they are listed in `glyph-variants.md` with a `Diagram` column pointing to a non-existent file.

## Regenerating

### Step 1 — Markdown tables

Python 3 stdlib only.

```bash
cd cyrillic-reference/
python3 generate.py
```

Reads `../cyrillic-languages/` by default; override with `--data` / `--out`.

### Step 2 — SVG diagrams

Requires Python 3.13+ with `fontTools` and FontDocTools:

```bash
# One-time setup (into the active venv):
pip install git+https://bitbucket.org/Lontar/FontDocTools.git

# Each regeneration:
cd cyrillic-reference/
python3 generate_svgs.py \
    --data ../cyrillic-languages \
    --font ../cyrillic-languages/fonts/web/PT-Serif-Expert_Regular/pt-serif-expert_regular.ttf
```

Takes ~35 seconds for the full 350+-row set. Invokes `glyphplotter` via subprocess for each row. The macOS-only tools in the FontDocTools package (`glyphshaper`, `glyphdump`, `roentgen`) are not needed and are skipped automatically on Linux via platform markers.

## Diagram layout

Each decomposable composite is rendered as a horizontal sequence of boxes:

```
[ base letter ]  +  [ mark₁ on ◌ ]  +  [ mark₂ on ◌ ]  →  [ composed ]
```

Single-accent rows have three boxes (base + mark + composed); double-accent rows have four. Structural composites and plain letters render as a single box. Locl/style variants render as `[ default ] → [ variant ]`.

**Service elements** (rectangles, `+`, `→`, labels) are drawn with glyphplotter primitives — `drawRectangle`, `drawCross`, `drawArrow`, `drawLabel` — **not** by saving glyphs from a second font. The only rendering font is PT Serif Expert Regular; the dotted circle `U+25CC` is native to it, so no Noto Serif Balinese fallback is needed.

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

To add a new per-mark tweak, append to `X_NUDGE_EXTRA` or `Y_NUDGE_EXTRA` in `generate_svgs.py`. The calibration sheet at `svg/_calibration/accents.svg` shows all 10 + 1 marks side-by-side on a dotted circle; regenerating it after a constants change gives immediate feedback.

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

Paratype's PT Sans Expert / PT Serif Expert fonts historically used Unicode Private Use Area codepoints (`E000`–`F8FF`) for glyphs that had no official Unicode assignment at the time. Where a PUA codepoint can be expressed as a sequence of standard Unicode characters, the master tables show the decomposition in the `Decomposition` column AND keep the old PUA codepoint in the `Legacy PUA` column for backwards compatibility with older documents.

Where no standard sequence exists (the 76 structural composites), the PUA codepoint is listed with its descriptive name and an empty `Decomposition` cell.

The PUA is a shared range in the Unicode standard — no organisation owns specific codepoints within it. `!FXXX` notation in Paratype's source data means "this glyph at this codepoint *in the Paratype Expert fonts*".

## Known limitations

- **15 locl rows unrendered.** `glyph-variants.md` has 41 localized entries, but only 26 have a suffixed glyph name (`uni0492.BSH` etc.) in PT Serif Expert Regular. The remaining 15 are reached purely through GSUB lookups without a standalone name, so they cannot be referenced by glyphplotter and stay unrendered. Adding `uharfbuzz` would allow rendering these.
- **No GPOS anchor positioning.** Glyphplotter does not apply GPOS mark-attachment anchors. Combining marks are placed by bbox centering plus hand-tuned nudges, not by the designer-intended anchor points. For the standard combining set this is close enough; unfamiliar marks may need their own `X_NUDGE_EXTRA` / `Y_NUDGE_EXTRA` override.
- **Italic / straight variants (`.ita` / `.str`) not rendered.** The `Style` column of `glyph-variants.md` distinguishes these but the generator currently only handles the default + locl shape pair. Style alternates would need their own template.
- **Python 3.13+ required for SVG stage.** FontDocTools itself requires ≥ 3.13. The Markdown-only pipeline (`generate.py`) is stdlib and runs on any Python 3.

## License

MIT. Inbound contributions must be compatible with the licenses listed below:

| License | URL |
| --- | --- |
| Apache 2.0 | <https://www.apache.org/licenses/LICENSE-2.0> |
| MIT | <https://opensource.org/licenses/MIT> |
| BSD 3-Clause | <https://opensource.org/licenses/BSD-3-Clause> |
| BSD 2-Clause | <https://opensource.org/licenses/BSD-2-Clause> |
| PSF License Agreement | <https://docs.python.org/3/license.html> |
| Unicode, Inc. License Agreement — Data Files and Software | <https://www.unicode.org/license.html> |

## Contact

© Paratype. Questions, suggestions: **info@paratype.net**.
