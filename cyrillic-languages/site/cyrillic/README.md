# Cyrillic site data — schema reference

This folder is the **machine-readable output** of the Paratype Cyrillic languages pipeline. The files here are generated — they are the exact artifacts that the public site at <https://paratype.github.io/cyrillic-languages/> loads to render its pages. They are also intended to be reusable by third-party projects (linguistic tooling, font-coverage checkers, Cyrillic reference material, etc.).

If you want to edit the data, do not edit files here — edit the source JSONs under `../../library/cyrillic/base/` and run the pipeline. See the repository's top-level [`README.md`](../../../README.md), [`CONTRIBUTING.md`](../../../CONTRIBUTING.md) and [`docs/MAINTAINING.md`](../../../docs/MAINTAINING.md). If you are a consumer of this data, read on.

## License and reuse

The data is released under the **MIT License** (see [`LICENSE`](../../../LICENSE) at the repository root). You may use it in open- or closed-source projects; attribution is welcome (“Paratype Cyrillic languages knowledge base”) but not required by the license.

The fonts referenced by some codepoints (PT Sans Expert, PT Serif Expert) are **not** part of this repository and are licensed separately under the SIL Open Font License.

## Stability

The schema described below is **de-facto stable** — it has not changed in the current generation of the pipeline, and the site depends on these exact field names. However, it is **not versioned**. There is no `schema_version` field and no deprecation policy. If you need reproducibility for a downstream project, **pin a specific commit of this repository** rather than tracking `master`. Breaking changes, if they happen, will be called out in commit messages but not in a machine-readable form.

Two output shapes you can rely on for now:

- every per-language file under `base/` has a root `name_eng` (string), `language_tag` (BCP 47 string), and `glyphs_list` (array);
- `cyrillic_characters_lib.json` has eight top-level list keys listed further down.

## Layout

```
site/cyrillic/
├── README.md                           (this file)
├── base/
│   └── <LanguageName>.json             one per language, 82 files
└── cyrillic_characters_lib.json        pan-Cyrillic aggregated summary
```

The per-language file name matches the English name used in `languages.json`. Names can contain spaces and parentheses — e.g. `Altaic (Oirot).json`, `Eskimo (Yupik).json` — so quote them when passing through a shell.

Three of the files under `base/` are **legacy-schema** and do not follow the schema below: `Russian Ancient (XVIII).json`, `Russian Church (X-XVII).json`, `Russian Old (XIX).json`. They have an empty `glyphs_list` and keep a pre-pipeline shape with top-level `uppercase_alphabet`, `lowercase_alphabet`, `uppercase_historic`, `lowercase_historic`, `uppercase_dialect`, `lowercase_dialect`, `uppercase_lexic`, `lowercase_lexic`, `uppercase_unicodes_list`, `lowercase_unicodes_list`. Most consumers should simply skip them.

## Per-language file

```jsonc
{
  "name_eng": "Russian",
  "language_tag": "ru",            // BCP 47 tag (since 2026-04)
  "glyphs_list": [
    { /* block */ },
    { /* block */ },
    …
    { "type": "charset", … }       // always last, if present
  ]
}
```

### Block

```jsonc
{
  "type": "alphabet",              // see table below
  "title": "Alphabet",             // locked string, determined by type
  "show_unicodes": false,          // true only for "charset" blocks
  "uppercase": [ /* glyphs */ ],
  "lowercase": [ /* glyphs */ ]
}
```

Block types observed in the current output:

| `type`          | `title`                           | Purpose                                                                                                   |
| --------------- | --------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `alphabet`      | `Alphabet`                        | The language's current alphabet.                                                                          |
| `extended`      | `Extended Orphographic Notation`  | Additional orthographic marks/letters used in this language (spelling preserved from source config).      |
| `historic`      | `Historical glyph forms`          | Letters used in older orthographies.                                                                      |
| `dialect`       | `Dialect glyph forms`             | Letters specific to regional dialects.                                                                    |
| `consideration` | `Signs under consideration`       | Candidate letters not yet firmly in the alphabet.                                                         |
| `charset`       | `Character Set`                   | A flat, per-codepoint view of everything above, with human-readable Unicode names. Every language has one. |

Two further types (`digraph`, `foreign`) are declared in `glyphs_list_categories.json` but no language currently emits them — safe to ignore unless you see them.

A given language always has an `alphabet` block and a `charset` block. The other four block types are optional and vary by language.

### Glyph in a source block (`alphabet` / `extended` / `historic` / `dialect` / `consideration`)

```jsonc
{
  "sign": "Гъ",                    // the glyph(s), may be multi-codepoint
  "unicodes": ["0413", "044A"],    // array of hex codepoints, one per character
  "local": "ru",                   // locl language tag — see below
  "types": ["alphabet"],           // see table below; may be null in edge cases
  "description": "0413, 044A",     // mostly just the codepoints (see note)
  "alts": [ /* 0..N nested glyph entries */ ]
}
```

- `sign` may be a **digraph or sequence** (e.g. `"Гъ"`, `"Джв"`) in which case `unicodes` has the codepoints in reading order.
- `sign` may be **empty** (`""`) when the entry is a glyph that only exists in the Paratype Expert fonts — the codepoint lives in the Unicode Private Use Area (see [PUA](#unicode-private-use-area) below) and will render as “□” (tofu) in any other font.
- `description` in source blocks is usually the hex list (`"0413, 044A"`); for localized-form entries it reads `"<HEX> Localized form of <BASE>"`.
- `alts` carries alternates, equivalents, digraphs, and replacement signs associated with the parent letter. Each alt has the same shape as a glyph entry, minus nested `alts` (always `[]`).
- `types` is **usually** a single-element array mirroring the block type. It may also contain compositional tags — see the next table. In two rare cases in the current dataset it is `null`; treat that as equivalent to `[]`.

### Glyph in the `charset` block

```jsonc
{
  "sign": "А",
  "unicodes": ["0410"],                      // always a single codepoint here
  "local": "ru",
  "display_unicode": "0410",                 // hex codepoint to display under the glyph
  "types": ["alphabet"],
  "description": "Cyrillic Capital Letter A" // human-readable Unicode name
}
```

Differences from source-block glyphs:

- **no `alts`** — the charset is flat;
- **`display_unicode`** is added (may be empty for localized forms without a standalone display codepoint);
- **`description`** is the human-readable Unicode character name (resolved from `unicode14.txt` and `PT_PUA_unicodes-descriptions.txt`), not the hex.

### `types` vocabulary (glyph-level)

Values you may see in the `types` array of any glyph entry:

| `types` value     | Meaning                                                                                     |
| ----------------- | ------------------------------------------------------------------------------------------- |
| `alphabet`        | Part of the alphabet.                                                                       |
| `extended`        | Extended orthographic notation.                                                             |
| `historic`        | Historical letter.                                                                          |
| `dialect`         | Dialect letter.                                                                             |
| `consideration`   | Candidate letter.                                                                           |
| `localform`       | A localized form (opentype `locl` variant) of another letter.                                |
| `alternatesign`   | An alternate glyph offered alongside the main one.                                          |
| `replacementsign` | A non-localized replacement for a localized-form letter (shown in `alts`).                   |
| `italic`          | Glyph only exists in italic style; pair it with `hide: "straight"` in the summary.           |
| `straight`        | Glyph only exists in upright/roman style; pair it with `hide: "italic"` in the summary.      |

Exactly one of the first five (`alphabet` / `extended` / `historic` / `dialect` / `consideration`) matches the enclosing block's `type`. The remaining values can co-occur with it.

### `local` — OpenType `locl` tags

Identifies which language's `locl` form of a glyph this entry represents. Values seen in Cyrillic data: `ru` (default), `bg` (Bulgarian), `sr` (Serbian), `ba` (Bashkir), `cv` (Chuvash). A string like `"ba"` means “this entry is the Bashkir-localized shape of the codepoint.”

## Pan-Cyrillic summary — `cyrillic_characters_lib.json`

This is a single file that aggregates the `charset` blocks of every enabled language into a pan-Cyrillic view, grouped and sorted. It is the best single source if you need “all Cyrillic codepoints used across these 79 languages, with per-codepoint language coverage.”

### Top-level keys

| Key                              | Contents                                                                               |
| -------------------------------- | -------------------------------------------------------------------------------------- |
| `uppercase_unicodes_list`        | Every uppercase entry, sorted by `sortorder_cyrillic.txt`.                              |
| `lowercase_unicodes_list`        | Every lowercase entry, sorted by `sortorder_cyrillic.txt`.                              |
| `uppercase_sorted_by_unicodes`   | The same uppercase entries, sorted by codepoint.                                       |
| `lowercase_sorted_by_unicodes`   | The same lowercase entries, sorted by codepoint.                                       |
| `uppercase_puazone_list`         | **Currently always `[]`** (reserved — PUA entries are merged into the main list).       |
| `lowercase_puazone_list`         | Same, for lowercase.                                                                   |
| `uppercase_nonunicode_list`      | **Currently always `[]`** (reserved — localized-only entries are merged into the main list). |
| `lowercase_nonunicode_list`      | Same, for lowercase.                                                                   |

The four “reserved” keys exist so that the site engine can parse the file with fixed expectations; they may be populated by a future pipeline change or stay empty.

### Entry shape

```jsonc
{
  "sign": "А",
  "unicodes": ["0410"],
  "local": "ru",
  "display_unicode": "0410",
  "description": "Cyrillic Capital Letter A",
  "hide": "",                                // "", "italic", or "straight"
  "languages": [
    { "name": "Abazin",      "types": ["alphabet"], "language_tag": "abq" },
    { "name": "Abkhazian",   "types": ["alphabet"], "language_tag": "ab" },
    …
    { "name": "All",         "types": ["alphabet"], "language_tag": null }  // only if every language uses it
  ],
  "id": "idWAA6PTVA"
}
```

- `hide` is a rendering hint: `"straight"` means “this glyph has an italic-only form; hide it when rendering in upright style,” and vice versa. Empty string means no restriction.
- `languages` lists every language whose charset contains this codepoint, plus each language's BCP 47 `language_tag`. If all enabled languages contain it, an extra `{"name": "All"}` sentinel is appended.
- **`id` is regenerated on every build** (random 8-char suffix after `id`). Do not use it as a stable key across regenerations — use `(unicodes, local)` instead. It is intended for DOM keys in the site's React bundle.

## Unicode Private Use Area

Some codepoints in this data sit in the Unicode **Private Use Area** (`U+E000`–`U+F8FF`). The PUA is a range the Unicode Consortium leaves unassigned for private interchange — **nobody owns specific codepoints in it**. The Paratype Expert fonts (PT Sans Expert, PT Serif Expert) historically use part of this range to encode glyphs that lack an official Unicode assignment (e.g. certain stressed-vowel combinations).

When you see a `!FXXX` escape in the source data or an entry whose `unicodes` starts with `F`, that means “the glyph at this codepoint **in the Paratype Expert fonts**.” The same codepoint in another foundry's font will almost certainly map to a different glyph or to nothing at all. If you plan to render these characters, you either need the Paratype Expert fonts or a font that specifically declares compatible PUA mappings.

The descriptive names for these PUA codepoints come from `PT_PUA_unicodes-descriptions.txt` in this repository.

## Working with the data — Python example

Python 3 stdlib is enough; there are no dependencies.

```python
import json
from pathlib import Path

site = Path("cyrillic-languages/site/cyrillic")

# Load one language.
russian = json.loads((site / "base" / "Russian.json").read_text(encoding="utf-8"))
alphabet = next(b for b in russian["glyphs_list"] if b["type"] == "alphabet")
print([g["sign"] for g in alphabet["uppercase"]])
#  ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', ...]

# Load the pan-Cyrillic summary and find which languages use "Ғ" (U+0492).
summary = json.loads((site / "cyrillic_characters_lib.json").read_text(encoding="utf-8"))
ghe_stroke = next(e for e in summary["uppercase_unicodes_list"] if e["unicodes"] == ["0492"])
print([lang["name"] for lang in ghe_stroke["languages"]])
#  ['Bashkir', 'Karachay-Balkar', 'Kazakh', ...]
```

Common use cases this dataset supports:

- **Font coverage checks** — given a set of language names, aggregate the union of their codepoints from the per-language `charset` blocks (or read it straight from the summary).
- **Reverse lookup** — given a codepoint, find which languages need it via `cyrillic_characters_lib.json.<*>_unicodes_list[*].languages`.
- **Pan-Cyrillic sort order** — `*_unicodes_list` keys are pre-sorted in Paratype's language-aware order (not by codepoint); `*_sorted_by_unicodes` keys are sorted by codepoint.
- **Digraph awareness** — in per-language files, look for glyph entries with `len(unicodes) > 1` or `type: "alphabet"` entries whose `sign` has more than one character.

## Example consumer

The [`cyrillic-reference/`](../../../cyrillic-reference/) subproject in this same repository consumes this data to generate a pan-Cyrillic Markdown character table, a glyph-variants catalog, and (in progress) SVG illustrations. Its `generate.py` is a practical reading of both `base/*.json` and `cyrillic_characters_lib.json`, and a reasonable starting point if you are writing your own consumer.

## Questions and corrections

Questions about the schema, reuse, or integration: **info@paratype.net**, or open an issue on this repository.

Data errors (a missing letter, a wrong alphabet) should go through [`CONTRIBUTING.md`](../../../CONTRIBUTING.md) — they are fixed by editing the source files under `library/cyrillic/base/`, not by editing the generated files here.
