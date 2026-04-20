# Cyrillic Reference

Open-source Unicode reference for 77 Cyrillic-based languages. A pan-Cyrillic table of every single character used across the covered languages — with each character's Unicode codepoint (or sequence of codepoints), a catalog of glyph variants that share a codepoint (localized and stylistic forms), and SVG illustrations of each letter.

Part of the Paratype Cyrillic Languages project; released under the **MIT License** — see [`LICENSE`](LICENSE).

## Scope

77 Cyrillic-based languages. The full list lives in [`generate.py`](generate.py) as `LANGUAGES_IN_SCOPE`.

## Source data

The character data is generated from the per-language JSON files in a sister directory of the same repository:

```
paratype-git/cyrillic-languages/
├── cyrillic-languages/          ← source data (per-language JSONs + reference tables)
└── cyrillic-reference/          ← this directory (generated documentation)
```

## Regenerating

Python 3 stdlib only; no dependencies.

```bash
cd cyrillic-reference/
python3 generate.py
```

By default `generate.py` reads from `../cyrillic-languages/` and writes alongside itself. Override with `--data` / `--out` if needed.

Per-letter SVG illustrations are produced via [`glyphplotter`](https://bitbucket.org/LindenbergSW/fontdoctools/src/master/) — a separate open-source tool. Install it adjacent to this tree when the SVG stage is wired up.

## Output

- `characters-uppercase.md` — master table of every unique uppercase Cyrillic codepoint used across the 77 languages, deduplicated by codepoint.
- `characters-lowercase.md` — same for lowercase.
- `glyph-variants.md` — rows for glyph variants that share a codepoint with a base letter but render differently under `locl` or stylistic-alternate features (Bulgarian `Д`, Serbian italic `г`, and so on).

## Private Use Area

Paratype's PT Sans Expert / PT Serif Expert fonts historically used Unicode Private Use Area codepoints (`E000`–`F8FF`) for glyphs that had no official Unicode assignment at the time. Where a PUA codepoint can be expressed as a sequence of standard Unicode characters, the standard sequence is used in the main tables and the legacy PUA codepoint is preserved in `pua-legacy.md` for backwards compatibility with older documents.

Where no standard sequence exists, the PUA codepoint is listed with a descriptive name (e.g. `CYRILLIC SMALL LETTER ZE WITH TAIL`).

The PUA is a shared range in the Unicode standard — no organisation owns specific codepoints within it. `!FXXX` notation in Paratype's source data means "this glyph at this codepoint *in the Paratype Expert fonts*".

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
