"""Shared data access and decomposition logic for the cyrillic-reference tools.

Consumed by `generate.py` (Markdown tables), `generate_svgs.py` (SVG + plotter
sources), and `generate_json.py` (data/ JSON outputs).

Single source of truth for:
  * The 77-language scope and the two skip-list entries excluded from the
    client-facing deliverable.
  * The Paratype-aware NFD: `… WITH <mark>` parsing, the BREVE swap to
    Cyrillic-shaped U+F6D1 / U+F6D4, and the structural-composite set that
    has no combining-mark equivalent.
  * Token classification for `&` / `+` marker semantics and style suffixes.
  * Per-language codepoint extraction from the raw `library/base/` JSONs.
  * Pan-Cyrillic catalog built on top of the compile_languages.py summary
    (`site/cyrillic/cyrillic_characters_lib.json`).

Python 3.8+ stdlib only.
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path


# ─── constants ─────────────────────────────────────────────────────────────

# Unicode Private Use Area range (BMP). PT Expert fonts encode glyphs without
# an official Unicode assignment here; callers treat these rows specially for
# display but not for decomposition logic.
PUA_RANGE = (0xE000, 0xF8FF)
PUA_TOKEN = re.compile(r"^!([0-9A-Fa-f]{4,5})$")

# The Paratype Expert fonts carry a distinct Cyrillic-shaped breve separate
# from the generic combining breve U+0306. Decomposition substitutes the
# case-specific glyph for U+0306 wherever a BREVE appears.
_CYRILLIC_BREVE = object()
CYRILLIC_BREVE_UC = 0xF6D1
CYRILLIC_BREVE_LC = 0xF6D4

# The ten decomposable accent names found in Unicode and PUA descriptions.
# Every other `… WITH <accent>` is a structural composite — no combining-mark
# equivalent exists, so the row keeps its original codepoint and empty
# decomposition.
ACCENT_COMBINING_MARK = {
    "MACRON":       0x0304,
    "DIAERESIS":    0x0308,
    "BREVE":        _CYRILLIC_BREVE,
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

# The same codepoints that ACCENT_COMBINING_MARK maps to — used by the NFD
# fallback path to recognise canonical decompositions whose Unicode name
# does not spell out the accent (Ё, Й, Ў, Ѓ, Ї, Ќ, and their lowercase).
_KNOWN_COMBINING_MARK_CPS = {
    0x0304, 0x0308, 0x0306, 0x0301, 0x0302,
    0x0300, 0x030C, 0x030B, 0x0327, 0x0307,
}

# The 77 Cyrillic-based languages in scope. Values are JSON filename stems
# under `<data>/library/cyrillic/base/`.
LANGUAGES_IN_SCOPE = [
    "Abazin", "Abkhazian", "Adyge", "Aghul", "Altaic (Oirot)", "Avar",
    "Azeri", "Bashkir", "Belarusian", "Bulgarian", "Buryat", "Chechen",
    "Chukchi", "Chuvash", "Dargwa", "Dolgan", "Dungan", "Enets",
    "Eskimo (Yupik)", "Even (Lamut)", "Evenki (Tungus)", "Gagauz",
    "Ingush", "Itelmen", "Kabardian", "Kabardino-Cirkassian", "Kalmyk",
    "Karachay-Balkar", "Karakalpak", "Kazakh", "Khakass", "Khanty",
    "Kirghiz", "Komi-Permyak", "Komi-Zyrian", "Koryak", "Kryashen Tatar",
    "Kumyk", "Kurdish", "Lak", "Lezgin", "Macedonian", "Manci",
    "Mari-high", "Mari-low", "Moldavian", "Mongolian", "Mordvin-Erzya",
    "Mordvin-Moksha", "Nanai", "Negidal", "Nenets (Yurak)", "Nganasan",
    "Nivkh", "Nogai", "Ossetic", "Russian", "Rutul", "Saami Kildin",
    "Selkup", "Serbian", "Shor", "Tabasaran", "Tadzhik", "Talysh", "Tat",
    "Tatar", "Tofalar", "Touva (Soyot)", "Tsakhur", "Turkmen", "Udmurt",
    "Uighur", "Ukrainian", "Ulch", "Yakut", "Yukagir",
]

# Listed in the source registry but excluded from the client-facing JSON
# deliverable. Still in scope for internal tooling — generate.py produces MD
# rows for their codepoints where they share with an in-scope language.
SKIP_LANGUAGES = {"Kaitag", "Uzbek"}

# The four OT locale tags that PT Expert exposes via suffixed glyph names
# (`uni<cp>.<tag>`). Ru is the default and has no locl variants.
LOCL_FEATURE = {
    "bg": "BGR ",
    "sr": "SRB ",
    "ba": "BSH ",
    "cv": "CHU ",
}

# Variants whose `.<SUFFIX>` glyph is not present in PT Serif Expert Regular
# and therefore cannot be rendered. Suppressed from generated outputs to
# avoid broken-image rows; tracked in TODO.md for the type-design team.
_FONT_GAPS_SUPPRESSED = {
    ("0416", "bg"),  # Ж — no uni0416.BGR
    ("041A", "bg"),  # К — no uni041A.BGR
}


# ─── path resolution ───────────────────────────────────────────────────────

def resolve_data_root(data_arg: Path) -> Path:
    """Return the directory that directly contains `library/cyrillic/base/`.

    Accepts either the data subfolder or the parent repo that holds it one
    level down — lets the tools run whether invoked from a sibling clone or
    the combined source tree.
    """
    if (data_arg / "library" / "cyrillic" / "base").is_dir():
        return data_arg
    nested = data_arg / "cyrillic-languages"
    if (nested / "library" / "cyrillic" / "base").is_dir():
        return nested
    raise FileNotFoundError(
        f"Could not find library/cyrillic/base/ under {data_arg} "
        f"or {nested}. Pass --data pointing at the cloned "
        f"cyrillic-languages repository."
    )


# ─── PUA / decomposition helpers ───────────────────────────────────────────

def is_pua(codepoint: int) -> bool:
    return PUA_RANGE[0] <= codepoint <= PUA_RANGE[1]


def _swap_breve(cp: int, case: str) -> int:
    """Generic combining breve U+0306 → case-specific Cyrillic breve glyph."""
    if cp == 0x0306:
        if case == "upper":
            return CYRILLIC_BREVE_UC
        if case == "lower":
            return CYRILLIC_BREVE_LC
        raise ValueError(f"_swap_breve: unknown case {case!r}")
    return cp


def has_decomposition_hint(description: str) -> bool:
    """True for descriptions containing `WITH` — decomposable or structural."""
    return " with " in f" {description.lower()} "


def decompose(description: str, case: str, sign: str = "") -> list[int] | None:
    """Break a composed Cyrillic codepoint into base + combining marks.

    Tries two paths in order:

    1. **Description-based.** If `description` contains `… WITH <accent>
       [AND <accent>]`, parse out the base name and the accent tokens.
       Every Paratype composite that spells out its accents lands here
       (Ӑ, F50E, …).
    2. **NFD fallback.** Description has no `WITH` but the character itself
       has a canonical Unicode decomposition into a base plus combining
       marks from our known set. Picks up the ~12 precomposed letters
       whose Unicode name only carries a language label (Ё, Й, Ў, Ѓ, Ї,
       Ќ and their lowercase forms).

    Returns codepoint list (base first) or None when neither path applies
    (structural `WITH DESCENDER / HOOK / …`, plain letters with no
    composition, …).

    `case` must be `"upper"` or `"lower"` — selects U+F6D1 or U+F6D4 for
    any BREVE token.
    """
    # Path 1: ... WITH <accent>
    parts = _WITH_RE.split(description, maxsplit=1)
    if len(parts) == 2:
        base_name, phrase = parts
        tokens = [t.strip().upper() for t in _AND_RE.split(phrase)]
        mapped: list[int] = []
        for token in tokens:
            mark = ACCENT_COMBINING_MARK.get(token)
            if mark is None:
                return None
            if mark is _CYRILLIC_BREVE:
                mapped.append(_swap_breve(0x0306, case))
            else:
                mapped.append(mark)
        try:
            base_char = unicodedata.lookup(base_name.strip().upper())
        except KeyError:
            raise ValueError(
                f"decompose: cannot resolve base letter {base_name!r} "
                f"from description {description!r}"
            )
        return [ord(base_char), *mapped]

    # Path 2: NFD fallback for precomposed characters whose description
    # does not spell out the accent.
    if sign:
        nfd = unicodedata.normalize("NFD", sign)
        if len(nfd) > 1:
            cps = [ord(c) for c in nfd]
            if all(cp in _KNOWN_COMBINING_MARK_CPS for cp in cps[1:]):
                return [cps[0], *(_swap_breve(cp, case) for cp in cps[1:])]

    return None


# ─── pan-Cyrillic data from site/ ──────────────────────────────────────────

def load_pan_cyrillic(data_root: Path) -> dict:
    """Load the aggregated pan-Cyrillic character set produced by
    compile_languages.py.

    `uppercase_unicodes_list` and `lowercase_unicodes_list` carry one entry
    per (codepoint × local) with sign, description, and the languages that
    use it. The `*_sorted_by_unicodes` variants carry the same rows sorted
    by codepoint so PUA naturally groups at the end of each table.
    """
    path = data_root / "site" / "cyrillic" / "cyrillic_characters_lib.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def dedupe_by_codepoints(entries: list[dict]) -> list[dict]:
    """Merge entries that share the same codepoint sequence.

    The pan-Cyrillic set intentionally emits duplicate rows for localized
    forms (`&` marker → `local='bg'` etc.) and style variants — these share
    a codepoint but render differently via `locl` or stylistic features.
    For the codepoint-level view we keep one row per sequence, union the
    language lists, and record which locales request a localized form in
    `locales`.
    """
    by_key: dict[tuple[str, ...], dict] = {}
    for entry in entries:
        key = tuple(u.upper() for u in entry.get("unicodes", []))
        if key not in by_key:
            merged = dict(entry)
            merged["unicodes"] = list(key)
            merged["languages"] = list(entry.get("languages", []))
            merged["locales"] = {entry.get("local")} if entry.get("local") else set()
            by_key[key] = merged
        else:
            merged = by_key[key]
            merged["languages"].extend(entry.get("languages", []))
            if entry.get("local"):
                merged["locales"].add(entry.get("local"))
    for merged in by_key.values():
        merged["locales"] = sorted(merged["locales"])
    return list(by_key.values())


# ─── per-language codepoint extraction from library/base/ ──────────────────

_ESCAPE_RE = re.compile(r"^!([0-9A-Fa-f]{4,6})$")


def token_to_codepoint(tok: str) -> str | None:
    """Resolve a glyphs_list token (already stripped of leading +/&/: markers)
    to a single-codepoint hex string, or None if it's a digraph / unparseable.

    Accepts:
      - single Unicode character         → ord → 4-hex
      - escape form "!FXXX" / "!FXXXX"
      - style-qualified single char      "г.ita" / "Д.str"
    Rejects multi-char tokens without a known style suffix (digraphs).
    """
    if not tok:
        return None
    m = _ESCAPE_RE.match(tok)
    if m:
        return m.group(1).upper().zfill(4)
    base = tok
    if "." in tok:
        head, sep, suffix = tok.partition(".")
        if suffix in ("ita", "str"):
            base = head
        else:
            return None
    if len(base) == 1:
        return f"{ord(base):04X}"
    return None


def extract_language_codepoints(base: dict) -> dict[str, dict]:
    """Per-language codepoint set + block categories.

    Walks `glyphs_list` tokens, applying marker filtering:

      - `:` prefix (digraph marker) — skip.
      - Multi-character tokens without a known style suffix — skip
        (Гь / Ӷә / Ҭә and similar digraphs without explicit `:`).
      - `!FXXX` escape — resolve to PUA codepoint.
      - `+` / `&` markers contribute the codepoint to the set and
        accumulate the block type under `categories`.

    Returns `{codepoint_hex: {"case": "uppercase"|"lowercase", "categories":
    set[str]}}`. `case` is the field of first appearance; `categories`
    accumulates across blocks.
    """
    out: dict[str, dict] = {}
    for block in base.get("glyphs_list", []):
        block_type = block.get("type", "alphabet")
        for field, case_name in [("uppercase", "uppercase"), ("lowercase", "lowercase")]:
            s = block.get(field, "") or ""
            for tok in s.split():
                if not tok:
                    continue
                if tok[0] == ":":
                    continue
                rest = tok[1:] if tok[0] in "+&" else tok
                cp = token_to_codepoint(rest)
                if cp is None:
                    continue
                entry = out.setdefault(cp, {"case": case_name, "categories": set()})
                entry["categories"].add(block_type)
    return out


# ─── variants (`&` / `+` markers) ──────────────────────────────────────────

def classify_variant_token(token: str) -> dict | None:
    """Decode a source token that carries a variant marker.

    Returns `{marker, style, glyph_text, codepoints}` for `&`-localized and
    `+`-alternate tokens; None for plain tokens (they belong in the main
    character table, not the variants table).
    """
    if not token:
        return None
    rest = token
    if rest[0] == "&":
        marker = "localized"
        rest = rest[1:]
    elif rest[0] == "+":
        marker = "alternate"
        rest = rest[1:]
    else:
        return None
    style = "any"
    for suffix, label in ((".ita", "italic"), (".str", "straight"), (".alt", "alt")):
        if rest.endswith(suffix):
            style = label
            rest = rest[: -len(suffix)]
            break
    if not rest:
        return None
    pua_match = PUA_TOKEN.match(rest)
    if pua_match:
        codepoints = [f"{int(pua_match.group(1), 16):04X}"]
    else:
        codepoints = [f"{ord(c):04X}" for c in rest]
    return {
        "marker": marker,
        "style": style,
        "glyph_text": rest,
        "codepoints": codepoints,
    }


def collect_glyph_variants(data_root: Path, languages: list[str]) -> list[dict]:
    """Scan in-scope base JSONs and collect every variant-marker token.

    Emits one entry per (codepoints, case, locale, style, marker, language)
    tuple. `aggregate_variants` later merges rows sharing everything except
    `language`.

    `+`-marker rows are dropped — they pair with `&` rows and carry the
    default (pre-locl) shape; the paired row's diagram cell already
    renders both shapes side-by-side. Side effect: ru-default rows also
    disappear (ru sources only emit `+`, never `&`).

    Rows in `_FONT_GAPS_SUPPRESSED` are dropped — the variant glyph is
    missing from the font, so the row cannot be rendered.
    """
    variants: list[dict] = []
    base_dir = data_root / "library" / "cyrillic" / "base"
    for lang_name in languages:
        path = base_dir / f"{lang_name}.json"
        if not path.exists():
            continue
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        locale = data.get("local", "")
        for block in data.get("glyphs_list", []):
            block_type = block.get("type", "")
            for side in ("uppercase", "lowercase"):
                for token in (block.get(side, "") or "").split():
                    info = classify_variant_token(token)
                    if info is None:
                        continue
                    if info["marker"] == "alternate":
                        continue
                    if info.get("codepoints") and (info["codepoints"][0], locale) in _FONT_GAPS_SUPPRESSED:
                        continue
                    variants.append({
                        **info,
                        "token": token,
                        "case": side,
                        "locale": locale,
                        "language": lang_name,
                        "block_type": block_type,
                    })
    return variants


def aggregate_variants(variants: list[dict]) -> list[dict]:
    """Merge variant rows sharing (codepoints, case, locale, style, marker).

    Different languages sometimes encode the same localized form; those
    fold into a single row with a merged `languages` list.
    """
    groups: dict[tuple, dict] = {}
    for v in variants:
        key = (
            tuple(v["codepoints"]), v["case"], v["locale"],
            v["style"], v["marker"],
        )
        if key not in groups:
            groups[key] = {
                "codepoints": v["codepoints"],
                "case": v["case"],
                "locale": v["locale"],
                "style": v["style"],
                "marker": v["marker"],
                "glyph_text": v["glyph_text"],
                "tokens": {v["token"]},
                "languages": {v["language"]},
            }
        else:
            groups[key]["tokens"].add(v["token"])
            groups[key]["languages"].add(v["language"])
    rows = []
    for g in groups.values():
        rows.append({
            **g,
            "tokens": sorted(g["tokens"]),
            "languages": sorted(g["languages"]),
        })
    rows.sort(key=lambda r: (
        [int(cp, 16) for cp in r["codepoints"]],
        r["case"],
        r["locale"],
        r["style"],
        r["marker"],
    ))
    return rows
