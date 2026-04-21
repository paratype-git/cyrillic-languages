# Glyph variants

Glyphs that do **not** have their own Unicode codepoint: they share a codepoint with a base letter, but render as a different shape under an OpenType `locl` feature (a localized form selected by the active language), sometimes with a style qualifier tying the swap to upright (`.str`) or italic (`.ita`) shaping.

This table complements the pan-Cyrillic character tables in `characters-uppercase.md` / `characters-lowercase.md`, which are deduplicated by codepoint. The entries below are the variant-form rows that the codepoint-level view collapses.

**39** locl variants — styles: any=22, straight=12, italic=5. Locales represented: ba, bg, cv, sr.

## Columns

- **Codepoint** — the Unicode codepoint the variant swaps shape for (same as the base letter in the main table), except for the Bashkir and Chuvash PUA-locl rows where it is the target PUA codepoint.
- **Case** — uppercase / lowercase.
- **Locale** — `bg` Bulgarian, `sr` Serbian, `ba` Bashkir, or `cv` Chuvash. These are the four non-default (non-ru) locl tags for which PT Serif Expert carries named variant glyphs.
- **Style** — `straight` or `italic` when the source token has a `.str` / `.ita` suffix; `any` otherwise.
- **Diagram** — an inline SVG showing `default shape → variant shape` plus a `[txt]` link to the glyphplotter source.
- **Languages** — language files that declare this variant.

## Variants

| # | Codepoint | Case | Locale | Style | Diagram | Languages |
| ---: | --- | --- | --- | --- | :---: | --- |
| 1 | 0414 | uppercase | bg | any | <img src="svg/variants/0414.bg.svg" width="170" alt="U+0414 .bg"> [txt](svg/variants/0414.bg.txt) | Bulgarian |
| 2 | 041B | uppercase | bg | any | <img src="svg/variants/041B.bg.svg" width="170" alt="U+041B .bg"> [txt](svg/variants/041B.bg.txt) | Bulgarian |
| 3 | 0431 | lowercase | sr | any | <img src="svg/variants/0431.sr.svg" width="170" alt="U+0431 .sr"> [txt](svg/variants/0431.sr.txt) | Macedonian, Serbian |
| 4 | 0432 | lowercase | bg | any | <img src="svg/variants/0432.bg.svg" width="170" alt="U+0432 .bg"> [txt](svg/variants/0432.bg.txt) | Bulgarian |
| 5 | 0433 | lowercase | bg | straight | <img src="svg/variants/0433.bg.svg" width="170" alt="U+0433 .bg"> [txt](svg/variants/0433.bg.txt) | Bulgarian |
| 6 | 0433 | lowercase | sr | italic | <img src="svg/variants/0433.sr.svg" width="170" alt="U+0433 .sr"> [txt](svg/variants/0433.sr.txt) | Serbian |
| 7 | 0434 | lowercase | bg | any | <img src="svg/variants/0434.bg.svg" width="170" alt="U+0434 .bg"> [txt](svg/variants/0434.bg.txt) | Bulgarian |
| 8 | 0434 | lowercase | sr | italic | <img src="svg/variants/0434.sr.svg" width="170" alt="U+0434 .sr"> [txt](svg/variants/0434.sr.txt) | Serbian |
| 9 | 0436 | lowercase | bg | any | <img src="svg/variants/0436.bg.svg" width="170" alt="U+0436 .bg"> [txt](svg/variants/0436.bg.txt) | Bulgarian |
| 10 | 0437 | lowercase | bg | any | <img src="svg/variants/0437.bg.svg" width="170" alt="U+0437 .bg"> [txt](svg/variants/0437.bg.txt) | Bulgarian |
| 11 | 0438 | lowercase | bg | straight | <img src="svg/variants/0438.bg.svg" width="170" alt="U+0438 .bg"> [txt](svg/variants/0438.bg.txt) | Bulgarian |
| 12 | 0439 | lowercase | bg | straight | <img src="svg/variants/0439.bg.svg" width="170" alt="U+0439 .bg"> [txt](svg/variants/0439.bg.txt) | Bulgarian |
| 13 | 043A | lowercase | bg | any | <img src="svg/variants/043A.bg.svg" width="170" alt="U+043A .bg"> [txt](svg/variants/043A.bg.txt) | Bulgarian |
| 14 | 043B | lowercase | bg | any | <img src="svg/variants/043B.bg.svg" width="170" alt="U+043B .bg"> [txt](svg/variants/043B.bg.txt) | Bulgarian |
| 15 | 043D | lowercase | bg | straight | <img src="svg/variants/043D.bg.svg" width="170" alt="U+043D .bg"> [txt](svg/variants/043D.bg.txt) | Bulgarian |
| 16 | 043F | lowercase | bg | straight | <img src="svg/variants/043F.bg.svg" width="170" alt="U+043F .bg"> [txt](svg/variants/043F.bg.txt) | Bulgarian |
| 17 | 043F | lowercase | sr | italic | <img src="svg/variants/043F.sr.svg" width="170" alt="U+043F .sr"> [txt](svg/variants/043F.sr.txt) | Serbian |
| 18 | 0442 | lowercase | bg | straight | <img src="svg/variants/0442.bg.svg" width="170" alt="U+0442 .bg"> [txt](svg/variants/0442.bg.txt) | Bulgarian |
| 19 | 0442 | lowercase | sr | italic | <img src="svg/variants/0442.sr.svg" width="170" alt="U+0442 .sr"> [txt](svg/variants/0442.sr.txt) | Serbian |
| 20 | 0446 | lowercase | bg | straight | <img src="svg/variants/0446.bg.svg" width="170" alt="U+0446 .bg"> [txt](svg/variants/0446.bg.txt) | Bulgarian |
| 21 | 0447 | lowercase | bg | straight | <img src="svg/variants/0447.bg.svg" width="170" alt="U+0447 .bg"> [txt](svg/variants/0447.bg.txt) | Bulgarian |
| 22 | 0448 | lowercase | bg | straight | <img src="svg/variants/0448.bg.svg" width="170" alt="U+0448 .bg"> [txt](svg/variants/0448.bg.txt) | Bulgarian |
| 23 | 0448 | lowercase | sr | italic | <img src="svg/variants/0448.sr.svg" width="170" alt="U+0448 .sr"> [txt](svg/variants/0448.sr.txt) | Serbian |
| 24 | 0449 | lowercase | bg | straight | <img src="svg/variants/0449.bg.svg" width="170" alt="U+0449 .bg"> [txt](svg/variants/0449.bg.txt) | Bulgarian |
| 25 | 044A | lowercase | bg | straight | <img src="svg/variants/044A.bg.svg" width="170" alt="U+044A .bg"> [txt](svg/variants/044A.bg.txt) | Bulgarian |
| 26 | 044C | lowercase | bg | straight | <img src="svg/variants/044C.bg.svg" width="170" alt="U+044C .bg"> [txt](svg/variants/044C.bg.txt) | Bulgarian |
| 27 | 044E | lowercase | bg | any | <img src="svg/variants/044E.bg.svg" width="170" alt="U+044E .bg"> [txt](svg/variants/044E.bg.txt) | Bulgarian |
| 28 | 0463 | lowercase | bg | any | <img src="svg/variants/0463.bg.svg" width="170" alt="U+0463 .bg"> [txt](svg/variants/0463.bg.txt) | Bulgarian |
| 29 | 0465 | lowercase | bg | any | <img src="svg/variants/0465.bg.svg" width="170" alt="U+0465 .bg"> [txt](svg/variants/0465.bg.txt) | Bulgarian |
| 30 | 046D | lowercase | bg | any | <img src="svg/variants/046D.bg.svg" width="170" alt="U+046D .bg"> [txt](svg/variants/046D.bg.txt) | Bulgarian |
| 31 | A657 | lowercase | bg | any | <img src="svg/variants/A657.bg.svg" width="170" alt="U+A657 .bg"> [txt](svg/variants/A657.bg.txt) | Bulgarian |
| 32 | F50A | uppercase | ba | any | <img src="svg/variants/F50A.ba.svg" width="170" alt="U+F50A .ba"> [txt](svg/variants/F50A.ba.txt) | Bashkir |
| 33 | F50B | lowercase | ba | any | <img src="svg/variants/F50B.ba.svg" width="170" alt="U+F50B .ba"> [txt](svg/variants/F50B.ba.txt) | Bashkir |
| 34 | F50C | uppercase | cv | any | <img src="svg/variants/F50C.cv.svg" width="170" alt="U+F50C .cv"> [txt](svg/variants/F50C.cv.txt) | Chuvash |
| 35 | F50D | lowercase | cv | any | <img src="svg/variants/F50D.cv.svg" width="170" alt="U+F50D .cv"> [txt](svg/variants/F50D.cv.txt) | Chuvash |
| 36 | F53C | uppercase | ba | any | <img src="svg/variants/F53C.ba.svg" width="170" alt="U+F53C .ba"> [txt](svg/variants/F53C.ba.txt) | Bashkir |
| 37 | F53D | lowercase | ba | any | <img src="svg/variants/F53D.ba.svg" width="170" alt="U+F53D .ba"> [txt](svg/variants/F53D.ba.txt) | Bashkir |
| 38 | F53E | uppercase | ba | any | <img src="svg/variants/F53E.ba.svg" width="170" alt="U+F53E .ba"> [txt](svg/variants/F53E.ba.txt) | Bashkir |
| 39 | F53F | lowercase | ba | any | <img src="svg/variants/F53F.ba.svg" width="170" alt="U+F53F .ba"> [txt](svg/variants/F53F.ba.txt) | Bashkir |
