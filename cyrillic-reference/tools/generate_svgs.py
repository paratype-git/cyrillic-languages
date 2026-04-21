#!/usr/bin/env python3
"""Render per-row SVG decomposition diagrams for the cyrillic-reference tables.

Reads the pan-Cyrillic master set and the source-language files, produces one
SVG per uppercase/lowercase codepoint and per locl/style variant. For each
SVG a companion `.txt` glyphplotter instruction file is also kept — the two
live side-by-side under `svg/{uc,lc,variants}/`.

Row types:
  * decomposable composite — base + mark(s) -> composed, e.g. Ӑ = 0410 + F6D1
  * structural composite — kept as a single glyph (Descender, Hook, Stroke, …)
  * plain letter — one glyph
  * locl/style variant — default shape -> variant shape

Requires FontDocTools (`glyphplotter` command) installed in the active Python
env; also fontTools. PT Serif Expert Regular is the rendering font.

Usage:
    python3 generate_svgs.py --font ../cyrillic-languages/fonts/web/\\
        PT-Serif-Expert_Regular/pt-serif-expert_regular.ttf
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

from fontTools.ttLib import TTFont


# ---------- calibration constants ----------
BOX_W = 1400
BOX_TOP = 1440
BOX_BOTTOM = -900
BOX_CENTER = 700
GAP = 150
DC_PEN_X = 244                     # dotted-circle pen_x in a 1400-wide box
FONT_SIZE = 1100
LABEL_FONT_SIZE = 200
LABEL_Y = -800
PLUS_GAP = 1200
ARROW_GAP = 1200
PLUS_CX, PLUS_CY, PLUS_R = 600, 200, 200
ARROW_X1, ARROW_X2, ARROW_Y = 350, 1000, 250
ARROW_STYLE = "closed60"
STROKE_BOX, STROKE_PLUS, STROKE_ARROW = 20, 80, 80
STROKE_COLOR = "9E9E9E"

# Mark-specific placement tweaks established via calibration sheet.
CYR_BREVES = {0xF6D1, 0xF6D4}
H_NUDGE_CYR_BREVE = -40
X_NUDGE_EXTRA = {0x030B: +20}      # DOUBLE ACUTE
Y_NUDGE_EXTRA = {0xF6D4: -30}      # Cyrillic lowercase breve

# Decomposition accent table — must match cyrillic-reference/generate.py.
CYRILLIC_BREVE_UC = 0xF6D1
CYRILLIC_BREVE_LC = 0xF6D4
_ACCENT_SENTINEL = object()
ACCENT_COMBINING_MARK = {
    "MACRON":       0x0304,
    "DIAERESIS":    0x0308,
    "BREVE":        _ACCENT_SENTINEL,
    "ACUTE":        0x0301,
    "CIRCUMFLEX":   0x0302,
    "GRAVE":        0x0300,
    "CARON":        0x030C,
    "DOUBLE ACUTE": 0x030B,
    "CEDILLA":      0x0327,
    "DOT ABOVE":    0x0307,
}
_WITH_RE = re.compile(r"\s+WITH\s+", re.IGNORECASE)
_AND_RE = re.compile(r"\s+AND\s+", re.IGNORECASE)


# ---------- font metrics ----------
class FontMetrics:
    def __init__(self, font_path: Path) -> None:
        self.path = font_path
        self.font = TTFont(str(font_path))
        self.cmap = self.font.getBestCmap()
        self.hmtx = self.font["hmtx"]
        self.glyf = self.font["glyf"]
        # Dotted-circle metrics — only needed by mark-on-dotted-circle boxes
        # (decomposable composites). Italic font has no U+25CC and that's
        # fine because variant diagrams don't draw dotted circles.
        if 0x25CC in self.cmap:
            dc = self.glyf[self.cmap[0x25CC]]
            self.dc_yMin = dc.yMin
            self.dc_yMax = dc.yMax
        else:
            self.dc_yMin = None
            self.dc_yMax = None

    def glyph_name(self, cp: int) -> str:
        return self.cmap[cp]

    def advance(self, name: str) -> int:
        aw, _ = self.hmtx[name]
        return aw

    def bbox(self, name: str) -> tuple[int, int, int, int]:
        g = self.glyf[name]
        return (
            getattr(g, "xMin", 0), getattr(g, "yMin", 0),
            getattr(g, "xMax", 0), getattr(g, "yMax", 0),
        )

    def pen_for_mark(self, cp: int) -> tuple[int, int]:
        """Pen (x, y) for a combining mark drawn on a dotted circle."""
        name = self.glyph_name(cp)
        xMin, yMin, xMax, yMax = self.bbox(name)
        bbox_cx = (xMin + xMax) / 2
        bbox_cy = (yMin + yMax) / 2
        h_nudge = (H_NUDGE_CYR_BREVE if cp in CYR_BREVES else 0) + X_NUDGE_EXTRA.get(cp, 0)
        v_nudge = Y_NUDGE_EXTRA.get(cp, 0)
        pen_x = int(round(BOX_CENTER + h_nudge - bbox_cx))
        if bbox_cy >= 0:
            pen_y = int(round((self.dc_yMax + GAP) - yMin)) + v_nudge
        else:
            pen_y = int(round((self.dc_yMin - GAP) - yMax)) + v_nudge
        return pen_x, pen_y

    def pen_for_letter(self, name: str) -> int:
        return int(round((BOX_W - self.advance(name)) / 2))


# ---------- decomposition (duplicated from generate.py to keep scripts standalone) ----------
_KNOWN_COMBINING_MARK_CPS = {
    0x0304, 0x0308, 0x0306, 0x0301, 0x0302,
    0x0300, 0x030C, 0x030B, 0x0327, 0x0307,
}


def _swap_breve(cp: int, case: str) -> int:
    if cp == 0x0306:
        return CYRILLIC_BREVE_UC if case == "upper" else CYRILLIC_BREVE_LC
    return cp


def decompose(description: str, case: str, sign: str = "") -> list[int] | None:
    """Same two-path logic as generate.py: WITH first, NFD fallback."""
    parts = _WITH_RE.split(description, maxsplit=1)
    if len(parts) == 2:
        base_name, phrase = parts
        tokens = [t.strip().upper() for t in _AND_RE.split(phrase)]
        mapped: list[int] = []
        for token in tokens:
            mark = ACCENT_COMBINING_MARK.get(token)
            if mark is None:
                return None
            if mark is _ACCENT_SENTINEL:
                mapped.append(_swap_breve(0x0306, case))
            else:
                mapped.append(mark)
        try:
            base_char = unicodedata.lookup(base_name.strip().upper())
        except KeyError:
            return None
        return [ord(base_char), *mapped]

    if sign:
        nfd = unicodedata.normalize("NFD", sign)
        if len(nfd) > 1:
            cps = [ord(c) for c in nfd]
            if all(cp in _KNOWN_COMBINING_MARK_CPS for cp in cps[1:]):
                return [cps[0], *(_swap_breve(cp, case) for cp in cps[1:])]

    return None


# ---------- instruction emitters ----------
def header_comment(txt_path: Path, svg_path: Path, font_hint: str) -> list[str]:
    """Leading comment listing the exact glyphplotter command that produces
    this .svg from this .txt. Paths are rendered relative to the
    cyrillic-reference directory (the subproject root), so the command is
    reproducible by running from that directory.
    """
    return [
        "# Generated by cyrillic-reference/tools/generate_svgs.py",
        "# To re-render manually (from cyrillic-reference/):",
        f"#   glyphplotter --input {txt_path} \\",
        f"#                --output {svg_path} \\",
        f"#                --font <path>/{font_hint}",
        "",
    ]


def box_for_letter(fm: FontMetrics, name: str, label: str) -> list[str]:
    pen_x = fm.pen_for_letter(name)
    return [
        f"# ==== Box: {label}",
        f"strokeWidth {STROKE_BOX}",
        f"strokeColor {STROKE_COLOR}",
        f"drawRectangle pen 0 {BOX_TOP} {BOX_W} {BOX_BOTTOM} stroke",
        "glyphMode fill",
        f"drawGlyph pen {pen_x} 0 /{name}",
        f'drawLabel pen {BOX_CENTER} {LABEL_Y} center "{label}"',
        f"move {BOX_W}",
    ]


def box_for_mark(fm: FontMetrics, mark_cp: int) -> list[str]:
    mark_name = fm.glyph_name(mark_cp)
    pen_x, pen_y = fm.pen_for_mark(mark_cp)
    return [
        f"# ==== Box: U+{mark_cp:04X} on dotted circle",
        f"strokeWidth {STROKE_BOX}",
        f"strokeColor {STROKE_COLOR}",
        f"drawRectangle pen 0 {BOX_TOP} {BOX_W} {BOX_BOTTOM} stroke",
        f"drawGlyph pen {DC_PEN_X} 0 /uni25CC",
        f"drawGlyph pen {pen_x} {pen_y} /{mark_name}",
        f'drawLabel pen {BOX_CENTER} {LABEL_Y} center "U+{mark_cp:04X}"',
        f"move {BOX_W}",
    ]


def plus_separator() -> list[str]:
    return [
        "# ==== Plus",
        "strokeDash 0 0",
        f"strokeWidth {STROKE_PLUS}",
        f"strokeColor {STROKE_COLOR}",
        f"drawCross pen {PLUS_CX} {PLUS_CY} {PLUS_R}",
        f"move {PLUS_GAP}",
    ]


def arrow_separator() -> list[str]:
    return [
        "# ==== Arrow",
        "strokeDash 0 0",
        f"strokeWidth {STROKE_ARROW}",
        f"strokeColor {STROKE_COLOR}",
        f"drawArrow pen {ARROW_X1} {ARROW_Y} {ARROW_X2} {ARROW_Y} {ARROW_STYLE}",
        f"move {ARROW_GAP}",
    ]


def preamble() -> list[str]:
    # Paint an opaque white background first so the SVG doesn't show through
    # when embedded in a Markdown viewer using a dark theme. Reset fillColor
    # to black afterwards so glyphs render in their usual ink color.
    return [
        f"fontSize {FONT_SIZE}",
        f"labelFontSize {LABEL_FONT_SIZE}",
        "fillColor FFFFFF",
        "drawBackground",
        "fillColor 000000",
        "",
    ]


# ---------- row builders ----------
def build_decomposable(fm: FontMetrics, base_cp: int, marks: list[int], composed_cp: int) -> list[str]:
    lines: list[str] = preamble()
    lines += box_for_letter(fm, fm.glyph_name(base_cp), f"U+{base_cp:04X}")
    for mark_cp in marks:
        lines.append("")
        lines += plus_separator()
        lines.append("")
        lines += box_for_mark(fm, mark_cp)
    lines.append("")
    lines += arrow_separator()
    lines.append("")
    lines += box_for_letter(fm, fm.glyph_name(composed_cp), f"U+{composed_cp:04X}")
    return lines


def build_single(fm: FontMetrics, cp: int) -> list[str]:
    lines: list[str] = preamble()
    lines += box_for_letter(fm, fm.glyph_name(cp), f"U+{cp:04X}")
    return lines


def build_variant(fm: FontMetrics, cp: int, variant_name: str, locale: str) -> list[str]:
    """default shape -> variant shape."""
    lines: list[str] = preamble()
    lines += box_for_letter(fm, fm.glyph_name(cp), f"U+{cp:04X}")
    lines.append("")
    lines += arrow_separator()
    lines.append("")
    lines += box_for_letter(fm, variant_name, f"U+{cp:04X} .{locale}")
    return lines


# ---------- writer / renderer ----------
def write_txt(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_svg(txt_path: Path, svg_path: Path, font_path: Path) -> None:
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.setdefault("PYTHON_GIL", "1")
    cmd = [
        "glyphplotter",
        "--input", str(txt_path),
        "--output", str(svg_path),
        "--font", str(font_path),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if res.returncode != 0:
        raise RuntimeError(
            f"glyphplotter failed for {txt_path.name}:\n"
            f"stdout:\n{res.stdout}\nstderr:\n{res.stderr}"
        )


# ---------- main driver ----------
def find_locl_variant(fm: FontMetrics, cp: int, locale: str) -> str | None:
    """Look up the locl variant glyph name (e.g. uni0492.BSH) in the TTF.

    locale is our data's short code; the TTF suffixes are capitalized
    3-letter tags: ba->BSH, bg->BGR, cv->CHU, sr->SRB.
    """
    locale_map = {"ba": "BSH", "bg": "BGR", "cv": "CHU", "sr": "SRB"}
    suffix = locale_map.get(locale)
    if not suffix:
        return None
    base = fm.cmap.get(cp)
    if not base:
        return None
    candidate = f"{base}.{suffix}"
    return candidate if candidate in fm.font.getGlyphOrder() else None


def process_main(
    fm: FontMetrics,
    pan: dict,
    font_hint: str,
    txt_root: Path,
    svg_root: Path,
    font_path: Path,
) -> dict:
    """Emit .txt+.svg for every uppercase/lowercase row. Return stats."""
    stats = {"uc": {"decomposed": 0, "single": 0}, "lc": {"decomposed": 0, "single": 0}}
    for case_key, case, subdir in (
        ("uppercase_sorted_by_unicodes", "upper", "uc"),
        ("lowercase_sorted_by_unicodes", "lower", "lc"),
    ):
        seen: dict[str, dict] = {}
        for entry in pan.get(case_key, []):
            cp_hex = entry["unicodes"][0].upper()
            if cp_hex in seen:
                continue
            seen[cp_hex] = entry
        for cp_hex, entry in seen.items():
            cp = int(cp_hex, 16)
            description = entry.get("description", "")
            sign = entry.get("sign", "")
            decomp = decompose(description, case, sign=sign)
            if decomp is not None:
                lines = build_decomposable(fm, decomp[0], decomp[1:], cp)
                stats[subdir]["decomposed"] += 1
            else:
                lines = build_single(fm, cp)
                stats[subdir]["single"] += 1
            txt_path = txt_root / subdir / f"{cp_hex}.txt"
            svg_path = svg_root / subdir / f"{cp_hex}.svg"
            full_lines = header_comment(txt_path, svg_path, font_hint) + lines
            write_txt(txt_path, full_lines)
            render_svg(txt_path, svg_path, font_path)
    return stats


def process_variants(
    fm_regular: FontMetrics,
    fm_italic: FontMetrics | None,
    data_root: Path,
    font_regular: Path,
    font_italic: Path | None,
    txt_root: Path,
    svg_root: Path,
) -> dict:
    """Emit .txt+.svg for every locl/style variant row.

    Three variant shapes are handled:

    * ``&letter`` — locl shape of a single Cyrillic letter. Variant
      glyph is ``uni<cp>.<SUFFIX>`` in the regular font. E.g. ``&Д``
      under Bulgarian locl ⇒ ``uni0414.BGR``.
    * ``&letter.ita`` — locl shape that only exists in italic (Serbian
      italic г, д, п, т, ш). Variant glyph is ``uni<cp>.SRB`` in the
      italic font; the default is also drawn from the italic font so
      the two side-by-side show the same italic context.
    * ``&!FXXX`` — locl shape that is itself a PUA codepoint (Bashkir
      and Chuvash). The diagram's left side is the paired ``+BASE``
      token that immediately follows in the source; the right side is
      the PUA glyph ``uniFXXX`` from the regular font.
    """
    locale_map = {"ba": "BSH", "bg": "BGR", "cv": "CHU", "sr": "SRB"}
    base_dir = data_root / "library" / "cyrillic" / "base"
    pua_tok = re.compile(r"^!([0-9A-Fa-f]{4,5})$")
    seen: set[tuple[str, int, str, str]] = set()
    stats = {"regular": 0, "italic": 0, "pua_pair": 0,
             "skipped_missing_pair": 0, "skipped_missing_variant": 0}

    def _strip_style_suffix(rest: str) -> tuple[str, str]:
        for sfx, label in ((".ita", "italic"), (".str", "straight"), (".alt", "alt")):
            if rest.endswith(sfx):
                return rest[:-len(sfx)], label
        return rest, "any"

    for lang_file in sorted(base_dir.glob("*.json")):
        with lang_file.open(encoding="utf-8") as f:
            data = json.load(f)
        locale = data.get("local", "")
        if locale not in locale_map:
            continue
        for block in data.get("glyphs_list", []):
            for side in ("uppercase", "lowercase"):
                tokens = (block.get(side, "") or "").split()
                for i, token in enumerate(tokens):
                    if not token or token[0] != "&":
                        continue
                    rest, style = _strip_style_suffix(token[1:])
                    if not rest:
                        continue

                    pm = pua_tok.match(rest)
                    if pm:
                        # &!FXXX — PUA locl. Pair with the immediate +BASE.
                        variant_cp = int(pm.group(1), 16)
                        if i + 1 >= len(tokens) or not tokens[i + 1].startswith("+"):
                            stats["skipped_missing_pair"] += 1
                            continue
                        pair_rest, _ = _strip_style_suffix(tokens[i + 1][1:])
                        pair_pm = pua_tok.match(pair_rest)
                        if pair_pm:
                            base_cp = int(pair_pm.group(1), 16)
                        elif len(pair_rest) == 1:
                            base_cp = ord(pair_rest)
                        else:
                            stats["skipped_missing_pair"] += 1
                            continue
                        variant_name = fm_regular.glyph_name(variant_cp)
                        fm_for_this = fm_regular
                        font_for_this = font_regular
                        file_cp = variant_cp
                        category = "pua_pair"
                    else:
                        if len(rest) != 1:
                            continue
                        base_cp = ord(rest)
                        suffix = locale_map[locale]
                        variant_name = f"uni{base_cp:04X}.{suffix}"
                        if style == "italic" and fm_italic is not None:
                            fm_for_this = fm_italic
                            font_for_this = font_italic
                            category = "italic"
                        else:
                            fm_for_this = fm_regular
                            font_for_this = font_regular
                            category = "regular"
                        if variant_name not in fm_for_this.font.getGlyphOrder():
                            stats["skipped_missing_variant"] += 1
                            continue
                        file_cp = base_cp

                    key = (locale, file_cp, side, style)
                    if key in seen:
                        continue
                    seen.add(key)

                    cp_hex = f"{file_cp:04X}"
                    stem = f"{cp_hex}.{locale}"
                    txt_path = txt_root / "variants" / f"{stem}.txt"
                    svg_path = svg_root / "variants" / f"{stem}.svg"
                    lines = build_variant(fm_for_this, base_cp, variant_name, locale)
                    full_lines = header_comment(
                        txt_path, svg_path, font_for_this.name
                    ) + lines
                    write_txt(txt_path, full_lines)
                    render_svg(txt_path, svg_path, font_for_this)
                    stats[category] += 1
    return stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data", type=Path, default=Path("../cyrillic-languages"),
                        help="Path to the sibling cyrillic-languages repository")
    parser.add_argument("--font", type=Path, required=True,
                        help="Path to pt-serif-expert_regular.ttf")
    parser.add_argument("--font-italic", type=Path, default=None,
                        help="Path to pt-serif-expert_italic.ttf "
                             "(needed to render Serbian italic locl variants)")
    parser.add_argument("--family", required=True, choices=("Sans", "Serif"),
                        help="Output subdir name under svg/ and glyphplotter/")
    parser.add_argument("--root", type=Path, default=Path("."),
                        help="Subproject root (default: current directory). "
                             "SVGs go to <root>/svg/<family>/... and "
                             "plotter sources to <root>/glyphplotter/<family>/...")
    args = parser.parse_args(argv)

    if not args.font.exists():
        parser.error(f"Font not found: {args.font}")
    if args.font_italic is not None and not args.font_italic.exists():
        parser.error(f"Italic font not found: {args.font_italic}")
    if not (args.data / "site" / "cyrillic" / "cyrillic_characters_lib.json").exists():
        parser.error(f"pan-Cyrillic summary not found under {args.data}")

    fm_regular = FontMetrics(args.font)
    fm_italic = FontMetrics(args.font_italic) if args.font_italic else None

    pan_path = args.data / "site" / "cyrillic" / "cyrillic_characters_lib.json"
    with pan_path.open(encoding="utf-8") as f:
        pan = json.load(f)

    svg_root = args.root / "svg" / args.family
    txt_root = args.root / "glyphplotter" / args.family

    print(f"Rendering {args.family} main character SVGs (uc, lc)…")
    stats = process_main(fm_regular, pan, args.font.name, txt_root, svg_root, args.font)
    print(f"  uc: {stats['uc']['decomposed']} decomposed, {stats['uc']['single']} single")
    print(f"  lc: {stats['lc']['decomposed']} decomposed, {stats['lc']['single']} single")

    print(f"Rendering {args.family} locl/style variants…")
    vstats = process_variants(
        fm_regular, fm_italic, args.data,
        args.font, args.font_italic,
        txt_root, svg_root,
    )
    print(f"  regular:  {vstats['regular']}")
    print(f"  italic:   {vstats['italic']}")
    print(f"  PUA pair: {vstats['pua_pair']}")
    if vstats["skipped_missing_variant"]:
        print(f"  skipped (no named variant in font): {vstats['skipped_missing_variant']}")
    if vstats["skipped_missing_pair"]:
        print(f"  skipped (no +BASE pair for &!PUA):   {vstats['skipped_missing_pair']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
