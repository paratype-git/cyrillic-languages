#!/usr/bin/env python3
"""Generate the cyrillic-reference Markdown tables.

Reads the aggregated character set from the Paratype Cyrillic language
knowledge base (a sibling `cyrillic-languages/` repository) and writes:

  * `characters-uppercase.md` / `characters-lowercase.md` — pan-Cyrillic
    master tables, one row per unique codepoint, with Unicode name,
    decomposition (base + combining marks), PUA flag, and SVG/plotter links.
  * `glyph-variants.md` — locl variant rows (glyphs that share a codepoint
    with a base letter but render differently under an OpenType `locl`).

Shared data access and decomposition logic live in `_catalog.py`, which
this script is a thin Markdown-rendering wrapper over. `generate_svgs.py`
and `generate_json.py` import from the same module.

Usage:
    python3 generate.py
    python3 generate.py --data ../cyrillic-languages --out .

Python 3.8+ stdlib only.
"""

import argparse
import sys
import unicodedata
from pathlib import Path

from _catalog import (
    CYRILLIC_BREVE_LC,
    CYRILLIC_BREVE_UC,
    LANGUAGES_IN_SCOPE,
    aggregate_variants,
    collect_glyph_variants,
    decompose,
    dedupe_by_codepoints,
    has_decomposition_hint,
    is_pua,
    load_pan_cyrillic,
    resolve_data_root,
)


# Target rendered height for inline SVG thumbnails in the Markdown tables.
# Widths per row are derived from this: img_width = svg_viewbox_w * HEIGHT / svg_viewbox_h.
# viewBox is always 2380 tall; raising this constant enlarges every thumbnail
# proportionally.
INLINE_DIAGRAM_HEIGHT = 130
VARIANT_DIAGRAM_WIDTH = round(4040 * INLINE_DIAGRAM_HEIGHT / 2380)


def format_unicodes(unicodes: list[str]) -> str:
    """Format a list of hex strings as `XXXX + XXXX + …`."""
    return " + ".join(u.upper() for u in unicodes)


def _diagram_img(family: str, subdir: str, cp_hex: str, img_width: int) -> str:
    """Inline <img> tag for one family's diagram."""
    return (
        f'<img src="svg/{family}/{subdir}/{cp_hex}.svg" width="{img_width}" '
        f'alt="{family} U+{cp_hex}">'
    )


def _txt_link(family: str, subdir: str, cp_hex: str, label: str) -> str:
    """Markdown link to a plotter source .txt file."""
    return f"[{label}](glyphplotter/{family}/{subdir}/{cp_hex}.txt)"


def _diagram_cell_both(subdir: str, cp_hex: str, img_width: int, stacked: bool) -> str:
    """Sans + Serif thumbnails together in one cell.

    * ``stacked=False`` → side-by-side (compact single-glyph rows).
    * ``stacked=True``  → Sans on top, Serif below (wide multi-box rows
      where side-by-side would overflow the column).

    Two `[txt]` links for the two plotter sources follow the images.
    """
    sans_img = _diagram_img("Sans", subdir, cp_hex, img_width)
    serif_img = _diagram_img("Serif", subdir, cp_hex, img_width)
    separator = "<br>" if stacked else " "
    txt_links = (
        f'{_txt_link("Sans", subdir, cp_hex, "txt sans")} '
        f'{_txt_link("Serif", subdir, cp_hex, "txt serif")}'
    )
    return f"{sans_img}{separator}{serif_img}<br>{txt_links}"


def render_glyph_variants_md(rows: list[dict]) -> str:
    """Render the variants table — locl (`&`) shape variants only.

    `+`-marker rows were dropped during collection: they described the
    default (pre-locl) shape that each `&` row swaps out, but the
    paired localized row's Diagram cell already renders both shapes
    side-by-side, so the alternate row was redundant information.
    """
    by_style = {"any": 0, "straight": 0, "italic": 0, "alt": 0}
    for r in rows:
        by_style[r["style"]] = by_style.get(r["style"], 0) + 1
    locales = sorted({r["locale"] for r in rows if r["locale"]})

    out: list[str] = []
    out.append("# Glyph variants")
    out.append("")
    out.append(
        "Glyphs that do **not** have their own Unicode codepoint: they "
        "share a codepoint with a base letter, but render as a different "
        "shape under an OpenType `locl` feature (a localized form "
        "selected by the active language), sometimes with a style "
        "qualifier tying the swap to upright (`.str`) or italic (`.ita`) "
        "shaping."
    )
    out.append("")
    out.append(
        "This table complements the pan-Cyrillic character tables in "
        "`characters-uppercase.md` / `characters-lowercase.md`, which are "
        "deduplicated by codepoint. The entries below are the "
        "variant-form rows that the codepoint-level view collapses."
    )
    out.append("")
    out.append(
        f"**{len(rows)}** locl variants — "
        f"styles: any={by_style['any']}, "
        f"straight={by_style.get('straight', 0)}, "
        f"italic={by_style.get('italic', 0)}. "
        f"Locales represented: {', '.join(locales) if locales else '—'}."
    )
    out.append("")
    out.append("## Columns")
    out.append("")
    out.append(
        "- **Codepoint** — the Unicode codepoint the variant swaps shape for "
        "(same as the base letter in the main table), except for the Bashkir "
        "and Chuvash PUA-locl rows where it is the target PUA codepoint."
    )
    out.append(
        "- **Case** — uppercase / lowercase."
    )
    out.append(
        "- **Locale** — `bg` Bulgarian, `sr` Serbian, `ba` Bashkir, or "
        "`cv` Chuvash. These are the four non-default (non-ru) locl tags "
        "for which PT Serif Expert carries named variant glyphs."
    )
    out.append(
        "- **Style** — `straight` or `italic` when the source token has "
        "a `.str` / `.ita` suffix; `any` otherwise."
    )
    out.append(
        "- **Diagram** — an inline SVG showing `default shape → variant "
        "shape` plus a `[txt]` link to the glyphplotter source."
    )
    out.append(
        "- **Languages** — language files that declare this variant."
    )
    out.append("")
    out.append("## Variants")
    out.append("")
    out.append("| # | Codepoint | Case | Locale | Style | Diagram (Sans / Serif) | Languages |")
    out.append("| ---: | --- | --- | --- | --- | :---: | --- |")
    for i, r in enumerate(rows, start=1):
        # Variant diagrams are always 2 boxes (default → variant): the row
        # IS a shape transformation, so stack Sans above Serif the same
        # way we stack multi-box decompositions in the main tables.
        diagram_cell = ""
        if r["locale"] and r["codepoints"]:
            cp_hex = r["codepoints"][0].upper()
            stem = f"{cp_hex}.{r['locale']}"
            sans_img = (
                f'<img src="svg/Sans/variants/{stem}.svg" width="{VARIANT_DIAGRAM_WIDTH}" '
                f'alt="Sans U+{cp_hex} .{r["locale"]}">'
            )
            serif_img = (
                f'<img src="svg/Serif/variants/{stem}.svg" width="{VARIANT_DIAGRAM_WIDTH}" '
                f'alt="Serif U+{cp_hex} .{r["locale"]}">'
            )
            txt_links = (
                f"[txt sans](glyphplotter/Sans/variants/{stem}.txt) "
                f"[txt serif](glyphplotter/Serif/variants/{stem}.txt)"
            )
            diagram_cell = f"{sans_img}<br>{serif_img}<br>{txt_links}"
        out.append(
            f"| {i} | {format_unicodes(r['codepoints'])} | {r['case']} | "
            f"{r['locale']} | {r['style']} | {diagram_cell} | "
            f"{', '.join(r['languages'])} |"
        )
    out.append("")
    return "\n".join(out)


def render_characters_md(side: str, entries: list[dict]) -> str:
    """Render the master table for either uppercase or lowercase characters."""
    case = "upper" if side == "uppercase" else "lower"

    pua_count = sum(
        1 for e in entries
        for u in e.get("unicodes", [])
        if is_pua(int(u, 16))
    )
    with_count = 0          # rows whose description contains WITH
    nfd_only_count = 0      # rows decomposed only via the NFD fallback path
    decomposed_count = 0    # rows with any decomposition
    row_cells: list[str] = []
    for entry in entries:
        description = entry.get("description", "")
        sign = entry.get("sign", "")
        unicodes = entry.get("unicodes", [])
        has_with = has_decomposition_hint(description)
        if has_with:
            with_count += 1
        seq = decompose(description, case, sign=sign)
        if seq is not None:
            decomposed_count += 1
            decomp_cell = " + ".join(f"{cp:04X}" for cp in seq)
            if not has_with:
                nfd_only_count += 1
            # Cross-validate the WITH-path result against NFD for non-PUA rows:
            # our decomposition must match NFD except that BREVE uses F6D1/F6D4
            # where NFD would use U+0306. Mismatch = accent table / base-letter
            # lookup is wrong. (The NFD-fallback path is NFD-derived by
            # construction, so no need to cross-check it.)
            is_pua_row = any(is_pua(int(u, 16)) for u in unicodes)
            if has_with and not is_pua_row and sign:
                nfd = unicodedata.normalize("NFD", sign)
                if len(nfd) > 1:
                    nfd_cps = [ord(c) for c in nfd]
                    expected = [
                        (CYRILLIC_BREVE_UC if case == "upper" else CYRILLIC_BREVE_LC)
                        if cp == 0x0306 else cp
                        for cp in nfd_cps
                    ]
                    if seq != expected:
                        raise AssertionError(
                            f"decompose mismatch for {sign!r} "
                            f"({description!r}): got {seq}, expected {expected}"
                        )
        else:
            decomp_cell = ""
        row_cells.append(decomp_cell)
    descriptive_count = with_count - (decomposed_count - nfd_only_count)

    out: list[str] = []
    out.append(f"# Pan-Cyrillic single characters — {side}")
    out.append("")
    out.append(
        f"**{len(entries)}** unique {side} characters across the 77 "
        f"languages in scope. Of these, **{pua_count}** are encoded in "
        f"the Unicode Private Use Area (E000–F8FF). "
        f"**{decomposed_count}** decompose into a base character plus "
        f"one or more combining marks — {decomposed_count - nfd_only_count} "
        f"via a `… WITH …` description and {nfd_only_count} via canonical "
        f"Unicode NFD on precomposed letters whose name carries only the "
        f"language label (Ё, Й, Ў, …). **{descriptive_count}** are "
        f"structural modifications (Descender, Hook, Tail, Stroke, Bar, "
        f"Tick, Upturn, Middle Hook, Vertical Stroke, or the Stroke+Hook "
        f"pair) with no standard combining-mark equivalent — kept as "
        f"their codepoint plus the descriptive name."
    )
    out.append("")
    out.append(
        "Decomposition note: the `BREVE` combining mark in Cyrillic rows "
        "resolves to `U+F6D1` (uppercase) / `U+F6D4` (lowercase) — the "
        "Cyrillic-shaped breve glyphs carried by Paratype Expert fonts — "
        "rather than the generic combining breve `U+0306`, whose shape "
        "does not match Cyrillic typography."
    )
    out.append("")
    out.append(
        "Codepoints are shown in uppercase hex. Multi-codepoint sequences "
        "use `XXXX + XXXX + …` in reading order (base first)."
    )
    out.append("")
    out.append("| # | Sign | Codepoint | Description | PUA | Decomposition | Diagram (Sans / Serif) | Locales |")
    out.append("| ---: | :---: | --- | --- | :---: | --- | :---: | --- |")
    subdir = "uc" if side == "uppercase" else "lc"
    for i, (entry, decomp_cell) in enumerate(zip(entries, row_cells), start=1):
        sign = entry.get("sign", "")
        unicodes = entry.get("unicodes", [])
        description = entry.get("description", "")
        pua_flag = "yes" if any(is_pua(int(u, 16)) for u in unicodes) else ""
        locales = ", ".join(entry.get("locales", []))
        # Diagram cell: show Sans + Serif together. Layout depends on the
        # diagram's natural width — single-glyph rows fit side-by-side,
        # multi-box rows are stacked vertically so the column doesn't blow
        # up past the table width.
        cp_hex = unicodes[0].upper() if unicodes else ""
        if cp_hex:
            n_accents = decomp_cell.count("+") if decomp_cell else 0
            # viewBox widths: 1440 (single), 6640 (1 accent), 9240 (2 accents)
            svg_width = 1440 if n_accents == 0 else (2600 * n_accents + 4040)
            img_width = round(svg_width * INLINE_DIAGRAM_HEIGHT / 2380)
            diagram_cell = _diagram_cell_both(
                subdir, cp_hex, img_width, stacked=(n_accents > 0)
            )
        else:
            diagram_cell = ""
        out.append(
            f"| {i} | {sign} | {format_unicodes(unicodes)} | "
            f"{description} | {pua_flag} | {decomp_cell} | "
            f"{diagram_cell} | {locales} |"
        )
    out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--data", type=Path, default=Path("../cyrillic-languages"),
        help="Path to the sibling cyrillic-languages repository "
             "(default: ../cyrillic-languages)",
    )
    parser.add_argument(
        "--out", type=Path, default=Path("."),
        help="Output directory (default: current directory)",
    )
    args = parser.parse_args(argv)

    if not args.data.exists():
        parser.error(f"--data directory does not exist: {args.data}")

    try:
        data_root = resolve_data_root(args.data)
    except FileNotFoundError as exc:
        parser.error(str(exc))

    pan = load_pan_cyrillic(data_root)
    args.out.mkdir(parents=True, exist_ok=True)

    # Read the codepoint-sorted view rather than the Paratype sort order so
    # PUA entries naturally group at the end of each table.
    upper = dedupe_by_codepoints(pan.get("uppercase_sorted_by_unicodes", []))
    lower = dedupe_by_codepoints(pan.get("lowercase_sorted_by_unicodes", []))

    (args.out / "characters-uppercase.md").write_text(
        render_characters_md("uppercase", upper), encoding="utf-8"
    )
    (args.out / "characters-lowercase.md").write_text(
        render_characters_md("lowercase", lower), encoding="utf-8"
    )

    variants = aggregate_variants(collect_glyph_variants(data_root, LANGUAGES_IN_SCOPE))
    (args.out / "glyph-variants.md").write_text(
        render_glyph_variants_md(variants), encoding="utf-8"
    )

    print(f"Wrote {args.out}/characters-uppercase.md ({len(upper)} entries)")
    print(f"Wrote {args.out}/characters-lowercase.md ({len(lower)} entries)")
    print(f"Wrote {args.out}/glyph-variants.md ({len(variants)} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
