#!/usr/bin/env python3
"""Emit per-language JSON deliverables + pan-Cyrillic reference JSON.

Reads (all via _catalog):
  cyrillic-languages/site/cyrillic/cyrillic_characters_lib.json     pan catalog
  cyrillic-languages/library/cyrillic/base/<Language>.json         per-language tokens
  cyrillic-languages/library/cyrillic/cyrillic_library.json         registry
  cyrillic-reference/language-tags.json                             BCP 47 / OT / ISO

Writes:
  cyrillic-reference/data/pan-cyrillic.json
  cyrillic-reference/data/languages/<Name>.json (×77 — Kaitag, Uzbek skipped)

Independent of the Markdown tables — produces JSON directly from the compile
pipeline's output plus the raw base files for variant markers.
"""

from __future__ import annotations

import json
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # noqa: E402

from _catalog import (
    LANGUAGES_IN_SCOPE,
    LOCL_FEATURE,
    SKIP_LANGUAGES,
    aggregate_variants,
    collect_glyph_variants,
    decompose,
    dedupe_by_codepoints,
    extract_language_codepoints,
    load_pan_cyrillic,
    resolve_data_root,
)

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
LANGS_REPO = REPO / "cyrillic-languages"
BASE_DIR = LANGS_REPO / "library" / "cyrillic" / "base"
LIBRARY_JSON = LANGS_REPO / "library" / "cyrillic" / "cyrillic_library.json"
TAGS_JSON = ROOT / "language-tags.json"

OUT_DIR = ROOT / "data"
OUT_LANGS_DIR = OUT_DIR / "languages"
OUT_PAN = OUT_DIR / "pan-cyrillic.json"


# ─── diagram paths ─────────────────────────────────────────────────────────

def _case_dir(case: str) -> str:
    if case == "uppercase":
        return "uc"
    if case == "lowercase":
        return "lc"
    return "lc"  # common (U+02BC) shares the lc SVG/plotter files


def diagram_for_character(cp: str, case: str) -> dict:
    cdir = _case_dir(case)
    return {
        "svg":     {"sans":  f"svg/Sans/{cdir}/{cp}.svg",
                    "serif": f"svg/Serif/{cdir}/{cp}.svg"},
        "plotter": {"sans":  f"glyphplotter/Sans/{cdir}/{cp}.txt",
                    "serif": f"glyphplotter/Serif/{cdir}/{cp}.txt"},
    }


def diagram_for_variant(cp: str, locale: str) -> dict:
    stem = f"{cp}.{locale}"
    return {
        "svg":     {"sans":  f"svg/Sans/variants/{stem}.svg",
                    "serif": f"svg/Serif/variants/{stem}.svg"},
        "plotter": {"sans":  f"glyphplotter/Sans/variants/{stem}.txt",
                    "serif": f"glyphplotter/Serif/variants/{stem}.txt"},
    }


# ─── pan catalog (codepoint → base record) ─────────────────────────────────

def build_pan_by_cp(pan: dict) -> dict[str, dict]:
    """Build {codepoint_hex: base_record} from the pan-script summary.

    base_record fields: character, codepoint, decomposition, case,
    description, diagram. Decomposition runs through the _catalog.decompose
    (Paratype-aware NFD); structural composites and plain letters get `[]`.

    U+02BC (modifier apostrophe) appears in both uc and lc lists; we keep
    the first emission and mark it case="common".
    """
    catalog: dict[str, dict] = {}
    for list_key, case in [
        ("uppercase_sorted_by_unicodes", "uppercase"),
        ("lowercase_sorted_by_unicodes", "lowercase"),
    ]:
        for entry in dedupe_by_codepoints(pan.get(list_key, [])):
            unicodes = entry.get("unicodes") or []
            if not unicodes:
                continue
            cp = unicodes[0].upper()
            if cp in catalog:
                continue
            effective_case = "common" if cp == "02BC" else case
            decomp_case = "upper" if case == "uppercase" else "lower"
            seq = decompose(
                entry.get("description", ""),
                decomp_case,
                sign=entry.get("sign", ""),
            )
            decomposition = [f"{c:04X}" for c in seq] if seq else []
            catalog[cp] = {
                "character": entry.get("sign", ""),
                "codepoint": cp,
                "decomposition": decomposition,
                "case": effective_case,
                "description": entry.get("description", ""),
                "diagram": diagram_for_character(cp, effective_case),
            }
    return catalog


def reverse_index_from_per_lang(
        per_lang_codepoints: dict[str, dict[str, dict]]) -> dict[str, list[str]]:
    """{codepoint_hex: sorted list of language names that hold this codepoint
    as a standalone character in their `characters[]` list}.

    Derived from the same extract as per-language output so the inverse
    invariant holds: cp ∈ lang.characters[] ↔ lang ∈ pan[cp].used_by[].
    Languages that reference a codepoint only inside a multi-char digraph
    token (e.g. Abkhazian's `Ӡʼ` → 02BC) don't count here — the codepoint
    is filtered out of their per-language characters[].
    """
    out: dict[str, set[str]] = {}
    for lang, cps in per_lang_codepoints.items():
        for cp in cps:
            out.setdefault(cp, set()).add(lang)
    return {cp: sorted(names) for cp, names in out.items()}


# ─── variants ──────────────────────────────────────────────────────────────

def build_variants_by_cp(data_root: Path, in_scope: list[str],
                          case_by_cp: dict[str, str]) -> dict[str, list[dict]]:
    """{codepoint_hex: [variant_entry, ...]}.

    Aggregates `&` marker tokens from in-scope base files. Each entry
    carries kind, language_tag (BCP 47 == the OT locale trigger after the
    Macedonian patch), feature_locl_tag, style, diagram, used_by.
    """
    raw = aggregate_variants(collect_glyph_variants(data_root, in_scope))
    out: dict[str, list[dict]] = {}
    for v in raw:
        cp = v["codepoints"][0].upper()
        out.setdefault(cp, []).append({
            "kind": "locl",
            "language_tag": v["locale"],
            "feature_locl_tag": LOCL_FEATURE.get(v["locale"], ""),
            "style": v["style"],
            "diagram": diagram_for_variant(cp, v["locale"]),
            "used_by": list(v["languages"]),  # already sorted by aggregate_variants
        })
    return out


# ─── per-language & pan output assembly ────────────────────────────────────

def char_entry_for_pan(pan_entry: dict, variants: list[dict],
                        used_by: list[str]) -> dict:
    return {
        "character": pan_entry["character"],
        "codepoint": pan_entry["codepoint"],
        "decomposition": list(pan_entry["decomposition"]),
        "case": pan_entry["case"],
        "description": pan_entry["description"],
        "diagram": pan_entry["diagram"],
        "variants": variants,
        "used_by": used_by,
    }


def char_entry_for_language(pan_entry: dict, categories: list[str],
                             language_name: str,
                             cp_variants: list[dict]) -> dict:
    """Per-language entry: pan base + `categories` + variants filtered to this lang."""
    my_variants = [
        {
            "kind": v["kind"],
            "language_tag": v["language_tag"],
            "feature_locl_tag": v["feature_locl_tag"],
            "style": v["style"],
            "diagram": v["diagram"],
        }
        for v in cp_variants if language_name in v["used_by"]
    ]
    return {
        "character": pan_entry["character"],
        "codepoint": pan_entry["codepoint"],
        "decomposition": list(pan_entry["decomposition"]),
        "case": pan_entry["case"],
        "description": pan_entry["description"],
        "categories": categories,
        "diagram": pan_entry["diagram"],
        "variants": my_variants,
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
    data_root = resolve_data_root(LANGS_REPO)

    library_list = json.loads(LIBRARY_JSON.read_text(encoding="utf-8"))
    tags_list = json.loads(TAGS_JSON.read_text(encoding="utf-8"))
    registry = {x["name_eng"]: x for x in library_list}
    tags = {x["name_eng"]: x for x in tags_list}

    pan = load_pan_cyrillic(data_root)
    pan_by_cp = build_pan_by_cp(pan)

    in_scope = [n for n in LANGUAGES_IN_SCOPE if n not in SKIP_LANGUAGES]

    # First pass: per-language codepoint extraction. Results are reused for
    # both per-language files and the pan used_by[] reverse index.
    per_lang_codepoints: dict[str, dict[str, dict]] = {}
    for name in in_scope:
        base_path = BASE_DIR / f"{name}.json"
        if not base_path.exists():
            print(f"warning: missing base file {base_path}", file=sys.stderr)
            continue
        base = json.loads(base_path.read_text(encoding="utf-8"))
        per_lang_codepoints[name] = extract_language_codepoints(base)

    pan_used_by = reverse_index_from_per_lang(per_lang_codepoints)

    case_by_cp = {cp: rec["case"] for cp, rec in pan_by_cp.items()}
    variants_by_cp = build_variants_by_cp(data_root, in_scope, case_by_cp)

    OUT_DIR.mkdir(exist_ok=True)
    OUT_LANGS_DIR.mkdir(exist_ok=True)

    # ─── pan-cyrillic.json ────────────────────────────────────────────────
    pan_characters = []
    for cp in sorted(pan_by_cp.keys(), key=lambda x: int(x, 16)):
        used_by = pan_used_by.get(cp, [])
        if not used_by:
            continue  # codepoint present in pan but not used by any in-scope language
        pan_characters.append(char_entry_for_pan(
            pan_by_cp[cp], variants_by_cp.get(cp, []), used_by,
        ))

    pan_out = {
        "meta": {
            "description": "Pan-Cyrillic character reference across 77 languages. "
                           "Sorted by Unicode codepoint (ascending hex). "
                           "Variants nested under the base character.",
            "languages_in_scope": len(in_scope),
            "generated_by": "cyrillic-reference/tools/generate_json.py",
        },
        "characters": pan_characters,
    }
    OUT_PAN.write_text(json.dumps(pan_out, ensure_ascii=False, indent=4) + "\n",
                       encoding="utf-8")
    print(f"wrote {len(pan_characters)} characters → {OUT_PAN.relative_to(REPO)}")

    # ─── per-language files ───────────────────────────────────────────────
    written = 0
    warnings: list[str] = []
    for reg in library_list:
        if not reg.get("enable"):
            continue
        name = reg["name_eng"]
        if name in SKIP_LANGUAGES:
            continue
        if name not in per_lang_codepoints:
            continue  # missing base file already warned
        codepoints = per_lang_codepoints[name]
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
            if cp not in pan_by_cp:
                warnings.append(f"{name}: codepoint {cp} not in pan catalog")
                continue
            categories = sorted(codepoints[cp]["categories"])
            chars.append(char_entry_for_language(
                pan_by_cp[cp], categories, name,
                variants_by_cp.get(cp, []),
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
