#!/usr/bin/env python3
"""Emit per-language JSON deliverables + pan-Cyrillic reference JSON.

Reads:
  cyrillic-reference/characters-uppercase.md   ← pan character catalog (source of truth for descriptions, decomposition, svg paths)
  cyrillic-reference/characters-lowercase.md
  cyrillic-reference/glyph-variants.md         ← locl-variant catalog
  cyrillic-reference/language-tags.json        ← BCP47 / OT / ISO enrichment
  cyrillic-languages/library/cyrillic/cyrillic_library.json
  cyrillic-languages/library/cyrillic/base/<Language>.json (×79)

Writes:
  cyrillic-reference/data/pan-cyrillic.json
  cyrillic-reference/data/languages/<Language>.json (×77 — Kaitag, Uzbek skipped)
"""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
REF = ROOT
LANGS_REPO = REPO / "cyrillic-languages"
BASE_DIR = LANGS_REPO / "library" / "cyrillic" / "base"
LIBRARY_JSON = LANGS_REPO / "library" / "cyrillic" / "cyrillic_library.json"
TAGS_JSON = REF / "language-tags.json"

UC_MD = REF / "characters-uppercase.md"
LC_MD = REF / "characters-lowercase.md"
VAR_MD = REF / "glyph-variants.md"

OUT_DIR = REF / "data"
OUT_LANGS_DIR = OUT_DIR / "languages"
OUT_PAN = OUT_DIR / "pan-cyrillic.json"

SKIP_LANGUAGES = {"Kaitag", "Uzbek"}

# 4-letter OT feature tags for the 4 locl-bearing locales. The font exposes
# locl substitutions keyed by these OT tags. Macedonian is patched to sr
# (see memory: macedonian_language_tag_patch); MKD locl does not exist.
LOCL_FEATURE = {
    "bg": "BGR ",
    "sr": "SRB ",
    "ba": "BSH ",
    "cv": "CHU ",
}


# ─── MD parsing ────────────────────────────────────────────────────────────

def parse_md_table(path: Path, columns: list[str]) -> list[dict]:
    rows: list[dict] = []
    header: list[str] | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            if cells and cells[0] == "#":
                header = cells
            continue
        if set("".join(cells)) <= {"-", ":", " "}:
            continue
        row = dict(zip(header, cells))
        rows.append({col: row.get(col, "") for col in columns})
    return rows


def parse_decomposition(s: str) -> list[str]:
    if not s.strip():
        return []
    return [p.strip().upper() for p in s.split("+") if p.strip()]


def case_dir(case: str) -> str:
    if case == "uppercase":
        return "uc"
    if case == "lowercase":
        return "lc"
    return "lc"  # common / caseless share the lc SVG path in current repo


def build_pan_catalog() -> dict[str, dict]:
    """{codepoint: {character, codepoint, decomposition, case, description, diagram}}"""
    catalog: dict[str, dict] = {}
    cols = ["Sign", "Codepoint", "Description", "PUA", "Decomposition", "Locales"]

    for md_path, case in [(UC_MD, "uppercase"), (LC_MD, "lowercase")]:
        for r in parse_md_table(md_path, cols):
            cp = r["Codepoint"].upper().strip()
            if not cp:
                continue
            effective_case = "common" if cp == "02BC" else case
            # apostrophe shows up in both files; keep the first emitted entry
            if cp in catalog:
                continue
            cdir = case_dir(effective_case)
            catalog[cp] = {
                "character": r["Sign"],
                "codepoint": cp,
                "decomposition": parse_decomposition(r["Decomposition"]),
                "case": effective_case,
                "description": r["Description"],
                "diagram": {
                    "svg": {
                        "sans":  f"svg/Sans/{cdir}/{cp}.svg",
                        "serif": f"svg/Serif/{cdir}/{cp}.svg",
                    },
                    "plotter": {
                        "sans":  f"glyphplotter/Sans/{cdir}/{cp}.txt",
                        "serif": f"glyphplotter/Serif/{cdir}/{cp}.txt",
                    },
                },
            }
    return catalog


def build_variants_catalog() -> dict[str, list[dict]]:
    """{codepoint: [variant_dict, ...]} from glyph-variants.md."""
    cols = ["Codepoint", "Case", "Locale", "Style", "Languages"]
    out: dict[str, list[dict]] = {}
    for r in parse_md_table(VAR_MD, cols):
        cp = r["Codepoint"].upper().strip()
        locale = r["Locale"].strip()
        style = r["Style"].strip() or "any"
        langs = [x.strip() for x in r["Languages"].split(",") if x.strip()]
        variant_base = f"{cp}.{locale}"
        out.setdefault(cp, []).append({
            "kind": "locl",
            "language_tag": locale,
            "feature_locl_tag": LOCL_FEATURE.get(locale, ""),
            "style": style,
            "diagram": {
                "svg": {
                    "sans":  f"svg/Sans/variants/{variant_base}.svg",
                    "serif": f"svg/Serif/variants/{variant_base}.svg",
                },
                "plotter": {
                    "sans":  f"glyphplotter/Sans/variants/{variant_base}.txt",
                    "serif": f"glyphplotter/Serif/variants/{variant_base}.txt",
                },
            },
            "used_by": langs,
        })
    return out


# ─── per-language codepoint extraction ─────────────────────────────────────

_ESCAPE_RE = re.compile(r"^!([0-9A-Fa-f]{4,6})$")


def token_to_codepoint(tok: str) -> str | None:
    """Resolve a glyphs_list token (already stripped of leading +/&/: markers)
    to a single-codepoint hex, or None if it's a digraph / unparseable.

    Accepts:
      - single Unicode character  → ord → 4-hex
      - escape form "!FXXX" / "!FXXXX"
      - style-qualified single char "г.ita" / "Д.str"
    Rejects multi-char tokens without the style suffix (digraphs).
    """
    if not tok:
        return None
    m = _ESCAPE_RE.match(tok)
    if m:
        return m.group(1).upper().zfill(4)
    # strip known style suffix
    base = tok
    if "." in tok:
        head, sep, suffix = tok.partition(".")
        if suffix in ("ita", "str"):
            base = head
        else:
            return None  # unknown suffix → skip
    if len(base) == 1:
        return f"{ord(base):04X}"
    return None


def extract_language_codepoints(base: dict) -> dict[str, dict]:
    """{codepoint: {case, categories: set[str]}} for this language."""
    out: dict[str, dict] = {}
    for block in base.get("glyphs_list", []):
        block_type = block.get("type", "alphabet")
        for field, case_name in [("uppercase", "uppercase"), ("lowercase", "lowercase")]:
            s = block.get(field, "") or ""
            for tok in s.split():
                if not tok:
                    continue
                if tok[0] == ":":
                    continue  # explicit digraph marker
                if tok[0] in "+&":
                    rest = tok[1:]
                else:
                    rest = tok
                cp = token_to_codepoint(rest)
                if cp is None:
                    continue
                entry = out.setdefault(cp, {"case": case_name, "categories": set()})
                entry["categories"].add(block_type)
    return out


# ─── output assembly ───────────────────────────────────────────────────────

def char_entry_for_language(cp: str, cat_info: dict, pan_entry: dict,
                             variants_for_cp: list[dict],
                             language_name: str) -> dict:
    out = {
        "character": pan_entry["character"],
        "codepoint": pan_entry["codepoint"],
        "decomposition": list(pan_entry["decomposition"]),
        "case": pan_entry["case"],
        "description": pan_entry["description"],
        "categories": sorted(cat_info["categories"]),
        "diagram": pan_entry["diagram"],
        "variants": [],
    }
    for v in variants_for_cp:
        if language_name in v["used_by"]:
            out["variants"].append({
                "kind": v["kind"],
                "language_tag": v["language_tag"],
                "feature_locl_tag": v["feature_locl_tag"],
                "style": v["style"],
                "diagram": v["diagram"],
            })
    return out


def char_entry_for_pan(cp: str, pan_entry: dict,
                        variants_for_cp: list[dict],
                        used_by: list[str]) -> dict:
    return {
        "character": pan_entry["character"],
        "codepoint": pan_entry["codepoint"],
        "decomposition": list(pan_entry["decomposition"]),
        "case": pan_entry["case"],
        "description": pan_entry["description"],
        "diagram": pan_entry["diagram"],
        "variants": [
            {
                "kind": v["kind"],
                "language_tag": v["language_tag"],
                "feature_locl_tag": v["feature_locl_tag"],
                "style": v["style"],
                "diagram": v["diagram"],
                "used_by": sorted(v["used_by"]),
            }
            for v in variants_for_cp
        ],
        "used_by": sorted(used_by),
    }


def build_url(name_eng: str) -> str:
    q = urllib.parse.quote(name_eng, safe="()")
    return f"https://paratype.github.io/cyrillic-languages/index.html?lang={q}&group=cyrillic&ui=en&pg=2"


def coerce_code_pt(v) -> int | str | None:
    if v is None:
        return None
    s = str(v)
    return int(s) if s.isdigit() else s


# ─── main ──────────────────────────────────────────────────────────────────

def main() -> int:
    library_list = json.loads(LIBRARY_JSON.read_text(encoding="utf-8"))
    tags_list = json.loads(TAGS_JSON.read_text(encoding="utf-8"))
    registry = {x["name_eng"]: x for x in library_list}
    tags = {x["name_eng"]: x for x in tags_list}

    pan_catalog = build_pan_catalog()
    variants_by_cp = build_variants_catalog()

    # Pass 1: per-language codepoint extraction + reverse index
    enabled_in_scope = [x for x in library_list
                        if x.get("enable") and x["name_eng"] not in SKIP_LANGUAGES]

    per_lang_codepoints: dict[str, dict[str, dict]] = {}
    cp_to_langs: dict[str, list[str]] = {}
    for reg in enabled_in_scope:
        name = reg["name_eng"]
        base_path = BASE_DIR / f"{name}.json"
        if not base_path.exists():
            print(f"warning: missing base file {base_path}", file=sys.stderr)
            continue
        base = json.loads(base_path.read_text(encoding="utf-8"))
        codepoints = extract_language_codepoints(base)
        per_lang_codepoints[name] = codepoints
        for cp in codepoints:
            cp_to_langs.setdefault(cp, []).append(name)

    # Pass 2: write pan-cyrillic
    OUT_DIR.mkdir(exist_ok=True)
    OUT_LANGS_DIR.mkdir(exist_ok=True)

    pan_characters = []
    for cp in sorted(pan_catalog.keys(), key=lambda x: int(x, 16)):
        used_by = cp_to_langs.get(cp, [])
        if not used_by:
            continue  # codepoint in MD but not used by any in-scope language
        pan_characters.append(char_entry_for_pan(
            cp, pan_catalog[cp], variants_by_cp.get(cp, []), used_by
        ))

    pan_out = {
        "meta": {
            "description": "Pan-Cyrillic character reference across 77 languages. "
                           "Sorted by Unicode codepoint (ascending hex). "
                           "Variants nested under the base character.",
            "languages_in_scope": len(enabled_in_scope),
            "generated_by": "cyrillic-reference/tools/generate_json.py",
        },
        "characters": pan_characters,
    }
    OUT_PAN.write_text(json.dumps(pan_out, ensure_ascii=False, indent=4) + "\n",
                       encoding="utf-8")
    print(f"wrote {len(pan_characters)} characters → {OUT_PAN.relative_to(REPO)}")

    # Pass 3: write per-language files
    written = 0
    warnings: list[str] = []
    for reg in enabled_in_scope:
        name = reg["name_eng"]
        codepoints = per_lang_codepoints.get(name, {})
        if not codepoints:
            continue
        base = json.loads((BASE_DIR / f"{name}.json").read_text(encoding="utf-8"))
        tag = tags.get(name, {})

        alts = [a for a in base.get("alt_names_eng", []) if a != name]

        meta = {
            "name_eng": name,
            "name_rus": base.get("name_rus"),
            "alternative_names": alts,
            "code_pt": coerce_code_pt(reg.get("code_pt")),
            "url": build_url(name),
            "language_tag": reg.get("language_tag") or tag.get("bcp47"),
            "default_language_tag": base.get("local"),
            "feature_locl_tag": tag.get("ot_lang"),
            "iso639_1": tag.get("iso639_1"),
            "iso639_3": tag.get("iso639_3"),
            "confidence": tag.get("confidence"),
            "note": tag.get("note"),
        }

        chars = []
        for cp in sorted(codepoints.keys(), key=lambda x: int(x, 16)):
            if cp not in pan_catalog:
                warnings.append(f"{name}: codepoint {cp} not in pan catalog (from base)")
                continue
            chars.append(char_entry_for_language(
                cp, codepoints[cp], pan_catalog[cp],
                variants_by_cp.get(cp, []), name,
            ))

        out = {"meta": meta, "characters": chars}
        fname = name.replace(" ", "_") + ".json"
        (OUT_LANGS_DIR / fname).write_text(
            json.dumps(out, ensure_ascii=False, indent=4) + "\n",
            encoding="utf-8",
        )
        written += 1

    print(f"wrote {written} per-language files → {OUT_LANGS_DIR.relative_to(REPO)}")
    if warnings:
        print(f"{len(warnings)} warnings:", file=sys.stderr)
        for w in warnings[:25]:
            print(f"  {w}", file=sys.stderr)
        if len(warnings) > 25:
            print(f"  ... and {len(warnings) - 25} more", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
