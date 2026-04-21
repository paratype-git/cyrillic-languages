#!/usr/bin/env python3
"""Dump the 79 in-scope Cyrillic languages with their identifier fields.

Combines three source files into a single machine-readable JSON + a
human-readable Markdown table:

  cyrillic-languages/library/cyrillic/cyrillic_library.json
      name_eng, name_rus, code_pt, enable

  cyrillic-languages/library/cyrillic/base/<Language>.json
      local  — the OT `locl` tag used as the source language's default
               layout (ru for most, bg / sr / ba / cv for the four
               non-Russian-default alphabets)

Fields we do NOT yet know for all 79 languages are written as the
literal string ``"TBD"`` so downstream maintainers can fill them in:

  iso639_1   — ISO 639-1 two-letter code (e.g. "ru")
  iso639_3   — ISO 639-3 three-letter code (e.g. "rus")
  bcp47      — full BCP 47 tag the site might want to expose
  ot_lang    — OpenType language-system tag (4-letter, uppercase;
               e.g. "RUS", "BGR", "SRB")

Run from cyrillic-reference/:

    python3 tools/generate_language_tags.py --data ../cyrillic-languages
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


KNOWN_FIELDS_TODO = ("iso639_1", "iso639_3", "bcp47", "ot_lang")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data", type=Path, default=Path("../cyrillic-languages"),
                        help="Path to the sibling cyrillic-languages repository")
    parser.add_argument("--out-json", type=Path, default=Path("language-tags.json"))
    parser.add_argument("--out-md", type=Path, default=Path("language-tags.md"))
    args = parser.parse_args(argv)

    library = args.data / "library" / "cyrillic" / "cyrillic_library.json"
    base_dir = args.data / "library" / "cyrillic" / "base"
    if not library.exists():
        parser.error(f"library not found: {library}")
    langs = json.loads(library.read_text(encoding="utf-8"))

    rows: list[dict] = []
    for entry in langs:
        name_eng = entry["name_eng"]
        row = {
            "name_eng": name_eng,
            "name_rus": entry.get("name_rus", ""),
            "code_pt": entry.get("code_pt", ""),
            "enable": bool(entry.get("enable", False)),
            "local": "",
        }
        lang_json = base_dir / f"{name_eng}.json"
        if lang_json.exists():
            with lang_json.open(encoding="utf-8") as f:
                try:
                    row["local"] = json.load(f).get("local", "")
                except json.JSONDecodeError:
                    pass
        for field in KNOWN_FIELDS_TODO:
            row[field] = "TBD"
        rows.append(row)

    args.out_json.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Markdown view
    md: list[str] = []
    md.append("# Cyrillic languages — language-tag table")
    md.append("")
    md.append(
        f"All {len(rows)} languages declared in "
        f"`cyrillic-languages/library/cyrillic/cyrillic_library.json`, "
        f"with the identifier fields we know today and placeholders for the "
        f"external tag systems we have not yet filled in. Re-generated from "
        f"[`tools/generate_language_tags.py`](tools/generate_language_tags.py)."
    )
    md.append("")
    md.append("**Columns:**")
    md.append("")
    md.append("- **name_eng / name_rus** — from `cyrillic_library.json`.")
    md.append("- **code_pt** — Paratype's internal per-language identifier.")
    md.append("- **enable** — whether the language is currently compiled by the pipeline.")
    md.append("- **local** — OT `locl` tag used as the source file's default "
              "(blank = inherits script default, which is `ru` for this library).")
    md.append("- **iso639_1 / iso639_3 / bcp47 / ot_lang** — external tag systems. "
              "`TBD` placeholders mean this row still needs a human-verified value; "
              "many of these languages have obscure ISO codes or none at all.")
    md.append("")
    md.append("| # | name_eng | name_rus | code_pt | enable | local | iso639_1 | iso639_3 | bcp47 | ot_lang |")
    md.append("| ---: | --- | --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    for i, r in enumerate(rows, start=1):
        md.append(
            f"| {i} | {r['name_eng']} | {r['name_rus']} | {r['code_pt']} | "
            f"{'yes' if r['enable'] else 'no'} | {r['local'] or '—'} | "
            f"{r['iso639_1']} | {r['iso639_3']} | {r['bcp47']} | {r['ot_lang']} |"
        )
    md.append("")
    args.out_md.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"Wrote {args.out_json} ({len(rows)} entries)")
    print(f"Wrote {args.out_md} ({len(rows)} entries)")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
