# Cyrillic Reference — status and next steps

Working notes for the next session / next agent picking this up.

## Where we are (2026-04-20)

This subproject lives as a subdirectory of `paratype-git/cyrillic-languages` — a monorepo decision made after the "separate repo" plan was reconsidered. The whole repository is MIT-licensed (see `/LICENSE` at repo root); `cyrillic-reference/LICENSE` is kept for clarity of this subtree. Scope is **pan-Cyrillic single characters across 77 languages**, not per-language alphabets with digraphs — decision made mid-session after the first per-language pass was thrown away.

Files present:
- `LICENSE` — MIT, Paratype, 2026
- `README.md` — project framing, repo map, regeneration instructions, PUA explanation, license matrix
- `generate.py` — Python 3 stdlib only; reads the sibling `cyrillic-languages` repo and writes the tables below
- `characters-uppercase.md` — **177** unique uppercase codepoints (deduped from 181; `&`/style duplicates collapsed into a `Locales` column). 54 PUA, 105 composed (`… WITH …`)
- `characters-lowercase.md` — **176** unique lowercase codepoints (deduped from 205). 54 PUA, 105 composed
- `glyph-variants.md` — **128** variant forms that share a codepoint with a base letter but render differently under `locl` or `.str`/`.ita` stylistic alternates. Locales: ba, bg, cv, ru, sr

Regeneration:
```bash
cd cyrillic-reference/
python3 generate.py
```

## Still to do

### 1. Decompose "… WITH …" composed descriptions into base + combining marks

105 uppercase + 105 lowercase entries currently flagged `Composed: yes`. For each, emit a `XXXX + XXXX (+ XXXX)` decomposition column alongside the single codepoint.

- **Standard Unicode composed chars (e.g. Ӑ U+04D0 "With Breve"):** start with `unicodedata.normalize('NFD', char)` — this handles the Unicode-canonical decompositions automatically.
- **PUA composed chars (e.g. F50E "Cyrillic Capital Letter A With Macron"):** NFD returns them unchanged. Need a dictionary `{"MACRON": 0x0304, "BREVE": 0x0306, "DIAERESIS": 0x0308, "CARON": 0x030C, "ACUTE": 0x0301, "GRAVE": 0x0300, "CIRCUMFLEX": 0x0302, "DOT ABOVE": 0x0307, …}` plus a parser for the description (split on " WITH ", then on " AND " for multi-accent cases like "DIAERESIS AND BREVE"). Base letter found by Unicode name lookup (`unicodedata.lookup("CYRILLIC CAPITAL LETTER A")` → А).
- **Non-decomposable cases (e.g. "With Descender", "With Hook", "With Tail"):** no standard combining mark exists. These fall under contract §4.10 — emit a "unicode plus transformation" descriptive form (e.g. `Cyrillic Capital Letter Ghe + descender`) in a separate list. Approximate count from a 20-case spot check: ~30–40 such cases across the 210 composed entries.

### 2. Legacy PUA mapping column (§4.9)

For the PUA rows whose NFD or descriptive decomposition can be represented as a standard Unicode sequence, the main table should show the sequence AND keep the old PUA codepoint in a `Legacy PUA` column. This is explicit in the spec.

### 3. SVG illustrations via `glyphplotter` (§4.2)

Sample code is in §4.13 of the spec. Required assets on disk:
- `ptsansexpert/PTS55E.ttf` — already in `cyrillic-languages/fonts/` (gitignored there)
- `Noto-2019/NotoSerifBalinese-Regular.ttf` — download from Google Fonts (OFL). Only used for U+25CC dotted-circle carrier when rendering combining marks in isolation.

`generate.py` needs a function that takes a single character (or decomposed sequence) and emits a glyphplotter input file describing one diagram per letter. Diagram shape: `<char-box> { + <char-box> } --> <final-glyph>`. Then invoke the glyphplotter binary to rasterize to SVG.

The `glyphplotter` tool lives at <https://bitbucket.org/LindenbergSW/fontdoctools/src/master/> — MIT-compatible. Clone adjacent to this repo.

For the 128 variant forms in `glyph-variants.md`, SVGs need to activate the matching OpenType feature (`locl` with the right language tag, or the right stylistic set). That's a glyphplotter config question — worth a small experiment before committing to a design.

### 4. Publish

No separate repo needed — this tree is already part of `paratype-git/cyrillic-languages`. When stages 1–3 produce usable output, commit the generated tables alongside the generator. The deliverable URL becomes `https://github.com/paratype-git/cyrillic-languages/tree/master/cyrillic-reference`.

## Non-negotiables carried over from the engagement

- **No mention of the contracting party anywhere** — not in READMEs, code, commit messages, PR bodies, issue templates, script names, CI config, or file names. See `.claude/.../memory/feedback_no_apple_mentions.md` in the source data repo.
- **MIT license on every outbound artifact.**
- **77-language scope** (the list is in `generate.py` as `LANGUAGES_IN_SCOPE`). Not 79 — `Kaitag` and `Uzbek` are in our data but out of scope here.
- **PUA is a shared Unicode range** used by Paratype Expert fonts, not proprietary. See `.claude/.../memory/pua_terminology.md`.

## Useful references in the source data repo

- `cyrillic-languages/PT_PUA_unicodes-descriptions.txt` — `FXXX  CYRILLIC …` mappings for every PUA codepoint used by PT Expert fonts. This is the canonical list for stage 1 (decomposition) and §4.10 descriptive forms.
- `cyrillic-languages/site/cyrillic/cyrillic_characters_lib.json` — aggregated pan-Cyrillic set that `generate.py` reads from.
- `cyrillic-languages/library/cyrillic/base/*.json` — 79 source language files; 77 are in scope.
- `cyrillic-languages/library/cyrillic/_legacy/Russian Old (XIX).json` — spec §4.11 mentions `RussianOld` for PUA but it is NOT in the 77-language scope.
