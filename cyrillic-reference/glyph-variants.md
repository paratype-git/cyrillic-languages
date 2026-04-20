# Glyph variants

Glyphs that do **not** have their own Unicode codepoint: they share a codepoint with a base letter, but render as a different shape under an OpenType feature — typically `locl` (localized form, selected by the active language) or a stylistic alternate tied to upright (`.str`) or italic (`.ita`) shaping.

This table complements the pan-Cyrillic character tables in `characters-uppercase.md` / `characters-lowercase.md`, which are deduplicated by codepoint. The entries below are the variant-form rows that the codepoint-level view collapses.

**128** variant forms — 41 localized (`&`), 87 alternate (`+`). Style breakdown: any=94, straight=17, italic=17. Locales represented: ba, bg, cv, ru, sr.

## Columns

- **Codepoint** — the Unicode codepoint this variant maps to. Same as the base letter in the main table.
- **Case** — uppercase / lowercase.
- **Locale** — the source language's `local` field (`ru` default, `bg` Bulgarian, `sr` Serbian, …). A `&`-marked token is the localized glyph selected by that locale.
- **Style** — `straight` or `italic` when the source token has a `.str` / `.ita` suffix; `any` otherwise.
- **Marker** — `localized` (source token started with `&`) or `alternate` (source token started with `+`).
- **Token(s)** — verbatim source token(s) from `library/cyrillic/base/*.json`.
- **Languages** — language files that declare this variant.

## Variants

| # | Codepoint | Case | Locale | Style | Marker | Token(s) | Languages |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 02BC | lowercase | ru | any | alternate | `+ʼ` | Saami Kildin |
| 2 | 02BC | uppercase | ru | any | alternate | `+ʼ` | Saami Kildin |
| 3 | 0414 | uppercase | bg | any | alternate | `+Д` | Bulgarian |
| 4 | 0414 | uppercase | bg | any | localized | `&Д` | Bulgarian |
| 5 | 0416 | uppercase | bg | any | alternate | `+Ж` | Bulgarian |
| 6 | 0416 | uppercase | bg | any | localized | `&Ж` | Bulgarian |
| 7 | 041A | uppercase | bg | any | alternate | `+К` | Bulgarian |
| 8 | 041A | uppercase | bg | any | localized | `&К` | Bulgarian |
| 9 | 041B | uppercase | bg | any | alternate | `+Л` | Bulgarian |
| 10 | 041B | uppercase | bg | any | localized | `&Л` | Bulgarian |
| 11 | 0431 | lowercase | sr | any | alternate | `+б` | Macedonian, Serbian |
| 12 | 0431 | lowercase | sr | any | localized | `&б` | Macedonian, Serbian |
| 13 | 0432 | lowercase | bg | any | alternate | `+в` | Bulgarian |
| 14 | 0432 | lowercase | bg | any | localized | `&в` | Bulgarian |
| 15 | 0433 | lowercase | bg | italic | alternate | `+г.ita` | Bulgarian |
| 16 | 0433 | lowercase | bg | straight | localized | `&г.str` | Bulgarian |
| 17 | 0433 | lowercase | sr | italic | localized | `&г.ita` | Serbian |
| 18 | 0433 | lowercase | sr | straight | alternate | `+г.str` | Serbian |
| 19 | 0434 | lowercase | bg | any | alternate | `+д` | Bulgarian |
| 20 | 0434 | lowercase | bg | any | localized | `&д` | Bulgarian |
| 21 | 0434 | lowercase | sr | italic | localized | `&д.ita` | Serbian |
| 22 | 0434 | lowercase | sr | straight | alternate | `+д.str` | Serbian |
| 23 | 0436 | lowercase | bg | any | alternate | `+ж` | Bulgarian |
| 24 | 0436 | lowercase | bg | any | localized | `&ж` | Bulgarian |
| 25 | 0437 | lowercase | bg | any | alternate | `+з` | Bulgarian |
| 26 | 0437 | lowercase | bg | any | localized | `&з` | Bulgarian |
| 27 | 0438 | lowercase | bg | italic | alternate | `+и.ita` | Bulgarian |
| 28 | 0438 | lowercase | bg | straight | localized | `&и.str` | Bulgarian |
| 29 | 0439 | lowercase | bg | italic | alternate | `+й.ita` | Bulgarian |
| 30 | 0439 | lowercase | bg | straight | localized | `&й.str` | Bulgarian |
| 31 | 043A | lowercase | bg | any | alternate | `+к` | Bulgarian |
| 32 | 043A | lowercase | bg | any | localized | `&к` | Bulgarian |
| 33 | 043B | lowercase | bg | any | alternate | `+л` | Bulgarian |
| 34 | 043B | lowercase | bg | any | localized | `&л` | Bulgarian |
| 35 | 043D | lowercase | bg | italic | alternate | `+н.ita` | Bulgarian |
| 36 | 043D | lowercase | bg | straight | localized | `&н.str` | Bulgarian |
| 37 | 043F | lowercase | bg | italic | alternate | `+п.ita` | Bulgarian |
| 38 | 043F | lowercase | bg | straight | localized | `&п.str` | Bulgarian |
| 39 | 043F | lowercase | sr | italic | localized | `&п.ita` | Serbian |
| 40 | 043F | lowercase | sr | straight | alternate | `+п.str` | Serbian |
| 41 | 0442 | lowercase | bg | italic | alternate | `+т.ita` | Bulgarian |
| 42 | 0442 | lowercase | bg | straight | localized | `&т.str` | Bulgarian |
| 43 | 0442 | lowercase | sr | italic | localized | `&т.ita` | Serbian |
| 44 | 0442 | lowercase | sr | straight | alternate | `+т.str` | Serbian |
| 45 | 0446 | lowercase | bg | italic | alternate | `+ц.ita` | Bulgarian |
| 46 | 0446 | lowercase | bg | straight | localized | `&ц.str` | Bulgarian |
| 47 | 0447 | lowercase | bg | italic | alternate | `+ч.ita` | Bulgarian |
| 48 | 0447 | lowercase | bg | straight | localized | `&ч.str` | Bulgarian |
| 49 | 0448 | lowercase | bg | italic | alternate | `+ш.ita` | Bulgarian |
| 50 | 0448 | lowercase | bg | straight | localized | `&ш.str` | Bulgarian |
| 51 | 0448 | lowercase | sr | italic | localized | `&ш.ita` | Serbian |
| 52 | 0448 | lowercase | sr | straight | alternate | `+ш.str` | Serbian |
| 53 | 0449 | lowercase | bg | italic | alternate | `+щ.ita` | Bulgarian |
| 54 | 0449 | lowercase | bg | straight | localized | `&щ.str` | Bulgarian |
| 55 | 044A | lowercase | bg | italic | alternate | `+ъ.ita` | Bulgarian |
| 56 | 044A | lowercase | bg | straight | localized | `&ъ.str` | Bulgarian |
| 57 | 044C | lowercase | bg | italic | alternate | `+ь.ita` | Bulgarian |
| 58 | 044C | lowercase | bg | straight | localized | `&ь.str` | Bulgarian |
| 59 | 044E | lowercase | bg | any | alternate | `+ю` | Bulgarian |
| 60 | 044E | lowercase | bg | any | localized | `&ю` | Bulgarian |
| 61 | 0463 | lowercase | bg | any | alternate | `+ѣ` | Bulgarian |
| 62 | 0463 | lowercase | bg | any | localized | `&ѣ` | Bulgarian |
| 63 | 0465 | lowercase | bg | any | alternate | `+ѥ` | Bulgarian |
| 64 | 0465 | lowercase | bg | any | localized | `&ѥ` | Bulgarian |
| 65 | 046D | lowercase | bg | any | alternate | `+ѭ` | Bulgarian |
| 66 | 046D | lowercase | bg | any | localized | `&ѭ` | Bulgarian |
| 67 | 048A | uppercase | ru | any | alternate | `+Ҋ` | Saami Kildin |
| 68 | 048B | lowercase | ru | any | alternate | `+ҋ` | Saami Kildin |
| 69 | 0492 | uppercase | ba | any | alternate | `+Ғ` | Bashkir |
| 70 | 0493 | lowercase | ba | any | alternate | `+ғ` | Bashkir |
| 71 | 0494 | uppercase | ru | any | alternate | `+Ҕ` | Even (Lamut) |
| 72 | 0495 | lowercase | ru | any | alternate | `+ҕ` | Even (Lamut) |
| 73 | 0496 | uppercase | ru | any | alternate | `+Җ` | Yukagir |
| 74 | 0497 | lowercase | ru | any | alternate | `+җ` | Yukagir |
| 75 | 0498 | uppercase | ba | any | alternate | `+Ҙ` | Bashkir |
| 76 | 0499 | lowercase | ba | any | alternate | `+ҙ` | Bashkir |
| 77 | 04A4 | uppercase | ru | any | alternate | `+Ҥ` | Even (Lamut) |
| 78 | 04A5 | lowercase | ru | any | alternate | `+ҥ` | Even (Lamut) |
| 79 | 04AA | uppercase | ba | any | alternate | `+Ҫ` | Bashkir |
| 80 | 04AA | uppercase | cv | any | alternate | `+Ҫ` | Chuvash |
| 81 | 04AB | lowercase | ba | any | alternate | `+ҫ` | Bashkir |
| 82 | 04AB | lowercase | cv | any | alternate | `+ҫ` | Chuvash |
| 83 | 04AE | uppercase | ru | any | alternate | `+Ү` | Even (Lamut) |
| 84 | 04AF | lowercase | ru | any | alternate | `+ү` | Even (Lamut) |
| 85 | 04BA | uppercase | ru | any | alternate | `+Һ` | Even (Lamut) |
| 86 | 04BB | lowercase | ru | any | alternate | `+һ` | Even (Lamut) |
| 87 | 04C3 | uppercase | ru | any | alternate | `+Ӄ` | Khanty, Yukagir |
| 88 | 04C4 | lowercase | ru | any | alternate | `+ӄ` | Khanty, Yukagir |
| 89 | 04C7 | uppercase | ru | any | alternate | `+Ӈ` | Khanty, Yukagir |
| 90 | 04C8 | lowercase | ru | any | alternate | `+ӈ` | Khanty, Yukagir |
| 91 | 04E6 | uppercase | ru | any | alternate | `+Ӧ` | Yukagir |
| 92 | 04E7 | lowercase | ru | any | alternate | `+ӧ` | Yukagir |
| 93 | 04EC | uppercase | ru | any | alternate | `+Ӭ` | Selkup |
| 94 | 04ED | lowercase | ru | any | alternate | `+ӭ` | Selkup |
| 95 | 04F0 | uppercase | ru | any | alternate | `+Ӱ` | Nganasan |
| 96 | 04F1 | lowercase | ru | any | alternate | `+ӱ` | Nganasan |
| 97 | 04F6 | uppercase | ru | any | alternate | `+Ӷ` | Yukagir |
| 98 | 04F7 | lowercase | ru | any | alternate | `+ӷ` | Yukagir |
| 99 | 04FC | uppercase | ru | any | alternate | `+Ӽ` | Khanty |
| 100 | 04FD | lowercase | ru | any | alternate | `+ӽ` | Khanty |
| 101 | 0510 | uppercase | ru | any | alternate | `+Ԑ` | Khanty |
| 102 | 0511 | lowercase | ru | any | alternate | `+ԑ` | Khanty |
| 103 | 0512 | uppercase | ru | any | alternate | `+Ԓ` | Khanty |
| 104 | 0513 | lowercase | ru | any | alternate | `+ԓ` | Khanty |
| 105 | 0526 | uppercase | ru | any | alternate | `+Ԧ` | Tat |
| 106 | 0527 | lowercase | ru | any | alternate | `+ԧ` | Tat |
| 107 | A657 | lowercase | bg | any | alternate | `+ꙗ` | Bulgarian |
| 108 | A657 | lowercase | bg | any | localized | `&ꙗ` | Bulgarian |
| 109 | F49E | uppercase | ru | any | alternate | `+` | Tat |
| 110 | F49F | lowercase | ru | any | alternate | `+` | Tat |
| 111 | F4C6 | uppercase | ru | any | alternate | `+` | Khanty |
| 112 | F4C7 | lowercase | ru | any | alternate | `+` | Khanty |
| 113 | F4CC | uppercase | ru | any | alternate | `+` | Karachay-Balkar |
| 114 | F4CD | lowercase | ru | any | alternate | `+` | Karachay-Balkar |
| 115 | F50A | uppercase | ba | any | localized | `&!F50A` | Bashkir |
| 116 | F50A | uppercase | ru | any | alternate | `+` | Selkup |
| 117 | F50B | lowercase | ba | any | localized | `&!F50B` | Bashkir |
| 118 | F50B | lowercase | ru | any | alternate | `+` | Selkup |
| 119 | F50C | uppercase | cv | any | localized | `&!F50C` | Chuvash |
| 120 | F50C | uppercase | ru | any | alternate | `+` | Enets, Nganasan |
| 121 | F50D | lowercase | cv | any | localized | `&!F50D` | Chuvash |
| 122 | F50D | lowercase | ru | any | alternate | `+` | Enets, Nganasan |
| 123 | F538 | uppercase | ru | any | alternate | `+` | Khanty |
| 124 | F539 | lowercase | ru | any | alternate | `+` | Khanty |
| 125 | F53C | uppercase | ba | any | localized | `&!F53C` | Bashkir |
| 126 | F53D | lowercase | ba | any | localized | `&!F53D` | Bashkir |
| 127 | F53E | uppercase | ba | any | localized | `&!F53E` | Bashkir |
| 128 | F53F | lowercase | ba | any | localized | `&!F53F` | Bashkir |
