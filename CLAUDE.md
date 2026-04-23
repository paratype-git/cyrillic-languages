# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project at a glance

Paratype's multilingual Cyrillic alphabet reference. A static site whose per-language JSON data is **generated** by a Python pipeline from hand-edited source JSONs. There is no package manager, no test suite, no build tool beyond Python 3 stdlib. The whole repository is released under the **MIT License** (`LICENSE` at repo root).

Two pipelines share this tree:
- `cyrillic-languages/` — the data repo proper: per-language JSONs, the Python pipeline that rolls them up, and the generated site artifacts.
- `cyrillic-reference/` — a pan-Cyrillic Unicode reference set generated from the data above. Produces Markdown character tables, a glyph-variant catalog, per-letter SVG decomposition diagrams in both PT Sans Expert and PT Serif Expert, and machine-readable per-language + pan-Cyrillic JSON under `data/`. Three independent generators share a `tools/_catalog.py` core: `tools/generate.py` (stdlib, emits MD tables), `tools/generate_svgs.py` (fontTools + FontDocTools, emits SVG diagrams), `tools/generate_json.py` (stdlib, emits `data/`). Own README + `data/README.md`.

**Where to find the authoritative docs.** Before writing anything that will end up in a user-visible place, check these first — they are the source of truth and must stay in sync with whatever you produce:

- `README.md` — project overview + repository map (what contributors may edit vs. what is operator-only)
- `CONTRIBUTING.md` / `CONTRIBUTING-RU.md` — contributor-facing guide: schema, markers, workflow
- `docs/MAINTAINING.md` — operator docs: pipeline, scripts, config files, known limitations

## Scope

Contributor-facing docs cover **the Cyrillic library only**. The Latin tree under `cyrillic-languages/library/latin/` is an internal work-in-progress and is explicitly not open for external PRs. When expanding docs or building tooling, default to cyrillic-only unless the user explicitly asks for latin.

## Commands

From `cyrillic-languages/scripts/` (Python 3 stdlib, no deps):

```bash
python3 compile_languages.py                                    # full rebuild (cyrillic + latin)
python3 compile_languages.py -s cyrillic                        # cyrillic only
python3 compile_languages.py -s cyrillic -n Avar                # one language
python3 compile_languages.py -s cyrillic -n "Altaic (Oirot)"    # quote names with spaces/parens
```

`-n` only rebuilds the per-language file; the pan-script summary is always regenerated from every enabled language. `DEVELOPMENT = True` at the top of `compile_languages.py` toggles `indent=4` in the output JSON. See `docs/MAINTAINING.md` "Running the pipeline" for the full operator workflow (reviewing a PR → regenerate site → commit).

## Pipeline big picture

```
library/cyrillic/{cyrillic_library.json,sortorder_cyrillic.txt}
library/cyrillic/base/<Language>.json          <-- hand-edited sources (contributor surface)
languages.json, locales.json, glyphs_list_categories.json,
unicode14.txt, PT_PUA_unicodes-descriptions.txt
             │
             ▼  scripts/compile_languages.py
             │
site/cyrillic/base/<Language>.json             <-- generated, operator commits alongside PR
site/cyrillic/cyrillic_characters_lib.json     <-- generated pan-script summary
```

Two stages: `compileLagnuages` emits per-language site JSONs; `makeMainCharactersSet` aggregates them into the pan-script summary, sorted via `sortorder_cyrillic.txt`.

## Glyph markers — read this before touching data

The per-language `glyphs_list` entries carry `uppercase`/`lowercase` strings of space-separated tokens annotated with markers. The `marks` list in `compile_languages.py` names more markers than are actually used — several are dead leftovers. **The full reference is `CONTRIBUTING.md`; `docs/MAINTAINING.md` "Known limitations" has the dead-marker breakdown.** The old `notes.txt` cheat-sheet is archived (and gitignored) under `scripts/_legacy/` — it is out of date and should not be used as a reference.

Short version (classification based on a full data scan performed April 2026; re-verify against `library/cyrillic/base/**/*.json` if in doubt):
- **Live:** `+` alternate, `=` equivalent (latin only in practice), `&` localized form, `:` digraph, `!XXXX` unicode escape, `.ita`/`.str` style-specific suffixes
- **Dead (do not use):** `*`, `$`, `#`, `@`, `<`, `.alt` (their role moved to the `type` field on each `glyphs_list` block); `(`, `)`, `[`, `]` would crash the parser

Categories now expressed via the `type` field: `alphabet`, `extended`, `historic`, `dialect`, `consideration` (+ the synthesized `charset`).

## Private Use Area — do not call it "Paratype-owned"

The Unicode PUA (`E000`–`F8FF`) is a blank range the Unicode Consortium leaves unassigned — **nobody owns specific codepoints in it.** Paratype historically uses part of this range inside its own fonts (PT Sans Expert / PT Serif Expert) to encode glyphs that lack an official Unicode assignment. `!FXXX` in this repo means "the glyph at this codepoint *in the Paratype Expert fonts*"; the same hex in another foundry's font usually shows a different glyph or nothing. When documenting PUA, frame it as a shared range that Paratype *uses*, never as a proprietary zone.

## Repository layout at a glance

```
/
├── README.md, CONTRIBUTING.md, CONTRIBUTING-RU.md, CLAUDE.md
├── docs/MAINTAINING.md                            ← operator docs
├── .github/
│   ├── CODEOWNERS                                 ← auto-requests @typedev on operator-only paths
│   └── PULL_REQUEST_TEMPLATE.md                   ← auto-filled PR body with checklist
├── .gitignore                                     ← excludes site-engine files kept only for local dev
├── LICENSE                                        ← MIT, covers the whole repository
├── cyrillic-languages/
│   ├── library/cyrillic/base/<Language>.json      ← contributor surface
│   ├── library/cyrillic/cyrillic_library.json     ← language registry (enable, code_pt)
│   ├── library/cyrillic/sortorder_cyrillic.txt    ← pan-Cyrillic sort order
│   ├── library/cyrillic/_legacy/                  ← archived legacy-schema files, not processed
│   ├── library/latin/**                           ← WIP, not open for contributions
│   ├── site/{cyrillic,latin}/**                   ← generated, operator-only
│   ├── scripts/compile_languages.py               ← the pipeline (the only script needed for builds)
│   ├── scripts/{dumpLangDescriptions,reloadDescriptions}.py   ← bulk description dump/reload round-trip
│   ├── {languages,locales,glyphs_list_categories}.json
│   └── unicode14.txt, PT_PUA_unicodes-descriptions.txt  ← reference tables
└── cyrillic-reference/
    ├── LICENSE                                    ← MIT (redundant w/ root; explicit for this subtree)
    ├── README.md                                  ← subproject docs — pipeline, calibration, manual re-render
    ├── TODO.md                                    ← status notes; §1–§3 done, §4 (publish) + two follow-ups open
    ├── tools/_catalog.py                          ← shared core: decompose, variants, language catalog (stdlib)
    ├── tools/generate.py                          ← stdlib; emits the MD tables below
    ├── tools/generate_svgs.py                     ← needs fontTools + FontDocTools; emits SVG diagrams
    ├── tools/generate_json.py                     ← stdlib; emits data/pan-cyrillic.json + data/languages/*.json
    ├── characters-uppercase.md                    ← generated; pan-Cyrillic uppercase codepoints
    ├── characters-lowercase.md                    ← generated; pan-Cyrillic lowercase codepoints
    ├── glyph-variants.md                          ← generated; locl variants
    ├── data/pan-cyrillic.json, data/languages/*.json  ← generated; machine-readable mirror (see data/README.md)
    ├── svg/{Sans,Serif}/{uc,lc,variants}/         ← generated; per-row .svg per family
    └── glyphplotter/{Sans,Serif}/{uc,lc,variants}/ ← generated; per-row plotter .txt sources per family
```

Two categories of files are **gitignored** here and kept only on the maintainer's machine:

- **Site engine** (`static/`, `fonts/`, `index.html`, `asset-manifest.json`, `favicon.ico`, `robots.txt`) — lives in [paratype/paratype.github.io](https://github.com/paratype/paratype.github.io/tree/main/cyrillic-languages). Kept locally for offline site preview.
- **`scripts/_legacy/`** — one-shot migrations, archived diagnostics, the old `PTLangLib` helper, and historical `langdesc-*.txt` snapshots. Not part of the recurring toolchain.

## Things that will bite

- **Hardcoded locales** in `compile_languages.py` (`laguagesOrderSorter.__init__`): adding a new locale requires editing code + `locales.json` + `sortorder_cyrillic.txt`. Logged in `docs/MAINTAINING.md` TODOs.
- **Absolute user paths** in `scripts/dumpLangDescriptions.py` and in the archived one-shots under `scripts/_legacy/` — they were written on someone's macOS setup and need path fixes before any run.
- **Legacy files in `library/cyrillic/_legacy/`** are not in the index and not processed; two of them use a pre-`glyphs_list` schema. Do not treat them as templates.
- **Contributor PRs must only touch `library/cyrillic/base/`** — `site/` is regenerated by the operator, never hand-edited. CODEOWNERS auto-requests `@typedev` on anything outside the contributor surface.
- **Editing `compile_languages.py` carries risk**: the file has layers of commented-out code from earlier iterations; the user's explicit preference is not to refactor it, only to annotate comments in English.
- **`README.md` / `CONTRIBUTING*.md` / `docs/MAINTAINING.md` are a contract** with external contributors. Edits to them may change what PRs contributors file. Prefer additions over rewrites; flag any substantive rule change explicitly.
- **Production site still fetches from the old data location.** The React bundle at <https://paratype.github.io/cyrillic-languages/> has `raw.githubusercontent.com/paratype/paratype.github.io/main/cyrillic-languages/site/...` URLs baked in. Until that bundle is rebuilt to point at `paratype-git/cyrillic-languages`, changes committed here do **not** reach the public site. Any "regenerate site/ → push" workflow looks correct locally but is invisible to users.
