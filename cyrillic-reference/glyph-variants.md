# Glyph variants

Glyphs that do **not** have their own Unicode codepoint: they share a codepoint with a base letter, but render as a different shape under an OpenType feature — typically `locl` (localized form, selected by the active language) or a stylistic alternate tied to upright (`.str`) or italic (`.ita`) shaping.

This table complements the pan-Cyrillic character tables in `characters-uppercase.md` / `characters-lowercase.md`, which are deduplicated by codepoint. The entries below are the variant-form rows that the codepoint-level view collapses.

**78** variant forms — 39 localized (`&`), 39 alternate (`+`). Style breakdown: any=44, straight=17, italic=17. Locales represented: ba, bg, cv, sr.

## Columns

- **Codepoint** — the Unicode codepoint this variant maps to. Same as the base letter in the main table.
- **Case** — uppercase / lowercase.
- **Locale** — the source language's `local` field. Only non-default locales (`bg` Bulgarian, `sr` Serbian, `ba` Bashkir, `cv` Chuvash) appear here, because ru-default languages do not produce locl shape variants — their `+` alternates are stylistic forms of letters that already have their own Unicode codepoint, listed in the main character table instead.
- **Style** — `straight` or `italic` when the source token has a `.str` / `.ita` suffix; `any` otherwise.
- **Marker** — `localized` (source token started with `&`) or `alternate` (source token started with `+`).
- **Token(s)** — verbatim source token(s) from `library/cyrillic/base/*.json`.
- **Languages** — language files that declare this variant.

## Variants

| # | Codepoint | Case | Locale | Style | Marker | Token(s) | Diagram | Languages |
| ---: | --- | --- | --- | --- | --- | --- | :---: | --- |
| 1 | 0414 | uppercase | bg | any | alternate | `+Д` |  | Bulgarian |
| 2 | 0414 | uppercase | bg | any | localized | `&Д` | <img src="svg/variants/0414.bg.svg" width="170" alt="U+0414 .bg"> [txt](svg/variants/0414.bg.txt) | Bulgarian |
| 3 | 041B | uppercase | bg | any | alternate | `+Л` |  | Bulgarian |
| 4 | 041B | uppercase | bg | any | localized | `&Л` | <img src="svg/variants/041B.bg.svg" width="170" alt="U+041B .bg"> [txt](svg/variants/041B.bg.txt) | Bulgarian |
| 5 | 0431 | lowercase | sr | any | alternate | `+б` |  | Macedonian, Serbian |
| 6 | 0431 | lowercase | sr | any | localized | `&б` | <img src="svg/variants/0431.sr.svg" width="170" alt="U+0431 .sr"> [txt](svg/variants/0431.sr.txt) | Macedonian, Serbian |
| 7 | 0432 | lowercase | bg | any | alternate | `+в` |  | Bulgarian |
| 8 | 0432 | lowercase | bg | any | localized | `&в` | <img src="svg/variants/0432.bg.svg" width="170" alt="U+0432 .bg"> [txt](svg/variants/0432.bg.txt) | Bulgarian |
| 9 | 0433 | lowercase | bg | italic | alternate | `+г.ita` |  | Bulgarian |
| 10 | 0433 | lowercase | bg | straight | localized | `&г.str` | <img src="svg/variants/0433.bg.svg" width="170" alt="U+0433 .bg"> [txt](svg/variants/0433.bg.txt) | Bulgarian |
| 11 | 0433 | lowercase | sr | italic | localized | `&г.ita` | <img src="svg/variants/0433.sr.svg" width="170" alt="U+0433 .sr"> [txt](svg/variants/0433.sr.txt) | Serbian |
| 12 | 0433 | lowercase | sr | straight | alternate | `+г.str` |  | Serbian |
| 13 | 0434 | lowercase | bg | any | alternate | `+д` |  | Bulgarian |
| 14 | 0434 | lowercase | bg | any | localized | `&д` | <img src="svg/variants/0434.bg.svg" width="170" alt="U+0434 .bg"> [txt](svg/variants/0434.bg.txt) | Bulgarian |
| 15 | 0434 | lowercase | sr | italic | localized | `&д.ita` | <img src="svg/variants/0434.sr.svg" width="170" alt="U+0434 .sr"> [txt](svg/variants/0434.sr.txt) | Serbian |
| 16 | 0434 | lowercase | sr | straight | alternate | `+д.str` |  | Serbian |
| 17 | 0436 | lowercase | bg | any | alternate | `+ж` |  | Bulgarian |
| 18 | 0436 | lowercase | bg | any | localized | `&ж` | <img src="svg/variants/0436.bg.svg" width="170" alt="U+0436 .bg"> [txt](svg/variants/0436.bg.txt) | Bulgarian |
| 19 | 0437 | lowercase | bg | any | alternate | `+з` |  | Bulgarian |
| 20 | 0437 | lowercase | bg | any | localized | `&з` | <img src="svg/variants/0437.bg.svg" width="170" alt="U+0437 .bg"> [txt](svg/variants/0437.bg.txt) | Bulgarian |
| 21 | 0438 | lowercase | bg | italic | alternate | `+и.ita` |  | Bulgarian |
| 22 | 0438 | lowercase | bg | straight | localized | `&и.str` | <img src="svg/variants/0438.bg.svg" width="170" alt="U+0438 .bg"> [txt](svg/variants/0438.bg.txt) | Bulgarian |
| 23 | 0439 | lowercase | bg | italic | alternate | `+й.ita` |  | Bulgarian |
| 24 | 0439 | lowercase | bg | straight | localized | `&й.str` | <img src="svg/variants/0439.bg.svg" width="170" alt="U+0439 .bg"> [txt](svg/variants/0439.bg.txt) | Bulgarian |
| 25 | 043A | lowercase | bg | any | alternate | `+к` |  | Bulgarian |
| 26 | 043A | lowercase | bg | any | localized | `&к` | <img src="svg/variants/043A.bg.svg" width="170" alt="U+043A .bg"> [txt](svg/variants/043A.bg.txt) | Bulgarian |
| 27 | 043B | lowercase | bg | any | alternate | `+л` |  | Bulgarian |
| 28 | 043B | lowercase | bg | any | localized | `&л` | <img src="svg/variants/043B.bg.svg" width="170" alt="U+043B .bg"> [txt](svg/variants/043B.bg.txt) | Bulgarian |
| 29 | 043D | lowercase | bg | italic | alternate | `+н.ita` |  | Bulgarian |
| 30 | 043D | lowercase | bg | straight | localized | `&н.str` | <img src="svg/variants/043D.bg.svg" width="170" alt="U+043D .bg"> [txt](svg/variants/043D.bg.txt) | Bulgarian |
| 31 | 043F | lowercase | bg | italic | alternate | `+п.ita` |  | Bulgarian |
| 32 | 043F | lowercase | bg | straight | localized | `&п.str` | <img src="svg/variants/043F.bg.svg" width="170" alt="U+043F .bg"> [txt](svg/variants/043F.bg.txt) | Bulgarian |
| 33 | 043F | lowercase | sr | italic | localized | `&п.ita` | <img src="svg/variants/043F.sr.svg" width="170" alt="U+043F .sr"> [txt](svg/variants/043F.sr.txt) | Serbian |
| 34 | 043F | lowercase | sr | straight | alternate | `+п.str` |  | Serbian |
| 35 | 0442 | lowercase | bg | italic | alternate | `+т.ita` |  | Bulgarian |
| 36 | 0442 | lowercase | bg | straight | localized | `&т.str` | <img src="svg/variants/0442.bg.svg" width="170" alt="U+0442 .bg"> [txt](svg/variants/0442.bg.txt) | Bulgarian |
| 37 | 0442 | lowercase | sr | italic | localized | `&т.ita` | <img src="svg/variants/0442.sr.svg" width="170" alt="U+0442 .sr"> [txt](svg/variants/0442.sr.txt) | Serbian |
| 38 | 0442 | lowercase | sr | straight | alternate | `+т.str` |  | Serbian |
| 39 | 0446 | lowercase | bg | italic | alternate | `+ц.ita` |  | Bulgarian |
| 40 | 0446 | lowercase | bg | straight | localized | `&ц.str` | <img src="svg/variants/0446.bg.svg" width="170" alt="U+0446 .bg"> [txt](svg/variants/0446.bg.txt) | Bulgarian |
| 41 | 0447 | lowercase | bg | italic | alternate | `+ч.ita` |  | Bulgarian |
| 42 | 0447 | lowercase | bg | straight | localized | `&ч.str` | <img src="svg/variants/0447.bg.svg" width="170" alt="U+0447 .bg"> [txt](svg/variants/0447.bg.txt) | Bulgarian |
| 43 | 0448 | lowercase | bg | italic | alternate | `+ш.ita` |  | Bulgarian |
| 44 | 0448 | lowercase | bg | straight | localized | `&ш.str` | <img src="svg/variants/0448.bg.svg" width="170" alt="U+0448 .bg"> [txt](svg/variants/0448.bg.txt) | Bulgarian |
| 45 | 0448 | lowercase | sr | italic | localized | `&ш.ita` | <img src="svg/variants/0448.sr.svg" width="170" alt="U+0448 .sr"> [txt](svg/variants/0448.sr.txt) | Serbian |
| 46 | 0448 | lowercase | sr | straight | alternate | `+ш.str` |  | Serbian |
| 47 | 0449 | lowercase | bg | italic | alternate | `+щ.ita` |  | Bulgarian |
| 48 | 0449 | lowercase | bg | straight | localized | `&щ.str` | <img src="svg/variants/0449.bg.svg" width="170" alt="U+0449 .bg"> [txt](svg/variants/0449.bg.txt) | Bulgarian |
| 49 | 044A | lowercase | bg | italic | alternate | `+ъ.ita` |  | Bulgarian |
| 50 | 044A | lowercase | bg | straight | localized | `&ъ.str` | <img src="svg/variants/044A.bg.svg" width="170" alt="U+044A .bg"> [txt](svg/variants/044A.bg.txt) | Bulgarian |
| 51 | 044C | lowercase | bg | italic | alternate | `+ь.ita` |  | Bulgarian |
| 52 | 044C | lowercase | bg | straight | localized | `&ь.str` | <img src="svg/variants/044C.bg.svg" width="170" alt="U+044C .bg"> [txt](svg/variants/044C.bg.txt) | Bulgarian |
| 53 | 044E | lowercase | bg | any | alternate | `+ю` |  | Bulgarian |
| 54 | 044E | lowercase | bg | any | localized | `&ю` | <img src="svg/variants/044E.bg.svg" width="170" alt="U+044E .bg"> [txt](svg/variants/044E.bg.txt) | Bulgarian |
| 55 | 0463 | lowercase | bg | any | alternate | `+ѣ` |  | Bulgarian |
| 56 | 0463 | lowercase | bg | any | localized | `&ѣ` | <img src="svg/variants/0463.bg.svg" width="170" alt="U+0463 .bg"> [txt](svg/variants/0463.bg.txt) | Bulgarian |
| 57 | 0465 | lowercase | bg | any | alternate | `+ѥ` |  | Bulgarian |
| 58 | 0465 | lowercase | bg | any | localized | `&ѥ` | <img src="svg/variants/0465.bg.svg" width="170" alt="U+0465 .bg"> [txt](svg/variants/0465.bg.txt) | Bulgarian |
| 59 | 046D | lowercase | bg | any | alternate | `+ѭ` |  | Bulgarian |
| 60 | 046D | lowercase | bg | any | localized | `&ѭ` | <img src="svg/variants/046D.bg.svg" width="170" alt="U+046D .bg"> [txt](svg/variants/046D.bg.txt) | Bulgarian |
| 61 | 0492 | uppercase | ba | any | alternate | `+Ғ` |  | Bashkir |
| 62 | 0493 | lowercase | ba | any | alternate | `+ғ` |  | Bashkir |
| 63 | 0498 | uppercase | ba | any | alternate | `+Ҙ` |  | Bashkir |
| 64 | 0499 | lowercase | ba | any | alternate | `+ҙ` |  | Bashkir |
| 65 | 04AA | uppercase | ba | any | alternate | `+Ҫ` |  | Bashkir |
| 66 | 04AA | uppercase | cv | any | alternate | `+Ҫ` |  | Chuvash |
| 67 | 04AB | lowercase | ba | any | alternate | `+ҫ` |  | Bashkir |
| 68 | 04AB | lowercase | cv | any | alternate | `+ҫ` |  | Chuvash |
| 69 | A657 | lowercase | bg | any | alternate | `+ꙗ` |  | Bulgarian |
| 70 | A657 | lowercase | bg | any | localized | `&ꙗ` | <img src="svg/variants/A657.bg.svg" width="170" alt="U+A657 .bg"> [txt](svg/variants/A657.bg.txt) | Bulgarian |
| 71 | F50A | uppercase | ba | any | localized | `&!F50A` | <img src="svg/variants/F50A.ba.svg" width="170" alt="U+F50A .ba"> [txt](svg/variants/F50A.ba.txt) | Bashkir |
| 72 | F50B | lowercase | ba | any | localized | `&!F50B` | <img src="svg/variants/F50B.ba.svg" width="170" alt="U+F50B .ba"> [txt](svg/variants/F50B.ba.txt) | Bashkir |
| 73 | F50C | uppercase | cv | any | localized | `&!F50C` | <img src="svg/variants/F50C.cv.svg" width="170" alt="U+F50C .cv"> [txt](svg/variants/F50C.cv.txt) | Chuvash |
| 74 | F50D | lowercase | cv | any | localized | `&!F50D` | <img src="svg/variants/F50D.cv.svg" width="170" alt="U+F50D .cv"> [txt](svg/variants/F50D.cv.txt) | Chuvash |
| 75 | F53C | uppercase | ba | any | localized | `&!F53C` | <img src="svg/variants/F53C.ba.svg" width="170" alt="U+F53C .ba"> [txt](svg/variants/F53C.ba.txt) | Bashkir |
| 76 | F53D | lowercase | ba | any | localized | `&!F53D` | <img src="svg/variants/F53D.ba.svg" width="170" alt="U+F53D .ba"> [txt](svg/variants/F53D.ba.txt) | Bashkir |
| 77 | F53E | uppercase | ba | any | localized | `&!F53E` | <img src="svg/variants/F53E.ba.svg" width="170" alt="U+F53E .ba"> [txt](svg/variants/F53E.ba.txt) | Bashkir |
| 78 | F53F | lowercase | ba | any | localized | `&!F53F` | <img src="svg/variants/F53F.ba.svg" width="170" alt="U+F53F .ba"> [txt](svg/variants/F53F.ba.txt) | Bashkir |
