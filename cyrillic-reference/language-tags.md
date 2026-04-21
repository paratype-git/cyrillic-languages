# Cyrillic languages — language-tag table

All 79 languages declared in `cyrillic-languages/library/cyrillic/cyrillic_library.json`, with the identifier fields we know today and placeholders for the external tag systems we have not yet filled in. Re-generated from [`tools/generate_language_tags.py`](tools/generate_language_tags.py).

**Columns:**

- **name_eng / name_rus** — from `cyrillic_library.json`.
- **code_pt** — Paratype's internal per-language identifier.
- **enable** — whether the language is currently compiled by the pipeline.
- **local** — OT `locl` tag used as the source file's default (blank = inherits script default, which is `ru` for this library).
- **iso639_1 / iso639_3 / bcp47 / ot_lang** — external tag systems. `TBD` placeholders mean this row still needs a human-verified value; many of these languages have obscure ISO codes or none at all.

| # | name_eng | name_rus | code_pt | enable | local | iso639_1 | iso639_3 | bcp47 | ot_lang |
| ---: | --- | --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Abazin | Абазинский | 1 | yes | ru | TBD | TBD | TBD | TBD |
| 2 | Abkhazian | Абхазский | 90 | yes | ru | TBD | TBD | TBD | TBD |
| 3 | Avar | Аварский | 5 | yes | ru | TBD | TBD | TBD | TBD |
| 4 | Aghul | Агульский | 147 | yes | ru | TBD | TBD | TBD | TBD |
| 5 | Adyge | Адыгейский | 2 | yes | ru | TBD | TBD | TBD | TBD |
| 6 | Azeri | Азербайджанский | 6 | yes | ru | TBD | TBD | TBD | TBD |
| 7 | Altaic (Oirot) | Алтайский | 92 | yes | ru | TBD | TBD | TBD | TBD |
| 8 | Bashkir | Башкирский | 8 | yes | ba | TBD | TBD | TBD | TBD |
| 9 | Belarusian | Белорусский | 9 | yes | ru | TBD | TBD | TBD | TBD |
| 10 | Bulgarian | Болгарский | 11 | yes | bg | TBD | TBD | TBD | TBD |
| 11 | Buryat | Бурятский | 12 | yes | ru | TBD | TBD | TBD | TBD |
| 12 | Gagauz | Гагаузский | 105 | yes | ru | TBD | TBD | TBD | TBD |
| 13 | Dargwa | Даргинский | 18 | yes | ru | TBD | TBD | TBD | TBD |
| 14 | Dolgan | Долганский | 148 | yes | ru | TBD | TBD | TBD | TBD |
| 15 | Dungan | Дунганский | 20 | yes | ru | TBD | TBD | TBD | TBD |
| 16 | Ingush | Ингушский | 34 | yes | ru | TBD | TBD | TBD | TBD |
| 17 | Itelmen | Ительменский | 146 | yes | ru | TBD | TBD | TBD | TBD |
| 18 | Kabardino-Cirkassian | Кабардино-Черкесский | 37 | yes | ru | TBD | TBD | TBD | TBD |
| 19 | Kabardian | Кабардинский | 136 | yes | ru | TBD | TBD | TBD | TBD |
| 20 | Kazakh | Казахский | 40 | yes | ru | TBD | TBD | TBD | TBD |
| 21 | Kaitag | Кайтагский | 161 | yes | ru | TBD | TBD | TBD | TBD |
| 22 | Kalmyk | Калмыцкий | 38 | yes | ru | TBD | TBD | TBD | TBD |
| 23 | Karakalpak | Каракалпакский | 39 | yes | ru | TBD | TBD | TBD | TBD |
| 24 | Karachay-Balkar | Карачаево-Балкарский | 114 | yes | ru | TBD | TBD | TBD | TBD |
| 25 | Saami Kildin | Кильдинский | 116 | yes | ru | TBD | TBD | TBD | TBD |
| 26 | Kirghiz | Киргизский | 41 | yes | ru | TBD | TBD | TBD | TBD |
| 27 | Komi-Zyrian | Коми-зырянский | 112 | yes | ru | TBD | TBD | TBD | TBD |
| 28 | Komi-Permyak | Коми-пермяцкий | 111 | yes | ru | TBD | TBD | TBD | TBD |
| 29 | Koryak | Корякский | 113 | yes | ru | TBD | TBD | TBD | TBD |
| 30 | Kryashen Tatar | Кряшенский | 135 | yes | ru | TBD | TBD | TBD | TBD |
| 31 | Kumyk | Кумыкский | 42 | yes | ru | TBD | TBD | TBD | TBD |
| 32 | Kurdish | Курдский | 142 | yes | ru | TBD | TBD | TBD | TBD |
| 33 | Lak | Лакский | 44 | yes | ru | TBD | TBD | TBD | TBD |
| 34 | Lezgin | Лезгинский | 46 | yes | ru | TBD | TBD | TBD | TBD |
| 35 | Macedonian | Македонский | 48 | yes | sr | TBD | TBD | TBD | TBD |
| 36 | Manci | Мансийский | 121 | yes | ru | TBD | TBD | TBD | TBD |
| 37 | Mari-high | Марийский (горный) | 122 | yes | ru | TBD | TBD | TBD | TBD |
| 38 | Mari-low | Марийский (луговой) | 118 | yes | ru | TBD | TBD | TBD | TBD |
| 39 | Moldavian | Молдавский | 50 | yes | ru | TBD | TBD | TBD | TBD |
| 40 | Mongolian | Монгольский | 51 | yes | ru | TBD | TBD | TBD | TBD |
| 41 | Mordvin-Moksha | Мордовско-Мокшанский | 53 | yes | ru | TBD | TBD | TBD | TBD |
| 42 | Mordvin-Erzya | Мордовско-Эрзянский | 52 | yes | ru | TBD | TBD | TBD | TBD |
| 43 | Nanai | Нанайский | 54 | yes | ru | TBD | TBD | TBD | TBD |
| 44 | Nganasan | Нганасанский | 149 | yes | ru | TBD | TBD | TBD | TBD |
| 45 | Negidal | Негидальский | 159 | yes | ru | TBD | TBD | TBD | TBD |
| 46 | Nenets (Yurak) | Ненецкий | 55 | yes | ru | TBD | TBD | TBD | TBD |
| 47 | Nivkh | Нивхский | 56 | yes | ru | TBD | TBD | TBD | TBD |
| 48 | Nogai | Ногайский | 57 | yes | ru | TBD | TBD | TBD | TBD |
| 49 | Ossetic | Осетинский | 123 | yes | ru | TBD | TBD | TBD | TBD |
| 50 | Russian | Русский | 64 | yes | ru | TBD | TBD | TBD | TBD |
| 51 | Rutul | Рутульский | 151 | yes | ru | TBD | TBD | TBD | TBD |
| 52 | Selkup | Селькупский | 65 | yes | ru | TBD | TBD | TBD | TBD |
| 53 | Serbian | Сербский | 66 | yes | sr | TBD | TBD | TBD | TBD |
| 54 | Tabasaran | Табасаранский | 73 | yes | ru | TBD | TBD | TBD | TBD |
| 55 | Tadzhik | Таджикский | 85 | yes | ru | TBD | TBD | TBD | TBD |
| 56 | Talysh | Талышский | 137 | yes | ru | TBD | TBD | TBD | TBD |
| 57 | Tatar | Татарский | 74 | yes | ru | TBD | TBD | TBD | TBD |
| 58 | Tat | Татский | 144 | yes | ru | TBD | TBD | TBD | TBD |
| 59 | Tofalar | Тофаларский | 134 | yes | ru | TBD | TBD | TBD | TBD |
| 60 | Touva (Soyot) | Тувинский | 77 | yes | ru | TBD | TBD | TBD | TBD |
| 61 | Turkmen | Туркменский | 76 | yes | ru | TBD | TBD | TBD | TBD |
| 62 | Udmurt | Удмуртский | 129 | yes | ru | TBD | TBD | TBD | TBD |
| 63 | Uzbek | Узбекский | 81 | yes | ru | TBD | TBD | TBD | TBD |
| 64 | Uighur | Уйгурский | 78 | yes | ru | TBD | TBD | TBD | TBD |
| 65 | Ukrainian | Украинский | 79 | yes | ru | TBD | TBD | TBD | TBD |
| 66 | Ulch | Ульчский | 160 | yes | ru | TBD | TBD | TBD | TBD |
| 67 | Khakass | Хакасский | 110 | yes | ru | TBD | TBD | TBD | TBD |
| 68 | Khanty | Хантыйский | 109 | yes | ru | TBD | TBD | TBD | TBD |
| 69 | Tsakhur | Цахурский | 152 | yes | ru | TBD | TBD | TBD | TBD |
| 70 | Chechen | Чеченский | 14 | yes | ru | TBD | TBD | TBD | TBD |
| 71 | Chuvash | Чувашский | 97 | yes | cv | TBD | TBD | TBD | TBD |
| 72 | Chukchi | Чукотский | 98 | yes | ru | TBD | TBD | TBD | TBD |
| 73 | Shor | Шорский | 133 | yes | ru | TBD | TBD | TBD | TBD |
| 74 | Evenki (Tungus) | Эвенкийский | 102 | yes | ru | TBD | TBD | TBD | TBD |
| 75 | Even (Lamut) | Эвенский | 101 | yes | ru | TBD | TBD | TBD | TBD |
| 76 | Enets | Энецкий | 150 | yes | ru | TBD | TBD | TBD | TBD |
| 77 | Eskimo (Yupik) | Эскимосский | 100 | yes | ru | TBD | TBD | TBD | TBD |
| 78 | Yukagir | Юкагирский | 158 | yes | ru | TBD | TBD | TBD | TBD |
| 79 | Yakut | Якутский | 130 | yes | ru | TBD | TBD | TBD | TBD |

